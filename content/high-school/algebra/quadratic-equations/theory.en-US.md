# Quadratic equations

## Learning objective

By the end of this topic you will be able to recognize a quadratic equation, identify its
coefficients, predict how many real roots it has using the discriminant, and solve it with
the quadratic formula.

## Prerequisites

- Operations with real numbers, including signs and square roots.
- Solving linear equations.
- Manipulating algebraic expressions (basic factoring and special products).

## Intuition

A linear equation such as $2x - 6 = 0$ asks "which number, once doubled and decreased by 6,
gives zero?". There is always exactly one answer.

Once $x^2$ shows up, things change. Squaring erases the sign: $3^2$ and $(-3)^2$ give the
same result. That is why a quadratic equation may have **two** answers, exactly one, or no
real answer at all — and it is possible to find out **which of the three cases** applies
before computing any root.

Geometrically, solving $ax^2 + bx + c = 0$ asks in how many points the parabola
$y = ax^2 + bx + c$ crosses the horizontal axis: two points, one point (it just touches), or
none (it stays entirely above or below the axis).

## Formal definition

A **quadratic equation** in the unknown $x$ is any equation that can be written as

$$ax^2 + bx + c = 0, \qquad a, b, c \in \mathbb{R}, \quad a \neq 0.$$

*Reading:* a times x squared, plus b times x, plus c, equals zero, with a, b and c real and
a different from zero.

The condition $a \neq 0$ is essential: if $a = 0$ the equation is no longer quadratic, it is
linear.

The **discriminant** of the equation is defined as

$$\Delta = b^2 - 4ac.$$

*Reading:* delta equals b squared minus four a c.

**Theorem (quadratic formula).** If $a \neq 0$, the real solutions of $ax^2 + bx + c = 0$ are
given by

$$x = \frac{-b \pm \sqrt{\Delta}}{2a}, \qquad \Delta = b^2 - 4ac,$$

*Reading:* x equals minus b, plus or minus the square root of delta, all divided by two a,

and the number of real roots is determined by the sign of $\Delta$:

| Sign of $\Delta$ | Real roots | Parabola and the $x$-axis |
|---|---|---|
| $\Delta > 0$ | two distinct roots | crosses at two points |
| $\Delta = 0$ | one (double) root | touches at one point |
| $\Delta < 0$ | no real root | does not cross |

When two roots $x_1$ and $x_2$ exist, **Vieta's formulas** hold:

$$x_1 + x_2 = -\frac{b}{a}, \qquad x_1 \cdot x_2 = \frac{c}{a}.$$

*Reading:* x subscript 1 plus x subscript 2 equals minus b divided by a; and x subscript 1
times x subscript 2 equals c divided by a.

## Worked examples

### Example 1 — two roots

Solve $x^2 - 5x + 6 = 0$.

Coefficients: $a = 1$, $b = -5$, $c = 6$.

$$\Delta = (-5)^2 - 4 \cdot 1 \cdot 6 = 25 - 24 = 1 > 0,$$

*Reading:* delta equals open parenthesis minus five close parenthesis squared, minus four
times one times six, equals twenty-five minus twenty-four, equals one, which is greater than
zero.

so there are two distinct real roots:

$$x = \frac{-(-5) \pm \sqrt{1}}{2 \cdot 1} = \frac{5 \pm 1}{2}
\;\Longrightarrow\; x_1 = 3, \quad x_2 = 2.$$

*Reading:* x equals minus, open parenthesis minus five close parenthesis, plus or minus the
square root of one, all divided by two times one; that equals five plus or minus one, all
divided by two; which implies x subscript 1 equals three and x subscript 2 equals two.

**Checking:** $3^2 - 5\cdot3 + 6 = 9 - 15 + 6 = 0$ and $2^2 - 5\cdot2 + 6 = 4 - 10 + 6 = 0$.
Substituting back is the cheapest way to catch a sign mistake.

### Example 2 — no real root

Solve $x^2 - 4x + 5 = 0$.

Coefficients: $a = 1$, $b = -4$, $c = 5$. Then

$$\Delta = (-4)^2 - 4 \cdot 1 \cdot 5 = 16 - 20 = -4 < 0.$$

*Reading:* delta equals open parenthesis minus four close parenthesis squared, minus four
times one times five, equals sixteen minus twenty, equals minus four, which is less than zero.

Since $\Delta < 0$, the equation has **no real root**. The parabola $y = x^2 - 4x + 5$ opens
upwards and its vertex lies above the $x$-axis, so it never touches it.

### Example 3 — finding a coefficient

For which values of $k$ does $x^2 + kx + 9 = 0$ have exactly one real root?

Exactly one root means $\Delta = 0$:

$$k^2 - 4 \cdot 1 \cdot 9 = 0 \;\Longrightarrow\; k^2 = 36 \;\Longrightarrow\; k = 6
\ \text{or} \ k = -6.$$

*Reading:* k squared minus four times one times nine equals zero, which implies k squared
equals thirty-six, which implies k equals six or k equals minus six.

Notice that the condition produced **two** values of $k$ — each one yields an equation with a
single root. Confusing "one root in $x$" with "one answer in $k$" is a frequent mistake.

## Common mistakes

| Mistake | Why it happens | How to avoid it |
|---|---|---|
| Computing $\Delta = b^2 + 4ac$ | Forgetting the minus sign in the formula | Write $\Delta = b^2 - 4ac$ before plugging in numbers |
| Getting the sign of $b$ wrong when $b < 0$ | $-b$ with $b = -5$ becomes $+5$, and $(-5)^2$ becomes $+25$ | Always substitute inside parentheses: $(-5)^2$ |
| Dividing only one term by $2a$ | Reading the fraction as $-b \pm \frac{\sqrt{\Delta}}{2a}$ | Remember the fraction bar groups the whole numerator |
| Using the formula with $a = 0$ | Not checking the definition's condition | Check $a \neq 0$ first |
| Saying "no solution" when $\Delta < 0$ | Confusing "no **real** root" with "no solution at all" | Say "no real root"; over $\mathbb{C}$ there are two |
| Skipping the check | Rushing | Substitute the roots back into the original equation |

## Summary

- A quadratic equation has the form $ax^2 + bx + c = 0$ with $a \neq 0$.
- The discriminant $\Delta = b^2 - 4ac$ tells you **how many** real roots exist before
  computing them: two if $\Delta > 0$, one if $\Delta = 0$, none if $\Delta < 0$.
- The real roots are $x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$.
- Sum and product of the roots: $-\dfrac{b}{a}$ and $\dfrac{c}{a}$.
- Substituting your answer back into the original equation is the fastest check.
