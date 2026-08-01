**Tipo:** sucesso
**ID:** L-005
**Contexto:** 2026-08-01, dev-loop `analyze-open-tickets`. Ao triar `TCK-0001`, o
`tech-lead` classificou o ticket, definiu owner (`researcher`) e escreveu o plano de
execução no log — mas o pedido do usuário era diagnóstico do backlog, não execução.

**Lição:** marcar um ticket como `triaged` (status + owner + plano no log) **não** é, por
si só, um `HANDOFF`. No protocolo (`docs/ai/ticket-protocol.md`, "Execução automática"),
quem dispara a execução imediata do próximo agente é a entrada `HANDOFF` — não a mudança de
status. É possível (e correto) triar um ticket inteiro, deixá-lo pronto para rodar, e
**não** acionar o próximo agente quando o pedido em curso for só diagnóstico/planejamento.
Confundir as duas coisas produz dois erros simétricos: (a) executar trabalho que ninguém
pediu, só porque o ticket foi triado; (b) achar que triar sem `HANDOFF` deixou o ticket
"esquecido" e reabrir triagem à toa.

**Como aplicar:** ao encerrar uma triagem, perguntar explicitamente "o usuário pediu para
executar ou só para planejar/diagnosticar?". Se só diagnóstico: registrar `ACTION` de
triagem, indicar no log qual comando aciona a execução (ex.: `/ticket-loop TCK-NNNN`) e
**não** escrever entrada `HANDOFF`. Vale para qualquer agente orquestrador (`tech-lead`,
`task-router`) que registre estado de um ticket sem necessariamente disparar a próxima
etapa.
