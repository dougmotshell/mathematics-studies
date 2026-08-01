---
name: learning-path
description: Desenha uma trilha de aprendizado — sequência de nós de conteúdo com objetivo, pré-requisitos, marcos, avaliações e critério de conclusão. Usar para criar percursos por objetivo do aluno (ex.: "do zero ao cálculo", "preparação para o ENEM", "álgebra linear para machine learning").
---

# Desenhar trilha de aprendizado

## 1. Definir o objetivo do aluno

Escreva em uma frase o que a pessoa saberá fazer ao final, de forma **observável**
("resolver sistemas lineares e interpretar sua geometria"), e para quem é a trilha
(estágio, ponto de partida assumido, tempo disponível).

## 2. Fazer o backward design

Do objetivo para trás:

1. Qual é a **avaliação final** que comprova o objetivo?
2. Quais habilidades (`skills[]`) ela exige?
3. Quais nós de `content/` desenvolvem essas habilidades?
4. Quais pré-requisitos desses nós ainda faltam? (repetir até chegar ao ponto de partida)

## 3. Montar a sequência

- Ordene respeitando o grafo de pré-requisitos (sem ciclos, sem salto de dificuldade > 1).
- Agrupe em **módulos** de 3–6 nós, cada um com um marco verificável.
- Insira **avaliações diagnósticas** no início (para pular o que a pessoa já domina) e
  **avaliações de módulo** ao final de cada bloco.
- Preveja **caminhos de recuperação**: se o aluno errar sistematicamente uma habilidade,
  para qual nó anterior ele volta.
- Estime a duração (soma de `estimatedMinutes` + prática).

## 4. Registrar

Crie/atualize o descritor da trilha (`content/paths/<slug>.json`) com:

```json
{
  "id": "zero-to-calculus",
  "title": { "pt-BR": "…", "en-US": "…" },
  "goal": { "pt-BR": "…", "en-US": "…" },
  "audience": { "stage": "high-school", "assumedKnowledge": ["…"] },
  "modules": [
    { "title": { "pt-BR": "…", "en-US": "…" },
      "nodes": ["middle-school/algebra/linear-equations"],
      "milestone": { "pt-BR": "…", "en-US": "…" } }
  ],
  "diagnostics": ["…"],
  "completionCriteria": { "pt-BR": "…", "en-US": "…" },
  "estimatedHours": 40
}
```

## 5. Validar

- Todos os nós citados existem e estão `published`? Liste os que faltam criar.
- Diagrama Mermaid (`flowchart LR`) da trilha, com os módulos e os caminhos de recuperação.
- Rode `bash scripts/audit-content.sh` para checar pré-requisitos e ciclos.
- Peça revisão ao `curriculum-architect`.
