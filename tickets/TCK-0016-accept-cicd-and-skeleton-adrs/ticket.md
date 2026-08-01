---
id: TCK-0016
title: Registrar o aceite dos ADR-0006 e ADR-0007
type: docs
status: done
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
- [x] 8. `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` sem erros.

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

**`done` em 2026-08-01, validado pelo `qa-validator#11`** — 8 de 8 critérios com evidência
reproduzida na validação (`log.md` `[016]`), 0 defeitos, 1 devolução no ciclo (`[009]`, sync não
executado, fechada em `[010]`). Ambiente da validação: `HEAD` `dea3303`, Node v24.14.1,
Python 3.12.3; sem preview (entrega documental). `sync-ai-adapters.py --check`,
`audit-ai-surface.sh` e `audit-content.sh` → **exit 0 nos três**, medidos duas vezes, a segunda
depois da última edição do TCK-0015 no workflow.

**O que passa a valer.** `ADR-0006` e `ADR-0007` estão `accepted` desde 2026-08-01, decisor
Douglas Silva. Ticket pode criar e alterar pipeline, `package.json`, `src/` e dependências com
fundamento — não mais como hipótese. Ficam fixados: **previews por PR ligados** (sem
autenticação, sem domínio de produção), **produção publica no push/merge em `main`**, **projeto
Astro na raiz**, **`src/content-contract/` como único leitor do acervo**, **URL com prefixo de
idioma em minúsculas** (`/pt-br/…`, `/en-us/…`, contrato público) e **Node ≥ 22.12.0**. Ficam
proibidos sem ADR novo: segredo no repositório, telemetria de visitante, CDN de terceiro, URL em
caixa mista, renderização por requisição, trocar o gerador, mover o repositório para uma
organização ou monetizar o projeto. A contradição de governança que originou o ticket — o
TCK-0015 construindo sob ADRs `proposed` — está resolvida **no registro**; o aceite autoriza
aquele trabalho e **não** atesta que ele esteja correto.

**O que continua aberto, apesar do aceite.** Verificado item a item contra `plan.md:132-142`:
**onde** roda o portão de validação do RF-18 (exercido pelo TCK-0015, aberto em 9 pontos dos
dois ADRs e dos dois C4), biblioteca de UI dentro da ilha, ferramenta de teste, mecanismo da
camada offline/service worker, momento em que a matemática vira HTML, ferramenta de Markdown →
HTML, e cada dependência nova. Fora dos ADRs e ainda do ticket: os números do orçamento de
performance (RNF-8). Nenhum item que era decisão de ticket foi absorvido pelo aceite. Pendente
de **ato humano**: proteção de branch em `main` — sem ela, o portão de mérito é informativo.

**Dívidas.** D-1: a convenção de emenda editorial (`docs/adr/README.md:9-16`) tem duas metades
não equivalentes; o QA decidiu que vale *"emenda quando a frase falsa não é a decisão;
`superseded` quando é"*, falta a redação. D-2: a lista "o que continua sendo decisão de ticket"
não é exaustiva contra `plan.md` (faltam o modelo concreto de renderização e o RNF-8). D-3:
`plan.md:132-142` envelheceu — os itens 1 e 2 já não são decisão de ticket.

**Para quem for commitar.** O sync carregou junto a edição do TCK-0006 em
`.github/instructions/core.instructions.md`, que o `dea3303` deixou **fora** do commit
(`git show HEAD:… | grep -c "agrupamento dito em palavras"` → 0, working tree → 1). Portanto
`core.instructions.md` e os **6** gerados derivados de `core` (`.cursor/rules/core.mdc`,
`.windsurf/rules/core.md`, `.agents/rules/core.md`, `.rules`, `.clinerules`,
`.junie/guidelines.md`) levam **os dois textos**: o aceite e a norma de leitura de fórmula.
Os 3 gerados de `app` levam só o aceite. **Não reverter** — não é arraste, é estado prévio do
working tree. Encaminhados ao `tech-lead`: `screen-states.md:689,833` (ticket novo,
`ui-ux-designer`), a pendência do `ADR-0003` aberta no TCK-0003, a promoção das duas notas de
memória a `L-026` (`retrospective-curator`) e a referência desatualizada em
`tickets/TCK-0015-.../ticket.md:89-90`.
