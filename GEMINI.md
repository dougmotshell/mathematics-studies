# GEMINI.md — Adaptador para o Gemini CLI

> O Gemini CLI carrega este arquivo como contexto hierárquico do projeto. A **fonte única de
> instruções** é o `AGENTS.md` na raiz — leia-o integralmente antes de qualquer tarefa.

@AGENTS.md

## Específico do Gemini CLI

- **Custom commands**: `.gemini/commands/*.toml` — gerados por
  `python3 scripts/sync-ai-adapters.py` a partir das skills (`.claude/skills/`) e dos
  agents (`.claude/agents/`). Comandos de agente ficam no namespace `agent:` (ex.:
  `/agent:math-reviewer`), skills no nível raiz (ex.: `/new-topic`). **Não editar os
  arquivos com o marcador `managed-by` à mão.**
- **Subagentes**: o Gemini CLI não delega para subagentes do Claude. Ao usar
  `/agent:<nome>`, o próprio modelo assume o papel descrito em `.claude/agents/<nome>.md` e
  respeita seus limites, fontes e protocolo de memória.
- **Workflows**: `.claude/workflows/*.js` são específicos do Claude Code. No Gemini, execute
  o equivalente manualmente seguindo as dimensões descritas no arquivo do workflow, ou use
  `tools/dev-loop.sh` para conduzir o loop de forma assistida.
- **Memória**: o Gemini CLI tem memória própria (`/memory`), mas a memória **canônica e
  compartilhada** do projeto é `memory/` (seção 5 do AGENTS.md). Registre ali tudo que
  outros CLIs precisam saber.
- **Ferramentas de shell**: prefira os scripts determinísticos do repositório
  (`scripts/audit-ai-surface.sh`, `scripts/audit-content.sh`) a comandos ad hoc.
- **Tickets**: todo desenvolvimento passa por `tickets/TCK-NNNN-<slug>/`
  (`docs/ai/ticket-protocol.md`). Use `/ticket` para criar e `/handoff` para registrar
  transições. Sem subagentes reais, o Gemini executa os papéis em sequência — assuma um
  papel por vez, registre cada etapa no `log.md` e **nunca valide o que você mesmo acabou de
  produzir sem antes reler o artefato como terceiro**, declarando isso no log.

## Regras que o Gemini costuma esquecer neste projeto

1. Conteúdo do produto é **sempre bilíngue** pt-BR + en-US (AGENTS.md §2b).
2. Nenhuma implementação sem spec aprovada em `docs/specs/`.
3. Resultado matemático não trivial só vira gabarito depois de verificado (`/math-verify`).
4. Não fazer commit ou push sem pedido explícito.
