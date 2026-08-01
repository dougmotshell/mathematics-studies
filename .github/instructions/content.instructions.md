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
- `references.json`: apenas fontes gratuitas, com autor, ano, URL, idioma e licença **lida na
  própria página** (nunca de memória — lições `L-006`/`L-007`).
- **Compatibilidade de licença (`ADR-0005`): publicamos sob CC BY-SA 4.0.** Fonte **CC BY**,
  **CC BY-SA**, **CC0** ou de **domínio público** (confirmado na jurisdição) pode ser
  adaptada, com atribuição completa. Fonte **CC BY-NC**, **CC BY-NC-SA**, **ND** ou **sem
  licença declarada** é **só citável**: proibido copiar ou traduzir trecho, exemplo, figura,
  enunciado ou sequência didática dela para `theory.<lang>.md`, `exercises.json` ou
  `assessments.json`. Mnemônico: "NC = leitura, não matéria-prima". Licença ambígua → vale a
  leitura mais restritiva. Árvore de decisão: `docs/content/content-standards.md`.
- Validar com `bash scripts/audit-content.sh` antes de considerar pronto.
