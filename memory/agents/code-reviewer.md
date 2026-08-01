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
