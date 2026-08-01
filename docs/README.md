# Documentação interna

`docs/` explica **como o projeto funciona**. O conteúdo entregue ao aluno vive em
`content/` — nunca misturar os dois planos.

| Pasta | Conteúdo |
|---|---|
| [`product/`](product/) | Visão, roadmap, glossário |
| [`content/`](content/) | Padrões do acervo: taxonomia, didática, i18n, exercícios, acessibilidade |
| [`architecture/`](architecture/) | Diagramas C4 da plataforma e do pipeline de conteúdo |
| [`adr/`](adr/) | Decisões registradas (ADRs numerados) |
| [`specs/`](specs/) | Spec-Driven Development: spec → plan → tasks |
| [`errors/`](errors/) | Registro de erros (anti-repetição) |
| [`ai/`](ai/) | Superfície de IA: protocolo de tickets e handoff entre CLIs |
| [`DOC-STANDARDS.md`](DOC-STANDARDS.md) | Padrões de documentação (C4 + ADR + SDD) |

## Por onde começar

1. [`../AGENTS.md`](../AGENTS.md) — fonte única de instruções.
2. [`product/vision.md`](product/vision.md) — o que estamos construindo e por quê.
3. [`content/taxonomy.md`](content/taxonomy.md) — como o acervo é organizado.
4. [`ai/ticket-protocol.md`](ai/ticket-protocol.md) — como o trabalho é executado.
