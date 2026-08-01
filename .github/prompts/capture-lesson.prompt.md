---
mode: agent
description: Registra uma lição aprendida em memory/lessons/ (protocolo de auto-aprendizado). Usar após correções do usuário, descobertas de domínio, decisões de terminologia bilíngue ou padrões que funcionaram b…
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Leia e siga integralmente as instruções da skill em [`.claude/skills/capture-lesson/SKILL.md`](../../.claude/skills/capture-lesson/SKILL.md).

Aplique-as ao seguinte contexto: ${input:contexto}

Respeite os arquivos de apoio da skill (`references/`, `scripts/`) e as regras do
`AGENTS.md` — em especial bilinguismo pt-BR/en-US, acessibilidade e verificação de
resultados matemáticos. Se a skill depender de um MCP (ex.: `chrome-devtools` em
`/pwa-audit` e `/a11y-audit`), verifique se ele está configurado; sem ele, use o
fallback documentado na própria skill e declare o que não foi verificado.

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
