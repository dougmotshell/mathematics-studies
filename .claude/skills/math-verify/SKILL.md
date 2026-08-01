---
name: math-verify
description: Verifica computacional ou simbolicamente uma afirmação matemática, um gabarito ou uma manipulação algébrica antes de publicá-la. Usar sempre que um resultado não trivial for afirmado como verdadeiro.
---

# Verificar afirmação matemática

Nenhum resultado não trivial vira conteúdo publicado sem passar por aqui ou por uma
demonstração explícita e revisada (AGENTS.md §9).

## 1. Formalizar a afirmação

Reescreva o que será verificado de forma inequívoca: enunciado, **hipóteses**, domínio das
variáveis e o que exatamente se afirma. Boa parte dos erros aparece já nesta etapa (hipótese
omitida, domínio implícito, quantificador trocado).

## 2. Escolher o método

| Situação | Método |
|---|---|
| Identidade algébrica, derivada, integral, limite, série | **Simbólico** (SymPy): `simplify(lhs - rhs) == 0` |
| Equação com solução fechada | Resolver simbolicamente e **substituir de volta** |
| Desigualdade / conjectura | **Amostragem numérica ampla** + busca de contra-exemplo nas fronteiras |
| Combinatória / teoria dos números | **Enumeração exaustiva** em faixa pequena vs fórmula |
| Geometria | Coordenadas + verificação numérica, ou construção simbólica |
| Probabilidade | Fórmula vs **simulação** (Monte Carlo) com margem declarada |
| Resultado com demonstração conhecida | Demonstração escrita passo a passo + revisão do `math-reviewer` |

## 3. Executar

Use Python (SymPy/NumPy) no scratchpad da sessão — **nunca** deixe scripts de verificação
soltos em `content/`:

```python
import sympy as sp
x = sp.symbols('x', real=True)
lhs = (x + 1)**2
rhs = x**2 + 2*x + 1
assert sp.simplify(lhs - rhs) == 0
```

Se a biblioteca não estiver disponível, faça verificação numérica manual em pontos
representativos e **declare a limitação**.

## 4. Testar as fronteiras (obrigatório)

Zero, negativos, denominador nulo, conjunto vazio, igualdade em desigualdades, casos
degenerados (triângulo colinear, matriz singular), extremos do domínio, ±∞.

## 5. Relatar

- **Veredito**: `confirmado` | `refutado` | `inconclusivo`
- **Método** usado e o que foi executado
- **Contra-exemplo**, se houver (com os valores exatos)
- **Hipóteses que precisam ser adicionadas** ao enunciado
- **O que não foi verificado** — nunca declare verificação mais forte do que a feita

Verificação numérica **não é demonstração**: para afirmações gerais, diga explicitamente
que a evidência é numérica e aponte a necessidade de prova.
