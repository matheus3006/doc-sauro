# grill-visao — visao-de-produto

Auditoria de `docs/00-dominio/visao-de-produto.md` contra os docs de negócio que ela liga (`docs/00-dominio/fluxos-negocio/*.md`), o índice do mapa (`.arquitetura/mapa/_indice.md`) e o glossário (`.arquitetura/contexto-produto.md`). Commit pinado `d20f55f`.

## Gate 1 · Âncora & honestidade (bloqueante): **PASSA**

- **1 linha de mapa** (o fluxo documentado), **1 com linha no Trace** apontando `fluxos-negocio/wakeup-run-settle.md` §Em uma frase, estado `herdado-verificado`. O doc linkado **existe** (conferido no disco). **SEM-ÂNCORA: 0.**
- **Síntese "O que é":** marcada `[inferido do código · a confirmar]`, base = fluxo documentado + `contexto.md` §Elicitação (Propósito/Tier). Não afirmada como fato. **Cobertura:** marcada, base = `_indice.md`. **Personas/jobs/vocabulário:** entram com a marcação **herdada** do `contexto-produto` (atribuído: operador). Nenhum fato novo afirmado sem marca. **FICÇÃO: 0.**

**Inferências a confirmar** (fila do dono de produto — não travam, mas não são fato):
1. "O que o produto é no todo" — síntese do conjunto de fluxos + propósito elicitado. Confirmar quando houver mais fluxos documentados.
2. A **cobertura** (~12 áreas de produto; 9 sem doc + a aprovação prévia) — inferida do inventário do mapa, ela mesma marcada `[inferido]` nos entrypoints.
3. Cada **área "ainda sem doc"** — nome de produto inferido dos entrypoints do mapa; algumas podem ser internas (ex.: histórico de ações, passagem de contexto), não fluxos de produto de verdade.

## Gate 2 · Zero jargão na prosa (bloqueante): **PASSA**

- **0** nome de classe/arquivo/método na prosa. **0** `arquivo:linha`. **0** enum cru (usa "feito / esperando revisão / bloqueado", herdado do one-liner já aprovado).
- **0** termo técnico cru da lista proibida (`idempotente`, `endpoint`, `lock`, `thread`…).
- Código só aparece como **par técnico** no *Vocabulário* (`Company`, `Agent`, `Issue`, `wakeup`, `Budget` — a ponte permitida, como no glossário do `grill-negocio`) e dentro do bloco **Trace** (recolhível). Ambos permitidos.

## Gate 3 · Mapa fiel (bloqueante): **PASSA**

- **Link resolve:** `fluxos-negocio/wakeup-run-settle.md` existe relativo à visão (conferido). Link quebrado: 0.
- **One-liner idêntico:** a frase do fluxo no mapa é **byte-a-byte** o "Em uma frase" do doc de negócio (diff automático: idêntico, incluindo negritos e pontuação). **ONE-LINER-DRIFT: 0.**
- **Sem fluxo fantasma / sem caminho cross-flow inventado:** o único fluxo listado como documentado tem doc; a lista "ainda sem doc" são nomes marcados, sem narrativa que atravesse fluxos. **MAPA-INFIEL: 0.**
- **Cobertura bate com o `_indice.md`** (conferido): 3 módulos `parcial` (execution/work/governance) + 11 `esqueleto`, dos quais 9 são áreas de produto + 2 transversais (config, common). A visão diz "1 fluxo, tocando 3 áreas (governança só em parte), ~12 áreas conhecidas, 9 + aprovação prévia sem doc, 2 transversais fora" — confere. **COBERTURA-FALSA: 0.**
  - *Catch do gate, corrigido antes do veredito:* a 1ª redação contava a governança como área "coberta" (via orçamento) **e** listava a "aprovação prévia" entre as 9 sem doc — um duplo-uso do módulo `governance`. Foi ajustado: a prosa agora diz explicitamente que a governança é coberta **só em parte** (orçamento sim, aprovação prévia não), e a aprovação prévia saiu da lista das 9 pra ser nomeada à parte. Aritmética honesta (3+9+2=14). *(O gate pegou a imprecisão antes do veredito — como o `grill-negocio` ajustou os rótulos de seção e o técnico pegou B14/B21.)*

## Gate 4 · Legibilidade (consultiva)

- [x] **O que é** diz o produto no todo sem rodeio ("operar agentes de IA como funcionários… de forma controlada") — ok.
- [x] **POV da PO** ("você monta uma empresa, cria seus agentes e dá trabalho a eles") — ok.
- [x] **Voz ativa**, ator nomeado (operador, agente, agente orquestrador) — ok.
- [x] **Vocabulário** só do glossário, consistente — ok.
- [x] **Esqueleto completo** (*O que é · Pra quem é · Vocabulário · Os fluxos principais + Cobertura · Trace*) — ok.

**Recomendações (não travam):**
- A lista "ainda sem doc" mistura áreas claramente de produto (criar empresa, montar organização) com áreas que podem ser internas (histórico de ações, passagem de contexto). Quando o dono de produto confirmar, marcar as internas como "fora do site" em vez de "fila de trabalho".
- "escolher o motor de cada um" (em *Montar a organização*) — "motor" é o termo de produto pro adaptador de IA; conferir se a PO reconhece o termo ou se convém glossar na primeira aparição.

## Resultado: **APROVADO** (os 3 gates bloqueantes PASSAM)

A visão de produto está **ancorada** (todo fluxo linkado existe e cita o "Em uma frase" aprovado), **sem jargão** e **fiel ao mapa** (link resolve, one-liner idêntico, cobertura honesta sem silenciar o que falta). Pronta pra PO / publicação. Confirme as 3 inferências marcadas quando um dono de produto puder — são hipóteses do modelo (o que o app é no todo, a cobertura estimada, quais áreas viram fluxo de produto), não fato.
