# Prompts da trilha — slice vertical (fluxos)

Cinco prompts **portáveis** que provam a tese do [DESIGN](../DESIGN.md): *mapa barato + leitura forçada + gates ⇒ some o gap raso*. Rodam em **Amazon Q + GitHub Copilot + Kiro** — o build acontece no Claude Code, mas o resultado **não usa nada de Claude**.

## Contrato de portabilidade (todo prompt respeita)

- **Standalone.** Cada prompt é uma sessão isolada; não chama outro prompt nem subagente.
- **Sem Claude.** Zero `/grilling`, zero `/domain-modeling`, zero skill. Os comportamentos (leitura forçada, registro de domínio) estão **encodados no texto**, não invocados.
- **Sem parser.** Leitura é LLM-native — nada de ctags/tree-sitter (quebraria a portabilidade poliglota).
- **Handoff explícito.** Cada prompt termina imprimindo o próximo comando. O **mapa é o ledger** — a única memória entre sessões.

## Cadeia (ordem de execução)

| # | Prompt | Trilha | Produz |
|---|---|---|---|
| 0 | [`bootstrap-contexto`](bootstrap-contexto.md) | extração + elicitação | `.arquitetura/contexto.md` |
| 1 | [`mapear-estrutura`](mapear-estrutura.md) | extração | `.arquitetura/mapa/` (semente L0-L1 + cobertura) |
| 2 | [`documentar-fluxo`](documentar-fluxo.md) | extração (a joia) | `docs/03-fluxos/<slug>.md` + `.arquitetura/mapa/fluxos/<slug>.grafo.md` |
| 3 | [`grill-doc`](grill-doc.md) | gate | veredito: completude estrutural (bloqueante) + citação (bloqueante) + rubrica (consultiva) |
| 4 | [`grill-mermaid`](grill-mermaid.md) | gate | veredito: sintaxe + MDX + fidelidade ao grafo |

## Princípio-norte (fonte canônica: [DESIGN §2](../DESIGN.md))

> O mapa e o depoimento humano são **hipóteses** — nunca citados. A única fonte citável sobre o que o código FAZ é o próprio código, como **`arquivo:linha`**.

Cada prompt carrega uma forma compacta desse princípio inline (o preço da portabilidade: sem disclosure entre arquivos em runtime). A forma longa vive só aqui e no DESIGN.

## Fora do escopo deste slice

Os outros 9 geradores (glossário, restrições, regras, topologia, dados, config, runbook, adr, rastreabilidade); o triplo-write `.amazonq/.github/.kiro` (§9, mecânico, pós-tese); o build-gate do `docusaurus build` (§7, futuro).
