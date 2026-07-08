---
inclusion: manual
---

# Prompt · `contexto-produto`

> Abre o **track de negócio** da trilha. Portável: roda em Amazon Q, GitHub Copilot ou Kiro — **standalone**, sem subagente, sem parser/ctags/tree-sitter. Leitura **LLM-native**. Roda **uma vez por projeto**, **depois** de todo o track técnico (contexto → mapa → fluxos → gates) estar completo.

Você produz a **lente de PO**: quem usa o produto, que **jobs** ele resolve e o **vocabulário de produto** que dá linguagem aos docs de negócio. Produz `.arquitetura/contexto-produto.md` — o pano de fundo que todo doc de negócio lê. Roda **depois do técnico** de propósito: quando o negócio não tem dono humano à mão pra explicar, você **infere da base técnica já verificada** — e só dá pra inferir do que já foi rastreado.

## Princípio-norte (inegociável)

> Este é o track de **elicitação**, não de extração. Você **não afirma comportamento de código como fato** aqui — isso é do doc técnico (`arquivo:linha`). O que você captura é **produto**: persona, job, termo de domínio. Cada afirmação entra **atribuída** (humano: verbatim + quem + quando) **ou** `[inferido do código · a confirmar]` (ancorada numa observação do doc técnico) — **nunca inventada**.

A regra de ouro do inferido: uma inferência **sempre aponta a base** (que observação do doc técnico a sustenta). Inferência sem base é chute — e chute não entra.

## Insumos

- `.arquitetura/contexto.md` (tier, propósito no vocabulário do domínio, blast radius, restrições, padrões-que-não-se-aplicam — já elicitados).
- `docs/03-fluxos/*.md` — os docs técnicos de fluxo **já produzidos e aprovados** (a base verificada de onde inferir).
- `.arquitetura/mapa/` — para o vocabulário de módulos/entrypoints.

## Passos

### 1 · Reúna a base

Leia o `contexto.md` inteiro e cada doc técnico de fluxo existente. O `contexto.md` já traz muito produto elicitado (propósito, blast radius, restrições) — **reuse, não re-elicite**. Os docs de fluxo mostram os **atores** (quem dispara), os estados e os termos de domínio.

### 2 · Personas / atores

Quem usa o produto — e o que cada um quer. Fonte: o humano; na ausência, os **atores** dos diagramas e o propósito do contexto (inferido). Para cada persona:

- **Nome** no vocabulário do domínio (não "usuário genérico").
- **O que faz** com o produto (o job de alto nível).
- Marque **atribuído** (verbatim + quem + quando) **ou** `[inferido do código · a confirmar]` com a base.

### 3 · Jobs (JTBD)

Os "trabalhos" que o produto resolve, na voz de quem tem o problema (*"quando eu ___, quero ___, pra ___"*). Derive do propósito elicitado + dos fluxos. Cada job atribuído ou inferido-marcado.

### 4 · Glossário de produto

Os **termos user-facing** do domínio, cada um com uma **definição simples** (uma frase, sem jargão). Este glossário é a **fonte de vocabulário** do `documentar-negocio` e o que o `grill-negocio` usa pra barrar jargão. Inclua o **par técnico → produto** quando ajudar (ex.: *"Issue = uma tarefa de trabalho"*; *"Run = uma tentativa de execução"*).

### 5 · Grave `.arquitetura/contexto-produto.md`

Interno, **fora de `docs/`**. Use exatamente esta forma:

```md
# Contexto de Produto — <nome do projeto>
> Interno. Lente de PO da trilha. Elicitação: atribuída OU [inferido do código · a confirmar].
> Frescor: <data-hora> · <commit/hash se houver>

## Personas
- **<Persona>** — <o que faz> — <atribuído: quem, quando> | [inferido do código · a confirmar] — base: <observação do doc técnico>

## Jobs (JTBD)
- Quando <situação>, <persona> quer <resultado>, pra <valor>. — <atribuído | inferido + base>

## Glossário de produto
- **<termo>** — <definição simples de 1 frase> (técnico: `<par>`) — <atribuído | inferido + base>
```

## Critério de conclusão (checável)

- `.arquitetura/contexto-produto.md` existe, fora de `docs/`.
- **Toda** persona, job e termo é **atribuído** OU **`[inferido do código · a confirmar]` com base explícita**. Zero afirmação sem uma das duas.
- O glossário cobre os termos de domínio que aparecem nos docs técnicos de fluxo.
- **Zero** `arquivo:linha` na prosa deste doc (isto é produto, não código) — a base do inferido aponta a **observação/seção do doc técnico**, não uma linha de código.
- **Nenhum** termo técnico (nome de classe/arquivo) tratado como termo de produto.

## Handoff

Imprima ao humano, literalmente:

> Contexto de produto gravado em `.arquitetura/contexto-produto.md`. Próximo passo: rode **`documentar-negocio`** informando **um** fluxo que o track técnico já documentou (ex.: `wakeup-run-settle`).
