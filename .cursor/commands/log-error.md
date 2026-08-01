<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /log-error

> Registra um erro não-trivial em docs/errors/ para não repeti-lo — comando que falhou por causa evitável, afirmação matemática errada publicada, suposição equivocada sobre a taxonomia ou retrabalho po…

Leia e siga integralmente as instruções da skill em `.claude/skills/log-error/SKILL.md` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de regras) e, para tarefa
significativa, `memory/MEMORY.md` e `docs/errors/README.md`. Respeite os arquivos de apoio
da skill (`references/`, `scripts/`).

Se a skill depender de um MCP (por exemplo `chrome-devtools` em `/pwa-audit` e
`/a11y-audit`), verifique se ele está disponível; sem ele, use o fallback documentado na
própria skill e **declare o que não foi verificado**.

Aplique a skill ao que o usuário pedir nesta conversa. Se nada for informado, pergunte o que
a skill precisa antes de prosseguir.
