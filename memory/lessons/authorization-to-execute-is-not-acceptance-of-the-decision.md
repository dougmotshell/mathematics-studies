# Autorização para executar não é aceite da decisão

**Tipo:** correção
**ID:** L-025
**Contexto:** 2026-08-01, `TCK-0016` (aceite do `ADR-0006` e do `ADR-0007`). O usuário disse
"configure tudo para o deploy" e "implemente o projeto base". O `devops-engineer` executou
(`TCK-0015`: `package.json`, `src/`, `vercel.json`, workflow) sob dois ADRs ainda `proposed` —
e o `ADR-0006:10-12` proibia isso em letra: *"enquanto não for aceito, nenhum ticket pode criar
ou alterar pipeline com base nele"*. O `qa-validator#9` detectou a contradição ao fechar o
`TCK-0011`. Nada estava errado na execução: a autorização era real e as três decisões pendentes
haviam sido tomadas. O que faltava era o **registro**.

**Lição:** autorização do usuário e aceite de ADR resolvem coisas diferentes e **não se
substituem**. A autorização destrava a *execução* de um trabalho concreto; o aceite fixa a
*decisão* que qualquer trabalho futuro herda. Executar com autorização e sem aceite produz um
estado em que a norma vigente proíbe o que já está feito — e quem chega depois não sabe se o
que existe é decisão ou improviso. O sintoma tem forma fixa e é detectável sozinho: **o ADR que
governa o artefato diz `proposed` enquanto o artefato existe no working tree**.

Corolário para quem escreve o ADR: a cláusula "nenhum ticket pode X antes do aceite" cria uma
dependência humana. Quem a escreve fica responsável por pedir o ticket de aceite **no mesmo
handoff** — não basta avisar que o bloqueio existe. Um bloqueio anunciado sem caminho de saída
é atropelado pela primeira autorização informal.

**Como aplicar:**

1. Ao propor ADR do qual um ticket já depende, sair do ticket com **duas** saídas declaradas:
   o handoff de execução **e** o pedido do ticket de aceite ao `tech-lead`. Um sem o outro é
   entrega incompleta.
2. Ao receber autorização do usuário para implementar algo governado por ADR `proposed`,
   verificar o status **antes** de executar. Se estiver `proposed`, a autorização vale para o
   trabalho — e abre um ticket de aceite em paralelo, não depois.
3. Ao aceitar o ADR depois de a implementação já existir, escrever no próprio ADR que **o
   aceite autoriza aquele trabalho e não atesta que ele esteja correto**, nomeando o ticket em
   revisão. ADR não é laudo de qualidade de código que ele não reviu.
4. Verificação barata, em qualquer auditoria de governança: para cada ADR `proposed`, procurar
   no working tree os artefatos que ele nomeia. Se existirem, ou o ADR está atrasado ou o
   ticket está fora da norma — nunca é "só formalidade".
