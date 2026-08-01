# MEMORY.md — Índice da memória compartilhada dos agentes

> Uma linha por memória. Ler este índice no início de toda tarefa significativa; abrir apenas
> os arquivos relevantes. Regras completas na seção 5 do `AGENTS.md` e em
> `docs/ai/ticket-protocol.md`.

## Contexto

- [project-context](context/project-context.md) — estado atual do projeto por frente
  (conteúdo, plataforma, superfície de IA, documentação).

## Contexto operacional por área

> Documento vivo por área: pegadinhas do ambiente, estado atual, decisões operacionais.

- [process](context/process.md) — fluxo de tickets, triagem, convenções de trabalho.
- [frontend](context/frontend.md) — interface, PWA, KaTeX, i18n, temas.
- [backend](context/backend.md) — dados, progresso, pipeline de conteúdo, integrações.
- [devops](context/devops.md) — CI/CD, Vercel, ambientes, monitoramento.
- [qa](context/qa.md) — validação, e2e, casos hostis, flakiness.
- [security](context/security.md) — privacidade de menores, segredos, dependências.
- [content](context/content.md) — produção de teoria e exercícios, revisão matemática.
- [curriculum](context/curriculum.md) — taxonomia, trilhas, grafo de pré-requisitos.

## Sub-índices

- [LESSONS](LESSONS.md) — índice de lições classificado por tipo (`sucesso | erro |
  correção`), com identificadores `L-NNN` citáveis nos logs de ticket.
- [agents/](agents/README.md) — memória individual por agente (`memory/agents/<name>.md`).

## Lições

- [L-001 · bilingual-content-is-not-translated-later](lessons/bilingual-content-is-not-translated-later.md)
  — conteúdo nasce nos dois idiomas; traduzir depois produz dívida que não se paga.
- [L-002 · verify-before-publishing-answers](lessons/verify-before-publishing-answers.md)
  — gabarito só existe depois de verificação independente.
- [L-003 · content-slugs-are-public-urls](lessons/content-slugs-are-public-urls.md)
  — slug de `content/` é contrato público; renomear quebra links de terceiros.
