# Log — TCK-0007

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:36 — tech-lead
- Ação: criação do ticket a partir das pendências 1, 2, 3 e 4 do TCK-0005 (`log.md` `[006]`,
  `[008]` §7, `[010]`, `[011]`), com os trechos de origem copiados verbatim.
- Motivo: as quatro pendências foram classificadas pelo `qa-validator#3` em `[011]` como
  **condicionantes da saída de `draft`** (1, 2 e 3) e como dependente de regra (4). O
  TCK-0005 está `done` e não reabre (regra 6 de auditoria) — a correção vem em ticket novo
  que o referencia.
- Resultado: ok — `tickets/TCK-0007-pilot-node-rigor-and-a11y-fixes/` criado. Nenhum arquivo
  de `content/` tocado nesta ação (`git status --short content/` → vazio).
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:38 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** as quatro pendências caem nos **mesmos dois
  arquivos** do mesmo nó, todas condicionam o mesmo evento (sair de `draft`) e exigem a mesma
  cadeia de revisão tripla — separá-las por severidade produziria três tickets disputando o
  mesmo diff, com risco de conflito e de paridade quebrada.
- **Divergência deliberada do encaminhamento de `[006]`:** o `math-reviewer` sugeriu "P2,
  tamanho P" para o item 1 isolado. Triado como **P1/M** porque o ticket agrega quatro itens,
  três deles declarados condicionantes de `draft` pelo QA, e porque o nó é o modelo dos 3–5
  nós piloto da Fase 1 — corrigir depois da cópia custa N vezes mais. Registro a mudança aqui
  em vez de alterar silenciosamente o critério de outro agente.
- **Tipo:** `content`. Toca só `content/` (e `exercises.json` se o TCK-0006 assim decidir).
- **Prioridade P1 · tamanho M.** M e não P: são 2 arquivos × 4 pontos, mais a possível
  varredura de `exercises.json`, com paridade obrigatória em cada alteração.
- **Owner: `content-author`.** É quem escreve teoria didática bilíngue. Os revisores que
  **diagnosticaram** os defeitos (`math-reviewer`, `a11y-ux-reviewer`) não escrevem a
  correção — assim continuam elegíveis para revisá-la.
- **Cadeia:** `tech-lead` → `content-author` → (`math-reviewer` ‖ `a11y-ux-reviewer` ‖
  `i18n-steward`, em paralelo) → `qa-validator`. `curriculum-architect` **dispensado**: não há
  mudança de taxonomia, pré-requisito ou dificuldade. Divisão de critérios entre os revisores:
  1, 2 e 7 → `math-reviewer`; 3, 4 e 5 → `a11y-ux-reviewer`; 6 → `i18n-steward`.
  Independência: nenhum deles produziu o texto que vai julgar.
- **Restrições passadas ao executor:**
  1. **Não começar antes do TCK-0006 entregue** — o critério 5 depende do veredito por
     ocorrência registrado lá. Se a execução for autorizada antes, o ticket entra
     `blocked` no critério 5 e entrega os demais.
  2. Toda alteração nos **dois** idiomas, no mesmo ciclo (ADR-0002 / L-001). Nada de
     "traduzo depois".
  3. Não renomear slug nem caminho (L-003) e não mudar `status` em `meta.json`.
  4. As 3 referências do nó são **CC BY-NC-SA** → só citáveis: nenhum trecho, exemplo ou
     sequência didática delas pode entrar no texto da correção (`AGENTS.md` §9.7, L-009).
  5. `git diff -- content/` tem de continuar restrito ao nó piloto.
- **Aderência ao plano:** Fase 1 do roadmap ("provar o formato com conteúdo real"). O nó
  piloto é o artefato dessa fase; sair de `draft` é o marco. Dentro do plano.
- **Requisitos inegociáveis conferidos:** bilinguismo (critério 6), acessibilidade (3, 4, 5),
  correção matemática (1, 2, 7), gratuidade (só texto), URLs preservadas (9); offline e
  privacidade não aplicáveis, com o porquê registrado no ticket.
- **Dependências:** depende de `TCK-0006` (critério 5). Não depende do `TCK-0009`
  (`references.json`) — são arquivos e defeitos distintos.
- Resultado: ok — `status: triaged`, `owner: content-author`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
