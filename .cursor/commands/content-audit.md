<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /content-audit

> Audita um nó, uma área ou todo o conteúdo — estrutura da taxonomia, completude didática, rigor, exercícios, referências e metadados. Usar antes de publicar e periodicamente para encontrar lacunas e i…

Leia e siga integralmente as instruções da skill em `.claude/skills/content-audit/SKILL.md` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de regras) e, para tarefa
significativa, `memory/MEMORY.md` e `docs/errors/README.md`. Respeite os arquivos de apoio
da skill (`references/`, `scripts/`).

Se a skill depender de um MCP (por exemplo `chrome-devtools` em `/pwa-audit` e
`/a11y-audit`), verifique se ele está disponível; sem ele, use o fallback documentado na
própria skill e **declare o que não foi verificado**.

Aplique a skill ao que o usuário pedir nesta conversa. Se nada for informado, pergunte o que
a skill precisa antes de prosseguir.
