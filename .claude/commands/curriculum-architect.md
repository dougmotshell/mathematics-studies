---
description: Desenha e mantém a taxonomia de conteúdo, as trilhas de aprendizado e o grafo de pré-requisitos (estágio → área → tópico → sub-tópico). Usar para decidir onde um assunto entra, criar/reorganizar tópi…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Delegue ao subagent `curriculum-architect` (definido em @.claude/agents/curriculum-architect.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`curriculum-architect`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
