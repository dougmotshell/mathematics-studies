---
mode: agent
description: Executa o ciclo completo de um ticket — triagem → implementação → code review → validação de QA — com handoffs e logs a cada etapa, em loop até todos os critérios de aceite passarem, o ticket bloquea…
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Leia e siga integralmente as instruções da skill em [`.claude/skills/ticket-loop/SKILL.md`](../../.claude/skills/ticket-loop/SKILL.md).

Aplique-as ao seguinte contexto: ${input:contexto}

Respeite os arquivos de apoio da skill (`references/`, `scripts/`) e as regras do
`AGENTS.md` — em especial bilinguismo pt-BR/en-US, acessibilidade e verificação de
resultados matemáticos. Se a skill depender de um MCP (ex.: `chrome-devtools` em
`/pwa-audit` e `/a11y-audit`), verifique se ele está configurado; sem ele, use o
fallback documentado na própria skill e declare o que não foi verificado.

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
