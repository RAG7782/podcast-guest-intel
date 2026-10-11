#!/usr/bin/env python3
"""Coletores de tendência para a pauta (task *pauta). Stdlib pura.

Subcomandos:
  collect --geo BR [--query Q ...] [--hl pt-BR] [--registry ARQ] [--confirm-batch] [-o SAIDA.json]
      consulta as fontes utilizáveis do registro (keyless habilitadas + BYOK habilitadas com
      credential.status=valid), na ordem de priority, e grava itens normalizados
      [{source, title, url, published_at, signal}] + contador de chamadas.
  verify SOURCE_ID [--registry ARQ]
      chamada mínima à fonte BYOK; imprime {status, verified_at, verification_note}.
      Nunca imprime o valor da chave: só o NOME da variável de ambiente aparece.

Guarda de lote: mais de 20 chamadas de fonte numa execução exige --confirm-batch
(manifesto HPF-3 da pauta). O plano é contado ANTES de disparar a primeira chamada.

Registro: references/contracts/trend-sources.yaml (YAML exige pyyaml; JSON roda só com stdlib).
Tendências do X (BYOK): adaptador em scripts/trends_x.py (plano pago: roda no servidor do PodFácil, fora do pacote), que fica no repositório e no servidor
(plano pago, tool MCP `trends_collect`); o pacote local não o traz, e aqui a fonte X recusa com o caminho.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import TREND_SOURCES as DEFAULT_REGISTRY  # noqa: E402
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
TIMEOUT_S = 15
BATCH_LIMIT = 20
HT_NS = "{https://trends.google.com/trending/rss}"
TRENDS_URL = "https://trends.google.com/trending/rss?geo={geo}"
NEWS_URL = "https://news.google.com/rss/search?q={query}&hl={hl}&gl={geo}&ceid={geo}:{ceid_lang}"
CEID_LANG = {"pt-BR": "pt-419", "pt": "pt-419", "en": "en", "en-US": "en"}


class TrendError(Exception):
    """Falha de coleta. A mensagem traz o valor ofensor e o esperado; nunca traz credencial."""


class BatchGuardError(TrendError):
    """Lote acima de BATCH_LIMIT chamadas sem --confirm-batch."""


# ── orçamento de chamadas ─────────────────────────────────────────────────

class CallBudget:
    """Conta chamadas de fonte; acima de BATCH_LIMIT só com confirmação explícita."""

    def __init__(self, confirmed=False, limit=BATCH_LIMIT):
        self.count, self.confirmed, self.limit = 0, confirmed, limit

    def check_plan(self, planned):
        if planned > self.limit and not self.confirmed:
            raise BatchGuardError(f"lote planejado={planned} chamadas | esperado: <= {self.limit}"
                                  " ou --confirm-batch (aviso ao usuário antes de disparar)")

    def take(self):
        self.check_plan(self.count + 1)
        self.count += 1


# ── HTTP ──────────────────────────────────────────────────────────────────

class SameHostAuthRedirect(urllib.request.HTTPRedirectHandler):
    """Redirect para OUTRO host perde o Authorization: a chave BYOK não vaza para quem redireciona (CRITIC B2)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname:
            new.remove_header("Authorization")
        return new


OPENER = urllib.request.build_opener(SameHostAuthRedirect)


def http_get(url, headers=None, budget=None):
    """GET com timeout e user-agent. headers pode levar Authorization: nunca entra em erro/log."""
    if budget is not None:
        budget.take()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with OPENER.open(req, timeout=TIMEOUT_S) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise TrendError(f"rede falhou em {redact_url(url)}: {exc} | esperado: HTTP 200 em"
                         f" {TIMEOUT_S}s") from exc


def redact_url(url):
    """URL sem query string longa (manchetes de busca podem ser grandes)."""
    return url if len(url) <= 160 else url[:160] + "…"


def expect_200(status, body, url):
    if status != 200:
        raise TrendError(f"HTTP {status} em {redact_url(url)} (corpo {len(body)} bytes)"
                         " | esperado: 200")
    return body


# ── parsing ───────────────────────────────────────────────────────────────

def iso_date(text):
    """RFC 822 (pubDate) ou ISO 8601 -> ISO 8601 UTC; None se ausente/ilegível."""
    if not text:
        return None
    try:
        dt = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    dt = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rss_items(xml_bytes, origin):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        head = xml_bytes[:60]
        raise TrendError(f"XML inválido de {origin}: {exc} | início={head!r}"
                         " | esperado: RSS 2.0 com channel/item") from exc
    return root.findall("./channel/item")


def parse_trends_rss(xml_bytes, source="google_trends_rss"):
    """Google Trends RSS: signal = ht:approx_traffic; url = 1ª matéria (ht:news_item_url)."""
    out = []
    for item in rss_items(xml_bytes, source):
        news_url = item.findtext(f"{HT_NS}news_item/{HT_NS}news_item_url")
        out.append(normalized(source, item.findtext("title"), news_url or item.findtext("link"),
                              item.findtext("pubDate"), item.findtext(f"{HT_NS}approx_traffic")))
    return out


def parse_news_rss(xml_bytes, source="google_news_rss"):
    """Google News RSS: signal = nome do veículo (<source>); o sufixo ' - Veículo' sai do título."""
    out = []
    for item in rss_items(xml_bytes, source):
        title, outlet = item.findtext("title") or "", item.findtext("source") or ""
        if outlet and title.endswith(f" - {outlet}"):
            title = title[: -len(outlet) - 3]
        out.append(normalized(source, title, item.findtext("link"), item.findtext("pubDate"), outlet))
    return out


def normalized(source, title, url, published, signal):
    return {"source": source, "title": " ".join((title or "").split()), "url": url,
            "published_at": iso_date(published), "signal": signal}


# ── coletores keyless ─────────────────────────────────────────────────────

def google_trends_rss(geo, budget=None, fetch=http_get):
    url = TRENDS_URL.format(geo=urllib.parse.quote(geo))
    return parse_trends_rss(expect_200(*fetch(url, None, budget), url))


def google_news_rss(query, hl="pt-BR", gl="BR", budget=None, fetch=http_get):
    q = urllib.parse.quote   # hl/gl podem vir do cliente remoto (MCP): nunca crus na URL (CRITIC B1)
    url = NEWS_URL.format(query=q(query), hl=q(hl), geo=q(gl), ceid_lang=q(CEID_LANG.get(hl, hl.split("-")[0])))
    return parse_news_rss(expect_200(*fetch(url, None, budget), url))


# ── BYOK ──────────────────────────────────────────────────────────────────

def bearer_from_env(source, env=None):
    """Valor resolvido da env nomeada em credential.ref; erro cita só o NOME da variável."""
    env = os.environ if env is None else env
    ref = (source.get("credential") or {}).get("ref") or {}
    if ref.get("store") != "env":
        raise TrendError(f"credential.ref.store={ref.get('store')!r} em {source.get('id')}"
                         " | esperado: 'env' (cofre ainda não suportado pelo adaptador v1)")
    value = env.get(ref.get("name") or "")
    if not value:
        raise TrendError(f"variável {ref.get('name')!r} vazia ou ausente para {source.get('id')}"
                         " | esperado: chave exportada no ambiente (o valor nunca é impresso)")
    return value


X_PAGO = ("a coleta do X (BYOK) é do plano pago e não vem no pacote local | esperado: tool `trends_collect`"
          " do MCP do PodFácil com a chave de licença e a sua chave do X no header X-Byok-X; sem ela, use as"
          " fontes Google Trends/News RSS (fonte x com enabled=false)")


def x_adapter():
    """scripts/trends_x.py (plano pago: roda no servidor do PodFácil, fora do pacote): presente no repo e no servidor; ausente no pacote local (gate real, não um if)."""
    try:
        import trends_x
    except ImportError as exc:
        raise TrendError(X_PAGO) from exc
    return trends_x


def x_recent_search(query, source, budget=None, fetch=http_get, env=None, max_results=10):
    return x_adapter().recent_search(query, source, budget, fetch, env, max_results)


def verify_credential(source, fetch=http_get, env=None, now=None):
    """Chamada mínima; devolve {status, verified_at, verification_note} sem expor o valor."""
    if source.get("id") != "x":
        raise TrendError(f"verify para {source.get('id')!r} não disponível nesta versão"
                         f" | esperado: uma de {AVAILABLE_BYOK} (as demais redes não têm adaptador)")
    return x_adapter().verify_usage(source, fetch, env, now)


def byok_unavailable(name, reason):
    """Mesma interface do x_recent_search; recusa com o motivo (BYOK sem adaptador nesta versão)."""
    def collector(query, source, budget=None, fetch=http_get, env=None):
        raise TrendError(f"tendências de {name!r} não disponíveis nesta versão ({reason}; query={query!r})"
                         f" | esperado: fonte desligada (enabled=false); use {AVAILABLE_BYOK} ou o fallback RSS")
    collector.__name__ = f"{name}_search"
    collector.__doc__ = f"{name}: não disponível nesta versão ({reason})."
    return collector


AVAILABLE_BYOK = ("x",)   # única rede com adaptador; o texto de venda só pode citar estas (DEBT-063)
tiktok_search = byok_unavailable("tiktok", "Research API exclui uso comercial, research/02 §3")
reddit_search = byok_unavailable("reddit", "API grátis só para uso não comercial; OAuth com aprovação manual")
linkedin_search = byok_unavailable("linkedin", "coleta automatizada proibida no User Agreement")
youtube_search = byok_unavailable("youtube", "adaptador da YouTube Data API v3 ainda não escrito")
BYOK_COLLECTORS = {"x": x_recent_search, "tiktok": tiktok_search, "reddit": reddit_search,
                   "linkedin": linkedin_search, "youtube": youtube_search}


# ── registro e coleta ─────────────────────────────────────────────────────

def load_registry(path=DEFAULT_REGISTRY):
    text = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as exc:
            raise TrendError(f"{path} é YAML e pyyaml não está instalado | esperado: registro"
                             " .json ou `uv run --with pyyaml`") from exc
        return yaml.safe_load(text)
    return json.loads(text)


def usable_sources(registry):
    """Keyless habilitadas + BYOK habilitadas com credential.status=valid, por priority."""
    def usable(src):
        if not src.get("enabled"):
            return False
        return src.get("kind") == "keyless" or (src.get("credential") or {}).get("status") == "valid"
    return sorted((s for s in registry.get("sources") or [] if usable(s)), key=lambda s: s["priority"])


def plan_calls(sources, queries):
    """(source, query|None) por chamada. Trends: 1 por geo; News e BYOK: 1 por query."""
    plan = []
    for src in sources:
        if src["id"] == "google_trends_rss":
            plan.append((src, None))
        elif src["id"] == "google_news_rss" or src.get("kind") == "byok":
            plan += [(src, q) for q in queries]
    return plan


def run_call(src, query, args, budget, fetch):
    if src["id"] == "google_trends_rss":
        return google_trends_rss(args.geo, budget, fetch)
    if src["id"] == "google_news_rss":
        return google_news_rss(query, args.hl, args.geo, budget, fetch)
    collector = BYOK_COLLECTORS.get(src["id"])
    if collector is None:
        raise TrendError(f"fonte {src['id']!r} sem coletor | esperado: um de {sorted(BYOK_COLLECTORS)}")
    return collector(query, src, budget, fetch)


def collect_trends(registry, args, fetch=http_get):
    """Executa o plano inteiro; erro de uma chamada vira registro em `erros`, não aborta."""
    plan = plan_calls(usable_sources(registry), args.query or [])
    budget = CallBudget(confirmed=args.confirm_batch)
    budget.check_plan(len(plan))
    items, errors = [], []
    for src, query in plan:
        try:
            items += [dict(it, query=query) if query else it for it in run_call(src, query, args, budget, fetch)]
        except TrendError as exc:
            errors.append({"source": src["id"], "query": query, "erro": str(exc)})
    return {"collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "geo": args.geo, "hl": args.hl, "calls": budget.count, "sources_used": sources_used(plan),
            "erros": errors, "items": items}


def sources_used(plan):
    seen = {}
    for src, _q in plan:
        status = (src.get("credential") or {}).get("status", "n/a")
        seen[src["id"]] = {"source_id": src["id"], "kind": src["kind"], "status": status}
    return list(seen.values())


# ── CLI ───────────────────────────────────────────────────────────────────

def cmd_collect(args):
    try:
        out = collect_trends(load_registry(args.registry), args)
    except BatchGuardError as exc:
        print(f"BLOQUEADO  {exc}", file=sys.stderr)
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    Path(args.output).write_text(text, encoding="utf-8") if args.output else sys.stdout.write(text)
    print(f"collect: chamadas={out['calls']} · itens={len(out['items'])} · erros={len(out['erros'])}",
          file=sys.stderr)
    return 1 if out["erros"] and not out["items"] else 0


def cmd_verify(args):
    registry = load_registry(args.registry)
    source = next((s for s in registry.get("sources") or [] if s.get("id") == args.source_id), None)
    if source is None:
        print(f"fonte {args.source_id!r} não está no registro | esperado: id existente", file=sys.stderr)
        return 2
    print(json.dumps(verify_credential(source), ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    sub = parser.add_subparsers(dest="cmd", required=True)
    col = sub.add_parser("collect")
    col.add_argument("--geo", default="BR")
    col.add_argument("--hl", default="pt-BR")
    col.add_argument("--query", action="append")
    col.add_argument("--confirm-batch", action="store_true", help=f"autoriza lote > {BATCH_LIMIT} chamadas")
    col.add_argument("-o", "--output")
    sub.add_parser("verify").add_argument("source_id")
    args = parser.parse_args(argv)
    try:
        return {"collect": cmd_collect, "verify": cmd_verify}[args.cmd](args)
    except TrendError as exc:
        print(f"FALHA  {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
