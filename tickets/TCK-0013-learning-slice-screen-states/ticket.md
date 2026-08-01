---
id: TCK-0013
title: Desenhar os estados de tela e o fluxo da fatia mínima
type: feature
status: done
owner: tech-lead
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0002, ADR-0002, ADR-0003]
---

# TCK-0013 — Desenhar os estados de tela e o fluxo da fatia mínima

## Pedido original (verbatim)

> inicie a implementação do projeto

Recorte: **task 3** de `docs/specs/minimum-learning-slice/tasks.md`, roteada como ticket
próprio pelo `task-router` (briefing `.dev-loop/start-implementation/briefings/01-route.md`).

## Requisito refinado

A spec `minimum-learning-slice` está `approved` e descreve **13 estados de tela** numa tabela,
mas nenhum deles foi desenhado. Sem isso, o `frontend-developer` das tasks 5–8 decidiria
layout, texto de interface e ordem de foco por conta própria, no meio da implementação — que
é exatamente onde acessibilidade e paridade bilíngue costumam se perder.

O artefato desta task é **desenho e texto**, não código: o que aparece em cada estado, com que
palavras nos dois idiomas, em que ordem o teclado percorre, e o que é anunciado a quem usa
leitor de tela.

## Critérios de aceite

- [x] 1. Existe um artefato por estado da tabela de estados de `spec.md` — os 13, sem
      omissão — identificando cada um pelo nome usado na spec.
- [x] 2. Cada estado traz o **texto de interface nos dois idiomas** (pt-BR e en-US), em
      paridade, sem fallback e sem string inventada que a spec não preveja.
- [x] 3. Cada estado define a **ordem de foco por teclado** e qual elemento recebe foco ao
      entrar nele.
- [x] 4. Estados que mudam sem navegação (resposta correta, incorreta, dica revelada, perda
      de rede) declaram **o que é anunciado por região viva** — resultado não pode ser
      comunicado só por cor ou só por posição.
- [x] 5. O fluxo `índice → nó → exercício` está desenhado como diagrama Mermaid, com os
      pontos de entrada e saída de cada estado (`docs/DOC-STANDARDS.md`).
- [x] 6. O **rótulo de rascunho** (nó com `status: "draft"`), o **alternador de idioma** e os
      **dois estados de rede** aparecem explicitamente, com o texto que os acompanha.
- [x] 7. Nada no desenho fixa framework, biblioteca ou componente concreto — `ADR-0003`
      decidiu site estático com ilhas, não a camada de UI.
- [x] 8. Nenhum estado introduz coleta de dado, conta, login ou identificador — RNF-7 da spec
      e ausência de ADR de privacidade.
- [x] 9. `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` sem erros.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — é critério 2
- [x] Acessibilidade WCAG 2.2 AA — critérios 3 e 4
- [x] Funciona offline / PWA — os dois estados de rede
- [x] Custo zero mantido
- [x] Privacidade e dados de menores (LGPD/COPPA) — critério 8
- [x] URLs de `content/` preservadas
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Implementar qualquer tela — isto é desenho; a implementação são as tasks 5–8.
- Escolher framework, biblioteca de componentes ou sistema de build.
- Alterar `content/`, a spec ou qualquer ADR.
- Progresso persistente, trilhas, busca ou conta — fora da fatia mínima.

## Contexto e referências

- Spec: `docs/specs/minimum-learning-slice/spec.md` (tabela de estados, RF, RNF, CA-1…CA-16)
- Plano: `docs/specs/minimum-learning-slice/plan.md`
- Task de origem: `tasks.md`, linha 3
- Contrato de dados real: `content/high-school/algebra/quadratic-equations/`
- Padrões: `docs/content/accessibility.md`, `docs/content/i18n.md`, `docs/DOC-STANDARDS.md`
- Decisão de stack: `docs/adr/ADR-0003-platform-stack.md`

## Perguntas em aberto

- A spec herdou três decisões humanas adiadas: exibir nó com `status: draft`, forma da URL
  bilíngue e rótulo de rascunho no índice. **Desenhe as alternativas** em vez de escolher
  sozinho; a decisão é do usuário e deve subir ao `tech-lead` no handoff.

## Resultado final

**`done` em 2026-08-01 pelo `qa-validator#7`** — 9/9 critérios com evidência própria, 2 loops de
devolução (`[006]` code-reviewer, `[010]` qa-validator), 0 defeitos abertos. Artefato:
`docs/design/minimum-learning-slice/screen-states.md` (893 linhas) + `README.md` do diretório +
1 linha em `docs/README.md`. Commit da validação: `5d1e2b6`.

**Evidência por critério** (reproduzida pelo QA, não herdada): 13/13 estados cruzados com a
tabela de `spec.md`; 68 chaves bilíngues com 0 vazias, 0 duplicadas, 0 tokens divergentes;
13/13 com ordem de foco e elemento de entrada; 13/13 com região viva, com texto declarado em
E6/E7/E8/E12; Mermaid validado no parser real (mermaid@11 + jsdom); rascunho, alternador e os
dois estados de rede presentes com texto; busca negativa de ~30 termos de stack = 0 ocorrências
afirmativas; nenhuma coleta de dado; `audit-ai-surface.sh` e `audit-content.sh` **exit 0**.

**O defeito que este ticket matou.** O loop 2 encontrou uma regra de entrada numérica que
marcava **certa uma resposta errada**: §9 aplicava o teste de ambiguidade só ao en-US, e em
pt-BR o ponto — que é separador de **milhar** (`docs/content/i18n.md:20`) — era lido como
decimal, fazendo `3.000` acertar `qe-003` (`answer: 3`, `tolerance: 0`) e `3.500` acertar
`qe-005`. A correção reescreveu §9 como pergunta respondida nos **dois** idiomas, com regra
única e gatilho inspecionável na string. Simulação final do QA: **26 vetores × 2 idiomas × 2
itens reais, zero falsos positivos**, CA-6 e CA-7 preservados. Registro: adendo à `L-022`
(família `L-013` ⇄ `L-021` ⇄ `L-022`).

**Decisões humanas ainda abertas — do usuário, via `tech-lead`:**

- **(a) Exibir o nó com `status: "draft"`?** A1 exibir com rótulo (é o que RF-5/CA-16 assumem)
  × A2 esconder do índice × A3 confirmação antes de entrar. **A2 torna RF-1/CA-1
  insatisfazíveis hoje** — o acervo tem 1 nó e ele está `draft` — e exigiria emenda na spec
  aprovada. Bloqueia a task 5 (índice) se for decidida contra A1.
- **(c) Rótulo de rascunho também no índice?** C1 por nó × C2 só na página × C3 aviso único no
  topo. Nenhuma exige texto novo; C1 e C3 são indistinguíveis hoje e divergem no primeiro nó
  `published`. O cartão está descrito nos dois pontos (§4 `I3` e §5) apenas no mínimo de RF-1,
  com remissão explícita — **não** é escolha de C2.
- (b) forma da URL: **fechada** pelo usuário no `TCK-0011` (prefixo minúsculo no caminho) e já
  aplicada; o registro (`ADR-0007`) segue `proposed`.

**Dívidas aceitas (nenhuma bloqueia as tasks 5–8):**

| ID | Dívida | Gatilho que a transforma em defeito |
|---|---|---|
| D-3 | E1 é silencioso na conclusão da carga (`:288-293`) | `/a11y-audit` da task 5: se quem ouviu "carregando" não perceber o fim, entra uma linha de estado curta |
| D-5 | Canal de anúncio da **recusa de formato** não atribuído — §7.1 `:474` associa `exercise.invalid-number` ao campo com o foco no controle acionado | `/a11y-audit` da task 7: se a mensagem só existir no campo, o leitor de tela fica **em silêncio** ao recusar |
| D-6 | A regra de §9 recusa espaço sem distinguir borda de interior (`" 3,5"` recusa como `3 000`); `+3.5` e `3.5e0` idem | Primeiro relato de "digitei certo e não aceitou"; direção é segura (recusa, não nota errada) |
| — | Catálogo de `tag.*`/`skill.*` vive na interface (`:407-410`) | RNF-9 proíbe tocar em `content/` nesta fatia — vira ticket de conteúdo/schema |

**Pendências de outras áreas:** `AGENTS.md` §4 sem a linha de `docs/design/` (escopo do
`tech-lead`; **não** exige `sync-ai-adapters.py` — `AGENTS.md` não é entrada do gerador,
`scripts/sync-ai-adapters.py:46-49`) e aceite do `ADR-0007`.

**Limites desta validação:** documental. Não existe aplicação (`src/`, `package.json`
inexistentes), então offline real, zoom 200%, tema claro/escuro, teclado e leitor de tela
**não foram executados** — são o roteiro de `/a11y-audit` e `/pwa-audit` nas tasks 5–8, e os
parágrafos **Foco** e **Região viva** de cada estado são o que esse roteiro vai conferir.
