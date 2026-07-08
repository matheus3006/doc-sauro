# grill-doc — wakeup-run-settle

Insumos: `docs/03-fluxos/wakeup-run-settle.md` × `.arquitetura/mapa/fluxos/wakeup-run-settle.grafo.md` (56 arestas).

## Gate 1 · Completude estrutural (BLOQUEANTE)

Toda aresta classificada. **Coberta:** 43 · **Fora-de-escopo:** 13 · **AUSENTE:** 0.

| Aresta | Classe | Onde no doc |
|---|---|---|
| A1 | fora-de-escopo | Fora de escopo (guard de segurança) |
| A2 A3 A4 | coberta | Happy path §A #1-2 |
| A5 | coberta | Happy path §A #3 + Error paths |
| A6 | fora-de-escopo | Fora de escopo (gate do arquiteto) |
| A7 A8 | coberta | Happy path §A #4 |
| A9 A10 A11 A12 | coberta | Compensação (mesma unidade `BudgetService`) |
| A13 A14 A15 A16 A17 A18 | coberta | Happy path §A #5 (+ Error paths p/ A14) |
| B1 B2 | coberta | Happy path §B #6 + Gatilho |
| B3 | coberta | Happy path §B #7 + Error paths |
| B4 | fora-de-escopo | Fora de escopo (gate do arquiteto) |
| B5 B6 B7 | coberta | Happy path §B #7 (+ Error paths) |
| B8 B9 B10 | coberta | Happy path §B #8 |
| B11 B12 B13 | coberta | Happy path §B #9-10 |
| B14 | coberta | Error paths ("Agent removido entre enqueue e dispatch", `AdapterRunExecutor.java:104-106`) — **pego pelo gate; era AUSENTE, corrigido** |
| B15 B16 | fora-de-escopo | Fora de escopo (workspace/skills) — falha de B16 ainda coberta em Error paths |
| B17 B18 | coberta | Happy path §B #10 + Error paths |
| B19 | fora-de-escopo | Fora de escopo (preview) |
| B20 | fora-de-escopo | Fora de escopo (turno de conversa) |
| B21 B22 B23 | coberta | Happy path §B #10 + Chamadas externas + Error paths |
| B24 | fora-de-escopo | Fora de escopo (preview) |
| B25 B26 B27 B29 B30 B31 | coberta | Settle §C #11 |
| B28 | coberta | Error paths (review de run sintético/alheio) |
| B32 B33 B34 B35 | coberta | Settle §C #12 + Transições |
| C1 C2 C3 | coberta | Gatilho + Timeout/retry |

**Resultado do Gate 1: PASSA** — 0 AUSENTE (13 fora-de-escopo, todas marcadas no grafo e listadas no doc com motivo). Nota: uma aresta (B14) entrou AUSENTE na 1ª passada e foi coberta antes do veredito — é a evidência do gate funcionando.

## Gate 2 · Disciplina de citação (BLOQUEANTE)

Varredura frase a frase das seções de comportamento (Gatilho, Happy path, Error paths, Chamadas externas, Transições/idempotência/timeout/compensação).

- Frases de comportamento **SEM-CITAÇÃO:** 0 — toda afirmação carrega `arquivo:linha`.
- **FONTE-ERRADA** (comportamento apoiado no mapa ou no depoimento como fato): 0. A seção *Divergências* é explícita: onde o `CONTEXT.md` afirma comportamento, a afirmação foi reverificada no código e citada por `arquivo:linha` (`IssueRepository.java:78,98,119`), não pelo depoimento. O depoimento aparece só como atribuição de *porquê/restrição*.

**Resultado do Gate 2: PASSA.**

## Gate 3 · Rubrica de fluxo (CONSULTIVA)

| Item | Estado |
|---|---|
| Gatilho nomeado | presente (3 gatilhos: HTTP + 2 agendados) |
| Happy path completo | presente (A enqueue · B dispatch · C settle) |
| Cada error path real | presente (13 caminhos, incl. o pego pelo gate) |
| Cada chamada externa | presente (Postgres · volume Docker · CLI no container) |
| Transições de estado | presente (Run + Issue, de→para, com guarda) |
| Idempotência | presente (coalescing, claim CAS, lock da Issue, RUN_OPEN 1×) |
| Timeout / retry | presente (lease 2min + reaper; sem auto-retry de Issue) |
| Compensação | presente (drena-até-checkpoint + guard limitCents>0) |

Recomendações: nenhuma bloqueante. Sugestão consultiva: quando existir, linkar os docs dos 5 fluxos *fora-de-escopo* (arquiteto, workspace/skills, preview, turno, segurança) para fechar a navegação.

## Resultado: **APROVADO** (Gate 1 PASSA + Gate 2 PASSA)

Handoff: rode `grill-mermaid` no doc `docs/03-fluxos/wakeup-run-settle.md`.
