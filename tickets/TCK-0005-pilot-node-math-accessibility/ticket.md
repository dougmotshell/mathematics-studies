---
id: TCK-0005
title: Completar as descrições textuais das fórmulas do nó piloto
type: content
status: done
owner: qa-validator
priority: P1
size: P
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0002, ADR-0002]
---

# TCK-0005 — Completar as descrições textuais das fórmulas do nó piloto

## Pedido original (verbatim)

Achado independente de dois validadores durante o `TCK-0002` (entradas `[007]` e `[008]` do
log daquele ticket), encaminhado ao `tech-lead`:

> `content/high-school/algebra/quadratic-equations/theory.pt-BR.md` tem **8 blocos `$$…$$`**
> (linhas 34, 44, 51, 66, 76, 80, 92, 103) e só **3 linhas `*Leitura:*`** (36, 46, 53);
> `theory.en-US.md` idem, 8 × 3. Contraria `AGENTS.md` §9.2 e faria o CA-2 da spec
> `minimum-learning-slice` falhar por dados, não por implementação.

## Requisito refinado

A regra do projeto (`AGENTS.md` §9.2 e `docs/content/accessibility.md`) exige que **toda**
fórmula em display tenha descrição textual — é o que permite a um usuário de leitor de tela
acompanhar a teoria. O único nó de conteúdo existente cumpre a regra em 3 de 8 fórmulas, nos
dois idiomas. Como o nó piloto é o modelo que os próximos nós vão copiar, o defeito se
multiplica se não for corrigido agora.

Confirmação independente em 2026-08-01:
`grep -c '^\$\$' theory.pt-BR.md theory.en-US.md` → 8 e 8;
`grep -c 'Leitura:\|Reading:'` → 3 e 3.

## Critérios de aceite

- [x] 1. Cada uma das 8 fórmulas em display de `theory.pt-BR.md` tem descrição textual
      imediatamente após o bloco, no mesmo padrão das 3 já existentes (`*Leitura:* …`).
- [x] 2. O mesmo vale para as 8 de `theory.en-US.md`, no padrão en-US já usado no arquivo.
- [x] 3. As descrições **lêem a fórmula**, não a repetem em palavras vagas: quem ouvir a
      descrição sem ver a fórmula consegue reconstruí-la.
- [x] 4. Paridade pt-BR/en-US: mesmas fórmulas descritas, mesma informação matemática, com as
      convenções locais corretas (vírgula decimal em pt-BR, ponto em en-US).
- [x] 5. Nenhuma afirmação matemática nova é introduzida — a descrição não pode contradizer
      nem estender a fórmula que descreve.
- [x] 6. O LaTeX das fórmulas permanece **intocado**; só texto é acrescentado.
- [x] 7. `bash scripts/audit-content.sh` sem erros e sem avisos novos.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US
- [x] Acessibilidade WCAG 2.2 AA (inclui matemática acessível) — é o objeto do ticket
- [ ] Funciona offline / PWA · [x] não aplicável
- [x] Custo zero mantido
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [x] URLs de `content/` preservadas — nenhum slug muda
- [x] Correção matemática verificada — as descrições passam pelo `math-reviewer`

## Fora de escopo

- Reescrever a teoria, os exemplos ou os exercícios.
- Alterar `references.json` (fechado no `TCK-0001`) ou `meta.json`.
- Tirar o nó de `status: "draft"` — depende também de revisão completa de rigor e idioma.
- Criar nós novos.

## Contexto e referências

- Nó: `content/high-school/algebra/quadratic-equations/theory.{pt-BR,en-US}.md`
- Regra: `AGENTS.md` §9.2, `docs/content/accessibility.md`, `docs/content/i18n.md`
- Spec afetada: `docs/specs/minimum-learning-slice/spec.md` (CA-2)
- Origem do achado: `tickets/TCK-0002-define-minimum-learning-slice/log.md`, `[007]` e `[008]`
- Contexto: `memory/context/content.md`

## Perguntas em aberto

- Nenhuma.

## Resultado final

**`done` em 2026-08-01, validado por `qa-validator#3`** — 7/7 critérios de aceite atendidos com
evidência reproduzida de forma independente (comando + saída) no `log.md`, entrada `[011]`.
Nenhum defeito bloqueante. Zero devoluções no ticket.

### O que foi entregue

5 descrições textuais novas em cada arquivo de teoria do nó
`content/high-school/algebra/quadratic-equations`, fechando **8/8 fórmulas em display
descritas nos dois idiomas** (era 3/8). Só texto foi acrescentado: 35 inserções, 0 remoções.

- `theory.pt-BR.md` (+18 linhas) — `*Leitura:*` nas linhas 68, 81, 90, 105, 121
- `theory.en-US.md` (+17 linhas) — `*Reading:*` nas linhas 66, 79, 88, 103, 118

Fórmulas descritas: relações de Girard/Vieta; discriminante do Exemplo 1; aplicação da fórmula
geral no Exemplo 1; discriminante do Exemplo 2; condição `\Delta = 0` do Exemplo 3.

### Evidência por critério (detalhe em `[011]`)

| # | Critério | Evidência |
|---|---|---|
| 1 | 8/8 em pt-BR | `grep -c '^\$\$'` → 8 e `grep -c '^\*Leitura:\*'` → 8; **ordem** por `grep -n` → 34/36 · 44/46 · 51/53 · 66/68 · 79/81 · 87/90 · 103/105 · 118/121, alternância estrita; `grep -o '\$\$' \| wc -l` → 16, confirmando que os 8 `^$$` são aberturas |
| 2 | 8/8 em en-US | idem → 33/35 · 43/45 · 50/52 · 64/66 · 77/79 · 85/88 · 101/103 · 115/118 |
| 3 | Descrições reconstrutíveis | leitura adversarial às cegas do QA em 4 das 10 descrições novas (incl. a mais longa, Exemplo 1 com a fórmula geral): 4/4 reconstruções idênticas ao bloco a menos de espaçamento tipográfico; 5 tentativas de reagrupamento hostil documentadas e todas falharam |
| 4 | Paridade pt-BR/en-US | cobertura simétrica por posição; comparação estrutural token a token das 5 descrições novas → sequências idênticas (única diferença: artigo `a`/`the`); `grep -E '[0-9]+[.,][0-9]+'` nas descrições → vazio, regra vírgula × ponto não acionada |
| 5 | Nenhuma afirmação nova | busca negativa por conectivo justificativo (`logo\|portanto\|porque\|therefore\|hence\|because\|since`) nas linhas acrescentadas → vazio; verificação numérica independente em Python com `Fraction` de todos os valores falados |
| 6 | LaTeX intocado | `git diff -U0 -- content/ \| grep -E '^-[^-]'` → vazio (0 linhas); e prova direta: linhas com `$$` byte a byte idênticas às de `HEAD` (`21f6ef1`) nos dois arquivos; `--name-status` só `M`, nenhum `R` |
| 7 | Auditoria limpa | `bash scripts/audit-content.sh` → exit `0`, `Resumo: 1 nós · 0 erros · 0 avisos` |

**Alcance da evidência do critério 7 (declarado):** `scripts/audit-content.py` não inspeciona
descrição de fórmula — só presença e não-vazio dos `theory.<lang>.md`. Auditoria verde é
necessária, não suficiente; o que sustenta os critérios 1–5 são os comandos e a leitura
adversarial, não o exit `0`.

**Não verificado (não há o que subir):** sem `package.json` e sem consumidor dos
`theory.*.md`, não foram exercitados leitor de tela real, MathML do KaTeX, teclado, foco,
contraste, tema, zoom 200%, offline nem rede lenta. Coberto pelas pendências 6 e 7 abaixo.

### Pendências herdadas (7) — nenhuma bloqueou este ticket

Todas fora do diff desta entrega e preexistentes no commit `21f6ef1`. As marcadas com **D**
**condicionam a saída do nó de `status: "draft"`**.

| # | Pendência | Origem | Condiciona `draft`? |
|---|---|---|---|
| 1 | Enunciado do teorema (48/47), Resumo (143/140) e soma-e-produto (144/141) dão a fórmula geral sem condicionar a `\Delta \ge 0` | `[006]` `math-reviewer` | **D** (L-014) |
| 2 | Descrição preexistente de 53/52 cobre só a primeira metade do bloco — `\Delta = b^2-4ac` fica mudo | `[008]` `a11y-ux-reviewer` | **D** |
| 3 | Tabela "Erros comuns" (133/130) contrasta duas frações cujo único diferencial é o agrupamento; lido linearmente o contraste some | `[008]` | **D** |
| 4 | `\dfrac` inline no Resumo e 10 `\frac` inline em `exercises.json` sem tratamento de leitura — avaliar se `AGENTS.md` §9.2 cobre inline | `[008]` | não (condiciona a **regra**) |
| 5 | Registrar em `docs/content/accessibility.md` a tabela de convenções de leitura e, no glossário de `docs/content/i18n.md`, `subscrito (índice) \| subscript` com nota de desambiguação | `[007]` + `[008]` | **D** (o piloto é o modelo; convenção inédita — confirmado por `grep -rn` em `docs/`) |
| 6 | KaTeX emitindo MathML fará o leitor de tela ouvir fórmula **e** descrição, duplicado — resolver na apresentação (depende do ADR-0003) | `[008]` | não (condiciona o 1º render) |
| 7 | Parte 2 do `/a11y-audit`: leitor de tela real, foco, contraste, zoom 200% | `[008]` | não (condiciona a 1ª publicação renderizada) |

### Dois vereditos de escopo do QA

- **Pendência 2 não é violação do critério 1.** O critério 1 é de **existência e posição**, não
  de suficiência de cobertura: ele fixa como padrão de conformidade "o mesmo padrão das 3 já
  existentes" — e a descrição incompleta **é uma das 3** — e o próprio ticket declara o baseline
  como "3 de 8", nomeando a linha 53 como cumprida. O delta contratado eram 5 descrições, e 5
  foram entregues. Estender o critério depois da entrega é decisão do `tech-lead`. Segue como
  pendência que **condiciona `draft`**, com severidade menor que a estimada em `[008]`: o
  `\Delta = b^2 - 4ac` mudo é repetição literal do bloco anterior (44/43), lido integralmente
  cinco linhas acima (46/45) — o usuário perde a repetição, não a definição.
- **Pendência 1 não bloqueia este ticket.** O trecho está fora do diff (linhas 48/47 byte a
  byte idênticas a `HEAD`), nenhum critério de 1 a 7 alcança prosa não alterada, e nenhuma das
  10 descrições novas repete a imprecisão. Severidade `menor`; corrigir antes de sair de
  `draft`, não antes deste `done`.

### Independência da cadeia

Produção: `content-author` (`[004]`). Revisões independentes e em papéis competentes:
critério 3 pelo `a11y-ux-reviewer` (`[008]`), critério 4 pelo `i18n-steward` (`[007]`),
critério 5 pelo `math-reviewer` (`[006]`). Validação: `qa-validator#3`, que não produziu nem
revisou nada deste ticket e reexecutou toda a evidência.
