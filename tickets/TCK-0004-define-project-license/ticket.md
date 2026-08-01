---
id: TCK-0004
title: Definir e registrar a licença do projeto (conteúdo e código)
type: docs
status: done
owner: qa-validator#5
priority: P1
size: P
created: 2026-08-01
updated: 2026-08-01
related: [ADR-0002, ADR-0005, TCK-0001, TCK-0003]
---

# TCK-0004 — Definir e registrar a licença do projeto (conteúdo e código)

## Pedido original (verbatim)

> faça tudo que for necessário

Decisão do usuário coletada em 2026-08-01 (Douglas Silva):

> **Conteúdo:** CC BY-SA 4.0. **Código:** MIT.

## Requisito refinado

A licença do projeto estava listada como decisão em aberto em
`memory/context/project-context.md` e bloqueia, na prática, tanto a reutilização do acervo
por terceiros quanto a incorporação de material externo — não dá para avaliar
compatibilidade de uma fonte sem saber sob que licença publicamos. O decisor escolheu
**CC BY-SA 4.0** para `content/` e **MIT** para o código. Falta registrar a decisão como ADR
e materializá-la em arquivos de licença e em regra operacional para quem escolhe fontes.

## Critérios de aceite

- [x] 1. Existe `docs/adr/ADR-0005-project-license.md` no padrão do template, com
      `status: accepted`, contexto, alternativas consideradas, decisão e consequências.
- [x] 2. Existe `LICENSE` na raiz com o texto **integral** da MIT (titular: Douglas Silva,
      ano 2026), aplicável ao código.
- [x] 3. Existe `LICENSE-CONTENT` na raiz identificando **CC BY-SA 4.0** para `content/`,
      com a URL canônica da licença e a forma de atribuição esperada.
- [x] 4. O ADR registra explicitamente a consequência de compatibilidade: fontes **CC BY** e
      domínio público podem ser adaptadas; fontes **CC BY-NC** ou **NC-SA** **não** podem
      ser incorporadas ao conteúdo (só citadas como leitura externa).
- [x] 5. A regra de compatibilidade aparece onde o autor de conteúdo a lê:
      `docs/content/content-standards.md` (ou o documento equivalente de fontes) e
      `memory/context/content.md`.
- [x] 6. `README.md` (se existir) e `memory/context/project-context.md` deixam de listar a
      licença como decisão em aberto.
- [x] 7. `bash scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` seguem sem
      erros.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — o `LICENSE-CONTENT` deve ser legível nos dois idiomas
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável
- [ ] Funciona offline / PWA · [x] não aplicável
- [x] Custo zero mantido — licenças gratuitas
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [x] URLs de `content/` preservadas
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Reavaliar as fontes já registradas em `references.json` — isso é o `TCK-0001`.
- Escolher licença para assets de terceiros caso a caso.
- Qualquer alteração em `content/` além do que o critério 5 exigir em `docs/`.

## Contexto e referências

- Template: `docs/adr/adr-template.md`; índice: `docs/adr/README.md`
- Regra de fontes: `AGENTS.md` §9.6 e §9.7, `docs/content/content-standards.md`
- Contexto: `memory/context/content.md`, `memory/context/project-context.md`
- Lição relevante: `L-003` (slug é contrato público — a licença também é contrato público)

## Perguntas em aberto

- Nenhuma. A decisão humana que faltava foi tomada em 2026-08-01.

## Resultado final

**`done` em 2026-08-01, validado por `qa-validator#5`** (log `[011]`). Ambiente da validação:
commit `f96baa9`, branch `main`, working tree compartilhado com TCK-0003 e TCK-0005;
`curl 8.5.0`, `python3`, `node v24.14.1`, `mermaid 11.16.0`. **7/7 critérios atendidos com
evidência reproduzida pelo QA** (nenhuma herdada do produtor ou do revisor), 0 defeitos
bloqueantes, 1 rodada de `REJECT` resolvida (loop 1/3, defeito B1).

Entregue: `docs/adr/ADR-0005-project-license.md` (`accepted`, decisor Douglas Silva,
2026-08-01), `LICENSE` (MIT literal — 169 palavras, zero diferenças contra o texto canônico
SPDX) e `LICENSE-CONTENT` (CC BY-SA 4.0, pt-BR e en-US com paridade 6↔6 seções e URLs
canônicas respondendo 200). A regra de compatibilidade **"NC = leitura, não matéria-prima"**
deixou de morar só no ADR: é imperativa em `AGENTS.md` §9.7 ("regra dura, não preferência"),
em `.github/instructions/{content,core}.instructions.md`, nos agents `content-author` e
`researcher`, em `docs/content/content-standards.md` (com item no checklist de `published`),
em `memory/context/content.md`, no `prompts/bootstrap-session.md`, no `CONTRIBUTING.md` e nos
adapters gerados das 12 ferramentas. Verificado que **nenhum caminho de auto-carregamento
relevante deixa a regra de fora** e que a renumeração §9.6/§9.7/§9.8 **não quebrou nenhuma
das 49 referências cruzadas** existentes.

Consequência dura para o acervo: as três referências do nó piloto (OpenStax ×2 e *Livro
Aberto de Matemática*) são CC BY-NC-SA e passam a ser **apenas leitura externa**.

### Pendências herdadas (não bloqueiam este ticket — encaminhadas ao `tech-lead`)

1. **TCK-0001:** confirmar que nenhum trecho, exemplo, figura ou sequência didática das três
   fontes NC entrou no texto autoral do nó piloto (`theory.pt-BR.md`, `theory.en-US.md`,
   `exercises.json`).
2. **Schema de `references.json`:** não existe campo que distinga fonte **adaptável** de
   **apenas citável**. A regra recém-criada depende de uma distinção que o schema ainda não
   expressa — vale ticket próprio.
3. **Licença do *Livro Aberto de Matemática*:** declaração divergente (página do projeto
   BY-NC-SA × colofão do PDF BY-SA). Esclarecer com IMPA/OBMEP; se for BY-SA, torna-se a
   única fonte pt-BR adaptável conhecida.
4. **Ausência de fonte gratuita em pt-BR compatível** (não-NC): o custo de produção autoral
   sobe; contar com isso no ritmo de produção de conteúdo.
5. **Rodapé da aplicação** deverá exibir as duas licenças com link canônico (`ADR-0005`,
   seção Impacto), quando a aplicação for construída sob o `ADR-0003`.
6. **Dívidas de precisão registradas no `[011]`:** D-1 (razão pela qual **ND** entra em "só
   citável" — não é proibição de redistribuição verbatim, é a declaração uniforme de
   `content/` sob CC BY-SA), D-2 (`Como reverter` do ADR ignora o share-alike de fonte
   externa adaptada), D-3 ("citar" pode ser lido como "transcrever"), D-4 (acrescentar à
   `L-009` a checagem de referências cruzadas quando uma seção do `AGENTS.md` é renumerada).
7. **`README.md:7-10`** descrevia `ADR-0003` como `proposed`: pendência do **TCK-0003**, não
   deste ticket.
