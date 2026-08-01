---
name: log-error
description: Registra um erro não-trivial em docs/errors/ para não repeti-lo — comando que falhou por causa evitável, afirmação matemática errada publicada, suposição equivocada sobre a taxonomia ou retrabalho por instrução mal interpretada.
---

# Registrar erro

1. Leia `docs/errors/README.md` — se o erro já está registrado, **atualize** o arquivo
   existente em vez de criar outro.
2. Crie `docs/errors/<short-error-name>.md` (en-US kebab-case, conteúdo pt-BR) a partir de
   `docs/errors/error-template.md`:
   - **Data** (absoluta, ex.: 2026-08-01)
   - **Contexto**: o que estava sendo feito
   - **O que aconteceu**: sintoma observado
   - **Causa raiz**: por que aconteceu de verdade (não o sintoma)
   - **Correção aplicada**
   - **Como evitar**: regra prática, verificável
   - **Alcance**: o mesmo erro pode existir em outros lugares? Quais foram verificados?
3. **Erro matemático em conteúdo publicado** tem tratamento extra:
   - corrigir o nó afetado;
   - verificar nós irmãos e dependentes (o mesmo equívoco costuma se propagar);
   - listar no registro exatamente quais foram verificados.
4. Atualize o índice `docs/errors/README.md`.
5. Se o erro gerou aprendizado generalizável, registre também a lição (`/capture-lesson`).
