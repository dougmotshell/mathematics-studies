---
name: spec-review
description: Revisa criticamente uma spec (docs/specs/<slug>/) antes da aprovação — completude, critérios de aceite verificáveis, requisitos do projeto contemplados, riscos e escopo. Usar antes de liberar qualquer implementação.
---

# Revisar spec

Leia `docs/specs/<slug>/spec.md`, `plan.md` e `tasks.md` e avalie, com viés cético:

## 1. Problema e valor
- O problema está descrito em termos de quem sofre com ele, não da solução?
- O resultado esperado é observável por alguém de fora?

## 2. Critérios de aceite
- Cada critério é **verificável** (teste, medição, checklist) — nada de "melhor", "mais
  intuitivo", "robusto"?
- Existe pelo menos um critério que falharia se a implementação estivesse errada?

## 3. Requisitos obrigatórios do projeto
Marque explicitamente contemplado / não aplicável / **ausente**:
- [ ] Bilinguismo pt-BR + en-US
- [ ] Acessibilidade WCAG 2.2 AA (incluindo matemática acessível)
- [ ] Funcionamento offline / PWA, quando afeta a experiência do aluno
- [ ] Gratuidade e custo operacional
- [ ] Privacidade e dados de menores (LGPD/COPPA), quando há coleta
- [ ] Estabilidade de URLs de `content/`
- [ ] Correção matemática e verificação de gabaritos, quando há conteúdo

## 4. Plano e tasks
- O plano decorre da spec ou introduz escopo novo?
- Decisões estruturais estão em ADR aceito, ou o plano está decidindo por conta própria?
- As tasks são executáveis por um agente sem contexto adicional? Têm critério de pronto?
- O que pode ser cortado sem perder o valor central (menor fatia entregável)?

## 5. Riscos
- O que pode dar errado e como se detecta cedo?
- Alguma parte é irreversível (URL pública, formato de dados, coleta de dados)?

## Saída
Lista de achados com **severidade** (`bloqueante | importante | menor`), local e correção
sugerida, seguida de veredito: `aprovada`, `aprovada com ajustes` ou `precisa retrabalho`.
