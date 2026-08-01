<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /ticket

> Cria um ticket de desenvolvimento no fluxo de agentes — coleta o pedido, gera tickets/TCK-NNNN-<slug>/ (ticket.md + log.md) a partir do template, faz a triagem com o tech-lead e entra automaticamente…

Leia e siga integralmente as instruções da skill em `.claude/skills/ticket/SKILL.md` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de regras) e, para tarefa
significativa, `memory/MEMORY.md` e `docs/errors/README.md`. Respeite os arquivos de apoio
da skill (`references/`, `scripts/`).

Se a skill depender de um MCP (por exemplo `chrome-devtools` em `/pwa-audit` e
`/a11y-audit`), verifique se ele está disponível; sem ele, use o fallback documentado na
própria skill e **declare o que não foi verificado**.

Aplique a skill ao que o usuário pedir nesta conversa. Se nada for informado, pergunte o que
a skill precisa antes de prosseguir.
