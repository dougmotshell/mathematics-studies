# LESSONS.md — Índice de lições aprendidas

> Uma lição por arquivo em `memory/lessons/`. Cada lição tem um identificador `L-NNN`
> **estável**, citável nos logs de ticket (`aplicada L-002`, `Lição: L-004`).
> Registro obrigatório nos gatilhos descritos em `docs/ai/ticket-protocol.md`.
>
> **Repetir um erro que já tem lição registrada é defeito bloqueante** em review e QA.

## Como registrar

Use `/capture-lesson`. Formato do arquivo:

```markdown
**Tipo:** sucesso | erro | correção
**ID:** L-NNN
**Contexto:** <onde/quando, com data absoluta e ticket, se houver>
**Lição:** <o que foi aprendido>
**Como aplicar:** <regra prática e verificável para as próximas tarefas>
```

Lição superada não é apagada: registre uma **nova** lição referenciando a antiga.

## Correção

- [L-001](lessons/bilingual-content-is-not-translated-later.md) — 2026-08-01 — conteúdo —
  conteúdo nasce bilíngue; "traduzir depois" vira dívida permanente e conteúdo monolíngue
  publicado.
- [L-006](lessons/openstax-license-varies-by-book.md) — 2026-08-01 — conteúdo —
  a licença do OpenStax varia por livro (CC BY 4.0 **ou** CC BY-NC-SA 4.0); ler na página,
  nunca de memória.

- [L-014](lessons/theorem-hypotheses-belong-in-the-statement.md) — 2026-08-01 — conteúdo —
  hipótese de existência ($\Delta \ge 0$, denominador não nulo, convergência) pertence ao
  **enunciado**, não ao parágrafo seguinte; a omissão não gera afirmação falsa, gera afirmação
  mal-formada — que nenhuma verificação numérica pega.

## Erro

- [L-002](lessons/verify-before-publishing-answers.md) — 2026-08-01 — conteúdo —
  gabarito afirmado sem verificação independente é a principal fonte de erro em plataformas
  de exercícios.
- [L-004](lessons/global-prompt-dirs-collide-between-repos.md) — 2026-08-01 — process —
  diretórios de comandos globais por usuário (ex.: `$CODEX_HOME/prompts`) colidem entre
  repositórios; isolar ou prefixar antes de instalar.
- [L-010](lessons/accepting-an-adr-means-updating-the-rules-agents-read.md) — 2026-08-01 —
  process — aceitar ADR sem atualizar `AGENTS.md`, `.github/instructions/` e `.claude/agents/`
  deixa o desbloqueio inerte: o agente lê a regra, não o ADR.
- [L-011](lessons/adr-decides-constraints-not-implementation-timing.md) — 2026-08-01 —
  plataforma — ADR decide restrição e resultado exigido, não mecanismo nem *momento* de
  execução; o que admite mais de uma implementação vai para a lista do que o ADR não decide.
- [L-013](lessons/fixing-the-cited-line-is-not-fixing-the-defect-class.md) — 2026-08-01 —
  process — corrigir as linhas citadas no `REJECT` não elimina o defeito: varrer o artefato
  inteiro com um `grep` pelo termo do erro, incluindo rótulo de diagrama, tabela e front matter.
- [L-015](lessons/a-monitor-that-guesses-must-guess-pessimistically.md) — 2026-08-01 —
  devops — monitor que adivinha um limite adivinha pelo lado pessimista, e a incerteza
  precisa sair pelo **canal automático** (hook/CI), não só no stdout de quem roda à mão:
  falso silêncio é indistinguível de "está tudo bem".
- [L-016](lessons/widening-a-permission-allowlist-is-not-preserving-it.md) — 2026-08-01 —
  devops — acrescentar entrada em `permissions.allow` é afrouxar controle, não "preservar o
  bloco"; provar preservação com `diff` de `jq -S` contra o `HEAD` e descrever a mudança pelo
  efeito, nunca por "o diff só tem inserções".
- [L-017](lessons/an-assumption-refuted-by-the-measurement-must-be-abandoned.md) — 2026-08-01
  — devops — complementa L-015: presunção desmentida pela própria medição é abandonada (nunca
  vira número autorrefutável), e alarme que satura no topo da escala precisa de rearme quando
  a régua muda, senão o pior estado é também o mais silencioso.
- [L-018](lessons/fixing-the-cause-is-not-fixing-the-outcome.md) — 2026-08-01 — process —
  corrigir a causa citada no `REJECT` não é corrigir o modo de falha: encenar a promessa da
  funcionalidade inteira (estado zerado, sequência realista, mais de um disparo) em vez de
  reproduzir só o caso citado.

## Sucesso

- [L-003](lessons/content-slugs-are-public-urls.md) — 2026-08-01 — currículo —
  tratar slugs como contrato público desde o primeiro nó evita migração de URLs depois.
- [L-005](lessons/triage-is-not-handoff.md) — 2026-08-01 — process —
  triar um ticket (status + owner + plano) não dispara execução; só a entrada `HANDOFF`
  aciona o próximo agente.
- [L-007](lessons/license-must-be-readable-without-javascript.md) — 2026-08-01 — conteúdo —
  fonte só é reutilizável se a licença for legível fora de JavaScript (HTML bruto, página
  institucional estática ou colofão do PDF); na dúvida entre duas declarações, vale a mais
  restritiva.
- [L-008](lessons/client-side-answer-key-is-a-product-constraint.md) — 2026-08-01 —
  plataforma — arquitetura sem servidor coloca o gabarito no cliente; o ADR deve declarar o
  que a decisão **proíbe** ao produto e a lista fechada de recursos que exigem ADR novo.
- [L-009](lessons/share-alike-license-excludes-nc-sources.md) — 2026-08-01 — conteúdo —
  publicar sob CC BY-SA 4.0 exclui fonte **NC** como matéria-prima ("NC = leitura, não
  matéria-prima"); a regra só está propagada quando chega ao `AGENTS.md` e às
  `.github/instructions/`, não só ao ADR e à memória (adendo do REJECT B1 — ver `L-010`).
- [L-012](lessons/formula-description-is-checked-by-order-not-by-count.md) — 2026-08-01 —
  conteúdo — descrição de fórmula em display se verifica pela **ordem** das ocorrências
  (alternância estrita fórmula → descrição), não pela contagem; e descrever é ler a
  estrutura, não nomear a fórmula.
