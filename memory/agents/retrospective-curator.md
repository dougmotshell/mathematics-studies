# Memória do agente `retrospective-curator`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Fecha o ciclo de trabalho — atualiza memory/agents/, registra lições em memory/lessons/, erros em docs/errors/ e mantém os índices (MEMORY.md, LESSONS.md) consistentes. Usar como última etapa do /dev-loop ou ao final de tarefas significativas.

## Notas persistentes

- **Nem toda etapa `curate` gera lição.** Se a tarefa foi diagnóstico/roteamento sem
  correção de erro nem padrão novo comprovado em código/conteúdo, o "curate express" é
  atualizar memória dos agents envolvidos e os índices de contexto — sem forçar lição.
- Triagem de ticket (`status: triaged`) não é `HANDOFF` — ver `L-005`. Ao revisar logs de
  ticket, não interpretar `triaged` sem entrada `HANDOFF` como pendência esquecida.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | dev-loop `analyze-open-tickets` (curate) | `memory/context/process.md` atualizado com estado real de TCK-0001/TCK-0002; L-005 registrada (triagem ≠ handoff) | L-005 |
