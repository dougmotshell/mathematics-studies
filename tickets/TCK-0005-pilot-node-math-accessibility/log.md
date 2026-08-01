# Log — TCK-0005

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 13:35 — tech-lead
- Ação: ticket criado a partir de achado encaminhado pela cadeia do `TCK-0002`.
- Motivo: `code-reviewer#3` e `qa-validator#2` detectaram, de forma independente, que o nó
  piloto tem 8 fórmulas em display e apenas 3 descrições textuais, nos dois idiomas —
  violação de `AGENTS.md` §9.2. O achado estava fora do escopo do `TCK-0002` (RNF-9 proíbe
  tocar `content/`), então virou ticket próprio em vez de correção silenciosa.
- Evidência reproduzida pelo `tech-lead` em 2026-08-01:
  `grep -c '^\$\$' theory.pt-BR.md theory.en-US.md` → `8` e `8`;
  `grep -c 'Leitura:\|Reading:'` → `3` e `3`.
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 13:35 — tech-lead
- Ação: triagem. Tipo `content`, P1, tamanho P, owner `content-author`.
- Motivo da prioridade P1 apesar do tamanho P: o nó piloto é o **modelo** que os próximos nós
  vão copiar. Defeito de padrão se multiplica; corrigir antes de produzir mais conteúdo é
  mais barato que corrigir depois em N nós.
- Cadeia definida: `content-author` → `math-reviewer` ‖ `i18n-steward` ‖ `a11y-ux-reviewer`
  (revisões independentes em paralelo) → `qa-validator`. `curriculum-architect` dispensado —
  a taxonomia não muda.
- Restrições: só acrescentar texto; LaTeX intocado; nenhuma afirmação matemática nova.
- Resultado: ok — `triaged`.

## [003] HANDOFF — 2026-08-01 13:35
- De: tech-lead → Para: content-author
- Status novo: in_progress
- O que foi feito: achado confirmado por comando próprio e transformado em ticket com
  critérios verificáveis.
- Artefatos: `tickets/TCK-0005-pilot-node-math-accessibility/ticket.md`.
- Como validar: critérios 1–7; `bash scripts/audit-content.sh` ao final.
- Pendências e riscos: descrição de fórmula é ponto clássico de erro matemático silencioso —
  a revisão de rigor não é opcional aqui.
- Critérios de aceite: [ ] 1–7 restantes.

## [004] ACTION — 2026-08-01 13:50 — content-author
- Ação: acrescentadas as 5 descrições textuais faltantes em cada arquivo de teoria do nó
  `content/high-school/algebra/quadratic-equations`, no padrão já existente no próprio
  arquivo (`*Leitura:*` em pt-BR, `*Reading:*` em en-US, parágrafo imediatamente após o
  bloco `$$…$$`). Nenhum caractere dentro dos blocos `$$…$$` foi tocado.
- Motivo: `AGENTS.md` §9.2 e `docs/content/accessibility.md` exigem descrição textual para
  **toda** fórmula em display; o nó tinha 3 de 8 nos dois idiomas.
- Critério de leitura adotado: ler a **estrutura** da fórmula da esquerda para a direita, na
  ordem em que ela é escrita, incluindo agrupamentos (`abre/fecha parênteses`, `tudo dividido
  por`), relações (`igual a`, `maior que`, `menor que`), implicações (`o que implica`, para
  `\Longrightarrow`) e índices (`x índice 1` / `x subscript 1`) — sem nomear a fórmula, sem
  interpretar e sem acrescentar passo, justificativa ou resultado que não esteja no LaTeX.
  Números são escritos por extenso, como nas 3 descrições preexistentes.
- Fórmulas descritas nesta ação (linhas na versão final do arquivo):

  | # | pt-BR | en-US | Fórmula |
  |---|---|---|---|
  | 4 | 68 | 66 | Soma e produto das raízes (relações de Girard / Vieta's formulas): $x_1 + x_2 = -b/a$ e $x_1 x_2 = c/a$ |
  | 5 | 81 | 79 | Exemplo 1 — cálculo do discriminante de $x^2 - 5x + 6 = 0$: $\Delta = (-5)^2 - 4\cdot1\cdot6 = 25 - 24 = 1 > 0$ |
  | 6 | 90 | 88 | Exemplo 1 — aplicação da fórmula geral e obtenção de $x_1 = 3$, $x_2 = 2$ |
  | 7 | 105 | 103 | Exemplo 2 — discriminante de $x^2 - 4x + 5 = 0$: $\Delta = 16 - 20 = -4 < 0$ |
  | 8 | 121 | 118 | Exemplo 3 — condição $\Delta = 0$ para $x^2 + kx + 9 = 0$, levando a $k = 6$ ou $k = -6$ |

  As fórmulas 1–3 (definição, discriminante, fórmula geral) já tinham descrição e não foram
  alteradas.
- Paridade: as mesmas 8 fórmulas descritas nos dois arquivos, com a mesma informação
  matemática. Nenhum número decimal aparece nas descrições novas (todos os valores são
  inteiros), portanto a convenção vírgula × ponto de `docs/content/i18n.md` não é acionada;
  os nomes locais dos resultados vêm do texto preexistente (Girard em pt-BR, Vieta em en-US)
  e não são repetidos nas descrições, que só leem a fórmula.
- Resultado: ok.
  - `grep -c '^\$\$' theory.pt-BR.md theory.en-US.md` → `8` e `8` (inalterado).
  - `grep -c '^\*Leitura:\*' theory.pt-BR.md` → `8`; `grep -c '^\*Reading:\*' theory.en-US.md`
    → `8` (era `3` e `3`).
  - Ordem verificada por `grep -n '^\$\$\|^\*Leitura:\*\|^\*Reading:\*'`: alternância estrita
    fórmula → descrição nos dois arquivos, sem bloco órfão.
  - `git diff --stat -- content/` → `2 files changed, 35 insertions(+)`, zero remoções;
    `git diff -U0 -- content/ | grep -E '^-[^-]' | wc -l` → `0` (nenhuma linha modificada).
  - `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos`.
- Fora de escopo respeitado: `references.json`, `meta.json` e `exercises.json` intocados;
  `status: "draft"` do nó mantido.
- Lição: n/a — não resolve `REJECT`.

## [005] HANDOFF — 2026-08-01 13:52
- De: content-author → Para: math-reviewer
- Status novo: in_review
- O que foi feito: as 5 descrições textuais faltantes de cada `theory.<lang>.md` foram
  acrescentadas, fechando 8/8 fórmulas em display descritas nos dois idiomas. Só texto foi
  adicionado — o LaTeX permanece byte a byte idêntico (diff com zero remoções).
- Artefatos:
  - `content/high-school/algebra/quadratic-equations/theory.pt-BR.md` (+18 linhas)
  - `content/high-school/algebra/quadratic-equations/theory.en-US.md` (+17 linhas)
  - (a diferença de 1 linha é só quebra de parágrafo em 90 colunas, não de conteúdo)
- Como validar:
  1. `grep -c '^\$\$' content/high-school/algebra/quadratic-equations/theory.{pt-BR,en-US}.md`
     → `8` e `8`.
  2. `grep -c '^\*Leitura:\*' …/theory.pt-BR.md` e `grep -c '^\*Reading:\*' …/theory.en-US.md`
     → `8` e `8`.
  3. `git diff -U0 -- content/ | grep -E '^-[^-]'` → vazio.
  4. `bash scripts/audit-content.sh` → 0 erros, 0 avisos.
  5. Leitura adversarial: ouvir cada descrição sem olhar a fórmula e tentar reescrever o
     LaTeX; qualquer divergência de sinal, agrupamento ou ordem é defeito.
- Pendências e riscos:
  - O risco central é o que o `tech-lead` já apontou em `[003]`: descrição de fórmula erra em
    silêncio. Pontos de atenção para o `math-reviewer` — o duplo sinal em
    $\frac{-(-5) \pm \sqrt{1}}{2\cdot1}$ (descrito como "menos, abre parênteses menos cinco
    fecha parênteses"), o escopo do sinal negativo em $-\frac{b}{a}$ (descrito como "menos b
    dividido por a") e o agrupamento do numerador ("tudo dividido por…").
  - **Observação sem correção** (regra: não conserto enunciado alheio): o enunciado do teorema
    na linha 48 (pt-BR) / 47 (en-US) afirma que "as soluções reais … são dadas por
    $x = \frac{-b \pm \sqrt{\Delta}}{2a}$" sem condicionar a $\Delta \ge 0$ — a ressalva vem
    só depois, na tabela de sinais. Não é objeto deste ticket e **não foi alterado**; fica
    registrado para o `math-reviewer` decidir se vira ticket próprio.
  - Convenção `x índice 1` / `x subscript 1` para subscritos é nova no repositório (não havia
    fórmula com índice descrita antes). Se aprovada, cabe virar convenção em
    `docs/content/accessibility.md` — decisão do `a11y-ux-reviewer`, fora deste ticket.
  - Revisões em paralelo: `i18n-steward` (paridade pt-BR/en-US, critério 4) e
    `a11y-ux-reviewer` (qualidade da descrição para leitor de tela, critério 3) revisam o
    mesmo artefato ao mesmo tempo, conforme a cadeia definida em `[002]`.
- Critérios de aceite:
  - [x] 1. 8/8 fórmulas de `theory.pt-BR.md` com `*Leitura:*` logo após o bloco.
  - [x] 2. 8/8 fórmulas de `theory.en-US.md` com `*Reading:*` logo após o bloco.
  - [x] 3. Descrições leem a estrutura da fórmula (critério em `[004]`) — confirmação de
        qualidade pertence ao `a11y-ux-reviewer`, não ao autor.
  - [x] 4. Paridade pt-BR/en-US — confirmação pertence ao `i18n-steward`.
  - [x] 5. Nenhuma afirmação matemática nova — confirmação pertence ao `math-reviewer`.
  - [x] 6. LaTeX intocado — evidência: diff com 35 inserções e 0 remoções.
  - [x] 7. `bash scripts/audit-content.sh` → 0 erros, 0 avisos.

## [007] ACTION — 2026-08-01 14:05 — i18n-steward
- Ação: revisão de **paridade pt-BR/en-US** (critério de aceite 4) das 5 descrições novas por
  arquivo. Escopo estrito: idioma. Rigor matemático (`math-reviewer`) e qualidade para leitor
  de tela (`a11y-ux-reviewer`) correm em paralelo e **não** foram julgados aqui.
- Veredito: **APROVADO** — critério 4 atendido. Nenhum defeito bloqueante.
- Cobertura simétrica (verificada por posição, não por contagem):
  - `grep -c '^\$\$'` → `8` e `8`; `grep -c '^\*Leitura:\*'` → `8`;
    `grep -c '^\*Reading:\*'` → `8`.
  - `grep -n '^\$\$\|^\*Leitura:\*'` / `'^\$\$\|^\*Reading:\*'` → alternância estrita
    fórmula → descrição nos dois arquivos, mesma ordem, mesmas seções, sem bloco órfão em
    nenhum dos idiomas. Nenhuma fórmula descrita em um idioma e não no outro.
  - Estrutura de seções inalterada: `grep -c '^#'` → `11` e `11`.
- Conferência par a par das 5 descrições novas:

  | # | Fórmula (linha pt / en) | Descrição pt-BR | Descrição en-US | Equivalentes? |
  |---|---|---|---|---|
  | 4 | `x_1 + x_2 = -b/a`, `x_1 x_2 = c/a` (66 / 64) | "x índice 1 mais x índice 2 é igual a menos b dividido por a; e x índice 1 vezes x índice 2 é igual a c dividido por a" | "x subscript 1 plus x subscript 2 equals minus b divided by a; and x subscript 1 times x subscript 2 equals c divided by a" | **Sim** — mesmos operandos, mesma ordem, mesmo agrupamento, mesma pontuação estrutural (ponto e vírgula separando as duas igualdades) |
  | 5 | `\Delta = (-5)^2 - 4·1·6 = 25 - 24 = 1 > 0` (79 / 77) | "abre parênteses menos cinco fecha parênteses ao quadrado … vinte e cinco menos vinte e quatro … que é maior que zero" | "open parenthesis minus five close parenthesis squared … twenty-five minus twenty-four … which is greater than zero" | **Sim** — todos os três passos de igualdade e a desigualdade final presentes nos dois |
  | 6 | `x = \frac{-(-5) ± \sqrt{1}}{2·1} = \frac{5±1}{2} \Longrightarrow x_1=3, x_2=2` (87 / 85) | "menos, abre parênteses menos cinco fecha parênteses … tudo dividido por dois vezes um; isso é igual a … tudo dividido por dois; o que implica …" | "minus, open parenthesis minus five close parenthesis … all divided by two times one; that equals … all divided by two; which implies …" | **Sim** — duplo sinal, agrupamento do numerador ("tudo dividido por" / "all divided by") e a implicação aparecem nos dois, na mesma posição |
  | 7 | `\Delta = (-4)^2 - 4·1·5 = 16 - 20 = -4 < 0` (103 / 101) | "… dezesseis menos vinte, igual a menos quatro, que é menor que zero" | "… sixteen minus twenty, equals minus four, which is less than zero" | **Sim** |
  | 8 | `k^2 - 4·1·9 = 0 \Longrightarrow k^2 = 36 \Longrightarrow k = 6 ou k = -6` (118 / 115) | "… o que implica k ao quadrado igual a trinta e seis, o que implica k igual a seis ou k igual a menos seis" | "… which implies k squared equals thirty-six, which implies k equals six or k equals minus six" | **Sim** — as duas implicações encadeadas e a disjunção final batem |

  Nenhuma informação matemática presente em um idioma e ausente no outro, nos dois sentidos.
- Convenções locais (`docs/content/i18n.md`):
  - **Decimais — afirmação do autor conferida por comando, não aceita de palavra:**
    `grep -E '[0-9]+[.,][0-9]+'` sobre os blocos `*Leitura:*`/`*Reading:*` → vazio. Todos os
    valores lidos são inteiros e escritos por extenso (`vinte e cinco` / `twenty-five`,
    `trinta e seis` / `thirty-six`). A regra vírgula × ponto **não é acionada** — confirmado.
    Também não há separador de milhar nem data nas descrições novas.
  - **Numerais por extenso:** grafia correta em cada idioma — pt-BR sem hífen e com "e"
    (`vinte e quatro`, `dezesseis`); en-US com hífen (`twenty-four`, `thirty-six`).
  - **Nomenclatura Girard × Vieta:** `grep -i vieta theory.pt-BR.md` → vazio;
    `grep -i girard theory.en-US.md` → vazio. Não houve mistura. As descrições novas **não**
    nomeiam o resultado (só leem a fórmula), então não reintroduzem o nome em idioma errado —
    escolha correta, porque nomear ali exigiria repetir "relações de Girard" / "Vieta's
    formulas" e criaria um segundo ponto de manutenção do par de nomes.
  - **LaTeX:** os 8 blocos `$$…$$` são byte a byte idênticos entre os dois arquivos, exceto o
    bloco 8, que difere **apenas** em `\text{ou}` (pt-BR) × `\text{or}` (en-US) — prosa dentro
    do LaTeX, que deve mesmo ser localizada. É pré-existente e não foi tocado.
    `git diff -U0 -- content/ | grep -E '^-[^-]'` → vazio (zero remoções).
  - `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos` (reproduzido).
- Registro e naturalidade: cada idioma segue o próprio uso corrente, não o do outro.
  pt-BR usa "abre parênteses / fecha parênteses", "tudo dividido por", "o que implica", "que é
  maior que zero"; en-US usa "open parenthesis / close parenthesis", "all divided by", "which
  implies", "which is greater than zero". Não há calque estrutural: a ordem das orações em
  en-US é a natural do inglês, não decalcada do português. As 5 novas seguem, **dentro de cada
  idioma**, o padrão fixado pelas 3 preexistentes ("tudo dividido por" / "all divided by" já
  apareciam na leitura da fórmula geral, e "tudo dividido por" é também o termo do exemplo
  canônico de `docs/content/accessibility.md`).
- **Convenção de subscrito `x índice 1` / `x subscript 1` — parecer de terminologia:**
  **aprovada como par equivalente.** Verificado que nem `docs/content/i18n.md` (glossário) nem
  `docs/content/accessibility.md` fixavam termo anterior para subscrito, e que não há outra
  ocorrência no repositório fora deste ticket — a convenção é de fato inédita, não conflita
  com nada. `subscript` é a forma consagrada em en-US para leitura falada de $x_1$; `índice` é
  a forma corrente em pt-BR escolar. O autor acertou ao **não** decalcar: "índice" → *index*
  seria errado em en-US, e *subscript* → "subscrito" seria aceitável mas menos idiomático em
  pt-BR.
  Ressalva **não bloqueante**, para registro: em pt-BR "índice" é sobrecarregado — é também o
  índice do radical ("raiz de índice n", $\sqrt[n]{\,}$). No contexto "x índice 1" não há
  ambiguidade, mas quando o acervo descrever radicais de índice n o par vai precisar de
  desambiguação. Recomendo fixar no glossário de `docs/content/i18n.md` a linha
  `subscrito (índice) | subscript` com nota "não confundir com índice do radical (*root
  index*)". **Não editei `docs/` nesta execução** — há trabalho paralelo em `docs/` e a
  instrução do handoff foi não tocar. Fica como pendência atribuível ao `tech-lead` na
  consolidação (candidata a lição de terminologia).
- Observações **não bloqueantes**, fora do meu critério (registradas para quem é dono delas,
  sem exigir refação):
  1. en-US usa "open/close parenthesis"; a convenção MathSpeak de leitores de tela é
     "left/right parenthesis". Não é erro de paridade nem de sentido — é escolha de registro
     de leitura, e é decisão do `a11y-ux-reviewer` (critério 3). Se ele preferir MathSpeak, a
     mudança é só em en-US e **não** quebra a paridade, porque "abre/fecha parênteses"
     continua sendo a forma correta em pt-BR.
  2. "x índice 1" / "x subscript 1" usam o algarismo `1`, enquanto os demais números vão por
     extenso. É **simétrico nos dois idiomas**, então não é defeito de paridade; se virar
     ajuste de estilo, tem de ser aplicado aos dois arquivos ao mesmo tempo.
  3. Pré-existente, não tocado: a leitura 3 termina com vírgula em en-US e ponto em pt-BR
     (linhas 52 / 53), acompanhando a pontuação do próprio LaTeX. Sem impacto.
- Conteúdo monolíngue: nenhum. As duas versões existem e estão em paridade; o nó segue em
  `status: "draft"` por decisão do ticket (revisões de rigor e a11y pendentes), não por falta
  de idioma.
- Status e owner **não alterados** — a consolidação das três revisões paralelas é do
  `tech-lead`.
- Critério de aceite avaliado: [x] 4. Paridade pt-BR/en-US — **atendido**.
- Lição: n/a — não resolve `REJECT`.

## [006] ACTION — 2026-08-01 14:05 — math-reviewer
- Ação: revisão de **rigor matemático** das 5 descrições novas em cada idioma (10 no total)
  do nó `content/high-school/algebra/quadratic-equations`. Escopo restrito a rigor —
  paridade (`i18n-steward`, `[007]`) e qualidade para leitor de tela (`a11y-ux-reviewer`,
  `[008]`) são revisões independentes em paralelo. Status e owner **não** alterados: a
  consolidação das três revisões é do `tech-lead`.
- Veredito de rigor: **APROVADO**. Nenhum defeito bloqueante nem importante nas descrições
  acrescentadas. 3 observações de severidade `menor`, nenhuma exigindo refação.
- Método: leitura adversarial — para cada descrição, o LaTeX foi reconstruído **a partir do
  texto isolado**, sem olhar a fórmula, e só então comparado com o LaTeX real. Divergência de
  sinal, agrupamento, ordem de operações ou escopo contaria como defeito.

### Leitura adversarial — 5 fórmulas × 2 idiomas

| # | Idioma | Linha | LaTeX reconstruído só a partir da descrição | LaTeX real | Bate? |
|---|---|---|---|---|---|
| 4 | pt-BR | 68 | `x_1 + x_2 = -b/a`, `x_1 \cdot x_2 = c/a` | `x_1 + x_2 = -\frac{b}{a}, \qquad x_1 \cdot x_2 = \frac{c}{a}` | sim |
| 4 | en-US | 66 | `x_1 + x_2 = -b/a`, `x_1 \cdot x_2 = c/a` | idem | sim |
| 5 | pt-BR | 81 | `\Delta = (-5)^2 - 4\cdot1\cdot6 = 25 - 24 = 1 > 0` | `\Delta = (-5)^2 - 4 \cdot 1 \cdot 6 = 25 - 24 = 1 > 0` | sim |
| 5 | en-US | 79 | idem | idem | sim |
| 6 | pt-BR | 90 | `x = \frac{-(-5) \pm \sqrt{1}}{2\cdot1} = \frac{5 \pm 1}{2} \Longrightarrow x_1 = 3, x_2 = 2` | `x = \frac{-(-5) \pm \sqrt{1}}{2 \cdot 1} = \frac{5 \pm 1}{2} \;\Longrightarrow\; x_1 = 3, \quad x_2 = 2` | sim |
| 6 | en-US | 88 | idem | idem | sim |
| 7 | pt-BR | 105 | `\Delta = (-4)^2 - 4\cdot1\cdot5 = 16 - 20 = -4 < 0` | `\Delta = (-4)^2 - 4 \cdot 1 \cdot 5 = 16 - 20 = -4 < 0` | sim |
| 7 | en-US | 103 | idem | idem | sim |
| 8 | pt-BR | 121 | `k^2 - 4\cdot1\cdot9 = 0 \Longrightarrow k^2 = 36 \Longrightarrow k = 6 \text{ ou } k = -6` | `k^2 - 4 \cdot 1 \cdot 9 = 0 \;\Longrightarrow\; k^2 = 36 \;\Longrightarrow\; k = 6 \ \text{ou} \ k = -6` | sim |
| 8 | en-US | 118 | idem, com `or` | idem, com `\text{or}` | sim |

10/10 reconstruções idênticas ao original a menos de espaçamento tipográfico (`\qquad`,
`\quad`, `\;`) e da vírgula/ponto final de pontuação do parágrafo — nenhum dos dois carrega
conteúdo matemático.

### Pontos de risco levantados pelo autor em `[005]` — julgados um a um

1. **Duplo sinal em `\frac{-(-5) \pm \sqrt{1}}{2 \cdot 1}`** ("menos, abre parênteses menos
   cinco fecha parênteses"): **correto**. O par explícito `abre/fecha parênteses` delimita o
   operando, de modo que o `menos` inicial só pode incidir sobre `(-5)`; e o `mais ou menos`
   seguinte é binário, o que fecha o operando à direita. Parse alternativo hostil
   (`menos` incidindo sobre todo o numerador, `-((-5) \pm \sqrt1)`) é implausível pela
   parentetização explícita e, mesmo assim, produziria `\frac{5 \mp 1}{2}` — o **mesmo**
   conjunto `{3, 2}`. Sem risco de erro de resultado.
2. **Escopo do negativo em `-\frac{b}{a}`** ("menos b dividido por a"): **não é ambíguo em
   valor**. Os dois parses possíveis, `-(b/a)` e `(-b)/a`, coincidem para todo `a \neq 0`
   (condição já garantida pela definição, linha 34/33). A reconstrução difere do original
   apenas em onde o sinal é impresso (`-\frac{b}{a}` vs `\frac{-b}{a}`), o que é escolha
   tipográfica, não matemática. `menor`, sem ação.
3. **Agrupamento do numerador** ("tudo dividido por…"): **correto e necessário**. É o único
   marcador que impede a leitura errada `-b \pm \frac{\sqrt{\Delta}}{2a}`, que o próprio nó
   lista como erro comum (linha 133/130). O uso está consistente com a descrição preexistente
   da linha 53/52.

### Verificação numérica independente (Python puro; SymPy indisponível — `memory/context/content.md`)

- `(-5)^2 = 25`; `4·1·6 = 24`; `25 − 24 = 1`; `1 > 0` — confere.
- `-(-5) = 5`; `(5+1)/2 = 3`; `(5−1)/2 = 2`; substituição de volta: `3² − 5·3 + 6 = 0` e
  `2² − 5·2 + 6 = 0` — confere (raízes exatas, aritmética em `Fraction`).
- `(-4)^2 = 16`; `4·1·5 = 20`; `16 − 20 = −4`; `−4 < 0` — confere. Vértice de
  `y = x² − 4x + 5` em `(2, 1)`, acima do eixo `x` — confere a afirmação geométrica adjacente.
- `k² − 36 = 0 \iff k = 6` ou `k = −6`; **unicidade do conjunto-solução em `\mathbb{R}`
  verificada** (não há terceiro valor); para ambos, `\Delta(1,k,9) = 0`, com raiz dupla
  `x = −3` e `x = 3` respectivamente — confere, e confirma o comentário do texto sobre "dois
  valores de `k`, uma raiz em `x`".
- Girard/Vieta no Exemplo 1: `3 + 2 = 5 = -b/a` e `3 · 2 = 6 = c/a` — confere.

### Critérios sob minha responsabilidade

- **Critério 5 (nenhuma afirmação matemática nova)** — **atendido**. Nenhuma das 10
  descrições introduz passo, justificativa, valor ou hipótese ausente do LaTeX. Os únicos
  acréscimos lexicais são conectivos de pontuação (`;`, "e"/"and" no lugar de `\qquad` e de
  `,\quad`) e a leitura da cadeia mista `… = 1 > 0` como "igual a um, que é maior que zero" —
  ambos fiéis; nenhum estende nem contradiz a fórmula.
- **Critério 3, parte de rigor (reconstrutibilidade)** — **atendido**: 10/10 reconstruções
  batem. A parte de *qualidade de escuta* continua sendo do `a11y-ux-reviewer`.
- **Critério 6 (LaTeX intocado)** — **atendido**, verificado por comando próprio:
  `git diff -U0 -- content/ | grep -E '^-[^-]' | wc -l` → `0`;
  `git diff --stat -- content/` → `2 files changed, 35 insertions(+)`, zero remoções.
  Também reconferido `grep -n '^\$\$\|^\*Leitura:\*\|^\*Reading:\*'`: alternância estrita
  fórmula → descrição nos dois arquivos (8/8 e 8/8), sem bloco órfão (L-012).
- `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos` (reproduzido).

### Veredito sobre o enunciado do teorema (achado herdado de `[005]`)

Enunciado em questão — `theory.pt-BR.md:48-51` / `theory.en-US.md:47-50`: "Se `a \neq 0`, as
soluções reais de `ax² + bx + c = 0` são dadas por `x = \frac{-b \pm \sqrt{\Delta}}{2a}`",
sem condicionar a `\Delta \ge 0`.

**Veredito: (b) imprecisão didática tolerável no contexto imediato — não é erro matemático
de fato.** Argumento:

1. O enunciado é **uma única sentença contínua**: "…são dadas por [fórmula] … **e o número de
   raízes reais é determinado pelo sinal de `\Delta`**:", seguida imediatamente da tabela que
   afirma `\Delta < 0` → nenhuma raiz real. A hipótese não está "em outro lugar do texto":
   está na segunda oração do próprio teorema. Lido como unidade, o teorema **não** afirma que
   existe raiz real quando `\Delta < 0`.
2. O quantificador do enunciado é sobre as soluções **reais**, não sobre todas as soluções —
   logo ele também não afirma, erradamente, que a fórmula entrega números reais em `\mathbb{C}`.
3. Pela convenção corrente (`\sqrt{t}` indefinida em `\mathbb{R}` para `t < 0`), com
   `\Delta < 0` o lado direito **não denota nada**: a sentença fica mal-formada para essa
   faixa de parâmetros, não *falsa*. Não existe atribuição de `a, b, c` que faça o teorema
   produzir uma afirmação real falsa. É por isso que **(a) está descartado**: não há
   contra-exemplo.
4. **(c) também está descartado**: "correto como está" seria complacência. Deixar a hipótese
   de existência implícita é exatamente o padrão de enunciado que o pilar de *correção
   matemática* do `AGENTS.md` §1 existe para evitar, e este nó é o **modelo** que os próximos
   copiarão — o custo de propagação é assimétrico em relação ao custo da correção.

**Severidade: `menor` (na fronteira com `importante` por ser nó-modelo). Não bloqueia o
TCK-0005**, por duas razões independentes: (i) o trecho está **fora do diff** — não foi
tocado, e o critério 5 restringe-se ao texto acrescentado; (ii) o ticket é de acréscimo de
descrições, e reescrever enunciado alheio aqui violaria o "Fora de escopo" declarado.

**Encaminhamento ao `tech-lead`: abrir ticket próprio** (tipo `content`, P2, tamanho P) com o
seguinte escopo mínimo, a ser decidido lá e não aqui:
- `theory.pt-BR.md:48` / `theory.en-US.md:47` — enunciar a hipótese na própria oração, na
  linha de "Se `a \neq 0` e `\Delta \ge 0`, as soluções reais … ; se `\Delta < 0`, não há
  solução real (e há duas em `\mathbb{C}`)". A tabela de sinais permanece como está.
- **Verificar a mesma imprecisão no resto do nó** (§6 do `AGENTS.md`): ocorre também no
  Resumo, `theory.pt-BR.md:143` / `theory.en-US.md:140` ("As raízes reais são
  `x = \dfrac{-b \pm \sqrt{\Delta}}{2a}`"), e, em grau menor, em
  `theory.pt-BR.md:144` / `theory.en-US.md:141` ("Soma e produto das raízes: `-b/a` e `c/a`"),
  que omite a condição de existência que o corpo do texto enuncia corretamente na linha
  64/62 ("Quando existem duas raízes …"). O `\pm` com `\Delta = 0` **não** é problema: os dois
  sinais coincidem e devolvem a raiz dupla.
- **Nós irmãos:** varredura feita — `find content -name meta.json` → **1 nó**. Não há nó irmão
  nem dependente afetado hoje; o risco é de *propagação futura*, o que é justamente o motivo
  de registrar a lição agora e não depois.
- A correção **deve entrar antes de o nó sair de `status: "draft"`** — não antes do `done` do
  TCK-0005.

Registrado como lição **L-013** (`memory/lessons/theorem-hypotheses-belong-in-the-statement.md`),
tipo `correção`, para que a formulação condicionada seja o padrão do próximo nó em vez de
dívida recorrente.

- Nada foi corrigido por mim: nenhum arquivo de `content/` foi editado nesta ação
  (`git diff --stat -- content/` inalterado em `2 files changed, 35 insertions(+)`).
- Resultado: ok — rigor **aprovado**, sem `REJECT`. Status `in_review` e owner mantidos para
  a consolidação do `tech-lead` após `[007]` e `[008]`.
- Lição: n/a — não resolve `REJECT`. (Lição nova registrada: L-013.)

## [009] CORRECTION — 2026-08-01 14:12 — math-reviewer
- Corrige: `[006]`, apenas o **identificador da lição** citado no fim da entrada.
- O que estava errado: `[006]` cita "lição **L-013**
  (`memory/lessons/theorem-hypotheses-belong-in-the-statement.md`)". O `L-013` já estava
  ocupado por `fixing-the-cited-line-is-not-fixing-the-defect-class.md` (TCK-0003) —
  o índice foi lido antes desse registro existir e o número foi reservado por leitura obsoleta.
- Leia-se: **L-014** — `memory/lessons/theorem-hypotheses-belong-in-the-statement.md`,
  indexada em `memory/LESSONS.md` (seção *Correção*) e em `memory/MEMORY.md`.
- Nada mais de `[006]` muda: o veredito de rigor (**APROVADO**), a tabela da leitura
  adversarial, a verificação numérica e o veredito sobre o enunciado do teorema
  (**(b) imprecisão didática, `menor`, não bloqueante para o TCK-0005**) permanecem válidos.
- Sequência `[009]` porque `[007]` e `[008]` estão reservadas às revisões paralelas de
  `i18n-steward` e `a11y-ux-reviewer`; entrada anterior não foi editada (log append-only).
- Causa raiz e como evitar: identificador `L-NNN` foi escolhido no início da tarefa e usado no
  fim, com escrita concorrente no intervalo. O número tem de ser alocado **imediatamente antes
  de escrever**, relendo `memory/LESSONS.md`, e conferido com
  `grep -o 'L-0[0-9][0-9]' memory/LESSONS.md | sort -u | tail -1`.

## [008] ACTION — 2026-08-01 14:05 — a11y-ux-reviewer
- Ação: revisão de **acessibilidade** das 10 descrições novas (5 × 2 idiomas) de
  `theory.pt-BR.md` e `theory.en-US.md`, contra o **critério de aceite 3** e contra
  `docs/content/accessibility.md`. Escopo restrito: rigor matemático é do `math-reviewer`
  (`[006]`) e paridade é do `i18n-steward` (`[007]`) — não opino sobre eles.
- Veredito: **APROVADO** no critério 3. Nenhum defeito de acessibilidade encontrado nas 5
  descrições novas de cada arquivo. Recomendações abaixo são para ticket próprio, não
  devoluções.
- Motivo: as descrições lêem a **estrutura** da fórmula na ordem escrita, com marcação
  explícita de agrupamento; ouvindo apenas a descrição é possível reescrever o LaTeX.

### 1. Correspondência um-para-um (aplicada L-012)
Verificação por **ordem**, não por contagem:
`grep -n '^\$\$\|^\*Leitura:\*' theory.pt-BR.md` → 34/36, 44/46, 51/53, 66/68, 79/81,
87/90, 103/105, 118/121; `grep -n '^\$\$\|^\*Reading:\*' theory.en-US.md` → 33/35, 43/45,
50/52, 64/66, 77/79, 85/88, 101/103, 115/118. Alternância estrita fórmula → descrição nos
dois arquivos, sem bloco mudo e sem descrição órfã. Toda descrição está imediatamente após
o bloco, separada só por linha em branco.

### 2. Reconstrutibilidade — teste adversarial descrição a descrição
Método: ler **apenas** a descrição, escrever o LaTeX que ela induz, comparar com o bloco.

| # | Idioma | LaTeX reconstruído de ouvido | Veredito |
|---|---|---|---|
| 4 | pt-BR / en-US | `x_1 + x_2 = -b/a`, `x_1 \cdot x_2 = c/a` | fiel |
| 5 | pt-BR / en-US | `\Delta = (-5)^2 - 4 \cdot 1 \cdot 6 = 25 - 24 = 1 > 0` | fiel |
| 6 | pt-BR / en-US | `x = \frac{-(-5) \pm \sqrt{1}}{2 \cdot 1} = \frac{5 \pm 1}{2} \Longrightarrow x_1 = 3, x_2 = 2` | fiel |
| 7 | pt-BR / en-US | `\Delta = (-4)^2 - 4 \cdot 1 \cdot 5 = 16 - 20 = -4 < 0` | fiel |
| 8 | pt-BR / en-US | `k^2 - 4 \cdot 1 \cdot 9 = 0 \Longrightarrow k^2 = 36 \Longrightarrow k = 6` ou `k = -6` | fiel |

Pontos de ambiguidade que **procurei ativamente** e como a entrega os resolve:

1. **Escopo de sinal em `(-5)^2`** (o erro clássico: `-5^2 = -25` vs `(-5)^2 = 25`). Resolvido
   com "abre parênteses menos cinco fecha parênteses ao quadrado" / "open parenthesis minus
   five close parenthesis squared" — o parêntese é falado, não subentendido. Correto, e é
   justamente o erro que a própria tabela "Erros comuns" do nó ensina a evitar.
2. **Agrupamento do numerador** em `\frac{-(-5) \pm \sqrt{1}}{2 \cdot 1}`. Resolvido com
   "tudo dividido por" / "all divided by", que fecha o numerador retroativamente. Sem esse
   marcador, o ouvinte reconstruiria `-(-5) \pm \frac{\sqrt{1}}{2 \cdot 1}` — exatamente o
   erro comum da linha 133 (pt-BR) / 130 (en-US). Marcador presente nas duas frações
   compostas da descrição 6. Correto.
3. **`-\frac{b}{a}` lido como "menos b dividido por a"** (descrição 4) — o caso que eu vinha
   caçar. Aqui as duas leituras possíveis, `-(b/a)` e `(-b)/a`, são **a mesma expressão**:
   nenhuma reconstrução errada é possível e o valor é idêntico. Além disso o numerador é um
   único token (`b`), então "tudo dividido por" seria ruído. **Não é defeito.** A regra
   prática que o autor aplicou — numerador de um token → "dividido por"; numerador composto
   → "tudo dividido por" — é a regra certa e deve virar convenção escrita (ver §6).
4. **Escopo do radical**: `\sqrt{1}` tem radicando de um token; "a raiz quadrada de um,
   tudo dividido por…" não tem como ser mal agrupado. Nenhuma fórmula nova tem radicando
   composto, então o caso difícil não aparece nesta entrega.
5. **Cadeia de relações** `= 25 - 24 = 1 > 0`: lida como "igual a vinte e cinco menos vinte
   e quatro, igual a um, que é maior que zero". O "que é" / "which is" separa a igualdade
   encadeada da desigualdade final; sem ele, "igual a um maior que zero" seria lido como um
   único predicado. Correto.
6. **`\;\Longrightarrow\;` como "o que implica" / "which implies"**: direção da implicação
   preservada, sem virar equivalência. Correto.

### 3. Carga cognitiva auditiva
- Descrições 5, 7 e 8: 20–30 palavras, uma cadeia cada. Dentro da memória de trabalho
  auditiva típica. Ok.
- Descrição 6 é a mais longa (≈ 55 palavras em pt-BR). Aceitável **porque** a fórmula é
  genuinamente uma cadeia de três partes e a descrição dá âncoras: ponto e vírgula separa os
  três elos, "tudo dividido por" fecha cada fração, "o que implica" marca a conclusão. O
  ouvinte não precisa segurar a estrutura inteira — cada elo fecha antes do próximo abrir.
- Limitação do padrão (não desta entrega): "tudo dividido por" é âncora **retroativa** —
  o ouvinte só descobre que estava num numerador quando ele acaba. Para fórmulas maiores que
  as deste nó, um marcador prospectivo ("a fração de numerador … e denominador …") seria
  melhor. O autor seguiu o exemplo documentado em `docs/content/accessibility.md`; seguir o
  padrão documentado é o comportamento certo. Evoluir o padrão é §6.

### 4. Consistência do vocabulário (as 8 descrições de cada arquivo)
- Igualdade: "é igual a" na primeira relação, "igual a" nas encadeadas — uniforme nas 5
  novas e compatível com as 3 preexistentes.
- Multiplicação: `\cdot` → "vezes"/"times"; justaposição (`4ac`) → justaposição ("quatro a
  c"). Regra coerente: `4 \cdot 1 \cdot 6` **precisa** de "vezes" (números justapostos seriam
  ilegíveis) e `4ac` não. Não é oscilação de vocabulário, é a distinção certa.
- Números por extenso em 100% das descrições novas, como nas preexistentes.
- Parênteses sempre falados como "abre/fecha". Uniforme.
- Nenhum caso de mesma construção com dois vocabulários diferentes. **Consistência ok.**

### 5. Posição e marcação
- Rótulo `*Leitura:*` / `*Reading:*` é **texto**, não só formatação: a semântica está na
  palavra, não no itálico — sem violação de WCAG 1.3.1 (informação por apresentação).
- A descrição não depende de cor (WCAG 1.4.1): ok.
- Para quem **não** usa leitor de tela, a descrição 5 fica encravada no meio de uma frase que
  continua ("…$= 1 > 0,$" → *Leitura:* → "logo há duas raízes reais distintas:"). É atrito de
  leitura visual real, **mas** o padrão do projeto exige adjacência ao bloco (critério 1) e
  qualquer outra posição orfanaria a descrição. O autor escolheu certo; a solução boa é de
  renderização, não de conteúdo — §6, item 3.

### 6. Veredito sobre a convenção de subscrito (decisão pedida em `[005]`)
**Adotar `x índice 1` (pt-BR) / `x subscript 1` (en-US). Aprovada.** Fundamentos:

1. **Ler o subscrito explicitamente é obrigatório**, e é o ponto principal. A alternativa
   natural na fala ("xis um") é irrecuperável: o ouvinte não distingue $x_1$ de $x^1$, de
   $x \cdot 1$ ou de "x, um". A entrega acertou ao verbalizar o nível tipográfico.
2. **en-US "subscript"**: é o termo que os leitores de tela usam nesse contexto e é
   inequívoco. Mantém.
3. **pt-BR "índice"**: é o registro natural do português matemático para variável indexada
   ("x índice i"); "subscrito" é o termo tipográfico/de software. Ambos reconstroem $x_1$ sem
   ambiguidade aqui. Escolho manter "índice" pelo registro, **com uma ressalva de colisão que
   precisa ser registrada junto**: "índice" também é o nome do índice do radical
   ($\sqrt[n]{a}$). A convenção só é segura se o radical de índice n for **sempre** lido como
   "raiz de índice n de …" (nunca "índice n" solto). Sem essa ressalva escrita, a convenção
   se torna ambígua no primeiro nó de radicais.
4. **Registrar em `docs/content/accessibility.md` NÃO é pré-requisito para aprovar este
   ticket.** Motivos: `docs/` está fora do escopo declarado do TCK-0005; outro agente pode
   estar em `docs/`; e travar uma entrega de conteúdo correta numa tarefa de documentação
   contraria o princípio de que o loop só para em `done`, `blocked` ou escalada. **Mas o
   registro é obrigatório antes do próximo nó de conteúdo** — o nó piloto é o modelo (razão
   do P1 em `[002]`), e convenção não escrita se multiplica divergente. Recomendo ticket
   próprio, dono `a11y-ux-reviewer` + `docs-writer`, para acrescentar a
   `docs/content/accessibility.md` a **tabela de convenções de leitura** já decidida na
   prática por esta entrega:

   | Construção | pt-BR | en-US |
   |---|---|---|
   | Subscrito `x_1` | "x índice 1" | "x subscript 1" |
   | Índice de radical `\sqrt[n]{a}` | "raiz de índice n de a" | "n-th root of a" |
   | Fração de numerador composto | "… tudo dividido por …" | "… all divided by …" |
   | Fração de numerador de um token | "b dividido por a" | "b divided by a" |
   | Parênteses | "abre/fecha parênteses" | "open/close parenthesis" |
   | `\cdot` × justaposição | "vezes" × justaposição | "times" × justaposition |
   | `\Longrightarrow` | "o que implica" | "which implies" |
   | Relação encadeada `= 1 > 0` | "igual a um, que é maior que zero" | "equals one, which is greater than zero" |
   | Números | por extenso | por extenso |

### 7. Achados fora do escopo desta entrega (ticket próprio, NÃO são defeitos do `[004]`)
Registrados aqui porque foram encontrados nesta revisão; nenhum toca linha alterada por este
ticket. Nenhum bloqueia o TCK-0005.

1. **Descrição preexistente incompleta** (importante). `theory.pt-BR.md:51` /
   `theory.en-US.md:50`: o bloco tem **duas** partes —
   `x = \frac{-b \pm \sqrt{\Delta}}{2a}, \qquad \Delta = b^2 - 4ac` — e a leitura das linhas
   53 / 52 descreve só a primeira; o lembrete `\Delta = b^2 - 4ac` fica **mudo**. Impacto:
   usuário de leitor de tela perde a metade do bloco no teorema central do nó. É uma das 3
   descrições preexistentes, não tocada pelo `[004]`.
2. **Fórmulas inline cujo sentido É o agrupamento** (importante). Linha 133 (pt-BR) / 130
   (en-US), tabela "Erros comuns": a célula contrasta $\frac{-b \pm \sqrt{\Delta}}{2a}$ com
   $-b \pm \frac{\sqrt{\Delta}}{2a}$. Lido linearmente, o contraste pode desaparecer e a
   linha vira "leia a fração como a fração". Impacto: a lição de erro comum fica inacessível
   exatamente para quem mais depende de leitura linear. Correção sugerida: enunciar a
   distinção **em palavras** na própria célula. Regra geral a registrar: quando o ponto
   matemático é o agrupamento, o texto ao redor precisa dizê-lo.
3. **`\dfrac` inline no Resumo** (menor). Linhas 143–144 (pt-BR) / 140–141 (en-US): frações
   em modo display dentro de bullets, sem leitura. `AGENTS.md` §9.2 fala em fórmula em
   display (`$$…$$`), então formalmente não são exigidas — mas carregam o mesmo risco de
   agrupamento. Avaliar se a regra deve cobrir `\dfrac` inline.
4. **Renderização da descrição** (importante, plataforma). Com KaTeX emitindo MathML, o
   usuário de leitor de tela ouvirá **a fórmula e depois a descrição** — conteúdo duplicado a
   cada bloco, e para o usuário visual três linhas de prosa redundante. O conteúdo em
   markdown não pode resolver isso; a plataforma pode (associar via `aria-describedby`,
   ou usar divulgação progressiva, ou suprimir uma das duas leituras). Depende da stack
   (ADR-0003 `proposed`). Vale ADR ou spec própria antes do primeiro render.
5. **`exercises.json`** (menor). 10 ocorrências de `\frac` em enunciados/alternativas, sem
   nenhum tratamento de leitura (`grep -c '\$\$' exercises.json` → 0, então §9.2 não é
   violada). Se o gabarito de algum item depender de agrupamento, o item é ambíguo em áudio.
   Auditar em ticket próprio.

### 8. O que NÃO foi verificado (declaração obrigatória)
Sem MCP `chrome-devtools` e sem leitor de tela neste ambiente, **não** foram verificados:
MathML realmente emitido pelo KaTeX, a locução real por NVDA/JAWS/VoiceOver em pt-BR e
en-US, ordem de foco, contraste, zoom 200% e alvos de toque. Esta revisão é de **conteúdo**
(parte 1 do `/a11y-audit`). A verificação de interface (parte 2) continua pendente e é
pré-requisito da primeira publicação renderizada, não deste ticket. Aprovação em auditoria
automática não é prova de acessibilidade; `scripts/audit-content.sh` não checa descrição de
fórmula (L-012).

- Resultado: ok — critério 3 **atendido**. Status e owner **inalterados**: a consolidação das
  três revisões paralelas (`[006]` `math-reviewer`, `[007]` `i18n-steward`, `[008]`
  `a11y-ux-reviewer`) é do `tech-lead`.
- Lição: n/a — não resolve `REJECT`. Convenções de §6 e achados de §7 encaminhados para
  ticket próprio.

## [010] HANDOFF — 2026-08-01 14:20
- De: tech-lead → Para: qa-validator
- Status novo: in_validation
- O que foi feito: as três revisões independentes definidas na triagem `[002]` concluíram e
  **todas aprovaram**, sem nenhum `REJECT`:
  - `[006]` `math-reviewer` — leitura adversarial 10/10, aritmética conferida em Python exato
    (`Fraction`), critérios 5 e 3-rigor atendidos.
  - `[007]` `i18n-steward` — paridade conferida par a par, cobertura verificada por posição
    (não por contagem), convenção de subscrito aprovada como par equivalente.
  - `[008]` `a11y-ux-reviewer` — reconstrutibilidade 10/10, vocabulário consistente,
    convenção `x índice 1` / `x subscript 1` aprovada.
  Nota de ordem: as entradas `[006]`–`[008]` foram escritas em paralelo, por isso aparecem
  fora de ordem no arquivo; as sequências foram atribuídas na convocação, sem colisão.
- Artefatos: `content/high-school/algebra/quadratic-equations/theory.pt-BR.md` e
  `theory.en-US.md` (35 inserções, 0 remoções).
- Como validar: critérios 1–7 do ticket; ver "Como validar" em `[005]`.
- Pendências e riscos (encaminhadas pelo `tech-lead` a tickets próprios, **nenhuma bloqueia
  este ticket** — todas fora do diff desta entrega):
  1. `math-reviewer` `[006]`: o enunciado do teorema (`theory.pt-BR.md:48` / `en-US.md:47`)
     dá a fórmula geral "para as soluções reais" sem condicionar a $\Delta \ge 0$ —
     imprecisão didática de severidade menor, com a mesma imprecisão no Resumo (143/140) e
     na linha de soma e produto (144/141). **Condição: corrigir antes de o nó sair de
     `status: "draft"`.**
  2. `a11y-ux-reviewer` `[008]`: descrição **preexistente** de `theory.pt-BR.md:51` /
     `en-US.md:50` cobre só a primeira metade do bloco — o $\Delta = b^2-4ac$ fica mudo.
  3. `a11y-ux-reviewer` `[008]`: tabela "Erros comuns" (133/130) contrasta duas frações cujo
     único diferencial é o agrupamento — lido linearmente, o contraste desaparece.
  4. `a11y-ux-reviewer` `[008]`: `\dfrac` inline no Resumo sem leitura; `exercises.json` com
     10 `\frac` inline sem tratamento — avaliar se `AGENTS.md` §9.2 deve cobrir inline.
  5. `a11y-ux-reviewer` `[008]` + `i18n-steward` `[007]`: registrar em
     `docs/content/accessibility.md` a tabela de convenções de leitura de fórmula (a11y
     entregou pronta em `[008]` §6) e, no glossário de `docs/content/i18n.md`, a linha
     `subscrito (índice) | subscript` com nota de desambiguação (em pt-BR, "índice" também
     nomeia o índice do radical). **Obrigatório antes do próximo nó** — o piloto é o modelo.
  6. `a11y-ux-reviewer` `[008]`: quando houver renderização, KaTeX emitindo MathML fará o
     usuário ouvir fórmula **e** descrição, duplicado — resolver na camada de apresentação.
  7. Parte 2 do `/a11y-audit` (leitor de tela real, foco, contraste, zoom 200%) segue não
     verificada: não há aplicação nem MCP de navegador. Pré-requisito da primeira publicação
     renderizada, não deste ticket.
- Critérios de aceite: [ ] 1–7 — atendidos na visão de produtor e dos três revisores;
  validação independente com evidência é do `qa-validator`.

## [011] HANDOFF — 2026-08-01 14:40
- De: qa-validator#3 → Para: tech-lead
- Status novo: **done**
- Veredito: **APROVADO — 7/7 critérios atendidos com evidência própria.** Nenhum defeito
  bloqueante. Nenhuma evidência herdada: todos os comandos abaixo foram reexecutados por mim;
  nenhuma linha de `[004]`–`[008]` foi copiada.

### Ambiente da validação
- Commit base: `21f6ef1` (`TCK-0002: aprova a spec da primeira fatia de aprendizagem`),
  branch `main`, working tree sujo (trabalho paralelo em TCK-0003/0004 — **não tocado**).
- Diff sob validação: `git diff --numstat -- content/` → `17 0` (en-US) e `18 0` (pt-BR).
  Apenas os 2 arquivos de teoria do nó piloto estão modificados em `content/`.
- Sem navegador, sem MCP `chrome-devtools`, sem leitor de tela. **Não há aplicação para
  subir**: `find . -maxdepth 2 -name package.json` → vazio; `grep -rn "theory\."
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.py' .` (excluído o próprio
  auditor) → vazio, isto é, **nenhum código consome os `theory.*.md` hoje**. Validação é de
  **artefato de conteúdo**; ver §"O que não foi verificado".

### Critério 1 — 8/8 fórmulas de `theory.pt-BR.md` com `*Leitura:*` logo após o bloco — **✓**
- `grep -c '^\$\$' theory.pt-BR.md` → `8`; `grep -c '^\*Leitura:\*' theory.pt-BR.md` → `8`.
- Contagem sozinha não prova nada (L-012). Prova de **posição**, por ordem:
  `grep -n '^\$\$\|^\*Leitura:\*' theory.pt-BR.md` →
  `34/36 · 44/46 · 51/53 · 66/68 · 79/81 · 87/90 · 103/105 · 118/121` —
  **alternância estrita fórmula → descrição, 8 pares, zero bloco órfão, zero descrição órfã.**
- Verificação extra que ninguém fez e que a contagem esconde: `grep -o '\$\$' theory.pt-BR.md
  | wc -l` → `16`. Como há 8 linhas começando com `$$` e 16 ocorrências no total, os 8 `^\$\$`
  são todos **aberturas** (os fechamentos ficam no fim da última linha, inclusive nos dois
  blocos multilinha 87–88 e 118–119). Logo são de fato 8 blocos, não 7 blocos + 1 fechamento
  contado por engano.

### Critério 2 — 8/8 em `theory.en-US.md` — **✓**
- `grep -c '^\$\$'` → `8`; `grep -c '^\*Reading:\*'` → `8`; `grep -o '\$\$' | wc -l` → `16`.
- Ordem: `grep -n '^\$\$\|^\*Reading:\*' theory.en-US.md` →
  `33/35 · 43/45 · 50/52 · 64/66 · 77/79 · 85/88 · 101/103 · 115/118` — alternância estrita.

### Critério 3 — as descrições **lêem** a fórmula (reconstrutível) — **✓**
Leitura adversarial **minha**, feita às cegas: li apenas o texto da descrição, escrevi o LaTeX
que ela induz e só depois abri o bloco. Escolhi 4 das 10 descrições novas, incluindo
obrigatoriamente a do Exemplo 1 com a fórmula geral (a mais longa e a de maior risco de
agrupamento).

| # | Onde | LaTeX que **eu** reconstruí de ouvido | Bate com o bloco? |
|---|---|---|---|
| 6 | pt-BR:90 / en-US:88 | `x = \frac{-(-5) \pm \sqrt{1}}{2 \cdot 1} = \frac{5 \pm 1}{2} \Longrightarrow x_1 = 3,\ x_2 = 2` | **sim** |
| 4 | pt-BR:68 / en-US:66 | `x_1 + x_2 = -b/a`, `x_1 \cdot x_2 = c/a` | **sim** |
| 8 | pt-BR:121 / en-US:118 | `k^2 - 4\cdot1\cdot9 = 0 \Longrightarrow k^2 = 36 \Longrightarrow k = 6\ \text{ou}\ k = -6` | **sim** |
| 5 | pt-BR:81 / en-US:79 | `\Delta = (-5)^2 - 4\cdot1\cdot6 = 25 - 24 = 1 > 0` | **sim** |

Divergências encontradas: apenas espaçamento tipográfico (`\;`, `\quad`, `\qquad`) e a
pontuação final do parágrafo — nenhum carrega conteúdo matemático.

Ataques que **eu** tentei contra a descrição 6 (a de maior risco), e por que falham:
1. *Reagrupar o numerador*: "tudo dividido por dois vezes um" é âncora retroativa; o único
   delimitador aberto antes dela é "x é igual a", então o numerador só pode ser
   `-(-5) \pm \sqrt{1}`. Não consegui produzir `-(-5) \pm \frac{\sqrt1}{2\cdot1}` sem ignorar
   o "tudo".
2. *Escopo do primeiro sinal*: tentei ler `-((-5) \pm \sqrt1)`. A vírgula após "menos" e o par
   falado "abre/fecha parênteses" fecham o operando em `(-5)`. E, mesmo nesse parse hostil, o
   conjunto-solução seria o mesmo `{3, 2}` — não há caminho para erro de resultado.
3. *Cadeia dupla de igualdade*: "isso é igual a … tudo dividido por dois" marca o segundo elo
   sem fundi-lo ao primeiro; a implicação final vem como "o que implica" (⟹), não como
   equivalência. Direção preservada.
4. *Subscrito*: "x índice 1" / "x subscript 1" — sem isso, "xis um" seria irrecuperável
   ($x_1$ vs $x^1$ vs $x\cdot1$). Verbalizado corretamente nas duas línguas.
5. Descrição 5/7: `(-5)^2` lido como "abre parênteses menos cinco fecha parênteses ao
   quadrado" — o erro clássico `-5^2 = -25` é impossível de reconstruir. Correto.

### Critério 4 — paridade pt-BR/en-US — **✓**
- Cobertura simétrica **por posição**, não por contagem: as duas listas de `grep -n` acima
  descrevem as mesmas 8 fórmulas, na mesma ordem e nas mesmas seções. Nenhuma fórmula descrita
  num idioma e muda no outro, nos dois sentidos.
- Comparação estrutural própria (script Python ad hoc, no scratchpad): extraí os 8 blocos de
  descrição de cada arquivo, normalizei o vocabulário par a par (`índice`↔`subscript`,
  `tudo dividido por`↔`all divided by`, `o que implica`↔`which implies`, `abre/fecha
  parênteses`↔`open/close parenthesis`, numerais por extenso → dígito) e comparei as sequências
  de tokens. **As 5 descrições novas (4, 5, 6, 7, 8) produzem sequências idênticas nos dois
  idiomas**; a única diferença residual, na 6, é o artigo (`a raiz quadrada` × `the square
  root`) — item lexical, não matemático.
- Convenção decimal (`docs/content/i18n.md`): `grep -n '^\*Leitura:\*\|^\*Reading:\*' -A2 |
  grep -E '[0-9]+[.,][0-9]+'` → **vazio nos dois arquivos**. Todo valor lido é inteiro e vem
  por extenso; a regra vírgula × ponto **não é acionada** — conferido por comando, não aceito
  de palavra.

### Critério 5 — nenhuma afirmação matemática nova — **✓**
- Busca negativa por conectivo justificativo dentro das linhas acrescentadas:
  `git diff -- content/ | grep -E '^\s*\+\*?(Leitura|Reading)' -A3 | grep -inE 'logo|portanto|
  porque|assim|therefore|hence|because|since'` → **vazio**. As descrições não concluem,
  não justificam e não estendem: só leem.
- Verificação numérica **independente** (Python puro com `Fraction`; SymPy indisponível):
  `(-5)^2 - 4·1·6 = 1 > 0` ✓ · `-(-5) = 5`, `(5±1)/2 = {3, 2}` ✓ · substituição de volta
  `3²-5·3+6 = 0` e `2²-5·2+6 = 0` ✓ · `x_1+x_2 = 5 = -b/a` e `x_1x_2 = 6 = c/a` ✓ ·
  `(-4)^2-4·1·5 = -4 < 0` ✓ · `k²-36 = 0` tem exatamente `{-6, 6}` em `[-100,100]` ✓.
  Todo valor falado nas descrições confere com o LaTeX e com a aritmética.

### Critério 6 — LaTeX intocado — **✓** (duas provas independentes)
1. `git diff -U0 -- content/ | grep -E '^-[^-]'` → **saída vazia**; `| grep -cE '^-[^-]'` →
   `0`. Zero linhas removidas ou modificadas: o diff é de acréscimo puro.
2. Prova direta, que não depende do formato do diff: para cada arquivo,
   `diff <(git show HEAD:<path> | grep -n '\$\$' | sed 's/^[0-9]*://') <(grep -n '\$\$' <path>
   | sed 's/^[0-9]*://')` → **sem diferença nos dois arquivos**. As linhas que contêm `$$` são
   byte a byte iguais às do commit `21f6ef1`.
- `git diff --name-status -- content/` → só `M`, nenhum `R`: **nenhum slug renomeado**.

### Critério 7 — `bash scripts/audit-content.sh` sem erros nem avisos novos — **✓**
- `bash scripts/audit-content.sh > out 2>&1; echo $?` → **exit `0`** (capturado sem pipe,
  para o código de saída ser o do script e não o do `tail`).
- Saída: `Resumo: 1 nós · 0 erros · 0 avisos`. Zero avisos no total ⇒ zero avisos novos.
- **Alcance desta evidência (declarado, para não ser lida a mais do que vale):**
  `grep -n 'Leitura\|Reading\|\$\$' scripts/audit-content.py` → nenhuma ocorrência. O auditor
  verifica presença e não-vazio de `theory.<lang>.md` (`check_theory`, linhas 149–157), **não**
  descrição de fórmula (L-012). Auditoria verde é necessária, não suficiente — o que sustenta
  os critérios 1–5 são os comandos e a leitura adversarial acima, não o exit `0`.

### Requisitos transversais
- **Bilinguismo:** os dois `theory.<lang>.md` existem, não estão vazios (auditor) e estão em
  paridade estrutural (critério 4). Nenhum conteúdo monolíngue introduzido.
- **Acessibilidade:** é o objeto do ticket — 8/8 blocos descritos nos dois idiomas, com
  reconstrutibilidade verificada por mim em 4 descrições.
- **Custo zero:** `git diff --numstat -- content/` → só inserções de texto em 2 arquivos
  markdown. Nenhuma dependência, serviço ou asset novo.
- **URLs de `content/` preservadas:** `git diff --name-status` só com `M`; o caminho
  `content/high-school/algebra/quadratic-equations/` é o mesmo do commit base.
- **Correção matemática verificada:** verificação numérica própria acima, independente da de
  `[006]`.
- **Offline/PWA e privacidade:** não aplicável, e **por quê**: a entrega é markdown estático,
  sem aplicação (`package.json` inexistente) e sem consumidor no repositório; não coleta dado
  algum.

### Independência da cadeia — conferida
Produtor `content-author` (`[004]`). Critério 3 avaliado pelo `a11y-ux-reviewer` (`[008]`),
critério 4 pelo `i18n-steward` (`[007]`), critério 5 pelo `math-reviewer` (`[006]`) — cada um
no papel competente, e **nenhum deles validou artefato próprio**: os três revisaram o texto do
`content-author`, e os três declararam explicitamente não opinar sobre o critério dos outros.
Eu, `qa-validator#3`, não produzi nem revisei nada deste ticket.

### Ponto de julgamento (a) — descrição preexistente incompleta: **NÃO bloqueia**
`theory.pt-BR.md:51` / `en-US.md:50` é um bloco de duas partes
(`x = \frac{-b \pm \sqrt{\Delta}}{2a}, \qquad \Delta = b^2 - 4ac`) e a descrição de 53 / 52
lê só a primeira; `\Delta = b^2 - 4ac` fica mudo. Confirmei por leitura própria, e confirmei
por `git diff | grep 'raiz quadrada de delta'` → **vazio**: a descrição é preexistente e não
foi tocada por esta entrega.

**Veredito: o critério 1 é de existência e posição, não de suficiência de cobertura.** Três
razões, todas no texto do próprio ticket, escrito antes da entrega:
1. O critério fixa como padrão de conformidade **"o mesmo padrão das 3 já existentes"** — e a
   descrição incompleta **é uma das 3**. Um critério não pode exigir que sua própria referência
   seja refeita; ler assim é reescrever o critério depois da entrega.
2. O "Pedido original" e o "Requisito refinado" declaram o baseline como "**3** linhas
   `*Leitura:*` (36, 46, 53)" e "cumpre a regra em **3 de 8**". A linha 53 está nomeada,
   contada como cumprida. O delta contratado eram 5 descrições, e 5 foram entregues.
3. A suficiência mora no critério 3 ("as descrições lêem a fórmula … consegue reconstruí-la"),
   que qualifica as descrições escritas — e as 10 novas passam. Cobertura de sub-expressão de
   um bloco é justamente o que nenhum dos 7 critérios enuncia.

Alterar o critério é decisão do `tech-lead`, não minha. **Não reprovo por isso.**

Achado próprio que **reduz** (sem anular) a severidade estimada em `[008]` §7.1: a metade muda
não é informação perdida do documento. `\Delta = b^2 - 4ac` aparece isolado no bloco anterior
(linha 44 / 43) e é lido integralmente na linha 46 / 45 ("delta é igual a b ao quadrado menos
quatro a c"), **cinco linhas acima**. O que o bloco 3 traz é um lembrete literal do que acabou
de ser lido; o usuário de leitor de tela não fica sem a definição do discriminante, fica sem a
repetição dela. Continua sendo defeito de a11y a corrigir — só não é "perder metade do teorema".

### Ponto de julgamento (b) — teorema sem a hipótese $\Delta \ge 0$: **NÃO bloqueia**
Confirmado por leitura própria de `theory.pt-BR.md:48-51` / `en-US.md:47-50`. Não bloqueia
este ticket por três razões independentes, e nenhuma delas é deferência ao `[006]`:
1. **Está fora do diff.** `git diff | grep 'soluções reais\|real solutions'` não retorna nada;
   as linhas 48/47 são idênticas ao commit `21f6ef1`. Nenhum critério de 1 a 7 alcança prosa
   não alterada — o critério 5 fala do que a **descrição** introduz.
2. **Nenhuma descrição nova repete a imprecisão.** Verifiquei: as 10 descrições acrescentadas
   não mencionam existência de raiz, condição sobre `\Delta` nem quantificação — elas leem
   estrutura. A entrega não propaga o defeito.
3. **Não é erro matemático**, e sim enunciado mal-formado para `\Delta < 0` (com `\sqrt{}`
   indefinida em `\mathbb{R}`, o lado direito não denota) — não existe atribuição de `a,b,c`
   que produza afirmação falsa. Minha verificação numérica não tinha como pegá-lo, e não pegou;
   é exatamente o que L-014 registra.
Severidade `menor`, com a condição correta já registrada: corrigir **antes de o nó sair de
`draft`**, não antes deste `done`.

### Pendências herdadas (7) — nenhuma bloqueia; reconfirmadas por mim uma a uma
Todas fora do diff desta entrega, todas verificadas como preexistentes no commit `21f6ef1`.
**Condicionam a saída de `status: "draft"`** as de nº 1, 2, 3 e 5; as de nº 4, 6 e 7 não.
1. Hipótese `\Delta \ge 0` ausente no enunciado (48/47), no Resumo (143/140) e em soma e
   produto (144/141) — **condiciona `draft`** (L-014).
2. Descrição preexistente incompleta (53/52) — **condiciona `draft`**: enquanto existir, o nó
   viola `AGENTS.md` §9.2 em 1 dos 8 blocos, ainda que o critério 1 deste ticket não a alcance.
   Julgamento (a) acima; severidade menor que a estimada em `[008]`, mas real.
3. Tabela "Erros comuns" (133/130) contrasta duas frações cujo único diferencial é o
   agrupamento — lido linearmente, o contraste desaparece e a lição fica inacessível
   justamente para quem depende de leitura linear. **Condiciona `draft`** (é conteúdo
   didático inacessível, não melhoria).
4. `\dfrac` inline no Resumo e 10 `\frac` inline em `exercises.json` — decisão de **regra**
   (`AGENTS.md` §9.2 deve cobrir inline?). Não condiciona `draft`; condiciona a regra.
5. Registrar as convenções de leitura em `docs/content/accessibility.md` e a linha
   `subscrito (índice) | subscript` no glossário de `docs/content/i18n.md` — **condiciona o
   próximo nó de conteúdo**, e por isso na prática **condiciona `draft`** do piloto, que é o
   modelo. Confirmei que a convenção é inédita: `grep -rn 'índice 1\|subscript 1' docs/
   content/` só encontra as ocorrências deste ticket.
6. Duplicação fórmula + descrição no áudio quando houver render (MathML do KaTeX) — depende de
   stack (ADR-0003). Não condiciona `draft`; condiciona o primeiro render.
7. Parte 2 do `/a11y-audit` (leitor de tela real, foco, contraste, zoom 200%) — não condiciona
   `draft`; é pré-requisito da primeira publicação renderizada.

### O que NÃO foi verificado (declaração obrigatória)
Sem aplicação, sem navegador e sem leitor de tela neste ambiente, **não** foram exercitados:
locução real por NVDA/JAWS/VoiceOver nos dois idiomas, MathML efetivamente emitido pelo KaTeX,
navegação por teclado, ordem de foco, contraste, tema claro/escuro, zoom 200%, offline e
reconexão, recarga no meio de exercício, rede lenta e dados vazios. Não é omissão: **não há o
que subir** (sem `package.json`, sem consumidor dos `theory.*.md`), e a bateria hostil é de
interface, não de artefato markdown. Fica coberta pelas pendências 6 e 7, ambas pré-requisito
da primeira publicação renderizada.

- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 — **todos com
  evidência reproduzida acima**.
- Resultado: **done**. Nada foi corrigido nem editado por mim em `content/`:
  `git diff --numstat -- content/` segue `17 0` / `18 0`.
- Lição: n/a — não resolve `REJECT`. L-012 aplicada (verificação por ordem, não por contagem)
  e não violada.
