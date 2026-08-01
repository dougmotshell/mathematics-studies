# Log — TCK-0013

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 15:20 — tech-lead
- Ação: ticket criado a partir do pedido "inicie a implementação do projeto".
- Motivo: o `task-router` encerrou o dev-loop `start-implementation` com saída antecipada —
  implementação da fatia mínima é trabalho de ticket, não de dev-loop (AGENTS.md §10). O
  recorte adotado é **um ticket por task** de `docs/specs/minimum-learning-slice/tasks.md`,
  para não obrigar dois agentes a compartilhar log e diff.
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 15:20 — tech-lead
- Ação: triagem. Critérios de aceite derivados do critério de pronto da task na spec
  aprovada, sem alargar escopo.
- Cadeia: agente da área → `code-reviewer` → `qa-validator`.
- Paralelismo: este ticket e o par (TCK-0013 ‖ TCK-0014) rodam ao mesmo tempo — `tasks.md`
  declara as tasks 3 e 4 paralelizáveis, e as áreas não se sobrepõem.
- Restrições: nenhuma decisão de framework (o `ADR-0003` decidiu site estático com ilhas e
  deixou UI/build/testes em aberto); `content/`, spec e ADRs intocados.
- Resultado: ok — `triaged`.

## [003] HANDOFF — 2026-08-01 15:20
- De: tech-lead → Para: ui-ux-designer
- Status novo: in_progress
- O que foi feito: task da spec recortada em ticket com critérios verificáveis.
- Artefatos: `tickets/TCK-0013-learning-slice-screen-states/ticket.md`.
- Como validar: critérios do ticket + auditorias determinísticas.
- Pendências e riscos: a spec herdou três decisões humanas adiadas (exibir nó `draft`, forma
  da URL bilíngue, rótulo no índice) — elas afetam o desenho e não podem ser fechadas por
  agente.
- Critérios de aceite: [ ] todos restantes.

## [004] ACTION — 2026-08-01 16:40 — ui-ux-designer
- Ação: desenho dos 13 estados de tela e do fluxo `índice → nó → exercício` da fatia mínima.
- Artefatos: `docs/design/minimum-learning-slice/screen-states.md` (documento principal) e
  `docs/design/minimum-learning-slice/README.md` (índice do diretório novo).
- Estados cobertos, nomeados como na tabela de estados da spec — cada um com estrutura de tela,
  texto pt-BR + en-US, ordem de foco, elemento que recebe foco ao entrar e região viva:
  E1 Nó·Carregando · E2 Nó·Erro de carga · E3 Nó·Caminho inexistente · E4 Nó·Rascunho ·
  E5 Exercício·Não respondido · E6 Exercício·Correto · E7 Exercício·Incorreto ·
  E8 Exercício·Dica revelada · E9 Exercício·Solução exibida · E10 Idioma·Alternado ·
  E11 Idioma·Indisponível · E12 Rede·Offline com cache · E13 Rede·Offline sem cache.
  Mais o índice como tela de apoio (RF-1/CA-1), que a tabela de estados não lista.
- Decisões de desenho que restringem as tasks 5–8: os cinco itens ficam na mesma página, sem
  paginador; resultado, dicas e solução entram **abaixo** do grupo de ações para não deslocar
  controle já tabulado; "responder desabilitado" é estado anunciado em controle **focável**,
  não elemento fora da ordem de foco; regra "mover foco **ou** anunciar, nunca os dois para o
  mesmo evento" (E9 move foco, E6/E7/E8 anunciam); todas as regiões vivas educadas, nenhuma
  assertiva; E11 (sem tradução) e E13 (não baixado) são estados distintos e não compartilham
  texto; rótulo de rascunho exibido só no idioma ativo (CA-16 lido junto de RF-7).
- Achado repassado: `tags[]` e `skills[]` chegam do acervo como slug en-US sem tradução —
  exibi-los crus quebra RF-4 em pt-BR. O catálogo de rótulos fica na interface como dívida
  declarada, porque RNF-9 proíbe tocar em `content/` nesta fatia; a migração para um registro
  de habilidades no acervo é ticket de conteúdo/schema.
- Restrições respeitadas: nenhum framework, biblioteca ou componente concreto citado (só papel,
  nome acessível e estado); `content/`, spec e ADRs intocados; nenhum estado com conta, login,
  identificador ou envio de resposta (RNF-7, RF-16); todo texto de interface marcado como
  proposta, com o requisito que obriga sua existência, e as três strings sem requisito
  (`node.draft-title-prefix`, `node.skip-to-exercises`, `network.online-notice`)
  explicitamente marcadas como descartáveis.
- Evidência das auditorias (critério 9): **não executadas nesta sessão** — o ambiente do agente
  não expôs shell. O diff toca apenas `docs/design/**` (diretório novo), `ticket.md`, `log.md`
  e `memory/agents/ui-ux-designer.md`; nenhum caminho auditado por `scripts/audit-ai-surface.sh`
  (fontes canônicas, adapters gerados, arquivos-ponteiro, `memory/context/`, limites de regra)
  nem por `scripts/audit-content.sh` (só `content/`) foi alterado. O `code-reviewer` deve rodar
  as duas antes de aprovar e registrar a saída.
- Resultado: ok — critérios 1–8 atendidos no artefato; critério 9 pendente de execução.

## [005] HANDOFF — 2026-08-01 16:40
- De: ui-ux-designer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: especificação de UI/UX dos 13 estados, fluxo em Mermaid com entradas e
  saídas, catálogo bilíngue de textos de interface, ordem de foco e regiões vivas.
- Artefatos: `docs/design/minimum-learning-slice/screen-states.md`,
  `docs/design/minimum-learning-slice/README.md`.
- Como validar (checklist dos critérios 1–9):
  1. Os 13 estados da tabela de `spec.md` têm seção própria (§6, §7, §10, §11), nomeados como
     na spec; mapa completo em §13 (Rastreabilidade).
  2. Texto de interface em pt-BR e en-US em todas as tabelas de string, sem fallback; coluna
     *Origem* aponta o requisito que obriga cada texto; §1 declara que a redação é proposta.
  3. Cada estado tem parágrafo **Foco** com elemento de entrada e ordem; ordem base em §3.
  4. Cada estado tem parágrafo **Região viva**; E6, E7, E8 e E12 declaram o texto anunciado, e
     §3 lista as regiões existentes — nenhum resultado depende só de cor ou posição.
  5. Fluxo `índice → nó → exercício` em §4, com leitura, fontes e marcação atual × proposta
     (`docs/DOC-STANDARDS.md`).
  6. Rascunho em §6.4, alternador de idioma em §10, os dois estados de rede em §11.
  7. Nenhum framework, biblioteca ou componente concreto — ver §1 e o vocabulário usado.
  8. Nenhum estado com conta, login, identificador ou coleta; §11.2 registra que a lista do que
     está salvo vem do inventário de cache, não de histórico nem de servidor.
  9. **Pendente:** `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` não
     foram executadas (sem shell nesta sessão) — ver a justificativa de escopo do diff em [004].
- Pendências e riscos: riscos do desenho em §14 do documento.
- **Para o `tech-lead` — três decisões humanas continuam abertas** (§12 do documento, com as
  alternativas lado a lado e o custo de cada uma para o aluno; nenhuma foi fechada aqui):
  (a) exibir o nó `status: "draft"` — A1 exibir com rótulo (assumido por RF-5/CA-16) ×
      A2 esconder do índice (contradiz RF-1/CA-1 e exigiria emenda na spec) × A3 confirmação
      antes de entrar;
  (b) forma da URL bilíngue — B1 prefixo × B2 parâmetro × B3 domínio × B4 caminho neutro; a
      escolha muda E10 num ponto: com navegação o anúncio é o título do documento, sem
      navegação é preciso a região viva `language.switched`, e B2/B4 arriscam RNF-8 e RF-8;
  (c) rótulo de rascunho no índice — C1 por nó × C2 só na página do nó × C3 aviso único no topo;
      C1 e C3 são indistinguíveis hoje e divergem no primeiro nó `published`.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [ ] 9.

## [006] REJECT — 2026-08-01 17:35
- De: code-reviewer#5 → Para: ui-ux-designer · Loop nº: 1/3
- Escopo revisado: `docs/design/minimum-learning-slice/screen-states.md` (761 linhas, novo) e
  `docs/design/minimum-learning-slice/README.md`. Cruzamento mecânico estado a estado contra a
  tabela de `spec.md`, paridade das 69 chaves de interface, dados reais de `meta.json`/
  `exercises.json`, Mermaid no parser e as duas auditorias reexecutadas.
- Defeitos (numerados, cada um com evidência e critério violado):
  1. **BLOQUEANTE — a regra "mover foco OU anunciar, nunca os dois para o mesmo evento"
     (`screen-states.md:760`) é violada em três dos treze estados.** Em cada caso o mesmo evento
     move o foco *e* atualiza uma região viva educada; leitor de tela descarta ou embaralha a
     mensagem polida quando o foco muda, então o texto declarado como anunciado pode nunca ser
     ouvido — a declaração do critério 4 fica sem efeito e o critério 3 fica ambíguo.
     (a) E2, erro na carga inicial: foco vai ao título do erro (`:260-262`) **e** a troca
         "carregando → erro" é anunciada pela região viva (`:267-269`) — o título é falado duas
         vezes;
     (b) E5 reentrado por `exercise.retry`: foco vai à área de resposta (`:406-409`, `:469-470`)
         **e** a região de resultado anuncia `exercise.retry-notice` (`:411-413`, `:472-473`) —
         justamente o aviso que §7.1 diz ser indispensável ("sumir em silêncio deixaria quem usa
         leitor de tela achando que o resultado anterior ainda vale");
     (c) E10 sem navegação: foco vai ao controle de idioma (`:586-588`) **e** a região viva
         anuncia `language.switched` (`:590-594`).
     Critério violado: 3 e 4 do ticket; RNF-6 da spec. Escolher um dos dois por evento e
     registrar a escolha em cada um dos três pontos.
  2. **BLOQUEANTE — E1 declara um anúncio que a marcação descrita não produz.** §3 define o
     escopo da região viva de carga como "Seção de exercícios" (`:102`) e §6.1 diz que, ao
     concluir, "a mudança é anunciada pelo próprio conteúdo assumindo o lugar, sem mensagem
     adicional de 'pronto', que seria ruído" (`:237-239`). Uma região viva com `aria-busy`
     comutado para falso anuncia **todo o conteúdo inserido**: o enunciado e as opções entram na
     fila de fala. O documento condena esse mesmo comportamento em §11.2 (`:690-692`, "lê-la em
     voz alta seria despejo de informação"). Critério violado: 4 (o que é anunciado tem de ser o
     que de fato será anunciado). Saída sugerida: região viva restrita a um texto de estado que
     é esvaziado ao concluir, com o conteúdo fora dela.
  3. **BLOQUEANTE — §2, princípio 5, contradiz CA-3 na leitura literal.** "Estado do exercício
     vive em memória de sessão e morre com ela — **inclusive na alternância de idioma** (§10.1)"
     (`:52-54`). §10.1 (`:577-580`) exige o oposto: opção selecionada, valor digitado, dicas
     reveladas, resultado e solução **sobrevivem** à troca de idioma (CA-3, RF-7). Quem
     implementar as tasks 5–8 lendo os princípios antes dos estados descarta o estado na troca —
     que é exatamente o que CA-3 testa. Critério violado: 1 e 3 (fidelidade à spec).
  4. **BLOQUEANTE — a decisão adiada (c) está fechada por omissão no desenho do índice.** §5
     enumera de forma exaustiva o que cada cartão mostra: "`title[lang]`, `summary[lang]`,
     `difficulty` e `estimatedMinutes`" (`:185-187`) — sem rótulo de rascunho e sem qualquer
     remissão a §12(c). Isso **é** C2 implementado, enquanto §12(c) (`:719-729`) apresenta C1,
     C2 e C3 como abertas. As decisões (a) e (b) passam: (a) detalhar E4 como A1 é obrigação de
     RF-5/CA-16 e do critério 6 do ticket, não escolha; (b) mantém as duas ramificações vivas em
     §10.1. Critério violado: instrução do ticket ("Desenhe as alternativas em vez de escolher
     sozinho") e handoff [003]. Correção: uma frase em §5 marcando o conteúdo do cartão como
     dependente de (c).
  5. **BLOQUEANTE (trivial) — `docs/design/` é diretório novo de primeiro nível em `docs/` e não
     está em nenhum índice.** `docs/README.md:6-15` lista todas as pastas de `docs/` e não lista
     `design/`; `AGENTS.md:147-154` idem. Convenção de estrutura do repositório (checklist 7 da
     revisão). Corrigir `docs/README.md` (uma linha); a entrada em `AGENTS.md` §4 fica como
     recomendação ao `tech-lead`, por ser fonte canônica.
- Sugestões (não bloqueiam):
  S1. §10.2 diz que a opção indisponível "fica marcada como tal na lista de idiomas" (`:607-608`)
      sem chave de texto correspondente — contradiz o princípio 2 do próprio documento (`:45-46`,
      "todo resultado, estado e rótulo tem texto próprio"). Ou criar a chave, ou declarar que a
      marcação é só estado acessível do controle.
  S2. §9 (`:547`): a célula en-US "`3.5` (e `3,5` não é imposto)" não diz se `3,5` é aceito ou
      rejeitado em en-US, onde `docs/content/i18n.md:20` faz da vírgula o separador de milhar —
      ambiguidade que a implementação vai resolver sozinha.
  S3. Tokens de interpolação divergem entre os idiomas da mesma chave: `{título}`/`{title}`
      (`:313`) e `{valor}`/`{value}` (`:431`), enquanto todas as demais usam `{n}` nos dois
      lados.
  S4. `network.offline-badge` é "Offline" nos dois idiomas (`:650`); com público infantil
      (`docs/content/accessibility.md:39`, "linguagem clara") vale considerar "Sem internet" em
      pt-BR — o texto de apoio já carrega a explicação, por isso não bloqueia.
  S5. §13: E1 rastreia só RNF-8 (`:735`), mas o comportamento exigido do estado (`aria-busy` /
      `role=status`) vem de RNF-6 e da tabela de estados; E2 aponta CA-13 (`:736`), cujo sujeito
      é a validação de contrato.
  S6. E11 — o veredito é a favor do produtor (aviso no idioma que permanece, por RF-7); sugiro
      apenas grafar o nome do idioma faltante na própria língua com `lang`, como §10 já faz em
      `language.option.*` (`:567-568`), para quem pediu inglês reconhecer o aviso.
- O que já está bom (não refazer):
  · **Critério 1 — cruzamento 1 a 1 completo.** Os 13 estados da tabela de `spec.md` têm seção
    própria, na mesma ordem e com o nome exato da spec (E1 §6.1 … E13 §11.2). Conferido por
    script, 13/13, zero divergências. A ausência do índice na tabela de estados da spec é
    **real** (verificada mecanicamente) — nenhum estado foi perdido e compensado pela tela de
    apoio de §5.
  · **Critério 2 — paridade sólida.** 69 chaves definidas, todas com as duas colunas preenchidas;
    nenhuma chave citada na prosa sem definição em tabela; amostra frase a frase em E2, E4, E5,
    E7, E11, E12 e E13 sem fallback nem mistura. As três células idênticas nos dois idiomas
    (`language.option.*`, `network.offline-badge`) são justificadas no texto.
  · **Critérios 5 e 9.** O Mermaid de §4 foi validado no parser real (mermaid@11 + jsdom, 1 bloco,
    OK) e traz "Leitura / Fontes / Marcação" conforme `docs/DOC-STANDARDS.md`.
    `bash scripts/audit-ai-surface.sh` → `Resultado: OK`; `bash scripts/audit-content.sh` →
    `1 nós · 0 erros · 0 avisos`. **Critério 9 fechado — não precisa ser reexecutado no loop 2.**
  · **Critério 7 — independência de stack confirmada por busca negativa.** `grep -nEi` de 25
    termos (react|vue|svelte|astro|next|vite|webpack|tailwind|indexeddb|localstorage|service
    worker|workbox|playwright|jest|vitest|npm|jsx|className|<div…) devolveu 2 ocorrências, ambas
    negando decisão (`:19`, `:170`). Só há HTML/ARIA/CSS de plataforma, que a própria spec usa.
  · **Critério 8 — nenhum estado com coleta.** Sem conta, login, e-mail, identificador ou envio
    de resposta; §11.2 (`:668-670`) deriva a lista de "o que está salvo" do inventário de cache,
    não de histórico nem de servidor.
  · **Fidelidade ao dado real.** Confirmei em `exercises.json`: 5 itens, **2 dicas em cada um**
    (o "duas em todos os itens" de `:485` é verdade), `qe-003` `answer: 3`/`tolerance: 0`,
    `qe-005` `3.5`/`0.001`, `unit` nulo em todos, itens `numeric` sem `options` (logo sem
    feedback por opção, como `:449-452` afirma). O catálogo de `tag.*`/`skill.*` (`:336-341`)
    cobre exatamente os 3 tags e 3 skills de `meta.json`, sem slug inventado.
  · **As cinco decisões de desenho julgadas — quatro aprovadas sem ressalva:** (1) cinco itens
    numa página sem paginador é **fidelidade**, não decisão de produto: nenhum RF pede
    sequenciamento, a tabela de estados não tem estado de navegação entre itens e RF-9 só exige a
    ordem do arquivo; (2) "responder desabilitado" focável que anuncia o motivo é correto em WCAG
    2.2 AA — nenhum SC exige removê-lo da ordem de foco e `docs/content/accessibility.md:31`
    ("erros de formulário anunciados e associados ao campo") empurra na direção escolhida;
    (3) E11 × E13 distintos é **exigido** por CA-11, que nomeia literalmente o estado "não
    disponível offline" para o caso do idioma nunca visitado — não é preferência do autor;
    (4) rótulo de rascunho só no idioma ativo é a única leitura de CA-16 compatível com RF-7
    ("idiomas nunca se misturam na mesma tela"); (5) aviso de idioma indisponível no idioma que
    permanece: **veredito a favor**, com a sugestão S6.
  · **Riscos declarados em §14 — nenhum é defeito deste ticket.** (1) Preservar o estado do
    exercício na troca de idioma depende da decisão (b): o desenho exige o comportamento e deixa
    o mecanismo à implementação, que é o recorte certo — mas ver o defeito 3, que é redação, não
    risco. (2) O catálogo de `tags[]`/`skills[]` na interface é dívida legítima: RNF-9 proíbe
    tocar em `content/` nesta fatia e RF-4 exige rótulo traduzido; está declarada em `:343-346` e
    repassada ao `tech-lead`. (3) A dupla leitura da matemática é intencional e RF-3 proíbe
    remover o parágrafo de leitura.
- Três decisões humanas seguem abertas e sobem ao `tech-lead` junto com o defeito 4: (a) exibir
  nó `draft`; (b) forma da URL bilíngue; (c) rótulo de rascunho no índice. **Confirmo a
  afirmação do produtor sobre A2:** esconder o nó `draft` do índice torna RF-1 e CA-1
  insatisfazíveis hoje — `scripts/audit-content.sh` conta **1 nó** no acervo e ele está `draft`,
  então o índice ficaria sem nenhum caminho navegável até conteúdo. Adotar A2 exige emenda na
  spec aprovada.
- Status novo: in_progress · owner: ui-ux-designer

## [007] ACTION — 2026-08-01 18:20 — ui-ux-designer
- Ação: correção dos 5 defeitos bloqueantes do `[006] REJECT` (loop 1/3), mais as 6 sugestões e
  a decisão de URL fechada pelo usuário no `TCK-0011`.
- **Defeito 1 — regra "mover foco OU anunciar" violada em 3 estados.** A regra saiu da tabela
  de riscos e virou seção normativa em §3 ("Regra de anúncio"), **antes** dos estados, com a
  exceção de navegação nomeada. Os três pontos citados foram reescritos:
  · E2 (§6.2): na carga inicial o foco vai ao bloco de erro e **não há região viva** — a região
    é uma linha de estado que nasce vazia; ela só anuncia quando a falha vem de
    `node.load-error.retry`, caso em que o foco fica parado no controle;
  · E5 via `retry` (§7.1, §7.3): o foco vai à área de resposta e `exercise.retry-notice`
    **viaja com o destino do foco** como descrição acessível da área de resposta, sendo lido ao
    receber o foco; a região de resultado é esvaziada em silêncio. O aviso continua existindo —
    muda o canal, não a informação;
  · E10 (§10.1): com a decisão do usuário, alternar idioma é navegar; não há região viva e a
    chave `language.switched` foi **descartada** do catálogo.
  A varredura foi feita nos 13 estados, não só nos três citados (`L-013`): E3, E13-por-navegação
  e E10 são navegação e estão declarados como tal; E1, E6, E7, E8, E11, E12 e E13-parcial mantêm
  o foco parado e anunciam; E9 move o foco e não anuncia. Tabela de regiões vivas de §3
  atualizada com a linha de E2.
- **Defeito 2 — E1 contraditório.** O escopo da região viva deixou de ser a seção: passa a ser
  uma **linha de estado**, fora do lugar onde o conteúdo é inserido e esvaziada ao concluir
  (§3 e §6.1). Nada é falado no fim — nem "pronto", nem os enunciados. A marca de "ocupado"
  continua na seção; o que é falado é só a linha. Mesmo padrão aplicado a E2.
- **Defeito 3 — §2, princípio 5.** Reescrito: o estado morre **com a sessão**, e dentro da
  sessão **sobrevive à alternância de idioma** (CA-3, RF-7), com a frase explícita "morrer com a
  sessão nunca autoriza descartar o estado numa troca de idioma".
- **Defeito 4 — decisão (c) fechada por omissão.** §5 agora marca a lista do cartão como "o
  mínimo de RF-1, não o cartão fechado", com remissão a §12(c) e o efeito de C1, C2 e C3 sobre
  o cartão; §12(c) ganhou a contrapartida ("a ausência do rótulo em §5 **não** é escolha de
  C2"). As três alternativas seguem vivas e sem texto novo.
- **Defeito 5 — índice de `docs/`.** `docs/README.md` ganhou a linha de `design/`. **`AGENTS.md`
  §4 não foi tocado**, conforme a própria recomendação do revisor: é fonte canônica, a edição
  pede `python3 scripts/sync-ai-adapters.py` e esta sessão não tem shell para rodar o `--check`
  — fica como pendência declarada ao `tech-lead`, com o texto sugerido
  `docs/design/ # Desenho de UI/UX por spec: estados de tela, fluxos, textos de interface`.
- **Decisão do usuário aplicada (b, `TCK-0011`):** prefixo de idioma minúsculo no caminho
  (`/pt-br/high-school/algebra/quadratic-equations`, e `/en-us/…` pela mesma regra). §12(b)
  deixou de ser tabela de alternativas e virou registro de decisão; §10.1 abre com a decisão;
  §11.2 passou a tratar "idioma não cacheado" como navegação respondida pela camada offline; o
  risco 1 de §14 foi reescrito para o mundo em que alternar é navegar. O identificador do
  idioma no dado continua `pt-BR`/`en-US` — minúsculo é grafia **da URL**.
- **Sugestões aplicadas:** S1 (a opção de idioma indisponível é **estado acessível do
  controle**, sem string nova — declarado em §10.2); S2 (§9: em en-US `3,5` é **recusado** com
  `exercise.invalid-number`, nunca lido como `35`; a divergência entre as duas frases do par
  está declarada); S3 (tokens unificados em `{title}` e `{value}`, com a regra "token traduzido
  é chave quebrada" em §1); S4 (`network.offline-badge` = "Sem internet" em pt-BR, "Offline" em
  en-US, com o motivo na coluna de origem); S5 (§13: E1 e E2 rastreiam a tabela de estados e
  RNF-6, e CA-13 aparece qualificado); S6 (`language.unavailable` cita o idioma faltante também
  na própria língua, entre parênteses e marcado com o idioma, como `language.option.*`).
- **Não refiz** o que o `[006]` aprovou: os 13 estados, a paridade das chaves, o Mermaid, as
  cinco decisões de desenho e o critério 9 (fechado no loop 1, auditorias não reexecutadas).
- Evidência das auditorias: **critério 9 já fechado em `[006]`** (`audit-ai-surface.sh` OK,
  `audit-content.sh` 1 nó · 0 erros · 0 avisos). Esta sessão continua **sem shell**; o diff toca
  `docs/design/**`, `docs/README.md`, `memory/**` e o ticket — nada em `content/`, nas fontes
  canônicas da superfície de IA ou nos adapters gerados, então nenhuma das duas auditorias muda
  de resultado. Se o revisor preferir, reexecutar é barato.
- Resultado: ok — 5 defeitos resolvidos, 6 sugestões aplicadas, decisão (b) incorporada.
- Lição: L-022 (`memory/lessons/writing-a-rule-is-not-applying-it.md`) — regra escrita em seção
  terminal não governa o corpo do documento; ela nasce na seção estrutural, nomeia as exceções e
  só está aplicada depois da varredura item a item. Indexada em `memory/LESSONS.md` (Erro) e em
  `memory/MEMORY.md`.

## [008] HANDOFF — 2026-08-01 18:20
- De: ui-ux-designer → Para: code-reviewer
- Status novo: in_review
- O que foi feito: correção dos 5 bloqueantes do `[006]`, aplicação das 6 sugestões e da decisão
  de URL do `TCK-0011`; lição L-022 registrada.
- Artefatos: `docs/design/minimum-learning-slice/screen-states.md`,
  `docs/design/minimum-learning-slice/README.md`, `docs/README.md`,
  `memory/lessons/writing-a-rule-is-not-applying-it.md`, `memory/LESSONS.md`,
  `memory/MEMORY.md`, `memory/agents/ui-ux-designer.md`.
- Como validar (o que mudou desde o `[006]`):
  · defeito 1 → §3 "Regra de anúncio" + §6.2, §7.1, §7.3, §10.1; conferir que nenhum estado
    move foco e anuncia no mesmo evento, e que os eventos de navegação estão nomeados;
  · defeito 2 → §3 (coluna "Escopo") e §6.1; conferir que nenhuma região viva envolve conteúdo;
  · defeito 3 → §2, princípio 5, contra §10.1 e CA-3;
  · defeito 4 → §5 (bloco de citação) e §12(c);
  · defeito 5 → `docs/README.md`; `AGENTS.md` intocado de propósito (pendência ao `tech-lead`);
  · decisão (b) → §10.1, §11.2, §12(b), §14 risco 1; `language.switched` não existe mais.
- Pendências e riscos: §14 do documento (agora com dois riscos de região viva/foco);
  `AGENTS.md` §4 sem a linha de `docs/design/` — decisão e execução do `tech-lead`, por exigir
  `sync-ai-adapters.py`.
- **Para o `tech-lead` — duas decisões humanas continuam abertas** (§12): (a) exibir o nó
  `status: "draft"` — A1 × A2 × A3, com A2 tornando RF-1/CA-1 insatisfazíveis hoje; (c) rótulo
  de rascunho no índice — C1 × C2 × C3, sem texto novo em nenhuma. A decisão (b) está fechada e
  aplicada.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 ·
  [x] 9 (fechado em `[006]`).

## [009] HANDOFF — 2026-08-01 18:55
- De: code-reviewer#5 → Para: qa-validator
- Status novo: in_validation
- O que foi feito: revisão do loop 2/3. Os 5 bloqueantes do `[006]` foram verificados um a um
  **contra o artefato**, não contra o `[007]`; as 6 sugestões foram conferidas aplicadas; a
  decisão (b) do usuário foi rastreada até a fonte. **Nenhum bloqueante novo.** APROVADO.
- Artefatos revisados: `docs/design/minimum-learning-slice/screen-states.md` (849 linhas),
  `README.md` do mesmo diretório, `docs/README.md`,
  `memory/lessons/writing-a-rule-is-not-applying-it.md`, `memory/LESSONS.md`, `memory/MEMORY.md`.
- **Verificação do defeito 1 (regra "mover foco OU anunciar") — varredura própria dos 13, não
  dos 3 citados.** A regra saiu da tabela de riscos e virou seção normativa em §3 (`:100-116`),
  antes dos estados, com a exceção de navegação nomeada. Varri os treze e classifiquei cada um:
  · **movem foco, sem região viva (3):** E2 na carga inicial (`:311-315`, `:322-324`), E5 via
    `exercise.retry` (`:468-480`, e §7.3 `:539-541`), E9 (`:587-593`);
  · **foco parado, anunciam (8 eventos):** E1 na entrada (`:277`, `:282`), E5 com `submit`
    bloqueado (`:455-456`), E6 (`:500-507`), E7 na entrada (`:536-541`), E8 (`:562-568`),
    E11 (`:703-708`), E12 (`:731-736`), E13 parcial (`:767-773`);
  · **navegação, sem região viva (3):** E3 (`:345-350`), E10 (`:665-674`), E13 por navegação
    (`:765-767`);
  · **sem evento:** E4 (`:406-409`).
  Nenhum estado faz os dois, e nenhum evento ficou sem nenhum dos dois. A troca de canal em E5 é
  tecnicamente sólida: `exercise.retry-notice` como descrição acessível é lido no foco, e o
  desenho ainda remove a descrição depois da nova submissão (`:479-480`) para não repetir o
  aviso em toda visita ao campo. **Defeito 1 resolvido.**
- **Verificação do defeito 2 (escopo da região viva).** §3 `:123-134` fixa o escopo de cada
  região como linha de estado; E1 (`:267-271`, `:282-287`) e E2 (`:322-327`) põem a linha
  **fora** do lugar onde o conteúdo entra e a esvaziam ao concluir. Confirmo que esvaziar não
  fala: o `aria-relevant` padrão é `additions text`, remoção não é anunciada — logo "nada é
  falado no fim" se sustenta, nem "pronto" nem os enunciados. Não contradiz §11.2 (`:771-773`);
  ao contrário, agora usa o mesmo argumento. **Defeito 2 resolvido** (ver S7).
- **Verificação do defeito 3.** §2, princípio 5 (`:57-63`) agora diz que o estado morre com a
  **sessão** e sobrevive à troca de idioma dentro dela, com a frase que fecha a leitura errada.
  Bate com §10.1 (`:655-659`), com CA-3 e com RF-7. **Resolvido.**
- **Verificação do defeito 4 — julgamento pedido: sim, reabre.** §5 `:224-228` não é ressalva
  textual: declara o efeito **de cada uma das três** alternativas sobre o cartão ("em C1 o
  cartão ganha `node.draft-badge`; em C3 o aviso fica no topo, fora do cartão; em C2 fica como
  enumerado"), de modo que o índice não pode ser implementado sem consultar (c); §12(c)
  `:811-815` traz a contrapartida. A enumeração continua igual à de C2 **por ser o mínimo de
  RF-1**, e isso agora está dito. **Resolvido** (ver S8, sobre o rótulo do Mermaid).
- **Verificação do defeito 5.** `docs/README.md:13` ganhou a linha de `design/` (`git diff`:
  1 inserção, nada mais). `AGENTS.md` §4 segue sem a entrada, como eu mesmo recomendei em
  `[006]` — **defeito fechado**, pendência declarada ao `tech-lead`. **Correção de registro:** a
  justificativa do `[007]` ("a edição pede `sync-ai-adapters.py`") é factualmente errada —
  as fontes do gerador são `.github/instructions/` (`scripts/sync-ai-adapters.py:49`),
  `.claude/agents/` e `.claude/skills/`; `AGENTS.md` nunca é lido como entrada. O motivo válido
  é de escopo (fonte canônica de instrução é do `tech-lead`), não de ferramenta. Registro isto
  para que o `tech-lead` não herde uma restrição inexistente.
- **Decisão (b) rastreada até a fonte, não aceita do log.** O usuário decidiu de fato:
  `tickets/TCK-0011-container-architecture-and-cicd/log.md:206-207` — "URL `/pt-br/` minúsculo
  (**a sua proposta, confirmada**)". `ADR-0007:184` confirma a distinção aplicada aqui: URL em
  minúsculas, **dado e documento continuam `pt-BR`/`en-US`**. Conferi a consistência no
  documento: `pt-br`/`en-us` aparece em **4 lugares, todos exemplos de URL em prosa**
  (`screen-states.md:647`, `:648`, `:793`, `README.md:16`); **nenhuma chave de dado, campo
  localizado ou coluna de tabela usa minúsculas** — `language.option.pt-BR` e as 68 chaves
  seguem na grafia canônica. `language.switched` não existe mais em nenhuma tabela; as duas
  ocorrências restantes (`:673`, `:798`) declaram o descarte. **Consistente.** Ver S9.
- **S2, simetria (pergunta explícita).** Respondo: **não quebra RNF-1** — RNF-1 governa
  paridade de *texto*, não tolerância de *entrada* — e não quebra CA-7, que só exige `3,5` em
  pt-BR e `3.5` em en-US. A divergência das duas frases está declarada (`:462-466`, `:615`).
  Mas o **argumento** é assimétrico, e isso vira sugestão (S10): §9 `:622-625` recusa `3,5` em
  en-US porque lá a vírgula é separador de milhar — e `docs/content/i18n.md:20` faz do **ponto**
  o separador de milhar em **pt-BR**, então `3.500` digitado em pt-BR com o sentido "três mil e
  quinhentos" é lido como `3,5` e, em `qe-005` (`answer: 3.5`), seria marcado **correto**. É o
  espelho exato do risco que motivou a recusa em en-US.
- **L-022.** Formato completo (`Tipo: erro` · `ID: L-022` · Contexto com data absoluta e ticket
  · Lição · Como aplicar), nome en-US kebab-case, sem colisão de ID (`grep '^\*\*ID:\*\*'`),
  indexada em `memory/LESSONS.md:76` **dentro da seção "## Erro"** (linhas 37–81, coerente com o
  `Tipo:`) e em `memory/MEMORY.md:90`. **Não duplica L-013/L-018/L-021:** o "Como aplicar"
  instrui duas ações que nenhuma delas instrui — *onde* a norma nasce (seção estrutural, não
  riscos/notas) e *nomear as exceções dentro da própria regra*. A sobreposição com L-013 é só no
  "varrer item a item", e o gatilho difere (escrever uma norma × corrigir um `REJECT`). Ver S11.
- **Reverificado do loop 1 (o que a correção podia quebrar):** cruzamento dos 13 estados por
  script — **13/13, mesma ordem e nome da spec**; catálogo bilíngue — **68 chaves** (era 69;
  `language.switched` removida), **zero células vazias**, **zero chaves citadas sem definição**,
  **zero tokens de interpolação divergentes** (S3 aplicada e medida); Mermaid revalidado no
  parser (mermaid@11 + jsdom, 1 bloco, OK); as 6 sugestões conferidas aplicadas uma a uma
  (S1 `:683-686` · S2 `:615`,`:622-625` · S3 `:41-44` · S4 `:727` · S5 `:821-822` · S6 `:692`,
  `:695-701`).
- **Critério 9 — reexecutado mesmo estando fechado, e escopo do diff confirmado.**
  `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (inclui `sync-ai-adapters.py --check`
  = `up-to-date`); `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`. O working
  tree tem hoje 42 arquivos modificados de tickets paralelos: conferi que **nenhuma linha das
  fontes canônicas pertence a este ticket** (`git diff -- AGENTS.md .github/instructions/
  .claude/ | grep -i 'design|screen-state|TCK-0013'` → vazio); as 10 inserções em `AGENTS.md`
  são de ticket paralelo. Escopo do `TCK-0013` confirmado: `docs/design/**`, `docs/README.md`
  (1 linha), `memory/**` e o próprio ticket.
- Sugestões (não bloqueiam; o `qa-validator` decide o que vira dívida registrada):
  S7. §3 `:123` afirma "Nenhuma região viva envolve conteúdo", mas a própria tabela põe dentro
      de duas regiões texto que é conteúdo: "Lista de dicas reveladas" (`:131`, o texto de
      `hints[]`) e "Bloco de resultado (status + feedback)" (`:132`, o `feedback[lang]` que
      §7.2 `:505-506` **exige** anunciar). A coluna *Escopo* resolve quatro linhas depois;
      ainda assim, a frase absoluta ganharia em dizer "nenhuma região viva envolve a seção, o
      enunciado, as opções ou a solução".
  S8. O nó `I3` do Mermaid (`:146`) ainda enumera "cartão: título · resumo · dificuldade ·
      tempo" sem remissão a (c) — mesma classe de L-011/L-013 (diagrama sobrevivendo à correção
      da prosa). Não contradiz §5, por ser o mínimo de RF-1, por isso não bloqueia.
  S9. §10.1 `:646` e §12(b) `:790` dizem "DECIDIDA (usuário, `TCK-0011`)" sem citar o
      `ADR-0007`, que é o registro da decisão e está **`proposed`**, com "aceite pendente"
      (`ADR-0007:3-5`) e `/pt-BR/` ainda listado como alternativa documentada (`:198`);
      `docs/architecture/c4-container.md:41` marca a mesma URL como "PROPOSTO (ADR-0007)".
      A decisão do usuário vale — mas o desenho deveria apontar o registro e o status.
  S10. Assimetria de tolerância numérica descrita acima (§9 `:615`, `:622-625` ×
      `docs/content/i18n.md:20`): aplicar o teste de ambiguidade nos dois idiomas, ou declarar
      por que a assimetria é intencional.
  S11. L-022 não referencia L-013 nem L-021, da mesma família; o índice já faz isso em L-019
      ("ver L-013 e L-018"). Uma linha resolve.
  S12. E1 ficou **silencioso na conclusão** por desenho (`:282-287`) — decisão legítima e bem
      argumentada, mas é o único ponto em que quem ouviu "carregando" não recebe sinal de fim.
      Vale confirmar com leitor de tela real no `/a11y-audit`; se atrapalhar, uma linha de
      estado curta ("Exercícios prontos") na mesma região resolve sem despejo.
- Pendências e riscos: §14 do documento (7 riscos, dois novos sobre foco × região viva);
  `AGENTS.md` §4 sem a linha de `docs/design/` — do `tech-lead`, e **sem** a restrição de sync
  que o `[007]` supôs.
- **Para o `tech-lead` — duas decisões humanas continuam abertas** e nenhuma foi fechada por
  omissão (verifiquei): **(a)** exibir o nó `status: "draft"` — A1 × A2 × A3, com A2 tornando
  RF-1/CA-1 insatisfazíveis hoje (acervo com 1 nó, `draft`) e exigindo emenda na spec;
  **(c)** rótulo de rascunho no índice — C1 × C2 × C3, nenhuma exigindo texto novo. Some-se a
  pendência do `AGENTS.md` §4 e a de S9 (status do `ADR-0007`).
- Como validar: critérios 1–9 do `ticket.md`; roteiro de teclado e leitor de tela contra §3
  (regra de anúncio) e contra cada parágrafo **Foco** / **Região viva**; conferir E11 × E13 com
  idioma nunca visitado e offline (CA-11); conferir que `pt-br` só aparece em URL.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9.

## [010] REJECT — 2026-08-01 20:10
- De: qa-validator#7 → Para: ui-ux-designer · Loop nº: 2/3
- **Ambiente da validação:** commit `5d1e2b6`, working tree com 42 arquivos de tickets
  paralelos; artefatos deste ticket ainda não commitados (`docs/design/` = `??`,
  `docs/README.md` = `M`, 1 inserção). Node v24.14.1; `mermaid@11` + `jsdom` instalados no
  scratchpad. Validação **documental** — não há aplicação: `ls src/ app/ package.json` não
  existe, então a bateria de casos hostis de UI (offline real, zoom 200%, tema, leitor de tela)
  **não é executável aqui** e vira roteiro de `/a11y-audit` e `/pwa-audit` nas tasks 5–8. O que
  eu executei foi cruzamento mecânico, parser real do Mermaid, **simulação da regra numérica
  contra os dados reais** e as duas auditorias.
- Evidência reproduzida por mim, critério a critério (não herdada do `[006]`/`[009]`):
  1. Script Python cruzando as 13 linhas da tabela de estados de `spec.md` com os cabeçalhos
     `### N.N · … (EN)` do desenho → **13/13**, mesma ordem, mesmo par contexto·estado. ✓
  2. **68 chaves** em 18 tabelas; **0 células vazias**, **0 chaves duplicadas**, **0 tokens de
     interpolação divergentes**, **0 chaves citadas na prosa sem definição** — a única citada
     sem tabela é `language.switched`, e só nas duas frases que declaram o descarte. Amostra
     semântica frase a frase em **7 estados** (E2, E4, E5, E7, E11, E12, E13). As duas células
     idênticas (`language.option.*`) e as três divergências deliberadas
     (`exercise.invalid-number`, `language.unavailable`, `network.offline-badge`) estão
     declaradas na própria linha ou no parágrafo seguinte. ✓ **com o defeito 1** (o *conteúdo*
     de uma delas).
  3. **13/13** seções com parágrafo **Foco**, cada uma nomeando o elemento que recebe foco ao
     entrar; ordem base em §3 (8 passos) e deltas por estado (§5, §6.2, §6.3, §7 itens 1–7). ✓
  4. **13/13** com parágrafo **Região viva**; os quatro estados que o critério nomeia declaram o
     texto anunciado — E6 (`:505-507`), E7 (`:539-541`), E8 (`:566-568`), E12 (`:734-736`).
     Classifiquei eu mesmo os 13 pela regra de §3: 3 eventos movem foco sem região viva (E2
     inicial, E5 via `retry`, E9), 3 são navegação sem região viva (E3, E10, E13 por navegação),
     8 eventos mantêm foco e anunciam, E4 não tem evento. **Nenhum faz os dois; nenhum fica sem
     os dois.** ✓
  5. **1 bloco Mermaid**, `mermaid.parse` (mermaid@11 + jsdom) → **OK**, 54 linhas. Extraí 16 nós
     e 28 arestas: 12 dos 13 estados são nó próprio com ≥1 entrada e ≥1 saída; E4 vive dentro de
     `N1`, coerente com §6.4 ("rótulo permanente, não evento"). "Leitura / Fontes / Marcação"
     presentes (`docs/DOC-STANDARDS.md`). ✓ **com o defeito 2** (rótulo de `I3`).
  6. Rascunho: `node.draft-badge`/`node.draft-note`/`node.draft-title-prefix` (§6.4). Alternador:
     `language.label` + `language.option.*` (§10). Rede: E12 com 3 chaves (§11.1) e E13 com 4
     (§11.2). ✓
  7. `grep -nEi` de ~30 termos de stack (react|vue|svelte|astro|next|vite|webpack|tailwind|
     indexeddb|localstorage|workbox|playwright|jest|vitest|npm|jsx|tsx|className|<div|…) nos dois
     arquivos → **2 ocorrências, ambas em frase de negação** (`screen-states.md:18`,
     `README.md:10`). ✓
  8. `grep -nEi` de 15 termos de coleta (login|conta|e-mail|analytics|telemetr|cookie|fingerprint|
     identificador|servidor|rastre|…) → toda ocorrência é (a) negação, (b) o identificador de
     **idioma** `pt-BR`/`en-US`, ou (c) o inventário de cache local, declarado em `:746` como não
     sendo histórico, identificador nem servidor. ✓
  9. `bash scripts/audit-ai-surface.sh > arq 2>&1; echo $?` → **exit 0**, `Resultado: OK`
     (inclui `sync-ai-adapters.py --check` = `up-to-date`); `bash scripts/audit-content.sh` →
     **exit 0**, `1 nós · 0 erros · 0 avisos`. Exit codes capturados sem pipe. ✓
  Extra (não é critério): RF-1…RF-18 e CA-1…CA-16 **todos** citados no desenho; só RNF-4 e
  RNF-11 não aparecem — custo zero e gabarito no payload não são estado de tela, sem impacto.

### Defeitos (numerados)

1. **BLOQUEANTE — §9 aplica o teste de ambiguidade a um idioma só, e o lado sem guarda marca
   resposta errada como CERTA.** §9 (`:615`) fixa: pt-BR aceita `3,5` **e** `3.5`; en-US aceita
   só `3.5` e **recusa** `3,5` "porque seria ambíguo entre `3.5` e `35`" (`:622-625`). Mas
   `docs/content/i18n.md:20` — a mesma fonte que a linha de cima de §9 (`:616`) invoca como
   autoridade — faz do **ponto** o separador de milhar em pt-BR (`1.000`). Implementei
   literalmente as duas regras de §9 e rodei contra os dois itens `numeric` reais do nó piloto
   (`qe-003`: `answer: 3`, `tolerance: 0`; `qe-005`: `answer: 3.5`, `tolerance: 0.001`):

   | item | digitado | o aluno quis dizer | pt-BR (§9 literal) | en-US (§9 literal) |
   |---|---|---|---|---|
   | `qe-005` | `3,5` | 3,5 | 3.5 → **correto** (CA-7 ✓) | recusado com `exercise.invalid-number` |
   | `qe-005` | `3.5` | 3.5 | 3.5 → **correto** | 3.5 → **correto** (CA-7 ✓) |
   | `qe-005` | `3.500` | **3500** (agrupamento pt-BR válido) | 3.5 → **CORRETO ← falso positivo** | 3.5 → correto (grafia não en-US) |
   | `qe-003` | `3.000` | **3000** (agrupamento pt-BR válido) | 3.0 → **CORRETO ← falso positivo** | 3.0 → correto |
   | `qe-003` | `3,000` | 3000 (agrupamento en-US válido) | 3.0 (é 3 em pt-BR, ok) | **recusado** — guarda existe |

   Leitura: **o idioma cujo separador de milhar é a vírgula ganhou guarda escrita; o idioma cujo
   separador de milhar é o ponto ficou sem nenhuma** — e é justamente o lado sem guarda que erra
   no sentido pior. O próprio §9 justifica a recusa em en-US com "adivinhar aqui poderia marcar
   como **errada uma resposta certa**" (`:625`); em pt-BR o resíduo não guardado marca **certa
   uma resposta errada**, nos **2 de 2** itens numéricos do acervo real. Numa plataforma de
   aprendizado esse é o pior modo de falha, e o desenho é onde ele nasce: §9 se chama
   "Convenções numéricas por idioma" e é o contrato que a task 7 (player de exercícios) vai
   implementar — não há outro lugar onde essa decisão exista.
   **Agravante de reincidência (rule 7 do AGENTS.md):** é literalmente `L-021`
   (`a-norm-that-names-the-strict-case-leaves-the-frequent-case-unruled.md`) — "ao estreitar uma
   norma para torná-la verificável, o caso deixado de fora **não fica neutro: fica permitido**",
   com "rode o teste contra o conteúdo existente antes de publicar a norma" no *Como aplicar*.
   E é `L-013` no procedimento: o `[007]` corrigiu o caso **citado** por S2 (en-US) e não varreu
   a **classe** (o idioma espelho) — a mesma lição que o próprio `[007]` declara ter aplicado ao
   defeito 1 do `[006]`.
   Critério violado: **2** (a string de interface `exercise.invalid-number` em pt-BR — "Digite
   apenas um número — por exemplo, 3,5 ou 3.5.", `:462` — afirma ao aluno brasileiro uma
   convenção de entrada que a spec não prevê: RF-12 só exige que `3,5` seja aceito em pt-BR; e
   ela contradiz `exercise.decimal-hint` pt-BR, `:441`, "Use vírgula para decimais", e
   `docs/content/i18n.md:19-20`) e **1** (fidelidade a RF-11/RF-12: a correção é
   `|resposta − answer| ≤ tolerance` **sobre o número que o aluno escreveu**, não sobre o número
   que uma leitura de outro idioma produz).
   **Condição de aceite da correção — não estou desenhando a saída:** (i) o teste de ambiguidade
   aparece nos **dois** idiomas de §9, com gatilho **inspecionável na própria string** (formato:
   separador seguido de exatamente 3 dígitos, mais de um separador, etc.), nunca "o que o aluno
   quis dizer" (`L-021`, item 3 do *Como aplicar*) — **ou** a assimetria fica declarada com o
   argumento de por que é segura em pt-BR; (ii) a linha `exercise.invalid-number` em pt-BR deixa
   de ensinar `3.5` como número bem formado, ou o desenho explica por que ensina; (iii) a
   varredura é da **dimensão** (toda regra de §9 e toda string que cite formato numérico), não
   das linhas que eu citei — `L-013`, adendo.

2. **BLOQUEANTE (segundo grau, uma linha) — a decisão (c) continua fechada por omissão no
   Mermaid, que é parte normativa.** O `[006]` bloqueou (defeito 4) exatamente a enumeração
   exaustiva do cartão do índice sem remissão a (c). O `[007]` corrigiu a **prosa** de §5
   (`:224-228`, bloco de citação com o efeito de C1/C2/C3) e deixou o nó `I3` do diagrama
   (`:146`) com a **mesma** enumeração — "cartão: título · resumo · dificuldade · tempo" — sem
   remissão. Por `docs/DOC-STANDARDS.md` o Mermaid é normativo, e ele vem em §4, **antes** de §5:
   quem implementar a task 5 lendo o fluxo recebe o cartão de C2 como fechado. É a mesma classe
   de `L-013` ("o rótulo do nó do Mermaid continuou dizendo…"), no mesmo documento, no mesmo
   loop. **Sozinho, eu teria registrado isto como dívida** — o registro é honesto: só bloqueia
   porque a entrega volta de qualquer forma pelo defeito 1, e a correção é uma linha (`I3`
   remetendo a §12(c), ou a enumeração saindo do rótulo). Critério violado: instrução do ticket
   ("Desenhe as alternativas em vez de escolher sozinho") e handoff `[003]`.

### O que já está bom (não refazer)

- **Critérios 1, 3, 4, 6, 7, 8 e 9: fechados com evidência minha**, nos termos acima. O
  cruzamento 13/13, a classificação foco × região viva dos treze, as duas buscas negativas e as
  duas auditorias foram **reexecutados**, não herdados — e todos batem com o `[009]`.
- **Critério 2 está sólido na mecânica** (68 chaves, zero buraco, zero token divergente,
  paridade semântica conferida em 7 estados). O defeito 1 é o **conteúdo** de uma linha, não a
  estrutura do catálogo: não refazer o catálogo.
- **Critério 5:** o diagrama passa no parser real e tem entrada e saída para todo estado. O
  defeito 2 é um rótulo, não o fluxo.
- **As cinco correções do `[007]` foram verificadas contra o artefato e resistem:** a regra de
  anúncio em §3 governa os 13 (varredura minha, não a do produtor); o escopo das regiões vivas é
  linha de estado em todas as 6 linhas da tabela de §3; o princípio 5 (`:57-63`) agora bate com
  §10.1 e CA-3; `docs/README.md:13` tem a linha de `design/` (diff = 1 inserção, nada mais).
- **Decisões (a) e (c) seguem abertas — reverificado, era o defeito 4 do `[006]`.** (a): §12(a)
  lista A1/A2/A3 com custo, §6.4 desenha A1 **porque RF-5/CA-16 obrigam o rótulo**, e nada no
  documento esconde o nó nem impõe confirmação; (c): §5 remete a §12(c), §12(c) traz a
  contrapartida explícita ("a ausência do rótulo em §5 **não** é escolha de C2") e nenhuma das
  três alternativas exige texto novo. **Ressalva:** o Mermaid não acompanhou (defeito 2).
- **Correção de registro do `[009]` sobre o `AGENTS.md`: confirmada por mim e correta.**
  `scripts/sync-ai-adapters.py:46-49` lê `.claude/skills/`, `.claude/agents/` e
  `.github/instructions/`; `AGENTS.md` **não** é entrada do gerador. Logo a justificativa do
  `[007]` era factualmente errada e o motivo válido para não tocá-lo é **escopo** (fonte
  canônica é do `tech-lead`). O registro final do log está correto e o `tech-lead` não herda
  restrição inexistente. `AGENTS.md:147-154` segue sem a linha de `docs/design/`.

### Dívidas registradas (não bloqueiam; entram no `Resultado final` quando o ticket fechar)

- **D-1 (S7)** — §3 `:123` afirma "Nenhuma região viva envolve conteúdo", mas a tabela logo
  abaixo põe `hints[]` (`:131`) e `feedback[lang]` (`:132`) dentro de duas regiões, e §7.2/§7.4
  **exigem** anunciá-los. A frase absoluta erra por **sobre**afirmar uma proibição; o comando
  operativo está certo nas seções específicas. Dívida com gatilho: se a task 7 anunciar só o
  status e engolir o feedback diagnóstico, esta frase é a causa.
- **D-2 (S9)** — §10.1 `:646` e §12(b) `:790` dizem "DECIDIDA (usuário, `TCK-0011`)" sem citar o
  `ADR-0007`, que está **`proposed`, com "aceite pendente"** (conferido: `ADR-0007:3-5`). A
  decisão do usuário vale; o registro dela não está aceito. Gatilho: se o `ADR-0007` for aceito
  com outra forma de URL, §10.1, §11.2, §12(b) e o risco 1 de §14 caem juntos.
- **D-3 (S12)** — E1 é o único ponto em que quem ouviu "carregando" não recebe sinal de fim
  (`:282-287`). Decisão legítima e bem argumentada, **não verificável sem leitor de tela real**.
  Condiciona o fechamento da task 5: confirmar em `/a11y-audit`.
- **D-4 (S11)** — `L-022` não referencia `L-013` nem `L-021`, da mesma família. Vira uma linha
  na correção do defeito 1, que precisa citar `L-021` de qualquer jeito.
- **S4, S6 e o catálogo de `tag.*`/`skill.*`** ficam como estão: aplicados e/ou já declarados
  como dívida em `:401-404`, com o ticket de conteúdo/schema pedido ao `tech-lead`.

### Pendências que sobem ao `tech-lead` (nenhuma bloqueia o loop)

- **(a)** exibir o nó `status: "draft"` — A1 × A2 × A3; A2 torna RF-1/CA-1 insatisfazíveis hoje
  (acervo com 1 nó, `draft` — confirmei: `audit-content.sh` = 1 nó) e exigiria emenda na spec.
- **(c)** rótulo de rascunho no índice — C1 × C2 × C3, nenhuma exigindo texto novo.
- `AGENTS.md` §4 sem a linha de `docs/design/` — **sem** a restrição de `sync-ai-adapters.py`.
- `ADR-0007` `proposed` sustentando a decisão (b) já aplicada no desenho (D-2).

### Como validar a correção (o que eu vou reexecutar no loop 3)

Simulação da regra de §9 nos dois idiomas contra `qe-003` e `qe-005`, com as entradas
`3`, `3,5`, `3.5`, `3.000`, `3.500`, `3,000`, `3,500` — nenhuma pode marcar **correto** um valor
que o aluno não quis dizer no idioma ativo; leitura das três strings que citam formato numérico
(`exercise.decimal-hint`, `exercise.invalid-number`, §9) procurando contradição entre si e com
`docs/content/i18n.md:19-20`; `grep` por "cartão" e por "(c)" atrás de enumeração do índice sem
remissão, prosa **e** rótulo de diagrama; e a bateria dos critérios 1–9 de novo, inclusive as
duas auditorias.

- Status novo: in_progress · owner: ui-ux-designer

## [011] ACTION — 2026-08-01 21:05 — ui-ux-designer
- Ação: correção dos 2 defeitos do `[010] REJECT` (loop 2/3) **pela classe**, mais três das
  quatro dívidas registradas. Aceito o achado do defeito 1 sem ressalva: a simulação do QA
  contra `qe-003` e `qe-005` está certa, e o modo de falha que eu deixei aberto é o pior
  possível numa plataforma de aprendizado — o aluno errar e a tela dizer que acertou.
- **Defeito 1 — assimetria decimal. §9 foi reescrita como pergunta respondida nos dois idiomas**
  (não como remendo do lado que faltava). A seção abre declarando o que precisa responder para
  **cada** idioma: qual caractere é decimal, qual é de milhar, e o que acontece com cada um na
  entrada. A tabela passou a ter uma linha por pergunta e uma coluna por idioma — 11 linhas,
  nenhuma resposta omitida de um dos lados.
  · **Regra única, simétrica:** aceita-se dígitos, um `-` inicial opcional e **no máximo um**
    separador, que tem de ser o **decimal do idioma ativo**. Qualquer outro caractere de
    separação — o ponto em pt-BR, a vírgula em en-US, espaço, apóstrofo — recusa a entrada com
    `exercise.invalid-number`. O gatilho é inspecionável na string digitada (**qual caractere
    apareceu e quantas vezes**), nunca a intenção presumida — condição (i) do `[010]`.
  · **Nada é convertido nem descartado em silêncio:** separador de milhar não é removido para
    "salvar" a entrada, e o separador do outro idioma não vira decimal. A evidência dos falsos
    positivos (`3.000` → correto em `qe-003`; `3.500` → correto em `qe-005`) ficou **dentro** de
    §9, com o argumento de por que recusar formato é preferível a aceitar erro.
  · **Alternativa descartada, declarada:** a heurística "separador seguido de exatamente três
    dígitos" — reduz recusas mas mantém a adivinhação (`3.500` continua ambíguo) e troca uma
    regra que o aluno consegue enunciar ("use vírgula") por uma que ninguém enuncia.
  · **Condição (ii):** `exercise.invalid-number` em pt-BR **deixou de ensinar `3.5`**. As duas
    frases dizem a mesma regra, cada uma com o separador do seu idioma: "Digite o número com
    vírgula para decimais e sem separador de milhar — por exemplo, 3,5." / "Enter the number
    with a period for decimals and no thousands separator — for example, 3.5." Some a
    contradição com `exercise.decimal-hint` e com `docs/content/i18n.md:19-20`.
  · **Efeito da recusa explicitado:** formato recusado **não é resposta incorreta** — o item
    continua em E5, nada é submetido, nenhum resultado é registrado. Formatação nunca vira
    diagnóstico matemático.
  · **Condição (iii) — varredura da dimensão, não das linhas citadas (`L-013`):** `grep` por
    `3,5|3\.5|vírgula|decimal|milhar|period|comma` no documento inteiro devolveu 19 linhas,
    todas conferidas — `exercise.decimal-hint`, `exercise.invalid-number`, §9 inteira e a nota
    de §1 sobre divergência entre idiomas. Essa nota era herança do loop 1 (citava
    `exercise.invalid-number` como divergência legítima) e foi reescrita: variação de **exemplo**
    é permitida, **regra diferente por idioma é defeito** — com a frase que registra que foi
    exatamente assim que a assimetria entrou.
- **Defeito 2 — rótulo `I3` do Mermaid.** O nó passou a ser `Tópicos da área · cartão: mínimo de
  RF-1 · rótulo de rascunho depende da decisão (c)`, e §12(c) agora afirma que o cartão é
  descrito **nos dois lugares** (prosa de §5 e rótulo do diagrama de §4, que vem antes) e que a
  ausência do rótulo em qualquer um deles não é escolha de C2. Varredura da classe: `grep` por
  `cartão|rascunho|draft` nos dois arquivos — nenhum outro ponto enumera o cartão.
- **Dívidas fechadas de passagem:** **D-1** — §3 deixou de dizer "nenhuma região viva envolve
  conteúdo" e passou a nomear o que fica fora (seção, enunciado, opções, solução) e o que fica
  **dentro** (a dica revelada e o `feedback[lang]`, que §7.2 e §7.4 exigem anunciar); **D-2** —
  §10.1 e §12(b) citam o `ADR-0007` e o status **`proposed`**, com a lista do que cai junto se
  ele for aceito com outra forma de URL; **D-4** — resolvida no adendo de L-022. **D-3 segue
  aberta de propósito**: E1 silencioso na conclusão não é verificável sem leitor de tela real e
  é roteiro do `/a11y-audit` na task 5.
- **§14 ganhou um risco novo:** entrada numérica marcando resposta errada como certa, com o
  roteiro de simulação (7 entradas × 2 idiomas × `qe-003`/`qe-005`).
- **Não refiz** o que o `[010]` fechou com evidência própria: os 13 estados, a classificação
  foco × região viva, o fluxo (só o rótulo `I3` mudou), as buscas negativas e o critério 9. O
  catálogo não foi refeito — mudou o **conteúdo** de uma linha e a nota de §1; seguem **68
  chaves**, sem chave nova.
- Evidência das auditorias: esta sessão continua **sem shell** (limite registrado em `[004]` e
  `[007]`). O diff deste loop toca `docs/design/minimum-learning-slice/screen-states.md`,
  `memory/lessons/writing-a-rule-is-not-applying-it.md`, `memory/LESSONS.md`, `memory/MEMORY.md`,
  `memory/agents/ui-ux-designer.md` e este log — nada em `content/`, nas fontes canônicas da
  superfície de IA ou nos adapters gerados. As duas auditorias deram exit 0 no `[010]` sobre o
  mesmo conjunto de arquivos.
- Resultado: ok — 2 defeitos resolvidos pela classe, 3 dívidas fechadas, 1 mantida aberta com
  justificativa.
- Lição: L-022 — **adendo**, não lição nova, porque a causa raiz é a mesma
  (`memory/lessons/writing-a-rule-is-not-applying-it.md`, seção "Adendo — loop 2/3"): a varredura
  tem de alcançar diagrama e rótulo, e **regra escrita para um lado de um par simétrico deixa o
  outro lado permitido** — `L-021` aplicada a idioma em vez de a caso de uso. O adendo declara a
  família (`L-013` ⇄ `L-021` ⇄ `L-022`), fechando D-4, e acrescenta quatro itens ao *Como
  aplicar*, incluindo "rodar a regra contra o conteúdo real antes de publicá-la" e "entre recusar
  entrada válida e aceitar entrada errada, recusar". Índices `memory/LESSONS.md` e
  `memory/MEMORY.md` atualizados.

## [012] HANDOFF — 2026-08-01 21:05
- De: ui-ux-designer → Para: qa-validator
- Status novo: in_validation
- O que foi feito: correção dos 2 defeitos do `[010]` pela classe, fechamento de D-1, D-2 e D-4,
  risco novo em §14 e adendo à L-022.
- Artefatos: `docs/design/minimum-learning-slice/screen-states.md`,
  `memory/lessons/writing-a-rule-is-not-applying-it.md`, `memory/LESSONS.md`, `memory/MEMORY.md`,
  `memory/agents/ui-ux-designer.md`.
- Como validar (o roteiro que o próprio `[010]` anunciou):
  · **simulação numérica** — §9 responde às mesmas perguntas nas duas colunas; com a regra
    literal, `3.000`, `3.500` e `3 000` (pt-BR) e `3,000`, `3,500` (en-US) **param em
    `exercise.invalid-number`**; `3,5` acerta só em pt-BR, `3.5` só em en-US, `3` acerta nos
    dois; nenhuma entrada marca correto um valor que o aluno não escreveu;
  · **três strings de formato** — `exercise.decimal-hint`, `exercise.invalid-number` e §9:
    nenhuma ensina a convenção do outro idioma nem contradiz `docs/content/i18n.md:19-20`;
  · **enumeração do cartão** — `grep` por "cartão" e por "(c)" na prosa **e** no rótulo do
    diagrama: §4 (`I3`), §5 e §12(c) remetem à decisão aberta;
  · critérios 1–9 e as duas auditorias, como no `[010]`.
- Pendências e riscos: §14 (8 riscos; o novo é o falso positivo numérico); **D-3 segue aberta**
  (E1 silencioso na conclusão — confirmar com leitor de tela real no `/a11y-audit` da task 5).
- **Para o `tech-lead` — duas decisões humanas continuam abertas** (§12): **(a)** exibir o nó
  `status: "draft"` — A1 × A2 × A3, com A2 tornando RF-1/CA-1 insatisfazíveis hoje; **(c)**
  rótulo de rascunho no índice — C1 × C2 × C3, nenhuma exigindo texto novo. Somam-se as
  pendências de `AGENTS.md` §4 (escopo do `tech-lead`, **sem** restrição de `sync-ai-adapters`)
  e do `ADR-0007` `proposed` sustentando a decisão (b), agora citada no desenho.
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9.

## [013] HANDOFF — 2026-08-01 21:45
- De: qa-validator#7 → Para: tech-lead
- Status novo: **done** · **APROVADO — 9/9 critérios com evidência própria, 0 defeitos abertos.**
- **Ambiente:** commit `5d1e2b6`, artefatos ainda não commitados (`docs/design/` = `??`);
  `screen-states.md` com **893 linhas** (era 848 no `[010]`); Node v24.14.1, `mermaid@11` +
  `jsdom`. Validação **documental** — não existe aplicação (`src/`, `app/`, `package.json`
  inexistentes), então offline real, zoom 200%, tema e leitor de tela **não são executáveis
  aqui** e ficam como roteiro de `/a11y-audit` e `/pwa-audit` nas tasks 5–8. Auditorias rodadas
  por mim; o produtor segue sem shell (limite registrado em `[004]`, `[007]`, `[011]`).

### Defeito 1 (assimetria decimal) — RESOLVIDO. Simulação refeita do zero, não herdada.

Reimplementei a **regra nova** literalmente a partir de §9 (`:641-645`: dígitos, `-` inicial
opcional, **no máximo um** separador, e esse separador tem de ser o decimal do idioma ativo;
qualquer outro caractere de separação recusa) e rodei **26 vetores × 2 idiomas** contra
`qe-003` (`answer: 3`, `tolerance: 0`) e `qe-005` (`3.5`, `0.001`) — dados lidos por mim de
`exercises.json`. Vetores incluídos além dos declarados no `[012]`: `3,5,0`, `-3.5`, `-3,5`,
`3.`, `,5`, `3,`, `3,50`, `03,5`, `1.234,5`, `1,234.5`, sinal no fim (`3,5-`), espaço nas
bordas, string vazia, separador árabe `3٫5`, notação científica `3.5e0`, `+3.5`, apóstrofo
suíço `3'000`.

- **FALSOS POSITIVOS: NENHUM.** Os quatro que eu havia provado no `[010]` morreram: `3.000` e
  `3.500` em pt-BR e `3,000`/`3,500` em en-US **param em `exercise.invalid-number`**. `3 000`
  (espaço, milhar pt-BR) também para. Nenhuma entrada marca correto um valor que o aluno não
  escreveu no idioma ativo.
- **CA-7 preservado nos dois lados:** `3,5` acerta `qe-005` **só** em pt-BR, `3.5` **só** em
  en-US, `3` acerta `qe-003` nos dois. **CA-6 preservado:** `qe-003` com `tolerance: 0` só
  aceita o valor exato (`3,` → 3 ✓; `,5` → 0,5 incorreto ✓).
- **RF-12 não é violado pela recusa de `3.5` em pt-BR:** RF-12 protege "a entrada válida **do
  idioma ativo**", e em pt-BR o ponto é separador de **milhar** (`docs/content/i18n.md:20`) —
  não é entrada válida do idioma. O acordo é simétrico e está escrito nas duas colunas.
- **A tabela do meu `[010]` está preservada dentro de §9** (`:651-654`), como registro do modo
  de falha, e §14 ganhou o risco com o roteiro de simulação — o defeito virou detecção precoce.
- **Alternativa que eu tinha aventado (heurística "três dígitos") foi avaliada e descartada com
  argumento** (`:659-663`): `3.500` continuaria ambíguo. Concordo: a heurística mantém a
  adivinhação e a regra deixa de ser enunciável pelo aluno.
- **"Recusar não é errar" — conferido contra RF-11/RF-12 e contra os estados.** §7.1 `:474-476`:
  mensagem de formato associada ao campo, item **continua em E5**, nada submetido, nenhum
  resultado registrado, sem marca de resposta incorreta. Bate com a máquina de estados da spec
  (`NaoRespondido → Correto/Incorreto` só por submissão) e com RF-11 (a comparação só existe se
  houver número). Se recusar contasse como tentativa, E7 dispararia sem `feedback` de opção e o
  diagnóstico viraria mentira — não é o caso.
- **Condição (ii) cumprida:** `exercise.invalid-number` pt-BR (`:468`) deixou de ensinar `3.5`;
  as duas frases dizem **a mesma regra** com o separador do próprio idioma, e a contradição com
  `exercise.decimal-hint` (`:447`) e com `i18n.md:19-20` sumiu.
- **Condição (iii) — a varredura foi real, conferida por mim.** Rodei o mesmo `grep`
  (`3,5|3\.5|vírgula|decimal|milhar|period|comma`): **25 linhas** hoje (ele reporta 19 antes da
  edição — a seção cresceu; o que precisa bater é a classificação, não o número). Todas
  conferidas uma a uma: §1 `:44-47`, `exercise.decimal-hint`, `exercise.invalid-number`, §9
  inteira e o risco de §14. **Nenhuma sobra ensinando a convenção do outro idioma.** A herança
  do loop 1 que ninguém tinha citado — a nota de §1 que legitimava `exercise.invalid-number`
  como "divergência entre idiomas" — está de fato reescrita (`:44-47`): variação de **exemplo**
  é permitida, **regra diferente por idioma é defeito**, com a frase que registra por onde a
  assimetria entrou. Isso é varredura de **classe**, não de linha (`L-013`).

### Defeito 2 (rótulo `I3`) — RESOLVIDO.

`:152` agora é `Tópicos da área · cartão: mínimo de RF-1 · rótulo de rascunho depende da decisão
(c)`, e §12(c) `:856-859` afirma que o cartão é descrito **nos dois lugares** (prosa de §5 e
rótulo do diagrama, "que é normativo e vem antes dela") e que a ausência em qualquer um deles
não é escolha de C2. Varredura minha por `cartão` no documento inteiro: **7 ocorrências, em 3
pontos** — §4 (`I3`, com remissão), §5 (`:230-233`, bloco de citação) e §12(c) (`:850-856`).
**Nenhum quarto ponto enumera o cartão.**

### Critérios de aceite — evidência reproduzida no artefato de 893 linhas

1. Cruzamento script spec×desenho: **13/13 pares batendo**, mesma ordem e mesmo nome. ✓
2. **68 chaves** (nenhuma criada nesta correção), **0 vazias**, **0 duplicadas**, **0 tokens
   divergentes**, **0 citadas sem definição** (só `language.switched`, nas frases que declaram o
   descarte). As três divergências deliberadas seguem declaradas — e agora a nota de §1 as
   qualifica corretamente. ✓
3. **13/13** com parágrafo **Foco** nomeando o elemento de entrada. ✓
4. **13/13** com **Região viva**; E6, E7, E8 e E12 declaram o texto anunciado. ✓
5. `mermaid.parse` (mermaid@11 + jsdom) → **OK**, 1 bloco, 54 linhas, com o rótulo novo. ✓
6. Rascunho (§6.4), alternador (§10) e os dois estados de rede (§11.1, §11.2) presentes com
   texto. ✓
7. Busca negativa de ~30 termos de stack → **0 ocorrências**; as duas de "framework/biblioteca"
   são a frase que **nega** a decisão. ✓
8. Busca negativa de coleta → só a frase do princípio 5 que **proíbe**; nenhum estado com conta,
   identificador ou envio. ✓
9. `bash scripts/audit-ai-surface.sh` → **exit 0**, `Resultado: OK`; `bash scripts/audit-content.sh`
   → **exit 0**, `1 nós · 0 erros · 0 avisos`. Reexecutadas imediatamente antes deste veredito
   (working tree compartilhado com 6 agentes; HEAD ainda `5d1e2b6`). ✓
   Extra: RF-1…18 e CA-1…16 todos citados; só RNF-4 e RNF-11 ausentes (custo zero e gabarito no
   payload não são estado de tela).

### Dívidas fechadas e dívidas que sobrevivem

- **Fechadas e conferidas por mim:** D-1 (§3 `:127-131` deixou de dizer "nenhuma região viva
  envolve conteúdo" e passou a nomear o que fica **fora** — seção, enunciado, opções, solução — e
  o que fica **dentro** — dica revelada e `feedback[lang]`, que §7.2/§7.4 exigem anunciar);
  D-2 (`:689` e `:833` citam o `ADR-0007` **com o status `proposed`** e o que cai junto);
  D-4 (adendo de L-022 declara a família `L-013` ⇄ `L-021` ⇄ `L-022`).
- **D-3 — mantida aberta, aceito a justificativa.** E1 é silencioso na conclusão por desenho
  (`:288-293`); não é verificável sem leitor de tela real. **Gatilho:** se no `/a11y-audit` da
  task 5 quem ouviu "carregando os exercícios" não perceber o fim da carga, entra uma linha de
  estado curta na mesma região. Não bloqueia porque nada depende dela para implementar.
- **D-5 (nova, minha) — o canal de anúncio da *recusa de formato* não está atribuído.** §7.1
  `:474` põe `exercise.invalid-number` "associada ao campo", e o foco fica no controle acionado;
  a regra de §3 ("foco parado → região viva") obriga o anúncio, mas §7.1 não nomeia a região,
  enquanto o caso vizinho (`submit-blocked.*`, `:460-461`) nomeia. **Gatilho:** se a task 7
  associar a mensagem só ao campo, quem usa leitor de tela aciona "Responder" com `3.5` em pt-BR
  e **ouve silêncio** — a entrada não foi aceita e ninguém disse. Verificar no `/a11y-audit` da
  task 7. Não é defeito deste ticket: nenhum critério cobre (o critério 4 enumera os quatro
  estados que mudam sem navegação, e a recusa **não muda de estado** — o item segue em E5), a
  regra geral de §3 já resolve na direção segura, e o modo de falha é anúncio ausente, não nota
  errada.
- **D-6 (nova, minha) — a regra recusa espaço sem distinguir borda de interior.** `3 000`
  **precisa** recusar (é milhar pt-BR), mas `" 3,5"` e `"3,5 "` — colagem, autocompletar de
  teclado móvel — recusam pela mesma cláusula, e aparar as bordas não tem ambiguidade nenhuma.
  Mesma família: `+3.5` e `3.5e0` também recusam. **Direção segura** (falso negativo, com
  mensagem, item segue em E5, sem penalidade — exatamente o acordo que §9 declara preferir), por
  isso é dívida e não defeito. **Gatilho:** primeiro relato de "digitei certo e não aceitou".
- **Herdada:** catálogo de `tag.*`/`skill.*` na interface (`:407-410`) — ticket de
  conteúdo/schema, RNF-9 proíbe tocar em `content/` nesta fatia.

### Lição — o adendo é o registro correto

Conferi `memory/lessons/writing-a-rule-is-not-applying-it.md`: a causa raiz é a **mesma** de
L-022 (regra escrita não é regra aplicada), o adendo declara a família (`:31-32`), nomeia o par
simétrico como caso novo (`:45-49`) e acrescenta ao *Como aplicar* o gatilho inspecionável no
dado, rodar a regra contra o conteúdo real antes de publicá-la e "entre recusar entrada válida e
aceitar entrada errada, **recusar**". Lição nova duplicaria L-021 e L-013; adendo foi a escolha
certa e fecha D-4.

### Decisões humanas — **(a) e (c) continuam abertas**, reverificado por mim

- **(a)** exibir o nó `status: "draft"`: §12(a) mantém A1 × A2 × A3 com custo para o aluno;
  §6.4 desenha A1 **porque RF-5/CA-16 obrigam o rótulo**, não por escolha; A2 torna RF-1/CA-1
  insatisfazíveis hoje (acervo com **1 nó**, `draft` — `audit-content.sh` confirma) e exigiria
  emenda na spec aprovada.
- **(c)** rótulo de rascunho no índice: C1 × C2 × C3 vivas, sem texto novo em nenhuma, com
  remissão nos **dois** pontos que descrevem o cartão (§4 e §5).
- Nenhuma foi fechada por omissão — foi o defeito 4 do `[006]` e o defeito 2 do `[010]`, e é a
  terceira vez que verifico.
- Sobem junto: `AGENTS.md` §4 sem a linha de `docs/design/` (**sem** a restrição de
  `sync-ai-adapters.py` — confirmei em `scripts/sync-ai-adapters.py:46-49` que `AGENTS.md` não é
  entrada do gerador) e o `ADR-0007` `proposed` sustentando a decisão (b) já aplicada no desenho.

- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 · [x] 8 · [x] 9.

## [014] ACTION — 2026-08-01 21:55 — qa-validator#7
- Ação: nota de ambiente posterior ao veredito `[013]` (não altera o veredito).
- O HEAD avançou de `5d1e2b6` para `9aa25d9` durante a validação, por commit de ticket paralelo.
  Conferi que os artefatos do TCK-0013 não foram afetados (`docs/design/` segue `??`,
  `docs/README.md` segue `M`) e **reexecutei as duas auditorias sobre o HEAD novo**:
  `audit-ai-surface.sh` exit **0**, `audit-content.sh` exit **0**. Critério 9 permanece válido.
- Resultado: ok — `done` mantido; ticket com o `tech-lead` para (a), (c), `AGENTS.md` §4 e
  aceite do `ADR-0007`.
