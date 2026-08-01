---
name: capture-lesson
description: Registra uma lição aprendida em memory/lessons/ (protocolo de auto-aprendizado). Usar após correções do usuário, descobertas de domínio, decisões de terminologia bilíngue ou padrões que funcionaram bem.
---

# Capturar lição aprendida

1. Leia `memory/MEMORY.md` e `memory/LESSONS.md` e verifique se já existe lição sobre o
   assunto — **atualize** em vez de duplicar; corrija ou remova lições que se provaram
   erradas.
2. Confirme que é lição de verdade: uma **regra aplicável no futuro**, não o resumo do que
   foi feito. Se não muda o comportamento das próximas tarefas, não registre.
3. Crie `memory/lessons/<short-lesson-name>.md` (en-US kebab-case, conteúdo pt-BR):
   - `**Tipo:**` `sucesso` | `erro` | `correção`
   - `**Contexto:**` onde/quando surgiu (data absoluta, ex.: 2026-08-01)
   - `**Lição:**` o que foi aprendido
   - `**Como aplicar:**` regra prática para as próximas tarefas
   - Links `[[outra-licao]]` para lições relacionadas, quando houver.
4. Adicione uma linha em `memory/LESSONS.md` (seção do tipo correspondente) **e** em
   `memory/MEMORY.md`.
5. Se a lição nasceu de um erro, garanta que o erro também está em `docs/errors/`
   (`/log-error`).
