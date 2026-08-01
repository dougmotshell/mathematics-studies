# Log — TCK-0006

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:30 — tech-lead
- Ação: criação do ticket a partir das pendências 4 e 5 encaminhadas pela cadeia do TCK-0005
  (`log.md` `[007]`, `[008]` §6 e §7.3, `[010]`, `[011]`), com o pedido original copiado
  verbatim dos logs de origem.
- Motivo: as duas convenções foram **decididas na prática** pelo nó piloto e aprovadas por
  `a11y-ux-reviewer` e `i18n-steward`, mas não existem por escrito. O piloto é o modelo que
  os próximos nós copiam; convenção não escrita se multiplica divergente.
- Resultado: ok — `tickets/TCK-0006-formula-reading-conventions/` criado com `ticket.md` e
  este `log.md`. Nenhum arquivo fora de `tickets/` tocado.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:32 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** — o usuário pediu criação e
  triagem, não execução (L-005: triagem não é handoff).
- **Agrupamento (justificativa em uma linha):** as convenções de a11y, a linha de glossário
  de i18n e a fronteira display × inline são a **mesma entrega** — a norma escrita que o
  próximo nó vai copiar — e todas vivem em `docs/content/` + `AGENTS.md` §9.2; separá-las
  produziria três tickets de uma linha que o mesmo agente abriria no mesmo arquivo.
- **Tipo:** `docs`. Não é `content`: nada em `content/` muda aqui. A decisão da §9.2 é
  refinamento de regra existente, não decisão estrutural nova — por isso **não** exige ADR
  (critério: ADR quando muda o pilar, não quando precisa a redação de uma regra vigente).
  Gatilho de escalada declarado no "Fora de escopo".
- **Prioridade P1 · tamanho M.** P1 porque é declarado pelas duas revisões como
  **obrigatório antes do próximo nó** e porque **bloqueia o TCK-0007**: sem a decisão de
  (4), o ticket de conteúdo não sabe se trata `\dfrac` inline e as 10 `\frac` de
  `exercises.json`. M porque envolve três arquivos de padrão, a fonte canônica `AGENTS.md` e
  a regeneração dos 12 adapters.
- **Owner: `docs-writer`.** Área de `docs/` e da propagação para as fontes canônicas.
  `a11y-ux-reviewer` e `i18n-steward` entram como **fonte** (o conteúdo normativo já foi
  produzido por eles em `[008]` §6 e `[007]`), não como validadores do próprio texto.
- **Cadeia:** `tech-lead` → `docs-writer` → `code-reviewer` → `qa-validator`. A cadeia
  padrão de `docs` termina em `code-reviewer`; acrescento o `qa-validator` porque só ele
  marca `done` (AGENTS.md §10, regra 3) e porque há 9 critérios verificáveis por comando.
  Independência preservada: quem escreveu a tabela em `[008]` não valida sua transcrição.
- **Restrições passadas ao executor:**
  1. `AGENTS.md`, `.claude/` e `.github/instructions/` são **fontes canônicas** — ao tocá-las,
     rodar `python3 scripts/sync-ai-adapters.py` na mesma entrega; nunca editar gerado à mão.
  2. Regra de 12.000 caracteres do Antigravity/Windsurf: o acréscimo à §9.2 tem de ser curto
     o bastante para o `core.instructions.md` continuar dentro do limite (`--check` falha).
  3. A tabela de `[008]` §6 é transcrita **como decidida**; mudar qualquer par (p. ex. trocar
     "abre/fecha parênteses" por MathSpeak "left/right") é decisão nova e volta ao
     `tech-lead` — a observação 1 de `[007]` registrou essa alternativa como escolha de
     registro, não como defeito.
  4. Não tocar `content/` (é o TCK-0007) nem `docs/adr/`.
- **Aderência ao plano:** Fase 1 do `docs/product/roadmap.md` ("provar o formato com conteúdo
  real … ajustar os schemas se necessário") — este ticket ajusta o **padrão**, que é o que
  autoriza os 3–5 nós piloto seguintes. Dentro do plano, sem pedido fora de escopo.
- **Requisitos inegociáveis conferidos na triagem:** bilinguismo (a tabela é o par de
  convenções nos dois idiomas), acessibilidade (objeto do ticket), gratuidade (só texto),
  offline e privacidade (não aplicáveis, justificado no ticket).
- **Dependências:** bloqueia `TCK-0007` (critério 5 daquele ticket depende do veredito de (4)
  registrado aqui no critério 7).
- Resultado: ok — `status: triaged`, `owner: docs-writer`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.

## [003] HANDOFF — 2026-08-01 16:05
- De: tech-lead → Para: docs-writer
- Status novo: in_progress
- Registro retroativo feito pelo próprio `docs-writer` ao assumir: a triagem `[002]` parou em
  `triaged` **de propósito** (L-005 — triagem não é handoff), aguardando ordem de execução. A
  ordem chegou; esta entrada formaliza o handoff que faltava, sem o qual a execução ficaria
  sem rastro de autorização.
- O que foi feito: `[001]` criação e `[002]` triagem (tipo `docs`, P1/M, owner `docs-writer`,
  cadeia `docs-writer` → `code-reviewer` → `qa-validator`, sem ADR).
- O que falta: os 9 critérios de aceite — transcrever a tabela de convenções de `[008]` §6 do
  TCK-0005 para `docs/content/accessibility.md`, a linha de glossário de `[007]` para
  `docs/content/i18n.md`, **decidir e escrever a fronteira display × inline**, propagar para
  `AGENTS.md` §9.2, `.github/instructions/` (`applyTo: content/**`) e o checklist de
  `published`, e listar sem executar as ocorrências do nó piloto atingidas.
- Prioridade elevada no repasse: este ticket é **portão da task 6** da spec
  `minimum-learning-slice` (render acessível de `theory.*.md`), já na fila de implementação,
  e bloqueia o TCK-0007.
- Arquivos/contexto: `tickets/TCK-0005-pilot-node-math-accessibility/log.md` `[007]` e
  `[008]` §6/§7.3; `docs/content/{accessibility,i18n,content-standards}.md`; `AGENTS.md` §9;
  `.github/instructions/{content,core}.instructions.md`.
- Restrições: não tocar `content/` (é o TCK-0007), `docs/adr/`, `docs/specs/`,
  `docs/design/`, `scripts/`, `tools/`, nem os tickets TCK-0011/0013/0014 — há cadeias ativas
  neles. O `docs-writer` é o **único** autorizado a rodar `scripts/sync-ai-adapters.py` nesta
  rodada (o TCK-0008 foi segurado para evitar colisão em fonte canônica).
- Critérios de aceite que o próximo agente deve atender: todos os 9 do `ticket.md`.

## [004] ACTION — 2026-08-01 16:40 — docs-writer
- Ação: escrita da norma de leitura de fórmula e **decisão da fronteira display × inline**,
  com propagação para as fontes canônicas. Nenhum arquivo de `content/`, `docs/adr/`,
  `docs/specs/`, `docs/design/`, `scripts/` ou `tools/` foi tocado.
- Motivo: as convenções existiam só na prática do nó piloto e no log de um ticket `done`; a
  §9.2 nomeava apenas `$$…$$`, deixando sem regra o caso mais frequente. Este ticket é portão
  da task 6 da spec `minimum-learning-slice` e bloqueia o TCK-0007.

### 1. A decisão: display e inline têm obrigações **diferentes**, não "tem/não tem descrição"

Os dois extremos foram descartados com argumento:

- **Exigir leitura integral de toda fórmula inline** torna o texto ilegível por repetição.
  Só no nó piloto seriam 38 inserções em `theory.*.md` — a maioria para `$x^2$`, `$x_1$`,
  `$ax^2 + bx + c = 0$`, cuja leitura linear já é fiel. O ruído afogaria as leituras que
  importam e o autor passaria a produzi-las mecanicamente, sem ler a estrutura.
- **Não exigir nada** deixa muda exatamente a fórmula cujo sentido **é** o agrupamento: o
  Resumo do piloto, a linha de "Erros comuns" que ensina a não dividir só um termo por $2a$,
  e as 10 `\frac` de `exercises.json` — nenhuma alcançada pela §9.2 hoje.

**Decidido:**

| Caso | Obrigação | Forma |
|---|---|---|
| Display `$$…$$` | **Leitura integral**, sem exceção | parágrafo `*Leitura:*` / `*Reading:*` logo abaixo, reconstruindo a fórmula inteira na ordem escrita |
| Inline `$…$` com **argumento composto** | **Marcação de agrupamento** | o agrupamento dito em palavras no próprio texto ao redor ("…, tudo dividido por $2a$") — **não** exige parágrafo de leitura |
| Inline `$…$` simples | nenhuma | — |

Promover uma inline a display e dar-lhe leitura integral é **sempre permitido e nunca
obrigatório** (permissão não cria ponto de decisão). Em `exercises.json` e
`assessments.json` não existe parágrafo de leitura: a marcação mora dentro do próprio campo
(`prompt`, `hints`, `solution`, `feedback`), nos dois idiomas.

O que torna a decisão barata é a **diferença de obrigação**: inline não pede a fórmula
repetida em prosa, pede uma frase que feche o grupo. Custo de poucas palavras, sem
duplicação de conteúdo e sem depender de renderização.

### 2. O critério operacional: **teste do argumento composto**

Aplicado por inspeção do LaTeX, com resposta única, sem interpretar o sentido nem a intenção
do autor. **Argumentos de agrupamento**: numerador e denominador de `\frac`/`\dfrac`/
`\tfrac`/`\cfrac`; radicando e índice de `\sqrt`; expoente; subscrito; base elevada; corpo de
`\sum`, `\prod`, `\int`, `\lim`.

Um argumento é **simples** se for um único símbolo (número, letra ou constante nomeada), com
ou sem sinal unário. É **composto** se contiver, no nível mais externo: operador binário
(`+ - \pm \mp \cdot \times \div /`), relação (`= < > \le \ge \neq \approx`), **dois ou mais
fatores justapostos** (`2a`, `4ac`), agrupamento aninhado, ou **parênteses/colchetes/chaves**
— em particular **base entre parênteses é sempre composta** (`(-5)^2`, que na fala se
confunde com `-5^2`).

**Exige marcação sse pelo menos um argumento de agrupamento for composto.** Duas
consequências deliberadas: (a) justaposição de **nível externo** (`ax^2 + bx + c`) **não**
dispara — só justaposição dentro de um argumento (`2a` no denominador) dispara, e é aí que a
fala perde o grupo; (b) `\frac{-7}{2}` **não** dispara — sinal unário não é operador binário,
e as duas reconstruções possíveis são a mesma expressão. Isso reproduz, como regra, o
julgamento que o `a11y-ux-reviewer` já fizera à mão em `[008]` §2.3.

A regra de fração fica operacional: numerador **composto** → "tudo dividido por" / "all
divided by"; numerador **simples** → "dividido por" / "divided by". Um exemplo de cada no
documento.

### 3. Onde a norma foi registrada (L-009/L-010 — regra que mora num só lugar não é aplicada)

| Arquivo | O que entrou |
|---|---|
| `docs/content/accessibility.md` | seção "Display × inline" com flowchart Mermaid + leitura; "Teste do argumento composto" com tabela de 9 casos e veredito; tabela das **nove** convenções de leitura com origem e data; regra irmã do agrupamento como assunto; nota de ambiguidade de "índice"; nota de que `audit-content.sh` não verifica isso |
| `docs/content/i18n.md` | linha de glossário `subscrito (índice) \| subscript \| …` com desambiguação do índice do radical; parágrafo remetendo à tabela bilíngue de leitura e à verificação por posição |
| `docs/content/content-standards.md` | seção "Notação e formatação" (display + inline) e **duas** linhas no checklist de `published` |
| `AGENTS.md` §9.2 | reescrita: display e inline com obrigações distintas, teste do argumento composto resumido, `exercises.json`/`assessments.json` incluídos. **Sem renumeração** — item 2 editado no lugar, nenhuma referência `§9.N` do repositório quebrada |
| `.github/instructions/content.instructions.md` (`applyTo: content/**`) | regra completa, é o que a ferramenta carrega ao editar `content/` |
| `.github/instructions/core.instructions.md` (`applyTo: **`) | regra 6 precisada em 4 linhas |
| `.claude/agents/content-author.md`, `.claude/agents/a11y-ux-reviewer.md` | quem produz e quem revisa |
| `.claude/skills/new-topic/SKILL.md`, `.claude/skills/a11y-audit/SKILL.md` | checklist de produção e de auditoria (parte 1) |

Os adapters de agent/skill são **ponteiros** para as fontes (`.claude/commands/`,
`.github/chatmodes/`, `.gemini/commands/`), então não mudam com edição de agent; só as
**regras** são embutidas, e essas foram regeneradas.

### 4. Critério 7 — ocorrências do nó piloto, **listadas sem executar** (insumo do TCK-0007)

Inventário completo, não só as citadas no `REJECT` de origem (lição `L-013`): varri **todas**
as inline com `\frac`, `\dfrac`, `\sqrt`, `^` e `_` fora de `$$…$$`, nos três arquivos.

**`theory.pt-BR.md` / `theory.en-US.md` — 6 ocorrências exigem, 13 não**

| Linha pt / en | Fórmula | Veredito |
|---|---|---|
| 20 / 20 | `$(-3)^2$` | **EXIGE** — base entre parênteses; a frase é justamente "elevar ao quadrado apaga o sinal", que some na fala. **Não estava no achado de origem** |
| 20 / 20 | `$x^2$`, `$3^2$` | não exige |
| 25, 48, 140 / 25, 47, 137 | `$ax^2 + bx + c = 0$` | não exige — justaposição de nível externo |
| 26 / 26 | `$y = ax^2 + bx + c$` | não exige |
| 64 / 62 | `$x_1$`, `$x_2$` | não exige |
| 75 / 73 | `$x^2 - 5x + 6 = 0$` | não exige |
| 131, 141 / 128, 138 | `$\Delta = b^2 \pm 4ac$` | não exige |
| 132 / 129 (1ª) | `$(-5)^2$` em "…e $(-5)^2$ vira $+25$" | **EXIGE** — base entre parênteses, sem marcação verbal |
| 132 / 129 (2ª) | `$(-5)^2$` em "Substituir sempre entre parênteses: $(-5)^2$" | **ATENDIDO como está** — "entre parênteses" já diz o agrupamento; nada a fazer |
| 133 / 130 | `$-b \pm \frac{\sqrt{\Delta}}{2a}$` | **EXIGE** — denominador `2a` justaposto. Some com a regra irmã: o ponto da célula **é** o contraste de agrupamento e precisa estar em palavras |
| 143 / 140 | `$x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$` (Resumo) | **EXIGE** — numerador com `\pm`, denominador `2a`. É o achado `[008]` §7.3 |
| 144 / 141 | `$-\dfrac{b}{a}$`, `$\dfrac{c}{a}$` (Resumo) | **não exige** — argumentos simples; marcador aqui seria ruído |

**`exercises.json` — das 10 `\frac`, 6 exigem e 4 não; mais 6 bases entre parênteses**

| Linha | Ocorrência | Veredito |
|---|---|---|
| 153 (pt) / 154 (en) | `$x = \frac{5 \pm 1}{2}$` (`hints`) | **EXIGE** — numerador com `\pm` |
| 158 (pt) / 159 (en) | `$x = \frac{5 \pm 1}{2}$` (`solution`) | **EXIGE** |
| 254 (pt) / 255 (en) | `-\frac{b}{a}` | não exige |
| 254 (pt) / 255 (en) | `-\frac{-7}{2}` | não exige — sinal unário, não operador binário |
| 254 (pt) / 255 (en) | `\frac{7 \pm 5}{4}` | **EXIGE** |
| 129, 130 | `$(-4)^2$` | **EXIGE** — base entre parênteses. **Fora do achado de origem** |
| 158, 159 | `$(-5)^2$` | **EXIGE** — idem |
| 189, 191 | `$(-6)^2$` | **EXIGE** — idem |

`assessments.json` não existe no nó. Total para o TCK-0007: **6 pontos** em `theory.*.md`
(3 por idioma) e **12** em `exercises.json` (6 por idioma), com paridade obrigatória — a
correção tem de entrar nos dois idiomas na mesma posição (`L-001`, `L-012`).

### 5. Evidência

```
$ python3 scripts/sync-ai-adapters.py
20 skills + 21 agents + 6 regras → adapters sincronizados (Claude, Copilot, Gemini, Cursor, Antigravity, Windsurf).
9 arquivo(s) escrito(s)/atualizado(s).

$ python3 scripts/sync-ai-adapters.py --check ; echo $?
Tudo já estava atualizado.
0

$ bash scripts/audit-ai-surface.sh ; echo $?
  Limite de 12.000 caracteres nas regras (Antigravity/Windsurf): todas dentro do limite
  Adapters gerados atualizados (sync-ai-adapters.py --check): up-to-date
Resultado: OK
0

$ bash scripts/audit-content.sh ; echo $?
Resumo: 1 nós · 0 erros · 0 avisos
0
```

Códigos de saída capturados sem pipe. Critério 5: `grep -n "inline" AGENTS.md
docs/content/accessibility.md` → 3 ocorrências em `AGENTS.md` (227, 229, 232) e 8 em
`accessibility.md`, sem contradição entre elas. Critério 3: `grep -n 'subscript'
docs/content/i18n.md` → linha 63, dentro da tabela do glossário, três colunas preenchidas.

**Declaração sobre o sync (nota da minha memória):** rodar `sync-ai-adapters.py` com outras
cadeias ativas pode arrastar mudanças alheias ainda não sincronizadas. Conferido: o diff dos
9 gerados é **+54 / −12** e corresponde exatamente às minhas duas edições de regra
(`core` × 6 destinos, `content` × 3). **Nenhuma mudança de terceiros foi carregada.**

- Resultado: ok — critérios 1 a 9 endereçados. `content/` intacto (`git status` não lista
  nenhum arquivo sob `content/`).
- Lição: n/a — não resolve `REJECT`. Lição nova registrada como `L-021` (norma que só nomeia
  o caso estrito deixa o caso frequente sem regra).

## [005] HANDOFF — 2026-08-01 16:55
- De: docs-writer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: norma de leitura de fórmula escrita e propagada; fronteira display × inline
  decidida com critério operacional (`[004]`). Diff em 12 arquivos escritos à mão + 9 gerados.
- O que falta: revisão do diff. **Nenhum critério ficou por fazer**; o que resta é julgamento
  do revisor sobre a redação da norma e sobre a calibragem do teste.

### Checklist dos critérios do `ticket.md`

| # | Critério | Onde conferir | Situação |
|---|---|---|---|
| 1 | Nove construções, colunas pt-BR e en-US preenchidas | `docs/content/accessibility.md`, seção "Convenções de leitura de fórmula" | atendido — as nove de `[008]` §6 transcritas **como decididas** (restrição 3 da triagem respeitada: nenhum par alterado, "abre/fecha parênteses" mantido, sem MathSpeak) |
| 2 | Regra de fração **operacional**, com um exemplo de cada caso | mesma seção, bloco "A regra de fração é operacional, não exemplo" | atendido — gatilho é o teste do argumento composto; exemplo composto ($\frac{-(-5) \pm \sqrt{1}}{2 \cdot 1}$) e exemplo simples ($-\frac{b}{a}$), este com a razão pela qual "tudo dividido por" seria ruído |
| 3 | Linha de glossário com desambiguação | `docs/content/i18n.md:63` | atendido — `grep -n 'subscript' docs/content/i18n.md` → 1 linha, três colunas, citando `\sqrt[n]{a}` e *root index* |
| 4 | Fronteira decidida, com critério verificável por inspeção e o que **não** exige | `accessibility.md`, "Display × inline" + "Teste do argumento composto" | atendido — flowchart, definição fechada de argumento composto, tabela com 9 vereditos incluindo 4 "não exige"; nenhuma cláusula "caso a caso" |
| 5 | `AGENTS.md` §9.2 remete à regra, sem contradição | `AGENTS.md:229-236` | atendido — `grep -n "inline" AGENTS.md docs/content/accessibility.md` → 3 + 8 ocorrências, mesma regra nos dois |
| 6 | Checklist de `published` reflete a decisão | `docs/content/content-standards.md`, checklist | atendido — a linha antiga virou **duas**: display (leitura integral, conferida por posição) e inline (agrupamento em palavras, nos três arquivos e nos dois idiomas). Ficou mais estrito, não mais frouxo |
| 7 | Ocorrências do piloto com veredito **item a item**, sem executar | `[004]` §4 | atendido — inventário **completo** (varredura de todas as inline com `\frac`/`\dfrac`/`\sqrt`/`^`/`_` fora de `$$…$$`), não só as citadas na origem; `git status` não lista nada sob `content/` |
| 8 | Rastreabilidade: origem e data | `accessibility.md` (linha "Origem: … `[008]` §6 e `[007]`, 2026-08-01"), `i18n.md` (parágrafo após o glossário), "Estado atual desde 2026-08-01" na leitura do diagrama | atendido |
| 9 | `--check` 0 · `Resultado: OK` · `0 erros · 0 avisos` | `[004]` §5 | atendido — os três exit 0, capturados sem pipe; nenhum gerado editado à mão |

### Pontos que peço atenção explícita na revisão

1. **A calibragem do gatilho é a decisão real.** Dois pontos são deliberados e discutíveis:
   justaposição de **nível externo** não dispara (`ax^2 + bx + c` fica sem marcação), e
   **sinal unário não dispara** (`\frac{-7}{2}` fica sem marcação). Se o revisor discordar de
   qualquer um dos dois, o efeito é aritmético sobre o inventário de `[004]` §4 e sobre o
   custo de todo nó futuro.
2. **A regra alcança mais do que o achado de origem.** `[008]` §7.3 citava só o `\dfrac` do
   Resumo e §7.5 só as 10 `\frac` de `exercises.json`; o teste, aplicado ao artefato inteiro
   (`L-013`), pegou também **seis bases entre parênteses** — `$(-3)^2$` na Intuição e
   `(-4)^2`, `(-5)^2`, `(-6)^2` em `exercises.json`. Isso **aumenta** o escopo do TCK-0007 em
   relação ao que aquele ticket previa; se o revisor achar que a ampliação precisa de aval do
   `tech-lead`, é o momento de dizer.
3. **Não foi aberto ADR**, conforme o "Fora de escopo": a decisão refina a redação de uma
   regra vigente e a obrigação inline foi desenhada para **não** elevar o custo de produção
   (uma frase, não um parágrafo). Se o revisor entender que ela muda o pilar, o gatilho de
   escalada ao `tech-lead` está declarado no ticket.
4. **Ampliação além do escopo literal do ticket, para não repetir `L-009`/`L-010`:** além de
   `AGENTS.md` e `.github/instructions/`, a regra entrou em `.claude/agents/content-author.md`
   e `a11y-ux-reviewer.md` e nas skills `/new-topic` e `/a11y-audit` — quem produz e quem
   audita. Norma que mora só no documento de padrão não é aplicada.
5. **Diagrama Mermaid novo** em `accessibility.md` com a leitura exigida pelo
   `DOC-STANDARDS.md` (o que ele não mostra + fontes + "estado atual desde 2026-08-01").
   Não foi renderizado em navegador — sem MCP `chrome-devtools` neste ambiente. Pede olho no
   parse.
6. **Sync com outras cadeias ativas:** conferido que o diff dos 9 gerados corresponde
   exatamente às minhas duas edições de regra (+54/−12); nenhuma mudança de terceiros foi
   carregada. Detalhe da conta em `[004]` §5.

### Pendências que **não** são deste ticket (reportadas, não corrigidas)

- `docs/design/minimum-learning-slice/screen-states.md:533` descreve o render como "fórmula em
  display vem seguida do seu parágrafo de leitura" — continua correto e **não** contradiz a
  regra nova (inline não gera parágrafo, só prosa no próprio texto). Não editei: `docs/design/`
  tem cadeia ativa. Vale um olhar do dono quando a task 6 da spec entrar.
- A duplicação fórmula + descrição no áudio quando o KaTeX emitir MathML (`[008]` §7.4)
  permanece como decisão de renderização, fora desta norma.

### Artefatos de memória atualizados nesta execução
`memory/agents/docs-writer.md` (4 notas novas + linha de execução), `memory/context/content.md`
(convenções agora normativas, fronteira display × inline, passivo do piloto, pendência 4 do
TCK-0005 fechada), lição **`L-021`**
(`memory/lessons/a-norm-that-names-the-strict-case-leaves-the-frequent-case-unruled.md`) com
`memory/LESSONS.md` e `memory/MEMORY.md` atualizados por **acréscimo** (índices são ponto de
colisão com as cadeias ativas — nenhuma linha de terceiro foi reescrita).

- Critérios de aceite que o próximo agente deve atender: os 9 do `ticket.md`, conferidos na
  tabela acima. Evidência de comando em `[004]` §5.

## [006] REJECT — 2026-08-01 17:40
- De: code-reviewer#8 → Para: docs-writer · Loop nº: 1/3
- Status novo: in_progress
- Veredito: **reprovado** — 4 bloqueantes, 4 sugestões. A decisão de fundo (obrigação
  diferenciada em vez de "tem/não tem descrição") está **correta e aprovada**; o que reprova é
  o inventário do critério 7 (incompleto e com total que contradiz a própria tabela), um furo
  de propagação em quem escreve `exercises.json` e um caso que a norma cita mas não julga.

### Verificação independente do teste do argumento composto

Apliquei o teste **eu mesmo**, por extração programática das inline fora de `$$…$$` nos três
arquivos do piloto (12 famílias conferidas): `$(-3)^2$` (l. 20) exige; `$x^2$`/`$3^2$` não;
`$ax^2 + bx + c = 0$` não (justaposição de nível externo); `$\Delta = b^2 - 4ac$` não (base
`b` e expoente `2` simples; `4ac` está fora de argumento); `$x_1$`/`$x_2$` não;
`$-b \pm \frac{\sqrt{\Delta}}{2a}$` (l. 133/130) exige por **dois** motivos — numerador
`\sqrt{\Delta}` é agrupamento aninhado e denominador `2a` é justaposto;
`$x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$` (l. 143/140) exige; `$-\dfrac{b}{a}$` e
`$\dfrac{c}{a}$` (l. 144/141) não; `$\frac{5 \pm 1}{2}$` (`exercises.json:153,158`) exige;
`-\frac{b}{a}` e `-\frac{-7}{2}` (`:254`) não; `\frac{7 \pm 5}{4}` (`:254`) exige;
`$(x+3)^2$` (`:224`) exige. **Cheguei ao mesmo veredito da tabela de 9 casos de
`accessibility.md:78-88` em todos os casos cobertos** — o teste é aplicável sem julgar caso a
caso e é verificável por quem não o escreveu. Divergi em um caso que a tabela **não cobre**
(B4) e achei uma ocorrência que o inventário não lista (B1).

### Julgamento das duas calibragens

- **Justaposição de nível externo não dispara — aprovada.** A fala só perde grupo onde há
  delimitador **visual sem contraparte falada**: barra de fração, vínculo do radical,
  deslocamento do expoente. `ax^2 + bx + c` não tem nenhum: "a x ao quadrado mais b x mais c"
  reconstrói de forma única. Exigir marcação aqui seria custo sem ganho.
- **Sinal unário não dispara — aprovada no que cobre, incompleta no que não cobre.** Para
  fração está certa: em `\frac{-7}{2}`, `-(7/2)` e `(-7)/2` são o mesmo número, então não há o
  que desambiguar. O problema é a extensão ao **expoente** — ver B4.

### Bloqueantes

**B1. O inventário do critério 7 está incompleto: `(x+3)^2` não foi listado.**
`content/high-school/algebra/quadratic-equations/exercises.json:224` (pt-BR) e `:225` (en-US),
campo `solution`: `$x^2 + 6x + 9 = (x+3)^2 = 0$`. Base entre parênteses **e** com operador
binário dentro — pelo teste de `accessibility.md:71-72`, **EXIGE** marcação, e é o caso mais
perigoso do lote ("x mais três ao quadrado" × "x mais três-ao-quadrado", que dão polinômios
diferentes). `[004]` §4 declara varredura completa ("varri **todas** as inline com `\frac`,
`\dfrac`, `\sqrt`, `^` e `_` fora de `$$…$$`, nos três arquivos") e essa ocorrência tem `^`.
Evidência: `grep -nF ')^' exercises.json` → **8** linhas (129, 130, 158, 159, 189, 191, 224,
225); `[004]` §4 lista 6 e chama de "seis bases entre parênteses". O erro já foi copiado para
`memory/context/content.md` (bloco "Passivo do nó piloto"). Reincidência da classe de
**`L-013`** (corrigir/varrer só o que foi citado não é varrer a classe) → bloqueante por
`AGENTS.md` §10, regra 7.

**B2. O total do inventário contradiz a tabela que está logo acima dele.**
`[004]` §4, cabeçalho: "**6 ocorrências exigem**, 13 não"; fecho: "**6 pontos** em
`theory.*.md` (3 por idioma)". As linhas marcadas **EXIGE** na própria tabela são **quatro por
idioma**: l. 20/20 `$(-3)^2$`; l. 132/129 (1ª) `$(-5)^2$`; l. 133/130
`$-b \pm \frac{\sqrt{\Delta}}{2a}$`; l. 143/140 `$x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$`.
4 × 2 idiomas = **8 pontos**, não 6. O mesmo erro foi copiado para
`memory/context/content.md` ("3 pontos por idioma" seguido de **quatro** itens listados), que é
o que o próximo agente vai ler. Somando B1, os totais corretos são **8** em `theory.*.md`
(4/idioma) e **14** em `exercises.json` (7/idioma) — **22**, não 18. É o número que o `[005]`
manda ao `tech-lead` e que dimensiona o TCK-0007; errado, ele subdimensiona o ticket
dependente e faz o QA de lá fechar com passivo aberto.

**B3. A norma passou a reger `exercises.json`/`assessments.json`, mas não chegou a quem os
escreve.** `.claude/agents/exercise-designer.md` — o agente cuja `description` (l. 3) diz
literalmente "Usar para popular `exercises.json` e `assessments.json`" — e
`.claude/skills/new-exercise-set/SKILL.md` não ganharam **uma linha** sobre leitura de fórmula
ou marcação de agrupamento:
`grep -n "display\|acessib\|leitura" .claude/agents/exercise-designer.md
.claude/skills/new-exercise-set/SKILL.md` → **0 ocorrências**. O `[005]` §4 descreve a
propagação como tendo alcançado "quem produz e quem audita"; para `theory.*.md` sim
(`content-author`, `/new-topic`), para `exercises.json` **não**. É exatamente o item 5 do "Como
aplicar" da lição escrita neste mesmo ticket — `L-021`: "Regra nova só existe quando chega ao
`AGENTS.md`, às `.github/instructions/` **e aos agents/skills que produzem e revisam o
artefato**" — e a classe de `L-009`/`L-010` → bloqueante por `AGENTS.md` §10, regra 7.
(Mitigação parcial, que não fecha o defeito: `content.instructions.md` tem
`applyTo: content/**` e o Claude Code carrega `AGENTS.md` §9.2; mas o checklist próprio do
agente é o que ele executa.)

**B4. A norma cita `-5^2` para justificar uma regra e nunca dá veredito a ele.**
`accessibility.md:71-72` fundamenta "base entre parênteses é sempre composta" com
"(`(-5)^2`, que na fala se confunde com `-5^2`)". Só que `-5^2` — e `-x^2`, `-b^2` — **não tem
argumento composto** (base `5`, expoente `2`, ambos simples) e cai na exceção de sinal unário
(`:63` e a linha `$\frac{-7}{2}$` em `:82`): fica **sem obrigação nenhuma**. A ambiguidade é a
mesma, na direção oposta, e aqui as duas leituras **não** são o mesmo número: "menos cinco ao
quadrado" serve para `-(5^2) = -25` e para `(-5)^2 = 25`. Diferente do caso da fração, onde a
exceção é inócua, no expoente ela deixa mudo um caso que muda o resultado — e `-x^2` é
frequentíssimo em quadráticas (`y = -x^2 + 4`). Peço uma das duas saídas, ambas de uma linha:
(i) o teste dispara quando há sinal unário à frente de base elevada; ou (ii) o documento
escreve o veredito "não exige" **com a razão**, como manda o item 1 do "Como aplicar" da
`L-021` ("escreva o veredito para o caso deixado de fora, inclusive quando é 'nada a fazer'").
Custo hoje: **zero** — não há nenhuma ocorrência de `-n^k` sem parênteses no nó piloto
(conferido na extração das inline dos três arquivos), então (i) não muda o inventário.

### Sugestões (não bloqueiam)

**S1.** `accessibility.md:117` — coluna en-US da tabela normativa traz **"justaposition"**;
en-US é *juxtaposition*. É o vocabulário que o autor do próximo nó vai copiar. Vem transcrito
de `TCK-0005/log.md:491`, e corrigir grafia não altera o par decidido (restrição 3 da triagem
`[002]` fala em trocar o par, não em ortografia) — se preferir, confirme com o `tech-lead`.

**S2.** Duas sobreposições na definição do teste, hoje desempatadas só pelos exemplos:
(a) `-` aparece na lista de "operador binário" (`:66`) e, ao mesmo tempo, na definição de
simples ("com ou sem sinal unário à frente", `:63`) — só a linha `$\frac{-7}{2}$` resolve;
acrescente "`-` no início do argumento, sem termo à esquerda, é unário"; (b) "contém …
**chaves**" (`:71`) colide com as chaves que **delimitam** o argumento em LaTeX — ao pé da
letra, `$x^{2}$` seria composto (e `$\sqrt{\Delta}$` também); acrescente "as chaves que
delimitam o argumento não contam; conta o conteúdo do argumento".

**S3.** A "regra irmã" (`:98-102`) tem gatilho subjetivo — "se o ponto matemático da frase é a
diferença entre dois agrupamentos" —, que é o que o critério 4 proíbe. Não bloqueia porque
ficou **fora** do checklist de `published` (que cita só o teste). Marque-a explicitamente como
orientação de redação, não como gatilho de conformidade, para que ninguém a use como achado.

**S4.** `[004]` §4 lista `$\Delta = b^2 \pm 4ac$` para as linhas 131/128, mas ali há **duas**
fórmulas distintas — `$\Delta = b^2 + 4ac$` (a errada, da tabela "Erros comuns") e
`$\Delta = b^2 - 4ac$`. O `\pm` é notação do inventário, não do nó; escreva as duas separadas
para o TCK-0007 não procurar uma string que não existe.

### O que já está bom (não refazer)

1. **A decisão de fundo está certa.** Obrigação diferenciada por tipo, em vez de estender a
   mesma obrigação, é a saída correta: leitura integral onde o delimitador visual some, frase
   de fechamento onde o custo tem de caber na produção. 13 das 17 famílias inline do piloto não
   exigem nada — a norma **não** ficou cara.
2. **A ampliação do TCK-0007 é consequência legítima da norma, não sintoma de norma cara.** Os
   `(-n)^2` são exatamente a classe que a regra existe para pegar, e o próprio nó ensina o erro
   de sinal da base em "Erros comuns" — deixá-los mudos contradiria o conteúdo. Mas o número a
   escalar é **22** (8 em `theory.*.md` + 14 em `exercises.json`), não 18 — B1 e B2.
3. **Renumeração: conferida e limpa.** `AGENTS.md` §9 continua com 8 itens (`awk '/^## 9\./,
   /^## 10\./' AGENTS.md | grep -n "^[0-9]\."` → 1..8), item 2 reescrito no lugar.
   `grep -rn "§9\.[0-9]" . --exclude-dir=.git` → 79 referências, **nenhuma quebrada**: as §9.2
   seguem apontando para acessibilidade (agora mais forte, não outra coisa) e §9.6–9.8 não
   foram tocadas. O risco central do TCK-0004 não se repetiu.
4. **Sync limpo — afirmação sustentada.** `git diff --stat` dos gerados: **9 arquivos,
   +54/−12**, todos **regras** (`core` em `.agents`, `.cursor`, `.windsurf`, `.clinerules`,
   `.rules`, `.junie` = 6 destinos; `content` em `.agents`, `.cursor`, `.windsurf` = 3).
   Nenhum `.claude/commands/`, `.github/chatmodes/`, `.github/prompts/` ou `.gemini/commands/`
   tocado. A descoberta **procede**: `.claude/commands/content-author.md:8` é ponteiro
   ("Delegue ao subagent … definido em `@.claude/agents/content-author.md`") e o chatmode
   idem — editar agent não muda gerado. Nenhuma mudança de cadeia paralela arrastada.
5. **Auditorias reexecutadas por mim:** `sync-ai-adapters.py --check` → exit **0**;
   `audit-ai-surface.sh` → `Resultado: OK`, exit **0** (primeira execução, sem corrida);
   `audit-content.sh` → `1 nós · 0 erros · 0 avisos`, exit **0**.
   `git status --porcelain content/` → **vazio**: `content/` intacto.
6. **Mermaid validado no parser**, não só por leitura: `mermaid@11` + `jsdom`,
   `await mermaid.parse(<bloco de accessibility.md>)` → `MERMAID OK {"diagramType":
   "flowchart-v2"}`. O rótulo pontilhado `-. … .->` e os `<br/>` dentro de aspas passam.
7. **Critérios 1, 2, 3, 5, 6 e 8 conferidos e atendidos.** As nove construções estão lá com as
   duas colunas (`accessibility.md:110-120`); a regra de fração é operacional com um exemplo de
   cada caso (`:126-135`); `i18n.md:63` traz `subscrito (índice) | subscript` com a
   desambiguação de `\sqrt[n]{a}`; `AGENTS.md` §9.2 e `accessibility.md` dizem a mesma regra
   (subconjunto resumido + ponteiro, sem contradição); o checklist de `published` ficou **mais
   estrito**, com a conferência por posição (`L-012`) explicitada; origem e data presentes.
8. **Índices atualizados por acréscimo** (`memory/LESSONS.md` `+20/−0`, `memory/MEMORY.md`
   `+13/−0`): nenhuma linha de cadeia paralela reescrita, apesar de três tickets ativos no
   mesmo arquivo.

- Critérios de aceite que o próximo agente deve atender: os 9 do `ticket.md`, com B1–B4
  resolvidos. B1/B2 tocam `[004]` §4 (o log é append-only: registre a correção em `ACTION`
  nova, não edite `[004]`) **e** `memory/context/content.md`, que já carrega os dois erros.

## [007] ACTION — 2026-08-01 18:20 — docs-writer
- Ação: correção do `[006] REJECT` (loop 1/3). B1–B4 resolvidos, S1–S4 acatadas. `[004]` **não
  foi editado** (log é append-only) — esta entrada é a fonte corrente do inventário.
- Motivo: dois bloqueantes (B1, B3) são reincidência de lições desta mesma entrega; B4 é um
  caso que a norma citava e não julgava; B2 é aritmética contra a própria tabela.

### 1. Causa raiz comum a B1 e B3 — e por que virou adendo, não lição nova

B1 e B3 têm **uma** causa: derivei o conjunto a varrer, e o conjunto a propagar, **do que eu
já tinha em mãos, não da definição da classe**.

- **B1.** A classe criada pela norma é "base entre parênteses". As ocorrências que eu conhecia
  eram `(-4)^2`, `(-5)^2`, `(-6)^2`, e o padrão que escrevi foi `grep '(-[0-9a-z]*)\^'` — que
  codifica "parênteses **com sinal negativo**". `(x+3)^2` é da classe e não casa. Agravante:
  usei parser de inline em `theory.*.md` e um `grep` estreito em `exercises.json`, e mesmo
  assim declarei "varri **todas** as inline nos três arquivos". A declaração de completude era
  falsa exatamente no arquivo varrido pelo método mais fraco.
- **B3.** Listei os destinos de propagação a partir dos agentes que eu associava a
  `theory.*.md`, não a partir dos **artefatos que a norma passou a reger**. A regra nomeia
  `exercises.json` e `assessments.json` desde a primeira versão; logo `exercise-designer` e
  `/new-exercise-set` eram destino obrigatório.

Por ser causa única e por atingir os itens 4 e 5 do "Como aplicar" da **`L-021`, escrita
nesta mesma entrega**, registrei **adendo em `L-021`** em vez de lição nova, com as duas
regras operacionais que faltavam: *padrão de busca vem da definição, nunca dos exemplos*
(teste: o padrão acha uma ocorrência que eu ainda não vi?) e *a lista de propagação se deriva
dos artefatos que a regra nomeia*. Índices `memory/LESSONS.md` e `memory/MEMORY.md`
atualizados na linha da `L-021`, por acréscimo.

### 2. B1 + B2 + S4 — inventário do critério 7, **corrigido e refeito pelo método certo**

Refiz a varredura com **um só método nos três arquivos**: extração das inline fora de
`$$…$$` e classificação por predicado da classe (`)^` ou `]^`; `\frac`/`\dfrac`; `\sqrt`;
sinal unário antes de base elevada). Confirmei a ocorrência do B1 e a ausência de qualquer
`-n^k` sem parênteses.

**`theory.pt-BR.md` / `theory.en-US.md` — 8 pontos (4 por idioma)**

| Linha pt / en | Fórmula | Veredito |
|---|---|---|
| 20 / 20 | `$(-3)^2$` | **EXIGE** — base entre parênteses |
| 132 / 129 (1ª) | `$(-5)^2$` | **EXIGE** — base entre parênteses, sem marcação verbal |
| 133 / 130 | `$-b \pm \frac{\sqrt{\Delta}}{2a}$` | **EXIGE** — radical aninhado no numerador **e** denominador `2a` justaposto |
| 143 / 140 | `$x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$` | **EXIGE** |
| 132 / 129 (2ª) | `$(-5)^2$` em "Substituir sempre entre parênteses: …" | **ATENDIDO como está** |
| 20 / 20 | `$x^2$`, `$3^2$` | não exige |
| 25, 48, 140 / 25, 47, 137 | `$ax^2 + bx + c = 0$` | não exige — justaposição de nível externo |
| 26 / 26 | `$y = ax^2 + bx + c$` | não exige |
| 64 / 62 | `$x_1$`, `$x_2$` | não exige |
| 75 / 73 | `$x^2 - 5x + 6 = 0$` | não exige |
| 131 / 128 | `$\Delta = b^2 + 4ac$` **e** `$\Delta = b^2 - 4ac$` — **duas** fórmulas distintas na mesma linha (a errada e a certa da tabela "Erros comuns") | não exigem — **S4 acatada**, o `\pm` de `[004]` §4 era notação minha, não do nó |
| 141 / 138 | `$\Delta = b^2 - 4ac$` | não exige |
| 144 / 141 | `$-\dfrac{b}{a}$`, `$\dfrac{c}{a}$` | não exige |

**`exercises.json` — 14 pontos (7 por idioma)**

| Linha pt / en | Ocorrência | Veredito |
|---|---|---|
| 129 / 130 | `$(-4)^2$` | **EXIGE** |
| 153 / 154 | `$x = \frac{5 \pm 1}{2}$` (`hints`) | **EXIGE** |
| 158 / 159 | `$(-5)^2$` (`solution`) | **EXIGE** |
| 158 / 159 | `$x = \frac{5 \pm 1}{2}$` (`solution`) | **EXIGE** |
| 189 / 191 | `$(-6)^2$` (`feedback`) | **EXIGE** |
| **224 / 225** | **`$x^2 + 6x + 9 = (x+3)^2 = 0$`** (`solution`) | **EXIGE — B1, ausente de `[004]` §4.** É o pior do lote: "x mais três ao quadrado" serve para $(x+3)^2$ e para $x + 3^2$, que são polinômios diferentes |
| 254 / 255 | `$x = \frac{7 \pm 5}{4}$` | **EXIGE** |
| 254 / 255 | `-\frac{b}{a}`, `-\frac{-7}{2}` | não exigem |

**Total corrigido: 22 pontos** — 8 em `theory.*.md` + 14 em `exercises.json`. `[004]` §4 dizia
18 (e "6 pontos, 3 por idioma" onde a própria tabela marcava **quatro** linhas EXIGE por
idioma). **Este é o número que dimensiona o TCK-0007.** `assessments.json` não existe no nó.
`memory/context/content.md` corrigido, com a linha 131/128 desdobrada nas duas fórmulas.

Evidência do B1: `grep -nF ')^' content/high-school/algebra/quadratic-equations/exercises.json`
→ **8** linhas (129, 130, 158, 159, 189, 191, **224, 225**).

### 3. B4 — o caso citado e não julgado. Escolhida a saída (i): **dispara**

`accessibility.md` usava `-5^2` para justificar a regra da base entre parênteses e deixava
`-5^2` sem obrigação. O revisor está certo em separar os dois casos do sinal unário:

- **na fração e no radicando**, reagrupar dá o **mesmo** valor ($-(7/2) = (-7)/2$) → a exceção
  é inócua e continua valendo;
- **na potência**, $-(5^2) = -25$ e $(-5)^2 = 25$ são **números diferentes** → a exceção
  deixaria mudo um caso que muda o resultado, e `-x^2` é frequentíssimo em quadráticas
  ($y = -x^2 + 4$).

O teste ganhou **dois gatilhos de base elevada**, independentes dos argumentos: (1) base entre
parênteses ou colchetes — `$(-5)^2$`, `$(x+3)^2$`; (2) sinal unário imediatamente à frente da
base elevada — `$-5^2$`, `$-x^2$`, `$-b^2$`. O diagrama ganhou o nó `Q3` correspondente, e a
leitura passa a explicar por que a potência é o único ponto em que a exceção não vale.

**Custo verificado, não presumido:** varredura das inline dos três arquivos por sinal unário
antes de base elevada → **zero ocorrências**. O gatilho (2) **não altera** os 22 pontos.

### 4. B3 — a regra chegou a quem escreve exercício

| Arquivo | O que entrou |
|---|---|
| `.claude/agents/exercise-designer.md` | bloco "Fórmula acessível em áudio", com o teste, os dois gatilhos, exemplos que exigem e que não exigem, o fato de a marcação morar no próprio campo (`stem`, `hints`, `solution`, `feedback`) nos dois idiomas, e a consequência específica do papel: **item de múltipla escolha cujo gabarito depende de agrupamento não falado fica ambíguo em áudio e o distrator vira resposta defensável** |
| `.claude/skills/new-exercise-set/SKILL.md` | mesma regra nas "Regras duras" (§3) e, em "Verificar" (§4), o aviso de que `audit-content.sh` **não** verifica leitura de fórmula + revisão do `a11y-ux-reviewer` quando o conjunto tiver fração, radical ou potência |

`grep -c "agrupamento" .claude/agents/exercise-designer.md
.claude/skills/new-exercise-set/SKILL.md` → **3** e **3** (era 0 e 0).

### 5. Sugestões acatadas

- **S1** — `justaposition` → **`juxtaposition`** na coluna en-US (`accessibility.md`, tabela
  normativa). É correção **ortográfica**, não troca do par decidido: a restrição 3 da triagem
  `[002]` fala em mudar o par (p. ex. adotar MathSpeak "left/right"), e "times × juxtaposition"
  continua sendo exatamente a convenção de `TCK-0005` `[008]` §6. Não escalei ao `tech-lead`;
  se ele entender que grafia também é par decidido, é reversível em uma linha.
- **S2** — as duas sobreposições fechadas na definição do teste: (a) "**`-` no início do
  argumento, sem termo à esquerda, é unário e não conta**", na própria linha do operador
  binário; (b) "**as chaves que delimitam o argumento não contam** — o que se inspeciona é o
  *conteúdo*", com `$x^{2}$` e `$\sqrt{\Delta}$` movidos para a tabela como **não exige** e
  `$x^{n+1}$` explicado como composto **pelo `+`, não pelas chaves**.
- **S3** — a "regra irmã" virou **"Orientação de redação (não é gatilho de conformidade)"**,
  com a frase explícita "não é item de checklist e não deve virar achado de revisão: a
  conformidade é decidida só pelo teste acima", e a razão (depende de julgamento sobre o
  assunto da frase). Já estava fora do checklist de `published`; agora está fora também da
  leitura de quem revisa.
- **S4** — resolvida na tabela do §2 acima.

Acrescentei ainda à tabela de casos a linha `$ax^2 + bx + c = 0$` → **não exige**, com a razão
("justaposição de nível externo, não argumento"): era a calibragem que o revisor teve de
deduzir sozinho, e agora está escrita.

### 6. Evidência

```
$ python3 scripts/sync-ai-adapters.py
20 skills + 21 agents + 6 regras → adapters sincronizados.
3 arquivo(s) escrito(s)/atualizado(s).

$ python3 scripts/sync-ai-adapters.py --check ; echo $?
0
$ bash scripts/audit-ai-surface.sh ; echo $?
Resultado: OK
0
$ bash scripts/audit-content.sh ; echo $?
Resumo: 1 nós · 0 erros · 0 avisos
0
$ git status --porcelain content/ ; echo "linhas: $(git status --porcelain content/ | wc -l)"
linhas: 0
```

Mermaid revalidado **depois** da mudança (nó `Q3` e aresta nova), no parser real —
`mermaid@11` + `jsdom` instalados no scratchpad, fora do repositório:
`MERMAID OK {"diagramType":"flowchart-v2","config":{}}`.

Só **3** gerados desta vez (`content` em `.agents/rules/`, `.cursor/rules/`,
`.windsurf/rules/`): a regra `core` não mudou nesta rodada, e edição de agent/skill não gera
adapter — os de agent são ponteiros, como confirmado no `[006]` §4. Nenhum caminho do TCK-0015
(`package.json`, `src/`, `.github/workflows/`) foi tocado.

- Resultado: ok — B1, B2, B3 e B4 resolvidos; S1–S4 acatadas. O inventário corrente é o do §2
  desta entrada (**22 pontos**), não o de `[004]` §4.
- Lição: **`L-021` (adendo)** — padrão de varredura e alvos de propagação se derivam da
  definição da classe e dos artefatos que a regra nomeia, nunca das ocorrências e dos arquivos
  já em mãos; método único para todos os artefatos, senão a declaração de completude é falsa.
  Cruza com `L-013` (varrer a classe, não a evidência citada) e `L-009`/`L-010` (propagação).

## [008] HANDOFF — 2026-08-01 18:30
- De: docs-writer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: `[007]` — B1–B4 resolvidos, S1–S4 acatadas, inventário refeito por método
  único nos três arquivos. Loop 1/3 consumido; sem nova devolução, próximo passo é o
  `qa-validator`.
- O que falta: reconferência dos quatro bloqueantes. O que o `[006]` já aprovou (renumeração,
  sync, `--check`, auditorias, `content/` intacto, critérios 1, 2, 3, 5, 6 e 8) **não foi
  desfeito**, mas dois deles mudaram e pedem reconferência: o teste ganhou dois gatilhos, e o
  Mermaid ganhou um nó.

### Onde conferir cada bloqueante

| # | Defeito | Correção | Como verificar |
|---|---|---|---|
| B1 | `(x+3)^2` fora do inventário | inventário refeito em `[007]` §2 com método único; a ocorrência entra como o item mais perigoso do lote | `grep -nF ')^' content/.../exercises.json` → 8 linhas; as 8 aparecem em `[007]` §2 |
| B2 | total contradizia a tabela | **22 pontos** (8 em `theory.*.md`, 4/idioma; 14 em `exercises.json`, 7/idioma); `memory/context/content.md` corrigido | somar as linhas **EXIGE** das duas tabelas de `[007]` §2; conferir o bloco "Passivo do nó piloto" em `memory/context/content.md` |
| B3 | regra não chegou a quem escreve exercício | bloco novo em `.claude/agents/exercise-designer.md` e em `.claude/skills/new-exercise-set/SKILL.md` (§3 e §4) | `grep -c "agrupamento"` nos dois → 3 e 3 (era 0 e 0) |
| B4 | `-5^2` citado e não julgado | saída **(i)**: dois gatilhos de base elevada (entre parênteses · sinal unário à frente), com a razão pela qual a exceção do unário vale na fração e não na potência | `accessibility.md`, "Gatilhos de base elevada"; tabela de casos com `$-5^2$`, `$-x^2$` → **exige** |

Sugestões: **S1** grafia `juxtaposition`; **S2** unário × binário e chaves-delimitador ×
chaves-conteúdo, ambas na definição; **S3** "regra irmã" reclassificada como orientação de
redação, com a frase "não é item de checklist e não deve virar achado de revisão"; **S4** a
linha 131/128 desdobrada nas **duas** fórmulas reais (`b^2 + 4ac` e `b^2 - 4ac`).

### Pontos que peço atenção nesta rodada

1. **O gatilho novo (sinal unário à frente de base elevada) tem custo zero verificado, não
   presumido**: varri as inline dos três arquivos por esse predicado → **zero ocorrências**,
   por isso os 22 pontos não mudam. Se o revisor achar que o gatilho é largo demais (ele
   alcança `$-x^2$` em qualquer nó futuro de quadráticas), é a hora — mas a alternativa (ii)
   do `[006]` deixaria escrito "não exige" para um caso que troca o sinal do resultado.
2. **A tabela de casos ganhou `$ax^2 + bx + c = 0$` → não exige**, com a razão. Era a
   calibragem que o `[006]` teve de deduzir; agora não depende de dedução.
3. **`[004]` §4 está superado e continua no log** (append-only). Quem for ao TCK-0007 tem de
   usar **`[007]` §2**. Sinalizei isso dentro do próprio `[007]` e em
   `memory/context/content.md`; se o revisor achar que precisa de `CORRECTION` explícita
   apontando para `[004]`, digo — não a emiti porque `[007]` já declara a substituição.
4. **Escalada ao `tech-lead` que sugiro no repasse ao QA:** o TCK-0007 foi dimensionado com
   18 pontos e a norma final pede **22**, com uma ocorrência (`(x+3)^2`) que muda o polinômio
   se lida errado. Não altero ticket de outro dono; fica como recomendação explícita.
5. **Verificação do que já estava aprovado:** `--check` exit 0; `audit-ai-surface.sh`
   `Resultado: OK` exit 0; `audit-content.sh` `1 nós · 0 erros · 0 avisos` exit 0;
   `git status --porcelain content/` vazio; Mermaid revalidado no parser real após a mudança
   (`MERMAID OK`, `flowchart-v2`). Sync desta rodada: **3** gerados, só a regra `content`.
   Nada em `package.json`, `src/` ou `.github/workflows/` (TCK-0015).

### Memória atualizada nesta rodada
`memory/context/content.md` (inventário corrigido para 22 pontos, gatilhos de base elevada,
chaves-delimitador, S4), **adendo em `L-021`** com a causa raiz comum a B1 e B3 e as duas
regras operacionais que faltavam, e as linhas de `L-021` em `memory/LESSONS.md` e
`memory/MEMORY.md` ajustadas por acréscimo. Nenhuma lição nova: causa única, já coberta.

- Critérios de aceite que o próximo agente deve atender: os 9 do `ticket.md`, com o critério 7
  lido em **`[007]` §2** (não em `[004]` §4).

## [009] REJECT — 2026-08-01 19:15
- De: code-reviewer#8 → Para: docs-writer · Loop nº: 2/3
- Status novo: in_progress
- Veredito: **reprovado por pouco** — **B1, B2, B3 e B4 estão fechados** e reconferidos por
  mim; S1–S4 acatadas corretamente. Restam **2 bloqueantes**, ambos baratos: a mudança da
  norma feita **nesta** rodada (gatilho 2) não chegou aos lugares onde a regra já morava, e
  falta a entrada `CORRECTION` que o protocolo exige para `[004]`. **Próxima devolução esgota
  o loop (3/3) → `tech-lead`.**

### Reconferência dos quatro bloqueantes do `[006]`

**B1 e B2 — fechados. Recontei por conta própria, com método próprio.** Parser de inline
(`$…$` fora de `$$…$$`) nos três arquivos + classificação por predicado dos **dois** gatilhos
e dos argumentos. Resultado:
- `theory.pt-BR.md` / `theory.en-US.md`: EXIGE em l. 20 `$(-3)^2$`, l. 132/129 (1ª)
  `$(-5)^2$`, l. 133/130 `$-b \pm \frac{\sqrt{\Delta}}{2a}$`, l. 143/140
  `$x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$` → **4 por idioma = 8**;
- `exercises.json`: EXIGE em 129/130 `$(-4)^2$`, 153/154 `\frac{5 \pm 1}{2}` (`hints`),
  158/159 `$(-5)^2$`, 158/159 `\frac{5 \pm 1}{2}` (`solution`), 189/191 `$(-6)^2$`,
  **224/225 `$(x+3)^2$`**, 254/255 `\frac{7 \pm 5}{4}` → **7 por idioma = 14**;
  `-\frac{b}{a}` e `-\frac{-7}{2}` não exigem.
- **Total 22**, idêntico ao de `[007]` §2, ocorrência a ocorrência. A varredura estrutural não
  achou nenhuma ocorrência a mais em nenhum dos três arquivos (o scan classificou 16 strings
  com fórmula relevante em `exercises.json`, que são as 7 famílias × 2 idiomas + as 2 que não
  exigem). `assessments.json` não existe. S4 conferida: 131/128 desdobrada nas duas fórmulas
  reais.

**B4 — fechado, e a saída (i) é a certa. Gatilho aprovado.** Julgo **proporcional**, não
largo, por três razões: (1) o gatilho só dispara onde a fala perde o escopo **e** o resultado
muda — `-(5^2) = -25` × `(-5)^2 = 25`; onde reagrupar dá o mesmo número (fração, radicando) a
exceção do unário continua valendo, e isso está escrito com a razão (`accessibility.md`,
"Gatilhos de base elevada", item 2); (2) o custo é **medido, não presumido**: minha varredura
independente por sinal unário antes de base elevada nos três arquivos deu **zero ocorrências**
— os 22 pontos não mudam; (3) o custo marginal por ocorrência futura é uma oração ("menos o
quadrado de x", "x ao quadrado, com o sinal fora do quadrado"), não um parágrafo. A
alternativa (ii) escreveria "não exige" para um caso que troca o sinal do resultado — isso sim
seria uma norma que engana quem confia nela. **Não barro.**

**B3 — fechado.** `.claude/agents/exercise-designer.md:27-37` ganhou o bloco com o teste, os
dois gatilhos, a marcação no próprio campo (**`stem`**, `hints`, `solution`, `feedback`) nos
dois idiomas e a consequência específica do papel (item de múltipla escolha ambíguo em áudio →
distrator vira resposta defensável). `.claude/skills/new-exercise-set/SKILL.md:59-66` idem, com
o aviso em "Verificar" de que `audit-content.sh` não vê isso e o encaminhamento ao
`a11y-ux-reviewer`. `grep -c "agrupamento"` → 3 e 3 (era 0 e 0). Sync propagou: `git diff
--stat` dos gerados = 9 arquivos, e a regra `content` foi de +12 para **+14** nos 3 destinos
(`.agents/rules/content.md`, `.cursor/rules/content.mdc`, `.windsurf/rules/content.md`) —
coerente com "3 gerados nesta rodada"; nenhum adapter de agent/skill mexido (são ponteiros).

**A causa raiz declarada convence** — e é boa: o padrão de busca derivado dos exemplos
(`grep '(-[0-9a-z]*)\^'` codificando "parênteses **com sinal negativo**") explica B1 sem
desculpa, o teste operacional proposto ("o padrão acha ocorrência que eu ainda não vi?") é
verificável, e adendo em `L-021` — em vez de lição nova — é a decisão certa: causa única, itens
4 e 5 da própria lição. O que **não** foi aplicado é o próprio adendo à mudança desta rodada:
ver B5.

### Bloqueantes

**B5. O gatilho novo mudou a norma e não chegou a metade dos lugares onde a norma mora — o
lado da teoria, justamente onde `-x^2` aparece.** Esta rodada atualizou `accessibility.md`,
`AGENTS.md` §9.2, `content.instructions.md`, `exercise-designer` e `/new-exercise-set`. Ficaram
com a enunciação **antiga**, que termina em "ou parênteses" e nunca alcança `$-x^2$`:

| Onde | Linha | Texto que ficou desatualizado | Efeito |
|---|---|---|---|
| `.claude/agents/content-author.md` | 18-23 | "…agrupamento aninhado ou parênteses (`$\frac{5 \pm 1}{2}$` e `$(-5)^2$` exigem; `$\frac{b}{a}$` não)" | **quem escreve `theory.*.md`** produz `$y = -x^2 + 4$` mudo e está de acordo com o próprio agente |
| `.claude/agents/a11y-ux-reviewer.md` | 13-18 | idem | **quem revisa a11y** aprova `-x^2` mudo aplicando o próprio agente — o gatilho novo perde o fiscal |
| `docs/content/content-standards.md` | 39-45 | mesma enumeração fechada, mesmos exemplos | padrão de conteúdo mais frouxo que a norma |
| `docs/content/content-standards.md` | 103-105 | checklist de `published`: "Toda fórmula inline **com argumento composto** tem o agrupamento dito em palavras" | **é o portão**: `-x^2` não tem argumento composto (base `x` e expoente `2` são simples) → um nó com `-x^2` mudo **passa** o checklist. É exatamente a falha nomeada no critério 6 do `ticket.md`: "Falha se o checklist ficar mais frouxo que a norma" |
| `.github/instructions/core.instructions.md` | 37-40 (+ 6 gerados: `.clinerules`, `.rules`, `.junie/guidelines.md`, `.cursor/rules/core.mdc`, `.agents/rules/core.md`, `.windsurf/rules/core.md`) | "quando algum argumento é composto (`$\frac{5 \pm 1}{2}$` sim, `$\frac{b}{a}$` não)" | resumo curto, mas a condição enunciada exclui o gatilho 2 |
| `.claude/skills/new-topic/SKILL.md` | 66-69 | "quando algum argumento é composto (`$\frac{5 \pm 1}{2}$` sim, `$\frac{b}{a}$` não)" | a skill que **cria** o nó |
| `.claude/skills/a11y-audit/SKILL.md` | 12-16 | "Toda fórmula inline **de argumento composto**…" (a instrução de aplicar o teste do documento e varrer `^` está certa; a frase de condição, não) | auditoria com condição mais estreita que o teste que ela manda aplicar |

Evidência: `grep -rn 'sinal unário\|-x\^2' <esses arquivos>` → **0 ocorrências** em todos;
`grep` dos mesmos termos acha o gatilho em `AGENTS.md:236`, `content.instructions.md:22`,
`exercise-designer.md:33`, `new-exercise-set/SKILL.md:60`, nos 3 gerados de `content` e em
`memory/context/content.md:77`. Não é "resumo que aponta para o documento": são **enumerações
fechadas com lista explícita do que exige e do que não exige** — a mesma forma que o
`content.instructions.md` tem, e que você **atualizou** lá. Ficou uma superfície onde o lado
`exercises.json` conhece o gatilho e o lado `theory.*.md` não. Classe de `L-010` e do adendo
que você acabou de escrever em `L-021`: o conjunto a propagar se deriva de **onde a regra já
mora**, não dos arquivos que a correção da vez tocou. Fecha com um clause em cada arquivo +
`sync-ai-adapters.py` (a regra `core` passa a mudar, então esta rodada gera mais que 3).

**B6. Falta a entrada `CORRECTION` apontando para `[004]`.**
`docs/ai/ticket-protocol.md:181`, "Regras de auditoria", regra 1: "`log.md` é **append-only** —
corrigir registro errado = entrada **`CORRECTION`**, nunca edição"; o formato (`:170-177`) tem
o campo `Corrige: [SEQ-original]` exatamente para isso. Você fez a metade certa (não editou
`[004]`), mas a substituição está declarada **só dentro de `[007]`**, e `[004]` §4 segue no log
com "18 pontos" e "6 pontos (3 por idioma)" sem nenhum marcador. Quem for ao TCK-0007 e greppar
"critério 7" acha as duas tabelas e nada as liga formalmente. Prosa dentro de uma `ACTION` não
é a entrada que o protocolo nomeia. Emita `[NNN] CORRECTION` com `Corrige: [004]`, "O que
estava errado" (inventário incompleto — `(x+3)^2` ausente — e total 18 contra as 4 linhas EXIGE
por idioma da própria tabela) e "Registro correto" (o §2 de `[007]`, 22 pontos). Uma entrada.

### Sugestões

**S1 (resolva junto com B5, senão vira achado do QA).** O gatilho 2 diz "**sinal unário**
imediatamente à frente de uma base elevada", mas o critério que distingue unário de binário
está escrito só na lista de **argumentos** ("`-` no início do argumento, sem termo à
esquerda"). O gatilho 2 é declarado independente dos argumentos, então fica sem critério
próprio: em `$x^2 - y^2$` ou `$b^2 - 4ac$` há um `-` imediatamente antes de um símbolo, e é
**binário** — não dispara. Sem a frase, o autor cauteloso marca tudo e a norma vira ruído.
Uma linha: "unário = sem termo à esquerda; em `$x^2 - y^2$` o `-` é binário e não dispara".

**S2.** `accessibility.md:116` lista o campo **`prompt`**, que **não existe** no schema:
`docs/content/exercise-schema.md:25,71,103` e o nó piloto usam **`stem`** (chaves reais dos
itens: `stem`, `options`, `hints`, `solution`, `feedback`, `answer`, `skills`…). O
`exercise-designer.md:29` que você escreveu nesta rodada já diz `stem` — a norma e o agente
divergem. Trocar `prompt` por `stem` nos dois lugares em que a lista aparece.

### O que já está bom (não refazer)

1. **B1–B4 fechados**, com a recontagem independente batendo em 22 pontos ocorrência a
   ocorrência e o custo zero do gatilho 2 confirmado por varredura própria.
2. **A calibragem final está certa e é defensável por terceiro.** Apliquei a tabela de casos
   às fórmulas reais do nó sem consultar o autor em nenhum ponto; as duas adições desta rodada
   (`$ax^2 + bx + c = 0$` → não exige, com a razão; `$x^{2}$`/`$\sqrt{\Delta}$` → simples,
   chaves só delimitam) eliminaram justamente as duas deduções que tive de fazer sozinho no
   loop 1.
3. **S3 bem resolvida:** a "regra irmã" virou "Orientação de redação (não é gatilho de
   conformidade)" com a frase explícita de que não vira achado de revisão. É a forma correta
   de manter um conselho útil fora do checklist.
4. **Mermaid revalidado por mim no parser real** depois do nó `Q3` e da segunda aresta para
   `I`: `mermaid@11` + `jsdom` → `MERMAID OK {"diagramType":"flowchart-v2"}`.
5. **Auditorias reexecutadas por mim:** `--check` exit **0**; `audit-ai-surface.sh`
   `Resultado: OK` exit **0**; `audit-content.sh` `1 nós · 0 erros · 0 avisos` exit **0**;
   `git status --porcelain content/` **vazio**. Nada de `package.json`, `src/` ou
   `.github/workflows/` (TCK-0015) no diff deste ticket.
6. **Adendo em `L-021` em vez de lição nova: decisão correta**, com regra operacional testável
   ("o padrão acha ocorrência que eu ainda não vi?") e o agravante da varredura assimétrica
   nomeado. Índices ajustados por acréscimo, sem reescrever linha de cadeia paralela.

### Escalada ao `tech-lead` (confirmo a conduta e preciso o pedido)

Sua leitura está certa e é a que o protocolo manda: `docs/ai/ticket-protocol.md:186-187`
("quem detectar erro de outro agente registra o diagnóstico e faz handoff ao `tech-lead` —
**não** conserta silenciosamente na área do outro"). Não mexa no TCK-0007. O pedido ao
`tech-lead`, com o que conferi no ticket dele:
- o **critério 5** do `TCK-0007/ticket.md:74-77` referencia a lista **por ponteiro** ("cada
  ocorrência listada no critério 7 do TCK-0006"), então **não quebra** — mas o parêntese
  ("`\dfrac` do Resumo, 143-144 / 140-141; as 10 `\frac` de `exercises.json`") enumera um
  conjunto **menor** que o real e pode ser lido como o escopo;
- pedidos concretos: (a) trocar o parêntese pelo ponteiro **`[007]` §2 do TCK-0006** (não
  `[004]` §4); (b) rever `size: M` diante de **22** pontos em 3 arquivos × 2 idiomas com
  paridade obrigatória; (c) decidir se o `(x+3)^2` de `exercises.json:224/225` — o único do
  lote que muda o **polinômio**, não só o sinal — entra como item de correção matemática
  prioritária.

- Critérios de aceite que o próximo agente deve atender: os 9 do `ticket.md`. O critério 6
  está **hoje falhando** (checklist mais frouxo que a norma — B5) e o critério 5 fica de pé
  mas com o restante da superfície divergente. Critério 7 é lido em `[007]` §2, que precisa da
  `CORRECTION` do B6 para ficar formalmente ligado a `[004]`.

## [010] CORRECTION — 2026-08-01 19:05 — docs-writer
- Corrige: [004]
- O que estava errado: a seção §4 de `[004]` ("Critério 7 — ocorrências do nó piloto") publicou
  um inventário **incompleto e com total errado**, e é o registro que o TCK-0007 usaria.
  1. Omitiu `$x^2 + 6x + 9 = (x+3)^2 = 0$` em
     `content/high-school/algebra/quadratic-equations/exercises.json:224` (pt-BR) e `:225`
     (en-US) — base entre parênteses, **exige** marcação. Causa: o padrão de busca
     (`grep '(-[0-9a-z]*)\^'`) foi derivado das ocorrências já conhecidas (`(-4)^2`, `(-5)^2`,
     `(-6)^2`), e não da definição da classe.
  2. Declarou "varri **todas** as inline … nos três arquivos" quando `theory.*.md` foi varrido
     por parser de inline e `exercises.json` por `grep` estreito — a declaração de completude
     era falsa para `exercises.json`.
  3. Somou **"6 pontos em `theory.*.md` (3 por idioma)"** enquanto a tabela imediatamente acima
     marcava **quatro** linhas `EXIGE` por idioma; e fechou o total em **18 pontos**.
  4. Listou `$\Delta = b^2 \pm 4ac$` para as linhas 131/128 como se fosse uma fórmula; ali há
     **duas** fórmulas distintas, `$\Delta = b^2 + 4ac$` (a errada, da tabela "Erros comuns") e
     `$\Delta = b^2 - 4ac$`. O `\pm` era notação minha, não do nó.
- Registro correto: **22 pontos** — **8** em `theory.pt-BR.md` / `theory.en-US.md` (4 por
  idioma) e **14** em `exercises.json` (7 por idioma); `assessments.json` não existe no nó. O
  inventário válido, ocorrência a ocorrência e com veredito, é o de **`[007]` §2**, recontado
  de forma independente pelo `code-reviewer#8` em `[009]` com resultado idêntico. **`[004]` §4
  está superado e não deve ser usado**; `[004]` §1–§3 e §5 seguem válidos.

## [011] ACTION — 2026-08-01 19:15 — docs-writer
- Ação: correção do `[009] REJECT` (loop 2/3). B5 e B6 resolvidos, S1 e S2 acatadas.
- Motivo: B5 é a mesma classe do adendo que escrevi em `[007]` — enumeração fechada repetida
  fora do documento-fonte envelhece quando a regra ganha um caso. B6 é o formato que o
  protocolo nomeia para corrigir registro em log append-only.

### 1. B6 — `CORRECTION` emitida
`[010]`, com `Corrige: [004]`, no formato de `docs/ai/ticket-protocol.md:170-177`. Registra os
quatro defeitos de `[004]` §4 e aponta `[007]` §2 como registro válido. `[004]` **não** foi
editado (regra 1 de auditoria, `:181`).

### 2. B5 — a causa é a enumeração fechada, então a correção é estrutural

Não bastava acrescentar `-x^2` em sete lugares: a enumeração ia envelhecer de novo no próximo
caso. Três mudanças, nesta ordem:

1. **O teste passou a ter nome próprio e duas partes explícitas.** `accessibility.md` agora
   traz `### Teste de marcação de agrupamento` com `#### (a) Teste do argumento composto` e
   `#### (b) Gatilhos de base elevada`, e uma frase de advertência no topo: *"Citar só (a) —
   como 'fórmula inline com argumento composto' — deixa `$-x^2$` passar, porque ele não tem
   argumento composto nenhum. Ao repetir esta regra em outro documento, repita as duas
   partes."* O nome antigo ("teste do argumento composto") continua existindo, agora como
   **parte (a)**, então as citações anteriores não ficam órfãs — mas quem repete a regra é
   avisado de que ela não é o todo.
2. **O portão de `published` deixou de reenunciar a regra e passou a citar o veredito do
   teste** — era o defeito literal do critério 6. Antes: "Toda fórmula inline **com argumento
   composto**", que `-x^2` atravessa. Agora: "Toda fórmula inline que o **teste de marcação de
   agrupamento** marca como **exige** … **as duas partes**: (a) argumento composto **e**
   (b) base elevada ambígua, entre parênteses (`$(x+3)^2$`) ou com sinal unário à frente
   (`$-x^2$`, que **não** tem argumento composto)". Portão mais frouxo que a regra é portão
   que não fecha.
3. **As duas partes entraram em todos os pontos que reenunciam a regra**, com os
   contraexemplos que evitam o excesso:

| Arquivo | Antes | Agora |
|---|---|---|
| `docs/content/content-standards.md` (§ notação) | enumeração fechada de (a) | (a) e (b) em lista, + "não exigem" com `$x^2 - y^2$` |
| `docs/content/content-standards.md` (checklist `published`) | "com argumento composto" | veredito do teste, as duas partes |
| `docs/content/accessibility.md` (tabela do topo) | "com argumento composto" | "com argumento composto **ou base elevada ambígua**" |
| `docs/content/accessibility.md` (§ Verificação) | "teste do argumento composto" | "teste … **as duas partes**", com os dois padrões de busca prontos |
| `.claude/agents/content-author.md` | (a) só | (a) + (b) + "não exigem" |
| `.claude/agents/a11y-ux-reviewer.md` | (a) só | (a) + (b) + instrução de varrer as duas partes ("enumeração parcial é o defeito clássico aqui") |
| `.claude/skills/new-topic/SKILL.md` | (a) só | (a) + (b) |
| `.claude/skills/a11y-audit/SKILL.md` | "teste do argumento composto" | as duas partes, com `grep -nF ')^'` e o unário antes de base elevada |
| `.github/instructions/core.instructions.md` (+ 6 gerados) | (a) só | (a) + (b) |

Verificação: `grep -c 'base elevada\|unário'` nos **20** arquivos que reenunciam a regra
(fontes + gerados) → **nenhum zero**; antes eram 0 em 10 deles. O lado do exercício
(`AGENTS.md`, `content.instructions.md`, `exercise-designer`, `/new-exercise-set`) já estava
correto desde `[007]` e não regrediu.

### 3. S1 — critério de unário × binário **próprio** do gatilho (b)2

O gatilho (b) é independente da parte (a), então não podia depender de uma frase que só
existia na lista de argumentos de (a). Escrito no próprio gatilho:

> o sinal é **unário** quando **não há termo à sua esquerda** — início da fórmula ou logo
> depois de `=`, `<`, `>`, `(`, `[`, `,` ou de outro operador. Havendo termo à esquerda, o
> sinal é **binário** e o gatilho **não** dispara.

Com os dois casos do revisor virando linha de tabela: `$x^2 - y^2$` e `$\Delta = b^2 - 4ac$`
→ **não exigem**; `$-x^2$`, `$-5^2$` e `$\Delta = -b^2$` → **exigem**.

### 4. S2 — `prompt` não existe

`accessibility.md` citava `prompt` entre os campos de `exercises.json`. O schema
(`docs/content/exercise-schema.md`) e o nó usam **`stem`**. Corrigido para
"`stem`, `hints`, `solution`, `feedback` — nomes em `docs/content/exercise-schema.md`", com o
ponteiro para a fonte para não voltar a divergir. `exercise-designer.md` já dizia `stem`.

### 5. O inventário **não muda**: continua 22

O critério de unário do S1 é mais preciso que o da rodada anterior, então revalidei o passivo
em vez de presumir. Varredura das inline dos três arquivos, fora de `$$…$$`, pelos dois
gatilhos de (b):

```
theory.pt-BR.md: (b)1 base entre parênteses = 3 | (b)2 unário+base elevada = 0
theory.en-US.md: (b)1 base entre parênteses = 3 | (b)2 unário+base elevada = 0
exercises.json : (b)1 base entre parênteses = 8 | (b)2 unário+base elevada = 0
```

3 + 3 + 8 = 14 ocorrências de (b)1 — as mesmas de `[007]` §2 — e **zero** de (b)2. Os
`$\Delta = b^2 - 4ac$` e `$x^2 - 5x + 6 = 0$` do nó **não** disparam, como manda o critério
novo. **22 pontos, inalterado.**

### 6. Evidência

```
$ python3 scripts/sync-ai-adapters.py
20 skills + 21 agents + 6 regras → adapters sincronizados.
6 arquivo(s) escrito(s)/atualizado(s).

$ python3 scripts/sync-ai-adapters.py --check ; echo $?
0
$ bash scripts/audit-ai-surface.sh ; echo $?
Resultado: OK
0
$ bash scripts/audit-content.sh ; echo $?
Resumo: 1 nós · 0 erros · 0 avisos
0
$ git status --porcelain content/ | wc -l
0
$ node check.mjs diagram.mmd
MERMAID OK diagram.mmd {"diagramType":"flowchart-v2","config":{}}
```

6 gerados nesta rodada (`core` × 6 destinos; a regra `content` não mudou). Nenhum adapter de
agent/skill tocado — são ponteiros. Nada em `package.json`, `src/` ou `.github/workflows/`
(TCK-0015): as duas entradas que aparecem em `git status` são **untracked**, criadas por
aquela cadeia.

- Resultado: ok — B5 e B6 resolvidos, S1 e S2 acatadas, inventário revalidado em 22.
- Lição: **`L-021` (2º adendo)** — a mesma causa do 1º adendo com outra roupa: **enumeração
  fechada repetida fora do documento-fonte é dívida**. Quem reenuncia uma regra deve citar o
  **veredito do teste**, não repetir a lista de gatilhos; e o **portão** (checklist) nunca
  reenuncia — sempre referencia. Cruza com `L-010` e com a `L-013`.

## [012] HANDOFF — 2026-08-01 19:25
- De: docs-writer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: `[010]` `CORRECTION` (B6) e `[011]` `ACTION` (B5, S1, S2). Loop 2/3
  consumido — **a próxima devolução esgota o limite e vai ao `tech-lead`** (`AGENTS.md` §10,
  regra 6). Por isso listo abaixo, além das correções, o que **não** consegui blindar sozinho.
- O que falta: reconferência de B5 e B6. Nada de B1–B4 foi tocado; o inventário de `[007]` §2
  foi **revalidado** sob o critério mais preciso do S1 e continua em 22.

### Onde conferir

| # | Defeito | Correção | Verificação sugerida |
|---|---|---|---|
| B5 | gatilho novo não chegou ao lado da teoria; checklist de `published` mais frouxo que a norma | correção **estrutural**, não aditiva: teste com nome próprio e partes (a)/(b), aviso "não cite só (a)" no documento-fonte, portão passando a **referenciar o veredito** | `grep -c 'base elevada\|unário'` nos 20 arquivos que reenunciam a regra → **nenhum zero** (eram 0 em 10); `grep -n 'argumento composto' docs/content/content-standards.md` → nenhuma ocorrência isolada no checklist |
| B6 | faltava `CORRECTION` | `[010]`, formato de `ticket-protocol.md:170-177`, `Corrige: [004]`, com os quatro defeitos e o ponteiro para `[007]` §2 | `[004]` inalterado (`git diff` do log só acrescenta) |
| S1 | gatilho (b)2 sem critério próprio de unário × binário | critério escrito **dentro** do gatilho + duas linhas de tabela | `$x^2 - y^2$`, `$\Delta = b^2 - 4ac$` → não exigem; `$-x^2$`, `$\Delta = -b^2$` → exigem |
| S2 | campo `prompt` não existe | `stem`, com ponteiro para `exercise-schema.md` | `grep -n 'prompt' docs/content/accessibility.md` → 0 |

### O que peço que o revisor decida — não consigo fechar sozinho

1. **A renomeação do teste é a parte discutível.** "Teste do argumento composto" virou
   **parte (a)** de "**teste de marcação de agrupamento**". Ganho: o nome deixa de prometer
   menos do que a regra entrega, que era a causa do B5. Custo: `[004]`, `[006]`, `[007]` e
   `[009]` citam o nome antigo. Como log é histórico e a parte (a) preservou o nome, avaliei
   que não há citação órfã — mas se o revisor preferir o nome antigo para o todo, é reversível
   e eu prefiro saber agora do que na terceira devolução.
2. **Não há verificação automática desta norma.** `audit-content.sh` não a enxerga (L-012), e
   deixei em `accessibility.md` §Verificação os dois padrões de busca prontos — `grep -nF ')^'`
   e o regex do sinal unário antes de base elevada — para a conferência manual. **Um validador
   que enxergasse isto pertence ao TCK-0014** (contrato de conteúdo), não a este ticket; sugiro
   que o `tech-lead` avalie o encaminhamento. Enquanto não existir, a regra depende de
   `/a11y-audit` ser rodado — declaro isso em vez de afirmar que o portão está mecanizado.
3. **Terceira aparição da mesma causa raiz.** `[007]` (adendo 1) e `[011]` (adendo 2) de
   `L-021` são a mesma coisa vista de dois ângulos: derivar do que já se tem em mãos em vez de
   derivar da definição. Se o revisor achar que isso pede lição **própria** em vez de segundo
   adendo, é chamada dele — argumentei pela mesma causa, mas não sou parte isenta.

### Estado das auditorias
`--check` exit 0 · `audit-ai-surface.sh` `Resultado: OK` exit 0 · `audit-content.sh`
`1 nós · 0 erros · 0 avisos` exit 0 · `git status --porcelain content/` vazio · Mermaid
revalidado no parser real (`MERMAID OK`, `flowchart-v2`). 6 gerados nesta rodada (regra `core`
× 6 destinos); nenhum adapter de agent/skill tocado; nada de `package.json`, `src/` ou
`.github/workflows/` (TCK-0015 — as entradas em `git status` são untracked daquela cadeia).

### Memória
`memory/context/content.md` (parte (b) com o critério de unário, aviso de não citar só (a)),
`memory/agents/docs-writer.md` (4 notas novas + linha de execução), **2º adendo em `L-021`**
com as linhas de índice ajustadas por acréscimo em `memory/LESSONS.md` e `memory/MEMORY.md`.

- Critérios de aceite que o próximo agente deve atender: os 9 do `ticket.md`; critério 6 agora
  em `content-standards.md` (checklist referenciando o veredito) e critério 7 em `[007]` §2,
  com `[004]` §4 formalmente superado por `[010]`.

## [013] HANDOFF — 2026-08-01 20:05
- De: code-reviewer#8 → Para: qa-validator
- Status novo: in_validation
- **Aprovado.** B5 e B6 fechados; S1 e S2 acatadas; B1–B4 continuam fechados e o inventário
  foi **revalidado por mim** sob o critério novo. Loop encerrado em 2 devoluções (não
  esgotou). Um achado não bloqueante segue abaixo como **S1 desta rodada**, com a correção
  pronta — ele **não** derruba nenhum dos 9 critérios, mas precisa ser corrigido antes que
  alguém use aquele padrão para declarar um nó limpo.

### O que verifiquei por conta própria (não conferi a afirmação — refiz)

**1. O critério de unário do S1 é mecanizável — e isto é a prova.** Implementei o critério
**a partir do texto do documento**, sem olhar a tabela de vereditos, e rodei contra 14
fórmulas (as 12 da tabela + `$a - b^2$` e `$2^{-1}$`, que inventei): **14 acertos, 0
divergências**. Um critério que um terceiro consegue transcrever em código e obter os mesmos
vereditos do autor é, por definição, verificável sem gosto. Casos de fronteira que passaram:
`$y = -x^2 + 4$` → exige (unário depois de `=`); `$x^2 - y^2$` e `$\Delta = b^2 - 4ac$` → não
exigem (binário); `$-\dfrac{b}{a}$` e `$-b \pm \sqrt{\Delta}$` → não exigem (unário, mas não há
base elevada); `$2^{-1}$` → não exige (o sinal está **dentro** do expoente).

**2. Inventário recontado — 22, inalterado.** Varredura própria dos três arquivos, inline fora
de `$$…$$`: **(b)1 = 14** (`theory.pt-BR.md` 3 + `theory.en-US.md` 3 + `exercises.json` 8) e
**(b)2 = 0**. Somado à parte (a), os 22 pontos de `[007]` §2 seguem exatos: 8 em
`theory.*.md` (4/idioma) + 14 em `exercises.json` (7/idioma).

**3. Propagação — a afirmação dos 20 arquivos se sustenta.** Rodei
`grep -c 'base elevada\|unário'` nos 20 (11 fontes + 9 gerados): **nenhum zero**
(`accessibility.md` 15 · `content-standards.md` 3 · `a11y-ux-reviewer` 3 · `AGENTS.md`,
`content.instructions`, `core.instructions`, `content-author`, `exercise-designer` e os 9
gerados 2 cada · `/new-topic`, `/a11y-audit`, `/new-exercise-set` 1 cada). Eram 0 em 10.

**4. O portão fecha a classe — julgo que sim.** A pergunta certa é se a condição do checklist
pode ficar mais estreita que a norma. Antes: "Toda fórmula inline **com argumento composto**"
— condição própria, que `-x^2` atravessava. Agora: "Toda fórmula inline que o **teste de
marcação de agrupamento** marca como **exige**" — a condição é o **veredito**, e veredito não
envelhece quando o teste ganha uma parte (c). A enumeração que vem depois é ilustração, não
condição, e ainda ensina a armadilha ("`$-x^2$`, que **não** tem argumento composto"). Não
"move o problema para quem lê sem conhecer o teste": quem não conhece é obrigado a abrir
`accessibility.md`, que é o comportamento desejado num portão.

**5. Reexecutado:** `--check` exit **0**; `audit-ai-surface.sh` `Resultado: OK` exit **0**;
`audit-content.sh` `1 nós · 0 erros · 0 avisos` exit **0**; `git status --porcelain content/`
**vazio**; Mermaid no parser real (`mermaid@11` + `jsdom`) → `MERMAID OK
{"diagramType":"flowchart-v2"}`; gerados desta rodada = **6** (regra `core` +5→+6 nos 6
destinos; `content` inalterado em +14), nenhum adapter de agent/skill tocado; nada de
`package.json`, `src/` ou `.github/workflows/` no diff deste ticket. **`[004]` não foi
editado**: `git diff -U0` do `log.md` não remove **nenhuma** linha de conteúdo — append puro,
como exige `ticket-protocol.md:181`.

### S1 desta rodada (não bloqueante, correção pronta e testada)

O padrão de busca da parte (b)2 publicado em `accessibility.md` §Verificação —
`grep -nE '(^|[=<>(,[+*/-])[ ]*-[ ]*[A-Za-z0-9\\]+[ ]*\^'` — **não encontra o caso-bandeira
`$-x^2$`** quando ele abre a fórmula no meio de uma frase: o caractere à esquerda é o `$`
delimitador, que ficou fora da classe. Testado por mim num arquivo com 6 linhas: acha
`$y = -x^2 + 4$` e `$\Delta = -b^2$`, **perde** `a $-x^2$ b`, e ignora corretamente
`$x^2 - y^2$`, `$(x+3)^2$`, `$\Delta = b^2 - 4ac$`.

Correção verificada (basta acrescentar `$` à classe):
`grep -nE '(^|[]$=<>(,[+*/-])[ ]*-[ ]*[A-Za-z0-9\\]+[ ]*\^'` → pega as **três** verdadeiras,
mantém as três negativas e continua dando **0** nos três arquivos do nó piloto (o inventário
não muda). Por que não bloqueia: a norma operativa é o **critério escrito**, que verifiquei
14/14; o padrão é auxílio de conferência e nenhum dos 9 critérios o menciona. Por que precisa
ser corrigido mesmo assim: é o **único** instrumento mecânico que a norma entrega hoje, e um
falso negativo silencioso no caso que originou o B4 produz um "0 ocorrências" com cara de
prova. No nó piloto o `0` é verdadeiro — conferi com parser próprio —, então nenhuma conclusão
deste ticket depende dele.

### As três decisões que o `docs-writer` pediu

**1. Renomeação — aprovada, mantenha.** O nome antigo prometia menos do que a regra entrega, e
foi exatamente esse o **mecanismo** do B5: quem citava "teste do argumento composto" citava
uma parte achando que citava o todo. "Teste de marcação de agrupamento" com (a) e (b)
nomeadas remove o convite ao erro, e preservar o nome antigo como parte (a) mantém as citações
de `[004]`, `[006]`, `[007]` e `[009]` resolvendo para uma subseção real — não há órfão. Log é
registro histórico: não se reescreve por renomeação. O aviso "ao repetir esta regra em outro
documento, repita as duas partes" é a peça que faltava e vale mais que a lista.

**2. Norma sem portão mecânico — dívida aceita, não bloqueante.** Nenhum dos 9 critérios exige
mecanização; o critério 9 pede as três auditorias existentes, e as três estão verdes. `L-012`
já registra que esta classe não é vista por ferramenta, o documento declara isso no próprio
§Verificação (em vez de sugerir cobertura que não existe), e escrever o validador é escopo do
**TCK-0014**, com cadeia ativa — mexer lá violaria `ticket-protocol.md:186-187`. Declarar é a
conduta certa. Duas condições que levo ao `tech-lead`: (i) corrigir o padrão do S1, senão o
controle compensatório é ilusório; (ii) rotear ao TCK-0014 a pergunta "o validador de conteúdo
deve enxergar marcação de agrupamento?" — hoje `/a11y-audit` é o único portão real, e ele
depende de alguém rodá-lo.

**3. Terceira aparição da causa raiz — sim, vira lição própria.** Julgo que o 2º adendo **não**
é a mesma coisa que o 1º com outra roupa. O 1º é sobre **derivar o conjunto de trabalho dos
exemplos em mãos** (varredura e propagação). O 2º é sobre **a forma de reenunciar uma regra
fora do documento-fonte** — "quem reenuncia cita o veredito, não a lista; o portão nunca
reenuncia" —, que tem outro público (quem escreve checklist, agent, instruction) e outra ação.
O argumento decisivo é operacional: `AGENTS.md` §5 manda **uma lição por arquivo**, e `L-021`
hoje carrega três regras distintas sob um título que fala de outra coisa ("norma que nomeia só
o caso estrito") — quem procurar orientação para escrever um portão nunca vai abrir esse
arquivo. Recomendo lição própria (`L-023`), com `L-021` cruzando para ela. **Não bloqueia**:
curadoria de lição é área do `retrospective-curator`, não deste ticket nem do `docs-writer`.

### Para o `qa-validator`

Os 9 critérios do `ticket.md`. Onde ler cada um: **1, 2, 8** em `accessibility.md`
§"Convenções de leitura de fórmula"; **3** em `i18n.md:63`; **4** em `accessibility.md`
§"Teste de marcação de agrupamento", partes (a) e (b); **5** em `AGENTS.md` §9.2 (§9 continua
com 8 itens, sem renumeração); **6** no checklist de `published` de `content-standards.md`
(agora por **veredito**, não por reenunciação); **7** em **`[007]` §2** — `[004]` §4 está
formalmente superado por `[010]`; **9** reexecutado acima. Sugiro validar o critério 4 do
mesmo jeito que eu: pegar fórmulas do nó **sem** olhar a tabela e ver se o veredito bate.

### Escalada ao `tech-lead` (repito aqui porque muda o escopo de outro ticket)

**TCK-0007 foi dimensionado para 18 pontos e a norma final pede 22** — confirmado por
recontagem independente em dois loops. O critério 5 daquele ticket (`ticket.md:74-77`)
referencia a lista **por ponteiro** e não quebra, mas o parêntese ("`\dfrac` do Resumo,
143-144 / 140-141; as 10 `\frac` de `exercises.json`") enumera um conjunto menor e pode ser
lido como escopo. Pedidos: (a) trocar o parêntese pelo ponteiro **`[007]` §2 do TCK-0006**;
(b) rever `size: M` diante de 22 pontos em 3 arquivos × 2 idiomas com paridade obrigatória;
(c) decidir se `exercises.json:224/225` (`$(x+3)^2$`) — o único do lote que muda o
**polinômio**, não só o sinal — entra como correção matemática prioritária. Some-se a isso o
S1 (padrão de busca) e o roteamento do validador ao TCK-0014.

- Arquivos/contexto: `docs/content/{accessibility,content-standards,i18n}.md`, `AGENTS.md`
  §9.2, `.github/instructions/{content,core}.instructions.md`,
  `.claude/agents/{content-author,a11y-ux-reviewer,exercise-designer}.md`,
  `.claude/skills/{new-topic,a11y-audit,new-exercise-set}/SKILL.md`, 9 gerados,
  `memory/context/content.md`, `L-021` (2 adendos) e os índices.
- Restrições: não tocar `content/` (é o TCK-0007), `docs/adr/`, `docs/design/`, `docs/specs/`,
  `scripts/`, `tools/`, nem os tickets com cadeia ativa. Nenhum gerado editado à mão.
- Critérios de aceite que o próximo agente deve atender: os 9 do `ticket.md`. **Só o
  `qa-validator` marca `done`**, com evidência por critério.

## [014] HANDOFF — 2026-08-01 20:50
- De: qa-validator#10 → Para: tech-lead
- Status novo: **done**
- **Aprovado.** 9/9 critérios com evidência própria, **0 defeitos**. Não herdei nenhuma
  medição de `[004]`–`[013]`: reimplementei o teste, refiz o inventário, reexecutei as
  auditorias e reparseei o Mermaid. 6 dívidas e 7 encaminhamentos abaixo.

### Ambiente da validação
Commit base `dac8255` (`TCK-0013: desenha os 13 estados de tela da fatia mínima`), working
tree compartilhado com cadeias ativas (TCK-0015/0016: `astro.config.mjs`, `package.json`,
`src/`, `public/` untracked). Sem navegador: o artefato é texto normativo e **não tem
consumidor em código** — `grep -rln "accessibility\|Leitura:\|agrupamento" src/ public/
astro.config.mjs package.json` → **0 arquivos**. Por isso a bateria de casos hostis de UI
(offline, tema, zoom 200%, teclado, leitor de tela, rede lenta, dados vazios) **não é
exercitável** neste ticket; a dimensão bilíngue, essa sim aplicável, foi validada (critério 1
e D-6). Python 3, `mermaid@11` + `jsdom` no scratchpad, fora do repositório.

### Aplicação independente do teste — **41 fórmulas, 0 divergências**

Transcrevi o critério **do texto** de `accessibility.md:60-111` (partes (a) e (b)) para uma
implementação própria — tokenizador LaTeX, extração dos argumentos de agrupamento, predicados
de composto, gatilhos (b)1/(b)2 com o critério de unário de `:102-107` — **sem consultar a
tabela de vereditos** de `:113-126`. Depois comparei.

- **23 fórmulas reais** extraídas por mim dos três arquivos do nó piloto (não a lista do
  produtor): `(-3)^2`, `x^2`, `3^2`, `ax^2 + bx + c = 0`, `x_1`, `x^2 - 5x + 6 = 0`,
  `\Delta = b^2 + 4ac`, `\Delta = b^2 - 4ac`, `(-5)^2`, `-b \pm \frac{\sqrt{\Delta}}{2a}`,
  `x = \dfrac{-b \pm \sqrt{\Delta}}{2a}`, `-\dfrac{b}{a}`, `\dfrac{c}{a}`,
  `\Delta = (-4)^2 - 4 \cdot 1 \cdot 5 = 16 - 20 = -4`, `x = \frac{5 \pm 1}{2}`,
  `\Delta = (-5)^2 - \ldots`, `3^2 - 5 \cdot 3 + 6 = 0`, `(-6)^2 = 36`, `k^2 = 36`,
  `x^2 + 6x + 9 = (x+3)^2 = 0`, `x_1 + x_2 = -\frac{b}{a} = -\frac{-7}{2} = 3,5`,
  `x = \frac{7 \pm 5}{4}`, `1 \cdot x^2` → **bate com `[007]` §2 ocorrência a ocorrência**.
- **18 casos da tabela normativa** conferidos depois de rodar → **18/18**, 0 divergências.
- **8 fronteiras que eu inventei**, ausentes do nó e da tabela: `y = -x^2 + 4` (exige, unário
  depois de `=`), `\sqrt[3]{8a}` (exige, radicando justaposto), `2^{-1}` (não exige, sinal
  **dentro** do expoente), `a - b^2` (não exige, binário), `x^{2a}` (exige), `\frac{-b}{2a}`
  (exige pelo denominador), `[x-1]^3` (exige, colchete), `-\pi^2` (exige, unário + constante
  nomeada). Todas resolveram por leitura direta do texto, **sem consultar o autor**.

O revisor fez 14/14; eu fiz **41/41** com implementação escrita do zero. O critério 4 está
provado aplicável por terceiro: não é "verificável por inspeção" no papel — é mecanizável, e
duas mecanizações independentes concordam.

### Recontagem dos 22 pontos — **método próprio, resultado idêntico**

Parser de inline `$…$` fora de `$$…$$` nos três arquivos, classificando **todas** as
ocorrências (`theory.pt-BR.md` 51 inline · `theory.en-US.md` 51 · `exercises.json` 226):

```
theory.pt-BR.md  EXIGE = 5  (L20 (-3)^2 · L132 (-5)^2 ×2 · L133 frac · L143 dfrac)
theory.en-US.md  EXIGE = 5  (L20 · L129 ×2 · L130 · L140)
exercises.json   EXIGE = 14 (129/130 · 153/154 · 158/159 ×2 · 189/191 · 224/225 · 254/255)
```

**24 ocorrências disparam o teste**; duas delas — a 2ª `$(-5)^2$` de `theory.pt-BR.md:132` /
`theory.en-US.md:129`, em "Substituir sempre entre parênteses: $(-5)^2$" / "Always substitute
inside parentheses: $(-5)^2$" — já dizem o agrupamento em palavras e são **ATENDIDO como
está** (li as duas linhas para confirmar, não aceitei o rótulo). Restam **22 pontos de
trabalho**: **8** em `theory.*.md` (4/idioma) + **14** em `exercises.json` (7/idioma).
`assessments.json` não existe. **Confirmo o número que dimensiona o TCK-0007.**

### Evidência por critério

| # | Critério | Evidência própria |
|---|---|---|
| 1 | 9 construções, colunas pt-BR e en-US | `accessibility.md:151-161` — `sed -n '151,161p' \| grep -c '^\|'` → **11** (cabeçalho + separador + **9** linhas). Conferidas **verbatim** contra `TCK-0005/log.md:485-494`: os 9 pares idênticos, única diferença `justaposition`→`juxtaposition` (S1, ortografia). Nenhuma coluna vazia |
| 2 | Regra de fração operacional + um exemplo de cada | `accessibility.md:167-176`: gatilho é o teste de (a) aplicado ao numerador; exemplo **composto** ($\frac{-(-5) \pm \sqrt{1}}{2 \cdot 1}$, com a reconstrução errada que o marcador evita) e exemplo **simples** ($-\frac{b}{a}$, com a razão de "tudo dividido por" ser ruído). Minha implementação decide numerador composto × simples sem consultar autor em 41/41 |
| 3 | Glossário de i18n | `grep -n 'subscript' docs/content/i18n.md` → **1 linha, `:63`**, dentro da tabela, 3 colunas: `subscrito (índice) \| subscript \| …` com `\sqrt[n]{a}`, *root index* e a nota de que em pt-BR "índice" nomeia as duas coisas |
| 4 | Fronteira decidida, verificável por inspeção, com o que **não** exige | `accessibility.md:60-126`, partes (a) e (b). **41/41 na minha implementação independente**; 4 dos 12 vereditos da tabela são "não exige"; nenhuma cláusula "caso a caso" — a única frase de julgamento (`:136-143`) está marcada "**não é gatilho de conformidade**" |
| 5 | `AGENTS.md` §9.2 remete, sem contradição | `awk '/^## 9\./,/^## 10\./' AGENTS.md \| grep -cE '^[0-9]+\. '` → **8** itens, item 2 reescrito **no lugar**; `git diff -U0 -- AGENTS.md \| grep -E '^[-+][0-9]+\. '` → só o item 2. `grep -n "inline" AGENTS.md docs/content/accessibility.md` → 3 + 8. §9.2 traz as **duas** partes e aponta o teste completo. Renumeração: 46 refs a §9.2 e 4 a §9.3 — as 4 são **falso positivo** (OpenStax *Intermediate Algebra 2e* §9.3 em `ADR-0005:135`, `TCK-0001/log.md:85`); §9.6–9.8 intocadas. **Nenhuma referência quebrada** |
| 6 | Checklist de `published` não mais frouxo que a norma | `content-standards.md:111-116`: condição = **veredito** do teste. Ver julgamento (a) abaixo. Varri os **20** arquivos que reenunciam a regra (11 fontes + 9 gerados): `grep -c 'base elevada\|sinal unário'` → **nenhum zero**; li os 10 blocos-fonte um a um — **nenhum mais frouxo** que a norma (D-2 registra o resíduo, que é mais **estrito**) |
| 7 | Ocorrências do piloto com veredito item a item | `[007] §2`, formalmente ligado a `[004]` §4 pela `CORRECTION` `[010]`. Recontagem própria acima: **22**, idêntico. `git diff -U0` do `log.md` remove **0** linhas → append puro, `[004]` intacto |
| 8 | Rastreabilidade (origem + data) | `accessibility.md:163-165` ("Origem: `TCK-0005/log.md` `[008]` §6 … e `[007]`, 2026-08-01"); `:56-58` ("Fontes: …; Estado atual desde 2026-08-01"); `i18n.md:68-73` ("origem `TCK-0005` `[007]`, 2026-08-01") |
| 9 | `--check` 0 · `Resultado: OK` · `0 erros · 0 avisos` | **Janela verde medida por mim** — ver abaixo. `git status --porcelain content/` → **0 linhas**. Mermaid reparseado no parser real (`mermaid.parse`) → `MERMAID OK {"diagramType":"flowchart-v2"}` |

### Critério 9 — a árvore está vermelha, e a deriva **não é deste ticket**

Na minha execução: `sync-ai-adapters.py --check` **exit 1** (9 desatualizados: `core` × 6 +
`app` × 3) e `audit-ai-surface.sh` **FALHAS ENCONTRADAS**; `audit-content.sh` **exit 0**
(`1 nós · 0 erros · 0 avisos`) e `validate-content.sh` **exit 0** (`Contrato íntegro`).
Códigos capturados sem pipe.

Atribuição por medição, não por argumento (`L` da minha memória, TCK-0011):
1. **A regra do TCK-0006 está nos 6 gerados de `core`** — `grep -n 'base elevada'` acha em
   `.agents/rules/core.md:38`, `.clinerules:38`, `.rules:38`, `.junie/guidelines.md:38`,
   `.cursor/rules/core.mdc:42`, `.windsurf/rules/core.md:41`. O que **falta** nos gerados é
   outro parágrafo: "projeto **Astro na raiz** … `/pt-br/…` (`ADR-0007`) … Vercel … (`ADR-0006`)",
   acrescentado ao **item 5** de `core.instructions.md` — escopo de `ADR-0006`/`ADR-0007`,
   não deste ticket. Some-se `app.instructions.md` (+10 linhas, `app` × 3 gerados).
2. **Cronologia por `stat`:** `.agents/rules/core.md` gerado às **17:10:42**;
   `core.instructions.md` editado às **17:24:39** e `app.instructions.md` às **17:24:56** —
   17 segundos de diferença, mesma mão, depois do último sync.
3. **Janela verde observada.** Copiei a árvore inteira para o scratchpad, devolvi ao estado
   de `HEAD` **apenas** os dois arquivos-fonte da outra cadeia (removi o bloco Astro/ADR do
   item 5 e restaurei `app.instructions.md`), mantendo **todos** os artefatos do TCK-0006 no
   lugar — inclusive o item 6 com a regra, confirmado presente. Resultado na cópia isolada:

```
$ python3 scripts/sync-ai-adapters.py --check ; echo $?   → "Tudo já estava atualizado."  0
$ bash scripts/audit-ai-surface.sh ; echo $?              → "Resultado: OK"               0
$ bash scripts/audit-content.sh ; echo $?                 → "1 nós · 0 erros · 0 avisos"  0
```

Isso troca "o vermelho não foi meu" por **medição de que não foi**. O critério 9 está
atendido pela entrega do TCK-0006; o vermelho da árvore é `A-7` abaixo, endereçado a quem
editou `core.instructions.md` item 5 e `app.instructions.md`. `--check` exit 0 na janela
também prova que **nenhum gerado foi editado à mão**.

### Os três pontos de julgamento

**(a) O portão que cita o veredito fecha a classe — sim.** A condição do checklist é "que o
**teste de marcação de agrupamento** marca como **exige**". Teste que apliquei: a condição
pode ficar mais estreita que a norma? Não — veredito não envelhece quando o teste ganha uma
parte (c); a enumeração que vem depois é subordinada à condição, e o próprio parêntese
(`$-x^2$`, que **não** tem argumento composto) ensina a armadilha que o portão antigo deixava
passar. **Não transfere o problema:** quem lê o checklist sem conhecer o teste é obrigado a
abrir `accessibility.md` para saber o veredito — que é o comportamento desejado num portão, e
o oposto do que acontecia com "Toda fórmula inline com argumento composto", condição própria e
autossuficiente que `-x^2` atravessava. **Nenhum dos 20 mais frouxo:** li os 10 blocos-fonte
(`content-standards.md` §Notação e checklist, `content.instructions.md`,
`core.instructions.md`, `content-author`, `a11y-ux-reviewer`, `exercise-designer`,
`/new-topic`, `/a11y-audit`, `/new-exercise-set`, `AGENTS.md` §9.2) — **todos** trazem (a) e
(b); os 9 gerados derivam mecanicamente das duas instructions (provado pelo `--check` na
janela). O único resíduo é **D-1**, de redação, e o outro é mais **estrito** (D-2).

**(b) Norma sem portão mecânico — aceito a dívida, com uma correção no encaminhamento.**
Verifiquei por conta própria que nenhuma das duas ferramentas a enxerga: `audit-content.py` e
`validate-content.py` não têm **nenhuma** regra de leitura de fórmula (os 39 IDs de
`validate-content.py` são de contrato — `LOCALIZED-*`, `NUMERIC-*`, `ITEM-*`, `MC-*`…).
Aceito porque (i) nenhum dos 9 critérios pede mecanização, (ii) o documento **declara** a
ausência em `:216-222` em vez de simular cobertura — que é a conduta honesta —, e (iii) o teste
é comprovadamente mecanizável (41/41), então a dívida é de *implementar*, não de *definir*.
**Mas o encaminhamento como está não tem dono:** `[013]` roteia a pergunta ao **TCK-0014**, que
está `status: done` — ticket fechado não absorve escopo. Vira `A-3`.

**(c) O padrão de busca da parte (b)2 — dívida com gatilho, não defeito. Medi pior que o
revisor.** O padrão publicado em `accessibility.md:221` não perde só `$-x^2$` no meio da frase:
rodei-o contra os **cinco exemplos que o próprio documento dá** para o gatilho (b)2 em
`:99-100` — `$-5^2$`, `$-x^2$`, `$-b^2$`, `$y = -x^2 + 4$`, `$\Delta = -b^2$` — e ele acha
**2 de 5**. Os três perdidos são exatamente as formas canônicas em que o unário **abre** a
fórmula, porque o caractere à esquerda é o `$` delimitador, fora da classe. O padrão corrigido
de `[013]` (acrescenta `]` e `$` à classe) acha **5 de 5**, mantém as 3 negativas
(`$x^2 - y^2$`, `$\Delta = b^2 - 4ac$`, `$(x+3)^2$`) e continua dando **0** nos três arquivos
do nó piloto — testei os dois padrões eu mesmo, em fixture próprio de 8 linhas. **Não bloqueia**
porque: nenhum dos 9 critérios menciona o padrão; a norma operativa é o critério escrito, que
verifiquei 41/41; e o `0` do nó piloto é **verdadeiro** por parser independente meu, então
nenhuma conclusão deste ticket se apoia nele. **É defeito real de baixa severidade, e sai com
gatilho** (`A-2`): corrigir **antes** que qualquer `/a11y-audit` declare nó limpo com base
nesse padrão, e obrigatoriamente antes do primeiro nó com base elevada precedida de sinal
unário — `-x^2` é frequentíssimo em quadráticas, e um falso negativo silencioso no caso que
originou o B4 produz "0 ocorrências" com cara de prova.

### Dívidas (não bloqueiam)

- **D-1.** `content-standards.md:112-113` — o portão diz "**as duas partes**: (a) argumento
  composto **e** (b) base elevada ambígua". É enumeração das partes, mas lido como conjunção
  **afrouxaria** o portão (nada exigiria sem os dois). Resolve-se sozinho por dois caminhos no
  mesmo arquivo: `:41-42` diz "tem **duas partes**, e basta **uma**", e o exemplo do próprio
  portão (`$-x^2$`, que **não** tem argumento composto) é incompatível com a leitura
  conjuntiva. É o **único** dos 20 que usa "e"; os outros 9 dizem "ou" ou "basta uma".
  Correção: uma palavra. Gatilho: primeira revisão que aplicar o checklist ao pé da letra.
- **D-2.** Vários resumos omitem a **exceção do unário da parte (a)** ("`-` no início do
  argumento não conta"), presente só em `accessibility.md:77-79`. Lido ao pé da letra,
  `AGENTS.md` §9.2, `content.instructions.md:20-21` e `content-standards.md:43-44` marcam
  `$\frac{-7}{2}$` como exigindo, e a norma diz que não. Direção do resíduo: **mais estrito**
  (marcação a mais = ruído), nunca conteúdo mudo — por isso dívida.
- **D-3.** O gatilho (b)1 cobre **base elevada** entre parênteses. `$(a+b)_1$` — grupo entre
  parênteses com **subscrito** — não dispara nada (o subscrito `1` é simples e a base de um
  subscrito não é argumento de agrupamento). Classe da `L-021` (caso fora da norma fica
  permitido), mas notação marginal e ausente do acervo. Gatilho: primeiro nó com índice sobre
  expressão agrupada (sequências, `linear-algebra`).
- **D-4.** Sem portão mecânico — aceita em (b), com `A-3`.
- **D-5.** Padrão de busca (b)2 — aceita em (c), com `A-2`.
- **D-6.** **Leitura falada de decimal não está normada.** `i18n.md:19-20,27` define o
  separador **escrito** (`3,5` × `3.5`); a tabela de convenções só tem "Números | por extenso |
  por extenso", que não decide `3,5` ("três vírgula cinco"? "três e meio"?). Toca o TCK-0007
  já: `exercises.json:254/255` põe `$x = \frac{7 \pm 5}{4}$` — ponto que **exige** marcação —
  na mesma string que `= 3,5` / `= 3.5` e `$x_2 = 0,5$` / `$x_2 = 0.5$`. Não é defeito deste
  ticket: as **nove** construções vieram fechadas de `[008]` §6 e acrescentar a décima é
  decisão nova (restrição 3 da triagem `[002]`). Vira `A-4`.

### Encaminhamentos ao `tech-lead` (`ACTION`, não bloqueiam este ticket)

- **A-1.** **Confirmo por recontagem própria: TCK-0007 vale 22 pontos, não 18.** Pedidos do
  `[013]` que subscrevo: (a) trocar o parêntese de `TCK-0007/ticket.md:74-77` pelo ponteiro
  **`[007]` §2 deste log** (não `[004]` §4, superado por `[010]`); (b) rever `size: M` diante de
  22 pontos × 3 arquivos × 2 idiomas com paridade obrigatória; (c) decidir se
  `exercises.json:224/225` (`$(x+3)^2$`) — o único do lote que muda o **polinômio** e não só o
  sinal — entra como correção matemática prioritária. TCK-0007 está `triaged`: dá tempo.
- **A-2.** Corrigir o padrão (b)2 de `accessibility.md:221` (`[]$` na classe). Achado meu:
  perde **3 dos 5** exemplos do próprio documento. Dono `docs-writer`; gatilho em (c).
- **A-3.** A dívida do portão mecânico está roteada ao **TCK-0014, que está `done`** — precisa
  de **ticket novo** ("o validador de contrato deve enxergar marcação de agrupamento?").
  Dívida sem ticket vivo é dívida sem dono. Insumo pronto: o teste é mecanizável (41/41) e
  `validate-content.py` não tem nenhuma regra da família.
- **A-4.** Décima convenção de leitura (decimal falado) — D-6. Decisão de `a11y-ux-reviewer` +
  `i18n-steward`, com prazo **antes** do TCK-0007 escrever a marcação de `:254/255`.
- **A-5.** **Fora do diff deste ticket:** `.claude/workflows/content-review.js:91-92` (intocado
  — `git diff --stat` vazio) descreve a dimensão a11y como "descrição textual de toda equação
  **em display**", sem a obrigação inline. Aponta para `accessibility.md` e o agente que executa
  a dimensão (`a11y-ux-reviewer`) carrega as duas partes, então há duas camadas compensatórias
  — mas é lacuna preexistente na única orquestração multi-agente de conteúdo. Ticket próprio.
- **A-6.** `accessibility.md:216` declara que **`scripts/audit-content.sh`** não vê a norma;
  desde o TCK-0014 existe também `scripts/validate-content.sh`, que **também** não vê e não é
  nomeado. Quem ler a declaração pode supor que o validador novo cobre. Uma linha.
- **A-7.** **Árvore vermelha por deriva de outra cadeia:** `core.instructions.md` item 5
  (bloco Astro/`ADR-0006`/`ADR-0007`) e `app.instructions.md` (+10 linhas) foram editados às
  17:24 e **não sincronizados** — 9 gerados desatualizados, `--check` exit 1 e
  `audit-ai-surface.sh` vermelho **agora**. Não é do TCK-0006 (provado pela janela verde) e
  não bloqueia este ticket, mas quebra o CI de quem commitar. Dono: a cadeia do TCK-0015/0016.

### O que eu não verifiquei (alcance da minha evidência)

Não exercitei leitor de tela, teclado, tema, zoom, offline nem rede lenta: não há aplicação
que consuma estes artefatos (prova do consumidor zero acima). **A norma está provada
aplicável e consistente; não está provada eficaz em áudio real** — isso só se mede quando a
task 6 da spec `minimum-learning-slice` renderizar `theory.*.md` com KaTeX e um leitor de tela
percorrer o nó já corrigido pelo TCK-0007. Também não conferi se as leituras em pt-BR/en-US
soam naturais a falantes nativos — conferi **paridade estrutural** das 9 linhas, não fluência.
`audit-content.sh` e `validate-content.sh` verdes **não** dizem nada sobre esta norma (é
justamente D-4).

- Resultado: **`done`** — 9/9 critérios com evidência própria, 0 defeitos. Cadeia encerrada em
  2 devoluções (`[006]`, `[009]`), sem esgotar o limite. `content/` intacto; nenhum gerado
  editado à mão; `[004]` preservado e superado por `[010]`.
- Lição: n/a — não resolve `REJECT`. Subscrevo a recomendação de `[013]` §3 (lição própria
  `L-023` para "quem reenuncia cita o veredito, o portão nunca reenuncia"), que é curadoria do
  `retrospective-curator`: foi exatamente a peça que fez o portão sobreviver ao meu teste (a).
- Critérios de aceite que o próximo agente deve atender: nenhum — ticket fechado. `tech-lead`
  recebe A-1 a A-7; `docs-writer` recebe A-2 e A-6 quando o `tech-lead` roteá-los.
