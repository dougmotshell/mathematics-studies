---
name: generate-project-context
description: Regenera memory/context/project-context.md com o estado atual do projeto — o que existe, o que está decidido, o que está em aberto e quais são os próximos passos. Usar após marcos, decisões aceitas ou quando o contexto estiver defasado.
---

# Gerar contexto do projeto

1. Levante o estado real, sem confiar na memória anterior:
   - `git log --oneline -20` e `git status --short`;
   - estrutura de `content/` (nós existentes, status `draft`/`published` nos `meta.json`);
   - `docs/adr/README.md` (decisões aceitas × propostas);
   - `docs/specs/README.md` (specs em aberto);
   - `docs/errors/README.md` e `memory/LESSONS.md` (o que já se aprendeu);
   - existência da aplicação web (há código? build? deploy?).
2. Reescreva `memory/context/project-context.md` com:
   - **Última atualização** (data absoluta);
   - **Estado atual** por frente: conteúdo · plataforma · superfície de IA · documentação;
   - **Decisões aceitas** (com link para o ADR) e **decisões em aberto**;
   - **Próximos passos** priorizados;
   - **Riscos/pendências conhecidos**.
3. Não infle: se uma frente ainda não existe, escreva "não iniciada". Contexto otimista é
   pior do que contexto ausente.
4. Preserve o histórico relevante — o arquivo é cumulativo por seções datadas; não apague
   estado anterior que ainda explica decisões atuais.
5. Atualize `memory/MEMORY.md` se algum ponteiro mudou.
