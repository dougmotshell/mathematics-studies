# Trilhas de aprendizado

Percursos curados que atravessam a taxonomia, definidos por **objetivo do aluno** e não por
estágio. Um descritor JSON por trilha (`<slug>.json`), criado com `/learning-path`.

## Formato

```json
{
  "id": "zero-to-calculus",
  "title": { "pt-BR": "Do zero ao cálculo", "en-US": "From zero to calculus" },
  "goal":  { "pt-BR": "…", "en-US": "…" },
  "audience": { "stage": "high-school", "assumedKnowledge": ["…"] },
  "modules": [
    {
      "title": { "pt-BR": "…", "en-US": "…" },
      "nodes": ["middle-school/algebra/linear-equations"],
      "milestone": { "pt-BR": "…", "en-US": "…" }
    }
  ],
  "diagnostics": ["…"],
  "completionCriteria": { "pt-BR": "…", "en-US": "…" },
  "estimatedHours": 40
}
```

## Regras

- Todo `nodes[]` referencia um nó existente (validado por `scripts/audit-content.sh`).
- Trilha **não duplica conteúdo**: ela sequencia nós, nunca copia.
- Deve prever **caminhos de recuperação**: para onde o aluno volta quando erra
  sistematicamente uma habilidade.
- Bilíngue em todos os campos de texto.
