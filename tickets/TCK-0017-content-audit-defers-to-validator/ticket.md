---
id: TCK-0017
title: Eliminar a divergência entre audit-content.py e validate-content.py sobre o mesmo arquivo
type: bug
status: triaged
owner: backend-developer
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0014, TCK-0009, TCK-0015]
---

# TCK-0017 — Eliminar a divergência entre `audit-content.py` e `validate-content.py` sobre o mesmo arquivo

## Pedido original (verbatim)

> ### Achado do `audit-content.py` — 4 instâncias reproduzidas, todas confirmadas
>
> Medidas por mim numa **cópia isolada do repositório** (`content/` real intocado — hash
> conferido), sempre com o auditor e o validador rodando sobre o mesmo arquivo:
>
> | Mutação | `audit-content.py` | `validate-content.py` |
> |---|---|---|
> | `"correct": "false"` (texto) na única alternativa de gabarito | **exit 0** · `1 nós · 0 erros · 0 avisos` | exit 1 · `CORRECT-NOT-BOOLEAN` + `MC-NO-CORRECT-OPTION` |
> | `title.en-US: 5` | **exit 0** · `0 erros` | exit 1 · `LOCALIZED-NOT-STRING` |
> | `title.en-US: None` | **exit 0** · `0 erros` | exit 1 · `LOCALIZED-NOT-STRING` |
> | `true-false` com 2 opções `correct: true` | **exit 0** · `0 erros` (só AVISO de dicas) | exit 1 · `MC-MULTIPLE-CORRECT-OPTIONS` |
> | Controle: MC sem nenhuma correta | exit 1 · 1 erro | exit 1 |
>
> Causa das quatro: veracidade implícita (`o.get("correct")`, `audit-content.py:229`/`:240`),
> `str(value.get(lang,""))` (`:85`) e o `>1` verificado só para `multiple-choice` (`:236`).
> Consequência operacional: **hoje é possível ter exercício com gabarito errado, ou título
> inexistente em en-US, passando na auditoria em silêncio.** `audit-content.py` **não foi
> tocado** — é ticket próprio do `tech-lead`.

— `tickets/TCK-0014-content-contract-validator/log.md` `[010]`.

> **Ticket próprio para `scripts/audit-content.py`** — as 4 instâncias acima, mesma classe.
> Enquanto existir, o auditor é o elo fraco da malha; com o `prebuild` do TCK-0015 já
> chamando o validador, o portão estrito passa a governar o build, mas o auditor continua
> sendo o que roda no CI de conteúdo.

— idem, "Pendências entregues ao `tech-lead`", item 1.

## Requisito refinado

Quem sofre: (a) o estudante que recebe um exercício cujo gabarito está marcado errado —
`"correct": "false"` é uma **string não vazia**, logo verdadeira, e o auditor a lê como
"esta é a alternativa certa"; (b) o autor de conteúdo, que roda `bash scripts/audit-content.sh`,
lê `0 erros · 0 avisos · exit 0` e conclui que o nó está íntegro quando não está; (c) o CI —
`.github/workflows/ai-surface-audit.yml:51` executa o auditor e `:64` o validador **no mesmo
job**, e hoje eles podem dar veredito oposto sobre o mesmo byte.

O defeito de fundo **não são as quatro instâncias**: é existirem **duas implementações do
mesmo contrato**. Corrigir as quatro deixa as duas implementações de pé e a divergência volta
na próxima regra — e já há candidatas medidas (`ITEMS-EMPTY`, `null`, `id` repetido entre
arquivos). Duas ferramentas discordando sobre o mesmo fato é pior que uma ferramenta errada:
com uma, o autor sabe o que confiar; com duas, o veredito depende de qual comando ele rodou.

Resultado esperado: sobre o **contrato de um arquivo de conteúdo** existe **uma** fonte de
verdade — `validate-content.py`. O auditor deixa de opinar sobre esse contrato e passa a
**delegar**, mantendo apenas o que só ele faz (relações entre nós e portões editoriais). A
divergência deixa de ser possível por construção, não por coincidência de correções.

## Decisão de recorte: **delegar**, não corrigir em paralelo — e por quê

Avaliadas as duas saídas:

| Saída | O que resolve | O que deixa de pé |
|---|---|---|
| **Corrigir o auditor** (booleano estrito em `:229`/`:240`, tipo de string em `:85`, `>1` para todo `SINGLE_CORRECT_TYPES`) | as 4 instâncias de hoje | as duas implementações; a 5ª divergência nasce na próxima regra que só uma das duas ganhar. É corrigir a **lista de casos**, não a **classe** — exatamente o erro que L-013, L-018 e o adendo da L-019 já custaram a este projeto duas vezes |
| **Delegar** (escolhida) | a classe: sobre contrato de arquivo passa a existir um só juízo, e a divergência vira impossível | nada que o auditor cubra sozinho — ver a prova de não-regressão abaixo |

Três fatos sustentam a escolha, todos já medidos e nenhum presumido:

1. **O validador é estritamente mais estrito na sobreposição.** O `qa-validator#8` atacou as
   duas ferramentas com sete fixtures de burla e registrou: *"Nenhum dos sete tem o auditor
   como o mais estrito. `audit=0 · validate=0` em todos"* (`TCK-0014/log.md` `[010]`). Não há
   um único caso conhecido em que delegar perca cobertura.
2. **A fronteira já existe no código.** As funções `check_prerequisites` (`:286`),
   `check_paths` (`:319`), `check_references` (`:264`), `check_theory` (`:149`), os portões de
   `status: "published"` (incluindo `verified`, L-002) e a cobertura de `skills[]` **não têm
   contrapartida** no validador: o inventário de códigos dele (`grep -oE '"[A-Z][A-Z0-9-]{3,}"'`)
   não tem nenhuma regra de grafo, de referências ou de trilha. Delegar não esvazia o auditor
   — o devolve à sua área exclusiva.
3. **Os papéis são diferentes e continuam necessários:** o validador responde *"este arquivo
   pode ser carregado?"* (por nó, portão de build — `package.json` `prebuild`); o auditor
   responde *"este acervo é coerente?"* (entre nós, portão editorial — grafo acíclico,
   dificuldade não crescente, licença das referências, trilhas apontando para nós existentes).

**O mecanismo da delegação não é decidido aqui** (L-011: o ticket fixa a restrição e o
resultado exigido, não o mecanismo). `import` do validador, subprocesso, ou composição em
`audit-content.sh` são todos aceitáveis desde que os critérios 2, 3 e 8 passem; a escolha e a
razão vão para o log.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. **As quatro instâncias, como fixtures obrigatórias.** Uma fixture por instância,
      derivada de uma cópia do nó piloto, cada uma com a mutação isolada; as duas ferramentas
      rodam sobre **o mesmo arquivo** e o resultado é registrado lado a lado:
      1. `"correct": "false"` (a **string**) na única alternativa de gabarito;
      2. `title.en-US: 5` (número);
      3. `title.en-US: null`;
      4. `true-false` com **duas** alternativas `correct: true`.
      Teste: nas quatro, `bash scripts/audit-content.sh <fixture>` → **exit 1**, com a regra
      nomeada e o localizador do item/campo na mensagem. Falha se qualquer uma sair `0` ou se
      a mensagem não disser **qual item** e **qual campo**. Controle obrigatório: o nó piloto
      intacto → exit 0 nas duas ferramentas (sem falso positivo).
- [ ] 2. **Invariante de não-divergência, automatizada.** Existe um teste executável que, para
      cada fixture de uma matriz, roda as duas ferramentas e falha se
      `validate-content` sair `1` e `audit-content` sair `0`. Matriz mínima: as 4 fixtures do
      critério 1 + as 5 do critério 3 do TCK-0014 (MC sem correta; MC com duas; `tolerance`
      negativa; chave de idioma faltando; `nodeId` divergente) + o piloto intacto. Teste: com
      a invariante temporariamente invertida em uma fixture, o teste **reprova** — provar que
      ele não é decorativo.
- [ ] 3. **Nenhuma regra de contrato de arquivo implementada duas vezes.** O log traz o
      inventário **completo** dos pontos de `err()`/`warn()` do `audit-content.py` de hoje
      (`grep -c 'err(\|warn(' scripts/audit-content.py` → **53** na entrega inicial),
      classificado item a item em: **delegado** (sai do auditor), **exclusivo** (fica) ou
      **reconciliado** (fica, com a razão de não ser duplicata). Teste: nenhuma linha
      classificada como "delegado" sobrevive no fonte do auditor (`grep` do trecho citado →
      0 ocorrências), e nenhum item fica sem classificação — a soma das três categorias é 53.
- [ ] 4. **Sem regressão de cobertura exclusiva.** Uma fixture por família que o validador
      **não** cobre, cada uma continuando a reprovar no auditor: (a) `prerequisites` apontando
      para nó inexistente; (b) ciclo no grafo de pré-requisitos; (c) pré-requisito de
      dificuldade **maior**; (d) `references.json` sem licença; (e) trilha em `content/paths/`
      apontando para nó inexistente; (f) `status: "published"` com item sem `verified`
      (L-002); (g) `theory.en-US.md` ausente. Teste: as sete → exit 1 no auditor, antes e
      depois da mudança, com a mesma regra nomeada. Falha se alguma passar a sair 0.
- [ ] 5. **`ITEMS-EMPTY` deixa de ser assimétrica.** Os três estados de `exercises.json` —
      **ausente**, conteúdo `null` (D-5) e `items: []` — produzem o **mesmo** veredito, e o
      **mesmo nas duas ferramentas**. Qual veredito é decisão do executor, registrada no log
      com a justificativa contra `docs/content/exercise-schema.md:107` (regra 8: 8–12 itens).
      Teste: matriz 3 estados × 2 ferramentas = 6 execuções, todas com o mesmo par
      (exit, regra). Falha se o veredito depender de a diferença ser de 4 caracteres.
      `docs/` **não** é editado aqui (critério 10).
- [ ] 6. **O acervo real passa e não é tocado.** `bash scripts/audit-content.sh` e
      `bash scripts/validate-content.sh` sobre `content/` → exit 0 nos dois;
      `git status --porcelain content/` → 0 linhas e hash do diretório idêntico antes e
      depois. Se o piloto **não** passar, é descoberta sobre o acervo e vai para o log
      **antes** de qualquer correção — nunca se ajusta o conteúdo para calar a ferramenta.
- [ ] 7. **As três classes da L-019 (ampliada) valem para o auditor.** (a) *Travessia*:
      fixture com defeito em subnó **dois níveis** abaixo do alvo (`…/discriminant/
      sign-analysis`) é encontrada com alvo = raiz, tópico, subnó e sub-subnó. (b) *Canais*:
      o código de saída sobrevive a `| head`, `> /dev/full`, `2>&1 | true` e `>&- 2>&-`, em
      stdout **e** stderr — matriz de 4 redirecionamentos × 3 desfechos (íntegro, violação,
      erro de uso), com os códigos declarados. (c) *Codificação*: verde em
      `env -i LC_ALL=POSIX PYTHONUTF8=0`. Falha se qualquer combinação transformar violação
      em `0`.
- [ ] 8. **Contratos de invocação preservados.** Continuam funcionando, sem mudança de
      assinatura: `bash scripts/audit-content.sh [caminho]`,
      `python3 scripts/audit-content.py [caminho]`, os dois passos do CI
      (`.github/workflows/ai-surface-audit.yml:51` e `:64`) e `npm run validate:content`
      (`package.json`). **Zero dependência nova** (`stdlib` apenas — teste: imports fora de
      `sys.stdlib_module_names` → `[]`). O auditor continua rodando **sem** a aplicação e a
      partir de qualquer diretório.
- [ ] 9. **Sem regressão no artefato do TCK-0014.** A suíte `bash scripts/validate-content-test.sh`
      continua **118 passaram · 0 falharam** (ou mais, se o executor acrescentar casos —
      nunca menos), e o md5 de `scripts/validate-content.py` só muda se o log explicar por quê.
      Ticket `done` não reabre: alterar o validador aqui exige justificativa nominal.
- [ ] 10. `bash scripts/audit-ai-surface.sh` → exit 0. Nada em `content/`, `docs/` ou
      `.github/instructions/` é alterado por este ticket (`git status --porcelain` limpo
      nesses três caminhos) — a reconciliação de `docs/content/exercise-schema.md` é ticket do
      `docs-writer` e recebe deste log a decisão do critério 5.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — instâncias 2 e 3 são exatamente falhas de paridade que
      passavam em silêncio; o critério 1 as transforma em erro visível
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável — ferramenta de linha de comando
- [ ] Funciona offline / PWA · [x] não aplicável
- [x] Custo zero mantido — critério 8 (zero dependência nova)
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [x] URLs de `content/` preservadas — critério 6 (`content/` intocado)
- [x] Correção matemática verificada — indireta e é o ponto do ticket: gabarito marcado
      errado deixa de atravessar a auditoria (L-002)

## Fora de escopo

- **Editar `docs/content/exercise-schema.md`** — a reconciliação do schema com as regras novas
  (`ITEMS-EMPTY`, `ITEM-ID-DUPLICATE`, `JSON-DUPLICATE-KEY`, `version`, `unit: null`) é
  trabalho do `docs-writer` (encaminhamento 3 do TCK-0014). Aqui a decisão do critério 5 é
  **registrada**, não documentada.
- **Os sete falsos negativos do validador** (`TCK-0014/log.md` `[010]`), que **não** são
  divergência — as duas ferramentas concordam neles: D-1 overflow (gatilho: primeiro `numeric`
  com inteiro ≥ 10^309), D-2 vazio de largura zero, D-3 `answer` inútil, D-4 `rubric` sem
  regra, D-6 `id` repetido entre `exercises.json` e `assessments.json`, D-8 seis tipos sem
  exemplar real. Ficam como dívida com gatilho; **D-1, D-2 e D-5** são as que o QA resolveria
  antes do primeiro lote grande de conteúdo, e **D-5 entra aqui** só porque é assimetria
  entre as duas ferramentas (critério 5).
- **D-7 — diretório só com `theory.*.md`, invisível às duas** (`audit-content.py:88-90`: nó é
  quem tem `meta.json`). Mudar a descoberta de nó muda o que **conta como nó** — é decisão de
  taxonomia (`curriculum-architect` + `docs/content/taxonomy.md`), não de ferramenta.
- **Natureza da `tolerance` (absoluta × relativa)** — decisão de contrato necessária antes das
  tasks 5–8 da spec; ticket próprio.
- Alterar `content/`, criar nó novo ou mudar `status` de nó.

## Contexto e referências

- Origem: `tickets/TCK-0014-content-contract-validator/log.md` `[010]` — seção "Achado do
  `audit-content.py`", "Minhas fixtures de burla" (D-5, D-7), ponto de julgamento (a)
  (assimetria do `ITEMS-EMPTY`) e "Pendências entregues ao `tech-lead`" item 1.
- Linhas citadas: `scripts/audit-content.py:85` (`str(value.get(lang,""))`), `:229` e `:240`
  (`o.get("correct")` — veracidade implícita), `:236` (`>1` só para `multiple-choice`),
  `:88-90` (descoberta de nó). Fronteira exclusiva: `:149`, `:264`, `:286`, `:319`.
- Consumidores a não quebrar: `.github/workflows/ai-surface-audit.yml:51` e `:64`;
  `package.json` (`prebuild` → `npm run validate:content`).
- ADRs aplicáveis: `ADR-0003` (stack aceita — o validador é CLI e independe dela);
  `ADR-0002` (paridade obrigatória: as instâncias 2 e 3 são furos nessa paridade).
- Lições relevantes: **L-019** (portão só protege o que enxerga — com o adendo de
  reincidência: escrever a **classe**, nunca a lista de casos); **L-013** e **L-018** (corrigir
  a linha/causa citada não é corrigir o defeito); **L-002** (gabarito sem verificação é a
  principal fonte de erro); **L-011** (ticket decide restrição, não mecanismo);
  **L-015**/**L-017** (falso silêncio é indistinguível de "está tudo bem").
- Cadeia: `tech-lead` → `backend-developer` → `code-reviewer` → `qa-validator`. O
  `backend-developer` escreveu o `validate-content.py` (TCK-0014) e por isso conhece a
  fronteira; a independência é preservada porque **quem revisa e valida aqui não escreveu
  nenhuma das duas ferramentas** — e o critério 9 protege o artefato já `done`.

## Reprodução (`type: bug`)

- **Passos:** numa cópia isolada do repositório, aplicar uma mutação por vez em
  `content/high-school/algebra/quadratic-equations/`: (1) trocar `"correct": true` por
  `"correct": "false"` na alternativa de gabarito de um item `multiple-choice`;
  (2) `meta.json` com `"title": {"pt-BR": "…", "en-US": 5}`; (3) idem com `null`;
  (4) item `true-false` com duas alternativas `correct: true`. Em cada uma rodar
  `bash scripts/audit-content.sh` e `bash scripts/validate-content.sh`.
- **Esperado:** as duas ferramentas reprovam o mesmo arquivo, ou pelo menos o auditor nunca
  diz "0 erros" sobre o que o validador recusa.
- **Obtido:** auditor `exit 0 · 1 nós · 0 erros · 0 avisos` nas quatro; validador `exit 1`
  nas quatro (`CORRECT-NOT-BOOLEAN` + `MC-NO-CORRECT-OPTION`, `LOCALIZED-NOT-STRING` ×2,
  `MC-MULTIPLE-CORRECT-OPTIONS`). Controle (MC sem nenhuma correta): as duas reprovam.
- **Ambiente:** Python 3.12.3, GNU bash 5.2.21, Linux 7.0.0-28-generic x86_64; medido pelo
  `qa-validator#8` em 2026-08-01, com `content/` real intocado (hash conferido).

## Perguntas em aberto

- Nenhuma que bloqueie. O veredito do critério 5 (ausente/`null`/`[]`) é decisão do executor
  dentro da norma escrita (`exercise-schema.md:107`, 8–12 itens); se ele concluir que a norma
  não decide, escala ao `tech-lead` em vez de escolher em silêncio.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
