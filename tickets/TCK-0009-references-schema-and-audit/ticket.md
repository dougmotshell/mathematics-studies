---
id: TCK-0009
title: Definir o schema de references.json e validá-lo no audit-content
type: feature
status: triaged
owner: backend-developer
priority: P2
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0001, TCK-0004, TCK-0010]
---

# TCK-0009 — Definir o schema de references.json e validá-lo no audit-content

## Pedido original (verbatim)

> - **D-1** — `references.json`: `covers` dos 3 itens carrega rastro de auditoria e, no item 1,
>   duplica a informação de licença. Mover proveniência para o log e deixar `covers` só com
>   cobertura.
> - **D-2** — `license` do item 3 mistura identificador e nota; separar em `license` +
>   `licenseNotes` quando houver schema.
> - **D-3** — URL pt-BR em `blob/master/` se move com a branch; trocar por permalink com SHA de
>   commit e reconferir periodicamente.
> - **ACTION sugerida ao `tech-lead`:** as três se resolvem de uma vez em **um ticket de schema
>   para `references.json`** (campos obrigatórios, `covers` sem proveniência, `licenseNotes`,
>   política de permalink) + a validação correspondente em `audit-content.py`.

— `tickets/TCK-0001-verify-pilot-node-references/log.md` `[007]`.

> **TCK-0001:** confirmar que nenhum trecho das três fontes NC do nó piloto foi incorporado
> ao texto autoral, e avaliar um campo em `references.json` que distinga fonte **adaptável**
> de **apenas citável** — hoje o schema não expressa isso, e a regra passou a depender dele.

— `tickets/TCK-0004-define-project-license/log.md` `[009]`, pendência 1 (mesma pendência em
`[006]` item 1).

> `check_references` só valida **presença** de `author/year/url/language/license`; não valida
> `covers`, não faz requisição de rede e não checa formato de licença. Ou seja, o critério 5
> é necessário, não suficiente.

— `tickets/TCK-0001-verify-pilot-node-references/log.md` `[007]`, critério 5.

## Requisito refinado

Quem sofre: (a) o `content-author` e o `researcher` do próximo nó — a regra `AGENTS.md` §9.7
("NC = leitura, não matéria-prima") virou **normativa** no TCK-0004, mas o arquivo que carrega
as fontes não expressa se uma delas pode ser adaptada; a regra depende de alguém reler a
licença toda vez; (b) o `qa-validator`, que hoje recebe `audit-content.sh` verde sem que isso
diga nada sobre licença ou cobertura — "auditoria verde não significa fonte verificada";
(c) a manutenção: `covers` duplica a licença do item 1, criando duas fontes de verdade para o
mesmo fato — exatamente a classe de erro que originou o TCK-0001.

Resultado esperado: `references.json` tem contrato escrito, campos legíveis por máquina e um
validador determinístico que **falha** quando o contrato é violado.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. Existe o contrato escrito (`docs/content/references-schema.md`, nos moldes de
      `docs/content/exercise-schema.md`), definindo por campo: obrigatoriedade, tipo, formato
      e um exemplo — `author`, `year`, `title`, `url`, `language`, `license`, `licenseNotes`,
      `covers`, `usage`. Falha se algum campo aparecer sem contrato ou sem exemplo.
- [ ] 2. `usage` tem **lista fechada** (`adaptable` | `citable-only`) e a regra de derivação a
      partir da licença está escrita e é coerente com o fluxograma de
      `docs/content/content-standards.md` (NC ou ND → `citable-only`; CC BY, CC BY-SA, CC0 ou
      domínio público → `adaptable`). Teste: aplicar a regra às 3 fontes do nó piloto devolve
      `citable-only` nas três, e o log mostra a derivação item a item.
- [ ] 3. `covers` contém **só cobertura**: nenhuma proveniência ("Verificado em …") e nenhuma
      informação de licença. Teste:
      `jq -r '.items[].covers' content/**/references.json | grep -inE "verificad|licen|CC BY|BY-NC|colofão"`
      → **vazio**. A proveniência que estiver no campo migra para o log deste ticket (não se
      perde).
- [ ] 4. `license` é legível por máquina: casa com a lista fechada de identificadores
      declarada em (1) — teste com regex sobre `jq -r '.items[].license'`, todas as 3 linhas
      casando. A nota longa do item pt-BR (divergência BY-NC-SA × BY-SA, versão não declarada)
      vive em `licenseNotes`, íntegra. Falha se qualquer informação da nota se perder.
- [ ] 5. A URL do item pt-BR é permalink por **SHA de commit**
      (`github.com/livro-aberto/…/blob/<sha40>/…`), com evidência de acesso no log
      (`http_code=200`, `num_redirects`, tamanho do PDF) e o SHA registrado; a política de
      permalink está escrita em (1). Falha se a URL continuar em `blob/master/`.
- [ ] 6. `scripts/audit-content.py` valida o contrato: campos obrigatórios, `usage` na lista
      fechada, `license` no formato fechado, `covers` sem proveniência nem licença, `url`
      absoluta. **Teste negativo obrigatório, um por regra:** violando cada regra numa cópia
      do arquivo, o auditor **falha** com mensagem que nomeia o item e o campo — as saídas vão
      no log. Falha se alguma regra passar despercebida (validador que só concorda não vale).
- [ ] 7. `bash scripts/audit-content.sh` no estado correto → `0 erros · 0 avisos`, exit 0
      (capturado sem pipe), e o log declara o alcance: o auditor **não** faz requisição de
      rede, logo não prova que a URL está viva.
- [ ] 8. Escopo: `git diff --name-status -- content/` mostra apenas
      `M .../quadratic-equations/references.json`. Teoria, exercícios e `meta.json`
      intocados; `status` segue `draft`; nenhum slug renomeado.
- [ ] 9. Restrição do `ADR-0003:157-174` preservada: um leitor escrito do zero, sem a
      aplicação, continua conseguindo ler `references.json`. Teste: `python3 -c` com `json`
      puro carrega o arquivo e imprime, por item, `usage`, `license` e `url` — sem depender de
      biblioteca, frontmatter proprietário ou transformação de build.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — o acervo do nó mantém fonte nos dois idiomas (`language`
      continua obrigatório); nomes de campo em en-US (AGENTS.md §2a)
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável — arquivo de dados, sem UI hoje
- [ ] Funciona offline / PWA · [x] não aplicável — nenhum consumidor em runtime ainda
- [x] Custo zero mantido — fontes gratuitas, verificação por acesso público anônimo
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [x] URLs de `content/` preservadas — critério 8 (a URL que muda é a da **fonte externa**,
      não o caminho público do nó)
- [ ] Correção matemática verificada · [x] não aplicável — nenhuma afirmação matemática

## Fora de escopo

- Reverificar o conteúdo das fontes: já foi feito e aprovado no TCK-0001 (URLs, licenças e
  cada alegação de `covers` conferidas). Aqui só muda a **forma**.
- Esclarecer a divergência de licença do *Livro Aberto* — é o **TCK-0010**. Até lá, vale a
  leitura mais restritiva (`citable-only`), como já registrado.
- Migrar outros nós: só existe um nó hoje (`find content -name meta.json` → 1).
- Criar UI que exiba referências; a hipótese de que `covers` é "exibido ao aluno" continua
  sendo hipótese sobre uma tela inexistente.

## Contexto e referências

- Origem: `TCK-0001/log.md` `[007]` (dívidas D-1, D-2, D-3 e a ACTION sugerida);
  `TCK-0004/log.md` `[006]` item 1 e `[009]` pendência 1 (campo adaptável × só citável).
- ADRs aplicáveis: **`ADR-0005`** (CC BY-SA 4.0 no conteúdo → incompatível com NC);
  **`ADR-0003`** §"independência do contrato de dados" (`:157-174`), que restringe o formato.
- Regra normativa: `AGENTS.md` §9.6–9.7 e o fluxograma de `docs/content/content-standards.md`.
- Arquivos-alvo: `docs/content/references-schema.md` (novo), `scripts/audit-content.py`,
  `content/high-school/algebra/quadratic-equations/references.json`, e a linha do checklist de
  `published` em `docs/content/content-standards.md` se o campo `usage` passar a ser cobrado.
- Lições relevantes: **L-006** (licença do OpenStax varia por livro); **L-007** (licença tem
  de ser legível sem JavaScript); **L-009** (share-alike exclui fonte NC).

## Perguntas em aberto

- Nenhuma bloqueante. Se o executor concluir que o contrato precisa de um campo além dos nove
  de (1), acrescenta com justificativa no log — o schema é novo, não há compatibilidade a
  preservar.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
