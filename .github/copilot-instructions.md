# Instruções do GitHub Copilot para este repositório

> Fonte única de instruções: **`AGENTS.md`** na raiz. Leia-o antes de qualquer tarefa. Este
> arquivo apenas resume o essencial e aponta os recursos específicos do Copilot.

## Regras essenciais (resumo do AGENTS.md)

- **Projeto**: plataforma gratuita de estudos de matemática (educação infantil → pesquisa),
  web PWA com deploy na Vercel, conteúdo bilíngue pt-BR/en-US, exercícios interativos com
  feedback e acompanhamento de progresso.
- **Idioma — repositório**: nomes de arquivos/pastas/identificadores em **en-US**;
  documentação e comentários em **pt-BR**.
- **Idioma — produto**: todo objeto de aprendizagem existe em **pt-BR e en-US**, em paridade.
  Nunca publicar conteúdo monolíngue (AGENTS.md §2b).
- **Taxonomia**: `content/<stage>/<area>/<topic>/[<subtopic>]` — estágios `early-childhood`,
  `elementary`, `middle-school`, `high-school`, `undergraduate`, `graduate`, `research`.
  Slugs são URLs públicas: não renomear sem ADR.
- **Memória**: antes de tarefas significativas, ler `memory/MEMORY.md` e
  `docs/errors/README.md`; ao concluir, registrar lições em `memory/lessons/` (+ índices) e
  erros em `docs/errors/`. Chatmodes mantêm `memory/agents/<name>.md`.
- **Documentação**: decisões → ADR em `docs/adr/`; arquitetura → C4 (Mermaid) em
  `docs/architecture/`; trabalho novo → spec em `docs/specs/` (spec → plan → tasks).
  Incluir visualizações Mermaid para fluxos, dependências, hierarquias e ciclos.
- **Matemática**: nada de gabarito sem verificação; fontes externas só gratuitas e com
  licença registrada.
- **Não** fazer commit/push sem solicitação explícita; **não** implementar sem spec aprovada.

## Fluxo de trabalho por tickets

Todo desenvolvimento, bug, infra ou conteúdo de porte passa por um ticket em
`tickets/TCK-NNNN-<slug>/` (`ticket.md` + `log.md` append-only) — ver
[`docs/ai/ticket-protocol.md`](../docs/ai/ticket-protocol.md) e o prompt `/ticket`.

- Ciclo: `new` → tech-lead (`triaged`) → agente da área (`in_progress`) → code-reviewer
  (`in_review`) → qa-validator (`in_validation`) → `done`.
- **Log ou não aconteceu**: toda ação vira entrada `ACTION`/`HANDOFF`/`REJECT` com `[SEQ]`
  incremental; append-only, corrigir = `CORRECTION`.
- **Evidência > afirmação**; critérios de aceite são a definição de pronto; só o
  `qa-validator` marca `done`.
- Nenhum chat mode valida artefato que ele mesmo produziu.
- 3 devoluções no mesmo par → escalar ao `tech-lead`.
- Commits com prefixo `TCK-NNNN:`.

## Recursos do Copilot neste repositório

- `.github/instructions/*.instructions.md` — instruções aplicadas por escopo de caminho
  (`applyTo`): `content/**`, `memory/**`, `docs/**` e código da aplicação.
- `.github/prompts/*.prompt.md` — prompt files reutilizáveis, espelhando as skills
  (`/new-topic`, `/new-exercise-set`, `/math-verify`, `/content-audit`, `/i18n-parity`,
  `/a11y-audit`, `/pwa-audit`, `/create-adr`, `/create-spec`, …). **Gerados** por
  `scripts/sync-ai-adapters.py` — não editar à mão.
- `.github/chatmodes/*.chatmode.md` — chat modes espelhando os agents
  (`curriculum-architect`, `content-author`, `math-reviewer`, `exercise-designer`,
  `i18n-steward`, `platform-architect`, `web-implementer`, `a11y-ux-reviewer`,
  `learning-analytics`, `researcher`, `docs-writer`, `task-router`,
  `retrospective-curator`).
- `tools/dev-loop.sh` — conduz o loop de desenvolvimento de forma assistida
  (`next` indica a próxima etapa e o chatmode a ativar).
- `scripts/audit-ai-surface.sh` e `scripts/audit-content.sh` — auditorias determinísticas.
