# Contexto — agente-orquestrator
> Interno. Insumo de toda a trilha. Extração carrega evidência; elicitação é atribuída.
> Frescor: 2026-07-07 · commit `d20f55f`
> Raiz analisada: `/Users/matheussouza/Pessoal/orquestrador-agentes/agente-orquestrator`
> (No piloto, os `arquivo:linha` são relativos à raiz do repo agente-orquestrator.)

## Stack
- Java 21 — evidência: `backend/pom.xml:21`
- Spring Boot (web, data-jpa, security, validation, actuator) — evidência: `backend/pom.xml:28-44`
- PostgreSQL 16 — evidência: `docker-compose.yml:4` (`image: postgres:16`), `backend/pom.xml:48`
- Flyway (migrations versionadas `V*`) — evidência: `backend/pom.xml:53-58`
- Docker Compose (db + backend) — evidência: `docker-compose.yml:3-20`
- Frontend Next.js 16 / React 19 / TypeScript — evidência: `frontend/package.json:22-23,35`
- H2 (só em teste) — evidência: `backend/pom.xml:72`

## Estrutura
- Raiz do código backend: `backend/src/main/java/com/orquestrador`
- Entrypoint da aplicação: `OrquestradorApplication.java` (`@SpringBootApplication`)
- Módulos top-level (pacotes):
  - `execution` — entrypoints: HTTP (`WakeupController`) + agendado (`HeartbeatScheduler` `@Scheduled`) — **[inferido]** casa do fluxo Wakeup→Run→Settle — evidência: `execution/`
  - `work` — entrypoints: HTTP (`IssueController`, `ReviewController`) — **[inferido]** unidade de trabalho (Issue) e o settle — evidência: `work/`
  - `governance` — entrypoints: HTTP (`ApprovalController`, `BudgetController`) — **[inferido]** approval pré-hoc + orçamento — evidência: `governance/`
  - `board` — entrypoints: HTTP (`MissionControlController`, `RunStepsController`, `ActivityController`) — **[inferido]** observação board-only — evidência: `board/`
  - `org` — entrypoints: HTTP (`AgentController`, `TeamController`, `RoleTemplateController`, `EngineCatalogController`) — **[inferido]** organização (Agent/Team/molde/motor) — evidência: `org/`
  - `memory` — entrypoints: HTTP (`DecisionController`, `CompanyMemoryController`, `IssueLedgerController`) — **[inferido]** segundo cérebro / carta de interesses — evidência: `memory/`
  - `skills` — entrypoints: HTTP (`SkillController`, `KnowAllController`, `AgentSkillController`, `IssueSkillController`) — **[inferido]** catálogo/instalação de Skills — evidência: `skills/`
  - `conversation` — entrypoints: HTTP (`ConversationController`) — **[inferido]** turno de conversa (1 turno = 1 Run) — evidência: `conversation/`
  - `preview` — entrypoints: HTTP (`PreviewArtifactController`, `PreviewServerController`) — **[inferido]** preview de protótipo — evidência: `preview/`
  - `identity` — entrypoints: HTTP (`CompanyController`) — **[inferido]** tenant/Company — evidência: `identity/`
  - `handoff` — **[inferido]** destilação de contexto a 50-60% — evidência: `handoff/`
  - `activitylog` — **[inferido]** registro durável de ação mutante — evidência: `activitylog/`
  - `config` · `common` — **[inferido]** transversais (segurança, clock, util) — evidência: `config/`, `common/`

## Elicitação (atribuído)
> Fonte: `CONTEXT.md` na raiz do repo — glossário canônico mantido pelo operador em sessões de grilling/domain-modeling. Atribuído ao **operador (via CONTEXT.md)**, 2026-07-07.

- **Tier:** "a empresa/tenant; fronteira de isolamento. O dono opera várias (uma por produto)" — plataforma interna de orquestração de agentes de IA; **crítica** (é o motor que executa e governa o trabalho dos agentes) — operador (via CONTEXT.md), 2026-07-07.
- **Propósito:** "Agent — um funcionário de IA dentro de uma Company; o CEO é o agente orquestrador mestre, delegador PURO (não produz conteúdo — grelha, descobre, contrata, atribui, delega)" — orquestrar agentes de IA como funcionários, mediando execução por aprovação humana — operador (via CONTEXT.md), 2026-07-07.
- **Blast radius:** "Budget — limite de custo/token por escopo; estouro → hard-stop + auto-pause"; a execução roda motores externos (CLIs Claude Code/Codex) em container Docker com credencial de plano montada. Se o motor/credencial cai, o Run falha; se o orçamento estoura, drena até o checkpoint — operador (via CONTEXT.md), 2026-07-07.
- **Restrições:** "deny-by-default é 'a coisa pra bater o Paperclip'"; cadeia de comando estrita (sem comunicação lateral no v1); arquiteto obrigatório por time; `spawn_lineage` proíbe acordar ancestral (anti-loop) + cap de profundidade 5; ledger de orquestração cobra na abertura — operador (via CONTEXT.md), 2026-07-07.
- **Padrões que não se aplicam:**
  - "o modelo escolhe o plano" → **NÃO**: o **adapter** (qual CLI roda) escolhe o plano de assinatura — operador (via CONTEXT.md), 2026-07-07.
  - "o agente sobe o servidor / registra o artefato" → **NÃO**: o agente **declara via contrato de lugar** (`.orq/`), o pipeline é dono do processo — operador (via CONTEXT.md), 2026-07-07.
  - "linhagem é autoria" → **NÃO**: linhagem é **causalidade** (quem causou o trabalho); o wakeup aprovado herda a linhagem do proponente — operador (via CONTEXT.md), 2026-07-07.
  - "auto-retry de Issue" → **NÃO** no v1: Issue FAILED vira BLOCKED e espera decisão humana (REOPEN/CANCEL) — operador (via CONTEXT.md), 2026-07-07.
