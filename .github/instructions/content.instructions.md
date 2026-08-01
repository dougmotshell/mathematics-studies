---
applyTo: "content/**"
---

# Instruções para `content/` (acervo entregue ao aluno)

- Endereço canônico: `content/<stage>/<area>/<topic>/[<subtopic>/]` — slugs en-US kebab-case
  **estáveis** (são URLs públicas; renomear exige ADR + redirect). Ver
  `docs/content/taxonomy.md`.
- **Bilinguismo obrigatório**: `theory.pt-BR.md` **e** `theory.en-US.md`, equivalentes em
  seções e exemplos; campos localizados como `{"pt-BR": …, "en-US": …}`. Enquanto faltar um
  idioma, `meta.json.status` fica `draft` (ADR-0002).
- Estrutura mínima da teoria: objetivo → pré-requisitos → intuição → definição formal →
  exemplos resolvidos → erros comuns → resumo (`docs/content/content-standards.md`).
- Matemática em KaTeX (`$…$`, `$$…$$`); **nunca** fórmula como imagem; toda equação em
  display precisa de descrição textual (`docs/content/accessibility.md`).
- Exercícios seguem `docs/content/exercise-schema.md`: feedback **diagnóstico** por
  alternativa errada, dicas progressivas, solução passo a passo, `skills` declaradas.
- **Gabarito só depois de verificado** (`/math-verify`), com o campo `verified` preenchido.
- `references.json`: apenas fontes gratuitas, com autor, ano, URL, idioma e licença.
- Validar com `bash scripts/audit-content.sh` antes de considerar pronto.
