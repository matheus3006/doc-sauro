---
inclusion: manual
---

# Prompt · `documentar-negocio`

> A joia do **track de negócio**. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem parser. Roda **um por fluxo**, depois do `contexto-produto`, sobre um fluxo que o **track técnico já documentou e aprovou**.

Você **reescreve um fluxo já rastreado em linguagem de negócio**, pra uma **PO nova** entender o que o app faz e por quê — **sem ver uma linha de código**. Não é resumo do doc técnico: é uma **tradução ancorada**. O QUÊ você **herda** do doc técnico (já verificado); o PORQUÊ você **elicita ou infere-e-marca**; e você **prova a fidelidade** por uma tabela de trace escondida.

> **Este prompt encoda dois comportamentos** que no Claude seriam skills e que **aqui não existem** — então estão escritos abaixo, não invocados:
> 1. **Grill de produto:** interroga cada passo por **sentido de negócio** (job, impacto, regra, consequência, porquê); nunca aceita "só reescrever bonito".
> 2. **Linguística:** escreve simples (POV do usuário, voz ativa, zero jargão) e traz **um exemplo real fiel** ao fluxo.

## Princípio-norte (inegociável)

> **Linguagem simples, mas ancorada — nunca ficção.**
> - **O QUÊ (comportamento)** você **herda** do doc técnico `docs/03-fluxos/<slug>.md` (que já verificou com `arquivo:linha`). Reescreve em linguagem de gente; **não re-cita** código na prosa e **não contradiz** o doc técnico.
> - **O PORQUÊ (valor / regra / decisão)** o código não prova. Entra **atribuído** (humano: verbatim + quem + quando) **ou** `[inferido do código · a confirmar]` — inferência **sempre com base** no que o fluxo mostra. Nunca inventado.
> - **Zero código na prosa.** A PO nunca vê `arquivo:linha`. A âncora à verdade é o **link** pro doc técnico + a **tabela de trace** no rodapé (recolhível).

## Insumos

- `.arquitetura/contexto.md` e `.arquitetura/contexto-produto.md` (persona, jobs, glossário de produto — a fonte do vocabulário).
- **O doc técnico do fluxo:** `docs/03-fluxos/<slug>.md` (o QUÊ verificado) + `.arquitetura/mapa/fluxos/<slug>.grafo.md` (o grafo — as arestas reais).
- **O fluxo** (o mesmo `<slug>` do doc técnico).

## A grill de produto (o interrogatório — o coração)

Percorra o fluxo do doc técnico **passo a passo**. Em **cada** passo/branch com sentido de negócio (ignore utilitário puro), pergunte — e responda no doc, atribuído ou inferido-marcado:

| | Pergunta de negócio | Onde a resposta mora |
|---|---|---|
| **Job** | que necessidade do usuário esse passo serve? | *Como funciona* / *Quem usa* |
| **Impacto** | se falha, quem sente e como? | *Quando dá errado* |
| **Regra** | esse guard/limiar é uma política de negócio? qual? | *Regras & porquês* |
| **Consequência** | dá errado → perde dinheiro / cliente / compliance / confiança? | *Quando dá errado* |
| **Porquê** | por que foi desenhado assim? | *Regras & porquês* (atribuído ou inferido + base) |

Um passo com todos "N/A" é suspeito — provavelmente você não leu o passo técnico fundo o bastante. A âncora de cada resposta de **comportamento** é a **seção do doc técnico** (ou aresta do grafo) que a sustenta — vai na tabela de trace.

## A linguística (como escrever)

- **Zero jargão / zero nome de código** na prosa. `idempotente` → "não cobra duas vezes"; `PENDING_REVIEW` → "fica esperando um humano revisar".
- **POV do usuário.** "Você pede o pagamento e vê 'processando'", não "o controller responde 202".
- **Voz ativa, ator nomeado, uma ideia por frase.** Sujeito concreto (a persona, o sistema) — nunca "isso/aquilo".
- **Só o vocabulário do glossário** do `contexto-produto`, sempre o mesmo termo.
- **Um exemplo real, fiel.** Um cenário concreto e nomeado (*"Maria pede um pagamento de R$ 250…"*), **rotulado `Exemplo:`**, cujos **desfechos existem no grafo** (não invente um caminho que o fluxo não tem). Valores podem ser ilustrativos; a **estrutura** obedece ao fluxo rastreado. Se houver fixture/teste real à mão, prefira os dados de lá.

## Saída · `docs/00-dominio/fluxos-negocio/<slug>.md`

Publicável (Camada 0 · Domínio). Frontmatter Docusaurus + o esqueleto abaixo. **Toda frase de comportamento tem uma linha na tabela de trace.**

```md
---
sidebar_position: <n>
title: "Negócio: <nome legível>"
description: "<uma linha, em linguagem de negócio>"
---

# <nome legível> — para o negócio
> Companheiro de negócio do fluxo técnico: [<slug>](../../03-fluxos/<slug>.md). Escrito pra quem toca o produto.

## Em uma frase
<o job que o fluxo resolve, em 1 frase>

## Quem usa
<persona(s) do contexto-produto + o que querem>

## Como funciona
<o caminho feliz narrado em linguagem de gente, JÁ com o exemplo real embutido>

## Quando dá errado
<os error paths e a compensação em termos de negócio: o que o produto faz, quem sente>

## Regras & porquês
<os guards/limiares como política; cada porquê atribuído OU [inferido do código · a confirmar] + base>

## Trace
<recolhível — a prova de que nada é ficção; cada afirmação → base no doc técnico>
```

O bloco **Trace** usa `<details>` do MDX pra recolher:

```md
<details>
<summary>Trace — cada afirmação, sua base (a PO não precisa; o cético clica)</summary>

| Afirmação (seção) | Tipo | Base | Estado |
|---|---|---|---|
| <frase resumida> | o quê / regra / porquê | <seção do doc técnico OU aresta do grafo OU quem atribuiu> | herdado-verificado / inferido-a-confirmar / atribuído |

</details>
```

## Critério de conclusão (checável e exaustivo)

- `docs/00-dominio/fluxos-negocio/<slug>.md` existe, com o esqueleto completo.
- **Zero** nome de classe/arquivo/método/`arquivo:linha` na prosa (fora do bloco Trace recolhível).
- **Toda** frase de comportamento (o quê) tem linha no Trace, com base no doc técnico e estado `herdado-verificado`.
- **Todo** porquê é `atribuído` OU `[inferido do código · a confirmar]` **com base** — zero porquê sem origem.
- O **exemplo** existe, está rotulado, e **nenhum** desfecho dele está fora do grafo.
- As **5** perguntas da grill foram respondidas ou marcadas N/A (com motivo) nos passos de negócio.
- O vocabulário é **só** o do glossário do `contexto-produto`.

## Handoff

Imprima ao humano, literalmente:

> Doc de negócio gravado em `docs/00-dominio/fluxos-negocio/<slug>.md`. Próximo passo: rode **`grill-negocio`** apontando para ele e para o doc técnico `docs/03-fluxos/<slug>.md`.
