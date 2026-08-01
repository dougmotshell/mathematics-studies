# Log — TCK-0008

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:42 — tech-lead
- Ação: criação do ticket a partir das ACTIONs A-1, A-2 e A-3 do `qa-validator#4`
  (`TCK-0003/log.md` `[015]`), com o pedido copiado verbatim.
- Motivo: sete artefatos lidos por agentes ainda descrevem a stack como indecidida depois de
  o `ADR-0003` ter sido aceito em 2026-08-01. Nenhum é área do `platform-architect` — quatro
  são memórias de outros agentes e três são o **ferramental do `tech-lead`**, por isso o
  ticket é meu.
- Resultado: ok — `tickets/TCK-0008-clear-stale-platform-stack-state/` criado.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:44 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** os oito pontos (7 + D-1) são **a mesma
  afirmação obsoleta** em oito lugares; corrigi-los em tickets separados repetiria oito vezes
  a mesma varredura de verificação e a mesma execução de `sync-ai-adapters.py`, que é o custo
  real da tarefa.
- **Inclusão do D-1 aqui, contrariando o `[015]` A-2** ("entra em qualquer edição futura do
  ADR, sem ticket próprio"): sem ticket, uma dívida de uma palavra fica órfã indefinidamente,
  e ela é da **mesma classe** dos outros sete (frase que descreve mal o estado decidido do
  ADR-0003). Registro a decisão em vez de mudar o critério de outro agente em silêncio.
- **Tipo:** `docs`. Toca prosa normativa, memórias e um `.js` de prompt — nenhum código de
  produção, nenhuma dependência. Não é `infra`: não há build, deploy nem ambiente envolvido.
- **Prioridade P2 · tamanho P.** Não condiciona a saída de `draft` do nó piloto nem o próximo
  nó — por isso não é P1. Mas está acima de P3 por dois motivos: o custo é de minutos, e o
  ponto de maior risco (`memory/agents/tech-lead.md:16`) corrompe justamente a **triagem** que
  vai abrir a frente de plataforma (Fase 2 do roadmap). Deve estar fechado **antes do primeiro
  ticket de `frontend-developer` / `backend-developer` / `devops-engineer`**.
- **Owner: `tech-lead`** (eu) — `.claude/agents/tech-lead.md`, `.claude/skills/ticket/SKILL.md`,
  `.claude/workflows/feature-plan-review.js` e `memory/agents/tech-lead.md` são meu papel e meu
  ferramental. `docs/adr/ADR-0003:95` (D-1) é edição de uma palavra num ADR aceito, sem mudar
  decisão; se o executor julgar que precisa do `platform-architect`, faz handoff em vez de
  editar — registro a alternativa aqui para não travar depois.
- **Cadeia:** `tech-lead` → (`product-analyst`, `docs-writer`, `a11y-ux-reviewer`, cada um só
  na **própria** memória — AGENTS.md §5) → `code-reviewer` → `qa-validator`. As três passagens
  de memória são independentes entre si e podem correr em paralelo. **Eu produzo, logo não
  valido**: o `done` é do `qa-validator`, com evidência por critério.
- **Restrições passadas ao executor:**
  1. `.claude/agents/`, `.claude/skills/` e `.claude/workflows/` são **fontes canônicas** —
     rodar `python3 scripts/sync-ai-adapters.py` na mesma entrega e nunca editar gerado à mão.
  2. Aplicar **L-013**: extrair o termo de busca do defeito e varrer o repositório inteiro,
     não só as oito linhas citadas — o TCK-0003 já perdeu uma sétima ocorrência por varredura
     parcial (S7 de `[014]`).
  3. Preservar a **norma** ao remover o exemplo envelhecido: "decisão estrutural exige ADR
     aceito" continua valendo; some o exemplo, não a regra.
  4. Não tocar `content/`, `docs/specs/` (TCK-0002) nem logs de tickets fechados.
- **Aderência ao plano:** manutenção da superfície de IA (`docs/ai/tool-support.md`,
  ADR-0004). Não é feature nova, não consome orçamento de fase.
- **Requisitos inegociáveis:** nenhum é acionado — artefatos internos, sem conteúdo de
  usuário, sem dados pessoais, sem custo. Registrado no ticket com o porquê de cada `não
  aplicável`, para a triagem não parecer omissa.
- **Dependências:** nenhuma. Pode correr em paralelo com TCK-0006/0007 (arquivos disjuntos) —
  atenção só à concorrência de `sync-ai-adapters.py` se o TCK-0006 estiver tocando `AGENTS.md`
  ao mesmo tempo: o `--check` já ficou vermelho uma vez por causa alheia (`[014]`).
- Resultado: ok — `status: triaged`, `owner: tech-lead`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
