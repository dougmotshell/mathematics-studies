---
applyTo: "memory/**"
---

# Instruções para `memory/`

- `memory/MEMORY.md` é o índice: uma linha por memória, sem conteúdo detalhado.
- Uma lição por arquivo em `memory/lessons/`, nome en-US kebab-case, conteúdo pt-BR no
  formato `**Tipo:** sucesso | erro | correção` / `**ID:** L-NNN` / `**Contexto:**` (data
  absoluta) / `**Lição:**` / `**Como aplicar:**`. Toda lição nova ganha linha em
  `memory/LESSONS.md` (índice por tipo) **e** em `memory/MEMORY.md`.
- Lição é **regra aplicável no futuro**, não resumo de tarefa. Lição superada não é apagada:
  registre uma nova referenciando a antiga.
- `memory/agents/<name>.md` é a memória individual de cada agente (chatmode homônimo no
  Copilot): ler no início da tarefa, atualizar ao concluir (notas persistentes + linha em
  "Últimas execuções"). Subagentes (`<agente>#N`) compartilham a memória do agente-pai.
- `memory/context/<área>.md` é documento **vivo** por área (process, frontend, backend,
  devops, qa, security, content, curriculum): pegadinhas do ambiente, estado atual, decisões
  operacionais. Atualizar com data ao final de ticket que mude esse conhecimento.
- `memory/context/project-context.md` guarda o estado do projeto — atualizar quando o estado
  mudar, com datas absolutas.
- Antes de criar memória nova, verifique se já existe uma que cobre o assunto — atualize em
  vez de duplicar; remova as que se provaram erradas.
- Nunca registrar PII, segredo ou dado real de usuário.
