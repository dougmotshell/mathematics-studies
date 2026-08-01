---
mode: agent
description: Audita a aplicação como PWA — instalabilidade, funcionamento offline, performance (Core Web Vitals), tamanho de bundle e comportamento em rede lenta. Usar antes de deploy e após mudanças que afetem c…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Leia e siga integralmente as instruções da skill em `.claude/skills/pwa-audit/SKILL.md` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de regras) e, para tarefa
significativa, `memory/MEMORY.md` e `docs/errors/README.md`. Respeite os arquivos de apoio
da skill (`references/`, `scripts/`).

Se a skill depender de um MCP (por exemplo `chrome-devtools` em `/pwa-audit` e
`/a11y-audit`), verifique se ele está disponível; sem ele, use o fallback documentado na
própria skill e **declare o que não foi verificado**.

Aplique a skill ao seguinte contexto: ${input:contexto}

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
