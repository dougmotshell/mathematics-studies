#!/usr/bin/env bash
# agent-handoff.sh — cria e valida checkpoints de troca de CLI (Claude/Codex/Copilot/Gemini).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SCRIPT_DIR/agent-handoff-template.md"

usage() {
  cat <<'USAGE'
Uso: tools/agent-handoff.sh <init|show|status|validate> [caminho]

Comandos:
  init      cria o arquivo sem sobrescrever um existente
  show      exibe o handoff atual
  status    exibe o handoff e o estado Git
  validate  verifica as seções obrigatórias e o estado Git

O caminho padrão é .agent-handoff.md (gitignored).
USAGE
}

command_name="${1:-}"
handoff_path="${2:-.agent-handoff.md}"
if [[ -z "$command_name" || "$command_name" == "-h" || "$command_name" == "--help" ]]; then
  usage; exit 0
fi

case "$handoff_path" in
  /*) handoff="$handoff_path" ;;
  *) handoff="$REPO_ROOT/$handoff_path" ;;
esac

case "$command_name" in
  init)
    [[ -f "$TEMPLATE" ]] || { echo "Template não encontrado: $TEMPLATE" >&2; exit 1; }
    if [[ -e "$handoff" ]]; then
      echo "Arquivo já existe; nada foi sobrescrito: $handoff" >&2
      exit 2
    fi
    mkdir -p "$(dirname "$handoff")"
    cp "$TEMPLATE" "$handoff"
    echo "Handoff criado: $handoff"
    ;;
  show)
    [[ -f "$handoff" ]] || { echo "Handoff não encontrado: $handoff" >&2; exit 1; }
    cat "$handoff"
    ;;
  status)
    if [[ -f "$handoff" ]]; then cat "$handoff"; else echo "Handoff não encontrado: $handoff"; fi
    echo
    echo "--- git status --short ---"
    git -C "$REPO_ROOT" status --short
    ;;
  validate)
    [[ -f "$handoff" ]] || { echo "ERRO: handoff não encontrado: $handoff" >&2; exit 1; }
    failed=0
    for heading in \
      "## Objetivo" \
      "## Estado atual" \
      "## Arquivos alterados" \
      "## Decisões técnicas" \
      "## Testes" \
      "## Problemas ou riscos" \
      "## Próxima ação exata" \
      "## Restrições" \
      "## Última atualização"; do
      if ! grep -qF "$heading" "$handoff"; then
        echo "ERRO: seção ausente: $heading" >&2
        failed=1
      fi
    done
    (( failed )) && exit 1
    echo "Handoff válido: $handoff"
    echo "--- alterações no working tree ---"
    git -C "$REPO_ROOT" status --short
    ;;
  *)
    echo "Comando desconhecido: $command_name" >&2
    usage >&2
    exit 2
    ;;
esac
