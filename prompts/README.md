# Prompts da trilha — técnico + revisão arquitetural + negócio

Onze prompts **portáveis** em dois tracks e um step opcional — **técnico** (o que o
código faz, citado `arquivo:linha`), **revisão arquitetural** (onde modules podem ganhar
depth) e **negócio** (o que o produto faz, pra uma PO nova, em linguagem simples). Provam
a tese do [DESIGN](../DESIGN.md): *mapa barato + leitura forçada + gates ⇒ some o gap
raso*. Rodam em **Amazon Q + GitHub Copilot + Kiro** — o build acontece no Claude Code,
mas o resultado **não usa nada de Claude**.

## Contrato de portabilidade (todo prompt respeita)

- **Standalone.** Cada prompt é uma sessão isolada; não chama outro prompt nem subagente.
- **Sem Claude.** Zero `/grilling`, zero `/domain-modeling`, zero skill. Os comportamentos
  (leitura forçada, registro de domínio, revisão de modules deep) estão **encodados no
  texto**, não invocados.
- **Sem parser.** Leitura é LLM-native — nada de ctags/tree-sitter (quebraria a portabilidade poliglota).
- **Handoff explícito.** Cada prompt termina imprimindo o próximo comando. O mapa mantém
  o ledger e `.arquitetura/gates/` mantém aprovações entre sessões.

## Constituição operacional dos prompts

Estas regras são compromissos arquiteturais da trilha. Cada prompt carrega o subconjunto
que precisa porque as sessões são isoladas.

1. **Domínio antes da solução.** Termos, atores, invariantes e limites do problema são
   registrados antes de sintetizar comportamento ou valor.
2. **Jurisdição explícita.** Código decide o que o sistema faz; humano decide propósito,
   restrições e trade-offs, sempre atribuído. Inferência permanece marcada.
3. **Compromissos não mudam em silêncio.** Convenções, contratos e decisões existentes
   recebem IDs `ARC-###`. Uma melhoria que os rompa vira `DECISAO-PENDENTE-###`; o prompt
   nunca a incorpora como se já tivesse sido aprovada.
4. **Unidades de cobertura não se misturam.** `ENTRY-###` identifica um entrypoint
   candidato; `FLUXO-<slug>` identifica um fluxo confirmado. Cobertura de entrypoints é
   `C/E`; quantidade de docs é `N`. Um número nunca substitui o outro.
5. **Rastreabilidade por identidade, não por semelhança textual.** Passos, arestas e
   fronteiras usam `PASSO-###`, `ARESTA-###` e `FRONTEIRA-###`. Os gates conferem esses
   IDs contra a evidência original.
6. **Falha fechada.** Insumo obrigatório ausente, entrypoint ambíguo ou gate anterior
   reprovado produz `BLOQUEADO` com a lacuna exata. O agente não adivinha para seguir.
7. **Frescor faz parte da verdade.** Todo artefato interno registra commit e estado do
   working tree. Se estiver alterado, cada arquivo citado recebe fingerprint de conteúdo;
   sem snapshot verificável, o gate bloqueia. Drift vira `stale`.
8. **Gate é artefato persistente.** Cada auditoria grava o veredito em
   `.arquitetura/gates/`; etapas posteriores não dependem da memória do chat.
9. **Humano mantém as decisões humanas.** Pendências de domínio, aprovação, compliance
   e trade-off ficam visíveis; a IA pode organizar evidências, não ratificá-las.
10. **Rubrica fixa, pergunta dinâmica.** Domínio, falha, consistência e demais eixos são
    lentes de cobertura — não perguntas para copiar. Toda `PERG-###` cita um sinal real
    do projeto, explica por que importa e define como será encerrada. As filas vivem em
    `.arquitetura/grills/`; pergunta genérica sem gatilho concreto é inválida.

## Cadeia (ordem de execução)

**Track técnico** — o que o código faz (extração + gates):

| # | Prompt | Trilha | Produz |
|---|---|---|---|
| 0 | [`bootstrap-contexto`](bootstrap-contexto.md) | extração + elicitação dinâmica | `.arquitetura/grills/contexto.md` + `.arquitetura/contexto.md` |
| 1 | [`mapear-estrutura`](mapear-estrutura.md) | extração | `.arquitetura/mapa/` (estrutura + inventário `ENTRY-###`) |
| 2 | [`documentar-fluxo`](documentar-fluxo.md) | extração + grill dinâmico | `.arquitetura/grills/tecnico.<slug>.md` + doc + ledger |
| 3 | [`grill-doc`](grill-doc.md) | gate | `.arquitetura/gates/grill-doc.<slug>.md` — contrato, completude, evidência e visão sistêmica |
| 4 | [`grill-mermaid`](grill-mermaid.md) | gate | `.arquitetura/gates/grill-mermaid.<slug>.md` — sintaxe, MDX e fidelidade ao grafo |

**Revisão arquitetural opcional** — usa somente a base técnica já aprovada e não altera
código:

| # | Prompt | Trilha | Produz |
|---|---|---|---|
| 5 | [`revisar-arquitetura`](revisar-arquitetura.md) | extração + escolha humana + grill dinâmico | HTML temporário + `.arquitetura/revisoes/arquitetura.<escopo>.md` + `.arquitetura/grills/arquitetura.<escopo>.<OPORT-ID>.md` |

**Track de negócio** — o que o produto faz, pra uma PO nova (roda depois de pelo menos
um fluxo passar nos dois gates técnicos):

| # | Prompt | Trilha | Produz |
|---|---|---|---|
| 6 | [`contexto-produto`](contexto-produto.md) | elicitação (lente de PO) | `.arquitetura/contexto-produto.md` (limite, personas, jobs, termos, regras e lacunas) |
| 7 | [`documentar-negocio`](documentar-negocio.md) | tradução + grill dinâmico | `.arquitetura/grills/negocio.<slug>.md` + doc de negócio |
| 8 | [`grill-negocio`](grill-negocio.md) | gate | `.arquitetura/gates/grill-negocio.<slug>.md` — âncora, domínio, linguagem e exemplo |
| 9 | [`documentar-visao`](documentar-visao.md) | síntese + grill dinâmico | `.arquitetura/grills/visao.md` + visão de produto |
| 10 | [`grill-visao`](grill-visao.md) | gate | `.arquitetura/gates/grill-visao.md` — âncora, linguagem, mapa e cobertura `C/E` |

> Os passos **9-10** produzem uma **Visão de Produto progressiva**. Rodam por último,
> depois de pelo menos um `grill-negocio` aprovado. A visão liga somente docs aprovados,
> preserva o "Em uma frase" e declara **N docs aprovados** separado de **C/E entrypoints
> cobertos**; assim a fatia nunca se apresenta como o produto inteiro.

### Dois papéis que não devem ser confundidos

- **Grill dinâmico:** `bootstrap-contexto` e os prompts `documentar-*` geram perguntas
  específicas do projeto em `.arquitetura/grills/` e resolvem a fila por evidência/humano.
- **Gate fixo:** os prompts nomeados `grill-doc`, `grill-negocio` e `grill-visao` auditam
  o resultado com invariantes estáveis. Eles não substituem o grill dinâmico; verificam
  que nenhuma pergunta foi genérica, desancorada ou deixada para a pessoa errada.
- **Revisão arquitetural:** `revisar-arquitetura` explora e mostra `OPORT-ARQ-###`, para
  na escolha humana e só então cria `PERG-ARQ-###` específicas, uma por vez. O HTML é
  efêmero; o ledger e as decisões são persistentes.

## Princípio-norte (fonte canônica: [DESIGN §2](../DESIGN.md))

> O mapa e o depoimento humano são **hipóteses** — nunca citados. A única fonte citável sobre o que o código FAZ é o próprio código, como **`arquivo:linha`**.

Cada prompt carrega uma forma compacta desse princípio inline (o preço da portabilidade: sem disclosure entre arquivos em runtime). A forma longa vive só aqui e no DESIGN.

No **track de negócio** o princípio ganha uma **terceira categoria de verdade**: além de *fato citado* (`arquivo:linha`) e *atribuído ao humano*, existe **`[inferido do código · a confirmar]`** — um porquê inferido da base técnica **já verificada**, sempre com base explícita e marcado como não-confirmado. Nunca ficção; a linguagem simplifica, mas não desancora.

## Fora do escopo deste slice

Os geradores por-tipo-de-doc do track técnico (glossário, restrições, regras, topologia,
dados, config, runbook, adr, rastreabilidade — §9), a implementação de blueprints da
revisão e o build-gate do `docusaurus build` (§7, futuro). O triplo-write
`.amazonq/.github/.kiro` **já existe** (`../tools/empacotar.py` → `../dist/`).
