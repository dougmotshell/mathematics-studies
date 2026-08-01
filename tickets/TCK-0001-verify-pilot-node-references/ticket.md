---
id: TCK-0001
title: Verificar as referências externas do nó piloto
type: content
status: done
owner: tech-lead
priority: P2
size: P
created: 2026-08-01
updated: 2026-08-01
related: []
---

# TCK-0001 — Verificar as referências externas do nó piloto

## Pedido original (verbatim)

> (Ticket aberto pelo próprio setup do repositório, em 2026-08-01, para registrar uma
> pendência identificada durante a criação do nó piloto.)

## Requisito refinado

O nó `content/high-school/algebra/quadratic-equations` foi criado com duas referências ao
OpenStax em `references.json`. As URLs e as licenças foram informadas **de memória**, sem
acesso à web no momento da criação — ou seja, não foram verificadas na própria página, como
exige o AGENTS.md §9.6.

Enquanto isso não for feito, o nó não pode sair de `status: "draft"`.

## Critérios de aceite

- [x] 1. Cada URL de `references.json` foi acessada e retorna a página esperada (sem 404 nem
      redirecionamento para outra obra).
- [x] 2. A licença registrada corresponde à licença declarada **na própria página** da fonte.
- [x] 3. O campo `covers` descreve o que a fonte realmente cobre, conferido no material.
- [x] 4. Foi adicionada ao menos **uma referência gratuita em português** (o acervo pt-BR é o
      mais escasso — ver `/research-sweep`), com autor, ano, URL, idioma e licença.
- [x] 5. `bash scripts/audit-content.sh` continua sem erros.

### Requisitos transversais

- [x] Bilinguismo pt-BR + en-US — referências devem cobrir os dois idiomas
- [x] não aplicável: Acessibilidade / Offline / Correção matemática (artefato é
  arquivo de dados, sem UI); **URLs verificadas** — critério 1
- [x] Custo zero mantido — apenas fontes gratuitas

## Fora de escopo

- Alterar a teoria ou os exercícios do nó.
- Publicar o nó (`status: "published"`) — depende também de revisão de `math-reviewer` e
  `i18n-steward`.

## Contexto e referências

- Nó: `content/high-school/algebra/quadratic-equations/references.json`
- Regra: `AGENTS.md` §9.6 e `docs/content/content-standards.md`
- Agente sugerido: `researcher` (com `/research-sweep` para o material em pt-BR)
- Contexto da área: `memory/context/content.md`

## Perguntas em aberto

- Nenhuma.

## Resultado final

**Validado e aprovado pelo `qa-validator` em 2026-08-01 — 5/5 critérios com evidência
própria, 0 defeitos.** Evidência completa, comando a comando, em
`tickets/TCK-0001-verify-pilot-node-references/log.md`, entrada `[007]`.

### O que foi entregue

Único arquivo alterado: `content/high-school/algebra/quadratic-equations/references.json`
(2 → 3 itens). Teoria, exercícios e `meta.json` intocados — o nó permanece `status: "draft"`
(sair de draft depende de `math-reviewer` e `i18n-steward`, fora do escopo).

1. **Duas licenças corrigidas** — as duas fontes OpenStax estavam registradas como
   `CC BY 4.0`, informação dada de memória. A licença declarada nas próprias páginas é
   `CC BY-NC-SA 4.0` (bloco `"license":{"url":"…/licenses/by-nc-sa/4.0/"…}` em ambas). Esse
   era o defeito de origem do ticket, e ele era real. Consequência prática registrada em
   `memory/context/content.md`: fonte NC-SA é **leitura, não matéria-prima** — pode ser
   citada, não incorporada nem traduzida para dentro do nó.
2. **Três `covers` reescritos** contra o sumário real de cada material.
3. **Uma referência gratuita em pt-BR adicionada** — *Livro Aberto de Matemática*, cap.
   "Função Quadrática" (Luiz Amorim e Bruno Vianna / Colégio Pedro II; IMPA-OS, realização
   OBMEP; 2021, v1.1), com licença CC BY-NC-SA verificada na página oficial do projeto e
   autoria lida no colofão do PDF. O acervo do nó passa a cobrir os dois idiomas do produto
   (2 en-US + 1 pt-BR), com custo zero mantido.
4. **`bash scripts/audit-content.sh` verde** — `1 nós · 0 erros · 0 avisos`.

### Onde estão as evidências

| Critério | Evidência (log `[007]`) |
|---|---|
| 1. URLs | `curl -w "%{http_code} %{num_redirects}"` → `200 0` nos 3 itens + `<title>` de cada página + `publish_date` conferindo o campo `year` |
| 2. Licenças | `grep '"license":{…}'` nas duas páginas OpenStax → `by-nc-sa/4.0`; item pt-BR: texto de `livroaberto.uniriotec.br/sobre/` + selo do colofão renderizado com `pdftoppm` |
| 3. `covers` | contagem de ocorrências dos termos alegados no texto extraído de cada página; PDF localizado com varredura página a página (`pdftotext -f 51 -l 53`, páginas impressas 47-49) |
| 4. pt-BR | `pdfinfo` (85 páginas) + colofão via `pdftotext -f 3 -l 3` (autor, ano/versão, editora, realização) + download anônimo sem paywall |
| 5. Auditoria | `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`, `exit=0` |

Toda a evidência foi **reproduzida** pelo validador, não copiada do produtor (`researcher`,
`[004]`) nem do revisor (`code-reviewer`, `[006]`). Ambiente: commit `d1ca2e5`, `curl 8.5.0`,
poppler (`pdftotext`/`pdfinfo`/`pdftoppm`). Sem commit e sem push.

### Dívidas aceitas (não bloqueiam; sugerido ticket único de schema)

- **D-1** — `covers` carrega rastro de auditoria e, no item 1, duplica a informação de
  licença (duas fontes de verdade para o mesmo fato).
- **D-2** — `license` do item 3 mistura identificador e nota longa; separar em
  `license` + `licenseNotes`.
- **D-3** — URL pt-BR aponta para `blob/master/`, que se move com a branch; usar permalink
  por SHA. Alternativas oficiais conferidas e fora do ar (`403` e falha de TLS).

Argumentação de por que nenhuma delas reprova (em especial D-1, que toca o critério 3):
log `[007]`, seção "Ponto de julgamento".
