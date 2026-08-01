**Tipo:** erro
**ID:** L-018
**Contexto:** 2026-08-01, TCK-0012. Duas devoluções seguidas pelo mesmo motivo estrutural.
Loop 1: o `REJECT` apontou "janela presumida otimista → falso verde"; a correção trocou a
presunção para conservadora e criou o aviso no hook — a **causa citada** foi eliminada.
Loop 2: o mecanismo continuava sem avisar na hora certa, agora por saturação do alarme no
topo da escala. O mesmo aconteceu com o exit code do hook: o loop 1 corrigiu `| head` e
`> /dev/full` (os casos citados) e o loop 2 achou `>&-`, em que `sys.stdout` é `None` e não
um arquivo quebrado. Nos dois casos a correção foi verificada pelos testes do defeito
citado, e não pela pergunta que interessa: *o mecanismo agora cumpre o que promete?*
Relacionada a [L-013](fixing-the-cited-line-is-not-fixing-the-defect-class.md) (varrer o
artefato inteiro, não só a linha citada); esta vai um passo adiante: varrer o artefato não
basta se ninguém simulou o desfecho.

**Lição:** corrigir a causa apontada não é corrigir o **modo de falha**. O `REJECT` cita uma
evidência, não o inventário do problema, e o defeito costuma sobreviver mudando de forma
(otimista → pessimista saturado; pipe quebrado → fd fechado). A verificação tem de ser feita
sobre o **resultado prometido**, com o cenário completo encenado do começo ao fim, e não
sobre o trecho de código que mudou.

**Como aplicar:** antes de devolver um `REJECT` como resolvido, escrever a promessa da
funcionalidade em uma frase verificável ("o hook avisa quando o uso real cruza 60/75/85% e
volta a avisar em cada faixa") e encenar essa frase inteira — estado zerado, sequência
realista de medidas, mais de um disparo — em vez de rodar apenas o caso citado. Se o teste
novo é a negação literal da linha do `REJECT` ("não pode sair verde"), ele provavelmente
fixa a decisão contestada em vez de proteger o resultado: revisar essa asserção junto com a
correção. Para a classe de falhas de E/S, cobrir a matriz inteira de uma vez (pipe fechado,
dispositivo cheio, fd fechado, stdin lixo, stdin fechado) — sai mais barato que descobri-la
um `REJECT` por vez.
