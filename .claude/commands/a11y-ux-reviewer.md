---
description: Revisa acessibilidade (WCAG 2.2 AA, matemática acessível a leitor de tela, teclado, contraste) e UX de aprendizagem (carga cognitiva, feedback, navegação, progresso). Usar antes de publicar interface…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `a11y-ux-reviewer` (definido em @.claude/agents/a11y-ux-reviewer.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`a11y-ux-reviewer`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
