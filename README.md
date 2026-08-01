# mathematics-studies

Plataforma **gratuita e aberta** de estudos de matemática — da matemática mais básica à mais
avançada, organizada de forma didática, bilíngue (**pt-BR** / **en-US**) e com exercícios
interativos, feedback imediato e acompanhamento de progresso.

> **Estado:** bootstrap. O repositório contém, neste momento, a **superfície de IA** e os
> padrões de trabalho (documentação, conteúdo, memória, agentes). A aplicação ainda não foi
> implementada — a stack está em avaliação em
> [`docs/adr/ADR-0003-platform-stack.md`](docs/adr/ADR-0003-platform-stack.md) (`proposed`).

## O que este projeto é

| Dimensão | Descrição |
|---|---|
| **Conteúdo** | Teoria, exemplos, exercícios, avaliações, vídeos e referências gratuitas, organizados por estágio educacional (educação infantil → pesquisa), área e dificuldade. |
| **Plataforma** | Aplicação web **PWA**, acessível de qualquer navegador, sem instalação, com deploy na **Vercel**. |
| **Produto** | Módulos de plataforma de cursos: trilhas de aprendizado, quizzes, fóruns, progresso, estatísticas de desempenho e certificados. |
| **Idiomas** | Todo objeto de aprendizagem existe em pt-BR **e** en-US, em paridade. |

## Como o conteúdo é organizado

```
content/<stage>/<area>/<topic>/[<subtopic>/]
    meta.json          # id, pré-requisitos, dificuldade, tags, status
    theory.pt-BR.md    # teoria (KaTeX)
    theory.en-US.md
    exercises.json     # itens de prática com feedback diagnóstico
    assessments.json   # avaliação somativa (opcional)
    references.json    # fontes gratuitas + licença
    assets/
```

Detalhes e listas canônicas: [`docs/content/taxonomy.md`](docs/content/taxonomy.md).

## Trabalhando com agentes de IA

Este repositório é preparado para ser operado por **Claude Code, OpenAI Codex, GitHub
Copilot, Gemini CLI** e qualquer outro assistente que leia `AGENTS.md`.

| Arquivo | Papel |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **Fonte única** de instruções (todos os CLIs). |
| [`CLAUDE.md`](CLAUDE.md) | Adaptador do Claude Code (agents, skills, workflows). |
| [`GEMINI.md`](GEMINI.md) | Adaptador do Gemini CLI (custom commands). |
| [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Adaptador do Copilot (prompts, chatmodes, instructions). |
| [`.codex/README.md`](.codex/README.md) | Adaptador do Codex (prompts pessoais, loop assistido). |
| [`SLASH_COMMANDS.md`](SLASH_COMMANDS.md) | Inventário de comandos disponíveis em cada CLI. |

### Setup rápido

```bash
# Gera/atualiza os adapters de Claude, Copilot e Gemini a partir de skills e agents
python3 scripts/sync-slash-commands.py

# Instala também os prompts pessoais do Codex em $CODEX_HOME/prompts
python3 scripts/sync-slash-commands.py --codex

# Auditorias determinísticas
bash scripts/audit-ai-surface.sh     # paridade da superfície de IA
bash scripts/audit-content.sh        # estrutura e paridade do conteúdo
```

### Fluxos mais usados

| Quero… | Comando |
|---|---|
| Pedir uma feature, reportar bug ou abrir demanda | `/ticket <descrição>` |
| Retomar um ticket parado | `/ticket-loop TCK-NNNN` |
| Passar o ticket ao próximo agente | `/handoff TCK-NNNN` |
| Criar um nó de conteúdo novo | `/new-topic <stage>/<area>/<topic>` |
| Criar exercícios para um nó | `/new-exercise-set <caminho do nó>` |
| Verificar um resultado matemático | `/math-verify <afirmação>` |
| Desenhar uma trilha de aprendizado | `/learning-path <objetivo do aluno>` |
| Auditar conteúdo (didática, rigor, i18n) | `/content-audit <caminho>` |
| Checar paridade pt-BR/en-US | `/i18n-parity [caminho]` |
| Registrar decisão / spec / erro / lição | `/create-adr`, `/create-spec`, `/log-error`, `/capture-lesson` |
| Rodar um loop leve, sem ticket | `/dev-loop <tarefa>` |
| Trocar de CLI no meio da tarefa | `/agent-handoff` |

### Como o trabalho anda sozinho

`/ticket` cria a demanda, o `tech-lead` faz a triagem e o ciclo **execução → code review →
QA** roda em loop até todos os critérios de aceite passarem. Você só é chamado em `done`, em
`blocked: human-input` ou quando três reprovações escalam o impasse. Tudo fica registrado no
`log.md` append-only do ticket. Contrato completo:
[`docs/ai/ticket-protocol.md`](docs/ai/ticket-protocol.md).

## Documentação

- [`docs/product/vision.md`](docs/product/vision.md) — visão, público-alvo e escopo.
- [`docs/product/roadmap.md`](docs/product/roadmap.md) — fases e próximos passos.
- [`docs/content/`](docs/content/) — padrões de conteúdo: taxonomia, i18n, exercícios,
  acessibilidade, didática.
- [`docs/DOC-STANDARDS.md`](docs/DOC-STANDARDS.md) — C4 + ADR + Spec-Driven Development.
- [`docs/adr/`](docs/adr/) — decisões registradas.
- [`memory/`](memory/) — memória compartilhada entre os agentes (contexto, lições).

## Contribuindo

Ver [`CONTRIBUTING.md`](CONTRIBUTING.md). Regra de ouro: **nada de conteúdo monolíngue,
nada de gabarito não verificado, nada de implementação sem spec.**

## Licença

A definir (ver `docs/adr/`). A intenção declarada é conteúdo sob licença aberta compatível
com reuso educacional.
