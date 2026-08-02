# Memória do agente `code-reviewer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Revisa o diff de um ticket como terceiro — correção, segurança, acessibilidade, performance, convenções e testes — aprovando para QA ou devolvendo com defeitos numerados. Usar após toda implementação.

## Notas persistentes

- **Afirmação de licença em `references.json` se reverifica, não se aceita.** O log do
  produtor não é evidência; a evidência é a fonte. Receita usada no TCK-0001:
  `curl -sSL <url> | grep -o '"license":{[^}]*}'` (OpenStax embute o bloco no HTML);
  para PDF, `pdftotext -f N -l N` no colofão e `pdftoppm -f N -l N -png` + leitura da
  imagem quando o selo de licença é figura (foi assim que confirmei o selo BY-SA sem NC
  do Livro Aberto, divergente do site do projeto). Ver L-006 e L-007.
- **Verificar `covers` por ocorrência no material**, não por plausibilidade: contar os
  termos declarados no HTML da seção / achar a página impressa citada no PDF.
- **`audit-content.sh` verde não é revisão.** Ele só checa **presença** de
  `author/year/url/language/license`; não valida URL, vocabulário de licença nem o texto de
  `covers`. Critério "audit verde" nunca substitui os demais.
- **Escopo do diff se prova com `git diff --stat -- <área>`**, não com a afirmação
  "não toquei em nada mais". No TCK-0001 o working tree tinha mudanças de 3 outros tickets
  em paralelo — filtrar por caminho antes de concluir qualquer coisa sobre escopo.
- **Fonte NC (CC BY-NC-SA) pode ser citada, não incorporada** — o projeto é conteúdo
  CC BY-SA 4.0 · código MIT (decisão de 2026-08-01, TCK-0004). Ao revisar um nó que cite
  fonte NC, checar sinal de adaptação (`grep -ri 'adaptado|based on|<fonte>'` no nó +
  leitura da teoria contra a estrutura da fonte). Incorporar material NC = bloqueante.
- **Índice de lições:** conferir `grep '^\*\*ID:\*\*' memory/lessons/` (colisão de L-NNN)
  e se a lição está na seção de `LESSONS.md` correspondente ao seu `Tipo:`.
- **Revisão de spec é revisão de fidelidade à fonte.** Havendo `.dev-loop/<slug>/requirements.md`,
  conferir RF/RNF/estados/CA por diff normalizado (regex + `re.sub(r'\s+',' ')`) em vez de
  leitura corrida: expõe requisito alterado em silêncio e prova a contagem no log.
- **Independência de stack se prova por busca negativa:**
  `grep -nEi 'react|vue|svelte|astro|next|vite|vercel|indexeddb|service worker|playwright|jest|vitest|tailwind'`
  no `spec.md` — casamento fora de uma seção *fora de escopo* é defeito. O `plan.md` pode
  citar o ADR como direção, nunca escolher biblioteca (TCK-0002).
- **Bater a spec contra o dado real:** ler `exercises.json`/`meta.json` com Python e conferir
  ids, `tolerance: 0`, `unit: null`, contagem de `hints[]` e `feedback` em toda opção. Campo
  descrito que não existe — ou campo existente ignorado — é defeito.
- **Delta justificado ≠ infidelidade.** Trocar "a definir no aceite do ADR" por "a definir na
  implementação" depois do ADR aceito é correção; citar uma lição (`L-008`) é melhoria.
  Registrar ambos no log em vez de reprovar.
- **Aprovar não é silenciar:** sugestão não bloqueante vai numerada no `HANDOFF`, com
  arquivo:linha, para o `qa-validator` decidir se vira dívida registrada.
- **Pergunta em aberto sem dono trava aprovação.** Quando o revisor não pode reescrever o
  artefato, adiar explicitamente no log (dono + prazo) satisfaz o critério sem editá-lo.
- **Formato de saída:** `docs/ai/ticket-protocol.md` (HANDOFF/REJECT) e
  `.claude/skills/dev-loop/references/briefing-template.md` — briefing de review exige a
  seção `## Veredito` e no máximo 40 linhas não vazias.
- **ADR aceito só desbloqueia de verdade quando a regra operativa muda.** Ao revisar o aceite de
  um ADR, `grep -rn "ADR-NNNN" AGENTS.md docs/ memory/ .claude/ .github/` — `docs/adr/README.md`
  e `memory/context/` são a parte fácil; o que governa comportamento é `AGENTS.md` (§1 e §11) e
  `.github/instructions/*.instructions.md` (checar o `applyTo`). Regra que ainda diz `proposed`
  depois do aceite é defeito bloqueante, não pendência estética (TCK-0003, B1).
- **Editar `AGENTS.md` e `docs/` não exige sync; `.github/instructions/` e `.claude/agents|skills/`
  exigem** `python3 scripts/sync-ai-adapters.py` (são fontes canônicas). Usar isso para derrubar o
  argumento "é ticket separado por causa do sync" — o sync é determinístico e o
  `audit-ai-surface.sh` já o verifica (`--check` = `up-to-date`).
- **ADR que decide × ADR que implementa:** procurar na seção Consequências verbos de execução
  ("pré-renderizado na build", "cacheado em", "via biblioteca X"). Cruzar com o `plan.md`/`tasks.md`
  da spec relacionada: se lá o item está listado como "decisão de implementação a tomar nos
  tickets", o ADR fechou o que não era dele fechar (TCK-0003, B2).
- **Artefato alterado e não listado no `HANDOFF` é defeito** (AGENTS.md §10, regra 2). Conferir a
  lista de artefatos do handoff contra o `git status`, e usar `stat -c '%y %n'` + `grep -rn <arquivo>
  tickets/*/log.md` para separar o que é de tickets paralelos do que ninguém declarou.
- **O working tree muda durante a review.** Em 2026-08-01 três tickets escreviam junto: reler o
  arquivo antes de citar linha e refazer `git status` no fim (um `ADR-0005` apareceu no meio da
  minha revisão do TCK-0003).

- **Decisão aceita que não chega ao `AGENTS.md` é decisão inerte.** `AGENTS.md` e
  `.github/instructions/` são o que as 12 ferramentas carregam sozinhas; `docs/` não é
  carregado por nenhuma. Ticket que cria regra normativa (licença, stack, processo) só está
  pronto quando a regra está lá — verificar com
  `grep -n -i '<tema>' AGENTS.md .github/instructions/*.md`. Se a fonte canônica contradiz o
  ADR recém-aceito, é bloqueante (TCK-0003 B1 e TCK-0004 B1, mesmo padrão no mesmo dia).
- **Texto de licença se confere por diff mecânico, não por leitura.** Receita: baixar o
  canônico (`https://raw.githubusercontent.com/spdx/license-list-data/main/text/<ID>.txt` e
  o corpo da página da OSI), normalizar espaços, aspas tipográficas e o placeholder de
  titular, e comparar palavra a palavra em Python (`difflib`). Evidência = contagem de
  palavras nos dois lados + zero diferenças. MIT canônica tem **169 palavras**.
- **Paridade bilíngue se mede:** número e ordem das seções, contagem de palavras por idioma,
  ocorrências da URL canônica e presença dos mesmos elementos normativos em cada lado.
- **Mermaid se valida com o parser, não a olho:** `npm i mermaid@11 jsdom` no scratchpad +
  `mermaid.parse()` em cada bloco ```mermaid``` do diff.
- **Working tree compartilhado:** antes de acusar escopo, cruzar o `git diff` com o `log.md`
  dos tickets paralelos — em 2026-08-01 quatro tickets escreviam nos mesmos índices
  (`docs/adr/README.md`, `memory/context/project-context.md`) sem colidir.
- **Correção de REJECT não termina no texto: conferir o diagrama.** No TCK-0003 o produtor
  corrigiu a prosa do ADR ("este ADR não decide build × runtime") e deixou o rótulo do nó Mermaid
  dizendo "KaTeX pré-renderizado". Mermaid é parte normativa do documento (`docs/DOC-STANDARDS.md`)
  — na re-revisão, reler o diagrama contra cada frase corrigida.
- **Repetição de erro que virou lição na própria entrega é bloqueante** (AGENTS.md §10, regra 7).
  Vale inclusive quando a lição foi criada no mesmo `ACTION` que se está revisando.
- **Verificar sync sem confiar no "rodei o sync".** `python3 scripts/sync-ai-adapters.py --check`
  (exit 0) + `git diff` dos gerados lado a lado com a fonte: o risco real é o gerado afirmar algo
  que a fonte não diz, e `--check` sozinho não mostra isso.
- **Ao aprovar remoção de uma regra, checar o que estava colado nela.** Em `AGENTS.md` §11,
  `core`/`app.instructions.md` e `prompts/bootstrap-session.md`, "não assumir stack" divide o item
  com "nenhuma implementação sem spec aprovada" — pedir a preservação literal e depois conferir
  com `grep -rn "spec aprovada"` nas fontes **e** nos gerados.
- **Varredura de aceite de ADR se faz da raiz**: `grep -rn "ADR-NNNN" . --exclude-dir=.git`.
  Ocorrências legítimas que sobram: `.dev-loop/**` (gitignorado), logs de ticket (histórico
  append-only) e artefatos de tickets paralelos. Tudo o mais é defeito ou pendência nominal.
- **`CORRECTION` é a forma certa de emendar log publicado** (`docs/ai/ticket-protocol.md:173-181`).
  Cobrar os rótulos do template ("O que estava errado:" / "Registro correto:") como sugestão, não
  como bloqueante, se a entrada citar o `[SEQ]` original e trouxer evidência.
- **`Lição: n/a — erro pontual` é aceitável** quando o defeito é descumprimento de regra já
  escrita e não existe lição prévia sobre ele (senão vira regra 7). Exigir que a prevenção
  apareça em algum lugar verificável — checklist na memória do agente serve.
- **Regra 7 (repetir erro com lição registrada = bloqueante) exige checar a cronologia.** Se a
  ocorrência é texto **anterior** à lição, que sobreviveu a uma correção parcial, não é
  repetição — é correção incompleta, e a sanção é o `REJECT` daquele loop, não uma segunda
  cobrança. Verificar com os próprios logs anteriores (no TCK-0003 meu `[006]` provou que o
  rótulo do Mermaid já existia antes da L-011).
- **Lição nova × racionalização:** aceitar quando o "Como aplicar" for executável e diferente do
  da lição vizinha (L-011 = *o que* não escrever; L-013 = *método* de varrer a classe do defeito)
  e quando ela **referenciar** a anterior em vez de reescrevê-la (`memory/LESSONS.md:21`).
- **Produtor que corrige além da linha citada não está fora de escopo** se for a mesma classe do
  defeito, no mesmo artefato, e declarar a edição no log com opção de rollback. Cobrar a letra do
  REJECT aqui seria preferência, não defeito — e contraria a própria lição que se exigiu.
- **Auditoria vermelha nem sempre é do ticket em revisão.** Teste de atribuição em working tree
  compartilhado: `grep -c <termo-do-meu-diff>` e `grep -c <termo-do-diff-alheio>` nos gerados —
  se o meu já está lá e o alheio não, a deriva é do outro. Reexecutar antes do veredito: no
  TCK-0003 a auditoria estava vermelha no `[011]` e verde 10 min depois, sem ação do produtor.
- **Refazer a varredura do defeito antigo a cada loop:** agentes paralelos criam ocorrências
  novas. No loop 3 do TCK-0003 apareceu `memory/agents/a11y-ux-reviewer.md:56` com
  `ADR-0003 proposed`, escrita depois da varredura do produtor — pendência nova, não defeito.
- **Distinção sutil que quase passa:** "HTML pré-renderizado" (página, decidido pela stack) ×
  "KaTeX pré-renderizado" (momento de renderização da fórmula, não decidido). Ao revisar um ADR
  de site estático, separar o sujeito de cada afirmação antes de chamá-la de mecanismo.

- **Regra que renumera seção do `AGENTS.md` exige varredura de referências cruzadas.**
  `grep -rn "§9\.[0-9]" . --exclude-dir=.git` + a variante sem `§` (`AGENTS.md.*9\.[6-8]`,
  `seção 9.x`). Conferir uma a uma: uma citação pode continuar *sintaticamente* válida e
  passar a apontar para outra regra. No TCK-0004 foram 30 ocorrências, todas resolvendo
  certo — mas por sorte de numeração, não por checagem prevista pelo autor.
- **"Propaguei para os gerados" se prova com inclusão linha a linha**, não com
  `sync --check`: script curto em Python conferindo que cada linha da fonte
  (`.github/instructions/<x>.instructions.md`) aparece no gerado (`.cursor/rules/*.mdc`,
  `.windsurf/rules/*`, `.agents/rules/*`, `.rules`, `.clinerules`, `.junie/guidelines.md`).
  Já os adapters de **agent** (`.github/chatmodes/`, `.gemini/commands/`, `.claude/commands/`)
  são ponteiros de ~25 linhas para `.claude/agents/<nome>.md` — a mudança chega por
  referência; procurar o texto da regra dentro deles dá falso negativo.
- **Afirmação jurídica se checa no legalcode.** CC BY-SA 3.0 §4(b)(ii) permite distribuir
  a adaptação sob "a later version of this License with the same License Elements" — logo
  BY-SA 1.0–3.0 → BY-SA 4.0 é legítimo, e a regra "CC BY-SA = adaptável" não tem furo de
  versão. Cuidado com o inverso do viés usual: erro **conservador** (classificar ND como
  "só citável" quando ND permite redistribuição verbatim) não é bloqueante — anotar como
  precisão, porque bloquear entrega segura em loop 2/3 é desproporcional.
- **Aprovar loop 2 não é reabrir o loop 1:** reconferir só o que a correção pôde quebrar
  (aqui: MIT literal, paridade do `LICENSE-CONTENT` depois da S3, Mermaid, escopo) e listar
  o restante como já verificado no `[007]`.

- **Ferramenta de observação: o modo de falha caro é o silêncio, não a exceção.** Ao revisar
  um watcher/gatilho, perguntar "qual valor default faz este tool nunca falar?" — no TCK-0012
  o mapa `DEFAULT_WINDOWS` casava um id de modelo *comprovadamente ambíguo* com a **maior**
  janela (1M), e a mensagem do hook não tinha ramo para `confiavel: false`: contexto cheio
  viraria "20% VERDE" e o aviso jamais sairia. Regra: quando um valor é presumido, o default
  tem de errar para o lado de avisar cedo, e o **caminho automático** (não só a saída
  interativa) precisa comunicar a incerteza. Aviso que só existe em `--json` ou em texto que
  ninguém roda não existe.
- **Invariante de exit code se testa nas bordas de I/O, não só nas de entrada.** "Hook sai 0
  sempre" costuma ser verdade para stdin inválido/vazio, `HOME` inexistente, diretório de
  estado sem escrita e arquivo corrompido — e falso quando o **stdout** falha:
  `cmd --hook | true` (BrokenPipe) e `cmd --hook > /dev/full` devolveram **120** no TCK-0012,
  porque a exceção acontece no flush do interpretador, fora do `try`. Receita de revisão:
  rodar os dois, e conferir se o `except BrokenPipeError` de nível de módulo não sai com
  código ≠ 0 também.
- **Suíte hermética se prova com `HOME` sintético, não com `env -i`.** `env -i` limpa o
  ambiente mas mantém o `HOME` real via `pwd`; o teste do TCK-0012 lia
  `~/.claude/settings.json` e quebrava (`40/1`) num `HOME` que continha justamente a
  configuração que a documentação do próprio ticket recomenda. Receita:
  `env HOME=<tmp-com-a-config-recomendada> bash <suite>`. CI verde não prova hermeticidade —
  prova só que o runner é pobre.
- **Privacidade se audita pelos caminhos de erro e pelos campos ecoados.** Checklist que usei:
  (1) `grep -nE 'urllib|requests|socket|http|subprocess|os\.system|popen'`; (2) toda mensagem
  de exceção — exigir `exc.strerror`/`type(exc).__name__`, nunca `str(exc)` nem a linha lida;
  (3) todo campo do arquivo que chega ao stdout (aqui `model` e `timestamp`) — fuzz com a
  string-canário **nesses campos**, não só no corpo da mensagem. A suíte do produtor punha o
  canário só em `content`, que o parser nunca toca: asserção que não podia falhar.
- **"Diff 100% inserção" não é sinônimo de "bloco preservado".** No TCK-0012 duas entradas
  novas entraram **dentro** de `permissions.allow` (15 → 17) auto-concedendo aprovação aos
  comandos do próprio ticket, e o log dizia "`permissions` preservado". Prova mecânica:
  `git show HEAD:<arquivo> | jq -r '.<bloco>[]'` × o working tree, e `diff` das duas listas.
  Mudança em bloco de permissão exige declaração explícita no log, mesmo quando é benigna.

- **Alarme que satura no topo da escala é silêncio com ruído no começo.** Ao revisar uma
  correção de "falso verde" para "presunção conservadora", medir o que acontece **depois** do
  primeiro aviso: se a zona pina no índice máximo, a condição `zona > anterior` nunca mais é
  verdadeira e o mecanismo morre pelo resto da sessão. No TCK-0012 (loop 2) a sessão de 1M não
  configurada recebia um `CRITICO` falso a 36% de uso real e **nenhum** aviso depois — mesmo
  destino do defeito reprovado no loop 1. Receita: rodar o hook 3× com o estado zerado e ler o
  arquivo de estado (`zone_index`, `window_warned`).
- **Presunção refutada pela própria medição não é conservadorismo, é erro.** `usado > janela
  presumida` prova que a presunção está errada; imprimir "181,3% (362.593/200.000)" é um número
  autorrefutável. Ao revisar qualquer heurística com limite adivinhado, procurar o caso em que
  o dado observado é **incompatível** com o palpite e exigir uma das duas saídas: declarar "não
  sei" (exit de sem-telemetria) ou escalonar **com** a ressalva obrigatória no canal automático.
- **Configuração do operador não conserta ferramenta desonesta no default** — e ainda pode
  piorar: variável declarada no comando do hook em arquivo versionado (a) vale só para o hook,
  criando divergência com o terminal e com o artefato gerado, e (b) marca o palpite como
  `confiavel: true`, desligando a ressalva. Procurar o arquivo per-máquina já suportado e
  gitignorado (aqui `.claude/settings.local.json`, lido primeiro por `resolve_window`) antes de
  aceitar hardcode em config compartilhada.
- **Correção de exit code se reverifica com o fd fechado, não só com o pipe quebrado.**
  `>&-` faz `sys.stdout` virar `None`: `except (BrokenPipeError, OSError, ValueError)` não pega
  `AttributeError`. E conferir **onde** o flush final é chamado — se está fora do
  `try/except BaseException`, a garantia "nada escapa" é falsa por construção. Baseline útil:
  `python3 -c 'print("x")' >&-` sai `0`; script que sai `1` está pior que o interpretador nu.
- **Suíte pode fixar o defeito que se está contestando.** Antes de exigir mudança de
  comportamento, `grep` na suíte pela asserção que protege o comportamento atual e citá-la no
  REJECT (no TCK-0012, `context-watch-test.sh:196` esperava exit `30` justamente no caso
  refutado) — senão o produtor corrige o código e a suíte reprova a correção.
- **Recusa de sugestão se julga com medida própria, não com a do produtor.** S3 (leitura
  reversa do transcript) foi recusada com "1,6 MB → 0,03 s"; gerei 51 MB sintéticos e medi
  `0,24 s` com RSS constante — a recusa se sustentava, e a evidência do revisor é o que fecha
  o assunto.

- **A prova de que um monitor "voltou a viver" é a sequência, não a medida.** Aprovar a
  correção de um alarme exige encenar a sessão inteira com transcripts sintéticos crescentes
  e estado zerado, e ver o disparo em **cada** faixa (no TCK-0012: 650k→ATENCAO, 780k→PREPARAR,
  900k→CRITICO). Uma medição isolada não distingue "corrigido" de "mudou de número".
  Complementar com a travessia da fronteira que muda a régua (199.999 · 200.000 · 200.001):
  é ali que se vê se o estado rearma ou se o mecanismo pina.
- **Refutação por medida é um argumento válido contra a saída que eu mesmo propus.** Se o dado
  observado é limite inferior verificado do limite desconhecido, exigir "declare não sei"
  (exit de sem-telemetria) cega a ferramenta justamente na faixa que ela existe para cobrir.
  Aceitar a alternativa do produtor quando ela preserva o critério **e** o resultado; a
  condição é a incerteza continuar declarada no canal automático — verificar isso rodando o
  hook, não lendo o código.
- **Exit ≠ 0 do shell não é exit ≠ 0 do script.** `> arquivo-sem-permissão` e `> diretório`
  devolvem `1` porque o **bash** falha ao abrir o redirecionamento (prefixo `bash: line 1:`) e
  o interpretador nem executa. Antes de contar como defeito, conferir o prefixo da mensagem e
  comparar com o baseline (`python3 -c 'print(1)' >&-` → `0`).
- **Suíte reescrita: conferir se a substituição não trocou cobertura por conveniência.**
  Receita: `grep -c` da asserção antiga (tem de ser 0), `grep` das novas por nome, e confirmar
  que o comportamento **aprovado** continua exercido com fixture que o satisfaz (no TCK-0012 a
  presunção conservadora migrou para 150k/200k → exit 20). Asserção que é a negação literal da
  linha do REJECT costuma fixar a decisão contestada.
- **Artefato gitignored é ponto cego do QA.** `.claude/settings.local.json` não aparece no
  `git status`: ao aprovar, declarar no HANDOFF que ele existe, o que contém e que a validação
  deve ser feita **com ele fora**. O mesmo vale para qualquer estado em `~/.local/state`.
- **Lição nova × duplicata (2ª aplicação):** L-018 passou porque cita L-013 e acrescenta um
  passo distinto (varrer o artefato × encenar a promessa do começo ao fim). O teste é o "Como
  aplicar": se ele instrui uma ação que a lição anterior não instrui, não é duplicata.

- **Revisão de artefato de desenho: a prova é o cruzamento mecânico, não a leitura.** Extrair a
  tabela de estados da spec com regex e casar 1 a 1 com os cabeçalhos do desenho (contexto, nome
  e ordem) — no TCK-0013 provou 13/13 e provou também que a tela extra ("índice") realmente não
  está na tabela da spec, refutando a hipótese "perdeu um estado e compensou com outro".
- **Paridade bilíngue de catálogo de UI se mede com script:** casar linhas `| \`chave\` |` para
  achar célula vazia ou idêntica, e cruzar as chaves citadas na prosa com as definidas em tabela
  (chave citada e não definida = string sem idioma). 69 chaves conferidas em segundos.
- **Regra de a11y que o próprio documento fixa é critério de revisão.** Quando o autor declara
  "mover foco OU anunciar, nunca os dois", varrer os treze estados atrás da conjunção proibida:
  no TCK-0013 três estados faziam os dois (E2 carga inicial, E5 via `retry`, E10 sem navegação).
  Região viva educada é descartada/embaralhada quando o foco muda — o texto "declarado como
  anunciado" pode nunca ser ouvido, e aí o critério "declara o que é anunciado" não está atendido.
- **Região viva cujo escopo é a seção inteira anuncia o conteúdo inserido, não um "pronto".**
  `aria-busy` comutado para falso despeja a fila. Ao revisar estado de carregamento, comparar o
  **escopo** declarado da região com a promessa de "sem mensagem adicional": se o escopo é a
  seção, a promessa é falsa por construção.
- **Escolha disfarçada mora na enumeração exaustiva.** Um documento pode listar as alternativas
  numa seção "decisões adiadas" e, ao mesmo tempo, fechar uma delas ao descrever a tela: no
  TCK-0013 §5 enumerava exatamente o que o cartão do índice mostra, sem o rótulo de rascunho e
  sem remissão à decisão (c) — isso é C2 implementado. Teste: para cada decisão aberta, procurar
  a tela onde ela se manifesta e checar se há remissão explícita à seção da decisão.
- **Contradição perigosa é a que está nos "princípios", não nos detalhes.** §2 do TCK-0013 dizia
  que o estado do exercício "morre ... inclusive na alternância de idioma", contra CA-3 e §10.1.
  Quem implementa lê os princípios primeiro. Ler a seção de princípios de um desenho **depois**
  de conhecer os CA, procurando a frase que os nega.
- **Diretório novo em `docs/` tem índice.** `docs/README.md` lista as pastas e `AGENTS.md` §4
  também: criar `docs/<area>/` sem entrar nos dois é defeito de convenção, barato de corrigir.

- **Portão de conteúdo: revisar a DESCOBERTA antes das regras.** A pergunta que expõe o falso
  negativo caro é "qual caminho de entrada faz o objeto nem chegar à primeira regra?". No
  TCK-0014 o `find_nodes` fazia `if any(marker exists): return [scope]` — apontar para um
  tópico que contém subtópico devolvia `Contrato íntegro: 1 nó` com 8 violações no disco.
  Receita: fixture com **nó dentro de nó**, rodar com alvo = pai, alvo = raiz e a ferramenta
  irmã no mesmo caminho; três resultados diferentes = defeito.
- **Duas ferramentas sobre o mesmo acervo: comparar por medição, não pelo cabeçalho.** Copiar
  os dois scripts para um repo sintético (`scratch/fakerepo/{scripts,content}` — as constantes
  `REPO_ROOT`/`CONTENT` passam a apontar para lá) e rodar as duas na MESMA fixture mutada.
  Foi assim que confirmei `"correct": "false"` passando no `audit-content.py` (veracidade
  implícita, `:229`/`:240`) e achei a segunda divergência que ninguém tinha visto
  (`title.en-US: 5` — `str(5).strip()` em `:85` aprova, o validador reprova). Cabeçalho que
  diz "não duplicado aqui" costuma estar errado: conferir regra a regra com `grep` nos dois.
- **Divergência entre ferramentas: o que importa é a DIREÇÃO.** Ferramenta estrita mais
  rígida que a lassa = seguro (registrar como achado para ticket próprio). Ferramenta estrita
  **aprovando** o que a lassa reprova = bloqueante, porque o portão é o que vai para o CI.
- **Exit code: cobrir stdout E stderr.** Corrigir só o stdout é meia correção. Matriz que uso:
  `{violação, íntegro, erro de uso} × {| head, | true, >&-, > /dev/full, 2>&1 | true,
  2>/dev/full, 2>&-} × {padrão, --json, --quiet}`. No TCK-0014 o caminho de conteúdo estava
  100% (12/12) e o de **uso** virava `120` em 4 combinações, porque as mensagens de uso usam
  `print(file=sys.stderr)` fora do `emit()` e o flush final só cobre `sys.stdout`.
- **Premissa "embutida" se checa no código, não no log.** O produtor declarou ter assumido
  `tolerance` absoluta; `grep -n tolerance` mostrou que a única checagem é `número finito ≥ 0`
  — idêntica nas duas leituras. Logo não há premissa embutida, só registro exagerado
  (sugestão), e a decisão de contrato só precisa existir antes da task que compara resposta.
  Regra geral: "assumi X" só vira defeito se existir um ramo de código que muda com X.
- **`emit()` genérico engole `UnicodeEncodeError`** (subclasse de `ValueError`) — com stdout
  ASCII o portão sai `1` sem imprimir nada. Testar com
  `PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=POSIX` sempre que a mensagem for em pt-BR.
- **Contar violações por TIPO, não por unidade.** "Lista as 7" não prova o critério "todas" se
  as 7 forem a mesma regra. Fixture própria com defeitos de famílias diferentes e
  `grep -oE '\[[A-Z0-9-]+\]' | sort -u | wc -l` fecha a conta (no TCK-0014: 18 violações,
  17 regras distintas).
- **Frase errada no cabeçalho que já virou `memory/context/`** é mais grave que no código:
  o código o próximo agente lê, a memória ele **acredita**. Ao reprovar por documentação
  interna, cobrar a correção nos dois lugares na mesma devolução.

- **Régua de ADR × ticket se testa contra a lista de decisões adiadas da spec, não contra a
  prosa do ADR.** No TCK-0011 o produtor escreveu a régua certa (L-020: "se eu trocar isto em
  seis meses, quem quebra?") e a aplicou bem em quase tudo — e o furo apareceu exatamente onde
  `docs/specs/<slug>/plan.md` tem a seção "Decisões de implementação a tomar nos tickets":
  o item 5 ("onde roda a validação do RF-18") estava fechado no ADR como `prebuild`. Receita:
  extrair essa lista numerada do `plan.md` e passar cada item por `grep` no ADR novo. É a
  versão mecânica do B2 do TCK-0003 e acha em segundos o que a leitura corrida perdoa.
- **Três marcadores obrigam a checar os dois excessos.** Convenção "sem marcador = decidido em
  ADR aceito · `PROPOSTO (ADR-N)` · `EM ABERTO (ticket)`": varrer **relação por relação**, não
  só nó por nó — no TCK-0011 os nós estavam certos e o furo era um `Rel(...)` sem marcador
  entre dois vizinhos marcados (`:42` e `:46` marcados, `:44` não). E procurar o inverso:
  container que **existe hoje** rotulado `PROPOSTO` inteiro (o workflow do repositório) é
  desenho ≠ realidade na direção contrária, e é o mesmo defeito.
- **Contradição entre dois ADRs da mesma entrega é evidência barata e forte.** Quando um ADR
  condiciona uma consequência ("é hipótese, não fato") e o irmão afirma a gêmea sem a
  condicional, não é questão de gosto — é um dos dois estar errado. Comparar as seções
  Consequências dos ADRs entregues juntos, procurando o mesmo enunciado com e sem ressalva.
- **Custo zero se reverifica na fonte, e a condição de elegibilidade importa mais que o
  número.** No TCK-0011 conferi verbatim as frases do GitHub ("free … for public repositories
  that use standard GitHub-hosted runners") e da Vercel ("does not support connecting a project
  on your Hobby team to Git repositories owned by Git organizations"; "non-commercial, personal
  use only"; "no billing cycles … wait until 30 days"), mais `gh repo view --json
  isPrivate,visibility,owner`. Receita de extração: `curl -sL <url> | python3 -c` com
  `re.sub(r'<[^>]+>',' ')` + `html.unescape` + `re.sub(r'\s+',' ')` e regex de janela
  (`.{80}<termo>.{160}`). Número que não está na página citada vira sugestão de precisão.
- **Decisão do usuário que chega depois da entrega não é defeito do produtor** — mas muda o que
  o ticket precisa registrar. Separar no REJECT: (a) o que ele errou, (b) o que o ticket de
  aceite tem de fazer, (c) o que **não** deve ser antecipado no loop de correção. Apagar a
  alternativa de um diagrama antes de o ADR virar `accepted` recria o desacordo desenho ×
  realidade que o ticket veio consertar.

- **Norma nova se revisa aplicando-a ao artefato, não lendo a redação.** No TCK-0006 o
  produtor publicou um teste mecânico (argumento composto) e um inventário do passivo; extraí
  as inline dos três arquivos do nó com script (`$…$` fora de `$$…$$`), apliquei o teste por
  conta própria e o confronto achou os dois defeitos: uma ocorrência não listada
  (`(x+3)^2`, `exercises.json:224`) e um total que contradizia a tabela do próprio log
  (4 EXIGE por idioma × 2 = 8, declarado 6). **Recontar o total declarado a partir das linhas
  da tabela é verificação de 30 segundos que quase sempre paga.**
- **Regra de a11y: perguntar qual caso simétrico a norma cita na justificativa mas não julga.**
  `(-5)^2` disparava; `-5^2`, citado como motivo do gatilho, ficava sem veredito — e é o caso
  em que as duas leituras dão números diferentes. Norma que nomeia um caso para se justificar
  tem de dar veredito a ele.
- **Propagação de regra se confere pelo agente que escreve o arquivo que a regra passou a
  reger**, não pela lista de arquivos tocados: a regra do TCK-0006 alcançou `exercises.json`,
  mas `exercise-designer` e `/new-exercise-set` ficaram sem uma linha (`grep -n
  "display\|acessib\|leitura"` → 0). L-009/L-010/L-021.
- **Adapter de agent e de skill é ponteiro; só regra é embutida.** Confirmado no TCK-0006:
  `.claude/commands/<agent>.md` e `.github/chatmodes/*.chatmode.md` só remetem a
  `.claude/agents/<agent>.md`. Consequência para revisão de escopo de sync: edição de agent
  **não** deve aparecer em gerado; se aparecer, algo alheio foi arrastado.
- **Mermaid dá para validar mesmo sem MCP de navegador:** `npx -y -p mermaid@11 -p jsdom node
  --input-type=module` com `global.window`/`global.document` do JSDOM (não sobrescrever
  `navigator`, é getter-only no Node 24) e `await mermaid.parse(txt)`.

- **Troca de canal é correção legítima, não escapatória.** Quando o REJECT proíbe "mover foco
  **e** anunciar", a saída boa não é apagar a informação: é fazê-la viajar com o destino do
  foco (descrição acessível do elemento que o recebe). No TCK-0013 o `exercise.retry-notice`
  migrou de região viva para descrição da área de resposta — e o desenho ainda removia a
  descrição depois da nova submissão, para não repeti-la em toda visita. Aprovar isso exige
  checar as duas pontas: a informação continua dita **e** não vira ruído permanente.
- **Esvaziar região viva não fala.** `aria-relevant` padrão é `additions text`: remoção não é
  anunciada. Serve para validar promessas do tipo "nada é falado no fim" sem leitor de tela.
- **Regra absoluta na seção estrutural × tabela que a desmente.** "Nenhuma região viva envolve
  conteúdo" convive mal com uma tabela cujo escopo declarado inclui `feedback[lang]` e o texto
  das dicas — que a spec **manda** anunciar. Antes de chamar de bloqueante, ver se a coluna
  seguinte resolve a ambiguidade: se resolve em poucas linhas, é sugestão de redação.
- **Ressalva textual × reabertura real de decisão adiada.** Teste que usei no TCK-0013: a seção
  declara o **delta de cada alternativa** sobre a tela (em C1 o cartão ganha X; em C3 o aviso
  vai para o topo; em C2 fica como está)? Se sim, a decisão está viva, porque a tela não pode
  ser implementada sem consultá-la. Se só diz "isto não é escolha de C2", é disclaimer.
- **Decisão do usuário × ADR que a registra.** Rastrear até o log onde o usuário fala
  (`grep -n 'confirmada\|decidiu' tickets/*/log.md`) antes de aceitar "DECIDIDA" num artefato.
  No TCK-0013 a decisão era real (usuário, TCK-0011 `[006]`), mas o `ADR-0007` que a registra
  estava `proposed` com a alternativa ainda listada e o C4 dizendo "PROPOSTO": a decisão vale
  (usuário > agente), e o defeito residual é de **citação**, não de autoridade — sugestão.
- **Grafia de URL × grafia de dado.** `/pt-br/` na URL e `pt-BR` na chave é distinção que se
  verifica com `grep -n 'pt-br'` e conferindo que toda ocorrência está em exemplo de URL:
  minúscula em coluna de tabela, chave ou campo localizado seria defeito.
- **Assimetria de tolerância de entrada não quebra RNF-1** (que governa paridade de *texto*),
  mas o **argumento** precisa ser simétrico: no TCK-0013 recusou-se `3,5` em en-US pela
  ambiguidade com o separador de milhar, enquanto `3.5` era aceito em pt-BR — onde o ponto é
  justamente o separador de milhar (`docs/content/i18n.md:20`). Procurar o espelho do próprio
  argumento do autor antes de aprovar a regra.
- **Lição da mesma família passa se o "Como aplicar" instrui ação nova.** L-022 × L-013/L-021:
  a ação nova era *onde* a norma nasce (seção estrutural, não a de riscos) e *nomear as
  exceções dentro da regra*. Conferir também a seção do índice (`## Erro`/`## Sucesso`) contra
  o campo `Tipo:` — L-022 caía certo em `LESSONS.md:76`, dentro de `## Erro` (37–81).
- **Justificativa técnica do produtor também se verifica.** "Editar `AGENTS.md` exigiria rodar
  o sync" é falso: as fontes do gerador são `.github/instructions/` (`sync-ai-adapters.py:49`),
  `.claude/agents/` e `.claude/skills/`. Aceitar a pendência pelo motivo certo (escopo do
  `tech-lead`) e corrigir o motivo errado no log, para não propagar restrição inexistente.

- **Aprovar correção de travessia exige caçar o falso positivo simétrico.** Quem conserta
  "não descia" pode passar a descer demais. Bateria que usei no TCK-0014 (loop 2): `assets/`
  + arquivo solto + diretório vazio, aninhamento de 3 níveis íntegro, symlink de diretório
  para fora da raiz, **symlink em loop** (com `timeout`, para provar que não trava) e um
  arquivo-marcador plantado dentro de `assets/`. Só o último gerou ruído — e não era
  regressão, porque a varredura da raiz já se comportava assim antes.
- **Afirmação de "quem prevalece" entre duas ferramentas se prova por fuzz diferencial.**
  Copiar as duas para um repo sintético (o `REPO_ROOT`/`CONTENT` delas passa a apontar para
  lá), aplicar N mutações à mesma fixture e procurar a assinatura `estrita=0 · lassa=1`. No
  TCK-0014 foram 22 mutações: zero inversões nas 20 de regra sobreposta, e as 2 ocorrências
  de "auditor mais estrito" (`difficulty`, `stage`) estavam **fora** da sobreposição, já
  declaradas como território dele. Leitura de cabeçalho não substitui isso — foi um cabeçalho
  falso que gerou o bloqueante do loop 1.
- **Citação de linha em documento normativo se confere com `sed -n "Np"`, uma a uma.** O
  cabeçalho corrigido citava 11 linhas do `audit-content.py`; imprimir as 11 é mais rápido
  que ler a prosa e é a única prova de que a correção da falsidade não virou outra falsidade.
- **Caçar o "oitavo caso" que o produtor não mediu.** Ele reportou 7 combinações de saída
  quebrada; rodei 23 (incluindo `--help` em 4 modos, `>&- 2>&-` simultâneo, `--quiet`/`--json`
  no caminho de erro de uso, `--root` sem valor e a guarda nova com stderr quebrado). Não
  achar o oitavo é resultado publicável — e é o que separa "aprovei" de "aprovei porque ele
  disse".
- **Guarda de usabilidade nova pede teste de caso legítimo recusado.** Ao aprovar um `ERRO DE
  USO` que antes era falso positivo, listar os usos válidos e rodá-los todos (aqui: `--root`
  correto, `--root` + alvo explícito, raiz com um nó chamado `content` em nível profundo, e
  sem `--root`). Fechar o argumento com a taxonomia: nenhum `stage` pode se chamar `content`,
  então não existe raiz legítima com `content/` na primeira camada.
- **Adendo × lição nova:** a norma (`memory/LESSONS.md:21`, `docs/ai/ticket-protocol.md:112`)
  manda criar lição nova quando a anterior é **superada**. Reincidência não é superação: a
  lição não foi contrariada, foi violada e ampliada — adendo no mesmo arquivo preserva o
  `L-NNN` citável e evita dois arquivos com "Como aplicar" quase idêntico. O que eu cobro no
  adendo é a troca de **lista de casos** por **regra de classe verificável**, e que cada
  regra nova tenha virado asserção na suíte.
- **Reincidência já sancionada não se cobra duas vezes.** A regra 7 se materializa no
  `REJECT` daquele loop; no loop seguinte o que se avalia é se a correção alcançou a classe.
- **Regra de contrato mais estrita que o schema: julgar por contradição, não por novidade.**
  Aceitei `ITEMS-EMPTY` e `JSON-DUPLICATE-KEY` num ticket de implementação porque (a) o texto
  do ticket atribuía a ele definir "conteúdo válido", (b) o "Fora de escopo" não as proibia e
  (c) nenhuma **contradiz** o documentado — `ITEMS-EMPTY` é mais frouxa que a regra 8 do
  schema e a outra é boa-formação de arquivo, não conteúdo. Teste: se a regra nova reprovasse
  algo que o schema aprova explicitamente, aí sim seria decisão do `tech-lead` antes.
- **Suíte que compara contagens > suíte que compara exit.** A asserção que fecha esta classe
  é "raiz e nó pai acusam o mesmo número de violações" (`validate-content-test.sh:384-388`) —
  exit igual passaria mesmo com o portão vendo metade do acervo.

- **"Não tenho a ferramenta" é afirmação verificável, e o revisor a verifica.** No TCK-0011 o
  produtor declarou como risco "não há Node nem `mermaid` no ambiente" e por isso não reparsou
  os diagramas — `node --version` devolvia **v24.14.1**. Custo de checar: um comando. Instalar
  parser no **scratchpad** não toca o repositório e não fere critério do tipo "nada instalado":
  separar *ambiente da revisão* de *dependência do projeto* antes de aceitar a recusa.
- **Legenda de diagrama é promessa auditável: separe a promessa substantiva da literal.** Ao
  revisar uma convenção do tipo "sem marcador = sustentado por ADR aceito ou spec aprovada, com
  a fonte no rótulo", testar as duas metades em separado. No TCK-0011 a substantiva era
  verdadeira nos 22 elementos (nenhum elemento sem marcador dependia de ADR `proposed`) e a
  literal falhava em 7 — atores, fronteiras e relações puramente descritivas. Critério de
  severidade: o dano da família B4 é o leitor tomar **hipótese por decisão**; promessa
  estilística quebrada não produz esse dano → sugestão, não bloqueante. Bloquear cosmética em
  loop 2/3 queima o último loop antes da escalada.
- **`EM ABERTO (ticket)` × `PROPOSTO (ADR-N)` não é preferência de rótulo.** Quando a fonte que
  atribui a decisão ao ticket é a **spec aprovada** (`plan.md`, "decisões de implementação a
  tomar nos tickets"), marcar `PROPOSTO (ADR-N)` afirma que **algum ADR deve** fechar aquilo —
  é o erro simétrico do que se veio corrigir. Aceitar o marcador de "ninguém decide por ADR" e
  conferir se a **legenda** foi generalizada junto (de "o que o ADR-0003 não decide" para "o
  que nenhum ADR decide de propósito"), senão o rótulo fica órfão da própria definição.
- **Adendo em lição existente × lição nova: o critério é a causa raiz, não a novidade do
  aprendizado.** Lição **superada** vira lição nova referenciando a antiga (AGENTS.md §5);
  lição **não aplicada** pede adendo — criar arquivo novo para a mesma causa fragmenta o
  índice. Aceitar o adendo quando ele acrescenta ação executável ao "Como aplicar" (no TCK-0011:
  frase-delatora "é isso que faz X ser Y, e não Z"; segundo passe sobre o texto pronto;
  bidirecionalidade da classe de marcação) e quando a distinção é **conferível no artefato
  original** — fui ler onde `prebuild` estava no texto reprovado e era mesmo dentro de um bullet
  legítimo, como justificativa de apoio. Distinção que não se confere no artefato é
  racionalização.
- **Antes de aprovar correção que devolve decisão ao ticket, ler o ticket que a recebeu.**
  `tickets/TCK-00NN/ticket.md` do executor em curso é a prova de que os dois documentos passaram
  a dizer a mesma coisa — no TCK-0011, o critério 8 do TCK-0015 e o `ADR-0007:122` convergiram
  palavra por palavra. Sem isso, "devolvi ao ticket" é promessa; com isso, é fato.
- **Critério de aceite vermelho por deriva alheia: atribuir com a fonte canônica, não com o
  gerado.** Receita usada: ler *qual* linha do relatório falhou (aqui só
  `sync --check: OUTDATED`), listar os **fontes** modificados (`.github/instructions/`,
  `.claude/agents|skills/`), cruzar com a lista de artefatos do handoff e contar ocorrências do
  meu tema nos gerados desatualizados (`grep -c "ADR-0006\|ADR-0007"` → 0). Aprovar com o
  critério marcado `[~]`, dizendo explicitamente ao QA para **não** pedir o sync ao produtor:
  regenerar reescreveria artefato de ticket em pleno voo.

- **Quando a norma **muda**, a lista de propagação é "onde a regra já mora", não "o que a
  correção tocou".** No TCK-0006 loop 2 o produtor acrescentou um gatilho ao teste e atualizou
  os 2 lugares que enunciam a regra por extenso + os 2 destinos novos do REJECT anterior,
  deixando `content-author`, `a11y-ux-reviewer`, o checklist de `published` e `core` com a
  enumeração antiga. Receita de revisão: pegar o **token** que a mudança introduziu
  (`sinal unário`, `-x^2`) e `grep -rn` em **todos** os arquivos que já citavam a regra; onde
  não aparecer, ou é ponteiro ("ver `docs/…`") ou é defeito. Enumeração fechada com lista de
  "exige/não exige" **não** é ponteiro.
- **O portão é o checklist, não o documento de padrão.** Critério do tipo "falha se o
  checklist ficar mais frouxo que a norma" se testa aplicando a **frase de condição** do
  checklist ao caso novo: "com argumento composto" não alcança `-x^2`, logo o portão aprova o
  que a norma proíbe.
- **`CORRECTION` é entrada, não parágrafo.** `docs/ai/ticket-protocol.md:170-181`: log
  append-only + registro errado ⇒ entrada `CORRECTION` com `Corrige: [SEQ]`. Declarar a
  substituição dentro da `ACTION` nova não satisfaz — quem grepa o log acha duas tabelas e
  nenhuma ligação formal.
- **Recontar inventário de passivo com método próprio, não conferir o do autor.** Parser de
  inline (`$…$` fora de `$$…$$`) + classificação por predicado nos três arquivos: bateu 22/22
  ocorrência a ocorrência e confirmou o custo zero do gatilho novo (0 ocorrências de sinal
  unário antes de base elevada no nó).

- **Critério textual se testa transcrevendo-o em código, sem olhar os vereditos do autor.** No
  TCK-0006 implementei o critério de unário ("não há termo à esquerda: início, ou após
  `=`, `<`, `>`, `(`, `[`, `,` ou outro operador") direto do texto e rodei contra as 12
  fórmulas da tabela + 2 inventadas: 14/14. **Bater 14/14 é a prova de que a regra é aplicável
  por quem não a escreveu** — muito mais forte que ler a redação e achá-la clara.
- **Padrão de busca publicado numa norma é artefato revisável: teste-o com positivos E
  negativos sintéticos.** O regex de "sinal unário antes de base elevada" perdia o caso-bandeira
  `$-x^2$` (o `$` delimitador ficou fora da classe) e acertava os outros — falso negativo
  silencioso que produz "0 ocorrências" com cara de prova. Receita: arquivo de 6 linhas com 3
  positivos e 3 negativos conhecidos antes de aceitar qualquer grep como controle.
- **Portão bom cita veredito, portão ruim reenuncia condição.** Critério do tipo "o checklist
  não pode ficar mais frouxo que a norma" se fecha estruturalmente: a condição vira "o que o
  teste marca como exige"; a enumeração que sobra é ilustração. Verificação: a condição
  sobreviveria se o teste ganhasse uma parte (c)?
- **Renomear um teste no meio do ticket não cria citação órfã se o nome antigo virar uma parte
  nomeada** do novo. Log é histórico e não se reescreve por renomeação (`ticket-protocol.md`
  regra 1 de auditoria).
- **Dívida sem portão mecânico não é bloqueante quando: nenhum critério a exige, o documento a
  declara, e o dono do mecanismo é outro ticket com cadeia ativa.** O que **é** exigível: que o
  controle compensatório (grep manual) funcione de verdade.
- **Proporcionalidade no loop 3/3:** achado real que não derruba nenhum critério de aceite vai
  como sugestão nomeada no handoff, com a correção testada junto — reprovar para escalar ao
  `tech-lead` por causa de um regex auxiliar seria custo sem ganho.

- **Portão de conteúdo: pergunte QUAIS portões estão em cada caminho, não SE existe portão.**
  No TCK-0015 o `prebuild` (caminho de publicação) rodava só `validate-content.sh`, e
  `audit-content.sh` — o único que enxerga paridade bilíngue — ficou só no Actions, que sem
  proteção de branch não bloqueia nada. Receita: montar a matriz *ferramenta × caminho* e, para
  cada regra normativa citada em ADR aceito, perguntar em qual célula ela é executada. Fixture
  que fecha a conta: nó `languages: ["pt-BR"]`, `status: published`, sem `theory.en-US.md` —
  `validate-content` exit 0, `audit-content` exit 1, `npm run build` exit 0 e HTML publicado.
- **Passo de CI feito de `if grep …; then exit 1; fi` é cego para alvo ausente.** `grep -r` sai
  **2** quando o caminho não existe; o `if` só dispara com 0, então o passo imprime o "OK" e
  fica verde. É L-019 no contexto de CI (a lição nomeia "verificação de CI" no Como aplicar) —
  bloqueante por regra 7. Teste de 5 segundos: rodar o `grep` do passo contra
  `<alvo>-INEXISTENTE/` e ler o exit.
- **Independência de módulo se prova em Node puro e em TRÊS `cwd`:** raiz do repo, subdiretório
  e fora do repo. O `grep` pelo nome do gerador é o teste fraco. Raiz achada subindo do `cwd`
  passa nos dois primeiros e lança no terceiro — aceitável (CI e host rodam na raiz, medido com
  cópia limpa em outro caminho absoluto), mas vira sugestão quando o módulo expõe parâmetro
  `root` que a avaliação **na carga** (`export const X = find()`) torna inalcançável.
- **`prebuild` se testa, não se lê:** `npm run build` com fixture inválida, mais uma repetição
  com `NODE_ENV=production` (é o ambiente do host) e outra numa cópia limpa do repositório em
  caminho absoluto diferente. O que liga o hook no host é `buildCommand: npm run build` no
  `vercel.json` — sem ele o preset do fornecedor chamaria o gerador direto e pularia o portão.
- **Afirmação sobre a imagem de build do host se confere na página citada e no contêiner.** No
  TCK-0015 o produtor disse que `python3` "não consta na lista publicada"; a mesma página traz a
  tabela *Runtime × Build image* com **Python 3.14/3.13/3.12**, e `amazonlinux:2023` puro já tem
  `/usr/bin/python3` (3.9.25) **sem instalar nada**, porque `dnf` requer `python3-dnf`. Receita
  de extração: `curl -sSL <url>` + `re.sub(r'<[^>]+>',' ')` + `html.unescape` + janela de regex.
  Erro **conservador** do produtor (risco declarado maior que o real) é sugestão de correção do
  log, nunca bloqueante — mas o revisor tem de fechar o número.
- **HTML publicado tem defeito de renderização que nenhum critério cobre.** Extrair o texto
  visível (`re.sub(r'<[^>]+>','')`) das páginas geradas e ler como um humano leria: no TCK-0015
  o compressor colou dois `<span>` irmãos e a raiz do site dizia "Escolha o idioma.Choose your
  language.". `grep` por recurso de terceiro não pega isso; só a leitura do texto renderizado.
- **Consequência falseável de ADR é checklist de portão de CI.** Quando o produtor transforma
  duas das três consequências falseáveis em passo do workflow, procurar a terceira: no TCK-0015
  "nenhuma rota emitida contém letra maiúscula" ficou sem guarda, e fixture com diretório
  `Uppercase-Slug` passou nas duas auditorias, no validador e na build.

- **Atribuição de sync se prova regenerando numa cópia, não comparando com o `HEAD`.** O teste
  `gerado contém o texto do outro ticket × HEAD da fonte não` é válido só até o outro ticket
  commitar — no TCK-0016 o `dea3303` caiu no meio da minha revisão e caducou a prova do
  produtor. Receita que não caduca: `tar --exclude=.git` para o scratchpad, rodar
  `sync-ai-adapters.py` **na cópia** e `diff` dos gerados contra os do repositório. O delta
  **semântico** (ignorando deslocamento de linha) nomeia o dono sozinho. Bônus: mostra qual
  texto de terceiro já está nos gerados e vai viajar junto quando o sync rodar — avisar isso no
  REJECT evita um segundo loop por susto.
- **Dívida com dono externo × dívida própria: o mesmo critério vermelho dá vereditos opostos.**
  No TCK-0011 aprovei com `[~]` porque a deriva era de outra cadeia e regenerar reescreveria
  artefato alheio em pleno voo. No TCK-0016 o delta era 100% do próprio ticket e o impedimento
  (outro ticket com o direito exclusivo de rodar o sync) tinha caído — aí `[~]` vira dispensa de
  critério de aceite. Antes de aceitar um `[~]`, perguntar as duas coisas: *de quem é o delta* e
  *o impedimento ainda existe?* Um "não" em qualquer das duas transforma a dívida em bloqueante.
- **Aceite de ADR: o antídoto de L-011 é o terceiro bloco de consequências.** "O que passa a
  valer · o que fica proibido sem ADR novo · o que continua sendo decisão de ticket". Revisar o
  terceiro bloco contra a lista numerada do `plan.md` fecha o B2 em minutos. E revisar os dois
  primeiros de outro jeito: cada afirmação deles tem de existir no corpo **já aceito**
  (`git show HEAD:<adr> | grep -n`) — consequência é onde se contrabandeia decisão nova, porque
  ninguém a lê como seção normativa.
- **Emendar ADR aceito por nota editorial é conduta correta quando o alvo é ilustração.** A
  regra "ADR não se reescreve" tem por objeto a **decisão**. Rótulo de Mermaid que exibe uma
  grafia que um ADR posterior descartou é informação falsa em documento normativo
  (`docs/DOC-STANDARDS.md`), e a alternativa "nota sem mexer no rótulo" **produz** o defeito B4.
  Forma que aprovei: nota no cabeçalho, datada, com o ticket, dizendo "nenhuma decisão foi
  alterada", diff mínimo, rótulo trocado por enunciado neutro.
- **Alternativa descartada não é "grafia viva".** Critério do tipo "a alternativa sai do ADR" se
  lê como "sai de onde é opção disponível" — remover as alternativas quebraria o formato de ADR.
  O que faz a diferença entre registro histórico e opção viva não é o argumento do produtor: é
  existir um parágrafo que **nomeia** a alternativa como fechada ("Fechado no aceite"). Sem ele,
  bloqueante; com ele, aprovado.
- **Pendência em área de outro dono: separar "consequência do meu ticket" de "consequência de
  outro ticket".** No TCK-0016 o produtor editou `spec.md` (pergunta que o aceite respondeu) e
  **não** `plan.md:103` ("não existe código hoje", superado pelo TCK-0015) — mesma pasta, donos
  iguais, fronteira certa. O teste é causal, não territorial. Ainda assim, nota no log não dá
  dono: exigir roteamento ao `tech-lead` como sugestão, senão a pendência apodrece (a do
  `ADR-0003` aberta no TCK-0003 seguia aberta no TCK-0016).

- **Relaxar um padrão de busca é afrouxar um portão — e a sugestão que pede o relaxamento é
  minha, mas a cobertura da implementação é do produtor.** No TCK-0015 loop 2 a troca de
  `https?://` por um padrão específico (minha S5) fez 8 de 18 vetores hostis passarem em
  silêncio: pixel em protocolo relativo (`src="//host/p.gif"`), aspas simples, `@import` sem
  `url()`, `<object data>`, `<a ping>` (beacon), `meta refresh`, `<image href>` em SVG e
  **qualquer tag em maiúscula** (`grep -rInE` sem `-i`, enquanto nome de tag em HTML é
  case-insensitive). Receita: sempre que um portão trocar "genérico" por "específico", rodar
  bateria de vetores **e** medir um padrão alternativo próprio, para o REJECT chegar com
  conserto provado (14/14 e zero falso positivo no artefato real), não com exigência.
- **`public/` é passagem verbatim para `dist/`** — é o vetor que transforma "o gerador nunca
  emite isso" em falso. Prova de bypass de guarda de HTML se faz com arquivo em `public/` e
  build de verdade, não com `dist/` sintético.
- **Bloco `run:` de workflow se testa extraindo o texto versionado do YAML por script** (regex
  em `- name: … run: |` + dedent de 10 espaços) e executando o arquivo resultante. Paráfrase
  não vale: o defeito mora na pontuação (`set +e` em volta do `grep`, `case "$rc"`).
- **Bateria mínima de passo de CI que usa `find`/`grep`:** alvo real · alvo ausente · alvo
  vazio · alvo com achado · **renome legítimo da extensão** · menção em arquivo não-alvo ·
  binário com o token · subdiretório sem permissão · e, para `[A-Z]` em `find`, repetir com
  `LC_ALL=C`, `en_US.UTF-8` e `pt_BR.UTF-8` (colação de faixa é fonte clássica de falso
  positivo — no TCK-0015 não houve).
- **Portão novo numa cadeia `a && b`: testar `b` sozinho.** No TCK-0015 `audit-content.sh`
  entrou no `prebuild`, e sozinho ele **aprova** `content/` ausente ou vazio
  (`audit-content.py:345-346`, `:360-362`, "nada a auditar" → exit 0); quem barra é o
  `validate-content.sh` que vem antes. O portão está fechado, mas por ordem — e ordem que
  ninguém documentou é buraco esperando reordenação.
- **Proporcionalidade de portão editorial no caminho de publicação se mede no código do
  exit**, não na prosa: `return 1 if errors else 0` prova que AVISO não derruba deploy. Sem
  isso, "erro editorial agora derruba deploy" seria desproporcional.
- **Escolher falhar × pular se julga comparando com a regra que JÁ existe no acervo.** O leitor
  que falha alto em nó monolíngue não inventou proibição: `audit-content.py` já reprovava
  `languages` incompleto **independentemente do `status`** — conferido rodando o caso `draft`,
  que o produtor não citou. Rede de segurança igual ao contrato = correta; mais estrita que o
  contrato = decisão de outro dono.

- **A prova de atribuição mais forte é a previsão registrada antes do ato.** No `[009]` do
  TCK-0016 regenerei os 9 adapters numa **cópia** para atribuir a deriva; quando o produtor
  rodou o sync de verdade, comparei os 9 do repositório com os 9 da minha cópia: **byte-idênticos
  nos 9**. Isso fecha de uma vez "a correção fez o certo", "não arrastou nada" e "a minha
  atribuição do loop anterior estava certa" — sem reler diff nenhum. Guardar a saída da
  verificação preditiva do loop 1 é o que torna o loop 2 barato.
- **Aprovar sync alheio: medir o ESCOPO por mtime, não pela lista do produtor.** `stat -c '%y %n'`
  nos gerados separa em segundos o que o comando escreveu (mesmo segundo, aqui `17:43:13`) do que
  já estava lá de outro ticket (`16:55:45`, as regras `content` do TCK-0006, não recriadas). O
  mesmo relógio prova que o ticket vizinho em revisão paralela não foi tocado (`package.json`
  17:28, `vercel.json` 17:00 — anteriores ao sync). Vale também para provar que a **correção** não
  perturbou os artefatos já aprovados: se o mtime deles é anterior à correção, não há o que
  reabrir no loop 2.
- **Convenção nova que eu mesmo pedi também se revisa — e o furo mora na equivalência falsa.**
  A fronteira escrita em `docs/adr/README.md` juntou por travessão "a emenda só vale para o que o
  ADR **não** decide" e "se a frase falsa **for** a decisão, o caminho é `superseded`": não são a
  mesma regra, e entre elas cai o caso que originou tudo (rótulo divergindo da decisão do próprio
  ADR — meu B4 do TCK-0003). Receita: para cada fronteira redigida com duas formulações, achar o
  caso que uma permite e a outra proíbe. Erro conservador ⇒ sugestão.
- **Log de ticket pode perder a ordem sem perder conteúdo.** Com dois agentes escrevendo o mesmo
  `log.md`, entradas novas podem ser **inseridas** antes de uma anterior: no TCK-0016 `[010]`–
  `[014]` ficaram acima do meu `[009]`. Teste que separa desordem de perda:
  `git diff --numstat -- <log>` — remoções **0** significa que nada foi reescrito. Desordem sem
  perda é sugestão ("ler por `[SEQ]`, não por posição") e **não se conserta**: reordenar seria
  reescrever log publicado, que é o defeito maior.
- **Nota de memória de agente × lição: o teste é a audiência, não a origem.** Conhecimento que
  serve a qualquer agente (dívida declarada expira quando o impedimento acaba; prova por `HEAD`
  caduca com commit alheio) pertence a `memory/lessons/` por AGENTS.md §5, mesmo tendo nascido na
  execução de um papel específico. Quando o produtor cita uma lição vizinha como "mesma família"
  e a proposição é claramente outra, não bloquear (a regra 7 foi cumprida e o conhecimento está
  registrado com receita executável) — encaminhar ao `retrospective-curator`.

- **A bateria de um detector tem DOIS lados, e o segundo é o que prova que ele não voltou a
  ser genérico.** Ao reaprovar um padrão reescrito, rodar os vetores hostis **e** os casos
  legítimos (link de referência, recurso de mesma origem, URL em texto corrido, fragmento
  `#id`). No TCK-0015 foram 18 + 8, reproduzidos por mim contra o bloco `run:` reextraído
  **depois** da última edição — e provado literal com `bloco reindentado in yaml`.
- **Cauda de regex × inversão de classe: é a distinção que decide bloqueante em loop 3.** No
  loop 2 escapavam o pixel clássico (`src="//host"`), o beacon nomeado no critério e
  **qualquer tag em caixa alta** — formas ordinárias, com bypass reproduzido em build real:
  bloqueante. No loop 3 sobrou `<base href>` (sério, mas tag única e incomum) e cauda
  (`src = "…"` com espaços, `srcset` sem aspas, `image-set()`, `<feImage>`, entidade HTML):
  achado numerado, não bloqueio. Critério: **existe forma ordinária de erro acidental que
  escapa?** Se não, é cauda — e exigir parser em vez de regex é desproporcional.
- **Caçar o vetor que reparenta, não só o que carrega.** `<base href="https://…">` transforma
  todo caminho relativo da página em terceiro com uma linha, e passa por qualquer padrão que
  procure `src=`/`href=` de recurso. Entrar na bateria padrão de guarda de HTML.
- **Dimensionar a dívida que o produtor declarou, em vez de aceitar o exemplo dele.** Ele
  declarou "fonte auto-hospedada vai reprovar"; medi as quatro colisões e o passo reprova
  também a ilha (`<script src="/_astro/…">`), o registro do service worker e `<iframe>` de
  mesma origem — ou seja, ele fica vermelho no **primeiro** ticket de interatividade, não no
  de tipografia. Dívida subdimensionada é dívida que ninguém agenda.
- **Três adendos na mesma lição: julgar pela causa, não pelo tamanho.** L-019 acumulou o que
  o portão percorre, onde ele fica e o que ele casa — mesma causa (ponto cego), três
  dimensões, nenhum superando o anterior: adendo é a forma certa, e dividir destruiria o
  `L-NNN` citável. O que se cobra é **usabilidade**: quatro listas "Como aplicar" em 140
  linhas viram lição não lida — pedir consolidação num checklist no topo, histórico abaixo.
- **Chave `"//"` em `package.json` é comentário válido** (npm a ignora); conferir com
  `require()`, `npm ci`, `npm run build` e `npm pkg get` antes de aceitar — foi a forma que
  resolveu "documentar a ordem load-bearing de uma cadeia `a && b`" onde ela pode ser quebrada.
- **Fechar uma revisão de deploy exige responder "está pronto para ir ao ar?" com a condição
  operacional explícita.** Aprovar o diff não é aprovar a publicação: dizer que o push é ato do
  usuário, que o QA valida **antes** do push, e qual é o modo de falha do primeiro deploy.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0001 — revisão do diff de `references.json` do nó piloto | APROVADO — 0 bloqueantes, 3 sugestões; licenças CC BY-NC-SA 4.0 reverificadas na fonte, divergência BY-SA do PDF pt-BR confirmada; handoff para `qa-validator` | L-006, L-007 |
| 2026-08-01 | TCK-0002 · revisão da spec `minimum-learning-slice` (como `code-reviewer#3`) | APROVADO — RF-1…RF-18, RNF-1…RNF-11, 13 estados e CA-1…CA-16 fiéis à fonte; spec marcada `approved` em `spec.md`, `plan.md` e `docs/specs/README.md`; 5 sugestões não bloqueantes; auditorias reexecutadas sem erro; handoff `[007]` para `qa-validator` | L-001, L-003, L-008 |
| 2026-08-01 | TCK-0003 — revisão do aceite do `ADR-0003` (stack) | REPROVADO (loop 1/3) — 3 bloqueantes: desbloqueio não propagado para `AGENTS.md`/`.github/instructions`, ADR fixando renderização do KaTeX na build, `docs/architecture/` alterado sem constar no log; 3 sugestões; auditorias verdes | — |
| 2026-08-01 | TCK-0004 — revisão do diff da licença do projeto (como `code-reviewer#4`) | REPROVADO — 1 bloqueante (regra NC ausente de `AGENTS.md` §9.6/§9.7 e de `content.instructions.md`), 4 sugestões; MIT conferida literal contra SPDX/OSI (169 palavras, 0 diferenças), paridade pt-BR/en-US do `LICENSE-CONTENT` medida, Mermaid validado no parser, auditorias reexecutadas verdes | L-009 |
| 2026-08-01 | TCK-0003 — re-revisão do aceite do `ADR-0003` (loop 2/3) | REPROVADO — 1 bloqueante (B4: nó Mermaid do ADR ainda diz "KaTeX pré-renderizado", contra `:12`/`:116` e L-011) + 2 sugestões; B1/B2/B3 e S1–S3 verificados e aprovados, sync sem deriva, auditorias verdes; próximo loop esgota o limite → `tech-lead` | L-010, L-011 |
| 2026-08-01 | TCK-0003 — re-revisão final do aceite do `ADR-0003` (loop 3/3) | APROVADO — B4 resolvido e 2ª ocorrência da classe (nó `S`) corrigida pelo produtor; `:64` HTML × KaTeX conferida; S4/S5 acatadas; L-013 julgada lição legítima (não repetição de L-011, por cronologia); 3 comandos reexecutados verdes; 2 sugestões; handoff `[014]` → `qa-validator` | L-010, L-011, L-013 |
| 2026-08-01 | TCK-0004 — revisão do loop 2/3 (correção do B1), como `code-reviewer#4` | APROVADO → `qa-validator`; renumeração do `AGENTS.md` §9 varrida (30 refs, 0 quebradas), gerados conferidos linha a linha, `sync --check` limpo, auditorias verdes, MIT reconferida (169/169) e paridade do `LICENSE-CONTENT` mantida (494/486 palavras); compatibilidade BY-SA entre versões confirmada no legalcode 3.0 §4(b)(ii); 4 sugestões não bloqueantes | L-009 (adendo) |
| 2026-08-01 | TCK-0012 — revisão da camada de detecção de contexto e gatilho de handoff | REPROVADO (loop 1/3) — 4 bloqueantes: falso verde por janela presumida otimista + hook sem ramo de incerteza (`context-watch.py:51`,`:357`), `--hook` saindo 120 em falha de stdout contra invariante documentada em 4 lugares, suíte não hermética (quebra com `autoCompactWindow` no `HOME`), duas entradas auto-concedidas em `permissions.allow` descritas como "bloco preservado"; 6 sugestões; privacidade auditada linha a linha sem vazamento; 5 faixas, 41 asserções, snapshot e auditorias reexecutados | — |
| 2026-08-01 | TCK-0012 — re-revisão da camada de contexto (loop 2/3) | REPROVADO — B2/B3/B4 e S1/S2/S4/S5/S6 resolvidos e reverificados (matriz de 15 saídas do hook, suíte 65/0 em 4 ambientes, `permissions` idêntico ao HEAD por `jq -S`, S3 reprovada com 51 MB → 0,24 s); 2 bloqueantes novos: B5 — presunção conservadora satura em CRITICO e mata o hook pelo resto da sessão (1 alarme falso, 0 verdadeiros) com número autorrefutável vazando para o `.agent-handoff.md`; B6 — `flush_stdio()` sai 1 com traceback quando o fd 1 está fechado. Próximo loop esgota → `tech-lead` | L-015, L-016 |
| 2026-08-01 | TCK-0012 — re-revisão final da camada de contexto (loop 3/3) | APROVADO → `qa-validator`; B5 resolvido pela refutação da presunção com escalonamento anunciado (reproduzi VERDE 37,8% sem setup e o hook falando em 3 faixas; travessia 199.999/200.000/200.001, degraus esgotados → 40, janela configurada não escalonada, oscilação por compactação), B6 fechado (14 invocações de fd fechado, todas 0); suíte 93/0 em 5 ambientes, substituição de asserção sem perda de cobertura, L-017/L-018 sem colisão e L-018 ≠ L-013; 4 sugestões, `WINDOW_TIERS` registrado como dívida declarada | L-015, L-016, L-017, L-018 |
| 2026-08-01 | TCK-0013 — revisão do desenho dos 13 estados de tela da fatia mínima (como `code-reviewer#5`) | REPROVADO (loop 1/3) — 5 bloqueantes: regra "mover foco OU anunciar" violada em E2/E5/E10, região viva de E1 com escopo que despeja o conteúdo, princípio §2 negando CA-3, decisão adiada (c) fechada por omissão no §5, `docs/design/` fora dos índices; 6 sugestões. Cruzamento 1-a-1 dos 13 estados (script, 13/13), 69 chaves bilíngues sem célula vazia, dados de `meta.json`/`exercises.json` conferidos, Mermaid validado no parser, busca negativa de stack (2 ocorrências, ambas negando), auditorias reexecutadas verdes (critério 9 fechado) | — |
| 2026-08-01 | TCK-0014 — revisão do validador do contrato de `content/` (como `code-reviewer#6`) | REPROVADO (loop 1/3) — 3 bloqueantes: B1 nó descendente invisível (`find_nodes:488-492` devolve `Contrato íntegro: 1 nó` onde o `audit-content.py` acha 2 nós e 3 erros; mesma classe da L-019 → regra 7), B2 `exit 2` virando `120` com stderr quebrado em 4 combinações (correção do [004] cobriu só o stdout), B3 fronteira do cabeçalho factualmente falsa e já copiada para `memory/context/backend.md` (4 famílias de regra duplicadas + 2 divergências de veredito); 6 sugestões; A5 confirmado por medição e roteado a ticket próprio, premissa de `tolerance` absoluta julgada inerte no código; 9 vetores de burla, 7 barrados; suíte 84/0 em 4 ambientes; auditorias verdes | L-019 |
| 2026-08-01 | TCK-0011 — revisão do C4 Container + `ADR-0006` (CI/CD) + `ADR-0007` (esqueleto), como `code-reviewer#7` | REPROVADO (loop 1/3) — 2 bloqueantes, ambos reincidência: B1 = `ADR-0007:115-121` fecha *onde* roda o validador do RF-18, que `plan.md:132,140` atribui ao ticket (padrão B2/L-011); B2 = `c4-container.md:44` afirma esse portão sem marcador entre duas relações marcadas (padrão B4/L-013). 4 sugestões. Verificados e aprovados: 4 blocos Mermaid no parser, critérios 2/6/7/9/10 reexecutados, custo zero reverificado verbatim nas 4 fontes + repositório PUBLIC, não-propagação de ADR `proposed` julgada correta, régua L-020 julgada legítima e usada para achar o defeito | L-011, L-013, L-020 |
| 2026-08-01 | TCK-0006 — revisão da norma de leitura de fórmula e da fronteira display × inline (como `code-reviewer#8`) | REPROVADO (loop 1/3) — 4 bloqueantes: B1 inventário do critério 7 sem `(x+3)^2` (`exercises.json:224/225`, `grep -nF ')^'` → 8 linhas × 6 listadas, classe L-013), B2 total declarado (6/3-por-idioma) contradizendo as 4 linhas EXIGE da própria tabela → 8, erro já copiado para `memory/context/content.md`, totais corretos 8 + 14 = 22, B3 regra passou a reger `exercises.json` sem chegar a `exercise-designer`/`/new-exercise-set` (L-021 item 5, L-009/L-010), B4 `-5^2` citado na justificativa e sem veredito, com leituras de valores diferentes; 4 sugestões. Decisão de fundo e as duas calibragens **aprovadas**; teste aplicado por mim a 12 famílias inline do piloto com veredito idêntico ao da tabela; renumeração §9 limpa (8 itens, 79 referências, nenhuma quebrada), sync +54/−12 em 9 gerados só de regra, Mermaid validado no parser, 3 auditorias verdes, `content/` intacto | L-009, L-013, L-021 |
| 2026-08-01 | TCK-0013 — re-revisão do desenho dos estados de tela (loop 2/3, `code-reviewer#5`) | APROVADO → `qa-validator`; os 5 bloqueantes verificados no artefato: regra de anúncio virou norma em §3 e **varri os 13** (3 movem foco sem região viva, 8 anunciam com foco parado, 3 são navegação, E4 sem evento — nenhum faz os dois), região viva reduzida a linha de estado (esvaziar não fala, `aria-relevant` padrão), §2 princípio 5 alinhado a CA-3, §5 reabre (c) declarando o delta de C1/C2/C3, `docs/README.md` indexado; decisão `/pt-br/` rastreada até o log do TCK-0011 (usuário) e a distinção URL × chave conferida (4 ocorrências, todas URL); 13/13 estados, 68 chaves sem célula vazia nem token divergente, Mermaid revalidado, auditorias verdes, escopo do diff isolado de 42 arquivos paralelos; 6 sugestões (S7–S12) | L-022 |
| 2026-08-01 | TCK-0014 — re-revisão do validador do contrato (loop 2/3, como `code-reviewer#6`) | **APROVADO** → `qa-validator`; B1 refeito com a minha fixture (nó pai, raiz e subnó dão o mesmo veredito; 5 cenários de falso positivo simétrico, incluindo symlink em loop, sem bloqueante), B2 com 23 combinações de saída quebrada e nenhum oitavo caso, B3 provado por fuzz diferencial de 22 mutações (0 inversões nas 20 sobrepostas) + 11 citações de linha conferidas; S1–S6 verificadas, S3 e S5 com caso legítimo testado; suíte 118/0 em 3 ambientes; adendo de reincidência em L-019 julgado registro correto; `ITEMS-EMPTY`/`JSON-DUPLICATE-KEY` aceitos por não contradizerem o schema; 4 sugestões novas e 3 encaminhamentos ao `tech-lead` | L-013, L-018, L-019 |
| 2026-08-01 | TCK-0011 — re-revisão do C4 Container + `ADR-0006`/`ADR-0007` (loop 2/3), como `code-reviewer#7` | APROVADO → `qa-validator`; B1 conferido por varredura da **raiz** (única sobra `ADR-0007:122`, legítima) e cruzado com `TCK-0015/ticket.md:55`, que agora diz o mesmo; B2 resolvido com `EM ABERTO (ticket)` — argumento julgado correto, mais a generalização da legenda; auditoria da legenda nos 22 elementos (substantiva verdadeira, literal falha em 7 → sugestão); 4 blocos Mermaid reparsados por mim (o risco "não há Node" do produtor era falso: v24.14.1); adendos em L-011/L-013/L-020 julgados forma correta e distinção conferida no artefato; critério 10 `[~]` por deriva do ticket de a11y matemática, atribuída pela fonte canônica; 4 sugestões | L-011, L-013, L-020 |
| 2026-08-01 | TCK-0006 — re-revisão da norma de leitura de fórmula (loop 2/3, como `code-reviewer#8`) | REPROVADO por pouco — B1–B4 **fechados** e reconferidos com método próprio (recontagem independente bateu **22** pontos ocorrência a ocorrência; gatilho 2 do B4 **aprovado** como proporcional, custo zero medido por varredura própria; B3 chegou a `exercise-designer`/`/new-exercise-set`, 0→3 ocorrências) e S1–S4 acatadas; 2 bloqueantes novos: B5 — o gatilho acrescentado **nesta** rodada não chegou a `content-author`, `a11y-ux-reviewer`, `content-standards` (Notação + checklist de `published`, que é o portão do critério 6), `core.instructions` + 6 gerados, `/new-topic` e `/a11y-audit`, todos com enumeração fechada terminando em "parênteses" (`-x^2` mudo passa); B6 — falta `CORRECTION` com `Corrige: [004]` (protocolo `:170-181`). 2 sugestões (critério unário×binário do gatilho 2; campo `prompt` inexistente, o schema usa `stem`). Mermaid revalidado com `Q3`, 3 auditorias verdes, `content/` intacto. Conduta de escalada do TCK-0007 confirmada, com 3 pedidos concretos ao `tech-lead`. **Próxima devolução esgota o loop** | L-010, L-021 (adendo) |
| 2026-08-01 | TCK-0006 — 3ª revisão da norma de leitura de fórmula, decisória (como `code-reviewer#8`) | **APROVADO** → `qa-validator` (`in_validation`), loop encerrado em 2 devoluções. B5 fechado por correção **estrutural** (teste renomeado com partes (a)/(b), portão de `published` passando a citar o **veredito** em vez de reenunciar a condição — verifiquei que a condição sobrevive a uma parte (c) futura) e B6 pela `CORRECTION` `[010]`. Verificações próprias: critério de unário do S1 transcrito em código a partir do texto → **14/14** contra a tabela do autor + 2 casos inventados; inventário recontado ((b)1=14, (b)2=0) → **22** confirmado; 20 arquivos com `grep -c 'base elevada\|unário'` sem nenhum zero (eram 0 em 10); log append puro (`git diff -U0` sem remoção); 3 auditorias verdes; Mermaid no parser; 6 gerados (`core` × 6). 1 sugestão com correção testada: o regex de (b)2 publicado perde `$-x^2$` (falta `$` na classe). Três julgamentos pedidos: renomeação **aprovada**, ausência de portão mecânico **aceita como dívida declarada** (roteada ao TCK-0014), 3ª aparição da causa raiz **vira lição própria** (`L-023`, `retrospective-curator`) por `AGENTS.md` §5 "uma lição por arquivo". TCK-0007 re-escalado ao `tech-lead`: 22 pontos, 3 pedidos concretos | L-010, L-012, L-021 (2 adendos) |
| 2026-08-01 | TCK-0015 — revisão do esqueleto da aplicação e do deploy (como `code-reviewer#9`) | REPROVADO (loop 1/3) — 3 bloqueantes: B1 nó sem paridade bilíngue vira rota publicada porque `audit-content.sh` (único que enxerga a regra, exit 1) não está no `prebuild`, só no Actions, que não bloqueia (`ADR-0006:93-94` accepted; medido: build exit 0 + HTML emitido); B2 os dois passos novos de CI (`:73-78`, `:90-95`) imprimem OK com alvo ausente porque `grep -r` sai 2 e o `if` só dispara com 0 — L-019/regra 7, e cega justamente o teste falseável do `ADR-0007:246-247`; B3 `dist/index.html` publica "Escolha o idioma.Choose your language." colado. 8 sugestões. Verificados e aprovados: contrato de dados em Node puro nos 3 `cwd` + cópia limpa noutro caminho absoluto, `prebuild` derrubando a build em 3 ambientes (inclusive `NODE_ENV=production`), rede de segurança da fixture B, rotas 200/200/200 e `/pt-BR/` 404, `lang` correto nas 3 páginas, zero terceiros no HTML (13 padrões), contraste 8,2:1 e 11,4:1, 5 auditorias verdes, `content/` intacto; Python na imagem de build reverificado (docs + `amazonlinux:2023` sem instalar nada) e `engines.node` conferido na tabela da Vercel | L-019 |
| 2026-08-01 | TCK-0016 — revisão do aceite dos `ADR-0006` e `ADR-0007` (como `code-reviewer#10`) | **REPROVADO** (loop 1/3) — 1 bloqueante: sync não rodado, `audit-ai-surface.sh` exit 1 (`OUTDATED`, 9 gerados) contra os critérios 6 e 8, com o impedimento externo extinto (TCK-0006 commitado em `dea3303` durante a revisão). Atribuição **provada por regeneração em cópia no scratchpad**: delta semântico 100% do próprio ticket; texto do TCK-0006 já presente dos dois lados. Reincidência **negativa** nas duas famílias: B2 conferido item a item contra `plan.md:132-142` (o item 5, lugar do portão do RF-18, preservado em 4 lugares) e cada afirmação dos blocos de consequências rastreada ao corpo já aceito via `git show HEAD:`; B4 conferido relação por relação nos dois C4 (`PROPOSTO (ADR-000[67])` só em `tickets/**`, `EM ABERTO (ticket)` 4× em `c4-container.md`, erro simétrico procurado e ausente). Julgamentos pedidos: emenda editorial no `ADR-0003` **aprovada** (a alternativa oferecida recriaria o B4), `/pt-BR/` nas alternativas do `ADR-0007` **mantido** (salvo pelo parágrafo "Fechado no aceite"), edição de `spec.md:277` proporcional. Verificados: 5 blocos Mermaid reparsados (5/0), `audit-content.sh` exit 0, L-025 sem colisão e na seção `## Correção`, `docs/design/…:689,833` confirmado de outro dono. 3 sugestões | L-010, L-011, L-013, L-020, L-025 |
| 2026-08-01 | TCK-0015 — re-revisão do esqueleto e do deploy (loop 2/3, `code-reviewer#9`) | REPROVADO por pouco — B1/B2/B3 **fechados** e reverificados com método próprio (monolíngue `published` **e** `draft`, os dois derrubando nas duas camadas; 8+18+7 cenários nos blocos `run:` extraídos do YAML, incluindo `.mjs`, binário, permissão negada e 3 locales; S3 ponta a ponta; S4 nos 3 `cwd` + `root` explícito). 1 bloqueante novo: **B4** — o padrão do passo de terceiros (`:127`, minha S5) regrediu a detecção: `public/legado.html` com `<SCRIPT SRC="https://…">` e `<img src="//pixel…">` chega ao `dist/` e o passo imprime **OK, exit 0**; 8 de 18 vetores passam, incluindo `<a ping>` e pixel em protocolo relativo. Medi um padrão substituto (14/14, zero falso positivo no `dist/` real) para o REJECT chegar com conserto provado. 4 sugestões; auditoria vermelha atribuída ao TCK-0016 por medição (0 ocorrências de TCK-0015 nos 9 gerados) → critério 13 `[~]`. **Próxima devolução esgota o loop** | L-013, L-019, L-021 |
| 2026-08-01 | TCK-0016 — re-revisão do aceite dos `ADR-0006`/`ADR-0007` (loop 2/3, `code-reviewer#10`) | **APROVADO** → `qa-validator` (`in_validation`), loop encerrado em 1 devolução. Defeito 1 fechado: os 3 comandos reexecutados por mim com exit 0 (`sync --check` "Tudo já estava atualizado", `audit-ai-surface` `up-to-date`/`Resultado: OK`, `audit-content` 0 erros). Prova decisiva: os 9 gerados do repositório são **byte-idênticos** aos que eu havia regenerado na cópia do scratchpad **antes** do sync dele — atribuição do loop 1 confirmada por construção, zero arraste. Separação declarada conferida arquivo a arquivo (`/pt-br/` nos 9; `agrupamento` nos 6 de `core`, 0 nos 3 de `app`; `git show HEAD:core.instructions.md` → 0). Escopo e não-contaminação do TCK-0015 medidos por mtime (sync 17:43:13 × `package.json` 17:28, `vercel.json` 17:00, regras `content` 16:55), e o mesmo relógio provou que os artefatos do loop 1 não foram perturbados. `[011] CORRECTION` conferida no `HEAD` (a 6ª linha era `spec.md:277`, dele) e recontagem independente = 5. 3 sugestões: ordem física do log ([010]–[014] inseridas antes do [009]; 0 remoções, ler por `[SEQ]`, não reordenar), equivalência falsa nas duas metades da fronteira da convenção de emenda editorial, e 2 notas de memória de interesse geral a rotear ao `retrospective-curator` (possível L-026) | L-010, L-011, L-013, L-020, L-025 |
| 2026-08-01 | TCK-0015 — revisão final do esqueleto e do deploy (loop 2/3 fechado, `code-reviewer#9`) | **APROVADO** → `qa-validator` (`in_validation`), sem escalada. B4 fechado: reproduzi os 26 vetores (18 reprovam, 8 legítimos passam) contra o bloco `run:` reextraído e provado literal, mais 4 formas ordinárias próprias — nenhuma escapa; ponta a ponta com `public/legado.html` (build exit 0, passo exit 1 citando as 2 linhas; sem fixture, exit 0). Job de CI inteiro do zero: 10/10 exit 0, critério 13 sem ressalva (TCK-0016 regenerou). Rotas 200/200/200 e `/pt-BR/` 404, `lang` correto, zero `https://` no dist, chave `"//"` inócua, escopo limpo. 4 achados não bloqueantes: A1 `<base href>` (o 19º vetor) + cauda medida, A2 dívida subdimensionada (ilha, service worker e iframe de mesma origem também reprovam), A3 consolidar as 4 listas da L-019, A4 notas ao QA. Declarei o artefato pronto para ir ao ar, com a condição de o QA validar antes do push | L-013, L-019, L-021, L-022 |
