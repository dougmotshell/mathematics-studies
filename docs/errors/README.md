# Registro de erros

Todo erro não trivial vira um arquivo aqui — comando que falhou por causa evitável, afirmação
matemática errada, suposição equivocada sobre a taxonomia, retrabalho por instrução mal
interpretada, CI quebrado por comportamento não óbvio de ferramenta.

**Ler este índice é parte do início de qualquer tarefa** (AGENTS.md §5).

Criar com `/log-error`, a partir de [`error-template.md`](error-template.md).

| Erro | Data | Área | Severidade |
|---|---|---|---|
| *nenhum erro registrado até 2026-08-01* | — | — | — |

## Regras

1. Um erro por arquivo; nome en-US kebab-case; conteúdo pt-BR.
2. Registrar a **causa raiz**, não o sintoma.
3. **Erro matemático em conteúdo publicado** exige, além do registro: correção do nó,
   verificação dos nós irmãos e dependentes, e lição em `memory/lessons/`.
4. Erro já registrado que se repete é **defeito bloqueante** em review/QA.
