**Tipo:** erro
**ID:** L-004
**Contexto:** 2026-08-01, ao ampliar a superfície de IA para Cursor, Antigravity, Grok e
outras ferramentas. Descoberto ao inspecionar `~/.codex/prompts` antes de rodar
`sync-ai-adapters.py --codex`.

**Lição:** algumas ferramentas descobrem comandos apenas em um diretório **global por
usuário**, não por repositório — o Codex usa `$CODEX_HOME/prompts` (top-level, sem
subpastas). Dois repositórios que instalam prompts com nomes genéricos (`create-adr`,
`dev-loop`, `researcher`) se sobrescrevem silenciosamente: o último a rodar vence, e o
comando passa a apontar para o repo errado sem nenhum aviso. No caso concreto, 12 nomes
colidiam com os do `product-kpi-ai`.

**Como aplicar:** antes de instalar comandos em diretório global, **listar o que já existe e
comparar os nomes**. Havendo colisão, isolar (`CODEX_HOME` por projeto, via `.envrc` — ver
`.envrc.example`) ou prefixar (`--codex-prefix ms`). Sempre incluir o nome do projeto na
descrição do prompt (`[mathematics-studies] …`), para que a origem seja visível na lista da
ferramenta. Vale para qualquer ferramenta futura com configuração global: verificar o escopo
(global × repositório) **antes** de escrever. Ver [[content-slugs-are-public-urls]] — mesma
família de problema: nome que vira contrato compartilhado.
