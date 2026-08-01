---
name: new-topic
description: Cria um nó de conteúdo completo na taxonomia (content/<stage>/<area>/<topic>/[<subtopic>]) com meta.json, teoria bilíngue, exercícios, referências e assets. Usar sempre que um assunto novo entrar na plataforma.
---

# Criar nó de conteúdo

## 1. Posicionar na taxonomia

Antes de criar qualquer arquivo, decida (ou peça ao agente `curriculum-architect`):

- **stage**: `early-childhood` | `elementary` | `middle-school` | `high-school` |
  `undergraduate` | `graduate` | `research`
- **area**: ver lista canônica em `docs/content/taxonomy.md`
- **topic** / **subtopic**: slug en-US kebab-case, **estável** (é URL pública)
- **prerequisites**: IDs de nós existentes, todos de dificuldade ≤ a deste nó, sem ciclo
- **difficulty**: 1–5 dentro do estágio

Se o assunto já existe em outro estágio, **não duplique**: crie um nó com abordagem
diferente e referencie o irmão, ou estenda o existente.

## 2. Criar a estrutura

```
content/<stage>/<area>/<topic>/[<subtopic>/]
├── meta.json
├── theory.pt-BR.md
├── theory.en-US.md
├── exercises.json
├── references.json
└── assets/
```

`meta.json` (contrato completo em `docs/content/taxonomy.md`):

```json
{
  "id": "high-school/algebra/quadratic-equations",
  "stage": "high-school",
  "area": "algebra",
  "title": { "pt-BR": "Equações do segundo grau", "en-US": "Quadratic equations" },
  "summary": { "pt-BR": "…", "en-US": "…" },
  "prerequisites": ["middle-school/algebra/linear-equations"],
  "difficulty": 3,
  "estimatedMinutes": 45,
  "tags": ["equations", "polynomials"],
  "skills": ["solve-quadratic", "interpret-discriminant"],
  "status": "draft",
  "languages": ["pt-BR", "en-US"],
  "updatedAt": "2026-08-01"
}
```

## 3. Escrever a teoria (os dois idiomas)

Estrutura mínima obrigatória (`docs/content/content-standards.md`):

1. **Objetivo de aprendizagem** — o que o aluno saberá fazer ao final
2. **Pré-requisitos** — com link para os nós
3. **Intuição** — a ideia antes do formalismo
4. **Definição formal** — enunciados precisos, hipóteses explícitas
5. **Exemplos resolvidos** — passo a passo, do simples ao não rotineiro
6. **Erros comuns** — o equívoco típico e por que ele acontece
7. **Resumo** — o que levar

Regras: KaTeX (`$…$`, `$$…$$`); toda equação em display com descrição textual; linguagem
calibrada ao estágio; **as duas versões equivalentes** (mesmas seções, mesmos exemplos).

## 4. Exercícios e referências

- Gere os exercícios com `/new-exercise-set` (schema em `docs/content/exercise-schema.md`).
- `references.json`: só fontes **gratuitas**, com `author`, `year`, `url`, `language`,
  `license` e `covers`.

## 5. Fechar

- Verifique resultados não triviais com `/math-verify`.
- Rode `bash scripts/audit-content.sh` (estrutura, paridade, schema, ciclos).
- Mantenha `status: "draft"` até teoria + exercícios + referências estarem completos nos
  dois idiomas; só então `"published"`.
- Peça revisão a `math-reviewer` e `i18n-steward`.
