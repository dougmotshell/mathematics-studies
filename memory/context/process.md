# Contexto operacional — process

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01 (re-escopo do TCK-0007 e abertura dos TCK-0017 e TCK-0018)

## Estado atual

- Superfície de IA cobre 12 ferramentas a partir de **três fontes canônicas**:
  `.claude/agents/`, `.claude/skills/` e `.github/instructions/`. Todo o resto é gerado por
  `python3 scripts/sync-ai-adapters.py`. Matriz: `docs/ai/tool-support.md`.
- Fluxo de trabalho por tickets ativo (ADR-0004). Backlog em 2026-08-01, depois da triagem
  das pendências herdadas: **TCK-0001…TCK-0005 `done`** (referências do nó piloto, fatia
  mínima de aprendizagem, aceite do `ADR-0003`, licença do projeto, a11y matemática do nó
  piloto) e **TCK-0006…TCK-0011 `triaged` sem handoff**, aguardando ordem de execução —
  `0006` convenções de leitura de fórmula (`docs-writer`, P1) → `0007` correções do nó piloto
  para sair de `draft` (`content-author`, P1, **depende do 0006**) → `0008` limpeza do estado
  obsoleto do `ADR-0003` (`tech-lead`, P2) → `0009` schema de `references.json`
  (`backend-developer`, P2) → `0010` licença do *Livro Aberto* (`researcher`, P2, pode parar
  em `blocked: human-input`) → `0011` C4 Container + ADR de CI/CD (`platform-architect`, P3,
  antes do primeiro ticket de aplicação). Acionar com `/ticket-loop TCK-NNNN` quando o
  usuário pedir execução — triagem não dispara ninguém (L-005).
- **Backlog aferido em 2026-08-01, 19:35** (lido do campo `status:` de cada `ticket.md`, não de
  memória): `done` — 0001, 0002, 0003, 0004, 0005, 0011, 0012, 0013, 0014; **em curso** — 0006
  `in_validation`, 0015 `in_progress` (`devops-engineer`), 0016 `in_review`
  (`platform-architect`); **`triaged` sem handoff** — 0007 (`content-author`, P1), 0008
  (`tech-lead`, P2), 0009 (`backend-developer`, P2), **0017** (`backend-developer`, P1),
  **0018** (`exercise-designer`, P1); **`blocked: human-input`** — 0010 (`researcher`, P2 —
  licença do *Livro Aberto*, dono: usuário).
- **Ordem recomendada a partir daqui:** `0017` (auditor de conteúdo delega o contrato ao
  validador — é portão de CI e hoje aprova gabarito errado em silêncio) → `0007` ‖ `0018`
  (metades disjuntas do nó piloto, ambas dependem do `0006` fechar) → `0008` → `0009`.
  `0010` só sai com decisão humana.
- **Duas ferramentas sobre `content/`, com papéis distintos e uma fronteira em disputa até o
  TCK-0017:** `scripts/validate-content.py` (TCK-0014, `done`) responde "este arquivo pode ser
  carregado?" — por nó, chamado pelo `prebuild` do `package.json` e pelo CI
  (`ai-surface-audit.yml:64`); `scripts/audit-content.py` responde "este acervo é coerente?" —
  grafo de pré-requisitos, `references.json`, `content/paths/`, portões de `published`
  (`:51` do mesmo CI). **Enquanto o TCK-0017 não rodar, `exit 0` de `audit-content.sh` não é
  evidência de contrato íntegro** (aceita `"correct": "false"` como gabarito válido e título
  não-string); em ticket de conteúdo, rodar também `bash scripts/validate-content.sh`.

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
