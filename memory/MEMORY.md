# MEMORY.md — Índice da memória compartilhada dos agentes

> Uma linha por memória. Ler este índice no início de toda tarefa significativa; abrir apenas
> os arquivos relevantes. Regras completas na seção 5 do `AGENTS.md` e em
> `docs/ai/ticket-protocol.md`.

## Contexto

- [project-context](context/project-context.md) — estado atual do projeto por frente
  (conteúdo, plataforma, superfície de IA, documentação).

## Contexto operacional por área

> Documento vivo por área: pegadinhas do ambiente, estado atual, decisões operacionais.

- [process](context/process.md) — fluxo de tickets, triagem, convenções de trabalho.
- [frontend](context/frontend.md) — interface, PWA, KaTeX, i18n, temas.
- [backend](context/backend.md) — dados, progresso, pipeline de conteúdo, integrações.
- [devops](context/devops.md) — CI/CD, Vercel, ambientes, monitoramento.
- [qa](context/qa.md) — validação, e2e, casos hostis, flakiness.
- [security](context/security.md) — privacidade de menores, segredos, dependências.
- [content](context/content.md) — produção de teoria e exercícios, revisão matemática.
- [curriculum](context/curriculum.md) — taxonomia, trilhas, grafo de pré-requisitos.

## Sub-índices

- [LESSONS](LESSONS.md) — índice de lições classificado por tipo (`sucesso | erro |
  correção`), com identificadores `L-NNN` citáveis nos logs de ticket.
- [agents/](agents/README.md) — memória individual por agente (`memory/agents/<name>.md`).

## Lições

- [L-001 · bilingual-content-is-not-translated-later](lessons/bilingual-content-is-not-translated-later.md)
  — conteúdo nasce nos dois idiomas; traduzir depois produz dívida que não se paga.
- [L-002 · verify-before-publishing-answers](lessons/verify-before-publishing-answers.md)
  — gabarito só existe depois de verificação independente.
- [L-003 · content-slugs-are-public-urls](lessons/content-slugs-are-public-urls.md)
  — slug de `content/` é contrato público; renomear quebra links de terceiros.
- [L-004 · global-prompt-dirs-collide-between-repos](lessons/global-prompt-dirs-collide-between-repos.md)
  — comandos em diretório global por usuário colidem entre projetos; isolar ou prefixar.
- [L-005 · triage-is-not-handoff](lessons/triage-is-not-handoff.md)
  — triar um ticket não é `HANDOFF`; só o `HANDOFF` dispara execução imediata do próximo
  agente.
- [L-006 · openstax-license-varies-by-book](lessons/openstax-license-varies-by-book.md)
  — licença do OpenStax varia por livro; verificar na própria página antes de registrar.
- [L-007 · license-must-be-readable-without-javascript](lessons/license-must-be-readable-without-javascript.md)
  — sem licença legível fora de JS, a fonte não entra em `references.json`.
- [L-008 · client-side-answer-key-is-a-product-constraint](lessons/client-side-answer-key-is-a-product-constraint.md)
  — sem servidor, o gabarito viaja no cliente; o ADR declara o que a decisão proíbe ao
  produto e o que exige ADR novo.
- [L-009 · share-alike-license-excludes-nc-sources](lessons/share-alike-license-excludes-nc-sources.md)
  — sob CC BY-SA 4.0, fonte NC só pode ser citada como leitura externa, nunca adaptada.
- [L-010 · accepting-an-adr-means-updating-the-rules-agents-read](lessons/accepting-an-adr-means-updating-the-rules-agents-read.md)
  — ADR aceito sem propagação para `AGENTS.md` e as regras das ferramentas é desbloqueio
  inerte: o agente obedece a regra, não o ADR.
- [L-011 · adr-decides-constraints-not-implementation-timing](lessons/adr-decides-constraints-not-implementation-timing.md)
  — ADR fixa resultado exigido, não mecanismo nem momento de execução; o resto é decisão do
  ticket.
- [L-012 · formula-description-is-checked-by-order-not-by-count](lessons/formula-description-is-checked-by-order-not-by-count.md)
  — descrição de fórmula em display se verifica pela ordem (alternância estrita fórmula →
  descrição), não pela contagem; descrever é ler a estrutura, não nomear a fórmula.
- [L-013 · fixing-the-cited-line-is-not-fixing-the-defect-class](lessons/fixing-the-cited-line-is-not-fixing-the-defect-class.md)
  — o `REJECT` lista evidências, não o inventário: varrer o artefato inteiro pelo termo do
  defeito, diagrama e tabela incluídos.
- [L-014 · theorem-hypotheses-belong-in-the-statement](lessons/theorem-hypotheses-belong-in-the-statement.md)
  — hipótese de existência faz parte do enunciado do teorema; omiti-la produz afirmação
  mal-formada, não falsa, e por isso invisível à verificação numérica.
- [L-015 · a-monitor-that-guesses-must-guess-pessimistically](lessons/a-monitor-that-guesses-must-guess-pessimistically.md)
  — quando o limiar depende de palpite, presumir o pior caso e fazer a incerteza sair pelo
  canal automático; falso alarme é ruído, falso silêncio é dano.
- [L-016 · widening-a-permission-allowlist-is-not-preserving-it](lessons/widening-a-permission-allowlist-is-not-preserving-it.md)
  — allowlist ampliada é mudança de segurança: só é "preservado" o bloco idêntico ao do
  `HEAD`, provado por `diff` de `jq -S`.
- [L-017 · an-assumption-refuted-by-the-measurement-must-be-abandoned](lessons/an-assumption-refuted-by-the-measurement-must-be-abandoned.md)
  — medida que desmente a presunção obriga a abandoná-la; alarme saturado no topo da escala
  precisa de rearme ao trocar a régua.
- [L-018 · fixing-the-cause-is-not-fixing-the-outcome](lessons/fixing-the-cause-is-not-fixing-the-outcome.md)
  — o defeito sobrevive mudando de forma: verificar a promessa da funcionalidade encenada
  inteira, não o caso citado no `REJECT`.
- [L-019 · a-validator-only-protects-what-it-can-see](lessons/a-validator-only-protects-what-it-can-see.md)
  — portão que não enxerga o objeto (inclusive subnó abaixo do alvo) ou perde o veredito na
  saída quebrada (stdout **e** stderr) aprova conteúdo defeituoso em silêncio; contém adendo
  de reincidência: registrar a **classe** do defeito, não a lista de casos corrigidos.
- [L-020 · public-contract-goes-to-adr-mechanism-goes-to-ticket](lessons/public-contract-goes-to-adr-mechanism-goes-to-ticket.md)
  — contrato público e permanente vai para ADR; mecanismo trocável fica com o ticket — e ADR
  `proposed` do qual um ticket depende bloqueia o ticket, o que precisa ser declarado.
- [L-021 · a-norm-that-names-the-strict-case-leaves-the-frequent-case-unruled](lessons/a-norm-that-names-the-strict-case-leaves-the-frequent-case-unruled.md)
  — o caso que a norma não nomeia fica permitido; fechar a lacuna é dar a ele obrigação
  diferente e mais barata, com gatilho inspecionável, testado contra o artefato real; com
  adendos: padrão de varredura e alvos de propagação vêm da definição, não dos exemplos; e
  quem reenuncia a regra cita o veredito do teste — checklist referencia, nunca reenuncia.
- [L-022 · writing-a-rule-is-not-applying-it](lessons/writing-a-rule-is-not-applying-it.md)
  — regra em seção terminal não governa o corpo do documento: enunciar na seção estrutural,
  nomear as exceções e varrer item a item (prosa **e** diagrama) antes de entregar; com adendo
  sobre pares simétricos, na família de `L-013` e `L-021`.
- [L-023 · a-collection-wide-license-claim-does-not-bind-each-work](lessons/a-collection-wide-license-claim-does-not-bind-each-work.md)
  — licença declarada "do projeto" não vincula cada obra: no *Livro Aberto de Matemática* o
  selo varia por capítulo (15 BY-SA × 13 BY-NC-SA em 28); auditar todos os artefatos, validar o
  automatismo contra leitura direta e, em divergência, concluir "indeterminado".
- [L-024 · a-pointer-with-a-copy-beside-it-is-not-a-pointer](lessons/a-pointer-with-a-copy-beside-it-is-not-a-pointer.md)
  — ponteiro com cópia enumerada ao lado são **duas** fontes, e o leitor obedece a que está ao
  alcance dos olhos; nomear a âncora (arquivo + entrada + seção) e não enumerar. Teste: se a
  fonte dobrar amanhã, o texto fica **errado** ou só incompleto?
- [L-025 · authorization-to-execute-is-not-acceptance-of-the-decision](lessons/authorization-to-execute-is-not-acceptance-of-the-decision.md)
  — autorização do usuário destrava execução, aceite de ADR fixa decisão; ADR `proposed` cujos
  artefatos já existem é sintoma detectável, e quem escreve "nenhum ticket pode X antes do
  aceite" sai do ticket pedindo também o ticket de aceite.
