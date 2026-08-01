# C4 — Nível 1: Contexto

**Estado:** majoritariamente decidido. Acervo e pipeline de conteúdo por ADR-0001 e ADR-0002;
a aplicação web por ADR-0003 (aceito em 2026-08-01: site estático com ilhas de
interatividade, progresso local-first em IndexedDB, deploy estático) — nenhum desses é
hipótese; o que falta neles é **implementação**. Continua **proposto** (sem ADR aceito) o
pipeline de CI/CD e o uso de previews por branch, marcado como tal no diagrama.

```mermaid
C4Context
    title Contexto — mathematics-studies

    Person(student, "Aluno", "Da educação infantil à pesquisa; usa navegador, às vezes offline")
    Person(teacher, "Professor / mediador", "Reutiliza o material com sua turma")
    Person(contributor, "Contribuidor", "Pessoa ou agente de IA que escreve conteúdo e código")

    System(platform, "mathematics-studies", "PWA gratuita de estudos de matemática, bilíngue pt-BR/en-US; site estático com ilhas de interatividade (ADR-0003)")

    System_Ext(repo, "Repositório Git", "Acervo versionado em content/ + código")
    System_Ext(vercel, "Vercel", "Hospedagem estática do resultado da build (ADR-0003); previews por branch: PROPOSTO")
    System_Ext(sources, "Fontes abertas externas", "Livros abertos, vídeos e materiais gratuitos referenciados")

    Rel(student, platform, "Estuda, pratica, acompanha progresso", "HTTPS / offline via PWA")
    Rel(teacher, platform, "Consulta e reutiliza material licenciado", "HTTPS")
    Rel(contributor, repo, "Escreve conteúdo e código", "Git")
    Rel(repo, vercel, "Dispara build e deploy (PROPOSTO — sem ADR de CI/CD)", "CI")
    Rel(vercel, platform, "Serve a aplicação", "HTTPS")
    Rel(platform, sources, "Aponta para referências gratuitas", "Links com licença registrada")
```

## Leitura

O sistema é essencialmente um **acervo versionado** publicado como aplicação estática. O aluno
é o ator central e pode operar sem conta e sem rede depois da primeira visita. O contribuidor
— humano ou agente de IA — atua sobre o repositório, não sobre a aplicação em execução. A
Vercel é infraestrutura de publicação, não guardiã de estado.

O diagrama **não** mostra: a persistência de progresso, que por ADR-0003 é **local ao
dispositivo do aluno** (IndexedDB) e portanto não aparece como sistema externo; nem fóruns e
certificados (fases 5–6 do roadmap), que exigem estado compartilhado e ADR próprio. Também
não há backend, conta ou telemetria — a ausência é decisão, não omissão. O detalhamento
interno (build estática, ilhas, service worker) pertence ao nível **Container**, ainda não
desenhado.

**Estado atual × proposta:** atores, acervo, aplicação estática e hospedagem decorrem de ADRs
aceitos (0001, 0002, 0003). O **pipeline de CI/CD e os previews por branch são proposta** —
nenhum ADR aceito os cobre; quem os implementar precisa de ADR próprio (`devops-engineer`).
Nenhum elemento do diagrama está implementado: a aplicação ainda não existe em código.

## Fontes

- `docs/adr/ADR-0001-content-taxonomy.md`
- `docs/adr/ADR-0002-bilingual-content.md`
- `docs/adr/ADR-0003-platform-stack.md` (status `accepted`, 2026-08-01)
- `docs/product/vision.md`, `docs/product/roadmap.md`
