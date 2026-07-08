---
description: 'Você escreve a Visão de Produto: o overview de Camada 0 que faz uma PO nova entender o app inteiro — o que o produto é, pra quem, e o mapa dos fluxos principais — sem ver uma linha de código.'
agent: 'agent'
---

# Prompt · `documentar-visao`

> A porta de entrada do **track de negócio**. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem parser. Roda **uma vez por projeto** (e re-roda quando novos fluxos ganham doc de negócio), **depois** do `contexto-produto` e de **pelo menos um** `documentar-negocio` — porque a visão **liga os docs de negócio já escritos**, não os inventa.

Você escreve a **Visão de Produto**: o overview de Camada 0 que faz uma **PO nova** entender **o app inteiro** — o que o produto é, pra quem, e o **mapa dos fluxos principais** — sem ver uma linha de código. Não é um fluxo a mais: é a **porta de entrada** que aponta pra cada doc de negócio por-fluxo. O QUÊ de cada fluxo você **herda** (cita o "Em uma frase" do doc de negócio, que já passou pelo gate); o que o produto **é no todo** você **infere-e-marca**; e você é **honesto sobre a cobertura** — nunca deixa parecer que a fatia documentada é o app inteiro.

> **Este prompt encoda três comportamentos** que no Claude seriam skills e que **aqui não existem** — então estão escritos abaixo, não invocados:
> 1. **Síntese de produto:** olha o conjunto dos fluxos e do propósito elicitado e diz **o que o app é como um todo** — nunca só empilha fluxos.
> 2. **Linguística:** escreve simples (POV da PO, voz ativa, zero jargão), só o vocabulário do glossário.
> 3. **Honestidade de cobertura:** sempre declara quantos fluxos a visão cobre de quantos o mapa conhece; a lista do que falta é a fila de trabalho da PO — nunca um silêncio que engana.

## Princípio-norte (inegociável)

> **Uma visão que liga, não que inventa.**
> - **O QUÊ de cada fluxo** você **herda** do doc de negócio `docs/00-dominio/fluxos-negocio/<slug>.md` (que já passou pelo `grill-negocio`). O one-liner de cada fluxo no mapa é o **próprio "Em uma frase"** daquele doc — você **cita, não reescreve**. Ancorar aqui é ancorar em verdade-de-produto já aprovada. A cadeia fica: **Visão → doc de negócio → doc técnico (`arquivo:linha`)**.
> - **O que o produto É no todo** (o parágrafo de síntese) nenhum fluxo isolado prova. Entra como **`[inferido do código · a confirmar]`**, base = **o conjunto de fluxos documentados + o propósito elicitado** no `contexto.md` / `contexto-produto.md`. Nunca como fato.
> - **Personas e jobs** você herda do `contexto-produto` **com a marcação que eles já têm** (atribuído OU inferido-com-base) — não re-afirma como fato novo.
> - **Zero código na prosa.** A PO nunca vê `arquivo:linha` nem nome de classe. A âncora à verdade é o **link** pro doc de negócio + a **tabela de trace** no rodapé (recolhível).
> - **Nada de narrativa cross-flow fabricada.** Não costure um "dia na vida" que atravesse fluxos que os docs não conectam — inventar um caminho entre fluxos é ficção. Se ilustrar, aponte pro exemplo do próprio doc de um fluxo.

## Insumos

- `.arquitetura/contexto-produto.md` — personas, jobs, glossário de produto (a fonte do vocabulário e de quem usa).
- `.arquitetura/contexto.md` — tier, propósito no vocabulário do domínio, blast radius, restrições (a fonte do "o que é" no todo).
- **Todos** os docs de negócio já escritos: `docs/00-dominio/fluxos-negocio/*.md` (o QUÊ herdado — a fonte de cada linha do mapa e do one-liner citado).
- `.arquitetura/mapa/_indice.md` — a tabela de cobertura (quantos módulos/entrypoints o mapa conhece) — a base pra nota de cobertura e pra lista "ainda sem doc".

## A grill de produto (o interrogatório — nível app)

Diferente do `documentar-negocio` (que grelha passo a passo), aqui você grelha o **app inteiro**. Responda cada uma no doc — herdado / atribuído / inferido-marcado:

| | Pergunta de produto | Onde a resposta mora |
|---|---|---|
| **O que é** | em 1-2 frases, o que este produto faz no mundo? | *O que é* (inferido + base: fluxos + propósito) |
| **Pra quem** | quem usa e que job cada um tem? | *Pra quem é* (herdado do contexto-produto) |
| **Quais fluxos** | quais são os fluxos principais — e qual o job de cada? | *Os fluxos principais* (herdado: "Em uma frase" de cada doc) |
| **O que falta** | quais fluxos o mapa conhece mas ainda não têm doc? | *Os fluxos principais* → "ainda sem doc" (inferido + base: `_indice.md`) |
| **Que palavras** | que termos a PO precisa aprender pra ler isto? | *Vocabulário* (herdado do glossário) |

Um "o que falta" respondido "nada" só vale se o `_indice.md` **confirma** que todo módulo/entrypoint já virou doc de negócio. Senão, você não olhou a cobertura.

## A linguística (como escrever)

- **Zero jargão / zero nome de código** na prosa (mesma régua do `documentar-negocio`). `endpoint` → "porta de entrada"; nome de classe → o termo de produto do glossário.
- **POV da PO.** "Você entra e entende o que o produto faz e por onde começar", não "o índice de domínio lista os fluxos".
- **Voz ativa, ator nomeado, uma ideia por frase.** Sujeito concreto (a persona, o produto) — nunca "isso/aquilo".
- **Só o vocabulário do glossário** do `contexto-produto`, sempre o mesmo termo.
- **Cita o "Em uma frase"** de cada doc de negócio como one-liner do fluxo — não reescreve (reescrever desancoraria do que o `grill-negocio` aprovou).

## Saída · `docs/00-dominio/visao-de-produto.md`

Publicável (Camada 0 · Domínio — a porta de entrada). Frontmatter Docusaurus + o esqueleto abaixo. **Toda linha do mapa e toda afirmação de síntese tem base no Trace.**

```md
---
sidebar_position: 1
title: "Visão de Produto: <nome do app>"
description: "<uma linha, em linguagem de negócio: o que o app é e pra quem>"
---

# <nome do app> — visão de produto

> A porta de entrada do domínio. Pra uma PO nova entender o **app inteiro** — não um fluxo só. Sem código. Cada fluxo aponta pro seu doc de negócio.

## O que é
<1-2 frases: o que o produto é no todo, no vocabulário do domínio — [inferido do código · a confirmar] + base>

## Pra quem é
<as personas do contexto-produto, em prosa, cada uma com o job que resolve — marcação herdada>

## Vocabulário
<só os termos de topo que esta visão usa; 1 frase simples cada (técnico: `<par>`) — marcação herdada do glossário>

## Os fluxos principais

<Documentados — tabela: cada fluxo linkado + o "Em uma frase" citado do doc de negócio:>

| Fluxo | O que faz pra você | Doc |
|---|---|---|
| <nome legível> | <"Em uma frase" citado do doc de negócio> | [ver fluxo](fluxos-negocio/<slug>.md) |

**Cobertura:** esta visão cobre <N> de ~<M> fluxos/entrypoints que o mapa conhece. Os demais ainda não têm doc de negócio — são a fila de trabalho:

<Ainda sem doc de negócio — [inferido do código · a confirmar], base: `_indice.md`:>
- <nome provável do fluxo/entrypoint> — ainda sem doc

## Trace

<recolhível — a prova de que nada é ficção; cada linha do mapa e cada síntese → sua base>
```

O bloco **Trace** usa `<details>` do MDX pra recolher:

```md
<details>
<summary>Trace — cada afirmação e sua base (a PO não precisa; o cético clica)</summary>

| Afirmação (seção) | Tipo | Base | Estado |
|---|---|---|---|
| <fluxo X no mapa — one-liner> | o quê | `docs/00-dominio/fluxos-negocio/<slug>.md` §Em uma frase | herdado-verificado |
| <"o que é" — a síntese> | síntese | conjunto de fluxos documentados + `contexto.md` §Propósito | inferido-a-confirmar |
| <cobertura N de ~M> | cobertura | `.arquitetura/mapa/_indice.md` (tabela de cobertura) | inferido-a-confirmar |
| <persona / job> | pra quem | `contexto-produto.md` §Personas / §Jobs | herdado (atribuído/inferido lá) |

</details>
```

## Critério de conclusão (checável e exaustivo)

- `docs/00-dominio/visao-de-produto.md` existe, com o esqueleto completo (*O que é · Pra quem é · Vocabulário · Os fluxos principais + Cobertura · Trace*).
- **Zero** nome de classe/arquivo/método/`arquivo:linha` na prosa (fora do bloco Trace recolhível).
- **Todo** fluxo documentado no mapa: o **link resolve** para um `docs/00-dominio/fluxos-negocio/<slug>.md` que existe, o one-liner é **idêntico** ao "Em uma frase" daquele doc, e tem linha no Trace com estado `herdado-verificado`.
- O **"O que é"** está marcado `[inferido do código · a confirmar]` **com base** (conjunto de fluxos + propósito) — **nunca** como fato.
- A **cobertura** está declarada (`N de ~M`); a lista "ainda sem doc" é `[inferido do código · a confirmar]` com base no `_indice.md` **ou** atribuída (se um humano a deu). Nada de silêncio que faça a fatia parecer o app inteiro.
- **Personas e jobs** entram com a **marcação herdada** do `contexto-produto` — zero re-afirmação como fato.
- O vocabulário é **só** o do glossário do `contexto-produto`, e cobre os termos que a visão usa.
- **Nenhuma** narrativa cross-flow fabricada (nenhum caminho entre fluxos que os docs não têm).

## Handoff

Imprima ao humano, literalmente:

> Visão de produto gravada em `docs/00-dominio/visao-de-produto.md`, cobrindo <N> de ~<M> fluxos. Próximo passo: rode **`grill-visao`** apontando para ela, para os docs de negócio em `docs/00-dominio/fluxos-negocio/` e para `.arquitetura/mapa/_indice.md`.
