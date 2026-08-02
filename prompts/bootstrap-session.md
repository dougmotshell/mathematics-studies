# Bootstrap de sessão (ferramenta genérica)

> Cole este texto no início de uma sessão em qualquer assistente que **não** leia
> automaticamente o `AGENTS.md`. Substitua `<TAREFA>` no final.

---

Você vai trabalhar no repositório **mathematics-studies**: uma plataforma web gratuita
(PWA, deploy na Vercel) de estudos de matemática, da educação infantil à pesquisa, com
conteúdo **bilíngue pt-BR/en-US**, exercícios interativos com feedback diagnóstico e
acompanhamento de progresso.

**Antes de qualquer coisa, leia nesta ordem** (peça os arquivos se não tiver acesso direto):

1. `AGENTS.md` — fonte única de instruções (obrigatório, leia inteiro)
2. `memory/MEMORY.md` — índice da memória compartilhada
3. `docs/errors/README.md` — erros já cometidos, para não repetir
4. `docs/ai/ticket-protocol.md` — como o trabalho é executado e registrado
5. Os padrões relevantes à tarefa em `docs/content/` ou `docs/DOC-STANDARDS.md`

**Regras que não podem ser violadas:**

1. Conteúdo do produto é **sempre bilíngue** pt-BR + en-US, em paridade. Nunca publicar
   monolíngue.
2. **Nenhum resultado matemático não trivial vira gabarito sem verificação** (simbólica,
   numérica ou demonstração revisada).
3. Nomes de arquivos, pastas e identificadores em **en-US**; documentação e comentários em
   **pt-BR**.
4. Slugs de `content/` são **URLs públicas** — não renomear sem ADR e redirect.
5. **Nenhuma implementação sem spec aprovada** (`docs/specs/`) e sem ADR para decisões
   estruturais. A stack está decidida (`ADR-0003`, `accepted`): site estático com ilhas de
   interatividade e progresso local-first (IndexedDB). **Backend, conta, login e telemetria
   identificável exigem ADR novo** — não presumir que existam. Também decididos em 2026-08-01:
   projeto **Astro na raiz** e URL `/pt-br/…` · `/en-us/…` (`ADR-0007`); Actions como portão de
   mérito, Vercel publicando por integração Git, previews por PR (`ADR-0006`).
6. Acessibilidade (WCAG 2.2 AA), funcionamento offline, custo zero e privacidade de menores
   (LGPD/COPPA) são requisitos, não desejos.
7. **Não** fazer commit, push, deploy ou qualquer gasto sem pedido explícito.
8. Fontes externas só gratuitas, com autor, ano, URL e licença registrados. Publicamos
   `content/` sob **CC BY-SA 4.0** e o código sob **MIT** (`ADR-0005`): fonte **CC BY /
   CC BY-SA / CC0 / domínio público** pode ser adaptada; fonte **CC BY-NC, CC BY-NC-SA, ND ou
   sem licença** é **só citável** — nunca incorporada nem traduzida para dentro do conteúdo.

**Formato de trabalho:** diga o que vai fazer, faça, e apresente evidência do resultado
(saída de comando, trecho do arquivo). Se algo estiver ambíguo, pergunte antes de assumir.
Ao final de tarefa significativa, proponha as atualizações de `memory/` correspondentes.

**Tarefa:**

<TAREFA>
