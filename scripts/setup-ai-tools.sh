#!/usr/bin/env bash
# setup-ai-tools.sh — prepara o repositório para todas as ferramentas de IA suportadas.
# Gera os adapters e imprime o que cada ferramenta precisa. Matriz completa:
# docs/ai/tool-support.md
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

WITH_CODEX=0
CODEX_PREFIX=""

usage() {
  cat <<'USAGE'
Uso: bash scripts/setup-ai-tools.sh [opções]

Opções:
  --codex                instala também os prompts globais do Codex
  --codex-prefix <p>     prefixa os prompts do Codex (evita colisão entre repositórios)
  -h, --help             esta ajuda

Sem opções, gera apenas os adapters versionados no repositório (Claude, Copilot, Gemini,
Cursor, Antigravity, Windsurf, Zed, Cline, Junie).
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --codex) WITH_CODEX=1; shift ;;
    --codex-prefix) CODEX_PREFIX="${2:?informe o prefixo}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; usage >&2; exit 2 ;;
  esac
done

echo "==> Gerando adapters a partir das fontes canônicas"
args=()
(( WITH_CODEX )) && args+=(--codex)
[[ -n "$CODEX_PREFIX" ]] && args+=(--codex-prefix "$CODEX_PREFIX")
python3 scripts/sync-ai-adapters.py "${args[@]}"

echo
echo "==> Auditoria da superfície de IA"
bash scripts/audit-ai-surface.sh >/dev/null && echo "  OK" || {
  echo "  FALHAS — rode 'bash scripts/audit-ai-surface.sh' para ver os detalhes" >&2
  exit 1
}

cat <<'GUIDE'

==> Pronto. O que cada ferramenta precisa agora:

  Claude Code ....... nada. `claude` na raiz do repo.
  Grok CLI .......... nada. Lê AGENTS.md, CLAUDE.md e .claude/ (skills e agents).
  Cursor ............ nada. Regras em .cursor/rules, comandos em .cursor/commands.
  GitHub Copilot .... nada. Instruções, prompts e chat modes em .github/.
  Gemini CLI ........ nada. GEMINI.md + comandos em .gemini/commands.
  Windsurf .......... nada. Regras e workflows em .windsurf/.
  Antigravity ....... escolha o modo de ativação das regras de .agents/rules na UI
                      (a sugestão está no comentário do topo de cada arquivo).
  Zed / Cline / Junie  nada. Regras em .rules, .clinerules e .junie/guidelines.md.
  ChatGPT, Grok web,   cole prompts/bootstrap-session.md no início da conversa
  Claude web ........  (ou prompts/assume-agent-role.md para assumir um papel).

  Codex ............. os prompts são GLOBAIS por usuário ($CODEX_HOME/prompts).
                      Rode com --codex. Se você usa o Codex em outros repositórios,
                      prefira isolar ou prefixar:

                        export CODEX_HOME="$HOME/.codex-mathematics-studies"
                        bash scripts/setup-ai-tools.sh --codex

                        # ou, para conviver no mesmo CODEX_HOME:
                        bash scripts/setup-ai-tools.sh --codex --codex-prefix ms

  Detalhes e limitações por ferramenta: docs/ai/tool-support.md
GUIDE
