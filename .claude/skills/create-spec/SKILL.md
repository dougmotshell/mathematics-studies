---
name: create-spec
description: Inicia trabalho novo pelo fluxo Spec-Driven Development em docs/specs/<slug>/ — spec.md (o quê/por quê) → plan.md (como) → tasks.md (passos executáveis). Usar antes de qualquer implementação de funcionalidade ou iniciativa de conteúdo de porte.
---

# Criar spec (Spec-Driven Development)

Nenhuma implementação começa sem spec aprovada (AGENTS.md §8).

1. Escolha um slug en-US kebab-case e crie `docs/specs/<slug>/`.
2. Copie os templates de `docs/specs/templates/` e preencha **nesta ordem**:

   **`spec.md` — o quê e por quê**
   - Problema e quem sofre com ele (aluno? contribuidor? mantenedor?);
   - Resultado esperado e **critérios de aceite verificáveis**;
   - Requisitos obrigatórios do projeto que se aplicam: bilinguismo, acessibilidade
     (WCAG 2.2 AA), funcionamento offline, gratuidade, privacidade de menores;
   - Fora de escopo (explícito);
   - Perguntas em aberto.

   **`plan.md` — como**
   - Abordagem escolhida e alternativas descartadas (ADR se for estrutural);
   - Impacto em `content/`, na aplicação, nos dados e nas URLs;
   - Riscos e mitigação; dependências.

   **`tasks.md` — passos executáveis**
   - Tarefas pequenas, ordenadas, cada uma com critério de pronto e agente sugerido;
   - Marcar quais podem rodar em paralelo.

3. Peça revisão com `/spec-review` antes de executar.
4. Registre a spec no índice `docs/specs/README.md` com o status
   (`draft | in-review | approved | done`).
5. Só depois de `approved`, execute as tasks (`web-implementer`, `content-author`, etc.).
