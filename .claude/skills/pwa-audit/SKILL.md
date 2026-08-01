---
name: pwa-audit
description: Audita a aplicação como PWA — instalabilidade, funcionamento offline, performance (Core Web Vitals), tamanho de bundle e comportamento em rede lenta. Usar antes de deploy e após mudanças que afetem carregamento ou cache.
---

# Auditar PWA e performance

Pressuposto do produto: a plataforma precisa funcionar **em qualquer dispositivo, sem
instalação, e offline para o conteúdo já visitado** (AGENTS.md §1).

## 1. Pré-condição

Verifique se há aplicação para auditar (build local ou deploy de preview). Se não houver,
pare e diga isso — não simule resultado.

## 2. Instalabilidade e offline

- [ ] `manifest.webmanifest` válido: `name`, `short_name`, `start_url`, `display`,
      `theme_color`, ícones (mínimo 192 e 512 px, incluindo `maskable`)
- [ ] Service worker registrado, com estratégia de cache **declarada e documentada**
- [ ] Conteúdo já visitado abre offline (teste com rede desativada)
- [ ] Estado do aluno (progresso, respostas) sobrevive a recarregamento e a queda de rede
- [ ] Há feedback claro quando algo exige conexão
- [ ] Atualização do service worker não deixa o app preso em versão antiga

## 3. Performance (Core Web Vitals)

Meta inicial em conexão 4G simulada e CPU 4× throttled:

| Métrica | Alvo |
|---|---|
| LCP | ≤ 2,5 s |
| INP | ≤ 200 ms |
| CLS | ≤ 0,1 |
| JS inicial | o menor possível; justificar cada dependência pesada |

Atenção específica: **renderização de KaTeX** (evitar layout shift e carregamento
bloqueante de fontes) e imagens/gráficos de conteúdo (dimensões declaradas).

## 4. Como executar

Com o MCP `chrome-devtools`: `performance_start_trace` → navegar → `performance_stop_trace`
→ `performance_analyze_insight`, e `lighthouse_audit` para o panorama. Sem o MCP: rodar
Lighthouse via CLI ou revisar estaticamente configuração de build, cache e bundle,
**declarando** o que não foi medido.

## 5. Saída

Tabela de achados com métrica medida × alvo, causa provável e correção sugerida, ordenada
por impacto no aluno em dispositivo modesto (o público-alvo inclui quem tem celular antigo e
internet ruim — otimizar para esse caso, não para desktop rápido).
