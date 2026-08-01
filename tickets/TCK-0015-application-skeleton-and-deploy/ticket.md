---
id: TCK-0015
title: Criar o esqueleto da aplicação e configurar o deploy
type: infra
status: done
owner: tech-lead
priority: P1
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0011, TCK-0014, ADR-0003, ADR-0006, ADR-0007]
---

# TCK-0015 — Criar o esqueleto da aplicação e configurar o deploy

## Pedido original (verbatim)

> já conectei o repositório na vercel, e tenho a vercel cli instaladi, o dominio ficou
> https://mathematics-studies.vercel.app depois configure tudo para o deploy

## Requisito refinado

O repositório está conectado à Vercel e o domínio é `https://mathematics-studies.vercel.app`,
mas **não existe aplicação**: nenhum `package.json`, nenhum esqueleto, nenhuma dependência.
Configurar o deploy exige, portanto, criar o esqueleto especificado no `ADR-0007` e o pipeline
do `ADR-0006`, e provar que a cadeia inteira funciona ponta a ponta — acervo → validação →
build → HTML publicável.

Este ticket entrega o **pipeline provado com uma página mínima**, não a interface. O índice, o
leitor de nó e o player de exercícios são as tasks 5–8 da spec, em tickets próprios com o
`frontend-developer`. A página mínima existe para provar que o pipeline publica, e some assim
que a task 5 entrar.

Decisões humanas já tomadas (2026-08-01): projeto **na raiz**, URL com prefixo de idioma
**minúsculo** (`/pt-br/`, `/en-us/`), previews por PR **ativados**.

## Critérios de aceite

- [x] 1. `package.json` na raiz, `private: true`, `engines.node >= 22.12.0`, com **apenas** as
      dependências que o esqueleto exige — nenhuma biblioteca de UI, de teste ou de
      componente entra aqui.
- [x] 2. Estrutura conforme `ADR-0007`, na raiz do repositório.
- [x] 3. O módulo que lê `content/` **não importa nada do gerador de site** — a independência
      do contrato de dados é restrição declarada no `ADR-0003` e precisa sobreviver a uma
      troca de stack.
- [x] 4. Rotas por idioma com prefixo **minúsculo** (`/pt-br/…`, `/en-us/…`); o identificador
      de idioma **no dado** continua `pt-BR`/`en-US` — minúsculo é grafia de URL, não chave.
- [x] 5. O caminho do nó piloto aparece na URL **sem tradução nem normalização**:
      `/pt-br/high-school/algebra/quadratic-equations` resolve (RNF-5, L-003).
- [x] 6. Uma página mínima por idioma lê o nó piloto **do acervo real** e mostra título e
      rótulo de rascunho. Não é o leitor da task 6 — é prova de vida do pipeline, e o log diz
      isso.
- [x] 7. `npm run build` gera saída estática publicável, e o build **falha** quando o acervo é
      inválido — provado com fixture inválida, com a saída anexada ao log.
- [x] 8. Onde a validação do RF-18 roda (`prebuild`, script de CI ou outro ponto) é **decisão
      deste ticket**, não do ADR — escolha, implemente e justifique no log contra a
      alternativa descartada.
- [x] 9. Configuração da Vercel sem recurso proprietário que quebre a portabilidade do
      diretório estático (`ADR-0003`): trocar de host deve custar reconfigurar, não reescrever.
- [x] 10. Workflow do GitHub Actions conforme `ADR-0006`: roda em PR e em push na `main`, com
      as auditorias existentes, o validador de conteúdo e o build de verificação.
- [x] 11. `.gitignore` cobre `node_modules/`, a saída de build e artefatos locais da Vercel —
      nenhum deles entra no repositório.
- [x] 12. **Zero coleta de dados**: nenhum analytics, pixel, fonte remota ou script de
      terceiro no HTML publicado. Verificado no HTML gerado, não por intenção.
- [x] 13. `bash scripts/audit-ai-surface.sh`, `bash scripts/audit-content.sh` e
      `bash scripts/validate-content.sh` sem erros.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — critérios 4 e 6
- [x] Acessibilidade WCAG 2.2 AA — `lang` correto por rota; o resto é das tasks 6–8
- [x] Funciona offline / PWA — **não** nesta entrega; a camada offline é a task 10
- [x] Custo zero mantido — plano gratuito, sem serviço pago
- [x] Privacidade e dados de menores (LGPD/COPPA) — critério 12
- [x] URLs de `content/` preservadas — critério 5
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Índice de navegação, leitor de nó e player de exercícios — tasks 5–8, tickets próprios.
- Camada offline, service worker e PWA — task 10.
- Escolher biblioteca de UI ou de testes — segue em aberto por decisão do `ADR-0003`.
- Alterar `content/`, a spec, ou aceitar os ADRs `proposed` (ato do usuário, ticket próprio).
- Domínio próprio, variáveis de ambiente secretas, qualquer recurso pago.

## Contexto e referências

- Esqueleto: `docs/adr/ADR-0007-application-skeleton.md` (`proposed`)
- CI/CD: `docs/adr/ADR-0006-continuous-integration-and-publication.md` (`proposed`)
- Stack: `docs/adr/ADR-0003-platform-stack.md` (`accepted`)
- Arquitetura: `docs/architecture/c4-container.md`
- Validador entregue no TCK-0014: `scripts/validate-content.sh`
- Spec: `docs/specs/minimum-learning-slice/` (RF-18, RNF-4, RNF-5, RNF-7)
- Ambiente verificado em 2026-08-01: Node v24.14.1, npm 11.11.0, Vercel CLI 58.4.4;
  domínio `https://mathematics-studies.vercel.app`; sem `.vercel` local (integração via
  GitHub, do lado da Vercel)

## Perguntas em aberto

- Nenhuma para executar. **Push na `main` dispara deploy de produção** pela integração
  existente — o commit é do orquestrador, não do agente, e sai só depois da validação.

## Resultado final

**Aprovado por `qa-validator#12` em 2026-08-01 — 13/13 critérios com evidência reexecutada do
zero, nenhum defeito.** Commit da validação: início `dea3303`, fim `aee5d3d` (o avanço do HEAD
é do TCK-0016 e não toca nenhum artefato deste ticket). Ambiente: Node v24.14.1, npm 11.11.0,
Python 3.12.3; `preview` em `astro preview` + `curl` (sem navegador com MCP nesta sessão).

### O que vai ao ar

**4 arquivos, 3 páginas HTML, ~2,2 KB por página, zero JavaScript**, em
`https://mathematics-studies.vercel.app`:

| rota | idioma | conteúdo |
|---|---|---|
| `/` | bilíngue (`lang="pt-BR"`, com trecho `lang="en-US"`) | escolha de idioma, com link para o nó em cada idioma |
| `/pt-br/high-school/algebra/quadratic-equations` | `lang="pt-BR"` | título, selo `Rascunho` e contagem de exercícios, lidos do acervo na build |
| `/en-us/high-school/algebra/quadratic-equations` | `lang="en-US"` | idem, em inglês |

Mais `/robots.txt` (indexação liberada, sem `Sitemap:`). Zero requisição externa, CSS embutido
no `<head>`, fontes do sistema, sem cookie, sem armazenamento, sem analytics, sem telemetria.

### O que **não** vai ao ar

Índice de navegação (task 5), leitor de nó com teoria renderizada e matemática acessível
(task 6), player de exercícios (tasks 7–8), camada offline/PWA e service worker (task 10),
progresso do aluno, biblioteca de UI e ferramenta de teste. Consequência conhecida e
esperada: `/pt-br/` e `/en-us/` **sem nó** respondem **404**, e não há página 404 do produto —
quem erra a URL vê o 404 genérico do host.

### Dívidas aceitas, com gatilho

- **D-1** — o comentário `"//"` do `package.json` afirma que inverter a ordem do `prebuild`
  reabre o buraco do acervo vazio; medido, **não reabre** (inverter sai 2 igual). Quem reabre é
  trocar `&&` por `;` (exit 0, publica site vazio). Erro conservador. *Gatilho:* próxima edição
  do `prebuild`.
- **D-2** — 7 formas reais de recurso de terceiro atravessam o passo de CI (`<base href>`,
  `report-uri` de CSP em `<meta>`, `manifest.webmanifest` com ícone externo, e `fetch` /
  `import()` / `WebSocket` / `EventSource` / `XMLHttpRequest` em chunk `.js` emitido).
  *Gatilhos:* o primeiro `<link rel="manifest">` (task 10, que **aprova hoje**) e o primeiro
  `<meta http-equiv="Content-Security-Policy">`.
- **D-3** — nó "bilíngue" cujo campo localizado é um espaço de largura zero (U+200B) atravessa
  as duas auditorias, o portão e o leitor, e publica. Mesma classe da dívida D-2 do TCK-0014;
  conserto é lá. *Gatilho:* o primeiro nó novo no acervo.
- **A2 (do `[013]`)** — o passo de terceiros vai reprovar recursos de **mesma origem** que o
  `ADR-0007` permite (`<script src="/_astro/…">`, registro de service worker, `<iframe>` e
  `<embed>` internos, fonte auto-hospedada). Falha na direção certa; o vermelho chega no
  primeiro ticket de **interatividade** (tasks 7–8) e de **offline** (task 10), não no de
  tipografia — corrigir a redação do comentário nessa mesma edição.

### Modo de falha do primeiro deploy

**Build vermelha, nunca publicação silenciosa.** O portão do RF-18 está nos dois caminhos
(`prebuild` na publicação, job do Actions no merge) e derruba de fato: com acervo inválido,
`npm run build` sai ≠ 0 e o `dist/` **sequer é criado** — 0 HTML, medido com quatro fixtures
(id divergente, monolíngue `published`, monolíngue `draft`, teoria ausente). Se a imagem de
build da Vercel surpreender, o resultado é deployment falho com mensagem, e o site anterior
(nenhum, neste primeiro deploy) permanece. Reversão: *Instant Rollback* no painel, ou remover
`package.json`, `astro.config.mjs`, `vercel.json`, `src/` e `public/` — o acervo nunca dependeu
deles.

### Pendências que são ato do usuário

Proteção de branch em `main`; previews por PR no painel; e — o único ponto cego do critério 12
— confirmar que **Vercel Web Analytics e Speed Insights estão desligados**, porque são ligados
no painel e injetam script na borda sem mudança no repositório. Verificação no ar:
`curl -s https://mathematics-studies.vercel.app/ | grep -icE '/_vercel/|insights'` tem de dar 0.
