---
id: TCK-0014
title: Implementar o validador do contrato de conteúdo
type: feature
status: done
owner: qa-validator
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0002, TCK-0009, ADR-0003]
---

# TCK-0014 — Implementar o validador do contrato de conteúdo

## Pedido original (verbatim)

> inicie a implementação do projeto

Recorte: **task 4** de `docs/specs/minimum-learning-slice/tasks.md`, roteada como ticket
próprio pelo `task-router` (briefing `.dev-loop/start-implementation/briefings/01-route.md`).

## Requisito refinado

O RF-18 da spec exige que o contrato de `content/` seja validado **na carga**, e diz que
falha silenciosa é defeito. Hoje `scripts/audit-content.sh` confere estrutura e presença de
campos, mas não valida as regras semânticas que a aplicação depende para não renderizar
exercício quebrado — e o acervo vai crescer para dezenas de nós antes de a aplicação existir.

Este ticket entrega o validador **antes** da interface, de propósito: é ele que define, na
prática, o que "conteúdo válido" significa, e é mais barato descobrir um contrato errado agora
do que depois de 30 nós escritos.

## Critérios de aceite

- [x] 1. Existe um validador executável que recebe um nó de `content/` (ou o acervo inteiro) e
      sai com código de erro quando o contrato é violado, listando **todas** as violações
      encontradas — não só a primeira.
- [x] 2. CA-13 e CA-14 da spec passam, exercitados por fixtures.
- [x] 3. Fixtures **inválidas** que devem falhar de forma visível e nomeada, cada uma com
      teste: `multiple-choice` sem nenhuma opção `correct: true`; `multiple-choice` com mais
      de uma; `numeric` com `tolerance` negativa; chave de idioma faltando num campo
      localizado; `nodeId` divergente do caminho do nó.
- [x] 4. Fixtures **válidas** passam sem falso positivo — incluindo `qe-003` com
      `tolerance: 0` (zero é válido; ausente ou negativo não é) e `prerequisites: []` vazio.
- [x] 5. A mensagem de erro identifica arquivo, item e regra violada em texto acionável —
      "conteúdo inválido" sem localização é reprovação.
- [x] 6. O nó piloto real (`high-school/algebra/quadratic-equations`) passa no validador sem
      alteração de `content/` — se não passar, o defeito é do validador ou uma descoberta
      sobre o acervo, e vai para o log antes de qualquer correção.
- [x] 7. Zero dependência nova de terceiros; `ADR-0003` não decidiu ferramenta de teste, então
      escolha a mais simples que o repositório já suporta e **justifique a escolha no log**.
- [x] 8. Nada em `content/` é alterado. Nenhuma decisão de framework de aplicação é embutida
      no validador — ele precisa rodar fora da aplicação (pipeline e linha de comando).
- [x] 9. `bash scripts/audit-content.sh` e `bash scripts/audit-ai-surface.sh` sem erros.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — a validação de paridade é parte do contrato
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável (sem interface)
- [ ] Funciona offline / PWA · [x] não aplicável
- [x] Custo zero mantido — sem dependência paga, sem serviço externo
- [x] Privacidade — o validador não lê nem emite dado de usuário
- [x] URLs de `content/` preservadas — validar `nodeId` × caminho reforça isso
- [ ] Correção matemática verificada · [x] não aplicável (valida contrato, não matemática)

## Fora de escopo

- Interface, renderização, KaTeX — tasks 5–8.
- Integrar o validador ao build/CI — é a task 11.
- Redesenhar o schema de `references.json` — é o **TCK-0009**, ticket próprio. Se este
  trabalho revelar necessidade de campo novo, **registre no log** e não altere o schema.
- Alterar `content/`, a spec ou qualquer ADR.

## Contexto e referências

- Spec: `docs/specs/minimum-learning-slice/spec.md` (RF-18, CA-13, CA-14)
- Task de origem: `tasks.md`, linha 4
- Contrato real: `content/high-school/algebra/quadratic-equations/{meta,exercises}.json`
  (ids `qe-001`…`qe-005`)
- Schema documentado: `docs/content/exercise-schema.md`
- Auditoria existente, a não duplicar: `scripts/audit-content.py`
- Contexto da área: `memory/context/backend.md`

## Perguntas em aberto

- Nenhuma. Se o contrato documentado divergir do arquivo real, isso é achado para o log e
  handoff ao `tech-lead` — não corrija `content/` nem `docs/` por conta própria.

## Resultado final


**`done` em 2026-08-01 pelo `qa-validator#8`** — 9/9 critérios com evidência reproduzida
(log `[010]`). Ambiente: commit `5d1e2b6`, Python 3.12.3, bash 5.2.21, Linux x86_64. Sem
preview: o artefato é executável de linha de comando.

Entregue: `scripts/validate-content.py` (portão de carga do RF-18, stdlib pura),
`scripts/validate-content.sh` (invólucro) e `scripts/validate-content-test.sh` (**118**
asserções, contadas por fora do script, verdes em 4 ambientes — inclusive um `env -i` com
`LC_ALL=POSIX PYTHONUTF8=0` montado na validação). Nó piloto real passa (`exit 0`) e
`content/` está intocado (hash `dad502b1…` idêntico antes e depois; `git status --porcelain
content/` vazio). Zero dependência de terceiros, provado por AST. Critério 1 comprovado com
**21 violações de 21 regras distintas numa só execução**.

Sete falsos negativos foram encontrados nas fixtures de burla do QA — todos **fora** do RF-18
enumerado e dos critérios 1–9, nenhum invertendo um veredito de regra contratada, e em nenhum
deles o `audit-content.py` é o mais estrito. Viraram dívidas D-1…D-8 no log `[010]`; D-1
(inteiro ≥ 10^309 derruba o validador com traceback e vira `exit 120` com canal quebrado),
D-2 (campo localizado com espaço de largura zero atravessa o portão bilíngue) e D-5
(`exercises.json` com conteúdo `null` passa como "Contrato íntegro") são as que devem ser
resolvidas antes do primeiro lote grande de conteúdo — o `prebuild` do TCK-0015 já chama este
validador.

## Pendências entregues ao `tech-lead` (não bloquearam o `done`)

1. **Ticket próprio para `scripts/audit-content.py`.** Quatro instâncias reproduzidas em cópia
   isolada: `"correct": "false"` (texto) na única alternativa de gabarito, `title.en-US: 5`,
   `title.en-US: None` e `true-false` com duas corretas — as quatro com `exit 0 · 0 erros` no
   auditor e `exit 1` no validador. Hoje é possível ter exercício com gabarito errado passando
   na auditoria em silêncio.
2. **Natureza da `tolerance` (absoluta × relativa).** Decisão de contrato **necessária antes
   das tasks 5–8**, onde a correção de resposta a torna observável. O validador não decide:
   exige só número finito ≥ 0, regra idêntica nas duas leituras.
3. **`docs/content/exercise-schema.md` alcançar as regras novas** (`ITEMS-EMPTY`,
   `ITEM-ID-DUPLICATE`, `JSON-DUPLICATE-KEY`, `version`, `unit: null`) e resolver a assimetria
   do `ITEMS-EMPTY` (nó sem `exercises.json` passa; com `items: []` reprova; com `null` passa
   de novo) — trabalho de `docs-writer` pós-`done`.
