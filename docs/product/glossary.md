# Glossário do projeto

Termos com significado **específico** neste repositório. Terminologia matemática bilíngue
fica em [`../content/i18n.md`](../content/i18n.md).

| Termo | Definição |
|---|---|
| **Nó (de conteúdo)** | Unidade endereçável do acervo: uma pasta `content/<stage>/<area>/<topic>/[<subtopic>]` com teoria, exercícios, referências e metadados. |
| **Estágio (`stage`)** | Faixa educacional: `early-childhood`, `elementary`, `middle-school`, `high-school`, `undergraduate`, `graduate`, `research`. |
| **Área (`area`)** | Ramo da matemática (`algebra`, `calculus`, `probability`, …), conforme lista canônica em `docs/content/taxonomy.md`. |
| **Habilidade (`skill`)** | Capacidade específica e verificável exercitada por exercícios (`solve-quadratic`), usada para diagnóstico e recomendação. |
| **Objeto de aprendizagem** | Qualquer artefato entregue ao aluno: teoria, exercício, avaliação, referência, asset. |
| **Trilha (`path`)** | Sequência curada de nós com objetivo declarado, marcos e critério de conclusão (`content/paths/`). |
| **Feedback diagnóstico** | Retorno que identifica **qual equívoco** produziu a resposta errada, não apenas que ela está errada. |
| **Paridade** | Estado em que pt-BR e en-US têm as mesmas seções, exemplos e significado. |
| **Ticket** | Unidade de trabalho auditável em `tickets/TCK-NNNN-<slug>/` (ADR-0004). |
| **Handoff** | Transferência registrada de um ticket entre agentes (ou entre CLIs). |
| **Lição (`L-NNN`)** | Regra aplicável no futuro, extraída de erro ou acerto, em `memory/lessons/`. |
| **Superfície de IA** | Conjunto de agents, skills, prompts, commands e workflows que os CLIs enxergam. |
| **Local-first** | Estratégia em que o estado do aluno vive no dispositivo, com sincronização opcional. |
