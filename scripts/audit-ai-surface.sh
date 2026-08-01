#!/usr/bin/env bash
# audit-ai-surface.sh — inventário e paridade da superfície de IA em todas as ferramentas.
# Matriz de suporte: docs/ai/tool-support.md
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"
status=0

check_file() {
  if [[ ! -f "$1" ]]; then
    printf 'MISSING\t%s\n' "$1"
    status=1
  fi
}

count() { find "$1" -type f -name "$2" 2>/dev/null | wc -l; }

printf '%s\n' 'AI surface audit — mathematics-studies' '======================================'

printf '\n%s\n' 'Fontes canônicas:'
printf '  agents ....... %s\n' "$(count .claude/agents '*.md')"
printf '  skills ....... %s\n' "$(find .claude/skills -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l)"
printf '  rules ........ %s\n' "$(count .github/instructions '*.instructions.md')"
printf '  workflows .... %s (exclusivos do Claude Code)\n' "$(count .claude/workflows '*.js')"

printf '\n%s\n' 'Adapters gerados:'
printf '  Claude commands ......... %s\n' "$(count .claude/commands '*.md')"
printf '  Copilot prompts ......... %s\n' "$(count .github/prompts '*.prompt.md')"
printf '  Copilot chat modes ...... %s\n' "$(count .github/chatmodes '*.chatmode.md')"
printf '  Gemini commands ......... %s\n' "$(count .gemini/commands '*.toml')"
printf '  Cursor commands ......... %s\n' "$(count .cursor/commands '*.md')"
printf '  Cursor rules ............ %s\n' "$(count .cursor/rules '*.mdc')"
printf '  Antigravity workflows ... %s\n' "$(count .agents/workflows '*.md')"
printf '  Antigravity rules ....... %s\n' "$(count .agents/rules '*.md')"
printf '  Windsurf workflows ...... %s\n' "$(count .windsurf/workflows '*.md')"
printf '  Windsurf rules .......... %s\n' "$(count .windsurf/rules '*.md')"

printf '\n%s\n' 'Arquivos canônicos e ponteiros:'
for file in \
  AGENTS.md \
  CLAUDE.md \
  GEMINI.md \
  SLASH_COMMANDS.md \
  .rules \
  .clinerules \
  .junie/guidelines.md \
  .codex/README.md \
  .github/copilot-instructions.md \
  .github/instructions/core.instructions.md \
  docs/ai/ticket-protocol.md \
  docs/ai/cross-agent-handoff.md \
  docs/ai/tool-support.md \
  prompts/bootstrap-session.md \
  prompts/assume-agent-role.md \
  tickets/README.md \
  tickets/TICKET-TEMPLATE.md; do
  check_file "$file"
done

printf '\n%s\n' 'Padrões e templates:'
for file in \
  docs/DOC-STANDARDS.md \
  docs/adr/adr-template.md \
  docs/adr/README.md \
  docs/errors/error-template.md \
  docs/errors/README.md \
  docs/specs/templates/spec.md \
  docs/specs/templates/plan.md \
  docs/specs/templates/tasks.md \
  docs/content/taxonomy.md \
  docs/content/content-standards.md \
  docs/content/i18n.md \
  docs/content/exercise-schema.md \
  docs/content/accessibility.md; do
  check_file "$file"
done

printf '\n%s\n' 'Memória:'
for file in \
  memory/MEMORY.md \
  memory/LESSONS.md \
  memory/agents/README.md \
  memory/lessons/README.md \
  memory/context/project-context.md; do
  check_file "$file"
done
for area in process frontend backend devops qa security content curriculum; do
  check_file "memory/context/$area.md"
done

printf '\n%s\n' 'Ferramentas:'
for file in \
  scripts/sync-ai-adapters.py \
  scripts/setup-ai-tools.sh \
  scripts/audit-content.py \
  scripts/audit-content.sh \
  tools/dev-loop.sh \
  tools/agent-handoff.sh \
  tools/agent-handoff-template.md \
  .claude/skills/dev-loop/references/briefing-template.md; do
  check_file "$file"
done

printf '\n%s\n' 'Paridade por agent (Claude · Copilot · Gemini · Cursor · Antigravity · Windsurf · memória):'
for agent_file in .claude/agents/*.md; do
  name="$(basename "$agent_file" .md)"
  check_file ".claude/commands/$name.md"
  check_file ".github/chatmodes/$name.chatmode.md"
  check_file ".gemini/commands/agent/$name.toml"
  check_file ".cursor/commands/agent-$name.md"
  check_file ".agents/workflows/agent-$name.md"
  check_file ".windsurf/workflows/agent-$name.md"
  check_file "memory/agents/$name.md"
done

printf '%s\n' 'Paridade por skill (Copilot · Gemini · Cursor · Antigravity · Windsurf):'
for skill_file in .claude/skills/*/SKILL.md; do
  name="$(basename "$(dirname "$skill_file")")"
  check_file ".github/prompts/$name.prompt.md"
  check_file ".gemini/commands/$name.toml"
  check_file ".cursor/commands/$name.md"
  check_file ".agents/workflows/$name.md"
  check_file ".windsurf/workflows/$name.md"
done

printf '%s\n' 'Paridade por regra (Cursor · Windsurf · Antigravity):'
for rule_file in .github/instructions/*.instructions.md; do
  name="$(basename "$rule_file" .instructions.md)"
  check_file ".cursor/rules/$name.mdc"
  check_file ".windsurf/rules/$name.md"
  check_file ".agents/rules/$name.md"
done

printf '\n%s\n' 'Limite de 12.000 caracteres nas regras (Antigravity/Windsurf):'
oversized=0
while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  size="$(wc -c < "$f")"
  if (( size > 12000 )); then
    printf '  OVERSIZED\t%s\t%s chars\n' "$f" "$size"
    oversized=1
    status=1
  fi
done < <(find .cursor/rules .windsurf/rules .agents/rules -type f 2>/dev/null; \
         printf '%s\n' .rules .clinerules .junie/guidelines.md)
(( oversized )) || printf '  todas dentro do limite\n'

printf '\n%s\n' 'Adapters gerados atualizados (sync-ai-adapters.py --check):'
if python3 scripts/sync-ai-adapters.py --check >/dev/null 2>&1; then
  printf '  up-to-date\n'
else
  printf '  OUTDATED — rode: python3 scripts/sync-ai-adapters.py\n'
  status=1
fi

printf '\n%s\n' 'Acesso do Codex documentado:'
if grep -q 'AGENTS.md' .codex/README.md; then
  printf '  documented\n'
else
  printf '  UNDOCUMENTED\n'
  status=1
fi

printf '\n%s\n' "Resultado: $([[ $status -eq 0 ]] && echo OK || echo 'FALHAS ENCONTRADAS')"
exit "$status"
