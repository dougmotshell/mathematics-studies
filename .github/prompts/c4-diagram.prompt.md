---
mode: agent
description: Cria ou atualiza diagramas C4 (Context, Container, Component) em Mermaid dentro de docs/architecture/. Usar ao documentar a arquitetura da plataforma, o pipeline de conteúdo ou a superfície de IA.
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Leia e siga integralmente as instruções da skill em [`.claude/skills/c4-diagram/SKILL.md`](../../.claude/skills/c4-diagram/SKILL.md).

Aplique-as ao seguinte contexto: ${input:contexto}

Respeite os arquivos de apoio da skill (`references/`, `scripts/`) e as regras do
`AGENTS.md` — em especial bilinguismo pt-BR/en-US, acessibilidade e verificação de
resultados matemáticos. Se a skill depender de um MCP (ex.: `chrome-devtools` em
`/pwa-audit` e `/a11y-audit`), verifique se ele está configurado; sem ele, use o
fallback documentado na própria skill e declare o que não foi verificado.

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
