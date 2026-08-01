---
name: create-adr
description: Registra uma decisão arquitetural, de produto ou de processo como ADR numerado em docs/adr/. Usar sempre que uma escolha estrutural for feita — stack, modelo de dados, taxonomia, licença, privacidade, política de conteúdo.
---

# Criar ADR (Architecture Decision Record)

1. Confirme que a decisão é **estrutural** (afeta arquitetura, produto, taxonomia,
   privacidade, licença ou processo). Ajuste pontual não vira ADR — vira lição.
2. Leia `docs/adr/README.md` e descubra o próximo número livre (`ADR-NNNN`, sequencial, sem
   furos).
3. Verifique se já existe ADR sobre o assunto:
   - decisão que substitui outra → marque a antiga como `superseded` e referencie a nova;
   - decisão que apenas detalha → atualize a existente em vez de criar duplicata.
4. Crie `docs/adr/ADR-NNNN-short-title.md` a partir de `docs/adr/adr-template.md`
   (nome en-US kebab-case, conteúdo pt-BR) preenchendo:
   - **Contexto**: o problema real e as restrições (custo, público, gratuidade, offline,
     bilinguismo, LGPD/COPPA quando houver dados de menores);
   - **Alternativas consideradas**: pelo menos duas, com trade-offs honestos;
   - **Decisão** e **Consequências** (positivas e negativas, incluindo o que fica mais
     difícil);
   - **Status**: `proposed` até haver aceite explícito de quem conduz o projeto.
5. Se a decisão alterar slugs de `content/`, liste as URLs afetadas e o plano de redirect.
6. Inclua um diagrama Mermaid quando a decisão envolver fluxo, dependência ou estrutura.
7. Atualize o índice `docs/adr/README.md`.
8. Se a decisão invalidar algo escrito em `AGENTS.md`, atualize o `AGENTS.md` no mesmo passo.
