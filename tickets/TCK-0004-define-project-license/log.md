# Log — TCK-0004

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 12:40 — tech-lead
- Ação: ticket criado a partir da decisão do usuário sobre a licença do projeto.
- Motivo: "licença do conteúdo e do código" estava listada como decisão em aberto em
  `memory/context/project-context.md`; sem ela não é possível avaliar compatibilidade de
  fontes externas (impacta diretamente o `TCK-0001`).
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 12:40 — tech-lead
- Ação: triagem. Tipo `docs`, P1, tamanho P.
- Motivo: a decisão já foi tomada pelo usuário; o trabalho é documental (ADR + arquivos de
  licença + propagação da regra de compatibilidade).
- Resultado: ok — `triaged`.

## [003] SPAWN — 2026-08-01 12:40
- Por: tech-lead → Subagente: docs-writer#2
- Motivo: o `docs-writer` (instância principal) está ocupado com o `TCK-0002` (spec da fatia
  mínima). Pelo protocolo, agente ocupado não enfileira — spawna subagente da própria área.
- Escopo delegado: ticket inteiro (TCK-0004), como dono pleno.

## [004] HANDOFF — 2026-08-01 12:40
- De: tech-lead → Para: docs-writer#2
- Status novo: in_progress
- O que foi feito: decisão humana coletada (conteúdo CC BY-SA 4.0, código MIT) e registrada
  no ticket; execução autorizada pelo usuário.
- Artefatos: `tickets/TCK-0004-define-project-license/ticket.md`.
- Como validar: critérios 1–7 do ticket; auditorias determinísticas ao final.
- Pendências e riscos: a consequência de compatibilidade (CC BY-SA não absorve fontes NC)
  precisa chegar ao `researcher` antes de ele fechar o `TCK-0001`, que roda em paralelo.
- Critérios de aceite: [ ] 1–7 restantes.

## [005] ACTION — 2026-08-01 12:52 — docs-writer#2
- Ação: materializada a decisão de licença (conteúdo CC BY-SA 4.0, código MIT) em ADR,
  arquivos de licença na raiz e regra operacional nos documentos que o autor de conteúdo lê.
  Criados: `docs/adr/ADR-0005-project-license.md` (`accepted`, decisor Douglas Silva,
  2026-08-01 — contexto, 3 alternativas de conteúdo e 3 de código com prós/contras, decisão,
  consequências, impacto e caminho de reversão); `LICENSE` (texto integral da MIT, titular
  Douglas Silva, 2026, com nota de escopo); `LICENSE-CONTENT` (CC BY-SA 4.0 em pt-BR e en-US
  em seções separadas, URL canônica `https://creativecommons.org/licenses/by-sa/4.0/`,
  modelos de atribuição com e sem alteração, e o que a licença **não** cobre).
  Alterados: `docs/adr/README.md` (só a linha do ADR-0005), `docs/content/content-standards.md`
  (nova seção "Licença e compatibilidade de fontes" com árvore de decisão Mermaid + leitura +
  fontes, e item novo no checklist de `published`), `memory/context/content.md` (decisão
  operacional + estado das referências do nó piloto), `memory/context/project-context.md`
  (edição cirúrgica: ADR-0005 em "Decisões aceitas", licença removida de "Decisões em aberto",
  próximos passos renumerados, linha de Documentação e riscos), `README.md` (seção Licença
  agora declara as duas licenças) e `docs/product/roadmap.md` (item da Fase 1 marcado como
  concluído na parte da licença, sem tocar na menção ao `ADR-0003`).
- Motivo: critérios de aceite 1–7 do ticket; a decisão humana já existia e faltava registro
  normativo e propagação.
- Regra operacional registrada (critério 4), com os exemplos reais do repositório: fontes
  **CC BY**, **CC BY-SA**, **CC0** e **domínio público** podem ser adaptadas (com atribuição;
  o derivado sai sob CC BY-SA 4.0); fontes **CC BY-NC** e **CC BY-NC-SA** — caso das duas
  referências OpenStax e do *Livro Aberto de Matemática* hoje em `references.json` — **não**
  podem ser incorporadas nem adaptadas, só citadas como leitura externa. Mnemônico adotado:
  **"NC = leitura, não matéria-prima"**. Lições relacionadas: L-006, L-007.
- Restrições respeitadas: nada alterado em `content/`, `references.json`, `docs/specs/`,
  `docs/adr/ADR-0003-platform-stack.md` ou nos tickets TCK-0001/0002/0003; em
  `docs/adr/README.md` apenas a linha nova foi acrescentada; texto da MIT copiado literalmente.
- Resultado: ok — evidência das auditorias (2026-08-01 12:52):
  `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (exit 0);
  `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos` (exit 0).

## [006] HANDOFF — 2026-08-01 12:52
- De: docs-writer#2 → Para: code-reviewer
- Status novo: in_review
- O que foi feito: ADR-0005 escrito e aceito; `LICENSE` (MIT) e `LICENSE-CONTENT`
  (CC BY-SA 4.0, bilíngue) criados na raiz; regra de compatibilidade de fontes propagada para
  `docs/content/content-standards.md` e `memory/context/content.md`; `README.md`,
  `memory/context/project-context.md` e `docs/product/roadmap.md` deixam de tratar a licença
  como decisão em aberto; auditorias verdes.
- Artefatos: `docs/adr/ADR-0005-project-license.md`, `LICENSE`, `LICENSE-CONTENT`,
  `docs/adr/README.md`, `docs/content/content-standards.md`, `memory/context/content.md`,
  `memory/context/project-context.md`, `README.md`, `docs/product/roadmap.md`.
- Como validar (checklist dos critérios 1–7):
  1. `docs/adr/ADR-0005-project-license.md` segue `docs/adr/adr-template.md`, `status:
     accepted`, decisor Douglas Silva, data 2026-08-01, com contexto, alternativas (CC BY 4.0
     · CC BY-SA 4.0 · CC0 · MIT · Apache-2.0 · AGPL-3.0), decisão e consequências. ✔
  2. `LICENSE` traz o texto integral da MIT, palavra por palavra, titular Douglas Silva,
     ano 2026 — conferir contra o texto canônico da OSI. ✔
  3. `LICENSE-CONTENT` declara CC BY-SA 4.0 para `content/`, com URL canônica e forma de
     atribuição esperada, em pt-BR e en-US, em seções separadas do mesmo arquivo. ✔
  4. A consequência de compatibilidade está no ADR de forma operacional (árvore Mermaid +
     tabela com as três fontes reais do nó piloto). ✔
  5. A regra aparece em `docs/content/content-standards.md` (seção própria + checklist de
     `published`) e em `memory/context/content.md` (decisões operacionais em vigor). ✔
  6. `README.md` e `memory/context/project-context.md` não listam mais a licença como decisão
     em aberto; o roadmap idem. ✔
  7. `bash scripts/audit-ai-surface.sh` → `Resultado: OK`; `bash scripts/audit-content.sh` →
     `0 erros · 0 avisos`. ✔
- Pendências e riscos:
  1. **Pendência para o `tech-lead` avaliar (não corrigida aqui, é escopo do TCK-0001):** as
     três referências do nó piloto são CC BY-NC-SA. Elas continuam **válidas como leitura
     externa**, mas alguém precisa confirmar explicitamente que nenhum trecho, exemplo,
     figura ou sequência didática delas foi incorporado a `theory.pt-BR.md`,
     `theory.en-US.md` ou `exercises.json` — e considerar registrar em `references.json` um
     campo que distinga fonte **adaptável** de fonte **apenas citável**, hoje inexistente no
     schema.
  2. Fonte gratuita em pt-BR compatível (não-NC) ainda não foi encontrada; o custo de produção
     autoral sobe. Registrado em `memory/context/project-context.md`.
  3. `README.md` ainda descreve o `ADR-0003` como `proposed` (linhas 7–10), o que ficou
     desatualizado com a aceitação no TCK-0003. **Não corrigi** por ser área de outro agente
     e para não colidir com edição em curso — vale um ticket ou uma linha no TCK-0003.
  4. Quando a aplicação for construída, o rodapé precisa exibir as duas licenças com link
     canônico (requisito registrado na seção "Impacto" do ADR-0005).
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 — todos
  entregues, pendentes de verificação independente.

## [007] ACTION — 2026-08-01 12:56 — docs-writer#2
- Ação: fechamento do protocolo de memória (não altera o status do ticket, que segue
  `in_review` com o `code-reviewer`). Registrada a lição **L-009**
  (`memory/lessons/share-alike-license-excludes-nc-sources.md`, tipo `sucesso`) e atualizados
  os índices `memory/LESSONS.md` e `memory/MEMORY.md`; notas persistentes e linha de execução
  acrescentadas em `memory/agents/docs-writer.md`.
- Motivo: AGENTS.md §5–6 — o aprendizado generalizável ("NC = leitura, não matéria-prima";
  regra normativa precisa sair do ADR e chegar ao praticante) é de interesse de outros
  agentes, não só deste.
- Resultado: ok — auditorias reexecutadas após as edições de memória:
  `bash scripts/audit-ai-surface.sh` → `Resultado: OK`;
  `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos`.

## [007] REJECT — 2026-08-01 12:59
- De: code-reviewer#4 → Para: docs-writer#2 · Loop nº: 1/3
- Escopo revisado (comandos): `git status --porcelain`; `git diff --stat`;
  `git diff -- <arquivo>` por artefato; `git diff --stat -- content/ docs/specs/
  docs/adr/ADR-0003-platform-stack.md tickets/TCK-0001* TCK-0002* TCK-0003*` (mudanças ali
  são dos tickets paralelos — confirmado nos logs de TCK-0001/0002/0003 —, **não** deste);
  conferência literal da MIT contra o texto canônico
  (`curl -sSL https://raw.githubusercontent.com/spdx/license-list-data/main/text/MIT.txt` e
  `curl -sSL https://opensource.org/license/mit`) com diff palavra a palavra em Python;
  `curl -sSI` nas três URLs da CC (200); paridade do `LICENSE-CONTENT` medida por seções e
  contagem; parser oficial do Mermaid 11 (`mermaid.parse`) nos dois diagramas;
  `bash scripts/audit-ai-surface.sh` (→ `Resultado: OK`, exit 0);
  `bash scripts/audit-content.sh` (→ `1 nós · 0 erros · 0 avisos`, exit 0);
  `grep -rn '^\*\*ID:\*\*' memory/lessons/` (L-009 sem colisão, seção `Sucesso` correta).

### Defeito bloqueante

**B1 — A regra "NC = leitura, não matéria-prima" não chegou às fontes canônicas de regra; nos
arquivos que o autor de conteúdo realmente carrega, o repositório continua dizendo o
contrário do `ADR-0005`.** (critério 5; e convenção do `AGENTS.md`: "Qualquer regra nova deve
ser adicionada AQUI")

Evidência — texto vigente hoje, já com o `ADR-0005` `accepted`:
- `AGENTS.md:234-236` (§9.6): "**Fontes externas:** só materiais **gratuitos**, com licença
  registrada em `references.json` (**preferência** por CC BY / CC BY-SA / domínio público)."
  Apresenta como *preferência* o que o `ADR-0005` transformou em **proibição**. Um autor que
  siga só esta regra pode incorporar OpenStax (CC BY-NC-SA) sem violar nenhuma instrução do
  repositório — e violar a licença que acabamos de declarar.
- `AGENTS.md:237-238` (§9.7): "quando adaptar algo licenciado, atribuir explicitamente e
  respeitar a licença (inclusive share-alike)" — lido isoladamente, autoriza adaptar
  **qualquer** material licenciado desde que se atribua. Não há ressalva de NC.
- `.github/instructions/content.instructions.md:20` (`applyTo: "content/**"`): "`references.json`:
  apenas fontes gratuitas, com autor, ano, URL, idioma e licença." É a regra auto-carregada
  **exatamente** ao editar `content/` em Copilot, Cursor, Windsurf, Antigravity, Zed, Cline e
  Junie, e não menciona compatibilidade de licença nem aponta para
  `docs/content/content-standards.md`.

Por que é bloqueante e não sugestão, com argumento:
(a) `AGENTS.md` se declara "o **arquivo-fonte único** de instruções", lido nativamente pelas 12
ferramentas; `docs/content/content-standards.md` **não** é carregado automaticamente por
nenhuma delas. Enquanto §9.6 disser "preferência", o próximo autor lê a regra, não o ADR.
(b) A lição `L-009`, escrita por esta mesma entrega
(`memory/lessons/share-alike-license-excludes-nc-sources.md:12-14`), afirma: "regra normativa
que mora só no ADR não é aplicada — ela precisa aparecer onde o praticante já lê". A entrega
contraria a própria lição que registra (protocolo §"Erro vira lição": repetir erro com lição
registrada é bloqueante).
(c) É o mesmo padrão já reprovado hoje no ticket paralelo (`TCK-0003`, defeito B1): decisão
aceita cuja propagação parou antes do `AGENTS.md` e das `.github/instructions/`.
(d) O custo é baixo e conhecido: `AGENTS.md` **não** é gerado (edição direta);
`.github/instructions/content.instructions.md` é fonte canônica e exige
`python3 scripts/sync-ai-adapters.py` + `bash scripts/audit-ai-surface.sh` depois — ambos
determinísticos e já verificados pela auditoria.

Correção esperada: reescrever `AGENTS.md` §9.6 (e a ressalva de §9.7) para a regra dura
("fonte com cláusula NC ou ND só pode ser **citada**, nunca incorporada nem traduzida —
`ADR-0005`"), acrescentar a mesma linha em `.github/instructions/content.instructions.md`,
rodar `python3 scripts/sync-ai-adapters.py` e reexecutar as duas auditorias. Ao resolver,
a `ACTION` termina com `Lição: L-009`.

### Sugestões (não bloqueiam)

- **S1.** `docs/adr/ADR-0005-project-license.md:133` e `docs/content/content-standards.md`
  afirmam o *Livro Aberto de Matemática* como `CC BY-NC-SA` sem registrar a divergência que o
  `TCK-0001` documentou em `content/high-school/algebra/quadratic-equations/references.json`
  ("a página do projeto declara 'BY-NC-SA' e o selo do colofão do PDF mostra apenas BY-SA").
  A conclusão está certa (`L-007`: na dúvida, a leitura mais restritiva), mas o ADR a
  apresenta como fato verificado; sem a nota, ninguém consegue reabrir a questão depois — e
  reabrir vale a pena, porque BY-SA sem NC tornaria a única fonte pt-BR **adaptável**.
- **S2.** A árvore (`ADR-0005:115` e `content-standards.md`) manda "PODE ADAPTAR" para
  **domínio público** sem ressalva de jurisdição: domínio público é territorial (prazo no
  Brasil ≠ EUA) e a etiqueta é frequentemente errada em agregadores. Uma linha na leitura do
  diagrama resolve.
- **S3.** `LICENSE-CONTENT` não diz qual texto prevalece. As seções pt-BR/en-US são um
  **resumo** da licença; convém uma linha declarando que, em caso de divergência, vale o
  `legalcode` em https://creativecommons.org/licenses/by-sa/4.0/legalcode.
- **S4.** `L-009`, `memory/LESSONS.md` e `memory/MEMORY.md` foram alterados por esta entrega
  mas não aparecem em "Artefatos" das entradas [005]/[006] ("log ou não aconteceu").

### Decisão de escopo registrada (`README.md:7-10`, `ADR-0003` ainda `proposed`)

**Não é defeito deste ticket** — é pendência do `TCK-0003`. Razões: (a) o requisito refinado e
os sete critérios do `TCK-0004` tratam só de licença; (b) o critério 5 do `TCK-0003` cobre
literalmente "nada mais descreve `ADR-0003` como decisão em aberto"; (c) editar, num working
tree compartilhado, a linha de uma decisão que outra cadeia está propagando cria dois donos
para a mesma linha. A conduta do `docs-writer#2` (reportar em vez de corrigir) está correta e
alinhada à nota que ele registrou na própria memória. **Atenção:** o `REJECT` do `TCK-0003`
lista `AGENTS.md`, `.github/instructions/`, `.claude/agents/` e o roadmap, mas **não** lista
`README.md:7-10` — fica aqui o registro para o `tech-lead` encaminhar àquela cadeia.

### O que já está bom (não refazer)

- **`LICENSE` (critério 2): MIT literal, confirmado mecanicamente.** Diff palavra a palavra
  contra o texto canônico SPDX e contra o corpo publicado pela OSI: **169 palavras em ambos,
  zero diferenças** após normalizar apenas espaçamento, aspas tipográficas e o placeholder
  `<year> <copyright holders>` → `2026 Douglas Silva`. Nenhuma cláusula omitida, disclaimer
  íntegro. A nota de escopo vem **depois** do separador `---`, sem tocar no texto legal.
- **`LICENSE-CONTENT` (critério 3): paridade bilíngue real.** 6 seções em pt-BR e 6 em en-US,
  uma a uma equivalentes; 433 vs 426 palavras; a URL canônica
  `https://creativecommons.org/licenses/by-sa/4.0/` aparece 4× em cada idioma; 2 modelos de
  atribuição (com e sem alteração) em cada; regra de NC nos dois. As três URLs da CC
  respondem `HTTP/2 200` (canônica, `deed.pt-br` e `legalcode`).
- **`ADR-0005` (critérios 1 e 4):** segue `docs/adr/adr-template.md` (status `accepted`,
  decisor Douglas Silva, data 2026-08-01, contexto, alternativas com prós/contras para
  conteúdo e código, decisão, consequências, impacto, reversão). A afirmação jurídica central
  — NC é mais restritivo que CC BY-SA, logo material NC não pode ser absorvido — está
  **correta** e não é otimista; a tabela usa as três fontes reais do nó piloto, coerentes com
  `references.json`. Os dois diagramas Mermaid **passam no parser oficial** (mermaid 11) e
  trazem leitura curta, o que o diagrama não cobre, fontes e marcação de estado atual
  (`docs/DOC-STANDARDS.md`).
- **Critério 6 e escopo:** `README.md:111-125` e `memory/context/project-context.md` não
  listam mais a licença como decisão em aberto. `content/`, `references.json`, `docs/specs/`,
  `ADR-0003` e os tickets TCK-0001/0002/0003 **não** foram tocados por este ticket;
  `docs/adr/README.md` recebeu apenas a linha do `ADR-0005`.
- **Critério 7:** as duas auditorias reexecutadas por mim seguem verdes.
- Refazer apenas o que B1 pede; o resto do diff está aprovado.

## [008] ACTION — 2026-08-01 13:16 — docs-writer#2
- Ação: resolvido o defeito bloqueante **B1** do `[007] REJECT` — a regra de compatibilidade
  saiu do ADR e entrou nas fontes canônicas de regra, que são o que as 12 ferramentas
  carregam sozinhas:
  - **`AGENTS.md` §9** reescrito: a antiga §9.6 ("preferência por CC BY / CC BY-SA / domínio
    público") virou regra de registro de fonte; entrou uma **§9.7 nova, imperativa** —
    "Compatibilidade de licença (`ADR-0005`) — regra dura, não preferência", com as duas
    listas fechadas (**adaptável**: CC BY, CC BY-SA, CC0, domínio público; **só citável**:
    CC BY-NC, CC BY-NC-SA, ND e fonte sem licença declarada), a proibição explícita de copiar
    ou traduzir trecho, exemplo, figura, enunciado ou sequência didática para
    `theory.<lang>.md` / `exercises.json` / `assessments.json`, a regra da leitura mais
    restritiva em caso de ambiguidade (`L-007`) e o mnemônico "NC = leitura, não
    matéria-prima". A antiga §9.7 (sem plágio) virou **§9.8** e agora remete à §9.7 em vez de
    autorizar "adaptar algo licenciado" de forma aberta. Renumeração conferida: as citações
    existentes a "§9.6" (fontes) continuam corretas e "§9.6–9.7" passa a apontar exatamente
    para fontes + compatibilidade.
  - **`.github/instructions/content.instructions.md`** (`applyTo: content/**`, auto-carregada
    ao editar `content/` em Copilot, Cursor, Windsurf, Antigravity, Zed, Cline e Junie):
    licença agora precisa ser "lida na própria página" (`L-006`/`L-007`) e entrou item novo
    com a regra de compatibilidade completa, apontando para
    `docs/content/content-standards.md`.
  - **`.github/instructions/core.instructions.md`** (regra de escopo amplo): a regra 9 passou
    a declarar as duas licenças do projeto e a distinção adaptável × só citável.
  - **`.claude/agents/content-author.md`** (regras duras) e **`.claude/agents/researcher.md`**
    (o agente que classifica fontes: agora precisa dizer no relatório "adaptável" ou "leitura
    externa"), para que o executor da tarefa leia a regra sem depender do ADR.
  - **`prompts/bootstrap-session.md`** (ferramentas web) e **`CONTRIBUTING.md`** (checklist de
    conteúdo), fechando o caminho de quem chega de fora.
- Motivo: B1 do `code-reviewer#4` — enquanto o `AGENTS.md` dissesse "preferência", incorporar
  OpenStax (CC BY-NC-SA) seguiria permitido pelas instruções vigentes, contrariando o
  `ADR-0005` recém-aceito. É o mesmo padrão de defeito do `TCK-0003` (lição `L-010`).
- Sugestões: **S1 acatada** — `ADR-0005` ganhou nota própria sobre o *Livro Aberto de
  Matemática* registrando a divergência (página do projeto: BY-NC-SA; colofão do PDF: BY-SA),
  a aplicação de `L-007` (vale a mais restritiva) e por que reabrir vale a pena (seria a única
  fonte pt-BR adaptável); a linha da tabela passou a "(declaração divergente — ver nota)" e
  `docs/content/content-standards.md` recebeu a mesma ressalva. **S2 acatada** — ressalva de
  jurisdição ("domínio público é territorial; prazo no Brasil ≠ EUA; etiqueta de agregador
  erra") na leitura do diagrama do ADR, no padrão de conteúdo, no `AGENTS.md` §9.7 e nas
  instructions. **S3 acatada** — `LICENSE-CONTENT` declara, nos dois idiomas, que as seções são
  resumo em linguagem comum e que prevalece o `legalcode` em caso de divergência ou omissão.
  **S4 acatada** — os artefatos de memória (`L-009`, `memory/LESSONS.md`, `memory/MEMORY.md`)
  estavam na entrada `[007] ACTION` da entrega anterior, mas não na lista de "Artefatos" de
  `[005]`/`[006]`; ficam listados agora no `[009] HANDOFF`, com o adendo novo de `L-009`.
- `L-009` atualizada com o adendo do próprio REJECT: a checklist de 7 pontos que define quando
  uma regra normativa está de fato propagada (AGENTS.md → instructions do escopo + core →
  documento do praticante + checklist → memória da área → agent que executa → bootstrap e
  CONTRIBUTING → sync + auditorias). Linha correspondente ajustada em `memory/LESSONS.md`.
- Evidência (2026-08-01 13:16):
  - `python3 scripts/sync-ai-adapters.py` → "20 skills + 21 agents + 6 regras → adapters
    sincronizados (Claude, Copilot, Gemini, Cursor, Antigravity, Windsurf). 9 arquivo(s)
    escrito(s)/atualizado(s)." (exit 0); `--check` posterior → "Tudo já estava atualizado."
  - `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (exit 0), incluindo "Limite de 12.000
    caracteres nas regras (Antigravity/Windsurf): todas dentro do limite" e "Adapters gerados
    atualizados: up-to-date".
  - `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos` (exit 0).
  - Regra presente nos gerados (`grep -rl 'NC = leitura\|só citável'`): `.cursor/rules/
    {content.mdc,core.mdc}`, `.windsurf/rules/{content.md,core.md}`, `.agents/rules/
    {content.md,core.md}`, `.rules`, `.clinerules`, `.junie/guidelines.md`.
- **Aviso ao revisor sobre concorrência:** o sync regenerou também `.agents/rules/app.md`,
  `.cursor/rules/app.mdc`, `.windsurf/rules/app.md` e as partes de `app` em `.rules`,
  `.clinerules` e `.junie/guidelines.md`, que carregam mudanças de
  `.github/instructions/app.instructions.md` feitas pela cadeia do **TCK-0003** (o
  `platform-architect` foi instruído a não rodar o sync). Essas linhas do diff **não são
  deste ticket**. Nada foi tocado em `docs/adr/ADR-0003-platform-stack.md`,
  `docs/architecture/`, `memory/context/frontend.md`, `content/`, `references.json`,
  `docs/specs/` ou nos tickets TCK-0001/0002/0003/0005.
- Resultado: ok — B1 resolvido, S1–S4 acatadas. Lição: L-009

## [009] HANDOFF — 2026-08-01 13:16
- De: docs-writer#2 → Para: code-reviewer
- Status novo: in_review
- O que foi feito: correção do REJECT loop 1/3. A regra "NC = leitura, não matéria-prima"
  agora é imperativa no `AGENTS.md` (§9.7 nova), nas instruções auto-carregadas de `content/`
  e de escopo amplo, nos agents `content-author` e `researcher`, no prompt de sessão das
  ferramentas web e no checklist do `CONTRIBUTING.md`; adapters das 12 ferramentas
  regenerados. Sugestões S1–S4 acatadas.
- Artefatos (ticket completo, incluindo os de memória — S4):
  - Criados: `docs/adr/ADR-0005-project-license.md`, `LICENSE`, `LICENSE-CONTENT`,
    `memory/lessons/share-alike-license-excludes-nc-sources.md` (L-009).
  - Fontes canônicas de regra: `AGENTS.md` (§9.6–9.8),
    `.github/instructions/content.instructions.md`,
    `.github/instructions/core.instructions.md`, `.claude/agents/content-author.md`,
    `.claude/agents/researcher.md`.
  - Documentação e produto: `docs/adr/README.md` (só a linha do ADR-0005),
    `docs/content/content-standards.md`, `docs/product/roadmap.md`, `README.md`,
    `CONTRIBUTING.md`, `prompts/bootstrap-session.md`.
  - Memória: `memory/context/content.md`, `memory/context/project-context.md`,
    `memory/LESSONS.md`, `memory/MEMORY.md`, `memory/agents/docs-writer.md`.
  - Gerados pelo sync (não editar à mão): `.cursor/rules/*`, `.windsurf/rules/*`,
    `.agents/rules/*`, `.rules`, `.clinerules`, `.junie/guidelines.md` — ver o aviso de
    concorrência em `[008]` sobre as partes de `app`.
- Como validar:
  - **B1:** `grep -n "só citável\|NC = leitura" AGENTS.md .github/instructions/*.md` deve
    mostrar a regra imperativa; conferir que `AGENTS.md` §9.6 não fala mais em "preferência" e
    que §9.8 (sem plágio) remete à §9.7; `python3 scripts/sync-ai-adapters.py --check` →
    "Tudo já estava atualizado"; `bash scripts/audit-ai-surface.sh` → `Resultado: OK`;
    `bash scripts/audit-content.sh` → `0 erros · 0 avisos`.
  - **S1–S3:** nota do *Livro Aberto* no `ADR-0005` e no padrão de conteúdo; ressalva de
    jurisdição de domínio público nos dois; cláusula de prevalência do `legalcode` nas duas
    seções do `LICENSE-CONTENT`.
  - **Critérios 1–7:** inalterados em relação ao `[006]`, e já aprovados em `[007]` ("o que já
    está bom") exceto o critério 5, que agora inclui as fontes canônicas de regra.
- Pendências e riscos (para o `tech-lead`):
  1. **TCK-0001:** confirmar que nenhum trecho das três fontes NC do nó piloto foi incorporado
     ao texto autoral, e avaliar um campo em `references.json` que distinga fonte **adaptável**
     de **apenas citável** — hoje o schema não expressa isso, e a regra passou a depender dele.
  2. **Livro Aberto (S1):** vale abrir trabalho para esclarecer a licença com IMPA/OBMEP; se
     for BY-SA sem NC, o projeto ganha a única fonte pt-BR adaptável conhecida.
  3. Nenhuma fonte gratuita em pt-BR compatível está disponível hoje: custo de produção
     autoral maior (registrado em `memory/context/project-context.md`).
  4. Rodapé da aplicação precisará exibir as duas licenças com link canônico (`ADR-0005`,
     seção Impacto).
  5. `README.md:7-10` (`ADR-0003` como `proposed`) — o revisor confirmou que é pendência do
     `TCK-0003` e que o `REJECT` daquele ticket não a lista. Encaminhar àquela cadeia.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 (agora incluindo `AGENTS.md` e as
  `.github/instructions/`) · [x] 6 · [x] 7.

## [010] HANDOFF — 2026-08-01 13:23
- De: code-reviewer#4 → Para: qa-validator
- Status novo: in_validation
- O que foi feito: revisão do loop 2/3. **B1 resolvido** e verificado de forma independente:
  a regra de compatibilidade é agora imperativa em `AGENTS.md` §9.7 (nova), com listas
  fechadas de adaptável × só citável, proibição explícita de copiar/traduzir para
  `theory.<lang>.md` / `exercises.json` / `assessments.json` e a regra da leitura mais
  restritiva; §9.6 deixou de falar em "preferência" e passou a exigir licença **lida na
  própria página**; §9.8 (sem plágio) remete à §9.7 em vez de autorizar adaptação genérica.
  S1–S4 acatadas. Aprovo para validação: os sete critérios estão materializados e a evidência
  abaixo é reprodutível.
- Artefatos revisados: os do `[009]`, mais os gerados pelo sync.
- Evidência da revisão (comandos reexecutados por mim, não copiados do log):
  1. **Renumeração — o ponto de maior risco desta correção.**
     `grep -rn "§9\.[0-9]" . --exclude-dir=.git` → **30 ocorrências, nenhuma quebrada.**
     Conferidas uma a uma: `docs/adr/ADR-0005:127` e `docs/content/content-standards.md:76`
     citam "§9.6–9.7", que agora aponta exatamente para *fontes* + *compatibilidade* (antes
     apontava para fontes + sem plágio) — a citação ficou **mais** correta, não menos;
     `tickets/TCK-0001/{ticket.md:26,56, log.md:10,65}` citam §9.6 no sentido de "licença
     verificada na própria página", que é justamente o que a nova §9.6 exige;
     `tickets/TCK-0004/ticket.md:71` ("§9.6 e §9.7") resolve para fontes + compatibilidade.
     As demais são §9.2 (acessibilidade, seção intocada) ou logs históricos append-only.
     Complementos: `grep -rn "AGENTS.md.*9\.[6-8]\|seção 9\.[6-8]"` sem `§` → vazio;
     `grep -rn "preferência por CC BY"` → só dentro da narrativa histórica da própria `L-009`.
  2. **Propagação real, não declarada.** `grep -rln "NC = leitura\|só citável"` → 22 arquivos,
     cobrindo `AGENTS.md`, `.github/instructions/{content,core}.instructions.md`,
     `.claude/agents/{content-author,researcher}.md`, `prompts/bootstrap-session.md`,
     `CONTRIBUTING.md`, `docs/`, `memory/` **e** os gerados
     (`.cursor/rules/{content,core}`, `.windsurf/rules/{content,core}`,
     `.agents/rules/{content,core}`, `.rules`, `.clinerules`, `.junie/guidelines.md`).
  3. **Gerado == fonte.** Script em Python conferindo linha a linha: **0 linhas** de
     `.github/instructions/content.instructions.md` ausentes em `.cursor/rules/content.mdc`,
     `.windsurf/rules/content.md` e `.agents/rules/content.md`; nenhum gerado afirma o que a
     fonte não afirma. Os adapters de agent (`.github/chatmodes/*`, `.gemini/commands/*`,
     `.claude/commands/*`) são ponteiros de ~25 linhas para `.claude/agents/<nome>.md` — a
     edição de `content-author`/`researcher` chega a eles por referência, sem cópia.
  4. `python3 scripts/sync-ai-adapters.py --check` → "Tudo já estava atualizado." (exit 0);
     `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (exit 0);
     `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos` (exit 0).
  5. **Critério 2 reconferido após as edições:** `LICENSE` segue com a MIT literal — diff
     palavra a palavra contra o SPDX, **169 palavras dos dois lados, zero diferenças**.
  6. **Critério 3 reconferido após S3:** paridade mantida — 6 seções pt-BR ↔ 6 en-US, 494 vs
     486 palavras, URL canônica 5× em cada idioma, e a cláusula de prevalência do `legalcode`
     existe **nos dois** (`LICENSE-CONTENT:25` e `:111`), na mesma posição relativa.
  7. Os dois blocos Mermaid seguem válidos no parser oficial (mermaid 11, `mermaid.parse`).
  8. **Escopo:** `content/`, `references.json`, `docs/specs/`, `ADR-0003` e os tickets
     TCK-0001/0002/0003/0005 não têm impressão digital deste ticket
     (`grep -rn "ADR-0005\|CC BY-SA" content/` → vazio). O ruído de `app` nos gerados e as
     linhas de stack em `core.instructions.md` / `bootstrap-session.md` vêm da cadeia do
     TCK-0003, como avisado em `[008]`.
- **Verificação jurídica que me cabia (critério 4), feita na fonte e não de memória:**
  - **"CC BY-SA → adaptável, derivado sai sob CC BY-SA 4.0" está correto, inclusive entre
    versões.** `curl -sSL https://creativecommons.org/licenses/by-sa/3.0/legalcode`, §4(b):
    "You may Distribute or Publicly Perform an Adaptation only under: (i) the terms of this
    License; (ii) **a later version of this License with the same License Elements**…" — ou
    seja, material BY-SA 1.0–3.0 (inclusive versões de jurisdição) pode legalmente ser
    adaptado e publicado sob BY-SA 4.0. Em 4.0, §3(b) admite "BY-SA 4.0, later version ou
    BY-SA Compatible License". A regra dura não tem furo de versão.
  - **CC BY → BY-SA:** correto; CC BY 4.0 permite licenciar o derivado sob quaisquer termos,
    inclusive share-alike. **CC0 / domínio público:** correto, com a ressalva de
    territorialidade que a S2 acrescentou.
  - **ND:** a árvore pergunta "permite derivados?" e responde "não" — isso está **certo**;
    ND proíbe distribuir material adaptado. Ver sugestão SG1 sobre a imprecisão residual.
- Pendências e riscos herdados (para o `qa-validator` repassar ao `tech-lead`, não são
  bloqueio deste ticket): as cinco listadas em `[009]`, com destaque para (1) `references.json`
  não ter campo que distinga **adaptável** de **apenas citável** — a regra nova depende de um
  schema que ainda não a expressa — e (5) `README.md:7-10` (`ADR-0003` como `proposed`),
  pendência do TCK-0003 conforme decisão de escopo registrada em `[007]`.
- Sugestões de refinamento (não bloqueiam, não devolvem o ticket):
  - **SG1 — precisão sobre ND.** `AGENTS.md` §9.7 e a árvore do `ADR-0005` colocam ND ao lado
    de NC em "só citável". A conclusão operacional está certa e é conservadora, mas a razão é
    diferente: CC BY-ND **permite** redistribuição verbatim, inclusive comercial — o que ela
    proíbe é distribuir material **adaptado**. Nós o excluímos por decisão de projeto
    (`content/` é declarado uniformemente CC BY-SA e não há campo de licença por asset), não
    por proibição da licença. Registrar essa distinção em uma linha evita que alguém "descubra"
    a imprecisão daqui a seis meses e reabra a regra inteira.
  - **SG2 — `Como reverter` do `ADR-0005` ficou incompleto depois desta mudança.** O texto
    condiciona a relicenciar apenas à ausência de **contribuição externa**; agora que adaptar
    fonte **CC BY-SA de terceiros** é explicitamente autorizado, o share-alike dessa fonte
    também trava a relicença. Uma oração resolve.
  - **SG3 — adendo da `L-009`: bom, e a melhor parte da entrega.** A checklist de 7 pontos é
    verificável, cita o sync e as auditorias como último passo e nomeia o ticket irmão que
    falhou igual (`TCK-0003`) — é o tipo de lição que de fato impede a terceira ocorrência.
    Falta-lhe um oitavo item, revelado por este próprio loop: quando a regra **renumera** uma
    seção do `AGENTS.md`, conferir as referências cruzadas (`grep -rn "§9\.[0-9]"`) — desta
    vez estava certo, mas por sorte de numeração, não por checagem prevista.
  - **SG4 — "Citar uma fonte NC é sempre legítimo"** (`ADR-0005:149`,
    `content-standards.md:79`): trocar por "citar = referência bibliográfica + link, sem
    transcrever" fecha a brecha de alguém entender "citar" como "transcrever um trecho entre
    aspas".
- Critérios de aceite (verificados, não aceitos do log): [x] 1 · [x] 2 · [x] 3 · [x] 4 ·
  [x] 5 · [x] 6 · [x] 7 — a validação final contra os critérios é do `qa-validator`.

## [011] HANDOFF — 2026-08-01 13:31
- De: qa-validator#5 → Para: tech-lead
- Status novo: **done**
- O que foi feito: validação independente dos sete critérios de aceite. Toda a evidência
  abaixo foi **reproduzida por mim** (comando reexecutado neste working tree), não herdada do
  `[006]`, do `[009]` nem do `[010]`. Nenhum defeito bloqueante; 4 dívidas registradas.
- **Ambiente da validação:** commit `f96baa9` (o `21f6ef1` avançou para `f96baa9` durante a
  validação — commit do TCK-0005, que toca `content/`, memórias de agente e o próprio
  TCK-0005; **nenhum artefato deste ticket foi afetado**: `LICENSE`, `LICENSE-CONTENT`,
  `docs/adr/ADR-0005-project-license.md` seguem untracked `??`). Branch `main`, working tree
  compartilhado com TCK-0003 e TCK-0005 em validação. Ferramentas: `curl 8.5.0` (com rede),
  `python3`, `node v24.14.1`, `mermaid 11.16.0` + `jsdom` instalados no scratchpad.
  Auditorias reexecutadas **imediatamente antes** deste veredito, às 13:31.
- **Validação documental (sem UI):** este ticket entrega arquivos de licença, ADR e regras de
  agente. Não há interface, componente nem rota — a bateria de casos hostis (offline, tema
  claro/escuro, zoom 200%, navegação por teclado, leitor de tela, rede lenta, dados vazios)
  **não é aplicável**, e isso é sustentado por checagem, não por suposição: `grep -rn
  "LICENSE\|LICENSE-CONTENT" --include='*.ts' --include='*.tsx' --include='*.astro'` não tem
  onde rodar (não existe código de aplicação no repositório) e nenhum artefato deste ticket é
  consumido em runtime. Os dois idiomas **são** validados, porque o `LICENSE-CONTENT` é
  bilíngue — ver critério 3. O requisito de rodapé com as duas licenças fica registrado como
  pendência para quando a aplicação existir.

### Checklist de critérios — evidência item a item

**[x] Critério 1 — `docs/adr/ADR-0005-project-license.md` no padrão do template,
`status: accepted`, decisor e data.**
Comparação programática do arquivo contra `docs/adr/adr-template.md`: as 6 seções `##` do
template (`Contexto`, `Alternativas consideradas`, `Decisão`, `Consequências`, `Impacto`,
`Como reverter`) estão **todas presentes**, "SEÇÕES DO TEMPLATE AUSENTES: nenhuma"; há 1
seção extra (`## Consequência operacional: compatibilidade de fontes externas`), acréscimo,
não desvio. Front matter: `- **Status:** accepted` · `- **Data:** 2026-08-01` ·
`- **Decisores:** Douglas Silva` · `- **Relacionados:** …`. As 3 subseções obrigatórias de
`Consequências` (`Positivas`, `Negativas / custos assumidos`, `O que fica mais difícil depois
desta decisão`) e os 3 bullets de `Impacto` (`Conteúdo (content/)`, `Plataforma`,
`Processo/agentes`) conferidos por regex. Indexado em `docs/adr/README.md:15` como
`accepted | 2026-08-01`. Os 2 blocos Mermaid validados **por mim** no parser oficial
(mermaid 11.16.0 + jsdom, `mermaid.parse`): ambos `VALIDO`, `diagramType = flowchart-v2`,
exit 0 — e ambos acompanhados de leitura curta, do que o diagrama não cobre e de fontes,
como exige `docs/DOC-STANDARDS.md`.

**[x] Critério 2 — `LICENSE` com a MIT integral e literal (Douglas Silva, 2026).**
Conferido por mim, palavra por palavra, contra a fonte canônica:
`curl -sSL https://raw.githubusercontent.com/spdx/license-list-data/main/text/MIT.txt`
(exit 0, 169 palavras). Isolei a parte legal do `LICENSE` (tudo antes do separador `---`),
normalizei apenas espaçamento/aspas tipográficas e substituí o placeholder
`<year> <copyright holders>` por `2026 Douglas Silva`. Resultado:
**169 palavras no SPDX, 169 no `LICENSE`, `IDÊNTICO palavra a palavra: True`** — `difflib`
não produziu uma única linha de diferença. Checagem redundante de cláusula, uma a uma, todas
`OK`: concessão ("Permission is hereby granted", "free of charge", "without restriction",
"sublicense, and/or sell"), cláusula de aviso ("The above copyright notice and this
permission notice shall be included in all copies or substantial portions of the Software")
e o **disclaimer íntegro** (`THE SOFTWARE IS PROVIDED "AS IS"…`, `MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT`, `IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE`, `WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE`). Nenhuma omissão,
nenhuma alteração. Titular: `Copyright (c) 2026 Douglas Silva`. A nota de escopo (406 chars)
vem **depois** do separador `---`, sem tocar no texto legal.

**[x] Critério 3 — `LICENSE-CONTENT`: CC BY-SA 4.0 para `content/`, URL canônica, forma de
atribuição, pt-BR e en-US em seções separadas com paridade real.**
Recorte programático do arquivo nos dois blocos: **6 seções `##` em pt-BR e 6 em en-US, na
mesma ordem e uma a uma equivalentes** (cobre → NÃO cobre → você pode → condições →
atribuição → contribuir). Volume: 494 vs 486 palavras (razão 1,02). A URL canônica
`https://creativecommons.org/licenses/by-sa/4.0/` aparece **5× em cada idioma**; `content/`
6×/6×; a cláusula de prevalência do `legalcode` 3×/3×; a regra de NC 2×/2×; **2 modelos de
atribuição em cada idioma** (uso sem alteração e uso com alteração), com os cinco elementos
(título, autoria, URL, licença com link, alterações). Escopo declarado no topo de cada bloco
e cobrindo `content/` explicitamente. As 3 URLs da CC verificadas por mim com
`curl -sS -o /dev/null -w "%{http_code}" -L`: canônica **200**, `deed.pt-br` **200**,
`legalcode` **200**.

**[x] Critério 4 — o ADR registra a compatibilidade de forma operacional, com os exemplos
reais do repositório.**
A regra está em seção própria (`## Consequência operacional…`) em três formas redundantes:
árvore Mermaid validada, tabela e regra prática. As listas conferem com o critério: **CC BY,
CC BY-SA, CC0 e domínio público → adaptável** (derivado sai sob CC BY-SA 4.0); **CC BY-NC e
CC BY-NC-SA → só citável**. Os exemplos são reais, e isso eu confirmei **na fonte, não no
ADR**: `python3` lendo
`content/high-school/algebra/quadratic-equations/references.json` devolve exatamente os três
itens da tabela — `Algebra and Trigonometry 2e` → `CC BY-NC-SA 4.0`; `Intermediate Algebra
2e` → `CC BY-NC-SA 4.0`; `Livro Aberto de Matemática` → `CC BY-NC-SA (versão não declarada;
leitura mais restritiva — a página do projeto declara 'BY-NC-SA' e o selo do colofão do PDF
mostra apenas BY-SA)`. A nota de divergência do ADR (linhas 139–147) reproduz fielmente o que
está no campo `license` do próprio `references.json`, inclusive a aplicação de `L-007`.

**[x] Critério 5 — a regra aparece onde o autor de conteúdo a lê.**
`docs/content/content-standards.md`: seção `## Licença e compatibilidade de fontes` com
árvore Mermaid (validada), leitura, ressalva de territorialidade do domínio público, a regra
prática e os três exemplos reais nomeados; e item novo no `## Checklist antes de marcar
published` (`- [ ] Nenhum trecho de fonte **NC** (CC BY-NC / CC BY-NC-SA) incorporado ou
traduzido no texto`). `memory/context/content.md:64-70`: "**Licença do conteúdo: CC BY-SA
4.0** … fonte **CC BY-NC** ou **CC BY-NC-SA** **não** pode ser incorporada nem traduzida
para dentro de `theory.<lang>.md` / `exercises.json` — só citada como leitura externa".
Verificação de alcance real em `### Verificação própria B` abaixo.

**[x] Critério 6 — `README.md` e `memory/context/project-context.md` não listam mais a
licença como decisão em aberto.**
`README.md:113-126`: seção `## Licença` com tabela declarando **CC BY-SA 4.0 para `content/`**
e **MIT para código e processo**, com link para `LICENSE-CONTENT`, `LICENSE` e o `ADR-0005`;
busca negativa `grep -ni "em aberto\|não decidid\|pendente" README.md` → **vazio**.
`memory/context/project-context.md`: a licença está em **"Decisões aceitas"** (linhas 31–35,
`ADR-0005`, decisor e data) e em "Documentação" (linha 18, "**Licença definida**"); li o
bloco `## Decisões em aberto` inteiro (linhas 37–44) — ele lista sincronização de progresso,
fóruns/certificados e biblioteca de UI/testes/service worker, e **não** menciona licença.

**[x] Critério 7 — auditorias sem erros.**
Reexecutadas por mim às 13:31, com exit code capturado **sem pipe** (nota da minha memória —
com `| tail` o `$?` seria do `tail`):
`bash scripts/audit-ai-surface.sh` → `Resultado: OK`, **EXIT=0** (inclui "Limite de 12.000
caracteres nas regras (Antigravity/Windsurf): todas dentro do limite" e "Adapters gerados
atualizados: up-to-date"); `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros ·
0 avisos`, **EXIT=0**. Alcance declarado: `audit-content.sh` valida *presença* de campos, não
faz rede nem valida formato de licença — verde é necessário, não suficiente; por isso as
fontes e URLs foram conferidas à mão acima.

### Verificação própria A — a regra é imperativa e chegou às fontes canônicas

`python3 scripts/sync-ai-adapters.py --check` → "Tudo já estava atualizado.", **EXIT=0**.

`AGENTS.md` §9.7 (lido integralmente via `awk '/^## 9\./,/^## 10\./'`) é **imperativo, não
preferência**: o título é literalmente "**Compatibilidade de licença (`ADR-0005`) — regra
dura, não preferência**", com duas listas fechadas ("Adaptável" × "**Só citável**"), a
proibição explícita "**proibido copiar ou traduzir trecho, exemplo, figura, enunciado ou
sequência didática** para `theory.<lang>.md`, `exercises.json` ou `assessments.json`", a
regra da leitura mais restritiva (`L-007`) e o mnemônico. §9.6 não fala mais em "preferência"
(passou a exigir licença "lida na própria página"); §9.8 (sem plágio) remete à regra 7 em vez
de autorizar adaptação genérica. **Teste do enunciado do REJECT:** um agente que leia só o
`AGENTS.md` encontra `CC BY-NC-SA` **nominalmente** na lista "Só citável" — como as duas
referências OpenStax do nó piloto são CC BY-NC-SA (verificado por mim no `references.json`),
a conclusão "não posso adaptar OpenStax" é **forçada, sem ambiguidade e sem depender do ADR**.

`.github/instructions/content.instructions.md` confirmado com `applyTo: "content/**"`
(linha 2) e com a regra completa nas linhas 22–28, incluindo `ND` e "sem licença declarada".
`core.instructions.md` (`applyTo: "**"`) carrega a mesma regra na regra 9.

**Propagação medida, não declarada:** `grep -rln "NC = leitura\|só citável\|Só citável"` →
**23 arquivos**, cobrindo `AGENTS.md`, as duas instructions, `.claude/agents/content-author.md`
e `.claude/agents/researcher.md`, `prompts/bootstrap-session.md`, `CONTRIBUTING.md`, `docs/`,
`memory/` e todos os gerados. Conferência gerado==fonte feita por mim com 5 frases-chave da
fonte: `.cursor/rules/content.mdc`, `.windsurf/rules/content.md` e `.agents/rules/content.md`
contêm **as 5**; `.rules`, `.clinerules` e `.junie/guidelines.md` derivam de `core`, não de
`content`, e carregam a versão condensada — que é igualmente imperativa: "fonte **CC BY-NC,
CC BY-NC-SA, ND ou sem licença** é **só citável** — nunca incorporada nem traduzida para
dentro do conteúdo" (linha 43 dos três).

### Verificação própria B — renumeração §9.6/§9.7/§9.8 (o risco central)

`grep -rn "§9\.[0-9]" . --exclude-dir=.git` → **49 ocorrências** (o revisor contou 30 em
`[010]`; o crescimento vem dos logs escritos depois, inclusive o dele). Classifiquei
**todas**, uma a uma:
- **Falsos positivos (2):** `ADR-0005:135` e `TCK-0001/log.md:85` — "§9.3" é seção do livro
  da OpenStax, não do `AGENTS.md`.
- **§9.2 (acessibilidade), seção intocada por este ticket (10):**
  `memory/lessons/formula-description-…:9`, `TCK-0002/{log.md:304, ticket.md:129}`,
  `TCK-0005/{log.md:10,44,514,524,571,770,777, ticket.md:23,28,72,130}`. Confirmei no
  `git diff -- AGENTS.md` que o hunk da seção 9 altera **apenas** os itens 6–8; os itens 1–5
  não aparecem no diff.
- **Referências vivas a §9.6/§9.7 (4) — todas resolvem para a seção certa:**
  `ADR-0005:127` e `content-standards.md:76` citam "`AGENTS.md` §9.6–9.7" como fonte da regra
  de fontes + compatibilidade — que é exatamente o par atual (antes apontava para fontes +
  sem plágio, ou seja, a citação ficou **mais** correta); `TCK-0004/ticket.md:71` ("Regra de
  fontes: `AGENTS.md` §9.6 e §9.7") idem; `TCK-0001/{ticket.md:26,56, log.md:10,65}` citam
  §9.6 no sentido de "licença verificada na própria página", que é o que a nova §9.6 exige
  literalmente.
- **Narrativa histórica em log append-only ou linha de execução de memória (o restante):**
  `TCK-0004/log.md` (descreve a própria mudança), `TCK-0003/log.md:380,498` ("§9.6/§9.7 não
  foram tocados **por esta cadeia**" — continua verdadeiro), `memory/agents/code-reviewer.md:164`
  e `memory/agents/docs-writer.md:72`.
**Nenhuma referência cruzada quebrada.** Buscas complementares próprias: referências à seção 9
**sem** o símbolo `§` (`grep -rniE "(AGENTS\.md|seç[ãa]o|section|regra|item|§)[^\n]{0,20}9\.[0-9]"`)
→ só ocorrências de "Section 9.3" da OpenStax; `grep -rn "preferência por CC BY"` → **nenhuma
regra viva**, só narrativa histórica (log deste ticket, `L-009` e a linha de execução do
`docs-writer`). Confirmo o resultado do revisor por conta própria.

### Verificação própria C — alcance real da regra por ferramenta (ponto de julgamento b)

Testei o caminho de auto-carregamento de cada ferramenta, não a existência do texto:
Claude Code (`CLAUDE.md:3` → `@AGENTS.md` → §9.7) ✔ · Codex e Grok CLI (`AGENTS.md` nativo) ✔ ·
Gemini CLI (`GEMINI.md:6` → `@AGENTS.md`) ✔ · Copilot (`.github/copilot-instructions.md` +
`content.instructions.md` com `applyTo: content/**`) ✔ · Cursor (`.cursor/rules/content.mdc`,
front matter `globs: content/**`) ✔ · Windsurf (`.windsurf/rules/content.md`,
`trigger: glob`, `globs: content/**`) ✔ · Antigravity (`AGENTS.md` nativo, **e** `.agents/rules/
content.md` com ativação sugerida por glob — mesmo que a UI não seja configurada, o
`AGENTS.md` fecha o caminho) ✔ · Zed (`.rules`), Cline/Roo (`.clinerules`), Junie
(`.junie/guidelines.md`) ✔ (versão condensada de `core`, imperativa) · ferramentas web
(`prompts/bootstrap-session.md:38-40`) ✔ · contribuidor humano (`CONTRIBUTING.md:59`) ✔.
Os adapters de agent (`.github/chatmodes/content-author.chatmode.md`,
`.gemini/commands/agent/content-author.toml`, `.claude/commands/content-author.md`) são
ponteiros de 13–25 linhas que **referenciam** `.claude/agents/content-author.md` — confirmei
com `grep -l`; a regra chega por referência, sem cópia que possa divergir. E o próprio
`content-author.md:31-33` traz a regra nas suas "regras duras".
**Conclusão: não há caminho relevante pelo qual um `content-author` futuro deixe de receber a
regra. Critério 5 atendido.**

### Verificação própria D — escopo

`grep -rn "ADR-0005\|LICENSE-CONTENT\|NC = leitura" content/` → **vazio**;
`grep -rn "ADR-0005" docs/adr/ADR-0003-platform-stack.md docs/architecture/` → **vazio**.
As citações a `ADR-0005` em `tickets/TCK-0003/log.md` são da própria cadeia do TCK-0003
declarando que **não** tocou nestes arquivos. O `git diff -- docs/adr/README.md` mostra a
linha nova do `ADR-0005` (deste ticket) convivendo com a mudança de status do `ADR-0003`
(cadeia do TCK-0003) — o ruído de `app` nos gerados e as linhas de stack em `AGENTS.md`
(§1 e §11) e em `core.instructions.md` são do TCK-0003, como avisado em `[008]`, e **não**
foram considerados na minha decisão.

### Pontos de julgamento decididos por mim

- **SG1 (ND ao lado de NC) — é dívida, não defeito; não compromete o critério 4.** Levantei
  **todas** as afirmações sobre ND nas fontes normativas (9 ocorrências, em `AGENTS.md:248`,
  `content.instructions.md:24`, `core.instructions.md:44`, `content-author.md:31`,
  `researcher.md:18`, `CONTRIBUTING.md:59`, `bootstrap-session.md:39`, `ADR-0005:112`,
  `content-standards.md:64`) e **nenhuma delas afirma que ND proíbe redistribuição**. A única
  justificativa anexada a ND é o ramo da árvore "permite derivados? → não", que é
  **factualmente verdadeiro** de CC BY-ND. A nuance que falta (ND permite redistribuição
  verbatim, inclusive comercial) é **omissão, não erro**: a razão pela qual ND fica de fora
  aqui é que `content/` é declarado uniformemente CC BY-SA e não há campo de licença por
  asset, então incorporar material ND — mesmo verbatim — implicaria oferecê-lo sob outros
  termos. Além disso, o critério 4, **como foi escrito**, cobre apenas CC BY, domínio público,
  CC BY-NC e CC BY-NC-SA; ND é extensão conservadora além do critério. Reprovar por precisão
  de justificativa numa cláusula que o critério não pede, e que não afirma nada falso, seria
  renegociar critério — não é papel do QA. Vira **D-1** abaixo.
- **Alcance da regra (b): atendido**, com o teste concreto documentado em "Verificação
  própria C".

### Dívidas e pendências repassadas ao `tech-lead` (não bloqueiam)

- **D-1 (SG1).** Registrar em uma linha, no `ADR-0005` e no `AGENTS.md` §9.7, *por que* ND
  entra em "só citável": não por a licença proibir redistribuição verbatim, mas porque
  `content/` é uniformemente CC BY-SA e não há licença por asset. Sem isso, alguém "descobre"
  a imprecisão daqui a seis meses e reabre a regra inteira.
- **D-2 (SG2 do revisor, não acatada nesta rodada).** `Como reverter` do `ADR-0005` condiciona
  a relicença apenas à ausência de contribuição externa; agora que adaptar fonte **CC BY-SA de
  terceiros** é autorizado, o share-alike dessa fonte também trava a relicença.
- **D-3 (SG4).** "Citar uma fonte NC é sempre legítimo" (`ADR-0005:149`,
  `content-standards.md`) pode ser lido como autorização para transcrever trecho entre aspas;
  trocar por "citar = referência bibliográfica + link, sem transcrever".
- **D-4 (SG3).** Acrescentar à checklist da `L-009` o oitavo item revelado por este loop:
  quando a mudança **renumera** seção do `AGENTS.md`, conferir as referências cruzadas
  (`grep -rn "§9\.[0-9]"`). Desta vez o resultado foi correto, mas por sorte de numeração.
- Pendências herdadas de `[009]`/`[010]`, repassadas sem alteração: (1) confirmar que nada
  das três fontes NC entrou no texto autoral do nó piloto e criar em `references.json` um
  campo que distinga **adaptável** × **apenas citável** (a regra nova depende de um schema que
  ainda não a expressa) — TCK-0001; (2) esclarecer a licença do *Livro Aberto de Matemática*
  com IMPA/OBMEP (se for BY-SA, é a única fonte pt-BR adaptável conhecida); (3) não há hoje
  fonte gratuita em pt-BR compatível — o custo de produção autoral sobe; (4) rodapé da
  aplicação precisará exibir as duas licenças com link canônico; (5) `README.md:7-10`
  (`ADR-0003` como `proposed`) é pendência do TCK-0003, não deste ticket — encaminhar.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 — **todos
  atendidos com evidência reproduzida. Ticket `done`.**
