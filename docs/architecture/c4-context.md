# C4 — Nível 1: Contexto

**Estado:** o acervo e o pipeline de conteúdo são **decididos** (ADR-0001, ADR-0002); a
aplicação web é **proposta** (ADR-0003 `proposed`).

```mermaid
C4Context
    title Contexto — mathematics-studies

    Person(student, "Aluno", "Da educação infantil à pesquisa; usa navegador, às vezes offline")
    Person(teacher, "Professor / mediador", "Reutiliza o material com sua turma")
    Person(contributor, "Contribuidor", "Pessoa ou agente de IA que escreve conteúdo e código")

    System(platform, "mathematics-studies", "PWA gratuita de estudos de matemática, bilíngue pt-BR/en-US (aplicação: PROPOSTA)")

    System_Ext(repo, "Repositório Git", "Acervo versionado em content/ + código")
    System_Ext(vercel, "Vercel", "Build e hospedagem estática, previews por branch")
    System_Ext(sources, "Fontes abertas externas", "Livros abertos, vídeos e materiais gratuitos referenciados")

    Rel(student, platform, "Estuda, pratica, acompanha progresso", "HTTPS / offline via PWA")
    Rel(teacher, platform, "Consulta e reutiliza material licenciado", "HTTPS")
    Rel(contributor, repo, "Escreve conteúdo e código", "Git")
    Rel(repo, vercel, "Dispara build e deploy", "CI")
    Rel(vercel, platform, "Serve a aplicação", "HTTPS")
    Rel(platform, sources, "Aponta para referências gratuitas", "Links com licença registrada")
```

## Leitura

O sistema é essencialmente um **acervo versionado** publicado como aplicação estática. O aluno
é o ator central e pode operar sem conta e sem rede depois da primeira visita. O contribuidor
— humano ou agente de IA — atua sobre o repositório, não sobre a aplicação em execução. A
Vercel é infraestrutura de publicação, não guardiã de estado.

O diagrama **não** mostra: persistência de progresso (indefinida — depende de ADR-0003 e de um
ADR de privacidade futuro), fóruns e certificados (fases 5–6 do roadmap).

## Fontes

- `docs/adr/ADR-0001-content-taxonomy.md`
- `docs/adr/ADR-0002-bilingual-content.md`
- `docs/adr/ADR-0003-platform-stack.md` (status `proposed`)
- `docs/product/vision.md`, `docs/product/roadmap.md`
