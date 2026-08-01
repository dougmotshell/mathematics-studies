# Contexto operacional — backend

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01

## Estado atual

- **Pipeline de conteúdo (2026-08-01, TCK-0014).** O contrato de carga de `content/` tem
  validador executável: `scripts/validate-content.py` (invólucro:
  `scripts/validate-content.sh`), com suíte em `scripts/validate-content-test.sh`
  (118 asserções). Python 3 stdlib, sem dependência de terceiros, sem vínculo com framework de
  aplicação: roda em linha de comando e em pipeline.
  - `python3 scripts/validate-content.py [--root DIR] [--json] [--quiet] [CAMINHO…]`
  - saída: `0` contrato íntegro · `1` violação · `2` erro de uso — os três preservados mesmo
    com `stdout`/`stderr` quebrados.
  - travessia **sempre recursiva**: validar um nó pai inclui os subnós.
  - `--root` no **pai** de `content/` é erro de uso (evita falso positivo de identidade).
  - o único nó real do acervo (`high-school/algebra/quadratic-equations`) passa limpo.
- **Ainda não integrado ao CI** — isso é a task 11 da spec `minimum-learning-slice`.
- Nenhuma persistência de progresso, conta ou API existe: RF-16/RNF-7 mantêm a fatia mínima
  sem servidor e sem dado de aluno.

## Pegadinhas conhecidas

- **Fixture de conteúdo dentro de `content/` quebra `audit-content.sh`.** Fixtures vivem em
  diretório temporário; o validador aceita `--root` justamente para isso, e é assim que a
  regra `nodeId` × caminho continua testável sem sujar o acervo.
- **`tolerance: 0` é válido; ausente e negativo não são.** Qualquer checagem por veracidade
  implícita (`if not item["tolerance"]`) reprova conteúdo correto. Vale para todo campo
  numérico em que zero tem significado.
- **`audit-content.py` usa veracidade implícita em `options[].correct`**: `"correct": "false"`
  (texto) é lido como alternativa correta. O validador reprova
  (`CORRECT-NOT-BOOLEAN`), mas as duas ferramentas divergem — não confiar só na auditoria.
- **`docs/content/exercise-schema.md` diz que `tolerance` deve declarar se é absoluta ou
  relativa; o arquivo real não declara.** **O validador não decide essa natureza**: exige só
  número finito ≥ 0, regra idêntica nas duas leituras (correção de 2026-08-01 — a redação
  anterior dizia "assume absoluta", registro mais forte do que o código). Fechar a decisão de
  contrato é do `tech-lead`, e precisa acontecer **antes** das tasks 5–8 da spec, onde a
  correção de resposta torna a escolha observável.
- **Um portão nunca para no alvo nem confia no canal de saída.** Ver L-019 e o adendo de
  reincidência: travessia recursiva sempre (subnó abaixo do alvo), proteção de código de saída
  em `stdout` **e** `stderr`, e saída forçada a UTF-8 para a mensagem não sumir em terminal
  ASCII.

## Decisões operacionais em vigor

- **As duas ferramentas de `content/` se sobrepõem de propósito** (descrição corrigida em
  2026-08-01 após o REJECT [006] do TCK-0014 — a versão anterior afirmava divisão estanque, o
  que era **falso**):
  - `scripts/audit-content.py` — auditoria editorial do acervo, e cobre bem mais: estrutura,
    taxonomia, unicidade de id de item, `skills`, grafo de pré-requisitos, trilhas,
    `references.json`, `status: published`, contagem de dicas.
  - `scripts/validate-content.py` — portão de carga (RF-18). **Repete** identidade do nó,
    gabarito, campos localizados e `answer`, que já existem no auditor: um portão de carga não
    pode depender de outra ferramenta ter rodado antes.
  - **Onde há sobreposição, o validador prevalece por ser o mais estrito.** Divergências
    medidas em 2026-08-01, ambas com o auditor mais permissivo: `"correct": "false"` (texto) e
    `title.en-US: 5` (não-texto) passam no `audit-content.py` e falham no validador. São
    defeitos do auditor, com **ticket próprio a abrir pelo `tech-lead`** — não se corrige
    `audit-content.py` a partir de um ticket de validador.
- **`references.json` não é validado aqui** — tem ticket próprio (TCK-0009).
- **Teste de ferramenta de linha de comando: bash + Python stdlib**, no molde de
  `tools/context-watch-test.sh`. Não há runner instalado e o `ADR-0003` não decidiu nenhum;
  o que se testa é a superfície de CLI (código de saída + texto da mensagem), que é o que o
  pipeline consome.
- **Mensagem de violação é contrato**: `arquivo: localizador: [REGRA] o que fazer`, com
  `items[i] (id=…)` e `options[j] (id=…)`. Mensagem sem localização é regressão.

## Validação do TCK-0014 (QA, 2026-08-01) — limites conhecidos do `validate-content.py`

O portão foi aprovado com 9/9 critérios, mas o `qa-validator#8` mediu **sete falsos negativos**
fora do RF-18 enumerado. Nenhum bloqueia; todos são invisibilidade ou sentinela, e em nenhum
deles o `audit-content.py` é mais estrito (cruzamento feito nas duas ferramentas, em cópia
isolada do repositório). Consultar esta lista **antes** de acrescentar regra ou de confiar no
portão para um lote novo de conteúdo:

- **D-1 (a mais urgente) — inteiro ≥ 10^309 em `answer`/`tolerance` derruba o validador.**
  `validate-content.py:438` e `:452` chamam `float(...)` sem proteção → `OverflowError`,
  traceback, **zero violações listadas**, execução do acervo abortada; com canal quebrado o
  código vira **120** (sintoma do B2 num caminho fora de `emit`/`emit_err`). Limiar medido:
  10^308 passa, 10^309 quebra; `1e400` em notação float é tratado certo. Gatilho: o primeiro
  item `numeric` com inteiro fora da faixa de `float` (`number-theory`, `research`). Correção
  de duas linhas (`try/except OverflowError` → `NUMERIC-ANSWER-NOT-FINITE`). Resolver antes de
  o `prebuild` do TCK-0015 virar bloqueio de release.
- **D-2 — `str.strip()` não remove espaço de largura zero.** `title.en-US = "​"` (ou
  `⁠`, `﻿`) passa em `LOCALIZED-EMPTY`: um nó monolíngue na prática atravessa o
  portão bilíngue. NBSP e `\t\n` são pegos corretamente.
- **D-3 — `answer` inútil passa em `short-answer`/`ordering`.** `"   "`, `false` e `0` passam;
  `""` reprova. O teste é `item["answer"] in (None, "", [], {})`, que é presença, não utilidade.
- **D-4 — `proof`/`step-by-step` sem `rubric`** (obrigatório em
  `docs/content/exercise-schema.md:80`) não tem regra nenhuma no validador; o auditor só emite
  AVISO. Nenhum dos dois barra.
- **D-5 — `None` significa duas coisas.** `load_json` devolve `None` para arquivo ausente **e**
  para arquivo cujo conteúdo é `null`; `validate_exercise_file:524` trata os dois como ausente,
  então `exercises.json` contendo `null` sai como "Contrato íntegro". É um desvio de 4
  caracteres na regra `ITEMS-EMPTY` (`[]` reprova, `null` passa). `exercises.json` como symlink
  quebrado tem o mesmo efeito.
- **D-6 — `seen_ids` é por arquivo** (`:554`): o mesmo `id` de item em `exercises.json` e em
  `assessments.json` passa nas **duas** ferramentas.
- **D-7 — diretório só com `theory.*.md` é invisível às duas ferramentas**
  (`audit-content.py:88-90` reconhece nó só por `meta.json`; o validador, por `meta.json` ou
  arquivo de exercícios). Teoria monolíngue solta não é checada por ninguém.
- **D-8 — cobertura real: 1 nó, 5 itens, só `multiple-choice` e `numeric`.** Ficam **seis**
  tipos sem exemplar real, não quatro: `matching`, `ordering`, `proof`, `step-by-step` e também
  **`short-answer`** e **`true-false`**. `true-false` é justamente onde o `audit-content.py`
  diverge (o `>1` corretas é checado só para `multiple-choice`, `:236`).

**Confirmado como verdadeiro** (não mexer sem motivo): a fronteira do cabeçalho e a seção
"Decisões operacionais" acima resistiram ao ataque — em nenhuma das mutações do QA houve
`audit=1 · validate=0`. O `assessments.json` é varrido de verdade. `ITEMS-EMPTY` e
`JSON-DUPLICATE-KEY` não contradizem o schema (a regra 8 já exige 8–12 itens), mas o
`ITEMS-EMPTY` é **assimétrico**: nó sem `exercises.json` passa, com `items: []` reprova, com
`null` passa de novo.
