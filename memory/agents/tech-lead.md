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
- Estado do backlog em 2026-08-01: TCK-0001 `triaged` → `researcher` (não acionado);
  TCK-0002 `triaged`, dev-loop `.dev-loop/minimum-learning-slice/` parado na etapa `plan`
  (`product-analyst`) — retomar, nunca reiniciar (o `loop.md` guarda a iteração 1/3).

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | Diagnóstico do backlog (dev-loop `analyze-open-tickets`) | Backlog priorizado; TCK-0001 triado para `researcher`; TCK-0002 apontado para retomada em `plan` | — |
