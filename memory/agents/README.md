# Memória individual por agente

Cada agente definido em `.claude/agents/` tem aqui um arquivo `<name>.md` com sua memória
persistente. Sessões são efêmeras; **o repositório é a memória**.

## Contrato

- **Antes de trabalhar:** o agente lê `memory/MEMORY.md`, este arquivo (`<name>.md`), o
  contexto da sua área em `memory/context/` e as lições relevantes de `memory/LESSONS.md`.
- **Ao concluir tarefa significativa:** atualiza "Notas persistentes" (conhecimento durável
  sobre o próprio papel) e adiciona uma linha em "Últimas execuções".
- **Conhecimento generalizável** não fica aqui: vira lição em `memory/lessons/` ou entra no
  contexto da área em `memory/context/`.

## Regras

1. Datas absolutas (`2026-08-01`), nunca relativas.
2. Nota que virou regra para todos → promover a lição e remover daqui.
3. Nada de PII, segredo ou dado real de usuário.
4. Subagentes (`<agente>#N`) compartilham a memória do agente-pai — não criar arquivo
   separado.
