**Tipo:** erro
**ID:** L-015
**Contexto:** 2026-08-01, TCK-0012 (`tools/context-watch.py`). O medidor de contexto do
Claude Code precisa de dois números: quanto foi usado (lido do transcript, exato) e qual é a
janela (não exposta em lugar nenhum). O transcript grava `claude-opus-5` sem distinguir a
variante de 200k da de 1M. O padrão por modelo foi escrito com a janela **maior** (1M) e a
incerteza foi sinalizada só na saída de terminal (`janela_confiavel: false` + um aviso em
texto). O `code-reviewer` reprovou: numa sessão de 200k, o contexto cheio apareceria como
"~20% VERDE" e o hook — o único caminho automático, a razão de existir da ferramenta —
**nunca falaria**, porque a zona nunca subiria. O aviso existia apenas para quem rodasse o
comando à mão, isto é, para quem não precisava do gatilho.

**Lição:** monitor que precisa adivinhar um limite tem de adivinhar **pelo lado pessimista**,
e a incerteza tem de viajar pelo mesmo canal que o alarme. Duas regras separadas, ambas
violadas no mesmo defeito:

1. **Presunção conservadora.** Entre duas hipóteses plausíveis, escolher a que dispara antes.
   Falso alarme é ruído — visível, incômodo, corrigível com uma variável de ambiente. Falso
   silêncio é indistinguível de "está tudo bem" e só é descoberto quando o dano ocorreu.
2. **A ressalva pertence ao canal automático.** Sinalizar incerteza em `--json` ou no
   terminal não protege quem depende do hook, do CI ou do alerta. Se o mecanismo fala
   sozinho, é ali que a dúvida precisa aparecer — com limite de repetição (uma vez por
   sessão) para não virar ruído e ser desligado.

**Como aplicar:** ao escrever qualquer verificação com limiar (contexto, quota, disco,
orçamento de bundle, tempo de build), responder por escrito a duas perguntas antes de
entregar: (a) *se o meu palpite estiver errado, o alarme dispara cedo demais ou tarde
demais?* — só "cedo demais" é aceitável; (b) *quem recebe o alarme recebe também a dúvida?*
Se a resposta de (b) for "só quem rodar o comando manualmente", a ressalva está no lugar
errado. Teste obrigatório: um caso que force a presunção e verifique que **o canal
automático** (hook/CI), não só o stdout, comunica a incerteza.
