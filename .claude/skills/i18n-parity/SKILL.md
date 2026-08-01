---
name: i18n-parity
description: Verifica a paridade pt-BR/en-US do conteúdo e da interface — arquivos ausentes, seções divergentes, campos localizados incompletos, convenções de decimais e terminologia. Usar antes de publicar e em auditorias periódicas.
---

# Auditar paridade de idiomas

Regra do projeto: **nenhum objeto de aprendizagem existe em um idioma só** (AGENTS.md §2b).

## 1. Levantamento mecânico

```bash
bash scripts/audit-content.sh [caminho]
```

O script reporta: `theory.<lang>.md` faltando, campos `{"pt-BR": …, "en-US": …}` incompletos
em `meta.json`/`exercises.json`/`references.json`, e `languages[]` inconsistente com os
arquivos reais.

## 2. Paridade estrutural

Compare `theory.pt-BR.md` × `theory.en-US.md`:

- [ ] Mesmos títulos de seção, na mesma ordem
- [ ] Mesmos exemplos, com os mesmos números
- [ ] Mesmas fórmulas (o LaTeX deve ser idêntico, exceto por separador decimal)
- [ ] Mesma quantidade de exercícios/itens referenciados

## 3. Paridade semântica

- A tradução preserva o **significado matemático**? Tradução literal que muda o sentido é
  achado **bloqueante**.
- Terminologia consolidada conforme o glossário de `docs/content/i18n.md` (ex.: *range* →
  "conjunto imagem"; "função afim" → *affine/linear function*, com a distinção explicada).
- Nomes de teoremas conforme o uso corrente de cada idioma.

## 4. Convenções locais

| Item | pt-BR | en-US |
|---|---|---|
| Decimal | vírgula (`3,14`) | ponto (`3.14`) |
| Milhar | ponto ou espaço fino | vírgula |
| Data | `01/08/2026` | `2026-08-01` ou `August 1, 2026` |
| Intervalo | `[0, 1]` (mesma notação) | `[0, 1]` |

## 5. Saída

Tabela: **arquivo · tipo do achado (`ausente | estrutural | semântica | convenção`) ·
severidade · correção**. Se algum nó estiver monolíngue, exigir `status: "draft"` no
`meta.json` até a paridade ser restaurada. Termos novos fixados vão para o glossário em
`docs/content/i18n.md` e viram lição (`/capture-lesson`).
