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
| **Plataforma** (aplicação web/PWA) | Não iniciada. Stack em avaliação — `ADR-0003` com status `proposed`. |
| **Superfície de IA** | Completa: 21 agents, 20 skills, 6 regras, 5 workflows, sistema de tickets. Adapters gerados para 12 ferramentas (Claude Code, Grok, Cursor, Copilot, Gemini, Antigravity, Windsurf, Codex, Zed, Cline, Junie, web). Auditorias verdes. |
| **Documentação** | Padrões estabelecidos (C4 + ADR + SDD), padrões de conteúdo escritos, 3 ADRs iniciais. |
| **Memória** | Estrutura criada; sem lições registradas além das de bootstrap. |

## Decisões aceitas

- `ADR-0001` — taxonomia de conteúdo por estágio/área/tópico com slugs estáveis.
- `ADR-0002` — bilinguismo obrigatório pt-BR/en-US em todo objeto de aprendizagem.

## Decisões em aberto

- `ADR-0003` — **stack da plataforma** (`proposed`). Nenhum ticket de implementação da
  aplicação deve avançar antes do aceite.
- Licença do conteúdo e do código — ainda não definida.
- Modelo de persistência de progresso (local-first × conta sincronizada).

## Próximos passos sugeridos

1. Decidir e aceitar `ADR-0003` (stack) — destrava a frente de plataforma.
2. Definir a licença do projeto (conteúdo e código).
3. Criar a primeira spec de produto (`/create-spec`) para a fatia mínima: navegar um nó de
   conteúdo e responder um exercício.
4. Fechar o TCK-0001 (verificar referências do nó piloto e acrescentar fonte em pt-BR).
5. Criar mais 2–4 nós piloto em estágios distintos (`/new-topic`) antes de construir a
   aplicação — o contrato de dados só se prova com variedade real.

## Riscos e pendências conhecidos

- Construir a aplicação antes de ter conteúdo real tende a produzir contrato de dados errado.
- Bilinguismo dobra o custo de produção de conteúdo: o fluxo precisa nascer com os dois
  idiomas, não "traduzir depois".
- Público inclui menores de idade: qualquer coleta de dados exige ADR de privacidade antes.
- SymPy não está instalado no ambiente: `/math-verify` opera com verificação numérica em
  Python puro até que isso mude (ver `memory/context/content.md`).
