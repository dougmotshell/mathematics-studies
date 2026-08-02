# Contexto operacional — frontend

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01

## Estado atual

- **Esqueleto entregue pelo TCK-0015** em 2026-08-01 (em revisão quando esta nota foi escrita):
  projeto Astro na raiz, `src/` criado, uma página mínima por idioma. Índice, leitor e player
  são as tasks 5–8.
- **Stack decidida em 2026-08-01** (`ADR-0003`, aceito): gerador de site estático orientado a
  conteúdo (**Astro**) com **ilhas de interatividade**; progresso **local-first sem conta**
  em **IndexedDB**; deploy estático na **Vercel**.
- Ainda **não decididos** (implementação, não ADR): biblioteca de UI dentro das ilhas,
  framework de testes, estratégia/ferramenta de service worker e o **momento de renderização
  do KaTeX** (build × runtime).
- **Esqueleto da aplicação: decidido** (`ADR-0007`, **`accepted`** em 2026-08-01 por Douglas
  Silva, TCK-0016). Vale como fato: Astro como gerador concreto; projeto **na raiz** do
  repositório; `src/` com `content-contract/`, `pages/`, `layouts/`, `components/`, `islands/`,
  `styles/`; `package.json` mínimo (só `astro`, `private: true`, `engines.node >= 22.12.0`, com
  `validate:content` como ponto de entrada nomeado do validador); **URL com prefixo de idioma
  em minúsculas** (`/pt-br/…`, `/en-us/…`) e taxonomia intacta — a grafia em caixa mista está
  **descartada** e voltar a ela exige ADR novo. `src/content-contract/` não importa nada do
  gerador; dependência que chegue ao navegador exige justificativa no log e revisão do
  `security-auditor`; nada de CDN de terceiro.
- **Não decidido, e nenhum ADR deve decidir:** **onde** roda o portão que impede publicar
  acervo reprovado — script do projeto, job de CI ou os dois. A spec aprovada atribui isso ao
  ticket (`docs/specs/minimum-learning-slice/plan.md`, item 5). O ADR só exige o **resultado**:
  nó que viole o contrato não vira página publicada, com falha visível e registrada (RF-18).
- **CI/CD e publicação: decididos** (`ADR-0006`, **`accepted`** em 2026-08-01) — GitHub Actions
  como portão de mérito, Vercel como construtora/publicadora por integração Git, **previews por
  PR ativados**, deploy no push em `main`. Sem segredo no repositório; Vercel Web Analytics e
  Speed Insights **desligados** (ligar exige ADR de privacidade).
- **C4 Container desenhado** em `docs/architecture/c4-container.md` (2026-08-01): acervo,
  validador, build, host, páginas por idioma, ilha, camada offline e progresso local, com o
  contrato de cada fronteira. Depois do aceite dos ADR-0006/0007 **não há mais marcador
  `PROPOSTO`** neste nível; o que é decisão de ticket segue como `EM ABERTO (ticket)`.

## Pegadinhas conhecidas

- Nenhuma registrada.

## Decisões operacionais em vigor

Decorrem do `ADR-0003` e valem para todo trabalho de frontend:

1. **JavaScript mínimo por padrão.** Página de teoria é HTML + CSS. Interatividade só dentro
   de uma ilha, com fronteira explícita. Recurso que exija hidratar a página inteira está mal
   desenhado — reprojetar antes de implementar.
2. **Uma rota estática por idioma**, com paridade obrigatória (`ADR-0002`). Nada de fallback
   silencioso: nó sem os dois idiomas fica `draft` e fora das rotas publicadas.
3. **Offline-first para o conteúdo visitado** — incluindo os exercícios do nó. É requisito de
   arquitetura, não acabamento.
4. **KaTeX acessível**: descrição textual para toda fórmula em display
   (`docs/content/accessibility.md`), imagem de fórmula proibida onde LaTeX resolve, e sem
   custo de JavaScript desproporcional numa página de teoria. O **momento** da renderização
   (build × runtime) **não está decidido** — é escolha do ticket de implementação
   (`docs/specs/minimum-learning-slice/plan.md`), não do `ADR-0003`.
5. **Não há backend, conta, login nem telemetria identificável.** Qualquer um dos quatro
   exige **ADR novo** (com LGPD/COPPA, o público inclui menores). Não assumir disponíveis.
6. **O gabarito viaja no cliente.** Nenhuma funcionalidade pode depender do segredo da
   resposta — sem avaliação valendo nota, sem ranking, sem certificado verificável.
   Feedback diagnóstico assume aluno capaz de ler a resposta.
7. **Portabilidade do deploy:** a saída da build é um diretório estático servível por
   qualquer host. Recurso proprietário da Vercel que quebre isso exige ADR.
8. **Contrato de dados de `content/` é independente da stack** — proibido frontmatter
   proprietário, componente de framework dentro do Markdown ou lógica de aprendizagem
   (pré-requisito, dificuldade, gabarito, feedback) morando no código em vez do dado.
