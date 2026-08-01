---
id: TCK-0011
title: Desenhar o C4 Container e propor o ADR de CI/CD antes do primeiro ticket de aplicação
type: infra
status: triaged
owner: platform-architect
priority: P3
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0003]
---

# TCK-0011 — Desenhar o C4 Container e propor o ADR de CI/CD antes do primeiro ticket de aplicação

## Pedido original (verbatim)

> **A-4 — lacunas de arquitetura herdadas, já registradas pela cadeia e confirmadas por mim:**
> C4 nível **Container** inexistente (`docs/architecture/` só tem Context) e CI/CD + previews
> por branch seguem `PROPOSTO` em `c4-context.md:20,26` sem ADR. Ambos merecem ticket próprio
> antes do primeiro ticket de implementação da aplicação.

— `tickets/TCK-0003-accept-platform-stack-adr/log.md` `[015]`, ACTION A-4 (mesma pendência
registrada pelo `code-reviewer` em `[014]`, "Pendências e riscos").

## Requisito refinado

Quem sofre: o primeiro `frontend-developer` / `devops-engineer` da Fase 2. O `ADR-0003` foi
aceito e destravou a frente de plataforma, mas o único diagrama existente é o de **Contexto**:
não há nível Container que diga quais peças existem (build, HTML por idioma, ilha interativa,
service worker, IndexedDB, host) nem quem fala com quem. E `docs/architecture/c4-context.md`
marca **CI/CD e previews por branch como `PROPOSTO`, sem nenhum ADR que os cubra** — enquanto
`.github/workflows/ai-surface-audit.yml` já roda de fato, o que deixa o desenho e a realidade
em desacordo.

Resultado esperado: o desenho da caixa aberta e uma proposta de decisão de CI/CD com custo
zero comprovado, prontos para o usuário aceitar — sem escrever pipeline nem código.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. `docs/architecture/c4-container.md` existe, com bloco Mermaid `C4Container` válido,
      contendo no mínimo: acervo `content/`, build estática, HTML por idioma (`/pt-BR/`,
      `/en-US/`), ilha interativa, cache offline do conteúdo visitado, IndexedDB do progresso
      e host estático. Cada elemento com **tecnologia e responsabilidade em uma linha**.
      Falha se algum elemento vier sem responsabilidade declarada.
- [ ] 2. O diagrama **não decide** o que o `ADR-0003` declara não decidir (momento de
      renderização do KaTeX — build × runtime —, estratégia de service worker, bibliotecas de
      UI/teste). Teste: no bloco Mermaid,
      `grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"` → nenhuma
      ocorrência que **prescreva** mecanismo; o que não estiver decidido aparece marcado
      `PROPOSTO` com o ADR pendente citado. (É exatamente o defeito B4 do TCK-0003 — L-011.)
- [ ] 3. Abaixo do diagrama há **Leitura** curta (padrão `docs/DOC-STANDARDS.md`) que nomeia
      explicitamente o que o diagrama **não** decide, e a seção **Fontes** com os ADRs.
- [ ] 4. `docs/adr/ADR-0006-<slug>.md` criado a partir de `docs/adr/adr-template.md`, com
      `status: proposed`, cobrindo os quatro pontos: (i) onde o CI roda (GitHub Actions ×
      recurso nativo da Vercel × ambos), (ii) o que ele executa em cada push/PR — no mínimo
      `audit-ai-surface.sh` e `audit-content.sh`, hoje parcialmente cobertos por
      `.github/workflows/ai-surface-audit.yml`, (iii) previews por branch: existem? quem
      dispara? (iv) gatilho do deploy em produção. Falha se qualquer um dos quatro ficar sem
      posição.
- [ ] 5. Alternativas descartadas com uma linha de motivo cada, e **consequências
      falseáveis** (não "melhora a qualidade", mas "PR com adapter desatualizado não pode ser
      mesclado"). Seção "Como reverter" preenchida.
- [ ] 6. **Custo zero comprovado**: os limites do plano gratuito usados (minutos de CI,
      builds, previews) aparecem com URL da política e data de consulta. Falha se o custo for
      afirmado sem fonte.
- [ ] 7. `docs/architecture/c4-context.md:20,26` deixa de marcar CI e previews como
      `PROPOSTO` **sem ADR**: passa a citar o `ADR-0006` (`proposed`), sem afirmar que estão
      decididos. Teste: `grep -n "PROPOSTO" docs/architecture/c4-context.md` → toda ocorrência
      restante remete a um ADR nomeado. O parágrafo "Estado atual × proposta" (`:45-48`)
      acompanha.
- [ ] 8. `docs/adr/README.md` lista o `ADR-0006` com status `proposed`, e
      `memory/context/project-context.md` o registra em **decisões em aberto**, com a pergunta
      objetiva dirigida ao usuário. Falha se algum arquivo descrever o ADR como aceito.
- [ ] 9. Nenhum arquivo de pipeline criado ou alterado: `git status --porcelain
      .github/workflows/` → **vazio**. Nenhum código, `package.json` ou dependência.
- [ ] 10. `python3 scripts/sync-ai-adapters.py --check` exit 0;
      `bash scripts/audit-ai-surface.sh` → `Resultado: OK`;
      `bash scripts/audit-content.sh` → `0 erros · 0 avisos` (exit codes capturados sem pipe).

### Requisitos transversais (marcar todos)

- [ ] Bilinguismo pt-BR + en-US · [x] não aplicável — documentação interna (pt-BR por
      convenção da §2a); as **rotas** por idioma aparecem no diagrama como estrutura
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável — nenhum artefato de usuário final
- [x] Funciona offline / PWA — o cache do conteúdo visitado é elemento obrigatório do
      diagrama (`ADR-0003`: offline é requisito de arquitetura, não recurso opcional)
- [x] Custo zero mantido — critério 6, com fonte e data
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável — o ADR **não** pode
      introduzir telemetria; se o desenho a exigir, é ADR próprio (`ADR-0003:143-145`)
- [ ] URLs de `content/` preservadas · [x] não aplicável — `content/` não é tocado
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- **Implementar** CI/CD, previews ou qualquer workflow: é ticket do `devops-engineer`, depois
  do aceite do ADR-0006.
- **Aceitar** o ADR-0006: aceite é ato do usuário (foi assim no `ADR-0003`, TCK-0003).
- Escolher biblioteca de UI, de testes ou estratégia de service worker — `ADR-0003:11` lista
  as três entre o que **não** decide; entram em ADR/spec próprios.
- Níveis C4 de Componente e Código.

## Contexto e referências

- Origem: `TCK-0003/log.md` `[014]` ("Pendências e riscos") e `[015]` ACTION A-4.
- ADRs aplicáveis: **`ADR-0003`** (`accepted`) — o container tem de caber dentro dele,
  inclusive a restrição de independência do contrato de dados (`:157-174`) e a portabilidade
  do deploy estático (`:151-155`); `ADR-0004` (tickets).
- Estado atual: `docs/architecture/` só tem `c4-context.md`;
  `.github/workflows/ai-surface-audit.yml` é o único pipeline existente.
- Arquivos-alvo: `docs/architecture/c4-container.md` (novo), `docs/architecture/README.md`,
  `docs/architecture/c4-context.md` (`:20`, `:26`, `:45-48`), `docs/adr/ADR-0006-*.md` (novo),
  `docs/adr/README.md`, `memory/context/project-context.md`.
- Lições relevantes: **L-011** (ADR decide restrição, não o momento da implementação — o
  rótulo "KaTeX pré-renderizado" num diagrama já custou um `REJECT`); **L-013** (o Mermaid é
  parte normativa do documento e entra na revisão com o mesmo peso da prosa); **L-010**
  (decisão aceita exige atualizar tudo que os agentes leem).

## Perguntas em aberto

- **Para o usuário, no aceite do ADR-0006:** previews por branch são desejados (expõem
  conteúdo em `draft` publicamente) ou o preview fica restrito ao ambiente local? A resposta
  muda a decisão (iii) e não pode ser presumida pelo agente.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
