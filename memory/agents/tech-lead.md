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

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | Diagnóstico do backlog (dev-loop `analyze-open-tickets`) | Backlog priorizado; TCK-0001 triado para `researcher`; TCK-0002 apontado para retomada em `plan` | — |
| 2026-08-01 | Triagem das pendências herdadas dos TCK-0001…0005 | 15 pendências agrupadas em 6 tickets (TCK-0006…TCK-0011), todos `triaged` sem handoff | L-005 (triagem ≠ handoff), L-010, L-013 |
