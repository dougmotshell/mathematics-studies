# L-021 — Norma que nomeia só o caso estrito deixa o caso frequente sem regra

**Tipo:** sucesso
**Data:** 2026-08-01
**Área:** conteúdo · documentação
**Origem:** TCK-0006 (fronteira display × inline da `AGENTS.md` §9.2), a partir dos achados
`[008]` §7.2, §7.3 e §7.5 do TCK-0005.

## Contexto

`AGENTS.md` §9.2 exigia descrição textual para "fórmula em display". A redação era correta e
verificável — e, por isso mesmo, silenciosa sobre o caso **mais comum**: a fórmula inline. No
nó piloto, o resultado foi um Resumo com `\dfrac` mudo, uma linha de "Erros comuns" cujo
assunto **é** o agrupamento sem nenhuma marcação verbal, e 10 `\frac` em `exercises.json` sem
tratamento — nenhum deles violando a regra escrita. A revisão de acessibilidade encontrou
tudo isso, mas teve de classificar como "avaliar se a regra deve cobrir", porque não havia
regra a aplicar.

Ao decidir, os dois extremos eram ruins: exigir leitura integral de toda inline tornaria o
texto ilegível por repetição (só o piloto pediria 38 inserções, quase todas para `$x^2$` e
`$x_1$`); não exigir nada mantinha muda a fórmula que mais precisa. E "avaliar caso a caso"
não é regra — é devolver o problema ao autor.

## Lição

Ao estreitar uma norma para torná-la verificável, o caso deixado de fora **não fica neutro:
fica permitido**. Fechar a lacuna raramente é estender a mesma obrigação ao caso novo — em
geral é dar a ele uma **obrigação diferente e mais barata**, disparada por um **teste
mecânico** aplicável por inspeção do artefato, sem julgar a intenção de quem escreveu.

Aqui, display ficou com "leitura integral" e inline com "agrupamento dito em palavras",
disparada pelo *teste do argumento composto* (numerador, denominador, radicando, expoente,
subscrito ou base que contenha operador, relação, fatores justapostos ou parênteses). O teste
foi calibrado para reproduzir, como regra, o julgamento que o revisor já fazia à mão — e a
calibragem se comprova rodando o teste contra o artefato real **antes** de publicar a norma:
foi assim que apareceram seis `(-n)^2` que nenhuma revisão anterior havia listado.

## Como aplicar

1. Ao escrever ou revisar norma, pergunte explicitamente **qual caso a redação deixa de
   fora** e escreva o veredito para ele — inclusive quando o veredito é "nada a fazer".
2. Prefira **obrigação diferenciada** a obrigação uniforme: o caso frequente precisa de uma
   regra que caiba no custo de produção, senão ela é ignorada ou cumprida mecanicamente.
3. O gatilho tem de ser **inspecionável no artefato** (formato, sintaxe, presença de token).
   Se depender de "o autor quis dizer", não é regra.
4. **Rode o teste contra o conteúdo existente antes de publicar a norma** e registre o
   veredito ocorrência a ocorrência. Isso calibra o limiar, dimensiona o passivo e vira o
   insumo pronto do ticket de correção.
5. Regra nova só existe quando chega ao `AGENTS.md`, às `.github/instructions/` com o
   `applyTo` da área e aos agents/skills que produzem e revisam o artefato — ver `L-009`
   (adendo) e `L-010`.

## Adendo (2026-08-01, após o `[006] REJECT` do TCK-0006)

Os itens 4 e 5 acima falharam **na mesma execução em que foram escritos**, e por uma única
causa raiz mais funda: **derivei o conjunto a varrer, e o conjunto a propagar, do que eu já
tinha em mãos — não da definição da classe.**

- **No inventário (item 4).** A classe que a norma criou é "base entre parênteses". As
  ocorrências que eu conhecia eram `(-4)^2`, `(-5)^2`, `(-6)^2`, e o padrão que escrevi foi
  `grep '(-[0-9a-z]*)\^'` — que codifica "parênteses **com sinal negativo**". `(x+3)^2` é da
  classe e não casa com o padrão. Agravante: usei varredura estrutural (parser de inline) em
  `theory.*.md` e um `grep` estreito em `exercises.json`, e mesmo assim declarei "varri todas
  as inline nos três arquivos" — a declaração de completude era falsa exatamente no arquivo
  varrido pelo método mais fraco. É a classe de `L-013`, um nível acima: não basta varrer o
  artefato inteiro se o **padrão** foi derivado das ocorrências já conhecidas.
- **Na propagação (item 5).** Listei os destinos a partir dos agentes que eu associava a
  `theory.*.md` (`content-author`, `/new-topic`), não a partir dos **artefatos que a norma
  passou a reger**. Como a regra nomeia `exercises.json` e `assessments.json`, os donos desses
  arquivos — `exercise-designer` e `/new-exercise-set` — eram destino obrigatório e ficaram de
  fora.

**Como aplicar (substitui a formulação frouxa dos itens 4 e 5):**

- **Padrão de busca vem da definição, nunca dos exemplos.** Escreva o predicado da classe
  ("qualquer base seguida de `^` cujo conteúdo esteja entre parênteses") e só então o
  converta em busca. Teste do padrão: ele acharia uma ocorrência que eu **ainda não vi**?
  `grep -nF ')^'` acha; `grep '(-[0-9a-z]*)\^'` não.
- **Um método só para todos os artefatos.** Varredura assimétrica invalida a declaração de
  completude no arquivo mais fraco. Se o parser roda em um arquivo, roda nos três.
- **Some os totais a partir da tabela publicada**, não da memória de quem a escreveu — em
  TCK-0006 o texto dizia "3 por idioma" com **quatro** linhas marcadas EXIGE logo acima.
- **A lista de propagação se deriva dos artefatos que a regra nomeia**: para cada artefato,
  quem o escreve e quem o revisa. Não da lista de arquivos que você já abriu.

## Segundo adendo (2026-08-01, após o `[009] REJECT` do TCK-0006)

Mesma causa raiz, terceira aparição: **enumeração fechada repetida fora do documento-fonte é
dívida**. Quando o teste ganhou o gatilho "base elevada ambígua", os dez pontos que
**reenunciavam** a regra ("fórmula inline com argumento composto") continuaram com a lista
antiga. `-x^2` não tem argumento composto — logo atravessava todos eles, inclusive o
**checklist de `published`**, que é o portão. Portão mais frouxo que a regra é portão que não
fecha, e o defeito é invisível porque cada frase, isolada, continua verdadeira.

**Como aplicar:**

- **Quem reenuncia uma regra cita o veredito do teste, não a lista de gatilhos.** "Toda
  fórmula que o teste X marca como *exige*" envelhece bem; "toda fórmula com argumento
  composto" envelhece no primeiro gatilho novo.
- **Checklist e portão nunca reenunciam — sempre referenciam.** Um checklist que reescreve a
  norma com outras palavras é uma segunda fonte de verdade que diverge em silêncio.
- **Se o teste tem mais de uma parte, dê nome a cada uma e diga no documento-fonte que
  repetir só uma delas é defeito.** O aviso viaja junto com a regra.
- **Ao acrescentar um gatilho a uma regra já propagada**, o trabalho não é editar o
  documento-fonte: é `grep` pela **formulação antiga** em toda a superfície e conferir que
  nenhum ponto ficou com a enumeração fechada — inclusive os gerados.
