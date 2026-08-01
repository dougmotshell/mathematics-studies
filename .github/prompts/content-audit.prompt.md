---
mode: agent
description: Audita um nó, uma área ou todo o conteúdo — estrutura da taxonomia, completude didática, rigor, exercícios, referências e metadados. Usar antes de publicar e periodicamente para encontrar lacunas e i…
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Leia e siga integralmente as instruções da skill em [`.claude/skills/content-audit/SKILL.md`](../../.claude/skills/content-audit/SKILL.md).

Aplique-as ao seguinte contexto: ${input:contexto}

Respeite os arquivos de apoio da skill (`references/`, `scripts/`) e as regras do
`AGENTS.md` — em especial bilinguismo pt-BR/en-US, acessibilidade e verificação de
resultados matemáticos. Se a skill depender de um MCP (ex.: `chrome-devtools` em
`/pwa-audit` e `/a11y-audit`), verifique se ele está configurado; sem ele, use o
fallback documentado na própria skill e declare o que não foi verificado.

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
