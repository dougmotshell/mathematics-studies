---
name: c4-diagram
description: Cria ou atualiza diagramas C4 (Context, Container, Component) em Mermaid dentro de docs/architecture/. Usar ao documentar a arquitetura da plataforma, o pipeline de conteúdo ou a superfície de IA.
---

# Criar diagrama C4

1. Determine o **nível** adequado:
   - **Context** (`C4Context`): a plataforma e seus atores externos (aluno, contribuidor,
     Vercel, fontes externas de conteúdo).
   - **Container** (`C4Container`): aplicação web/PWA, pipeline de build do conteúdo,
     armazenamento de progresso, serviços auxiliares.
   - **Component** (`C4Component`): dentro de um container (ex.: renderizador de conteúdo,
     motor de exercícios, módulo de progresso).
2. Crie ou atualize o arquivo em `docs/architecture/` com nome en-US kebab-case
   (`c4-context.md`, `c4-container-web-app.md`, …).
3. Escreva o diagrama em **Mermaid** e acompanhe-o de:
   - **leitura do diagrama** em 3–6 linhas (o que ele mostra e o que não mostra);
   - **fontes**: ADRs e specs que sustentam o desenho;
   - **estado**: o que já existe × o que é proposta (marcar claramente).
4. Não desenhe arquitetura ainda não decidida como se fosse fato — enquanto o ADR de stack
   estiver `proposed`, rotular os elementos como *proposto*.
5. Atualize o índice `docs/architecture/README.md`.
