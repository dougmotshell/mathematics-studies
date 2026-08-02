# Memória do agente `qa-validator`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Valida a entrega contra os critérios de aceite do ticket, executando a aplicação de verdade e produzindo evidência por critério. Único agente que pode marcar um ticket como done.

## Notas persistentes

- **Ticket documental não se valida "por leitura de código" — valida-se por contagem e busca
  na fonte.** Quando a entrega é spec/ADR/doc, a evidência por critério é `grep -c`/`grep -n`
  reproduzido pelo próprio QA (contagem de RF/RNF/CA/tasks, seções, e busca **negativa** por
  termos proibidos), mais o código de saída dos scripts de auditoria. Declarar no log que a
  validação foi documental e apontar em qual task a execução real acontece.
- **Prova de "não trava a stack" é busca negativa.** `grep -nEi 'astro|react|vue|next|vite|
  vercel|tailwind|indexeddb|service worker|playwright|jest|vitest|…'` nos artefatos: toda
  ocorrência precisa estar em contexto de exclusão (fora de escopo / decisão adiada). Zero
  ocorrência positiva = critério provado; uma ocorrência afirmativa = defeito.
- **Capturar exit code sem pipe.** `bash script.sh > arquivo 2>&1; echo $?` — com
  `bash script.sh | tail`, o `$?` é do `tail` e a evidência do critério fica falsa.
- **Pergunta em aberto só bloqueia se deixar a próxima etapa sem alvo.** Teste aplicado:
  a spec decide um padrão normativo (RF/CA) para a pergunta? A próxima task consegue começar
  sob esse padrão? Se sim nas duas, `approved` com adiamento registrado (dono + prazo) é
  legítimo; se não, é `blocked: human-input`. Padrão do projeto: `tasks.md` "resolvidas ou
  explicitamente adiadas com dono".
- **Critério pede informação, não cabeçalho.** Antes de reprovar por seção ausente, conferir o
  template canônico (`docs/specs/templates/`): se ele não prevê a seção e a informação está
  presente e falseável, o critério está atendido — reprovar seria negociar critério por forma,
  o que não é papel do QA.
- **Defeito fora do escopo não bloqueia, mas tem de sair com evidência.** Achado em `content/`
  durante ticket que proíbe tocar `content/` (RNF-9) vira `ACTION` no handoff, com arquivo +
  linhas, endereçado ao `tech-lead`, e prazo relativo à task que ele quebraria.
- **Contradição em documento normativo só é defeito se produzir restrição operativa errada.**
  Teste aplicado em TCK-0003: o rótulo Mermaid "KaTeX pré-renderizado" contra o texto que dizia
  não decidir era defeito (o dev receberia obrigação inexistente); "o diagrama não mostra nenhum
  mecanismo" enquanto exibe IndexedDB e Vercel **decididos** é dívida — erra **subestimando**, e
  a decisão é afirmada normativamente em outros 4 pontos. Direção do erro importa: sobreafirmar
  bloqueia, subafirmar não. Reprovar por precisão de redação, com a frente parada e o limite de
  loops esgotado, é negociar critério por forma.
- **Regra obsoleta não anula desbloqueio se for guarda condicional com condição falsa.** Ao
  validar propagação de aceite de ADR, classificar cada ocorrência restante em: (a) guarda
  condicional ("enquanto X estiver `proposed`") → não dispara; (b) exemplo envelhecido dentro de
  norma que continua válida sozinha → não dispara; (c) registro meta/histórico → inofensivo;
  (d) **afirmação** do estado obsoleto como fato → é a única que arrisca anular. Em TCK-0003 as
  7 pendências caíram em (a)/(b)/(c), e só `.claude/workflows/feature-plan-review.js:64` era (d).
- **Ao remover um bloqueio, provar por busca negativa que a regra vizinha sobreviveu.**
  `git diff -U0 | grep '^-' | grep -i '<regra>'` **vazio** + contagem `git show HEAD:<arq> |
  grep -c` igual à atual é a prova; ler os pontos editados não é. Em TCK-0003 a regra em risco
  era "nenhuma implementação sem spec aprovada", vizinha do texto de stack em 11 arquivos.
- **Gerado pode ter texto que a fonte não tem sem ser invenção.** Comparar corpo a corpo (sem
  front matter e marcadores `managed-by`) e, para cada linha extra, checar `git show HEAD:` —
  rodapé fixo do gerador é pré-existente, não deriva. `--check` verde prova sincronia, não
  correção do texto propagado.
- **Dono e prazo de decisão pendente registrados só no `log.md` são dívida.** Quem retoma lê a
  spec, não o log; sinalizar como pendência ao aceitar.

- **Reproduzir, nunca herdar evidência.** Produtor e revisor já anexam saída de comando no
  log; o valor do QA é reexecutar. Em TCK-0001 isso significou baixar o PDF de novo,
  localizar a seção por varredura própria e renderizar o selo de licença — não citar o
  `[006]`.
- **Nem todo ticket tem UI.** Quando o artefato é arquivo de dados (`references.json`,
  `meta.json`), a bateria de casos hostis (offline, tema, zoom, teclado, leitor de tela) não
  é aplicável — mas **registrar explicitamente no log por que não é**, com a checagem que
  sustenta isso (ex.: `grep -rn "<arquivo>" --include='*.ts' …` mostrando que nenhum código
  o consome). Marcar "n/a" sem justificar é aprovar na confiança.
- **Critério só se lê com o que estava escrito.** Sugestão de revisor que redefine o critério
  depois da entrega vira dívida, não `REJECT`. Antes de tratar algo como violação, checar se
  existe contrato real: schema em `docs/content/`, validação em `scripts/audit-content.py`,
  consumidor no repositório. Se não existe nenhum dos três, é dívida — mudar critério é
  decisão do `tech-lead`.
- **Medir o alcance da própria evidência.** `audit-content.sh` só valida *presença* de
  `author/year/url/language/license` (`scripts/audit-content.py:264-283`): não faz rede, não
  valida `covers` nem formato de licença. Auditoria verde é necessária, não suficiente —
  declarar isso no log evita que "audit passou" seja lido como "fonte verificada".
- **Duplicação de fato é dívida com data de validade.** Quando a mesma informação aparece em
  dois campos (licença dentro de `covers` *e* no campo `license`), um deles envelhece em
  silêncio. Vale registrar mesmo quando nada está errado hoje.
- **Critério de cobertura: existência × suficiência é decisão de leitura, e a âncora está no
  próprio critério.** Quando o critério diz "no mesmo padrão dos N já existentes", ele **elege
  os preexistentes como referência de conformidade** — exigir que um deles seja refeito é
  reescrever o critério depois da entrega (decisão do `tech-lead`, não do QA). Teste rápido:
  (i) o baseline do ticket conta esse item como cumprido? (ii) o delta contratado foi
  entregue? Se sim nas duas, o defeito é real mas é **pendência**, não `REJECT` — e sai com
  condição explícita (ex.: "condiciona a saída de `draft`").
- **Antes de aceitar a severidade que o revisor atribuiu, medir o impacto você mesmo.** Em
  TCK-0005, "o usuário perde metade do bloco do teorema" virou "perde a repetição, não a
  definição" depois que eu confiri que o `\Delta = b^2-4ac` mudo era repetição literal de um
  bloco descrito integralmente 5 linhas acima. Continua defeito; muda a prioridade.
- **`grep -c '^\$\$'` pode mentir sobre número de blocos.** Se um bloco fechar com `$$` em
  início de linha, o fechamento entra na contagem. Cruzar com
  `grep -o '\$\$' <arquivo> | wc -l`: total = 2 × blocos. Em TCK-0005 deu 8 e 16 — os 8 eram
  todos aberturas, inclusive nos dois blocos multilinha.
- **"LaTeX intocado" merece uma segunda prova que não dependa do diff.**
  `diff <(git show HEAD:<path> | grep -n '\$\$' | sed 's/^[0-9]*://') <(grep -n '\$\$' <path>
  | sed 's/^[0-9]*://')` compara as linhas de fórmula com o commit base direto. Vale porque
  `git diff -U0 | grep '^-[^-]'` vazio prova "nada removido", não "as fórmulas são as mesmas".
- **Paridade i18n se prova por token, não por leitura.** Extrair as descrições dos dois
  arquivos, normalizar o vocabulário par a par (`índice`↔`subscript`, `tudo dividido
  por`↔`all divided by`, numerais por extenso → dígito) e comparar as sequências. Diferença
  residual só em artigo/preposição = paridade; diferença em operador, sinal ou ordem = defeito.
- **Achado fora do diff sai com condição, não só com endereço.** Listar pendência herdada sem
  dizer *o que ela condiciona* (saída de `draft`, a regra, o primeiro render) devolve ao
  `tech-lead` a triagem que o QA acabou de fazer com o artefato na mão.
- Ambiente: `curl 8.5.0` e poppler (`pdftotext`, `pdfinfo`, `pdftoppm`) disponíveis e com
  rede — dá para validar fonte externa de ponta a ponta, inclusive licença que só existe
  como **imagem** (selo CC), via `pdftoppm -png` + leitura da imagem.
- **Conferência literal de licença é diff mecânico, não leitura.** Baixar a fonte canônica
  (`curl -sSL https://raw.githubusercontent.com/spdx/license-list-data/main/text/MIT.txt`),
  isolar a parte legal (cortar no separador `---`), normalizar só espaçamento/aspas
  tipográficas, substituir o placeholder pelo titular real e comparar **palavra a palavra**
  com `difflib` — depois repetir com uma lista fechada de cláusulas obrigatórias. Ler "parece
  a MIT" não é evidência; 169 palavras dos dois lados e zero diferenças é.
- **Regra propagada se mede pelo caminho de auto-carregamento, não pelo `grep`.** Para cada
  ferramenta, provar o caminho: `CLAUDE.md`/`GEMINI.md` → `@AGENTS.md`; `applyTo` da
  instruction casando com o glob do escopo; `globs:`/`trigger:` no front matter do gerado
  (Cursor/Windsurf); concatenados (`.rules`, `.clinerules`, `.junie/guidelines.md`) derivam de
  **core**, não do escopo — carregam versão condensada e precisam ser lidos à parte. Adapters
  de agent (`.github/chatmodes/`, `.gemini/commands/`, `.claude/commands/`) são **ponteiros**
  de ~25 linhas: a regra chega por referência, não por cópia — conferir com `grep -l` pelo
  caminho da fonte em vez de procurar o texto da regra neles.
- **Renumeração de seção: classificar todas as ocorrências, inclusive os falsos positivos.**
  `grep -rn "§9\.[0-9]"` pega "§9.3" de livro externo e narrativa histórica de log
  append-only. Separar em (a) falso positivo, (b) seção intocada — provar com `git diff` que o
  hunk não a alcança, (c) referência viva — resolver uma a uma contra o texto novo, (d)
  histórico. Complementar com busca **sem** o símbolo `§` e com busca negativa pelo texto
  antigo da regra ("preferência por CC BY"): se só sobrar narrativa histórica, está limpo.
- **Contagem de ocorrências não bate entre revisor e QA — e isso é normal.** O log cresce
  entre a revisão e a validação (30 → 49 aqui), então divergência de contagem não é defeito;
  o que precisa bater é a **classificação**, não o número.
- **Imprecisão na justificativa ≠ regra errada.** Antes de reprovar por "razão declarada
  imprecisa", levantar **todas** as afirmações sobre o objeto nas fontes normativas e checar
  se alguma afirma algo **falso**. Omissão de nuance numa cláusula que o critério não pede,
  com conclusão operacional correta e conservadora, é dívida. Reprovar aí seria renegociar
  critério.
- **Working tree compartilhado: registrar o commit no início E no fim.** Em 2026-08-01 o HEAD
  avançou (`21f6ef1` → `f96baa9`) no meio da validação, por commit de outro ticket. Confirmar
  que os artefatos do ticket validado não foram afetados (`git status --porcelain` mostrando-os
  ainda `??`/`M`) e reexecutar as auditorias **imediatamente antes** do veredito.
- **Mermaid valida em Node sem navegador, com dois ajustes.** `npm install mermaid@11 jsdom`
  no scratchpad; setar `global.window`/`global.document` a partir do `JSDOM` (não tentar
  sobrescrever `global.navigator` — só tem getter no Node 24) e chamar `mermaid.parse`. Sem o
  shim, o erro é `DOMPurify.addHook is not a function` — que é ambiente, não diagrama inválido.

- **Configuração invisível ao `git status` falsifica a validação.** `.claude/settings.local.json`
  é gitignored e não aparece em diff nem em `git status`, mas entra **primeiro** na resolução
  da janela do `context-watch`. Antes de validar qualquer ferramenta que leia configuração,
  perguntar "existe arquivo local ignorado que muda este resultado?" e validar com ele
  **movido para fora**, restaurando por `diff` contra a cópia no final. Validar com ele no
  lugar é validar a máquina, não a ferramenta.
- **Ferramenta de alarme não se valida por chamada isolada — encena-se a sessão inteira.**
  A prova que importa é a **travessia**: estado zerado, sem configuração nenhuma, transcripts
  sintéticos crescentes, medindo hook e terminal em cada passo. Foi ela que mostrou 7 disparos
  em 4 faixas em TCK-0012 (e teria mostrado o defeito B5 — um alarme falso e zero verdadeiros
  — se ele ainda existisse). Rodar cada zona uma vez não distingue "avisa" de "avisa uma vez e
  emudece".
- **Dívida declarada só é aceitável depois de eu medir o modo de falha, não o rótulo.** Em
  TCK-0012 o rótulo era "superestima a janela"; a simulação de um modelo de 400k mostrou que o
  modo real é **um aviso na travessia e silêncio em toda a faixa de perigo** (85% e 98,8% de
  uso reportados como `verde`). Aceitei mesmo assim, mas com **gatilho escrito**: o dia em que
  a condição de raio-zero cair (existir modelo com janela intermediária), a dívida vira
  defeito. Dívida sem gatilho é defeito adiado sem dono.
- **Contar as asserções por fora do contador do próprio script.** `grep -c '^ok '` na saída,
  cruzado com o total impresso, e `grep -ci skip` para garantir que nada foi pulado. "93
  passaram" dito pelo script que eu estou validando não é evidência independente.
- **`| tail` mata o exit code; `$?` de `bash script.sh | tail -1` é do `tail`.** Rodar
  `cmd > arquivo 2>&1; echo $?` e só depois inspecionar o arquivo (já estava na memória —
  reconfirmado aqui ao medir os cinco exit codes).
- **Teste de canário de privacidade se faz na saída agregada de TODOS os canais.** Texto,
  `--json`, `--hook` silencioso, `--hook` com mensagem, `--quiet` e o caminho de erro, num só
  arquivo, com `grep -c <canario>` → 0. Espalhar o canário em 7 posições do fixture (prompt,
  `thinking`, `text`, `tool_use.input`, `toolUseResult`, `tool_result`, `cwd`/`gitBranch`)
  cobre a classe; testar só `message.content` cobre um caso.
- **Hook ativo se prova por efeito colateral observado, não por invocação.** Em TCK-0012 o
  `PostToolBatch` foi provado ativo vendo `updated_at` do arquivo de estado em
  `~/.local/state/` avançar em lockstep com os meus lotes de ferramenta, **sem** eu invocar o
  script. Invocar por pipe prova que o comando funciona; só o efeito colateral prova que o
  runtime o está chamando.
- **"Casos hostis de UI não se aplicam" exige a prova do consumidor zero.** `grep -rn` pelo
  nome da ferramenta nas extensões de aplicação (`*.ts|*.tsx|*.js|*.astro|*.html|*.css`) → 0,
  mais `ls package.json src/ app/` inexistentes. Sem isso é "n/a" na confiança.
- **Regra de entrada que aceita os dois separadores decimais é falso positivo esperando
  acontecer.** Em pt-BR o **ponto** é separador de milhar (`docs/content/i18n.md:20`), em en-US é
  a **vírgula**. Um desenho que escreve a guarda de ambiguidade só para um dos idiomas deixa o
  outro lendo `3.000` como `3.0` — e, contra `answer: 3, tolerance: 0`, isso marca **certa uma
  resposta errada**. Teste que aplico: implementar a regra **literalmente** nos dois idiomas e
  rodar contra os itens `numeric` reais com as sete entradas `3 · 3,5 · 3.5 · 3.000 · 3.500 ·
  3,000 · 3,500`. Direção do resíduo decide a severidade: recusar entrada válida é mensagem de
  erro; aceitar entrada ambígua é nota errada.
- **Lição registrada transforma imprecisão em bloqueio.** `L-021` diz que o caso deixado de fora
  de uma norma "não fica neutro: fica permitido"; `L-013` diz que corrigir a linha citada não é
  corrigir a classe. Quando o achado do revisor cai **exatamente** dentro de uma lição indexada,
  a regra 7 do AGENTS.md o torna bloqueante — mesmo que, sem a lição, eu o registrasse como
  dívida. Vale dizer isso no `REJECT` (fiz no defeito 2 do TCK-0013): declarar "sozinho, isto
  seria dívida" mantém a severidade honesta e evita inflar o loop.
- **Diagrama é a segunda metade de todo defeito de prosa.** No TCK-0013 o `[006]` bloqueou a
  enumeração do cartão do índice em §5; a correção arrumou a prosa e deixou o mesmo texto no
  rótulo do nó Mermaid, que vem **antes** no documento e é normativo por `DOC-STANDARDS`.
  Ao revalidar um `REJECT`, buscar o **texto do defeito**, não a linha do defeito.
- **Auditoria vermelha por deriva de ticket alheio: nem `REJECT`, nem `done` — é segurar.** O
  critério "`--check` exit 0" mede o **estado do repositório**, não o diff do ticket. Com
  working tree compartilhado, a saída correta é manter `in_validation` até a outra cadeia
  sincronizar: reprovar puniria quem não causou, e aprovar assinaria o estado alheio. Em
  TCK-0011 o estado **oscilou dentro da minha própria validação**: verde às 16:5x (a cadeia do
  TCK-0006 sincronizou), vermelho de novo às 17:1x (ela passou de `content.*` para `core.*`).
  **Evidência de auditoria envelhece nos dois sentidos**, e por isso o QA reexecuta em vez de
  herdar o `[~]` — mas também por isso o veredito não pode se apoiar em "está verde agora".
- **Contra invariante global que o ticket não controla, a prova é a janela verde observada.**
  O que fecha o critério não é a atribuição da deriva (necessária, insuficiente), é ter
  **medido** um estado do repositório em que os artefatos do ticket já estão todos no lugar
  **e** a invariante vale. Isso troca "argumento de que não fui eu" por "medição de que não
  fui eu". Sem essa janela, a saída correta volta a ser segurar. E segurar por deriva cíclica
  de outra cadeia é tornar o fechamento refém de calendário alheio, sem ganho de informação.
- **Correção do próprio veredito se faz por `CORRECTION`, não reescrevendo a entrada.** Escrevi
  no `[010]` que a auditoria estava verde; 20 minutos depois não estava. Emendei em `[011]`
  citando o `[SEQ]`, com a base da decisão trocada explicitamente. Log append-only vale para o
  QA também — e era exatamente a providência que eu estava cobrando de outro agente.
- **Atribuir artefato intruso antes de ler como violação.** `package.json` apareceu no working
  tree durante um ticket cujo critério 9 dizia "nenhum `package.json`". Três provas de
  atribuição, todas necessárias: (i) o arquivo não está na lista de artefatos das entradas do
  ticket; (ii) o ticket paralelo o reivindica como entrega sua; (iii) o próprio artefato
  normativo do meu ticket declara que **não** cria arquivo de projeto. Sem as três, é palpite.
- **`PROPOSTO (ADR-N)` × `EM ABERTO (ticket)` se decide na fonte normativa, não na legenda.**
  Ler `plan.md`/`spec.md`: se a spec aprovada **atribui a decisão ao ticket**, marcar
  `PROPOSTO (ADR-N)` afirma que algum ADR deve fechá-la — erro simétrico ao de omitir o
  marcador, mesma família. A legenda só vale como prova depois de conferida contra a spec.
- **O defeito de texto só morre de verdade quando o ticket downstream exerce a autoridade
  devolvida.** Em TCK-0011 a prova decisiva não foi o `grep` no ADR corrigido: foi o TCK-0015
  já ter escrito `"prebuild"` no `package.json` **como decisão dele**, com o vocabulário
  ("rede de segurança") que o ADR passou a usar. Procurar essa confirmação a jusante vale mais
  que reler o parágrafo consertado.
- **Reproduzir a classificação do revisor pode expor erro de aritmética dele.** "7 de 22" era
  na verdade 7 de **28** (11 nós + 3 fronteiras + 14 relações) — a decomposição que ele mesmo
  escreveu (14 + 14) já não fechava com o total. A classificação estava certa; o número, não.
  Corrigir no log sem transformar em defeito.
- **Auditar legenda de diagrama é classificar 100% dos elementos, com a cláusula de herança.**
  Extrair `Person|Container|ContainerDb|System_Boundary|Rel` por regex, marcar quem traz token
  de fonte (`ADR-\d{4}`, `RF-\d+`, `PROPOSTO`, `EM ABERTO`) e **subtrair** os que herdam
  marcador do contêiner. Em TCK-0011: 15 sem token − 8 herdeiros = os 7 reais. O teste final
  não é a legenda, é o dano: o elemento sem fonte afirma mecanismo que só um ADR `proposed`
  sustenta? Se não, é dívida de redação.
- **Fonte de custo se confere baixando a página e casando cada número.** `curl -L` + remoção de
  `<script>`/tags + `re` por linha da tabela do ADR. Em TCK-0011, 6/6 linhas bateram — e sobrou
  um achado ao contrário: um número **verdadeiro** ("Concurrent Deployments 1") tinha sido
  removido no loop anterior por estar sob rótulo diferente do que o revisor procurou. Revisão
  que manda remover também erra.

- **Burla de portão se desenha por *classe de sentinela*, não por campo.** Em TCK-0014 os 7
  falsos negativos que achei caem em 3 classes: (i) **vazio que não é vazio** — `str.strip()`
  não remove U+200B/U+2060/U+FEFF, então um campo localizado "traduzido" com espaço de largura
  zero atravessa a regra de paridade bilíngue (NBSP e `\t\n` são pegos: o controle importa
  tanto quanto o ataque); (ii) **`None` significando duas coisas** — `load_json` devolve `None`
  para "arquivo ausente" **e** para arquivo cujo conteúdo é `null`, e o segundo vira "Contrato
  íntegro"; (iii) **estado por arquivo em vez de por nó** — `seen_ids` local torna `id`
  duplicado entre `exercises.json` e `assessments.json` invisível. Testar campo a campo não
  encontra nenhuma das três.
- **Controle negativo em cada vetor de burla.** `answer: ""` reprova e `answer: "   "` passa;
  `1e400` (float) é pego e `10^400` (inteiro) derruba o processo. Sem o par ataque+controle não
  dá para distinguir "a regra não existe" de "a regra existe e tem furo" — e é a segunda que
  vira dívida com gatilho.
- **Crash com `exit` conservador é dívida, não `REJECT` — mas só depois de medir o limiar.**
  `float(int)` estoura em ≥ 10^309 e o traceback vira `exit 120` com canal quebrado. Aceitei
  porque a direção do erro é barrar conteúdo (nunca aprovar) e nenhum critério nomeava o caso;
  registrei com **gatilho** (primeiro `numeric` com inteiro fora da faixa de `float`, plausível
  em `number-theory`/`research`). Medir `10^307 · 10^308 · 10^309 · 10^400` é o que transforma
  "quebra com número grande" em gatilho falseável.
- **Contar a cobertura declarada em vez de herdá-la.** Produtor e revisor disseram "4 tipos sem
  exemplar real"; a contagem no acervo deu **6** (faltavam `short-answer` e `true-false`) — e
  `true-false` era justamente o tipo da 4ª divergência do auditor. Uma linha de Python sobre
  `content/` refuta ou confirma a lista em segundos.
- **Regra nova dentro de ticket de implementação: o teste é "cabe dentro da norma escrita?".**
  `ITEMS-EMPTY` reprova em 0 itens enquanto o schema já exige 8–12 — é **mais frouxa** que a
  norma, logo automatização parcial, não contrato novo; não exige decisão prévia. Se fosse
  mais estrita que o documentado, seria decisão do `tech-lead`. Vale checar também a
  **simetria** da regra: `ITEMS-EMPTY` pune declarar vazio e não pune omitir o arquivo.
- **Falso negativo só pesa como bloqueante se a ferramenta *mais estrita* for a que aprova.**
  Foi o que tornou B1 bloqueante no loop 1. Rodei os meus 5 principais nas duas ferramentas em
  cópia isolada do repo (`audit=0 · validate=0` em todas): sem inversão, viram dívida. Esse
  cruzamento é barato e decide a severidade.
- **Regra de entrada se valida por vetor, não por leitura — e o vetor tem de ir além dos que o
  produtor declarou.** No TCK-0013 a regra corrigida foi checada com **26 entradas × 2 idiomas ×
  2 itens reais**: os 7 declarados no handoff mais separador duplicado, separador nas pontas
  (`3,`, `,5`, `3.`), sinal no fim, `+`, notação científica, separador árabe `3٫5`, apóstrofo
  suíço, espaço nas bordas e string vazia. Foram os vetores **não declarados** que produziram as
  duas dívidas novas; os declarados só confirmaram o que ele já sabia.
- **Classificar o resíduo por direção fecha a decisão sozinha.** Depois que os falsos positivos
  zeram, tudo o que sobra é falso negativo — e falso negativo com mensagem, sem penalidade e com
  o item parado no estado anterior é **dívida com gatilho**, nunca defeito. Escrever a direção do
  resíduo no veredito evita a discussão de severidade no loop seguinte.
- **A correção introduz eventos novos: revalidar as regras antigas contra eles.** A recusa de
  formato não existia antes; ela é um evento sem mudança de estado, com o foco parado, e o
  desenho não atribuiu região viva a ela (D-5). Ao aprovar uma regra nova, perguntar quais
  eventos ela cria e passar cada um pelas normas transversais do documento (anúncio, foco,
  paridade) — o produtor testa a regra, não os eventos que ela inventa.
- **Contagem do produtor não bate com a minha e isso não é defeito.** Ele reportou 19 linhas no
  `grep` da dimensão, eu medi 25 no arquivo já editado. O que precisa bater é a **classificação**
  (nenhuma sobra ensinando a convenção do outro idioma), não o número — mesma regra que já valia
  para contagem de log.
- **No loop 3/3 o QA decide entre bloquear e nomear.** Achado real, fora dos critérios escritos,
  com a regra geral do documento já resolvendo na direção segura e a devolução indo ao
  `tech-lead` em vez do produtor: vira **dívida com gatilho nomeado**, não `REJECT`. Bloquear aí
  é negociar critério por forma com a frente parada.

- **Norma normativa se valida reimplementando o critério, não relendo a tabela.** Em TCK-0006
  transcrevi o teste do texto de `accessibility.md:60-111` para um tokenizador LaTeX próprio
  **antes** de olhar os vereditos publicados, e só então comparei: 41/41 (23 fórmulas reais que
  eu extraí, 18 da tabela, 8 fronteiras que inventei). É a única prova de que a norma é
  aplicável por terceiro — "li e concordo" não distingue norma mecanizável de norma que só o
  autor sabe aplicar. E o resultado tem uso duplo: a mesma implementação refaz o inventário.
- **Ocorrência que dispara ≠ ponto de trabalho.** Meu parser achou **24** ocorrências que
  exigem marcação e o inventário dizia **22**: a diferença eram duas fórmulas cujo texto ao
  redor **já** dizia o agrupamento ("Substituir sempre entre parênteses: $(-5)^2$"). Antes de
  chamar divergência de contagem, ler a linha inteira — a norma exige o agrupamento **dito**,
  não uma marcação nova.
- **Padrão de busca publicado se testa contra os exemplos que o próprio documento dá.** O
  revisor achou 1 falso negativo no regex de `accessibility.md`; rodando-o contra os **cinco**
  exemplos que o documento lista para o gatilho, ele acha **2 de 5** — os três perdidos são as
  formas em que o `$` delimitador fica à esquerda. Fixture de 8 linhas com positivos e
  negativos custa 2 minutos e mede a severidade em vez de herdá-la.
- **Portão que cita veredito × portão que reenuncia a regra: o teste é "a condição pode ficar
  mais estreita que a norma?".** Condição = veredito do teste → não envelhece quando o teste
  ganha uma parte nova; condição = enumeração própria → envelhece calada, e foi assim que
  `-x^2` atravessava o checklist. A enumeração que sobra depois do veredito é ilustração, não
  condição — mas confira a conjunção: "as duas partes: (a) X **e** (b) Y" lido como conjunção
  afrouxaria o portão (D-1 do TCK-0006).
- **Dívida roteada a ticket `done` é dívida sem dono.** `[013]` encaminhou o validador da norma
  ao TCK-0014 — que já estava fechado. Ao aceitar dívida com encaminhamento, conferir o
  `status:` do ticket de destino; se for `done`, o encaminhamento vira pedido de ticket novo.
- **Janela verde se constrói em cópia da árvore, não se espera.** Com working tree
  compartilhado, `tar` da raiz para o scratchpad, `git show HEAD:<arquivo>` devolvendo **só** os
  arquivos da outra cadeia ao estado base, e as auditorias rodando **na cópia** com todos os
  artefatos do meu ticket no lugar → exit 0 nos três. Isso mede a atribuição em vez de
  argumentá-la, e não depende da outra cadeia sincronizar. Complementar com `stat -c '%y'`:
  fonte editada às 17:24 e gerado às 17:10 fecha a cronologia.

- **"Aceitar o ADR não fechou X" se prova por *absorção*, não por enumeração.** O teste correto
  é: pegar a fonte que **atribui** a decisão (`docs/specs/.../plan.md`, lista de decisões de
  implementação), e para cada item procurar no ADR o **vocabulário do item** — se o ADR não
  enuncia nada sobre ele, está aberto, mesmo que a lista "continua sendo decisão de ticket" o
  omita. Em TCK-0016 o item 7 (números do RNF-8) não aparecia em ADR nenhum: omissão da lista,
  não fechamento. E o inverso também existe: item que o ADR **decide** (fronteira ilha ×
  estático, `ADR-0007` item 6) sem estar na lista — aí confira `git diff` para saber se a
  absorção é do aceite ou já vinha do ticket que propôs o ADR. Absorção antiga não é defeito do
  ticket de aceite.
- **Diffar o ADR contra o `HEAD` é o que separa "o aceite decidiu" de "o aceite registrou".**
  `git diff -U0` dos dois ADRs mostrou hunks só em cabeçalho, item da pergunta respondida,
  "Estado no aceite" e o bloco de consequências novo — nenhum enunciado de mecanismo. Cada
  afirmação do bloco novo conferida com `git show HEAD:<adr> | grep -c` contra a contagem atual:
  incremento de 1 é **repetição** da regra no bloco, não regra nova.
- **Convenção nascida de sugestão não-bloqueante não vira critério.** Em TCK-0016 o produtor
  escreveu uma convenção de "emenda editorial" em `docs/adr/README.md` para atender ao `S2` do
  revisor; o `S5` apontou incoerência nela. Nenhum dos 8 critérios pedia a convenção — logo,
  incoerência ali é **dívida** e o QA **decide a leitura operativa** em vez de devolver.
  Reprovar seria renegociar critério depois da entrega (mesma família de "critério só se lê com
  o que estava escrito").
- **Antes de herdar o exemplo do revisor, construa o caso você mesmo.** O `S5` dizia que o vão
  entre as duas metades da regra era o `B4` do TCK-0003 ("KaTeX pré-renderizado") — mas aquele
  caso era justamente algo que o `ADR-0003` **não** decide, portanto permitido pelas duas
  metades. O vão é real, só que o caso é outro: **rótulo que contradiz a decisão do próprio
  ADR**. Diagnóstico certo, exemplo errado — e o exemplo é o que decide a redação da correção.
- **Direção do resíduo decide entre `REJECT` e dívida também em norma de processo.** Metade de
  regra **restritiva demais** produz excesso de cerimônia (`superseded` para consertar rótulo),
  não permissão indevida. Erro conservador = dívida com gatilho. Se fosse frouxa demais, seria
  L-021 e bloqueante.
- **Janela verde medida DEPOIS da última edição da cadeia paralela vale mais que a do revisor.**
  Em TCK-0016 rodei as três auditorias às 17:52 e de novo às 17:58; `.github/workflows/…` do
  TCK-0015 tinha mtime **17:49**, posterior ao sync deste ticket (17:43). Cruzar `stat -c '%y'`
  do artefato alheio com a hora da minha execução transforma "está verde agora" em "está verde
  depois do último movimento deles".
- **Carimbo de hora do `log.md` pode não ser o relógio do sistema.** Em TCK-0016 as entradas
  corriam ~1h à frente do mtime dos arquivos que elas descreviam. Registrar a divergência em vez
  de "corrigir" o relógio dos outros — e reforçar a leitura por `[SEQ]`.

- **A primeira validação com aplicação de verdade muda o que é evidência.** Até o TCK-0015 os
  tickets eram documentais; aqui a prova é `rm -rf dist .astro node_modules` → `npm ci` →
  `npm run build`, a árvore de `dist/` e o `grep` no HTML gerado. Regra que ficou: **fixture
  hostil roda em cópia isolada da árvore** (`tar` da raiz para o scratchpad + `npm ci`
  próprio), não no working tree compartilhado — e a cópia num caminho absoluto diferente vira,
  de graça, prova de portabilidade da build.
- **Conjunção × ordem não são a mesma afirmação.** `validate && audit` com `content/` vazio:
  trocar `&&` por `;` publica site vazio (exit 0); **inverter a ordem não abre nada** (o
  auditor sai 0, o validador roda em seguida e sai 2, o `&&` propaga). Produtor e revisor
  escreveram "a ordem é load-bearing"; medindo os quatro cenários, o que é load-bearing é a
  **conjunção**. Erro conservador em comentário = dívida de precisão, não defeito — mas só dá
  para dizer isso depois de rodar as duas ordens.
- **Caçar o vetor N+1 vale mais quando a resposta é "não há inversão".** Rodei 30 vetores meus
  contra o passo de terceiros e 17 passaram; o que decidiu a severidade não foi o número, foi
  rodar **o padrão anterior lado a lado**: o atual ganha em 6 formas de erro ordinário e nos 3
  casos legítimos que o antigo reprovava; o antigo ganha em 6 formas exóticas. **Nenhum é
  superconjunto do outro** — e a régua "a ferramenta mais estrita é a que aprova" (que tornou
  o B4 bloqueante) simplesmente não se aplica. Sem essa comparação eu teria herdado a
  severidade do loop anterior.
- **Classificar os próprios vetores inclui admitir os que não são vetor.** Dos 17 que passaram,
  3 eram expectativa minha errada (`download=`, `<html manifest>` appcache, `<applet archive>`
  — atributos que não buscam bytes ou removidos dos navegadores) e 2 marginais. Publicar os 17
  como "furos" inflaria o achado; publicar 7 com a classificação aberta é o que dá para o
  próximo agente trabalhar.
- **Dívida sem gatilho automático é a única que precisa de gatilho escrito.** No TCK-0015, 5 das
  7 formas novas chegam junto com o JavaScript, e aí o passo já está vermelho por outra dívida
  (A2) — a revisita é forçada por construção. As **duas** que não têm gatilho nenhum
  (`<link rel="manifest">`, que aprova hoje, e `report-uri` de CSP) foram as que ganharam
  gatilho nomeado. Antes de escrever gatilho para tudo, checar quais já são forçados.
- **O portão que verifica o artefato não vê o que o host injeta.** Critério "zero coleta no HTML
  publicado" fecha no `dist/`, mas Vercel Web Analytics e Speed Insights se ligam **no painel**
  e injetam script na borda sem mudança no repositório. Não é defeito do ticket (o artefato está
  limpo), é o limite do alcance da evidência — sai como `ACTION` com verificação **na URL
  pública**, não no build.
- **"Caso hostil não se aplica" tem prova barata quando há HTML.** Offline e recarregar no meio
  do exercício: `<script>`=0, `<form>`=0, `<input>`=0 e `grep -rIniE 'serviceworker|sw\.js|
  manifest|workbox|indexeddb' dist/` → exit 1. Formato decimal: nenhum número fracionário
  renderizado. Leitura de fórmula: nenhuma fórmula no HTML. Três `grep` substituem três
  parágrafos de justificativa.
- **A11y de página estática se mede sem navegador.** Contraste calculado dos tokens CSS nos
  **dois** temas (10 pares, mínimo 4,90:1), `viewport` sem `user-scalable=no`/`maximum-scale`,
  zero largura em `px`, contagem de focáveis + `tabindex` positivo/`autofocus`/`accesskey`,
  um `<h1>` por página, `alt` em 100% das imagens. E conferir se algum reset removeu o
  sublinhado do link: sem ele, cor de link a 1,56:1 do texto violaria 1.4.1 — com o sublinhado
  padrão do navegador, não viola.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0001 — verificar referências do nó piloto | **done** — 5/5 critérios com evidência própria, 0 defeitos; 3 dívidas aceitas (D-1 rastro de auditoria em `covers`, D-2 nota dentro de `license`, D-3 URL em `blob/master`) e sugestão de ticket de schema para `references.json` | L-006, L-007 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0002 — spec da fatia mínima de aprendizagem | `done` — 6/6 critérios com evidência própria; 2 `ACTION` encaminhadas ao `tech-lead` (lacuna de `*Leitura:*` no nó piloto; perguntas em aberto sem dono na spec) | L-001, L-003, L-008, L-011 |
| 2026-08-01 | TCK-0005 — descrições textuais das 8 fórmulas do nó piloto | **done** — 7/7 critérios com evidência própria (contagem + **ordem**, dupla prova de LaTeX intocado, leitura adversarial às cegas de 4/10 descrições, paridade por token, verificação numérica em `Fraction`), 0 defeitos; 7 pendências herdadas confirmadas fora do diff, 4 marcadas como condicionantes da saída de `draft` | L-012 (aplicada), L-014 (não bloqueante aqui) |
| 2026-08-01 | TCK-0003 — aceite do `ADR-0003` (stack da plataforma) | **done** — 6/6 critérios com evidência própria; validação documental (sem aplicação, casos hostis n/a e justificado); varredura própria da raiz = 186 ocorrências, só `.dev-loop/` (gitignorado), logs de ticket, `docs/specs/` e 7 pendências de área alheia; S6 julgada dívida `D-1`, não defeito; 4 `ACTION` ao `tech-lead` | L-010, L-011, L-013 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0004 — licença do projeto (CC BY-SA 4.0 conteúdo · MIT código), como `qa-validator#5` | **done** — 7/7 critérios com evidência própria; MIT conferida palavra a palavra contra o SPDX (169 vs 169, 0 diferenças), renumeração §9.6–9.8 com 49 referências classificadas e nenhuma quebrada, alcance da regra provado ferramenta a ferramenta; SG1 (ND) julgado **dívida**, não defeito; 4 dívidas + 5 pendências herdadas ao `tech-lead` | L-006, L-007, L-009, L-010 |
| 2026-08-01 | TCK-0012 — gatilho de handoff por esgotamento de contexto, como `qa-validator#6` | **done** — 12/12 critérios com evidência própria, 0 defeitos; validado com `.claude/settings.local.json` (gitignored) movido para fora; travessia sem configuração = 7 disparos em 4 faixas (B5 morto); matriz de 17 invocações `--hook` todas exit `0`; canário próprio em 7 posições, 0 vazamentos; suíte 93/0 em 5 ambientes; `PostToolBatch` **provado ativo** por efeito colateral; 5 dívidas aceitas (D-1 `WINDOW_TIERS` com gatilho, D-2 origem ambígua, D-3 alarmes falsos pré-refutação, D-4 dev-loop fantasma, D-5 allowlist do usuário) | L-015, L-016, L-017, L-018 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0013 — estados de tela da fatia mínima, como `qa-validator#7` | **REPROVADO** (loop 2/3) — 7 de 9 critérios com evidência própria (13/13 estados, 68 chaves sem buraco, foco × região viva classificados nos 13, Mermaid no parser, 2 buscas negativas, 2 auditorias exit 0); 2 defeitos: §9 aplica o teste de ambiguidade decimal só a en-US e o lado pt-BR marca `3.000` como correto para `answer: 3` (falso positivo em 2 de 2 itens `numeric` reais), e a enumeração do cartão do índice sobrevive no rótulo do Mermaid; 4 dívidas (D-1 frase absoluta de §3, D-2 `ADR-0007` `proposed`, D-3 E1 silencioso, D-4 `L-022` sem elos) | L-013, L-021 (violadas pela entrega), L-011 |
| 2026-08-01 | TCK-0011 — C4 Container + ADR-0006 (CI/CD) e ADR-0007 (esqueleto), como `qa-validator#9` | **done** — 10/10 critérios com evidência própria, 0 defeitos; 4 blocos Mermaid reparseados (`mermaid.parse`, 0 falhas), 28 elementos do C4 classificados um a um, 6/6 linhas de custo conferidas ao vivo nas 3 URLs (200), varredura da raiz com 26 arquivos citando os ADRs e nenhum como aceito; critério 10 fechado pela **janela verde observada** às 16:5x com todos os artefatos no lugar (o estado oscilou para vermelho às 17:1x por deriva do TCK-0006, atribuída e emendada em `[011] CORRECTION`); `package.json` intruso atribuído ao TCK-0015; 5 dívidas + 4 `ACTION` ao `tech-lead` | L-011, L-013, L-020 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0014 — validador do contrato de carga de `content/`, como `qa-validator#8` | **done** — 9/9 critérios com evidência própria; critério 1 provado com **21 violações de 21 regras distintas** numa execução; suíte 118/0 contada por fora em 4 ambientes (inclusive `env -i LC_ALL=POSIX PYTHONUTF8=0` meu); B1 reverificado com fixture de 2 níveis, B2 em 11 combinações de canal; 4 fixtures de burla → **7 falsos negativos**, todos fora do RF-18 enumerado e nenhum com o auditor mais estrito; 8 dívidas (D-1 overflow com gatilho, D-2 largura zero, D-5 `null` como arquivo ausente as 3 urgentes); 4 instâncias do defeito do `audit-content.py` reproduzidas; 3 pendências ao `tech-lead` | L-019 (adendo conferido), L-013, L-018 |
| 2026-08-01 | TCK-0013 — estados de tela da fatia mínima, loop 3 (aprovação), como `qa-validator#7` | **done** — 9/9 critérios com evidência própria no artefato de 893 linhas; defeito 1 morto por simulação refeita (**26 vetores × 2 idiomas × `qe-003`/`qe-005`, zero falsos positivos**, CA-6 e CA-7 preservados), defeito 2 confirmado pela varredura de `cartão` (7 ocorrências, 3 pontos, todos com remissão a (c)); D-1, D-2 e D-4 fechadas, D-3 aceita aberta, **D-5** (anúncio da recusa de formato) e **D-6** (espaço nas bordas) registradas com gatilho; (a) e (c) abertas ao `tech-lead` | L-013, L-021, L-022 (adendo) |
| 2026-08-01 | TCK-0006 — norma de leitura de fórmula e fronteira display × inline, como `qa-validator#10` | **done** — 9/9 critérios com evidência própria, 0 defeitos; teste **reimplementado do texto** e aplicado a **41 fórmulas** (23 reais que extraí + 18 da tabela + 8 fronteiras minhas) com **0 divergências**; inventário recontado por parser próprio (24 disparos − 2 já atendidos = **22 pontos**, idêntico a `[007]` §2); critério 9 fechado por **janela verde medida em cópia isolada** (deriva atribuída a `core.instructions.md` item 5 + `app.instructions.md` da cadeia do TCK-0015/0016, com cronologia por `stat`); padrão de busca (b)2 medido pior que o revisor (**2 de 5** exemplos do próprio documento) e aceito como dívida com gatilho; 6 dívidas + 7 `ACTION` ao `tech-lead` | L-012, L-013, L-021 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0016 — aceite dos `ADR-0006` (CI/CD) e `ADR-0007` (esqueleto), como `qa-validator#11` | **done** — 8/8 critérios com evidência própria, 0 defeitos; cruzamento **refeito** dos 7 itens de `plan.md:132-142` contra os dois ADRs (nenhum absorvido; o lugar do portão do RF-18 aberto em **9** pontos; RNF-8 ausente de todo ADR); varredura da raiz em 4 padrões (grafia alternativa = 5 linhas, todas históricas; `PROPOSTO (ADR-000[67])` = 0 fora de `tickets/`; 8 `PROPOSTO` restantes classificados; `EM ABERTO (ticket)` preservado 4+2+1+1); 5 blocos Mermaid reparseados (5/0); 3 comandos exit 0 medidos **duas vezes**, a segunda após a última edição do TCK-0015 (mtime 17:49 × sync 17:43); emenda do `ADR-0003` medida em +7/−2; julgamentos: (a) convenção de emenda editorial **decidida pela segunda metade**, dívida D-1, (b) estado não commitado do TCK-0006 confirmado (`HEAD`=0 × WT=1, 6 gerados de `core`), (c) 2 notas encaminhadas como `L-026`; 3 dívidas + 4 `ACTION` ao `tech-lead` | L-010, L-011, L-013, L-020, L-025 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0015 — esqueleto da aplicação e deploy (primeiro código executável), como `qa-validator#12` | **done** — 13/13 critérios com evidência própria do zero (`rm -rf dist .astro node_modules` → `npm ci` → `npm run build`), 0 defeitos; portão de bilinguismo fechado nas **duas** camadas e nas 4 fixtures (mono pt-BR/en-US × `published`/`draft` + teoria ausente): build ≠ 0, `dist/` inexistente, 0 HTML; portão de terceiros com **18/18 + 8/8 + 4/4** reproduzidos e **30 vetores meus** → 17 passam (7 novos e reais), julgados dívida por **ausência de inversão** medida contra o padrão do loop 1; `<base>` (A1) confirmado ponta a ponta via `public/`; job de CI inteiro 10/10 exit 0 no HEAD final `aee5d3d`; 3 dívidas com gatilho (D-1 conjunção × ordem, D-2 os 7 vetores, D-3 largura zero) + 4 `ACTION` (analytics do painel, 404 do produto, slug em caixa mista, proteção de branch) | L-019 (adendos 1–3), L-013, L-021 (aplicadas, não violadas) |
