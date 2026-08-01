---
name: new-exercise-set
description: Cria um conjunto de exercícios ou uma avaliação para um nó de conteúdo, com gradiente de dificuldade, feedback diagnóstico por alternativa, dicas progressivas e metadados. Usar para popular exercises.json e assessments.json.
---

# Criar conjunto de exercícios

## 1. Entender o alvo

Leia `meta.json` e `theory.pt-BR.md` do nó. Liste as **habilidades** (`skills[]`) que o nó
promete desenvolver — cada exercício exercita pelo menos uma delas explicitamente.

## 2. Projetar o conjunto

Um conjunto padrão tem 8–12 itens com este gradiente:

| Faixa | Dificuldade | Propósito |
|---|---|---|
| 1–2 itens | 1 | Reconhecimento / vocabulário |
| 3–4 itens | 2–3 | Aplicação direta do procedimento |
| 2–3 itens | 3–4 | Aplicação com obstáculo (caso-limite, forma não canônica) |
| 1–2 itens | 4–5 | Transferência: contexto novo, múltiplos passos, justificar |

Tipos disponíveis (`docs/content/exercise-schema.md`): `multiple-choice`, `numeric`,
`short-answer`, `true-false`, `ordering`, `matching`, `step-by-step`, `proof`.

## 3. Escrever cada item

```json
{
  "id": "qe-007",
  "type": "multiple-choice",
  "difficulty": 3,
  "skills": ["interpret-discriminant"],
  "stem": { "pt-BR": "…$\\Delta$…", "en-US": "…$\\Delta$…" },
  "options": [
    { "id": "a", "text": { "pt-BR": "…", "en-US": "…" }, "correct": false,
      "feedback": { "pt-BR": "Você trocou o sinal de $b$ ao elevar ao quadrado.",
                    "en-US": "You flipped the sign of $b$ when squaring." } }
  ],
  "hints": [ { "pt-BR": "…", "en-US": "…" } ],
  "solution": { "pt-BR": "…", "en-US": "…" },
  "estimatedSeconds": 90
}
```

**Regras duras:**

- Feedback de alternativa errada **diagnostica o equívoco** ("você somou os expoentes em vez
  de multiplicá-los"). Feedback genérico ("resposta incorreta") é rejeitado na revisão.
- Distratores derivam de erros reais e plausíveis; nunca opções absurdas de enchimento;
  **nunca duas alternativas corretas**.
- Dicas progressivas (2–3) reduzem o espaço de busca sem entregar a resposta.
- Solução passo a passo, com a justificativa de cada passo.
- Itens `numeric` declaram `tolerance` e `unit` quando aplicável.
- Enunciado bilíngue e matematicamente idêntico; decimais conforme o idioma
  (`docs/content/i18n.md`).
- Sem contexto que exija conhecimento externo à matemática ou culturalmente restrito.

## 4. Verificar

- Resolva cada item de forma independente **antes** de fixar o gabarito.
- Rode `/math-verify` nos resultados não triviais.
- Rode `bash scripts/audit-content.sh` para validar o schema.
- Peça revisão a `math-reviewer` (gabaritos) e `i18n-steward` (paridade).
