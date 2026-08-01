# C4 — Nível 2: Container

**Estado:** o desenho decorre do `ADR-0003` (aceito em 2026-08-01) e detalha o que o
`c4-context.md` mostra como uma caixa só. **Nada aqui está implementado** — a aplicação não
existe em código. Dois grupos de elementos ainda **não** têm ADR aceito e estão marcados como
tais no diagrama, no texto e nas relações:

- `PROPOSTO (ADR-0006)` — o papel de portão de merge da integração contínua, os previews e o
  gatilho do deploy;
- `PROPOSTO (ADR-0007)` — esqueleto concreto da aplicação (gerador, diretórios, forma da URL
  bilíngue).

Um terceiro marcador, `EM ABERTO (ticket)`, indica o que nenhum ADR decide **de propósito** e
que **não** vira ADR: é escolha do ticket de implementação — mecanismo da camada offline e
**lugar** do portão de validação do acervo, entre outros.

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

    System_Boundary(pipeline, "Build e publicação — build exigida pelo ADR-0003; automação PROPOSTA (ADR-0006)") {
        Container(ci, "Integração contínua", "GitHub Actions, workflow já em uso para auditorias; papel de portão de merge PROPOSTO (ADR-0006)", "Executa as auditorias do acervo e da superfície de IA a cada PR")
        Container(validator, "Validador do contrato", "Executável autônomo, fora da aplicação — exigido pela spec da fatia mínima (RF-18); entrega em curso no TCK-0014", "Reprova acervo inválido antes de existir página; falha visível e registrada")
        Container(build, "Build estática", "Gerador de site orientado a conteúdo (ADR-0003); esqueleto PROPOSTO (ADR-0007)", "Lê o acervo validado e emite um diretório de arquivos estáticos por idioma")
        Container(host, "Host estático", "Vercel, plano gratuito (ADR-0003); gatilho PROPOSTO (ADR-0006)", "Serve arquivos por HTTPS; não guarda estado do aluno nem executa código do produto")
    }

    System_Boundary(device, "Dispositivo do aluno — navegador") {
        Container(pages, "Páginas por idioma", "HTML + CSS estáticos, uma rota estática por idioma: /pt-br/... e /en-us/... propostos, /pt-BR/... e /en-US/... como alternativa — PROPOSTO (ADR-0007)", "Entrega índice, teoria e matemática acessível sem exigir JavaScript para ler")
        Container(island, "Ilha de interatividade", "Componente isolado, hidratado sob demanda, só onde há exercício (ADR-0003)", "Corrige a resposta no próprio cliente e devolve feedback diagnóstico por alternativa")
        Container(offline, "Camada offline", "Cache do navegador; mecanismo EM ABERTO (ticket)", "Mantém o conteúdo já visitado, com seus exercícios, acessível sem rede")
        ContainerDb(progress, "Progresso local", "IndexedDB do dispositivo (ADR-0003)", "Guarda progresso sem conta e sem servidor; nenhum dado sai do dispositivo")
    }

    Rel(contributor, content, "Escreve teoria, exercícios e metadados", "Git")
    Rel(contributor, build, "Escreve e configura a aplicação", "Git")
    Rel(ci, validator, "Executa as auditorias do acervo hoje; validador e build de verificação a cada PR PROPOSTO (ADR-0006)", "Shell")
    Rel(validator, content, "Lê e verifica os arquivos do acervo", "Sistema de arquivos")
    Rel(build, validator, "Nó reprovado não vira página publicada (RF-18) — lugar do portão EM ABERTO (ticket)", "Verificação do acervo antes de publicar")
    Rel(build, content, "Lê metadados, teoria e exercícios do nó", "Sistema de arquivos, na build")
    Rel(build, host, "Publica o diretório estático — gatilho PROPOSTO (ADR-0006)", "Envio de arquivos")
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
`EM ABERTO (ticket)` na relação `build → validador`, e não como `PROPOSTO`: nenhum ADR deve
fechá-lo. O que **exige ADR** antes de existir está marcado `PROPOSTO` com o número do ADR
pendente: `ADR-0006` para o papel de portão de merge da CI, o gatilho de deploy e os previews;
`ADR-0007` para o gerador concreto, os diretórios e a forma exata da URL bilíngue. O que já
existe e funciona hoje — o workflow de auditorias — aparece como fato, com a parte proposta
separada no mesmo rótulo. O diagrama também **não** mostra fóruns, certificados nem
sincronização entre dispositivos: os três exigem estado compartilhado e ADR próprio.

## Contrato das fronteiras

| Fronteira | O que atravessa | O que nunca atravessa |
|---|---|---|
| `content/` → build | Arquivos do acervo lidos como dado: `meta.json`, `theory.<lang>.md`, `exercises.json` | Componente de framework, frontmatter proprietário ou lógica de aprendizagem — o acervo não conhece a aplicação (`ADR-0003`, independência do contrato de dados) |
| Validador → build | Aprovação ou reprovação do acervo, com arquivo, item e regra violada | Objeto inválido: nó reprovado não vira página (RF-18) |
| Build → host | Um diretório de arquivos estáticos, servível por qualquer host | Segredo, variável de ambiente com dado pessoal, função executada por requisição |
| Host → dispositivo | HTML, CSS, ativos e o payload do exercício — **incluindo o gabarito** | Identificador de usuário, cookie de sessão, resposta do aluno em qualquer direção |
| Página → ilha | Dados do exercício **já validados**, entregues na fronteira do componente — o *como* é decisão do ticket (`ADR-0007`, `proposed`, propõe propriedade serializada na build) | Hidratação da página inteira: recurso que a exija está mal desenhado (`ADR-0003`); e requisição de rede feita pela ilha — o payload já traz o que ela precisa (`ADR-0003`: offline do conteúdo visitado, sem backend) |
| Ilha → progresso local | Eventos de progresso do próprio dispositivo | Qualquer coisa que saia do dispositivo — sem rede, sem servidor, sem telemetria |

Consequência que atravessa todas as linhas: **o gabarito viaja no cliente** (L-008). Nada pode
depender do segredo da resposta — sem prova valendo nota, sem ranking, sem certificado
verificável.

## Fontes

- `docs/adr/ADR-0003-platform-stack.md` (`accepted`, 2026-08-01) — site estático com ilhas,
  local-first sem conta, portabilidade do host, independência do contrato de dados.
- `docs/adr/ADR-0006-continuous-integration-and-publication.md` (`proposed`) — integração
  contínua, previews e gatilho do deploy.
- `docs/adr/ADR-0007-application-skeleton.md` (`proposed`) — gerador concreto, diretórios,
  leitura de `content/` na build e lugar das ilhas.
- `docs/adr/ADR-0002-bilingual-content.md` — paridade obrigatória por idioma.
- `docs/architecture/c4-context.md` — nível acima; `docs/specs/minimum-learning-slice/`
  (RF-18, RNF-3, RNF-5) — comportamento exigido da primeira fatia.
- `tickets/TCK-0014-content-contract-validator/` — validador do contrato em execução.
