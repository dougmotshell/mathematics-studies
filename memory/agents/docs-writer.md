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
| 2026-08-01 | TCK-0004 · correção do `[007] REJECT` (loop 1/3, `code-reviewer#4`), como `docs-writer#2` | B1 resolvido: regra de compatibilidade tornada **imperativa** em `AGENTS.md` (§9.7 nova; §9.6 sem "preferência"; sem plágio → §9.8), `.github/instructions/{content,core}.instructions.md`, `.claude/agents/{content-author,researcher}.md`, `prompts/bootstrap-session.md` e `CONTRIBUTING.md`; S1–S4 acatadas (divergência do *Livro Aberto*, jurisdição do domínio público, prevalência do `legalcode`, artefatos de memória no log); `sync-ai-adapters.py` rodado (9 arquivos) e `--check` limpo; auditorias verdes; handoff `[009]` → `code-reviewer` | L-009 (adendo), L-010 |
