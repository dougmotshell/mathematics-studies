# Log — TCK-0016

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 17:30 — tech-lead
- Ação: ticket criado a partir de achado do `qa-validator#9` ao fechar o TCK-0011.
- Motivo: o TCK-0015 implementa pipeline e esqueleto sob ADRs `proposed`, e `ADR-0006:10-12`
  proíbe isso em letra. A execução está autorizada pelo usuário; o que falta é o registro.
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 17:30 — tech-lead
- Ação: triagem. Tipo `docs`, P1, tamanho P, owner `platform-architect` (ADRs são escopo
  exclusivo dele, AGENTS.md §10).
- Precedente seguido: o aceite do `ADR-0003` foi feito assim, em ticket próprio (TCK-0003).
- Restrições: não tocar em código nem no TCK-0015; não reabrir o mérito das decisões.
- Resultado: ok — `triaged`.

## [003] HANDOFF — 2026-08-01 17:30
- De: tech-lead → Para: platform-architect
- Status novo: in_progress
- O que foi feito: contradição de governança transformada em ticket com critérios.
- Artefatos: `tickets/TCK-0016-accept-cicd-and-skeleton-adrs/ticket.md`.
- Como validar: critérios 1–8 e as duas auditorias.
- Pendências e riscos: o TCK-0015 está em revisão e toca `package.json`, `src/`,
  `vercel.json` e `.github/workflows/` — colidir ali travaria os dois; o TCK-0006 está em
  correção e é o **único** autorizado a rodar `sync-ai-adapters.py` até fechar.
- Critérios de aceite: [ ] 1–8 restantes.

## [004] ACTION — 2026-08-01 18:10 — platform-architect
- Ação: aceite formal do `ADR-0006` e do `ADR-0007`, com propagação por varredura da **raiz**
  (L-010) e por **classe** de defeito (L-013).
- **Arquivos alterados (todos declarados, AGENTS.md §10 regra 2 — 17):**
  1. `docs/adr/ADR-0006-continuous-integration-and-publication.md`
  2. `docs/adr/ADR-0007-application-skeleton.md`
  3. `docs/adr/ADR-0003-platform-stack.md` (emenda editorial — ver defeito de classe abaixo)
  4. `docs/adr/README.md` (edição cirúrgica das 2 linhas + nota do aceite)
  5. `docs/architecture/c4-container.md`
  6. `docs/architecture/c4-context.md`
  7. `docs/architecture/README.md`
  8. `docs/specs/minimum-learning-slice/spec.md` (só a pergunta em aberto da URL — nenhum
     requisito tocado)
  9. `AGENTS.md` (§1 e §11)
  10. `README.md`
  11. `prompts/bootstrap-session.md`
  12. `.github/instructions/core.instructions.md` — **fonte canônica**
  13. `.github/instructions/app.instructions.md` — **fonte canônica**
  14. `.claude/agents/platform-architect.md` — **fonte canônica**
  15. `memory/context/frontend.md`
  16. `memory/context/devops.md`
  17. `memory/context/project-context.md`
  Nada tocado em `package.json`, `src/`, `vercel.json`, `.github/workflows/`, `content/`,
  `docs/design/`, `docs/content/`, `scripts/` ou outros tickets (`git status --porcelain`
  desses caminhos: sem alteração minha).
- **Critério 1 — status.** Os dois ADRs: `Status: accepted`, `Data: 2026-08-01`, decisor
  **Douglas Silva** (aceite registrado no TCK-0016). O aviso "aceite pendente" foi
  **substituído**, não apagado: o novo bloco diz o que o aceite destrava **e** o que continua
  aberto. `docs/adr/README.md:16-17` → `accepted`.
- **Critério 2 — as três decisões do usuário, na seção Decisão de quem as governa.**
  URL minúscula → `ADR-0007`, Decisão item 7 ("proposta confirmada por Douglas Silva em
  2026-08-01"); projeto na raiz → `ADR-0007`, item 2; previews por PR → `ADR-0006`, item (iii).
  A seção "Perguntas ao usuário (no aceite)" virou **"Respostas do usuário no aceite"**.
- **Critério 3 — consequências em três blocos**, nos dois ADRs: *o que passa a valer* · *o que
  fica proibido sem ADR novo* · *o que continua sendo decisão de ticket*. O terceiro bloco é o
  antídoto de L-011/L-020: sem ele, o aceite é lido como fechamento geral.
- **Critério 4 — grafia alternativa da URL, varrida por classe.** Fronteira aplicada: some de
  onde é apresentada como **escolha disponível**; permanece só onde é **registro histórico da
  própria decisão** (as listas de alternativas consideradas/descartadas do `ADR-0007`, que são
  exigência do formato de ADR). Removida de: `c4-container.md:41` (rótulo "…como alternativa"),
  `ADR-0007` "Perguntas ao usuário", `docs/specs/minimum-learning-slice/spec.md:277` (pergunta
  em aberto que a decisão respondeu) e — achado da varredura da classe, não citado no ticket —
  **`ADR-0003:86`**, cujo rótulo Mermaid exibia `/pt-BR/… · /en-US/…` num ADR **aceito que não
  decide a forma da URL**. Corrigido para "uma rota estática por idioma", com **nota de emenda
  editorial** no cabeçalho declarando que nenhuma decisão foi alterada. Acrescentado ao
  `ADR-0007` o parágrafo "Fechado no aceite", que torna a regra citável.
  Evidência: `grep -rn "pt-BR/\|en-US/"` em `docs/{adr,architecture,specs}`, `AGENTS.md`,
  `README.md`, `prompts/`, `.github/instructions/`, `.claude/`, `memory/context/` → 6 linhas,
  **todas** históricas (3 alternativas do `ADR-0007`, 2 da nota de emenda, e nenhuma como opção
  viva).
- **Critério 5 — marcadores por classe.** `grep` de `PROPOSTO (ADR-0006)` e
  `PROPOSTO (ADR-0007)` fora de `tickets/`, `memory/agents/` e `docs/design/` → **0
  ocorrências**. As 7 linhas remanescentes com a palavra `PROPOSTO` são: a **legenda** dos três
  marcadores (`docs/architecture/README.md:14`), quatro afirmações **negativas** ("sem marcador
  `PROPOSTO`") e o **Contexto histórico** do `ADR-0006:23`. `EM ABERTO (ticket)` **preservado**:
  4 ocorrências em `c4-container.md`, 2 em `docs/architecture/README.md`, 1 em cada ADR — em
  especial o `Rel(build, validator)` e o **lugar do portão de validação**, que o TCK-0015
  exerceu e que continua sendo decisão de ticket (registrado como pendência 1 **aberta** do
  `ADR-0006` e em `memory/context/{devops,project-context}.md`).
- **Critério 6 — varredura da raiz.** `grep -rn "ADR-0006\|ADR-0007" . --exclude-dir=.git -l`
  → 30 arquivos; mais varredura por classe de frase
  (`aceite pendente|espera aceite|antes do aceite|proposed`) e por conteúdo
  (`a aplicação não existe|esqueleto|vercel|pipeline`) em `AGENTS.md`, `README.md`, `prompts/`,
  `.github/instructions/`, `.claude/`, `docs/`, `memory/`. Resultado: nenhuma menção aos dois
  ADRs como pendentes fora de `tickets/**` e `memory/agents/**` (registros append-only e
  históricos) e de `docs/design/**` (fora do meu escopo — pendência abaixo).
  Verificação final: `grep -rniE "ADR-000[67].{0,80}(proposed|pendente|hipótese)"` em
  `docs/`, `AGENTS.md`, `README.md`, `prompts/`, `memory/context/`, `.github/`, `.claude/`
  → **vazio**.
- **Critério 7:** `docs/adr/README.md` (tabela + nota nova dizendo o que o aceite **não**
  fecha) e `memory/context/project-context.md` (os dois ADRs migrados de "Decisões em aberto"
  para "Decisões aceitas", com o que fica proibido; "5 ADRs aceitos" → "7 ADRs, todos
  `accepted`"; duas pendências reais mantidas em aberto; próximos passos corrigidos).
- **Critério 8 — auditorias.**
  - `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`, **exit 0**.
  - `bash scripts/audit-ai-surface.sh` → **exit 1**, com **uma única** verificação vermelha:
    `Adapters gerados atualizados (sync-ai-adapters.py --check): OUTDATED`. Todo o resto verde
    (21 agents, 20 skills, 6 regras, 5 workflows, paridade completa, limite de 12.000
    caracteres respeitado, acesso do Codex documentado). **Causa declarada, não herdada** — ver
    `[005]`.
- **Verificação extra (diagrama é normativo):** os 5 blocos Mermaid tocados
  (`c4-container`, `c4-context`, `ADR-0006`, `ADR-0007`, `ADR-0003`) reparseados com
  `mermaid.parse` → **5 blocos, 0 falhas**. Em Node puro o parser quebra com
  `purify.addHook is not a function`; foi preciso `jsdom` do cache do npx e `navigator`
  injetado por `Object.defineProperty` (getter-only no Node 24).
- Resultado: ok — critérios 1–7 atendidos; 8 atendido em `audit-content.sh` e **parcial** em
  `audit-ai-surface.sh`, com a causa isolada e atribuída.
- Lição: n/a — não resolve `REJECT`.

## [005] ACTION — 2026-08-01 18:15 — platform-architect
- Ação: declaração da **pendência de sync**, exigida pela restrição do ticket (o TCK-0006 é o
  único autorizado a rodar `scripts/sync-ai-adapters.py` até fechar).
- **Não rodei o sync.** Editei 3 fontes canônicas: `.github/instructions/core.instructions.md`,
  `.github/instructions/app.instructions.md` e `.claude/agents/platform-architect.md`.
- **O que precisa ser regenerado — 9 arquivos**, saída literal de
  `python3 scripts/sync-ai-adapters.py --check`:
  `.cursor/rules/app.mdc` · `.windsurf/rules/app.md` · `.agents/rules/app.md` ·
  `.cursor/rules/core.mdc` · `.windsurf/rules/core.md` · `.agents/rules/core.md` ·
  `.rules` · `.clinerules` · `.junie/guidelines.md`.
  Comando: `python3 scripts/sync-ai-adapters.py` (sem `--check`), **por quem tiver o direito**.
- **Atribuição provada, não alegada** (padrão da minha memória): a sobra é **inteiramente
  minha**. Prova em dois passos — (a) os gerados **já contêm** o texto do TCK-0006
  (`grep -c "agrupamento dito em palavras"` = 1 em `.cursor/rules/core.mdc`,
  `.windsurf/rules/core.md`, `.agents/rules/core.md`, `.rules`, `.clinerules`,
  `.junie/guidelines.md`), enquanto o `HEAD` da fonte **não** o contém (`git show
  HEAD:.github/instructions/core.instructions.md | grep -c` → 0): o TCK-0006 editou **e**
  sincronizou; (b) os mesmos gerados têm `grep -c "/pt-br/"` = **0**, e as duas fontes que
  editei têm 1 cada. Nenhuma regra `content` aparece na lista de desatualizados, o que confirma
  que não há resíduo do outro ticket.
- **Achado útil ao próximo aceite:** editar `.claude/agents/<nome>.md` **não** derruba o
  `--check` (o adapter gerado embute só o front matter: `grep -c "Stack em vigor"` = 0 em
  `.claude/commands/platform-architect.md` e no chatmode). Uma regra em
  `.github/instructions/` derruba nove arquivos.
- **Consequência para o CI:** enquanto o sync não rodar, o workflow de auditoria reprova. Não é
  deriva de terceiro nem falha de propagação — é a dívida declarada acima, com dono definido.
- Resultado: ok — pendência registrada com comando, arquivos e prova de atribuição.
- Lição: n/a.

## [006] ACTION — 2026-08-01 18:20 — platform-architect
- Ação: pendências **nominais** em área de outro agente, encontradas pela varredura da raiz e
  **não** corrigidas por mim (escopo exclusivo, AGENTS.md §10).
- 1. `ui-ux-designer` — `docs/design/minimum-learning-slice/screen-states.md:689` ("o registro
  formal é o `ADR-0007`, hoje **`proposed`** (aceite pendente)") e `:833` ("registro em
  `ADR-0007`, `proposed`"). As duas afirmam status agora falso; a **decisão** que o documento
  descreve continua correta e não muda. Fora do meu escopo por restrição explícita do ticket.
- 2. `product-analyst` / `tech-lead` — `docs/specs/minimum-learning-slice/plan.md:103` diz "Não
  existe código hoje", superado pelo TCK-0015. Não é consequência do aceite e por isso não foi
  tocado.
- 3. `tech-lead` — segue valendo a pendência que abri no TCK-0003: `memory/agents/{tech-lead,
  product-analyst,docs-writer}.md`, `.claude/agents/tech-lead.md`,
  `.claude/skills/ticket/SKILL.md` e `.claude/workflows/feature-plan-review.js` ainda tratam
  `ADR-0003` como `proposed`.
- Resultado: ok — registrado nominalmente, não implícito.
- Lição: n/a.

## [007] ACTION — 2026-08-01 18:22 — platform-architect
- Ação: memória e lição (AGENTS.md §5–7).
- `memory/agents/platform-architect.md`: quatro notas novas — (a) aceite não deixa `PROPOSTO`
  em Context/Container e **não** apaga `EM ABERTO (ticket)`; (b) aceitar ≠ implementar ≠ atestar
  a implementação; (c) fronteira para matar a grafia alternativa (opção viva sai, registro
  histórico fica), com o achado do `ADR-0003`; (d) sync retido por outro ticket vira dívida
  provada no log, mais o parser de Mermaid deste ambiente. Linha nova em "Últimas execuções".
- `memory/context/{project-context,frontend,devops}.md` atualizados no `[004]`.
- **Lição nova: `L-025` — "autorização para executar não é aceite da decisão"**
  (`memory/lessons/authorization-to-execute-is-not-acceptance-of-the-decision.md`), tipo
  `correção`, indexada em `memory/LESSONS.md` (seção Correção) e em `memory/MEMORY.md`. É a
  generalização do achado do `qa-validator#9` que originou este ticket, e a única lição da
  entrega: as demais aplicações (L-010, L-011, L-013, L-020) já tinham registro e viraram nota
  de memória, não lição duplicada.
- Resultado: ok.
- Lição: L-025.

## [008] HANDOFF — 2026-08-01 18:25
- De: platform-architect → Para: code-reviewer
- Status novo: in_review
- O que foi feito: `ADR-0006` e `ADR-0007` aceitos (status, decisor, as 3 decisões do usuário,
  consequências em 3 blocos); marcadores `PROPOSTO` eliminados por classe nos dois C4 com
  `EM ABERTO (ticket)` preservado; grafia `/pt-BR/` removida como opção viva em 4 documentos,
  incluindo um achado no `ADR-0003`; propagação L-010 por varredura da raiz em 17 arquivos.
- Artefatos: os 17 arquivos listados em `[004]`.
- Como validar: critérios 1–8 do `ticket.md`; as evidências de cada um estão em `[004]`, a
  dívida de sync em `[005]` e as pendências de outras áreas em `[006]`.
- **Pontos que pedem julgamento seu, declarados de propósito:**
  1. **Editei um ADR aceito** (`ADR-0003`): rótulo Mermaid com `/pt-BR/…`. Justificativa: o
     `ADR-0003` **não** decide a forma da URL, e a ilustração passou a contradizer o `ADR-0007`.
     Feito como emenda **editorial** declarada no cabeçalho, sem tocar em decisão. Se você
     julgar que ADR aceito é imutável mesmo para ilustração, o caminho alternativo é uma nota
     sem alterar o rótulo — diga qual prefere.
  2. **Mantive `/pt-BR/` nas listas de alternativas do `ADR-0007`** (linhas 80, 183, 206). Leio
     o critério 4 como "sai de onde é opção viva", não "some do registro da decisão" — remover
     as alternativas descartadas destruiria o formato de ADR exigido por `docs/DOC-STANDARDS.md`.
  3. **Editei `docs/specs/.../spec.md:277`** (pergunta em aberto que a decisão respondeu),
     apesar de spec ser artefato do `product-analyst`. Restringi-me à pergunta; nenhum requisito
     foi tocado.
- Pendências e riscos: (a) `audit-ai-surface.sh` **exit 1** por sync não rodado — dívida
  declarada em `[005]`, com dono (TCK-0006) e comando; (b) o TCK-0015 permanece em revisão — o
  aceite **autoriza** aquele trabalho e não atesta que ele esteja correto, o que está escrito
  nos dois ADRs; (c) proteção de branch em `main` continua pendente de ato do usuário, sem ela
  o portão de mérito é informativo.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 ·
  [~] 8 (`audit-content.sh` exit 0; `audit-ai-surface.sh` exit 1 **apenas** por `OUTDATED`,
  causa atribuída e fora do meu direito de correção).

## [010] ACTION — 2026-08-01 18:45 — platform-architect
- Ação: correção do **defeito 1** do `[009] REJECT` — sync executado.
- **Impedimento verificado antes de agir, não presumido:** `tickets/TCK-0006-formula-reading-
  conventions/ticket.md` → `status: done`, e `git log --oneline -3` → `dea3303 TCK-0006: norma
  de leitura de fórmula…` no `HEAD`. Sem impedimento externo, o `[~]` do critério 8 deixaria de
  ser dívida atribuída e viraria dispensa de critério — o revisor tem razão.
- **Comando e saída literal:** `python3 scripts/sync-ai-adapters.py` →
  `20 skills + 21 agents + 6 regras → adapters sincronizados (Claude, Copilot, Gemini, Cursor,
  Antigravity, Windsurf).` / `9 arquivo(s) escrito(s)/atualizado(s).`
- **Os 9 gerados, agora artefatos deste ticket** (critérios 6 e 8): `.cursor/rules/app.mdc` ·
  `.windsurf/rules/app.md` · `.agents/rules/app.md` · `.cursor/rules/core.mdc` ·
  `.windsurf/rules/core.md` · `.agents/rules/core.md` · `.rules` · `.clinerules` ·
  `.junie/guidelines.md`.
- **Auditorias reexecutadas, saída literal:**
  - `bash scripts/audit-ai-surface.sh` → `Adapters gerados atualizados (sync-ai-adapters.py
    --check): up-to-date` · `Limite de 12.000 caracteres nas regras: todas dentro do limite` ·
    `Acesso do Codex documentado: documented` · **`Resultado: OK`**, **exit 0**.
  - `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos`, **exit 0**.
- **Estado prévio do working tree que o sync carregou junto, declarado como o revisor pediu:**
  o TCK-0006 fechou e commitou em `dea3303`, mas **a edição dele em
  `.github/instructions/core.instructions.md` ficou fora do commit** — prova:
  `git show HEAD:.github/instructions/core.instructions.md | grep -c "agrupamento dito em
  palavras"` → **0**, enquanto o arquivo no working tree a contém. Consequência inevitável: os
  6 gerados que derivam de `core` (as 3 regras `core` mais `.rules`, `.clinerules`,
  `.junie/guidelines.md`) passaram a conter **tanto** o meu texto **quanto** o item 6 do
  TCK-0006. Medido depois do sync: `/pt-br/` presente nos 9; `agrupamento dito em palavras`
  presente nos 6 de `core` e ausente nos 3 de `app`. **Não é resíduo meu e não é arraste: é
  estado prévio não commitado por outro ticket**, e quem commitar precisa saber que leva os
  dois.
- **O sync não alcançou o TCK-0015** (que está em revisão): `find -mmin -3` lista apenas os 9
  adapters (mais os meus arquivos de ticket e `memory/agents/code-reviewer.md`, do revisor);
  `.github/workflows/ai-surface-audit.yml` (17:29), `package.json` (17:28), `vercel.json`
  (17:00) e `astro.config.mjs` (16:57) mantêm mtime anterior ao sync (17:43). `diff` do
  `git status --porcelain` antes × depois: **três** entradas novas, todas `rules/app`.
- **Critério 8 passa de `[~]` a `[x]`**: as duas auditorias saem com exit 0.
- Resultado: ok — defeito 1 corrigido.
- Lição: L-025 (a mesma família: dívida declarada só é legítima enquanto o impedimento existe;
  extinto o impedimento, declarar vira dispensar).

## [011] CORRECTION — 2026-08-01 18:47 — platform-architect
- Corrige: `[004]`, critério 4, contagem da varredura da grafia alternativa.
- O que estava errado: registrei *"→ 6 linhas, todas históricas (3 alternativas do `ADR-0007`,
  2 da nota de emenda, e nenhuma como opção viva)"*. A soma da própria decomposição dá **5**, e
  o número 6 era a contagem colhida **antes** de eu editar
  `docs/specs/minimum-learning-slice/spec.md:277`, que era a sexta linha e deixou de casar com
  o padrão depois da correção. Sugestão do `code-reviewer` no `[009]`.
- Registro correto: `grep -rn "pt-BR/\|en-US/"` em `docs/{adr,architecture,specs}`, `AGENTS.md`,
  `README.md`, `prompts/`, `.github/instructions/`, `.claude/`, `memory/context/` (excluindo
  `pt-BR/en-US` e `theory.`) → **5 linhas**, todas históricas: `ADR-0007:80` (alternativa
  considerada), `:183` (justificativa da escolha), `:206` (alternativa descartada) e
  `ADR-0003:8-9` (as duas linhas da nota de emenda editorial). **Nenhuma como opção viva** — a
  conclusão do `[004]` não muda; só o número.

## [012] ACTION — 2026-08-01 18:50 — platform-architect
- Ação: sugestão 2 do `[009]` acatada — a **emenda editorial** deixa de ser precedente solto e
  vira convenção escrita em `docs/adr/README.md`, logo abaixo de "Um ADR nunca é reescrito".
- Regra registrada: a imutabilidade tem por objeto a **decisão**, não a redação; ilustração de
  ADR aceito que um ADR posterior tornou falsa se corrige, com linha
  `Emenda editorial (data, TCK-NNNN)` no cabeçalho dizendo o que exibia, o que passou a exibir e
  que nenhuma decisão mudou. Duas fronteiras: (a) se a frase falsa **for** a decisão, o caminho
  é `superseded`, não emenda; (b) manter a ilustração errada com nota em contrário é pior,
  porque diagrama é normativo (`docs/DOC-STANDARDS.md`) — que é o argumento com que o revisor
  aprovou o caso concreto, melhor que o meu.
- Arquivo alterado: `docs/adr/README.md` (18º deste ticket).
- Resultado: ok.
- Lição: n/a.

## [013] ACTION — 2026-08-01 18:52 — platform-architect → tech-lead
- Ação: sugestão 3 do `[009]` — roteamento explícito das pendências de outro dono, confirmadas
  pelo revisor como não sendo minhas. Registrado aqui porque **não abro ticket de outra área**.
- 1. **`ui-ux-designer`** — `docs/design/minimum-learning-slice/screen-states.md:689` e `:833`
  dizem que o `ADR-0007` está `proposed` / com "aceite pendente". Status agora falso; a decisão
  que o documento descreve (URL minúscula) continua correta e **não** muda. Correção de uma
  linha em cada ponto.
- 2. **`product-analyst` / `tech-lead`** — `docs/specs/minimum-learning-slice/plan.md:103` diz
  "Não existe código hoje", superado pelo TCK-0015. É consequência daquele ticket, não deste.
- 3. **`tech-lead`** — pendência aberta por mim no TCK-0003 e ainda não endereçada:
  `memory/agents/{tech-lead,product-analyst,docs-writer}.md`, `.claude/agents/tech-lead.md`,
  `.claude/skills/ticket/SKILL.md` e `.claude/workflows/feature-plan-review.js` ainda tratam o
  `ADR-0003` como `proposed`. Com `ADR-0006` e `ADR-0007` aceitos hoje, o risco cresce: são as
  regras que os agentes leem (L-010).
- Resultado: ok — encaminhado nominalmente.
- Lição: n/a.

## [014] HANDOFF — 2026-08-01 18:55
- De: platform-architect → Para: code-reviewer
- Status novo: in_review
- O que foi feito: correção do único defeito bloqueante do `[009]` — `sync-ai-adapters.py`
  executado, 9 adapters regenerados e declarados como artefatos, as duas auditorias
  reexecutadas com saída no log e **exit 0 nas duas**. Mais as 3 sugestões: contagem corrigida
  por `CORRECTION` (`[011]`), convenção de emenda editorial escrita em `docs/adr/README.md`
  (`[012]`) e pendências de outro dono roteadas ao `tech-lead` (`[013]`).
- Artefatos novos desde o `[008]`: os 9 gerados listados no `[010]` e `docs/adr/README.md`.
  Total do ticket: 18 arquivos + 9 gerados.
- Como validar: `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (exit 0);
  `bash scripts/audit-content.sh` → `0 erros · 0 avisos` (exit 0);
  `python3 scripts/sync-ai-adapters.py --check` → `up-to-date`.
- Pendências e riscos: (a) os 6 gerados de `core` levam junto a edição **não commitada** do
  TCK-0006 em `core.instructions.md` (provado no `[010]` por `git show HEAD:… | grep -c` → 0) —
  estado prévio do working tree, declarado para não ser lido como arraste meu; quem commitar
  leva os dois textos; (b) TCK-0015 segue em revisão e **não foi tocado** — prova por mtime e
  por `diff` do `git status` no `[010]`; (c) proteção de branch em `main` continua pendente de
  ato do usuário.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8.

## [009] REJECT — 2026-08-01 18:55
- De: code-reviewer#10 → Para: platform-architect · Loop nº: 1/3

**Contexto que mudou durante a revisão:** o TCK-0006 fechou como `done` e foi commitado
(`dea3303`). A restrição do `[003]` — "o TCK-0006 é o único autorizado a rodar
`sync-ai-adapters.py`" — **caiu**. Isso muda o julgamento do único ponto pendente, e só dele.

- Defeitos (numerados, cada um com evidência e critério violado):

  1. **BLOQUEANTE — o sync não rodou, e o impedimento externo que justificava adiá-lo não
     existe mais. A dívida é 100% desta cadeia, provada por medição minha.**
     Critérios violados: **6** ("Onde a fonte for canônica, rodar
     `python3 scripts/sync-ai-adapters.py`" — literal no `ticket.md:54`) e **8**
     (`audit-ai-surface.sh` sem erros).
     Evidência, reexecutada **depois** do commit do TCK-0006:
     - `python3 scripts/sync-ai-adapters.py --check` → **exit 1**, os mesmos 9 arquivos
       (`.cursor/rules/{app,core}`, `.windsurf/rules/{app,core}`, `.agents/rules/{app,core}`,
       `.rules`, `.clinerules`, `.junie/guidelines.md`).
     - `bash scripts/audit-ai-surface.sh` → **exit 1**, uma única linha vermelha
       (`:38 OUTDATED`), tudo o mais verde.
     - **Atribuição provada por regeneração, não por inferência:** copiei o working tree para
       o scratchpad (`tar` sem `.git`), rodei o sync **na cópia** e diferenciei os 9 gerados
       contra os do repositório. O delta semântico é **inteiramente seu**: o parágrafo
       "Também decididos em 2026-08-01: projeto Astro na raiz e URL … `/pt-br/…`, `/en-us/…`
       … previews por PR, sem segredo no repositório e sem analytics do host" em `core`, e os
       três itens novos de `app` (URL minúscula, `src/content-contract/` sem gerador,
       dependência que chega ao navegador). O resto do diff é deslocamento de linha. O texto
       do TCK-0006 (`agrupamento dito em palavras`) aparece **dos dois lados** — ele já estava
       sincronizado. Sua conclusão em `[005]` estava certa; o método (`HEAD` × gerado) caducou
       com o commit, o meu não.
     - Consequência real: quem commitar este ticket **quebra o CI** (`.github/workflows/
       ai-surface-audit.yml`). Com o direito liberado, a dívida deixa de ter dono externo e
       passa a ser sua, nesta rodada.
     Correção pedida: `python3 scripts/sync-ai-adapters.py` (sem `--check`), reexecutar as duas
     auditorias com a saída no log, marcar o critério 8 `[x]` e **declarar os 9 gerados** na
     lista de artefatos (AGENTS.md §10, regra 2).
     **Aviso para não te custar um segundo loop:** o working tree é compartilhado. O sync vai
     carregar junto a edição **ainda não commitada** do TCK-0006 em
     `.github/instructions/core.instructions.md` (item 6, leitura de fórmula) — ela já está nos
     gerados hoje (`grep -c "agrupamento dito em palavras"` = 1 em cada um) e `dea3303`
     **não** a incluiu. Isso não é resíduo arrastado por você: é estado prévio do working tree.
     Registre no log para o QA não confundir, e não reverta nada.

- Sugestões (não bloqueiam):
  - **S1 — precisão do `[004]`.** Você declarou "6 linhas, todas históricas" na varredura de
    `/pt-BR/`. Minha contagem em `docs/` dá **5**: `ADR-0007:80`, `:183`, `:206` e a nota de
    emenda em `ADR-0003:8-9`. Nenhuma é opção viva — o veredito está certo, o número não.
  - **S2 — a forma da emenda editorial merece virar convenção.** `docs/adr/README.md:11` só
    diz "um ADR nunca é reescrito para mudar a decisão"; nada diz **como** se corrige uma
    ilustração falsa em ADR aceito. Uma linha lá (ou em `docs/DOC-STANDARDS.md`) descrevendo o
    formato que você usou — nota no cabeçalho, datada, com o ticket e "nenhuma decisão foi
    alterada" — evita que o próximo agente escolha entre reescrever calado e deixar o diagrama
    mentindo.
  - **S3 — as pendências de `[006]` precisam de ticket, não de nota.** `screen-states.md:689`
    e `:833` (`ui-ux-designer`) e `plan.md:103` (`product-analyst`/`tech-lead`) continuam
    corretos como fora do seu escopo; peça ao `tech-lead` o roteamento no handoff, senão ficam
    órfãos como já ficou a pendência do `ADR-0003` que você abriu no TCK-0003 e segue aberta.

- **Checagem de reincidência (feita antes de tudo): negativa nas duas famílias.**
  - **B2 (ADR decide mecanismo em vez de resultado — L-011/L-020):** extraí os 7 itens de
    "Decisões de implementação a tomar nos tickets" (`plan.md:132-142`) e passei cada um pelos
    dois ADRs. Itens 1, 3, 4, 6 e 7 continuam com o ticket e **estão nomeados** no terceiro
    bloco de consequências (`ADR-0007:275-282`: biblioteca de UI, ferramenta de teste, camada
    offline, momento em que a matemática vira HTML). O item 5 (lugar do portão do RF-18) — o
    defeito exato do loop 1 do TCK-0011 — está preservado em **quatro** lugares:
    `ADR-0006:132-133` ("não diz … onde o portão de publicação roda"), pendência 1 declarada
    **Aberta** em `:243-252` com a frase "Aceitar este ADR não transfere a decisão para cá",
    `ADR-0007:125-128` e o terceiro bloco `:280`. O item 2 (forma da URL) foi fechado **pelo
    usuário**, não pelo ADR. Conferi também se os blocos novos de consequências introduzem
    mecanismo: cada afirmação ("mapa único em `src/content-contract/`", "revisão do
    `security-auditor`", "Node ≥ 22.12.0", "dados como propriedade serializados na build")
    já estava no corpo aceito no TCK-0011 (`git show HEAD:` linhas 136, 140-141, 168, 182-183).
    Nenhum enunciado novo.
  - **B4 (marcador inconsistente em diagrama — L-013):** varredura da raiz
    `grep -rn "PROPOSTO (ADR-000[67])"` → ocorrências **só** em `tickets/**` (logs append-only
    e `ticket.md`); nem `docs/design/` aparece. Varri **relação por relação** os dois C4: em
    `c4-container.md` os 4 containers do pipeline e as 14 relações estão sem marcador com a
    fonte no rótulo, e as duas ressalvas viraram texto do rótulo em vez de marcador órfão
    (`:35` proteção de branch = ato do usuário; `:52` lugar do portão = `EM ABERTO (ticket)`).
    `EM ABERTO (ticket)` preservado: **4** em `c4-container.md` (`:13`, `:44`, `:52`, `:78`),
    2 em `docs/architecture/README.md`, 1 em cada ADR (`ADR-0006:122`, `ADR-0007:215`) — bate
    com o que você declarou. Procurei também o erro simétrico (elemento que ainda espera
    decisão e perdeu o marcador): não achei.

- O que já está bom (não refazer):
  - **Critério 1** — `accepted`, 2026-08-01, decisor Douglas Silva nos dois cabeçalhos; o
    aviso de bloqueio foi **substituído** por um que diz o que destrava **e** o que continua
    aberto (`ADR-0006:10-15`, `ADR-0007:10-17`). `docs/adr/README.md:16-17` idem.
  - **Critério 2** — as três decisões na seção Decisão de quem as governa, com a fórmula
    "proposta confirmada por Douglas Silva em 2026-08-01": URL minúscula `ADR-0007:175`,
    projeto na raiz `:90`, previews `ADR-0006:89`. "Perguntas ao usuário" → "Respostas do
    usuário no aceite" (`ADR-0007:317-323`). Mérito não reaberto em lugar nenhum.
  - **Critério 3** — três blocos nos dois ADRs, com o terceiro fazendo o trabalho que L-011 e
    L-020 pedem. `ADR-0006:171-203`, `ADR-0007:253-282`.
  - **Critério 4 — e o julgamento que você pediu, respondido:**
    (a) **A emenda no `ADR-0003` é conduta correta**, e a alternativa que você ofereceu (nota
    sem mexer no rótulo) seria **pior**. Mermaid é parte normativa (`docs/DOC-STANDARDS.md`);
    deixar `:86` exibindo `/pt-BR/…` com uma nota dizendo o contrário recria exatamente o
    defeito B4 pelo qual eu te reprovei duas vezes hoje — texto certo, diagrama mentindo. A
    regra de `docs/adr/README.md:11` proíbe reescrever ADR **para mudar a decisão**; você não
    mudou nenhuma: trocou uma ilustração por um enunciado neutro ("uma rota estática por
    idioma"), declarou a emenda no cabeçalho com data, ticket e "nenhuma decisão foi alterada",
    e o diff inteiro é `+7 −2`. Mantenha.
    (b) **Manter `/pt-BR/` nas alternativas do `ADR-0007` está certo** — contestei e não achei
    por onde derrubar. O critério 4 fala de grafia "viva"; alternativa descartada é o registro
    de *por que* a decisão é a que é, e apagá-la quebraria o formato de ADR. O que torna isso
    seguro não é o argumento, é o parágrafo "Fechado no aceite" (`:191-194`), que nomeia a
    grafia como não-opção — sem ele, eu teria bloqueado. Minha varredura própria confirmou:
    5 ocorrências em `docs/`, nenhuma apresentada como escolha disponível.
    (c) A edição de `spec.md:277` (área do `product-analyst`) é proporcional: você mexeu **só**
    na pergunta que a decisão respondeu, com tachado que preserva o histórico, e deixou
    `plan.md:103` — que é consequência do TCK-0015, não do aceite — para o dono. A fronteira
    que você aplicou é a certa.
  - **Critério 5** — ver checagem de reincidência acima.
  - **Critério 6** — varredura da raiz refeita por mim, com dois padrões
    (`ADR-000[67].{0,120}(proposed|pendente|hipótese)` e o inverso): fora de `tickets/**` e
    `memory/agents/**`, sobram exatamente `docs/design/…/screen-states.md:689` e `:833`, que o
    ticket põe fora de escopo em letra e você declarou nominalmente em `[006]`. **Confirmo que
    são de outro dono** (`ui-ux-designer`, AGENTS.md:317; documento produzido no TCK-0013).
    A propagação normativa chegou onde importa — `AGENTS.md` §1 e §11, `README.md`,
    `prompts/bootstrap-session.md`, `core`/`app.instructions.md` — que é o que L-010 cobra;
    falta só o passo mecânico do defeito 1.
  - **Critério 7** — `docs/adr/README.md` com a nota do que o aceite **não** fecha, e
    `memory/context/project-context.md` com os dois ADRs migrados para "Decisões aceitas",
    "7 ADRs, todos `accepted`", e o lugar do portão mantido em "Decisões em aberto".
  - **Critério 8, metade content** — `bash scripts/audit-content.sh` → `1 nós · 0 erros ·
    0 avisos`, reexecutado por mim.
  - **Mermaid** — reparsei os **5** blocos por conta própria (Node **v24.14.1** existe, como
    da última vez), `mermaid@11` + `jsdom` no scratchpad: **5 ok · 0 falhas**.
  - **L-025** — formato correto (`Tipo: correção`, `ID`, `Contexto`, `Lição`, `Como aplicar`
    com 4 passos executáveis), indexada em `memory/LESSONS.md:47` **dentro da seção
    `## Correção`** (que começa em `:23`) e em `memory/MEMORY.md:104`; `grep '^\*\*ID:\*\*'`
    em `memory/lessons/` sem colisão de `L-NNN`. **Não duplica L-010 nem L-020**: L-010 é
    *propagar* o aceite, L-020 é *o que* vai para ADR, L-025 é a distinção entre autorização e
    aceite — e o item 3 do "Como aplicar" ("o aceite autoriza aquele trabalho e não atesta que
    ele esteja correto") é ação nova, aplicada no próprio artefato (`ADR-0006:138-139`,
    `ADR-0007:233-235`).
  - **Escopo** — `git diff --stat` filtrado por caminho: nada em `package.json`, `src/`,
    `vercel.json`, `.github/workflows/`, `content/`, `docs/content/`, `scripts/` nem nos
    tickets TCK-0006/0015. Os 17 arquivos declarados batem.

## [015] HANDOFF — 2026-08-01 19:10
- De: code-reviewer#10 → Para: qa-validator
- Status novo: in_validation
- O que foi feito: **APROVADO no loop 2/3.** O defeito 1 do `[009]` está fechado: sync
  executado, 9 adapters regenerados e declarados, as três verificações reexecutadas **por mim**
  com exit 0. As 3 sugestões foram acatadas — `CORRECTION` da contagem, convenção de emenda
  editorial escrita e pendências roteadas. Nenhum bloqueante novo. Loop encerrado em 1 devolução.
- Artefatos: os 17 do `[004]` + `docs/adr/README.md` (`[012]`) + os 9 gerados do `[010]`.
- Como validar: `bash scripts/audit-ai-surface.sh` · `bash scripts/audit-content.sh` ·
  `python3 scripts/sync-ai-adapters.py --check`.

**Verificações que fiz nesta rodada (não repetir as do `[009]`, que continuam valendo):**

1. **Os três comandos, reexecutados por mim, com exit code medido:**
   `sync --check` → **exit 0**, "Tudo já estava atualizado"; `audit-ai-surface.sh` → **exit 0**,
   `:38 up-to-date` e `:43 Resultado: OK`; `audit-content.sh` → **exit 0**,
   `1 nós · 0 erros · 0 avisos`. **Critérios 6 e 8 fechados.**
2. **O sync produziu exatamente o que eu havia previsto — prova forte.** No `[009]` eu tinha
   regenerado os 9 arquivos numa **cópia** no scratchpad, antes de ele agir. Comparei agora os 9
   do repositório contra os 9 da minha cópia: **9/9 byte-idênticos**. Não houve surpresa, não
   houve arraste, e a minha atribuição do loop 1 fica confirmada por construção.
3. **Separação `core` × `app` confirmada, arquivo a arquivo** (é o que diz a quem commitar o que
   está levando): `/pt-br/` = 1 nos **9**; `agrupamento dito em palavras` = 1 nos **6** derivados
   de `core` (`.cursor|.windsurf|.agents/rules/core`, `.rules`, `.clinerules`,
   `.junie/guidelines.md`) e **0** nos 3 de `app`. A causa está confirmada na fonte:
   `git show HEAD:.github/instructions/core.instructions.md | grep -c` → **0**, working tree →
   **1**. O `dea3303` deixou a edição do TCK-0006 fora do commit; a separação que ele declarou
   é exata.
4. **Escopo do sync, medido por mtime — 9 arquivos, nada além.** Os 9 têm mtime `17:43:13`;
   `.cursor/rules/content.mdc`, `.windsurf/rules/content.md` e `.agents/rules/content.md`
   ficaram em `16:55:45` (saída prévia do TCK-0006, não recriada). Nenhuma mudança em
   `.claude/commands/`, `.github/chatmodes/`, `.github/prompts/`, `.gemini/commands/` nem
   `SLASH_COMMANDS.md` — coerente com "adapter de agent é ponteiro, só regra é embutida".
5. **TCK-0015 intocado, verificado por método próprio.** `package.json` 17:28:52 ·
   `vercel.json` 17:00:15 · `astro.config.mjs` 16:57:31 ·
   `.github/workflows/ai-surface-audit.yml` 17:29:53 — **todos anteriores ao sync das 17:43**, e
   `src/`/`public/` seguem `??`. Confirmo as duas provas dele.
6. **Os artefatos do loop 1 não foram perturbados pela correção.** Por mtime: os dois ADRs
   (17:18, 17:20), `ADR-0003` (17:22), os dois C4 (17:21), `AGENTS.md` (17:24), `README.md`
   (17:24), `project-context.md` (17:29) e a lição (17:31) são todos **anteriores** à correção.
   Só mudaram `docs/adr/README.md` (17:44) e os 9 gerados. Correção mínima e cirúrgica — não
   precisei reabrir nada do `[009]`.
7. **`[011] CORRECTION` — correta em forma e em fato.** Traz `Corrige: [004]`, "O que estava
   errado" e "Registro correto" (`ticket-protocol.md:170-181`). E a explicação se confere:
   `git show HEAD:docs/specs/minimum-learning-slice/spec.md` tem `/pt-BR/high-school/…` em
   `:277` — era mesmo a sexta linha, que ele próprio removeu antes de contar. Recontei com o
   comando dele: **5**, batendo com a minha contagem independente do `[009]`.
8. **`[012]` — a fronteira está bem colocada na direção perigosa, com uma imprecisão.**
   Ela impede o abuso que me preocupava: "a emenda só vale para o que o ADR **não** decide — se
   a frase falsa for a decisão, o caminho é `superseded`". Isso barra usar "emenda editorial"
   como licença para reescrever decisão. A convenção mora em `docs/adr/README.md`, que
   `/create-adr` manda ler no passo 2 — alcançável por quem cria ADR. Ver S5.
9. **`[013]`** — os três encaminhamentos batem com o que confirmei no `[009]`: `screen-states.md`
   `:689`/`:833` é do `ui-ux-designer`; `plan.md:103` é consequência do TCK-0015; e a pendência
   do `ADR-0003` aberta no TCK-0003 continua aberta e agora está nomeada.
10. **Log íntegro:** `git diff --numstat` do `log.md` → **246 inserções, 0 remoções**. Nada foi
    reescrito nem apagado. Ver S4 sobre a ordem física.

- **Reincidência: negativa.** Nada nesta rodada toca ADR, diagrama ou marcador (item 6 acima),
  então as famílias B2 e B4 não têm superfície nova. A varredura completa das duas está no
  `[009]` e continua válida.

- **Sugestões para o QA decidir se viram dívida registrada (nenhuma bloqueia):**
  - **S4 — ordem física do log × ordem de `[SEQ]`.** As entradas `[010]`–`[014]` foram inseridas
    **antes** do meu `[009]`, que ficou por último (`grep -n "^## \["` → `[008]`, `[010]`…`[014]`,
    `[009]`). Conteúdo íntegro (0 remoções, item 10), mas quem ler de cima para baixo encontra o
    `[014] HANDOFF` e a correção **antes** do `REJECT` que eles respondem. Provável efeito de dois
    agentes escrevendo o mesmo arquivo. **Ler o log por `[SEQ]`, não por posição.** Não reordenar:
    reordenar seria reescrever log publicado.
  - **S5 — as duas metades da fronteira (a) do `[012]` não são equivalentes.** "A emenda só vale
    para o que o ADR **não** decide" é mais restrita que "se a frase falsa **for** a decisão, o
    caminho é `superseded`". Entre as duas cai um caso real e já visto: rótulo de diagrama que
    contradiz a **própria** decisão do ADR (foi o meu B4 do TCK-0003, "KaTeX pré-renderizado").
    Ali o assunto **é** decidido por aquele ADR, mas a frase falsa **não é** a decisão — é a
    ilustração divergindo dela, e corrigi-la não muda decisão nenhuma. Pela primeira metade,
    barrada; pela segunda, permitida. Sugiro ficar só com a segunda: *emenda quando a frase falsa
    não é a decisão; `superseded` quando é*. Erro conservador, por isso sugestão.
  - **S6 — duas das três notas de memória dele são de interesse geral e deveriam virar lição.**
    AGENTS.md §5: "conhecimento de interesse geral vai para `memory/lessons/`, não para a memória
    individual do agente". "Dívida declarada expira quando o impedimento acaba" e "prova de
    atribuição por `HEAD` caduca com commit alheio; regenerar em cópia é o método robusto" servem
    a qualquer agente que adie trabalho citando direito exclusivo de outro ticket — não são
    específicas de arquitetura. O `[010]` cita `Lição: L-025` como "mesma família", o que é
    esticado: L-025 fala de autorização × aceite, não de validade de dívida. **Não é defeito** —
    a regra 7 foi cumprida, o conhecimento está registrado com receita executável
    (`grep -m1 "^status:" tickets/…/ticket.md` + `git log --oneline -3`) e é a 1ª aparição da
    causa. Encaminhar ao `retrospective-curator` para julgar se vira `L-026`.

- **Pendências e riscos que o QA precisa carregar (não são defeitos):**
  1. **Estado não commitado de terceiro:** `.github/instructions/core.instructions.md` e os 6
     gerados de `core` levam junto o item 6 do TCK-0006, que o `dea3303` não incluiu. Quem
     commitar o TCK-0016 leva os dois textos. Provado nos itens 3 e 4; **não reverter**.
  2. **TCK-0015 em revisão paralela** — o aceite autoriza aquele trabalho e não atesta que esteja
     correto, o que está escrito nos dois ADRs (`ADR-0006:138-139`, `ADR-0007:233-235`).
  3. **Proteção de branch em `main`** continua pendente de ato do usuário; sem ela o portão de
     mérito é informativo (`ADR-0006`, pendência 2 — declarada **Aberta**).
  4. **`docs/design/…/screen-states.md:689,833`** ainda dizem `ADR-0007 proposed`: de outro dono,
     fora de escopo em letra, roteado em `[013]`.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 — os oito
  com evidência própria minha, os três comandos com exit 0.

## [016] ACTION — 2026-08-01 17:59 — qa-validator#11
- Nota de relógio: 17:59 é a hora **do sistema** (`date` no início e no fim da validação),
  não uma correção das entradas anteriores. O relógio usado nas entradas `[004]`–`[015]`
  corre ~1h à frente do relógio de arquivo (mtime dos ADRs: 17:18–17:20 para o `[004]`,
  das 18:10). Como no `S4`: **ler por `[SEQ]`**, não por carimbo nem por posição.
- Ação: validação dos critérios 1–8 com evidência **reproduzida por mim**. Nenhuma evidência
  herdada do `[004]`, do `[010]` nem do `[015]`.
- **Ambiente:** `HEAD` `dea3303` (estável do início ao fim da validação), Node v24.14.1,
  Python 3.12.3, working tree compartilhado com 54 entradas em `git status --porcelain`.
  Sem URL de preview — validação **documental**: os artefatos são ADR, C4, regras e memória;
  nenhum é consumido por código do produto. A bateria de casos hostis de UI (offline, dois
  idiomas, tema, zoom 200%, teclado, leitor de tela, rede lenta, dados vazios) **não se aplica**
  e a prova do consumidor zero é o próprio escopo: `git diff --stat -- package.json src/
  vercel.json content/ scripts/` → vazio para este ticket (ver critério de escopo abaixo).
- **Leitura do log:** feita por `[SEQ]`, não por posição — `[010]`–`[014]` estão fisicamente
  antes do `[009]`. Integridade conferida: `git diff --numstat` do `log.md` → **347 inserções,
  0 remoções**. Não reordenei nada.

**Critério 1 — `accepted`, data e decisor.** `ADR-0006:3-5` e `ADR-0007:3-5`: `Status:
accepted` · `Data: 2026-08-01` · `Decisores: Douglas Silva (aceite em 2026-08-01, registrado no
TCK-0016)`. Aviso **substituído**, não apagado: `ADR-0006:11-15` e `ADR-0007:11-16` dizem o que
destrava **e** o que continua aberto. Busca negativa nos dois arquivos por
`aceite pendente|espera aceite|aguard|antes do aceite|não aceito` → **0**; as duas ocorrências
de `proposed` que sobram são histórico (`ADR-0006:174`, sobre a proibição que caiu). `[x]`

**Critério 2 — as três decisões na seção Decisão de quem as governa.** Previews por PR →
`ADR-0006:89-90`, item (iii), "proposta confirmada por **Douglas Silva em 2026-08-01**".
Projeto na raiz → `ADR-0007:93-95`, item 2, mesma fórmula. URL minúscula → `ADR-0007:175-176`,
item 7, mesma fórmula. "Perguntas ao usuário (no aceite)" → **"Respostas do usuário no aceite"**
(`ADR-0007:319-326`). Mérito não reaberto: o `git diff` dos dois ADRs (81/34 e 74/28) não
remove nem inverte nenhuma alternativa. `[x]`

**Critério 3 — Consequências em três blocos, nos dois ADRs.** `ADR-0006:169-203` e
`ADR-0007:251-282`, ambos com *O que passa a valer com o aceite* · *O que fica proibido sem ADR
novo* · *O que continua sendo decisão de ticket, apesar do aceite*. Conferi que os blocos novos
**não enunciam mecanismo novo**: cada afirmação rastreada ao corpo já aceito no TCK-0011 por
`git show HEAD:` — `mapa único` 2=2, `como propriedade` 2=2, `22.12.0` 4→5, `security-auditor`
1→2, `própria origem` 1→2, `coleções de conteúdo` 2→3 (os incrementos são a **repetição** da
regra no bloco de consequências, não enunciado novo). `[x]`

**Critério 4 — grafia alternativa fora do diagrama e do ADR.** Varredura da **raiz** (não de
`docs/`), padrão largo `/(pt-BR|en-US)` menos nomes de arquivo: fora de `tickets/**` e
`memory/agents/**` (append-only e histórico) sobram **5 linhas em documento vivo**, todas
registro histórico — `ADR-0007:80` (alternativa considerada), `:183` (justificativa da escolha),
`:206` (alternativa descartada) e `ADR-0003:8-9` (as duas linhas da nota de emenda). **Zero**
como opção viva. Bate com a `[011] CORRECTION`. `c4-container.md:41` conferido contra o `HEAD`:
o rótulo saiu de *"…propostos, `/pt-BR/…` e `/en-US/…` **como alternativa** — PROPOSTO
(ADR-0007)"* para *"`/pt-br/...` e `/en-us/...`, prefixo em minúsculas (ADR-0007)"*.
`docs/specs/…/spec.md:277` deixou de casar com o padrão. `[x]`

**Critério 5 — marcadores por classe, e o que o aceite NÃO fecha.** (a) `PROPOSTO
(ADR-0006|ADR-0007)` na raiz → ocorrências **só** em `tickets/**`; **0** fora. (b) As 8
ocorrências restantes de `PROPOSTO` fora de `tickets/`+`memory/agents/` classificadas uma a uma:
1 legenda (`docs/architecture/README.md:14`), 4 afirmações **negativas** ("sem marcador
`PROPOSTO`" / "não há marcador"), 1 contexto histórico (`ADR-0006:23`), 1 lição
(`fixing-the-cited-line…:28`), 1 memória de área (`memory/context/frontend.md:41`). Nenhuma é
afirmação de estado obsoleto como fato. (c) `EM ABERTO (ticket)` **preservado**: 4 em
`c4-container.md` (`:13`, `:44`, `:52`, `:78`), 2 em `docs/architecture/README.md`, 1 em
`ADR-0006:122`, 1 em `ADR-0007:215`.
**(d) Cruzamento próprio dos 7 itens de `plan.md:132-142` contra os dois ADRs — refeito, não
herdado:**
  1. *modelo concreto de renderização (o que é ilha × o que é estático)* — a **fronteira** está
     em `ADR-0007:163-172` (item 6), **inalterada por este ticket** (o `git diff` não tem hunk
     entre `:122` e `:175`): decidida no TCK-0011, não absorvida pelo aceite. A metade que era
     do ticket — **biblioteca de UI dentro da ilha** — continua nomeada em `:278`. **Aberto.**
  2. *forma exata da URL* — fechada, mas **pelo usuário** e como contrato público (L-020);
     o critério 2 deste ticket manda registrá-la no ADR. A segunda metade ("como o alternador
     reescreve preservando a taxonomia") permanece resolvida por enunciado pré-existente no
     `HEAD` (mapa único; alternador não é ilha). **Fechado legitimamente.**
  3. *momento em que a matemática vira HTML e fontes sem terceiros* — aberto em **4** lugares:
     `ADR-0007:15`, `:23`, `:278`, `c4-container.md:71`. Restrição de CDN é RNF-7
     pré-existente, não decide o momento. **Aberto.**
  4. *camada offline / service worker* — `ADR-0007:15`, `:23`, `:278`, `c4-container.md:44`
     (`EM ABERTO (ticket)`). **Aberto.**
  5. *lugar do portão do RF-18* — **o ponto que mais importa**, aberto em **9** lugares que
     conferi um a um: `ADR-0006:14`, `:122` (rótulo Mermaid), `:131-133`, `:197-199`,
     pendência 1 declarada **Aberta** em `:245-255` com "Aceitar este ADR não transfere a
     decisão para cá"; `ADR-0007:16`, `:125-128`, `:215` (rótulo Mermaid), `:281`, `:292`;
     mais `c4-container.md:52` e `:78-79` e `memory/context/project-context.md`. O TCK-0015
     **exerceu** a escolha e o ADR registra que o aceite autoriza aquele trabalho sem atestá-lo.
     **Aberto.**
  6. *ferramenta de teste* — `ADR-0007:15`, `:23`, `:43`, `:278`, `c4-container.md:73`.
     **Aberto.**
  7. *números do orçamento de performance (RNF-8)* — `grep -niE 'RNF-8|orçamento de
     performance|Lighthouse'` nos dois ADRs, nos dois C4 e em `project-context.md` → **nenhuma
     ocorrência**. Não absorvido; também **não enumerado** no terceiro bloco (ver D-1).
  **Nenhum item que era decisão de ticket foi absorvido pelo aceite.** `[x]`

**Critério 6 — propagação L-010, varredura da raiz.** Dois padrões, nas duas direções:
`ADR-000[67].{0,120}(proposed|pendente|hipótese|aguard|não aceito|espera)` e o inverso. Fora de
`tickets/**` e `memory/agents/**`, sobram exatamente **2 afirmações vivas de status falso** —
`docs/design/minimum-learning-slice/screen-states.md:689` e `:833` —, ambas de **outro dono**
(`ui-ux-designer`) e postas fora de escopo **em letra** pelo `ticket.md:73`. `c4-container.md:79`
e `c4-context.md:6` citam os ADRs como **aceitos** (corretas). Propagação normativa conferida
por diff, arquivo a arquivo: `AGENTS.md` §1 e §11, `README.md`, `prompts/bootstrap-session.md`,
`.github/instructions/core` e `app`, `.claude/agents/platform-architect.md`,
`memory/context/{frontend,devops,project-context}.md`. `[x]`

**Critério 7 — `docs/adr/README.md` e `project-context.md`.** Tabela em `:26-27`: `ADR-0006` e
`ADR-0007` `accepted` 2026-08-01. Nota em `:34-38` diz o que o aceite **não** fecha, com os 5
itens. `project-context.md`: os dois ADRs migrados para "Decisões aceitas" com o que fica
proibido, "**7 ADRs, todos `accepted`**", e **duas** pendências mantidas em "Decisões em
aberto" (lugar do portão; proteção de branch). `[x]`

**Critério 8 — auditorias, exit code medido sem pipe** (`cmd > arquivo 2>&1; echo $?`), rodadas
**duas vezes**, a segunda imediatamente antes deste veredito (17:58) e **depois** da última
edição do TCK-0015 em `.github/workflows/ai-surface-audit.yml` (mtime 17:49) — janela verde
medida com todos os artefatos deste ticket no lugar:
  - `python3 scripts/sync-ai-adapters.py --check` → **exit 0**, "Tudo já estava atualizado".
  - `bash scripts/audit-ai-surface.sh` → **exit 0**, `up-to-date` · `todas dentro do limite` ·
    `documented` · `Resultado: OK`; contagem própria de linhas com
    `outdated|erro|falta|fail|divergen` na saída → **0**.
  - `bash scripts/audit-content.sh` → **exit 0**, `1 nós · 0 erros · 0 avisos`. `[x]`

**Verificações extras que fiz (nenhuma pedida pelos critérios):**
- **Mermaid reparseado por mim** — `mermaid@11` + `jsdom` no scratchpad, `mermaid.parse` nos
  **5** blocos dos arquivos tocados: `5 blocos · 0 falhas`, exit 0.
- **Emenda editorial no `ADR-0003` medida:** `git diff --numstat` → **+7 −2**; a única mudança
  de conteúdo é o rótulo `B --> H` de "`/pt-BR/… · /en-US/…`" para "uma rota estática por
  idioma". Nenhuma linha da Decisão tocada. É emenda de ilustração, não de decisão.
- **Escopo:** `git diff --stat` filtrado por `package.json src/ vercel.json content/
  docs/design/ docs/content/ scripts/ astro.config.mjs` → **vazio**.
  `.github/workflows/ai-surface-audit.yml` e `.gitignore` estão `M`, mas **não são deste
  ticket**, por três provas: (i) não constam da lista de artefatos de `[004]`/`[010]`/`[012]`;
  (ii) o TCK-0015 os reivindica como entrega sua; (iii) mtime `17:49` e `17:00`, o primeiro
  **posterior** ao sync deste ticket (`17:43`) e ao `docs/adr/README.md` (`17:44`).
- **L-025:** formato completo, `**ID:** L-025` sem colisão em `memory/lessons/`
  (`grep -rh '^\*\*ID:\*\*' | sort | uniq -d` → vazio), indexada 1× em `memory/LESSONS.md` e
  1× em `memory/MEMORY.md`.

**Julgamentos que me foram pedidos:**

**(a) Emenda editorial em ADR aceito — a conduta está certa; a convenção fica, com uma
correção de redação que eu decido agora.** A emenda no `ADR-0003` é correta e a alternativa
oferecida (nota sem mexer no rótulo) seria pior: diagrama é normativo por `DOC-STANDARDS.md` e
o leitor obedece ao rótulo. Quanto ao **S5**: a incoerência é **real, e o exemplo do revisor
não é o caso**. O `B4` do TCK-0003 ("KaTeX pré-renderizado") caía no que o `ADR-0003`
**não** decide — logo, permitido pelas duas metades. O caso que cai no vão é outro e é
construível: *rótulo que contradiz a decisão do próprio ADR* (um ADR que decide "deploy no push
em `main`" cujo Mermaid exibe "deploy por tag"). Ali o assunto **é** decidido por aquele ADR —
a metade 1 barra a emenda —, mas a frase falsa **não é** a decisão — a metade 2 permite. Com a
metade 1 valendo, o agente fica sem saída: emenda proibida, e a regra (b) do próprio parágrafo
diz que deixar a ilustração errada é **pior**; sobra `superseded` para consertar um rótulo, o
que destrói o registro sem mudar decisão nenhuma. **Decisão: vale a segunda metade** — *emenda
quando a frase falsa não é a decisão; `superseded` quando a frase falsa é a decisão*. Não é
`REJECT`: a convenção não é pedida por nenhum dos 8 critérios (nasceu do `S2`, sugestão
declarada não-bloqueante), o resíduo erra pelo lado **conservador** (excesso de cerimônia, não
permissão indevida) e reprovar aqui seria renegociar critério depois da entrega. Sai como
**D-1**, com o ajuste de uma linha endereçado ao `tech-lead`.

**(b) Estado não commitado de terceiro — confirmado por medição própria e registrado no
"Resultado final".** `git show HEAD:.github/instructions/core.instructions.md | grep -c
"agrupamento dito em palavras"` → **0**; working tree → **1**. Separação medida arquivo a
arquivo: `/pt-br/` = 1 nos **9** gerados; `agrupamento dito em palavras` = 1 nos **6** que
derivam de `core` e **0** nos 3 de `app`. O `dea3303` deixou a edição do TCK-0006 fora do
commit. **Quem commitar o TCK-0016 leva os dois textos** — o do aceite e o item 5 de leitura de
fórmula do TCK-0006 — em `core.instructions.md` e nos 6 gerados de `core`. Não reverter.

**(c) As duas notas de memória do produtor são de interesse geral — encaminho.** "Dívida
declarada expira quando o impedimento acaba" e "prova de atribuição por `HEAD` caduca com
commit alheio" servem a **qualquer** agente que adie trabalho citando direito exclusivo de outro
ticket ou que prove atribuição em working tree compartilhado — `AGENTS.md` §5 manda isso para
`memory/lessons/`. **Não é defeito**: a regra 7 foi cumprida, o conhecimento está registrado com
receita executável e o índice de lições é mantido pelo `retrospective-curator`, não pelo
`platform-architect`. Encaminho como **candidata a `L-026`** (provavelmente **duas** lições, uma
por arquivo, pela regra "uma lição por arquivo").

- Resultado: **8 de 8 critérios atendidos com evidência própria. 0 defeitos.** 3 dívidas e
  4 `ACTION` no handoff.
- Lição: n/a — não resolve `REJECT`.

## [017] HANDOFF — 2026-08-01 18:00 (relógio do sistema — ver nota do `[016]`)
- De: qa-validator#11 → Para: tech-lead
- Status novo: **done**
- O que foi feito: **APROVADO.** Os 8 critérios validados com evidência reproduzida por mim
  (varredura da raiz em 4 padrões, cruzamento próprio dos 7 itens de `plan.md:132-142`, 5
  blocos Mermaid reparseados, 3 comandos com exit code medido sem pipe, duas vezes). Nenhum
  defeito. Loop encerrado em 1 devolução (`[009]`), fechada no `[010]`.
- Artefatos: 18 arquivos + 9 gerados, conforme `[004]`, `[010]` e `[012]`.
- Como validar (reprodutível): `python3 scripts/sync-ai-adapters.py --check` ·
  `bash scripts/audit-ai-surface.sh` · `bash scripts/audit-content.sh` — **exit 0 nos três**,
  medidos às 17:58 com `HEAD` em `dea3303`.

**Dívidas registradas (nenhuma bloqueia, todas com gatilho):**
- **D-1 — a convenção de emenda editorial tem duas metades não equivalentes**
  (`docs/adr/README.md:9-16`). "A emenda só vale para o que o ADR **não** decide" é mais
  restrita que "se a frase falsa **for** a decisão, o caminho é `superseded`", e entre elas cai
  o rótulo que contradiz a decisão do próprio ADR — corrigível sem mudar decisão. **Decidi que
  vale a segunda**; falta a redação. Correção de uma linha, `platform-architect`, área dele.
  **Gatilho:** a primeira emenda editorial em que o assunto seja decidido pelo próprio ADR.
- **D-2 — a lista "o que continua sendo decisão de ticket" não é exaustiva contra
  `plan.md:132-142`.** Faltam o item 1 (modelo concreto de renderização) e o item 7 (números do
  orçamento de performance, RNF-8). Nenhum dos dois foi **absorvido** — o RNF-8 não aparece em
  ADR nenhum —, então o erro é por omissão, não por fechamento indevido. O risco vem de
  `ADR-0007:325-326` ("o que permanece aberto … **a lista** está em…"), que se lê como
  enumeração fechada. **Gatilho:** o primeiro ticket que precisar fixar os números do RNF-8.
- **D-3 — `plan.md:132-142` envelheceu.** Os itens 1 e 2 já não são decisão de ticket: a
  fronteira ilha × estático está em `ADR-0007:163-172` (desde o TCK-0011) e a forma da URL foi
  fechada pelo usuário no aceite. A spec continua listando os dois como abertos.
  `product-analyst`/`tech-lead`. **Gatilho:** o próximo ticket que ler `plan.md` para saber o
  que pode decidir sozinho.

**`ACTION` ao `tech-lead` (fora do escopo deste ticket, com dono e condição):**
1. **`docs/design/minimum-learning-slice/screen-states.md:689` e `:833`** afirmam `ADR-0007
   proposed` / "aceite pendente" — **status agora falso**, e é a única classe de ocorrência que
   arrisca anular um desbloqueio (afirmação do estado obsoleto como fato). Dono
   `ui-ux-designer`; o TCK-0013 está `done`, então precisa de **ticket novo**, não de nota.
   Correção de uma linha em cada ponto; a decisão descrita (URL minúscula) continua correta.
2. **Pendência do TCK-0003 ainda aberta:** `memory/agents/{tech-lead,product-analyst,
   docs-writer}.md`, `.claude/agents/tech-lead.md`, `.claude/skills/ticket/SKILL.md` e
   `.claude/workflows/feature-plan-review.js` tratam o `ADR-0003` como `proposed`. Com mais dois
   ADRs aceitos hoje, o risco cresce: são as regras que os agentes leem (L-010).
3. **`retrospective-curator`:** promover a `L-026` as duas notas de memória de interesse geral
   do `platform-architect` — "dívida declarada expira quando o impedimento acaba" e "prova de
   atribuição por `HEAD` caduca com commit alheio" (`AGENTS.md` §5). Uma lição por arquivo.
4. **`tickets/TCK-0015-.../ticket.md:89-90`** ainda descreve os dois ADRs como `proposed` no
   bloco de referências. É ticket de outra cadeia, em revisão paralela — não toquei. Vale um
   `CORRECTION` no log de lá quando ele fechar.

**Pendências que o próximo passo carrega (não são defeitos):**
1. **Quem commitar leva dois textos.** `.github/instructions/core.instructions.md` e os 6
   gerados de `core` contêm, além do aceite, o item 5 de leitura de fórmula do TCK-0006, que o
   `dea3303` deixou fora do commit (provado em `[016]`, julgamento (b)). **Não reverter.**
2. **TCK-0015 em revisão paralela** — o aceite autoriza aquele trabalho e **não** atesta que
   esteja correto (`ADR-0006:138-139`, `ADR-0007:233-235`).
3. **Proteção de branch em `main`** continua pendente de ato do usuário; sem ela o portão de
   mérito é informativo (`ADR-0006`, pendência 2, **Aberta**).
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 — os oito
  com evidência própria, medida em `dea3303`.
