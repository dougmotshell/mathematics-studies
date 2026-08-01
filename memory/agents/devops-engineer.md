# Memória do agente `devops-engineer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Cuida de CI/CD, build, deploy na Vercel, previews, variáveis de ambiente, monitoramento e performance de entrega. Usar para tickets de infraestrutura, pipeline e publicação.

## Notas persistentes

- **Pipeline da aplicação (a partir de TCK-0015):** `npm run build` = `prebuild`
  (`validate-content.sh` **e** `audit-content.sh`) + build estática em `dist/`. As duas
  auditorias também são passos do Actions. Decisão registrada: **portão nos dois caminhos**,
  porque o host constrói o que foi empurrado e não lê o resultado do CI — gate só no CI deixa
  o push direto em `main` publicar acervo reprovado.
- **Portão se lista por CAMINHO, não por ferramenta** (L-019, adendo TCK-0015). Errei aqui:
  pus o validador do RF-18 nos dois caminhos e deixei a auditoria editorial — a única que
  enxerga paridade bilíngue — só no merge; push direto publicava nó monolíngue. Antes de
  entregar pipeline, montar a matriz *caminhos que chegam ao usuário × verificações* e
  conferir célula a célula.
- **Portão só existe se estiver no caminho e derrubar o processo.** Ao entregar um, provar
  com fixture inválida: código de saída ≠ 0 **e** `find dist -name '*.html' | wc -l` = 0.
  Diretório de saída existir não é publicação — build derrubada deixa lixo intermediário.
- **Padrão de detecção se escreve como classe, e se prova pelos dois lados** (L-019, 3º
  adendo). Estreitei o padrão de terceiros para não reprovar link de referência (falso
  positivo legítimo) e abri 8 falsos negativos: protocolo relativo `//host`, aspas simples,
  `@import` sem `url()`, `<object data>`, `<a ping>`, `meta refresh`, `<image href>` e
  **qualquer tag em maiúscula** (faltava `-i`). Bateria mínima ao mexer em detector: vetores
  que **precisam reprovar** + casos legítimos que **precisam passar**, derivados da classe.
  E lembrar que `dist/` contém o que `public/` copia verbatim — arquivo que ninguém escreveu
  na aplicação.
- **`if grep …; then falha; fi` em passo de CI aprova o que não conseguiu olhar:** `grep -r`
  sai **2** com alvo inexistente e o `if` só trata `0`. Receita: `test -d` no alvo, contagem
  de objetos > 0, e `case "$rc" in 0|1|*)` — inconclusivo reprova. Provar executando o bloco
  `run:` **extraído do próprio workflow**, com alvo presente e ausente.
- **Defesa em duas camadas para regra de publicação:** portão (script, removível) + rede de
  segurança no código que gera a rota (não removível sem quebrar a build). Para regra de
  paridade/idioma, a rede **falha**, não pula o nó: pular é o fallback silencioso proibido
  pelo `AGENTS.md` §2b.
- **Constante de módulo que resolve caminho é armadilha:** avaliada na carga, ela lança no
  `import` e inutiliza o parâmetro que o chamador passaria. Função memorizada resolve.
- **Ambiente de host se verifica, não se presume:** a imagem de build da Vercel é Amazon
  Linux 2023 e a lista publicada de pacotes **não** cita `python3`; rodar a cadeia inteira em
  `docker run --rm amazonlinux:2023` (+ `dnf install nodejs22`) resolveu a pendência 1 do
  `ADR-0006` em minutos. Detalhes e demais pegadinhas: `memory/context/devops.md`.
- **Independência do contrato de dados é testável por `grep`** — e o teste é frágil ao
  próprio texto: escrever o nome do gerador em **comentário** dentro de
  `src/content-contract/` já derruba o `grep` que o `ADR-0007` nomeia. Não citar a ferramenta
  ali, nem em prosa.
- **Hooks do Claude Code (a partir de TCK-0012):** o repositório registra dois em
  `.claude/settings.json` — `PostToolBatch` → `python3 tools/context-watch.py --hook`
  (avisa só quando a zona de contexto sobe) e `PreCompact` matcher `auto` →
  `bash tools/precompact-snapshot.sh` (escreve o handoff antes da compactação lossy).
  Ao mexer nesse arquivo: **nunca** reescrever sem preservar `permissions`; validar com
  `jq -e` (settings malformado desativa o arquivo inteiro em silêncio) e conferir que o
  `git diff` tem só inserções.
- **Hook não pode bloquear:** todo comando de hook deste repo sai `0` sempre; exit code de
  hook tem semântica de bloqueio no Claude Code. Isso inclui o caminho em que a **escrita**
  falha (`| head`, `> /dev/full`): sem `flush()` dentro do `try` + `dup2` para `os.devnull`,
  o Python sai `120` no shutdown e a invariante vira mentira documentada.
- **Medição incerta avisa cedo, nunca calada** (L-015): janela presumida usa o valor
  conservador e o hook declara a presunção uma vez por sessão. **Presunção refutada pela
  medida é abandonada** (L-017), e o estado do antirruído zera quando a régua muda — senão o
  alarme satura no topo e o mecanismo morre calado.
- **Verificar o desfecho, não a linha citada no `REJECT`** (L-018): encenar a promessa
  inteira (estado zerado, medidas crescentes, mais de um disparo) antes de dizer "resolvido".
- **`permissions` só se amplia a pedido do usuário** (L-016); provar preservação com
  `diff` de `jq -S` contra o `HEAD`, não com "o diff só tem inserções".
- **Hook ruidoso morre:** aviso repetido a cada chamada de ferramenta faz o usuário
  desligar o mecanismo. O estado da última zona vive em
  `${XDG_STATE_HOME:-~/.local/state}/mathematics-studies/`, fora do repositório.
- **Testes sem framework:** o padrão do repo é script bash + Python 3 da stdlib montando
  fixtures em `mktemp -d` (`tools/context-watch-test.sh`, 41 asserções), plugado no
  workflow `ai-surface-audit.yml`. Nada de `pip install`.
- **Medida de contexto:** `python3 tools/context-watch.py` (exit `0/10/20/30/40`). Sem
  telemetria, sai `40` — nunca inventar estimativa para Codex/Copilot/Gemini.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0012 — detectar esgotamento de contexto e disparar handoff | `context-watch.py` + hooks + `agent-handoff.sh snapshot` + suíte de 41 casos no CI; handoff ao `code-reviewer` | hooks só recarregam via `/hooks`/reinício — critério 9 |
| 2026-08-01 | TCK-0012 — `REJECT` 1/3 do `code-reviewer` (B1–B4) | janela presumida virou conservadora + aviso no hook; `--hook` sai 0 mesmo com stdout quebrado; suíte isolada do `HOME` (41 → 65 asserções); duas entradas de `permissions.allow` revertidas | L-015, L-016 |
| 2026-08-01 | TCK-0015 — `REJECT` 2/3 (B4: detector estreitado demais) | padrão do passo de terceiros reescrito a partir da classe (`-i`, `//host`, aspas simples, `data`/`ping`/`poster`/`formaction`/`background`/`srcset`, `@import`, `meta refresh`, `<object>`/`<embed>`), 26 vetores contra o bloco `run:` versionado + fixture em `public/`; S9–S12 | L-019 (3º adendo): tirar falso positivo abre falso negativo |
| 2026-08-01 | TCK-0015 — `REJECT` 1/3 do `code-reviewer` (B1–B3) | auditoria editorial entrou no `prebuild` + leitor falha alto sem paridade bilíngue; três passos de CI com alvo conferido e três desfechos de `grep`; raiz deixou de publicar frases coladas; S3/S4/S5/S7 incorporadas | L-019 (2º adendo): portão se lista por caminho; `grep` tem 3 códigos de saída |
| 2026-08-01 | TCK-0015 — esqueleto da aplicação e pipeline de publicação | esqueleto do ADR-0007 na raiz + validador, build de verificação e greps de independência/terceiros no CI; portão do RF-18 no `prebuild` **e** no Actions; `vercel.json` sem recurso proprietário; handoff ao `code-reviewer` | pendência 1 do ADR-0006 resolvida em contêiner AL2023; `import.meta.url` não sobrevive ao empacotamento |
| 2026-08-01 | TCK-0012 — `REJECT` 2/3 (B5 alarme saturado, B6 fd fechado) | presunção refutada pela medida passa a ser abandonada (escalona um degrau e anuncia); estado rearma ao trocar a régua; `>&-` tratado; janela declarada em `.claude/settings.local.json` (65 → 93 asserções) | L-017, L-018 |
