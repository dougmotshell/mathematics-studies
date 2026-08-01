---
description: Projeta fluxos, telas, design system e microinterações da plataforma, com foco em carga cognitiva, acessibilidade e público amplo (crianças a pesquisadores). Usar antes de implementar interface nova…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `ui-ux-designer` (definido em @.claude/agents/ui-ux-designer.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`ui-ux-designer`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
