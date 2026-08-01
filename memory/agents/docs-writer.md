# Memória do agente `docs-writer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Produz e mantém a documentação interna do projeto (docs/) nos padrões do repositório — ADRs, specs, C4, padrões de conteúdo, READMEs e índices. Usar para escrever, reorganizar ou corrigir documentação que não é conteúdo do produto.

## Notas persistentes

- **Spec nasce `draft`.** Quem escreve não aprova (`AGENTS.md` §10, regra 4). Marcar
  `approved` no mesmo turno em que se escreve a spec é defeito de processo — a aprovação é da
  etapa de review, e o status aparece em três lugares: front matter de `spec.md`, de `plan.md`
  e a linha em `docs/specs/README.md`.
- **Separação spec × plan quando há ADR pendente ou recém-decidido.** O `spec.md` só fala de
  comportamento observável e contrato de dados — assim ele sobrevive a qualquer stack. A
  citação da decisão de arquitetura fica no `plan.md`, e mesmo lá só como *direção*: escolha de
  biblioteca, teste, service worker e forma de URL é decisão de implementação, feita nos
  tickets. Isso mantém o critério "não bloqueia a escolha da stack" verificável.
- **Regra visual do `DOC-STANDARDS.md` cobra três coisas além do diagrama**: leitura de 3–6
  linhas dizendo também o que o diagrama **não** mostra, as fontes que o sustentam e a marcação
  estado atual × proposta. Diagrama sem esses três itens é entrega incompleta.
- **Mermaid `stateDiagram-v2`:** evitar `\n` e `<=` dentro de rótulos de transição; usar `—`
  para separar rótulo e referência (`nova tentativa — RF-15`). Reduz risco de falha de parse
  nos renderizadores.
- **Requisito transversal "correção matemática"** em spec que não cria conteúdo = *não
  aplicável*, justificando com o campo `verified` dos itens de `exercises.json`. Não inventar
  verificação que não foi feita nesta etapa.
- Templates de spec ficam em `docs/specs/templates/{spec,plan,tasks}.md`; o índice
  `docs/specs/README.md` tem uma linha placeholder ("nenhuma spec criada ainda") que deve ser
  **substituída**, não acrescida, na primeira spec.
- Evidência de auditoria útil no handoff: `bash scripts/audit-ai-surface.sh` (espera
  `Resultado: OK`) e `bash scripts/audit-content.sh` (espera `0 erros · 0 avisos`).
- **Texto de licença é literal.** MIT, CC e afins se copiam palavra por palavra; parafrasear
  ou "melhorar" invalida a licença. O que é nosso vem *ao redor* do texto legal: escopo
  (o que a licença cobre e o que não cobre), forma de atribuição esperada e regra para quem
  contribui.
- **ADR de licença só serve se disser o que fazer na segunda-feira.** A parte que muda o
  trabalho é a compatibilidade de fontes; escrevê-la como árvore de decisão + tabela com as
  fontes **reais** do repositório (não hipóteses) foi o que tornou o critério verificável.
  Mnemônico que ficou: **"NC = leitura, não matéria-prima"**.
- **Regra normativa mora em três lugares**, senão não é lida: o ADR (por quê), o documento do
  praticante (`docs/content/content-standards.md`, incluindo o checklist de `published`) e a
  memória operacional da área (`memory/context/<área>.md`). ADR sozinho é regra que ninguém
  aplica.
- **Decisão aceita só está propagada quando chega à fonte que a ferramenta carrega sozinha.**
  ADR + documento do praticante + memória **não** bastam: `AGENTS.md` e
  `.github/instructions/` são o que as 12 ferramentas leem automaticamente; enquanto eles
  disserem outra coisa (ou disserem "preferência" onde o ADR diz "proibido"), a regra não
  existe na prática. Checklist de propagação em `L-009` (adendo) e `L-010`. Regra em fonte
  canônica exige `python3 scripts/sync-ai-adapters.py` + as duas auditorias depois.
- **Ao mexer em regra numerada do `AGENTS.md`**, conferir quem cita os números (`grep -rn
  "§9\." --include="*.md" .`) antes de inserir item novo no meio da lista — a renumeração
  quebra referências silenciosamente em ADRs, docs e tickets.
- **Rodar o sync com outra cadeia ativa** regenera adapters que carregam mudanças alheias
  ainda não sincronizadas. Não é erro, mas precisa ser declarado no handoff, senão o revisor
  atribui esse diff ao ticket errado.
- **Estreitar uma norma para torná-la verificável cria uma permissão silenciosa.** O caso que
  a redação deixa de fora não fica neutro — fica permitido (§9.2 dizia "display", e a fórmula
  inline ficou sem regra). Ao fechar a lacuna, quase nunca se estende a mesma obrigação: dá-se
  ao caso frequente uma obrigação **diferente e mais barata**, com **gatilho mecânico**
  inspecionável no artefato. "Avaliar caso a caso" não é regra — é devolver o problema ao
  autor. Lição `L-021`.
- **Calibrar o gatilho rodando-o contra o artefato real, antes de publicar a norma.** Foi o
  que dimensionou o passivo do nó piloto e revelou ocorrências que nenhuma revisão anterior
  tinha listado. O inventário com **veredito item a item** é o que torna o ticket de correção
  executável sem reinterpretar a norma (`L-013`).
- **O padrão de busca vem da definição da classe, nunca das ocorrências que já vi** — e o
  mesmo método vale para **todos** os artefatos. No TCK-0006 escrevi
  `grep '(-[0-9a-z]*)\^'` a partir dos `(-4)^2` conhecidos e perdi `(x+3)^2`, depois de usar
  parser em `theory.*.md` e `grep` estreito em `exercises.json` — e declarei varredura
  completa nos três. Teste do padrão antes de usá-lo: *ele acharia uma ocorrência que eu ainda
  não vi?* Adendo de `L-021`.
- **A lista de propagação se deriva dos artefatos que a regra nomeia**, não dos arquivos que
  já abri: para cada artefato citado na norma, quem o **escreve** e quem o **revisa**. A regra
  do TCK-0006 nomeava `exercises.json` desde a primeira versão e mesmo assim não chegou ao
  `exercise-designer` nem a `/new-exercise-set`.
- **Enumeração fechada repetida fora do documento-fonte é dívida.** Quem **reenuncia** uma
  regra deve citar o **veredito do teste** ("toda fórmula que o teste X marca como *exige*"),
  não a lista de gatilhos — senão o gatilho novo passa pela formulação antiga em silêncio, e
  cada frase continua verdadeira isoladamente. **Checklist e portão referenciam, nunca
  reenunciam:** no TCK-0006, o checklist de `published` dizia "com argumento composto" e
  `-x^2` (que não tem argumento composto) atravessava o portão. 2º adendo de `L-021`.
- **Acrescentar gatilho a regra já propagada não é editar o documento-fonte** — é `grep` pela
  **formulação antiga** em toda a superfície, gerados incluídos, e conferir que nenhum ponto
  ficou com a enumeração fechada. Métrica que usei:
  `for f in <20 arquivos>; do grep -c '<termo do gatilho novo>' $f; done` → nenhum zero.
- **Se o teste tem mais de uma parte, dê nome a cada uma** e escreva no documento-fonte que
  repetir só uma delas é defeito. O aviso viaja junto com a regra e sobrevive ao próximo
  agente que a copiar.
- **Somar totais a partir da tabela publicada, não da lembrança de tê-la escrito.** "3 pontos
  por idioma" com quatro linhas EXIGE logo acima passou por mim e foi para a memória
  compartilhada, de onde o ticket dependente ia ler.
- **Caso citado como justificativa precisa de veredito próprio.** Usei `-5^2` para justificar
  "base entre parênteses é composta" e deixei `-5^2` sem obrigação — a exceção do sinal unário
  é inócua na fração ($-(7/2) = (-7)/2$) e **não** na potência ($-25 \ne 25$). Se o exemplo
  serve de argumento, ele é um caso da norma.
- **Adapter de agent/skill é ponteiro; adapter de regra é cópia.** `.claude/commands/`,
  `.github/chatmodes/` e `.gemini/commands/` só apontam para `.claude/agents/*.md` — editar um
  agent **não** muda esses arquivos, e o `--check` continua verde. Só
  `.github/instructions/*.md` é embutido em `.cursor/rules/`, `.windsurf/rules/`,
  `.agents/rules/`, `.rules`, `.clinerules` e `.junie/guidelines.md`. Consequência: propagar
  regra exige tocar as **instructions**, não só o agent.
- **Prova de que o sync não arrastou trabalho alheio:** conferir que o `git diff --stat` dos
  gerados bate com a aritmética das próprias edições (regra `core` × 6 destinos + regra
  `content` × 3 = 9 arquivos, +54/−12). Declarar essa conta no handoff resolve a dúvida do
  revisor sem ele precisar ler os gerados.
- **Editar arquivo que outro agente está mexendo:** `memory/context/project-context.md` e
  índices (`docs/adr/README.md`) são pontos de colisão. Reler imediatamente antes, editar só
  a linha da própria decisão, nunca reescrever o arquivo. Quando um trecho desatualizado é de
  outra área (ex.: o README ainda chamando o `ADR-0003` de `proposed`), **reportar como
  pendência no handoff em vez de corrigir**.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0002 · etapa `execute` do dev-loop `minimum-learning-slice` | `docs/specs/minimum-learning-slice/{spec,plan,tasks}.md` criados em `draft` a partir de `.dev-loop/minimum-learning-slice/requirements.md`; índice `docs/specs/README.md` atualizado; auditorias sem erro; handoff `[006]` para `code-reviewer`, ticket em `in_review` | L-001, L-003 |
| 2026-08-01 | TCK-0004 · licença do projeto (como **`docs-writer#2`**, subagente spawnado com a instância principal ocupada no TCK-0002) | `ADR-0005-project-license.md` (`accepted`), `LICENSE` (MIT literal) e `LICENSE-CONTENT` (CC BY-SA 4.0, pt-BR + en-US) criados; regra "NC = leitura, não matéria-prima" propagada para `docs/content/content-standards.md` e `memory/context/content.md`; `README.md`, `project-context.md` e roadmap deixam de listar a licença como aberta; auditorias verdes; handoff `[006]` para `code-reviewer`, ticket em `in_review` | L-006, L-007, L-009 |
| 2026-08-01 | TCK-0006 · convenções de leitura de fórmula e fronteira display × inline | Fronteira decidida por **obrigação diferenciada** (display = leitura integral; inline com argumento composto = agrupamento em palavras) com o *teste do argumento composto* como gatilho mecânico; tabela das 9 convenções e teste em `docs/content/accessibility.md`; glossário `subscrito (índice) \| subscript` com desambiguação do índice do radical em `i18n.md`; propagação para `AGENTS.md` §9.2 (sem renumeração), `.github/instructions/{content,core}`, `content-author`, `a11y-ux-reviewer`, `/new-topic`, `/a11y-audit` e o checklist de `published`; inventário do passivo do piloto com veredito item a item; sync (9 gerados) e `--check` limpos; auditorias verdes; handoff `[005]` → `code-reviewer` | L-021, L-009, L-013 |
| 2026-08-01 | TCK-0006 · correção do `[006] REJECT` (loop 1/3, `code-reviewer#8`) | B1 (inventário perdeu `(x+3)^2` — padrão de busca derivado dos exemplos) e B3 (regra não chegou a `exercise-designer` nem a `/new-exercise-set`) resolvidos: **uma** causa raiz, registrada como **adendo em `L-021`**, não lição nova. B2: total corrigido para **22 pontos** (8+14), também em `memory/context/content.md`. B4: gatilho novo "sinal unário à frente de base elevada" (custo zero verificado). S1–S4 acatadas; Mermaid revalidado no parser; 3 gerados; auditorias verdes; handoff `[008]` → `code-reviewer` | L-021 (adendo), L-013 |
| 2026-08-01 | TCK-0006 · correção do `[009] REJECT` (loop 2/3, `code-reviewer#8`) | B5 (gatilho novo não chegou ao lado da teoria; **checklist de `published` mais frouxo que a norma** — `-x^2` atravessava o portão) resolvido de forma **estrutural**: teste renomeado para "teste de marcação de agrupamento" com partes (a) e (b) nomeadas, aviso de "não cite só (a)" no documento-fonte, e o portão passando a **referenciar o veredito** em vez de reenunciar; 10 pontos atualizados, `grep` de verificação sem zeros nos 20 arquivos. B6: `CORRECTION` `[010]` com `Corrige: [004]`. S1 (critério unário × binário próprio do gatilho (b)2) e S2 (`prompt` → `stem`) acatadas. Inventário revalidado: **22, inalterado**; Mermaid, `--check` e auditorias verdes | L-021 (2º adendo), L-010 |
| 2026-08-01 | TCK-0004 · correção do `[007] REJECT` (loop 1/3, `code-reviewer#4`), como `docs-writer#2` | B1 resolvido: regra de compatibilidade tornada **imperativa** em `AGENTS.md` (§9.7 nova; §9.6 sem "preferência"; sem plágio → §9.8), `.github/instructions/{content,core}.instructions.md`, `.claude/agents/{content-author,researcher}.md`, `prompts/bootstrap-session.md` e `CONTRIBUTING.md`; S1–S4 acatadas (divergência do *Livro Aberto*, jurisdição do domínio público, prevalência do `legalcode`, artefatos de memória no log); `sync-ai-adapters.py` rodado (9 arquivos) e `--check` limpo; auditorias verdes; handoff `[009]` → `code-reviewer` | L-009 (adendo), L-010 |
