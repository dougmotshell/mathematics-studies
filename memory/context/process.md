# Contexto operacional — process

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01 (dev-loop `analyze-open-tickets`)

## Estado atual

- Superfície de IA cobre 12 ferramentas a partir de **três fontes canônicas**:
  `.claude/agents/`, `.claude/skills/` e `.github/instructions/`. Todo o resto é gerado por
  `python3 scripts/sync-ai-adapters.py`. Matriz: `docs/ai/tool-support.md`.
- Fluxo de trabalho por tickets ativo (ADR-0004). Backlog em 2026-08-01:
  - `TCK-0001` (verificar referências do nó piloto) — `triaged`, owner `researcher`,
    P2/P. Plano de execução já registrado no log; **handoff ainda não disparado** — acionar
    com `/ticket-loop TCK-0001` quando o usuário pedir execução (não diagnóstico).
  - `TCK-0002` (definir a fatia mínima de aprendizagem) — `triaged`, owner `task-router`,
    P1/M. Dev-loop em `.dev-loop/minimum-learning-slice/` parado na etapa `plan`
    (`product-analyst`) — **retomar, nunca reiniciar** (`loop.md` guarda a iteração 1/3).

## Pegadinhas conhecidas

- **Nunca editar adapter gerado à mão** — a próxima geração sobrescreve. Arquivos com o
  marcador `managed-by:mathematics-studies/sync-ai-adapters` são gerados; sem o marcador,
  são preservados (é assim que se personaliza um adapter de propósito).
- **Limite de 12.000 caracteres** em regras do Antigravity e do Windsurf. O `AGENTS.md`
  (≈ 25 mil) não cabe: por isso existe `.github/instructions/core.instructions.md`, o resumo
  sempre ativo. O gerador falha se alguma regra passar do limite.
- **O corpo do `core.instructions.md` é reaproveitado em várias profundidades** de diretório
  (`.cursor/rules/`, `.junie/`, raiz). Links relativos ali quebram em alguns destinos —
  citar caminhos como texto, a partir da raiz.
- **`$CODEX_HOME/prompts` é global por usuário** — ver lição L-004.

## Decisões operacionais em vigor

- Ao alterar agent, skill ou regra: rodar `python3 scripts/sync-ai-adapters.py` na mesma
  entrega. O CI falha se os adapters estiverem desatualizados.
- Ferramenta nova entra pelo passo a passo de `docs/ai/tool-support.md`
  ("Adicionando uma ferramenta nova"), nunca com arquivos escritos à mão.
