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
- **Diagrama C4 não mistura decidido com proposto**: `PROPOSTO` sem ADR nomeado é órfão e volta
  como defeito. Afirmação absoluta do tipo "nada aqui é hipótese" é armadilha. Desde o aceite
  do TCK-0016 (2026-08-01) **não há mais `PROPOSTO` nos níveis Context e Container** —
  `ADR-0003`, `ADR-0006` e `ADR-0007` estão todos `accepted`; o que sobra é `EM ABERTO
  (ticket)`, que o aceite **não** apaga.
- **Aceitar ADR ≠ implementar, e ≠ atestar a implementação.** Quando o ticket de execução já
  está em revisão (TCK-0015 no TCK-0016), escrever no ADR "o aceite autoriza aquele trabalho,
  não afirma que ele esteja correto" — senão o ADR vira certificado de qualidade de código que
  ele não reviu. Vale também para "Estado atual × proposta": o parágrafo tem de virar "Estado
  no aceite" e datar o que já existia.
- **Decisão tomada mata a grafia alternativa em toda parte, inclusive em ADR aceito antigo**
  (aplicação de L-013 no TCK-0016): mantida como opção viva, a alternativa descartada vira
  informação falsa. Fronteira que uso: some de tudo que a apresente como **escolha disponível**
  (perguntas ao usuário, rótulo de diagrama, "como alternativa", pergunta em aberto de spec);
  **fica** só onde é registro histórico da própria decisão (lista de alternativas consideradas
  e descartadas). O rótulo Mermaid do `ADR-0003` mostrava `/pt-BR/…` — ADR aceito que **não**
  decidia URL: generalizado, com nota de "emenda editorial" no cabeçalho e sem tocar na decisão.
- **`docs/adr/README.md` é editado por vários agentes** — sempre edição cirúrgica da linha do
  próprio ADR, nunca reescrita do arquivo.
- **Régua para arbitrar ADR × ticket** (L-020): permanência observável de fora. "Se eu trocar
  isto em seis meses, quem quebra?" — link de terceiro, arquivo do acervo, fatura ou outro ADR
  → ADR; só o nosso código → ticket. Serviu para decidir **dentro** do `ADR-0007` a forma da
  URL bilíngue (contrato público) e para **deixar fora** biblioteca de UI, teste, cache e
  momento do KaTeX. É o complemento operacional de L-011, que só dizia o que não fazer.
- **Três marcadores no diagrama, não dois** (`docs/architecture/README.md`): sem marcador =
  decidido em ADR aceito; `PROPOSTO (ADR-NNNN)` = espera aceite; `EM ABERTO (ticket)` = o ADR
  decidiu **não** decidir. Sem o terceiro, toda escolha de ticket vira `PROPOSTO` órfão — o
  defeito B4 do TCK-0003 pelo avesso. Marcar de **mais** é o mesmo defeito que marcar de
  menos: rotulei um boundary inteiro como `PROPOSTO` e ele continha uma build que o `ADR-0003`
  já exige.
- **ADR `proposed` do qual um ticket depende é bloqueio, não pendência decorativa.** Entregar
  o esqueleto como `proposed` significa que a task 5 da fatia mínima não começa sem aceite
  humano — declarar isso no handoff e no relatório, senão o executor descobre sozinho e
  improvisa. **Desfecho observado (TCK-0011 → TCK-0015 → TCK-0016):** o executor não esperou; o
  usuário autorizou a execução e o registro ficou para trás, produzindo um ticket implementando
  sob ADR que se proibia a si mesmo. Autorização do usuário destrava a **execução**, não
  substitui o **aceite** — quando eu escrever "nenhum ticket pode X antes do aceite", pedir o
  ticket de aceite no mesmo handoff, e não só avisar.
- **Ao aceitar, a lista de "o que continua sendo decisão de ticket" é seção obrigatória do
  ADR** (L-011/L-020 na forma positiva). Sem ela, o aceite é lido como fechamento geral e a
  próxima entrega trata o mecanismo como decidido. As três seções que uso: *o que passa a
  valer* · *o que fica proibido sem ADR novo* · *o que continua sendo decisão de ticket*.
- **Gratuidade tem condição de elegibilidade, não só limite:** GitHub Actions é grátis porque
  o repositório é **público** (`gh repo view --json visibility` → `PUBLIC`), e a Vercel Hobby
  porque a conta é **pessoal** e o uso **não comercial** (projeto de organização não conecta no
  Hobby). Citar o limite sem a condição é o tipo de afirmação que envelhece em silêncio.
- **Portão só existe onde a publicação acontece.** Validação que só roda no CI não impede push
  direto em `main`; e o runtime do validador precisa existir onde o portão for posto. **Mas
  escolher o lugar do portão é do ticket, não do ADR** (`plan.md`, item 5) — o ADR exige o
  resultado (nó reprovado não vira página publicada) e para por aí. Foi exatamente aqui que
  reincidi em L-011 no TCK-0011.
- **A segunda leitura é obrigatória, e é sobre o texto pronto** (adendo de L-020): a régua
  ADR × ticket aplicada só na triagem das decisões candidatas não pega o que entra depois como
  *justificativa de apoio*, rótulo de Mermaid ou linha de `scripts`. Frase delatora, com forma
  fixa: **"é isso que faz X ser Y, e não Z"**.
- **Comparar as consequências gêmeas dos ADRs irmãos** antes do handoff: no TCK-0011 o
  `ADR-0006` chamava de "hipótese" a mesma consequência que o `ADR-0007` afirmava como fato.
  Dois documentos da mesma entrega discordando é sintoma detectável sozinho.
- **Marcação tem duas direções** (adendo de L-013): corrigi um "marcar de mais" e entreguei um
  "marcar de menos" na mesma malha. Receita barata: listar **cada** nó e **cada** `Rel` do bloco
  e escrever ao lado a fonte que o sustenta; o que ficar sem fonte é o defeito.
- **Quando outro ticket detém o direito de rodar o sync, a propagação não para — o log é que
  carrega a dívida.** No TCK-0016 editei `.github/instructions/{core,app}` sem rodar
  `sync-ai-adapters.py` (direito exclusivo do TCK-0006 até fechar) e declarei os **9 arquivos**
  a regenerar. `.claude/agents/<nome>.md` **não** derruba o `--check` (o adapter só embute o
  front matter); uma regra em `.github/instructions/` derruba nove arquivos.
- **Dívida declarada tem validade: expira quando o impedimento acaba** (defeito bloqueante do
  `[009]` no TCK-0016). Deixei o critério 8 em `[~]` porque o TCK-0006 detinha o sync; ele
  fechou e commitou **durante** a minha execução, e o `[~]` virou dispensa de critério de
  aceite. Regra: antes de entregar com dívida atribuída, **reverificar o impedimento** —
  `grep -m1 "^status:" tickets/TCK-NNNN-*/ticket.md` e `git log --oneline -3` — e, se tiver
  caído, executar. Bloqueio externo não se presume estável só porque era verdade quando comecei.
- **Prova de atribuição por `HEAD` caduca com o commit alheio.** Provei a autoria do `OUTDATED`
  comparando o texto do outro ticket nos gerados com `git show HEAD:<fonte>`; o `dea3303`
  entrou depois e o método parou de discriminar (o texto passa a aparecer dos dois lados). O
  revisor refez por **regeneração em cópia no scratchpad** e chegou à mesma conclusão. Método
  robusto: regenerar num clone/cópia e comparar, não confiar em `HEAD` como linha de base móvel.
- **Sync pode carregar edição não commitada de terceiro — declarar antes que pareça arraste.**
  O TCK-0006 fechou deixando `core.instructions.md` fora do commit (`git show HEAD:… | grep -c`
  → 0), então o meu sync propagou o texto dele para os 6 gerados de `core`. Verificação barata
  ao rodar o sync: `diff` do `git status --porcelain` antes × depois, `find -mmin -3` e mtime
  dos arquivos do ticket vizinho — prova, no mesmo log, o que foi e o que não foi tocado.
- **Parser de Mermaid neste ambiente:** `mermaid.parse` em Node puro falha com
  `purify.addHook is not a function`. Precisa de DOM — `jsdom` do cache do npx
  (`/home/douglas-silva/.npm/_npx/27e1695deffacbeb/node_modules`), com `navigator` injetado por
  `Object.defineProperty` (é getter-only no Node 24). Sem isso, a "falha" é do harness, não do
  diagrama.
- Auditorias relevantes ao encerrar: `bash scripts/audit-ai-surface.sh` e
  `bash scripts/audit-content.sh` (ambas devem sair com exit 0).

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0016 — correção do `[009] REJECT` (loop 1/3) | Defeito único: `sync-ai-adapters.py` não rodado. O impedimento (TCK-0006 com o direito exclusivo) **caiu durante a execução** — fechou e commitou em `dea3303` —, e a dívida declarada virou dispensa de critério. Sync rodado (9 gerados), auditorias exit 0 nas duas, edição não commitada de terceiro em `core.instructions.md` declarada com prova; 3 sugestões acatadas (contagem 6→5 por `CORRECTION`, convenção de emenda editorial em `docs/adr/README.md`, pendências roteadas ao `tech-lead`). Reincidência: **negativa** nas duas famílias | L-025 |
| 2026-08-01 | TCK-0016 — aceite do `ADR-0006` (CI/CD) e do `ADR-0007` (esqueleto) | `accepted` com as 3 decisões do usuário (URL minúscula, previews por PR, projeto na raiz); consequências em 3 seções (passa a valer / proibido sem ADR novo / continua do ticket); `PROPOSTO` eliminado por classe nos dois C4 e `EM ABERTO (ticket)` preservado (4 ocorrências); grafia `/pt-BR/` removida como opção viva, inclusive do rótulo Mermaid do `ADR-0003` (emenda editorial) e da pergunta em aberto da spec; varredura da raiz com propagação para `AGENTS.md`, `README.md`, `prompts/`, `.github/instructions/{core,app}`, `.claude/agents/platform-architect.md` e `memory/context/{frontend,devops,project-context}`; sync **não** rodado (direito do TCK-0006), 9 arquivos declarados; 5 blocos Mermaid reparseados, 0 falhas; `audit-content.sh` exit 0 | L-010, L-011, L-013, L-020 |
| 2026-08-01 | TCK-0011 — correção do `[006] REJECT` (loop 1/3) | B1: `ADR-0007` fechava `prebuild` como lugar do portão do RF-18, que a spec aprovada dá ao ticket — trocado por resultado exigido, com varredura de `prebuild`/"portão da build" nos 3 documentos + memória; B2: `Rel(build, validator)` sem marcador → `EM ABERTO (ticket)`, mais varredura nó a nó e correção do excesso em `ci`; S1–S4 acatadas. Terceira ocorrência da família hoje: adendos em L-011, L-013 e L-020, sem lição nova | L-011, L-013, L-020 |
| 2026-08-01 | TCK-0011 — C4 Container + ADR de CI/CD + esqueleto da aplicação | `c4-container.md` (3 marcadores: decidido / `PROPOSTO (ADR-NNNN)` / `EM ABERTO (ticket)`), `ADR-0006` (CI/CD, `proposed`, custo zero com fonte e data) e `ADR-0007` (esqueleto: Astro, raiz, `src/content-contract/`, `package.json` mínimo, URL `/pt-br/`, `proposed`); `c4-context.md` sem `PROPOSTO` órfão; nenhuma linha de código, nenhum `package.json`; auditorias verdes | L-020 |
| 2026-08-01 | TCK-0003 — aceite do `ADR-0003` (stack da plataforma) | `accepted`: opção C (estático + ilhas) + persistência local-first sem conta; consequências, restrição do contrato de dados e propagação para README/memória; auditorias verdes; handoff → `code-reviewer` | L-008 |
| 2026-08-01 | TCK-0003 — correção do `[010] REJECT` (loop 2/3) | B4: rótulo do Mermaid do ADR ainda dizia "KaTeX pré-renderizado", contradizendo o texto; corrigido + varredura da classe no arquivo (achou 2ª ocorrência: nó do service worker); leitura do diagrama e S4/S5 acatadas | L-013 |
| 2026-08-01 | TCK-0003 — correção do `[006] REJECT` (loop 1/3) | B1 propagação inerte (7 pontos: `AGENTS.md` §1/§11, `core`/`app` instructions, `.claude/agents/platform-architect.md`, `roadmap.md`, `README.md`, `prompts/bootstrap-session.md`) + sync; B2 ADR deixou de fixar build × runtime do KaTeX; B3 `docs/architecture/*` declarados e contradição de CI/preview resolvida; S1–S3 acatadas | L-010, L-011 |
