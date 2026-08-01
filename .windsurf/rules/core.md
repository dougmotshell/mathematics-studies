---
trigger: always_on
description: Regras essenciais do mathematics-studies
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# Regras essenciais do mathematics-studies

> Regra **sempre ativa**. A fonte completa é o `AGENTS.md` na raiz do repositório — leia-o
> antes de qualquer tarefa significativa. Este arquivo é o resumo que cabe nos limites de
> tamanho das ferramentas (12.000 caracteres).
>
> Este conteúdo é reaproveitado em vários caminhos (`.cursor/rules/`, `.windsurf/rules/`,
> `.agents/rules/`, `.rules`, `.clinerules`, `.junie/`), então **não use links relativos
> aqui** — cite os caminhos a partir da raiz, como texto.

## O projeto

Plataforma **gratuita** de estudos de matemática, da educação infantil à pesquisa: teoria,
exercícios interativos com feedback diagnóstico e acompanhamento de progresso. Aplicação web
**PWA** com deploy na Vercel. Todo conteúdo é **bilíngue pt-BR + en-US**.

## Regras que não podem ser violadas

1. **Bilinguismo total.** Todo objeto de aprendizagem existe em pt-BR **e** en-US, em
   paridade estrutural e semântica. Enquanto faltar um idioma, `meta.json.status` fica
   `draft`. Nunca publicar monolíngue.
2. **Correção matemática.** Nenhum resultado não trivial vira gabarito sem verificação
   (simbólica, numérica ou demonstração revisada). Erro matemático é falha crítica.
3. **Idioma do repositório.** Nomes de arquivos, pastas, variáveis, funções e identificadores
   em **en-US**; documentação, comentários e textos de time em **pt-BR**.
4. **Slugs são URLs públicas.** `content/<stage>/<area>/<topic>` não se renomeia sem ADR e
   redirect.
5. **Nada de implementação sem spec aprovada** (`docs/specs/`) e sem ADR para decisões
   estruturais. A stack está **decidida** (`docs/adr/ADR-0003-platform-stack.md`,
   `accepted`): site estático com ilhas de interatividade e progresso local-first
   (IndexedDB). **Backend, conta, login e telemetria identificável exigem ADR novo.**
   Também decididos em 2026-08-01: projeto **Astro na raiz** e **URL com prefixo de idioma em
   minúsculas** (`/pt-br/…`, `/en-us/…`, `ADR-0007`); Actions como portão de mérito, Vercel
   publicando por integração Git com previews por PR, **sem segredo no repositório e sem
   analytics do host** (`ADR-0006`).
6. **Acessibilidade WCAG 2.2 AA** é requisito de entrada: teclado, foco visível, contraste,
   fórmulas em KaTeX (nunca imagem de fórmula). Equação em **display** exige leitura textual
   integral logo abaixo; fórmula **inline** exige o **agrupamento dito em palavras** quando
   algum argumento é composto **ou** a base elevada é ambígua — entre parênteses ou com sinal
   unário à frente (`$\frac{5 \pm 1}{2}$`, `$(x+3)^2$`, `$-x^2$` sim; `$\frac{b}{a}$`,
   `$x_1$`, `$ax^2 + bx + c$` não) — regra em `docs/content/accessibility.md`.
7. **Custo zero.** Free tier e soluções estáticas; qualquer gasto exige aprovação explícita.
8. **Privacidade de menores.** O público inclui crianças: minimização de dados; qualquer
   coleta identificável exige ADR tratando LGPD/COPPA **antes** da implementação.
9. **Fontes externas** só gratuitas, com autor, ano, URL e licença registrados. Nunca
   material pirateado nem plágio. **Licença (`ADR-0005`):** conteúdo sai sob CC BY-SA 4.0 e
   código sob MIT; fonte **CC BY / CC BY-SA / CC0 / domínio público** pode ser adaptada, mas
   fonte **CC BY-NC, CC BY-NC-SA, ND ou sem licença** é **só citável** — nunca incorporada
   nem traduzida para dentro do conteúdo.
10. **Não fazer commit, push, deploy ou qualquer gasto sem pedido explícito** do usuário.

## Onde as coisas ficam

| Caminho | Conteúdo |
|---|---|
| `content/` | O acervo entregue ao aluno (bilíngue, público) |
| `docs/` | Como o projeto funciona (interno, pt-BR) |
| `tickets/` | Unidades de trabalho `TCK-NNNN-<slug>/` com log auditável |
| `memory/` | Memória compartilhada: contexto, lições, memória por agente |
| `.claude/agents/` | Definição canônica dos papéis (todos os CLIs usam) |
| `.claude/skills/` | Definição canônica das capacidades (todos os CLIs usam) |

## Fluxo de trabalho

Desenvolvimento, bugs, infra e conteúdo de porte passam por **ticket**:
`new` → `tech-lead` (triagem) → agente da área → `code-reviewer` → `qa-validator` → `done`.

- **Log ou não aconteceu:** toda ação vira entrada no `log.md` do ticket (`[SEQ]`
  incremental, append-only; corrigir = `CORRECTION`).
- **Evidência > afirmação:** "os testes passam" exige a saída do comando.
- Critérios de aceite são a definição de pronto; só o `qa-validator` marca `done`.
- Nenhum agente valida artefato que ele mesmo produziu.
- 3 devoluções no mesmo par → escalar ao `tech-lead`; sem saída → perguntar ao usuário.
- Commits usam prefixo `TCK-NNNN:`.

Contrato completo: `docs/ai/ticket-protocol.md`.

## Memória (antes e depois de cada tarefa)

- **Antes:** ler `memory/MEMORY.md`, `memory/context/<área>.md` da sua área e
  `docs/errors/README.md`.
- **Depois:** atualizar `memory/agents/<seu-papel>.md` e registrar lições novas em
  `memory/lessons/` com os índices. Repetir erro que já tem lição registrada é defeito
  **bloqueante**.

## Papéis e capacidades

Os papéis vivem em `.claude/agents/*.md` e as capacidades em `.claude/skills/*/SKILL.md` —
são **Markdown legível por qualquer ferramenta**. Se o seu CLI não carrega esses arquivos
automaticamente, abra o arquivo do papel/capacidade e siga suas instruções.

Inventário e equivalências por ferramenta: `SLASH_COMMANDS.md` e `docs/ai/tool-support.md`.
