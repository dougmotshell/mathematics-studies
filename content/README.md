# content/ — o acervo

Aqui vive o **produto**: o conteúdo entregue ao aluno. Documentação sobre *como o projeto
funciona* fica em [`../docs/`](../docs/) — não misturar os dois planos.

## Endereço canônico

```
content/<stage>/<area>/<topic>/[<subtopic>/]
```

Slugs en-US kebab-case, **estáveis** — são URLs públicas (ADR-0001, lição L-003).

## Estrutura de um nó

| Arquivo | Obrigatório | Conteúdo |
|---|---|---|
| `meta.json` | sim | id, stage, area, título/resumo bilíngues, pré-requisitos, dificuldade, skills, status |
| `theory.pt-BR.md` | sim | Teoria em português (KaTeX) |
| `theory.en-US.md` | sim | Teoria em inglês (KaTeX) |
| `exercises.json` | para publicar | Itens de prática com feedback diagnóstico |
| `assessments.json` | não | Avaliação somativa do nó |
| `references.json` | para publicar | Fontes gratuitas com licença |
| `assets/` | não | Imagens, SVGs, ponteiros de mídia |

Trilhas de aprendizado ficam em `content/paths/<slug>.json`.

## Regras rápidas

1. **Bilíngue sempre** — nó com um idioma só permanece `status: "draft"` (ADR-0002).
2. **Gabarito verificado** antes de publicar (`/math-verify`, lição L-002).
3. **Pré-requisitos** existentes, sem ciclo, de dificuldade ≤ à do nó.
4. **Fontes gratuitas** com licença registrada; nada de material pirateado.
5. Validar com `bash scripts/audit-content.sh`.

## Criando conteúdo

```
/new-topic <stage>/<area>/<topic>      # cria a estrutura completa
/new-exercise-set <caminho do nó>      # popula exercises.json
/content-audit <caminho>               # audita antes de publicar
```

Padrões completos: [`../docs/content/`](../docs/content/).
