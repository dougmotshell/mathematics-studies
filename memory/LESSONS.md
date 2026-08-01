# LESSONS.md — Índice de lições aprendidas

> Uma lição por arquivo em `memory/lessons/`. Cada lição tem um identificador `L-NNN`
> **estável**, citável nos logs de ticket (`aplicada L-002`, `Lição: L-004`).
> Registro obrigatório nos gatilhos descritos em `docs/ai/ticket-protocol.md`.
>
> **Repetir um erro que já tem lição registrada é defeito bloqueante** em review e QA.

## Como registrar

Use `/capture-lesson`. Formato do arquivo:

```markdown
**Tipo:** sucesso | erro | correção
**ID:** L-NNN
**Contexto:** <onde/quando, com data absoluta e ticket, se houver>
**Lição:** <o que foi aprendido>
**Como aplicar:** <regra prática e verificável para as próximas tarefas>
```

Lição superada não é apagada: registre uma **nova** lição referenciando a antiga.

## Correção

- [L-001](lessons/bilingual-content-is-not-translated-later.md) — 2026-08-01 — conteúdo —
  conteúdo nasce bilíngue; "traduzir depois" vira dívida permanente e conteúdo monolíngue
  publicado.

## Erro

- [L-002](lessons/verify-before-publishing-answers.md) — 2026-08-01 — conteúdo —
  gabarito afirmado sem verificação independente é a principal fonte de erro em plataformas
  de exercícios.

## Sucesso

- [L-003](lessons/content-slugs-are-public-urls.md) — 2026-08-01 — currículo —
  tratar slugs como contrato público desde o primeiro nó evita migração de URLs depois.
