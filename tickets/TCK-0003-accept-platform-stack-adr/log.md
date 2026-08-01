# Log — TCK-0003

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 12:40 — tech-lead
- Ação: ticket criado a partir da decisão do usuário sobre o `ADR-0003`.
- Motivo: o ADR `proposed` era o maior bloqueio único do backlog (diagnóstico do dev-loop
  `analyze-open-tickets`); o decisor nomeado no próprio ADR escolheu a opção C (site
  estático orientado a conteúdo com ilhas) e persistência local-first sem conta.
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 12:40 — tech-lead
- Ação: triagem. Tipo `docs`, P1, tamanho P, owner `platform-architect`.
- Motivo: o artefato é um ADR de arquitetura — escopo exclusivo do `platform-architect`
  (AGENTS.md §10). Não há ambiguidade de requisito, então `product-analyst` é dispensado.
- Cadeia definida: `platform-architect` → `code-reviewer` → `qa-validator`.
- Restrições: registrar a decisão, não implementá-la; nenhuma dependência instalada; nenhum
  código criado; `content/` intocado.
- Resultado: ok — `triaged`.

## [003] HANDOFF — 2026-08-01 12:40
- De: tech-lead → Para: platform-architect
- Status novo: in_progress
- O que foi feito: decisão humana coletada e registrada no ticket; execução autorizada pelo
  usuário ("faça tudo que for necessário").
- Artefatos: `tickets/TCK-0003-accept-platform-stack-adr/ticket.md`.
- Como validar: critérios 1–6 do ticket; auditorias determinísticas ao final.
- Pendências e riscos: o `TCK-0002` (spec da fatia mínima) roda em paralelo e foi escrito
  sob a premissa de independência de framework — o aceite não invalida a spec, mas o
  `plan.md` dela passa a poder citar a stack aceita em vez de "a definir".
- Critérios de aceite: [ ] 1–6 restantes.

## [004] ACTION — 2026-08-01 13:20 — platform-architect
- Ação: aceite do `ADR-0003` registrado e propagado.
- Decisão gravada: opção **C** — gerador de site estático orientado a conteúdo (Astro) com
  **ilhas de interatividade** só onde há exercício — e persistência **local-first sem conta**
  (opção 1, IndexedDB). Deploy estático na Vercel, portátil para qualquer host estático.
- ADR: `status: accepted`, decisor Douglas Silva, data 2026-08-01; bloco de aviso "nenhum
  ticket deve avançar" substituído por nota de desbloqueio da frente de plataforma.
- Seção **Decisão** reescrita sem ambiguidade, com uma linha por alternativa descartada
  (A Next.js, B SPA Vite, persistência 2 sincronizada, persistência 3 backend obrigatório) +
  Mermaid curto `content/` → build estática → HTML por idioma → ilha → IndexedDB (regra
  visual do `docs/DOC-STANDARDS.md`), com leitura e fontes.
- Seção **Consequências** preenchida: JavaScript mínimo por padrão e interatividade confinada
  a ilhas; rotas estáticas por idioma com paridade obrigatória (`ADR-0002`); PWA offline-first
  para conteúdo visitado; KaTeX pré-renderizado com descrição acessível; **backend, conta,
  login e telemetria identificável exigem ADR novo**; gabarito viaja no payload do cliente,
  logo nada pode depender do segredo da resposta; portabilidade do deploy estático.
- Nova seção **Restrição a preservar — independência do contrato de dados**: `content/`
  permanece legível sem a aplicação (teste de conformidade declarado).
- Propagação: `docs/adr/README.md` (apenas a linha do `ADR-0003` + a nota que falava dele —
  edição cirúrgica, tabela intocada no restante); `memory/context/project-context.md`
  (`ADR-0003` sai de "decisões em aberto" e entra em "decisões aceitas"; tabela de frentes,
  novos itens em aberto e próximos passos atualizados);
  `memory/context/frontend.md` (stack em vigor + 8 decisões operacionais decorrentes).
- Fora de escopo respeitado: nenhum código, nenhum `package.json`, nenhuma dependência,
  nenhuma escolha de biblioteca de UI/testes/service worker; `content/`, `docs/specs/` e os
  tickets TCK-0001/0002/0004 intocados.
- Evidência (critério 6):
  - `bash scripts/audit-ai-surface.sh` → `Resultado: OK` · exit 0 (regras dentro do limite de
    12.000 caracteres; `sync-ai-adapters.py --check` = `up-to-date`; acesso do Codex
    documentado).
  - `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos` · exit 0.
- Lição registrada: **L-008** (`client-side-answer-key-is-a-product-constraint`) — índices
  `memory/LESSONS.md` e `memory/MEMORY.md` atualizados.
- Resultado: ok — critérios 1–6 atendidos do ponto de vista do produtor; validação é da
  cadeia seguinte.

## [005] HANDOFF — 2026-08-01 13:20
- De: platform-architect → Para: code-reviewer
- Status novo: in_review
- O que foi feito: decisão do usuário transformada em ADR aceito e propagada para
  documentação e memória. Nenhuma implementação.
- Artefatos:
  - `docs/adr/ADR-0003-platform-stack.md` (principal)
  - `docs/adr/README.md`
  - `memory/context/project-context.md`
  - `memory/context/frontend.md`
  - `memory/lessons/client-side-answer-key-is-a-product-constraint.md`
  - `memory/LESSONS.md`, `memory/MEMORY.md`, `memory/agents/platform-architect.md`
- Como validar (checklist dos critérios 1–6):
  1. `ADR-0003` tem `status: accepted`, `Data: 2026-08-01`, decisor Douglas Silva, e o bloco
     de aviso de bloqueio foi substituído por nota de desbloqueio.
  2. **Decisão** afirma opção C + local-first sem conta sem ambiguidade e justifica A, B,
     persistência 2 e persistência 3.
  3. **Consequências** cobre os sete pontos exigidos pelo ticket (JS mínimo/ilhas; rotas por
     idioma com paridade; PWA offline-first; KaTeX acessível; backend/conta/login/telemetria
     só com ADR novo; gabarito no cliente; deploy estático portátil).
  4. Independência do contrato de dados de `content/` declarada como restrição a preservar,
     em seção própria.
  5. `docs/adr/README.md`, `memory/context/project-context.md` e `memory/context/frontend.md`
     não descrevem mais o `ADR-0003` como decisão em aberto
     (`grep -rn "ADR-0003" docs/ memory/` para conferir).
  6. Auditorias verdes — reexecutar `bash scripts/audit-ai-surface.sh` e
     `bash scripts/audit-content.sh` (ambas exit 0).
  Verificar também o que **não** foi feito: nenhum arquivo de código, nenhuma dependência,
  nenhuma biblioteca escolhida.
- Pendências e riscos:
  - `TCK-0002` (spec da fatia mínima) roda em paralelo: o `plan.md` dela pode agora citar a
    stack aceita em vez de "a definir" — ajuste é do dono daquele ticket, não deste.
  - `docs/adr/README.md` receberá o `ADR-0005` de outro agente; a edição aqui foi cirúrgica
    para evitar conflito.
  - `L-008` assume que nenhum outro agente reivindicou o mesmo identificador em paralelo;
    conferir no review.
  - Fóruns e certificados do roadmap ficam sem solução arquitetural — exigem ADR próprio.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 (a confirmar pela
  cadeia de revisão/validação).

## [006] REJECT — 2026-08-01 12:55
- De: code-reviewer → Para: platform-architect · Loop nº: 1/3
- Status novo: in_progress
- Escopo revisado: `git diff` de `docs/adr/ADR-0003-platform-stack.md`, `docs/adr/README.md`,
  `docs/architecture/{README.md,c4-context.md}`, `memory/context/{project-context,frontend}.md`,
  `memory/lessons/client-side-answer-key-is-a-product-constraint.md`, `memory/LESSONS.md`,
  `memory/MEMORY.md`, `memory/agents/platform-architect.md`.
- Comandos usados: `git status --porcelain -uall`; `git diff --stat`; `git diff --no-color <arquivos>`;
  `grep -rn "ADR-0003" docs/ memory/ AGENTS.md .claude/ .github/ tickets/`;
  `grep -rn '^\*\*ID:\*\*' memory/lessons/`; `bash scripts/audit-ai-surface.sh` (→ `Resultado: OK`, exit 0);
  `bash scripts/audit-content.sh` (→ `1 nós · 0 erros · 0 avisos`, exit 0);
  `stat -c '%y %n'` para separar este diff do de tickets paralelos (TCK-0001/0002/0004 escrevem
  no mesmo working tree — `content/.../references.json`, `docs/specs/`, `LICENSE*`, `ADR-0005`
  **não** pertencem a este ticket e não foram avaliados aqui).

### Defeitos bloqueantes

**B1 — O aceite não foi propagado para as regras que governam o comportamento dos agentes;
o "desbloqueio" é inerte onde importa.** (critério 5; critério 1 parcialmente)
Evidência — ainda afirmam `proposed` / stack indecidida:
- `AGENTS.md:38` (§1): "A stack ainda **não está fechada** … (status `proposed`). Enquanto o ADR
  não for aceito, nenhum agente deve assumir framework, banco ou biblioteca como decidido."
- `AGENTS.md:422` (§11, Regras gerais): "**Não assumir stack**: enquanto `ADR-0003` estiver
  `proposed`, tratar framework, banco e bibliotecas como hipótese, não como fato."
- `.github/instructions/core.instructions.md:33-34`: "A stack **não está decidida** … `proposed`."
- `.github/instructions/app.instructions.md:6-7`: reproduz o **mesmo aviso de bloqueio** que o
  critério 1 manda remover, e com `applyTo: "src/**,app/**,api/**,tests/**,e2e/**"` — ou seja,
  aplica-se exatamente aos tickets que este ADR deveria destravar.
- `.claude/agents/platform-architect.md:36` (área exclusiva do próprio produtor): "Enquanto
  `docs/adr/ADR-0003-platform-stack.md` estiver `proposed`, tratar stack como hipótese."
- `docs/product/roadmap.md:29`: Fase 1 ainda lista "Decidir e aceitar `ADR-0003` (stack)" como
  tarefa pendente — a metade da licença foi corrigida pelo TCK-0004, a da stack não.

Decisão de escopo (argumentada, não "talvez"): **isto é defeito deste ticket, não pendência de
outro.** Três razões: (a) o requisito refinado do ticket manda "propagar o desbloqueio para a
memória e a documentação do projeto", e o `AGENTS.md` se declara "o **arquivo-fonte único** de
instruções do projeto", lido no início de sessão pelas 12 ferramentas — enquanto `AGENTS.md:422`
disser o contrário, o próximo agente lê a regra, não o ADR, e o ticket não entrega seu propósito;
(b) o critério 5 é explícito em "nada mais descreve `ADR-0003` como decisão em aberto";
(c) o custo alegado não se sustenta: `AGENTS.md` e `docs/product/roadmap.md` **não** são gerados
e não exigem sync; só `.github/instructions/` e `.claude/agents/` exigem
`python3 scripts/sync-ai-adapters.py`, que é determinístico e já é verificado por
`scripts/audit-ai-surface.sh` (`--check` = `up-to-date`).
Correção esperada: ajustar os seis pontos acima, rodar `python3 scripts/sync-ai-adapters.py` e
reexecutar `bash scripts/audit-ai-surface.sh`.
**Fora desta correção** (áreas exclusivas de outros agentes — registrar como pendência e pedir
ticket ao `tech-lead`, não editar): `memory/agents/tech-lead.md:16`,
`memory/agents/product-analyst.md:18`, `.claude/agents/tech-lead.md:52`,
`.claude/skills/ticket/SKILL.md:51`, `.claude/workflows/feature-plan-review.js:64`.

**B2 — O ADR decide implementação: fixa o *momento* da renderização do KaTeX.**
(viola "Fora de escopo" do ticket: "decisões de implementação, não do ADR")
Evidência:
- `docs/adr/ADR-0003-platform-stack.md:111-112`: "a fórmula chega ao navegador **já renderizada**".
- `memory/context/frontend.md` (pegadinha 4): "**KaTeX pré-renderizado na build**" — enunciado
  como regra dura para todo trabalho de frontend.
- Contradiz `docs/specs/minimum-learning-slice/plan.md:134`, item 3, que lista "momento da
  renderização do KaTeX (**build × runtime**)" como decisão de implementação a tomar nos tickets;
  e `plan.md:114` trata esse mesmo item como risco de reabrir arquitetura.
O que o critério 3 pede é **KaTeX acessível**, e isso está atendido. O que sobra — quando e como
renderizar — não foi decidido por ninguém (o decisor escolheu opção C + persistência local-first)
e não é consequência necessária: ilhas hidratadas podem renderizar em runtime. Correção: manter o
requisito (fórmula em display com descrição textual; teoria legível sem JavaScript) e remover a
fixação do momento da renderização do ADR e de `frontend.md` — ou, se o produtor sustentar que é
corolário, declará-lo como tal, explicitamente, e assumir que fecha o item 3 do `plan.md`.

**B3 — Artefatos alterados e não declarados no log** (AGENTS.md §10, regra 2: "Log ou não
aconteceu"). `docs/architecture/README.md:8-12` e `docs/architecture/c4-context.md:3-6,16,37-42,48`
foram reescritos para refletir o aceite do `ADR-0003` — área exclusiva do `platform-architect`
(C4) — mas **não constam** da lista de artefatos do `[005]` nem de nenhum log dos tickets
paralelos (`grep -rn "architecture" tickets/*/log.md` = 0 ocorrências). O `qa-validator` não pode
validar o que não foi declarado.
Agravante no conteúdo desses arquivos: `c4-context.md:5` afirma "**Nada aqui é hipótese**", mas o
diagrama mantém elementos não cobertos por ADR aceito — `c4-context.md:19` ("Vercel … previews por
branch") e `:25` (`Rel(repo, vercel, "Dispara build e deploy", "CI")`) — pipeline de CI/preview não
é objeto do `ADR-0003`. Isso viola a regra que o próprio `docs/architecture/README.md:9-10` acabou
de reescrever ("elemento ainda não decidido em ADR aceito é marcado como **proposto**").
Correção: entrada `CORRECTION` declarando os arquivos (ou identificando o autor, se não foi este
ticket) e ajuste da afirmação absoluta em `c4-context.md`.

### Sugestões (não bloqueiam)

- **S1.** `ADR-0003:106-107` amarra `status: "draft"` a "fora das rotas publicadas". O nó piloto
  (`content/high-school/algebra/quadratic-equations/meta.json:18`) é bilíngue e está `draft`, e a
  spec paralela o exibe com rótulo (`docs/specs/minimum-learning-slice/spec.md:64-65` e a pergunta
  aberta em `:274`). Reescrever como "nó **sem paridade de idioma** não é publicado", sem vincular
  ao valor `draft`, evita fechar por tabela uma pergunta marcada como decisão humana.
- **S2.** `memory/context/project-context.md:19` continua dizendo "Memória | … **sem lições
  registradas além das de bootstrap**" no mesmo arquivo que este ticket atualizou — L-005 a L-008
  já existem (o próprio L-008 é deste ticket).
- **S3.** Registrar no log as pendências de área alheia listadas em B1; `[005]` não as mencionou.

### O que já está bom (não refazer)

- Critério 1 no ADR: `status: accepted`, `Data: 2026-08-01`, decisor Douglas Silva, aviso de
  bloqueio substituído por nota de desbloqueio que já delimita o que o ADR **não** decide.
- Critério 2: seção **Decisão** inequívoca (opção C + local-first sem conta) com uma linha por
  alternativa descartada (A, B, persistência 2 e 3) e motivação explícita.
- Mermaid do ADR (`:82-90`) sintaticamente válido, com leitura curta, o que o diagrama **não**
  mostra e fontes — atende `docs/DOC-STANDARDS.md`.
- Critério 3: **Consequências** cobre os sete pontos exigidos, nos três blocos do template
  (positivas / negativas / o que fica mais difícil) + portabilidade. Concreta, não genérica.
- Critério 4: seção "Restrição a preservar — independência do contrato de dados" com proibições
  explícitas e teste de conformidade verificável. Melhor parte do diff.
- `docs/adr/README.md`: edição cirúrgica, sobreviveu à inserção do `ADR-0005` por outro agente.
- `memory/context/frontend.md`: 8 regras operacionais derivadas (exceto a nº 4, ver B2).
- L-008: formato de `memory/lessons/README.md` correto, `L-008` sem colisão
  (`grep '^\*\*ID:\*\*' memory/lessons/` → L-001…L-008 únicos), indexado na seção **Sucesso** de
  `LESSONS.md` (coerente com `**Tipo:** sucesso`) e em `MEMORY.md`.
- Critério 6 reexecutado por mim: `audit-ai-surface.sh` → `Resultado: OK` (exit 0);
  `audit-content.sh` → `1 nós · 0 erros · 0 avisos` (exit 0).
- Fora de escopo respeitado no essencial: nenhum código, nenhum `package.json`, nenhuma dependência
  instalada, nenhuma biblioteca de UI/testes/service worker escolhida; `content/`, `docs/specs/` e
  os tickets TCK-0001/0002/0004 não foram tocados por este ticket.
- Critérios de aceite: [x] 1 (parcial — ver B1) · [x] 2 · [ ] 3 (ver B2) · [x] 4 · [ ] 5 (ver B1) ·
  [x] 6.

## [007] ACTION — 2026-08-01 13:40 — platform-architect
- Ação: correção dos três defeitos bloqueantes do `[006] REJECT` (loop 1/3). Defeitos aceitos
  integralmente — o argumento de "ticket separado por causa do sync" estava errado e não é
  sustentado aqui.

**B1 — desbloqueio inerte. Resolvido nos seis pontos da minha área:**
- `AGENTS.md` §1 ("Produto"): a stack deixa de ser "não fechada" e passa a descrever a decisão
  (site estático + ilhas, local-first em IndexedDB), com a fronteira dura (sem backend, conta,
  login ou telemetria identificável — cada um exige ADR novo) e o que o ADR **não** decide.
- `AGENTS.md` §11 (Regras gerais): a regra "Não assumir stack … enquanto `proposed`" virou
  "Stack decidida, fronteira dura" — o que passa a ser proibido presumir é backend/conta/
  login/telemetria. A regra vizinha "**Nenhuma implementação sem spec aprovada**" foi
  preservada literalmente, como pedido.
- `.github/instructions/core.instructions.md` item 5: mesma correção, mantendo intacta a
  primeira metade ("Nada de implementação sem spec aprovada").
- `.github/instructions/app.instructions.md` (`applyTo: src/**,app/**,api/**,tests/**,e2e/**`):
  o aviso de bloqueio foi substituído pela stack aceita e por quatro regras operacionais que
  faltavam ao código da aplicação (JS mínimo/ilhas; sem backend/conta/login/telemetria;
  gabarito no cliente; deploy estático portátil).
- `.claude/agents/platform-architect.md`: removida a cláusula "enquanto `proposed`, tratar
  stack como hipótese"; acrescentada a seção **Stack em vigor** e um limite novo — não decidir
  por ADR o que é implementação (UI, testes, service worker, KaTeX build × runtime). O item de
  contexto sobre progresso deixou de dizer "avaliar antes de assumir backend" e passou a
  refletir a decisão.
- `docs/product/roadmap.md` Fase 1: "Decidir e aceitar `ADR-0003`" deixou de ser tarefa
  pendente; stack e licença aparecem como decididas em 2026-08-01.
- `python3 scripts/sync-ai-adapters.py` executado (sem `--check`): "20 skills + 21 agents +
  6 regras → adapters sincronizados … **9 arquivo(s) escrito(s)/atualizado(s)**". Propagou para
  `.agents/rules/{core,app}.md`, `.cursor/rules/{core,app}.mdc`, `.windsurf/rules/{core,app}.md`,
  `.rules`, `.clinerules`, `.junie/guidelines.md`. Os adapters de **agent** (`.claude/commands/`,
  `.github/chatmodes/`) não mudaram por construção: embutem só o `description` do front matter
  (inalterado) e apontam para `.claude/agents/<nome>.md` — verificado com
  `grep -rln "Stack em vigor"`, que só casa no arquivo-fonte.
- Pendências de **área alheia** (não editadas, conforme B1; peço ticket ao `tech-lead`):
  `memory/agents/tech-lead.md:16`, `memory/agents/product-analyst.md:18`,
  `memory/agents/docs-writer.md:51`, `.claude/agents/tech-lead.md:52`,
  `.claude/skills/ticket/SKILL.md:51`, `.claude/workflows/feature-plan-review.js:64` — todos
  ainda descrevem o `ADR-0003` como `proposed`. As duas últimas exigem `sync-ai-adapters.py`
  depois da edição. `docs/specs/` não foi tocado (ticket paralelo).

**B2 — o ADR decidia implementação. Resolvido, sem sustentar o corolário:**
- `ADR-0003`, consequência do KaTeX: "a fórmula chega ao navegador já renderizada" foi
  substituída por requisito de **resultado** — descrição textual em toda fórmula em display,
  proibição de imagem de fórmula e ausência de custo de JavaScript desproporcional — com a
  frase explícita "**este ADR não decide *quando* a fórmula é renderizada (build × runtime)**".
- A nota de desbloqueio no topo do ADR passou a listar o momento de renderização do KaTeX
  entre as decisões de implementação que o ADR não toma.
- `memory/context/frontend.md`: regra 4 reescrita no mesmo espírito, remetendo a
  `docs/specs/minimum-learning-slice/plan.md`; o item "ainda não decididos" do estado atual
  passou a incluir build × runtime. O item 3 do `plan.md` **continua aberto** — nada foi
  fechado por este ticket.

**B3 — artefatos não declarados. Resolvido:**
- Declaro agora, como autor: `docs/architecture/README.md` (linhas 8–12) e
  `docs/architecture/c4-context.md` (estado, `System_Ext` da Vercel, `Rel` de CI, leitura e
  fontes) foram alterados por **mim**, nesta cadeia, no `[004]`, e omitidos da lista de
  artefatos do `[005]`. Omissão minha, não de ticket paralelo.
- Contradição apontada resolvida: a afirmação absoluta "Nada aqui é hipótese" saiu.
  `c4-context.md` agora separa o que decorre de ADR aceito do que **continua proposto** —
  pipeline de CI/CD e previews por branch, marcados como `PROPOSTO` no próprio diagrama
  (rótulo do `System_Ext` e do `Rel`), com parágrafo "Estado atual × proposta" exigido por
  `docs/DOC-STANDARDS.md`. O estado na tabela do `docs/architecture/README.md` acompanha.

**Sugestões acatadas:**
- S1: a consequência sobre rotas por idioma deixou de amarrar `status: "draft"` a "fora das
  rotas publicadas". Agora afirma só o que o ADR-0002 impõe ("nó **sem paridade de idioma**
  não é publicado") e declara que o tratamento de nó bilíngue em `draft` é decisão de produto
  em aberto — não fechada aqui.
- S2: `memory/context/project-context.md` não diz mais "sem lições registradas além das de
  bootstrap".
- S3: pendências de área alheia registradas acima.

- Evidência:
  - `python3 scripts/sync-ai-adapters.py` → "9 arquivo(s) escrito(s)/atualizado(s)", exit 0.
  - `python3 scripts/sync-ai-adapters.py --check` → exit 0.
  - `bash scripts/audit-ai-surface.sh` → `Resultado: OK`, exit 0 (`up-to-date`; todas as regras
    dentro do limite de 12.000 caracteres, inclusive `core` e `app` que cresceram).
  - `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos`, exit 0.
  - `grep -rn "ADR-0003" … | grep -iE "proposed|hipótese|em aberto|pendente"` → só restam as
    ocorrências de área alheia listadas em B1 e `docs/specs/` (fora deste ticket).
- Lição: **L-010** (`accepting-an-adr-means-updating-the-rules-agents-read`) para B1 e
  **L-011** (`adr-decides-constraints-not-implementation-timing`) para B2, ambas indexadas em
  `memory/LESSONS.md` (seção **Erro**) e `memory/MEMORY.md`. B3 não gerou lição nova: é
  descumprimento direto de regra já escrita (AGENTS.md §10, regra 2 — "log ou não aconteceu"),
  erro pontual de disciplina, não conhecimento novo; a prevenção virou item do checklist na
  minha memória de agente.
- Resultado: ok — B1, B2 e B3 corrigidos; critérios 1, 3 e 5 refeitos.

## [008] HANDOFF — 2026-08-01 13:40
- De: platform-architect → Para: code-reviewer
- Status novo: in_review
- O que foi feito: correção dos três defeitos bloqueantes do `[006]` + S1, S2 e S3.
- Artefatos (lista completa desta cadeia, incluindo os omitidos no `[005]`):
  - `docs/adr/ADR-0003-platform-stack.md`
  - `docs/adr/README.md`
  - `docs/architecture/README.md` · `docs/architecture/c4-context.md` (declarados em B3)
  - `AGENTS.md` (§1 e §11) · `docs/product/roadmap.md`
  - `.github/instructions/core.instructions.md` · `.github/instructions/app.instructions.md`
  - `.claude/agents/platform-architect.md`
  - Gerados por `sync-ai-adapters.py` (não editados à mão): `.agents/rules/{core,app}.md`,
    `.cursor/rules/{core,app}.mdc`, `.windsurf/rules/{core,app}.md`, `.rules`, `.clinerules`,
    `.junie/guidelines.md`
  - `memory/context/project-context.md` · `memory/context/frontend.md`
  - `memory/lessons/client-side-answer-key-is-a-product-constraint.md` (L-008),
    `memory/lessons/accepting-an-adr-means-updating-the-rules-agents-read.md` (L-010),
    `memory/lessons/adr-decides-constraints-not-implementation-timing.md` (L-011)
  - `memory/LESSONS.md` · `memory/MEMORY.md` · `memory/agents/platform-architect.md`
- Como validar (critérios 1–6 + defeitos):
  1. `ADR-0003` `accepted`, decisor e data corretos, nota de desbloqueio no lugar do aviso.
  2. **Decisão** inequívoca (opção C + local-first) com uma linha por alternativa descartada.
  3. **Consequências** cobrem os sete pontos **sem** fixar o momento de renderização do KaTeX
     (B2): conferir que ADR e `frontend.md` falam de resultado, e que `plan.md:134` segue aberto.
  4. Restrição de independência do contrato de dados de `content/` intacta.
  5. B1: `grep -rn "ADR-0003" AGENTS.md docs/ memory/ .claude/ .github/ | grep -i proposed` deve
     retornar apenas as pendências de área alheia listadas no `[007]` e `docs/specs/`. Conferir
     também que "Nenhuma implementação sem spec aprovada" continua em `AGENTS.md` §11 e no item
     5 de `core.instructions.md`.
  6. `python3 scripts/sync-ai-adapters.py --check`, `bash scripts/audit-ai-surface.sh` e
     `bash scripts/audit-content.sh` — os três em exit 0.
  - B3: `docs/architecture/*` declarados acima; `c4-context.md` sem afirmação absoluta e com
    CI/previews marcados como `PROPOSTO`.
  - Continua valendo o que **não** foi feito: nenhum código, `package.json`, dependência ou
    escolha de biblioteca; `content/`, `docs/specs/`, `LICENSE*`, `ADR-0005` e os tickets
    TCK-0001/0002/0004 intocados; `docs/adr/README.md` só na linha do `ADR-0003`.
- Pendências e riscos:
  - Seis pontos de área alheia ainda dizem `proposed` (lista no `[007]`) — precisam de ticket
    do `tech-lead`; dois deles (`.claude/skills/ticket/SKILL.md`,
    `.claude/workflows/feature-plan-review.js`) exigem novo `sync-ai-adapters.py`.
  - `AGENTS.md` e as regras `core`/`app` cresceram; o limite de 12.000 caracteres por regra
    está atendido hoje, mas fica mais apertado para a próxima adição.
  - Nível **Container** do C4 (build, ilhas, service worker, IndexedDB) e ADR de CI/CD seguem
    não escritos — ambos merecem ticket próprio.
  - `L-010`/`L-011` conferidos contra colisão (`grep '^\*\*ID:\*\*' memory/lessons/` → L-001…
    L-011 únicos), mas outros tickets escrevem no mesmo working tree; reconferir no review.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 (a confirmar pela cadeia
  de revisão/validação).

## [009] CORRECTION — 2026-08-01 13:55 — platform-architect
- Corrige: a lista de ocorrências do defeito **B1** no `[007]` e a lista de artefatos do
  `[008]` — ambas estavam **incompletas**.
- Por que entrada nova e não edição do `[007]`: o log é append-only (AGENTS.md §10, regra 2 —
  "corrigir registro anterior = nova entrada `CORRECTION`, nunca edição"), e o `[007]`/`[008]`
  já estavam publicados quando a ocorrência chegou. O pedido do coordenador ("citar
  explicitamente no `[007]`") é atendido aqui por referência cruzada, sem reescrever histórico.
- Origem: revisor do `TCK-0004` encontrou a ocorrência; ela **não** constava do `[006] REJECT`
  e pertence a este ticket.
- Ocorrência adicional de B1: `README.md:7-10` — a nota de estado do repositório ainda dizia
  "a stack está em avaliação … (`proposed`)". Corrigida: agora afirma stack **decidida**
  (`accepted`, 2026-08-01), com a síntese da decisão (site estático com ilhas, progresso
  local-first em IndexedDB, deploy estático, sem backend e sem conta). `grep -n "ADR-0003"
  README.md` não retorna mais nenhuma menção a `proposed`.
- Escopo respeitado, conforme aviso de concorrência: a edição no `README.md` ficou **restrita
  às linhas 7-10** (estado/`ADR-0003`); a seção **Licença** do `README.md` é do `docs-writer#2`
  (TCK-0004) e não foi tocada, assim como `AGENTS.md` §9.6/§9.7 e
  `.github/instructions/content.instructions.md`.
- Artefato a somar ao `[008]`: `README.md`.
- Evidência após a correção: `python3 scripts/sync-ai-adapters.py --check` → exit 0;
  `bash scripts/audit-ai-surface.sh` → exit 0; `bash scripts/audit-content.sh` → exit 0.
  Nenhum novo `sync-ai-adapters.py` de escrita foi necessário: `README.md` não é fonte
  canônica nem arquivo gerado. O working tree fica livre para o `docs-writer#2` rodar o sync
  dele em seguida.
- Lição: **L-010** — é exatamente a falha que ela descreve (propagação incompleta do aceite).
  O `grep` de verificação prescrito na lição cobria `AGENTS.md docs/ memory/ .claude/ .github/`
  e **não incluía a raiz do repositório**, por isso o `README.md` escapou nas duas passagens.
  Lição atualizada para exigir o `README.md` e a raiz no comando de verificação.
- Ocorrência adicional encontrada pela varredura corrigida (`grep -rn "ADR-0003" .
  --exclude-dir=.git`), não apontada por ninguém: `prompts/bootstrap-session.md:31` — regra 5
  do prompt de bootstrap das ferramentas web (ChatGPT, Grok, Claude web) ainda dizia "a stack
  ainda não está decidida". Mesma classe do `AGENTS.md`: é instrução de sessão, não memória de
  agente nem arquivo gerado (sem marcador `managed-by`). Corrigida no mesmo espírito — stack
  decidida + fronteira dura de backend/conta/login/telemetria. A regra "nenhuma implementação
  sem spec aprovada", que abre o mesmo item, foi preservada.
- Não corrigido de propósito: `.dev-loop/**` (estado efêmero de dev-loops encerrados,
  gitignorado — `.gitignore:17`) e as seis pendências de área alheia já listadas no `[007]`.
- Artefatos a somar ao `[008]`: `README.md`, `prompts/bootstrap-session.md`.
- Status: inalterado (`in_review`, owner `code-reviewer`); o handoff `[008]` permanece válido.

## [010] REJECT — 2026-08-01 14:10
- De: code-reviewer → Para: platform-architect · Loop nº: 2/3
- Status novo: in_progress
- Aviso: **próxima devolução no mesmo par esgota o limite de 3 loops** (AGENTS.md §10, regra 6)
  e vai para o `tech-lead`. O defeito abaixo é único e de uma linha; o resto está verificado e
  aprovado — não refazer nada além dele.
- Comandos usados nesta passagem (nenhum aceito de segunda mão):
  - `grep -rn "ADR-0003" . --exclude-dir=.git | grep -iE "proposed|hipótese|em aberto|pendente|não decidid|não está|em avaliação|aguarda"`
  - `grep -rniE "stack ainda|não assumir stack|não está fechada|stack não está decidida" . --exclude-dir=.git`
  - `grep -rn "spec aprovada" AGENTS.md .github/instructions/*.md prompts/bootstrap-session.md .agents/rules/core.md .cursor/rules/core.mdc .windsurf/rules/core.md .rules .clinerules .junie/guidelines.md`
  - `grep -rn "renderiz" docs/adr/ADR-0003-platform-stack.md memory/context/frontend.md AGENTS.md .github/instructions/app.instructions.md .claude/agents/platform-architect.md`
  - `grep -rn '^\*\*ID:\*\*|^\*\*Tipo:\*\*' memory/lessons/*.md`; `grep -n "^## |^- \[L-" memory/LESSONS.md`
  - `git diff --no-color` de `AGENTS.md`, `README.md`, `prompts/bootstrap-session.md`,
    `docs/product/roadmap.md`, `.github/instructions/{core,app}.instructions.md`,
    `.claude/agents/platform-architect.md`, `docs/adr/ADR-0003-platform-stack.md`,
    `docs/architecture/*`, `memory/context/*`, `memory/agents/platform-architect.md`
    e dos 9 gerados (`.agents/`, `.cursor/`, `.windsurf/`, `.rules`, `.clinerules`, `.junie/`)
  - `python3 scripts/sync-ai-adapters.py --check` → "Tudo já estava atualizado", exit 0
  - `bash scripts/audit-ai-surface.sh` → `Resultado: OK` · `up-to-date` · regras dentro do limite
  - `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`, exit 0

### Defeito bloqueante

**B4 — o diagrama do próprio ADR ainda decide o que o texto acaba de declarar não decidido.**
Evidência: `docs/adr/ADR-0003-platform-stack.md:86`
`B --> H["HTML por idioma<br/>/pt-BR/… · /en-US/…<br/>KaTeX pré-renderizado"]`
contra `:12` ("o que este ADR não decide … **momento de renderização do KaTeX — build ×
runtime**") e `:116` ("**Este ADR não decide *quando* a fórmula é renderizada**"), e contra
`memory/context/frontend.md:37`.
Critério violado: critério 3 do ticket + "Fora de escopo" ("decisões de implementação, não do
ADR"), e **AGENTS.md §10, regra 7** — é a repetição do erro que acabou de virar lição nesta
mesma entrega: `memory/lessons/adr-decides-constraints-not-implementation-timing.md` (L-011)
diz, textualmente, "não como mecanismo (**'pré-renderizado na build'**)". O `docs/DOC-STANDARDS.md`
trata o Mermaid como parte normativa do documento: quem lê o diagrama recebe a restrição errada,
e o `frontend-developer` não tem como saber qual das duas afirmações vale.
Correção esperada: trocar o rótulo do nó `H` por algo que descreva só o que está decidido
(ex.: "HTML por idioma · /pt-BR/… · /en-US/… · matemática acessível") e conferir se a
**Leitura** logo abaixo (`:93-96`) continua coerente. Nada mais neste arquivo precisa mudar.

### Sugestões (não bloqueiam)

- **S4.** `ADR-0003:122-124` (negativa do progresso local): "a aplicação **deve** … prever
  export/import local do progresso" prescreve uma funcionalidade de produto dentro de um ADR de
  stack — escopo de spec/`product-analyst`. Reescrever como restrição ("a perda de progresso
  precisa ser explícita ao aluno e recuperável sem servidor") ou remeter a ticket próprio.
- **S5.** `[009]` cumpre o append-only (AGENTS.md §10 regra 2 e `docs/ai/ticket-protocol.md:181`
  mandam exatamente `CORRECTION` em vez de editar o `[007]`) e **não** deixou o registro
  ambíguo: cita `[007]` e `[008]`, nomeia origem, arquivos e evidência. Só não usa os rótulos
  literais do template (`docs/ai/ticket-protocol.md:173-177`: "O que estava errado:" /
  "Registro correto:"). Ajustar o formato nas próximas correções.

### Verificado e aprovado nesta passagem (não refazer)

- **B1 — resolvido, e a varredura confere.** `AGENTS.md:36-43` (§1) e `:423-426` (§11),
  `.github/instructions/core.instructions.md:32-35`, `.github/instructions/app.instructions.md:6-19`,
  `.claude/agents/platform-architect.md:16-18,35-42,44-50`, `docs/product/roadmap.md:29-31`,
  `README.md:7-10` e `prompts/bootstrap-session.md:30-32` descrevem a stack como decidida com a
  fronteira dura. A varredura da raiz que eu mesmo rodei não encontra mais nenhuma ocorrência
  fora de: `.dev-loop/**` (gitignorado, `.gitignore:17`), logs de ticket (histórico append-only),
  `docs/specs/` (TCK-0002) e as seis pendências de área alheia — que **confirmo serem de outros
  donos**: `memory/agents/{tech-lead:16,product-analyst:18,docs-writer:51}.md` (AGENTS.md §5: cada
  agente mantém a própria memória), `.claude/agents/tech-lead.md:52`, `.claude/skills/ticket/SKILL.md:51`
  e `.claude/workflows/feature-plan-review.js:64` (papel e ferramental do `tech-lead`). Nenhuma
  delas é do `platform-architect`.
- **Regra "nenhuma implementação sem spec aprovada" intacta** nos 4 pontos editados e nos 7
  gerados (`AGENTS.md:221,424`, `core.instructions.md:32`, `app.instructions.md:11`,
  `bootstrap-session.md:30`, `.agents/rules/core.md:31`, `.cursor/rules/core.mdc:35`,
  `.windsurf/rules/core.md:34`, `.rules:31`, `.clinerules:31`, `.junie/guidelines.md:31`).
- **Sync sem deriva:** os 9 gerados (`.agents/rules/{core,app}`, `.cursor/rules/{core,app}`,
  `.windsurf/rules/{core,app}`, `.rules`, `.clinerules`, `.junie/guidelines.md`) reproduzem
  literalmente o texto das fontes — comparei os diffs lado a lado; nenhum afirma nada que a
  fonte não diga. `--check` limpo e `audit-ai-surface.sh` `OK`.
- **B2 — resolvido no texto:** `ADR-0003:12` e `:113-117` e `frontend.md:15-18,34-39` exigem
  resultado (descrição textual, imagem de fórmula proibida, sem custo de JS desproporcional) e
  declaram build × runtime em aberto; `docs/specs/minimum-learning-slice/plan.md:134` item 3
  continua aberto, não foi fechado por este ticket. Falta só o rótulo do diagrama (B4).
- **B3 — resolvido e consistente nos cinco pontos:** autoria declarada no `[007]`; artefatos no
  `[008]`; "Nada aqui é hipótese" removido (`c4-context.md:3-7`); `PROPOSTO` no `System_Ext` da
  Vercel (`:20`) e no `Rel` de CI (`:26`); parágrafo "Estado atual × proposta" (`:45-48`); e a
  tabela de `docs/architecture/README.md:8` acompanha, sem contradizer a regra permanente de
  `:10-12`.
- **S1 acatada** (`ADR-0003:105-108`: "nó **sem paridade de idioma** não é publicado", e o
  tratamento de nó bilíngue em `draft` declarado como decisão de produto em aberto — coerente com
  `ADR-0002:34-36` e sem fechar a pergunta de `docs/specs/minimum-learning-slice/spec.md:274`).
  **S2 acatada** (`memory/context/project-context.md:19`). **S3 acatada** (`[007]`, lista nominal).
- **Lições:** `Lição:` presente ao fim do `[007]` com L-010 e L-011, e o `n/a` de B3 é
  **justificado e aceito** — não havia lição prévia sobre declarar artefato no log, então não é
  repetição (regra 7), e a prevenção virou item verificável em
  `memory/agents/platform-architect.md`. IDs sem colisão: `L-001…L-011` únicos, incluindo o
  `L-009` criado em paralelo pelo TCK-0004. Tipos batem com a seção do índice (L-010 e L-011 são
  `**Tipo:** erro` e estão em `## Erro` de `memory/LESSONS.md:40,43`), ambas em `MEMORY.md:53,56`.
  L-010 foi de fato atualizada para exigir a varredura a partir da raiz (`:16-19`).
- **Escopo:** nenhum código, `package.json`, dependência ou biblioteca. `content/` (TCK-0005,
  `theory.*.md`), `docs/specs/` (TCK-0002), `LICENSE*`/`ADR-0005`/seção Licença do `README.md`
  (TCK-0004) e `AGENTS.md` §9.6/§9.7 não foram tocados por esta cadeia.
- Critérios de aceite: [x] 1 · [x] 2 · [ ] 3 (só por B4) · [x] 4 · [x] 5 · [x] 6.

## [011] ACTION — 2026-08-01 14:25 — platform-architect
- Ação: correção do defeito único **B4** (loop 2/3). Escopo estritamente limitado ao
  `docs/adr/ADR-0003-platform-stack.md`, como instruído — nada do que já foi verificado e
  aprovado foi refeito, e **não** rodei `sync-ai-adapters.py` (trabalho paralelo do
  `docs-writer#2`).

**B4 — resolvido.**
- `:86`, rótulo do nó `H`: `KaTeX pré-renderizado` → `matemática acessível`. O nó passa a
  descrever o resultado exigido ("HTML por idioma · /pt-BR/… · /en-US/… · matemática
  acessível"), coerente com `:12` e `:119`.
- **Varredura da classe do defeito no arquivo inteiro** (`grep -n "renderiz\|service worker"`),
  em vez de corrigir só a linha citada. Achei uma segunda ocorrência do mesmo tipo, não
  apontada no `[010]`: o nó `S` dizia `Service worker / cache do visitado` — mecanismo que o
  próprio `:11` lista entre as decisões que o ADR **não** toma (estratégia de service worker).
  Trocado por `Conteúdo visitado disponível offline`, que é o que está decidido. Declaro a
  edição explicitamente por sair da letra do `[010]` ("nada mais neste arquivo"): é a mesma
  classe do B4, no mesmo diagrama, e deixá-la seria oferecer o próximo `REJECT`; se o revisor
  discordar, o rollback é de uma linha.
- Demais ocorrências de "renderiz" no arquivo conferidas uma a uma e mantidas: `:19`
  (requisito de contexto), `:30`, `:39`, `:75` (descrição das alternativas A e B) e `:64`
  ("SEO nativo do HTML pré-renderizado" — pré-renderização **das páginas** é a decisão da
  opção C, não o momento de renderização da fórmula).
- **Leitura** do diagrama (`:93-99`) revista, como pedido: não repetia o mecanismo, mas era
  omissa. Agora declara que o diagrama mostra "só resultados exigidos, nenhum mecanismo" e que
  não decide *como* cada caixa é obtida — nominalmente o momento de renderização da matemática
  (build × runtime) e a estratégia de disponibilidade offline.

**S4 — acatada.** `:123-125` deixou de prescrever funcionalidade ("a aplicação deve … prever
export/import local do progresso"). Passou a restrição verificável — "a perda de progresso
precisa ser explícita ao aluno e recuperável sem servidor" — com a mitigação concreta
(export/import de arquivo, aviso na interface ou outra) declarada como decisão de produto em
spec própria. Concordo com o revisor: era prescrição de spec dentro de ADR de stack, mesma
família do B2.

**S5 — acatada para as próximas.** O `[009]` fica como está (append-only). Da próxima
`CORRECTION` em diante uso os rótulos literais de `docs/ai/ticket-protocol.md:173-177`
(`Corrige:` / `O que estava errado:` / `Registro correto:`); item anotado em
`memory/agents/platform-architect.md`.

- Evidência:
  - `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos`, exit 0.
  - `bash scripts/audit-ai-surface.sh` → **`Resultado: FALHAS ENCONTRADAS`, exit 1**, por
    `OUTDATED` em `sync-ai-adapters.py --check`. **A causa não é esta correção** e não é minha:
    são `.cursor/rules/content.mdc`, `.windsurf/rules/content.md`, `.agents/rules/content.md`,
    `.cursor/rules/core.mdc`, `.windsurf/rules/core.md`, `.agents/rules/core.md`, `.rules`,
    `.clinerules` e `.junie/guidelines.md`, desatualizados pelas edições **em andamento** do
    `docs-writer#2` (TCK-0004) em `.github/instructions/content.instructions.md` e no item 9 de
    `.github/instructions/core.instructions.md` (texto de licença do `ADR-0005`).
    Prova: `grep -c accepted` = 1 em **todos** os nove gerados (meu texto de stack já está lá,
    sincronizado no `[007]`) e `grep -c "ADR-0005"` = 0 em todos, contra 1 na fonte
    `core.instructions.md` — o delta pendente é inteiramente o da licença. Meu diff desta
    rodada não toca em nenhuma fonte canônica: só `docs/adr/`, `memory/` e este log.
    Conforme instruído, **não rodei o sync**; ele cabe ao `docs-writer#2` ao fechar o TCK-0004.
    A auditoria deve voltar a `OK` depois disso — reexecutar antes do `done`.
- Lição: **L-013** (`fixing-the-cited-line-is-not-fixing-the-defect-class`), lição **nova**, não
  repetição da L-011. Reflexão honesta sobre a causa raiz, porque a distinção importa: a L-011
  descreve *o que* não escrever num ADR, e eu não voltei a cometer o erro de julgamento — o
  rótulo do Mermaid era **texto pré-existente do `[004]` que sobreviveu à correção**. O que
  falhou foi o **método de correção**: tratei o `REJECT` como inventário e corrigi as duas
  linhas citadas, sem varrer o artefato pelo termo do defeito. Um `grep -n "renderiz"` no
  próprio arquivo teria custado segundos e pego a linha 86. É a mesma causa raiz do
  `[009]`/L-010 (varredura restrita ao que já se sabe, em vez de varredura exaustiva),
  agravada por um viés específico: revisei prosa e não revisei **diagrama**, que o
  `docs/DOC-STANDARDS.md` trata como parte normativa. Índices `memory/LESSONS.md` (seção
  **Erro**) e `memory/MEMORY.md` atualizados; ID conferido sem colisão (`L-012` foi criado em
  paralelo por outro ticket, então esta é `L-013`).
- Resultado: ok — B4 corrigido, classe do defeito varrida, S4 e S5 acatadas.

## [012] HANDOFF — 2026-08-01 14:25
- De: platform-architect → Para: code-reviewer
- Status novo: in_review
- O que foi feito: B4 (rótulo do nó `H`) + a segunda ocorrência da mesma classe (nó `S`) +
  leitura do diagrama + S4 + S5. Nada além disso.
- Artefatos desta rodada:
  - `docs/adr/ADR-0003-platform-stack.md` (diagrama `:86,89`, leitura `:93-99`, negativa
    `:123-125`)
  - `memory/lessons/fixing-the-cited-line-is-not-fixing-the-defect-class.md` (L-013)
  - `memory/LESSONS.md` · `memory/MEMORY.md` · `memory/agents/platform-architect.md`
  - este `log.md` e o front matter do `ticket.md`
  (A lista acumulada da cadeia continua nos `[008]` e `[009]`.)
- Como validar:
  1. `grep -n "renderiz\|service worker" docs/adr/ADR-0003-platform-stack.md` — nenhuma
     ocorrência dentro do bloco ```mermaid``` (`:83-91`); as que restam são contexto,
     descrição das alternativas A/B ou a negação explícita em `:12` e `:119`.
  2. Diagrama e texto coerentes: `:12`, `:86`, `:89`, `:93-99` e `:119` dizem a mesma coisa.
  3. S4: `:123-125` afirma restrição verificável, não funcionalidade; a mitigação está
     remetida a spec.
  4. `bash scripts/audit-content.sh` → exit 0.
  5. `bash scripts/audit-ai-surface.sh` → hoje **exit 1** por sync pendente do TCK-0004;
     conferir pelo teste de atribuição descrito no `[011]` (`grep -c accepted` = 1 e
     `grep -c ADR-0005` = 0 nos nove gerados) que a deriva não vem desta cadeia. Reexecutar
     depois que o `docs-writer#2` rodar `python3 scripts/sync-ai-adapters.py`.
- Pendências e riscos:
  - **Bloqueio externo ao ticket:** `audit-ai-surface.sh` só volta a `OK` após o sync do
    `docs-writer#2`. Não é motivo de `REJECT` desta cadeia, mas o `qa-validator` não deveria
    marcar `done` com a auditoria vermelha — sugiro sincronizar o fechamento dos dois tickets.
  - Se o revisor discordar da edição do nó `S` (fora da letra do `[010]`), o rollback é de uma
    linha e não afeta B4.
  - Seguem valendo as pendências já registradas: seis pontos de área alheia com `ADR-0003
    proposed` (ticket ao `tech-lead`), C4 nível **Container** e ADR de CI/CD não escritos.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 (critério 6 com a ressalva
  de atribuição acima).

## [013] CORRECTION — 2026-08-01 14:35 — platform-architect
- Corrige: [011] (bloco "Evidência") e [012] (item 5 de "Como validar" e primeira pendência).
- O que estava errado: registrei `bash scripts/audit-ai-surface.sh` → `FALHAS ENCONTRADAS`,
  exit 1, com a ressalva de que a deriva vinha do sync pendente do `docs-writer#2` e de que a
  auditoria só voltaria a `OK` depois que ele rodasse `sync-ai-adapters.py`. O diagnóstico
  estava certo, mas o **resultado registrado ficou obsoleto minutos depois**: o sync do
  TCK-0004 entrou no working tree e o critério 6 deixou de ter ressalva. Deixar o `[012]` com
  "hoje exit 1" induziria o `code-reviewer` a validar um estado que não existe mais.
- Registro correto: reexecutados agora, os três comandos passam —
  `python3 scripts/sync-ai-adapters.py --check` → "Tudo já estava atualizado", exit 0;
  `bash scripts/audit-ai-surface.sh` → `Resultado: OK`, exit 0;
  `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`, exit 0.
  Confirmação de que a deriva era mesmo do TCK-0004 e foi ele quem a fechou:
  `grep -c "ADR-0005"` passou de 0 para 1 em `.rules`, `.clinerules` e `.cursor/rules/core.mdc`
  — o texto de licença chegou aos gerados sem que eu rodasse o sync, como instruído.
  **Critério 6 verde, sem ressalva.** A pendência "auditoria vermelha bloqueia o `done`",
  registrada no `[012]`, está **resolvida**; o `qa-validator` não precisa mais sincronizar o
  fechamento com o TCK-0004.
- Formato: esta entrada já usa os rótulos literais de `docs/ai/ticket-protocol.md:173-177`,
  conforme S5 do `[010]`.
- Status: inalterado (`in_review`, owner `code-reviewer`); o handoff `[012]` permanece válido.

## [014] HANDOFF — 2026-08-01 14:50
- De: code-reviewer → Para: qa-validator
- Status novo: in_validation
- O que foi feito: revisão do diff aprovada no loop 3/3 sem defeito bloqueante. B4 resolvido e,
  além dele, a segunda ocorrência da mesma classe encontrada e corrigida pelo próprio produtor.
  S4 e S5 acatadas. Os defeitos B1, B2 e B3 (loops 1 e 2) seguem resolvidos e reconferidos.
- Artefatos (cadeia completa — `[008]`, `[009]` e `[012]`):
  - `docs/adr/ADR-0003-platform-stack.md` (principal) · `docs/adr/README.md`
  - `docs/architecture/README.md` · `docs/architecture/c4-context.md`
  - `AGENTS.md` (§1 e §11) · `README.md` (linhas 7-10) · `prompts/bootstrap-session.md`
  - `docs/product/roadmap.md` · `.github/instructions/{core,app}.instructions.md`
  - `.claude/agents/platform-architect.md` + 9 gerados por `sync-ai-adapters.py`
    (`.agents/rules/{core,app}`, `.cursor/rules/{core,app}`, `.windsurf/rules/{core,app}`,
    `.rules`, `.clinerules`, `.junie/guidelines.md`)
  - `memory/context/{project-context,frontend}.md`
  - `memory/lessons/{client-side-answer-key-is-a-product-constraint (L-008),
    accepting-an-adr-means-updating-the-rules-agents-read (L-010),
    adr-decides-constraints-not-implementation-timing (L-011),
    fixing-the-cited-line-is-not-fixing-the-defect-class (L-013)}.md`
  - `memory/LESSONS.md` · `memory/MEMORY.md` · `memory/agents/platform-architect.md`

### O que verifiquei nesta passagem (reexecutado, não aceito do log)

- **B4 resolvido.** `docs/adr/ADR-0003-platform-stack.md:86` agora é
  `H["HTML por idioma<br/>/pt-BR/… · /en-US/…<br/>matemática acessível"]`.
  `grep -n "renderiz\|service worker" docs/adr/ADR-0003-platform-stack.md` → **nenhuma
  ocorrência dentro do bloco Mermaid (`:83-91`)**.
- **Concordo com a edição extra do nó `S`** (`:89`, `Service worker / cache do visitado` →
  `Conteúdo visitado disponível offline`) e ela **não perde informação necessária**: a
  estratégia de service worker já constava em `:11` entre as não-decisões, e o requisito de
  offline continua explícito em `:21` (contexto) e `:113` (consequência positiva). Sair da letra
  do meu "nada mais neste arquivo" foi correto e está declarado no `[011]` — era a mesma classe
  do defeito, no mesmo diagrama; corrigir só a linha citada é exatamente o que a L-013 combate.
- **Distinção de `:64` confirmada por leitura própria.** "SEO nativo do **HTML** pré-renderizado"
  fala da **página**, que é a decisão da opção C (`:41-45`, `:56-61`); o que o ADR não decide é
  o momento de renderização da **fórmula** (`:12`, `:119`). São coisas distintas: uma página
  estática pode ter a matemática renderizada na build ou dentro de uma ilha em runtime — as duas
  cabem sob a restrição de `:116-120`. As demais ocorrências (`:19` requisito de contexto; `:30`,
  `:39`, `:75` descrição das alternativas A e B) são legítimas.
- **Leitura do diagrama (`:92-99`) não reintroduz mecanismo.** "vira HTML por idioma na build" é
  a decisão, não um mecanismo em aberto; e o parágrafo passou a negar nominalmente as duas
  não-decisões (momento de renderização da matemática e estratégia de offline).
- **S4 continua sendo ADR, não spec disfarçada** (`:126-130`): afirma restrição derivada da
  decisão ("a perda de progresso precisa ser explícita ao aluno e recuperável sem servidor") e
  remete a escolha da mitigação a spec própria. Não nomeia funcionalidade nem tela.
- **S5 acatada:** o `[013]` usa os rótulos literais de `docs/ai/ticket-protocol.md:173-177`.
- **Critério 6 verde, sem ressalva, reexecutado por mim agora:**
  `python3 scripts/sync-ai-adapters.py --check` → "Tudo já estava atualizado", exit 0;
  `bash scripts/audit-ai-surface.sh` → `Resultado: OK` · `up-to-date`, exit 0;
  `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`, exit 0.
  O `[013]` estava certo: a deriva do `[011]` era do TCK-0004 e foi fechada por ele.
- **B1 reconferido depois das edições paralelas** (`grep -rn "ADR-0003" . --exclude-dir=.git |
  grep -iE "proposed|hipótese|em aberto|pendente|não decidid|não está|em avaliação"`, excluindo
  `.dev-loop/` e `tickets/`): nenhuma ocorrência na área do produtor. B2 e B3 intactos
  (`memory/context/frontend.md:34-39`; `docs/architecture/c4-context.md:3-7,20,26,45-48` e
  `docs/architecture/README.md:8`). Estrutura do ADR completa contra `docs/adr/adr-template.md`.

### Julgamento explícito sobre a L-013 (pedido do coordenador)

**O enquadramento se sustenta; não é racionalização, e não é repetição da L-011 sob a regra 7
(AGENTS.md §10).** Três razões verificáveis:
1. **Cronologia.** O rótulo `KaTeX pré-renderizado` foi escrito no `[004]`, **antes** de a L-011
   existir. Regra 7 pune *repetir* erro com lição já registrada; aqui não houve nova ocorrência
   escrita depois da lição — houve uma ocorrência antiga que sobreviveu a uma correção parcial.
2. **Evidência independente do log dele:** no meu próprio `[006]` eu aprovei esse Mermaid
   ("sintaticamente válido, com leitura curta … atende `docs/DOC-STANDARDS.md`") com o rótulo
   já lá. O texto era pré-existente — isso é fato registrado, não versão do produtor.
3. **Conteúdo distinto.** L-011 é sobre *o que* não escrever num ADR (resultado × mecanismo);
   L-013 é sobre *método de correção* (extrair um termo de busca do `REJECT` e varrer o
   artefato; diagrama, tabela e rótulo entram na revisão com o mesmo peso da prosa). O "Como
   aplicar" é executável e não duplica o da L-011; e a lição referencia L-010 e L-011 em vez de
   reescrevê-las, como manda `memory/LESSONS.md:21`.
   Registro que a sanção pela ocorrência já foi aplicada — foi o `[010] REJECT`, que invocou a
   regra 7 explicitamente. Cobrá-la de novo seria punir duas vezes o mesmo defeito.
- **Sem colisão de ID:** `L-001…L-014` únicos (`grep '^\*\*ID:\*\*' memory/lessons/ | sort | uniq -d`
  → vazio), incluindo `L-012` (TCK-0005) e `L-014` criados em paralelo. L-013 é `**Tipo:** erro`
  e está na seção `## Erro` de `memory/LESSONS.md:51` e em `memory/MEMORY.md:62`.

### Sugestões (não bloqueiam, para o autor considerar depois)

- **S6.** `ADR-0003:95` diz que o diagrama traz "só resultados exigidos, **nenhum mecanismo**",
  mas `IndexedDB` (`:88`) e `Vercel` (`:90`) são mecanismos — decididos, e por isso legítimos no
  diagrama. Precisão: "nenhum mecanismo **não decidido**". Não muda nenhuma restrição.
- **S7.** Surgiu uma **sétima** ocorrência de área alheia depois da varredura do `[011]`:
  `memory/agents/a11y-ux-reviewer.md:56` ("depende de ADR-0003 (`proposed`)"), escrita por
  cadeia paralela. Somar à lista do ticket a pedir ao `tech-lead`, junto de
  `memory/agents/{tech-lead:16,product-analyst:18,docs-writer:63}.md`,
  `.claude/agents/tech-lead.md:52`, `.claude/skills/ticket/SKILL.md:51` e
  `.claude/workflows/feature-plan-review.js:64`. Nenhuma é do `platform-architect`.

### Como validar (para o `qa-validator`)

1. Critério 1 — `docs/adr/ADR-0003-platform-stack.md:3-13`.
2. Critério 2 — `:55-81` (decisão + 4 alternativas descartadas).
3. Critério 3 — `:102-146`: JS mínimo/ilhas, rotas por idioma com paridade, PWA offline-first,
   KaTeX acessível, backend/conta/login/telemetria só com ADR novo, gabarito no cliente,
   deploy estático portátil. Conferir que nenhum item fixa mecanismo.
4. Critério 4 — seção "Restrição a preservar — independência do contrato de dados" (`:152-169`),
   com teste de conformidade.
5. Critério 5 — `grep -rn "ADR-0003" . --exclude-dir=.git | grep -i proposed`: só devem restar
   `.dev-loop/` (gitignorado), logs de ticket, `docs/specs/` (TCK-0002) e as sete pendências de
   área alheia da S7.
6. Critério 6 — os três comandos acima, todos exit 0.

- Pendências e riscos:
  - Sete pontos de área alheia ainda dizem `ADR-0003 proposed` (S7) — **não** bloqueiam este
    ticket (fora do escopo do produtor); precisam de ticket do `tech-lead`.
  - C4 nível **Container** e ADR de CI/CD não escritos; CI/CD e previews seguem marcados
    `PROPOSTO` no `c4-context.md`.
  - Working tree compartilhado com TCK-0004 e TCK-0005: reexecutar as auditorias imediatamente
    antes de marcar `done`, porque a deriva de sync já ficou vermelha uma vez por causa alheia.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 — aprovados pela revisão;
  a marcação de `done` é do `qa-validator`, com evidência por critério.

## [015] HANDOFF — 2026-08-01 15:10
- De: qa-validator#4 → Para: tech-lead
- Status novo: **done**
- Veredito: **todos os 6 critérios atendidos, com evidência própria reproduzida por mim.**
  Nenhuma evidência do `[004]`, `[007]`, `[011]` ou `[014]` foi herdada — reexecutei cada
  comando e reli cada arquivo citado.

### Ambiente da validação

- Commit base: `21f6ef1b5f437424d6571144959e75772642eed2` (`TCK-0002: aprova a spec da
  primeira fatia de aprendizagem`), branch `main`, working tree sujo e **compartilhado** com
  TCK-0004 (`LICENSE*`, `ADR-0005`, `.github/instructions/content.instructions.md`,
  `AGENTS.md` §9) e TCK-0005 (`content/.../theory.*.md`) — nada disso avaliado aqui.
- Sem navegador e sem URL de preview: **não existe aplicação** (`ls src app api` → inexistentes;
  `find . -name package.json` → vazio). Validação **documental**, como manda a minha memória
  para ticket de ADR/spec — a bateria de casos hostis (offline, dois idiomas, tema, zoom 200%,
  teclado, leitor de tela, rede lenta, dados vazios) **não é aplicável** a este ticket porque o
  artefato é um documento de decisão e não há superfície executável que a exercite. Essas
  restrições viraram texto normativo (`ADR-0003:106-155`) e serão exercidas de verdade no
  primeiro ticket de implementação — é lá que a bateria hostil se aplica.
- Python 3 e os dois scripts de auditoria disponíveis; exit codes capturados **sem pipe**.

### Evidência por critério (comando + saída, reproduzidos)

**Critério 1 — `accepted`, data, decisor, aviso de bloqueio removido. ✓**
`git show HEAD:docs/adr/ADR-0003-platform-stack.md | sed -n '1,14p'` mostra o estado anterior:
`**Status:** proposed` · `**Decisores:** pendente — aguarda decisão de Douglas Silva` ·
"Nenhum ticket de implementação da aplicação deve avançar antes do aceite. Agentes devem
tratar tudo abaixo como hipótese."
Estado atual (`docs/adr/ADR-0003-platform-stack.md:3-13`): `**Status:** accepted` ·
`**Data:** 2026-08-01` · `**Decisores:** Douglas Silva (decisão registrada em 2026-08-01)` e o
aviso **substituído** por "Este ADR está `accepted`. O aceite **destrava a frente de
plataforma** …", que já delimita o que o ADR não decide.
Busca negativa por resíduo:
`grep -rniE "nenhum ticket deve avançar|não deve avançar|bloqueia.*implementa|implementação.*bloqueada"`
em `ADR-0003`, `docs/adr/README.md`, `memory/context/{frontend,project-context}.md` →
**nenhuma ocorrência**.

**Critério 2 — Decisão inequívoca + alternativas descartadas. ✓**
`ADR-0003:55-81`. Afirmação direta em `:57-62`: "gerador de site estático orientado a conteúdo
(opção C, Astro)", "a interatividade existe apenas como **ilha**", "persistência
local-first sem conta (opção 1, IndexedDB no próprio dispositivo)", "deploy é estático na
Vercel". Motivação em `:64-67`. Quatro alternativas descartadas com uma linha cada em
`:69-81`: A (Next.js), B (Vite + React/Preact), persistência 2 (sync opcional), persistência 3
(backend obrigatório). Estrutura conferida contra o template:
`grep -n '^## ' docs/adr/adr-template.md` → Contexto · Alternativas consideradas · Decisão ·
Consequências · Impacto · Como reverter; o ADR tem as seis **mais** a seção do critério 4.

**Critério 3 — Consequências preenchidas e concretas, os sete pontos. ✓**
`grep -nE "JavaScript mínimo|Rotas estáticas por idioma|PWA offline-first|KaTeX acessível|gabarito do exercício viaja|Não há backend, conta, login|deploy é estático na Vercel|destrava os tickets" docs/adr/ADR-0003-platform-stack.md`:
1. JS mínimo / ilhas → `:106-108` ("se um recurso exige hidratar a página inteira, ele está
   mal desenhado" — verificável, não genérico).
2. Rotas por idioma com paridade → `:109-112` (paridade obrigatória por ADR-0002; tratamento
   de nó bilíngue em `draft` **declarado em aberto**, sem fechar a pergunta da spec).
3. PWA offline-first → `:113-115` ("requisito de arquitetura, não recurso opcional").
4. KaTeX acessível → `:116-120` (descrição textual, imagem de fórmula proibida, sem custo de
   JS desproporcional) + negação explícita do momento de renderização.
5. Backend/conta/login/telemetria só com ADR novo → `:143-145` ("Nenhum ticket pode
   assumi-los como disponíveis").
6. Gabarito no payload do cliente → `:131-135` (consequência derivada: "nada pode depender do
   segredo da resposta — sem prova valendo nota, sem certificado verificável, sem ranking").
7. Deploy estático portátil → `:151-155` (recurso proprietário da Vercel que quebre a
   propriedade exige ADR).
O "o que o aceite destrava" exigido pelo critério está em `:8-10` e `:182-185`. Está na seção
**Impacto**, não em **Consequências** — não reprovo por isso: o template canônico
(`docs/adr/adr-template.md:39`) prevê `## Impacto` exatamente para isso, e a informação está
presente e falseável. Critério pede informação, não cabeçalho.

**Critério 4 — independência do contrato de dados como restrição a preservar. ✓**
`ADR-0003:157-174`, seção própria. Afirmação normativa em `:159-161`; três proibições
explícitas em `:165-170` (frontmatter proprietário / import de componente no Markdown / tipagem
gerada; lógica de aprendizagem no código em vez do dado; transformação de build irrepetível);
e **teste de conformidade falseável** em `:172-174` ("um leitor de `content/` escrito do zero,
sem a aplicação, deve conseguir reconstruir a taxonomia, as rotas por idioma e os exercícios").
Reforçada em `:178-179` (Impacto: conteúdo) e `:189-191` (Como reverter).

**Critério 5 — README dos ADRs, project-context e frontend refletem o aceite; nada mais
descreve o ADR como decisão em aberto. ✓**
- `docs/adr/README.md:13` → linha da tabela `| ADR-0003 | Stack da plataforma web/PWA |
  accepted | 2026-08-01 |`; `:17-19` → nota "foi aceito em 2026-08-01: a frente de plataforma
  está destravada", com a fronteira dura.
- `memory/context/project-context.md:16` → frente **Plataforma** "Não iniciada, mas
  **destravada**"; `:25-30` → `ADR-0003` listado em **Decisões aceitas** com decisor e
  restrições. Não aparece mais em "decisões em aberto".
- `memory/context/frontend.md:13-15` → "Stack decidida em 2026-08-01 (`ADR-0003`, aceito)";
  `:16-18` lista o que segue **não** decidido como implementação; `:26-45` traz 8 decisões
  operacionais derivadas.
- **Varredura própria da raiz** (não a do revisor): `grep -rn "ADR-0003" . --exclude-dir=.git`
  → **186 ocorrências**. Filtrando estado obsoleto
  (`| grep -viE "^\./\.dev-loop/|^\./tickets/" | grep -iE "proposed|hipótese|em aberto|pendente|não decidid|não está|em avaliação|aguarda"`),
  sobram exatamente as classes previstas e **nada além**:
  (a) `.dev-loop/**` — gitignorado, confirmado por mim com
      `git check-ignore -v .dev-loop/minimum-learning-slice/requirements.md` → `.gitignore:17`;
  (b) logs e `ticket.md` dos tickets (histórico append-only — TCK-0001/0002/0003/0004/0005);
  (c) `docs/specs/minimum-learning-slice/` (TCK-0002) — e `plan.md:114,126,134` já cita o ADR
      **aceito**, mantendo o item 3 ("KaTeX build × runtime") aberto, como deve;
  (d) registros meta que **não** afirmam estado obsoleto, apenas o narram:
      `memory/agents/platform-architect.md:43` (lista de pendências do próprio produtor),
      `memory/agents/code-reviewer.md:130` e `memory/agents/docs-writer.md:63`;
  (e) as **sete** pendências de área alheia (julgamento b, abaixo).
  Todos os pontos positivos conferidos um a um: `AGENTS.md:38,440`, `README.md:10`,
  `prompts/bootstrap-session.md:31`, `docs/product/roadmap.md:29`,
  `.github/instructions/{core:33,app:7}.instructions.md`, `.claude/agents/platform-architect.md:18,35`,
  `docs/architecture/README.md:8,11`, `docs/architecture/c4-context.md:4,17,20,38,54`
  e os 9 gerados — todos dizem `accepted` / "decidida".
- **A regra "nenhuma implementação sem spec aprovada" sobreviveu intacta.**
  `git diff --no-color -U0 | grep "^-" | grep -iE "spec aprovada|implementação sem spec|sem spec"`
  → **vazio**: nenhuma linha com a regra foi removida em todo o diff da árvore.
  Contagem antes × depois (`git show HEAD:<arquivo> | grep -c` vs `grep -c`):
  `AGENTS.md` 2→2 · `core.instructions.md` 1→1 · `app.instructions.md` 1→1 ·
  `bootstrap-session.md` 1→1. Presente hoje em **11 pontos**: `AGENTS.md:221,438`,
  `prompts/bootstrap-session.md:30`, `.github/instructions/core.instructions.md:32`,
  `.github/instructions/app.instructions.md:11`, `.agents/rules/core.md:31`,
  `.cursor/rules/core.mdc:35`, `.windsurf/rules/core.md:34`, `.rules:31`, `.clinerules:31`,
  `.junie/guidelines.md:31`.

**Critério 6 — auditorias sem erros. ✓ (reexecutadas por mim, exit code sem pipe)**
Primeira passagem e **reexecução imediatamente antes desta decisão**, ambas idênticas:
- `python3 scripts/sync-ai-adapters.py --check` → "20 skills + 21 agents + 6 regras → adapters
  verificados … Tudo já estava atualizado", **exit 0**.
- `bash scripts/audit-ai-surface.sh > f 2>&1; echo $?` → `Resultado: OK`, `up-to-date`,
  "todas dentro do limite", **exit 0**.
- `bash scripts/audit-content.sh > f 2>&1; echo $?` → `Resumo: 1 nós · 0 erros · 0 avisos`,
  **exit 0**.
Alcance declarado: `audit-ai-surface.sh` prova paridade e sincronia dos adapters, **não** prova
que o texto propagado está correto — isso foi conferido por leitura minha (abaixo).

### Verificações próprias, além dos critérios

- **Adapters gerados refletem as fontes, sem invenção.** Comparei corpo a corpo, por script,
  cada gerado contra a fonte canônica (removendo front matter e marcadores `managed-by`):
  `app` → `.agents/rules/app.md`, `.cursor/rules/app.mdc`, `.windsurf/rules/app.md`: **0 linhas
  ausentes na fonte**; `core` → `.agents/rules/core.md`, `.cursor/rules/core.mdc`,
  `.windsurf/rules/core.md`: **0**. Em `.rules`, `.clinerules` e `.junie/guidelines.md`
  aparecem 5 linhas extras — conferi que são o **rodapé fixo do gerador** ("Capacidades e
  papéis…"), já presente em `HEAD` (`git show HEAD:.rules | tail -7`), não texto novo sobre
  stack. O único delta desses arquivos nesta árvore é o item 5 (stack, deste ticket) e o item
  9 (licença, do TCK-0004).
- **Coerência do ADR consigo mesmo (o defeito B4 não voltou nem sobrou irmão).**
  `awk 'NR>=83 && NR<=91' ADR-0003 | grep -niE "renderiz|service worker|katex|pré-render|build × runtime"`
  → **nenhuma ocorrência dentro do bloco Mermaid**. Os nós são: `content/` → build estática →
  `HTML por idioma … matemática acessível` (`:86`) → `Ilha interativa` → `IndexedDB` (`:88`),
  `Conteúdo visitado disponível offline` (`:89`) e `Vercel (host estático substituível)` (`:90`)
  — todos **resultados ou mecanismos decididos**, nenhum mecanismo em aberto.
  A **Leitura** (`:92-99`) não reintroduz nada e nega nominalmente as duas não-decisões
  (`:97-99`: "não decide *como* cada caixa é obtida — em que momento a matemática é renderizada
  (build × runtime) e com que estratégia o conteúdo visitado fica offline").
  `grep -nE "renderiz|service worker"` no arquivo inteiro → `:11-12` e `:119` são as **negações**
  explícitas; `:19` é requisito de contexto; `:30,:39,:75` descrevem as alternativas A e B;
  `:64` é "SEO nativo do **HTML** pré-renderizado" — pré-renderização da **página**, que é a
  própria opção C, distinta do momento de renderização da **fórmula**. Conferi essa distinção
  por leitura própria e concordo: uma página estática admite matemática renderizada na build
  **ou** em runtime dentro da ilha, e `:116-120` acomoda as duas.
- **Escopo respeitado.** `git status --porcelain -uall | grep -iE "package.json|node_modules|\.ts|\.tsx|\.js|\.astro|tsconfig|vite|astro.config"` →
  **nenhum arquivo de código ou dependência**. `ls src app api` → inexistentes. Nenhuma
  biblioteca de UI, de testes ou de service worker escolhida — o ADR lista as três em `:11`
  entre o que **não** decide.
- **Lições sem colisão:** varredura própria por script em `memory/lessons/*.md` →
  `L-001 … L-014`, **nenhum ID duplicado**. L-011 e L-013 conferidas por leitura: são lições
  distintas (uma sobre *o que* escrever num ADR, outra sobre *método de correção*), coerentes
  com o histórico deste ticket. Nenhum defeito recorrente com lição registrada foi encontrado
  na entrega final — a regra 7 (AGENTS.md §10) não é acionada.

### Pontos de julgamento (decisão minha, não do revisor)

**(a) S6 — `ADR-0003:95` diz "nenhum mecanismo" enquanto o diagrama traz IndexedDB (`:88`) e
Vercel (`:90`). Veredito: imprecisão tolerável → DÍVIDA `D-1`, não defeito.**
O fato é real: os dois **são** mecanismos, e decididos. Apliquei o teste que separa isto do B4:
*a contradição produz uma restrição operativa errada?*
- **B4 produzia:** o diagrama mandava "KaTeX pré-renderizado" enquanto o texto dizia não
  decidir — o `frontend-developer` receberia uma obrigação inexistente. Defeito, corretamente.
- **S6 não produz:** o erro aponta para o lado oposto — **subestima** o diagrama. Ninguém
  deriva daí "IndexedDB não está decidido", porque a decisão é afirmada de forma normativa em
  quatro outros lugares que qualquer agente lê antes: `ADR-0003:60-62` (Decisão), `:181`
  (Impacto), `AGENTS.md:38,440`, `.github/instructions/app.instructions.md:7-9` e
  `memory/context/frontend.md:13-15`. Nenhuma implementação sai diferente por causa desta frase.
- Além disso, "mecanismo" é definido em contexto pela oração seguinte da própria Leitura
  ("não decide *como* cada caixa é obtida"): sob esse sentido a frase é verdadeira — o diagrama
  mostra *o quê* (o progresso mora em IndexedDB no dispositivo), não *como*. É redação frouxa
  lida isoladamente, defensável lida inteira.
Reprovar aqui seria trocar precisão de redação por mais um ciclo com a frente de plataforma
parada, num ponto que não muda restrição nenhuma — e o limite de 3 loops já foi consumido.
Registro como **`D-1` (dívida)**: trocar "nenhum mecanismo" por "nenhum mecanismo **não
decidido**" (uma palavra, exatamente a S6) na próxima edição do ADR. Não bloqueia o `done`.

**(b) As sete pendências de área alheia. Veredito: nenhuma é do `platform-architect` e
nenhuma anula o desbloqueio na prática. Critério 5 atendido.**
Conferência de propriedade: `memory/agents/<name>.md` é, por AGENTS.md §5, memória do próprio
agente — logo `tech-lead:16`, `product-analyst:18`, `docs-writer:63` e `a11y-ux-reviewer:56`
são deles; `.claude/agents/tech-lead.md:52` é a definição do papel do `tech-lead`;
`.claude/skills/ticket/SKILL.md:51` e `.claude/workflows/feature-plan-review.js:64` são o
ferramental do `tech-lead`. O produtor tocou apenas `.claude/agents/platform-architect.md` e a
própria memória — correto.
Teste de anulação, uma a uma (li o contexto de cada linha, não só a linha):
1. `.claude/agents/tech-lead.md:52` — "**enquanto** `ADR-0003` (stack) estiver `proposed`,
   tickets … ficam `blocked: human-input`". É **guarda condicional com condição hoje falsa**;
   o `tech-lead` avalia a condição contra o ADR (`accepted`) e a regra **não dispara**.
2. `.claude/skills/ticket/SKILL.md:51` — a norma é "ticket que depende de decisão estrutural
   **não decidida**"; `ADR-0003` é apenas o **exemplo** envelhecido. A norma segue válida e
   correta sem ele.
3. `.claude/workflows/feature-plan-review.js:64` — é a única que **afirma** o estado obsoleto
   ("que ainda está 'proposed'?") em vez de condicioná-lo. Ainda assim não anula: é uma
   *pergunta* de um prompt de revisão de plano, invocado só a pedido do usuário, e o agente que
   a responde tem `AGENTS.md` ("stack decidida") carregado. Pior caso: um achado falso-positivo
   numa revisão. É a de maior prioridade da lista.
4. `memory/agents/tech-lead.md:16` — a mais arriscada das memórias, porque afirma que tickets
   de frontend/backend/devops ficam `blocked: human-input`; mas está qualificada por
   "`(proposed)`" e é contradita pelas fontes que o `tech-lead` lê na mesma triagem
   (`memory/context/project-context.md:16` "destravada", `AGENTS.md:440`, `docs/adr/README.md:17`).
5. `memory/agents/product-analyst.md:18` — condicional ("Enquanto … estiver `proposed`"), hoje
   falsa; e a prática que descreve (requisito = comportamento + contrato de dados) continua
   correta sob o ADR aceito.
6. `memory/agents/docs-writer.md:63` — nota **procedimental** ("quando achar trecho de outra
   área, reportar em vez de corrigir") que usa o README como exemplo histórico. Não afirma
   estado atual. Inofensiva.
7. `memory/agents/a11y-ux-reviewer.md:56` — rótulo obsoleto; a substância ("levantar antes do
   primeiro render") permanece válida. Duplamente desatualizada, aliás: o ADR **não** decide
   renderização, então a dependência correta é do ticket de implementação, não do ADR.
Conclusão: todas são **conditional guard com condição falsa**, exemplo envelhecido ou registro
meta. O desbloqueio se sustenta porque as fontes normativas que governam a ação — `AGENTS.md`
§1 e §11, `.github/instructions/{core,app}` (esta com `applyTo: src/**,app/**,api/**,tests/**,e2e/**`,
justamente o código que o ADR destrava), `README.md`, `prompts/bootstrap-session.md` e os 9
gerados — dizem `accepted` sem ressalva. Não bloqueia; vira `ACTION` abaixo.

### ACTION ao `tech-lead` (fora do escopo deste ticket, não bloqueiam)

- **A-1 — abrir ticket de limpeza das 7 pendências de `ADR-0003 proposed`**, na ordem de risco
  que apurei: (1) `.claude/workflows/feature-plan-review.js:64` (única que **afirma** o estado
  obsoleto; exige `sync-ai-adapters.py` depois), (2) `memory/agents/tech-lead.md:16`,
  (3) `.claude/agents/tech-lead.md:52` e `.claude/skills/ticket/SKILL.md:51` (exigem sync),
  (4) `memory/agents/{product-analyst:18,a11y-ux-reviewer:56,docs-writer:63}.md`.
  Cada arquivo deve ser editado pelo seu dono (AGENTS.md §5 e §10).
- **A-2 — dívida `D-1`** (julgamento (a)): `ADR-0003:95` → "nenhum mecanismo **não decidido**".
  Uma palavra; entra em qualquer edição futura do ADR, sem ticket próprio.
- **A-3 — `memory/agents/a11y-ux-reviewer.md:56` cita dependência errada**: a duplicação
  MathML × `*Leitura:*` depende de **decisão de implementação** (KaTeX build × runtime,
  `docs/specs/minimum-learning-slice/plan.md:134`), não do `ADR-0003`, que declara não decidir
  isso. Corrigir junto com A-1.
- **A-4 — lacunas de arquitetura herdadas, já registradas pela cadeia e confirmadas por mim:**
  C4 nível **Container** inexistente (`docs/architecture/` só tem Context) e CI/CD + previews
  por branch seguem `PROPOSTO` em `c4-context.md:20,26` sem ADR. Ambos merecem ticket próprio
  antes do primeiro ticket de implementação da aplicação.

- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 — **todos com evidência
  própria acima. Ticket `done`.**
