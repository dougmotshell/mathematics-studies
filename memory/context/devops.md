# Contexto operacional — devops

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01 (TCK-0015)

## Estado atual

- CI: um único workflow, `.github/workflows/ai-surface-audit.yml` (PR, push em `main`,
  semanal). Roda `audit-ai-surface.sh`, `sync-ai-adapters.py --check`, `audit-content.sh`,
  `tools/context-watch-test.sh` (TCK-0012) e, **desde TCK-0015**, `validate-content.sh`,
  `npm ci`, o `grep` de independência do contrato de dados, a **build de verificação** e o
  `grep` que reprova recurso de terceiro em `dist/`. O **nome do arquivo é mantido** de
  propósito (`ADR-0006` e tickets fechados o citam); só o `name:` exibido mudou.
- **Aplicação existe desde TCK-0015** (esqueleto do `ADR-0007`, na raiz): `package.json`
  (`private`, `engines.node >= 22.12.0`, `dependencies` = só `astro`, `devDependencies`
  vazio), `astro.config.mjs`, `vercel.json`, `public/`, `src/{content-contract,pages,layouts,
  components,islands,styles}`. `npm run build` → `dist/` estático. Uma página mínima por
  idioma; índice, leitor e player são tickets próprios (tasks 5–8).
- **Portão do acervo (decisão do TCK-0015, critério 8): nos dois caminhos, mesmos comandos.**
  `prebuild` = `npm run validate:content && npm run audit:content` protege o caminho de
  **publicação** (viaja com o repositório, funciona em qualquer host); os mesmos dois scripts
  são passos do Actions, que protege o **merge**. Só-CI foi descartado: a Vercel constrói o
  que foi empurrado e **não lê** o resultado do Actions. **`audit-content.sh` entrou no
  `prebuild` só no REJECT [006]** — sem ele, nó `languages: ["pt-BR"]` era publicado com o CI
  vermelho ao lado, porque `validate-content.sh` não enxerga paridade bilíngue. Custo
  assumido: erro editorial agora derruba deploy, não só merge.
- **Rede de segurança no leitor:** `src/content-contract/loadNode` falha alto se o nó não
  declarar os dois idiomas do contrato — camada que sobrevive a alguém trocar o
  `buildCommand` ou remover o `prebuild`.
- **Três passos de guarda no CI**, cada um com alvo conferido antes da busca: independência
  do contrato de dados, ausência de recurso de terceiro em `dist/` e ausência de rota em
  caixa mista. São as três consequências falseáveis do `ADR-0007`, agora todas com guarda.
- `vercel.json` tem só `installCommand`, `buildCommand` e `outputDirectory`. `buildCommand:
  npm run build` é obrigatório — se a Vercel chamar `astro build` pelo preset do framework, o
  `prebuild` (o portão) é pulado. Sem `rewrites`, `redirects`, `cleanUrls`, `trailingSlash`,
  `crons`, `functions`, Analytics ou Speed Insights.
- **Correção de 2026-08-01 (TCK-0011):** a stack **não** está indefinida — `ADR-0003` foi
  **aceito** em 2026-08-01 (site estático com ilhas, local-first sem conta, deploy estático na
  Vercel, portátil para qualquer host de arquivos).
- **`ADR-0006` e `ADR-0007` foram aceitos em 2026-08-01** (Douglas Silva, TCK-0016): ticket
  pode criar e alterar pipeline e configuração de publicação com base neles. Das pendências
  desta área, a 1 (**lugar e runtime do validador no caminho de publicação**) **continua sendo
  decisão do ticket** — o aceite não a puxou para o ADR; o TCK-0015 a exerceu (`prebuild` +
  passo no Actions) e verificou em contêiner. A 2 (**proteção de branch em `main`**) segue
  pendente e é ato do usuário — sem ela, o portão de merge é informativo. A 3 foi **fechada**:
  previews por PR **ativados**, decisão do usuário no aceite.
- Observabilidade de sessão (TCK-0012): `tools/context-watch.py` mede o consumo de contexto
  do Claude Code; hooks `PostToolBatch` e `PreCompact` em `.claude/settings.json`;
  `tools/agent-handoff.sh snapshot` grava o estado real antes da compactação.

## Pegadinhas conhecidas

*(verificadas em 2026-08-01, Claude Code 2.1.220)*

### Build, host e pipeline da aplicação (TCK-0015)

- **`grep` em passo de CI tem três desfechos, não dois:** `0` achou, `1` limpo, `2` erro
  (inclusive alvo inexistente). `if grep …; then falha; fi` imprime "OK" no caso 2 — o passo
  fica verde exatamente quando o alvo que ele vigia desaparece. Padrão em vigor no workflow:
  `test -d` no alvo, contagem de objetos > 0, e `case "$rc" in 0) reprova;; 1) aprova;; *)
  reprova por inconclusão;; esac`.
- **Passo de CI se prova executando o texto versionado**, não uma paráfrase: dá para extrair
  o bloco `run: |` do próprio `.yml` por script (recorte por indentação; a stdlib do Python
  não tem YAML) e rodar cada cenário — alvo real, alvo ausente, alvo vazio, alvo sujo.
- **Padrão de busca de terceiro precisa mirar o que carrega recurso**, não qualquer
  `https://`: quando a teoria for renderizada, links de `references.json` são conteúdo
  legítimo e derrubariam o pipeline. **E precisa cobrir a classe inteira** — a primeira
  versão específica deixou 8 de 18 vetores passarem (REJECT [010]). Em vigor, com `-i`:
  `<script|<iframe|<object|<embed`, `@font-face`, `@import`, `.woff`, `url((https?:)?//`,
  `(src|data|poster|action|formaction|background|ping)=(https?:)?//`, `srcset` com candidato
  externo, `href` de `<link>`/`<image>`/`<use>`, `http-equiv=refresh` para fora, e nomes de
  rastreadores. Protocolo relativo (`//host`) e caixa alta são obrigatórios — HTML é
  case-insensitive e pixel clássico não escreve o esquema.
- **`public/` é vetor de terceiros:** o que está lá é copiado **verbatim** para `dist/` sem
  passar por nenhuma página. Um `.html` legado ali publica script remoto com a aplicação
  inteira limpa. O passo de CI inspeciona `dist/`, não `src/`, exatamente por isso.
- **Dívida conhecida do passo de terceiros:** fonte auto-hospedada (`@font-face` + `.woff` da
  própria origem, permitida pelo `ADR-0007`) vai reprovar. Refinar no ticket de tipografia,
  no próprio passo — nunca afrouxar a classe para destravar.
- **Ordem do `prebuild` é load-bearing:** `validate:content && audit:content`. Com `content/`
  ausente ou vazio o auditor sozinho devolve `0` ("nada a auditar"); quem barra é o validador,
  que sai `2` antes e faz o `&&` cortar. Inverter, ou trocar `&&` por `;`, publica site vazio
  em silêncio. Registrado na chave `"//"` do `package.json`, que é onde alguém quebraria isso.
- **A imagem de build da Vercel documenta Python 3.14/3.13/3.12** na tabela *Runtime × Build
  image* de <https://vercel.com/docs/builds/build-image>; a lista de pacotes `dnf` da mesma
  página **não é o inventário do runtime** (ela também não cita o Node). Ler a página inteira
  antes de declarar ausência de uma dependência.

- **`import.meta.url` mente depois do empacotamento.** `new URL('../../content/',
  import.meta.url)` parece o jeito certo de achar o acervo a partir de `src/`, mas o
  empacotador do gerador move o módulo para `dist/.prerender/chunks/` e a URL passa a apontar
  para lá — o acervo "some" com `acervo não encontrado em .../dist/content/`, sem que o
  contrato tenha mudado. Custou uma build quebrada. Receita: achar a raiz **subindo do
  `cwd`** até o diretório que tenha `package.json` **e** `content/`. Vale para qualquer módulo
  de dado que o gerador vá empacotar.
- **A imagem de build da Vercel é Amazon Linux 2023** (<https://vercel.com/docs/builds/build-image>),
  e `python3` **não** está na lista de pacotes pré-instalados publicada — mas a base tem
  `python3` **3.9.25** e `bash` 5.2. Verificado rodando a cadeia inteira em
  `docker run --rm amazonlinux:2023` + `dnf -y install nodejs22` (Node v22.23.1): `npm ci`,
  `prebuild` (validador em Python) e build passam. A 3.9 executa `scripts/validate-content.py`
  porque ele tem `from __future__ import annotations` — sem isso, `X | None` em assinatura
  quebraria em 3.9. **Qualquer script Python novo no caminho de build precisa dessa linha.**
- **`engines.node` aceita faixa semver na Vercel** e resolve para o maior major disponível:
  `>=22.12.0` → 24.x (tabela em
  <https://vercel.com/docs/functions/runtimes/node-js/node-js-versions>, 2026-08-01). Não é
  preciso trocar para `22.x`.
- **`buildCommand` explícito no `vercel.json` não é enfeite:** o preset de framework da Vercel
  pode chamar o binário do gerador direto, e aí o `prebuild` do npm — que é o portão do
  acervo — **não roda**. Portão que depende de lifecycle do npm exige que o host passe pelo
  npm.
- **Build derrubada deixa `dist/` parcial** (chunks intermediários e o que veio de `public/`),
  mas **zero `.html`**. Não confundir "diretório existe" com "publicou": na Vercel, saída
  diferente de zero é deployment falho e nada é servido. Ao provar um portão, verificar
  `find dist -name '*.html' | wc -l`, não a existência de `dist/`.
- **O gerador tem telemetria anônima de build ligada por padrão** (aviso na primeira
  execução). Os scripts `dev`/`build`/`preview` exportam `ASTRO_TELEMETRY_DISABLED=1` —
  `astro telemetry disable` só valeria para a máquina de quem rodou, e não alcança CI nem host.
- **Nada de `vercel login`/`link`/`build`/`deploy` a partir de agente:** são interativos. A
  integração Git já existe do lado da Vercel; produção sai do push em `main` (ato do usuário).

- **Recarga de hooks:** o watcher de settings só observa diretórios que já tinham arquivo de
  settings **quando a sessão começou**. Editar `.claude/settings.json` no meio da sessão não
  garante hook ativo: é preciso abrir `/hooks` (recarrega) ou reiniciar. Um agente não
  consegue provar a ativação sozinho pela UI — `/hooks` é do usuário. Não afirmar "está
  ativo" sem prova; dizer o que foi provado (pipe-test + `jq -e`).
  **Adendo (QA de TCK-0012, 2026-08-01): dá para provar por efeito colateral.** Se o hook
  escreve arquivo (aqui, o estado de zona em
  `${XDG_STATE_HOME:-~/.local/state}/mathematics-studies/context-zone-<session>.json`), basta
  observar o `updated_at`/mtime avançar **em lockstep com os lotes de ferramenta, sem
  invocação manual do script** — foi assim que o `PostToolBatch` ficou provado ativo nesta
  sessão (1785610758 → 1785610768 → 1785610776). Vale só para hooks com efeito colateral
  observável: o `PreCompact` continua não provável sem provocar uma compactação real.
- **Arquivo de configuração gitignored falsifica validação e revisão.**
  `.claude/settings.local.json` é lido **primeiro** por `resolve_window` e não aparece em
  `git status` nem em diff nenhum. Quem for medir/validar comportamento default tem de
  movê-lo para fora e restaurá-lo depois (conferindo por `diff` contra a cópia). Regra geral:
  antes de validar ferramenta que lê configuração, listar os arquivos ignorados que ela
  consulta.
- **`settings.json` malformado desativa o arquivo inteiro em silêncio** — inclusive
  `permissions`. Sempre validar com `jq -e` depois de editar, e conferir que o `git diff`
  não removeu blocos existentes.
- **Exit code de hook tem semântica:** `2` bloqueia a ação. Watcher/observador deve sair `0`
  em todos os caminhos, inclusive em erro. Saída visível ao usuário: uma linha JSON com
  `systemMessage` no stdout.
- **Python sai 120 quando falha o flush do stdout no shutdown** (`| head`, `| true`,
  `> /dev/full`) — acontece *depois* do seu `try/except`, então não adianta proteger só o
  `main()`. Receita: escrever **e** dar `flush()` dentro do `try`, redirecionar o fd para
  `os.devnull` com `dup2` quando quebrar, e dar um último `flush` protegido antes do
  `sys.exit`. Sem isso, "o hook sai 0 sempre" é falso e ninguém percebe.
- **Com o fd fechado pelo shell (`>&-`), `sys.stdout` é `None`** — não um arquivo quebrado:
  a exceção é `AttributeError`, que não está em `(BrokenPipeError, OSError, ValueError)`, e
  a limpeza pós-`except` volta a derrubar o processo. Matriz mínima de E/S para qualquer
  ferramenta de hook: `| head`, `| true`, `> /dev/full`, `>&-`, `2>&-`, stdin fechado,
  stdin lixo, stdin binário. Baseline honesto: `python3 -c 'print("x")' >&-` sai `0`.
- **Suíte de teste precisa isolar `HOME`**, não só o diretório de dados: qualquer código que
  leia `~/.claude/settings.json` (ou `~/.config/…`) faz o teste passar/falhar conforme a
  máquina. O CI fica verde por acidente (runner sem `~/.claude`) e quebra para quem seguiu a
  documentação do próprio projeto.
- **Transcript da sessão** (`~/.claude/projects/<cwd-com-barras-viradas-em-hífen>/<session>.jsonl`):
  - `message.model` vem como `claude-opus-5` **mesmo em sessão de 1M** — a variante `[1m]`
    não está lá (aparece só, por acidente, em `toolUseResult.resolvedModel`). Logo, deduzir
    a janela pelo modelo é chute; declare a janela da máquina em
    `.claude/settings.local.json` (`{"autoCompactWindow": <tokens>}`) — é o único lugar que
    alcança terminal, hook e `snapshot` ao mesmo tempo. **`CONTEXT_WINDOW` exportado no shell
    não chega ao hook**, que é lançado pelo Claude Code: usar a variável só para teste
    pontual. Quando o chute é inevitável, ele é **conservador** (200k), é abandonado assim
    que a medida o refuta (`usado > janela` → sobe um degrau, origem `refutado:…`) e é
    declarado no canal automático — L-015, L-017.
  - Pode haver **vários** `.jsonl` no mesmo diretório de projeto (uma sessão cada). O
    caminho confiável é o `transcript_path` que o hook entrega no stdin; `mtime` é fallback.
  - Mensagens de subagente têm `isSidechain: true` e não contam para o contexto da thread
    principal — que é o que a compactação atinge.
  - O arquivo contém a **conversa inteira**: qualquer ferramenta que o leia trata isso como
    requisito de segurança (só contagens e metadados na saída).
- **`~/.claude/settings.json` é do usuário**, não do repositório: já tem um hook
  `PreToolUse` em `Bash` (`rtk hook claude`). Não editar a partir de tarefas do projeto.

## Decisões operacionais em vigor

- Custo zero: nenhuma telemetria sai da máquina; nenhum serviço externo. As ferramentas de
  observação usam só bash + Python 3 da stdlib. **Inclui a telemetria de build do gerador**,
  desligada por variável nos scripts do `package.json`.
- **Portão de conteúdo em todo caminho que chega ao aluno** (TCK-0015): `prebuild` para a
  publicação, passo do Actions para o merge, mesmo comando nos dois. Falha é sempre
  **fechada** — sem Python no ambiente, a build cai; nunca "pula a validação para destravar".
- **Configuração de host sem recurso proprietário:** só o que existe em qualquer host
  estático (comando de instalação, comando de build, diretório de saída). Redirect, rewrite,
  função ou analytics do fornecedor exige ADR — quebram a portabilidade que o `ADR-0003`
  comprou.
- **Nada de biblioteca de UI, de teste ou de PWA no `package.json`** sem ticket que decida o
  assunto (`ADR-0007`): cada dependência que chega ao navegador precisa de justificativa no
  log e revisão do `security-auditor`.
- Testes de ferramentas internas: script bash com fixtures em `mktemp -d`, executável no CI
  sem instalar nada (`tools/context-watch-test.sh` é o modelo).
- Estado efêmero de ferramenta (última zona de contexto etc.) vive em
  `${XDG_STATE_HOME:-~/.local/state}/mathematics-studies/` — nunca no working tree.
- Artefatos de handoff (`.agent-handoff.md`, `.agent-handoff.prev.md`) são gitignored.
- **`permissions` em `.claude/settings.json` não se amplia por conta própria** (L-016):
  entrada nova em `allow` é pedido ao usuário, não efeito colateral de entrega de tooling.
  Prova de preservação:
  `diff <(git show HEAD:.claude/settings.json | jq -S .permissions) <(jq -S .permissions .claude/settings.json)`.
- **Monitor que adivinha limiar adivinha pessimista** (L-015) e declara a dúvida no canal
  automático, com no máximo um aviso por sessão.

## Validação do primeiro deploy — o que ficou provado e o que ficou aberto (TCK-0015, 2026-08-01)

Validado por `qa-validator#12` no commit `aee5d3d`. O artefato publicável é **4 arquivos,
3 páginas, ~2,2 KB cada, zero JavaScript, zero requisição externa**. O que a validação
estabeleceu como fato operacional para os próximos tickets de infra:

- **O portão do RF-18 derruba a build de verdade, não só em teoria.** Quatro fixtures
  (`id` divergente · monolíngue `published` · monolíngue `draft` · teoria ausente) →
  `npm run build` ≠ 0 e **`dist/` sequer é criado**. O modo de falha do deploy é build
  vermelha, nunca publicação silenciosa. Vale repetir esse teste a cada mudança no `prebuild`.
- **A conjunção do `prebuild` é load-bearing; a ordem não.** Medido nos quatro cenários com
  `content/` vazio: `validate && audit` = 2 · `audit && validate` = 2 · `validate ; audit` =
  **0 e publica um site vazio**. Ao mexer no `prebuild`, o que não se pode perder é o `&&`.
- **O passo "HTML publicado sem recurso de terceiro" fecha a classe de erro ordinário e tem
  7 furos conhecidos** (`<base href>`, `report-uri` de CSP em `<meta>`, `manifest.webmanifest`
  com ícone externo, e `fetch`/`import()`/`WebSocket`/`EventSource`/`XMLHttpRequest` dentro de
  chunk `.js` emitido). Dois deles **não** têm gatilho automático: o primeiro
  `<link rel="manifest">` (aprova hoje, medido) e o primeiro `<meta http-equiv="Content-Security-Policy">`.
  Ao editar o padrão, refazer a bateria dos **dois lados** e acrescentar `<base>`.
- **O passo vai ficar vermelho no primeiro ticket de interatividade, não no de tipografia.**
  Medido: `<script src="/_astro/…">`, registro de service worker, `<iframe>` e `<embed>` de
  mesma origem e `@font-face` auto-hospedada — todos permitidos pelo `ADR-0007` — **reprovam**.
  É a revisita forçada; ao liberá-los, o conteúdo do chunk `.js` vira o novo ponto cego.
- **Ponto cego que não está no repositório: analytics do painel.** Vercel Web Analytics e
  Speed Insights se ligam no dashboard e injetam script na borda **sem mudança no Git** — o
  passo de CI inspeciona `dist/` e nunca veria. Verificação obrigatória depois do primeiro
  deploy, contra a URL pública:
  `curl -s https://mathematics-studies.vercel.app/ | grep -icE '/_vercel/|insights'` → **0**.
- **Rotas publicadas hoje:** `/`, `/pt-br/high-school/algebra/quadratic-equations` e
  `/en-us/…`. `/pt-br/`, `/en-us/`, `/pt-br/high-school` e qualquer caixa mista → **404**.
  **Não existe `404.astro`**, então o 404 é o genérico do host (monolíngue, sem volta para `/`).
- **Fixture hostil de infra roda em cópia isolada da árvore** (`tar` da raiz para o
  scratchpad + `npm ci` próprio), nunca no working tree compartilhado — e a cópia num caminho
  absoluto diferente serve, de graça, como prova de portabilidade da build.
