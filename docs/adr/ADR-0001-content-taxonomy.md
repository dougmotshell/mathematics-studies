# ADR-0001 — Taxonomia de conteúdo por estágio, área e tópico

- **Status:** accepted
- **Data:** 2026-08-01
- **Decisores:** Douglas Silva
- **Relacionados:** ADR-0002, `docs/content/taxonomy.md`

## Contexto

A plataforma cobre da educação infantil à pesquisa. Sem um endereçamento único e estável,
conteúdo equivalente acaba duplicado em lugares diferentes, o grafo de pré-requisitos não se
sustenta e URLs públicas mudam depois de circularem.

Restrições: conteúdo bilíngue, navegação por dificuldade/estágio/assunto, links precisam
sobreviver a reorganizações, e a estrutura precisa ser legível por humanos e por scripts de
build.

## Alternativas consideradas

### A. Hierarquia por estágio → área → tópico (escolhida)
- **Prós:** corresponde à forma como aluno e professor procuram; permite navegação por nível;
  slug curto e legível; fácil de auditar.
- **Contras:** um mesmo assunto pode aparecer em mais de um estágio (com abordagens
  diferentes) — exige disciplina para não duplicar.

### B. Grafo plano de tópicos com tags (sem hierarquia de pastas)
- **Prós:** evita duplicação; flexível.
- **Contras:** sem caminho natural de navegação; URL sem contexto; difícil de auditar
  manualmente; ordem de aprendizado depende inteiramente de metadados.

### C. Hierarquia por área → estágio
- **Prós:** boa para quem estuda uma área inteira.
- **Contras:** ruim para o caso mais comum (aluno de um nível procurando o que estudar
  agora).

## Decisão

O endereço canônico de todo conteúdo é `content/<stage>/<area>/<topic>/[<subtopic>/]`, com
slugs en-US kebab-case **estáveis**, complementado por metadados (`prerequisites`,
`difficulty`, `tags`, `skills`) que sustentam navegação alternativa e trilhas.

## Consequências

**Positivas**
- Navegação previsível por estágio e por área; URL autoexplicativa.
- Grafo de pré-requisitos auditável por script (`scripts/audit-content.sh`).
- Trilhas (`content/paths/`) podem atravessar a hierarquia sem duplicar conteúdo.

**Negativas / custos assumidos**
- Assunto que aparece em dois estágios exige decisão consciente: nó novo com abordagem
  distinta e referência cruzada, nunca cópia.
- A lista de áreas precisa de governança (critério de inclusão em `docs/content/taxonomy.md`).

**O que fica mais difícil depois desta decisão**
- Reorganizar a hierarquia depois de o conteúdo circular: exige ADR e redirects.

## Impacto

- **Conteúdo:** define a estrutura de pastas e o `meta.json` de todo nó.
- **Plataforma:** as rotas públicas derivam diretamente do caminho do nó.
- **Processo/agentes:** `curriculum-architect` é o dono da taxonomia; `/new-topic` a aplica.

## Como reverter

Reversível apenas com migração completa + redirects permanentes; o custo cresce com o volume
de conteúdo publicado. Na prática, tratar como decisão de longo prazo.
