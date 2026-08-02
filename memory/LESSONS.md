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

- [L-023](lessons/a-collection-wide-license-claim-does-not-bind-each-work.md) — 2026-08-01 — conteúdo —
  declaração de licença "do projeto" não vincula cada obra: no *Livro Aberto de Matemática* o
  selo variou **por capítulo** (15 BY-SA × 13 BY-NC-SA em 28); auditar todos os artefatos e, em
  divergência, concluir "indeterminado" — nunca o mais permissivo.

- [L-024](lessons/a-pointer-with-a-copy-beside-it-is-not-a-pointer.md) — 2026-08-01 — process —
  ponteiro com cópia enumerada ao lado não é ponteiro, são **duas fontes**: quando a fonte muda,
  a cópia passa a contradizê-la em silêncio e é nela que o leitor acredita. Nomear a âncora
  (arquivo + entrada + seção) e não enumerar itens ao lado.

- [L-025](lessons/authorization-to-execute-is-not-acceptance-of-the-decision.md) — 2026-08-01 — process —
  autorização do usuário destrava a **execução**; o aceite de ADR fixa a **decisão** — um não
  substitui o outro. ADR `proposed` cujos artefatos já existem no working tree é sintoma
  detectável; quem escreve "nenhum ticket pode X antes do aceite" sai do ticket pedindo também
  o ticket de aceite.

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
- [L-019](lessons/a-validator-only-protects-what-it-can-see.md) — 2026-08-01 — backend —
  portão que não enxerga o objeto (nó sem `meta.json`, subnó abaixo do alvo, caminho errado) ou
  que perde o veredito na saída quebrada (`| head`, `>&-`, `> /dev/full`, em stdout **e**
  stderr) aprova conteúdo defeituoso em silêncio. **Com adendo de reincidência no próprio
  TCK-0014** (REJECT [006]): corrigir os casos citados não é corrigir a classe — a regra vale
  para toda a travessia e para todos os canais (ver L-013 e L-018). **Segundo adendo,
  TCK-0015** (REJECT [006]): a classe vale fora do validador — passo de CI com `if grep …`
  fica verde quando o alvo não existe (`grep` sai `2`), e portão certo posto em só um dos
  caminhos que chegam ao aluno protege só aquele caminho. **Terceiro adendo, TCK-0015**
  (REJECT [010]): afrouxar um detector para eliminar falso positivo é reescrevê-lo, e o novo
  precisa da bateria **inteira** — trocar regra de classe por lista de casos deixou 8 de 18
  vetores passarem calados (protocolo relativo, aspas simples, `ping`, tag em maiúscula).
- [L-022](lessons/writing-a-rule-is-not-applying-it.md) — 2026-08-01 — design —
  regra escrita em seção terminal (riscos, notas) não governa o corpo do documento: ela nasce
  na seção estrutural, com as exceções nomeadas, e só está aplicada depois de varrer item a
  item — foi assim que "mover foco **ou** anunciar" foi violada em 3 dos 13 estados no mesmo
  documento que a definia. **Adendo (loop 2):** a varredura alcança diagrama e rótulo, não só
  prosa, e regra escrita para um lado de um par simétrico (idioma, sentido, extremo) deixa o
  outro **permitido** — ver `L-013` e `L-021`, da mesma família.

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
- [L-020](lessons/public-contract-goes-to-adr-mechanism-goes-to-ticket.md) — 2026-08-01 —
  plataforma — o que separa ADR de ticket é a **permanência observável de fora** (URL,
  formato de dado, custo → ADR; biblioteca, cache, momento de renderização → ticket); teste:
  "se eu trocar isto em seis meses, quem quebra?".
- [L-021](lessons/a-norm-that-names-the-strict-case-leaves-the-frequent-case-unruled.md) —
  2026-08-01 — conteúdo — norma que nomeia só o caso estrito **permite** o caso deixado de
  fora; feche a lacuna com obrigação **diferenciada** e gatilho mecânico (teste do argumento
  composto: display pede leitura integral, inline pede o agrupamento em palavras), e rode o
  teste contra o conteúdo real antes de publicar a norma. **Adendo (REJECT do TCK-0006):**
  padrão de busca e lista de propagação se derivam da **definição da classe** e dos artefatos
  que a regra nomeia — nunca das ocorrências e dos arquivos que você já tinha em mãos.
  **2º adendo:** quem *reenuncia* uma regra cita o **veredito do teste**, não a lista de
  gatilhos; checklist e portão **referenciam, nunca reenunciam** — senão o gatilho novo passa
  pelo portão antigo.
