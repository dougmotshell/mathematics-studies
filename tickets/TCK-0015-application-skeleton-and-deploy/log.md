# Log — TCK-0015

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 16:10 — tech-lead
- Ação: ticket criado a partir de pedido direto do usuário ("configure tudo para o deploy" +
  "implemente o projeto base e já inicie o desenvolvimento da plataforma").
- Motivo: o repositório está conectado à Vercel (`https://mathematics-studies.vercel.app`),
  mas não existe aplicação — nenhum `package.json`, nenhum esqueleto. Configurar deploy sem
  aplicação não é possível; as duas coisas são a mesma entrega.
- Ambiente verificado antes de triar: Node v24.14.1 (atende `engines.node >= 22.12.0` do
  ADR-0007), npm 11.11.0, Vercel CLI 58.4.4, sem `.vercel` local (integração via GitHub).
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 16:10 — tech-lead
- Ação: triagem. Tipo `infra`, P1, tamanho M, owner `devops-engineer`.
- Motivo do recorte: entrega o **pipeline provado com página mínima**, não a interface. O
  índice, o leitor e o player são as tasks 5–8 da spec, com o `frontend-developer`. Misturar
  as duas coisas tornaria a revisão impossível de fazer com rigor.
- Decisões humanas incorporadas (2026-08-01): projeto na raiz; URL com prefixo de idioma
  minúsculo; previews por PR ativados.
- Nota sobre os ADRs `proposed`: `ADR-0006` e `ADR-0007` seguem `proposed` e o aceite formal é
  ato do usuário em ticket próprio. O usuário autorizou **executar** o que eles especificam —
  isso não os torna aceitos, e o ticket não os altera.
- Ponto que o REJECT do TCK-0011 devolveu para cá: **onde a validação do RF-18 roda** é
  decisão de implementação, não de ADR (L-020). Este ticket decide, no critério 8.
- Restrições: sem biblioteca de UI, de teste ou de componente; sem recurso proprietário que
  quebre a portabilidade; zero coleta de dados no HTML publicado; `content/` intocado.
- Resultado: ok — `triaged`.

## [003] HANDOFF — 2026-08-01 16:10
- De: tech-lead → Para: devops-engineer
- Status novo: in_progress
- O que foi feito: ambiente verificado, escopo recortado, decisões humanas incorporadas.
- Artefatos: `tickets/TCK-0015-application-skeleton-and-deploy/ticket.md`.
- Como validar: critérios 1–13; build local, fixture inválida derrubando o build, e inspeção
  do HTML gerado.
- Pendências e riscos: push na `main` dispara deploy de produção pela integração existente —
  o commit é do orquestrador e sai só após validação; o `vercel login` é interativo e, se for
  necessário, quem executa é o usuário.
- Critérios de aceite: [ ] 1–13 restantes.

## [004] ACTION — 2026-08-01 17:10 — devops-engineer
- Ação: criado o esqueleto do `ADR-0007` e o pipeline do `ADR-0006`, com a cadeia
  acervo → validação → build → HTML publicável provada ponta a ponta.
- Arquivos criados: `package.json`, `package-lock.json`, `astro.config.mjs`, `vercel.json`,
  `public/robots.txt`, `src/content-contract/{index.js,languages.js}`,
  `src/layouts/BaseLayout.astro`, `src/pages/index.astro`,
  `src/pages/[lang]/[...node].astro`, `src/styles/base.css`,
  `src/components/README.md`, `src/islands/README.md`.
  Alterados: `.github/workflows/ai-surface-audit.yml`, `.gitignore` (`+.astro/`).
  **Não** tocados: `content/`, ADRs, spec, `docs/`, `.claude/`, `AGENTS.md`.

### Decisão do critério 8 — onde o portão do RF-18 roda

**Escolha: nos dois caminhos, com o mesmo comando.** `prebuild` (`npm run validate:content`
→ `bash scripts/validate-content.sh`) no caminho de **publicação**, e um passo nomeado no job
do Actions no caminho de **merge**.

- **Por que não só no CI (alternativa descartada):** a Vercel constrói o que já foi
  empurrado e **não lê o resultado do Actions**. Um push direto em `main` — que o próprio
  `ADR-0006` reconhece como caminho real, já que a proteção de branch ainda não existe
  (pendência 2, ato do usuário) — publicaria acervo reprovado com o CI vermelho ao lado.
  Um portão que não está no caminho não é portão.
- **Por que não só no `prebuild`:** ele não reprova o PR antes do merge, e o `ADR-0006`
  quer o Actions como portão de mérito.
- **Por que o `prebuild` e não `buildCommand` da Vercel:** o `prebuild` viaja com o
  repositório. Trocar de host (Netlify, Cloudflare Pages, GitHub Pages) mantém o portão;
  configuração no painel do fornecedor, não.
- **Falha é fechada, nunca aberta:** se o `python3` não existir no ambiente de build, o
  `prebuild` **derruba a build** e nada é publicado — o modo de falha correto. Nenhum
  caminho "pula a validação para destravar".

**A pendência 1 do `ADR-0006` (Python + Node no mesmo ambiente de build) foi verificada, não
presumida.** A documentação da Vercel diz que a imagem de build usa **Amazon Linux 2023** como
base (<https://vercel.com/docs/builds/build-image>, consultado em 2026-08-01) — e `python3`
**não** aparece na lista de pacotes pré-instalados de lá, o que impedia afirmar qualquer coisa
por leitura. Rodei a cadeia inteira nessa base:

```
$ docker run --rm -v <cópia do repo>:/repo -w /repo amazonlinux:2023 sh -c \
    'dnf -y install nodejs22 >/dev/null 2>&1; npm ci; npm run build'
runtime: node v22.23.1 · npm 10.9.8 · Python 3.9.25 · GNU bash
> mathematics-studies@0.0.0 prebuild
Contrato íntegro: 1 nó(s) validado(s), 0 violações.
  ├─ /pt-br/high-school/algebra/quadratic-equations/index.html (+16ms)
  ├─ /en-us/high-school/algebra/quadratic-equations/index.html (+2ms)
  ├─ /index.html (+3ms)
[build] Complete!   --- exit=0
```

Python 3.9 do sistema executa o validador sem erro (ele tem `from __future__ import
annotations`, então a sintaxe `X | None` das anotações não é avaliada). Node 22.23.1 atende o
piso `>= 22.12.0`. **Ressalva honesta:** isto é a *imagem-base documentada*, não a imagem da
Vercel — a prova definitiva é o primeiro deploy, e o modo de falha dele é build vermelha com
mensagem clara, não publicação silenciosa de acervo inválido.

### Verificações (comando + saída real)

**Critério 7a — acervo válido:**
```
$ npm run build
> prebuild → validate:content → Contrato íntegro: 1 nó(s) validado(s), 0 violações.
  ├─ /pt-br/high-school/algebra/quadratic-equations/index.html (+11ms)
  ├─ /en-us/high-school/algebra/quadratic-equations/index.html (+2ms)
  ├─ /index.html (+2ms)
[build] 3 page(s) built in 237ms · Complete!        exit=0
```

**Critério 7b — fixture inválida derruba o build.** Fixture A em
`content/high-school/algebra/invalid-fixture/meta.json` (`id` divergente do caminho e `title`
sem `en-US`), removida depois do teste:
```
$ rm -rf dist && npm run build
[META-ID-MISMATCH] meta.json.id é 'high-school/algebra/wrong-id' mas o nó está em
  'high-school/algebra/invalid-fixture' — … (RF-17)
[LOCALIZED-MISSING-LANG] campo 'title' sem a chave 'en-US' — paridade bilíngue é obrigatória
CONTRATO VIOLADO: 2 violação(ões) em 2 nó(s).
### exit code de 'npm run build' com acervo inválido = 1
### dist existe? NAO - nada foi gerado
```

**Critério 7c — a rede de segurança também derruba.** Fixture B (nó que **passa** no
validador — ele não cobre `theory.<lang>.md` — mas que o leitor não consegue montar):
```
$ bash scripts/validate-content.sh      → Contrato íntegro: 2 nó(s), 0 violações.  exit=0
$ npm run build
[content-contract] nó 'high-school/algebra/missing-theory-fixture' declara o idioma 'pt-BR'
  mas não tem theory.pt-BR.md
    exit code de 'npm run build' = 1
```
Observação para o review: a build derrubada **deixa um `dist/` parcial** com os chunks
intermediários do gerador e `robots.txt`, mas **0 arquivos `.html`** — e, na Vercel, saída
diferente de zero significa deployment falho: nada é servido. Registrado por transparência,
não como defeito.

Acervo intacto depois dos dois testes: `git status --porcelain -- content/` → vazio.

**Critério 3 — o leitor não conhece o gerador:**
```
$ grep -rn 'astro' src/content-contract/                  → (vazio)
$ grep -rniE 'astro|@astrojs|vite' src/content-contract/  → (vazio)
$ grep -rhn '^import' src/content-contract/
  import { readFileSync, readdirSync, statSync } from 'node:fs';
  import { dirname, join, posix, resolve, sep } from 'node:path';
  import { LANGUAGES, isLanguage, urlSegmentOf } from './languages.js';
```
Prova positiva (o módulo roda em Node puro, sem o gerador no caminho):
```
$ node --input-type=module -e "import {loadAllNodes,routesOf} from './src/content-contract/index.js' …"
CONTENT_ROOT = /home/douglas-silva/www/mathematics-studies/content
high-school/algebra/quadratic-equations | status: draft | idiomas: pt-BR,en-US
  | teoria(bytes): 6055/5894 | itens: 5
   rotas: /pt-br/high-school/algebra/quadratic-equations  /en-us/high-school/…
```
O nome do gerador **não aparece nem em comentário** dentro de `src/content-contract/` — senão
o `grep` que o `ADR-0007` nomeia como teste falseável passaria a acusar o próprio comentário.
O CI executa esse `grep` como passo bloqueante.

**Critérios 4 e 5 — URL:** servida por `npm run preview`:
```
/                                               -> 200
/pt-br/high-school/algebra/quadratic-equations  -> 200
/en-us/high-school/algebra/quadratic-equations  -> 200
/pt-BR/high-school/algebra/quadratic-equations  -> 404   (caixa mista não resolve, como decidido)
$ find dist -path '*[A-Z]*'   → (vazio: nenhuma rota emitida com maiúscula)
$ grep -oh '<html lang="[^"]*"' …  → lang="pt-BR" · lang="en-US" · lang="pt-BR" (raiz)
```
O caminho do nó aparece sem tradução e sem normalização; `pt-BR`/`en-US` seguem sendo a chave
no dado e no atributo `lang` — minúsculo só na URL.

**Critério 12 — HTML gerado, não intenção:**
```
$ find dist | sort
dist/index.html · dist/pt-br/high-school/algebra/quadratic-equations/index.html
dist/en-us/high-school/algebra/quadratic-equations/index.html · dist/robots.txt
$ grep -rInE 'https?://|<script|@font-face|\.woff2?|<iframe|analytics|gtag|pixel|beacon' dist/
    (nenhuma ocorrência)
```
Zero JavaScript emitido, zero requisição externa, CSS embutido no `<head>`, pilha de fontes
do sistema. Achado do caminho: o gerador imprimia aviso de **telemetria anônima de build** na
primeira execução; os scripts `dev`/`build`/`preview` passaram a exportar
`ASTRO_TELEMETRY_DISABLED=1` — telemetria de build não chega ao aluno, mas "nenhuma telemetria
sai da máquina" é decisão em vigor em `memory/context/devops.md`. O passo
"HTML publicado sem recurso de terceiro" no CI transforma este critério em verificação
permanente.

**Critério 13:**
```
$ bash scripts/audit-ai-surface.sh   → Resultado: OK                                  exit=0
$ bash scripts/audit-content.sh      → Resumo: 1 nós · 0 erros · 0 avisos             exit=0
$ bash scripts/validate-content.sh   → Contrato íntegro: 1 nó(s), 0 violações         exit=0
```

**Build de verificação equivalente ao do CI** (mesmos comandos, mesma ordem, após
`rm -rf dist node_modules`): `audit-ai-surface` ok · `sync-ai-adapters --check` ok ·
`audit-content` ok · `context-watch-test` 93 passaram, 0 falharam · `validate-content` ok ·
`npm ci` ok · grep de independência vazio · `npm run build` 3 rotas · grep de terceiros vazio.

### Notas de configuração e ambiente

- `vercel.json` tem só `installCommand`, `buildCommand` e `outputDirectory` — três conceitos
  que existem em qualquer host estático. **Nenhum recurso proprietário**: sem `rewrites`,
  `redirects`, `cleanUrls`, `trailingSlash`, `crons`, `functions` nem Analytics/Speed
  Insights. `buildCommand: npm run build` é o que garante que o `prebuild` rode no host (se a
  Vercel chamasse `astro build` direto pelo preset do framework, o portão seria pulado).
- `engines.node: ">=22.12.0"` é aceito pela Vercel como faixa semver e resolve para o
  **24.x** (tabela em <https://vercel.com/docs/functions/runtimes/node-js/node-js-versions>,
  consultada em 2026-08-01) — não é o formato inválido que quebra deploy.
- Nenhum segredo, nenhuma variável de ambiente nova, nenhum `.env`:
  `grep -rn "secrets\." .github/workflows/` continua vazio.
- O **nome do arquivo** do workflow foi mantido (`ai-surface-audit.yml`) porque `ADR-0006`,
  `memory/context/devops.md` e tickets fechados o citam, e este ticket não pode editar ADR.
  Só o `name:` exibido mudou.
- Pegadinha nova, custou uma build quebrada: `new URL('../../content/', import.meta.url)`
  **não** resolve para o código-fonte depois que o empacotador move o módulo para dentro do
  diretório de build (`dist/.prerender/chunks/…`), e o acervo "some". A raiz passou a ser
  encontrada subindo do `cwd` até o diretório que tenha `package.json` **e** `content/`.
  Candidata a lição — o ID fica com o `retrospective-curator` para não colidir com os agentes
  que estão editando `memory/LESSONS.md` agora.
- Reversão: apagar `package.json`, `package-lock.json`, `astro.config.mjs`, `vercel.json`,
  `src/`, `public/` e reverter os dois arquivos alterados devolve o repositório ao estado
  anterior — o acervo nunca dependeu deles. Desligar a publicação é desconectar o projeto no
  painel; voltar uma versão é *Instant Rollback* na Vercel (promover o deployment anterior).
- **Não executado de propósito:** `vercel login`, `vercel link`, `vercel build` e `vercel
  deploy`. Todos exigem sessão interativa; a integração Git já existe do lado da Vercel e o
  deploy de produção sai do push na `main`, que é ato do usuário/orquestrador.
- Restrições respeitadas: `dependencies` = apenas `astro`; `devDependencies` vazio; nenhuma
  biblioteca de UI, de teste ou de componente; `npm audit` = 0 vulnerabilidades.
- Resultado: ok — critérios 1–13 executados e verificados com saída anexada.
- Lição: n/a — nenhum `REJECT` a resolver nesta entrada.

## [005] HANDOFF — 2026-08-01 17:15
- De: devops-engineer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: esqueleto do `ADR-0007` na raiz (manifesto, configuração do gerador,
  leitor do acervo independente, layout, duas rotas por idioma e a raiz de escolha de idioma),
  pipeline do `ADR-0006` no workflow existente (validador, build de verificação, grep de
  independência do contrato de dados e grep de terceiros no HTML), `vercel.json` portátil e
  `.gitignore` completo. Portão do RF-18 decidido para os **dois** caminhos (`prebuild` +
  Actions), com a pendência 1 do `ADR-0006` verificada em contêiner Amazon Linux 2023.
- Artefatos: `package.json`, `package-lock.json`, `astro.config.mjs`, `vercel.json`,
  `public/robots.txt`, `src/**`, `.github/workflows/ai-surface-audit.yml`, `.gitignore`.
  Sem commit e sem push — push na `main` dispara produção.
- Como validar:
  `npm ci && npm run build` · `find dist` · `grep -rInE 'https?://|<script|@font-face' dist/`
  · `grep -rniE 'astro|@astrojs|vite' src/content-contract/` (vazio) ·
  `bash scripts/audit-ai-surface.sh` · `bash scripts/audit-content.sh` ·
  `bash scripts/validate-content.sh` · fixture inválida em `content/` derrubando o build.
- Pendências e riscos:
  1. A imagem real de build da Vercel só é observável no primeiro deploy; provado na
     imagem-base documentada (AL2023 + Node 22 + Python 3.9). Falha, se houver, é build
     vermelha — não publicação de acervo inválido.
  2. Proteção de branch em `main` continua sendo ato do usuário (`ADR-0006`, pendência 2);
     sem ela o portão de merge é informativo.
  3. Previews por PR dependem da configuração do projeto no painel da Vercel (não está no
     Git); nada neste ticket os desliga.
  4. A página mínima **não é** o leitor de nó: ela some quando a task 6 entrar.
  5. `ADR-0006` e `ADR-0007` seguem `proposed` — este ticket os executou por autorização
     explícita do usuário, sem alterar status.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 ·
  [x] 9 · [x] 10 · [x] 11 · [x] 12 · [x] 13 — todos com evidência em `[004]`; nenhum
  restante.

## [006] REJECT — 2026-08-01 17:35 — code-reviewer#9
- De: code-reviewer#9 → Para: devops-engineer
- Status novo: in_progress · **loop 1/3**
- Escopo conferido: `git status --porcelain` limitado a `package.json`, `package-lock.json`,
  `astro.config.mjs`, `vercel.json`, `public/`, `src/`, `.github/workflows/ai-surface-audit.yml`
  e `.gitignore` — exatamente os artefatos declarados em `[005]`. `content/`, `docs/`,
  `docs/specs/`, `scripts/`, `tools/` e os ADRs intocados. As mudanças em `.claude/agents/*`,
  `.claude/skills/*` e `AGENTS.md` no working tree são do TCK-0006 (destinos do REJECT [006]
  daquele ticket), não deste.

### O que está bom (reexecutado por mim, não aceito do log)

- `npm ci` (0 vulnerabilidades) e `npm run build` → exit 0, 3 rotas, 4 arquivos em `dist/`.
- **Critério 3 provado no teste forte, não no `grep`:** importei
  `src/content-contract/index.js` em **Node puro** (v24.14.1, sem o gerador no caminho) e li o
  nó piloto — `CONTENT_ROOT` correto, `status: draft`, `pt-BR,en-US`, teoria 6055/5894 bytes,
  5 itens, rotas `/pt-br/…` e `/en-us/…`. Funciona também com `cwd` num subdiretório do repo e
  numa **cópia limpa do repositório em outro caminho absoluto** (`npm ci` + `npm run build`
  exit 0, 3 HTML) — a troca de `import.meta.url` pela subida a partir do `cwd` sobrevive ao
  empacotamento e ao CI.
- **Critério 8 — o `prebuild` dispara e derruba, testado, não configurado:** `npm run build`
  com fixture inválida → `CONTRATO VIOLADO: 3 violação(ões)`, **exit 1**, `dist/` inexistente,
  0 HTML. Repetido com `NODE_ENV=production` (o ambiente da Vercel) e na cópia limpa: mesmo
  resultado. `vercel.json:4` (`buildCommand: npm run build`) é o que liga o hook no caminho
  do host, e a decisão dos dois portões está corretamente justificada.
- **Critério 7c — a rede de segurança derruba:** fixture que **passa** no validador
  (exit 0, "2 nó(s), 0 violações") e não tem `theory.pt-BR.md` → build exit 1 com
  `[content-contract] … declara o idioma 'pt-BR' mas não tem theory.pt-BR.md`, `dist/` parcial
  com **0 HTML**. Confere com o declarado em `[004]`.
- **Critérios 4 e 5, medidos no `preview`:** `/` 200 · `/pt-br/high-school/algebra/quadratic-equations`
  200 · `/en-us/…` 200 · `/pt-BR/…` **404** · `/PT-BR/x` 404. `lang="pt-BR"`, `lang="pt-BR"`,
  `lang="en-US"` nas três páginas; `find dist -path '*[A-Z]*'` vazio no acervo atual.
- **Critério 12 conferido no HTML, não na intenção:** `grep -rInE 'https?://|<script|@font-face|\.woff2?|<iframe|analytics|gtag|pixel|beacon|fbq|clarity|hotjar|plausible|umami' dist/`
  → **nenhuma ocorrência**. Zero JavaScript emitido, CSS embutido no `<head>`, pilha de fontes
  do sistema. `ASTRO_TELEMETRY_DISABLED` confirmado como variável real do pacote de telemetria
  do gerador e presente nos três scripts que o invocam — é onde a Vercel e o CI leem, porque
  os dois chamam `npm run build`. Contraste conferido: texto 8,2:1 e link 11,4:1 sobre branco.
- **Critério 13 + portão de merge:** `audit-ai-surface.sh` OK · `audit-content.sh` 1 nó, 0
  erros · `validate-content.sh` 0 violações · `sync-ai-adapters.py --check` atualizado ·
  `context-watch-test.sh` 93/0 — todos exit 0. `grep -rn "secrets\." .github/workflows/` vazio.
- **Critérios 1, 2, 9, 11:** `private: true`, `engines.node >=22.12.0`, `dependencies` só
  `astro@^7.1.6`, `devDependencies` vazio; estrutura idêntica ao `ADR-0007` §3;
  `vercel.json` com três chaves portáteis e nenhum recurso proprietário; `.gitignore` cobre
  `node_modules/`, `dist/`, `.astro/` e `.vercel/`.
- **Fixtures removidas:** `git status --porcelain -- content/` → **vazio** ao fim da revisão.

### Bloqueantes

**B1 — nó sem paridade de idioma vira rota publicada; o portão que pega isso não está no
caminho de publicação.** `ADR-0006:93-94` (**accepted**) declara como salvaguarda: "nó sem
paridade de idioma continua **fora das rotas publicadas** (`ADR-0002`)" — e `AGENTS.md` §2b
proíbe publicar conteúdo monolíngue. Medido numa cópia do repositório, com um nó
`languages: ["pt-BR"]`, `status: "published"`, sem `theory.en-US.md`:

```
bash scripts/validate-content.sh   (roda no prebuild)      exit=0
bash scripts/audit-content.sh      (roda só no Actions)    exit=1
   ERRO  …/mono-pub  languages deve ser exatamente ['pt-BR', 'en-US'] (encontrado: ['pt-BR'])
   ERRO  …/mono-pub  theory.en-US.md ausente (bilinguismo obrigatório — ADR-0002)
   ERRO  …/mono-pub  status 'published' com teoria incompleta
npm run build      (caminho de PUBLICAÇÃO)                 exit=0
   publicado: dist/pt-br/high-school/algebra/mono-pub/index.html
```

O `routesOf` (`src/content-contract/index.js:254-259`) emite uma rota por idioma **declarado**,
então um nó que declara um só idioma ganha uma rota publicada sem que nada reclame. É o seu
próprio argumento do critério 8 aplicado ao portão que você deixou de fora: *"a Vercel constrói
o que já foi empurrado e não lê o resultado do Actions… Um portão que não está no caminho não é
portão"* (`log.md:61-66`). `validate-content.sh` ficou nos dois caminhos; `audit-content.sh` —
o único que enxerga a paridade bilíngue — ficou só no caminho de merge, que a pendência 2 do
`ADR-0006` reconhece como não bloqueante. Resultado: push direto em `main` publica conteúdo
monolíngue. A correção é sua escolha (encadear `audit-content.sh` no `prebuild`, ou fazer o
leitor falhar quando `languages` ≠ `LANGUAGES`, que é a "rede de segurança" que o `ADR-0007`
§5 promete), com a justificativa registrada.

**B2 — os dois passos novos de portão do CI imprimem "OK" quando o alvo não existe.**
`.github/workflows/ai-surface-audit.yml:73-78` e `:90-95`. `grep -r` sai **2** (erro) quando o
caminho não existe; `if grep …; then exit 1; fi` só dispara com exit **0**, então o `else`
implícito cai no `echo "OK: …"` e o passo passa verde. Reproduzido:

```
$ grep -rniE 'astro|@astrojs|vite' src/nao-existe/   ; echo $?
grep: src/nao-existe/: No such file or directory
2
  -> o passo imprimiria: "OK: src/content-contract/ não cita o gerador de site."
$ (com dist/ removido) grep -rInE 'https?://|<script|@font-face' dist/
  -> o passo imprimiria: "OK: nenhum recurso externo em dist/."
```

O cenário que o teste falseável do `ADR-0007:246-247` existe para pegar é justamente
`src/content-contract/` deixar de existir como módulo independente (renomeado, absorvido pelo
gerador) — e é exatamente nele que o portão fica cego. `L-019` ("um validador só protege o que
consegue enxergar") nomeia isto no "Como aplicar", literalmente para verificação de CI:
*"Testar o caminho vazio: alvo sem nenhum objeto encontrado nunca sai 0. 'Nada encontrado' é
erro de uso, não aprovação."* Erro com lição registrada → bloqueante (AGENTS.md §10, regra 7).
Correção: exigir que o alvo exista antes do `grep` (`test -d` / `test -n "$(find …)"`) e
separar "nada encontrado" de "diretório ausente".

**B3 — a página raiz publica duas frases coladas.** `src/pages/index.astro:36-37` gera, em
`dist/index.html`:

```
HTML : <span lang="pt-BR">Escolha o idioma.</span><span lang="en-US">Choose your language.</span>
TEXTO: 'Escolha o idioma.Choose your language.'
```

O compressor de HTML do gerador remove o espaço entre os dois `<span>` irmãos, e o resultado é
o texto visível de `/` — a primeira página do primeiro deploy de produção. Não mapeia num
critério de aceite, e é o mais barato dos três; entra como bloqueante porque é saída publicada
errada, não preferência de estilo. Um separador explícito (`{' '}`, `&nbsp;` ou dois blocos)
resolve.

### Sugestões (não bloqueiam)

- **S1 — a evidência da pendência 1 do `ADR-0006` é mais forte do que o log diz; corrija-a.**
  Na **mesma página** que você cita (<https://vercel.com/docs/builds/build-image>, consultada
  por mim em 2026-08-01) a tabela *Runtime × Build image* declara **"Python 3.14, 3.13, 3.12"**
  na imagem de build — logo o `python3` consta, sim, na documentação; o que não o lista é a
  lista de pacotes `dnf`, que também não lista o Node. E ele é **estruturalmente inevitável**:
  em `amazonlinux:2023` puro, **sem instalar nada**, `command -v python3` → `/usr/bin/python3`,
  `Python 3.9.25`, fornecido por `python3-3.9.25-1.amzn2023`, porque `dnf` requer
  `python3-dnf`. Some-se a isso que o validador já roda de fato em Python **3.12.3** (este
  ambiente) — a versão que a Vercel documenta. Registre por `CORRECTION`: o risco de build
  vermelha por falta de Python é menor que o declarado em `[004]:75-97`.
- **S2 — `engines.node: ">=22.12.0"` verificado e correto.** A tabela de
  <https://vercel.com/docs/functions/runtimes/node-js/node-js-versions> mapeia `>=20.0.0` →
  "latest 24.x version", então a faixa é aceita e resolve para 24.x. Nada a mudar; anotado
  porque a checagem valia por si.
- **S3 — a consequência falseável "nenhuma rota emitida contém letra maiúscula"
  (`ADR-0007:252-253`) não tem guarda automática.** Fixture com o nó em
  `content/high-school/algebra/Uppercase-Slug/`: `validate-content.sh` exit 0,
  `audit-content.sh` exit 0, `npm run build` exit 0, e `dist/pt-br/high-school/algebra/Uppercase-Slug/index.html`
  publicado. Você já deu passo de CI a dois dos três testes falseáveis do ADR; o terceiro cabe
  em uma linha (`find dist -path '*[A-Z]*'` tem de sair vazio). O buraco de origem (slug fora de
  kebab-case aprovado pelas duas ferramentas) é território do TCK-0014 — vale um apontamento ao
  `tech-lead`, não uma correção aqui.
- **S4 — `CONTENT_ROOT` é avaliado na carga do módulo** (`src/content-contract/index.js:110`).
  Com `cwd` fora do repositório o **import** já lança, mesmo que quem chame pretendesse passar
  `root` explícito em `loadAllNodes(root)`. Não afeta CI nem Vercel (ambos rodam com `cwd` na
  raiz — medido), mas torna o parâmetro `root` inutilizável fora do repo. Avaliação preguiçosa
  resolveria sem reintroduzir `import.meta.url`.
- **S5 — o `grep 'https?://'` sobre `dist/` vira vermelho na task 6**, quando a teoria passar a
  ser renderizada com links de `references.json`. Ou declare a dívida no comentário do passo, ou
  restrinja o padrão ao que de fato busca recurso (`<script src=`, `<link … href=`, `@font-face`,
  `url(`, `<img src=` externo).
- **S6 — `/pt-br/` e `/en-us/` devolvem 404** (medido): só existe rota de nó. É esperado até a
  task 5, mas convém dizer isso ao QA para não virar defeito de validação.
- **S7 — `<meta name="description">` de `/` só existe em pt-BR** (`src/pages/index.astro:32`),
  numa página cuja função é ser bilíngue. As páginas de nó não têm `description` nenhuma.
- **S8 — `ADR-0006` e `ADR-0007` passaram a `accepted`** (TCK-0016) depois do seu `[005]`: a
  pendência 5 do handoff está desatualizada e o trabalho agora se apoia em ADR aceito, não em
  autorização avulsa. Ajuste na próxima entrada.

- Como validar a correção: `npm run build` com nó `languages: ["pt-BR"]` tem de sair ≠ 0 (B1);
  os dois passos de CI têm de reprovar com o alvo ausente (B2); `dist/index.html` tem de
  separar as duas frases (B3). Refaça os critérios 7, 10 e 12 com a saída anexada.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [ ] 7 (B1) · [x] 8 ·
  [x] 9 · [ ] 10 (B2) · [x] 11 · [x] 12 · [x] 13.

## [007] CORRECTION — 2026-08-01 17:55 — devops-engineer
- Corrige: `[004]`, seção da pendência 1 do `ADR-0006`, e `[005]`, pendências 1 e 5.
- **S1 — a evidência de Python no ambiente de build era mais forte do que eu declarei.**
  Escrevi que "`python3` não aparece na lista de pacotes pré-instalados" e tratei isso como
  incerteza relevante. A leitura foi parcial: a **mesma página**
  (<https://vercel.com/docs/builds/build-image>) declara, na tabela *Runtime × Build image*,
  **Python 3.14, 3.13 e 3.12** — a lista `dnf` que eu citei também não menciona o Node, ou
  seja, ela não é o inventário do runtime. Some-se que `amazonlinux:2023` traz
  `/usr/bin/python3` **sem instalar nada** (dependência do próprio `dnf`), e que este
  ambiente roda o validador em Python 3.12.3. Onde `[004]` diz "a prova definitiva é o
  primeiro deploy", leia-se: **o risco de build vermelha por falta de Python é
  residual**; a verificação em contêiner permanece válida como reforço, não como a única
  fonte. Método corrigido para a próxima vez: ler a página inteira antes de declarar ausência
  — "não está na lista X" só vira risco depois de conferir se X é a lista certa.
- **S8 — `ADR-0006` e `ADR-0007` estão `accepted`** (TCK-0016, 2026-08-01), depois do meu
  `[005]`. A pendência 5 daquele handoff ("seguem `proposed`, executados por autorização
  avulsa") está **superada**: este trabalho se apoia em ADR aceito. Também passou a existir
  `.github/instructions/app.instructions.md` governando `src/**` — li e conferi a entrega
  contra ela antes de seguir.
- Resultado: ok — nenhuma mudança de código decorre desta entrada.

## [008] ACTION — 2026-08-01 18:05 — devops-engineer
- Ação: resolvidos B1, B2 e B3; incorporadas S3, S4, S5 e S7.
- Arquivos: `src/content-contract/index.js`, `src/pages/index.astro`,
  `src/pages/[lang]/[...node].astro`, `package.json`,
  `.github/workflows/ai-surface-audit.yml`. `content/`, `docs/` e `scripts/` intocados.

### B1 — paridade bilíngue passa a estar no caminho de publicação (defesa em duas camadas)

Aceitei o diagnóstico inteiro: apliquei o argumento do critério 8 a **uma** ferramenta e
deixei a outra fora do caminho. Fechei nos dois lugares que o `REJECT` ofereceu, porque eles
protegem coisas diferentes:

1. **Portão (`prebuild`)** — `audit-content.sh` entrou na cadeia:
   `"prebuild": "npm run validate:content && npm run audit:content"`. É a auditoria editorial
   que enxerga paridade, taxonomia, grafo de pré-requisitos e `status: published` incompleto;
   agora ela reprova **antes de publicar**, não só antes de mesclar. Custo aceito: erro
   editorial passa a derrubar deploy — que é exatamente o resultado exigido pelo RF-18
   ("acervo reprovado não vira página publicada"), e o mesmo runtime Python já provado.
2. **Rede de segurança (leitor)** — `loadNode` falha alto quando `languages` não traz os dois
   idiomas do contrato. Escolhi **falhar** em vez de **pular o nó**: pular seria o "fallback
   silencioso" que o `AGENTS.md` §2b proíbe — o acervo ficaria com um nó invisível que
   ninguém acusa. A camada existe porque o portão pode ser removido, renomeado ou pulado por
   um `buildCommand` diferente; o leitor não pode.

Evidência com a fixture do `REJECT` (`languages: ["pt-BR"]`, `status: "published"`, sem
`theory.en-US.md`), removida depois:
```
B1.1  bash scripts/validate-content.sh   (escopo RF-18, inalterado)          exit=0
B1.2  npm run build   (CAMINHO DE PUBLICAÇÃO)
      ERRO  high-school/algebra/mono-pub  languages deve ser exatamente ['pt-BR', 'en-US'] …
      ERRO  high-school/algebra/mono-pub  theory.en-US.md ausente (bilinguismo obrigatório — ADR-0002)
      ERRO  high-school/algebra/mono-pub  status 'published' com teoria incompleta
      Resumo: 2 nós · 5 erros · 0 avisos                                     exit=1
      dist existe? NAO - nada foi gerado
B1.3  npx astro build  (pulando o prebuild, para provar a 2ª camada sozinha)
      [content-contract] nó 'high-school/algebra/mono-pub' declara apenas [pt-BR] em
      'languages' — falta en-US. Paridade bilíngue é obrigatória e não há fallback
      (ADR-0002, AGENTS.md §2b); nó sem paridade não pode virar rota publicada (ADR-0006).
                                                                             exit=1
      rota monolíngue publicada? 0 arquivo(s) HTML
```

### B2 — os passos de CI deixam de aprovar o que não conseguiram olhar

Os dois passos passaram a (i) exigir que o alvo **exista**, (ii) exigir que ele **não esteja
vazio** e (iii) tratar o código de saída do `grep` em **três** casos (`0` achou → reprova;
`1` limpo → aprova; qualquer outro → reprova por inconclusão). O erro de origem foi tratar
`grep` como binário quando ele tem três desfechos.

Prova executada sobre o **texto versionado do próprio workflow** — os blocos `run:` foram
extraídos do arquivo por script e executados, não parafraseados:
```
PASSO 'Contrato de dados independente do gerador'
  A. repositório real                                  exit=0 aprova   OK: 2 módulo(s), nenhum cita o gerador
  B. src/content-contract AUSENTE (o cego de antes)    exit=1 REPROVA  ::error::… não existe — teste não pôde ser executado
  C. diretório existe mas sem módulo .js               exit=1 REPROVA  ::error::'nada encontrado' é erro de uso (L-019)
  D. leitor citando o gerador                          exit=1 REPROVA  ::error::o leitor do acervo cita o gerador (ADR-0003)
PASSO 'HTML publicado sem recurso de terceiro'
  A. dist real                                         exit=0 aprova   OK: 3 página(s), nenhuma carrega terceiro
  B. dist/ AUSENTE (o cego de antes)                   exit=1 REPROVA
  C. dist/ sem nenhum HTML                             exit=1 REPROVA
  D. <script src="https://cdn.exemplo.com/a.js">       exit=1 REPROVA
  E. <a href="https://openstax.org/…"> (conteúdo)      exit=0 aprova   ← S5: link de referência não reprova
  F. @font-face com url(https://fonts.gstatic.com/…)   exit=1 REPROVA
PASSO 'Nenhuma rota publicada em caixa mista'
  A. dist real                                         exit=0 aprova
  B. dist/ AUSENTE                                     exit=1 REPROVA
  C. rota Uppercase-Slug publicada                     exit=1 REPROVA
```

### B3 — a raiz não publica mais duas frases coladas

Trocados os dois `<span>` irmãos por dois `<p>` (`src/pages/index.astro`): separação
estrutural não depende de o espaço em branco sobreviver ao compressor, e cada frase mantém o
`lang` próprio. `dist/index.html`:
```
HTML : <h1>mathematics-studies</h1><p lang="pt-BR">Escolha o idioma.</p><p lang="en-US">Choose your language.</p>
TEXTO: 'mathematics-studies Escolha o idioma. Choose your language. Português (Brasil) …'
```

### Sugestões incorporadas

- **S3** — a terceira consequência falseável do `ADR-0007` ganhou passo próprio no CI. Ponta a
  ponta com a fixture `Uppercase-Slug`: `npm run build` **exit 0**, 5 rotas, e
  `dist/pt-br/high-school/algebra/Uppercase-Slug/index.html` publicado — e o passo novo
  reprova com `exit 1`. **Apontamento ao `tech-lead`:** o buraco de origem continua aberto —
  slug fora de kebab-case passa por `validate-content.sh` **e** por `audit-content.sh`; o
  guarda de CI é rede, não conserto (território do TCK-0014).
- **S4** — `CONTENT_ROOT` (constante avaliada na carga) virou `contentRoot()` com memorização.
  Importar o módulo com `cwd` fora do repositório deixou de lançar antes de o chamador poder
  passar `root`. Sem reintroduzir `import.meta.url`. **Mudança de API declarada:** quem
  importava `CONTENT_ROOT` passa a chamar `contentRoot()`.
- **S5** — o padrão do passo de terceiros deixou de ser `https?://` genérico e passou a buscar
  o que **carrega recurso** (`<script`, `<iframe`, `@font-face`, `.woff`, `url(https:`,
  `src|srcset|poster|action="https:`, `<link … href="https:`, mais tokens de analytics
  conhecidos). Caso E acima prova que link de `references.json` na teoria não reprovará a
  task 6.
- **S7** — `<meta name="description">` da raiz agora traz as duas frases (a página é
  bilíngue por definição) e as páginas de nó ganharam `description` localizada vinda de
  `meta.summary[idioma]` — dado real do acervo, exigido pelo leitor nos dois idiomas.
- **S2 e S6** — nada a mudar; S6 (`/pt-br/` e `/en-us/` sem nó = 404 até a task 5) vai
  declarado ao QA no handoff.

### Verificação completa refeita (critérios 7, 10 e 12)

```
$ rm -rf dist .astro node_modules && (job de CI, mesma ordem do arquivo)
  audit-ai-surface.sh                      exit=1  ✘  ← causa externa, ver abaixo
  sync-ai-adapters.py --check              exit=1  ✘  ← causa externa, ver abaixo
  audit-content.sh                         exit=0  ✔
  context-watch-test.sh                    exit=0  ✔  (93/0)
  validate-content.sh (RF-18)              exit=0  ✔
  npm ci                                   exit=0  ✔
  grep independência (passo real)          exit=0  ✔
  npm run build                            exit=0  ✔  prebuild: "Contrato íntegro" + "1 nós · 0 erros"
  HTML sem terceiro (passo real)           exit=0  ✔
  rota sem caixa mista (passo real)        exit=0  ✔
$ find dist -type f
  dist/index.html · dist/pt-br/…/index.html · dist/en-us/…/index.html · dist/robots.txt
$ git status --porcelain -- content/        (vazio — nenhuma das três fixtures sobrou)
```

**Os dois vermelhos não são deste ticket e não foram silenciados.** Às 17:20 os cinco passos
estavam verdes (registrado em `[004]`); às 18:00, `sync-ai-adapters.py --check` acusa
`.cursor/rules/app.mdc`, `.windsurf/rules/app.md`, `.agents/rules/app.md` e os três `core.*`
desatualizados, porque `.github/instructions/app.instructions.md` e `core.instructions.md`
estão sendo editados agora por TCK-0006/TCK-0016; `audit-ai-surface.sh` falha **só** por
consumir esse mesmo `--check`. Regenerar os adapters é a ação correta e **não é minha**: rodar
`sync-ai-adapters.py` no meio da edição alheia congelaria um estado intermediário e criaria
conflito com quem está escrevendo a fonte. Registrado para o `tech-lead`; nenhuma verificação
foi desabilitada para "destravar".

- Resultado: ok — B1, B2 e B3 corrigidos com evidência executada; S3, S4, S5 e S7
  incorporadas; S1 e S8 corrigidas em `[007]`.
- Lição: **L-019 (adendo)** — `memory/lessons/a-validator-only-protects-what-it-can-see.md`,
  seção "Adendo — 2026-08-01, TCK-0015". B1 e B2 são a mesma classe da lição existente, fora
  do validador: "nada encontrado" não é aprovação (agora com o `grep` e seus **três** códigos
  de saída) e portão se lista **por caminho**, não por ferramenta. Índice atualizado em
  `memory/LESSONS.md`.

## [009] HANDOFF — 2026-08-01 18:10
- De: devops-engineer → Para: code-reviewer
- Status novo: in_review · loop 1/3 respondido
- O que foi feito: B1 fechado nas duas camadas (auditoria editorial no `prebuild` + leitor
  falhando alto sem paridade bilíngue); B2 fechado com alvo conferido e três desfechos de
  `grep` tratados nos dois passos, mais um terceiro passo para a consequência falseável que
  faltava (S3); B3 fechado com dois parágrafos. S4, S5 e S7 incorporadas; S1 e S8 corrigidas
  por `CORRECTION`.
- Artefatos: `src/content-contract/index.js`, `src/pages/index.astro`,
  `src/pages/[lang]/[...node].astro`, `package.json`,
  `.github/workflows/ai-surface-audit.yml`, `memory/lessons/a-validator-only-protects-what-it-can-see.md`,
  `memory/LESSONS.md`, `memory/agents/devops-engineer.md`, `memory/context/devops.md`.
  Sem commit e sem push.
- Como validar:
  1. **B1:** nó com `languages: ["pt-BR"]` → `npm run build` ≠ 0 e `dist/` inexistente; e
     `npx astro build` (sem o portão) ≠ 0 pela mensagem do `content-contract`.
  2. **B2:** extrair os blocos `run:` dos três passos e executá-los com o alvo ausente, com o
     alvo vazio e com o alvo real — os dois primeiros têm de reprovar.
  3. **B3:** `dist/index.html` com dois `<p>`; texto visível com espaço entre as frases.
  4. Critérios 7, 10 e 12 refeitos; `git status --porcelain -- content/` vazio.
- Pendências e riscos:
  1. **CI vermelho por causa externa:** `sync-ai-adapters.py --check` e, por consequência,
     `audit-ai-surface.sh` estão reprovando por edições em curso em
     `.github/instructions/*` (TCK-0006/TCK-0016). Não é deste ticket e não foi contornado —
     precisa de `python3 scripts/sync-ai-adapters.py` por quem estiver editando a fonte.
  2. **S6, para o QA:** `/pt-br/` e `/en-us/` respondem **404** — só existe rota de nó até a
     task 5. Comportamento esperado, não defeito.
  3. **Novo custo assumido em B1:** erro editorial (`audit-content.sh`) agora derruba deploy,
     não só o merge. É o resultado exigido pelo RF-18, e o preço é acervo com erro editorial
     bloquear publicação de todo o site.
  4. Buraco de origem do S3 (slug em caixa mista aprovado pelas duas auditorias) segue aberto
     — apontamento ao `tech-lead`, território do TCK-0014.
  5. Imagem real de build da Vercel só observável no primeiro deploy; risco reavaliado como
     residual em `[007]`.
  6. Proteção de branch em `main` e previews por PR continuam sendo ato do usuário.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 (B1 fechado) ·
  [x] 8 · [x] 9 · [x] 10 (B2 fechado) · [x] 11 · [x] 12 · [x] 13 — nenhum restante.

## [010] REJECT — 2026-08-01 18:40 — code-reviewer#9
- De: code-reviewer#9 → Para: devops-engineer
- Status novo: in_progress · **loop 2/3** · a próxima devolução esgota o limite → `tech-lead`
- Um bloqueante novo (B4), na parte da S5 que **eu** sugeri e que a implementação escolhida
  não cobre. B1, B2 e B3 estão **fechados** e reverificados com método próprio; S3, S4, S5
  (direção), S7, e as `CORRECTION` de S1/S8 estão aceitas. Não reabro nada delas.

### B1 — fechado. A escolha de falhar (e não pular) está certa, e o custo é proporcional

Reproduzi a fixture do meu `REJECT` **e o caminho que você não citou** (`status: draft`), numa
cópia do repositório, para não tocar o acervo:

```
nó monolíngue, status=published    validate-content=0  audit-content=1  npm run build=1  dist=NAO  html=0
                                   npx astro build=1  → [content-contract] … declara apenas [pt-BR] … falta en-US
nó monolíngue, status=draft        validate-content=0  audit-content=1  npm run build=1  dist=NAO  html=0
                                   npx astro build=1  → mesma mensagem
```

**Julgamento da escolha: correta, e por um motivo mais forte do que o seu.** Falhar em vez de
pular não é só evitar o fallback silencioso — é que o leitor passou a **espelhar** uma regra que
já existia no acervo, sem inventar proibição nova: `audit-content.py` já reprova
`languages deve ser exatamente ['pt-BR','en-US']` e `theory.en-US.md ausente (bilinguismo
obrigatório — ADR-0002)` **independentemente do `status`** — foi o que o caso `draft` mostrou.
Logo a rede de segurança não é mais estrita que o contrato do acervo; é igual a ele. Se algum
dia o projeto quiser tradução em curso (o "traduzir depois" que o `AGENTS.md` §2b tolera com
`status: draft`), quem tem de mudar primeiro é `audit-content.py` — TCK-0014, não você.

**Proporcionalidade do `audit-content.sh` no `prebuild`: verificada, e aceitável.**
`audit-content.py:398` é `return 1 if errors else 0` — **AVISO não derruba deploy**, só ERRO.
E a ordem `validate:content && audit:content` é **load-bearing**: com `content/` ausente ou
vazio, `audit-content.sh` sozinho devolve `0` (`:345-346`, `:360-362`, "nada a auditar"), mas
`validate-content.sh` sai `2` antes e o `&&` corta — medido: `npm run build` → **exit 2**,
0 HTML, nos dois cenários. O portão está fechado; a dependência da ordem é que não está
escrita (S9 abaixo).

### B2 — fechado, e verificado com bateria maior que a sua

Extraí por script os três blocos `run:` do YAML versionado (literais, sem paráfrase) e rodei
**8 + 18 + 7 cenários**, incluindo os que você não rodou:

```
PASSO 1 (independência)   A real=0 · B alvo ausente=1 · C sem .js=1 · D cita gerador=1
  NOVOS: E módulo renomeado p/ .mjs=1 (falso positivo fechado, aceitável) · F menção em
  README.md=1 · G binário com o token=1 · H subdiretório sem permissão=1 (set -e no find)
PASSO 3 (caixa mista)     A real=0 · B ausente=1 · C vazio=1 · D Uppercase-Slug=1
  NOVOS: E rota acentuada minúscula=0 (sem falso positivo) · F LC_ALL=C / en_US.UTF-8 /
  pt_BR.UTF-8 com rota minúscula=0,0,0 (o `[A-Z]` do find não colapsa por locale)
```

Os três desfechos (`0` achou · `1` limpo · `*` inconclusivo) estão nos **dois** passos com
`grep`; o terceiro passo usa `find` + contagem sob `set -euo pipefail`, que falha fechado por
construção. Nenhum outro passo do workflow usa `grep` como portão — a classe está coberta.
S3 confirmado ponta a ponta: fixture `Uppercase-Slug` → `validate-content=0`, `audit-content=0`,
`npm run build=0` com **5 rotas** e `dist/pt-br/…/Uppercase-Slug/index.html` publicado, e o
passo novo **reprova com exit 1**. O buraco de origem é mesmo de outro dono: as duas auditorias
aprovam o slug em caixa mista — TCK-0014, apontamento correto.

### B3 — fechado

`dist/index.html`: `<h1>…</h1><p lang="pt-BR">Escolha o idioma.</p><p lang="en-US">Choose your
language.</p>`; texto visível `'mathematics-studies Escolha o idioma. Choose your language. …'`.
Separação estrutural, independe do compressor.

### S4 — fechado, sem regressão no teste que aprovei no loop 1

```
A) cwd = raiz do repo          contentRoot() correto · nó lido · memorizado === true   exit 0
B) cwd = src/pages             idem                                                     exit 0
C) cwd = /tmp + loadAllNodes(root) explícito   → funciona (era o ponto do S4)           exit 0
D) cwd = /tmp sem root         → ContentContractError, falha alta                       ≠ 0
grep -rn CONTENT_ROOT src/ .github/ package.json → nenhuma ocorrência órfã
```

### Bloqueante

**B4 — o passo "HTML publicado sem recurso de terceiro" deixou de enxergar o que o critério 12
nomeia.** Ao trocar `https?://` pelo padrão específico (`:127`), a S5 foi atendida e a detecção
regrediu. **Prova ponta a ponta, com build real** (arquivo em `public/`, que o gerador copia
verbatim para `dist/`):

```
public/legado.html:  <SCRIPT SRC="https://cdn.exemplo.com/track.js"></SCRIPT>
                     <img src="//pixel.exemplo.com/p.gif">
$ npm run build                                                          exit=0
$ test -f dist/legado.html                                               SIM
$ (passo real do workflow)  → "OK: 4 página(s) em dist/, nenhuma carrega recurso de terceiro."
                                                                          exit=0
$ (padrão antigo, https?://) → dist/legado.html                          teria REPROVADO
```

Bateria de 18 vetores no passo real: **8 passam em silêncio** —
`src="//host/p.gif"` (pixel em protocolo relativo, a forma clássica), `src='https://…'` (aspas
simples), `url('https://…')`, `@import "https://…"` (sem `url()`), `<object data="https://…">`,
`<a ping="https://…">` (**beacon**, palavra que está no critério 12), `<meta http-equiv=refresh
… url=https://…>`, `<image href>` em SVG, e **qualquer tag em maiúscula** (`grep -rInE` sem
`-i`, enquanto nome de tag em HTML é case-insensitive). O `<IFRAME>` só reprovou porque o
atributo `src=` estava minúsculo — não pelo `<iframe`.

Não é regressão de intenção: o `dist/` de hoje continua limpo (reconferi com o padrão genérico,
zero ocorrências). É o **portão permanente** do critério 12 que ficou mais frouxo que o
artefato que ele protege, e `public/` é vetor real, não hipotético. Vale a régua que já usei
aqui: ferramenta que **aprova** o que a anterior reprovava é bloqueante, porque é ela que vai
para o CI.

**A direção da S5 continua certa e é minha; a cobertura da implementação é que falha.** Não
peça de volta o `https?://` genérico. Medi um padrão que satisfaz as duas coisas — **14/14
casos corretos e zero falso positivo no `dist/` real**:

```
grep -rIniE  (o -i é metade do conserto)
'<script|<iframe|<object|@font-face|@import|\.woff2?|url\([''"]?(https?:)?//|(src|srcset|poster|action|ping|data|formaction)=[''"]?(https?:)?//|<link[^>]+href=[''"]?(https?:)?//|<(image|use)[^>]+href=[''"]?(https?:)?//|googletagmanager|google-analytics|gtag\(|fbq\('
```
Aprova: HTML limpo · `<a href="https://openstax.org/…">` (S5) · `https://` em texto corrido.
Reprova: os 11 vetores acima. Use este, um seu ou outro caminho — mas com bateria anexada.
Seu próprio adendo à `L-019` manda "executá-lo, com o alvo presente **e** ausente"; o que
faltou foi a outra dimensão: a **carga**. Seis casos no passo 2 não fecham a classe — é
`L-013`/`L-021` (lista de casos × regra de classe) aplicada ao padrão, não ao alvo.

### Sugestões

- **S9 — declare que a ordem do `prebuild` é o que fecha o portão.** `audit-content.sh`
  sozinho aprova `content/` ausente ou vazio (`audit-content.py:345-346`, `:360-362`); quem
  barra é o `validate-content.sh` que vem antes no `&&`. Uma linha de comentário no
  `package.json` ou no log evita que uma reordenação futura abra o buraco em silêncio.
- **S10 — o cabeçalho do workflow (`:9-10`) ainda diz "os ADRs são `proposed` e o aceite é ato
  do usuário".** A `[007]` corrigiu isso no log, não no arquivo.
- **S11 — `.github/instructions/app.instructions.md:33`** ("nenhuma string voltada ao usuário
  hard-coded — tudo em catálogo pt-BR/en-US") passou a reger `src/**` durante este ticket
  (TCK-0016). O `UI` de `[...node].astro` é catálogo bilíngue e cumpre o espírito; já
  `index.astro` tem literais em JSX (`Escolha o idioma.` / `Choose your language.`,
  `LANGUAGE_NAME`, `title`, `description`). As duas páginas somem na task 5/6 — registre a
  dívida em vez de refatorar agora.
- **S12 — passo 1 reprova módulo renomeado para `.mjs`** (`modulos` conta só `*.js`). Falha
  fechada, então é seguro; só vale um comentário para quem for renomear.

### Auditoria vermelha — atribuída por medição, não impede este ticket

`audit-ai-surface.sh` exit 1 (`OUTDATED`) e `sync --check` exit 1, com 9 gerados desatualizados
(`.cursor/rules/{app,core}`, `.windsurf/rules/{app,core}`, `.agents/rules/{app,core}`, `.rules`,
`.clinerules`, `.junie/guidelines.md`). Medição própria: as **fontes** modificadas são
`.github/instructions/{app,core}.instructions.md` e `.claude/agents/platform-architect.md`,
todas declaradas no `log.md` do **TCK-0016** (`:46`, `:122`) — o `git diff` de
`app.instructions.md` são as linhas de `ADR-0007`/URL/independência escritas por lá. O TCK-0015
não tocou **nenhuma** fonte canônica, e `grep -c 'TCK-0015\|prebuild'` nos 9 gerados
desatualizados → **0** em todos. Com o TCK-0006 já commitado em `dea3303`, o resíduo é
exclusivamente do TCK-0016. **Sua decisão de não regenerar está certa** e não conta contra
você; ao QA: critério 13 fica `[~]` e o sync é do TCK-0016, não deste ticket.

### Também reverificado

`npm run build` acervo válido exit 0, 3 HTML + `robots.txt`; `validate-content` 0 ·
`audit-content` 0 · `context-watch-test` 93/0; `description` localizada vinda de
`meta.summary[idioma]` nas duas páginas de nó (S7); adendo da `L-019` escrito como **classe**
(não lista de casos), indexado em `LESSONS.md:92`, sem colisão de `L-NNN`; escopo do diff
idêntico ao declarado em `[009]`; `git status --porcelain -- content/` **vazio**.

- Como validar a correção: bateria do passo 2 com os 11 vetores acima + `public/legado.html`
  num build real, com a saída anexada; `dist/` real tem de continuar aprovando.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [x] 10 · [x] 11 · [ ] 12 (B4 — o HTML de hoje está limpo; o portão permanente não) ·
  [~] 13 (vermelho por deriva do TCK-0016, atribuído acima).

## [011] ACTION — 2026-08-01 19:05 — devops-engineer
- Ação: B4 resolvido; S9, S10, S11 e S12 incorporadas. Nada de B1/B2/B3/S3/S4 foi refeito.
- Arquivos: `.github/workflows/ai-surface-audit.yml`, `package.json`, `src/pages/index.astro`.
  `content/`, `docs/`, `scripts/` e `public/` (fora da fixture temporária) intocados.

### B4 — o padrão substituto virou regra de classe, não lista de casos

O diagnóstico está certo e o erro é de método, não de intenção: ao estreitar o padrão para
atender a S5, **troquei uma regra de classe ("qualquer URL absoluta") por uma lista de formas
específicas, e testei a lista contra ela mesma** — seis casos, todos verdes, entregue. A
assimetria que eu devia ter aplicado: falso positivo custa uma build vermelha; falso negativo
publica rastreio. Entre recusar entrada válida e aceitar entrada errada, recusa-se.

Padrão reescrito a partir da **classe** — *tudo que faz o navegador buscar bytes de outra
origem* — e não de uma enumeração. O que a classe obriga, e que a versão anterior não tinha:

- `-i` (`grep -rIniE`): nome de tag e de atributo em HTML são case-insensitive. Metade do
  conserto, como o `REJECT` observou.
- **protocolo relativo** em toda posição: `(https?:)?//`, não `https?:`.
- **aspas simples, duplas ou ausentes**: a aspa simples entra por variável (`q=$(printf …)`),
  porque dentro de string entre aspas simples no shell não há como escapá-la.
- **atributos que buscam bytes**, não só `src`: `data`, `poster`, `action`, `formaction`,
  `background`, `ping` (o beacon que o critério 12 nomeia), `srcset` em qualquer candidato, e
  `href` de `<link>`, `<image>` e `<use>`.
- **canais de CSS**: `url(…)`, `@import` **com ou sem** `url()`, `@font-face`.
- **navegação forçada**: `<meta http-equiv=refresh>` apontando para fora.
- **tags de embutir**: `<script`, `<iframe`, `<object`, `<embed`.
- nomes de rastreadores, que não dependem de sintaxe (`googletagmanager`, `gtag(`, `fbq(`,
  `hotjar`, `plausible.io`, `umami`, `clarity.ms`, `sendBeacon`).

**Bateria de 26 vetores + caso base, executada contra o bloco `run:` extraído do YAML
versionado** (não paráfrase). 18 têm de reprovar, 8 têm de passar — o segundo lado é o que
prova que o padrão não voltou a ser genérico e que a S5 continua atendida:

```
  BASE  dist/ real, sem vetor                        exit=0 aprova   OK
  V01   pixel em protocolo relativo //host           exit=1 REPROVA  OK
  V02   aspas simples em src                         exit=1 REPROVA  OK
  V03   url() com aspas simples                      exit=1 REPROVA  OK
  V04   @import sem url()                            exit=1 REPROVA  OK
  V05   <object data>                                exit=1 REPROVA  OK
  V06   <a ping> (beacon)                            exit=1 REPROVA  OK
  V07   meta refresh para fora                       exit=1 REPROVA  OK
  V08   <image href> em SVG                          exit=1 REPROVA  OK
  V09   tag em MAIUSCULA                             exit=1 REPROVA  OK
  V10   script de terceiro                           exit=1 REPROVA  OK
  V11   iframe                                       exit=1 REPROVA  OK
  V12   @font-face remota                            exit=1 REPROVA  OK
  V13   link de folha de estilo remota               exit=1 REPROVA  OK
  V14   analytics por nome                           exit=1 REPROVA  OK
  V15   <use href> em SVG                            exit=1 REPROVA  OK
  V16   <embed src> protocolo relativo               exit=1 REPROVA  OK
  V17   srcset com candidato externo                 exit=1 REPROVA  OK
  V18   atributo background legado                   exit=1 REPROVA  OK
  P01   link de referência no conteúdo (S5)          exit=0 aprova   OK
  P02   URL de licença em texto corrido              exit=0 aprova   OK
  P03   folha de estilo da própria origem            exit=0 aprova   OK
  P04   imagem da própria origem                     exit=0 aprova   OK
  P05   link interno de rota                         exit=0 aprova   OK
  P06   url() da própria origem                      exit=0 aprova   OK
  P07   <use href> por fragmento                     exit=0 aprova   OK
  P08   texto citando script/analytics sem tag       exit=0 aprova   OK

  26 vetores + base · falhas: 0
```

**Ponta a ponta com a fixture do `REJECT`** (`public/legado.html`, removida ao fim):
```
$ npm run build                                            exit=0
$ test -f dist/legado.html                                 SIM   (4 HTML em dist/)
$ (passo real do workflow)
dist/legado.html:2:<SCRIPT SRC="https://cdn.exemplo.com/track.js"></SCRIPT>
dist/legado.html:3:<img src="//pixel.exemplo.com/p.gif">
::error::recurso externo no HTML publicado — script, iframe, pixel, beacon ou fonte remota
                                                           exit=1
$ (fixture removida, build limpo) → "OK: 3 página(s) em dist/, nenhuma carrega recurso de terceiro."
```
`ls public/` → só `robots.txt`; `git status --porcelain -- content/ public/` sem resíduo de
fixture.

**Dívida declarada no próprio passo:** fonte auto-hospedada (`@font-face` + `.woff` da
própria origem, que o `ADR-0007` permite) vai reprovar. Fica no comentário do passo, com a
instrução de refinar ali quando o ticket de tipografia existir — nunca afrouxar a classe.

### Sugestões incorporadas

- **S9** — a dependência de ordem do `prebuild` está escrita onde ela pode ser quebrada: uma
  chave `"//"` no `package.json` (npm ignora chaves com esse nome — `npm ci` e `npm run
  build` reverificados) explicando que `validate:content` vem antes porque o auditor sozinho
  aprova `content/` ausente ou vazio, e que trocar `&&` por `;` reabre o buraco.
- **S10** — cabeçalho do workflow corrigido: `ADR-0006` **accepted** em 2026-08-01 (TCK-0016).
  A justificativa de manter o nome do arquivo perdeu a menção a "aceite pendente".
- **S11** — dívida de i18n registrada em comentário no topo de `index.astro`, com o motivo de
  não refatorar: a página é a escolha de idioma, existe nos dois idiomas ao mesmo tempo e some
  na task 5. O `UI` de `[...node].astro` já é catálogo bilíngue.
- **S12** — comentário no passo 1 explicando que a contagem de `*.js` é deliberada: renomear
  para `.mjs`/`.ts` **reprova** até a linha ser atualizada junto. Falha fechada, mantida.

### Verificação completa (job de CI inteiro, após `rm -rf dist .astro node_modules`)

```
  audit-ai-surface.sh                        exit=0 ✔
  sync-ai-adapters.py --check                exit=0 ✔   ← TCK-0016 regenerou; critério 13 verde
  audit-content.sh                           exit=0 ✔
  context-watch-test.sh                      exit=0 ✔   (93/0)
  validate-content.sh (RF-18)                exit=0 ✔
  npm ci                                     exit=0 ✔
  passo: independência do contrato de dados  exit=0 ✔   (alvo ausente → exit=1, reconferido)
  npm run build                              exit=0 ✔   prebuild: "Contrato íntegro" + "0 erros"
  passo: HTML sem recurso de terceiro        exit=0 ✔   (bateria de 26 acima)
  passo: nenhuma rota em caixa mista         exit=0 ✔   (dist ausente → exit=1, reconferido)
  saída: 4 arquivos · 3 HTML
```
Os três passos foram reextraídos do YAML **depois** da última edição e reexecutados, para que
a evidência corresponda ao texto versionado agora.

- Resultado: ok — B4 fechado com 26 vetores e a fixture derrubada; S9–S12 incorporadas; as
  cinco auditorias verdes (a deriva do TCK-0016 foi resolvida por eles).
- Lição: **L-019 (3º adendo)** — "estreitar para tirar falso positivo abre falso negativo",
  em `memory/lessons/a-validator-only-protects-what-it-can-see.md`. Classe registrada:
  afrouxar um detector é **reescrevê-lo**, e o novo exige a bateria inteira (os dois lados,
  vetores que reprovam e casos legítimos que passam), derivada da classe e não do delta —
  L-013/L-021 aplicadas ao **padrão**, com a assimetria do adendo de L-022 (na dúvida,
  recusar). Índice atualizado em `memory/LESSONS.md`.

## [012] HANDOFF — 2026-08-01 19:10
- De: devops-engineer → Para: code-reviewer
- Status novo: in_review · loop 2/3 respondido
- O que foi feito: padrão do passo de terceiros reescrito a partir da classe "tudo que busca
  bytes de outra origem" (com `-i`, protocolo relativo, aspas simples, atributos `data`,
  `ping`, `poster`, `formaction`, `background`, `srcset`, `href` de `link`/`image`/`use`,
  `@import` sem `url()`, `meta refresh`, `<object>`, `<embed>` e rastreadores por nome),
  provado com 26 vetores contra o bloco `run:` versionado e com a fixture `public/legado.html`
  em build real. S9 (ordem do `prebuild` documentada no `package.json`), S10 (cabeçalho do
  workflow com `ADR-0006` accepted), S11 (dívida de i18n em comentário) e S12 (nota sobre
  `.mjs`) incorporadas.
- Artefatos: `.github/workflows/ai-surface-audit.yml`, `package.json`, `src/pages/index.astro`,
  `memory/lessons/a-validator-only-protects-what-it-can-see.md`, `memory/LESSONS.md`,
  `memory/agents/devops-engineer.md`, `memory/context/devops.md`. Sem commit e sem push.
- Como validar:
  1. **B4:** `public/legado.html` com `<SCRIPT SRC="https://…">` e `<img src="//…">` →
     `npm run build` exit 0, `dist/legado.html` presente, e o passo real **exit 1** citando as
     duas linhas; sem a fixture, o passo aprova as 3 páginas reais.
  2. Bateria: 18 vetores que precisam reprovar e 8 casos legítimos que precisam passar
     (link de referência, URL em texto, recursos de mesma origem, `<use href="#frag">`).
  3. Job de CI inteiro após `rm -rf dist .astro node_modules` — dez passos, todos exit 0.
- Pendências e riscos:
  1. **Dívida assumida no passo de terceiros:** fonte auto-hospedada reprovará (`@font-face`,
     `.woff`). Está no comentário do passo; refinar no ticket de tipografia, sem afrouxar a
     classe.
  2. **S11:** literais de i18n em `index.astro` seguem fora de catálogo, por decisão
     registrada — a página some na task 5.
  3. **S6:** `/pt-br/` e `/en-us/` sem nó respondem 404 até a task 5 — esperado, não defeito.
  4. Erro editorial (`audit-content.sh`) derruba deploy, não só merge — custo do B1.
  5. Buraco de origem do S3 (slug em caixa mista aprovado pelas duas auditorias) segue com o
     `tech-lead`/TCK-0014.
  6. Proteção de branch em `main` e previews por PR continuam sendo ato do usuário.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [x] 10 · [x] 11 · [x] 12 (B4 fechado) · [x] 13 (as cinco auditorias verdes; a deriva era do
  TCK-0016 e foi regenerada por eles) — nenhum restante.

## [013] HANDOFF — 2026-08-01 19:40
- De: code-reviewer#9 → Para: qa-validator
- Status novo: in_validation · **APROVADO no loop 2/3** (loop encerrado sem escalada)
- O que foi revisado: o diff completo do esqueleto e do pipeline, em três passagens
  (`[006]` 3 bloqueantes, `[010]` 1 bloqueante, esta). **B1, B2, B3 e B4 fechados**; S1–S12
  incorporadas ou corrigidas por `CORRECTION`. Nada aprovado por afirmação do produtor: todo
  número abaixo foi reexecutado por mim.

### B4 — fechado, e a correção é de classe, não de caso

Reextraí os três blocos `run:` do YAML **depois** da última edição e provei que são o texto
versionado (reindentados, `bloco in yaml → True` nos três). Reproduzi a bateria inteira, os
**dois lados**, contra o passo real:

```
18/18 vetores hostis REPROVAM — inclusive os 8 que passavam calados no loop 2:
  //host (pixel), aspas simples, @import sem url(), <object data>, <a ping> (beacon),
  meta refresh, <image href> em SVG, tag em MAIÚSCULA
   + <embed src> relativo, srcset externo, background legado, <use href> externo, <link>
     remoto, @font-face remota, iframe, script de terceiro, analytics por nome
 8/8 casos legítimos APROVAM — <a href="https://openstax.org/…"> (S5 preservada), URL de
  licença em texto corrido, folha e imagem de mesma origem, url(/assets/…), <use href="#frag">,
  link interno de rota, texto citando "script"/"analytics" sem tag
```
Quatro formas ordinárias que ele não listou e que eu testei também reprovam: `<IMG SRC=//e.x/p.gif>`
(sem aspas, maiúsculo, relativo), `<link rel=preload as=font href="//cdn/…woff2">`,
`<source srcset>` em `<picture>`, `<form action="//…">`. **Não achei nenhuma forma comum que
escape** — que é a diferença de natureza em relação ao loop 2, onde escapavam o pixel clássico,
o beacon nomeado no critério e *qualquer* tag em caixa alta.

Ponta a ponta, com build real:
```
public/legado.html com <SCRIPT SRC="https://cdn…"> e <img src="//pixel…">
  npm run build → exit 0, dist/legado.html presente, 4 HTML
  passo real    → exit 1, citando dist/legado.html:2 e :3
fixture removida, build limpo
  passo real    → exit 0, "OK: 3 página(s) em dist/, nenhuma carrega recurso de terceiro."
ls public/ → robots.txt   ·   git status --porcelain -- content/ → vazio
```

### Job de CI inteiro, do zero (`rm -rf dist .astro node_modules`)

```
audit-ai-surface.sh 0 ✔ · sync-ai-adapters.py --check 0 ✔ · audit-content.sh 0 ✔ ·
context-watch-test.sh 0 ✔ (93/0) · validate-content.sh 0 ✔ · npm ci 0 ✔ ·
passo independência 0 ✔ · npm run build 0 ✔ · passo HTML sem terceiro 0 ✔ ·
passo caixa mista 0 ✔      saída: 4 arquivos · 3 HTML
```
Casos negativos reconferidos **após** a última edição: passo 1 sem `src/content-contract/`
→ exit 1; passo 3 sem `dist/` → exit 1. **Critério 13 fecha sem ressalva** — a deriva do
`sync --check` era do TCK-0016 (atribuída por medição em `[010]`) e eles regeneraram.

### Demais critérios, reconferidos no artefato final

`/` 200 · `/pt-br/high-school/algebra/quadratic-equations` 200 · `/en-us/…` 200 ·
`/pt-BR/…` **404**; `lang="pt-BR"`, `lang="en-US"`, `lang="pt-BR"`; zero rota em caixa mista;
`grep -rIloE 'https?://' dist/` **vazio**; raiz renderizando `'… Escolha o idioma. Choose your
language. …'` com espaço (B3). `"//"` no `package.json` é lido como campo comum e não afeta
`npm ci`, `npm run build` nem `npm pkg get`. Escopo idêntico ao declarado: `package.json`,
`package-lock.json`, `astro.config.mjs`, `vercel.json`, `public/`, `src/`, o workflow e o
`.gitignore` — **nenhuma fonte canônica** (`.github/instructions/`, `.claude/`) tocada por
este ticket; as alterações em `docs/adr/`, `docs/architecture/`, `docs/specs/` e
`.github/instructions/` são do TCK-0016 e **confirmam** as decisões desta entrega (URL
minúscula, projeto na raiz).

### Julgamento da dívida declarada: a decisão de não afrouxar a classe está certa

Recusar recurso legítimo custa build vermelha; aceitar recurso externo publica rastreio. Errar
para o lado de recusar é a escolha certa, e é a mesma assimetria que faltou no B4. **Mas a
dívida é maior do que o comentário diz** — ver A2.

### Achados não bloqueantes (numerados, para o QA decidir o que vira dívida registrada)

- **A1 — o 19º vetor: `<base href="https://cdn.evil.com/">` passa** (`workflow:71-78`). Medido:
  `<base href="https://cdn.evil.com/"><img src="a.png">` → passo **exit 0**. É uma tag padrão
  de `<head>` cuja função é reparentar **todos** os caminhos relativos da página: uma linha
  transforma cada ativo de mesma origem em terceiro, e o padrão genérico do loop 1 a pegava.
  Cauda menor, também medida e também passando: `<img src = "https://…">` (espaços em volta do
  `=`, HTML válido), `srcset=//cdn/a.png` sem aspas, `image-set("https://…")` sem `url()`,
  `<feImage href>`, e atributo codificado por entidade (`&#104;ttps://`, evasão deliberada —
  fora do modelo de ameaça). Não bloqueia porque nenhuma delas existe no artefato e nenhuma é
  forma ordinária de erro acidental; **mas `<base>` deve entrar no padrão** na mesma edição
  forçada por A2. O próprio 3º adendo da `L-019` dá a regra que fecharia isto: "listar o que o
  padrão novo **deixou** de pegar".
- **A2 — a dívida declarada é maior que "fonte auto-hospedada".** Medi as quatro colisões
  futuras contra o passo real: `@font-face` auto-hospedada **reprova** (declarada);
  `<script type="module" src="/_astro/ilha.js">` — a ilha do player, tasks 7–8 — **reprova**;
  `<script>navigator.serviceWorker.register('/sw.js')</script>` — task 10 — **reprova**;
  `<iframe src="/media/aula.html">` de mesma origem — **reprova**. Ou seja, o passo fica
  vermelho no **primeiro** ticket de interatividade, não só no de tipografia. Isso é bom (força
  a revisita) e é onde `<base>` entra; o que falta é o comentário dizer isso.
- **A3 — `L-019` está com 140 linhas e três adendos, logo quatro listas "Como aplicar".** O
  adendo é a **forma correta** (nenhum superou o anterior; é a mesma causa — o ponto cego do
  portão — em três dimensões: o que ele percorre, onde ele fica, o que ele casa), e dividir
  destruiria o `L-NNN` citável. Sugestão: consolidar as quatro listas num checklist único no
  topo, mantendo os adendos como histórico abaixo — é uma lição cujo valor depende de ser lida
  até o fim.
- **A4 — para o QA:** `/pt-br/` e `/en-us/` sem nó respondem **404** até a task 5 (confirmado);
  comportamento esperado, não defeito. Erro editorial (`audit-content.sh`) derruba deploy, não
  só merge — custo consciente do B1, com AVISO não derrubando (`audit-content.py:398`). O
  buraco de origem do S3 (slug em caixa mista aprovado pelas duas auditorias) segue com o
  `tech-lead`/TCK-0014.

### Está pronto para ir ao ar?

**Sim, na minha avaliação — com uma condição operacional que não é do produtor.** O artefato
publicável tem 4 arquivos, 3 páginas, **zero JavaScript**, zero requisição externa, CSS
embutido, fontes do sistema, `lang` correto por rota e URLs minúsculas; o portão do RF-18 está
nos dois caminhos e derruba a build de fato, provado com fixture em três ambientes; `python3` na
imagem de build da Vercel foi reverificado na documentação e no contêiner; `engines.node` bate
com a tabela do fornecedor; não há segredo, nem recurso proprietário, nem coleta. A condição:
**push na `main` publica em produção**, e o commit é ato do usuário/orquestrador — o QA deve
validar antes do push, não depois. Se o primeiro deploy falhar, o modo de falha é build
vermelha com mensagem, nunca publicação silenciosa.

- Artefatos a validar: `package.json`, `package-lock.json`, `astro.config.mjs`, `vercel.json`,
  `public/robots.txt`, `src/**`, `.github/workflows/ai-surface-audit.yml`, `.gitignore`.
- Como validar: critérios 1–13 do `ticket.md`; `npm ci && npm run build`; fixture inválida
  derrubando a build; `find dist`; os três blocos `run:` extraídos do YAML; as cinco auditorias.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [x] 10 · [x] 11 · [x] 12 · [x] 13 — todos com evidência reexecutada por mim nesta entrada e
  em `[006]`/`[010]`. Nenhum bloqueante restante; A1–A4 são não bloqueantes.

## [014] HANDOFF — 2026-08-01 21:30
- De: qa-validator#12 → Para: tech-lead
- Status novo: **done** — 13/13 critérios com evidência **reexecutada por mim**, do zero.
- Cadeia respeitada: produtor `devops-engineer`, revisor `code-reviewer#9`, validador
  `qa-validator#12`. Não produzi nem revisei nenhum artefato deste ticket.

### Ambiente da validação

Commit no **início** `dea3303`; no **fim** `aee5d3d` (`TCK-0016: aceita os ADR-0006 e ADR-0007`,
outra cadeia). `git diff --name-only dea3303 aee5d3d` × artefatos do TCK-0015 = **0
ocorrências** — o avanço do HEAD não tocou nada que eu estava validando, e as cinco
auditorias foram **reexecutadas no HEAD final** (todas exit 0). Node v24.14.1 · npm 11.11.0 ·
Python 3.12.3 · Linux. Sem navegador com MCP nesta sessão: a verificação visual foi feita no
HTML gerado e no servidor de `preview` (`astro preview`, `curl`), não por captura de tela —
declarado como limite da evidência.
Sequência: `rm -rf dist .astro node_modules` → `npm ci` → `npm run build`. Fixtures hostis
rodadas em **cópia isolada da árvore** (`tar` da raiz para o scratchpad + `npm ci` próprio,
caminho absoluto diferente), para não expor `content/` do working tree compartilhado — o que
também serviu de prova de portabilidade: build exit 0 e 3 HTML fora do caminho original.

### Critérios — uma linha de evidência por critério

- [x] **1.** `private: true` · `engines.node ">=22.12.0"` · `type: module` ·
  `dependencies {"astro":"^7.1.6"}` · `devDependencies {}`; varredura por nome contra 20
  famílias de UI/teste/componente (react, vue, svelte, preact, solid, lit, mui, bootstrap,
  tailwind, jest, vitest, mocha, playwright, cypress, testing-library, storybook…) →
  **0 ocorrências**, diretas e transitivas. `npm ci` exit 0, 0 vulnerabilidades.
- [x] **2.** Os 10 caminhos do `ADR-0007` §3 presentes (`package.json`, `package-lock.json`,
  `astro.config.mjs`, `public/`, `src/{content-contract,pages,layouts,components,islands,styles}`);
  **nenhum diretório extra** em `src/` além dos seis do ADR.
- [x] **3.** `grep -rniE 'astro|@astrojs|vite|@vite' src/content-contract/` → **exit 1**;
  os únicos `import` do módulo são `node:fs`, `node:path` e `./languages.js`. Prova positiva
  minha: `node --input-type=module` importando o módulo **sem o gerador no caminho** leu o nó
  piloto (`contentRoot` correto, `status: draft`, `pt-BR,en-US`, teoria 6055/5894 bytes,
  5 itens, as duas rotas).
- [x] **4.** `lang="pt-BR"` / `lang="en-US"` / `lang="pt-BR"` (raiz) nos três HTML, com as
  URLs em `/pt-br/` e `/en-us/`; `find dist -path '*[A-Z]*'` → **0 linhas**.
- [x] **5.** Matriz de 14 rotas no `preview`: `/` 200 · `/pt-br/high-school/algebra/quadratic-equations`
  **200** · `/en-us/…` **200** · `/pt-BR/…` **404** · `/PT-BR/…` 404 · `/en-US/…` 404 ·
  `/pt-br/high-school/algebra/Quadratic-Equations` 404. Caminho da taxonomia na URL sem
  tradução e sem normalização.
- [x] **6.** As duas páginas de nó trazem título, `summary` e `status` **lidos do acervo real**
  na build (`Equações do segundo grau` / `Quadratic equations`, selo `Rascunho` / `Draft`,
  `5 exercícios no acervo` / `5 exercises in the corpus`) e o próprio texto declara que não é
  o leitor. Testei os dados vazios: nó **sem** `exercises.json` → "0 exercícios no acervo";
  nó com 1 item → singular correto nos dois idiomas.
- [x] **7.** Acervo válido: `npm run build` exit 0, 3 rotas. Fixture inválida **na árvore
  real** (`id` divergente + `title` sem `en-US`): `[META-ID-MISMATCH]` + `[LOCALIZED-MISSING-LANG]`,
  `CONTRATO VIOLADO: 2 violação(ões)`, **exit 1**, `dist` **inexistente**, **0 HTML**.
  Fixture removida; `git status --porcelain -- content/` **vazio**.
- [x] **8.** Decisão registrada em `[004]` com a alternativa descartada nomeada. Verifiquei o
  resultado, não a redação: o portão está nos dois caminhos e derruba de fato (critério 7 e o
  portão 1 abaixo), e `vercel.json:4` (`buildCommand: npm run build`) é o que liga o
  `prebuild` no caminho do host.
- [x] **9.** `vercel.json` = `$schema`, `installCommand`, `buildCommand`, `outputDirectory`.
  Busca por 15 chaves proprietárias/não-portáteis (`rewrites`, `redirects`, `headers`,
  `cleanUrls`, `trailingSlash`, `crons`, `functions`, `regions`, `routes`, `images`,
  `analytics`, `speedInsights`, `framework`…) → **nenhuma**.
- [x] **10.** `on: push[main] · pull_request · schedule · workflow_dispatch`; 10 passos
  executáveis, todos exit 0 do zero (abaixo). Os três passos com portão foram **extraídos do
  YAML versionado por script** e provados literais (`bloco in yaml → True` nos três) antes de
  serem executados.
- [x] **11.** `git check-ignore -v` confirma cobertura efetiva de `node_modules/` (`:25`),
  `.astro/` (`:26`), `dist/` (`:29`), `.vercel/` (`:32`), `coverage/` (`:33`), `.env` (`:99`);
  `git ls-files` com esses prefixos → **0 arquivos rastreados**.
- [x] **12.** No `dist/` gerado: 4 arquivos, 3 HTML, 52 KB no total, ~2,2 KB por página.
  `grep -rInE 'https?://|<script|@font-face|\.woff2?|<iframe|analytics|gtag|pixel|beacon|<base|<object|<embed|@import|ping=|srcset|src *=|url\('` → **exit 1, nenhuma ocorrência**.
  Zero `<script>`, zero `<form>`, zero `<input>`, zero requisição externa (`num_connects=1`),
  CSS embutido, pilha de fontes do sistema. `ASTRO_TELEMETRY_DISABLED` confirmada como
  variável real do `@astrojs/telemetry` **instalado** e presente nos três scripts que chamam
  o gerador. Sem service worker, manifesto, IndexedDB ou Cache API (`grep` → exit 1).
- [x] **13.** `audit-ai-surface.sh` 0 · `audit-content.sh` 0 (1 nó · 0 erros · 0 avisos) ·
  `validate-content.sh` 0 (1 nó · 0 violações) — e reexecutados no HEAD final `aee5d3d`,
  junto com `sync-ai-adapters.py --check` 0.

**Job de CI inteiro, do zero (`rm -rf dist .astro node_modules`), na árvore real:**
`audit-ai-surface 0 · sync --check 0 · audit-content 0 · context-watch-test 0 · validate-content 0 ·
npm ci 0 · passo independência 0 · npm run build 0 · passo HTML sem terceiro 0 · passo caixa
mista 0` — saída 4 arquivos, 3 HTML. As 93 asserções do `context-watch` contadas **por fora**
do contador do script (`grep -c '^ok '` = 93, `skip` = 0).
Casos negativos dos três passos, medidos por mim na cópia: passo 1 (alvo ausente=1, sem
`.js`=1, leitor citando o gerador=1, restaurado=0); passo 3 (`dist` ausente=1, vazio=1,
rota `Uppercase-Slug`=1, restaurado=0). Falham fechado nos três desfechos do `grep`.

### Portão 1 — bilinguismo no caminho de publicação: **FECHADO**

Montei os nós monolíngues eu mesmo, nas duas direções e nos dois `status`, em cópia isolada:

```
mono pt-BR, published   validate=0 audit=1 | npm run build=1 dist=NAO html=0 | astro build sozinho=1 html=0
mono pt-BR, draft       validate=0 audit=1 | npm run build=1 dist=NAO html=0 | astro build sozinho=1 html=0
mono en-US, published   validate=0 audit=1 | npm run build=1 dist=NAO html=0 | astro build sozinho=1 html=0
declara 2, sem theory.en-US.md   audit=1 | npm run build=1 dist=NAO html=0 | astro build sozinho=1 html=0
```
As duas camadas respondem: o `prebuild` (`audit-content`) e o leitor (`[content-contract] …
declara apenas [pt-BR] … falta en-US … nó sem paridade não pode virar rota publicada`).
**Nenhuma rota monolíngue chega a existir** — `dist/` sequer é criado.

**Ordem × conjunção — correção de registro.** A **conjunção** é load-bearing, a **ordem não**:
```
content/ vazio    audit sozinho=0 ("0 nós")  validate sozinho=2 ("ERRO DE USO")  npm run build=2  html=0
content/ ausente  audit sozinho=0 (AVISO)     validate sozinho=2                  npm run build=2  html=0
prebuild invertido (audit && validate), content/ vazio                            npm run build=2  html=0
prebuild com ';' no lugar de '&&',  content/ vazio                                npm run build=0  html=1  <-- FURO
```
Ou seja: trocar `&&` por `;` **publica um site vazio**; **inverter a ordem não abre nada**
(o auditor sai 0, o validador roda em seguida e sai 2, o `&&` propaga). O comentário `"//"` do
`package.json` e o `[010]` dizem que inverter reabre o buraco — não reabre. O erro é na
direção **conservadora** (avisa demais), então é **dívida de precisão (D-1)**, não defeito.

### Portão 2 — terceiros: **FECHADO para a classe de erro ordinário**, com furos medidos

Reproduzi a bateria do revisor contra o bloco `run:` versionado: **18/18 hostis reprovam ·
8/8 legítimos aprovam · 4/4 formas extras dele reprovam — 0 divergências**. Ponta a ponta com
`public/legado.html` (`<SCRIPT SRC="https://…">` + `<img src="//pixel…">`) em build real:
build exit 0, `dist/legado.html` presente, **passo real exit 1** citando as duas linhas;
sem a fixture, exit 0 com as 3 páginas reais.

**Procurei o 20º vetor: rodei 30 vetores meus + 4 controles. 17 passam calados.** Classificação:

| classe | vetores | veredito |
|---|---|---|
| já declarados em A1 | `<base href>`, `src = "https://…"` (espaço no `=`), `srcset=//` sem aspas, `image-set("https://…")`, `<feImage href>` | confirmados, não novos |
| não são vetor / obsoletos | `download="//…"`, `<html manifest>` (appcache), `<applet archive>` | expectativa minha errada |
| marginais | `<meta property="og:image">`, `<?xml-stylesheet href>` | sem alcance no artefato |
| **novos e reais** | **`report-uri https://…` num `<meta http-equiv="Content-Security-Policy">`**; **`manifest.webmanifest` com `"src":"https://…"`** (JSON não tem `=`); **`fetch()` · `import()` dinâmico · `WebSocket` · `EventSource` · `XMLHttpRequest`** dentro de um chunk `.js` emitido | **D-2, com gatilho** |

**Por que dívida e não defeito** — medi as três coisas que decidem a severidade:
1. **Zero ocorrência no artefato:** o `grep` genérico `https?://` sobre o `dist/` de hoje é
   vazio; não há uma única URL absoluta no HTML publicado.
2. **Não há inversão limpa.** Rodei o padrão do loop 1 (`https?://|<script|…`) e o atual lado
   a lado: o atual **ganha** em 6 formas de erro ordinário (`<embed src=//`, `background=//`,
   `<IMG SRC=//` sem aspas, `srcset` de `<source>`, `<form action=//`, `<track src=//`) e nos
   **3 casos legítimos** que o antigo reprovava (link do OpenStax — o S5 —, URL de licença em
   texto corrido, prosa citando "analytics"); o antigo ganha em 6 formas de URL absoluta
   exótica. **Nenhum é superconjunto do outro** — a régua "a ferramenta mais estrita é a que
   aprova", que tornou o B4 bloqueante, não se aplica aqui.
3. **Gatilho já forçado por construção** para 5 dos 7 (ver A2 abaixo). As duas exceções, que
   ficam com gatilho **escrito**, são: `<link rel="manifest" href="/manifest.webmanifest">`
   **aprova** (medido) — então o manifesto do PWA entra na task 10 sem forçar a revisita — e o
   `report-uri` de CSP, alcançável a qualquer momento por um ticket de segurança, **sem
   gatilho nenhum**.

### Julgamento das dívidas

- **A1 — `<base href="https://cdn.evil.com/">` passa: confirmado ponta a ponta.** Não só o
  passo aprova o vetor isolado: pus o arquivo em `public/`, a build saiu **exit 0**,
  `dist/reparent.html` foi publicado e o passo real aprovou **4 páginas**. Uma linha reparenta
  todos os caminhos relativos da página para um CDN de terceiro. Não bloqueia (não existe no
  artefato, e não é forma de erro acidental), mas **entra no padrão junto com D-2**.
- **A2 — aceito, com o gatilho corrigido.** Medi as colisões contra o passo real:
  `@font-face` auto-hospedada **reprova** · `<script type="module" src="/_astro/ilha.js">`
  **reprova** · registro do service worker **reprova** · `<iframe src="/media/…">` de mesma
  origem **reprova** · `<embed src="/media/x.pdf">` **reprova** — todos **permitidos** pelo
  `ADR-0007`. O comentário do passo nomeia só "o ticket de tipografia"; o vermelho chega
  **antes**, no primeiro ticket de interatividade (tasks 7–8) e no de offline (task 10).
  Aceito porque a direção da falha é a certa (fecha, não abre) e porque essa revisita forçada
  é justamente o que traz D-2 de volta à mesa — mas o comentário tem de dizer *quando*.
- **A4 — esperado, não quebra.** Confirmei: `/pt-br/`, `/en-us/`, `/pt-br`, `/en-us` e
  `/pt-br/high-school` → **404**; `/`, `/pt-br/…/quadratic-equations` e `/en-us/…` → **200**.
  É a fatia contratada (o índice é a task 5). Achado colateral: **não existe `404.astro`**, então
  quem erra a URL recebe o 404 padrão do host — sem marca, monolíngue em inglês e sem volta
  para `/` (ver `ACTION` 2).
- **Erro editorial derrubando deploy — proporcional.** Confirmei `audit-content.py:398`
  (`return 1 if errors else 0`): **AVISO não derruba**, só ERRO. E as quatro fixtures acima
  mostram que o que derruba é violação de contrato, não estilo. O custo (um erro editorial em
  qualquer nó bloqueia a publicação do site inteiro) é o resultado que o RF-18 exige; a
  alternativa é publicar acervo reprovado. Aceito.

### Casos hostis — o que se aplica e o que não, com a prova de por que não

Aplicáveis, **executados**: dois idiomas (as duas páginas de nó + a raiz, conteúdo e `lang`
corretos, plural e singular certos nos dois); tema claro **e** escuro (`prefers-color-scheme`
com paleta própria — contraste medido nos **10** pares: mínimo **4,90:1** em alvo 3,0 e
**8,24:1** em alvo 4,5, os dois temas passam AA); zoom 200% (`viewport` sem `user-scalable=no`
nem `maximum-scale`, zero largura em `px`, `main` em `68ch`, `.node-path` com
`overflow-wrap: anywhere` — reflow sem barra horizontal); navegação só por teclado (1–2
focáveis por página, todos `<a>`, ordem de tabulação = ordem do documento, **zero** `tabindex`
positivo/`autofocus`/`accesskey`, `:focus-visible` com contorno de 3px em `currentColor`);
leitor de tela (um `<h1>` por página, `<main>` presente, `lang` no documento e nos trechos do
outro idioma, `hreflang` nos links, `alt` em 100% das imagens — há 0); dispositivo modesto e
rede lenta (**1 requisição, 2,2 KB, zero JavaScript**); dados vazios (nó sem `exercises.json`
→ "0 exercícios"; acervo vazio/ausente → build **exit 2**, 0 HTML).

**Não aplicáveis, com a checagem que sustenta isso** — e não por confiança: *offline e
reconexão* e *recarregar no meio de um exercício* dependem de estado no cliente, e o artefato
publicado tem `<script>`=0, `<form>`=0, `<input>`=0 e `grep -rIniE 'serviceworker|sw\.js|
manifest|workbox|indexeddb'` sobre `dist/` → **exit 1**: não há estado a perder nem camada
offline a reconectar (é a task 10, e o `ticket.md` a exclui). *Formato decimal*: as três
páginas não renderizam nenhum número fracionário — só a contagem inteira de exercícios, cuja
pluralização conferi nos dois idiomas. *Leitura de fórmula por leitor de tela*: **não há
fórmula** no HTML publicado (a teoria não é renderizada nesta fatia) — a norma do TCK-0006 se
aplica à task 6.

### Dívidas registradas (com gatilho) e `ACTION` ao `tech-lead`

- **D-1 — `"//"` do `package.json` e `[010]` afirmam que inverter a ordem do `prebuild`
  reabre o buraco; medido, não reabre.** Quem reabre é trocar `&&` por `;` (exit 0, 1 HTML).
  Erro conservador → dívida de precisão. *Gatilho:* a próxima edição do `prebuild`.
- **D-2 — 7 formas reais de terceiro atravessam o passo.** *Gatilho escrito, porque estas
  duas não têm gatilho automático:* (i) o primeiro `<link rel="manifest">` (task 10) —
  **aprova hoje**, medido; (ii) o primeiro `<meta http-equiv="Content-Security-Policy">` com
  `report-uri`/`report-to`. As outras cinco (`fetch`, `import()`, `WebSocket`, `EventSource`,
  `XMLHttpRequest` em chunk emitido) chegam junto com o JavaScript, e aí o passo já está
  vermelho por A2 — mas ao **refinar** o passo para liberar `<script src="/_astro/…">`, o
  conteúdo do chunk vira o novo ponto cego. `<base>` (A1) entra na mesma edição.
- **D-3 — bilíngue de fachada por espaço de largura zero.** Nó declarando os dois idiomas com
  `title["en-US"]` = U+200B passa `validate=0`, `audit=0`, `npm run build=0` e **publica 5
  páginas**, uma delas com título invisível em inglês. É a mesma classe da dívida D-2 que eu
  registrei no TCK-0014 (`str.strip()`/`.trim()` não removem U+200B/U+2060/U+FEFF), e o
  leitor daqui **espelha** o contrato do acervo em vez de afrouxá-lo — sem inversão entre as
  ferramentas. *Gatilho:* o primeiro nó novo no acervo. Conserto é no TCK-0014, não aqui.
- **`ACTION` 1 (privacidade, para o usuário/`tech-lead`) — o ponto cego do critério 12 fica
  fora do repositório.** Vercel Web Analytics e Speed Insights se ligam **no painel** e
  injetam script na resposta HTML na borda, **sem nenhuma mudança no repositório** — o passo
  de CI inspeciona `dist/`, então nunca veria. Antes ou logo após o primeiro deploy, conferir
  que os dois estão **desligados** no projeto, e verificar no ar:
  `curl -s https://mathematics-studies.vercel.app/ | grep -icE '/_vercel/|insights|speed-insights'`
  tem de dar **0**. Sugiro ticket para automatizar essa verificação contra a URL pública.
- **`ACTION` 2 — não existe página 404 do produto.** `dist/404.html` não é emitido; quem erra
  a URL cai no 404 genérico do host, monolíngue em inglês e sem link de volta. Fora do escopo
  deste ticket; cabe na task 5 (índice) ou em ticket próprio.
- **`ACTION` 3 — slug em caixa mista continua aprovado pelas duas auditorias do acervo**
  (S3/`[008]`): o passo de CI é rede, não conserto. Segue com o `tech-lead`/TCK-0014.
- **`ACTION` 4 — proteção de branch em `main` e previews por PR** continuam sendo ato do
  usuário; sem a primeira, o portão de merge é informativo e quem segura a publicação é o
  `prebuild`.

- Limpeza confirmada ao fim: `git status --porcelain -- content/` **vazio** · `ls public/` =
  **só `robots.txt`** · `docs/`, `scripts/`, `tools/` e os demais tickets **não tocados por
  mim** (o que aparece em `docs/architecture/` é do TCK-0016) · servidor de `preview`
  encerrado · fixtures e cópia isolada fora do repositório.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [x] 10 · [x] 11 · [x] 12 · [x] 13 — **13/13 com evidência própria. Nenhum defeito.**
- Lição: n/a — nenhum `REJECT` a resolver nesta entrada; as dívidas D-1 a D-3 saem com gatilho
  nomeado, e as classes que elas exercitam já estão indexadas em `L-019` (adendos 1–3) e nas
  lições do TCK-0014.
