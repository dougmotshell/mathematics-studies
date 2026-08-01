---
applyTo: "src/**,app/**,api/**,tests/**,e2e/**"
---

# Instruções para o código da aplicação

> A stack ainda **não está decidida** (`docs/adr/ADR-0003-platform-stack.md`, status
> `proposed`). Não introduzir framework, banco ou serviço sem ADR aceito.

- **Nenhuma implementação sem spec aprovada** (`docs/specs/<slug>/`) e ticket
  (`tickets/TCK-NNNN-<slug>/`).
- Identificadores em **en-US**; comentários e mensagens de commit (corpo) em **pt-BR**.
- **i18n**: nenhuma string voltada ao usuário hard-coded — tudo em catálogo pt-BR/en-US.
- **Acessibilidade** é requisito: semântica correta, foco visível, operação por teclado,
  contraste, alvo de toque ≥ 24 px, `prefers-reduced-motion`. Matemática renderizada com
  KaTeX + descrição textual; nunca imagem de fórmula.
- **Offline/PWA**: o conteúdo já visitado abre sem rede; o estado do aluno sobrevive a
  recarregamento e queda de conexão.
- **Privacidade**: público inclui menores. Minimização de dados; qualquer coleta
  identificável exige ADR de privacidade (LGPD/COPPA) antes da implementação. Segredos só em
  variáveis de ambiente.
- **Custo zero**: preferir free tier e soluções estáticas; dependência nova exige
  justificativa de custo/benefício (peso no bundle conta).
- Funcionalidade nova nasce com teste. Rodar lint/testes/build antes de entregar e **relatar
  a saída real**, inclusive falhas.
- Não alterar `content/` para fazer o código passar — se o contrato de dados está errado,
  escalar ao `platform-architect`.
