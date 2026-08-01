# Equações do segundo grau

## Objetivo de aprendizagem

Ao final deste tópico, você será capaz de reconhecer uma equação do segundo grau, identificar
seus coeficientes, prever quantas raízes reais ela tem usando o discriminante e resolvê-la
pela fórmula geral.

## Pré-requisitos

- Operações com números reais, incluindo sinais e raiz quadrada.
- Resolução de equações do primeiro grau.
- Manipulação de expressões algébricas (fatoração básica e produtos notáveis).

## Intuição

Uma equação do primeiro grau, como $2x - 6 = 0$, pergunta "qual número, depois de dobrado e
diminuído de 6, dá zero?". Há sempre exatamente uma resposta.

Quando aparece um $x^2$, a situação muda. Elevar ao quadrado apaga o sinal: $3^2$ e $(-3)^2$
dão o mesmo resultado. Por isso uma equação do segundo grau pode ter **duas** respostas, uma
só, ou nenhuma resposta real — e é possível descobrir **qual desses três casos** ocorre
antes de calcular qualquer raiz.

Geometricamente, resolver $ax^2 + bx + c = 0$ é perguntar em quantos pontos a parábola
$y = ax^2 + bx + c$ cruza o eixo horizontal: dois pontos, um ponto (ela apenas encosta) ou
nenhum (ela passa inteira acima ou abaixo do eixo).

## Definição formal

Uma **equação do segundo grau** (ou quadrática) na incógnita $x$ é toda equação que pode ser
escrita na forma

$$ax^2 + bx + c = 0, \qquad a, b, c \in \mathbb{R}, \quad a \neq 0.$$

*Leitura:* a vezes x ao quadrado, mais b vezes x, mais c, igual a zero, com a, b e c reais e
a diferente de zero.

A condição $a \neq 0$ é essencial: se $a = 0$, a equação deixa de ser do segundo grau e passa
a ser do primeiro.

Define-se o **discriminante** da equação como

$$\Delta = b^2 - 4ac.$$

*Leitura:* delta é igual a b ao quadrado menos quatro a c.

**Teorema (fórmula geral).** Se $a \neq 0$, as soluções reais de $ax^2 + bx + c = 0$ são
dadas por

$$x = \frac{-b \pm \sqrt{\Delta}}{2a}, \qquad \Delta = b^2 - 4ac,$$

*Leitura:* x é igual a menos b, mais ou menos a raiz quadrada de delta, tudo dividido por
dois a.

e o número de raízes reais é determinado pelo sinal de $\Delta$:

| Sinal de $\Delta$ | Raízes reais | Parábola e o eixo $x$ |
|---|---|---|
| $\Delta > 0$ | duas raízes distintas | cruza em dois pontos |
| $\Delta = 0$ | uma raiz (dupla) | encosta em um ponto |
| $\Delta < 0$ | nenhuma raiz real | não cruza |

Quando existem duas raízes $x_1$ e $x_2$, valem as **relações de Girard**:

$$x_1 + x_2 = -\frac{b}{a}, \qquad x_1 \cdot x_2 = \frac{c}{a}.$$

## Exemplos resolvidos

### Exemplo 1 — duas raízes

Resolver $x^2 - 5x + 6 = 0$.

Coeficientes: $a = 1$, $b = -5$, $c = 6$.

$$\Delta = (-5)^2 - 4 \cdot 1 \cdot 6 = 25 - 24 = 1 > 0,$$

logo há duas raízes reais distintas:

$$x = \frac{-(-5) \pm \sqrt{1}}{2 \cdot 1} = \frac{5 \pm 1}{2}
\;\Longrightarrow\; x_1 = 3, \quad x_2 = 2.$$

**Conferindo:** $3^2 - 5\cdot3 + 6 = 9 - 15 + 6 = 0$ e $2^2 - 5\cdot2 + 6 = 4 - 10 + 6 = 0$.
Substituir de volta é o modo mais barato de detectar um erro de sinal.

### Exemplo 2 — nenhuma raiz real

Resolver $x^2 - 4x + 5 = 0$.

Coeficientes: $a = 1$, $b = -4$, $c = 5$. Então

$$\Delta = (-4)^2 - 4 \cdot 1 \cdot 5 = 16 - 20 = -4 < 0.$$

Como $\Delta < 0$, a equação **não tem raiz real**. A parábola $y = x^2 - 4x + 5$ tem
concavidade para cima e vértice acima do eixo $x$, portanto nunca o toca.

### Exemplo 3 — determinando um coeficiente

Para quais valores de $k$ a equação $x^2 + kx + 9 = 0$ tem uma única raiz real?

Uma única raiz significa $\Delta = 0$:

$$k^2 - 4 \cdot 1 \cdot 9 = 0 \;\Longrightarrow\; k^2 = 36 \;\Longrightarrow\; k = 6
\ \text{ou} \ k = -6.$$

Repare que a condição produziu **dois** valores de $k$ — cada um deles gera uma equação com
uma única raiz. Confundir "uma raiz em $x$" com "uma resposta em $k$" é um erro frequente.

## Erros comuns

| Erro | Por que acontece | Como evitar |
|---|---|---|
| Calcular $\Delta = b^2 + 4ac$ | Esquecimento do sinal negativo na fórmula | Escrever $\Delta = b^2 - 4ac$ antes de substituir números |
| Errar o sinal de $b$ quando $b < 0$ | $-b$ com $b = -5$ vira $+5$, e $(-5)^2$ vira $+25$ | Substituir sempre entre parênteses: $(-5)^2$ |
| Dividir só um termo por $2a$ | Ler a fração como $-b \pm \frac{\sqrt{\Delta}}{2a}$ | Lembrar que a barra de fração agrupa todo o numerador |
| Aplicar a fórmula com $a = 0$ | Não verificar a condição da definição | Conferir $a \neq 0$ antes de tudo |
| Dizer "não tem solução" quando $\Delta < 0$ | Confundir ausência de raiz **real** com ausência total | Dizer "não tem raiz real"; em $\mathbb{C}$ existem duas |
| Esquecer de simplificar ou conferir | Pressa | Substituir as raízes na equação original |

## Resumo

- Uma equação do segundo grau tem a forma $ax^2 + bx + c = 0$ com $a \neq 0$.
- O discriminante $\Delta = b^2 - 4ac$ diz **quantas** raízes reais existem antes de
  calculá-las: duas se $\Delta > 0$, uma se $\Delta = 0$, nenhuma se $\Delta < 0$.
- As raízes reais são $x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$.
- Soma e produto das raízes: $-\dfrac{b}{a}$ e $\dfrac{c}{a}$.
- Substituir a resposta na equação original é a verificação mais rápida.
