---
id: TCK-0008
title: Remover o estado obsoleto do ADR-0003 da superfície de IA e das memórias
type: docs
status: triaged
owner: tech-lead
priority: P2
size: P
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0003]
---

# TCK-0008 — Remover o estado obsoleto do ADR-0003 da superfície de IA e das memórias

## Pedido original (verbatim)

> **A-1 — abrir ticket de limpeza das 7 pendências de `ADR-0003 proposed`**, na ordem de risco
> que apurei: (1) `.claude/workflows/feature-plan-review.js:64` (única que **afirma** o estado
> obsoleto; exige `sync-ai-adapters.py` depois), (2) `memory/agents/tech-lead.md:16`,
> (3) `.claude/agents/tech-lead.md:52` e `.claude/skills/ticket/SKILL.md:51` (exigem sync),
> (4) `memory/agents/{product-analyst:18,a11y-ux-reviewer:56,docs-writer:63}.md`.
> Cada arquivo deve ser editado pelo seu dono (AGENTS.md §5 e §10).
>
> **A-2 — dívida `D-1`** (julgamento (a)): `ADR-0003:95` → "nenhum mecanismo **não decidido**".
> Uma palavra; entra em qualquer edição futura do ADR, sem ticket próprio.
>
> **A-3 — `memory/agents/a11y-ux-reviewer.md:56` cita dependência errada**: a duplicação
> MathML × `*Leitura:*` depende de **decisão de implementação** (KaTeX build × runtime,
> `docs/specs/minimum-learning-slice/plan.md:134`), não do `ADR-0003`, que declara não decidir
> isso. Corrigir junto com A-1.

— `tickets/TCK-0003-accept-platform-stack-adr/log.md` `[015]`, "ACTION ao `tech-lead`".

## Requisito refinado

Quem sofre: o próprio `tech-lead` na próxima triagem da frente de plataforma — a sua memória
(`:16`) afirma que tickets de `frontend-developer` / `backend-developer` / `devops-engineer`
ficam `blocked: human-input`, condição que o `ADR-0003 accepted` tornou falsa — e o agente que
rodar `feature-plan-review`, cujo prompt **afirma** que a stack "ainda está `proposed`" e pode
produzir um achado falso-positivo contra um plano correto.

Resultado esperado: nenhum artefato lido por agente afirma estado obsoleto do `ADR-0003`; o
que restar cita o ADR apenas como histórico narrado, identificado um a um.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. `.claude/workflows/feature-plan-review.js` não afirma mais que a stack está
      `proposed`: a pergunta de revisão passa a exigir a **checagem do status real** do ADR
      citado pelo plano, sem exemplo datado. Teste:
      `grep -niE "proposed|ainda não|não decidid" .claude/workflows/feature-plan-review.js`
      → nenhuma ocorrência ligada ao `ADR-0003`.
- [ ] 2. `.claude/agents/tech-lead.md:52` e `.claude/skills/ticket/SKILL.md:51` enunciam a
      norma ("decisão estrutural exige ADR aceito") **sem** usar o `ADR-0003` como exemplo de
      decisão pendente. Teste:
      `grep -rn "ADR-0003" .claude/ | grep -iE "proposed|em aberto|não decidid|aguarda"` →
      vazio. A norma continua legível sem o exemplo (falha se a regra sumir junto).
- [ ] 3. As quatro memórias — `memory/agents/{tech-lead:16, product-analyst:18,
      docs-writer:63, a11y-ux-reviewer:56}.md` — deixam de descrever a stack como indecidida,
      **cada uma editada pelo seu próprio dono** (AGENTS.md §5). O log nomeia quem editou
      cada arquivo; falha se um agente editar a memória de outro.
- [ ] 4. `memory/agents/a11y-ux-reviewer.md:56` passa a citar a dependência correta — decisão
      de implementação do KaTeX (build × runtime, `docs/specs/minimum-learning-slice/
      plan.md:134`) — e não o `ADR-0003`, que declara **não** decidir isso (A-3). Falha se só
      trocar o rótulo de status mantendo a dependência errada.
- [ ] 5. `docs/adr/ADR-0003-platform-stack.md:95` diz "nenhum mecanismo **não decidido**"
      (D-1). Teste: `git diff --numstat docs/adr/ADR-0003-platform-stack.md` → **1 linha
      alterada**; `grep -n "^\*\*Status:\*\*" ` continua `accepted`; a Decisão e as
      Consequências não mudam. Falha se a edição tocar qualquer decisão do ADR.
- [ ] 6. Varredura final registrada no log, com a saída do comando:
      `grep -rn "ADR-0003" . --exclude-dir=.git | grep -viE "^\./\.dev-loop/|^\./tickets/" |
      grep -iE "proposed|hipótese|em aberto|pendente|não decidid|não está|em avaliação|aguarda"`
      → só restam ocorrências que **narram** histórico (registros meta, `docs/specs/`), e o
      log lista cada uma com a razão de permanecer. Falha se restar qualquer ocorrência que
      **afirme** o estado atual.
- [ ] 7. `python3 scripts/sync-ai-adapters.py --check` → exit 0;
      `bash scripts/audit-ai-surface.sh` → `Resultado: OK`;
      `bash scripts/audit-content.sh` → `0 erros · 0 avisos`. Nenhum gerado editado à mão:
      o diff dos gerados corresponde exatamente ao que o sync produz.
- [ ] 8. O log explica **por que a varredura da L-010 não pegou estes sete pontos** no
      TCK-0003 e o que muda no procedimento (termos de busca, diretórios, arquivos `.js` da
      superfície de IA). Se a conclusão for que a L-010 precisa evoluir, a lição nova
      referencia a antiga em vez de reescrevê-la (`memory/LESSONS.md`).

### Requisitos transversais (marcar todos)

- [ ] Bilinguismo pt-BR + en-US · [x] não aplicável — documentação interna, pt-BR por convenção
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável — nenhum artefato de usuário final
- [ ] Funciona offline / PWA · [x] não aplicável
- [x] Custo zero mantido — só texto
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [ ] URLs de `content/` preservadas · [x] não aplicável — `content/` não é tocado
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Reabrir qualquer decisão do `ADR-0003`: a edição de D-1 é de **precisão de redação**, uma
  palavra na leitura do diagrama. Mudar decisão exige ADR novo (`docs/adr/README.md`).
- Editar os logs dos tickets TCK-0001…TCK-0005 (append-only) nem `.dev-loop/` (gitignorado).
- Escrever o C4 Container ou o ADR de CI/CD — é o TCK-0011.

## Contexto e referências

- Origem: `TCK-0003/log.md` `[010]` (lista das 6 pendências de área alheia), `[014]` S6 e S7
  (sétima ocorrência + D-1), `[015]` julgamentos (a) e (b) e ACTIONs A-1, A-2, A-3.
- ADRs aplicáveis: `ADR-0003` (`accepted`, 2026-08-01) e `ADR-0004` (fluxo por tickets).
- Arquivos-alvo: os 7 pontos listados + `docs/adr/ADR-0003-platform-stack.md:95` + os
  gerados por `scripts/sync-ai-adapters.py`.
- Lições relevantes: **L-010** (aceitar um ADR significa atualizar as regras que os agentes
  leem — é a lição cuja varredura falhou aqui); **L-013** (corrigir a linha citada não é
  corrigir a classe do defeito); **L-005** (triagem não é handoff).
- Classificação de risco herdada do `qa-validator#4` (`[015]` julgamento (b)): só o
  `feature-plan-review.js:64` **afirma** o estado obsoleto — prioridade 1 dentro do ticket;
  os demais são guarda condicional com condição hoje falsa ou registro meta.

## Perguntas em aberto

- Nenhuma.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
