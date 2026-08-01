#!/usr/bin/env bash
# dev-loop.sh — workspace e validação do loop de desenvolvimento entre agents.
# Contrato completo em .claude/skills/dev-loop/SKILL.md.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOOP_ROOT="$REPO_ROOT/.dev-loop"
DEFAULT_CHAIN="route,plan,execute,review,curate"
MAX_BRIEFING_LINES=40

usage() {
  cat <<'USAGE'
Uso: tools/dev-loop.sh <init|status|next|validate> [argumentos]

Comandos:
  init <task-slug> [cadeia]   cria .dev-loop/<task-slug>/ com loop.md e briefings/
                              (cadeia default: route,plan,execute,review,curate)
  status <task-slug>          exibe loop.md e os briefings existentes
  next <task-slug>            informa a próxima etapa/agente a partir dos briefings
  validate <briefing.md>      verifica seções obrigatórias e o limite de linhas
USAGE
}

cmd="${1:-}"
[[ -z "$cmd" || "$cmd" == "-h" || "$cmd" == "--help" ]] && { usage; exit 0; }

case "$cmd" in
  init)
    slug="${2:?informe o task-slug}"
    chain="${3:-$DEFAULT_CHAIN}"
    dir="$LOOP_ROOT/$slug"
    if [[ -e "$dir/loop.md" ]]; then
      echo "Loop já existe; nada foi sobrescrito: $dir/loop.md" >&2
      exit 2
    fi
    mkdir -p "$dir/briefings"
    cat > "$dir/loop.md" <<LOOP
# dev-loop: $slug

- **Cadeia:** $chain
- **Iteração:** 1/3
- **Status:** active
- **Criado em:** $(date +%F)

Briefings em briefings/NN-<etapa>.md — cada um é a única entrada da etapa seguinte
(contrato: .claude/skills/dev-loop/SKILL.md).
LOOP
    echo "Loop criado: $dir"
    ;;
  status)
    slug="${2:?informe o task-slug}"
    dir="$LOOP_ROOT/$slug"
    [[ -f "$dir/loop.md" ]] || { echo "Loop não encontrado: $dir" >&2; exit 1; }
    cat "$dir/loop.md"
    echo
    echo "--- briefings ---"
    ls -1 "$dir/briefings" 2>/dev/null || echo "(nenhum)"
    ;;
  next)
    slug="${2:?informe o task-slug}"
    dir="$LOOP_ROOT/$slug"
    [[ -f "$dir/loop.md" ]] || { echo "Loop não encontrado: $dir" >&2; exit 1; }
    chain="$(sed -n 's/^- \*\*Cadeia:\*\* //p' "$dir/loop.md")"
    IFS=',' read -r -a stages <<< "$chain"
    last="$(ls -1 "$dir/briefings" 2>/dev/null | sort | tail -n 1 || true)"
    if [[ -z "$last" ]]; then
      echo "Próxima etapa: ${stages[0]} (nenhum briefing ainda)"
      exit 0
    fi
    last_stage="$(basename "$last" .md | sed 's/^[0-9]*-//')"
    echo "Último briefing: $last (etapa: $last_stage)"
    if [[ "$last_stage" == "review" ]] && grep -qi 'ajustes' "$dir/briefings/$last"; then
      echo "Próxima etapa: execute (veredito: ajustes — incrementar iteração em loop.md)"
      exit 0
    fi
    next_stage=""
    for i in "${!stages[@]}"; do
      if [[ "${stages[$i]}" == "$last_stage" && $((i + 1)) -lt ${#stages[@]} ]]; then
        next_stage="${stages[$((i + 1))]}"
      fi
    done
    if [[ -n "$next_stage" ]]; then
      echo "Próxima etapa: $next_stage"
    else
      echo "Cadeia concluída (ou etapa fora da cadeia) — verificar loop.md"
    fi
    ;;
  validate)
    briefing="${2:?informe o caminho do briefing}"
    [[ -f "$briefing" ]] || { echo "ERRO: briefing não encontrado: $briefing" >&2; exit 1; }
    failed=0
    for heading in \
      "## Resultado desta etapa" \
      "## Decisões tomadas" \
      "## Arquivos relevantes" \
      "## Próxima ação exata" \
      "## Critério de pronto"; do
      if ! grep -qF "$heading" "$briefing"; then
        echo "ERRO: seção ausente: $heading" >&2
        failed=1
      fi
    done
    lines="$(grep -vc '^[[:space:]]*$' "$briefing" || true)"
    if (( lines > MAX_BRIEFING_LINES + 15 )); then
      echo "ERRO: briefing longo demais ($lines linhas não vazias; alvo ≤ $MAX_BRIEFING_LINES)" >&2
      failed=1
    fi
    (( failed )) && exit 1
    echo "Briefing válido: $briefing ($lines linhas não vazias)"
    ;;
  *)
    echo "Comando desconhecido: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac
