# C4 — Nível 2: Container

**Estado:** o desenho decorre de três ADRs **aceitos em 2026-08-01** — `ADR-0003` (site
estático com ilhas, local-first, host substituível), `ADR-0006` (integração contínua, previews
e gatilho do deploy) e `ADR-0007` (esqueleto concreto: gerador, diretórios, forma da URL
bilíngue) — e detalha o que o `c4-context.md` mostra como uma caixa só. **Nenhum elemento tem
marcador `PROPOSTO`**: não há, hoje, elemento deste nível esperando aceite.

A implementação começou em 2026-08-01 pelo **TCK-0015** (esqueleto na raiz e pipeline de
publicação), que estava em revisão quando este documento foi atualizado — o diagrama descreve o
**estado decidido**, e nem tudo que ele mostra existe em código.

O marcador `EM ABERTO (ticket)` continua em uso e **não** foi removido pelo aceite: ele indica
o que nenhum ADR decide **de propósito** e que **não** vira ADR — é escolha do ticket de
implementação, como o mecanismo da camada offline e o **lugar** do portão de validação do
acervo. Aceitar um ADR não fecha o que ele decidiu não decidir.

**Como ler a ausência de marcador:** elemento sem marcador está sustentado por **ADR aceito ou
spec aprovada**, e a fonte aparece no próprio rótulo (`ADR-0003`, `RF-18`, …). Marcador posto
num contêiner **vale para as relações que decorrem dele** — a camada offline é marcada uma vez,
no contêiner, e as duas relações de cache herdam esse marcador em vez de repeti-lo.

```mermaid
C4Container
    title Container — mathematics-studies (acervo, build estática e dispositivo do aluno)

    Person(student, "Aluno", "Navegador, com ou sem rede; sem conta")
    Person(contributor, "Contribuidor", "Pessoa ou agente de IA que escreve conteúdo e código")

    System_Boundary(origin, "Repositório Git público — origem de tudo") {
        ContainerDb(content, "Acervo de conteúdo", "content/: Markdown + JSON versionados", "Fonte única de taxonomia, teoria bilíngue, exercícios e gabarito; contrato independente da stack (ADR-0003)")
    }

    System_Boundary(pipeline, "Build e publicação — build exigida pelo ADR-0003; automação decidida no ADR-0006") {
        Container(ci, "Integração contínua", "GitHub Actions; portão de mérito do repositório (ADR-0006) — bloqueio de merge depende de proteção de branch, ato do usuário", "Executa as auditorias do acervo e da superfície de IA a cada PR")
        Container(validator, "Validador do contrato", "Executável autônomo, fora da aplicação — exigido pela spec da fatia mínima (RF-18); entregue pelo TCK-0014", "Reprova acervo inválido antes de existir página; falha visível e registrada")
        Container(build, "Build estática", "Astro na raiz do repositório, gerador orientado a conteúdo (ADR-0003, ADR-0007)", "Lê o acervo validado e emite um diretório de arquivos estáticos por idioma")
        Container(host, "Host estático", "Vercel, plano gratuito (ADR-0003); publica no push em main e abre preview por PR (ADR-0006)", "Serve arquivos por HTTPS; não guarda estado do aluno nem executa código do produto")
    }

    System_Boundary(device, "Dispositivo do aluno — navegador") {
        Container(pages, "Páginas por idioma", "HTML + CSS estáticos, uma rota estática por idioma: /pt-br/... e /en-us/..., prefixo em minúsculas (ADR-0007)", "Entrega índice, teoria e matemática acessível sem exigir JavaScript para ler")
        Container(island, "Ilha de interatividade", "Componente isolado, hidratado sob demanda, só onde há exercício (ADR-0003)", "Corrige a resposta no próprio cliente e devolve feedback diagnóstico por alternativa")
        Container(offline, "Camada offline", "Cache do navegador; mecanismo EM ABERTO (ticket)", "Mantém o conteúdo já visitado, com seus exercícios, acessível sem rede")
        ContainerDb(progress, "Progresso local", "IndexedDB do dispositivo (ADR-0003)", "Guarda progresso sem conta e sem servidor; nenhum dado sai do dispositivo")
    }

    Rel(contributor, content, "Escreve teoria, exercícios e metadados", "Git")
    Rel(contributor, build, "Escreve e configura a aplicação", "Git")
    Rel(ci, validator, "Executa auditorias, validador do acervo e build de verificação a cada PR (ADR-0006)", "Shell")
    Rel(validator, content, "Lê e verifica os arquivos do acervo", "Sistema de arquivos")
    Rel(build, validator, "Nó reprovado não vira página publicada (RF-18) — lugar do portão EM ABERTO (ticket)", "Verificação do acervo antes de publicar")
    Rel(build, content, "Lê metadados, teoria e exercícios do nó", "Sistema de arquivos, na build")
    Rel(build, host, "Publica o diretório estático a cada push em main; preview por PR (ADR-0006)", "Envio de arquivos")
    Rel(host, pages, "Entrega HTML, CSS e ativos", "HTTPS")
    Rel(student, pages, "Lê teoria e navega estágio, área e tópico", "HTTPS ou offline")
    Rel(pages, island, "Ativa a ilha quando o nó tem exercício", "Fronteira explícita: a ilha recebe dado já validado e não busca dado na rede")
    Rel(student, island, "Responde, pede dica e recebe feedback", "Interação local, sem rede")
    Rel(island, progress, "Grava e lê o progresso do próprio dispositivo", "API do navegador")
    Rel(pages, offline, "Registra o que foi visitado", "API do navegador")
    Rel(offline, pages, "Reabre o conteúdo visitado sem rede", "Cache local")
```

## Leitura

O caminho é de mão única: o acervo em `content/` entra na build, passa por uma verificação que
impede o nó reprovado de virar página, e sai como arquivos estáticos; do host para o
dispositivo só descem HTML, CSS e ativos. Nenhuma seta volta do aluno para o servidor — não há
backend, conta nem telemetria, e a ausência é decisão do `ADR-0003`, não omissão do desenho. O
progresso e o cache do conteúdo visitado nascem e morrem no dispositivo.

O diagrama **não decide** mecanismo: em que momento a matemática vira HTML (build × execução no
navegador), com que estratégia a camada offline guarda o conteúdo visitado, que biblioteca roda
dentro da ilha, com que ferramenta se testa e **onde exatamente roda o portão que reprova
acervo inválido** — script do projeto, job de CI ou os dois. Este último é decisão de
implementação por definição da própria spec aprovada
(`docs/specs/minimum-learning-slice/plan.md`, item 5), e por isso aparece como
`EM ABERTO (ticket)` na relação `build → validador`: nenhum ADR deve fechá-lo, e o aceite do
`ADR-0006` não o fechou. O que antes esperava aceite — papel de portão de merge da CI, gatilho
de deploy, previews, gerador concreto, diretórios e forma da URL bilíngue — foi **decidido em
2026-08-01** pelos `ADR-0006` e `ADR-0007` e por isso aparece sem marcador, com a fonte no
próprio rótulo. Duas ressalvas ficam explícitas no rótulo em vez de virarem marcador: o
bloqueio de merge depende de **proteção de branch**, que é ato do usuário, e o **lugar** do
portão de publicação é do ticket. O diagrama também **não** mostra fóruns, certificados nem
sincronização entre dispositivos: os três exigem estado compartilhado e ADR próprio.

## Contrato das fronteiras

| Fronteira | O que atravessa | O que nunca atravessa |
|---|---|---|
| `content/` → build | Arquivos do acervo lidos como dado: `meta.json`, `theory.<lang>.md`, `exercises.json` | Componente de framework, frontmatter proprietário ou lógica de aprendizagem — o acervo não conhece a aplicação (`ADR-0003`, independência do contrato de dados) |
| Validador → build | Aprovação ou reprovação do acervo, com arquivo, item e regra violada | Objeto inválido: nó reprovado não vira página (RF-18) |
| Build → host | Um diretório de arquivos estáticos, servível por qualquer host | Segredo, variável de ambiente com dado pessoal, função executada por requisição |
| Host → dispositivo | HTML, CSS, ativos e o payload do exercício — **incluindo o gabarito** | Identificador de usuário, cookie de sessão, resposta do aluno em qualquer direção |
| Página → ilha | Dados do exercício **já validados**, entregues na fronteira do componente — serializados na build como propriedade (`ADR-0007`, `accepted`); a biblioteca que roda dentro da ilha continua sendo decisão do ticket | Hidratação da página inteira: recurso que a exija está mal desenhado (`ADR-0003`); e requisição de rede feita pela ilha — o payload já traz o que ela precisa (`ADR-0003`: offline do conteúdo visitado, sem backend) |
| Ilha → progresso local | Eventos de progresso do próprio dispositivo | Qualquer coisa que saia do dispositivo — sem rede, sem servidor, sem telemetria |

Consequência que atravessa todas as linhas: **o gabarito viaja no cliente** (L-008). Nada pode
depender do segredo da resposta — sem prova valendo nota, sem ranking, sem certificado
verificável.

## Fontes

- `docs/adr/ADR-0003-platform-stack.md` (`accepted`, 2026-08-01) — site estático com ilhas,
  local-first sem conta, portabilidade do host, independência do contrato de dados.
- `docs/adr/ADR-0006-continuous-integration-and-publication.md` (`accepted`, 2026-08-01) —
  integração contínua, previews por PR, gatilho do deploy.
- `docs/adr/ADR-0007-application-skeleton.md` (`accepted`, 2026-08-01) — gerador concreto,
  projeto na raiz, URL `/pt-br/` e `/en-us/`, leitura de `content/` na build e lugar das ilhas.
- `docs/adr/ADR-0002-bilingual-content.md` — paridade obrigatória por idioma.
- `docs/architecture/c4-context.md` — nível acima; `docs/specs/minimum-learning-slice/`
  (RF-18, RNF-3, RNF-5) — comportamento exigido da primeira fatia.
- `tickets/TCK-0014-content-contract-validator/` (fechado) — validador do contrato;
  `tickets/TCK-0015-application-skeleton-and-deploy/` — implementação do esqueleto e do
  pipeline; `tickets/TCK-0016-accept-cicd-and-skeleton-adrs/` — aceite dos ADR-0006 e ADR-0007.
