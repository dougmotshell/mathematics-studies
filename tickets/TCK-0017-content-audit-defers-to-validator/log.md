# Log — TCK-0017

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 19:20 — tech-lead
- Ação: criação do ticket a partir do achado e da pendência 1 entregues pelo `qa-validator#8`
  em `tickets/TCK-0014-content-contract-validator/log.md` `[010]`, com as duas passagens de
  origem copiadas verbatim.
- Motivo: o TCK-0014 está `done` e não reabre (regra 5 de `tickets/README.md`). O defeito é de
  **outro artefato** (`scripts/audit-content.py`), reproduzido e medido lá, e vem em ticket
  próprio que o referencia.
- Resultado: ok — `tickets/TCK-0017-content-audit-defers-to-validator/` criado. Nenhum arquivo
  de `scripts/`, `content/`, `docs/` ou `.github/` tocado nesta ação.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 19:22 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Tipo `bug`** e não `infra`: o comportamento observado é errado, não ausente — o auditor
  **afirma** `0 erros` sobre conteúdo que viola o contrato. Por isso o ticket tem seção de
  Reprodução, com as quatro mutações, o controle e o ambiente da medição.
- **Prioridade P1.** Prazo relativo, que é o que este projeto consegue verificar: **antes do
  primeiro lote grande de conteúdo**. Hoje o acervo tem 1 nó e 5 itens; o auditor é o passo
  do CI de conteúdo (`ai-surface-audit.yml:51`) e é o comando que o autor roda à mão. Um
  auditor que diz "íntegro" sobre gabarito marcado errado não erra na direção conservadora:
  erra deixando passar (L-015 — falso silêncio é indistinguível de "está tudo bem").
- **Tamanho M.** A superfície é um arquivo de ~350 linhas e a mudança principal é **remoção**
  (delegar), não escrita. O custo real está nas fixtures: 4 (critério 1) + 10 (critério 2) +
  7 (critério 4) + 6 execuções (critério 5) + a matriz de canais e travessia (critério 7).
- **Owner `backend-developer`** — `scripts/` de pipeline de conteúdo é a área dele
  (`AGENTS.md` §10: "Dados, progresso, pipeline de conteúdo, APIs"). É o mesmo agente que
  escreveu `validate-content.py` no TCK-0014: **execução** por quem conhece a fronteira é
  desejável; a independência que a regra 4 protege é a de **revisão**, e nem o
  `code-reviewer` nem o `qa-validator` desta cadeia escreveram qualquer das duas ferramentas.
- **Cadeia:** `tech-lead` → `backend-developer` → `code-reviewer` → `qa-validator`.
  Sem revisor de conteúdo: o ticket não toca `content/` (critério 6) nem `docs/` (critério 10).

### Decisão de recorte — corrigir × delegar

Registro aqui o **porquê**, já que é o miolo do ticket e a parte que um executor poderia
desfazer sem perceber.

O pedido chega como "quatro bugs". Não é. Quatro bugs no mesmo arquivo, com três causas
distintas (`o.get("correct")`, `str(…)`, `>1` só para um tipo) e **um** efeito comum —
divergir do validador sobre o mesmo byte — são sintoma de uma decisão estrutural nunca tomada:
**qual das duas ferramentas é dona do contrato de arquivo**. Enquanto as duas opinarem, a
correção de hoje é a divergência de amanhã, porque nada obriga as duas a evoluírem juntas. É
literalmente a classe que L-013, L-018 e o adendo da L-019 já cobraram deste projeto: corrigir
a lista de casos citados em vez da classe.

**Delegar.** `validate-content.py` passa a ser a fonte única sobre "este arquivo pode ser
carregado?"; `audit-content.py` para de opinar sobre isso e fica com o que só ele faz — grafo
de pré-requisitos, `references.json`, `content/paths/`, presença de arquivos do nó, portões de
`published` (incl. `verified`, L-002) e cobertura de `skills[]`. Os dois papéis continuam
existindo porque respondem perguntas diferentes: um é portão de **build** (por nó,
`prebuild`), o outro é portão **editorial** (entre nós, coerência do acervo).

Três fatos medidos sustentam que delegar **não perde cobertura** — nenhum é presunção minha:

1. O `qa-validator#8` atacou as duas ferramentas com sete fixtures de burla e registrou
   "Nenhum dos sete tem o auditor como o mais estrito — `audit=0 · validate=0` em todos".
   Não existe caso conhecido em que o auditor pegue algo do contrato de arquivo que o
   validador deixe passar.
2. A fronteira já está no código: nenhum código de regra do validador
   (`grep -oE '"[A-Z][A-Z0-9-]{3,}"` → 40 códigos) fala de grafo, referências ou trilha.
   As funções `check_prerequisites:286`, `check_paths:319`, `check_references:264` e
   `check_theory:149` são exclusivas do auditor por construção.
3. A prova de não-regressão não fica no meu argumento: virou o **critério 4**, com sete
   fixtures nomeadas que precisam continuar reprovando **no auditor**.

**O que eu deliberadamente não decidi** (L-011 — o ticket fixa a restrição e o resultado, não
o mecanismo): se a delegação é `import`, subprocesso ou composição em `audit-content.sh`. Os
três atendem à invariante do critério 2; a escolha e a razão vão para o log do executor. Se eu
escolhesse, estaria decidindo arquitetura de ferramenta pelo agente cuja área é essa.

**Invariante que define "não diverge"** (critério 2, automatizada): para qualquer entrada,
`validate-content` sair `1` e `audit-content` sair `0` é **proibido**. É mais fraca que
"vereditos idênticos" — de propósito: o auditor tem regras próprias e avisos que o validador
não tem, e exigir igualdade os fundiria numa ferramenta só, matando o portão editorial. E é
mais forte que "as quatro instâncias corrigidas", porque vale para toda entrada, inclusive as
que ninguém escreveu ainda. O critério 2 ainda exige provar que o teste **reprova** quando a
invariante é violada de propósito — teste que não falha não é teste (L-015).

### O que entrou de fora do pedido, e por quê

- **`ITEMS-EMPTY` assimétrica** (critério 5). O QA pediu no ponto de julgamento (a) que "quem
  reconcilia o schema decida isso junto". Discordo do endereço: `exercises.json` **ausente**
  passar, `[]` reprovar e `null` (D-5) voltar a passar é a **mesma classe** deste ticket — o
  veredito mudando por uma diferença de 4 caracteres, e mudando entre as duas ferramentas.
  Entra aqui como *simetria* (os três estados dão o mesmo par exit/regra nas duas
  ferramentas); **qual** veredito é decisão do executor contra a norma escrita
  (`exercise-schema.md:107`: 8–12 itens, logo vazio é violação), e a documentação do schema
  continua sendo do `docs-writer`, que recebe a decisão deste log.
- **Classes da L-019 aplicadas ao auditor** (critério 7). O validador foi endurecido em
  travessia, canais e codificação no TCK-0014; o auditor nunca foi. Delegar sem isso apenas
  move o ponto cego: um auditor que perde o código de saída em `| head` continua aprovando em
  silêncio o que o validador reprovou.
- **Critério 9** (suíte 118/118 e md5 do validador). Delegar cria a tentação de "ajustar
  levemente" o artefato já `done`. Se for preciso, que seja nominal e justificado.

### O que ficou de fora, com o gatilho

Os sete falsos negativos do validador **não são divergência** — as duas ferramentas concordam
neles, e concordar errado é outro problema. Ficam fora, com os gatilhos que o QA já escreveu:
D-1 (overflow: primeiro `numeric` com inteiro ≥ 10^309, plausível em `number-theory`), D-2
(vazio de largura zero: nó monolíngue atravessando o portão bilíngue), D-3, D-4 (`rubric`:
primeiro nó real com `proof`/`step-by-step`), D-6, D-8. **D-5 entra** só pela assimetria.
**D-7** (diretório só com `theory.*.md`) fica fora por razão de área, não de esforço: mudar
`find_nodes` muda o que **conta como nó**, e isso é `docs/content/taxonomy.md` +
`curriculum-architect`.

- **Aderência ao plano:** Fase 1 do roadmap. O RF-18 da spec `minimum-learning-slice` exige
  validação de contrato na carga e diz que falha silenciosa é defeito — este ticket é
  exatamente a falha silenciosa que sobrou fora do validador.
- **Requisitos inegociáveis conferidos:** bilinguismo (as instâncias 2 e 3 são furos de
  paridade — `ADR-0002`); custo zero (critério 8, zero dependência); URLs preservadas
  (critério 6, `content/` intocado); correção matemática (L-002 — é o gabarito que estava
  atravessando); a11y, offline e privacidade não aplicáveis, com o porquê no ticket.
- **Dependências:** nenhuma dura. Depende de artefatos já `done` (TCK-0014). **Conflito de
  working tree** se rodar junto com TCK-0015 (`package.json`, `src/`) — não há sobreposição de
  arquivo, mas os dois mexem no caminho `prebuild`; rodar em série é mais seguro.
- Resultado: ok — `status: triaged`, `owner: backend-developer`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
