<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /math-verify

Verifica computacional ou simbolicamente uma afirmação matemática, um gabarito ou uma manipulação algébrica antes de publicá-la. Usar sempre que um resultado não trivial for afirmado como verdadeiro.

## Passos

1. Abra e leia integralmente `.claude/skills/math-verify/SKILL.md` neste repositório — ele contém o procedimento
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
