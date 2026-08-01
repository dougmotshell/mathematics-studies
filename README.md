# mathematics-studies

Plataforma **gratuita e aberta** de estudos de matemática — da matemática mais básica à mais
avançada, organizada de forma didática, bilíngue (**pt-BR** / **en-US**) e com exercícios
interativos, feedback imediato e acompanhamento de progresso.

> **Estado:** bootstrap. O repositório contém, neste momento, a **superfície de IA** e os
> padrões de trabalho (documentação, conteúdo, memória, agentes). A aplicação ainda não foi
> implementada, mas a stack já está **decidida** em
> [`docs/adr/ADR-0003-platform-stack.md`](docs/adr/ADR-0003-platform-stack.md) (`accepted`,
> 2026-08-01): site estático orientado a conteúdo com ilhas de interatividade, progresso
> local-first no próprio dispositivo (IndexedDB) e deploy estático — sem backend e sem conta.

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

Funciona com **qualquer** assistente de código: Claude Code, Grok CLI, Cursor, GitHub
Copilot, Gemini CLI, Google Antigravity, Windsurf, OpenAI Codex, Zed, Cline/Roo, JetBrains
Junie e ferramentas web (ChatGPT, Grok, Claude).

Três fontes canônicas, escritas uma única vez, geram os adapters de todas elas:

| Fonte | O que define |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Regras completas do projeto |
| [`.claude/agents/`](.claude/agents/) | Papéis (escopo exclusivo, limites, memória) |
| [`.claude/skills/`](.claude/skills/) | Capacidades (procedimentos executáveis) |
| [`.github/instructions/`](.github/instructions/) | Regras por escopo de caminho |

Matriz de suporte, limitações e instalação por ferramenta:
[`docs/ai/tool-support.md`](docs/ai/tool-support.md). Inventário de comandos:
[`SLASH_COMMANDS.md`](SLASH_COMMANDS.md).

### Setup rápido

```bash
# Gera os adapters de todas as ferramentas e mostra o que cada uma precisa
bash scripts/setup-ai-tools.sh

# Codex: os prompts são globais por usuário — isole ou prefixe para não colidir
bash scripts/setup-ai-tools.sh --codex --codex-prefix ms

# Auditorias determinísticas
bash scripts/audit-ai-surface.sh     # paridade da superfície de IA
bash scripts/audit-content.sh        # estrutura e paridade do conteúdo
```

A maioria das ferramentas não precisa de setup algum: basta abrir o repositório.

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

Duas licenças, decididas em 2026-08-01 ([`ADR-0005`](docs/adr/ADR-0005-project-license.md)):

| O quê | Licença | Arquivo |
|---|---|---|
| **Conteúdo** — `content/` (teoria, exercícios, avaliações, trilhas, assets autorais) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [`LICENSE-CONTENT`](LICENSE-CONTENT) |
| **Código e processo** — aplicação, `scripts/`, `tools/`, `docs/`, `memory/`, `tickets/` | MIT | [`LICENSE`](LICENSE) |

Você pode copiar, traduzir e adaptar o conteúdo, inclusive comercialmente, desde que **dê
crédito** e mantenha as adaptações sob a **mesma licença**. Forma de atribuição esperada em
[`LICENSE-CONTENT`](LICENSE-CONTENT).

Materiais de terceiros citados em `references.json` mantêm a licença de seus autores. Fontes
com cláusula **não-comercial** (CC BY-NC / CC BY-NC-SA) são incompatíveis com CC BY-SA 4.0:
podem ser **citadas como leitura externa**, nunca incorporadas ao conteúdo.
