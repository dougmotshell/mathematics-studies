# Schema de exercícios e avaliações

Define `exercises.json` (prática) e `assessments.json` (avaliação somativa). Ambos usam a
mesma estrutura de item.

## Estrutura do arquivo

```json
{
  "nodeId": "high-school/algebra/quadratic-equations",
  "version": 1,
  "items": [ /* … itens … */ ]
}
```

## Item

```json
{
  "id": "qe-007",
  "type": "multiple-choice",
  "difficulty": 3,
  "skills": ["interpret-discriminant"],
  "bloom": "analyze",
  "stem": {
    "pt-BR": "Qual é o número de raízes reais de $x^2 - 4x + 5 = 0$?",
    "en-US": "How many real roots does $x^2 - 4x + 5 = 0$ have?"
  },
  "options": [
    {
      "id": "a",
      "text": { "pt-BR": "Nenhuma", "en-US": "None" },
      "correct": true,
      "feedback": {
        "pt-BR": "Isso: $\\Delta = 16 - 20 = -4 < 0$, então não há raiz real.",
        "en-US": "Right: $\\Delta = 16 - 20 = -4 < 0$, so there is no real root."
      }
    },
    {
      "id": "b",
      "text": { "pt-BR": "Duas", "en-US": "Two" },
      "correct": false,
      "feedback": {
        "pt-BR": "Você provavelmente calculou $\\Delta = 16 + 20$: atenção ao sinal de $-4ac$ quando $c > 0$.",
        "en-US": "You likely computed $\\Delta = 16 + 20$: mind the sign of $-4ac$ when $c > 0$."
      }
    }
  ],
  "hints": [
    { "pt-BR": "O sinal de $\\Delta$ decide a quantidade de raízes reais.", "en-US": "The sign of $\\Delta$ decides the number of real roots." },
    { "pt-BR": "Calcule $\\Delta = b^2 - 4ac$ com $a=1$, $b=-4$, $c=5$.", "en-US": "Compute $\\Delta = b^2 - 4ac$ with $a=1$, $b=-4$, $c=5$." }
  ],
  "solution": {
    "pt-BR": "$\\Delta = (-4)^2 - 4\\cdot1\\cdot5 = 16 - 20 = -4$. Como $\\Delta < 0$, não há raízes reais.",
    "en-US": "$\\Delta = (-4)^2 - 4\\cdot1\\cdot5 = 16 - 20 = -4$. Since $\\Delta < 0$, there are no real roots."
  },
  "estimatedSeconds": 90,
  "verified": { "method": "sympy", "date": "2026-08-01" }
}
```

## Campos

| Campo | Obrigatório | Regra |
|---|---|---|
| `id` | sim | Único no arquivo; prefixo curto do tópico + número |
| `type` | sim | Ver tabela de tipos |
| `difficulty` | sim | 1–5, relativo ao estágio do nó |
| `skills` | sim | Pelo menos uma; deve existir em `meta.json.skills` |
| `bloom` | não | `remember` \| `understand` \| `apply` \| `analyze` \| `evaluate` \| `create` |
| `stem` | sim | Bilíngue; KaTeX permitido |
| `options` | se `multiple-choice`/`true-false`/`matching` | Ver regras abaixo |
| `answer` | se `numeric`/`short-answer`/`ordering` | Formato de máquina (ponto decimal) |
| `tolerance` | se `numeric` | Absoluta ou relativa; declarar qual |
| `unit` | não | Quando aplicável |
| `hints` | sim | 2–3, progressivas |
| `solution` | sim | Passo a passo bilíngue, com justificativa dos passos |
| `estimatedSeconds` | não | Ajuda no planejamento de trilha |
| `verified` | sim para publicar | Método e data da verificação (lição L-002) |
| `rubric` | se `proof`/`step-by-step` | Critérios de avaliação da resposta aberta |

## Tipos

| Tipo | Uso | Verificação |
|---|---|---|
| `multiple-choice` | Discriminação de conceito, diagnóstico de equívoco | Exata |
| `true-false` | Verificação rápida de enunciado | Exata (exigir justificativa em nível avançado) |
| `numeric` | Cálculo com resposta numérica | Com `tolerance` |
| `short-answer` | Expressão algébrica ou termo | Normalização + equivalência simbólica |
| `ordering` | Sequência de passos, ordenação de valores | Sequência exata |
| `matching` | Associação conceito ↔ definição/gráfico | Pareamento completo |
| `step-by-step` | Resolução guiada por etapas | Por etapa, com feedback em cada uma |
| `proof` | Demonstração | Rubrica; revisão humana/agente |

## Regras duras

1. **Feedback diagnóstico**: cada alternativa errada explica **qual equívoco** leva a ela.
   "Resposta incorreta" é rejeitado em revisão.
2. **Nunca duas alternativas corretas** em `multiple-choice` (salvo tipo explícito de
   múltipla resposta, que deve ser declarado no enunciado).
3. **Distratores plausíveis**, derivados de erros reais — nada de opção absurda de enchimento.
4. **Dicas não entregam a resposta**; reduzem o espaço de busca.
5. **Bilinguismo integral**: `stem`, `options`, `hints`, `solution`, `feedback`.
6. **Gabarito verificado** antes de publicar (`/math-verify`), com o campo `verified`
   preenchido.
7. **Sem dependência de tempo** para responder (acessibilidade).
8. Conjunto padrão: 8–12 itens cobrindo dificuldade 1→5 e todas as `skills` do nó.

## Validação

`scripts/audit-content.sh` verifica presença de campos obrigatórios, bilinguismo, `skills`
existentes no `meta.json`, unicidade de `id` e ausência de múltiplas alternativas corretas.
