# Contexto de Produto — agente-orquestrator
> Interno. Lente de PO da trilha. Elicitação: atribuída OU [inferido do código · a confirmar].
> Frescor: 2026-07-07 · commit `d20f55f`
> Base técnica: `contexto.md` + `docs/03-fluxos/wakeup-run-settle.md` (já verificado, gates aprovados).

## Personas

- **Operador (dono da Company)** — a pessoa que opera a plataforma: dispara trabalho (acorda um agente), aprova o que é arriscado e define o orçamento. — atribuído: operador via CONTEXT.md, 2026-07-07 ("o dono opera várias [Companies], uma por produto").
- **Agente (funcionário de IA)** — o "funcionário" que executa uma tarefa dentro de uma Company. — atribuído: operador via CONTEXT.md, 2026-07-07 ("Agent — um funcionário de IA dentro de uma Company").
- **Agente orquestrador (CEO)** — o agente-mestre que só delega (não produz conteúdo: grelha, descobre, contrata, atribui). — atribuído: operador via CONTEXT.md, 2026-07-07.

## Jobs (JTBD)

- Quando preciso que um agente faça um trabalho, quero **acordá-lo e ter certeza de que roda uma vez só e termina com um desfecho seguro**, pra não pagar duas vezes nem perder trabalho. — [inferido do código · a confirmar] — base: o fluxo garante ≤1 execução ativa por agente e sempre liquida a tarefa (doc técnico, §Idempotência e §Settle).
- Quando um trabalho é **arriscado**, quero que ele **pare pra revisão humana** antes de virar "feito". — atribuído: operador via CONTEXT.md, 2026-07-07 ("deny-by-default é 'a coisa pra bater o Paperclip'").
- Quando o **orçamento** aperta, quero que o sistema **pare de gastar** sem jogar fora trabalho que já paguei. — atribuído: operador via CONTEXT.md, 2026-07-07 ("Budget… estouro → hard-stop + auto-pause").

## Glossário de produto

- **Company (empresa)** — a fronteira de isolamento; um dono opera várias, uma por produto. (técnico: `Company/tenant`) — atribuído: operador via CONTEXT.md.
- **Agente** — um funcionário de IA dentro de uma Company. (técnico: `Agent`) — atribuído: operador via CONTEXT.md.
- **Acordar** — disparar um trabalho pra um agente. (técnico: `wakeup`) — [inferido do código · a confirmar] — base: entrypoint `POST /wakeups` enfileira o pedido (doc técnico, §Gatilho).
- **Trabalho / execução** — uma tentativa de executar a tarefa de um agente. (técnico: `Run`) — [inferido do código · a confirmar] — base: o fluxo cria e executa um `Run` por tarefa (§Happy path).
- **Tarefa** — a unidade de trabalho a ser feita e concluída. (técnico: `Issue`) — [inferido do código · a confirmar] — base: o settle liquida a `Issue` (§Settle).
- **Orçamento** — limite de custo por escopo; se estoura, o sistema para de criar coisa nova. (técnico: `Budget`) — atribuído: operador via CONTEXT.md.
- **Linhagem** — quem causou o trabalho; não se pode acordar quem está acima na cadeia (anti-loop), no máximo 5 de profundidade. (técnico: `spawn_lineage`) — atribuído: operador via CONTEXT.md.
- **Liquidar** — dar o desfecho final da tarefa: feito, bloqueado, ou esperando revisão. (técnico: `settle`) — [inferido do código · a confirmar] — base: `settleAfterRun` na saída terminal (§Settle).
- **Esperando revisão** — estado de uma tarefa arriscada que aguarda um humano aprovar antes de virar "feito". (técnico: `PENDING_REVIEW`) — [inferido do código · a confirmar] — base: gate de risco no settle (§Settle).
