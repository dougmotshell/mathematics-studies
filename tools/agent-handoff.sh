#!/usr/bin/env bash
# agent-handoff.sh — cria e valida checkpoints de troca de CLI (Claude/Codex/Copilot/Gemini).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SCRIPT_DIR/agent-handoff-template.md"

usage() {
  cat <<'USAGE'
Uso: tools/agent-handoff.sh <init|snapshot|show|status|validate> [caminho] [--force] [--quiet]

Comandos:
  init      cria o arquivo a partir do template, sem sobrescrever um existente
  snapshot  preenche o handoff com o estado real do repositório (sem digitação):
            branch, HEAD, git status/diff, tickets em aberto com a última entrada
            do log, estado do dev-loop, comandos de verificação e medição de contexto
  show      exibe o handoff atual
  status    exibe o handoff e o estado Git
  validate  verifica as seções obrigatórias e o estado Git

Opções:
  --force   snapshot sobrescreve um handoff existente (o anterior vira
            .agent-handoff.prev.md)
  --quiet   sem saída em caso de sucesso (usado pelo hook PreCompact)

O caminho padrão é .agent-handoff.md (gitignored).
USAGE
}

command_name="${1:-}"
if [[ -z "$command_name" || "$command_name" == "-h" || "$command_name" == "--help" ]]; then
  usage; exit 0
fi
shift || true

force=0
quiet=0
handoff_path=".agent-handoff.md"
for arg in "$@"; do
  case "$arg" in
    --force) force=1 ;;
    --quiet) quiet=1 ;;
    -*) echo "Opção desconhecida: $arg" >&2; usage >&2; exit 2 ;;
    *) handoff_path="$arg" ;;
  esac
done

say() { (( quiet )) || echo "$@"; }

case "$handoff_path" in
  /*) handoff="$handoff_path" ;;
  *) handoff="$REPO_ROOT/$handoff_path" ;;
esac

git_q() { git -C "$REPO_ROOT" "$@" 2>/dev/null || true; }

frontmatter_field() { # <arquivo> <campo>
  awk -v key="$2" '
    NR == 1 && $0 == "---" { inside = 1; next }
    inside && $0 == "---" { exit }
    inside && index($0, key ":") == 1 { sub(/^[^:]*:[[:space:]]*/, ""); print; exit }
  ' "$1"
}

last_log_entry() { # <log.md> — última entrada, cabeçalho + até 5 linhas
  [[ -f "$1" ]] || { echo "(sem log.md)"; return; }
  local entry total
  entry="$(awk '/^## \[/ { buf = "" } { buf = buf $0 "\n" } END { printf "%s", buf }' "$1" \
    | grep -v '^[[:space:]]*$' || true)"
  [[ -n "$entry" ]] || { echo "(log sem entradas)"; return; }
  total="$(wc -l <<< "$entry")"
  head -6 <<< "$entry" || true
  (( total > 6 )) && echo "(… entrada truncada; íntegra em $1)"
  return 0
}

# write_snapshot <destino> — estado real do repositório, sem digitação (TCK-0012, crit. 6).
# Emite exatamente as seções exigidas por `validate`.
write_snapshot() {
  local target="$1"
  local branch head_line generated
  branch="$(git_q rev-parse --abbrev-ref HEAD)"; branch="${branch:-(sem git)}"
  head_line="$(git_q log -1 --format='%h %s')"; head_line="${head_line:-(sem commits)}"
  generated="$(date -u '+%Y-%m-%d %H:%M UTC')"

  {
    echo "# Handoff entre CLIs"
    echo
    echo "> Gerado por \`tools/agent-handoff.sh snapshot\` em $generated —"
    echo "> estado mecânico do repositório. As seções marcadas com \`<preencher>\` exigem"
    echo "> intenção humana/do agente: o snapshot não inventa o que não sabe."
    echo
    echo "## Objetivo"
    echo
    echo "<preencher: o que a tarefa deve alcançar, em 1–3 frases.> Tickets em aberto listados"
    echo "em \"Estado atual\"; se a tarefa pertence a um deles, cite \`tickets/TCK-NNNN-<slug>/\`."
    echo
    echo "## Estado atual"
    echo
    echo "**Pronto:**"
    echo
    echo "- Branch \`$branch\` · HEAD \`$head_line\`"
    local dirty
    dirty="$(git_q status --short)"
    if [[ -n "$dirty" ]]; then
      echo "- Working tree com alterações não commitadas (tabela abaixo). Nada foi commitado."
    else
      echo "- Working tree limpo."
    fi
    echo
    echo "**Tickets com status diferente de \`done\`:**"
    echo
    local found=0 ticket id title status owner
    for ticket in "$REPO_ROOT"/tickets/TCK-*/ticket.md; do
      [[ -f "$ticket" ]] || continue
      status="$(frontmatter_field "$ticket" status)"
      [[ "$status" == "done" ]] && continue
      found=1
      id="$(frontmatter_field "$ticket" id)"
      title="$(frontmatter_field "$ticket" title)"
      owner="$(frontmatter_field "$ticket" owner)"
      echo "- **${id:-?}** — ${title:-(sem título)} · status \`${status:-?}\` · owner \`${owner:-?}\`"
      echo "  - última entrada do log:"
      last_log_entry "$(dirname "$ticket")/log.md" | sed 's/^/    > /'
    done
    (( found )) || echo "- (nenhum)"
    echo
    echo "**dev-loop ativo:**"
    echo
    local loop found_loop=0
    for loop in "$REPO_ROOT"/.dev-loop/*/loop.md; do
      [[ -f "$loop" ]] || continue
      found_loop=1
      echo "- \`.dev-loop/$(basename "$(dirname "$loop")")/loop.md\`"
      grep -E '^- \*\*(Cadeia|Iteração|Status):' "$loop" | sed 's/^/  /' || true
      echo "  - briefings: $(ls -1 "$(dirname "$loop")/briefings" 2>/dev/null | tr '\n' ' ')"
    done
    (( found_loop )) || echo "- (nenhum)"
    echo
    echo "**Falta:**"
    echo
    echo "- <preencher: o que ainda não está pronto. \"Quase pronto\" não é estado.>"
    echo
    echo "## Arquivos alterados"
    echo
    echo "| Arquivo | O que mudou |"
    echo "|---|---|"
    if [[ -n "$dirty" ]]; then
      local code path
      while IFS= read -r line; do
        [[ -n "$line" ]] || continue
        code="${line:0:2}"
        path="${line:3}"
        echo "| \`$path\` | git status \`$code\` |"
      done <<< "$dirty"
    else
      echo "| (nenhum) | working tree limpo |"
    fi
    echo
    echo '```'
    echo "\$ git diff --stat"
    git_q diff --stat
    echo "\$ git diff --stat --cached"
    git_q diff --stat --cached
    echo '```'
    echo
    echo "## Decisões técnicas"
    echo
    echo "- <preencher: decisão — motivo — alternativa descartada. O snapshot não infere isto;"
    echo "  se houver ADR ou entrada de \`log.md\` que já registre a decisão, cite o caminho.>"
    echo
    echo "## Testes"
    echo
    echo "| Comando | Resultado (saída real) |"
    echo "|---|---|"
    echo "| \`bash scripts/audit-ai-surface.sh\` | <não executado neste snapshot> |"
    echo "| \`bash scripts/audit-content.sh\` | <não executado neste snapshot> |"
    echo "| \`python3 scripts/sync-ai-adapters.py --check\` | <não executado neste snapshot> |"
    echo "| \`bash tools/context-watch-test.sh\` | <não executado neste snapshot> |"
    echo
    echo "<Rodar antes de entregar e substituir por saída real; \"não executado\" é resposta"
    echo "válida, omitir não é.>"
    echo
    echo "## Problemas ou riscos"
    echo
    echo "- Contexto da sessão no momento do snapshot:"
    local ctx
    ctx="$(python3 "$SCRIPT_DIR/context-watch.py" --json --cwd "$REPO_ROOT" 2>/dev/null || true)"
    if [[ -n "$ctx" ]]; then
      echo "  \`$ctx\`"
    else
      echo "  (sem telemetria de contexto nesta ferramenta — ver docs/ai/cross-agent-handoff.md)"
    fi
    echo "- <preencher: o que pode morder o próximo agente.>"
    echo
    echo "## Próxima ação exata"
    echo
    echo "<preencher: uma instrução inequívoca — o quê, em qual arquivo, com qual critério de"
    echo "pronto. Se pertence a um ticket, cite \`tickets/TCK-NNNN-<slug>/log.md\`.>"
    echo
    echo "## Restrições"
    echo
    echo "- Não fazer commit, push ou stash sem pedido explícito do usuário."
    echo "- Apenas um agente edita o working tree por vez."
    echo "- Não reverter trabalho alheio presente no working tree."
    echo "- <outras restrições específicas desta tarefa>"
    echo
    echo "## Última atualização"
    echo
    echo "- **Data:** $generated"
    echo "- **CLI/agente:** ${AGENT_HANDOFF_CLI:-Claude Code} — ${AGENT_HANDOFF_ROLE:-<papel assumido>}"
    echo "- **Origem:** \`tools/agent-handoff.sh snapshot\`"
  } > "$target"
}

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
  snapshot)
    if [[ -e "$handoff" && $force -eq 0 ]]; then
      echo "Handoff já existe; use --force para sobrescrever: $handoff" >&2
      exit 2
    fi
    mkdir -p "$(dirname "$handoff")"
    if [[ -e "$handoff" ]]; then
      cp "$handoff" "${handoff%.md}.prev.md" 2>/dev/null || true
    fi
    write_snapshot "$handoff"
    say "Snapshot escrito: $handoff"
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
