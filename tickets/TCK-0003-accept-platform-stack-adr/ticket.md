---
id: TCK-0003
title: Registrar o aceite do ADR-0003 (stack da plataforma)
type: docs
status: done
owner: qa-validator#4
priority: P1
size: P
created: 2026-08-01
updated: 2026-08-01
related: [ADR-0003, TCK-0002]
---

# TCK-0003 — Registrar o aceite do ADR-0003 (stack da plataforma)

## Pedido original (verbatim)

> faça tudo que for necessário

Decisão do usuário coletada em 2026-08-01 (Douglas Silva, decisor nomeado no ADR):

> **Stack:** opção **C** — gerador de site estático orientado a conteúdo (Astro) com ilhas
> de interatividade.
> **Persistência de progresso:** opção **1** — local-first sem conta (IndexedDB).

## Requisito refinado

O `ADR-0003` está `proposed` e, por isso, bloqueia todos os tickets de implementação da
aplicação (`frontend-developer`, `backend-developer`, `devops-engineer`). O decisor já
escolheu. Falta transformar a escolha em decisão registrada: mudar o status para `accepted`,
escrever a seção **Decisão** de forma inequívoca, preencher **Consequências** (hoje "A
preencher no aceite") e propagar o desbloqueio para a memória e a documentação do projeto.

## Critérios de aceite

- [x] 1. `docs/adr/ADR-0003-platform-stack.md` tem `status: accepted`, data e decisor
      preenchidos, e o aviso de "nenhum ticket deve avançar" removido/substituído.
- [x] 2. A seção **Decisão** afirma sem ambiguidade a opção C (site estático orientado a
      conteúdo, ilhas de interatividade) e a persistência local-first sem conta, com a
      justificativa das alternativas descartadas.
- [x] 3. A seção **Consequências** está preenchida com o que passa a valer na prática:
      restrições de arquitetura, o que fica proibido sem novo ADR (backend obrigatório,
      conta, telemetria identificável) e o que o aceite destrava.
- [x] 4. A independência do contrato de dados de `content/` em relação à stack é declarada
      como restrição a preservar.
- [x] 5. `docs/adr/README.md`, `memory/context/project-context.md` e
      `memory/context/frontend.md` refletem o aceite (nada mais descreve `ADR-0003` como
      decisão em aberto).
- [x] 6. `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` seguem sem
      erros.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — o aceite preserva a exigência de rotas bilíngues
- [x] Acessibilidade WCAG 2.2 AA — restrição registrada nas consequências
- [x] Funciona offline / PWA — restrição registrada nas consequências
- [x] Custo zero mantido — local-first sem backend
- [x] Privacidade e dados de menores (LGPD/COPPA) — sem conta e sem telemetria identificável
- [x] URLs de `content/` preservadas
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Instalar dependências, criar o esqueleto da aplicação ou qualquer código.
- Escolher biblioteca de UI, de testes ou de service worker — decisões de implementação,
  não do ADR.
- Decidir a licença do projeto (é o `TCK-0004`).
- Alterar `content/`.

## Contexto e referências

- ADR: `docs/adr/ADR-0003-platform-stack.md` (hoje `proposed`)
- Spec dependente: `docs/specs/minimum-learning-slice/` (produzida no `TCK-0002`)
- Requisitos da fatia mínima: `.dev-loop/minimum-learning-slice/requirements.md`
- Padrão: `docs/adr/adr-template.md`, `docs/DOC-STANDARDS.md`
- Contexto: `memory/context/project-context.md`, `memory/context/frontend.md`

## Perguntas em aberto

- Nenhuma. A decisão humana que faltava foi tomada em 2026-08-01.

## Resultado final

**`done` em 2026-08-01, validado por `qa-validator#4`** — 6/6 critérios com evidência própria
reproduzida (comando + saída ou arquivo + linha) na entrada `[015]` do `log.md`. Três loops de
devolução consumidos (`[006]` B1–B3, `[010]` B4); zero defeito bloqueante na validação.

### O que este aceite destrava

- **A frente de plataforma sai do bloqueio.** Tickets de `frontend-developer`,
  `backend-developer` e `devops-engineer` deixam de nascer `blocked: human-input` por
  indefinição de stack (`ADR-0003:8-13`, `:182-185`).
- **A `docs/specs/minimum-learning-slice/` ganha chão técnico:** `plan.md` já cita o ADR aceito
  como direção, mantendo aberto o que é implementação (item 3, KaTeX build × runtime).
- **O `backend-developer` muda de objeto:** passa a atuar sobre pipeline de conteúdo e modelo
  de dados local — não há servidor (`ADR-0003:182-185`).
- Continua valendo o portão anterior: **nenhuma implementação sem spec aprovada**
  (`AGENTS.md:221,438` e mais 9 pontos) — o aceite remove o bloqueio de stack, não o de spec.

### Restrições que passam a valer (verificáveis em qualquer ticket futuro)

1. JavaScript mínimo por padrão; interatividade confinada a **ilhas** com fronteira explícita.
2. Uma rota estática **por idioma**, com paridade obrigatória (`ADR-0002`).
3. **PWA offline-first** para o conteúdo visitado, exercícios inclusos — requisito de
   arquitetura, não acabamento.
4. **KaTeX acessível**: descrição textual em toda fórmula em display; imagem de fórmula
   proibida onde LaTeX resolve; sem custo de JS desproporcional.
5. **Sem backend, conta, login ou telemetria identificável** — cada um exige **ADR novo**, com
   LGPD/COPPA quando envolver menor de idade.
6. **O gabarito viaja no cliente**: nada pode depender do segredo da resposta (sem prova
   valendo nota, ranking ou certificado verificável).
7. **Deploy estático portátil**: recurso proprietário da Vercel que quebre a portabilidade
   exige ADR.
8. **Independência do contrato de dados de `content/`**, com teste de conformidade declarado
   (`ADR-0003:157-174`): um leitor escrito do zero deve reconstruir taxonomia, rotas e
   exercícios só lendo os arquivos e o schema de `docs/content/`.

O que o ADR **não** decide, e segue como decisão do ticket de implementação: biblioteca de UI,
framework de testes, estratégia/ferramenta de service worker, ferramenta de build auxiliar e o
**momento de renderização do KaTeX** (build × runtime).

### Pendências herdadas (não bloqueiam; `ACTION` ao `tech-lead` no `[015]`)

- **A-1** — 7 pontos de área alheia ainda dizem `ADR-0003 proposed`, por ordem de risco:
  `.claude/workflows/feature-plan-review.js:64` (única que **afirma** o estado obsoleto, em vez
  de condicioná-lo), `memory/agents/tech-lead.md:16`, `.claude/agents/tech-lead.md:52`,
  `.claude/skills/ticket/SKILL.md:51`,
  `memory/agents/{product-analyst:18,a11y-ux-reviewer:56,docs-writer:63}.md`. Nenhuma anula o
  desbloqueio (todas são guarda condicional com condição hoje falsa, exemplo envelhecido ou
  registro meta), mas cada uma deve ser corrigida pelo respectivo dono; duas exigem
  `sync-ai-adapters.py`.
- **A-2 / dívida D-1** — `ADR-0003:95` diz que o diagrama traz "nenhum mecanismo", enquanto
  IndexedDB (`:88`) e Vercel (`:90`) são mecanismos **decididos**. Julgado imprecisão
  tolerável, não defeito: não gera restrição operativa errada e a decisão é afirmada de forma
  normativa em `:60-62`, `:181`, `AGENTS.md:38,440` e `frontend.md:13-15`. Correção de uma
  palavra ("nenhum mecanismo **não decidido**") na próxima edição do ADR.
- **A-3** — `memory/agents/a11y-ux-reviewer.md:56` atribui ao `ADR-0003` uma dependência que
  ele declara **não** decidir (momento de renderização); o dono correto é o ticket de
  implementação.
- **A-4** — C4 nível **Container** inexistente e CI/CD + previews por branch marcados
  `PROPOSTO` (`docs/architecture/c4-context.md:20,26`) sem ADR. Ambos merecem ticket próprio
  antes do primeiro ticket de implementação.

### Alcance da validação (declarado)

Validação **documental**: não existe aplicação (`ls src app api` → inexistentes;
`find . -name package.json` → vazio), logo a bateria de casos hostis (offline, dois idiomas,
tema claro/escuro, zoom 200%, teclado, leitor de tela, rede lenta, dados vazios) **não é
aplicável** aqui — ela se aplica ao primeiro ticket de implementação, onde as restrições 1–7
acima viram comportamento executável.
