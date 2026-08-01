# Memória do agente `platform-architect`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Desenha a arquitetura da plataforma web/PWA — estrutura da aplicação, modelo de dados de conteúdo e progresso, renderização, offline, i18n, autenticação e deploy na Vercel. Usar para decisões estruturais, ADRs de stack e diagramas C4.

## Notas persistentes

- **Stack em vigor desde 2026-08-01 (`ADR-0003`, accepted):** site estático orientado a
  conteúdo (Astro) com **ilhas de interatividade** só onde há exercício; progresso
  **local-first sem conta** (IndexedDB); PWA offline-first para o conteúdo visitado; rotas
  estáticas por idioma; deploy estático na Vercel, portátil para qualquer host estático.
- **Fronteira dura do que ficou decidido:** não existe backend, conta, login nem telemetria
  identificável. Cada um desses exige **ADR novo** (com LGPD/COPPA — há menores no público).
  Não instruir implementação que os pressuponha.
- **Fora do `ADR-0003` de propósito:** biblioteca de UI, framework de testes e estratégia de
  service worker são decisões de implementação. Resistir a decidi-las em ADR de stack.
- **Consequência de produto que sempre volta:** sem servidor, o gabarito viaja no cliente —
  nada pode depender do segredo da resposta (L-008). Fóruns e certificados do roadmap não têm
  solução nesta arquitetura.
- **Restrição a preservar em qualquer decisão futura:** o contrato de dados de `content/` é
  independente da stack. Teste de conformidade: um leitor escrito do zero, sem a aplicação,
  reconstrói taxonomia, rotas por idioma e exercícios só lendo os arquivos + `docs/content/`.
- **Aceitar ADR = atualizar as regras que os agentes leem** (L-010). O aceite só existe de
  fato depois de varrer `grep -rn "ADR-NNNN" . --exclude-dir=.git` — **da raiz**, nunca de uma
  lista de diretórios escolhida a dedo. No `TCK-0003` isso custou dois REJECTs: a primeira
  passagem esqueceu `AGENTS.md` §1/§11, `.github/instructions/{core,app}`,
  `.claude/agents/platform-architect.md` e `docs/product/roadmap.md`; a segunda ainda deixou
  `README.md` e `prompts/bootstrap-session.md`. Checklist mínimo: ADR + `docs/adr/README.md`
  + `AGENTS.md` + `README.md` + `prompts/` + `.github/instructions/` + `.claude/agents|skills|
  workflows` + `docs/product/roadmap.md` + `docs/architecture/` + `memory/context/`.
  Mexeu em fonte canônica → `python3 scripts/sync-ai-adapters.py` (sem `--check`) e reauditar.
- **"Custo do sync" não é desculpa para adiar propagação**: `AGENTS.md`, `README.md`,
  `roadmap.md` e `prompts/` não são gerados; o resto é determinístico e verificado pela
  auditoria. Argumento recusado com razão pelo `code-reviewer`.
- **O que é de outra área vai para o log como pendência nominal**, não fica implícito:
  `memory/agents/{tech-lead,product-analyst,docs-writer}.md`, `.claude/agents/tech-lead.md`,
  `.claude/skills/ticket/SKILL.md`, `.claude/workflows/feature-plan-review.js` ainda dizem
  `ADR-0003 proposed` — ticket pedido ao `tech-lead`.
- **ADR decide resultado, não mecanismo nem momento** (L-011). "Pré-renderizado na build"
  virou defeito: o exigível era "KaTeX acessível, sem custo de JS desproporcional". Antes de
  entregar um ADR, para cada consequência perguntar "isto admite mais de uma implementação?";
  se sim, mover para a lista do que o ADR **não** decide.
- **Corrigir `REJECT` = varrer a classe do defeito, não as linhas citadas** (L-013). O
  `REJECT` traz evidências, não o inventário. Extrair um **termo de busca** do defeito e rodar
  `grep` sobre todos os artefatos antes do handoff — no `TCK-0003`, `grep -n "renderiz"` teria
  pego o rótulo do Mermaid que custou o loop 2/3.
- **Diagrama é normativo** (`docs/DOC-STANDARDS.md`): rótulo de nó Mermaid, tabela e front
  matter entram na revisão com o mesmo peso da prosa. Meu viés é revisar texto corrido e não
  reler o diagrama que eu mesmo escrevi.
- **`CORRECTION` usa os rótulos literais** de `docs/ai/ticket-protocol.md:173-177`:
  `Corrige:` / `O que estava errado:` / `Registro correto:`.
- **Auditoria vermelha por trabalho paralelo se prova, não se alega:** quando
  `audit-ai-surface.sh` acusa `OUTDATED`, atribuir a deriva com evidência (`grep -c` do próprio
  texto × do texto do outro ticket nos gerados) antes de concluir que não é sua — e **não**
  rodar o sync se outro agente estiver no meio de uma edição de fonte canônica.
- **Declarar no log todo arquivo tocado, inclusive os da própria área** (AGENTS.md §10,
  regra 2). Reescrevi `docs/architecture/*` sem declarar e virou defeito bloqueante — o
  `qa-validator` não valida o que não foi declarado.
- **Diagrama C4 não mistura decidido com proposto**: CI/CD e previews por branch não têm ADR
  aceito e ficam marcados `PROPOSTO` no `c4-context.md`; afirmação absoluta do tipo "nada aqui
  é hipótese" é armadilha.
- **`docs/adr/README.md` é editado por vários agentes** — sempre edição cirúrgica da linha do
  próprio ADR, nunca reescrita do arquivo.
- Auditorias relevantes ao encerrar: `bash scripts/audit-ai-surface.sh` e
  `bash scripts/audit-content.sh` (ambas devem sair com exit 0).

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0003 — aceite do `ADR-0003` (stack da plataforma) | `accepted`: opção C (estático + ilhas) + persistência local-first sem conta; consequências, restrição do contrato de dados e propagação para README/memória; auditorias verdes; handoff → `code-reviewer` | L-008 |
| 2026-08-01 | TCK-0003 — correção do `[010] REJECT` (loop 2/3) | B4: rótulo do Mermaid do ADR ainda dizia "KaTeX pré-renderizado", contradizendo o texto; corrigido + varredura da classe no arquivo (achou 2ª ocorrência: nó do service worker); leitura do diagrama e S4/S5 acatadas | L-013 |
| 2026-08-01 | TCK-0003 — correção do `[006] REJECT` (loop 1/3) | B1 propagação inerte (7 pontos: `AGENTS.md` §1/§11, `core`/`app` instructions, `.claude/agents/platform-architect.md`, `roadmap.md`, `README.md`, `prompts/bootstrap-session.md`) + sync; B2 ADR deixou de fixar build × runtime do KaTeX; B3 `docs/architecture/*` declarados e contradição de CI/preview resolvida; S1–S3 acatadas | L-010, L-011 |
