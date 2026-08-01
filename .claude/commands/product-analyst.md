---
description: Refina pedidos em requisitos claros e critérios de aceite verificáveis, confrontando-os com a visão do produto, o roadmap e as specs. Usar quando um ticket chega ambíguo ou quando é preciso decidir o…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Delegue ao subagent `product-analyst` (definido em @.claude/agents/product-analyst.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`product-analyst`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
