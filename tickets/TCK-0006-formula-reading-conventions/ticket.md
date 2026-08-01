---
id: TCK-0006
title: Registrar as convenções de leitura de fórmula e decidir o escopo inline da §9.2
type: docs
status: triaged
owner: docs-writer
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0005, TCK-0007]
---

# TCK-0006 — Registrar as convenções de leitura de fórmula e decidir o escopo inline da §9.2

## Pedido original (verbatim)

> `a11y-ux-reviewer` `[008]` + `i18n-steward` `[007]`: registrar em
> `docs/content/accessibility.md` a tabela de convenções de leitura de fórmula (a11y
> entregou pronta em `[008]` §6) e, no glossário de `docs/content/i18n.md`, a linha
> `subscrito (índice) | subscript` com nota de desambiguação (em pt-BR, "índice" também
> nomeia o índice do radical). **Obrigatório antes do próximo nó** — o piloto é o modelo.

— `tickets/TCK-0005-pilot-node-math-accessibility/log.md` `[010]`, pendência 5.

> **`\dfrac` inline no Resumo** (menor). Linhas 143–144 (pt-BR) / 140–141 (en-US): frações
> em modo display dentro de bullets, sem leitura. `AGENTS.md` §9.2 fala em fórmula em
> display (`$$…$$`), então formalmente não são exigidas — mas carregam o mesmo risco de
> agrupamento. Avaliar se a regra deve cobrir `\dfrac` inline.

— `tickets/TCK-0005-pilot-node-math-accessibility/log.md` `[008]` §7.3; o `qa-validator#3`
classificou em `[011]` como pendência que "não condiciona `draft`; condiciona a **regra**".

## Requisito refinado

Quem sofre: (a) o próximo autor de nó, que hoje só tem como referência a prática do nó
piloto e o log de um ticket `done` — convenção não escrita se multiplica divergente; (b) o
estudante que usa leitor de tela, que recebe leituras inconsistentes entre nós; (c) o
revisor, que hoje decide caso a caso se uma fórmula inline precisa de leitura.

Resultado esperado: as convenções que o TCK-0005 fixou **na prática** viram norma escrita e
citável, e a fronteira display × inline da `AGENTS.md` §9.2 deixa de ser ambígua — com um
critério que um revisor aplica mecanicamente, não por gosto.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. `docs/content/accessibility.md` contém uma tabela de convenções de leitura com as
      **nove** construções de `TCK-0005/log.md` `[008]` §6 (subscrito; índice de radical;
      fração de numerador composto; fração de numerador de um token; parênteses; `\cdot` ×
      justaposição; `\Longrightarrow`; relação encadeada `= 1 > 0`; números por extenso),
      cada uma com coluna **pt-BR** e coluna **en-US** preenchidas. Falha se qualquer uma
      das nove faltar ou vier com uma coluna vazia.
- [ ] 2. A regra de fração está enunciada como critério **operacional**, não como exemplo:
      numerador com mais de um token → "tudo dividido por" / "all divided by"; numerador de
      um token → "dividido por" / "divided by". O documento traz um exemplo de cada caso.
      Falha se um revisor precisar consultar o autor para decidir qual usar.
- [ ] 3. O glossário de `docs/content/i18n.md` ganha a linha `subscrito (índice) |
      subscript |` com nota de desambiguação citando o índice do radical (`\sqrt[n]{a}`,
      *root index*). `grep -n 'subscript' docs/content/i18n.md` retorna a linha dentro da
      tabela do glossário, com as três colunas preenchidas.
- [ ] 4. A fronteira display × inline está decidida e escrita: o documento enuncia **quando**
      uma fórmula inline exige leitura textual, por um critério verificável por inspeção
      (p. ex. "fração, radical, expoente ou índice cujo sentido dependa de agrupamento"), e
      declara o que **não** exige. Falha se a regra final for "avaliar caso a caso" sem
      critério, ou se depender de julgamento sobre a intenção do autor.
- [ ] 5. `AGENTS.md` §9.2 remete à regra de (4) — o texto canônico deixa de sugerir que só
      `$$…$$` está coberto. `grep -n "inline" AGENTS.md docs/content/accessibility.md`
      mostra a regra nos dois pontos, sem contradição entre eles.
- [ ] 6. O checklist de `published` em `docs/content/content-standards.md` reflete a decisão
      de (4): a linha "Toda equação em display tem descrição textual" passa a cobrir também
      o caso inline decidido, ou ganha linha própria. Falha se o checklist ficar mais frouxo
      que a norma.
- [ ] 7. O log lista, **sem executar**, as ocorrências do nó piloto atingidas pela decisão
      de (4) — `theory.pt-BR.md:143-144` / `theory.en-US.md:140-141` e as 10 ocorrências de
      `\frac` em `exercises.json` — com o veredito por ocorrência (exige leitura / não
      exige) para o TCK-0007 aplicar. Falha se a lista vier sem veredito item a item.
- [ ] 8. Rastreabilidade: cada convenção registrada cita a origem (`TCK-0005` `[008]` §6 /
      `[007]`) e a data (2026-08-01), como manda `docs/DOC-STANDARDS.md` para conhecimento
      derivado de decisão anterior.
- [ ] 9. `python3 scripts/sync-ai-adapters.py --check` → exit 0;
      `bash scripts/audit-ai-surface.sh` → `Resultado: OK`;
      `bash scripts/audit-content.sh` → `0 erros · 0 avisos`, exit 0 (códigos capturados sem
      pipe). Se `AGENTS.md` ou `.github/instructions/` forem tocados, os gerados acompanham
      no mesmo commit e nenhum gerado é editado à mão.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — a tabela é, ela própria, o par de convenções pt-BR/en-US
- [x] Acessibilidade WCAG 2.2 AA (inclui matemática acessível) — é o objeto do ticket
- [ ] Funciona offline / PWA · [x] não aplicável (documentação interna)
- [x] Custo zero mantido — só texto em `docs/` e `AGENTS.md`
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [ ] URLs de `content/` preservadas · [x] não aplicável — `content/` não é tocado
- [ ] Correção matemática verificada · [x] não aplicável — nenhuma afirmação matemática
      nova; as convenções descrevem leitura de notação, não resultados

## Fora de escopo

- Editar `content/` — toda aplicação das convenções ao nó piloto é o **TCK-0007**.
- Parte 2 do `/a11y-audit` (leitor de tela real, foco, contraste, zoom 200%): não há
  aplicação para exercitar.
- Duplicação fórmula + descrição no áudio quando houver render (MathML do KaTeX): depende de
  decisão de implementação (`docs/specs/minimum-learning-slice/plan.md:134`), não desta norma.
- Criar ADR: a decisão de (4) **refina** uma regra existente da §9.2; se durante a execução
  ficar claro que ela muda o pilar (custo de produção de todo nó), escalar ao `tech-lead`
  para abrir ADR em vez de decidir dentro deste ticket.

## Contexto e referências

- Origem: `tickets/TCK-0005-pilot-node-math-accessibility/log.md` `[007]`, `[008]` §6 e §7.3,
  `[010]` pendências 4 e 5, `[011]` pendência 5.
- ADRs aplicáveis: `ADR-0002` (bilinguismo, paridade obrigatória); `ADR-0001` (taxonomia).
- Arquivos-alvo prováveis: `docs/content/accessibility.md`, `docs/content/i18n.md`,
  `docs/content/content-standards.md`, `AGENTS.md` §9.2 e os gerados por
  `scripts/sync-ai-adapters.py`.
- Lições relevantes: `L-012` (descrição de fórmula se confere por **ordem**, não por
  contagem — a auditoria automática não a verifica); `L-001` (bilinguismo não é etapa
  posterior); `L-010` (mudar regra exige atualizar tudo que os agentes leem).

## Perguntas em aberto

- Nenhuma que bloqueie. A decisão de (4) é normativa e cabe ao executor propor com
  argumento; divergência entre `a11y-ux-reviewer` e `docs-writer` volta ao `tech-lead`.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
