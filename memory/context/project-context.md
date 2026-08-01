# Project Context — Estado atual

> Atualizar sempre que o estado do projeto mudar (skill `/generate-project-context`).
> Datas absolutas. Não inflar: frente que não existe se descreve como "não iniciada".

**Última atualização:** 2026-08-01

## Estado em 2026-08-01 (bootstrap da superfície de IA)

O repositório foi inicializado com a **superfície de IA e os padrões de trabalho**. Não há
aplicação nem conteúdo ainda.

| Frente | Estado |
|---|---|
| **Conteúdo** (`content/`) | 1 nó piloto (`high-school/algebra/quadratic-equations`, `draft`) validando o contrato de dados; taxonomia em `docs/content/taxonomy.md`. |
| **Plataforma** (aplicação web/PWA) | Não iniciada, mas **destravada**: `ADR-0003` aceito em 2026-08-01 — site estático orientado a conteúdo (Astro) com ilhas de interatividade, progresso local-first em IndexedDB, deploy estático na Vercel. Sem backend, conta ou telemetria. |
| **Superfície de IA** | Completa: 21 agents, 20 skills, 6 regras, 5 workflows, sistema de tickets. Adapters gerados para 12 ferramentas (Claude Code, Grok, Cursor, Copilot, Gemini, Antigravity, Windsurf, Codex, Zed, Cline, Junie, web). Auditorias verdes. |
| **Documentação** | Padrões estabelecidos (C4 + ADR + SDD), padrões de conteúdo escritos, 5 ADRs aceitos. **Licença definida** (`ADR-0005`): `LICENSE` (MIT) e `LICENSE-CONTENT` (CC BY-SA 4.0) na raiz. |
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
  fora do `ADR-0003`.

## Próximos passos sugeridos

1. Concluir a spec da fatia mínima (`docs/specs/minimum-learning-slice/`) e atualizar o
   `plan.md` para citar a stack aceita em vez de "a definir".
2. Fechar o TCK-0001 (verificar referências do nó piloto e acrescentar fonte em pt-BR),
   agora sob a regra de compatibilidade do `ADR-0005`.
3. Criar mais 2–4 nós piloto em estágios distintos (`/new-topic`) antes de construir a
   aplicação — o contrato de dados só se prova com variedade real.
4. Só então abrir o ticket de esqueleto da aplicação, sob as restrições do `ADR-0003`.

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
