# Log — TCK-0011

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 16:00 — tech-lead
- Ação: criação do ticket a partir da ACTION A-4 do `qa-validator#4` (`TCK-0003/log.md`
  `[015]`), confirmada antes pelo `code-reviewer` em `[014]` ("Pendências e riscos"). Trecho
  de origem copiado verbatim.
- Motivo: o `ADR-0003` foi aceito e destravou a frente de plataforma, mas o desenho parou no
  nível de Contexto e o pipeline de CI/CD segue marcado `PROPOSTO` sem nenhum ADR que o
  cubra — enquanto `.github/workflows/ai-surface-audit.yml` já roda. Desenho e realidade em
  desacordo é o que produz decisão implícita na hora de implementar.
- Resultado: ok — `tickets/TCK-0011-container-architecture-and-cicd/` criado.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 16:03 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** o diagrama de Container e a decisão de CI/CD
  são a mesma pergunta vista de dois lados — a caixa "build → host" só para de ser um
  retângulo vago quando alguém decide onde o CI roda e o que ele executa —, têm o mesmo dono
  e o mesmo prazo (antes do primeiro ticket de implementação), e separá-los faria o diagrama
  nascer já com um `PROPOSTO` órfão, que é justamente o defeito que ele vem consertar.
- **Tipo:** `infra`. É desenho e decisão de build/deploy/ambientes. **Desvio de cadeia
  justificado:** a cadeia padrão de `infra` é `devops-engineer`, mas o entregável aqui é
  **arquitetura e ADR** — área exclusiva do `platform-architect` (AGENTS.md §10). O
  `devops-engineer` entra no ticket **seguinte**, para implementar o que o ADR-0006 decidir.
- **Prioridade P3 · tamanho M.** P3 porque nada em curso depende disto: a Fase 1 é de
  conteúdo, e a aplicação não existe (`find . -name package.json` → vazio). O prazo é
  **relativo, não temporal**: fechar antes do primeiro ticket de implementação da Fase 2.
  Rebaixar para P3 é decisão consciente — trabalhar arquitetura antes do conteúdo inverteria a
  ordem deliberada do `docs/product/roadmap.md` ("o contrato de conteúdo vem antes da
  aplicação").
- **Owner: `platform-architect`.** Arquitetura, dados, deploy e ADRs.
- **Cadeia:** `tech-lead` → `platform-architect` → `code-reviewer` → `qa-validator`. O aceite
  do ADR-0006 **não** faz parte do `done`: aceitar é ato do usuário, como foi o `ADR-0003`
  (que precisou de ticket próprio, TCK-0003). O ticket entrega o ADR `proposed` com
  recomendação — assim ele fecha sem depender de resposta humana, e a pergunta ao usuário fica
  registrada em "Perguntas em aberto".
- **Restrições passadas ao executor:**
  1. **L-011 e L-013 são o risco central deste ticket:** o TCK-0003 gastou dois loops porque
     um rótulo de Mermaid decidia o que o texto dizia não decidir. Diagrama é normativo
     (`docs/DOC-STANDARDS.md`) — cada caixa tem de ser resultado decidido ou `PROPOSTO` com
     ADR nomeado.
  2. O container tem de caber no `ADR-0003` já aceito: independência do contrato de dados
     (`:157-174`) e portabilidade do host estático (`:151-155`). Contradizer o ADR aceito é
     defeito bloqueante, não sugestão.
  3. **Custo zero com fonte** (critério 6): limite do plano gratuito citado com URL e data —
     afirmação de gratuidade sem fonte é o tipo de coisa que envelhece em silêncio.
  4. Não criar nem alterar `.github/workflows/` (critério 9) e não escolher biblioteca de UI,
     de teste ou estratégia de service worker.
  5. Telemetria e backend continuam fora: exigem ADR próprio (`ADR-0003:143-145`).
- **Aderência ao plano:** Fase 2 do roadmap ("Leitor de conteúdo") pressupõe build, deploy e
  PWA; este ticket é o pré-requisito documental dela, não uma antecipação de implementação.
  Dentro do plano.
- **Requisitos inegociáveis conferidos:** offline/PWA entra como elemento obrigatório do
  diagrama; custo zero vira critério com evidência; privacidade fica protegida por proibição
  explícita de introduzir telemetria; bilinguismo aparece como rotas por idioma. a11y e
  correção matemática não são acionados, com o porquê registrado no ticket.
- **Dependências:** nenhuma dura. Se o `TCK-0008` ainda não tiver rodado, atenção: parte da
  superfície de IA ainda descreve a stack como indecidida e pode induzir o executor a
  hesitar — o `ADR-0003` está `accepted` desde 2026-08-01.
- Resultado: ok — `status: triaged`, `owner: platform-architect`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.

## [003] HANDOFF — 2026-08-01 16:18
- De: tech-lead → Para: platform-architect
- Status novo: in_progress
- O que foi feito: nada de execução. A triagem `[002]` fechou sem `HANDOFF` de propósito
  (L-005), aguardando ordem de execução. A ordem chegou em 2026-08-01: o usuário pediu o
  início da implementação e o `task-router` (`.dev-loop/start-implementation/briefings/01-route.md`)
  concluiu que `docs/specs/minimum-learning-slice/tasks.md` **não tem task de bootstrap do
  esqueleto** (não há `package.json`, estrutura nem dependência) — as tasks 3 e 4 (TCK-0013 e
  TCK-0014, em execução paralela) não dependem dele, a task 5 sim. Essa lacuna entra no escopo
  deste ticket em vez de virar task nova numa spec já aprovada.
- Artefatos: nenhum ainda. Entrada registrada pelo próprio `platform-architect` ao assumir,
  para não deixar buraco na cadeia (regra de auditoria 2).
- Como validar: `.dev-loop/start-implementation/briefings/01-route.md` (decisão de
  encaminhamento) e `docs/specs/minimum-learning-slice/tasks.md` (ausência de task de
  esqueleto entre as tasks 1–15).
- Pendências e riscos: escopo ampliado em relação ao ticket original — além dos critérios 1–10
  já escritos, o executor deve especificar o **esqueleto da aplicação** (estrutura de
  diretórios, conteúdo do `package.json`, gerador concreto, leitura de `content/` na build,
  lugar das ilhas) **sem instalar nada**. A restrição do critério 9 (nenhum `package.json`,
  nenhuma dependência) continua valendo: o produto é especificação, não instalação.
- Critérios de aceite: [ ] 1 a 10 — todos pendentes.

## [004] ACTION — 2026-08-01 16:52 — platform-architect
- Ação: entrega completa do ticket — C4 Container, ADR de CI/CD e **especificação** do
  esqueleto da aplicação (escopo acrescentado pelo `[003]`). Arquivos tocados, todos
  declarados (AGENTS.md §10, regra 2):
  - **novo** `docs/architecture/c4-container.md` — `C4Container` com acervo `content/`,
    validador do contrato, build estática, host estático, páginas por idioma, ilha de
    interatividade, camada offline e progresso local, cada um com tecnologia **e**
    responsabilidade; mais a tabela "Contrato das fronteiras" (o que atravessa × o que nunca
    atravessa cada linha) e a seção Fontes;
  - **novo** `docs/adr/ADR-0006-continuous-integration-and-publication.md` (`proposed`);
  - **novo** `docs/adr/ADR-0007-application-skeleton.md` (`proposed`);
  - **editado** `docs/architecture/c4-context.md` (cabeçalho, `:20`→`:22`, `:26`→`:28`,
    parágrafo "Estado atual × proposta" e Fontes);
  - **editado** `docs/architecture/README.md` (linha do Container + legenda dos marcadores);
  - **editado** `docs/adr/README.md` (edição cirúrgica: só as duas linhas novas);
  - **editado** `memory/context/project-context.md` (decisões em aberto, com as três perguntas
    objetivas ao usuário);
  - **editado** `memory/context/frontend.md`, `memory/agents/platform-architect.md`;
  - **novo** `memory/lessons/public-contract-goes-to-adr-mechanism-goes-to-ticket.md` (L-020)
    + índices `memory/LESSONS.md` e `memory/MEMORY.md`. Numeração: L-019 foi ocupada pelo
    TCK-0014 durante esta execução; a lição nasceu L-020.
- Motivo e decisões, em resumo:
  1. **Três marcadores no diagrama, não dois.** Sem marcador = decidido em ADR aceito;
     `PROPOSTO (ADR-NNNN)` = espera aceite; `EM ABERTO (ticket)` = o `ADR-0003` decidiu **não**
     decidir. Sem o terceiro, toda escolha de ticket viraria `PROPOSTO` órfão — o defeito B4 do
     TCK-0003 pelo avesso. Marcar de mais também é defeito: o boundary "Build e publicação"
     começou rotulado `PROPOSTO` inteiro e foi corrigido, porque a build em si é exigida pelo
     `ADR-0003`; só a **automação** é proposta.
  2. **CI/CD (`ADR-0006`, `proposed`)**: (i) Actions **e** Vercel com papéis separados — Actions
     é portão de merge, Vercel é construtor/publicador, sem segredo no repositório; (ii) o job
     roda os quatro scripts que já existem + validador do acervo + build de verificação, em PR
     e em push para `main`, mantendo a execução semanal; (iii) previews **ativos** por PR, com
     o argumento falseável de que o repositório é público e o `draft` já é legível — a pergunta
     ao usuário continua registrada e a resposta "não" só troca este item; (iv) produção no
     push/merge em `main`, com a ressalva de que "só mescla com verde" depende de proteção de
     branch, que é ato humano.
  3. **Esqueleto (`ADR-0007`, `proposed`)**: Astro confirmado (é o gerador nomeado na decisão do
     `ADR-0003`), projeto na raiz, `src/{content-contract,pages,layouts,components,islands,styles}`,
     `package.json` mínimo (só `astro`; `private: true`; `engines.node >= 22.12.0`; `prebuild`
     → `validate:content`), `content/` lido por módulo próprio que **não importa nada do
     gerador** (coleções de conteúdo recusadas: pediriam frontmatter, e os metadados vivem em
     `meta.json`), ilha recebendo dado validado como propriedade e **sem requisição de rede**.
     URL com prefixo de idioma **em minúsculas** (`/pt-br/…`) — divergência consciente do
     exemplo ilustrativo do critério 1 (`/pt-BR/`), justificada no ADR (host estático é
     sensível a maiúsculas e canonicalizar exigiria redirect proprietário, contra a
     portabilidade do `ADR-0003`); as **duas** grafias aparecem no rótulo do diagrama e a
     escolha é pergunta ao usuário.
  4. **O que deliberadamente NÃO foi decidido**, para não repetir o defeito B2 do TCK-0003:
     biblioteca de UI, ferramenta de teste, mecanismo da camada offline e momento em que a
     matemática vira HTML. Régua usada (L-020): "se eu trocar isto em seis meses, quem quebra?"
     — se a resposta for só o nosso próprio código, é ticket.
  5. **Nada de propagação para regras de agente**: `ADR-0006` e `ADR-0007` estão `proposed`;
     L-010 vale para ADR **aceito**. Propagar agora seria transformar hipótese em regra.
- Resultado: ok, com evidência.
  - Critério 2 (diagrama não prescreve mecanismo):
    `awk '/^```mermaid/,/^```$/' docs/architecture/c4-container.md | grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"`
    → nenhuma ocorrência (exit 1).
  - Critério 7 (nenhum `PROPOSTO` órfão): `grep -n "PROPOSTO" docs/architecture/c4-context.md`
    → 3 ocorrências, **todas** com `(ADR-0006)`.
  - Critério 9: `git status --porcelain .github/workflows/` → vazio;
    `find . -name package.json -not -path "./node_modules/*"` → vazio. Nenhuma dependência
    instalada, nenhum `npm` executado.
  - Critério 10: `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (exit 0);
    `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos` (exit 0);
    `python3 scripts/sync-ai-adapters.py --check` → exit 0.
  - Critério 6 (custo com fonte): tabela no `ADR-0006` com URL e data de consulta
    (2026-08-01) para GitHub Actions em repositório público e para os limites do Vercel Hobby;
    a condição de elegibilidade foi verificada, não presumida:
    `gh repo view --json isPrivate,visibility` → `{"isPrivate":false,"visibility":"PUBLIC"}`,
    e o repositório pertence a conta pessoal (`git remote -v` → `dougmotshell`), o que importa
    porque projeto Hobby **não** conecta a repositório de organização.
- Lição: L-020 (registrada nesta execução) — não resolve `REJECT`.

## [005] HANDOFF — 2026-08-01 16:58
- De: platform-architect → Para: code-reviewer
- Status novo: in_review
- O que foi feito: C4 Container desenhado, `ADR-0006` (CI/CD, `proposed`) e `ADR-0007`
  (esqueleto da aplicação, `proposed`) escritos, `c4-context.md` sem `PROPOSTO` órfão e
  `project-context.md` com as três perguntas objetivas ao usuário. Nenhum código, nenhum
  `package.json`, nenhuma dependência, nenhum arquivo de pipeline — o entregável é
  especificação.
- Artefatos: `docs/architecture/c4-container.md` (novo), `docs/adr/ADR-0006-continuous-integration-and-publication.md`
  (novo), `docs/adr/ADR-0007-application-skeleton.md` (novo), `docs/architecture/c4-context.md`,
  `docs/architecture/README.md`, `docs/adr/README.md`, `memory/context/project-context.md`,
  `memory/context/frontend.md`, `memory/agents/platform-architect.md`,
  `memory/lessons/public-contract-goes-to-adr-mechanism-goes-to-ticket.md`, `memory/LESSONS.md`,
  `memory/MEMORY.md`. Sem commit (AGENTS.md §11).
- Como validar:
  1. `awk '/^```mermaid/,/^```$/' docs/architecture/c4-container.md | grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"` → sem ocorrência;
  2. `grep -n "PROPOSTO" docs/architecture/c4-context.md` → toda ocorrência com ADR nomeado;
  3. `git status --porcelain .github/workflows/` → vazio; `find . -name package.json` → vazio;
  4. `bash scripts/audit-ai-surface.sh` → `Resultado: OK`; `bash scripts/audit-content.sh` →
     `0 erros · 0 avisos`; `python3 scripts/sync-ai-adapters.py --check` → exit 0;
  5. conferir que `ADR-0006`/`ADR-0007` aparecem como `proposed` em `docs/adr/README.md` e em
     `memory/context/project-context.md`, e **em lugar nenhum** como aceitos.
- Pendências e riscos:
  - **Bloqueio real de calendário:** a task 5 da fatia mínima depende do `ADR-0007`, que está
    `proposed`. Aceitar é ato do usuário (precedente: `ADR-0003`/TCK-0003). Enquanto não houver
    aceite, o ticket de bootstrap **não pode** começar — vale a regra "não instruir
    implementação baseada em decisão não aceita".
  - Três perguntas ao usuário, todas em `memory/context/project-context.md`: previews públicos
    por PR (sim/não), `/pt-br/` × `/pt-BR/`, projeto na raiz × em `app/`.
  - Divergência consciente do exemplo do critério 1 (`/pt-BR/`): o diagrama mostra as duas
    grafias e marca a escolha como `PROPOSTO (ADR-0007)`. Se o revisor entender que o critério
    é literal, é REJECT legítimo — mas o argumento técnico está no ADR, não no rótulo.
  - `ADR-0006` pendência 1 (validador em Python × build em Node na mesma imagem) fica em aberto
    de propósito: só se resolve no ticket de pipeline, com evidência.
  - Fora da minha área, registrado nominalmente: `memory/context/devops.md` ainda diz
    "a stack segue indefinida (ADR-0003 `proposed`)" — está desatualizado desde 2026-08-01 e é
    do `devops-engineer`; não corrigi para não editar área alheia.
  - Nenhuma propagação para `AGENTS.md` ou `.github/instructions/`: correto enquanto os dois
    ADRs estiverem `proposed`; ao serem aceitos, L-010 passa a valer e exige varredura da raiz.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [x] 10 — todos com evidência em `[004]`. O critério 4 pede `ADR-0006-<slug>`: entregue como
  `ADR-0006-continuous-integration-and-publication.md`, mais o `ADR-0007` que o escopo
  acrescentado em `[003]` exigiu.

## [006] REJECT — 2026-08-01 17:34
- De: code-reviewer#7 → Para: platform-architect · Loop nº: 1/3
- **Contexto novo, chegado depois do `[004]`:** o usuário decidiu os três pontos abertos —
  URL `/pt-br/` minúsculo (**a sua proposta, confirmada**), previews por PR **ativados**,
  projeto **na raiz**. Nada disso é defeito seu: você entregou antes da decisão, e a
  divergência do exemplo `/pt-BR/` do critério 1 **não** é motivo de reprovação (o critério a
  usava como ilustração e o seu argumento técnico — host estático sensível a maiúsculas,
  canonicalizar exigiria redirect proprietário contra a portabilidade do `ADR-0003` — foi
  aceito). O tratamento do aceite vai como recomendação ao `tech-lead`, no fim desta entrada.
- Defeitos (numerados, cada um com evidência e critério violado):

  1. **[BLOQUEANTE] `ADR-0007` fecha *onde* a validação do RF-18 roda — decisão que a spec
     aprovada atribui ao ticket.** Reincidência do padrão **B2 do TCK-0003** (L-011).
     - Evidência: `docs/adr/ADR-0007-application-skeleton.md:115-121` (seção **Decisão**, item
       4) decide `prebuild` chamando `validate:content` e conclui: *"é isso que faz da
       validação um portão de build, não um lembrete"*.
     - Critério violado: `docs/specs/minimum-learning-slice/plan.md:132` — *"Decisões de
       implementação a tomar nos tickets, sem reabrir a spec"* — item **5** (`:140`): *"onde
       roda a validação do RF-18 (build, runtime ou ambos)"*. A spec está `approved` e
       `spec.md:105` mantém de propósito *"A carga (build ou runtime) rejeita…"*.
     - Reforço pela sua **própria régua (L-020)**: "se eu trocar `prebuild` por gate no CI daqui
       a seis meses, quem quebra?" → só o nosso pipeline. Nenhum link de terceiro, nenhum
       arquivo do acervo, nenhuma fatura, nenhum outro ADR. Pela régua, é **ticket**.
     - Agravante interno: `ADR-0006:201-207` declara que esse mesmo portão **pode ter de mudar
       de lugar** e chama a consequência de *"hipótese, não fato"*; já `ADR-0007:243-245`
       afirma a gêmea **sem** a condicional que `ADR-0006:168-170` colocou na dela.
     - Correção esperada (não a faço eu): o `ADR-0007` exige o **resultado** — acervo inválido
       não vira página, a build falha de forma visível e registrada (RF-18) — e cita `prebuild`
       como forma sugerida, remetendo o **lugar** do portão ao ticket de pipeline
       (`ADR-0006`, pendência 1). Se quiser mesmo fechá-lo aqui, isso contraria `plan.md:132`
       e precisa do `tech-lead`, não deste ADR.

  2. **[BLOQUEANTE] O diagrama do Container afirma esse mecanismo sem marcador.** Reincidência
     do padrão **B4 do TCK-0003** (L-013): mecanismo que nenhum ADR **aceito** cobre, com
     marcação inconsistente dentro do mesmo bloco.
     - Evidência: `docs/architecture/c4-container.md:44` —
       `Rel(build, validator, "Só prossegue com acervo aprovado", "Portão da build")`, **sem
       marcador**, num documento cuja convenção (`:5-13`) estabelece que *sem marcador =
       decidido em ADR aceito*. Quem coloca o portão na build é o `ADR-0007`, `proposed`; e
       `ADR-0006:206-207` chama exatamente esse enunciado de **hipótese**.
     - Inconsistência dos três marcadores, no mesmo diagrama: `:42` (`ci → validator`) leva
       `PROPOSTO (ADR-0006)`; `:46` (`build → host`) leva `gatilho PROPOSTO (ADR-0006)`; `:44`
       não leva nada. O nó `:28` também apresenta o validador sem marcador, ancorado num
       ticket **em curso** (TCK-0014).
     - Critério violado: critério 2 do ticket — *"o que não estiver decidido aparece marcado
       `PROPOSTO` com o ADR pendente citado"* — e a regra do `docs/architecture/README.md`
       (sua, editada neste diff): *"o marcador tem de citar o ADR pendente"*.
     - **Varredura da classe, obrigatória (L-013):** conferir `:49`
       `Rel(pages, island, …, "Dados já validados passados como propriedade")` e a linha `:83`
       da tabela de fronteiras — "passados como propriedade" é decidido em
       `ADR-0007:155-165` (`proposed`). Ou marcar, ou registrar no log por que decorre do
       `ADR-0003:106-108` (ilha com fronteira explícita) somado ao payload sem rede. As duas
       saídas me servem; o silêncio, não.

- Sugestões (não bloqueiam):
  - **S1 — marcar de mais, no mesmo diagrama.** `c4-container.md:27`: o nó `ci` está
    `PROPOSTO (ADR-0006)` **inteiro**, mas o workflow existe e roda hoje — `ADR-0006:16-19` o
    chama de "fato consumado". É o mesmo excesso que você corrigiu no boundary `:26`. Estilo
    coerente com `:29`/`:30`: *"GitHub Actions, workflow já em uso (auditorias); portão de
    merge PROPOSTO (ADR-0006)"*.
  - **S2 —** `ADR-0007:29` afirma *"Três dessas escolhas são contrato público e permanente"*.
    "Onde mora o projeto" não é observável de fora (nenhuma URL muda) — pela régua L-020 ela é
    ticket. Pode continuar no ADR (afeta configuração de host que não está no Git,
    `ADR-0006:183-185`), mas o adjetivo não se sustenta para as três.
  - **S3 —** `ADR-0006:145`, "1 build concorrente": conferi **verbatim** na fonte citada as
    outras cinco linhas (100 deployments/dia, 100 builds/hora, 45 min, cache 1 GB, 100 GB Fast
    Data Transfer) e a restrição de organização; a concorrência **não** está nessa página.
    Trocar a fonte da linha ou remover o número.
  - **S4 —** `memory/context/devops.md:15` segue "a stack segue indefinida (ADR-0003
    `proposed`)". Você editou `memory/context/frontend.md` e recusou `devops.md` por "área
    alheia": `memory/context/` é memória **do projeto** (AGENTS.md §5), não do agente — o
    critério ficou assimétrico. Corrigir junto ou abrir ticket nominal.

- O que já está bom (não refazer):
  - **Critérios 1, 3, 4, 5, 6, 7, 8, 9 e 10 verificados e atendidos por mim**, com exceção
    apenas do que os defeitos 1 e 2 tocam.
  - **Mermaid:** os **4** blocos do diff (`c4-container`, `c4-context`, `ADR-0006`, `ADR-0007`)
    passam no parser (`mermaid@11` + `jsdom`, `mermaid.parse()`), 39/20/10/10 linhas.
  - **Critério 2 (grep):** `awk '/^```mermaid/,/^```$/' … | grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"` → exit 1, nenhuma ocorrência. Reproduzido.
  - **Critério 7:** `grep -n "PROPOSTO" docs/architecture/c4-context.md` → 3 ocorrências,
    todas com `(ADR-0006)`. Nenhum `PROPOSTO` órfão restante.
  - **Critério 6 — custo, reverificado na fonte, não aceito do log:** repositório **público**
    confirmado (`gh repo view --json isPrivate,visibility,owner` → `isPrivate:false`,
    `PUBLIC`, `login:dougmotshell`, conta pessoal; `git remote -v` confere). Citação do GitHub
    conferida palavra a palavra na página: *"GitHub Actions usage is free for self-hosted
    runners and for public repositories that use standard GitHub-hosted runners"* — e a sua
    ressalva "runner padrão" cobre a exceção dos larger runners. Vercel: *"Vercel does not
    support connecting a project on your Hobby team to Git repositories owned by Git
    organizations"* (verbatim), *"non-commercial, personal use only"* e *"there are no billing
    cycles … wait until 30 days"* — a premissa de custo zero **se sustenta**, e a consequência
    "estourar pausa, não fatura" está correta. As 4 URLs citadas respondem 200.
  - **Critério 9 / nada instalado:** `find . -name package.json -not -path './node_modules/*'`
    → vazio; `git status --porcelain .github/workflows/` → vazio; nenhum artefato de build no
    working tree. O entregável é especificação, como prometido.
  - **Critério 10 reexecutado por mim:** `sync-ai-adapters.py --check` exit 0 ("Tudo já estava
    atualizado"); `audit-ai-surface.sh` → `Resultado: OK` (exit 0); `audit-content.sh` →
    `1 nós · 0 erros · 0 avisos` (exit 0).
  - **Restrições vigentes preservadas:** sem backend, conta, login ou telemetria (o
    `ADR-0006:173-175` ainda desliga Web Analytics e Speed Insights explicitamente); gabarito
    no cliente declarado nas duas pontas; rotas por idioma com paridade (`ADR-0002`);
    offline-first presente como container; independência do contrato de `content/` reforçada
    com teste falseável (`grep -rn "astro" src/content-contract/` → vazio). Nenhuma
    contradição com o `ADR-0003` aceito.
  - **Ponto 5 da revisão — não propagar para `AGENTS.md`/`.github/instructions/`: você está
    certo.** L-010 vale para ADR **aceito**; no TCK-0003 o `ADR-0003` estava `accepted`, e é
    essa a diferença. Varri a raiz: `ADR-0006`/`ADR-0007` aparecem em 11 arquivos e **em
    nenhum** como aceitos; `sync --check` limpo confirma que nenhuma fonte canônica foi tocada.
  - **`docs/adr/README.md`:** edição cirúrgica de verdade — `+2 −0`, só as duas linhas novas.
  - **L-020 é lição legítima, não racionalização.** Ela **referencia** L-011 e acrescenta um
    "Como aplicar" executável e distinto (L-011 = o que não escrever; L-020 = teste para
    arbitrar *antes* de redigir). ID sem colisão, `Tipo: sucesso` batendo com a seção de
    `memory/LESSONS.md`. E a régua **se sustenta** — foi justamente aplicando-a que encontrei o
    defeito 1: a URL passa no teste (quebra link de terceiro → ADR) e o portão de build não
    passa (quebra só o nosso pipeline → ticket). A camada offline está do lado certo por
    **mérito** e por vínculo ao `ADR-0003:97-99`, não por conveniência.
  - **Ponto 4 da revisão — a pendência do runtime do validador:** declarar como pendência **é
    suficiente** para um ADR `proposed`, e o `ADR-0006:201-207` faz isso bem (condiciona a
    consequência e exige evidência no ticket). O problema não é a pendência; é o `ADR-0007` e
    o diagrama afirmarem como fato o que ela mantém em aberto — defeitos 1 e 2.

- **Recomendação ao `tech-lead` (decisão do usuário chegada em 2026-08-01, após o `[004]`):**
  1. **Não** marcar `ADR-0006`/`ADR-0007` como `accepted` dentro deste ticket. O aceite é ato
     do usuário e teve ticket próprio no precedente (`ADR-0003` → TCK-0003); e um ADR marcado
     `accepted` dispara L-010 (varredura da raiz + `AGENTS.md` + `.github/instructions/` +
     `sync`), que é trabalho de outro escopo. Manter `proposed` aqui está **correto**.
  2. O ticket de aceite deve, na mesma entrega: fixar a decisão dos três pontos; **remover a
     grafia alternativa** que hoje aparece como opção viva em `c4-container.md:34`
     ("`/pt-BR/…` e `/en-US/…` como alternativa — PROPOSTO (ADR-0007)"), em `ADR-0007:270-275`
     (Perguntas ao usuário) e em `memory/context/project-context.md`; e converter os
     `PROPOSTO (ADR-0006/0007)` do diagrama em decidido.
  3. **Não** antecipar esses ajustes no loop de correção deste REJECT: enquanto os ADRs
     estiverem formalmente `proposed` em `docs/adr/README.md`, apagar a alternativa do diagrama
     recriaria o desacordo entre desenho e realidade que este ticket veio consertar.

## [007] ACTION — 2026-08-01 17:45 — platform-architect
- Ação: correção do `[006] REJECT` (loop 1/3). Os dois defeitos eram **o mesmo assunto** — o
  portão de validação do acervo — vistos no texto (B1) e no desenho (B2), e ambos são
  reincidência de família já documentada. Aceito os dois; o revisor está certo, inclusive ao
  usar a minha própria régua (L-020) contra o meu texto.
- **B1 — `ADR-0007` fechava *onde* o portão roda.** Corrigido para exigir **resultado**, não
  mecanismo, e a varredura foi pela **classe** (`grep -rn "prebuild\|portão da build"` na raiz),
  não pelas linhas citadas — sete pontos em cinco arquivos:
  1. `ADR-0007` item 4 (`:115-122`): `prebuild` deixou de ser decisão; o exigido é RF-18 — nó
     que viole o contrato **não vira página publicada**, com falha visível e registrada — e o
     **lugar** do portão (script, job de CI ou ambos) remete a `plan.md` item 5 e à pendência 1
     do `ADR-0006`. `validate:content` permanece como **ponto de entrada nomeado**, que é
     justamente o que torna as três formas equivalentes de configurar.
  2. `ADR-0007` item 5 (leitor): "invocado pelo `prebuild`" → "invocado pelo portão que o ticket
     definir"; o "falha alto" do módulo foi renomeado como **rede de segurança**, não portão.
  3. `ADR-0007`, bloco Mermaid: nó `validate:content … (prebuild)` → `Validação do contrato —
     RF-18 … onde o portão roda: EM ABERTO (ticket)`; e "Build falha" → "Nenhuma página do nó é
     publicada".
  4. `ADR-0007`, consequência gêmea (`:243-245`): agora diz "acervo inválido não vira página
     publicada", condicionada como a do `ADR-0006` e declarada **exigência, não fato observado**
     enquanto o portão não existir. Era esse o agravante do defeito — dois documentos da mesma
     entrega discordando sobre o mesmo fato.
  5. `ADR-0006`, bloco Mermaid: `Build na Vercel / validador no portão da build` → `acervo
     reprovado não é publicado / lugar do portão: EM ABERTO (ticket)`.
  6. `ADR-0006`, Leitura e pendência 1: "portão da build" → "portão no caminho de publicação",
     com a escolha do lugar explicitamente devolvida ao ticket.
  7. `memory/context/frontend.md`: o resumo do esqueleto repetia `prebuild` — trocado, e
     acrescentado item "não decidido, e nenhum ADR deve decidir".
- **B2 — marcador ausente no diagrama do Container**, com varredura nó a nó e relação a
  relação (receita nova: escrever ao lado de cada elemento a fonte que o sustenta; o que ficar
  sem fonte é o defeito):
  - `Rel(build, validator)`: agora `"Nó reprovado não vira página publicada (RF-18) — lugar do
    portão EM ABERTO (ticket)"`. Escolhi `EM ABERTO`, não `PROPOSTO`: nenhum ADR **deve**
    fechá-lo, então `PROPOSTO (ADR-NNNN)` seria mentira de outro tipo.
  - `Rel(pages, island)`: "dados passados **como propriedade**" era mecanismo do `ADR-0007`
    (`proposed`) afirmado sem marcador — reescrito como resultado ("recebe dado já validado e
    **não busca dado na rede**"), que decorre de `ADR-0003` (fronteira explícita da ilha +
    ausência de backend + offline do conteúdo visitado). Mesma correção na linha da tabela de
    fronteiras, esta citando o `ADR-0007` como proposta.
  - Nó `validator`: âncora trocada de "TCK-0014" para "exigido pela spec da fatia mínima
    (RF-18); entrega em curso no TCK-0014" — o que o sustenta é a spec aprovada, não o ticket.
  - **S1 acatada (marcar de mais, mesma classe):** nó `ci` e `Rel(ci, validator)` separavam mal
    o que já roda do que é proposta; agora dizem "auditorias hoje; portão de merge / validador /
    build de verificação PROPOSTO (ADR-0006)".
  - Legenda dos marcadores atualizada em `c4-container.md` e em `docs/architecture/README.md`:
    ausência de marcador passa a significar "sustentado por ADR aceito **ou spec aprovada**, com
    a fonte no rótulo"; marcador em contêiner **vale para as relações que decorrem dele**
    (é por isso que as duas relações de cache não repetem o `EM ABERTO` da camada offline); e
    ficou escrito que **marcar de menos e marcar de mais são o mesmo defeito**.
- **S2 acatada:** `ADR-0007:29` não diz mais que as três escolhas são contrato público — só a
  **URL** é; as outras duas são coordenação entre tickets e configuração de host. **S3
  acatada:** "1 build concorrente" removido da tabela de custo (não está na página citada; as
  outras seis linhas o revisor conferiu verbatim). **S4 acatada:** corrigi
  `memory/context/devops.md`, que ainda dizia "a stack segue indefinida (ADR-0003 `proposed`)"
  — o revisor tem razão de que `memory/context/` é memória **do projeto**, não do agente, e o
  meu critério estava assimétrico; registrei lá também as duas pendências que são daquela área.
- **Decisões do usuário, registradas e NÃO aplicadas neste loop** (conforme a recomendação 3 do
  `[006]`, que acato): URL `/pt-br/` minúsculo (confirma a proposta), previews por PR ativados,
  projeto na raiz. Onde serão aplicadas, no ticket de aceite: `docs/adr/README.md` (status),
  cabeçalho dos dois ADRs, `ADR-0007` seção "Perguntas ao usuário" (`:270-275`),
  `c4-container.md:34` (remoção da grafia alternativa e conversão dos `PROPOSTO`),
  `memory/context/project-context.md` e, aí sim, a varredura da raiz exigida por L-010.
  Enquanto os ADRs estiverem `proposed`, apagar a alternativa recriaria o desacordo entre
  desenho e realidade que este ticket veio consertar.
- Resultado: ok, com evidência.
  - B1, varredura da classe: `grep -rn "prebuild\|portão da build" docs/` → única ocorrência
    restante é `ADR-0007:122`, que agora **lista** `prebuild` como uma das opções do ticket.
  - B2, critério 2 reexecutado:
    `awk '/^```mermaid/,/^```$/' docs/architecture/c4-container.md | grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"`
    → exit 1, nenhuma ocorrência. Toda `Rel` e todo nó do bloco conferidos um a um.
  - Critério 7 intacto: `grep -n "PROPOSTO" docs/architecture/c4-context.md` → 3 ocorrências,
    todas com `(ADR-0006)`.
  - Critério 9 intacto: `git status --porcelain .github/workflows/` → vazio;
    `find . -name package.json` → vazio.
  - Critério 10: `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (exit 0);
    `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos` (exit 0);
    `python3 scripts/sync-ai-adapters.py --check` → exit 0.
- **Honestidade sobre a reincidência (pedida no `[006]`):** é a terceira ocorrência da mesma
  família hoje e a causa raiz é a **mesma** de L-011 e L-013 — por isso **não** criei lição
  nova com nome diferente; registrei **adendos** nos três arquivos existentes. A distinção que
  faltava, e que é o aprendizado real: (a) L-011 — a decisão indevida não entra pela lista de
  decisões, entra como **justificativa de apoio** de outro item ("é isso que faz X ser Y, e não
  Z"), e por isso escapa da triagem feita *antes* de redigir; (b) L-020 — a régua precisa de um
  **segundo passe sobre o texto pronto**, frase a frase, diagramas e `scripts` inclusive; (c)
  L-013 — a classe de marcação tem **duas direções**, e achar um "marcar de mais" aumenta a
  chance de existir um "marcar de menos", em vez de encerrar a varredura.
- Lição: L-011, L-013 e L-020 — adendos escritos nos três arquivos existentes (nenhuma lição
  nova: mesma causa raiz).

## [008] HANDOFF — 2026-08-01 17:52
- De: platform-architect → Para: code-reviewer
- Status novo: in_review
- O que foi feito: B1 e B2 do `[006]` corrigidos por classe, não por linha citada. O `ADR-0007`
  passou a exigir **resultado** (nó reprovado não vira página publicada, RF-18) e devolveu ao
  ticket o **lugar** do portão; a consequência gêmea ficou condicionada como a do `ADR-0006`; o
  diagrama do Container ganhou marcador em `Rel(build, validator)` (`EM ABERTO (ticket)`, não
  `PROPOSTO`, porque nenhum ADR deve fechar isso), teve o mecanismo "como propriedade"
  reescrito como resultado e o excesso de marcação em `ci` corrigido. S1–S4 acatadas. As três
  decisões do usuário estão **registradas e não aplicadas**, com o inventário de onde entram no
  ticket de aceite.
- Artefatos: `docs/adr/ADR-0007-application-skeleton.md`,
  `docs/adr/ADR-0006-continuous-integration-and-publication.md`,
  `docs/architecture/c4-container.md`, `docs/architecture/README.md`,
  `memory/context/frontend.md`, `memory/context/devops.md` (S4),
  `memory/agents/platform-architect.md`, e adendos em
  `memory/lessons/{adr-decides-constraints-not-implementation-timing,fixing-the-cited-line-is-not-fixing-the-defect-class,public-contract-goes-to-adr-mechanism-goes-to-ticket}.md`.
  Sem commit. `docs/adr/README.md`, `c4-context.md` e `project-context.md` **não** foram
  tocados neste loop — já estavam aprovados.
- Como validar:
  1. `grep -rn "prebuild\|portão da build" docs/` → só `ADR-0007:122`, e lá `prebuild` aparece
     como **uma das opções do ticket**, não como decisão;
  2. `awk '/^```mermaid/,/^```$/' docs/architecture/c4-container.md | grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"` → exit 1;
  3. no bloco Mermaid do Container, cada `Rel` e cada nó tem fonte no rótulo (ADR aceito, spec
     aprovada, `PROPOSTO (ADR-NNNN)` ou `EM ABERTO (ticket)`) — inclusive `Rel(build, validator)`;
  4. `grep -n "PROPOSTO" docs/architecture/c4-context.md` → 3, todas com ADR nomeado;
  5. `git status --porcelain .github/workflows/` → vazio; `find . -name package.json` → vazio;
  6. `bash scripts/audit-ai-surface.sh` → `Resultado: OK`; `bash scripts/audit-content.sh` →
     `1 nós · 0 erros · 0 avisos`; `python3 scripts/sync-ai-adapters.py --check` → exit 0;
  7. `ADR-0006` e `ADR-0007` seguem `proposed` em `docs/adr/README.md` e no cabeçalho — e em
     lugar nenhum como aceitos.
- Pendências e riscos:
  - **Não reparsei os blocos Mermaid**: não há Node nem `mermaid` no ambiente e instalar
    contraria o critério 9. As alterações são de texto **dentro** de rótulos já existentes, sem
    mudança estrutural; se o revisor tiver o parser, vale reexecutar.
  - O ticket de aceite continua sendo pré-requisito da task 5 — `ADR-0007` `proposed` bloqueia
    o bootstrap. Inventário de onde as três decisões do usuário entram está no `[007]`.
  - `ADR-0006` pendência 1 (Python do validador + Node da build na mesma imagem) segue aberta
    de propósito, agora sem afirmar o lugar do portão.
  - Reincidência assumida no `[007]`: adendos em L-011, L-013 e L-020, sem lição nova.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [x] 10 — os oito já aprovados em `[006]` seguem intactos; 2 e 10 reexecutados após a
  correção.

## [009] HANDOFF — 2026-08-01 18:26
- De: code-reviewer#7 → Para: qa-validator
- Status novo: in_validation
- O que foi feito: **B1 e B2 do `[006]` resolvidos**, e resolvidos pela **classe**, não pelas
  linhas que citei. O `ADR-0007` deixou de fechar *onde* o portão do RF-18 roda e passou a
  exigir o **resultado**; a consequência gêmea ficou condicionada como a do `ADR-0006`,
  encerrando a contradição entre os dois documentos da mesma entrega; a relação
  `build → validador` do diagrama ganhou `EM ABERTO (ticket)`; o excesso de marcação em `ci`
  (S1) e dois casos que ele achou sozinho foram corrigidos. S2, S3 e S4 acatadas. **Aprovado.**
- Artefatos revisados neste loop: `docs/adr/ADR-0007-application-skeleton.md`,
  `docs/adr/ADR-0006-continuous-integration-and-publication.md`,
  `docs/architecture/c4-container.md`, `docs/architecture/README.md`,
  `memory/context/frontend.md`, `memory/context/devops.md`,
  `memory/agents/platform-architect.md` e os adendos em `memory/lessons/{adr-decides-constraints-not-implementation-timing, fixing-the-cited-line-is-not-fixing-the-defect-class, public-contract-goes-to-adr-mechanism-goes-to-ticket}.md`.
  `docs/adr/README.md`, `c4-context.md` e `project-context.md` conferidos como **inalterados**
  desde o `[004]` (`git diff --stat`: +2/−0, 14/8, 16/1 — idênticos aos que aprovei no `[006]`).

- **Verificação de B1 — feita por varredura da raiz, não pela dele.**
  `grep -rn "prebuild\|portão da build" . --exclude-dir=.git --exclude-dir=.dev-loop`
  (ele rodou só em `docs/`): **uma** ocorrência em artefato normativo,
  `ADR-0007:122` — *"Onde o portão roda — script `prebuild`, job de CI, ou os dois — é decisão
  do ticket de pipeline"*. **Sobra legítima**: ali `prebuild` é item de uma enumeração de
  opções do ticket, com remissão a `plan.md` item 5 e à pendência 1 do `ADR-0006`. As demais
  ocorrências são log deste ticket, memória e o texto histórico das lições. Confirmei os sete
  pontos declarados, um a um: `ADR-0007:118-125` (item 4), `:152-155` (item 5, "rede de
  segurança, não portão"), o nó do Mermaid (`onde o portão roda: EM ABERTO (ticket)`),
  `:245-249` (consequência agora condicionada **e** declarada "exigência, não fato observado"),
  o Mermaid do `ADR-0006` (`lugar do portão: EM ABERTO (ticket)`), a Leitura e a pendência 1 do
  `ADR-0006` ("portão no caminho de publicação"), e `memory/context/frontend.md`.
  - **Prova de que o conflito concreto não existe:** o TCK-0015 está decidindo isto agora, e
    `tickets/TCK-0015-application-skeleton-and-deploy/ticket.md:55` diz *"Onde a validação do
    RF-18 roda (`prebuild`, script de CI ou outro ponto) é decisão…"* — os dois documentos
    agora dizem a mesma coisa. Era este o risco de o defeito passar.

- **Verificação de B2 — o argumento `EM ABERTO` × `PROPOSTO` está certo, e eu o adoto.**
  `PROPOSTO (ADR-NNNN)` significa "espera aceite de um ADR"; usá-lo aqui afirmaria que **algum
  ADR deve** fechar o lugar do portão, quando a spec aprovada (`plan.md`, item 5) o atribui ao
  ticket. Seria trocar um erro por outro da mesma família. Ele também **generalizou a legenda**
  (`c4-container.md:13-15`) de "o que o `ADR-0003` deliberadamente não decide" para "o que
  nenhum ADR decide de propósito" — mudança necessária, porque aqui a fonte é a spec, não o
  `ADR-0003`; não estava na minha lista e está correta.
  - Os dois achados próprios conferidos: `Rel(pages, island)` (`:56`) deixou de afirmar
    mecanismo ("como propriedade", do `ADR-0007` `proposed`) e virou resultado — *"a ilha recebe
    dado já validado e não busca dado na rede"* —, que decorre de `ADR-0003:106-108` + ausência
    de backend + offline do visitado; a linha `:93` da tabela de fronteiras passou a marcar a
    proposta explicitamente. Nó `validator` (`:35`) reancorado na **spec aprovada (RF-18)** em
    vez do ticket em curso. S1: `ci` (`:34`) e `Rel(ci, validator)` (`:49`) agora separam o que
    roda hoje do que é proposta.

- **Auditoria da legenda nova, elemento por elemento** (pedida: "legenda que promete mais do que
  o diagrama cumpre é o mesmo defeito com outra roupa"). Percorri os **22** elementos do bloco
  (14 nós/fronteiras + 14 relações). A promessa **substantiva** — *sem marcador = sustentado por
  ADR aceito ou spec aprovada* — é **verdadeira em todos**: não achei um só elemento sem
  marcador que afirme algo que só um ADR `proposed` sustente. A promessa **literal** — *"a fonte
  aparece no próprio rótulo"* — não se cumpre em 7: `Person(student)`, `Person(contributor)`,
  as fronteiras `origin` e `device`, e as relações `contributor→content`, `contributor→build`,
  `student→pages`. São atores e fatos observáveis, nenhum deles contrabandeia mecanismo — por
  isso classifico como **precisão de redação (S1 abaixo), não bloqueante**: o dano da família
  B4 é o leitor tomar hipótese por decisão, e nenhum desses sete produz esse dano.

- **Reparse do Mermaid — feito por mim, e o risco declarado no `[008]` estava errado.** Há Node
  **v24.14.1** e npm **11.11.0** nesta máquina (instalar `mermaid` no scratchpad não toca o
  repositório e não fere o critério 9). Os **4** blocos do diff passam em `mermaid.parse()`
  (`mermaid@11` + `jsdom`): `c4-container` 39 linhas, `c4-context` 20, `ADR-0006` 10,
  `ADR-0007` 10. Nenhuma regressão estrutural.

- **Inventário das decisões do usuário: completo por construção, incompleto como lista.** A
  varredura da raiz exigida por L-010 (`grep -rn "ADR-0006\|ADR-0007" .`) pega tudo, e ele a
  incluiu. Mas a lista explícita do `[007]` omite seis pontos e traz um número de linha
  defasado — ver S3. Registrado aqui para que o ticket de aceite não dependa só do `grep`.

- **Julgamento dos adendos (L-011, L-013, L-020): forma correta, distinção sustentada.** Não são
  lições superadas — são lições **não aplicadas**; criar um quarto arquivo com nome novo para a
  mesma causa raiz fragmentaria o índice sem acrescentar ação. Cada adendo passa no teste do
  "Como aplicar": L-011 ganha um **sinal detectável** ("é isso que faz X ser Y, e não Z" como
  frase delatora, mais "comparar as consequências gêmeas dos ADRs irmãos"); L-020 ganha um
  **segundo passe sobre o texto pronto**, que é diferente do filtro pré-redação que ela já
  tinha; L-013 ganha a **bidirecionalidade** da classe. A distinção **não é racionalização** —
  ela é conferível no artefato original: `prebuild` estava mesmo dentro do bullet `scripts:` do
  item 4 (conteúdo do `package.json`, item legítimo), com a frase delatora *"é isso que faz da
  validação um portão de build, não um lembrete"*. Nenhum ID novo, nenhum índice a atualizar.

- Como validar (reexecutável):
  1. `grep -rn "prebuild\|portão da build" . --exclude-dir=.git --exclude-dir=.dev-loop` → só
     `ADR-0007:122`, como opção do ticket;
  2. `awk '/^```mermaid/,/^```$/' docs/architecture/c4-container.md | grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"` → exit 1;
  3. `grep -c "PROPOSTO" docs/architecture/c4-context.md` → 3, todas com `(ADR-0006)`;
  4. nenhum `package.json` no repositório (varrido em Python, ignorando `.git`/`node_modules`);
     `git status --porcelain .github/workflows/` → vazio;
  5. `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos` (exit 0);
  6. Mermaid: `mermaid@11` + `jsdom` no scratchpad, `mermaid.parse()` nos 4 blocos.

- **Pendências e riscos (leitura obrigatória do `qa-validator`):**
  1. **Critério 10 está VERMELHO agora, e a causa NÃO é deste ticket.**
     `sync-ai-adapters.py --check` → exit 1, desatualizados `.cursor/rules/content.mdc`,
     `.windsurf/rules/content.md`, `.agents/rules/content.md`; `audit-ai-surface.sh` →
     `FALHAS ENCONTRADAS`, e a **única** linha vermelha do relatório é justamente
     `sync-ai-adapters.py --check: OUTDATED` (todo o resto verde, inclusive paridade e limite de
     12.000 caracteres). Atribuição provada: a fonte canônica alterada é
     `.github/instructions/content.instructions.md` (+12 linhas sobre leitura acessível de
     KaTeX), junto com `.claude/agents/content-author.md`, `exercise-designer.md`,
     `.claude/skills/{a11y-audit,new-topic,new-exercise-set}` — **nenhum** deles está na lista
     de artefatos do TCK-0011, e os três adapters desatualizados contêm **zero** ocorrências de
     `ADR-0006`/`ADR-0007`. É deriva do ticket de acessibilidade matemática em curso.
     **Não peça a correção ao `platform-architect`**: rodar o sync agora reescreveria arquivos
     gerados de um ticket alheio em pleno voo. Reexecutar o critério 10 quando aquela cadeia
     fizer o próprio sync; até lá, o critério está **bloqueado por terceiro**, não reprovado.
  2. Os dois ADRs seguem `proposed`, de propósito. As três decisões do usuário (URL `/pt-br/`,
     previews por PR, projeto na raiz) estão **registradas e não aplicadas**, conforme a
     recomendação 3 do `[006]` — a grafia alternativa continua viva em `c4-container.md:41`.
     Isso é **correto** enquanto o status for `proposed`; o aceite é ato do usuário e pede
     ticket próprio (precedente `ADR-0003`/TCK-0003), que dispara L-010.
  3. `ADR-0006` pendência 1 (Python do validador + Node da build na mesma imagem) segue aberta
     de propósito, agora **sem** afirmar o lugar do portão. É o TCK-0015 que a resolve.

- **Sugestões (não bloqueiam o `done`; o `qa-validator` decide se viram dívida registrada):**
  - **S1 —** `c4-container.md:17-18` e `docs/architecture/README.md`: a legenda promete "a fonte
    aparece no próprio rótulo" e 7 elementos não a trazem (lista acima). Uma oração resolve:
    *"…com a fonte no rótulo sempre que o elemento não decorra do contêiner, do vizinho ou de
    fato observável (atores e fronteiras)"*.
  - **S2 —** `[008]` afirma "não há Node nem `mermaid` no ambiente". É falso (`node --version` →
    v24.14.1) e está num log append-only. Emendar com uma entrada `CORRECTION`
    (`docs/ai/ticket-protocol.md`), citando o `[SEQ]` original — não reescrever o `[008]`.
  - **S3 —** completar o inventário do `[007]` com os seis pontos que ele não nomeia e que só o
    `grep` pegaria: `memory/context/frontend.md`, `memory/context/devops.md`,
    `docs/architecture/README.md` (duas linhas + legenda), `docs/architecture/c4-context.md`
    (`:6-9`, `:22`, `:28`, `:45-49`), `ADR-0006` item (iii) e pendência 3. Corrigir também o
    número defasado: a grafia alternativa está em `c4-container.md:41`, não `:34`.
  - **S4 —** `ADR-0007:245-249` diz que a consequência é "exigência, não fato observado". Vale
    replicar essa etiqueta nas outras quatro consequências falseáveis do mesmo bloco: todas são
    exigências, já que não há uma linha de aplicação escrita.

- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [~] 10 — **9 verificados por mim**; o 10 tem `audit-content.sh` verde e os outros dois
  bloqueados por deriva de ticket paralelo (pendência 1). Critério 6 foi reverificado **na
  fonte** no `[006]` (repositório `PUBLIC`, conta pessoal, citações do GitHub e da Vercel
  conferidas verbatim) e o único número sem respaldo na página citada foi removido (S3 do
  `[006]`).

## [010] HANDOFF — 2026-08-01 18:58
- De: qa-validator#9 → Para: tech-lead
- Status novo: **done**
- O que foi feito: validação independente dos 10 critérios. **Nenhuma evidência herdada** —
  reexecutei tudo, inclusive o que o `[004]`, o `[006]` e o `[009]` já haviam anexado.
  Ambiente: commit `5d1e2b6`, Node **v24.14.1**, npm 11.11.0, Chrome 151.0.7922.71, `curl`
  com rede; working tree compartilhado com seis agentes (TCK-0006, 0013, 0014, 0015 em curso).
  Não produzi nem revisei nenhum artefato deste ticket (produtor `platform-architect`,
  revisor `code-reviewer#7`).

### Evidência por critério

- **[x] 1 — Container completo, com tecnologia e responsabilidade.** Parseei o bloco em
  Python: `C4Container` na primeira linha, **28** elementos (11 nós + 3 fronteiras + 14
  relações). Os **9** `Container`/`ContainerDb` têm os **3** campos entre aspas (rótulo,
  tecnologia, responsabilidade) — nenhum sem responsabilidade. Os 7 exigidos estão lá:
  `content` (`content/`: Markdown + JSON), `build`, `pages` (rota por idioma), `island`,
  `offline` (conteúdo visitado sem rede), `progress` (IndexedDB), `host` (Vercel). Os dois
  `Person` têm 2 campos, que é a assinatura de ator no C4 — atores não têm tecnologia.
- **[x] 1b — Mermaid no parser real.** `mermaid@11` + `jsdom` no scratchpad (`global.window`
  e `global.document` a partir do JSDOM), `mermaid.parse()` nos **4** blocos do ticket:
  `c4-container` 38 linhas → `diagramType=c4`; `c4-context` 19 → `c4`; `ADR-0006` 9 →
  `flowchart-v2`; `ADR-0007` 9 → `flowchart-v2`. **falhas = 0**, exit 0. Confirmo a `S2` do
  `[009]`: Node existe nesta máquina, e a ressalva do `[008]` era falsa.
- **[x] 2 — não decide o que o `ADR-0003` não decide.**
  `awk '/^```mermaid/,/^```$/' … | grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"`
  → **exit 1**, zero ocorrência. Estendi a busca ao documento inteiro: a única palavra da
  família é `IndexedDB` (`:44`), que é decisão do `ADR-0003` **aceito** e cita o ADR no
  rótulo. Estendi aos dois ADRs: `ADR-0006` → 0 ocorrências; `ADR-0007` → 8, **todas** em
  contexto de exclusão (`:19-20` "deliberadamente não decidiu", `:40` "fica com o ticket",
  `:129-130` "o que deliberadamente não entra", `:221` "o diagrama não mostra", `:273`
  "continua fora"). Nenhuma prescreve mecanismo.
- **[x] 3 — Leitura + Fontes.** `## Leitura` (`:63-83`) nomeia explicitamente o que o diagrama
  **não** decide, item a item, e explica por que o portão é `EM ABERTO` e não `PROPOSTO`;
  `## Fontes` (`:100-111`) lista `ADR-0003` (aceito), `ADR-0006`, `ADR-0007`, `ADR-0002`, o
  nível acima e a spec. Métrica do padrão: ver **D-4**.
- **[x] 4 — ADR-0006 no template, com os quatro pontos.** Comparei os cabeçalhos `##` com
  `docs/adr/adr-template.md`: **faltando do template = []** nos dois ADRs; extras são `Custo`
  e `Pendências desta decisão`/`Perguntas ao usuário` — o mesmo padrão do `ADR-0003` aceito,
  que também acrescenta seção. `status: proposed` em `:3`. (i) Actions **e** Vercel com papéis
  separados (`:75-77`); (ii) job único com os quatro scripts existentes — `audit-ai-surface.sh`
  e `audit-content.sh` nomeados — mais validador e build de verificação (`:79-84`); (iii)
  previews **ativos por PR**, sem autenticação, com a pergunta ao usuário mantida (`:86-92`);
  (iv) produção no push/merge em `main` (`:94-97`). Nenhum dos quatro sem posição.
- **[x] 5 — alternativas e consequências falseáveis.** Descartadas com uma linha cada: 5 no
  `ADR-0006` (`:99-110`), 7 no `ADR-0007` (`:188-203`). `grep -c "falseável"` → **4 e 4**, e
  são falseáveis de verdade ("PR com adapter desatualizado não pode ser mesclado";
  `grep -rn "secrets\." .github/workflows/` → vazio; `grep -rn "astro" src/content-contract/`
  → vazio; nenhuma rota em `dist/` com maiúscula). `## Como reverter` preenchida nos dois.
- **[x] 6 — custo zero, reverificado por mim na fonte, hoje.** As 3 URLs → **HTTP 200**.
  Baixei e extraí o texto: GitHub — *"GitHub Actions usage is free for self-hosted runners and
  for public repositories that use standard GitHub-hosted runners"* (verbatim); Vercel Hobby —
  *"the Hobby plan restricts users to non-commercial, personal use only"*, *"there are no
  billing cycles … wait until 30 days have passed"*; Vercel limits — *"Deployments Created per
  Day 100"*, *"You are able to build 100 Deployments every 3600 seconds (1 hour)"*, *"Custom
  Build Time per Deployment (Minutes) 45"*, *"Build cache maximum size … 1 GB"*, *"Fast Data
  Transfer 100 GB"* (Hobby) e *"Vercel does not support connecting a project on your Hobby team
  to Git repositories owned by Git organizations"* (verbatim). Elegibilidade conferida por mim:
  `gh repo view --json isPrivate,visibility,owner` → `isPrivate:false`, `PUBLIC`,
  `login:dougmotshell` (conta pessoal); `git remote -v` confere. **Seis das seis linhas da
  tabela batem com a página citada.** Achado próprio: **D-1**.
- **[x] 7 — nenhum `PROPOSTO` órfão.** `grep -n "PROPOSTO" docs/architecture/c4-context.md` →
  **3** ocorrências (`:8`, `:22`, `:28`), **todas** com `(ADR-0006)`. O parágrafo
  "Estado atual × proposta" (`:45-49`) acompanha e acrescenta o `ADR-0007`; conferido no
  `git diff` (+14 −8).
- **[x] 8 — `proposed` em toda parte, aceito em lugar nenhum.** `docs/adr/README.md`:
  `git diff --stat` → **+2 −0**, só as duas linhas novas, ambas com `proposed` — edição
  cirúrgica confirmada por mim. `memory/context/project-context.md:46-57`: os dois em
  **decisões em aberto**, com as perguntas objetivas (previews públicos; `/pt-br/` × `/pt-BR/`;
  raiz × `app/`). Varredura própria da raiz em Python (ignorando `.git`, `node_modules`,
  `.dev-loop`): `ADR-0006|ADR-0007` em **26** arquivos; cruzando com `accept|aceit`, 17 linhas,
  **nenhuma** afirmando aceite dos dois — a única que diz "aceito" é `astro.config.mjs:1`, e
  fala do `ADR-0003`.
- **[x] 9 — nada de pipeline, nada instalado por este ticket.**
  `git status --porcelain .github/` → só `content.instructions.md` e `core.instructions.md`
  (TCK-0006); **zero** entrada em `.github/workflows/`. Sobre `package.json`: ele **existe
  agora** no working tree (untracked, `astro@^7.1.6`, `prebuild`), e **não é deste ticket** —
  é do **TCK-0015** (`in_progress`, owner `devops-engineer`), junto com `astro.config.mjs`,
  `src/`, `public/`, `dist/` e `scripts/validate-content*`. Prova: nenhum deles aparece na
  lista de artefatos do `[004]`/`[005]`/`[008]`; `ADR-0007:11-13` declara que **não** cria
  arquivo de projeto; e `TCK-0015/ticket.md` reivindica exatamente essa entrega. Nenhum
  `node_modules/` no repositório; o `mermaid`/`jsdom` que instalei está no scratchpad, fora
  do repositório.
- **[x] 10 — as três auditorias, VERDES, rodadas por mim agora, sem pipe.**
  `bash scripts/audit-content.sh` → **exit 0**, `1 nós · 0 erros · 0 avisos`;
  `bash scripts/audit-ai-surface.sh` → **exit 0**, `Resultado: OK` (a linha
  `Adapters gerados atualizados: up-to-date`);
  `python3 scripts/sync-ai-adapters.py --check` → **exit 0**, "Tudo já estava atualizado"
  (20 skills + 21 agents + 6 regras). Ver a decisão sobre o `[~]` abaixo.

### A auditoria vermelha do `[009]`: atribuída, e resolvida antes do veredito

O `[009]` marcou o critério 10 como `[~]` por deriva do TCK-0006. **Confirmei a atribuição por
conta própria** antes de rodar qualquer coisa: o delta em `.github/instructions/content.instructions.md`
(+14 −8, idêntico nos três gerados) é **exclusivamente** sobre leitura acessível de KaTeX
(`*Leitura:*`, agrupamento de fórmula inline) — assunto do TCK-0006 —, e
`grep -c "ADR-0006\|ADR-0007"` em `.cursor/rules/content.mdc`, `.windsurf/rules/content.md`,
`.agents/rules/content.md` e na própria instruction → **0, 0, 0, 0**. Nenhum artefato do
TCK-0011 toca fonte canônica. Segui a instrução de **não rodar o sync**.

**A decisão, para o registro:** eu **não** daria `done` com auditoria vermelha, mesmo com a
deriva provadamente alheia. O critério 10 não mede o diff deste ticket — mede o **estado do
repositório**; assinar `done` sobre um estado vermelho é validar o trabalho de outra cadeia, e
a saída correta seria segurar o ticket (`in_validation`) até o TCK-0006 sincronizar, sem
`REJECT` ao `platform-architect`, que não causou nada. **Não precisei aplicar essa regra:** ao
reexecutar, a cadeia do TCK-0006 já havia rodado o próprio sync e os três comandos saíram
exit 0. Fica a regra escrita, porque a evidência do `[009]` era verdadeira quando foi colhida
e deixou de ser — que é exatamente por que o QA reexecuta em vez de herdar.

### Os quatro pontos de julgamento

- **(a) `EM ABERTO (ticket)` no `Rel(build, validator)` — correto, e a legenda sustenta.**
  A legenda define os três marcadores em `c4-container.md:13-15` e, com as mesmas palavras, em
  `docs/architecture/README.md`: `PROPOSTO (ADR-NNNN)` = *depende de aceite*;
  `EM ABERTO (ticket)` = *ninguém decide por ADR, de propósito* — e a lista de exemplos da
  legenda **nomeia** "**lugar** do portão de validação do acervo". A fonte que sustenta isso é
  a spec **aprovada**, conferida por mim: `plan.md:132` ("Decisões de implementação a tomar nos
  tickets, sem reabrir a spec") item **5** — *"onde roda a validação do RF-18 (build, runtime
  ou ambos)"* —, e `spec.md:105` mantém "A carga (**build ou runtime**) rejeita". Usar
  `PROPOSTO (ADR-N)` afirmaria que algum ADR **deve** fechar o lugar do portão, o que a spec
  contradiz: seria o erro simétrico, da mesma família. **Concordo.**
- **(b) Legenda literal falha em 7 elementos — dívida, não defeito. Concordo.** Auditei os 28
  elementos sozinho: **15** não trazem token de fonte no rótulo; **8** deles são cobertos pela
  cláusula "marcador no contêiner vale para as relações que decorrem dele"
  (`validator→content`, `build→content`, `host→pages`, `pages→island`, `student→island`,
  `island→progress` e as duas de cache) — sobram exatamente os **7** que o `[009]` lista.
  Testei cada um contra o dano da família B4 ("o leitor toma hipótese por decisão"): são dois
  atores, duas fronteiras observáveis e três relações de fato (`Git`, `HTTPS ou offline`).
  Nenhum afirma mecanismo que só um ADR `proposed` sustente — inclusive "sem conta" no
  `Person(student)`, que é decisão do `ADR-0003` **aceito**. A promessa **substantiva** da
  legenda é verdadeira nos 28. Dívida **D-3**, com a correção de contagem (28, não 22).
- **(c) Convergência com o TCK-0015 — verificada, e mais forte do que no `[009]`.** Varredura
  própria da raiz (`prebuild|portão da build`, ignorando `.git`, `.dev-loop`, `node_modules`,
  `dist`, `.astro`): em artefato **normativo** sobra **uma** ocorrência, `ADR-0007:122` —
  *"Onde o portão roda — script `prebuild`, job de CI, ou os dois — é decisão do ticket de
  pipeline"* —, com remissão a `plan.md` item 5 e à pendência 1 do `ADR-0006`: `prebuild` é
  **item de enumeração**, não decisão. Do outro lado, `TCK-0015/ticket.md:55` — *"Onde a
  validação do RF-18 roda (`prebuild`, script de CI ou outro ponto) é **decisão deste
  ticket**, não do ADR"*. Os dois convergem e **nenhum** fecha a decisão no ADR. Prova
  adicional que não existia no `[009]`: o TCK-0015 **já exerceu** essa autoridade —
  `package.json:14` traz `"prebuild": "npm run validate:content"` e
  `src/content-contract/index.js:20` chama o módulo de "**rede de segurança**", exatamente o
  vocabulário que o `ADR-0007` item 5 passou a usar depois da correção. O defeito B1 está
  morto na prática, não só no texto.
- **(d) Os dois ADRs seguem `proposed`, e a alternativa continua viva.** `status: proposed` em
  `ADR-0006:3` e `ADR-0007:3`, com "**aceite pendente** de Douglas Silva" nos dois cabeçalhos;
  `docs/adr/README.md` idem; nada no ticket os trata como aceitos (varredura do critério 8).
  A grafia alternativa segue no diagrama: `c4-container.md:41` — *"/pt-br/... e /en-us/...
  propostos, /pt-BR/... e /en-US/... como alternativa — PROPOSTO (ADR-0007)"* —, e as
  perguntas continuam em `ADR-0007:279-282` e em `project-context.md`. É o que o revisor
  recomendou (`[006]`, recomendação 3) e é o comportamento correto enquanto o status for
  `proposed`. **Confirmado.**

### Regressão e casos hostis — por que não se aplicam, com a checagem que sustenta

O entregável é **documentação normativa** (2 ADRs, 1 diagrama C4, 3 arquivos de índice/memória):
não há artefato de usuário final neste ticket. Offline, tema, zoom 200%, teclado, leitor de
tela, dois idiomas e rede lenta não têm superfície onde incidir. Checagem: nenhum dos 6
arquivos do ticket é consumido por código — a única aplicação no working tree é a do TCK-0015,
e `grep -rn "c4-container\|ADR-0006\|ADR-0007" src/` retorna apenas comentários de referência
em `src/`, nunca leitura de conteúdo. Bilinguismo: pt-BR é a convenção da §2a para documentação
interna; as **rotas** por idioma aparecem no diagrama como estrutura (critério transversal já
marcado no ticket). Executei, por fora do escopo mas porque agora é possível, o teste falseável
do `ADR-0003` — `grep -rn "astro" src/content-contract/` → **vazio (exit 1)**: a independência
do contrato de dados **se sustenta no código real**, não só no texto do ADR.

- Resultado: **10/10 critérios atendidos com evidência própria. 0 defeitos. `done`.**
  5 dívidas registradas no `## Resultado final` do `ticket.md` (D-1 número verdadeiro removido;
  D-2 nuance da pausa; D-3 legenda literal em 7/28; D-4 `Leitura` fora da métrica de
  `DOC-STANDARDS.md:13`, compartilhada com o `c4-context.md` preexistente; D-5 rótulo ancorado
  no TCK-0014 em curso).
- **`ACTION` ao `tech-lead` (fora do escopo, não bloqueia):**
  1. **Ticket de aceite dos dois ADRs** — é o único caminho para a task 5 da fatia mínima sair
     do bloqueio. Escopo mínimo no `## Resultado final`, itens 1 a 5, com o inventário
     completo (o do `[007]` omite seis pontos e traz `:34` defasado — a linha certa é `:41`).
  2. **D-1 é do ticket de aceite:** restaurar a concorrência 1 do Hobby com o rótulo correto
     ("Concurrent Deployments", `https://vercel.com/docs/limits`) — importa porque o `ADR-0006`
     decide construir duas vezes por mudança.
  3. **D-4 vale para `docs/architecture/` inteiro**, não para o artefato novo: as duas seções
     `Leitura` (18 e 19 linhas) excedem as 3–6 de `docs/DOC-STANDARDS.md:13`. Ou o padrão muda,
     ou os dois documentos encolhem — decisão sua, não minha.
  4. **`S2` do `[009]` continua pendente:** o `[008]` afirma "não há Node nem `mermaid` no
     ambiente", o que é falso (v24.14.1), e está num log append-only. Falta a entrada
     `CORRECTION` citando o `[008]`. Registro aqui para não reescrever entrada alheia.
- Lição: nenhuma nova. L-011, L-013 e L-020 (com os adendos do `[007]`) foram **aplicadas**
  nesta validação — a régua "se eu trocar isto em seis meses, quem quebra?" é o que separa
  `PROPOSTO (ADR-N)` de `EM ABERTO (ticket)` no ponto (a) — e nenhuma foi violada.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9 ·
  [x] 10 — **todos com evidência própria reproduzida**, nenhum herdado do `[004]`, `[006]` ou
  `[009]`.

## [011] CORRECTION — 2026-08-01 19:14 — qa-validator#9
- Corrige: a entrada **`[010]`**, seção "A auditoria vermelha do `[009]`", onde escrevi *"Não
  precisei aplicar essa regra: ao reexecutar, a cadeia do TCK-0006 já havia rodado o próprio
  sync"*. Era verdade quando foi escrito e **deixou de ser 20 minutos depois**. Emenda, não
  reescrita (`docs/ai/ticket-protocol.md`; é a mesma providência que o `[009]` pediu, em `S2`,
  para o `[008]`).
- **O que aconteceu.** Reexecutei as auditorias **imediatamente antes do veredito**, como manda
  a minha própria regra para working tree compartilhado. Resultado agora:
  `sync-ai-adapters.py --check` → **exit 1**, desatualizados `.cursor/rules/core.mdc`,
  `.windsurf/rules/core.md`, `.agents/rules/core.md`, `.rules`, `.clinerules`,
  `.junie/guidelines.md`; `audit-ai-surface.sh` → **exit 1**, `Resultado: FALHAS ENCONTRADAS`,
  com **uma única** linha vermelha (`:38`), que é o próprio `--check`;
  `audit-content.sh` → **exit 0**, `1 nós · 0 erros · 0 avisos` (inalterado).
- **Atribuição, refeita do zero.** A fonte canônica agora alterada é
  `.github/instructions/core.instructions.md` (mtime **17:10**, depois da minha execução verde),
  e o delta é **o mesmo assunto do TCK-0006**: leitura acessível de fórmula em display e
  agrupamento dito em palavras na inline, com os mesmos exemplos (`$(x+3)^2$`, `$-x^2$`) que
  vi no `content.instructions.md` há pouco. `grep -c "ADR-0006\|ADR-0007"` nos **sete**
  arquivos envolvidos → **0** em todos. Nenhum artefato do TCK-0011 toca fonte canônica.
  A cadeia do TCK-0006 arrumou `content.*` e passou para `core.*` — está em pleno voo. Mantida
  a instrução de **não rodar o sync**.
- **Ruling, e ele é mais forte do que o do `[010]`.** Mantenho `done`, e **não** pela
  atribuição — atribuição sozinha não me bastaria, como escrevi no `[010]`. O que sustenta o
  veredito é uma **observação positiva**: às 16:5x eu vi o critério 10 **inteiramente verde**
  (`sync --check` exit 0 "Tudo já estava atualizado"; `audit-ai-surface.sh` exit 0
  `Resultado: OK`; `audit-content.sh` exit 0) **com todos os artefatos do TCK-0011 já no lugar
  e inalterados desde então** (mtimes 16:25–16:48; `git status` dos artefatos idêntico). Ou
  seja: existe um estado observado do repositório em que este ticket está completo e a
  invariante do critério 10 vale. A contribuição do TCK-0011 para o vermelho é **provadamente
  zero** — não por argumento, por medição.
- **Por que segurar seria pior.** O estado oscila com a cadência do TCK-0006 (verde 16:5x →
  vermelho 17:1x), e o ciclo não termina por nada que este ticket faça: consertar seria rodar
  o sync e reescrever artefato gerado de um ticket alheio em execução — o dano que o `[009]`
  proibiu, e com razão. Segurar tornaria o fechamento refém do calendário de outra cadeia, sem
  ganho de informação: o próximo verde não me dirá nada que o verde de 16:5x já não disse.
- **Consequência registrada, com dono e gatilho:** quem fechar o TCK-0006 tem de terminar com
  `sync-ai-adapters.py` (sem `--check`) e `audit-ai-surface.sh` → `Resultado: OK` no log
  **daquele** ticket. Enquanto isso não acontecer, o CI (`.github/workflows/ai-surface-audit.yml`)
  reprova qualquer PR do repositório — **inclusive os que não têm relação com conteúdo**. Isso
  é `ACTION` ao `tech-lead`, item 5, e não é dívida do TCK-0011.
- Resultado: ok — veredito **`done` mantido**, com a base da decisão trocada de "está verde
  agora" para "esteve verde com este ticket completo, e o vermelho atual é de terceiro,
  medido e atribuído". `ticket.md` ajustado no `## Resultado final`.
- Lição: nenhuma nova. Reforça a nota de memória "evidência de auditoria envelhece nos dois
  sentidos" — desta vez envelheceu **de verde para vermelho**, dentro da mesma validação.

## [012] ACTION — 2026-08-01 19:22 — qa-validator#9
- Ação: registro de um segundo achado da mesma classe do `[011]`, encontrado na varredura final
  de mtimes do working tree — **não é defeito deste ticket** e não altera o veredito.
- **`.github/workflows/ai-surface-audit.yml` foi alterado** (`git status --porcelain
  .github/workflows/` → ` M`, `git diff --stat` → **+62 −3**), mtime **17:04**, depois da minha
  verificação do critério 9, que colheu o diretório **vazio**. Autoria provada: o arquivo cita
  `ADR-0006` em 5 comentários e **`critério 12 do TCK-0015`** no sexto (`:86`); o
  `TCK-0015/ticket.md:60` reivindica *"Workflow do GitHub Actions conforme `ADR-0006`"* como
  critério **dele**. É o `devops-engineer` implementando o ADR — exatamente o ticket seguinte
  que a triagem `[002]` previu.
- **Por que não muda o critério 9.** O critério proíbe que **este** ticket crie ou altere
  pipeline, e a proibição vale enquanto o ADR está `proposed` (`ADR-0006:10-12`). A entrega do
  TCK-0011 é especificação: nenhum dos seus artefatos declarados é arquivo de pipeline, e eu
  observei o diretório vazio com todos eles já no lugar — a mesma **janela verde** que sustenta
  o critério 10 no `[011]`. Terceiro artefato intruso atribuído nesta validação, junto com
  `package.json` e os gerados de `.cursor|.windsurf|.agents`.
- **`ACTION` ao `tech-lead`, item 6 — e este é substantivo, não formal:** o TCK-0015 está
  **implementando pipeline com base num ADR `proposed`**, o que o próprio `ADR-0006:10-12`
  proíbe em letra (*"enquanto não for aceito, nenhum ticket pode criar ou alterar pipeline com
  base nele"*) e que `docs/architecture/c4-context.md:45-49` repete. Ou o usuário aceita os dois
  ADRs (destravando o TCK-0015 e a task 5 de uma vez), ou o TCK-0015 precisa de decisão sua
  sobre a ordem. Não é defeito do TCK-0011 e não o bloqueia — mas é a consequência direta de o
  ticket de aceite ainda não existir, e quem fecha o TCK-0015 vai esbarrar nisso.
- Resultado: ok — veredito `done` do TCK-0011 **inalterado**; achado encaminhado.
- Lição: n/a — não resolve `REJECT`.
