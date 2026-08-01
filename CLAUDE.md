# CLAUDE.md — Adaptador para Claude Code

@AGENTS.md

## Específico do Claude Code

- **Subagentes** (`.claude/agents/`), com escopo exclusivo:
  - *fluxo de desenvolvimento*: `tech-lead`, `product-analyst`, `platform-architect`,
    `ui-ux-designer`, `frontend-developer`, `backend-developer`, `devops-engineer`,
    `code-reviewer`, `qa-validator`, `security-auditor`, `docs-writer`;
  - *conteúdo e currículo*: `curriculum-architect`, `content-author`, `math-reviewer`,
    `exercise-designer`, `i18n-steward`, `a11y-ux-reviewer`, `learning-analytics`,
    `researcher`;
  - *suporte ao loop*: `task-router`, `retrospective-curator`.
- **Skills locais** (`.claude/skills/`): `/ticket`, `/ticket-loop`, `/handoff`, `/dev-loop`,
  `/agent-handoff`, `/create-adr`, `/create-spec`, `/spec-review`, `/c4-diagram`,
  `/log-error`, `/capture-lesson`, `/generate-project-context`, `/new-topic`,
  `/new-exercise-set`, `/learning-path`, `/math-verify`, `/content-audit`, `/i18n-parity`,
  `/a11y-audit`, `/pwa-audit`.
- **Tickets e loop de desenvolvimento**: `/ticket <descrição>` cria o ticket, faz a triagem
  com o `tech-lead` e **entra automaticamente** no `/ticket-loop` (execução → code review →
  QA), parando só em `done`, `blocked: human-input` ou escalada por 3 loops. Ao invocar
  subagentes, respeite a independência de cadeia: **quem produziu não revisa nem valida**.
  Contrato: `docs/ai/ticket-protocol.md`.
- **Workflows** (`.claude/workflows/`): `content-review`, `curriculum-audit`,
  `ai-surface-audit`, `feature-plan-review`, `research-sweep`. Invocar via tool `Workflow`
  (ex.: `{name: "content-review"}`) **somente quando o usuário pedir orquestração
  multi-agente**.
- **Agents como slash commands**: todo agent também é acessível como `/agente <tarefa>`
  (ex.: `/math-reviewer`, `/content-author`) — comandos gerados em `.claude/commands/` por
  `scripts/sync-slash-commands.py`. **Não editar os gerados à mão.**
- **MCPs úteis neste projeto** (quando configurados): `chrome-devtools` para `/pwa-audit` e
  verificação visual da aplicação; Figma para design. Sem o MCP, usar o fallback documentado
  na skill.
- **Memória do projeto**: além da memória interna do Claude Code, manter a memória
  compartilhada do repositório em `memory/` (seção 5 do AGENTS.md) — ela é lida também por
  Codex, Copilot e Gemini. Cada agent mantém a própria memória em `memory/agents/<name>.md`;
  lições são indexadas em `memory/LESSONS.md`.

## Ao encerrar tarefas significativas

Seguir o protocolo de auto-aprendizado do AGENTS.md (seções 5–7): atualizar `memory/`,
registrar erros em `docs/errors/` e lições em `memory/lessons/`.
