#!/usr/bin/env python3
"""Chave de licença do plano pago no pacote local (memória do show). Stdlib.

O que o servidor do PodFácil já serve (pauta em 3 troncos, os 7 modos de roteiro, coleta do X) nem
vem neste pacote: aquele gate é real. Este aqui cobre o que só pode rodar no computador do usuário,
porque os dados são dele: confere a chave contra o servidor (tool MCP `licenca_status`).

  python3 scripts/licenca.py configurar   lê a chave sem eco e grava em ~/.podfacil/licenca (permissão 600)
  python3 scripts/licenca.py status       confere a chave agora (sai 0 = plano pago ativo)

Chave: env PODFACIL_LICENSE_KEY ou ~/.podfacil/licenca. Dispositivo: env PODFACIL_DEVICE_ID ou
~/.podfacil/dispositivo (criado na 1ª vez); use o MESMO valor no X-Device-Id do conector MCP, senão o
plano conta dois dispositivos. Pasta: env PODFACIL_HOME (padrão ~/.podfacil).

Cache: resultado positivo vale REVALIDAR_H sem nova consulta e até OFFLINE_H se o servidor não
responder (funciona offline por pouco tempo). Recusa explícita do servidor nunca usa o cache.

ponytail: este gate é contornável por quem editar o código aberto (Apache-2.0); o gate real é o do
servidor. Se a fraude passar a importar, mover o recurso para uma tool do MCP.
"""
import argparse
import getpass
import hashlib
import json
import os
import secrets
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import produto  # noqa: E402

TIMEOUT_S = 15
LICENCA_ARQ, DISPOSITIVO_ARQ, CACHE_ARQ = "licenca", "dispositivo", "licenca-cache.json"
COMO_CONFIGURAR = ("Já tem a chave? Rode `python3 scripts/licenca.py configurar` (grava em ~/.podfacil/licenca,"
                   " permissão 600) ou exporte PODFACIL_LICENSE_KEY.")


class LicencaNegada(SystemExit):
    """Recurso pago sem licença válida: a mensagem (pt-BR) já diz o que fazer."""


class Indisponivel(Exception):
    """Servidor não respondeu de forma conclusiva (rede, tempo, 5xx, 429)."""


def home(env=None):
    env = os.environ if env is None else env
    return Path(env.get("PODFACIL_HOME") or Path.home() / ".podfacil")


def write_private(path, text):
    """Arquivo só do dono (600), criado já com a permissão: a chave nunca fica legível por outros."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(path, 0o600)


def read_key(env=None):
    env = os.environ if env is None else env
    if (env.get("PODFACIL_LICENSE_KEY") or "").strip():
        return env["PODFACIL_LICENSE_KEY"].strip()
    path = home(env) / LICENCA_ARQ
    if not path.is_file():
        return None
    if path.stat().st_mode & 0o077:
        print(f"AVISO: {path} legível por outros usuários; rode `chmod 600 {path}`", file=sys.stderr)
    return path.read_text(encoding="utf-8").strip() or None


def device_id(env=None):
    """X-Device-Id estável deste computador (o plano conta dispositivos por ele)."""
    env = os.environ if env is None else env
    if (env.get("PODFACIL_DEVICE_ID") or "").strip():
        return env["PODFACIL_DEVICE_ID"].strip()[:128]
    path = home(env) / DISPOSITIVO_ARQ
    if path.is_file() and path.read_text(encoding="utf-8").strip():
        return path.read_text(encoding="utf-8").strip()[:128]
    value = "dev_" + secrets.token_hex(8)
    write_private(path, value + "\n")
    return value


# ── servidor ──────────────────────────────────────────────────────────────

def http_post(url, body, headers):
    """(status, bytes) com User-Agent e timeout. headers leva a chave: nunca entra em erro nem log."""
    req = urllib.request.Request(url, data=body, method="POST", headers={"User-Agent": produto.USER_AGENT, **headers})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise Indisponivel(f"rede falhou em {url}: {exc} | esperado resposta em {TIMEOUT_S}s") from exc


def ask_server(key, device, post=http_post):
    """Resposta da tool licenca_status: {"result": {...}} ou {"error": código, "message": texto}."""
    rpc = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "licenca_status", "arguments": {}}}
    headers = {"Content-Type": "application/json", "Accept": "application/json",
               "Authorization": "Bearer " + key, "X-Device-Id": device}
    status, body = post(produto.SERVER_URL, json.dumps(rpc).encode("utf-8"), headers)
    if status == 401:
        return {"error": "license_unknown", "message": "chave de licença não reconhecida pelo servidor"}
    if status != 200:
        raise Indisponivel(f"servidor respondeu HTTP {status}: {body[:200]!r} | esperado 200")
    try:
        result = json.loads(body)["result"]
    except (ValueError, KeyError, TypeError) as exc:
        raise Indisponivel(f"resposta fora do formato JSON-RPC: {body[:200]!r} | esperado {{result: ...}}") from exc
    return result.get("structuredContent") or {}


# ── cache (só resultado positivo) ─────────────────────────────────────────

def key_hash(key):
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def read_cache(key, env=None):
    path = home(env) / CACHE_ARQ
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        return doc if doc.get("chave") == key_hash(key) else None
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        print(f"AVISO: cache de licença ilegível em {path} ({exc}); ignorado", file=sys.stderr)
        return None


def cache_age_h(doc, now):
    return (now - datetime.fromisoformat(doc["confirmado_em"])).total_seconds() / 3600


def save_cache(key, plan, now, env=None):
    doc = {"chave": key_hash(key), "plano": plan, "confirmado_em": now.isoformat(timespec="seconds")}
    write_private(home(env) / CACHE_ARQ, json.dumps(doc) + "\n")


# ── decisão ───────────────────────────────────────────────────────────────

def negada(recurso, motivo):
    return LicencaNegada(f"O recurso '{recurso}' é do plano pago do PodFácil: {motivo}.\n"
                         f"Planos e assinatura: {produto.PRICING_URL}\n{COMO_CONFIGURAR}")


def judge(recurso, answer):
    """Resposta do servidor -> plano pago (str) ou LicencaNegada."""
    if answer.get("error"):
        raise negada(recurso, answer.get("message") or answer["error"])
    info = answer.get("result") or {}
    if info.get("tier") != "paid":
        raise negada(recurso, f"a chave está no plano {info.get('plan') or 'free'} (assinatura ou teste vencido?)")
    return info.get("plan") or "paid"


def exigir(recurso, env=None, post=http_post, now=None):
    """Plano pago ativo -> nome do plano. Sem chave, chave recusada ou servidor fora sem cache -> LicencaNegada."""
    now = now or datetime.now(timezone.utc)
    key = read_key(env)
    if not key:
        raise negada(recurso, "nenhuma chave de licença configurada neste computador")
    cached = read_cache(key, env)
    if cached and cache_age_h(cached, now) < produto.REVALIDAR_H:
        return cached["plano"]
    try:
        plan = judge(recurso, ask_server(key, device_id(env), post))
    except Indisponivel as exc:
        if cached and cache_age_h(cached, now) < produto.OFFLINE_H:
            print(f"AVISO: servidor do PodFácil sem resposta ({exc}); usando a confirmação de"
                  f" {cached['confirmado_em']} (vale {produto.OFFLINE_H:.0f} h)", file=sys.stderr)
            return cached["plano"]
        raise negada(recurso, f"não consegui confirmar a licença agora ({exc}); tente de novo em alguns minutos") from exc
    save_cache(key, plan, now, env)
    return plan


# ── CLI ───────────────────────────────────────────────────────────────────

def cmd_configurar(_args):
    key = getpass.getpass("Cole a chave de licença do PodFácil (não aparece na tela): ").strip()
    if not key:
        print("nenhuma chave digitada | esperado a chave do e-mail de compra", file=sys.stderr)
        return 2
    write_private(home() / LICENCA_ARQ, key + "\n")
    print(f"chave gravada em {home() / LICENCA_ARQ} (permissão 600). Dispositivo deste computador:"
          f" {device_id()} (use o mesmo valor no header X-Device-Id do conector MCP).")
    return cmd_status(_args)


def cmd_status(_args):
    try:
        plan = exigir("licenca")
    except LicencaNegada as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"licença ativa: plano {plan} · servidor {produto.SERVER_URL} · dispositivo {device_id()}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("configurar")
    sub.add_parser("status")
    args = parser.parse_args(argv)
    return {"configurar": cmd_configurar, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
