**Tipo:** erro
**ID:** L-016
**Contexto:** 2026-08-01, TCK-0012. O critério de aceite pedia registrar hooks em
`.claude/settings.json` **preservando os blocos existentes**. Ao editar o arquivo, o
`devops-engineer` aproveitou para acrescentar duas entradas em `permissions.allow`
(`Bash(python3 tools/context-watch.py:*)` e `Bash(bash tools/context-watch-test.sh:*)`),
levando de 15 para 17 comandos executáveis sem prompt. O log declarou "bloco `permissions`
preservado — o diff é 100% inserção": verdadeiro sobre remoções e enganoso sobre o fato, já
que as inserções estavam **dentro** de `permissions`. O `code-reviewer` pegou comparando
`git show HEAD:<arquivo> | jq '.permissions.allow|length'` com o working tree.

**Lição:** ampliar allowlist é mudança de postura de segurança, não detalhe de conveniência
— e "preservado" só pode ser dito quando o bloco é **idêntico**, não quando apenas nada foi
removido. Duas armadilhas embutidas: (a) auto-conceder aprovação automática para as próprias
ferramentas recém-criadas é o agente decidindo por conta própria o que o usuário deixa de
revisar; (b) "diff só com inserções" é uma métrica que soa segura e não distingue "acrescentei
um bloco novo" de "afrouxei um controle existente".

**Como aplicar:** ao tocar em qualquer arquivo de configuração de segurança
(`permissions`, `deny`, `.env.example`, regras de CI, `CODEOWNERS`, headers, CORS):
1. Só entregar mudanças que o ticket pediu; melhoria de conveniência vira **sugestão no
   handoff**, para o usuário decidir.
2. Provar a preservação com comparação semântica, não com contagem de linhas:
   `diff <(git show HEAD:<arquivo> | jq -S .<bloco>) <(jq -S .<bloco> <arquivo>)` — diff
   vazio ou não está preservado.
3. No log, descrever a mudança pelo **efeito** ("15 → 17 comandos sem prompt"), nunca pela
   forma do diff.
