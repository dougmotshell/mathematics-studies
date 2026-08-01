# Escrever a regra não é aplicá-la

**Tipo:** erro
**ID:** L-022
**Contexto:** `TCK-0013`, 2026-08-01 — desenho dos 13 estados de tela da fatia mínima
(`docs/design/minimum-learning-slice/screen-states.md`). O documento definia a regra "para o
mesmo evento, mover foco **ou** anunciar por região viva, nunca os dois" numa tabela de riscos
no fim do arquivo — e violava a própria regra em 3 dos 13 estados descritos acima dela
(E2 na carga inicial, E5 pela nova tentativa, E10 sem navegação). O `code-reviewer` encontrou
por cruzamento estado a estado.

**Lição:** regra enunciada em seção terminal (riscos, notas, apêndice) não governa o corpo do
documento — ela vira observação, não norma, e o autor a aplica de memória, que é onde ela
falha. Duas consequências: (1) a norma precisa nascer na **seção estrutural** que todos os
itens herdam, antes dos itens; (2) enunciá-la não substitui **verificá-la item a item** contra
o que já está escrito. No caso específico, a regra tinha efeito técnico invisível na prosa:
região viva educada é descartada ou embaralhada quando o foco muda no mesmo instante, então o
texto declarado como "anunciado" pode nunca ser ouvido — a declaração de acessibilidade fica
sem efeito exatamente onde parecia mais completa.

**Como aplicar:**
1. Toda regra transversal vai para a seção estrutural do artefato (a que define esqueleto,
   ordem ou contrato), não para riscos, notas ou conclusão.
2. Depois de escrever a regra, **varrer todos os itens do artefato** e marcar em cada um qual
   lado da regra vale — a varredura é parte da entrega, não da revisão.
3. Quando a regra tem exceções legítimas (navegação, por exemplo), nomeá-las na própria regra;
   exceção não declarada volta como defeito.
4. Vale para qualquer par mutuamente exclusivo declarado num documento de desenho ou de
   arquitetura: mover foco × anunciar, região viva × conteúdo, validar no build × em runtime.

**Família:** complementa `L-013` (corrigir a linha citada não corrige a classe) e `L-021` (o
caso que a norma não nomeia fica **permitido**). L-013 diz *até onde* varrer, L-021 diz *o que*
a norma deixou de fora, e L-022 diz *onde a norma nasce*. As três descrevem o mesmo defeito em
momentos diferentes do trabalho.

## Adendo — 2026-08-01, `TCK-0013`, loop 2/3 (`[010] REJECT`)

A lição foi escrita no loop 1 e **os dois defeitos do loop seguinte eram dela**:

1. **A varredura tem de alcançar diagrama e rótulo.** A correção da enumeração do cartão do
   índice foi feita na prosa e não no rótulo do nó Mermaid, que é normativo e vem **antes** da
   prosa no documento. Prosa corrigida com diagrama desatualizado é a decisão errada continuando
   a valer, pelo caminho que se lê primeiro. Varrer = prosa + diagrama + rótulo + tabela + front
   matter (`L-013`).
2. **Regra escrita para um lado de um par simétrico deixa o outro lado sem regra.** O documento
   recusava a entrada `3,5` em en-US (vírgula = separador de milhar lá) e **não** recusava
   `3.000` em pt-BR (ponto = separador de milhar aqui): o lado sem guarda marcava como
   **correta** uma resposta errada em 2 de 2 itens numéricos reais. É `L-021` aplicada a um par
   simétrico — idioma, sentido, extremo, direção.

**Como aplicar (adendo):**
5. Regra que menciona um idioma, um sentido ou um extremo tem de ser escrita como **pergunta
   respondida para todos os lados** ("para cada idioma: qual é o separador decimal, qual é o de
   milhar, o que acontece com cada um"), em tabela com uma coluna por lado. Coluna vazia é
   defeito, não estilo.
6. O gatilho da regra é **inspecionável no dado de entrada** (qual caractere apareceu, quantas
   vezes), nunca a intenção presumida de quem digitou.
7. Antes de publicar a regra, **rodá-la contra o conteúdo real** e escrever o resultado — no
   caso, os cinco itens de `exercises.json`. Foi o que expôs o falso positivo (`L-021`, item 3).
8. Entre recusar entrada válida e aceitar entrada errada, o desenho de aprendizagem prefere
   **recusar**: falso positivo manda o aluno embora achando que acertou.
