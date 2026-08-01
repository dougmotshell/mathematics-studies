# Log — TCK-0014

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 15:20 — tech-lead
- Ação: ticket criado a partir do pedido "inicie a implementação do projeto".
- Motivo: o `task-router` encerrou o dev-loop `start-implementation` com saída antecipada —
  implementação da fatia mínima é trabalho de ticket, não de dev-loop (AGENTS.md §10). O
  recorte adotado é **um ticket por task** de `docs/specs/minimum-learning-slice/tasks.md`,
  para não obrigar dois agentes a compartilhar log e diff.
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 15:20 — tech-lead
- Ação: triagem. Critérios de aceite derivados do critério de pronto da task na spec
  aprovada, sem alargar escopo.
- Cadeia: agente da área → `code-reviewer` → `qa-validator`.
- Paralelismo: este ticket e o par (TCK-0013 ‖ TCK-0014) rodam ao mesmo tempo — `tasks.md`
  declara as tasks 3 e 4 paralelizáveis, e as áreas não se sobrepõem.
- Restrições: nenhuma decisão de framework (o `ADR-0003` decidiu site estático com ilhas e
  deixou UI/build/testes em aberto); `content/`, spec e ADRs intocados.
- Resultado: ok — `triaged`.

## [003] HANDOFF — 2026-08-01 15:20
- De: tech-lead → Para: backend-developer
- Status novo: in_progress
- O que foi feito: task da spec recortada em ticket com critérios verificáveis.
- Artefatos: `tickets/TCK-0014-content-contract-validator/ticket.md`.
- Como validar: critérios do ticket + auditorias determinísticas.
- Pendências e riscos: a spec herdou três decisões humanas adiadas (exibir nó `draft`, forma
  da URL bilíngue, rótulo no índice) — elas afetam o desenho e não podem ser fechadas por
  agente.
- Critérios de aceite: [ ] todos restantes.

## [004] ACTION — 2026-08-01 16:21 — backend-developer

- Ação: implementado o validador do contrato de carga de `content/` (RF-18) e a suíte que
  o exercita. Artefatos novos, nada removido nem alterado fora deles:
  - `scripts/validate-content.py` — validador (Python 3 stdlib, sem dependência de terceiros);
  - `scripts/validate-content.sh` — invólucro, no mesmo padrão de `audit-content.sh`;
  - `scripts/validate-content-test.sh` — suíte de 84 asserções.

### Desenho: por que um validador separado de `audit-content.py`

`audit-content.py` é auditoria **editorial** (presença de arquivo e campo, taxonomia, grafo
de pré-requisitos, trilhas, `references.json`, unicidade de id, contagem de dicas). Este é o
**portão de carga**: só as regras semânticas de que a renderização depende — gabarito
resolvível, resposta numérica comparável, paridade bilíngue campo a campo e identidade do nó
coerente com a URL pública. A fronteira está escrita no cabeçalho do arquivo para não haver
duplicação futura. Nada de `references.json` (é o TCK-0009) e nada de teoria (já coberta).

Regras nomeadas (o identificador entra na mensagem): `META-ID-MISMATCH`, `NODE-ID-MISMATCH`,
`LOCALIZED-{NOT-OBJECT,MISSING-LANG,NOT-STRING,EMPTY,UNKNOWN-LANG}`, `MC-NO-CORRECT-OPTION`,
`MC-MULTIPLE-CORRECT-OPTIONS`, `CHOICE-NO-CORRECT-OPTION`, `OPTIONS-MISSING`,
`OPTION-{NOT-OBJECT,ID-MISSING,ID-DUPLICATE,FEEDBACK-MISSING}`, `CORRECT-NOT-BOOLEAN`,
`NUMERIC-ANSWER-{MISSING,NOT-NUMBER,NOT-FINITE}`,
`NUMERIC-TOLERANCE-{MISSING,NOT-NUMBER,NEGATIVE,NOT-FINITE}`, `ANSWER-MISSING`,
`ITEM-{NOT-OBJECT,ID-MISSING,TYPE-MISSING,TYPE-UNKNOWN,FIELD-MISSING}`, `ITEMS-MISSING`,
`HINTS-NOT-LIST`, `JSON-INVALID`, `NODE-META-MISSING`, `META-NOT-OBJECT`,
`META-FIELD-MISSING`, `FILE-UNREADABLE`.

Interface: `python3 scripts/validate-content.py [--root DIR] [--json] [--quiet] [CAMINHO…]`.
Sem argumento valida o acervo; com argumento aceita nó, subárvore ou raiz alternativa.
Saída `0` íntegro · `1` violação · `2` erro de uso. `--root` existe para que fixtures vivam
fora de `content/` — sem ele, a checagem `nodeId` × caminho não teria como ser testada sem
sujar o acervo. Não há import de framework, servidor nem build: roda em linha de comando e
em pipeline.

### Escolha do mecanismo de teste (critério 7)

**bash + Python stdlib**, no molde de `tools/context-watch-test.sh`. Justificativa: (a) o
`ADR-0003` não decidiu runner e o ticket proíbe dependência nova — `pytest` está fora;
(b) o repositório já tem esse precedente, então não introduzo um segundo estilo de teste;
(c) o que os critérios 1, 3 e 5 julgam é a superfície de **linha de comando** — código de
saída e texto da mensagem —, não funções internas: `unittest` (stdlib, também sem
dependência) testaria a API Python e deixaria de fora justamente o contrato que o pipeline
consome. As fixtures são construídas em diretório temporário a partir de uma **cópia** do nó
piloto, com **uma mutação por caso**: cada teste prova que o validador pega aquele defeito e
que não inventa outros. A suíte verifica hash de `content/` antes e depois (critério 8).

### Evidência — nó piloto real, sem alterar `content/` (critério 6)

```
$ python3 scripts/validate-content.py high-school/algebra/quadratic-equations
Contrato íntegro: 1 nó(s) validado(s), 0 violações.        # exit=0
$ python3 scripts/validate-content.py                       # acervo inteiro
Contrato íntegro: 1 nó(s) validado(s), 0 violações.        # exit=0
```

### Evidência — mensagem por fixture inválida (critérios 3 e 5)

Cada linha traz arquivo, item (índice + id) e regra; exit=1 em todas.

```
…/exercises.json: items[0] (id=qe-001): [MC-NO-CORRECT-OPTION] item 'multiple-choice' sem
nenhuma opção com "correct": true — não há gabarito, o item não pode ser apresentado ao
aluno (RF-18); marque exatamente uma das 4 alternativas

…/exercises.json: items[1] (id=qe-002): [MC-MULTIPLE-CORRECT-OPTIONS] item 'multiple-choice'
com 2 opções corretas (a, c) — esperada exatamente 1 (RF-18); múltipla resposta exige tipo
próprio declarado no enunciado

…/exercises.json: items[2] (id=qe-003): [NUMERIC-TOLERANCE-NEGATIVE] 'tolerance' negativa
(-0.5) — nenhuma resposta seria aceita (RF-18); use 0 para exigir valor exato

…/meta.json: title: [LOCALIZED-MISSING-LANG] campo 'title' sem a chave 'en-US' — paridade
bilíngue é obrigatória e não há fallback (chaves presentes: ['pt-BR'])

…/exercises.json: nodeId: [NODE-ID-MISMATCH] nodeId é 'high-school/algebra/linear-equations'
mas o arquivo está no nó 'high-school/algebra/quadratic-equations' — exercícios seriam
servidos sob o nó errado (RF-18); corrija o campo ou mova o arquivo
```

Fixture com 7 defeitos simultâneos lista **as 7** e fecha com
`CONTRATO VIOLADO: 7 violação(ões) em 1 nó(s).` — critério 1 (não para na primeira).

### Evidência — suíte e auditorias

```
$ bash scripts/validate-content-test.sh
validate-content: 84 passaram, 0 falharam                   # exit=0
$ bash scripts/audit-content.sh
Resumo: 1 nós · 0 erros · 0 avisos                          # exit=0
$ bash scripts/audit-ai-surface.sh
Resultado: OK                                               # exit=0
$ git status --porcelain content/
(vazio — content/ intocado)
```

### Dois defeitos que a própria suíte pegou (corrigidos antes da entrega)

1. **Nó invisível.** A descoberta de nós exigia `meta.json`; um diretório com
   `exercises.json` e sem `meta.json` sumia da validação em silêncio — exatamente o que
   RF-18 proíbe. Agora qualquer diretório com `meta.json` **ou** arquivo de exercícios é nó,
   e um alvo sem nenhum nó sai com erro de uso (2), não com "tudo certo" (0).
2. **Veredito perdido na saída quebrada.** Com `| head` ou `>&-`, o flush de encerramento do
   Python trocava o código 1 por 120 — um pipeline leria "erro de infraestrutura" onde havia
   violação de contrato, ou o inverso. A saída agora é silenciada, o veredito é preservado, e
   há teste para os dois modos.

### Achados registrados (sem alterar `docs/`, `content/` nem outro ticket)

- **A1 — `tolerance` sem natureza declarada.** `docs/content/exercise-schema.md` diz
  "Absoluta ou relativa; **declarar qual**", mas o arquivo real traz número puro (`0`,
  `0.001`) sem declaração. O validador trata como **absoluta**, que é a leitura compatível
  com CA-6 e CA-7. Fechar a divergência (campo `toleranceKind` ou texto do schema) é decisão
  de contrato — vai para o `tech-lead`, não para este ticket.
- **A2 — `"unit": null` em `qe-005`.** O schema prevê `unit` opcional "quando aplicável", não
  prevê `null` explícito. Aceito sem violação; achado de documentação.
- **A3 — `version` de `exercises.json`** aparece no exemplo de estrutura do schema mas não na
  tabela de campos, e ninguém valida. Não validei para não inventar contrato.
- **A4 — divergência de severidade proposital.** `audit-content.py` só **avisa** para
  `numeric` sem `tolerance`; aqui é **violação**, porque o critério 4 e o RF-18 exigem que
  ausente ≠ `0`. Documentado no cabeçalho do validador.
- **A5 — `"correct": "false"` (texto) passa em `audit-content.py`**, que usa veracidade
  implícita (`opt.get("correct")`): a string não vazia vira "correta". Aqui é
  `CORRECT-NOT-BOOLEAN`. Não toquei em `audit-content.py` — está fora do escopo deste ticket.
- **A6 — regra 8 do schema (8–12 itens por conjunto)** não é atendida pelo piloto (5 itens,
  `status: draft`). Não é contrato de carga; nenhuma ação aqui.

- Resultado: ok — critérios 1 a 9 atendidos, `content/` intocado, zero dependência nova.

## [005] HANDOFF — 2026-08-01 16:21

- De: backend-developer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: validador do contrato de carga (RF-18) + suíte de 84 asserções,
  em três arquivos novos sob `scripts/`.
- Artefatos:
  - `scripts/validate-content.py`
  - `scripts/validate-content.sh`
  - `scripts/validate-content-test.sh`
- Como validar:
  - `python3 scripts/validate-content.py` → exit 0
  - `python3 scripts/validate-content.py high-school/algebra/quadratic-equations` → exit 0
  - `bash scripts/validate-content-test.sh` → 84 passaram, 0 falharam
  - `bash scripts/audit-content.sh` e `bash scripts/audit-ai-surface.sh` → exit 0
  - `git status --porcelain content/` → vazio
- Checklist dos critérios:
  - [x] 1. Nó ou acervo; exit 1 em violação; lista **todas** (caso 9 da suíte: 7 de 7).
  - [x] 2. CA-13 (caso 3) e CA-14 (caso 6) exercitados por fixture.
  - [x] 3. As cinco fixtures inválidas exigidas, cada uma com teste nomeado
        (casos 3, 4, 5, 6, 7) — mais `tolerance` ausente, `answer` em texto, `correct`
        em texto, tipo desconhecido, JSON inválido e nó sem `meta.json`.
  - [x] 4. Sem falso positivo: cópia intacta do piloto, `tolerance: 0` em `qe-003` **e** em
        `qe-005`, `prerequisites: []`, e nó sintético mínimo independente do piloto.
  - [x] 5. Mensagem com arquivo, `items[i] (id=…)` (ou `options[j] (id=…)`), regra entre
        colchetes e o que fazer.
  - [x] 6. Nó piloto real passa sem alteração de `content/` (hash conferido pela suíte).
  - [x] 7. Zero dependência nova; escolha de mecanismo de teste justificada em [004].
  - [x] 8. `content/` intocado; nenhuma decisão de framework de aplicação embutida.
  - [x] 9. Ambas as auditorias com exit 0.
- Pendências e riscos:
  - **A1** (natureza de `tolerance` não declarada) é decisão de contrato para o `tech-lead`;
    a interpretação "absoluta" está assumida no validador e no CA-6/CA-7.
  - **A5** deixa `audit-content.py` mais permissivo que o validador em `correct` não
    booleano; se o time quiser convergir, é ticket próprio.
  - O validador ainda não roda no CI — é a task 11 (fora de escopo aqui).
  - Contrato exercitado contra **um** nó real; regras de tipos ainda sem exemplar no acervo
    (`matching`, `ordering`, `proof`, `step-by-step`) só têm cobertura sintética.

## [006] REJECT — 2026-08-01 17:05

- De: code-reviewer#6 → Para: backend-developer · Loop nº: 1/3
- Status novo: in_progress
- Escopo revisado: `scripts/validate-content.py`, `scripts/validate-content.sh`,
  `scripts/validate-content-test.sh`, `memory/agents/backend-developer.md`,
  `memory/context/backend.md`, `memory/lessons/a-validator-only-protects-what-it-can-see.md`
  (L-019) e o log/ticket. Nada reexecutado por herança: rodei tudo de novo.

### O que reexecutei (não herdado do [004])

- `python3 scripts/validate-content.py high-school/algebra/quadratic-equations` → `exit 0`;
  sem argumento → `exit 0`; `bash scripts/validate-content.sh` → `exit 0`. Confere com [004].
- `bash scripts/validate-content-test.sh` → **84 passaram, 0 falharam** (`ok` contados: 84).
  Também verde em `env -i`, em `env -i HOME=<tmp> TMPDIR=<tmp> PATH=/usr/bin:/bin` e em
  `LC_ALL=C LANG=C` — suíte hermética de verdade, não só "o runner é pobre".
- As cinco fixtures inválidas do critério 3, uma a uma, fora da suíte: todas `exit 1`, todas
  com arquivo + `items[i] (id=…)` + `[REGRA]` + o que fazer (critério 5 satisfeito).
- Critério 4 sem falso positivo: cópia intacta do piloto, `tolerance: 0` em `qe-003` e em
  `qe-005`, `prerequisites: []` → `exit 0`.
- `git status --porcelain content/` → 0 linhas (critério 8). Zero dependência de terceiros
  confirmada por AST (`stdlib_module_names`): nada fora da stdlib; nenhum termo de framework
  nos três arquivos (critério 7/8).
- `bash scripts/audit-content.sh` → `exit 0`. `bash scripts/audit-ai-surface.sh` → deu `1`
  numa execução e `0` em três seguidas, sempre com `Resultado: OK`: corrida com os tickets
  paralelos que estão editando `AGENTS.md`/`docs/` agora, não deriva deste ticket.

### Critério 1 — listar TODAS as violações: verificado com fixture própria

Montei uma fixture com defeitos de **tipos diferentes** (não repetições da mesma regra):
saíram **18 violações de 17 regras distintas** numa só execução — `META-ID-MISMATCH`,
`LOCALIZED-{MISSING-LANG,EMPTY,UNKNOWN-LANG,NOT-OBJECT}`, `NODE-ID-MISMATCH`,
`HINTS-NOT-LIST`, `OPTION-ID-DUPLICATE`, `MC-{NO-CORRECT-OPTION,MULTIPLE-CORRECT-OPTIONS}`,
`NUMERIC-ANSWER-NOT-NUMBER`, `NUMERIC-TOLERANCE-{NEGATIVE,NOT-NUMBER}`,
`ITEM-{TYPE-UNKNOWN,FIELD-MISSING,ID-MISSING,NOT-OBJECT}`, `ANSWER-MISSING`. O caso 9 da
suíte (7 defeitos) também é de 7 tipos distintos, não repetição. Critério 1 **atendido**.

### Tentativas de burla (9 vetores) — 7 barrados, 2 passaram

Barrados corretamente: localizado `""` e só-espaços (`LOCALIZED-EMPTY`); `correct: "true"`
(`CORRECT-NOT-BOOLEAN` + `MC-NO-CORRECT-OPTION`); `tolerance: "0.001"`
(`NUMERIC-TOLERANCE-NOT-NUMBER`); `answer: "3.5"` (`NUMERIC-ANSWER-NOT-NUMBER`); `id` de
opção duplicado (`OPTION-ID-DUPLICATE`); `meta.json.id` divergente com `nodeId` correto
(`META-ID-MISMATCH`); arquivo com BOM (`JSON-INVALID`, linha e coluna, sem traceback).
Chave JSON duplicada: o último valor vence, igual ao `JSON.parse` do runtime — comportamento
consistente, não defeito (vira S4). Passaram sem violação: `items: []` (S1) e **nó
descendente invisível** (B1, abaixo).

---

## Defeitos bloqueantes

**B1 — nó descendente some em silêncio quando o alvo é ele mesmo um nó.**
`scripts/validate-content.py:488-492`: `find_nodes` faz
`if any((scope / marker).exists() for marker in markers): return [scope]` e **nunca desce**.
Reprodução (fixture = cópia do piloto + subnó `discriminant/` com `meta.json.id` errado,
`title` sem `en-US`, `summary` não-objeto, `nodeId` errado e item sem `stem`/`solution`/
`answer`/`tolerance`):

```
$ validate-content.py <topic>          → Contrato íntegro: 1 nó(s) validado(s), 0 violações.  exit 0
$ validate-content.py <raiz>           → CONTRATO VIOLADO: 8 violação(ões) em 2 nó(s).        exit 1
$ audit-content.py <o MESMO topic>     → 2 nós · 3 erros                                      exit 1
```

Critério violado: **1** (o validador "recebe um nó de `content/`" e tem de sair com erro
quando o contrato é violado) e RF-18 ("falha silenciosa é defeito"). É o **único** caso que
achei de veredito divergente entre as duas ferramentas em que a **mais estrita é a que
aprova** — pior cenário possível para um portão. E é a mesma classe do defeito 1 do [004],
já registrado como **L-019** nesta mesma entrega ("Reconhecer o objeto por mais de um
marcador, para que um arquivo faltando não apague o objeto inteiro da varredura") → AGENTS.md
§10 regra 7 torna isto **bloqueante**. A taxonomia autoriza a estrutura (`AGENTS.md` §3:
`T --> O` e `T --> U --> O`; `docs/content/taxonomy.md:88`), `audit-content.py:89-91` já é
recursivo sempre, e a task 11 vai rodar isto no CI. Nenhuma asserção da suíte fixa o
comportamento atual — a correção não vai reprovar teste existente.

**B2 — `exit 2` (erro de uso) vira `120` quando o stderr está quebrado.**
`scripts/validate-content.py:540`, `:547-548`, `:557-558`, `:564` e `:570-571` escrevem com
`print(..., file=sys.stderr)` **fora** do `emit()`, e o flush de encerramento em `:611-615`
só cobre `sys.stdout`. Medido:

```
$ validate-content.py nao/existe 2>&1 | true ; ${PIPESTATUS[0]}   → 120   (esperado 2)
$ validate-content.py nao/existe 2>/dev/full                      → 120   (esperado 2)
$ validate-content.py --root <raiz-sem-nenhum-nó> 2>&1 | true     → 120   (esperado 2)
$ validate-content.py --xx 2>&1 | true                            → 120   (esperado 2)
```

Controle: o veredito de **conteúdo** sobrevive a tudo — `exit 1` em 8/8 combinações
(`| head`, `| true`, `>&-`, `> /dev/full`, `--json >&-`, `--json > /dev/full`,
`--quiet >&-`, wrapper `.sh | head`) e `exit 0` em 4/4. Ou seja, metade da correção do
defeito 2 do [004] foi feita. Critério violado: o contrato de saída "0 · 1 · 2" declarado em
`validate-content.py:68`, `validate-content.sh:4`, no log [004] e em
`memory/context/backend.md`; e **L-019 item 2** ("Emissão: o veredito virava refém do estado
do terminal") → regra 7, bloqueante. Agrava: o caso `--root` sem nenhum nó é exatamente o
"apontar o pipeline para o diretório errado" que a própria L-019 cita como perigo. A suíte
tem 12e/12f/12g para stdout e **nenhum** caso para stderr.

**B3 — a fronteira declarada no cabeçalho é factualmente falsa, e já foi copiada para a
memória compartilhada.** `validate-content.py:12-19` afirma "auditoria editorial, que **NÃO**
é duplicada aqui" e reivindica quatro famílias como exclusivas do validador (gabarito
resolvível, resposta numérica comparável, paridade bilíngue por campo, identidade do nó ×
caminho). As quatro já existem em `scripts/audit-content.py`: identidade `:110-111`;
gabarito `:229-233`; campos localizados `:131-133`, `:211`, `:216`, `:221-222`, `:239`,
`:244`; `answer` obrigatório `:245-247`. A duplicação em si é **defensável** (um portão de
carga não pode depender de outra ferramenta ter rodado) — o defeito é a declaração dizer o
contrário, e a mesma frase estar em `memory/context/backend.md` como "Decisão operacional em
vigor" com a instrução "consultar antes de acrescentar regra em qualquer um dos dois, para
não duplicar nem divergir por acidente". Mapa errado da malha de segurança é caro depois.
Nos pontos de sobreposição há **duas** divergências reais de veredito, ambas com o `audit`
mais permissivo (medidas em cópia isolada do repositório, sem tocar em `content/`):

| Entrada | `audit-content.py` | `validate-content.py` |
|---|---|---|
| `"correct": "false"` na única alternativa de gabarito | `0 erros · exit 0` | `CORRECT-NOT-BOOLEAN` + `MC-NO-CORRECT-OPTION` · exit 1 |
| `title.en-US: 5` (não-texto) | `0 erros · exit 0` (`:85` faz `str(5).strip()`) | `LOCALIZED-NOT-STRING` · exit 1 |

A primeira é o A5 do [004] — **confirmada**. A segunda é nova, não registrada.
Critério violado: instrução do ticket "Auditoria existente, **a não duplicar**" +
integridade do registro em `memory/`. Correção esperada: reescrever a fronteira dizendo o que
é redundância deliberada, qual ferramenta prevalece e quais são as divergências conhecidas; e
corrigir `memory/context/backend.md` no mesmo sentido. Não mexer em `audit-content.py`.

## Sugestões (não bloqueiam)

- **S1 — `exercises.json` com `items: []` passa nas duas ferramentas.**
  `validate-content.py:454-458` aceita lista vazia (`exit 0`, "Contrato íntegro");
  `audit-content.py` só emite AVISO de "skills declaradas sem exercício". Um nó que anuncia
  prática e entrega zero itens não tem rede em lugar nenhum. Ou `ITEMS-EMPTY`, ou dizer na
  fronteira que contagem de itens é editorial (regra 8 do schema, hoje sem dono — A6).
- **S2 — `id` de item duplicado passa no validador.** `:388-394` só checa presença; quem pega
  é `audit-content.py:186-187`. Como o validador se apresenta como portão autossuficiente de
  identidade, cabe `ITEM-ID-DUPLICATE` (o equivalente já existe para opções, `:294-296`).
- **S3 — a mensagem some em stdout ASCII.** `emit` (`:149-155`) captura `UnicodeEncodeError`
  (subclasse de `ValueError`) e silencia o stdout para sempre: com
  `PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=POSIX` o validador sai `1` **sem imprimir uma
  linha** — contra o critério 5. `LC_ALL=C` puro está OK (coerção do Python). Sugestão:
  `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` no início.
- **S4 — chave JSON duplicada** (`"correct": false, "correct": true`) é aceita em silêncio.
  Não é defeito (o `JSON.parse` do runtime faz o mesmo), mas `object_pairs_hook` detectaria
  contradição escondida no arquivo.
- **S5 — `--root` apontando para o *pai* de `content/` gera falso positivo confiante**:
  `META-ID-MISMATCH` e `NODE-ID-MISMATCH` num nó íntegro, porque o id passa a ser
  `content/<stage>/…`. Reproduzido. Avisar (ou descer) quando `--root` contiver `content/`.
- **S6 — o registro da premissa de `tolerance` é mais forte que o código.** O log [004] A1 e
  `memory/context/backend.md` dizem "o validador assume **absoluta**"; em `:361-377` a
  `tolerance` só é checada como número finito ≥ 0 — checagem **idêntica** nas duas leituras,
  absoluta ou relativa. Trocar por "não decide a natureza da tolerância" evita que as tasks
  5–8 herdem como decidida uma premissa que ninguém decidiu.

## Vereditos pedidos explicitamente

- **A5 (`"correct": "false"` no `audit-content.py`): procede — confirmado por medição.** Com
  a string `"false"` na única alternativa de gabarito, o auditor devolve `1 nós · 0 erros ·
  0 avisos · exit 0`, porque `:229` e `:240` usam veracidade implícita
  (`o.get("correct")`) — a string não vazia vira "correta" e a alternativa ainda escapa da
  exigência de `feedback`. **Não bloqueia o TCK-0014**: o defeito é do auditor, o validador
  novo acerta e é mais estrito, o ticket manda registrar achado e não corrigir, e a partir
  da task 11 o portão mais estrito governa o CI. É **ticket próprio para o `tech-lead`**,
  junto com a segunda divergência achada aqui (`LOCALIZED-NOT-STRING`).
- **Premissa "tolerância absoluta": aceitável nesta entrega, sem ADR.** Não porque seja
  irrelevante, mas porque **não está embutida no código**: nenhuma comparação numérica é
  feita pelo validador, e `número finito ≥ 0` é a mesma regra nas duas leituras (`:361-377`).
  Premissa embutida seria, por exemplo, rejeitar `tolerance > 1` (relativa) ou aplicar a
  margem. Nada disso existe. O que precisa mudar é o **registro** (S6) — e a decisão de
  contrato tem de estar fechada **antes** da task de correção de resposta (5–8), onde ela
  passa a ter efeito observável. A2 (`"unit": null`), A3 (`version`) e A6 (5 itens × regra 8)
  ficam como achados de documentação, corretamente não-decididos aqui.

## O que já está bom (não refazer)

1. Critério 1 provado com folga (18 violações, 17 regras distintas, numa execução).
2. Critério 5: toda mensagem tem arquivo + `items[i] (id=…)` / `options[j] (id=…)` + regra
   entre colchetes + o que fazer. É o melhor da entrega; manter o formato como contrato.
3. Critério 4 sem falso positivo, incluindo `tolerance: 0` e `prerequisites: []`.
4. Critério 6: piloto real limpo, `content/` intocado (hash na suíte + `git status` vazio).
5. Critério 7: zero dependência (verificado por AST), e a justificativa do mecanismo de teste
   está correta — testar a superfície de CLI é o que o pipeline consome.
6. `exit 1` e `exit 0` sobrevivem a stdout quebrado em 12/12 combinações. O defeito remanescente
   é só o do stderr (B2).
7. Suíte hermética (verde em 4 ambientes, inclusive `HOME`/`TMPDIR` sintéticos).
8. `--root` como mecanismo para manter fixture fora de `content/`: decisão certa.
9. `find_nodes` reconhecer nó por `meta.json` **ou** arquivo de exercícios, e alvo sem nó
   sair `2` em vez de `0`: mantém — B1 é o complemento que falta, não a reversão disso.

- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9
  em condições nominais; **reprovado por B1/B2 (falso negativo e código de saída fora das
  condições nominais) e B3 (declaração falsa propagada para a memória)**.

## [007] ACTION — 2026-08-01 17:20 — backend-developer

- Ação: corrigidos os três bloqueantes do `[006]`, mais as seis sugestões, com regressão fixada
  na suíte (84 → **118** asserções). Arquivos tocados: `scripts/validate-content.py`,
  `scripts/validate-content-test.sh`, `memory/context/backend.md`,
  `memory/agents/backend-developer.md`, `memory/lessons/a-validator-only-protects-what-it-can-see.md`
  (adendo em L-019), `memory/LESSONS.md`, `memory/MEMORY.md`. `content/`, `docs/`,
  `audit-content.py` e os tickets paralelos: **intocados**.

### B1 — travessia parava no alvo (aceito integralmente; era falso negativo)

`find_nodes` agora coleta os marcadores por `rglob` **sempre** e apenas acrescenta o próprio
alvo, em vez de retornar `[scope]` e sair. Evidência com a fixture do revisor reproduzida
(cópia do piloto + `discriminant/` com `meta.id` errado, `title` sem `en-US`, `summary`
não-objeto, `nodeId` errado e item sem `stem`/`solution`/`answer`/`tolerance`):

```
$ validate-content.py --root <raiz> <raiz>/high-school/algebra/quadratic-equations
…/discriminant/meta.json: id: [META-ID-MISMATCH] …
…/discriminant/meta.json: title: [LOCALIZED-MISSING-LANG] …
…/discriminant/meta.json: summary: [LOCALIZED-NOT-OBJECT] …
…/discriminant/exercises.json: nodeId: [NODE-ID-MISMATCH] …
…/discriminant/exercises.json: items[0] (id=dc-001): [ITEM-FIELD-MISSING] … 'stem'
…/discriminant/exercises.json: items[0] (id=dc-001): [ITEM-FIELD-MISSING] … 'solution'
…/discriminant/exercises.json: items[0] (id=dc-001): [NUMERIC-ANSWER-MISSING] …
…/discriminant/exercises.json: items[0] (id=dc-001): [NUMERIC-TOLERANCE-MISSING] …

CONTRATO VIOLADO: 8 violação(ões) em 2 nó(s).                                  exit 1
```

Era `Contrato íntegro: 1 nó(s) validado(s), 0 violações · exit 0`. Alvo = raiz e alvo = o
próprio subnó também dão `exit 1`, e o caso 14b da suíte **compara as contagens** de raiz e nó
pai para que não voltem a divergir. Caso 14d prova que pai + subnó íntegros continuam
passando (`2 nó(s) validado(s)`, exit 0) — a correção não troca falso negativo por falso
positivo.

### B2 — `exit 2` virava 120 com a saída de erro quebrada (aceito integralmente)

Três mudanças: `_write(stream, …)` protege **qualquer** fluxo (não só o stdout); os cinco
`print(file=sys.stderr)` viraram `emit_err`; `safe_flush()` no encerramento cobre stdout **e**
stderr. E a mensagem do próprio argparse passou a sair por `SafeArgumentParser._print_message`
— sem isso, `--xx` continuaria em 120, porque o texto não passava por código meu.

```
$ validate-content.py nao/existe 2>&1 | true            → 2   (era 120)
$ validate-content.py nao/existe 2>/dev/full            → 2   (era 120)
$ validate-content.py --root <raiz-sem-nó> 2>&1 | true  → 2   (era 120)
$ validate-content.py --xx 2>&1 | true                  → 2   (era 120)
$ validate-content.py --xx 2>/dev/full                  → 2
$ validate-content.py nao/existe 2>&-                   → 2
$ validate-content.py --help >/dev/null 2>&1            → 0
```

Casos 15–15h da suíte. Os 12 casos de stdout quebrado que já passavam continuam passando.

### B3 — a fronteira declarada era falsa (aceito; conferi as linhas citadas)

Reescrevi o cabeçalho (`validate-content.py`) e a seção correspondente de
`memory/context/backend.md` e de `memory/agents/backend-developer.md`. A descrição agora diz o
que é verdade: **redundância deliberada**, com as linhas do auditor onde a sobreposição existe
(`audit-content.py:110`, `:229-233`, `:131/:211/:216/:221/:239/:244`, `:245-247`), a razão de
repetir (um portão de carga não pode depender de outra ferramenta ter rodado), **qual
prevalece** (este, por ser o mais estrito) e as **duas divergências conhecidas** com o auditor
mais permissivo (`"correct": "false"` e `title.en-US: 5`), ambas marcadas como defeito do
auditor e ticket do `tech-lead`. `audit-content.py` não foi tocado.

### Sugestões implementadas

- **S1** `ITEMS-EMPTY` — `exercises.json` presente com `items: []` agora falha (caso 17).
- **S2** `ITEM-ID-DUPLICATE` — id de item repetido (caso 17b); o validador passa a ser
  autossuficiente também na identidade do item, como já era para opções.
- **S3** `make_output_lossless()` reconfigura as saídas para UTF-8 com `errors="replace"`.
  Com `PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=POSIX` a violação continua impressa e
  localizada (caso 16) — antes o processo saía 1 mudo, perdendo o critério 5.
- **S4** `JSON-DUPLICATE-KEY` via `object_pairs_hook` (caso 17c): chave repetida no mesmo
  objeto esconde o valor descartado da revisão.
- **S5** `--root` no **pai** de `content/` agora é erro de uso com a raiz correta sugerida
  (caso 17d), em vez de `META-ID-MISMATCH` num nó íntegro. De brinde, alvo apontando para um
  arquivo (`meta.json`) passou a valer pelo nó (caso 17e).
- **S6** registro corrigido: o validador **não decide a natureza da `tolerance`** — exige
  número finito ≥ 0, idêntico nas duas leituras. Corrigido no cabeçalho e em
  `memory/context/backend.md`; a decisão continua pendente do `tech-lead` antes das tasks 5–8.

### Verificação (tudo reexecutado agora, nada herdado)

```
$ python3 scripts/validate-content.py                       → Contrato íntegro: 1 nó · exit 0
$ python3 scripts/validate-content.py high-school/algebra/quadratic-equations  → exit 0
$ bash scripts/validate-content.sh                          → exit 0
$ bash scripts/validate-content-test.sh                     → 118 passaram, 0 falharam
$   idem em `env -i PATH=… HOME=<tmp> TMPDIR=<tmp>`         → 118 passaram, 0 falharam
$   idem em `LC_ALL=C LANG=C`                               → 118 passaram, 0 falharam
$ bash scripts/audit-content.sh                             → 1 nós · 0 erros · 0 avisos · exit 0
$ bash scripts/audit-ai-surface.sh                          → Resultado: OK · exit 0
$ git status --porcelain content/                           → 0 linhas
$ AST (stdlib_module_names)                                 → fora da stdlib: []
```

### Enquadramento honesto: isto foi reincidência, não descoberta

B1 e B2 são **a mesma lição que eu escrevi nesta entrega** (L-019), violada nos dois itens.
Não criei lição nova com nome diferente: registrei um **adendo de reincidência** em
`memory/lessons/a-validator-only-protects-what-it-can-see.md` explicando por que escapou —
corrigi os casos **citados** pela minha própria suíte e escrevi a lição descrevendo os casos,
não a classe, que é exatamente o que L-013 e L-018 já alertavam. A regra ficou mais forte:
travessia nunca encerra no alvo (teste obrigatório com objeto quebrado um nível abaixo) e a
proteção do código de saída vale para todo canal, inclusive o texto emitido por bibliotecas.
`memory/LESSONS.md` e `memory/MEMORY.md` foram atualizados no mesmo sentido.

- Resultado: ok — B1, B2 e B3 corrigidos com regressão fixada; S1–S6 implementadas.
  Lição: L-019 (adendo de reincidência; ver também L-013 e L-018).

## [008] HANDOFF — 2026-08-01 17:20

- De: backend-developer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: correção dos três bloqueantes do `[006]` e das seis sugestões, com a suíte
  passando de 84 para 118 asserções.
- Artefatos:
  - `scripts/validate-content.py` (travessia recursiva, `emit_err`/`safe_flush`,
    `SafeArgumentParser`, UTF-8 forçado, `ITEMS-EMPTY`, `ITEM-ID-DUPLICATE`,
    `JSON-DUPLICATE-KEY`, guarda de `--root`, cabeçalho reescrito)
  - `scripts/validate-content-test.sh` (casos 14, 15, 16, 17 novos)
  - `memory/context/backend.md`, `memory/agents/backend-developer.md`,
    `memory/lessons/a-validator-only-protects-what-it-can-see.md`, `memory/LESSONS.md`,
    `memory/MEMORY.md`
- Como validar:
  - **B1:** montar nó pai + subnó quebrado, apontar o validador para o **pai** → `exit 1` com
    as violações do subnó e `em 2 nó(s)`; comparar com o alvo = raiz (mesmo veredito). Casos
    14–14d.
  - **B2:** `nao/existe 2>&1 | true`, `nao/existe 2>/dev/full`,
    `--root <raiz-sem-nó> 2>&1 | true`, `--xx 2>&1 | true` → todos `exit 2`. Casos 15–15h.
  - **B3:** ler o cabeçalho de `scripts/validate-content.py` e a seção "Decisões operacionais"
    de `memory/context/backend.md` contra `audit-content.py:110/229-233/131/211/216/221/239/244/245-247`.
  - `bash scripts/validate-content-test.sh` → 118/0; auditorias → exit 0;
    `git status --porcelain content/` → vazio.
- Pendências e riscos:
  - **Para o `tech-lead`, não para este ticket:** (a) ticket próprio para as duas divergências
    do `audit-content.py` (`"correct": "false"` e `title.en-US: 5`); (b) decisão de contrato
    sobre a natureza da `tolerance`, necessária **antes** das tasks 5–8.
  - `ITEMS-EMPTY` e `JSON-DUPLICATE-KEY` são regras **novas** de contrato criadas a partir de
    S1/S4: nenhum nó atual é afetado (acervo tem 1 nó, que passa), mas são mais estritas que o
    schema documentado — se o `tech-lead` discordar, é reversão de uma linha cada.
  - Validador ainda fora do CI (task 11). Tipos `matching`, `ordering`, `proof` e
    `step-by-step` continuam sem exemplar real no acervo.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9,
  agora também fora das condições nominais (subnó abaixo do alvo, stdout/stderr quebrados,
  terminal ASCII).

## [009] HANDOFF — 2026-08-01 17:55

- De: code-reviewer#6 → Para: qa-validator
- Status novo: in_validation
- Loop nº: 2/3 — **APROVADO**. B1, B2 e B3 corrigidos e reverificados por medição própria;
  S1–S6 aplicadas; nenhum bloqueante novo.
- O que foi feito: correção dos três bloqueantes do `[006]` e das seis sugestões, com a suíte
  de 84 → 118 asserções.
- Artefatos: `scripts/validate-content.py`, `scripts/validate-content-test.sh`,
  `memory/context/backend.md`, `memory/agents/backend-developer.md`,
  `memory/lessons/a-validator-only-protects-what-it-can-see.md` (adendo em L-019),
  `memory/LESSONS.md`, `memory/MEMORY.md`. `scripts/validate-content.sh`, `content/`,
  `docs/`, `scripts/audit-content.py` e os tickets paralelos: intocados (conferido no
  `git status`, num working tree que agora tem 5 tickets escrevendo junto).

### B1 — resolvido, com a MINHA fixture do `[006]`, não com a dele

`find_nodes` (`:576-596`) agora coleta por `rglob` sempre e só **acrescenta** o alvo.
Reconstruí a fixture original (cópia do piloto + `discriminant/` quebrado):

```
alvo = nó pai   → CONTRATO VIOLADO: 8 violação(ões) em 2 nó(s)   exit 1   (antes: 0 violações, exit 0)
alvo = raiz     → CONTRATO VIOLADO: 8 violação(ões) em 2 nó(s)   exit 1   (idêntico — era a divergência)
alvo = o subnó  → CONTRATO VIOLADO: 8 violação(ões) em 1 nó(s)   exit 1
```

O caso 14b da suíte (`:384-388`) **compara as contagens** de raiz e nó pai, não só o exit —
é a asserção certa para esta classe. 14d prova o inverso (pai + subnó íntegros → exit 0,
`2 nó(s) validado(s)`). As asserções são falsificáveis: no `[006]` eu medi `exit 0` nos
mesmos comandos.

**Falso positivo simétrico — procurei, não achou nada bloqueante.** Cinco cenários que a
travessia sempre-recursiva poderia quebrar:

| Cenário | Resultado |
|---|---|
| `assets/`, `assets/img/`, `README.md` solto e diretório vazio dentro do nó | `1 nó · exit 0` — nada vira nó |
| Aninhamento de 3 níveis (`topic/subtopic/subsub`), todos íntegros | `3 nó(s) validado(s) · exit 0` |
| Symlink de diretório apontando para fora da raiz | não é seguido; `exit 0`, sem erro "fora da raiz" |
| Symlink em **loop** dentro do nó | não trava (timeout de 25 s não disparou), `exit 0` |
| `assets/` contendo um arquivo chamado `exercises.json` | vira nó → `NODE-META-MISSING` + `NODE-ID-MISMATCH` |

Só o último gera ruído, é contrived (o schema reserva `assets/` a mídia), **não é regressão**
(a varredura da raiz já se comportava assim antes do fix) e é consequência direta da regra
dos dois marcadores que a L-019 exige. Anotado como S2' abaixo.

### B2 — resolvido; reexecutei os 7 casos dele e mais 16 na caça ao oitavo

`_write` (`:172-184`) protege qualquer fluxo, `emit_err` substitui os cinco
`print(file=sys.stderr)`, `safe_flush` (`:195-203`) cobre os dois canais e
`SafeArgumentParser._print_message` (`:609-618`) captura o texto do argparse — que era o
ponto não óbvio: sem ele `--xx` continuaria em 120, porque a mensagem não passava por código
do autor. Os 7 casos declarados reproduzem (`2,2,2,2,2,2` e `--help` = `0`). **Não achei um
oitavo**: `--help | true`, `--help >&-`, `--help > /dev/full`, `--help >&- 2>&-` → `0`;
`--xx >&- 2>&-`, `nao/existe >&- 2>&-`, `--quiet nao/existe 2>&1|true`,
`--json nao/existe 2>&1|true`, `--root` sem valor, guarda do `--root` com `2>&1|true` e com
`2>/dev/full` → `2`; violação com `>&- 2>&-`, `>/dev/full 2>/dev/full`, `--json | head`,
`| head` → `1`; acervo íntegro com `>&- 2>&-` → `0`. **23 combinações, 23 vereditos certos,
zero traceback.** Também: arquivo sem permissão de leitura → `FILE-UNREADABLE` + `exit 1`,
sem traceback.

### B3 — a nova declaração é verdadeira; conferi linha a linha e por fuzz diferencial

Todas as citações do cabeçalho (`:12-39`) batem com o arquivo real: `audit-content.py:85`
(`str(value.get(lang,"")).strip()`), `:110` (`meta.get("id") != rel`), `:131`, `:211`,
`:216`, `:221`, `:239`, `:240`, `:244`, `:229-233` (lista de corretas e `>1` só para
`multiple-choice`), `:245-247` (`answer` obrigatório). A frase que gerou o defeito ("NÃO é
duplicada aqui") sumiu, e o texto agora nomeia a redundância como deliberada, dá a razão
(portão não pode depender de outra ferramenta ter rodado) e diz **qual prevalece**.

A afirmação "onde há sobreposição, este validador prevalece por ser o mais estrito" eu testei,
não li: **22 mutações** rodadas nas duas ferramentas numa cópia isolada do repositório
(`REPO_ROOT` sintético, `content/` real intocado). Em **20 mutações de regra sobreposta**,
nunca houve `audit=1 · validate=0`. As duas únicas ocorrências de "auditor mais estrito"
foram `difficulty: 9` e `stage` inválido — **fora** da sobreposição, e ambas listadas no
cabeçalho como território do auditor. As duas divergências declaradas reproduzem:
`"correct": "false"` → auditor `1 nós · 0 erros · exit 0` × validador `CORRECT-NOT-BOOLEAN`
+ `MC-NO-CORRECT-OPTION` · exit 1; `title.en-US: 5` → auditor exit 0 × validador
`LOCALIZED-NOT-STRING`. Achei ainda `title.en-US: None` e `true-false` com duas corretas como
instâncias novas da **mesma** classe já declarada (`str(None)` = "None" e `>1` só checado
para `multiple-choice`) — não exigem texto novo, entram no ticket do auditor.

### Sugestões — as seis conferidas

- **S3** (a que mais podia falhar mal): `PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=POSIX` →
  violação impressa, acentuada e localizada, `exit 1`. Idem com `PYTHONIOENCODING=ascii`.
  Antes saía `1` mudo. `make_output_lossless` (`:206-217`) resolve na origem.
- **S5**: a guarda recusa `--root <pai-de-content>` com a raiz certa na mensagem (`exit 2`).
  **Não recusa caso legítimo**: `--root .../content` (exit conforme o conteúdo),
  `--root .../content` + alvo explícito, `--root` de uma raiz que contém um nó chamado
  `content` em nível profundo, e a operação sem `--root` (`content`, `content/high-school`)
  continuam todas funcionando. E nenhum `stage` pode se chamar `content`, então não há
  raiz válida com `content/` na primeira camada.
- **S1/S2/S4**: `ITEMS-EMPTY`, `ITEM-ID-DUPLICATE` e `JSON-DUPLICATE-KEY` disparam com
  mensagem localizada e acionável; nenhum falso positivo no acervo real. **S6**: o registro
  agora diz "não decide a natureza da `tolerance`", que é o que o código faz (`:437-453`).
- Reexecutei a bateria de burla inteira do `[006]` (12 vetores): **12/12 barrados**. Os três
  buracos daquele loop (`items: []`, id de item duplicado, subnó invisível) fecharam. O único
  `exit 0` restante é nó sem `exercises.json` e sem `theory.en-US` — território declarado do
  `audit-content.py`, que reprova.

### Reprodução da verificação declarada

```
piloto · acervo · wrapper                       → exit 0 · 0 · 0
bash scripts/validate-content-test.sh           → 118 passaram, 0 falharam (118 linhas 'ok')
  env -i HOME=<tmp> TMPDIR=<tmp> PATH=…         → 118/0
  LC_ALL=C LANG=C                               → 118/0
AST (stdlib_module_names)                       → fora da stdlib: []
git status --porcelain content/                 → 0 linhas
bash scripts/audit-content.sh                   → exit 0
bash scripts/audit-ai-surface.sh (3×)           → exit 0 · 0 · 0
```

### Vereditos pedidos

- **Enquadramento da lição: adendo em L-019 é o registro correto, e a regra ficou mais
  forte.** A norma manda criar lição nova quando a anterior é **superada**
  (`memory/LESSONS.md:21`, `docs/ai/ticket-protocol.md:112`) — não é o caso: a L-019 não foi
  contrariada nem substituída, foi **violada e ampliada**. Lição nova com outro nome
  fragmentaria a mesma classe em dois arquivos com "Como aplicar" quase idêntico, que é o
  teste de duplicata que eu mesmo aplico. O adendo preserva o ID citável, admite a
  reincidência com nome ("corrigi os casos citados, escrevi a lição descrevendo casos, não a
  classe"), referencia L-013 e L-018 corretamente e troca a lista de casos por regra de
  classe **verificável**: travessia nunca encerra no alvo, com teste obrigatório de objeto
  quebrado um nível abaixo comparado à raiz; proteção de exit em **todo** canal, incluindo
  texto de biblioteca; codificação que não apaga mensagem. As três viraram asserção (14b,
  15–15f, 16). Índices `LESSONS.md:70-75` e `MEMORY.md:80-83` atualizados, sem colisão de
  `L-NNN`. A sanção pela reincidência já foi o `REJECT` do loop 1 — não se cobra duas vezes.
- **`ITEMS-EMPTY` e `JSON-DUPLICATE-KEY`: aceitáveis neste ticket, sem decisão prévia do
  `tech-lead`.** Três razões: (1) o próprio ticket atribui a este trabalho a definição
  prática de "conteúdo válido" ("é ele que define, na prática, o que 'conteúdo válido'
  significa"), e o "Fora de escopo" só proíbe alterar `content/`, a spec, os ADRs e o schema
  de `references.json` — nada disso foi tocado; (2) **nenhuma das duas contradiz o schema**:
  a regra 8 de `docs/content/exercise-schema.md` já exige 8–12 itens por conjunto, então
  `ITEMS-EMPTY` é *mais frouxa* que o documentado, e `JSON-DUPLICATE-KEY` não é regra de
  conteúdo e sim de boa-formação do arquivo; (3) impacto zero no acervo, reversão de uma
  linha, e ambas declaradas no `[008]`. O que **precisa** ir ao `tech-lead` é a consequência:
  `docs/content/exercise-schema.md` passou a ser menos preciso que a ferramenta, e quem
  reconcilia é o `docs-writer` depois do `done`.

### Encaminhamentos ao `tech-lead` (não bloqueiam o `done` deste ticket)

1. **Ticket próprio para `scripts/audit-content.py`**: `"correct": "false"` e `title.en-US`
   não-texto (mais `None` e `true-false` com duas corretas, mesma classe) passam no auditor.
   Enquanto existir, o auditor é o elo fraco; a partir da task 11 o portão mais estrito
   governa o CI.
2. **Decisão de contrato sobre a natureza da `tolerance`** (absoluta × relativa), necessária
   **antes** das tasks 5–8, onde passa a ter efeito observável. Hoje o validador não decide.
3. **`docs/content/exercise-schema.md` alcançar as regras novas** (`ITEMS-EMPTY`,
   `ITEM-ID-DUPLICATE`, `JSON-DUPLICATE-KEY`, `version`, `unit: null`) — trabalho de
   `docs-writer` pós-`done`.

### Sugestões novas (nenhuma bloqueante, nenhuma exige ação neste ticket)

- **S1' — diretório sem permissão de leitura é pulado em silêncio.** `rglob` ignora, e um
  `meta.json` abaixo dele não é validado (`Contrato íntegro · exit 0`). Não vem de checkout
  (git não versiona modo `000` de diretório); é a única invisibilidade que sobrou e a
  ferramenta literalmente não pode ver. Registrar como limite conhecido, não corrigir agora.
- **S2' — `assets/` com arquivo chamado `exercises.json` vira nó.** Ruído contrived,
  não-regressão; se incomodar, excluir `assets/` da varredura de marcadores.
- **S3' — symlink de diretório não é seguido**: um nó alcançável só por symlink não é
  validado, sem aviso. `content/` não usa symlink; anotar no cabeçalho resolveria.
- **S4' — a guarda do `--root` roda antes dos alvos**, então recusa mesmo quando os alvos
  explícitos estão certos. Não achei caso legítimo recusado.

- Como validar (para o `qa-validator`): critérios 1–9 do ticket; os comandos do bloco
  "Reprodução da verificação declarada"; e, para o critério 1, montar um nó com defeitos de
  **tipos diferentes** e conferir que todos saem (medi 18 violações de 17 regras distintas no
  `[006]`, com o mesmo desenho de coletor).
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9
  — agora também fora das condições nominais: subnó abaixo do alvo, stdout **e** stderr
  quebrados nos três códigos de saída, e terminal ASCII.
- Pendências e riscos: os três encaminhamentos ao `tech-lead` acima; validador ainda fora do
  CI (task 11); tipos `matching`, `ordering`, `proof` e `step-by-step` sem exemplar real no
  acervo — cobertura sintética apenas.

## [010] HANDOFF — 2026-08-01 18:40

- De: qa-validator#8 → Para: tech-lead
- Status novo: **done** — 9/9 critérios com evidência própria, 0 defeitos bloqueantes.
- Ambiente da validação: commit `5d1e2b6` (HEAD igual no início e no fim), Python 3.12.3,
  GNU bash 5.2.21, Linux 7.0.0-28-generic x86_64. Sem preview/navegador: o artefato é CLI.
- Nada herdado: reconstruí todas as fixtures. As do produtor e do revisor não foram
  reaproveitadas; as cinco do critério 3 foram remontadas com mutações diferentes
  (`tolerance = -1e-9`, `stem.pt-BR` em vez de `meta.title`, `nodeId` para outro estágio).

### Checklist — evidência por critério

- [x] **1. Nó ou acervo, exit 1, lista TODAS.** Fixture minha com defeitos de famílias
      distintas: **21 violações de 21 regras distintas numa só execução**, exit 1,
      `CONTRATO VIOLADO: 21 violação(ões) em 1 nó(s).` (supera as 18/17 do `[006]`; inclui
      `ITEMS-EMPTY` em `assessments.json`, `ITEM-ID-DUPLICATE`, `ITEM-NOT-OBJECT`,
      `OPTIONS-MISSING`, `NUMERIC-ANSWER-NOT-FINITE`). Regressão do **B1** com fixture minha
      de **dois** níveis (`…/discriminant/sign-analysis`): alvo = raiz, tópico, subnó e
      sub-subnó → `1 · 1 · 1 · 1`, e raiz e tópico com contagem idêntica (3 violações, 2 nós).
- [x] **2. CA-13 e CA-14.** CA-13: `multiple-choice` com todas as opções `correct: false` →
      exit 1, `[MC-NO-CORRECT-OPTION]`, uma única violação (sem ruído). CA-14 literal
      (`meta.json` sem `title.en-US`) → exit 1, `[LOCALIZED-MISSING-LANG]` com
      "não há fallback".
- [x] **3. As cinco fixtures inválidas.** Reconstruídas fora da suíte, uma a uma:
      MC sem correta → `[MC-NO-CORRECT-OPTION]`; MC com duas → `[MC-MULTIPLE-CORRECT-OPTIONS]`
      "(a, b)"; `tolerance: -1e-9` → `[NUMERIC-TOLERANCE-NEGATIVE]`; `stem` sem `pt-BR` →
      `[LOCALIZED-MISSING-LANG]`; `nodeId: undergraduate/calculus/limits` →
      `[NODE-ID-MISMATCH]`. **Todas exit 1, todas com exatamente 1 violação.**
- [x] **4. Sem falso positivo.** Cópia intacta do piloto (`tolerance: 0` em `qe-003`,
      `prerequisites: []`) → exit 0; `tolerance: 0` em **todos** os `numeric` → exit 0;
      `tolerance: 0.0` (float) com `answer: 0` e `answer: -0.0` → exit 0. Zero é aceito nas
      três formas.
- [x] **5. Mensagem acionável.** Das 21 linhas da fixture de critério 1, **21/21** casam
      `arquivo: localizador: [REGRA] o que fazer`; localizadores medidos: `items[i] (id=…)`,
      `items[i] (id=…).options[j]`, `nodeId`, `title`, `summary`, `items`. Nenhuma linha
      genérica. Mantida em terminal ASCII (`env -i LC_ALL=POSIX PYTHONUTF8=0`).
- [x] **6. Nó piloto real.** `validate-content.py high-school/algebra/quadratic-equations`,
      sem argumento e via `.sh` → `exit 0 · 0 · 0`. `content/` intocado: `git status
      --porcelain content/` = 0 linhas e hash `dad502b194460c91…` idêntico antes e depois de
      tudo o que rodei (inclusive da suíte).
- [x] **7. Zero dependência nova.** AST própria em `validate-content.py`: imports =
      `__future__, argparse, dataclasses, json, math, os, pathlib, sys`; **fora da
      `stdlib_module_names`: []**. Nenhum arquivo de dependência Python criado ou alterado.
      Justificativa do mecanismo de teste registrada em `[004]` e coerente com o precedente
      `tools/context-watch-test.sh`.
- [x] **8. Sem decisão de framework.** Busca negativa nos três artefatos por
      `astro|react|vue|svelte|next|vite|vercel|tailwind|indexeddb|service worker|playwright|
      jest|vitest|pytest|express|fastapi|django|flask` → **zero ocorrências**. Roda por CLI
      puro, com `--root` arbitrário. `content/` intocado (acima).
- [x] **9. Auditorias.** `audit-content.sh` → exit 0 (`1 nós · 0 erros · 0 avisos`);
      `audit-ai-surface.sh` → exit 0 em **3 execuções seguidas** (`Resultado: OK`).

### Suíte — contada por fora e em 4 ambientes

`grep -c '^ok   '` = **118**, `FAIL` = 0, `skip|pend|todo` = 0 — o número bate com o que o
script imprime. Verde em: (a) shell normal; (b) `env -i PATH=/usr/bin:/bin HOME=<tmp>
TMPDIR=<tmp>`; (c) `LC_ALL=C LANG=C`; (d) **ambiente meu, não declarado pelo produtor**:
`env -i` + `LC_ALL=POSIX LANG=POSIX PYTHONUTF8=0 PYTHONCOERCECLOCALE=0` → 118/0. Suíte
hermética confirmada.

Regressão do **B2** medida por mim, 11 combinações: erro de uso com `2>&1 | true`,
`2>/dev/full`, `2>&- >&-`, `--xx | pipe`, guarda do `--root` → `2` em todas; violação com
`| head`, `>/dev/full 2>/dev/full`, `--quiet` com canais fechados, `--json | pipe` → `1`;
íntegro com ambos os canais fechados → `0`; `--help` em `/dev/full` → `0`.

### Casos hostis de UI: não aplicável, com a prova

O artefato é um executável de linha de comando; não há interface neste diff. Consumidores
hoje: `package.json` (`prebuild` → `npm run validate:content`, do TCK-0015 paralelo) e uma
**citação em comentário** em `src/content-contract/index.js:18` — nenhum código de
apresentação. Offline/PWA, tema, zoom 200%, teclado e leitor de tela não têm superfície aqui.
O que **é** aplicável eu exercitei: **os dois idiomas** (paridade campo a campo, chave
ausente, idioma fora do contrato, texto vazio) e **formato decimal** (`answer: "3,5"` e
`tolerance: "0,1"` recusados com orientação de ponto decimal); **dados vazios** (nó sem
exercícios, `items: []`, `options` com 1 alternativa, raiz sem nenhum nó).

### Minhas fixtures de burla — objetivo: fazer o portão aprovar o que deveria reprovar

Montei quatro famílias novas (nenhuma repetida do produtor ou do revisor). **Sete falsos
negativos encontrados, todos fora dos critérios 1–9 e do RF-18 enumerado**; nenhum deles
inverte um veredito para "aprovado" em regra contratada.

1. **B-QA-1 — "vazio invisível".** `title.en-US = U+200B`, `summary.en-US = U+2060 U+FEFF`,
   `stem.en-US = U+200B` → **exit 0, "Contrato íntegro"**. `str.strip()` não remove espaços
   de largura zero. Controles corretos: NBSP e `\t\n` → exit 1 (`LOCALIZED-EMPTY`). Um nó
   monolíngue na prática atravessa o portão bilíngue. → **D-2**.
   No mesmo lote: `short-answer` com `answer: "   "`, `answer: false` e `answer: 0` → exit 0;
   controle `answer: ""` → exit 1. → **D-3**.
2. **B-QA-2 — os tipos sem exemplar real.** `proof` e `step-by-step` **sem `rubric`** —
   campo marcado como obrigatório em `docs/content/exercise-schema.md:80` — passam (exit 0);
   `matching` com as duas opções corretas idênticas passa; `ordering` com
   `answer: "qualquer coisa"` passa. → **D-4**.
3. **B-QA-3 — identidade e visibilidade entre arquivos.** (a) `assessments.json` com gabarito
   invertido **é pego** (3 × `MC-MULTIPLE-CORRECT-OPTIONS`) — o segundo arquivo é varrido de
   verdade. (b) `exercises.json` copiado para `assessments.json` (mesmos `id` de item nos
   dois) → **exit 0**: `seen_ids` é por arquivo (`validate-content.py:554`) → **D-6**.
   (c) subnó só com `theory.pt-BR.md` (monolíngue, sem `meta.json`) → **invisível às duas
   ferramentas** (`audit-content.py:88-90` só reconhece `meta.json`) → **D-7**.
4. **B-QA-4 — sentinela e números.** `exercises.json` contendo literalmente `null` →
   **exit 0, "Contrato íntegro"**: `load_json` devolve `None` e `validate_exercise_file:524`
   trata "conteúdo null" como "arquivo ausente". É um desvio de 4 caracteres na regra
   `ITEMS-EMPTY` recém-criada (`[]` reprova, `null` passa). `exercises.json` como symlink
   quebrado: mesmo efeito. → **D-5**. Pegos corretamente: arquivo de 0 bytes
   (`JSON-INVALID`), `meta.json` como array (`META-NOT-OBJECT`), `meta.json` symlink quebrado
   (`NODE-META-MISSING`), `nodeId` com barra final (`NODE-ID-MISMATCH`).

**Nenhum dos sete tem o auditor como o mais estrito.** Rodei os cinco principais nas duas
ferramentas, numa cópia isolada do repositório: `audit=0 · validate=0` em todos. A afirmação
do cabeçalho ("onde há sobreposição, este validador prevalece") **sobreviveu** ao meu ataque.

### Defeito real, não bloqueante, com gatilho — D-1

`answer` (ou `tolerance`) com **literal inteiro ≥ 10^309** derruba o validador:
`validate-content.py:438` e `:452` chamam `float(item[...])` sem proteção →
`OverflowError: int too large to convert to float`, traceback, **zero violações listadas** e
a execução do acervo inteiro abortada. Limiar medido: `10^307` e `10^308` passam,
`10^309` e `10^400` quebram; a notação float `1e400` é tratada certo
(`NUMERIC-ANSWER-NOT-FINITE`). Com canal quebrado (`2>&1 | true`) o código vira **120** — o
sintoma do B2 num caminho que a correção do `[007]` não cobre (o traceback é emitido pelo
interpretador, fora de `emit`/`emit_err`).

**Por que não bloqueia:** a direção do erro é conservadora — com canais íntegros o veredito é
`exit 1` (conteúdo barrado), nunca `0`; não é falso negativo. Nenhum critério do ticket nomeia
esse caso, e o acervo atual (1 nó) não o produz. **Gatilho escrito:** o primeiro item
`numeric` com inteiro fora da faixa de `float` — plausível em `number-theory` e `research`
(ex.: `2^1024` = 309 dígitos) — transforma esta dívida em defeito. Correção é de duas linhas
(`try/except OverflowError` → `NUMERIC-ANSWER-NOT-FINITE`). Recomendo resolver **antes** de o
`prebuild` do TCK-0015 virar bloqueio de release.

### Pontos de julgamento pedidos

- **(a) `ITEMS-EMPTY` e `JSON-DUPLICATE-KEY` — concordo com o revisor, com uma ressalva.**
  Conferi as duas condições que sustentam o argumento: (i) o ticket atribui a este trabalho
  definir "o que 'conteúdo válido' significa" (§Requisito refinado) e o "Fora de escopo" lista
  `content/`, spec, ADRs e o schema de `references.json` — nenhum tocado
  (`git status --porcelain content/ docs/` limpo para os dois); (ii) nenhuma **contradiz** o
  documentado: a regra 8 de `docs/content/exercise-schema.md:107` exige **8–12 itens**, então
  `ITEMS-EMPTY` (falha só em 0) é estritamente **mais frouxa** que a norma escrita, e
  `JSON-DUPLICATE-KEY` é boa-formação de arquivo, sobre a qual o schema é silente. Regra que
  cabe dentro da norma existente não é contrato novo: é a norma sendo parcialmente
  automatizada. Não exigiria decisão prévia. **Ressalva:** `ITEMS-EMPTY` é assimétrica — nó
  **sem** `exercises.json` passa (exit 0), nó **com** o arquivo e `items: []` reprova, e nó com
  o arquivo em `null` volta a passar (D-5). A regra pune declarar vazio e não pune omitir;
  quem reconcilia o schema (encaminhamento 3) precisa decidir isso junto.
- **(b) Adendo na L-019 — confirmado nos dois pontos.** Li o arquivo: o adendo (linhas 39-73)
  admite a reincidência com nome, explica **por que escapou** ("corrigi os dois casos citados
  pela minha própria suíte, e escrevi a lição descrevendo os casos, não a classe"), referencia
  L-013/L-018 e — o que importa — a seção "Como aplicar (revisão da regra, mais forte que a
  original)" troca a lista de casos por **regra de classe**: *travessia* ("nenhum caminho de
  código pode encerrar a varredura no alvo", com teste obrigatório de objeto quebrado um nível
  abaixo comparado à raiz), *canais* ("stdout **e** stderr, incluindo o texto emitido por
  bibliotecas", matriz `| true` × `>&-` × `>/dev/full` × 3 códigos) e *codificação*. Fecha com
  a meta-regra "escrever a classe, nunca a lista de casos corrigidos". As três viraram
  asserção e eu as exercitei fora da suíte: classe 1 → casos 14–14d, reproduzida com fixture
  minha de **dois** níveis; classe 2 → casos 15–15h, reproduzida em 11 combinações; classe 3 →
  caso 16, reproduzido em `env -i LC_ALL=POSIX PYTHONUTF8=0`. Adendo é o registro correto:
  L-019 não foi superada, foi violada e ampliada. **Nota honesta:** o D-1 acima é uma variante
  da classe 2 num caminho que nem a regra ampliada alcança (traceback do interpretador) — é
  material para um segundo adendo quando for corrigido, não para um `REJECT`.
- **(c) Cobertura sintética — dívida aceitável, não compromete o critério 1; e é maior do que
  foi declarado.** Contei o acervo inteiro: **1 nó, 5 itens, só `multiple-choice` (3) e
  `numeric` (2)**. Sem exemplar real ficam **seis** tipos, não quatro: além de `matching`,
  `ordering`, `proof` e `step-by-step`, também **`short-answer`** e **`true-false`** — e
  `true-false` importa porque está em `SINGLE_CORRECT_TYPES` e é exatamente onde o
  `audit-content.py` diverge (ver encaminhamento 1). O critério 1 pede que o validador saia
  com erro quando o contrato é violado e liste todas as violações; ele não pede cobertura por
  tipo com conteúdo real, e o critério 6 fixa o piloto como a âncora de "sem falso positivo".
  Não compromete. Mas a dívida deixou de ser hipotética: **eu medi um falso negativo concreto**
  em `proof`/`step-by-step` (D-4, `rubric` ausente). Gatilho: o primeiro nó real com um desses
  seis tipos exige revisitar as regras antes de publicar.

### Achado do `audit-content.py` — 4 instâncias reproduzidas, todas confirmadas

Medidas por mim numa **cópia isolada do repositório** (`content/` real intocado — hash
conferido), sempre com o auditor e o validador rodando sobre o mesmo arquivo:

| Mutação | `audit-content.py` | `validate-content.py` |
|---|---|---|
| `"correct": "false"` (texto) na única alternativa de gabarito | **exit 0** · `1 nós · 0 erros · 0 avisos` | exit 1 · `CORRECT-NOT-BOOLEAN` + `MC-NO-CORRECT-OPTION` |
| `title.en-US: 5` | **exit 0** · `0 erros` | exit 1 · `LOCALIZED-NOT-STRING` |
| `title.en-US: None` | **exit 0** · `0 erros` | exit 1 · `LOCALIZED-NOT-STRING` |
| `true-false` com 2 opções `correct: true` | **exit 0** · `0 erros` (só AVISO de dicas) | exit 1 · `MC-MULTIPLE-CORRECT-OPTIONS` |
| Controle: MC sem nenhuma correta | exit 1 · 1 erro | exit 1 |

Causa das quatro: veracidade implícita (`o.get("correct")`, `audit-content.py:229`/`:240`),
`str(value.get(lang,""))` (`:85`) e o `>1` verificado só para `multiple-choice` (`:236`).
Consequência operacional: **hoje é possível ter exercício com gabarito errado, ou título
inexistente em en-US, passando na auditoria em silêncio.** `audit-content.py` **não foi
tocado** — é ticket próprio do `tech-lead`.

### Pendências entregues ao `tech-lead`

1. **Ticket próprio para `scripts/audit-content.py`** — as 4 instâncias acima, mesma classe.
   Enquanto existir, o auditor é o elo fraco da malha; com o `prebuild` do TCK-0015 já
   chamando o validador, o portão estrito passa a governar o build, mas o auditor continua
   sendo o que roda no CI de conteúdo.
2. **Natureza da `tolerance` (absoluta × relativa)** — decisão de contrato **necessária antes
   das tasks 5–8**, onde a correção de resposta a torna observável. Confirmei que hoje o
   validador **não** decide: `:448-458` só exige número finito ≥ 0, regra idêntica nas duas
   leituras; e o registro em `memory/context/backend.md:38-43` diz exatamente isso.
3. **`docs/content/exercise-schema.md` alcançar as regras novas** (`ITEMS-EMPTY`,
   `ITEM-ID-DUPLICATE`, `JSON-DUPLICATE-KEY`, `version`, `unit: null`), mais a assimetria do
   `ITEMS-EMPTY` apontada em (a) — trabalho de `docs-writer` pós-`done`.

### `ACTION` fora do escopo deste ticket

- **A task 11 já foi parcialmente antecipada pelo TCK-0015**: `package.json` traz
  `"prebuild": "npm run validate:content"`. Não é defeito deste ticket e não bloqueia, mas
  muda a urgência de **D-1** (traceback derruba o build com mensagem inútil) e de **D-5**
  (`null` atravessa o portão que o build passou a confiar).
- **Dívidas registradas (nenhuma bloqueante):** D-1 overflow (com gatilho); D-2 vazio de
  largura zero; D-3 `answer` inútil em `short-answer`/`ordering`; D-4 `rubric` sem regra;
  D-5 `null`/symlink quebrado tratado como arquivo ausente; D-6 `id` de item repetido entre
  `exercises.json` e `assessments.json` (as duas ferramentas erram); D-7 diretório só com
  `theory.*.md` invisível às duas ferramentas; D-8 seis dos oito tipos sem exemplar real.
  D-1, D-2 e D-5 são as três que eu resolveria antes do primeiro lote grande de conteúdo.

- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9
  — todos com evidência reproduzida por mim. **Ticket `done`.**

## [011] CORRECTION — 2026-08-01 18:55 — qa-validator#8

- Corrige: `[010]`, linha "commit `5d1e2b6` (HEAD igual no início e no fim)". **Não ficou
  igual.** Entre a última reexecução e o registro do veredito, o working tree compartilhado
  recebeu `9aa25d9` ("TCK-0011: C4 Container e os ADRs de CI/CD e do esqueleto"), de outro
  ticket em paralelo.
- Verificação feita depois do avanço do HEAD, antes de fechar: os três artefatos do TCK-0014
  continuam **não rastreados** (`??` em `git status --porcelain`) e não aparecem no
  `--name-only` do commit novo — ou seja, não foram tocados; `scripts/validate-content.py`
  segue com md5 `ae91c7a5671e6962d44ead96713de8b8`. Reexecutado agora: suíte **118 passaram,
  0 falharam**; `validate-content.py` no acervo → `exit 0`; `audit-content.sh` → `exit 0`;
  `audit-ai-surface.sh` → `exit 0`; `git status --porcelain content/` → 0 linhas; hash de
  `content/` → `dad502b194460c91…`, o mesmo do início da validação.
- Leitura correta: a validação começou em `5d1e2b6` e foi confirmada em `9aa25d9`, com os
  artefatos e o acervo inalterados entre os dois. O veredito **`done`** do `[010]` permanece.
- Resultado: ok — registro corrigido, sem mudança de veredito.
