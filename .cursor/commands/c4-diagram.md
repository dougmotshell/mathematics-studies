<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /c4-diagram

> Cria ou atualiza diagramas C4 (Context, Container, Component) em Mermaid dentro de docs/architecture/. Usar ao documentar a arquitetura da plataforma, o pipeline de conteúdo ou a superfície de IA.

Leia e siga integralmente as instruções da skill em `.claude/skills/c4-diagram/SKILL.md` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de regras) e, para tarefa
significativa, `memory/MEMORY.md` e `docs/errors/README.md`. Respeite os arquivos de apoio
da skill (`references/`, `scripts/`).

Se a skill depender de um MCP (por exemplo `chrome-devtools` em `/pwa-audit` e
`/a11y-audit`), verifique se ele está disponível; sem ele, use o fallback documentado na
própria skill e **declare o que não foi verificado**.

Aplique a skill ao que o usuário pedir nesta conversa. Se nada for informado, pergunte o que
a skill precisa antes de prosseguir.
