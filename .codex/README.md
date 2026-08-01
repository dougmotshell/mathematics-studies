# OpenAI Codex — Notas de uso neste repositório

O Codex (CLI, IDE e cloud) lê automaticamente o **`AGENTS.md`** na raiz — ele é a fonte
única de instruções do projeto e cobre visão do produto, convenções de idioma (incluindo o
bilinguismo obrigatório do conteúdo), taxonomia de conteúdo, memória, auto-aprendizado,
registro de erros e padrões de documentação (C4, ADR, SDD).

## Como espelhar as capacidades no Codex

- **Prompts customizados** são configurados por usuário em `~/.codex/prompts/*.md` (não por
  repositório). Para replicar toda a superfície deste projeto, rode:

  ```bash
  python3 scripts/sync-ai-adapters.py --codex
  ```

  Isso instala no `$CODEX_HOME/prompts` um prompt para cada skill (`.claude/skills/`) e para
  cada agent (`.claude/agents/`), embutindo o caminho absoluto deste repositório. Os
  arquivos gerados carregam o marcador `managed-by:mathematics-studies` — prompts pessoais
  não são tocados.

- **Workflows longos**: decompor via Spec-Driven Development (`docs/specs/`, fluxo
  spec → plan → tasks) e executar as tasks incrementalmente.

- **Loop entre agents**: sem tool de subagente, o `/dev-loop` roda assistido —
  `tools/dev-loop.sh next <task-slug>` informa a próxima etapa e o agente correspondente;
  cole o conteúdo de `.claude/agents/<name>.md` como instrução do papel e mantenha os
  briefings em `.dev-loop/<task-slug>/briefings/` como único contrato entre etapas.

- **Tickets**: todo desenvolvimento passa por `tickets/TCK-NNNN-<slug>/` — leia
  `docs/ai/ticket-protocol.md` e `tickets/README.md`. Os prompts `/ticket`, `/handoff` e
  `/ticket-loop` são instalados pelo passo `--codex`. Sem tool de subagente, execute os
  papéis em sequência, registrando cada etapa no `log.md` com `[SEQ]` incremental.

- **Handoff entre CLIs**: `tools/agent-handoff.sh init` / `validate`, com o procedimento em
  `docs/ai/cross-agent-handoff.md`.

- **Auditorias determinísticas**: `scripts/audit-ai-surface.sh` (inventário e paridade de
  skills/agents/prompts/commands) e `scripts/audit-content.sh` (estrutura da taxonomia,
  paridade de idiomas, schema dos exercícios, ciclos de pré-requisito).

- **Memória**: o Codex não tem memória persistente própria — usar a memória compartilhada do
  repositório (`memory/`), conforme a seção 5 do AGENTS.md. Ao assumir um papel `agent:`,
  ler e atualizar `memory/agents/<name>.md`.

- **Documentação visual**: ao produzir docs sobre fluxos, dependências, hierarquias, ciclos
  ou integrações, incluir uma seção Mermaid com leitura curta e fontes; reservar tabelas
  para contratos e inventários.

## Lembretes específicos do domínio

1. Todo objeto de aprendizagem é bilíngue **pt-BR + en-US** — sem fallback parcial.
2. Slugs de `content/` são URLs públicas: não renomear sem ADR + redirect.
3. Gabarito só depois de verificação (`.claude/skills/math-verify/SKILL.md`).
4. Fontes externas apenas gratuitas, com licença registrada em `references.json`.
5. Não fazer commit/push sem solicitação explícita.
