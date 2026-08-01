# ADR-0003 — Stack da plataforma web/PWA

- **Status:** proposed
- **Data:** 2026-08-01
- **Decisores:** pendente — aguarda decisão de Douglas Silva
- **Relacionados:** ADR-0001, ADR-0002

> **Este ADR está `proposed`.** Nenhum ticket de implementação da aplicação deve avançar
> antes do aceite. Agentes devem tratar tudo abaixo como hipótese.

## Contexto

O produto é uma aplicação web **PWA**, gratuita, com deploy na **Vercel**, que precisa:

- renderizar conteúdo versionado em Git (`content/`: Markdown + JSON) com matemática em
  KaTeX;
- funcionar **offline** para o conteúdo já visitado;
- ser **bilíngue** em todas as rotas, com URLs estáveis por idioma;
- rodar bem em dispositivo modesto e rede lenta;
- registrar progresso do aluno com **custo operacional próximo de zero** e privacidade forte
  (o público inclui crianças);
- crescer para módulos de curso: trilhas, quizzes, fóruns, certificados.

## Alternativas consideradas

### A. Framework React full-stack com renderização estática do conteúdo (ex.: Next.js na Vercel)
- **Prós:** integração natural com a Vercel; geração estática das páginas de conteúdo; i18n
  por rota; ecossistema grande; API routes disponíveis se/quando houver backend.
- **Contras:** peso e complexidade acima do necessário para um site majoritariamente
  estático; acoplamento ao fornecedor se forem usados recursos proprietários.

### B. SPA leve com build estático (ex.: Vite + React/Preact) + Vercel como host estático
- **Prós:** bundle menor; portabilidade alta (qualquer host estático); simples de entender e
  manter; ótimo casamento com PWA offline-first.
- **Contras:** SEO exige pré-renderização explícita; roteamento e i18n ficam por conta do
  time; sem backend embutido.

### C. Gerador de site estático orientado a conteúdo (ex.: Astro)
- **Prós:** HTML mínimo por padrão (excelente performance e SEO); ilhas de interatividade só
  onde há exercício; ótimo para conteúdo Markdown volumoso.
- **Contras:** interatividade rica (player de exercícios, progresso) exige disciplina de
  arquitetura; ecossistema menor que o React puro.

### Persistência de progresso (transversal às opções)
1. **Local-first** (IndexedDB) sem conta — custo zero, privacidade máxima, sem sincronização
   entre dispositivos.
2. Local-first + **sincronização opcional** com backend gratuito — melhor experiência, exige
   ADR de privacidade e conta.
3. Backend obrigatório desde o início — pior custo e pior privacidade; descartado.

## Decisão

**Pendente.** Recomendação para discussão: começar pela opção **C ou B** (conteúdo estático,
JavaScript mínimo, PWA offline-first) com persistência **local-first sem conta** (opção 1),
adiando qualquer backend até existir uma necessidade comprovada — o que mantém custo zero,
privacidade máxima e a decisão de conta/sincronização para um ADR próprio.

## Consequências

A preencher no aceite.

## Impacto

- **Conteúdo:** nenhum — o contrato de dados de `content/` é deliberadamente independente da
  stack.
- **Plataforma:** define toda a implementação.
- **Processo/agentes:** destrava os tickets de `frontend-developer`, `backend-developer` e
  `devops-engineer`.

## Como reverter

Enquanto o contrato de dados de `content/` permanecer independente da aplicação, trocar a
stack custa reescrever a camada de apresentação — não o acervo. Essa independência é uma
restrição a preservar em qualquer opção escolhida.
