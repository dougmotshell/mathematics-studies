# Log — TCK-0006

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:30 — tech-lead
- Ação: criação do ticket a partir das pendências 4 e 5 encaminhadas pela cadeia do TCK-0005
  (`log.md` `[007]`, `[008]` §6 e §7.3, `[010]`, `[011]`), com o pedido original copiado
  verbatim dos logs de origem.
- Motivo: as duas convenções foram **decididas na prática** pelo nó piloto e aprovadas por
  `a11y-ux-reviewer` e `i18n-steward`, mas não existem por escrito. O piloto é o modelo que
  os próximos nós copiam; convenção não escrita se multiplica divergente.
- Resultado: ok — `tickets/TCK-0006-formula-reading-conventions/` criado com `ticket.md` e
  este `log.md`. Nenhum arquivo fora de `tickets/` tocado.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:32 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** — o usuário pediu criação e
  triagem, não execução (L-005: triagem não é handoff).
- **Agrupamento (justificativa em uma linha):** as convenções de a11y, a linha de glossário
  de i18n e a fronteira display × inline são a **mesma entrega** — a norma escrita que o
  próximo nó vai copiar — e todas vivem em `docs/content/` + `AGENTS.md` §9.2; separá-las
  produziria três tickets de uma linha que o mesmo agente abriria no mesmo arquivo.
- **Tipo:** `docs`. Não é `content`: nada em `content/` muda aqui. A decisão da §9.2 é
  refinamento de regra existente, não decisão estrutural nova — por isso **não** exige ADR
  (critério: ADR quando muda o pilar, não quando precisa a redação de uma regra vigente).
  Gatilho de escalada declarado no "Fora de escopo".
- **Prioridade P1 · tamanho M.** P1 porque é declarado pelas duas revisões como
  **obrigatório antes do próximo nó** e porque **bloqueia o TCK-0007**: sem a decisão de
  (4), o ticket de conteúdo não sabe se trata `\dfrac` inline e as 10 `\frac` de
  `exercises.json`. M porque envolve três arquivos de padrão, a fonte canônica `AGENTS.md` e
  a regeneração dos 12 adapters.
- **Owner: `docs-writer`.** Área de `docs/` e da propagação para as fontes canônicas.
  `a11y-ux-reviewer` e `i18n-steward` entram como **fonte** (o conteúdo normativo já foi
  produzido por eles em `[008]` §6 e `[007]`), não como validadores do próprio texto.
- **Cadeia:** `tech-lead` → `docs-writer` → `code-reviewer` → `qa-validator`. A cadeia
  padrão de `docs` termina em `code-reviewer`; acrescento o `qa-validator` porque só ele
  marca `done` (AGENTS.md §10, regra 3) e porque há 9 critérios verificáveis por comando.
  Independência preservada: quem escreveu a tabela em `[008]` não valida sua transcrição.
- **Restrições passadas ao executor:**
  1. `AGENTS.md`, `.claude/` e `.github/instructions/` são **fontes canônicas** — ao tocá-las,
     rodar `python3 scripts/sync-ai-adapters.py` na mesma entrega; nunca editar gerado à mão.
  2. Regra de 12.000 caracteres do Antigravity/Windsurf: o acréscimo à §9.2 tem de ser curto
     o bastante para o `core.instructions.md` continuar dentro do limite (`--check` falha).
  3. A tabela de `[008]` §6 é transcrita **como decidida**; mudar qualquer par (p. ex. trocar
     "abre/fecha parênteses" por MathSpeak "left/right") é decisão nova e volta ao
     `tech-lead` — a observação 1 de `[007]` registrou essa alternativa como escolha de
     registro, não como defeito.
  4. Não tocar `content/` (é o TCK-0007) nem `docs/adr/`.
- **Aderência ao plano:** Fase 1 do `docs/product/roadmap.md` ("provar o formato com conteúdo
  real … ajustar os schemas se necessário") — este ticket ajusta o **padrão**, que é o que
  autoriza os 3–5 nós piloto seguintes. Dentro do plano, sem pedido fora de escopo.
- **Requisitos inegociáveis conferidos na triagem:** bilinguismo (a tabela é o par de
  convenções nos dois idiomas), acessibilidade (objeto do ticket), gratuidade (só texto),
  offline e privacidade (não aplicáveis, justificado no ticket).
- **Dependências:** bloqueia `TCK-0007` (critério 5 daquele ticket depende do veredito de (4)
  registrado aqui no critério 7).
- Resultado: ok — `status: triaged`, `owner: docs-writer`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
