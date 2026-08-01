---
trigger: glob
description: Instruções para `tickets/`
globs: tickets/**
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# Instruções para `tickets/`

- Toda tarefa de desenvolvimento, bug, infra ou conteúdo de porte vive em
  `tickets/TCK-NNNN-<slug>/` com `ticket.md` e `log.md`. Contrato completo:
  `docs/ai/ticket-protocol.md`.
- **`log.md` é append-only.** Corrigir registro = entrada `CORRECTION` referenciando o
  `[SEQ]` original. Nunca editar ou apagar entrada anterior.
- Toda entrada tem `[SEQ]` incremental — buraco na sequência indica ação não logada.
- **Evidência > afirmação**: "os testes passam" exige a saída do comando; "a tela está
  pronta" exige screenshot; "o cálculo está certo" exige a verificação.
- `status:` e `owner:` no `ticket.md` só mudam junto com uma entrada `HANDOFF` no log.
- Critérios de aceite são a **definição de pronto**; só o `qa-validator` marca `done`.
- Nenhum agente valida artefato produzido pela própria cadeia.
- 3 devoluções no mesmo par → escalar ao `tech-lead`; sem saída → `blocked: human-input`.
- A `ACTION` que resolve um `REJECT` termina com `Lição: L-NNN` ou
  `Lição: n/a — erro pontual`.
- Commits usam prefixo `TCK-NNNN:`; commit e push só com pedido explícito do usuário.
- Ticket `done` nunca reabre — regressão vira ticket novo referenciando o original.
