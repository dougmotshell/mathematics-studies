---
trigger: glob
description: Instruções para `content/` (acervo entregue ao aluno)
globs: content/**
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# Instruções para `content/` (acervo entregue ao aluno)

- Endereço canônico: `content/<stage>/<area>/<topic>/[<subtopic>/]` — slugs en-US kebab-case
  **estáveis** (são URLs públicas; renomear exige ADR + redirect). Ver
  `docs/content/taxonomy.md`.
- **Bilinguismo obrigatório**: `theory.pt-BR.md` **e** `theory.en-US.md`, equivalentes em
  seções e exemplos; campos localizados como `{"pt-BR": …, "en-US": …}`. Enquanto faltar um
  idioma, `meta.json.status` fica `draft` (ADR-0002).
- Estrutura mínima da teoria: objetivo → pré-requisitos → intuição → definição formal →
  exemplos resolvidos → erros comuns → resumo (`docs/content/content-standards.md`).
- Matemática em KaTeX (`$…$`, `$$…$$`); **nunca** fórmula como imagem.
- **Acessibilidade da fórmula, display e inline:** equação em **display** exige leitura
  integral logo abaixo (`*Leitura:*` / `*Reading:*`), reconstruindo a fórmula inteira na
  ordem escrita. Fórmula **inline** exige o **agrupamento dito em palavras** no texto ao
  redor quando algum argumento (numerador, denominador, radicando, expoente, subscrito ou
  base) for **composto** — operador, relação, fatores justapostos (`2a`), agrupamento
  aninhado ou parênteses — **ou** quando a base elevada for ambígua na fala: entre parênteses
  (`$(-5)^2$`, `$(x+3)^2$`) ou com sinal unário à frente (`$-x^2$`). Assim
  `$\frac{5 \pm 1}{2}$`, `$(x+3)^2$` e `$-x^2$` exigem; `$\frac{b}{a}$`, `$x_1$` e
  `$ax^2 + bx + c$` não. Também em `exercises.json` e `assessments.json`, dentro do próprio
  campo de texto e nos dois idiomas. Teste e convenções de leitura:
  `docs/content/accessibility.md`.
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
