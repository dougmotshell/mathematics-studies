---
id: TCK-0018
title: Aplicar a norma de leitura de fórmula aos 14 pontos de exercises.json do nó piloto
type: content
status: triaged
owner: exercise-designer
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0005, TCK-0006, TCK-0007]
---

# TCK-0018 — Aplicar a norma de leitura de fórmula aos 14 pontos de `exercises.json` do nó piloto

## Pedido original (verbatim)

> | **224 / 225** | **`$x^2 + 6x + 9 = (x+3)^2 = 0$`** (`solution`) | **EXIGE — B1, ausente de `[004]` §4.** É o pior do lote: "x mais três ao quadrado" serve para $(x+3)^2$ e para $x + 3^2$, que são polinômios diferentes |
>
> **Total corrigido: 22 pontos** — 8 em `theory.*.md` + 14 em `exercises.json`. `[004]` §4 dizia
> 18 (e "6 pontos, 3 por idioma" onde a própria tabela marcava **quatro** linhas EXIGE por
> idioma). **Este é o número que dimensiona o TCK-0007.**

— `tickets/TCK-0006-formula-reading-conventions/log.md` `[007]` §2.

> `item cujo gabarito depende de agrupamento não falado fica ambíguo em áudio e o distrator
> vira resposta defensável`

— `[007]` §4, consequência da norma para o papel `exercise-designer`.

## Requisito refinado

Quem sofre: o estudante que usa leitor de tela e chega à **solução** do exercício `qe-004`.
`$x^2 + 6x + 9 = (x+3)^2 = 0$` lido linearmente vira "x mais três ao quadrado" — que descreve
$(x+3)^2$ **e** $x + 3^2$, dois polinômios diferentes. Não é ambiguidade estética: é a solução
do exercício descrevendo, em áudio, um objeto matemático que não é o do enunciado. Os outros
13 pontos do lote (frações e potências de base entre parênteses em `stem`, `hints`, `solution`
e `feedback`) degradam a leitura sem trocar o objeto.

Este ticket nasce da **divisão do TCK-0007** (ver `TCK-0007/log.md` `[003]`): dos 22 pontos do
inventário, 8 estão em `theory.*.md` (lá) e **14 em `exercises.json`** (aqui) — artefato do
`exercise-designer`, diff disjunto, nenhuma dependência entre os dois tickets.

Resultado esperado: as 14 ocorrências têm veredito registrado e tratamento conforme a norma,
e nenhuma solução, dica ou feedback do nó piloto descreve em áudio um objeto diferente do
que mostra na tela.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. **`exercises.json:224` (pt-BR) / `:225` (en-US)** — a leitura de
      `$x^2 + 6x + 9 = (x+3)^2 = 0$` marca o agrupamento da base elevada. **Teste de
      reconstrução às cegas:** a partir **apenas** das palavras da leitura (sem ver o LaTeX),
      o revisor escreve **um** polinômio, e ele é $(x+3)^2$. Falha se a reconstrução admitir
      $x + 3^2$. **Assinatura dupla obrigatória:** `math-reviewer` (o objeto está
      determinado?) **e** `a11y-ux-reviewer` (a marcação é audível e não vira ruído), cada um
      registrando a própria reconstrução no log. Nenhum dos dois escreveu a redação.
- [ ] 2. Cada uma das **14 ocorrências** de `exercises.json` do inventário corrente —
      `tickets/TCK-0006-formula-reading-conventions/log.md` `[007]` §2, tabela
      "`exercises.json` — 14 pontos (7 por idioma)" — tem o par ocorrência → ação registrado
      no log, incluindo as marcadas "não exigem" com o motivo. O ponteiro é a fonte; a lista
      **não** é copiada para cá. Falha se qualquer linha daquela tabela ficar sem veredito.
- [ ] 3. Os **dois gatilhos** decididos no TCK-0006 são aplicados como classe, não como lista:
      (1) base entre parênteses ou colchetes; (2) sinal unário imediatamente à frente da base
      elevada. Teste: varredura do arquivo inteiro por **predicado da classe** (não pelos
      exemplos conhecidos), com o padrão e a saída no log; o resultado tem de reencontrar as
      14 ocorrências e declarar quantas fora da lista apareceram (esperado hoje: 0 do gatilho
      2, conforme a medição de `[007]` §3). Falha se a varredura for feita por `grep` dos
      casos já citados — foi exatamente assim que a ocorrência de 224/225 escapou (adendo da
      L-021).
- [ ] 4. **A matemática não muda.** Nenhum `id`, `type`, `answer`, `tolerance`, `correct`,
      `verified` ou expressão LaTeX é alterado — só o texto de leitura/marcação verbal.
      Teste: `python3 -c` (ou `jq`) extraindo esses campos de todos os itens **antes** e
      **depois** → diferença **vazia**; e `git diff` do arquivo não contém alteração dentro de
      `$…$`. Falha se qualquer alternativa trocar de gabarito.
- [ ] 5. **Paridade pt-BR/en-US** (ADR-0002, L-001): as 7 ocorrências de cada idioma são
      tratadas no **mesmo item**, no **mesmo campo** e no mesmo ciclo. Teste por
      correspondência item a item (L-012 — por ordem, não por contagem): para cada `id` de
      item alterado, o campo alterado existe nos dois idiomas; nenhuma marcação órfã.
      Verificado pelo `i18n-steward`.
- [ ] 6. **A leitura é conteúdo, e conteúdo bilíngue é escrito, não traduzido de máquina:** a
      marcação verbal usa a convenção decidida em `docs/content/accessibility.md` (tabela
      normativa, coluna pt-BR e coluna en-US), e não uma tradução literal de uma na outra.
      Verificado pelo `i18n-steward` contra a tabela.
- [ ] 7. `meta.json` continua com `status: "draft"`. O log declara quais dos 14 pontos
      condicionavam a saída de `draft`: **um** (224/225, critério 1) — os outros 13 condicionam
      a aplicação da norma, não a publicação. Falha se o status mudar aqui.
- [ ] 8. Escopo e URLs: `git diff --name-status -- content/` mostra **apenas**
      `M content/high-school/algebra/quadratic-equations/exercises.json` — nenhum `R`, nenhum
      `theory.*.md` (é o diff do TCK-0007), nenhum slug renomeado (L-003).
- [ ] 9. `bash scripts/audit-content.sh` **e** `bash scripts/validate-content.sh` → exit 0
      (capturados sem pipe). O log declara o **alcance**: nenhuma das duas verifica descrição
      de fórmula (L-012), e o auditor tem furos conhecidos (TCK-0017) — os critérios 1–6 se
      sustentam por leitura adversarial, não por exit 0.
- [ ] 10. O `exercises.json` continua com os mesmos **5 itens** e a mesma ordem; nenhum item
      novo, removido ou reordenado. Teste: lista de `id` na ordem, antes e depois, idêntica.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — critérios 5 e 6
- [x] Acessibilidade WCAG 2.2 AA (matemática acessível) — critérios 1, 2 e 3; é o ticket inteiro
- [ ] Funciona offline / PWA · [x] não aplicável — JSON estático, sem aplicação
- [x] Custo zero mantido — só texto
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [x] URLs de `content/` preservadas — critério 8
- [x] Correção matemática verificada — critérios 1 e 4 (o objeto lido é o objeto escrito, e
      nenhum gabarito é tocado)

## Fora de escopo

- **`theory.pt-BR.md` / `theory.en-US.md`** — os outros 8 pontos do inventário e os defeitos de
  rigor ($\Delta \ge 0$) são o **TCK-0007**. Diff disjunto (critério 8).
- **Alterar a norma** de leitura de fórmula: é o TCK-0006. Aqui só se aplica.
- **Mudar `status` para `published`**, reescrever enunciados, trocar exercícios, cobrir as
  `skills[]` declaradas sem exercício ou acrescentar itens até os 8–12 do
  `exercise-schema.md:107` — cada um é decisão de ticket próprio.
- `assessments.json` — não existe neste nó (`[007]` §2).

## Contexto e referências

- Origem: divisão do TCK-0007 registrada em `tickets/TCK-0007-pilot-node-rigor-and-a11y-fixes/log.md`
  `[003]`; inventário em `tickets/TCK-0006-formula-reading-conventions/log.md` `[007]` §2 e §3;
  consequência para o papel em `[007]` §4.
- **Dependência dura:** TCK-0006 entregue (a norma e os dois gatilhos). **Independente do
  TCK-0007** — arquivos distintos; podem correr em paralelo.
- **Reclassificação registrada:** o TCK-0005 `[011]` classificou as fórmulas inline como "não
  condiciona `draft`". Vale para 13 dos 14 pontos; **224/225 passa a condicionar**, porque
  `[007]` §2 mostrou que a leitura errada troca o polinômio — mesma classe da pendência 3
  (conteúdo didático inacessível). Justificativa em `TCK-0007/log.md` `[003]` (c).
- ADRs aplicáveis: `ADR-0002` (paridade obrigatória), `ADR-0001` (slug é URL pública),
  `ADR-0005` (as 3 referências do nó são CC BY-NC-SA: citáveis, nunca matéria-prima — L-009).
- Arquivos-alvo: `content/high-school/algebra/quadratic-equations/exercises.json` — **só este**.
- Lições relevantes: **L-021** (com o adendo: padrão de busca vem da **definição** da classe,
  nunca dos exemplos — critério 3); **L-012** (descrição de fórmula se confere por ordem);
  **L-013** (corrigir a linha citada não é corrigir a classe); **L-002** (gabarito não se toca
  sem verificação — critério 4); **L-003** (slug é URL); **L-001** (nasce bilíngue).
- Nós irmãos: 1 nó no acervo. Nada a propagar hoje; a regra já está em
  `.claude/agents/exercise-designer.md` e `.claude/skills/new-exercise-set/SKILL.md` (`[007]` §4),
  então o próximo conjunto de exercícios nasce conforme.

## Perguntas em aberto

- Nenhuma. A redação exata da marcação verbal é decisão do `exercise-designer` dentro da tabela
  normativa de `docs/content/accessibility.md`; divergência resolve-se no loop de review.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
