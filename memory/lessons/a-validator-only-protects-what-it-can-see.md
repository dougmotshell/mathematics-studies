# Um validador só protege o que ele consegue enxergar

**Tipo:** erro
**ID:** L-019
**Contexto:** TCK-0014, 2026-08-01 — implementação de `scripts/validate-content.py`, o portão
de carga do contrato de `content/` (RF-18: "falha silenciosa é defeito"). A suíte de casos
hostis pegou dois defeitos no próprio validador, antes da entrega.

**Lição:** validador que reprova bem o conteúdo que ele lê ainda pode ser inútil, porque as
falhas mais perigosas acontecem **antes** da primeira regra rodar e **depois** da última:

1. **Descoberta.** A varredura procurava nós por `meta.json`. Um diretório com
   `exercises.json` e sem `meta.json` não aparecia como nó — e o resultado era
   `0 violações · exit 0`, ou seja, o conteúdo quebrado passava com selo de aprovado. O mesmo
   valia para um caminho errado na linha de comando: apontar o pipeline para o diretório
   errado devolvia sucesso.
2. **Emissão.** Com `| head` ou `>&-`, o flush de encerramento do Python trocava o `exit 1`
   (contrato violado) por `120`. O veredito sobre o conteúdo virava refém do estado do
   terminal: um pipeline leria "erro de ferramenta" onde havia violação real — e, em outra
   combinação, o inverso.

Em ambos os casos a lógica de validação estava correta. O que faltava era tratar
**invisibilidade** e **saída quebrada** como modos de falha de primeira classe, do mesmo
nível que uma regra errada.

**Como aplicar:** ao escrever qualquer portão (validador, auditoria, verificação de CI):

- Testar o caminho **vazio**: alvo sem nenhum objeto encontrado nunca sai `0`. "Nada
  encontrado" é erro de uso, não aprovação.
- Reconhecer o objeto por mais de um marcador (aqui: `meta.json` **ou** arquivo de
  exercícios), para que um arquivo faltando não apague o objeto inteiro da varredura.
- Ter um caso de teste com a saída padrão quebrada (`| true` e `>&-`) provando que o código de
  saída continua sendo o veredito sobre o **conteúdo**, e não sobre o canal.
- Verificar também o inverso do falso negativo: uma cópia intacta do artefato real precisa
  passar limpa, senão o portão vira ruído e será desligado.

Complementa L-015 e L-017 (silêncio falso é indistinguível de "está tudo bem").

## Adendo — 2026-08-01, TCK-0014, REJECT [006]: a lição foi violada na mesma entrega

Esta lição foi escrita e **reincidida no mesmo commit de trabalho**. O `code-reviewer#6`
achou os dois modos de falha de novo, cada um numa variante que a correção original não
alcançou:

- **B1 (descoberta).** Eu troquei o marcador (`meta.json` **ou** exercícios) e parei aí.
  A varredura continuava com `return [scope]` quando o alvo já era um nó: apontar o
  validador para um tópico com subnó quebrado dava `Contrato íntegro, exit 0`, enquanto a
  raiz acusava 8 violações em 2 nós. Pior forma possível de falso negativo — a ferramenta
  fica **mais** cega quanto mais o acervo cresce.
- **B2 (emissão).** Eu protegi o `stdout` e não o `stderr`. O `exit 2` de erro de uso
  continuava virando `120` com `2>&1 | true`, `2> /dev/full` e `--xx` (mensagem do próprio
  argparse) — inclusive no caso "apontar o pipeline para o diretório errado" que esta lição
  cita nominalmente como o perigo a evitar.

**Por que escapou:** corrigi os dois casos **citados** pela minha própria suíte, e escrevi a
lição descrevendo os casos, não a classe. É exatamente L-013 ("corrigir a linha citada não é
corrigir a classe do defeito") e L-018 ("corrigir a causa citada não é corrigir o modo de
falha") aplicadas a mim — e é o motivo de a checagem valer para **todo canal** e **todo nível
de profundidade**, não para o exemplo que apareceu primeiro.

**Como aplicar (revisão da regra, mais forte que a original):**

- **Travessia:** nenhum caminho de código pode encerrar a varredura no alvo. Teste
  obrigatório: objeto quebrado **um nível abaixo** do alvo, com o veredito comparado ao da
  raiz — os dois têm de coincidir.
- **Canais:** a proteção do código de saída se aplica a `stdout` **e** `stderr`, incluindo o
  texto emitido por bibliotecas (argparse). Matriz de teste: `| true`, `>&-`, `> /dev/full`,
  para os três códigos (0, 1, 2), nos dois canais.
- **Codificação:** mensagem que some por causa do terminal (`LC_ALL=POSIX`) equivale a não
  ter mensagem; forçar `errors="replace"` na saída.
- Ao registrar lição sobre um defeito, escrever a **classe** ("nada some da varredura",
  "nenhum canal muda o veredito"), nunca a lista de casos corrigidos — a lista é o que o
  próximo defeito vai contornar.

## Adendo — 2026-08-01, TCK-0015, REJECT [006]: a mesma classe fora do validador

Terceira reincidência, agora em **devops**, em duas formas que a redação anterior não
alcançava porque falavam do validador como programa, não do portão como posição:

- **B2 — a verificação não verifica.** Dois passos de CI usavam
  `if grep -r <padrão> <alvo>; then falha; fi`. `grep -r` sai **2** quando o alvo não existe,
  e o `if` só trata `0` — então o passo imprimia `OK` e ficava **verde justamente no cenário
  que ele existia para pegar** (o diretório `src/content-contract/` desaparecer, absorvido
  pelo gerador). É literalmente o "testar o caminho vazio" que a regra já mandava fazer, na
  palavra "verificação de CI" que já estava escrita — e ainda assim escapou, porque `grep`
  parece binário (achou / não achou) e tem **três** desfechos.
- **B1 — o portão certo, fora do caminho.** O portão do contrato de carga foi posto no
  `prebuild` **e** no CI, com a justificativa correta ("a Vercel não lê o resultado do
  Actions; portão fora do caminho não é portão") — e a auditoria editorial, única que enxerga
  a paridade bilíngue, ficou só no CI. Resultado medido: push direto em `main` publicava
  `dist/pt-br/…/index.html` de um nó `languages: ["pt-BR"]`, com o CI vermelho ao lado. O
  argumento estava certo e foi aplicado a **uma** das ferramentas.

**Como aplicar (extensão da regra):**

- **Código de saída de ferramenta de linha de comando tem mais de dois valores.** Em portão
  de CI, tratar `0`, `1` e "qualquer outro" explicitamente (`case "$rc" in`), e conferir a
  **existência e a não-vacuidade do alvo** antes de rodar a busca. Verificação inconclusiva
  vale como reprovação, nunca como aprovação.
- **Portão se lista por caminho, não por ferramenta.** Enumerar os caminhos que chegam ao
  usuário (merge, push direto, publicação pelo host, execução local) × as verificações que
  existem, e conferir a matriz completa. Uma verificação que só existe em um caminho protege
  só aquele caminho, por mais correta que ela seja.
- **A prova de um passo de CI é executá-lo**, com o alvo presente **e** ausente. O texto do
  passo é extraível do próprio arquivo do workflow; rodar uma cópia paráfrase não prova nada
  sobre o que está versionado.

## Adendo — 2026-08-01, TCK-0015, REJECT [010]: estreitar para tirar falso positivo abre falso negativo

Quarta reincidência, na correção da anterior. O passo "sem recurso de terceiro" reprovava
qualquer `https://` — inclusive link de referência bibliográfica, que será conteúdo legítimo.
Troquei o padrão genérico por uma lista de formas específicas (`<script`, `src="https:`,
`@font-face`…), rodei **seis** casos, todos passaram, e entreguei. Medição do revisor: **8 de
18 vetores passavam calados** — protocolo relativo (`//host`, a forma clássica de pixel),
aspas simples, `@import` sem `url()`, `<object data>`, `<a ping>` (beacon, palavra que o
próprio critério nomeia), `meta refresh`, `<image href>` em SVG e **qualquer tag em
maiúscula**, porque o `grep` perdeu o `-i` e nome de tag em HTML é case-insensitive. Um
arquivo em `public/` — copiado verbatim para a saída — publicava rastreador com o passo
verde.

**A classe:** *afrouxar um detector para eliminar falso positivo é reescrevê-lo por inteiro, e
o novo detector precisa da bateria inteira, não do delta.* Falso positivo custa uma build
vermelha; falso negativo publica o que o portão existia para impedir — a assimetria manda
errar para o lado de recusar (é o adendo de L-022 aplicado a portão de CI). O erro de método
é o de L-013/L-021: eu troquei uma **regra de classe** ("qualquer URL absoluta") por uma
**lista de casos** e testei a lista contra ela mesma.

**Como aplicar:**

- Ao substituir um padrão de detecção, escrever antes a **classe em uma frase** ("tudo que faz
  o navegador buscar bytes de outra origem") e derivar os vetores da classe — sintaxe
  alternativa (aspas simples/duplas/sem aspas), forma abreviada (`//host`), caixa alta,
  atributo equivalente (`data`, `ping`, `poster`, `formaction`, `background`, `srcset`) e o
  canal equivalente (`@import` sem `url()`, `meta refresh`).
- Toda bateria tem os **dois lados**: vetores que precisam reprovar **e** casos legítimos que
  precisam passar. Só o segundo lado prova que o padrão não voltou a ser genérico.
- Nunca comparar o padrão novo com o antigo só pelo que ele ganhou: listar o que ele
  **deixou** de pegar. Se a lista não estiver vazia, é regressão.
- Rodar a bateria contra o **passo versionado**, com o artefato real incluso — e lembrar que a
  saída da build contém arquivos que ninguém escreveu na aplicação (`public/`).
