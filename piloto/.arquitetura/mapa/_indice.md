# Mapa — índice (L0-L1)
> Interno. Ledger da trilha. NUNCA citado numa doc. Frescor: 2026-07-07 · `d20f55f`
> Raiz: `backend/src/main/java/com/orquestrador`

## Árvore (L0-L1)
- agente-orquestrator
  - `execution/`
    - `adapter/` · `lineage/` · `runtime/`
  - `work/`
    - `issue/` · `review/`
  - `governance/`
    - `approval/` · `budget/`
  - `board/` · `org/` · `memory/` · `skills/` · `conversation/` · `preview/` · `identity/` · `handoff/` · `activitylog/` · `config/` · `common/`

## Cobertura
| Módulo | Entrypoints (inferidos) | Status | Fluxos que cobriram | Frescor |
|---|---|---|---|---|
| `execution` | HTTP `[inferido]` (`WakeupController`) + agendado `[inferido]` (`HeartbeatScheduler`) | **parcial** | wakeup-run-settle | `d20f55f` |
| `work` | HTTP `[inferido]` (`IssueController`, `ReviewController`) | **parcial** | wakeup-run-settle (settle) | `d20f55f` |
| `governance` | HTTP `[inferido]` (`ApprovalController`, `BudgetController`) | **parcial** | wakeup-run-settle (budget) | `d20f55f` |
| `board` | HTTP `[inferido]` (`MissionControlController`, `RunStepsController`) | esqueleto | — | `d20f55f` |
| `org` | HTTP `[inferido]` (`AgentController`, `TeamController`) | esqueleto | — | `d20f55f` |
| `memory` | HTTP `[inferido]` (`DecisionController`) | esqueleto | — | `d20f55f` |
| `skills` | HTTP `[inferido]` (`SkillController`, `KnowAllController`) | esqueleto | — | `d20f55f` |
| `conversation` | HTTP `[inferido]` (`ConversationController`) | esqueleto | — | `d20f55f` |
| `preview` | HTTP `[inferido]` (`PreviewArtifactController`) | esqueleto | — | `d20f55f` |
| `identity` | HTTP `[inferido]` (`CompanyController`) | esqueleto | — | `d20f55f` |
| `handoff` | — `[inferido]` | esqueleto | — | `d20f55f` |
| `activitylog` | — `[inferido]` (registro de ação mutante) | esqueleto | — | `d20f55f` |
| `config` | — `[inferido]` (segurança, clock) | esqueleto | — | `d20f55f` |
| `common` | — `[inferido]` (util) | esqueleto | — | `d20f55f` |

> `parcial` = um fluxo já promoveu unidades nesse módulo para `verificado` (ver stub do módulo). `esqueleto` = ainda no L0-L1, enche lazy no primeiro toque.
