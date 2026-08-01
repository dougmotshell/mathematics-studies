# Log — TCK-0002

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 12:12 — /ticket
- Ação: ticket criado a partir do pedido do usuário.
- Motivo: registrar a primeira fatia de produto no fluxo auditado antes de qualquer implementação.
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] HANDOFF — 2026-08-01 12:12
- De: tech-lead → Para: task-router
- Status novo: triaged
- O que foi feito: documentação analisada; escopo reduzido à spec da fatia mínima para não assumir a stack proposta em `ADR-0003`.
- Artefatos: `tickets/TCK-0002-define-minimum-learning-slice/ticket.md`; `.dev-loop/minimum-learning-slice/`.
- Como validar: `bash tools/dev-loop.sh status minimum-learning-slice` e `bash tools/dev-loop.sh next minimum-learning-slice`.
- Pendências e riscos: a implementação da aplicação permanece bloqueada até spec aprovada e aceite do `ADR-0003`.
- Critérios de aceite: [ ] 1–6 restantes; o router deve definir a cadeia mínima.

## [003] ACTION — 2026-08-01 12:12 — task-router
- Ação: roteamento inicial executado e briefing `01-route.md` criado.
- Motivo: acionar o primeiro agente do dev-loop no modo assistido do Codex.
- Resultado: ok — próxima etapa `plan`, agente `product-analyst`; briefing validado pelo script.

## [004] HANDOFF — 2026-08-01 12:28
- De: task-router → Para: product-analyst
- Status novo: in_progress
- O que foi feito: usuário autorizou a execução; o dev-loop em
  `.dev-loop/minimum-learning-slice/` é retomado na etapa `plan` (iteração 1/3), conforme o
  briefing `01-route.md` — sem reiniciar o loop.
- Artefatos: `.dev-loop/minimum-learning-slice/briefings/01-route.md`.
- Como validar: `bash tools/dev-loop.sh status minimum-learning-slice`.
- Pendências e riscos: nenhuma etapa pode escolher a stack — `ADR-0003` segue `proposed`.
- Critérios de aceite: [ ] 1–6 restantes.

## [005] HANDOFF — 2026-08-01 12:52
- De: product-analyst → Para: docs-writer
- Status novo: in_progress
- O que foi feito: requisito da fatia mínima refinado a partir do contrato real de
  `content/high-school/algebra/quadratic-equations/` — escopo dentro/fora, RF-1…RF-18,
  RNF-1…RNF-11, 13 estados de tela, CA-1…CA-16 redigidos como testes, dependências travadas
  pelo `ADR-0003` e a lista exata dos arquivos que o `docs-writer` deve criar. Nenhuma
  escolha de framework, biblioteca, banco ou host foi feita.
- Artefatos: `.dev-loop/minimum-learning-slice/requirements.md`;
  `.dev-loop/minimum-learning-slice/briefings/02-plan.md`.
- Como validar: `bash tools/dev-loop.sh validate .dev-loop/minimum-learning-slice/briefings/02-plan.md`
  e `bash tools/dev-loop.sh next minimum-learning-slice`.
- Pendências e riscos: a spec nasce `draft` — quem escreve não aprova (critério 5 depende da
  etapa de review); exibir o nó piloto com `status: "draft"` e a forma da URL bilíngue ficam
  como perguntas em aberto na spec; a implementação segue bloqueada pelo `ADR-0003`.
- Critérios de aceite: [ ] 1–6 restantes (a etapa `plan` produz o insumo, não os arquivos da
  spec).

## [006] HANDOFF — 2026-08-01 13:24
- De: docs-writer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: spec da fatia mínima escrita em `docs/specs/minimum-learning-slice/` —
  `spec.md` (problema, escopo, RF-1…RF-18, RNF-1…RNF-11, 13 estados de tela, CA-1…CA-16,
  transversais, perguntas em aberto, métricas), `plan.md` (4 camadas de comportamento,
  alternativas descartadas, impacto, riscos, dependências, menor fatia) e `tasks.md` (15 tasks
  com agente, dependência e critério de pronto). Status `draft` nos três — quem escreve não
  aprova. `docs/specs/README.md` passou a listar a spec. Mermaid em `spec.md`
  (`stateDiagram-v2` do ciclo do item) e em `plan.md` (`flowchart` dado → tela, atual ×
  proposta), ambos com leitura e fontes. Nenhuma biblioteca escolhida; `content/` intocado;
  nenhum ADR criado ou editado.
- Artefatos: `docs/specs/minimum-learning-slice/{spec,plan,tasks}.md`; `docs/specs/README.md`;
  `.dev-loop/minimum-learning-slice/briefings/03-execute.md`; `memory/agents/docs-writer.md`.
- Como validar: `bash tools/dev-loop.sh validate .dev-loop/minimum-learning-slice/briefings/03-execute.md`
  (válido, 40 linhas); `bash scripts/audit-ai-surface.sh` → `Resultado: OK`;
  `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`; conferir a spec contra
  `.dev-loop/minimum-learning-slice/requirements.md`.
- Pendências e riscos: critério 5 depende desta revisão (a spec só vira `approved` por quem não
  a escreveu); o `plan.md` cita a direção decidida do `ADR-0003`, cujo aceite formal corre no
  `TCK-0003` — se o registro divergir, o plano precisa de ajuste; três perguntas em aberto
  (exibir nó `draft`, forma da URL bilíngue, rótulo de rascunho no índice) exigem decisão
  humana antes da aprovação.
- Critérios de aceite:
  - [x] 1. `docs/specs/minimum-learning-slice/spec.md` com objetivo, escopo, usuários,
    requisitos funcionais e não funcionais, estados principais e critérios verificáveis.
  - [x] 2. Spec exige paridade pt-BR/en-US (RNF-1, RF-7, RF-8), KaTeX acessível (RNF-2, RF-2,
    RF-3), offline do conteúdo visitado (RNF-3), custo zero (RNF-4) e preservação dos slugs
    (RNF-5, RF-17).
  - [x] 3. `plan.md` com abordagem independente de framework, dependências, riscos e o que fica
    como decisão de implementação sob o `ADR-0003`.
  - [x] 4. `tasks.md` com 15 tarefas executáveis, ordem de handoff, paralelizáveis e validação
    final.
  - [ ] 5. Aprovação da spec — pertence ao `code-reviewer`/revisor independente.
  - [x] 6. `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` sem erros.

## [007] HANDOFF — 2026-08-01 13:41
- De: code-reviewer#3 → Para: qa-validator
- Status novo: in_validation
- O que foi feito: revisão independente dos três arquivos da spec contra
  `.dev-loop/minimum-learning-slice/requirements.md` (fonte) e o contrato real do nó piloto.
  Fidelidade conferida item a item por diff normalizado: **RF-1…RF-18 idênticos**,
  **RNF-1…RNF-11** com dois deltas justificados (RNF-8 "a definir no aceite do `ADR-0003`" →
  "a definir na implementação", coerente com o ADR já aceito sem orçamento numérico; RNF-11
  ganhou a citação de `L-008`), **13 estados de tela** e **CA-1…CA-16 idênticos** — nenhum
  requisito inventado, nenhum descartado. Spec marcada `approved` em `spec.md:4`, `plan.md:4`
  e `docs/specs/README.md:13`.
- Artefatos: `docs/specs/minimum-learning-slice/{spec,plan,tasks}.md`; `docs/specs/README.md`;
  `.dev-loop/minimum-learning-slice/briefings/04-review.md`; `memory/agents/code-reviewer.md`.
- Como validar: `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (reexecutado);
  `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos` (reexecutado);
  `bash tools/dev-loop.sh validate .dev-loop/minimum-learning-slice/briefings/04-review.md`;
  `git status --porcelain` confirma que este ticket só tocou os quatro arquivos acima.
- Evidência do critério 5:
  - **Não bloqueia a escolha da stack.** `spec.md` não cita framework, biblioteca, banco,
    host nem ferramenta de teste (busca por `react|vue|svelte|astro|next|vite|vercel|
    indexeddb|service worker|playwright|jest|vitest|tailwind` só casa em `spec.md:259`, que
    é a linha de **fora de escopo** declarando essas escolhas como não-decididas).
    `plan.md:31-38` cita o `ADR-0003` apenas como direção (site estático com ilhas,
    local-first sem conta) e devolve biblioteca de UI, teste, service worker, momento do
    KaTeX e forma da URL bilíngue para "decisão de implementação"; `plan.md:132-142` lista
    essas sete decisões em aberto. `plan.md:105` mantém IndexedDB **fora** desta fatia.
  - **Não introduz coleta de dados.** RNF-7 (`spec.md:130-132`) proíbe conta, login, e-mail,
    analytics, cookie de rastreio e fingerprint; RF-16 (`spec.md:98-101`) prende o estado à
    memória de sessão; CA-12 (`spec.md:230-232`) testa o tráfego; a tabela de transversais
    (`spec.md:253`) amarra persistência entre sessões a um ADR de privacidade futuro;
    `tasks.md:24` reserva a auditoria ao `security-auditor`. Nenhum identificador de aluno é
    criado — compatível com público que inclui menores (LGPD/COPPA) e com `ADR-0003:134-136`.
  - **Coerência de dados** conferida contra
    `content/high-school/algebra/quadratic-equations/exercises.json`: `nodeId` + `version`,
    itens `qe-001`…`qe-005`, `feedback` nas quatro opções de todo `multiple-choice`
    (inclusive na correta), `qe-003` `answer: 3` / `tolerance: 0`, `qe-005` `answer: 3.5` /
    `tolerance: 0.001` / `unit: null`, `hints[]` com duas entradas por item e `solution`
    presente. Nenhum campo inexistente descrito.
- Pendências e riscos (sugestões, não bloqueantes — registradas para o `qa-validator`):
  1. RNF-2 exige descrição textual para **toda** fórmula em display, mas o nó piloto tem 3
     parágrafos `*Leitura:*` (`theory.pt-BR.md:36,46,53`) para 8 blocos `$$…$$`
     (linhas 34,44,51,66,76,80,92,103). Como RNF-9 proíbe tocar `content/`, a lacuna deve
     virar ticket de conteúdo na implementação, não emenda na spec.
  2. CA-2 (`spec.md:203-205`) cita `$$ax^2 + bx + c = 0$$`; o arquivo traz
     `$$ax^2 + bx + c = 0, \qquad a, b, c \in \mathbb{R}, \quad a \neq 0.$$`
     (`theory.pt-BR.md:34`). O critério continua falseável, mas a citação é abreviada.
  3. Perguntas em aberto (`spec.md:272-280`) **adiadas explicitamente**, dono `tech-lead` +
     decisão humana, prazo: antes da task 3 do `tasks.md`. A primeira delas (exibir nó
     `draft`) tensiona `docs/content/taxonomy.md:81` e `ADR-0002:36`; a segunda já está
     parcialmente decidida por `ADR-0003:62` ("i18n por rota estática, uma URL real por
     idioma"), que exclui a variante "parâmetro" oferecida na spec.
  4. `plan.md:132-142` não repete dois itens da seção 7 de `requirements.md` (mecanismo de
     armazenamento local e pipeline/ambientes) — cobertos pelo `ADR-0003` e pela task 11;
     omissão justificada, não silenciosa.
  5. `spec.md` não tem seção dedicada a "usuários": o público aparece em Problema
     (`spec.md:13-16`, "um aluno") e Resultado esperado (`spec.md:23`, "qualquer pessoa").
     Considerado atendido; nomear o público (inclui menores) melhoraria o critério 1.
- Critérios de aceite:
  - [x] 1. `docs/specs/minimum-learning-slice/spec.md` com objetivo (`Problema`,
    `Resultado esperado`), escopo (`spec.md:30-46` + `Fora de escopo`), usuários
    (`spec.md:13-23`), RF-1…RF-18, RNF-1…RNF-11, 13 estados de tela (`spec.md:147-161`) e
    CA-1…CA-16 verificáveis.
  - [x] 2. Paridade pt-BR/en-US sem fallback (RNF-1, RF-7, RF-8, RF-12), KaTeX acessível
    (RNF-2, RF-2, RF-3), offline do conteúdo visitado (RNF-3 + dois estados de rede), custo
    zero (RNF-4) e slugs preservados (RNF-5, RF-17) — todos exigidos no texto da spec.
  - [x] 3. `plan.md` com abordagem em quatro camadas de comportamento, alternativas
    descartadas, Mermaid atual × proposta, impacto, sete riscos, dependências bloqueantes e
    o que fica sob o `ADR-0003`.
  - [x] 4. `tasks.md` com 15 tarefas executáveis, agente, dependência, critério de pronto,
    paralelizáveis e validação final citando CA-1…CA-16 e as duas auditorias.
  - [x] 5. Spec `approved` por revisor independente (`code-reviewer#3`, que não produziu o
    artefato), com a evidência de stack e de privacidade registrada acima.
  - [x] 6. `bash scripts/audit-ai-surface.sh` → `Resultado: OK`; `bash scripts/audit-content.sh`
    → `1 nós · 0 erros · 0 avisos` — ambos reexecutados por este revisor em 2026-08-01.

## [008] HANDOFF — 2026-08-01 14:05
- De: qa-validator#2 → Para: tech-lead
- Status novo: done
- O que foi feito: validação independente dos critérios 1–6 contra os artefatos reais, com
  evidência reproduzida por este validador (não copiada do `code-reviewer#3`). Ambiente da
  validação: commit `d1ca2e5`, branch `main`, working tree com os artefatos do ticket ainda
  não commitados (`git status --porcelain` → `?? docs/specs/minimum-learning-slice/`,
  `M docs/specs/README.md`); shell zsh, Linux 7.0.0-28. Sem aplicação para exercitar — este
  ticket entrega **documento**, e a validação é documental por natureza (a validação de
  execução da fatia é a task 14 do `tasks.md`, em ticket próprio).
- Artefatos: `docs/specs/minimum-learning-slice/{spec,plan,tasks}.md`; `docs/specs/README.md`;
  `tickets/TCK-0002-define-minimum-learning-slice/ticket.md`;
  `.dev-loop/minimum-learning-slice/briefings/05-validate.md`; `memory/agents/qa-validator.md`.
- Como validar: os comandos de cada critério estão abaixo; todos reexecutados em 2026-08-01.

### Evidência por critério

- **[x] 1. `spec.md` com objetivo, escopo, usuários, RF, RNF, estados e critérios.**
  `grep -n '^## ' spec.md` → 14 seções, entre elas `Problema` (l.11), `Resultado esperado`
  (l.21), `Escopo` (l.30, com `### Dentro` l.32), `Requisitos funcionais` (l.48),
  `Requisitos não funcionais` (l.111), `Estados de tela` (l.145), `Critérios de aceite`
  (l.196). Contagens próprias: `grep -c '^- \*\*RF-'` → **18** (RF-1…RF-18, sequência sem
  buraco); `grep -c '^- \*\*RNF-'` → **11**; `grep -c '^- \[ \] \*\*CA-'` → **16**; tabela de
  estados `spec.md:147-161` → 15 linhas `|` = cabeçalho + separador + **13 estados**.
  **Usuários:** ver veredito (a) abaixo — atendido.
- **[x] 2. Spec exige paridade, KaTeX acessível, offline, custo zero e slugs.**
  Cinco exigências localizadas uma a uma no texto normativo: paridade sem fallback
  `spec.md:113-115` (RNF-1) + `spec.md:70-75` (RF-7/RF-8) + `spec.md:86-89` (RF-12);
  matemática acessível `spec.md:116-118` (RNF-2) + `spec.md:58-61` (RF-3); offline do
  conteúdo visitado `spec.md:119-121` (RNF-3) + os dois estados de rede `spec.md:160-161`;
  custo zero `spec.md:122-123` (RNF-4); slugs preservados `spec.md:124-125` (RNF-5) +
  `spec.md:102-104` (RF-17). Cada um tem CA correspondente (CA-3/CA-7/CA-11/CA-14, CA-2/CA-15,
  CA-10/CA-11, CA-12, CA-1), ou seja, é exigência falseável e não declaração de intenção.
- **[x] 3. `plan.md` independente de framework, com dependências, riscos e o que depende do
  `ADR-0003`.** `grep -n '^## ' plan.md` → `Abordagem escolhida` (l.7), `Alternativas
  descartadas` (l.40), `Arquitetura afetada` (l.52), `Impacto` (l.97), `Riscos` (l.110, **7
  riscos** com probabilidade/impacto/mitigação), `Dependências` (l.122: **3 bloqueantes** +
  **7 decisões de implementação** numeradas em l.132-142), `Menor fatia entregável` (l.147).
  Independência de framework verificada por busca própria em **spec.md, plan.md e tasks.md**
  (`grep -nEi 'astro|react|vue|svelte|next\.?js|vite|webpack|vercel|netlify|tailwind|
  indexeddb|localstorage|service worker|playwright|cypress|jest|vitest|postgres|supabase|
  firebase'`): apenas 4 ocorrências, **todas negativas** — `spec.md:259` (fora de escopo),
  `plan.md:33` e `plan.md:105` (IndexedDB declarado **fora** desta fatia) e `plan.md:139`
  (service worker como decisão adiada). `tasks.md`: **zero** ocorrências. Nem `Astro` nem
  `Vercel` — as escolhas concretas do `ADR-0003` — aparecem em qualquer dos três arquivos;
  o plano fica um nível acima da decisão do ADR (`plan.md:31-38`).
- **[x] 4. `tasks.md` com tarefas executáveis e ordem de handoff.**
  `grep -c '^| [0-9]' tasks.md` → **15 tasks**, cada uma com agente, coluna `Depende de` e
  critério de pronto verificável. Ordem de handoff completa e sem ciclo: 1 (`platform-architect`)
  → 2 (`code-reviewer`) → 3 (`ui-ux-designer`) ‖ 4 (`backend-developer`) → 5, 6
  (`frontend-developer`) → 7 → 8 → 9 (`i18n-steward`) ‖ 10 (`+ devops-engineer`) → 11
  (`devops-engineer`) → 12 (`a11y-ux-reviewer`) ‖ 13 (`security-auditor`) → **14
  (`qa-validator`)** → 15 (`docs-writer`). Implementação (4–11), revisão/auditoria (2, 12, 13)
  e validação (14) estão cobertas; `tasks.md:28-36` marca o que é paralelizável e o que **não**
  é (7 e 8); `tasks.md:38-57` fixa a validação final por CA e pelas duas auditorias, e
  `tasks.md:57` repete a regra "cada agente valida apenas o que não produziu".
- **[x] 5. Spec `approved` com evidência de que não trava a stack nem coleta dados.**
  Independência da cadeia conferida no próprio log: produtor `docs-writer` [006], aprovador
  `code-reviewer#3` [007], validador `qa-validator#2` — três papéis distintos.
  **Não trava a stack:** a busca do critério 3 (acima), reexecutada por mim, é a prova — as
  únicas menções a tecnologia são exclusões. `plan.md:132-142` devolve sete decisões
  (renderização, URL bilíngue, KaTeX build×runtime, cache, onde roda RF-18, ferramentas de
  teste, orçamento de performance) para os tickets de implementação.
  **Não introduz coleta:** RNF-7 (`spec.md:130-132`) proíbe conta, login, e-mail, analytics,
  cookie de rastreio, fingerprint e terceiro que registre o visitante; RF-16
  (`spec.md:98-101`) prende o estado à memória de sessão; CA-12 (`spec.md:230-232`) torna isso
  testável por inspeção de tráfego; `spec.md:253` amarra persistência entre sessões a um ADR
  de privacidade futuro; `spec.md:261` põe telemetria e analytics fora de escopo; `spec.md:296`
  recusa deliberadamente métrica por instrumentação. Coerente com `ADR-0003:131-136`
  ("Não há backend, conta, login nem telemetria identificável... exige ADR novo... LGPD/COPPA
  quando envolver dado de menor"). Marcação `approved` conferida em `spec.md:4`, `plan.md:4` e
  `docs/specs/README.md:13` (`tasks.md` não tem campo de status — o template
  `docs/specs/templates/tasks.md` também não tem; ausência correta, não omissão).
- **[x] 6. Auditorias sem erros — reexecutadas por este validador.**
  `bash scripts/audit-ai-surface.sh` → `Resultado: OK`, **exit 0** (limite de 12.000 caracteres
  nas regras OK; `sync-ai-adapters.py --check` → `up-to-date`; acesso do Codex `documented`).
  `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos`, **exit 0**. Código de
  saída capturado direto do script, não de um pipe.

### Pontos de julgamento (veredito do `qa-validator`)

- **(a) Critério 1, "usuários" — ATENDIDO.** O critério exige a *informação*, não um cabeçalho.
  O template canônico `docs/specs/templates/spec.md` **não tem** seção "Usuários": instrui, na
  seção `Problema`, "descrever em termos do usuário (aluno, contribuidor, mantenedor)" — que é
  exatamente o que `spec.md:13-16` faz ("um aluno não consegue ler um nó nem praticar"), com o
  alcance delimitado em `spec.md:23` ("Qualquer pessoa"). A fatia tem **um único papel**; não há
  fluxo de contribuidor ou mantenedor no escopo. Teste de falseabilidade: um implementador
  erraria a entrega por falta de definição de usuário? Não — os 18 RF e os 16 CA são todos
  escritos da perspectiva do aluno. Exigir uma seção que o próprio template não prevê seria
  negociar critério por preferência de forma, e isso não é papel do QA.
  *Nit registrado (não bloqueante):* a spec nunca **nomeia** que o público inclui menores — o
  vínculo só aparece na tabela de transversais (`spec.md:253`) e no `ADR-0003:63-64`. Como RNF-7
  proíbe **toda** coleta identificável (regra estritamente mais forte que qualquer exigência
  específica de menor), a omissão não pode gerar implementação errada. Vira melhoria de redação
  em revisão futura da spec, não devolução.
- **(b) Perguntas em aberto com spec `approved` — COMPATÍVEL; nenhuma é bloqueante.** O padrão do
  próprio projeto está em `tasks.md:13`: "perguntas em aberto **resolvidas ou explicitamente
  adiadas com dono**". Avaliação caso a caso, com o teste "isto impede a task 3 de começar?":
  1. **Exibir o nó `draft`?** (`spec.md:274-276`) — **não bloqueia.** A spec **decide um padrão
     normativo**: RF-5 (`spec.md:64-66`, "ele deve aparecer mesmo assim, marcado"), CA-16
     (`spec.md:242-243`) e CA-1 (`spec.md:200-202`). A pergunta é pedido de confirmação de uma
     decisão já tomada, não um vazio. E o estado "Nó | Rascunho" (`spec.md:152`) é necessário
     **sob qualquer desfecho** — um nó `draft` alcançado por URL direta continua precisando do
     rótulo —, logo a task 3 tem alvo inequívoco. Conferi que **não há contradição** com norma
     aceita: `docs/content/taxonomy.md:81` e `ADR-0002:33-36` condicionam **publicar** aos dois
     idiomas completos, e o nó piloto tem `languages: ["pt-BR","en-US"]` com `status: "draft"`
     (`content/high-school/algebra/quadratic-equations/meta.json`) — está `draft` por ciclo de
     vida, não por lacuna de idioma; nenhuma regra existente proíbe exibi-lo. Se a decisão humana
     reverter o padrão, o retrabalho cai na **task 5** (índice), a jusante — risco aceito e
     rastreável, não impedimento agora.
  2. **Forma da URL bilíngue?** (`spec.md:277-279`) — **não bloqueia.** Desenhar estados de tela
     não fixa forma de URL. O invariante que importa está travado em RF-17 (`spec.md:102-104`) e
     em RNF-5, e `plan.md:136-137` adia a forma para os tickets. *ACTION:* a spec ainda oferece
     "parâmetro ou domínio separado", variantes já excluídas por `ADR-0003:62-63` ("i18n por rota
     estática, uma URL real por idioma"), aceito no mesmo dia — a pergunta encolheu para
     prefixo × sufixo. Desatualização de redação; não viola o critério 3, que exige do plano
     apenas sinalizar o que depende do ADR (`plan.md:126-142` sinaliza).
  3. **Rótulo de rascunho no índice?** (`spec.md:280`) — **não bloqueia.** É sub-detalhe da
     pergunta 1, não está entre os 13 estados e não impede a task 3, cujo "rótulo de rascunho"
     é satisfeito pelo estado de página de nó que a spec define.
  Conclusão: nenhuma decisão pendente deixa a próxima etapa sem alvo; o ticket **não** vai a
  `blocked: human-input`. Dívida aceita e registrada: o dono (`tech-lead`) e o prazo (antes da
  task 3) das três perguntas estão no log [007], **não no corpo da spec** — quem retomar deve
  ler o log junto com `spec.md:272-280`.

### Requisitos transversais — rastreabilidade conferida (`spec.md:245-255`)

Cada um dos seis marcados no `ticket.md` tem exigência normativa e prova: bilinguismo → RNF-1,
RF-7, RF-8, RF-12 / CA-3, CA-7, CA-11, CA-14 · a11y → RNF-2, RNF-6, RF-3 / CA-2, CA-15 ·
offline → RNF-3 + estados `spec.md:160-161` / CA-10, CA-11 · custo zero → RNF-4, RNF-11 / CA-12 ·
privacidade de menores → RNF-7, RF-16 / CA-12 · URLs preservadas → RNF-5, RF-17 / CA-1. Nenhum
transversal ficou sem RNF **e** sem CA. "Correção matemática" está corretamente como *não
aplicável* (`spec.md:255`): RNF-9 proíbe a fatia de alterar `content/`.

- Pendências e riscos (encaminhados ao `tech-lead`; nenhum bloqueia este ticket):
  1. **ACTION — fora do escopo do TCK-0002, vira ticket próprio.** O nó piloto tem **8 blocos
     `$$…$$` para apenas 3 parágrafos `*Leitura:*`**, nos **dois** idiomas — reproduzido por mim:
     `grep -n '^\$\$' content/high-school/algebra/quadratic-equations/theory.pt-BR.md` → linhas
     **34, 44, 51, 66, 76, 80, 92, 103**; `grep -n '\*Leitura:\*'` no mesmo arquivo → linhas
     **36, 46, 53**; em `theory.en-US.md`, 8 blocos e 3 `Reading:`. Contraria `AGENTS.md` §9.2 e
     RNF-2/RF-3 da própria spec, e faria CA-2 falhar por dados quando a fatia for implementada.
     **Não corrigido aqui:** RNF-9 (`spec.md:136-138`) e a seção "Fora de escopo" do `ticket.md`
     proíbem tocar `content/` neste ticket. Sugestão: ticket de conteúdo para
     `content-author` + `a11y-ux-reviewer`, **antes da task 6** do `tasks.md`.
  2. **ACTION — decisão humana pendente.** As três perguntas em aberto (`spec.md:272-280`)
     precisam de dono e prazo registrados **na spec**, não só no log [007]; a segunda deve ser
     reduzida a prefixo × sufixo à luz de `ADR-0003:62-63`.
  3. **ACTION — melhoria de redação.** Nomear o público (inclui menores de idade) na spec, para
     que RNF-7 fique justificado no próprio documento.
  4. Nota de método: por ser entrega documental, **não houve execução de aplicação** — não
     existe código. Os casos hostis do `qa-validator` (offline, dois idiomas, teclado, leitor de
     tela, zoom 200%, rede lenta, dados vazios) foram verificados como **exigência escrita e
     falseável** na spec, e sua execução real é a task 14 (`tasks.md:25`).
- Critérios de aceite:
  - [x] 1. Objetivo, escopo, usuários, RF-1…RF-18, RNF-1…RNF-11, 13 estados e CA-1…CA-16.
  - [x] 2. Paridade, KaTeX acessível, offline, custo zero e slugs exigidos e testáveis.
  - [x] 3. `plan.md` independente de framework, com dependências, 7 riscos e 7 decisões sob o
    `ADR-0003`.
  - [x] 4. `tasks.md` com 15 tarefas executáveis e ordem de handoff sem ciclo.
  - [x] 5. `approved` por revisor independente, com evidência de stack e privacidade reproduzida.
  - [x] 6. `audit-ai-surface.sh` OK (exit 0) e `audit-content.sh` 0 erros / 0 avisos (exit 0).
