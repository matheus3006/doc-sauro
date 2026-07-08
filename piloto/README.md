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

## Track de negócio + Visão de Produto (Camada 0)

Sobre o mesmo fluxo e o mesmo commit `d20f55f`, rodei também o track de negócio e a Visão de Produto — a prova de que o QUÊ verificado vira linguagem de PO **sem desancorar**:

| Prompt | Saída | Gate |
|---|---|---|
| `contexto-produto` | [`.arquitetura/contexto-produto.md`](.arquitetura/contexto-produto.md) | — |
| `documentar-negocio` | [`docs/00-dominio/fluxos-negocio/wakeup-run-settle.md`](docs/00-dominio/fluxos-negocio/wakeup-run-settle.md) | [`grill-negocio`](gates/grill-negocio.wakeup-run-settle.md) — **APROVADO** |
| `documentar-visao` | [`docs/00-dominio/visao-de-produto.md`](docs/00-dominio/visao-de-produto.md) | [`grill-visao`](gates/grill-visao.visao-de-produto.md) — **APROVADO** |

A **Visão de Produto** cobre **1** de ~12 áreas de produto que o mapa conhece, com as 9 restantes **listadas** como fila de trabalho (honestidade de cobertura — sem *silent-cap*). Verificação mecânica do gate: o link resolve, o one-liner de cada fluxo é **byte-a-byte** o "Em uma frase" do doc de negócio, a cobertura confere com o `_indice.md` (3 `parcial` + 9 `esqueleto` de produto + 2 transversais), e a prosa tem **zero** nome de classe / `arquivo:linha` / enum cru.

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
