**Tipo:** sucesso
**ID:** L-008
**Contexto:** 2026-08-01, `TCK-0003` — aceite do `ADR-0003` (site estático com ilhas de
interatividade e progresso local-first, sem backend).

**Lição:** escolher arquitetura estática sem servidor decide, no mesmo ato, o que o **produto**
pode prometer. Sem backend, o gabarito do exercício viaja no payload entregue ao navegador:
qualquer funcionalidade que dependa do segredo da resposta (prova valendo nota, ranking
competitivo, certificado com verificação externa) nasce impossível. Escrever essa consequência
na seção **Consequências** do ADR, no momento do aceite, evita que ela seja descoberta meses
depois por um ticket de produto que assume um servidor inexistente.

**Como aplicar:** ao aceitar um ADR de arquitetura, derivar explicitamente (a) o que a decisão
**proíbe** ao produto, não só o que ela permite, e (b) a lista fechada de recursos que
**exigem ADR novo** — aqui: backend, conta, login e telemetria identificável. Ao desenhar
exercício ou avaliação neste projeto, assumir sempre que o aluno pode ler a resposta; o valor
está no feedback diagnóstico e na trilha, não no sigilo. Ver
[[triage-is-not-handoff]] para a disciplina equivalente no plano de processo.
