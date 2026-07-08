# Evidência da tese — piloto Wakeup → Run → Settle

> Tese (DESIGN §1): a doc rasa sai rasa por **profundidade** (não segue a execução) e **completude**
> (omite o 20% difícil). O slice ataca os dois: **mapa barato + leitura forçada (`documentar-fluxo`) +
> gates (`grill-doc`/`grill-mermaid`)**. Aqui está o que o rastreamento pegou e a passada rasa/template
> deixaria de fora — cada item com `arquivo:linha` (commit pinado `d20f55f`).

## O que a passada rasa/template deixaria de fora

Um gerador *template-driven* preencheria "gatilho / happy path / diagrama" e pararia. Cada achado
abaixo exigiu **abrir o corpo do método e seguir a chamada** — nenhum aparece na assinatura.

1. **O `POST /wakeups` não executa o agente — é assíncrono.** Ele *enfileira* e responde `202` (`WakeupController.java:32`,`38`); quem executa é um `@Scheduled` de 1s (`HeartbeatScheduler.java:38-40`) que claima o run depois. O template escreveria "POST → roda o agente" e erraria a natureza do fluxo. **(profundidade)**

2. **Cada guard tem DUAS faces — enqueue e checkout.** Budget, arquiteto, fan-out e linhagem são checados no enqueue (409, antes de criar: `WakeupService.java:68`,`73`,`88`; `SpawnLineageGuard.java:47`) **e de novo** no preflight do dispatcher (cancela o run: `HeartbeatDispatcher.java:53`,`61`,`68`,`75`; `SpawnLineageGuard.java:63`), porque runs entram "por fora" via promote-on-finalize (`HeartbeatRunStore.java:91`). Um template documentaria uma face e perderia a outra — a metade que existe justamente para o caminho difícil. **(completude)**

3. **O settle é guardado por lock e é idempotente — não é "sucesso→DONE, falha→BLOCKED".** `tryComplete`/`tryBlock`/`trySubmitForReview` só casam se `execution_lock_run_id = :runId` (`IssueRepository.java:78`,`98`,`119`); um run que falhou antes do checkout ou perdeu a corrida liquida **0 linhas → NOT_SETTLED**, e a Issue-vítima fica intacta (`IssueService.java:105-106`,`108-109`). O template descreveria a máquina de estados sem o guard que a torna segura sob concorrência. **(profundidade)**

4. **Compensação: drena-até-o-checkpoint, não "para tudo".** Budget estoura → abre incidente 1×/escopo e cancela **só o que não começou** (QUEUED + wakeups); o `RUNNING` termina o passo e liquida no settle (`BudgetService.java:136-143`,`14-21`). Matar RUNNING no banco nunca matou o processo — só jogaria fora trabalho pago. Template: "estourou → para". **(completude — compensação)**

5. **Gate de risco escondido no sucesso.** Sucesso **não** vira DONE se `risk_level ≥ limiar`: estaciona em `PENDING_REVIEW` (`IssueService.java:102-103` → `IssueRepository.java:101`). Uma transição inteira que o happy-path template pula. **(completude — transição)**

6. **Idempotência de billing.** `RUN_OPEN` é cobrado **só em `attempt == 1`** (`HeartbeatRunStore.java:47-48`); a re-execução do reaper (attempt++ no claim, `HeartbeatRunRepository.java:69`) é o mesmo ato e não recobra. Só se vê lendo o corpo do claim. **(profundidade)**

7. **Edge case achado no próprio código — guard `limitCents > 0`.** Sem ele, um teto ≤ 0 + uma emissão inócua (`costCents=0`) faria `spent(0) ≥ limit(0)` abrir incidente e cancelar o escopo (`BudgetService.java:94-98`). O comentário no código credita uma revisão adversarial; um template nunca chegaria nessa borda. **(completude — edge case)**

8. **Duas chamadas externas escondidas atrás de interface.** `adapter.execute` (`AdapterRunExecutor.java:195`) é o CLI real do agente (Claude/Codex) num container Docker com credencial de plano; `writeWorkspaceFiles` (`AdapterRunExecutor.java:172`) escreve num volume Docker que o backend **não enxerga**. Um scan de metadados vê "chama um método"; só o trace revela a fronteira externa (e o que acontece se ela falhar/expirar: `AdapterRunExecutor.java:180`,`200`). **(profundidade — dependência externa como risco)**

9. **Config fail-closed.** `risk-threshold` fora de 1-5 **derruba o boot** com mensagem clara em vez de desligar o gate em silêncio (`IssueService.java:36-40`). **(completude — modo de falha)**

Nove achados concretos; o critério pedia ≥3. Todos são "o 20% difícil": error paths, chamada externa, compensação, idempotência, transição, edge case.

## Resultado dos gates

| Gate | Veredito | Nota |
|---|---|---|
| **Completude estrutural** (`grill-doc`, bloqueante) | **PASSA** | 56 arestas: 43 cobertas + 13 fora-de-escopo, **0 AUSENTE**. B14 (agent-null no executor) entrou AUSENTE na 1ª passada e foi coberto antes do veredito — o gate funcionando. |
| **Disciplina de citação** (`grill-doc`, bloqueante) | **PASSA** | 0 frases de comportamento sem `arquivo:linha`; 0 fonte-errada (depoimento/mapa citados como fato). |
| **Rubrica de fluxo** (`grill-doc`, consultiva) | 8/8 presentes | gatilho, happy path, error paths, chamadas externas, transições, idempotência, timeout/retry, compensação. |
| **grill-mermaid** (sintaxe + MDX + fidelidade) | **LIMPO** | B21 (escrita no volume Docker) entrou ausente do diagrama e foi adicionada — Eixo 3 funcionando. |

## Verificação de execução (`/verify`)

Superfície observada de verdade, não "os testes passam":

1. ✅ **Integridade de citação** — 194 ocorrências de `arquivo:linha`, 12 arquivos, **0 quebradas** contra o commit pinado `d20f55f` (`git show`). Script: `scratchpad/verify_citations_pinned.py`.
2. ✅ **Conteúdo bate com a afirmação** — spot-check de 12 citações load-bearing: `MAX_DEPTH=5` (`SpawnLineageGuard.java:24`), lease 2min (`HeartbeatDispatcher.java:30`), `attempt+1` (`HeartbeatRunRepository.java:69`), lock guard (`IssueRepository.java:78`), `adapter.execute` (`AdapterRunExecutor.java:195`) — todas confirmadas.
3. ✅ **Mermaid renderiza** — `mmdc` gerou SVG de 67KB, `aria-roledescription="sequence"`, **37 messageText** (= as 37 mensagens do diagrama), **0 erro de sintaxe**. É o mesmo motor do `@docusaurus/theme-mermaid`.
4. ✅ **Frontmatter válido** + **MDX limpo** — `sidebar_position`/`title`/`description` presentes; 0 `{ }` ou `<tag>` crus na prosa (as chaves `{companyId}` estão em código inline).
5. 🔍 **Probe que virou achado real — drift do working tree.** Durante o piloto, o repo foi **editado ao vivo** (`AdapterRunExecutor.java`, mtime 21:44; `git status` = Modified; novo dir `handoff/`). As linhas driftaram **duas vezes** sob mim (execute saiu de 83→87→constructor). O spot-check de conteúdo do `/verify` **pegou** o drift; a resolução correta foi ancorar as citações ao **commit pinado `d20f55f`** (imutável) — exatamente o que o carimbo de frescor do DESIGN promete. **A tese ganhou uma prova de campo: sem o anchor pinado, a doc teria citações silenciosamente erradas.**

**Veredito /verify: PASS** — o slice roda ponta-a-ponta, produz 1 doc de fluxo que passa os gates, e as afirmações são reproduzíveis contra um commit imutável.

## Camada 0 — Visão de Produto: cobertura honesta (a fatia nova)

Depois do técnico e do negócio, a **Visão de Produto** (`documentar-visao` → `grill-visao`) fecha a Camada 0: o overview que uma PO nova lê pra entender o app **inteiro**. O que ela prova que a passada rasa erraria:

- **Não finge que 1 fluxo é o app.** O mapa da visão lista **1** fluxo documentado **e** as **9** áreas de produto que o `_indice.md` conhece e ainda **não têm doc** — fila de trabalho explícita, não silêncio. É a completude-estrutural (§7) aplicada ao overview: *coberto OU marcado*, sem *silent-cap*.
- **Liga sem reescrever.** O one-liner de cada fluxo é **byte-a-byte** o "Em uma frase" do doc de negócio já aprovado (diff automático: idêntico) — reescrever desancoraria do que o `grill-negocio` chancelou. Cadeia: Visão → negócio → técnico (`arquivo:linha`).
- **Síntese marcada, nunca fato.** "O que o app é no todo" entra `[inferido do código · a confirmar]` (nenhum fluxo isolado prova o todo); personas/jobs herdam a marcação do `contexto-produto`.

**Gate `grill-visao`: APROVADO** (3 bloqueantes PASSAM — âncora, zero-jargão, mapa-fiel). O gate pegou um **duplo-uso do módulo `governance`** (contado como área "coberta" via orçamento **e** listado como "sem doc" via aprovação prévia) e forçou o ajuste antes do veredito — mesmo padrão de B14/B21 no técnico e dos rótulos de seção no negócio: **o gate funcionando**. Verificação mecânica: link resolve, one-liner idêntico, `N=1` doc de negócio, cobertura confere com o `_indice.md`.

## Refinamentos que o piloto forçou nos prompts (DESIGN §10: "ajuste só se o piloto exigir")

1. **`mapear-estrutura`** — stubs por-módulo viraram **lazy (no primeiro toque)**, não eager-14-arquivos: eager contradiz "mapa barato + não mapeie o repo inteiro".
2. **`grill-mermaid` Eixo 1** — aspas em label são regra de **flowchart**; em `sequenceDiagram` a mensagem vai após `:` **sem** aspas (aspas renderizam literais). A regra genérica anterior estava errada.
3. **`grill-mermaid` Eixo 3** — o diagrama é **resumo fiel** (sem seta inventada; branch/error/externa representados), não 1-seta-por-aresta — senão fica ilegível e duplica o gate estrutural do `grill-doc`.

Nenhum toca as 15 decisões do DESIGN §8; são ajustes mecânicos de precisão dos prompts.
