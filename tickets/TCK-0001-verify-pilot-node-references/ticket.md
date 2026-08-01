---
id: TCK-0001
title: Verificar as referências externas do nó piloto
type: content
status: new
owner: tech-lead
priority: P2
size: P
created: 2026-08-01
updated: 2026-08-01
related: []
---

# TCK-0001 — Verificar as referências externas do nó piloto

## Pedido original (verbatim)

> (Ticket aberto pelo próprio setup do repositório, em 2026-08-01, para registrar uma
> pendência identificada durante a criação do nó piloto.)

## Requisito refinado

O nó `content/high-school/algebra/quadratic-equations` foi criado com duas referências ao
OpenStax em `references.json`. As URLs e as licenças foram informadas **de memória**, sem
acesso à web no momento da criação — ou seja, não foram verificadas na própria página, como
exige o AGENTS.md §9.6.

Enquanto isso não for feito, o nó não pode sair de `status: "draft"`.

## Critérios de aceite

- [ ] 1. Cada URL de `references.json` foi acessada e retorna a página esperada (sem 404 nem
      redirecionamento para outra obra).
- [ ] 2. A licença registrada corresponde à licença declarada **na própria página** da fonte.
- [ ] 3. O campo `covers` descreve o que a fonte realmente cobre, conferido no material.
- [ ] 4. Foi adicionada ao menos **uma referência gratuita em português** (o acervo pt-BR é o
      mais escasso — ver `/research-sweep`), com autor, ano, URL, idioma e licença.
- [ ] 5. `bash scripts/audit-content.sh` continua sem erros.

### Requisitos transversais

- [x] Bilinguismo pt-BR + en-US — referências devem cobrir os dois idiomas
- [ ] não aplicável: Acessibilidade / Offline / URLs / Correção matemática
- [x] Custo zero mantido — apenas fontes gratuitas

## Fora de escopo

- Alterar a teoria ou os exercícios do nó.
- Publicar o nó (`status: "published"`) — depende também de revisão de `math-reviewer` e
  `i18n-steward`.

## Contexto e referências

- Nó: `content/high-school/algebra/quadratic-equations/references.json`
- Regra: `AGENTS.md` §9.6 e `docs/content/content-standards.md`
- Agente sugerido: `researcher` (com `/research-sweep` para o material em pt-BR)
- Contexto da área: `memory/context/content.md`

## Perguntas em aberto

- Nenhuma.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
