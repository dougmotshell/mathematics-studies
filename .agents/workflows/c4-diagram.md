<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /c4-diagram

Cria ou atualiza diagramas C4 (Context, Container, Component) em Mermaid dentro de docs/architecture/. Usar ao documentar a arquitetura da plataforma, o pipeline de conteúdo ou a superfície de IA.

## Passos

1. Abra e leia integralmente `.claude/skills/c4-diagram/SKILL.md` neste repositório — ele contém o procedimento
   completo desta capacidade.
2. Leia `AGENTS.md` (regras do projeto). Para tarefa significativa, leia também
   `memory/MEMORY.md`, o contexto da área em `memory/context/` e `docs/errors/README.md`.
3. Execute o procedimento da skill sobre a entrada fornecida pelo usuário, respeitando os
   arquivos de apoio referenciados (`references/`, `scripts/`).
4. Se a skill depender de um MCP indisponível, use o fallback documentado nela e declare
   explicitamente o que não foi verificado.
5. Ao concluir, apresente o resultado com evidência (saída de comando, trecho de arquivo) e
   proponha as atualizações de `memory/` cabíveis.

Se o usuário não informar a entrada necessária, pergunte antes de prosseguir.
