---
name: ticket
description: Cria um ticket de desenvolvimento no fluxo de agentes — coleta o pedido, gera tickets/TCK-NNNN-<slug>/ (ticket.md + log.md) a partir do template, faz a triagem com o tech-lead e entra automaticamente no ciclo de execução. Usar para qualquer feature, bug, tarefa de conteúdo, infra ou segurança.
---

# Skill: /ticket

Cria um ticket completo no padrão de [`tickets/README.md`](../../../tickets/README.md) e
**dispara o ciclo de execução** descrito em
[`docs/ai/ticket-protocol.md`](../../../docs/ai/ticket-protocol.md).

## Passos

1. **Número:** listar `tickets/TCK-*` e usar o próximo `NNNN` sequencial (começa em `0001`).
2. **Slug:** 2–4 palavras en-US derivadas do pedido (`TCK-0007-exercise-player`).
3. **Criar** `tickets/TCK-NNNN-<slug>/ticket.md` copiando `tickets/TICKET-TEMPLATE.md`:
   - Pedido original **verbatim** (nunca parafrasear na seção verbatim);
   - `type`, `priority`, `size` e um rascunho de critérios de aceite quando o pedido permitir
     inferir (marcar "rascunho — validar na triagem");
   - Marcar os **requisitos transversais** aplicáveis (bilinguismo, acessibilidade, offline,
     custo zero, privacidade de menores, URLs, correção matemática).
4. **Criar** `tickets/TCK-NNNN-<slug>/log.md` com a primeira entrada:

   ```markdown
   ## [001] ACTION — AAAA-MM-DD HH:MM — /ticket
   - Ação: ticket criado a partir do pedido do usuário
   - Motivo: registro da demanda no fluxo auditado
   - Resultado: ok — status new, owner tech-lead
   ```

5. **Triagem imediata:** assumir o papel do
   [`tech-lead`](../../../.claude/agents/tech-lead.md) (ou invocá-lo como subagente) para:
   classificar, dimensionar, validar/escrever critérios de aceite, apontar as lições e o
   contexto relevantes de `memory/`, escolher o agente responsável e registrar o `HANDOFF`
   `new → triaged` no log.
6. **Continuar automaticamente:** a triagem **não** encerra o fluxo. Se o ticket saiu
   `triaged`, entrar direto no ciclo do [`/ticket-loop`](../ticket-loop/SKILL.md) — sem
   esperar novo comando. Parar apenas se a triagem resultou em `blocked: human-input`
   (listar as perguntas) ou se o pedido está fora do plano e precisa de decisão do usuário.
7. **Responder ao usuário no final:** número do ticket, critérios de aceite, o que cada
   agente entregou, evidências — ou, se parou em `blocked`, as perguntas objetivas que
   destravam.

## Regras

- Um pedido com múltiplas entregas independentes = **múltiplos tickets** (avisar o usuário);
  eles podem correr em paralelo, com subagentes (`<agente>#N`) quando o dono estiver ocupado.
- Nunca pular o log — esta skill é a origem da trilha de auditoria.
- Ticket de `bug` exige seção de reprodução preenchida antes de sair da triagem; se não for
  reproduzível, o primeiro passo do ciclo é reproduzir.
- Ticket que depende de decisão estrutural não decidida (ex.: `ADR-0003` ainda `proposed`)
  nasce `blocked: human-input` ou gera um ticket de decisão antes.
- Convenções: pastas/slug en-US; conteúdo pt-BR.
