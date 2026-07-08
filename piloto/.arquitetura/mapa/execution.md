# Mapa — módulo `execution`
> Nível-declaração. Assinaturas e arestas enchem lazy por-fluxo. Frescor: 2026-07-07 · `d20f55f`
> Raiz: `backend/src/main/java/com/orquestrador/execution`

## Unidades (L2)
- `WakeupController` — papel: entrypoint HTTP `[inferido]` — status: esqueleto
- `WakeupService` — papel: lógica de enfileirar wakeup `[inferido]` — status: esqueleto
- `WakeupOutcome` · `WakeupStatus` — papel: resultado/estado do wakeup `[inferido]` — status: esqueleto
- `AgentWakeupRequest` (+ `Repository`) — papel: entidade da fila de wakeup `[inferido]` — status: esqueleto
- `HeartbeatScheduler` — papel: gatilho agendado `@Scheduled` `[inferido]` — status: esqueleto
- `HeartbeatDispatcher` — papel: checkout + abertura de Run `[inferido]` — status: esqueleto
- `HeartbeatRun` (+ `Repository`/`Store`/`Event`) — papel: entidade do Run `[inferido]` — status: esqueleto
- `RunExecutor` / `AdapterRunExecutor` — papel: executa o Run `[inferido]` — status: esqueleto
- `RunContext` · `RunOutcome` · `RunFinalOutput` · `RunStatus` — papel: contexto/resultado do Run `[inferido]` — status: esqueleto
- `LeaseReaper` — papel: recupera lease preso (timeout) `[inferido]` — status: esqueleto
- `TeamFanOutGate` — papel: cap de runs concorrentes por time `[inferido]` — status: esqueleto
- `lineage/SpawnLineageGuard` · `SpawnLineage` — papel: guard anti-loop + cap de profundidade `[inferido]` — status: esqueleto
- `adapter/AgentAdapter` (+ `ClaudeCodeAdapter`/`CodexAdapter`/`ProcessAgentAdapter`/`AdapterRegistry`) — papel: integração com CLI de agente (fronteira externa) `[inferido]` — status: esqueleto
- `adapter/EngineContainer` · `ClaudeStreamParser` · `CodexStreamParser` — papel: material de container + parse de stream `[inferido]` — status: esqueleto
- `runtime/ExecutionTarget` (+ `Docker`/`Local`) · `WorkspaceResolver` · `DatabaseClock` — papel: onde/como o Run roda `[inferido]` — status: esqueleto

> assinaturas (L3) e arestas (L4) enchem **lazy** quando um fluxo passar por aqui.

## Promovidos pelo fluxo `wakeup-run-settle` (esqueleto → **verificado**)
Corpo aberto e citado no grafo `.arquitetura/mapa/fluxos/wakeup-run-settle.grafo.md`:
- `WakeupController.wake` → **verificado** (`WakeupController.java:33`)
- `WakeupService.enqueue` → **verificado** (`WakeupService.java:50,56`)
- `SpawnLineageGuard.assertWakeupAllowed` / `checkoutBlockReason` → **verificado** (`SpawnLineageGuard.java:47,63`)
- `TeamFanOutGate.assertFanOutAllowed` / `fanOutBlocked` → **verificado** (`TeamFanOutGate.java:38,53`)
- `HeartbeatScheduler.dispatch` / `reap` → **verificado** (`HeartbeatScheduler.java:39,44`)
- `HeartbeatDispatcher.dispatchOnce` → **verificado** (`HeartbeatDispatcher.java:47`)
- `HeartbeatRunStore.claim` / `finishSuccess` / `finishFailure` / `promoteIfNeeded` / `reapExpired` / `cancel` → **verificado** (`HeartbeatRunStore.java:39,64,72,91,81,123`)
- `AdapterRunExecutor.execute` / `runToOutcome` → **verificado** (`AdapterRunExecutor.java:83,103`)
- `LeaseReaper.reapOnce` → **verificado** (`LeaseReaper.java:18`)
- `AgentAdapter.execute` → **verificado como fronteira externa** (`AdapterRunExecutor.java:195`)

Fora deste fluxo: `adapter/*` internos (parsers/EngineContainer), `runtime/*` (Docker/Local target) — seguem `esqueleto`, enchem no fluxo que os cruzar.
