---
mode: agent
description: Cria um nó de conteúdo completo na taxonomia (content/<stage>/<area>/<topic>/[<subtopic>]) com meta.json, teoria bilíngue, exercícios, referências e assets. Usar sempre que um assunto novo entrar na…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Leia e siga integralmente as instruções da skill em `.claude/skills/new-topic/SKILL.md` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de regras) e, para tarefa
significativa, `memory/MEMORY.md` e `docs/errors/README.md`. Respeite os arquivos de apoio
da skill (`references/`, `scripts/`).

Se a skill depender de um MCP (por exemplo `chrome-devtools` em `/pwa-audit` e
`/a11y-audit`), verifique se ele está disponível; sem ele, use o fallback documentado na
própria skill e **declare o que não foi verificado**.

Aplique a skill ao seguinte contexto: ${input:contexto}

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
