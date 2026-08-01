---
name: content-audit
description: Audita um nó, uma área ou todo o conteúdo — estrutura da taxonomia, completude didática, rigor, exercícios, referências e metadados. Usar antes de publicar e periodicamente para encontrar lacunas e inconsistências.
---

# Auditar conteúdo

## 1. Camada mecânica (sempre primeiro)

```bash
bash scripts/audit-content.sh [caminho]
```

Cobre: estrutura de pastas, `meta.json` válido, paridade de idiomas, schema dos exercícios,
pré-requisitos existentes e grafo acíclico, referências com licença.

Não repita à mão o que o script já faz — parta dos achados dele.

## 2. Camada didática (leitura humana/agente)

Para cada nó auditado, verifique:

- [ ] **Objetivo de aprendizagem** explícito e observável
- [ ] **Pré-requisitos** realmente necessários (nem faltando, nem inflados)
- [ ] **Progressão**: intuição antes do formalismo; exemplo antes da generalização
- [ ] **Exemplos** cobrem o caso típico **e** pelo menos um não rotineiro
- [ ] **Erros comuns** documentados, com a causa do equívoco
- [ ] **Dificuldade** coerente com o estágio e com os nós vizinhos
- [ ] **Exercícios** cobrem todas as `skills[]` declaradas, com gradiente 1→5
- [ ] **Feedback** dos distratores é diagnóstico, não genérico
- [ ] **Referências** gratuitas, com licença e efetivamente relacionadas ao nó

## 3. Camada de rigor

Delegue ao `math-reviewer` (ou aplique o mesmo método): hipóteses omitidas, casos-limite,
gabaritos conferidos de forma independente, notação consistente.

## 4. Camada de acessibilidade e idioma

- `/i18n-parity` para paridade e convenções pt-BR/en-US.
- `/a11y-audit` para descrição de equações em display, `alt` de imagens e contraste.

## 5. Relatório

Uma tabela por nó auditado:

| Nó | Achado | Camada | Severidade | Correção sugerida |
|---|---|---|---|---|

Severidade: `bloqueante` (impede publicação — erro matemático, monolíngue, gabarito errado),
`importante` (prejudica aprendizado), `menor` (polimento). Encerre com o veredito por nó:
`pronto para publicar` | `ajustes necessários` | `retrabalho`.
