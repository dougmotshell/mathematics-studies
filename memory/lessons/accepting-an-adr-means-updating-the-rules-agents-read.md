**Tipo:** erro
**ID:** L-010
**Contexto:** 2026-08-01, `TCK-0003` — o aceite do `ADR-0003` foi gravado no ADR, no
`docs/adr/README.md` e na memória, mas `AGENTS.md`, `.github/instructions/` e
`.claude/agents/` continuaram mandando "tratar a stack como hipótese". `REJECT` do
`code-reviewer` (defeito B1): o desbloqueio era inerte exatamente onde importa.

**Lição:** agente não lê ADR por iniciativa própria — lê o `AGENTS.md` e as regras da
ferramenta no início da sessão. Enquanto a regra disser o contrário do ADR, **a regra vence**,
e o ticket de aceite não entrega seu propósito por mais completo que o documento esteja. O
custo de propagar foi alegado como motivo para adiar; era falso: `AGENTS.md` e `docs/` não são
gerados, e `.github/instructions/` + `.claude/agents/` são fontes canônicas cujo sync é
determinístico (`python3 scripts/sync-ai-adapters.py`, verificado por
`scripts/audit-ai-surface.sh`).

**Como aplicar:** ao aceitar ou substituir um ADR, antes de fazer handoff rodar
`grep -rn "ADR-NNNN" . --exclude-dir=.git` — varredura da **raiz**, não de uma lista de
diretórios escolhida a dedo: no `TCK-0003` a busca restrita a `AGENTS.md docs/ memory/
.claude/ .github/` deixou passar o `README.md`, que é a primeira coisa que um humano lê.
Tratar **toda** ocorrência que descreva a decisão como pendente. Corrigir o que é da própria área; listar no log, como
pendência endereçada ao `tech-lead`, o que é de área alheia — nunca deixar ambos implícitos.
Mexeu em `.claude/agents/` ou `.github/instructions/` → rodar `sync-ai-adapters.py` (sem
`--check`) e reexecutar a auditoria. Ver [[client-side-answer-key-is-a-product-constraint]].
