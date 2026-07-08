# Grafo rastreado — Wakeup → Run → Settle
> Interno. Insumo do gate `grill-doc`. Frescor: 2026-07-07 · commit pinado `d20f55f`.
> **Linhas ancoradas ao commit `d20f55f`** (não ao working tree). Durante o piloto o working tree
> foi editado ao vivo (`AdapterRunExecutor.java`), e as linhas driftaram — o `/verify` pegou; a
> resolução é o carimbo de frescor fazendo seu trabalho: cite o commit imutável.
> Caminhos relativos à raiz do repo `agente-orquestrator`, sob `backend/src/main/java/com/orquestrador/`.
> O fluxo é **assíncrono**, com **3 entrypoints** desacoplados pela fila `heartbeat_run`:
> **A) enqueue** (HTTP `POST /wakeups`) · **B) dispatch** (`@Scheduled` 1s) · **C) reaper** (`@Scheduled` 5s).

## A · Enqueue (HTTP)

| # | Caller (arquivo:linha) | Callee (arquivo:linha) | Papel do salto | Fronteira? | Estado |
|---|---|---|---|---|---|
| A1 | `execution/WakeupController.java:35` | `common/security/CompanyAccessGuard.assertMember` | 403 se não-membro da company | interna | fora-de-escopo (cross-cut de segurança) |
| A2 | `execution/WakeupController.java:38` | `execution/WakeupService.java:50` | delega o enqueue | interna | verificado |
| A3 | `execution/WakeupService.java:51` | `execution/WakeupService.java:56` | ato humano direto ⇒ linhagem raiz | interna | verificado |
| A4 | `execution/WakeupService.java:59` | `org/agent/AgentRepository.findByIdForUpdate` | **lock pessimista** na linha do Agent (serializa wakeups) | externa (DB) | verificado |
| A5 | `execution/WakeupService.java:68` | `execution/lineage/SpawnLineageGuard.java:47` | **guard anti-loop + cap prof. 5** → 409 antes de criar | interna | verificado |
| A6 | `execution/WakeupService.java:73` | `org/team/TeamService.assertDispatchAllowed` | **gate do arquiteto** → 409 antes de criar | interna | fora-de-escopo (interno do gate; fluxo ADR-0017) |
| A7 | `execution/WakeupService.java:75` | `execution/AgentWakeupRequestRepository.save` | persiste o wakeup | externa (DB) | verificado |
| A8 | `execution/WakeupService.java:80` | `governance/budget/BudgetService.java:76` | **cobra WAKEUP no ledger na abertura** (conta do causador) | interna | verificado |
| A9 | `governance/budget/BudgetService.java:78` | `governance/budget/CostEventRepository.save` | grava o cost_event de orquestração | externa (DB) | verificado |
| A10 | `governance/budget/BudgetService.java:80` | `governance/budget/BudgetService.java:106` | reavalia o teto de orquestração (company + agente) | interna | verificado |
| A11 | `governance/budget/BudgetService.java:116` | `governance/budget/BudgetService.java:122` | abre incidente 1×/escopo se cruzou o teto | interna | verificado |
| A12 | `governance/budget/BudgetService.java:127` | `governance/budget/BudgetService.java:136` | **drena até o checkpoint** (cancela QUEUED+wakeups; em-voo liquida) | externa (DB) | verificado |
| A13 | `execution/WakeupService.java:82` | `execution/HeartbeatRunRepository.findByAgentAndStatuses` | acha runs ativos → decisão de coalescing | externa (DB) | verificado |
| A14 | `execution/WakeupService.java:88` | `execution/TeamFanOutGate.java:38` | **cap de fan-out** (só no caminho que cria run) → 409 | interna | verificado |
| A15 | `execution/WakeupService.java:89` | `execution/HeartbeatRunRepository.save` | cria o Run `QUEUED` (branch: sem run ativo) | externa (DB) | verificado |
| A16 | `execution/WakeupService.java:92` | `execution/HeartbeatRunEventRepository.save` | evento `RUN_QUEUED` | externa (DB) | verificado |
| A17 | `execution/WakeupService.java:97-103` | (mesma tx) | branch **coalesce**: run ativo `QUEUED` → mescla, adota issue, `COALESCED` | interna | verificado |
| A18 | `execution/WakeupService.java:106-109` | (mesma tx) | branch **defer**: run `RUNNING`/`RECOVERING` → `needs_followup`, `DEFERRED` | interna | verificado |

## B · Dispatch (@Scheduled)

| # | Caller (arquivo:linha) | Callee (arquivo:linha) | Papel do salto | Fronteira? | Estado |
|---|---|---|---|---|---|
| B1 | `execution/HeartbeatScheduler.java:39` | `execution/HeartbeatDispatcher.java:47` | tick de 1s aciona o dispatcher | interna | verificado |
| B2 | `execution/HeartbeatDispatcher.java:49` | `execution/HeartbeatRunRepository.findTop50ByStatusOrderByCreatedAtAsc` | carrega até 50 runs `QUEUED` | externa (DB) | verificado |
| B3 | `execution/HeartbeatDispatcher.java:53` | `governance/budget/BudgetService.java:48` | preflight budget: incidente OPEN → cancel | interna | verificado |
| B4 | `execution/HeartbeatDispatcher.java:61` | `org/team/TeamService.dispatchBlocked` | preflight arquiteto (2ª face) → cancel | interna | fora-de-escopo (interno do gate; fluxo ADR-0017) |
| B5 | `execution/HeartbeatDispatcher.java:68` | `execution/TeamFanOutGate.java:53` | preflight fan-out (2ª face, conta em-voo) → cancel | interna | verificado |
| B6 | `execution/HeartbeatDispatcher.java:75` | `execution/lineage/SpawnLineageGuard.java:63` | preflight linhagem (2ª face) → cancel run nascido ilegal | interna | verificado |
| B7 | `execution/HeartbeatDispatcher.java:54,62,69,77` | `execution/HeartbeatRunStore.java:123` | cancela o run `QUEUED` (qualquer preflight) → `RUN_CANCELLED` | externa (DB) | verificado |
| B8 | `execution/HeartbeatDispatcher.java:81` | `execution/HeartbeatRunStore.java:39` | **claim CAS** `QUEUED→RUNNING` + lease 2min + owner | interna | verificado |
| B9 | `execution/HeartbeatRunStore.java:41` | `execution/HeartbeatRunRepository.java:72` | CAS: `attempt++`, lease, owner where status=QUEUED | externa (DB) | verificado |
| B10 | `execution/HeartbeatRunStore.java:48` | `governance/budget/BudgetService.java:76` | **cobra RUN_OPEN só se attempt==1** (reaper não recobra) | interna | verificado |
| B11 | `execution/HeartbeatDispatcher.java:87` | `execution/HeartbeatRunStore.java:58` | monta `RunContext` (run sumiu → IllegalStateException → failure) | externa (DB) | verificado |
| B12 | `execution/HeartbeatDispatcher.java:89` | `execution/AdapterRunExecutor.java:83` | executa o Run (try/catch → `RunOutcome.failure`) | interna | verificado |
| B13 | `execution/AdapterRunExecutor.java:84` | `execution/AdapterRunExecutor.java:103` | corpo do run → `RunOutcome` | interna | verificado |
| B14 | `execution/AdapterRunExecutor.java:104` | `org/agent/AgentRepository.findById` | agente sumiu → failure | externa (DB) | verificado |
| B15 | `execution/AdapterRunExecutor.java:113` | `execution/runtime/WorkspaceResolver.resolve` | resolve o workDir (git worktree) | externa (FS) | fora-de-escopo (interno do resolver; F.9) |
| B16 | `execution/AdapterRunExecutor.java:115` | `skills/SkillMaterializer.materialize` | materializa SkillSet; I/O falha (antes do checkout) → failure | externa (FS) | fora-de-escopo (interno; fluxo de skills) |
| B17 | `execution/AdapterRunExecutor.java:123` | `work/issue/IssueService.java:64` | **checkout atômico com runId** = adquire o lock da Issue | interna | verificado |
| B18 | `work/issue/IssueService.java:66` | `work/issue/IssueRepository.java:61` | `tryCheckout`: lock se livre-ou-mesmo-run; !acquired → failure | externa (DB) | verificado |
| B19 | `execution/AdapterRunExecutor.java:129` | `preview/server/PreviewServerSupervisor.teardownOnCheckout` | mata preview vivo do estado anterior (best-effort) | interna | fora-de-escopo (fluxo de preview F.10) |
| B20 | `execution/AdapterRunExecutor.java:139` | `conversation/ConversationTurnCoordinator.claimFor` | run **sem Issue** = turno de conversa (variante paralela) | interna | fora-de-escopo (fluxo de conversa T.3) |
| B21 | `execution/AdapterRunExecutor.java:172` | `execution/runtime/ExecutionTarget.writeWorkspaceFiles` | **escreve a árvore no volume Docker**; falha → failure | externa (Docker vol) | verificado |
| B22 | `execution/AdapterRunExecutor.java:195` | `execution/adapter/AgentAdapter.execute` | **chama o CLI do agente no container** (Claude/Codex/process) | externa (processo/container) | verificado |
| B23 | `execution/AdapterRunExecutor.java:208` | `governance/budget/BudgetService.java:58` | roteia tokens reais → ledger (`costCents=0` na assinatura) | interna | verificado |
| B24 | `execution/AdapterRunExecutor.java:88-92` | `preview/PreviewArtifactCapturer.captureIfPublished` + `PreviewServerManifestRegistrar.registerIfDeclared` | captura preview após sucesso, antes do settle (best-effort) | interna | fora-de-escopo (fluxo de preview F.9/F.10) |
| B25 | `execution/AdapterRunExecutor.java:98` | `work/issue/IssueService.java:99` | **settleAfterRun**: liquida a Issue na saída terminal | interna | verificado |
| B26 | `work/issue/IssueService.java:102` | `work/issue/IssueService.java:126` | sucesso + `risk≥limiar` → **PENDING_REVIEW** (gate de risco) | interna | verificado |
| B27 | `work/issue/IssueService.java:127` | `work/issue/IssueRepository.java:101` | `trySubmitForReview`: PENDING_REVIEW sob lock guard | externa (DB) | verificado |
| B28 | `work/issue/IssueService.java:134` | `execution/HeartbeatRunRepository.existsByIdAndCompanyId` | review exige run real da company → senão 409 + rollback | externa (DB) | verificado |
| B29 | `work/issue/IssueService.java:105` | `work/issue/IssueRepository.java:80` | `tryComplete`: **DONE** sob lock guard; 0 linhas → NOT_SETTLED | externa (DB) | verificado |
| B30 | `work/issue/IssueService.java:108` | `work/issue/IssueRepository.java:122` | falha → `tryBlock`: **BLOCKED** sob lock guard | externa (DB) | verificado |
| B31 | `work/issue/IssueService.java:115` | `activitylog/ActivityLogService.record` | evento `ISSUE_BLOCKED` (só IDs, sem msg de erro) | externa (DB) | verificado |
| B32 | `execution/HeartbeatDispatcher.java:95` | `execution/HeartbeatRunStore.java:64` | sucesso → `finishSuccess` | interna | verificado |
| B33 | `execution/HeartbeatDispatcher.java:97` | `execution/HeartbeatRunStore.java:72` | falha → `finishFailure` | interna | verificado |
| B34 | `execution/HeartbeatRunStore.java:65,73` | `execution/HeartbeatRunRepository.java:82` | `finalizeRun` **guardado por leaseOwner** (só o detentor finaliza) | externa (DB) | verificado |
| B35 | `execution/HeartbeatRunStore.java:67,75` | `execution/HeartbeatRunStore.java:91` | **promote-on-finalize**: cria run seguinte herdando a linhagem MAIS FUNDA | externa (DB) | verificado |

## C · Reaper (@Scheduled, timeout)

| # | Caller (arquivo:linha) | Callee (arquivo:linha) | Papel do salto | Fronteira? | Estado |
|---|---|---|---|---|---|
| C1 | `execution/HeartbeatScheduler.java:44` | `execution/LeaseReaper.java:18` | tick de 5s aciona o reaper | interna | verificado |
| C2 | `execution/LeaseReaper.java:19` | `execution/HeartbeatRunStore.java:81` | `reapExpired` | interna | verificado |
| C3 | `execution/HeartbeatRunStore.java:82` | `execution/HeartbeatRunRepository.java:92` | `requeueExpired`: `RUNNING` + lease vencido → `QUEUED` (idempotente) | externa (DB) | verificado |

> **Fora-de-escopo (decisões registradas):** A6/B4 (gate do arquiteto, ADR-0017), B15/B16 (resolver/materializer de workspace e skills), B19/B24 (fluxo de preview F.9/F.10), B20 (turno de conversa T.3), A1 (guard de segurança). Cada um é **fluxo próprio** — a aresta que os aciona está coberta; o corpo interno não foi aberto (lazy).
