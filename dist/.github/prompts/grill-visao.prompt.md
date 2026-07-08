---
description: 'Você audita a visão de produto em quatro frentes: âncora/honestidade (bloqueante), zero jargão (bloqueante), mapa fiel (bloqueante) e legibilidade (consultiva).'
agent: 'agent'
---

# Prompt · `grill-visao`

> Gate da **Visão de Produto** (Camada 0). Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem parser. Roda depois do `documentar-visao`, apontando pra visão, pros docs de negócio que ela liga, e pro índice do mapa.

Você **audita a visão de produto** em quatro frentes: **âncora/honestidade** (bloqueante), **zero jargão** (bloqueante), **mapa fiel** (bloqueante) e **legibilidade** (consultiva). Você não reescreve — emite um **veredito** com a lista exata do que consertar. A diferença pro `grill-negocio`: aqui não há um exemplo contra um grafo; a fidelidade é do **mapa** (todo fluxo linkado existe e diz o que o doc dele diz) e da **cobertura** (a visão não finge cobrir o app inteiro).

## Insumos

- A visão: `docs/00-dominio/visao-de-produto.md` (com o bloco Trace).
- Os docs de negócio que ela liga: `docs/00-dominio/fluxos-negocio/*.md` (cada um com seu "Em uma frase").
- `.arquitetura/mapa/_indice.md` (a tabela de cobertura — quantos fluxos/entrypoints o mapa conhece).
- `.arquitetura/contexto-produto.md` (o glossário — a lista de vocabulário permitido).

## Gate 1 · Âncora & honestidade — **BLOQUEANTE**

A tese: **nada na visão é ficção — toda afirmação é rastreável.** Varra o doc:

- Toda **linha do mapa** (cada fluxo documentado) tem linha no **Trace** apontando um `docs/00-dominio/fluxos-negocio/<slug>.md` que **existe de verdade**, estado `herdado-verificado`? Sem linha, ou doc inexistente → **SEM-ÂNCORA** (reprova).
- O **"O que é"** (síntese) está `[inferido do código · a confirmar]` **com base** (conjunto de fluxos + propósito)? A **cobertura** (N de ~M) idem, base no `_indice.md`? Uma síntese ou cobertura afirmada como fato, sem marca → **FICÇÃO** (reprova).
- **Personas / jobs** entram com a marcação herdada do `contexto-produto` (atribuído ou inferido-com-base), nunca como fato novo? Senão → **FICÇÃO**.
- Liste **todas as inferências a confirmar** num bloco à parte — é a fila do dono de produto. (Registra-e-segue: não reprova por *ser* inferência; reprova por inferência **sem base** ou fato inventado.)

## Gate 2 · Zero jargão na prosa — **BLOQUEANTE**

A PO não pode topar com código. Fora do bloco Trace (recolhível), a prosa tem algum **nome de classe/arquivo/método**, `arquivo:linha`, ou **termo técnico cru** (`idempotente`, `mutex`, `PENDING_REVIEW`, `endpoint`, `lock`, `thread`)? Cada ocorrência → **JARGÃO** (reprova), com a frase e a sugestão em linguagem de gente. (Os pares `técnico: <nome>` na seção *Vocabulário* são a ponte permitida — não são jargão cru, como no glossário do `grill-negocio`.)

## Gate 3 · Mapa fiel — **BLOQUEANTE**

O mapa liga a verdade certa e não engana sobre cobertura:

- Todo fluxo do mapa **linka um doc que existe** e o **link resolve** (caminho relativo certo)? Link quebrado → **MAPA-INFIEL** (reprova).
- O **one-liner** de cada fluxo é **idêntico** ao "Em uma frase" do doc de negócio linkado (citado, não reescrito)? Divergiu → **ONE-LINER-DRIFT** (reprova) — reescrever desancora do que o `grill-negocio` aprovou.
- Existe algum fluxo listado como documentado que **não tem doc**, ou algum caminho **cross-flow inventado** (uma história que atravessa fluxos que os docs não conectam)? → **MAPA-INFIEL** (reprova).
- A **nota de cobertura** bate: `N` = nº de docs de negócio que existem de fato; `~M` = o que o `_indice.md` conhece; e o que falta está **listado** (não silenciado)? Cobertura omitida ou número errado → **COBERTURA-FALSA** (reprova).

## Gate 4 · Legibilidade — **CONSULTIVA**

Marque cada item `ok` / `fraco` / `N/A`:

- [ ] **O que é** diz o produto no todo sem rodeio.
- [ ] **POV da PO** (não da máquina / não do código).
- [ ] **Voz ativa**, ator nomeado, uma ideia por frase.
- [ ] **Vocabulário** só do glossário, consistente.
- [ ] **Esqueleto completo** (*O que é · Pra quem é · Vocabulário · Os fluxos principais + Cobertura · Trace*).

Consultivo = **não reprova**, mas todo `fraco` vira **recomendação**.

## Veredito

```md
# grill-visao — visao-de-produto
## Gate 1 · Âncora & honestidade (bloqueante): PASSA / REPROVA
SEM-ÂNCORA: <n> · FICÇÃO: <n>  — Inferências a confirmar: <lista>
## Gate 2 · Zero jargão (bloqueante): PASSA / REPROVA
JARGÃO: <n>  — <frase + sugestão>
## Gate 3 · Mapa fiel (bloqueante): PASSA / REPROVA
MAPA-INFIEL: <n> · ONE-LINER-DRIFT: <n> · COBERTURA-FALSA: <n>
## Gate 4 · Legibilidade (consultiva)
<checklist>  — recomendações: <lista>
## Resultado: APROVADO  (só se os 3 bloqueantes PASSAM)
        ou   BLOQUEADO  → conserte: <lista exata>
```

## Critério de conclusão (checável)

- **Toda** linha do mapa classificada (ancorada / SEM-ÂNCORA), e o doc linkado conferido que existe.
- **Todo** one-liner comparado ao "Em uma frase" da fonte; **toda** síntese e a cobertura classificadas (inferido-com-base / FICÇÃO).
- **Toda** ocorrência de jargão listada.
- Cobertura conferida contra o `_indice.md` (N e ~M).
- Os **5** itens de legibilidade marcados.
- Veredito final coerente com os **3** gates bloqueantes.

## Handoff

- **APROVADO** → imprima: *"grill-visao aprovado. A visão `docs/00-dominio/visao-de-produto.md` está ancorada, sem jargão e fiel ao mapa (todo fluxo linkado existe e a cobertura é honesta) — pronta pra PO / publicação. Confirme as inferências marcadas quando um dono de produto puder."*
- **BLOQUEADO** → imprima: *"grill-visao bloqueado por <n> âncora / <n> jargão / <n> mapa. Volte ao **`documentar-visao`** e cubra a lista acima."*
