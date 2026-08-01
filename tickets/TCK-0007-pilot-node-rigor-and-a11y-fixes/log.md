# Log — TCK-0007

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:36 — tech-lead
- Ação: criação do ticket a partir das pendências 1, 2, 3 e 4 do TCK-0005 (`log.md` `[006]`,
  `[008]` §7, `[010]`, `[011]`), com os trechos de origem copiados verbatim.
- Motivo: as quatro pendências foram classificadas pelo `qa-validator#3` em `[011]` como
  **condicionantes da saída de `draft`** (1, 2 e 3) e como dependente de regra (4). O
  TCK-0005 está `done` e não reabre (regra 6 de auditoria) — a correção vem em ticket novo
  que o referencia.
- Resultado: ok — `tickets/TCK-0007-pilot-node-rigor-and-a11y-fixes/` criado. Nenhum arquivo
  de `content/` tocado nesta ação (`git status --short content/` → vazio).
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:38 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** as quatro pendências caem nos **mesmos dois
  arquivos** do mesmo nó, todas condicionam o mesmo evento (sair de `draft`) e exigem a mesma
  cadeia de revisão tripla — separá-las por severidade produziria três tickets disputando o
  mesmo diff, com risco de conflito e de paridade quebrada.
- **Divergência deliberada do encaminhamento de `[006]`:** o `math-reviewer` sugeriu "P2,
  tamanho P" para o item 1 isolado. Triado como **P1/M** porque o ticket agrega quatro itens,
  três deles declarados condicionantes de `draft` pelo QA, e porque o nó é o modelo dos 3–5
  nós piloto da Fase 1 — corrigir depois da cópia custa N vezes mais. Registro a mudança aqui
  em vez de alterar silenciosamente o critério de outro agente.
- **Tipo:** `content`. Toca só `content/` (e `exercises.json` se o TCK-0006 assim decidir).
- **Prioridade P1 · tamanho M.** M e não P: são 2 arquivos × 4 pontos, mais a possível
  varredura de `exercises.json`, com paridade obrigatória em cada alteração.
- **Owner: `content-author`.** É quem escreve teoria didática bilíngue. Os revisores que
  **diagnosticaram** os defeitos (`math-reviewer`, `a11y-ux-reviewer`) não escrevem a
  correção — assim continuam elegíveis para revisá-la.
- **Cadeia:** `tech-lead` → `content-author` → (`math-reviewer` ‖ `a11y-ux-reviewer` ‖
  `i18n-steward`, em paralelo) → `qa-validator`. `curriculum-architect` **dispensado**: não há
  mudança de taxonomia, pré-requisito ou dificuldade. Divisão de critérios entre os revisores:
  1, 2 e 7 → `math-reviewer`; 3, 4 e 5 → `a11y-ux-reviewer`; 6 → `i18n-steward`.
  Independência: nenhum deles produziu o texto que vai julgar.
- **Restrições passadas ao executor:**
  1. **Não começar antes do TCK-0006 entregue** — o critério 5 depende do veredito por
     ocorrência registrado lá. Se a execução for autorizada antes, o ticket entra
     `blocked` no critério 5 e entrega os demais.
  2. Toda alteração nos **dois** idiomas, no mesmo ciclo (ADR-0002 / L-001). Nada de
     "traduzo depois".
  3. Não renomear slug nem caminho (L-003) e não mudar `status` em `meta.json`.
  4. As 3 referências do nó são **CC BY-NC-SA** → só citáveis: nenhum trecho, exemplo ou
     sequência didática delas pode entrar no texto da correção (`AGENTS.md` §9.7, L-009).
  5. `git diff -- content/` tem de continuar restrito ao nó piloto.
- **Aderência ao plano:** Fase 1 do roadmap ("provar o formato com conteúdo real"). O nó
  piloto é o artefato dessa fase; sair de `draft` é o marco. Dentro do plano.
- **Requisitos inegociáveis conferidos:** bilinguismo (critério 6), acessibilidade (3, 4, 5),
  correção matemática (1, 2, 7), gratuidade (só texto), URLs preservadas (9); offline e
  privacidade não aplicáveis, com o porquê registrado no ticket.
- **Dependências:** depende de `TCK-0006` (critério 5). Não depende do `TCK-0009`
  (`references.json`) — são arquivos e defeitos distintos.
- Resultado: ok — `status: triaged`, `owner: content-author`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.

## [003] ACTION — 2026-08-01 19:10 — tech-lead
- Ação: **re-escopo** do ticket a pedido da cadeia do TCK-0006 (três pontos do revisor: (a)
  ponteiro do critério 5, (b) `size` diante de 22 pontos, (c) tratamento de
  `exercises.json:224/225`). Editado o `ticket.md`; `[001]` e `[002]` **não** foram tocados
  (log append-only) — esta entrada é a fonte corrente do escopo.
- Motivo: o inventário que dimensiona este ticket mudou. `TCK-0006/log.md` `[007]` §2 fixa
  **22 pontos** (8 em `theory.*.md`, 14 em `exercises.json`), confirmados em duas recontagens
  independentes, contra os 18 de `[004]` §4. Escopo dimensionado por número obsoleto é escopo
  errado.

### (a) Critério 5 — ponteiro no lugar do parêntese

O critério **não estava quebrado**: ele já referenciava "o critério 7 do TCK-0006". O defeito
era o parêntese explicativo (`\dfrac` do Resumo + "as 10 `\frac` de `exercises.json`"), que
enumerava o conjunto **antigo e menor** e, lido isolado, contradizia o ponteiro. Ponteiro e
cópia divergem sempre que a fonte muda; quem lê acredita na cópia, que está ao alcance dos
olhos. Trocado por ponteiro nominal à tabela de `[007]` §2, com a nota de que ela
**substitui** `[004]` §4 e de que "não exige" e "ATENDIDO como está" também exigem veredito
registrado. **Nenhuma lista foi copiada para o `ticket.md`** — a fonte continua sendo uma só.

### (b) `size` — reavaliado, e a resposta foi dividir, não engordar

22 pontos com paridade obrigatória não cabem em `M`. Mas antes do tamanho há um problema de
**área**: 14 dos 22 pontos estão em `exercises.json`, artefato do `exercise-designer`
(`AGENTS.md` §10) — mantê-los aqui obrigaria o `content-author` a editar a área de outro
agente. Aplicado o critério da minha própria memória (agrupar por **artefato + evento que a
pendência condiciona**):

| Ticket | Artefato | Pontos | Evento que condiciona | Owner |
|---|---|---|---|---|
| TCK-0007 (este) | `theory.pt-BR.md` · `theory.en-US.md` | 8 | sair de `draft` | `content-author` |
| **TCK-0018** (novo) | `exercises.json` | 14 | sair de `draft` (só 224/225) · aplicar a norma (13) | `exercise-designer` |

Diffs disjuntos, sem dependência entre os dois, revisores independentes em cada um. Com o
recorte, **`size: M` se mantém aqui** (2 arquivos, 8 pontos, 4 defeitos de rigor/a11y) — a
alternativa era um `G` de 3 arquivos cruzando duas áreas. Registro a divergência: sem a
divisão, este ticket seria `G`.

### (c) `exercises.json:224/225` — entra como prioritário, mas **não** como correção matemática

`$x^2 + 6x + 9 = (x+3)^2 = 0$` está **matematicamente correto** — não há afirmação falsa a
corrigir, e nenhuma verificação numérica acusaria nada. O defeito é de **acessibilidade com
consequência matemática**: lido linearmente, "x mais três ao quadrado" descreve tanto
$(x+3)^2$ quanto $x + 3^2$, que são polinômios diferentes — é o único ponto do lote de 22 em
que a leitura errada **muda o objeto**, não a estética. Classificar como "erro matemático"
mandaria o executor procurar uma conta errada que não existe; classificar como "estilo inline"
o rebaixaria a melhoria. Fica como **defeito de a11y com teste matemático**.

Consequências, todas no **TCK-0018** (não aqui):
1. É o **critério 1** de lá, e o único dos 14 pontos que **condiciona `draft`**. Reclassifico
   aqui a pendência 4 do TCK-0005 `[011]` ("não condiciona `draft`"): ela foi julgada quando o
   item era "10 `\frac` inline", antes de `[007]` §2 revelar a ocorrência de 224/225. É a mesma
   classe da pendência 3 (conteúdo didático inacessível), e não uma questão de regra. Mudança
   de critério registrada, não silenciosa.
2. **Cadeia:** o `math-reviewer` passa a ser obrigatório no TCK-0018 — que sem isso teria só
   `a11y-ux-reviewer` + `i18n-steward` —, porque o teste de aceite ("a partir só das palavras,
   o revisor escreve **um** polinômio, e é $(x+3)^2$") é juízo matemático, não tipográfico.
   Assinatura dupla: `math-reviewer` **e** `a11y-ux-reviewer`, às cegas, sem ver o LaTeX.
3. **Aqui a cadeia não muda.** O `math-reviewer` continua com os critérios 1, 2 e 7 (hipótese
   $\Delta \ge 0$) — nenhum deles alcança `exercises.json`.

### Outras edições no `ticket.md`

- Critério 10 passa a exigir também `bash scripts/validate-content.sh` exit 0, e a declarar
  que exit 0 do auditor não é evidência de contrato íntegro — o auditor aceita em silêncio
  `"correct": "false"` e título não-string (TCK-0014 `[010]`, agora **TCK-0017**).
- "Fora de escopo" ganha `exercises.json` → TCK-0018, com teste (`git diff --name-only`).
- "Arquivos-alvo" reduzido aos dois `theory.*.md`; `related` e a dependência dura atualizados.
- Status permanece **`triaged`**, sem `HANDOFF` (L-005). Owner inalterado.
- Resultado: ok — escopo de 22 → 8 pontos aqui; `git status --short content/` → vazio.
- Lição: n/a — não resolve `REJECT`.
