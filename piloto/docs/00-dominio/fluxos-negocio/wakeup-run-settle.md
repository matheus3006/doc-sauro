---
sidebar_position: 1
title: "Negócio: Acordar um agente e concluir o trabalho"
description: "Como o operador aciona um agente para trabalhar — uma vez só, dentro do orçamento, com um desfecho seguro."
---

# Acordar um agente e concluir o trabalho — para o negócio

> Companheiro de negócio do fluxo técnico: [wakeup-run-settle](../../03-fluxos/wakeup-run-settle.md). Escrito pra quem toca o produto — sem código.

## Em uma frase

Acionar um agente pra fazer uma tarefa — garantindo que ela roda **uma vez só**, dentro do **orçamento**, e termina com um **desfecho seguro**: feito, esperando revisão, ou bloqueado.

## Quem usa

- **O operador** aciona — pede pra acordar um agente e tocar uma tarefa.
- **O agente** (o "funcionário de IA") executa a tarefa.

## Como funciona

Você, operador, pede pra **acordar um agente**. O sistema **não faz o trabalho na hora**: ele anota o pedido numa fila e te responde na mesma hora que **recebeu** — nada fica travado te esperando.

Um instante depois, um processo de fundo pega o pedido da fila e conduz a execução em três tempos:

1. **Confere as regras** — se há orçamento, permissão e se os limites de segurança estão ok.
2. **Reserva a tarefa** pra este agente, pra ninguém executar a mesma coisa em paralelo.
3. **Põe o agente pra trabalhar** de verdade.

Quando o agente termina, o sistema **liquida** a tarefa — dá o desfecho:

- deu certo e é **baixo risco** → **feito**;
- deu certo mas é **arriscado** → **esperando revisão** de um humano;
- **falhou** → **bloqueado**, pra alguém decidir o que fazer.

> **Exemplo:** Maria, operadora, acorda o agente *Redator* pra escrever um comunicado. Na hora, ela vê **"recebido, em processamento"** e segue a vida. Um segundo depois, o sistema confere que há orçamento, reserva a tarefa pro Redator e o põe pra trabalhar. O texto sai; como escrever um comunicado é baixo risco, a tarefa vira **feito**. Se fosse algo sensível, em vez de "feito" ela ficaria **esperando revisão** até Maria aprovar.

## Quando dá errado

- **Acordar o mesmo agente várias vezes ao mesmo tempo** não cria trabalho duplicado: o sistema junta os pedidos num só, ou agenda pra depois. Você nunca paga duas vezes pela mesma coisa.
- **Se o orçamento estoura**, o sistema para de criar coisa nova e cancela o que **ainda não começou** — mas **deixa terminar** o que já estava rodando (matar no meio só jogaria fora trabalho já pago). E avisa quem cuida do orçamento.
- **Se o motor que roda o agente falha** (por exemplo, a credencial de acesso expira), a tarefa fica **bloqueada** esperando decisão — não some no silêncio, e nenhuma outra tarefa é afetada.
- **Se alguém tenta acordar um agente que criaria um loop** (acordar quem está acima dele na cadeia) **ou uma cadeia longa demais**, o sistema **recusa na hora**, antes de criar qualquer coisa.

## Regras & porquês

- **Um trabalho de cada vez, por agente.** *Por quê:* pra não duplicar custo nem esforço. — `[inferido do código · a confirmar]` — base: o sistema serializa os pedidos do mesmo agente e junta os repetidos.
- **Trabalho arriscado espera revisão humana.** *Por quê:* o dono decide antes que algo arriscado vire "feito" — *"deny-by-default é a coisa pra bater o Paperclip"*. — atribuído: operador via CONTEXT.md, 2026-07-07.
- **Não se pode acordar um agente acima na cadeia, e a cadeia tem no máximo 5 níveis.** *Por quê:* evitar que agentes se acordem em círculo sem fim. — atribuído: operador via CONTEXT.md, 2026-07-07.
- **O custo é lançado quando o trabalho começa, uma vez só.** *Por quê:* previsibilidade de orçamento — uma re-tentativa não recobra. — `[inferido do código · a confirmar]` — base: a cobrança de abertura acontece só na primeira tentativa.
- **Orçamento estourado drena até o checkpoint, não mata no meio.** *Por quê:* matar um trabalho em andamento jogaria fora dinheiro já gasto. — `[inferido do código · a confirmar]` — base: cancela só o que não começou; o que está em andamento termina e liquida.

## Trace

<details>
<summary>Trace — cada afirmação e sua base (a PO não precisa; o cético clica)</summary>

Base = seção do [doc técnico](../../03-fluxos/wakeup-run-settle.md) e/ou aresta do grafo rastreado.

| Afirmação (seção) | Tipo | Base | Estado |
|---|---|---|---|
| Anota o pedido e responde "recebido" na hora (*Como funciona*) | o quê | §Gatilho / §Happy path A · grafo A2 | herdado-verificado |
| Um processo de fundo pega da fila depois (*Como funciona*) | o quê | §Happy path B · grafo B1–B2 | herdado-verificado |
| Confere regras: orçamento, permissão, limites (*Como funciona*) | o quê | §Happy path B (preflights) · grafo B3–B6 | herdado-verificado |
| Reserva a tarefa pro agente, execução única (*Como funciona*) | o quê | §Happy path B (checkout) · grafo B17–B18 | herdado-verificado |
| Põe o agente pra trabalhar (*Como funciona*) | o quê | §Chamadas externas · grafo B22 | herdado-verificado |
| Desfecho feito / esperando revisão / bloqueado (*Como funciona*) | o quê | §Happy path·C·Settle · grafo B26 / B29 / B30 | herdado-verificado |
| Não duplica; junta ou agenda (*Quando dá errado*) | o quê | §Transições·idempotência·compensação (coalescing) · grafo A17 / A18 | herdado-verificado |
| Orçamento estoura → para novo, cancela não-iniciado, deixa o em-voo terminar (*Quando dá errado*) | o quê | §Transições·idempotência·compensação · grafo A12 | herdado-verificado |
| Motor falha → bloqueado, nenhuma outra tarefa afetada (*Quando dá errado*) | o quê | §Error paths / §Happy path·C·Settle (guard de posse) · grafo B22 | herdado-verificado |
| Recusa loop / cadeia longa demais, antes de criar (*Quando dá errado*) | o quê | §Error paths · grafo A5 | herdado-verificado |
| "Um por agente" — porquê: não duplicar (*Regras & porquês*) | porquê | inferência de §Transições·idempotência·compensação (serialização + coalescing) | inferido-a-confirmar |
| "Arriscado espera revisão" — porquê: deny-by-default (*Regras & porquês*) | porquê | `contexto.md` §Restrições | atribuído (operador) |
| "Anti-loop, no máx. 5" — porquê: evitar círculo (*Regras & porquês*) | porquê | `contexto.md` §Restrições | atribuído (operador) |
| "Cobra uma vez" — porquê: previsibilidade (*Regras & porquês*) | porquê | inferência de §Transições·idempotência·compensação (cobrança na 1ª tentativa) | inferido-a-confirmar |
| "Drena, não mata" — porquê: não perder trabalho pago (*Regras & porquês*) | porquê | inferência da nota de §Transições·idempotência·compensação | inferido-a-confirmar |

</details>
