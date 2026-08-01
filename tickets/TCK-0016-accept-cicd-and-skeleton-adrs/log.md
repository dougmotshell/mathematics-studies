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
