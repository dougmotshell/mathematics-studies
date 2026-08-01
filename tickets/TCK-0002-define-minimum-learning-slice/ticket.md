---
id: TCK-0002
title: Definir a primeira fatia de aprendizagem
type: docs
status: done
owner: tech-lead
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [ADR-0003]
---

# TCK-0002 — Definir a primeira fatia de aprendizagem

## Pedido original (verbatim)

> .agents/workflows/dev-loop.md  analise as docs e inicia a implementação, crie um ticket e faça o trigger para acionar o primeiro agent e iniciar o loop de desenvolvimento

## Requisito refinado

Preparar a primeira fatia implementável do produto — navegar um nó bilíngue de conteúdo e
responder um exercício — por meio de uma spec aprovada e um plano executável, respeitando o
contrato de conteúdo existente e sem assumir a stack enquanto `ADR-0003` estiver `proposed`.

## Critérios de aceite

- [x] 1. Existe `docs/specs/minimum-learning-slice/spec.md` com objetivo, escopo, usuários,
      requisitos funcionais e não funcionais, estados principais e critérios verificáveis.
- [x] 2. A spec exige paridade pt-BR/en-US, KaTeX acessível, operação offline do conteúdo
      visitado, custo zero e preservação dos slugs de `content/`.
- [x] 3. Existe `docs/specs/minimum-learning-slice/plan.md` com abordagem independente de
      framework, dependências, riscos e decisões que dependem do aceite do `ADR-0003`.
- [x] 4. Existe `docs/specs/minimum-learning-slice/tasks.md` com tarefas executáveis e ordem
      de handoff para implementação, revisão e validação.
- [x] 5. A spec foi revisada e marcada `approved` somente com evidência de que não bloqueia
      a escolha da stack nem introduz coleta de dados sem ADR de privacidade.
- [x] 6. `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` continuam
      sem erros.

### Requisitos transversais

- [x] Bilinguismo pt-BR + en-US
- [x] Acessibilidade WCAG 2.2 AA (inclui matemática acessível)
- [x] Funciona offline / PWA
- [x] Custo zero mantido
- [x] Privacidade e dados de menores (LGPD/COPPA)
- [x] URLs de `content/` preservadas
- [ ] Correção matemática verificada — [x] não aplicável nesta etapa de especificação

## Fora de escopo

- Escolher ou aceitar a stack do produto; isso pertence ao `ADR-0003`.
- Implementar a aplicação, banco, autenticação, sincronização ou deploy.
- Coletar dados de usuário ou criar uma conta.
- Alterar o nó piloto, seus slugs, teoria, exercícios ou referências.

## Contexto e referências

- Spec: `docs/specs/minimum-learning-slice/`
- ADR aplicável: `docs/adr/ADR-0003-platform-stack.md` (proposed)
- Contrato de conteúdo: `content/high-school/algebra/quadratic-equations/`
- Padrões: `docs/DOC-STANDARDS.md`, `docs/content/`, `docs/specs/README.md`
- Workflow: `.agents/workflows/dev-loop.md`, `.claude/skills/dev-loop/SKILL.md`
- Contexto: `memory/context/project-context.md`, `memory/context/process.md`
- Lições relevantes: `L-001`, `L-003`, `L-004`

## Perguntas em aberto

- Nenhuma para produzir a spec; o aceite do `ADR-0003` será necessário antes de qualquer
  ticket posterior de implementação da aplicação.

## Resultado final

**Veredito: `done`** — todos os seis critérios atendidos, com evidência própria do
`qa-validator#2` no `log.md` [008] (comando executado ou caminho + linha, por critério).
Cadeia independente: produziu `docs-writer` [006], aprovou `code-reviewer#3` [007], validou
`qa-validator#2` [008].

**O que foi entregue.** A spec da primeira fatia implementável do produto — abrir um nó
bilíngue, ler a teoria com matemática acessível, responder um exercício e receber feedback
diagnóstico —, em três documentos `approved` e sem uma única escolha de stack:

- `docs/specs/minimum-learning-slice/spec.md` — problema, resultado esperado, escopo,
  **RF-1…RF-18**, **RNF-1…RNF-11**, **13 estados de tela**, **CA-1…CA-16** falseáveis,
  transversais, fora de escopo, perguntas em aberto, métricas e `stateDiagram-v2` do ciclo do
  item de exercício.
- `docs/specs/minimum-learning-slice/plan.md` — quatro camadas de comportamento, alternativas
  descartadas, `flowchart` atual × proposta, impacto, **7 riscos**, **3 dependências
  bloqueantes**, **7 decisões devolvidas à implementação** e menor fatia entregável.
- `docs/specs/minimum-learning-slice/tasks.md` — **15 tarefas** com agente, dependência e
  critério de pronto; paralelizáveis marcadas; validação final por CA e pelas duas auditorias.
- `docs/specs/README.md:13` — spec indexada como `approved`.

**Onde estão as evidências.** `tickets/TCK-0002-define-minimum-learning-slice/log.md`, entrada
`[008]`, seção "Evidência por critério" (1–6), mais os dois vereditos de julgamento e a
rastreabilidade dos transversais. Ambiente: commit `d1ca2e5`, branch `main`, artefatos ainda
não commitados. `bash scripts/audit-ai-surface.sh` → `Resultado: OK` (exit 0);
`bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos` (exit 0).

**Dívidas aceitas (não bloqueiam o `done`).**

1. Validação **documental**: este ticket entrega spec, não software — não há aplicação para
   exercitar. Os casos hostis (offline, dois idiomas e separador decimal, teclado, leitor de
   tela, rede lenta, dados vazios) foram validados como *exigência escrita e falseável*; a
   execução real é a **task 14** do `tasks.md`.
2. A spec não **nomeia** que o público inclui menores de idade; o vínculo com LGPD/COPPA só
   aparece em `spec.md:253` e no `ADR-0003`. RNF-7 já proíbe toda coleta identificável, o que é
   mais forte — melhoria de redação, não defeito.
3. `spec.md:277-279` ainda oferece "parâmetro ou domínio separado" para a URL bilíngue,
   variantes já excluídas por `ADR-0003:62-63`. Redação desatualizada em um dia.
4. Dono (`tech-lead`) e prazo (antes da task 3) das perguntas em aberto estão no log `[007]`,
   não no corpo da spec — quem retomar precisa ler os dois.

**Perguntas em aberto herdadas pela spec** (`spec.md:272-280`) — nenhuma bloqueante; todas com
padrão normativo decidido, dono `tech-lead` e prazo "antes da task 3":

1. **Exibir o nó `draft` ao público?** A spec já decide que sim, com rótulo (RF-5, CA-1, CA-16).
   Sem contradição com `docs/content/taxonomy.md:81` nem `ADR-0002:33-36`, que condicionam
   *publicar* — não *exibir* — aos dois idiomas completos; o nó piloto tem os dois. Reverter o
   padrão gera retrabalho na **task 5** (índice), a jusante.
2. **Forma da URL bilíngue.** Reduzida a prefixo × sufixo por `ADR-0003:62-63`; o invariante
   (caminho da taxonomia íntegro) está travado em RF-17/RNF-5.
3. **Rótulo de rascunho também no índice?** Sub-detalhe da pergunta 1; fora dos 13 estados.

**Encaminhado ao `tech-lead` como ticket novo (fora do escopo deste).** Lacuna de
acessibilidade no nó piloto: `theory.pt-BR.md` tem **8 blocos `$$…$$`** (linhas 34, 44, 51, 66,
76, 80, 92, 103) e apenas **3 parágrafos `*Leitura:*`** (linhas 36, 46, 53); `theory.en-US.md`,
8 × 3 `Reading:`. Contraria `AGENTS.md` §9.2 e faria CA-2 falhar por dados. Não corrigido aqui
porque RNF-9 e a seção "Fora de escopo" proíbem tocar `content/` neste ticket. Sugerido para
`content-author` + `a11y-ux-reviewer`, **antes da task 6**.
