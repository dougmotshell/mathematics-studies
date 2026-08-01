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

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0001 — verificar referências do nó piloto | **done** — 5/5 critérios com evidência própria, 0 defeitos; 3 dívidas aceitas (D-1 rastro de auditoria em `covers`, D-2 nota dentro de `license`, D-3 URL em `blob/master`) e sugestão de ticket de schema para `references.json` | L-006, L-007 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0002 — spec da fatia mínima de aprendizagem | `done` — 6/6 critérios com evidência própria; 2 `ACTION` encaminhadas ao `tech-lead` (lacuna de `*Leitura:*` no nó piloto; perguntas em aberto sem dono na spec) | L-001, L-003, L-008, L-011 |
| 2026-08-01 | TCK-0005 — descrições textuais das 8 fórmulas do nó piloto | **done** — 7/7 critérios com evidência própria (contagem + **ordem**, dupla prova de LaTeX intocado, leitura adversarial às cegas de 4/10 descrições, paridade por token, verificação numérica em `Fraction`), 0 defeitos; 7 pendências herdadas confirmadas fora do diff, 4 marcadas como condicionantes da saída de `draft` | L-012 (aplicada), L-014 (não bloqueante aqui) |
| 2026-08-01 | TCK-0003 — aceite do `ADR-0003` (stack da plataforma) | **done** — 6/6 critérios com evidência própria; validação documental (sem aplicação, casos hostis n/a e justificado); varredura própria da raiz = 186 ocorrências, só `.dev-loop/` (gitignorado), logs de ticket, `docs/specs/` e 7 pendências de área alheia; S6 julgada dívida `D-1`, não defeito; 4 `ACTION` ao `tech-lead` | L-010, L-011, L-013 (aplicadas, não violadas) |
| 2026-08-01 | TCK-0004 — licença do projeto (CC BY-SA 4.0 conteúdo · MIT código), como `qa-validator#5` | **done** — 7/7 critérios com evidência própria; MIT conferida palavra a palavra contra o SPDX (169 vs 169, 0 diferenças), renumeração §9.6–9.8 com 49 referências classificadas e nenhuma quebrada, alcance da regra provado ferramenta a ferramenta; SG1 (ND) julgado **dívida**, não defeito; 4 dívidas + 5 pendências herdadas ao `tech-lead` | L-006, L-007, L-009, L-010 |
