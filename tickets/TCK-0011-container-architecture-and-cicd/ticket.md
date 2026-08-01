---
id: TCK-0011
title: Desenhar o C4 Container e propor o ADR de CI/CD antes do primeiro ticket de aplicação
type: infra
status: done
owner: qa-validator#9
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

- [x] 1. `docs/architecture/c4-container.md` existe, com bloco Mermaid `C4Container` válido,
      contendo no mínimo: acervo `content/`, build estática, HTML por idioma (`/pt-BR/`,
      `/en-US/`), ilha interativa, cache offline do conteúdo visitado, IndexedDB do progresso
      e host estático. Cada elemento com **tecnologia e responsabilidade em uma linha**.
      Falha se algum elemento vier sem responsabilidade declarada.
- [x] 2. O diagrama **não decide** o que o `ADR-0003` declara não decidir (momento de
      renderização do KaTeX — build × runtime —, estratégia de service worker, bibliotecas de
      UI/teste). Teste: no bloco Mermaid,
      `grep -inE "pré-renderiz|renderiz|service worker|react|preact|vitest"` → nenhuma
      ocorrência que **prescreva** mecanismo; o que não estiver decidido aparece marcado
      `PROPOSTO` com o ADR pendente citado. (É exatamente o defeito B4 do TCK-0003 — L-011.)
- [x] 3. Abaixo do diagrama há **Leitura** curta (padrão `docs/DOC-STANDARDS.md`) que nomeia
      explicitamente o que o diagrama **não** decide, e a seção **Fontes** com os ADRs.
- [x] 4. `docs/adr/ADR-0006-<slug>.md` criado a partir de `docs/adr/adr-template.md`, com
      `status: proposed`, cobrindo os quatro pontos: (i) onde o CI roda (GitHub Actions ×
      recurso nativo da Vercel × ambos), (ii) o que ele executa em cada push/PR — no mínimo
      `audit-ai-surface.sh` e `audit-content.sh`, hoje parcialmente cobertos por
      `.github/workflows/ai-surface-audit.yml`, (iii) previews por branch: existem? quem
      dispara? (iv) gatilho do deploy em produção. Falha se qualquer um dos quatro ficar sem
      posição.
- [x] 5. Alternativas descartadas com uma linha de motivo cada, e **consequências
      falseáveis** (não "melhora a qualidade", mas "PR com adapter desatualizado não pode ser
      mesclado"). Seção "Como reverter" preenchida.
- [x] 6. **Custo zero comprovado**: os limites do plano gratuito usados (minutos de CI,
      builds, previews) aparecem com URL da política e data de consulta. Falha se o custo for
      afirmado sem fonte.
- [x] 7. `docs/architecture/c4-context.md:20,26` deixa de marcar CI e previews como
      `PROPOSTO` **sem ADR**: passa a citar o `ADR-0006` (`proposed`), sem afirmar que estão
      decididos. Teste: `grep -n "PROPOSTO" docs/architecture/c4-context.md` → toda ocorrência
      restante remete a um ADR nomeado. O parágrafo "Estado atual × proposta" (`:45-48`)
      acompanha.
- [x] 8. `docs/adr/README.md` lista o `ADR-0006` com status `proposed`, e
      `memory/context/project-context.md` o registra em **decisões em aberto**, com a pergunta
      objetiva dirigida ao usuário. Falha se algum arquivo descrever o ADR como aceito.
- [x] 9. Nenhum arquivo de pipeline criado ou alterado: `git status --porcelain
      .github/workflows/` → **vazio**. Nenhum código, `package.json` ou dependência.
- [x] 10. `python3 scripts/sync-ai-adapters.py --check` exit 0;
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
- **Para o usuário, no aceite do ADR-0007** (escopo acrescentado pelo `log.md` `[003]`):
  (a) a URL do idioma deve ser `/pt-br/` (proposto, por causa da sensibilidade a maiúsculas em
  host estático) ou `/pt-BR/` (grafia idêntica à dos arquivos)? Depois da primeira publicação,
  mudar custa redirect (L-003). (b) O projeto Node fica na **raiz** do repositório (proposto)
  ou em `app/`?
- **Consequência de calendário, não pergunta:** a task 5 da fatia mínima depende do `ADR-0007`;
  enquanto ele estiver `proposed`, o ticket de bootstrap está bloqueado por decisão humana.

## Resultado final

**`done` em 2026-08-01, validado por `qa-validator#9`** — 10/10 critérios com evidência
própria (comando + saída, reproduzida na entrada `[010]` do `log.md`), 0 defeitos. Um loop de
devolução consumido (`[006]`, B1 e B2). Ambiente da validação: commit `5d1e2b6`, Node
v24.14.1, Chrome 151.0.7922.71, working tree compartilhado com seis agentes em paralelo.

**Critério 10 — a base do veredito, explícita.** Às 16:5x observei as três auditorias
**verdes** (exit 0; `Resultado: OK`; `Tudo já estava atualizado`) **com todos os artefatos
deste ticket já no lugar**. Na reexecução imediatamente anterior ao veredito, às 17:1x, o
`sync --check` voltou a **exit 1** — deriva do **TCK-0006**, ainda em execução, que alterou
`.github/instructions/core.instructions.md` (leitura acessível de KaTeX); os **7** arquivos
envolvidos têm **zero** ocorrências de `ADR-0006`/`ADR-0007`. O `done` se apoia na observação
verde, não na atribuição: existe estado medido do repositório em que este ticket está completo
e a invariante vale. Detalhamento e ruling: `log.md` `[011] CORRECTION`. **Gatilho para o
`tech-lead`:** enquanto o TCK-0006 não rodar o próprio sync, o CI reprova **qualquer** PR do
repositório.

**Critério 9 — mesma leitura.** No momento da verificação, `git status --porcelain
.github/workflows/` estava **vazio** com todos os artefatos deste ticket no lugar. Depois
disso, o **TCK-0015** alterou `ai-surface-audit.yml` (+62 −3, com `critério 12 do TCK-0015`
citado no próprio arquivo) e criou `package.json`, `src/`, `dist/`, `vercel.json`. Nenhum é
artefato declarado do TCK-0011. Ver `log.md` `[012]` — que também encaminha ao `tech-lead` o
fato substantivo de o TCK-0015 estar implementando pipeline sob ADR ainda `proposed`.

### Os dois ADRs saem daqui `proposed` — e isso é o desenho, não uma pendência do ticket

`ADR-0006` (integração contínua, previews, publicação) e `ADR-0007` (esqueleto da aplicação)
estão `status: proposed` no cabeçalho e em `docs/adr/README.md`. Varredura da raiz por
`ADR-0006|ADR-0007`: 26 arquivos, **nenhum** os descreve como aceitos. O aceite é ato do
usuário e pede ticket próprio (precedente `ADR-0003`/TCK-0003).

**O que o aceite vai exigir**, para que o ticket de aceite não nasça cego:

1. Fixar as três decisões já dadas pelo usuário e ainda **não aplicadas** de propósito: URL
   `/pt-br/` minúscula, previews por PR ativados, projeto na raiz.
2. **Remover a grafia alternativa** que hoje continua viva como opção: `c4-container.md:41`
   (`/pt-BR/... e /en-US/... como alternativa — PROPOSTO (ADR-0007)`), `ADR-0007:279-282`
   (Perguntas ao usuário) e `memory/context/project-context.md`. Manter as duas grafias
   enquanto o status é `proposed` está **correto**: apagá-las antes recriaria o desacordo
   entre desenho e realidade que este ticket veio consertar.
3. Converter os `PROPOSTO (ADR-0006)` / `PROPOSTO (ADR-0007)` do diagrama em decidido — sem
   tocar nos `EM ABERTO (ticket)`, que continuam válidos depois do aceite.
4. Disparar **L-010** (varredura da raiz, `AGENTS.md`, `.github/instructions/`, `sync`), que
   só vale para ADR **aceito** — por isso, e corretamente, nada foi propagado aqui.
5. Inventário completo dos pontos a tocar (o do `[007]` omite seis): `memory/context/frontend.md`,
   `memory/context/devops.md`, `docs/architecture/README.md`, `docs/architecture/c4-context.md`
   (`:6-9`, `:22`, `:28`, `:45-49`), `ADR-0006` item (iii) e pendência 3.

### Dívidas registradas (nenhuma bloqueia; todas com gatilho)

- **D-1 — número verdadeiro removido.** A S3 do `[006]` mandou tirar "1 build concorrente" por
  não estar na página citada. Conferi em 2026-08-01: `https://vercel.com/docs/limits` lista
  **"Concurrent Deployments 1"** para Hobby. O rótulo estava errado, o fato não. Como o
  `ADR-0006` decide construir **duas vezes** (Actions + Vercel), a concorrência 1 é restrição
  material. *Gatilho:* restaurar a linha com o rótulo certo no ticket de aceite.
- **D-2 — nuance de pausa.** `ADR-0006:150` diz "pausa até o ciclo de 30 dias virar"; a página
  acrescenta *"Some usage limits have shorter pause periods"*. A conclusão operacional
  ("não gera fatura, gera indisponibilidade") está correta e é conservadora.
- **D-3 — legenda literal.** "A fonte aparece no próprio rótulo" não se cumpre em **7 dos 28**
  elementos do bloco (os dois `Person`, as fronteiras `origin` e `device`, e as relações
  `contributor→content`, `contributor→build`, `student→pages`). Reproduzi a classificação do
  revisor e ela se sustenta: nenhum dos sete contrabandeia mecanismo de ADR `proposed`, logo
  não produz o dano da família B4. *Correção de contagem:* o total do bloco é **28**
  (11 nós + 3 fronteiras + 14 relações), não 22 como diz o `[009]`.
- **D-4 — `Leitura` fora da métrica do padrão.** `docs/DOC-STANDARDS.md:13` pede 3–6 linhas; a
  do Container tem 19 (264 palavras) e a do Context, **já aprovada antes deste ticket**, tem 18
  (210 palavras). O baseline elege a prática; exigir a métrica só do artefato novo seria
  reescrever o critério depois da entrega. *Gatilho:* vale para `docs/architecture/` inteiro —
  `ACTION` ao `tech-lead`.
- **D-5 — rótulo com prazo de validade.** `c4-container.md:35` ancora o validador em
  "entrega em curso no TCK-0014". *Gatilho:* quando o TCK-0014 fechar, o rótulo envelhece.

### O que este ticket destrava e o que continua travado

- **Destrava:** o primeiro ticket de aplicação deixa de escolher diretórios, forma de URL e
  modo de ler `content/` no meio de um ticket de interface — as três estão especificadas.
- **Continua travado:** a task 5 da fatia mínima depende do `ADR-0007`; enquanto `proposed`, o
  bootstrap segue bloqueado por decisão humana. `ADR-0006` pendência 1 (validador em Python +
  build em Node na mesma imagem) e pendência 2 (proteção de branch em `main`, ato do usuário)
  seguem abertas de propósito.
