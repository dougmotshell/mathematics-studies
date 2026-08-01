# ADR-0002 — Bilinguismo obrigatório pt-BR/en-US

- **Status:** accepted
- **Data:** 2026-08-01
- **Decisores:** Douglas Silva
- **Relacionados:** ADR-0001, `docs/content/i18n.md`, lição L-001

## Contexto

O projeto se propõe a oferecer conteúdo em português e inglês. A abordagem usual — escrever no
idioma principal e "traduzir depois" — produz, na prática, conteúdo permanentemente
monolíngue: a tradução nunca sobe na fila e as duas versões divergem estruturalmente a cada
revisão.

## Alternativas consideradas

### A. Paridade obrigatória no mesmo ciclo (escolhida)
- **Prós:** impede dívida de tradução; garante experiência equivalente nos dois idiomas;
  auditável mecanicamente.
- **Contras:** dobra o custo de produção de cada nó; reduz a velocidade aparente.

### B. Idioma principal pt-BR com tradução assíncrona
- **Prós:** publica mais rápido.
- **Contras:** en-US vira segunda classe; divergência estrutural cresce; usuário encontra
  páginas vazias ou desatualizadas.

### C. Tradução automática com revisão posterior
- **Prós:** cobertura imediata.
- **Contras:** matemática traduzida automaticamente erra terminologia e convenções
  (decimais, nomes de teoremas, "range" vs "conjunto imagem"); risco de erro conceitual.

## Decisão

Todo objeto de aprendizagem existe em **pt-BR e en-US, em paridade estrutural e semântica**,
produzido no mesmo ciclo de trabalho. Enquanto faltar um idioma, o nó permanece
`status: "draft"` e não é publicado. Tradução automática pode ser ponto de partida, nunca
entrega final — revisão humana/agente é obrigatória.

## Consequências

**Positivas**
- Nenhum usuário encontra conteúdo pela metade no seu idioma.
- A terminologia bilíngue é decidida uma vez e registrada no glossário.

**Negativas / custos assumidos**
- Produção mais lenta por nó; o roadmap precisa refletir isso.
- Toda revisão altera dois arquivos.

**O que fica mais difícil depois desta decisão**
- Adicionar um terceiro idioma multiplica o custo; exigiria novo ADR.

## Impacto

- **Conteúdo:** `theory.pt-BR.md` + `theory.en-US.md`; campos localizados como objetos
  `{"pt-BR": …, "en-US": …}`.
- **Plataforma:** rotas e catálogo de strings nos dois idiomas.
- **Processo/agentes:** `i18n-steward` valida; `/i18n-parity` e `scripts/audit-content.sh`
  verificam antes da publicação.

## Como reverter

Reversível (bastaria relaxar a exigência), mas com custo de credibilidade: conteúdo já
publicado em dois idiomas cria expectativa.
