---
id: TCK-0016
title: Registrar o aceite dos ADR-0006 e ADR-0007
type: docs
status: in_review
owner: platform-architect
priority: P1
size: P
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0011, TCK-0015, ADR-0006, ADR-0007]
---

# TCK-0016 — Registrar o aceite dos ADR-0006 e ADR-0007

## Pedido original (verbatim)

> já conectei o repositório na vercel (…) depois configure tudo para o deploy

> sim, implemente o projeto base e já inicie o desenvolvimento da plataforma

Decisões do usuário (Douglas Silva, 2026-08-01): URL com prefixo de idioma **minúsculo**
(`/pt-br/`, `/en-us/`), **previews por PR ativados**, projeto Astro **na raiz**.

## Requisito refinado

O `qa-validator#9` levantou, ao fechar o TCK-0011, uma contradição real de governança: o
**TCK-0015 está implementando o pipeline e o esqueleto sob ADRs ainda `proposed`**, e o
próprio `ADR-0006:10-12` proíbe isso em letra.

A contradição não é de execução — o usuário autorizou explicitamente implementar e
configurar o deploy, e as três decisões que faltavam foram tomadas. É de **registro**: falta
transformar a autorização em aceite formal, com as consequências preenchidas e a propagação
que L-010 exige para ADR aceito (e que foi corretamente omitida enquanto estavam `proposed`).

## Critérios de aceite

- [x] 1. `ADR-0006` e `ADR-0007` com `status: accepted`, data 2026-08-01 e decisor
      Douglas Silva; o aviso de "espera aceite" removido ou substituído.
- [x] 2. As três decisões do usuário registradas na seção **Decisão** de quem as governa:
      URL minúscula, previews por PR, projeto na raiz.
- [x] 3. **Consequências** preenchidas nos dois ADRs — o que passa a valer, o que fica
      proibido sem ADR novo, e o que continua sendo decisão de ticket.
- [x] 4. A grafia alternativa de URL sai do diagrama e do ADR: com a decisão tomada, mantê-la
      viva passa a ser informação falsa (`c4-container.md:41`, `ADR-0007`, e onde mais
      aparecer).
- [x] 5. Marcadores atualizados por **classe**, não por linha: nenhum elemento continua
      `PROPOSTO (ADR-0006)` ou `PROPOSTO (ADR-0007)` depois do aceite; o que era
      `EM ABERTO (ticket)` **permanece** — aceitar o ADR não fecha o que ele decidiu não
      decidir.
- [x] 6. Propagação L-010: varredura da **raiz** (não de `docs/`) por menção aos dois ADRs
      como pendentes — `AGENTS.md`, `.github/instructions/`, `.claude/`, `prompts/`,
      `README.md`, `memory/context/`, `docs/product/roadmap.md`. Onde a fonte for canônica,
      rodar `python3 scripts/sync-ai-adapters.py`.
- [x] 7. `docs/adr/README.md` e `memory/context/project-context.md` refletem o aceite.
- [~] 8. `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` sem erros.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — o aceite preserva a exigência de rotas bilíngues
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável
- [x] Funciona offline / PWA — restrição preservada, implementação é a task 10
- [x] Custo zero mantido — a elegibilidade já foi verificada no TCK-0011
- [x] Privacidade e dados de menores (LGPD/COPPA) — sem backend, conta ou telemetria
- [x] URLs de `content/` preservadas — critério 4
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Alterar código, `package.json`, `src/`, `vercel.json` ou `.github/workflows/` — é o
  TCK-0015, em revisão agora.
- Reabrir o mérito das decisões: elas foram tomadas pelo usuário.
- Tocar `content/`, `docs/design/`, `docs/content/` ou `scripts/`.

## Contexto e referências

- `docs/adr/ADR-0006-continuous-integration-and-publication.md`, `ADR-0007-application-skeleton.md`
- `docs/architecture/c4-container.md` (legenda dos três marcadores em `:13-15`)
- Origem do achado: `tickets/TCK-0011-container-architecture-and-cicd/log.md`, `[012]`
- Lições aplicáveis: L-010 (aceite exige varrer a raiz), L-011, L-013, L-020

## Perguntas em aberto

- Nenhuma. As três decisões humanas foram tomadas em 2026-08-01.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
