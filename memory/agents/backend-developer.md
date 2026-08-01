# Memória do agente `backend-developer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Implementa a camada de dados e serviços — persistência de progresso, sincronização, autenticação, APIs, pipeline de build do conteúdo e integrações. Usar para executar tickets de backend/dados.

## Notas persistentes

- **Duas ferramentas que se sobrepõem de propósito** (corrigido em 2026-08-01: eu havia
  declarado divisão estanque, e era falso — identidade, gabarito, campos localizados e
  `answer` já existiam no auditor). `scripts/audit-content.py` é auditoria editorial e cobre
  mais coisa; `scripts/validate-content.py` é o portão de carga (RF-18) e **repete** o que a
  renderização exige, porque não pode depender de outra ferramenta ter rodado. Onde há
  sobreposição, o validador prevalece por ser o mais estrito. **Antes de descrever fronteira
  entre ferramentas, ler o código da outra e citar linha** — descrição errada vira mapa errado
  da malha de segurança e se propaga para `memory/`.
- **Fixture de conteúdo nunca dentro de `content/`.** Ia quebrar `audit-content.sh`. O
  validador aceita `--root` justamente para que a fixture viva em diretório temporário e a
  regra `nodeId` × caminho continue testável.
- **Fixture = cópia do nó real com UMA mutação.** Prova que a regra pega aquele defeito e que
  não inventa outros; e o caso "cópia intacta" vira o teste de falso positivo de graça.
- **Zero valores válidos são armadilha recorrente.** `tolerance: 0` é válido, ausente não é.
  Qualquer checagem por veracidade implícita (`if not tolerance`) reprova conteúdo correto.
- Teste de CLI no repositório: bash + Python stdlib, molde de `tools/context-watch-test.sh`.
  Não há runner instalado e o ADR-0003 não decidiu nenhum.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0014 — validador do contrato de `content/` (RF-18) | `scripts/validate-content.{py,sh}` + suíte de 84 asserções; piloto passa sem tocar em `content/`; handoff ao `code-reviewer` | L-019 |
| 2026-08-01 | TCK-0014 — REJECT [006], loop 1/3 | **reincidência da L-019 que eu mesmo escrevi** (B1 travessia parava no alvo; B2 stderr fora da proteção) + fronteira falsa propagada para `memory/` (B3). Corrigidos; suíte 84 → 118 | L-019 (adendo), L-013, L-018 |
