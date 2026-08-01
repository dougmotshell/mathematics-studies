**Tipo:** erro
**ID:** L-017
**Contexto:** 2026-08-01, TCK-0012, segundo `REJECT` (loop 2/3). Complementa
[L-015](a-monitor-that-guesses-must-guess-pessimistically.md), que mandou presumir pelo lado
pessimista — regra que continua certa e não muda. O que faltava: o que fazer quando a
presunção pessimista é **desmentida pelo próprio dado**. O medidor de contexto presumia
200.000 tokens de janela e media 362.593 tokens vivos. Manteve a presunção e imprimiu
`181,3%`, `CRITICO`. Dois estragos: (1) o número é autorrefutável — não existe sessão viva
com mais tokens do que a janela comporta, então a medição prova que a régua está errada;
(2) o alarme saturou no topo da escala e o mecanismo **morreu calado**, porque o aviso só
dispara quando a zona sobe e nada é maior que `critico` — a sessão terminou com um alarme
falso e zero alarmes verdadeiros. O falso verde reprovado no loop anterior virou falso
vermelho permanente: forma diferente, mesmo destino (nenhum aviso na hora certa).

**Lição:** duas regras, que valem para qualquer monitor com limiar presumido:

1. **Presunção refutada pela medição é abandonada, não repetida.** Se o dado é
   incompatível com a hipótese, o monitor sobe ao próximo valor plausível (anunciando a
   refutação) ou declara "não sei" (`sem-telemetria`) — nunca imprime o número impossível.
   Publicar um valor que o próprio dado desmente destrói a credibilidade do canal inteiro:
   quem vê `181%` aprende a ignorar o alarme seguinte, que pode ser verdadeiro.
2. **Alarme que satura no topo da escala deixa de ser alarme.** Todo antirruído baseado em
   "só avisa quando piora" precisa de um caminho de rearme: mudança da régua (limiar,
   janela, unidade) invalida o estado anterior e tem de zerá-lo. Sem rearme, o pior estado
   possível é também o mais silencioso.

**Como aplicar:** ao implementar um monitor com limiar presumido, escrever três testes no
**canal automático** (hook/CI/alerta), não no stdout: (a) medida que refuta a presunção — o
monitor abandona a hipótese e diz por quê; (b) medida acima de todos os valores plausíveis —
o monitor sai como "sem dado", nunca com percentual; (c) sequência de medidas crescentes
depois de um estado alto registrado sob outra régua — o alarme volta a falar. Se o teste (c)
não existir, o monitor pode estar morto desde a primeira medição e ninguém percebe.
