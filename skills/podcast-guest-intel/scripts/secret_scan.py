#!/usr/bin/env python3
"""Varre o CONTEÚDO e o NOME dos arquivos alterados num intervalo de commits atrás de segredo (SEC-001).

Uso: python3 scripts/secret_scan.py --base <sha|vazio> [--head HEAD]
  exit 0 = limpo (com denominador > 0) · 1 = segredo encontrado · 2 = erro (git falhou, intervalo vazio)

Por que existe: o job antigo fazia `git diff HEAD~1 2>/dev/null` num checkout raso; o git falhava,
o erro ia para /dev/null e o job dava verde sem olhar nada. Aqui todo erro do git derruba o job e o
denominador (commits e arquivos examinados) sai no log; denominador zero é erro, nunca verde.
ponytail: padrões fixos (sem gitleaks); trocar por gitleaks se aparecer formato de chave fora da lista.
"""
import argparse
import re
import subprocess
import sys

NAME_RE = re.compile(r'(^|/)(\.env(\..+)?|.*\.(pem|key|p12|pfx)|.*credentials[^/]*|id_(rsa|ed25519|ecdsa))$')
CONTENT_RES = [
    re.compile(r'(api_key|password|secret|token)\s*[:=]\s*[A-Za-z0-9/+_-]{8,}', re.I),
    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    re.compile(r'\b(ghp|gho|ghs|github_pat)_[A-Za-z0-9_]{20,}\b'),
    re.compile(r'\bsk-(live|ant|proj)?[A-Za-z0-9_-]{20,}\b'),
]
NULL_SHA = '0' * 40


def git(*args):
    """Roda git; qualquer código != 0 vira SystemExit(2) com o comando e o stderr (nunca some)."""
    p = subprocess.run(['git', *args], capture_output=True, text=True)
    if p.returncode != 0:
        print(f'::error::git {" ".join(args)} falhou ({p.returncode}): {p.stderr.strip()}', file=sys.stderr)
        raise SystemExit(2)
    return p.stdout


def resolve_base(base):
    if base and base != NULL_SHA:
        return base
    return 'HEAD~1'   # push sem "before" (branch nova): ao menos o último commit; checkout raso → erro, não verde


def scan(base, head):
    base = resolve_base(base)
    commits = [c for c in git('rev-list', f'{base}..{head}').split() if c]
    files = [f for f in git('diff', '--name-only', '--diff-filter=ACMR', base, head).splitlines() if f]
    print(f'secret_scan: intervalo {base}..{head} · commits examinados={len(commits)} · arquivos examinados={len(files)}')
    if not commits:
        print('::error::nenhum commit no intervalo; esperado >= 1 (denominador zero não é verde)', file=sys.stderr)
        return 2
    hits = [f'nome   {f}' for f in files if NAME_RE.search(f)]
    current = None
    for line in git('diff', '-U0', '--no-color', base, head).splitlines():
        if line.startswith('+++ '):
            current = line[6:] if line.startswith('+++ b/') else line[4:]
        elif line.startswith('+') and any(r.search(line) for r in CONTENT_RES):
            hits.append(f'conteúdo {current}: {line[1:80]}…')   # trecho curto: o log não vira o vazamento
    if hits:
        print(f'::error::{len(hits)} possível(is) segredo(s):', file=sys.stderr)
        for h in hits:
            print('  ' + h, file=sys.stderr)
        return 1
    print('OK: 0 segredos em nome ou conteúdo')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--base', default='')
    ap.add_argument('--head', default='HEAD')
    a = ap.parse_args(argv)
    return scan(a.base, a.head)


if __name__ == '__main__':
    sys.exit(main())
