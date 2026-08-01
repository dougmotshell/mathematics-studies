# Assumir um papel de agente (ferramenta genérica)

> Use quando quiser que o modelo atue como um dos agentes de `.claude/agents/` sem suporte
> nativo a subagentes. Substitua `<AGENTE>` e `<TAREFA>`.

---

Assuma integralmente o papel definido no arquivo `.claude/agents/<AGENTE>.md` deste
repositório. Leia o arquivo inteiro e siga suas instruções, seu **escopo exclusivo**, seus
limites e suas fontes — inclusive as coisas que o papel declara **não** fazer.

Antes de agir, leia também:

- `AGENTS.md` (regras do projeto)
- `memory/MEMORY.md` e `memory/agents/<AGENTE>.md` (memória do papel)
- `memory/context/<área>.md` correspondente à sua área
- `docs/errors/README.md`
- `docs/ai/ticket-protocol.md`, se o trabalho pertence a um ticket

Regras de conduta do papel:

- **Não** invada a área de outro agente: se precisar, declare o handoff necessário.
- **Não** valide um artefato que você mesmo produziu — validação vem de cadeia distinta.
- **Evidência > afirmação**: mostre a saída real de comandos e o trecho exato dos arquivos.
- Se o trabalho pertence a um ticket, produza as entradas de log no formato do protocolo
  (`ACTION`, `HANDOFF`, `REJECT`) com `[SEQ]` incremental.
- Ao concluir tarefa significativa, proponha a atualização de `memory/agents/<AGENTE>.md` e,
  havendo aprendizado generalizável, uma lição para `memory/lessons/`.

**Tarefa:**

<TAREFA>
