---
id: TCK-0007
title: Corrigir os defeitos de rigor e de acessibilidade que prendem o nó piloto em draft
type: content
status: triaged
owner: content-author
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0005, TCK-0006, TCK-0018]
---

# TCK-0007 — Corrigir os defeitos de rigor e de acessibilidade que prendem o nó piloto em draft

## Pedido original (verbatim)

> 1. Hipótese `\Delta \ge 0` ausente no enunciado (48/47), no Resumo (143/140) e em soma e
>    produto (144/141) — **condiciona `draft`** (L-014).
> 2. Descrição preexistente incompleta (53/52) — **condiciona `draft`**: enquanto existir, o nó
>    viola `AGENTS.md` §9.2 em 1 dos 8 blocos, ainda que o critério 1 deste ticket não a alcance.
>    Julgamento (a) acima; severidade menor que a estimada em `[008]`, mas real.
> 3. Tabela "Erros comuns" (133/130) contrasta duas frações cujo único diferencial é o
>    agrupamento — lido linearmente, o contraste desaparece e a lição fica inacessível
>    justamente para quem depende de leitura linear. **Condiciona `draft`** (é conteúdo
>    didático inacessível, não melhoria).
> 4. `\dfrac` inline no Resumo e 10 `\frac` inline em `exercises.json` — decisão de **regra**
>    (`AGENTS.md` §9.2 deve cobrir inline?). Não condiciona `draft`; condiciona a regra.

— `tickets/TCK-0005-pilot-node-math-accessibility/log.md` `[011]`, "Pendências herdadas (7)".

> **Encaminhamento ao `tech-lead`: abrir ticket próprio** (tipo `content`, P2, tamanho P) com
> o seguinte escopo mínimo, a ser decidido lá e não aqui: `theory.pt-BR.md:48` /
> `theory.en-US.md:47` — enunciar a hipótese na própria oração, na linha de "Se `a \neq 0` e
> `\Delta \ge 0`, as soluções reais … ; se `\Delta < 0`, não há solução real (e há duas em
> `\mathbb{C}`)". A tabela de sinais permanece como está.

— `tickets/TCK-0005-pilot-node-math-accessibility/log.md` `[006]`.

## Requisito refinado

Quem sofre: (a) o estudante que usa leitor de tela — hoje 1 dos 8 blocos do teorema central
tem metade muda, e a lição de erro comum sobre agrupamento desaparece na leitura linear;
(b) todo nó futuro — o piloto é o **modelo** declarado em `meta.json` (`"notes"`), e a
imprecisão de enunciar a fórmula resolutiva sem condicionar a $\Delta \ge 0$ se propaga por
cópia (L-014); (c) o `qa-validator` do dia da publicação, que hoje não conseguiria fechar o
checklist de `published` de `docs/content/content-standards.md`.

Resultado esperado: o nó `high-school/algebra/quadratic-equations` deixa de ter defeito
conhecido que impeça a saída de `status: "draft"` — sem que este ticket decida publicar.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. O enunciado do teorema (`theory.pt-BR.md:48` / `theory.en-US.md:47`) condiciona a
      fórmula resolutiva a $\Delta \ge 0$ **na própria oração** e diz o que ocorre quando
      $\Delta < 0$. Teste: lida **isolada da tabela de sinais**, a sentença não afirma nem
      sugere existência de raiz real para $\Delta < 0$. Verificado pelo `math-reviewer`, que
      não escreveu a nova redação.
- [ ] 2. A mesma condição aparece no Resumo (`pt-BR:143` / `en-US:140`) e na linha de soma e
      produto (`pt-BR:144` / `en-US:141`), esta última condicionada à existência das raízes
      reais (o corpo do texto já o faz corretamente em 64/62). Teste: `grep` das três linhas
      → nenhuma afirma a fórmula ou as relações de forma incondicional.
- [ ] 3. A descrição de leitura do bloco de duas partes (`pt-BR:51-53` / `en-US:50-52`) lê
      **as duas** fórmulas, incluindo $\Delta = b^2 - 4ac$. Teste de reconstrução: a partir
      **apenas** do texto da leitura é possível reescrever o bloco inteiro; feito pelo
      `a11y-ux-reviewer`, às cegas, e a reconstrução é registrada no log.
- [ ] 4. A célula da tabela "Erros comuns" (`pt-BR:133` / `en-US:130`) enuncia **em palavras**
      a diferença de agrupamento entre $\frac{-b \pm \sqrt{\Delta}}{2a}$ e
      $-b \pm \frac{\sqrt{\Delta}}{2a}$. Teste: lendo só o texto da célula (sem ver o LaTeX),
      o revisor reconstrói **duas** expressões distintas e diz qual é a errada. Falha se a
      distinção depender de enxergar a barra de fração.
- [ ] 5. Cada ocorrência **de `theory.pt-BR.md` / `theory.en-US.md`** do inventário corrente
      do TCK-0006 — `tickets/TCK-0006-formula-reading-conventions/log.md` `[007]` §2, tabela
      "`theory.pt-BR.md` / `theory.en-US.md` — 8 pontos (4 por idioma)", que **substitui** a
      contagem de `[004]` §4 — está tratada conforme a regra decidida lá, e o log registra o
      par ocorrência → ação, inclusive os "nada a fazer" com o motivo. Falha se qualquer
      ocorrência daquela tabela (inclusive as marcadas "não exige" e "ATENDIDO como está")
      ficar sem veredito. As 14 ocorrências de `exercises.json` **não** são deste ticket —
      são o **TCK-0018**. O ponteiro é a fonte; nenhuma lista é copiada para cá.
- [ ] 6. Paridade pt-BR/en-US: toda alteração existe nos **dois** arquivos, na mesma seção e
      na mesma ordem; nenhuma informação em um idioma só. Teste (L-012 — por ordem, não por
      contagem): `grep -n '^\$\$\|^\*Leitura:\*' theory.pt-BR.md` e
      `grep -n '^\$\$\|^\*Reading:\*' theory.en-US.md` mostram alternância estrita, mesmo
      número de pares, sem bloco órfão. Verificado pelo `i18n-steward`.
- [ ] 7. Correção matemática: todo valor ou passo alterado é reverificado (`/math-verify` ou
      aritmética exata em Python), com a saída no log. Nenhuma afirmação nova entra sem
      verificação.
- [ ] 8. `meta.json` continua com `status: "draft"` e o log traz o checklist de `published`
      de `docs/content/content-standards.md` **item a item**, com o estado de cada um após a
      entrega. Falha se o status mudar aqui: publicar é decisão de ticket próprio.
- [ ] 9. Escopo e URLs: `git diff --name-status -- content/` mostra apenas `M` (nenhum `R`),
      restrito ao nó `high-school/algebra/quadratic-equations`; nenhum slug renomeado (L-003).
- [ ] 10. `bash scripts/audit-content.sh` **e** `bash scripts/validate-content.sh` → exit 0
      (capturados sem pipe; o auditor com `0 erros · 0 avisos`). Declarar no log o **alcance**:
      o auditor não verifica descrição de fórmula (L-012) e, desde o TCK-0014 `[010]`,
      sabe-se que ele aceita em silêncio `"correct": "false"` e título não-string (**TCK-0017**)
      — exit 0 do auditor **não** é evidência de contrato íntegro. Os critérios 1–6 se
      sustentam por leitura adversarial, não por exit 0.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — critério 6, obrigatório em toda alteração
- [x] Acessibilidade WCAG 2.2 AA (inclui matemática acessível) — critérios 3, 4 e 5
- [ ] Funciona offline / PWA · [x] não aplicável — markdown estático, sem aplicação
- [x] Custo zero mantido — só texto; nenhuma dependência ou asset novo
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [x] URLs de `content/` preservadas — critério 9
- [x] Correção matemática verificada — critérios 1, 2 e 7

## Fora de escopo

- **Mudar `status` para `published`** — decisão de ticket próprio, com o checklist completo
  (exercícios cobrindo todas as `skills[]`, revisão final) e não só as pendências herdadas.
- Reescrever partes do nó não listadas nos critérios; o texto aprovado em TCK-0005 fica.
- Alterar a **regra** de fórmula inline: é o TCK-0006. Aqui só se **aplica** o que lá ficou
  decidido.
- **Tocar `exercises.json`** — as 14 ocorrências do inventário `[007]` §2 (7 por idioma),
  inclusive a de 224/225, são o **TCK-0018** (`exercise-designer`). Artefato de outra área e
  diff disjunto: `git diff --name-only -- content/` deste ticket não pode listar
  `exercises.json`.
- Renderização/MathML e parte 2 do `/a11y-audit` — dependem da aplicação, que não existe.

## Contexto e referências

- Origem: `TCK-0005/log.md` `[006]` (veredito do enunciado), `[008]` §7 itens 1-3,
  `[010]` pendências 1-4, `[011]` "Pendências herdadas" 1-4 e "Pontos de julgamento" (a) e (b).
- **Dependência dura:** o critério 5 exige o TCK-0006 entregue (critério 7 de lá). O
  inventário corrente é `TCK-0006/log.md` `[007]` §2 — **22 pontos**, dos quais **8 aqui**
  (`theory.*.md`) e 14 no TCK-0018 (`exercises.json`).
- ADRs aplicáveis: `ADR-0002` (paridade obrigatória), `ADR-0001` (slug é URL pública),
  `ADR-0005` (nenhum trecho de fonte NC incorporado — as 3 referências do nó são NC).
- Arquivos-alvo: `content/high-school/algebra/quadratic-equations/theory.pt-BR.md` e
  `theory.en-US.md` — **só estes dois**. `exercises.json` saiu do escopo (TCK-0018).
- Lições relevantes: **L-014** (hipótese pertence ao enunciado — é a lição que originou o
  item 1); **L-012** (descrição de fórmula se confere por ordem); **L-003** (slug é URL);
  **L-002** (verificar antes de publicar resposta); **L-009** (fonte NC é leitura, não
  matéria-prima).
- Nós irmãos: `find content -name meta.json` → **1 nó**. Não há propagação a corrigir hoje;
  o risco é futuro, e é por isso que a correção entra antes de o modelo ser copiado.

## Perguntas em aberto

- Nenhuma. A redação exata do enunciado é decisão do `content-author` dentro da forma
  sugerida em `[006]`; divergência com o `math-reviewer` resolve-se no loop de review.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
