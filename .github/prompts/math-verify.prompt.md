---
mode: agent
description: Verifica computacional ou simbolicamente uma afirmação matemática, um gabarito ou uma manipulação algébrica antes de publicá-la. Usar sempre que um resultado não trivial for afirmado como verdadeiro.
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Leia e siga integralmente as instruções da skill em [`.claude/skills/math-verify/SKILL.md`](../../.claude/skills/math-verify/SKILL.md).

Aplique-as ao seguinte contexto: ${input:contexto}

Respeite os arquivos de apoio da skill (`references/`, `scripts/`) e as regras do
`AGENTS.md` — em especial bilinguismo pt-BR/en-US, acessibilidade e verificação de
resultados matemáticos. Se a skill depender de um MCP (ex.: `chrome-devtools` em
`/pwa-audit` e `/a11y-audit`), verifique se ele está configurado; sem ele, use o
fallback documentado na própria skill e declare o que não foi verificado.

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
