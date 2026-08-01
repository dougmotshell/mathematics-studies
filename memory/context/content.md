# Contexto operacional — content

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01

## Estado atual

- Um nó piloto criado: `content/high-school/algebra/quadratic-equations` (`status: draft`).
  Ele serve de **referência de formato** para novos nós — teoria bilíngue com as sete seções,
  5 exercícios com feedback diagnóstico, `references.json` com licença.
- `bash scripts/audit-content.sh` passa sem erros nem avisos com esse nó.

## Pegadinhas conhecidas

- **SymPy não está instalado no ambiente** (`ModuleNotFoundError: No module named 'sympy'`).
  Para `/math-verify`, a alternativa usada é verificação aritmética/numérica em Python puro
  (discriminante, raízes, substituição de volta na equação) — suficiente para álgebra
  elementar, insuficiente para identidades simbólicas gerais. Se a verificação simbólica for
  necessária, instalar SymPy antes ou declarar a limitação no relatório.
- **Verificação numérica não é demonstração**: para afirmações gerais, declarar isso
  explicitamente (lição L-002).

## Decisões operacionais em vigor

- Antes de fixar qualquer gabarito, resolver o exercício de forma independente **e**
  substituir a resposta na equação original — a substituição pega quase todo erro de sinal.
- Referências externas só entram em `references.json` com autor, ano, URL, idioma e licença.
  **URL precisa ser verificada de fato** (acesso e licença na própria página) antes de o nó
  sair de `draft` — ver TCK-0001.
