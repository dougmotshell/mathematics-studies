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
