# Prompts da trilha — dois tracks (técnico + negócio)

Dez prompts **portáveis** em dois tracks — **técnico** (o que o código faz, citado `arquivo:linha`) e **negócio** (o que o produto faz, pra uma PO nova, em linguagem simples). Provam a tese do [DESIGN](../DESIGN.md): *mapa barato + leitura forçada + gates ⇒ some o gap raso*. Rodam em **Amazon Q + GitHub Copilot + Kiro** — o build acontece no Claude Code, mas o resultado **não usa nada de Claude**.

## Contrato de portabilidade (todo prompt respeita)

- **Standalone.** Cada prompt é uma sessão isolada; não chama outro prompt nem subagente.
- **Sem Claude.** Zero `/grilling`, zero `/domain-modeling`, zero skill. Os comportamentos (leitura forçada, registro de domínio) estão **encodados no texto**, não invocados.
- **Sem parser.** Leitura é LLM-native — nada de ctags/tree-sitter (quebraria a portabilidade poliglota).
- **Handoff explícito.** Cada prompt termina imprimindo o próximo comando. O **mapa é o ledger** — a única memória entre sessões.

## Cadeia (ordem de execução)

**Track técnico** — o que o código faz (extração + gates):

| # | Prompt | Trilha | Produz |
|---|---|---|---|
| 0 | [`bootstrap-contexto`](bootstrap-contexto.md) | extração + elicitação | `.arquitetura/contexto.md` |
| 1 | [`mapear-estrutura`](mapear-estrutura.md) | extração | `.arquitetura/mapa/` (semente L0-L1 + cobertura) |
| 2 | [`documentar-fluxo`](documentar-fluxo.md) | extração (a joia) | `docs/03-fluxos/<slug>.md` + `.arquitetura/mapa/fluxos/<slug>.grafo.md` |
| 3 | [`grill-doc`](grill-doc.md) | gate | veredito: completude estrutural (bloqueante) + citação (bloqueante) + rubrica (consultiva) |
| 4 | [`grill-mermaid`](grill-mermaid.md) | gate | veredito: sintaxe + MDX + fidelidade ao grafo |

**Track de negócio** — o que o produto faz, pra uma PO nova (roda **depois do track técnico completo**, pra inferir da base já verificada):

| # | Prompt | Trilha | Produz |
|---|---|---|---|
| 5 | [`contexto-produto`](contexto-produto.md) | elicitação (lente de PO) | `.arquitetura/contexto-produto.md` (personas, jobs, glossário) |
| 6 | [`documentar-negocio`](documentar-negocio.md) | elicitação (a joia) | `docs/00-dominio/fluxos-negocio/<slug>.md` (+ trace recolhível) |
| 7 | [`grill-negocio`](grill-negocio.md) | gate | veredito: âncora/honestidade + zero jargão + exemplo fiel (bloqueantes) + legibilidade (consultiva) |
| 8 | [`documentar-visao`](documentar-visao.md) | elicitação (síntese · Camada 0) | `docs/00-dominio/visao-de-produto.md` (overview de app + mapa de fluxos com cobertura) |
| 9 | [`grill-visao`](grill-visao.md) | gate | veredito: âncora/honestidade + zero jargão + **mapa fiel** (bloqueantes) + legibilidade (consultiva) |

> Os passos **8-9** produzem a **Visão de Produto** — a porta de entrada de Camada 0 pra uma PO nova entender o app **inteiro**. Rodam **por último**, depois de **pelo menos um** `documentar-negocio` (a visão **liga** os docs de negócio já escritos e cita o "Em uma frase" de cada um); re-rode a visão quando novos fluxos ganharem doc, pra o mapa crescer. O `grill-visao` troca o "exemplo fiel" do `grill-negocio` por **"mapa fiel"**: todo fluxo linkado existe, o one-liner é idêntico ao do doc de negócio, e a **cobertura é honesta** (não finge cobrir o app inteiro).

## Princípio-norte (fonte canônica: [DESIGN §2](../DESIGN.md))

> O mapa e o depoimento humano são **hipóteses** — nunca citados. A única fonte citável sobre o que o código FAZ é o próprio código, como **`arquivo:linha`**.

Cada prompt carrega uma forma compacta desse princípio inline (o preço da portabilidade: sem disclosure entre arquivos em runtime). A forma longa vive só aqui e no DESIGN.

No **track de negócio** o princípio ganha uma **terceira categoria de verdade**: além de *fato citado* (`arquivo:linha`) e *atribuído ao humano*, existe **`[inferido do código · a confirmar]`** — um porquê inferido da base técnica **já verificada**, sempre com base explícita e marcado como não-confirmado. Nunca ficção; a linguagem simplifica, mas não desancora.

## Fora do escopo deste slice

Os geradores por-tipo-de-doc do track técnico (glossário, restrições, regras, topologia, dados, config, runbook, adr, rastreabilidade — §9); o build-gate do `docusaurus build` (§7, futuro). O triplo-write `.amazonq/.github/.kiro` **já existe** (`../tools/empacotar.py` → `../dist/`).
