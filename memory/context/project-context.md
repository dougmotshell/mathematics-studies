# Project Context — Estado atual

> Atualizar sempre que o estado do projeto mudar (skill `/generate-project-context`).
> Datas absolutas. Não inflar: frente que não existe se descreve como "não iniciada".

**Última atualização:** 2026-08-01

## Estado em 2026-08-01 (bootstrap da superfície de IA)

O repositório foi inicializado com a **superfície de IA e os padrões de trabalho**. Desde
2026-08-01 (TCK-0015, **em revisão**) existe o esqueleto da aplicação na raiz e um pipeline
que vai do acervo ao HTML publicável; o conteúdo ainda é um nó piloto.

| Frente | Estado |
|---|---|
| **Conteúdo** (`content/`) | 1 nó piloto (`high-school/algebra/quadratic-equations`, `draft`) validando o contrato de dados; taxonomia em `docs/content/taxonomy.md`. |
| **Pipeline de conteúdo** | Primeiro artefato de implementação existe (TCK-0014, 2026-08-01): `scripts/validate-content.py` valida o contrato de carga de `content/` (RF-18) na linha de comando e em pipeline, com suíte própria e sem dependência nova. **Ligado ao CI e ao `prebuild` em TCK-0015** (portão do RF-18 nos dois caminhos). |
| **Plataforma** (aplicação web/PWA) | **Esqueleto entregue em TCK-0015** (em revisão), conforme `ADR-0007`: `package.json` (só `astro`), leitor de `content/` independente do gerador, rotas `/pt-br/…` e `/en-us/…`, build estática em `dist/`, `vercel.json` portátil, CI com validador + build de verificação. Uma página mínima por idioma — índice, leitor e player de exercícios são as tasks 5–8. Sem backend, conta ou telemetria. |
| **Superfície de IA** | Completa: 21 agents, 20 skills, 6 regras, 5 workflows, sistema de tickets. Adapters gerados para 12 ferramentas (Claude Code, Grok, Cursor, Copilot, Gemini, Antigravity, Windsurf, Codex, Zed, Cline, Junie, web). Auditorias verdes. |
| **Documentação** | Padrões estabelecidos (C4 + ADR + SDD), padrões de conteúdo escritos, **7 ADRs, todos `accepted`** (0001–0007). **Licença definida** (`ADR-0005`): `LICENSE` (MIT) e `LICENSE-CONTENT` (CC BY-SA 4.0) na raiz. |
| **Memória** | Estrutura criada e **em uso**: lições registradas e indexadas em `memory/LESSONS.md` (L-001 em diante); memórias individuais dos agentes sendo preenchidas pelos tickets. |

## Decisões aceitas

- `ADR-0001` — taxonomia de conteúdo por estágio/área/tópico com slugs estáveis.
- `ADR-0002` — bilinguismo obrigatório pt-BR/en-US em todo objeto de aprendizagem.
- `ADR-0003` — **stack da plataforma** (aceito em 2026-08-01, decisor Douglas Silva): site
  estático orientado a conteúdo com **ilhas de interatividade** só onde há exercício;
  progresso **local-first sem conta** (IndexedDB); PWA offline-first para conteúdo visitado;
  rotas estáticas por idioma; deploy estático na Vercel, portátil para qualquer host
  estático. **Backend, conta, login e telemetria identificável exigem ADR novo.** O contrato
  de dados de `content/` permanece independente da stack.
- `ADR-0006` — **integração contínua, previews e publicação** (aceito em 2026-08-01, decisor
  Douglas Silva, TCK-0016): GitHub Actions é o **portão de mérito** do repositório e a Vercel é
  a **construtora e publicadora**, por integração Git; **previews por PR ativados**, sem
  autenticação e sem domínio de produção; produção publica no **push/merge em `main`**.
  **Nenhum segredo no repositório**; Vercel Web Analytics e Speed Insights **desligados** —
  ligar qualquer telemetria de visitante exige ADR de privacidade (LGPD/COPPA). Mover o
  repositório para uma organização ou monetizar o projeto quebra a gratuidade e exige ADR novo.
- `ADR-0007` — **esqueleto da aplicação** (aceito em 2026-08-01, decisor Douglas Silva,
  TCK-0016): Astro como gerador concreto (Node ≥ 22.12.0), projeto **na raiz** do repositório,
  `src/content-contract/` como único leitor do acervo e sem importar o gerador, `package.json`
  mínimo (`dependencies` = só `astro`), e **URL com prefixo de idioma em minúsculas**
  (`/pt-br/…`, `/en-us/…`) com a taxonomia intacta — contrato público; caixa mista está
  descartada e mudar exige ADR + redirect. Dependência que chegue ao navegador exige
  justificativa no log e revisão do `security-auditor`; nada de CDN de terceiro.
- `ADR-0005` — **licença do projeto** (aceito em 2026-08-01, decisor Douglas Silva):
  `content/` sob **CC BY-SA 4.0**, código e material de processo sob **MIT** (titular Douglas
  Silva, 2026). Consequência operacional: fonte externa **CC BY / CC BY-SA / CC0 / domínio
  público** pode ser adaptada; fonte **CC BY-NC / CC BY-NC-SA** só pode ser **citada como
  leitura externa**, nunca incorporada.

## Decisões em aberto

- Sincronização de progresso entre dispositivos (exigiria conta + ADR de privacidade de
  menores) — adiada até haver demanda comprovada.
- Fóruns de discussão e certificados de conclusão — sem solução na stack aceita; exigem ADR
  próprio por dependerem de estado compartilhado.
- Biblioteca de UI, de testes e estratégia de service worker — decisões de implementação,
  fora do `ADR-0003`. Também o momento em que a matemática vira HTML (build × navegador).
- **Onde roda o portão que impede publicar acervo reprovado** — script do projeto, job de CI
  ou os dois. Aceitar o `ADR-0006` **não** fechou isto: a spec aprovada dá a escolha ao ticket
  (`plan.md`, item 5) e o ADR só exige o resultado (RF-18). O TCK-0015 a exerceu; trocar de
  lugar depois continua sendo decisão de ticket, não emenda de ADR.
- **Proteção de branch em `main`** — ato do usuário no GitHub (`ADR-0006`, pendência 2). Sem
  ela, a checagem do Actions é informativa e não impede merge.

## Próximos passos sugeridos

1. Concluir a spec da fatia mínima (`docs/specs/minimum-learning-slice/`) e atualizar o
   `plan.md` para citar a stack aceita em vez de "a definir".
2. Fechar o TCK-0001 (verificar referências do nó piloto e acrescentar fonte em pt-BR),
   agora sob a regra de compatibilidade do `ADR-0005`.
3. Criar mais 2–4 nós piloto em estágios distintos (`/new-topic`) — o contrato de dados só se
   prova com variedade real, e o esqueleto já existe para consumi-los.
4. Ligar a **proteção de branch em `main`** no GitHub (ato do usuário): sem ela, o portão de
   mérito do `ADR-0006` é apenas informativo.
5. Seguir para as tasks 5–8 da fatia mínima (índice, leitor, player, alternador de idioma),
   agora sem bloqueio de decisão — `ADR-0006` e `ADR-0007` estão aceitos.

## Riscos e pendências conhecidos

- Construir a aplicação antes de ter conteúdo real tende a produzir contrato de dados errado.
- Bilinguismo dobra o custo de produção de conteúdo: o fluxo precisa nascer com os dois
  idiomas, não "traduzir depois".
- Público inclui menores de idade: qualquer coleta de dados exige ADR de privacidade antes.
- SymPy não está instalado no ambiente: `/math-verify` opera com verificação numérica em
  Python puro até que isso mude (ver `memory/context/content.md`).
- CC BY-SA 4.0 (`ADR-0005`) encolhe o universo de fontes reutilizáveis: as três referências
  do nó piloto (OpenStax ×2 e *Livro Aberto de Matemática*) são **CC BY-NC-SA** e servem
  apenas como leitura externa. Produzir teoria e exercícios autorais custa mais do que
  adaptar — contar com isso no ritmo de produção de conteúdo.
