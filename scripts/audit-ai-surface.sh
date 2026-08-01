#!/usr/bin/env bash
# audit-ai-surface.sh — inventário e paridade da superfície de IA nos quatro CLIs.
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

printf '%s\n' 'AI surface audit — mathematics-studies' '======================================'

printf '\n%s\n' 'Claude agents:'
find .claude/agents -maxdepth 1 -type f -name '*.md' -printf '  %f\n' | sort

printf '\n%s\n' 'Claude skills:'
find .claude/skills -mindepth 2 -maxdepth 2 -name SKILL.md -printf '%h\n' \
  | sed 's#^.claude/skills/#  #' | sort

printf '\n%s\n' 'Claude workflows:'
find .claude/workflows -maxdepth 1 -type f -name '*.js' -printf '  %f\n' 2>/dev/null | sort

printf '\n%s\n' 'Copilot prompts:'
find .github/prompts -maxdepth 1 -type f -name '*.prompt.md' -printf '  %f\n' 2>/dev/null | sort

printf '\n%s\n' 'Copilot chat modes:'
find .github/chatmodes -maxdepth 1 -type f -name '*.chatmode.md' -printf '  %f\n' 2>/dev/null | sort

printf '\n%s\n' 'Gemini commands:'
find .gemini/commands -type f -name '*.toml' -printf '  %P\n' 2>/dev/null | sort

printf '\n%s\n' 'Arquivos canônicos:'
for file in \
  AGENTS.md \
  CLAUDE.md \
  GEMINI.md \
  SLASH_COMMANDS.md \
  .codex/README.md \
  .github/copilot-instructions.md \
  docs/ai/ticket-protocol.md \
  docs/ai/cross-agent-handoff.md \
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
  scripts/sync-slash-commands.py \
  scripts/audit-content.py \
  scripts/audit-content.sh \
  tools/dev-loop.sh \
  tools/agent-handoff.sh \
  tools/agent-handoff-template.md \
  .claude/skills/dev-loop/references/briefing-template.md; do
  check_file "$file"
done

printf '\n%s\n' 'Paridade por agent (chatmode + command + gemini + memória):'
for agent_file in .claude/agents/*.md; do
  name="$(basename "$agent_file" .md)"
  check_file ".github/chatmodes/$name.chatmode.md"
  check_file ".claude/commands/$name.md"
  check_file ".gemini/commands/agent/$name.toml"
  check_file "memory/agents/$name.md"
done

printf '\n%s\n' 'Paridade por skill (prompt Copilot + command Gemini):'
for skill_file in .claude/skills/*/SKILL.md; do
  name="$(basename "$(dirname "$skill_file")")"
  check_file ".github/prompts/$name.prompt.md"
  check_file ".gemini/commands/$name.toml"
done

printf '\n%s\n' 'Adapters gerados atualizados (sync-slash-commands.py --check):'
if python3 scripts/sync-slash-commands.py --check >/dev/null 2>&1; then
  printf '  up-to-date\n'
else
  printf '  OUTDATED — rode: python3 scripts/sync-slash-commands.py\n'
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
