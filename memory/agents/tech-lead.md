# Memória do agente `tech-lead`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Orquestrador técnico — recebe todo ticket novo, faz triagem, decide a abordagem, delega ao agente certo e desbloqueia loops travados. Ponto de entrada de qualquer tarefa de desenvolvimento, manutenção ou correção de bug.

## Notas persistentes

- **Triagem ≠ handoff.** Registrar `triaged` no `ticket.md` + `log.md` não aciona ninguém; o
  `HANDOFF` é que dispara execução imediata (`docs/ai/ticket-protocol.md`, regra 1). Em pedido
  de diagnóstico/planejamento, triar e parar — o handoff sai quando o usuário pedir execução.
- **`ADR-0003` (proposed) bloqueia só a aplicação**, não o acervo: o próprio ADR declara
  impacto nulo em `content/`. Tickets de conteúdo, spec e docs seguem normalmente; tickets de
  `frontend-developer` / `backend-developer` / `devops-engineer` ficam `blocked: human-input`.
- **Há acesso à rede no ambiente** (verificado 2026-08-01, `curl` HTTP 200 em openstax.org):
  ticket de verificação de fonte externa não é bloqueado por isso.
- **A linha 16 acima está obsoleta** desde o aceite do `ADR-0003` em 2026-08-01 (TCK-0003):
  a stack **está decidida** e tickets de `frontend-developer` / `backend-developer` /
  `devops-engineer` **não** ficam mais `blocked` por causa dela. A correção da linha (e de
  mais seis pontos iguais na superfície de IA) é o **TCK-0008**; até ele rodar, valem
  `docs/adr/README.md:17`, `AGENTS.md` §1 e `memory/context/project-context.md`.
- **Pendência levantada em QA vira ticket, não nota de rodapé.** As cadeias de review e QA
  dos TCK-0001…0005 entregaram 15 pendências fora de escopo. O que funcionou: agrupar por
  **artefato + evento que a pendência condiciona** (sair de `draft`, próximo nó, primeiro
  ticket de implementação), não por severidade nem por agente que a reportou.
- **Prazo relativo é mais honesto que prioridade absoluta** neste projeto: "antes de o nó
  piloto sair de `draft`", "antes do próximo nó", "antes do primeiro ticket de aplicação"
  são verificáveis; "urgente" não é. A prioridade P1/P2/P3 do ticket traduz esse prazo.
- Estado do backlog em 2026-08-01, depois da rodada de triagem: TCK-0001…TCK-0005 `done`;
  TCK-0006…TCK-0011 `triaged`, **nenhum com `HANDOFF`** — aguardam ordem de execução do
  usuário. Ordem recomendada: 0006 → 0007 → 0008 → 0009 → 0010 → 0011.
- Dependência dura registrada: **TCK-0007 depende do TCK-0006** (o critério 5 do 0007 aplica
  a regra de fórmula inline que o 0006 decide). As demais são independentes; 0008 e 0006
  disputam `sync-ai-adapters.py` se rodarem juntos.
- **Escopo dimensionado por número obsoleto é escopo errado.** O TCK-0007 foi triado contra
  "18 pontos"; `TCK-0006/log.md` `[007]` §2 refez o inventário e deu **22**. Antes de mexer no
  `size`, conferir **onde** os pontos caem: 14 dos 22 estavam em `exercises.json`, artefato do
  `exercise-designer` — o problema era de **área**, não de tamanho. Recorte por artefato
  (TCK-0007 = `theory.*.md`, TCK-0018 = `exercises.json`) manteve os dois em `M`, com diffs
  disjuntos e revisores independentes; sem a divisão, seria um `G` cruzando duas áreas.
- **Regra de escrita de critério de aceite:** critério que depende de lista mantida em outro
  lugar **aponta e não enumera** (L-024). Foi o parêntese "resumindo" o inventário que
  envelheceu e passou a contradizer o ponteiro no mesmo critério.
- **Duas ferramentas discordando sobre o mesmo fato é dívida estrutural, não bug plural.**
  No TCK-0017 (auditor × validador de conteúdo) a saída foi **delegar** — uma fonte de verdade
  por pergunta ("este arquivo carrega?" = validador; "este acervo é coerente?" = auditor) — e
  não corrigir as 4 instâncias em paralelo, que deixaria as duas implementações de pé. O que
  tornou a decisão defensável foi a **medição já existente** ("nenhum dos sete casos tem o
  auditor como o mais estrito", `TCK-0014/log.md` `[010]`) mais um **critério de
  não-regressão** com 7 fixtures da área exclusiva do auditor. Delegar sem essa prova seria
  perder cobertura no escuro.
- **Invariante vale mais que lista de casos** ao fechar divergência entre ferramentas: exigir
  vereditos idênticos as fundiria numa só; a restrição certa é assimétrica — *proibido o
  validador sair 1 e o auditor sair 0* —, vale para entradas que ninguém escreveu ainda, e o
  teste dela precisa provar que **reprova** quando violada de propósito.
- **Reclassificar julgamento de outro agente é legítimo quando há fato novo** — e o registro
  vai no ticket novo, nunca editando o log alheio (append-only, `done` não reabre). Feito duas
  vezes em 2026-08-01: a pendência 4 do TCK-0005 ("inline não condiciona `draft`") passou a
  condicionar **em uma** das 14 ocorrências, porque `[007]` §2 mostrou que ali a leitura errada
  troca o polinômio.
- **Ambiguidade de leitura não é erro matemático.** `$(x+3)^2$` está correto; o defeito é de
  a11y **com teste matemático**. A classificação muda a cadeia: obriga o `math-reviewer` num
  ticket que seria só de a11y, com assinatura dupla (reconstrução às cegas por ele **e** pelo
  `a11y-ux-reviewer`). Chamar de "erro matemático" mandaria o executor procurar conta errada
  que não existe; chamar de "estilo inline" o rebaixaria a melhoria.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | Diagnóstico do backlog (dev-loop `analyze-open-tickets`) | Backlog priorizado; TCK-0001 triado para `researcher`; TCK-0002 apontado para retomada em `plan` | — |
| 2026-08-01 | Triagem das pendências herdadas dos TCK-0001…0005 | 15 pendências agrupadas em 6 tickets (TCK-0006…TCK-0011), todos `triaged` sem handoff | L-005 (triagem ≠ handoff), L-010, L-013 |
| 2026-08-01 | Re-escopo do TCK-0007 (22 pontos do `[007]` §2 do TCK-0006) | Critério 5 vira ponteiro; ticket dividido por artefato → TCK-0018 (`exercises.json`, `exercise-designer`, P1) criado; `size: M` mantido nos dois; 224/225 classificado como a11y com teste matemático e assinatura dupla | **L-024** (nova), L-021, L-012 |
| 2026-08-01 | Ticket dos defeitos do `audit-content.py` (achado do TCK-0014 `[010]`) | **TCK-0017** criado e triado (`bug`, P1, M, `backend-developer`): recorte = **delegar** o contrato de arquivo ao validador, com invariante de não-divergência e 7 fixtures de não-regressão | L-019 (adendo), L-013, L-018, L-011, L-002 |
