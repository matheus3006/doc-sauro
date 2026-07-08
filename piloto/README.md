# Piloto — fluxo Wakeup → Run → Settle (agente-orquestrator)

Prova de campo do slice vertical: rodei os 5 prompts de [`../prompts/`](../prompts/) contra um repo
real e um fluxo crítico real, produzindo **1 doc de fluxo** que passa os gates.

- **Projeto:** `agente-orquestrator` (Spring Boot / Java 21 / Postgres+Flyway / Next.js).
- **Fluxo:** Wakeup → Run → Settle — a espinha de orquestração (enqueue HTTP + dispatch agendado + reaper).
- **Commit pinado:** `d20f55f` (todas as citações ancoram nele; o working tree driftou durante o piloto — ver EVIDENCIA §5).

## Artefatos (o que cada prompt produziu)

| Prompt | Saída |
|---|---|
| `bootstrap-contexto` | [`.arquitetura/contexto.md`](.arquitetura/contexto.md) |
| `mapear-estrutura` | [`.arquitetura/mapa/_indice.md`](.arquitetura/mapa/_indice.md) · [`execution.md`](.arquitetura/mapa/execution.md) |
| `documentar-fluxo` | [`docs/03-fluxos/wakeup-run-settle.md`](docs/03-fluxos/wakeup-run-settle.md) (o doc) + [grafo rastreado](.arquitetura/mapa/fluxos/wakeup-run-settle.grafo.md) |
| `grill-doc` | [`gates/grill-doc.wakeup-run-settle.md`](gates/grill-doc.wakeup-run-settle.md) — **APROVADO** |
| `grill-mermaid` | [`gates/grill-mermaid.wakeup-run-settle.md`](gates/grill-mermaid.wakeup-run-settle.md) — **LIMPO** |

**Resultado + verificação:** [`EVIDENCIA.md`](EVIDENCIA.md) — 9 gaps que a passada rasa deixaria de fora, os vereditos dos gates, e o `/verify` (194 citações resolvem no commit pinado, mermaid renderiza em SVG de 67KB, frontmatter/MDX limpos, drift do working tree pego e resolvido).

## Reproduzir a verificação

```bash
# citações resolvem contra o commit pinado
python3 <scratchpad>/verify_citations_pinned.py
# mermaid renderiza (mesmo motor do @docusaurus/theme-mermaid)
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg -p pptr.json
```

## Fronteiras do piloto

- `.arquitetura/` e `docs/` vivem **aqui sob `piloto/`** (não dentro do repo agente-orquestrator) — o piloto não muta o repo alvo. Num run real, viveriam na raiz do repo documentado.
- O mapa está **parcial de propósito**: só os módulos que o fluxo tocou foram promovidos a `verificado` (lazy). Os outros 13 seguem `esqueleto` no `_indice.md`.
- **Sem `docusaurus build`** (build-gate é futuro, DESIGN §7). O render foi conferido via `mmdc` + parse de frontmatter + scan MDX — suficiente pro slice.
