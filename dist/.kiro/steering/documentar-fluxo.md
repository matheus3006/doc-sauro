---
inclusion: manual
---

# Prompt · `documentar-fluxo`

> A joia da trilha. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem parser. Roda **um por fluxo crítico**, depois do `mapear-estrutura`.

Você **rastreia UM fluxo ponta-a-ponta lendo o corpo do código** e produz o doc de fluxo `.md` (prosa + `sequenceDiagram`). Este passo é *trace-driven*, não *template-driven*: você **segue a execução real**, não preenche campos. O template é o inimigo — ele convida à passada rasa; o rastreamento força a profundidade.

> **Este prompt encoda dois comportamentos** que no Claude seriam skills (`/grilling`, `/domain-modeling`) e que **aqui não existem** — então estão escritos abaixo, não invocados:
> 1. **Leitura forçada (grill):** abrir o corpo, seguir cada chamada até a folha, nunca aceitar "provavelmente faz X".
> 2. **Registro verbatim do domínio:** capturar o termo do domínio como ele aparece, sem parafrasear.

## Princípio-norte (inegociável)

> O mapa e o depoimento humano são **hipóteses** — nunca citados. A **única** fonte citável sobre o que o código FAZ é o próprio código, como **`arquivo:linha`**. Toda frase de comportamento no doc carrega `arquivo:linha`. Se você não abriu o corpo, você **não sabe** — está `[inferido]`.

## Jurisdição (modelo de verdade)

- **Fato-de-código** (o que o código faz) → **código manda**; cite `arquivo:linha`.
- **Porquê / restrição** → **humano manda**, e entra **atribuído** (verbatim + quem + quando), nunca como fato objetivo.
- **Verificação independe da fonte:** afirmação sobre o que o código faz — venha do mapa OU do humano — é checada contra o código antes de entrar. Humano diz "retorna string", código diz `int` → humano **refutado** com `arquivo:linha`.
- **Contradição = achado:** humano contradiz o código → não resolva no silêncio. Vira **divergência** registrada (**registra-e-segue**: o código vence o fato; a doc não trava; a divergência vira registro de primeira classe).

## Insumos

- `.arquitetura/contexto.md` (stack, estrutura, domínio elicitado).
- `.arquitetura/mapa/` (semente — para localizar entrypoints rápido).
- **O fluxo + entrypoint** que o humano te deu (ex.: `"autorização de pagamento" — POST /payments`). Derive um `slug` kebab-case (ex.: `autorizacao-de-pagamento`).

## O laço de rastreamento (o coração)

Comece no **entrypoint** do fluxo (localize pelo mapa; confirme abrindo o arquivo). A partir dele:

1. **Abra o corpo.** Leia a unidade inteira, não a assinatura. Cite onde o fluxo entra: `arquivo:linha`.
2. **Siga cada chamada que faz parte do fluxo INTO o alvo.** Não pare na chamada — abra o corpo do **callee** e continue. Cada salto vira uma **aresta** do **grafo rastreado**: `<caller> arquivo:linha → <callee> arquivo:linha`.
3. **Pare um ramo** só quando chegar a: (a) uma **fronteira externa** (rede/HTTP, banco, fila, filesystem, processo/container, relógio), (b) um **retorno** ao chamador, ou (c) uma chamada que você **decide** não seguir — e aí **marque `fora-de-escopo`** com motivo. `fora-de-escopo` é uma **decisão registrada**, não uma omissão.
4. **Promova as afirmações:** tudo que você confirmou abrindo o corpo vira **`[verificado: arquivo:linha]`**. O que continua fechado fica **`[inferido]`** — e `[inferido]` **não pode** virar frase de comportamento no doc; ou você abre, ou marca `fora-de-escopo`.
5. **Capture o domínio verbatim:** ao cruzar um termo do domínio (estado, evento, entidade, invariante), registre-o como aparece no código/comentário/depoimento. Não invente sinônimo.

> **Lazy:** siga só a fatia deste fluxo. Não mapeie o repo inteiro. Utilitário genérico fora do caminho do fluxo (logging, mapper trivial) → `fora-de-escopo`, com motivo curto.

## Interrogatório do 20% difícil (por nó — o que a passada rasa pula)

O template preenche o happy path e cala o resto. Em **cada** nó do rastreamento, **pergunte ativamente** (e responda no doc, com `arquivo:linha`, ou marque N/A com motivo):

- **Error path** — o que acontece quando falha aqui? exceção, retorno de erro, status? pra onde vai?
- **Chamada externa** — este nó fala com rede/banco/fila/fs/processo? qual? (dependência externa = risco; muitas ficam escondidas atrás de uma interface.)
- **Transição de estado** — muda status de alguma entidade? de quê pra quê? sob qual guarda?
- **Idempotência** — chamar duas vezes causa efeito duplo? há lock/chave/guarda que protege?
- **Timeout / retry** — há prazo? re-tentativa? backoff? quem re-dispara?
- **Compensação** — se um passo depois falha, o que desfaz/estanca este? (drena, cancela, reverte?)

Esses seis são o gatilho de profundidade. Um nó com todos "N/A" é suspeito — provavelmente você não abriu fundo o bastante.

## Saídas

### 1 · Grafo rastreado → `.arquitetura/mapa/fluxos/<slug>.grafo.md`

Interno (é insumo do gate, não vai pro site). Liste **toda** aresta na ordem do rastreamento:

```md
# Grafo rastreado — <fluxo>
> Interno. Insumo do gate `grill-doc`. Frescor: <data-hora> · <hash>
> Entrypoint: `<arquivo:linha>`

| # | Caller (arquivo:linha) | Callee (arquivo:linha) | Papel do salto | Fronteira? | Estado da aresta |
|---|---|---|---|---|---|
| 1 | `<a:linha>` | `<b:linha>` | <o que este salto faz> | externa/interna | verificado / fora-de-escopo |
...
```

### 2 · Doc de fluxo → `docs/03-fluxos/<slug>.md`

Publicável. Frontmatter Docusaurus + prosa + `sequenceDiagram`. **Toda frase de comportamento carrega `arquivo:linha`.**

```md
---
sidebar_position: <n>
title: "Fluxo: <nome legível>"
description: "<uma linha>"
---

# Fluxo: <nome legível>

## Gatilho
<quem/o quê dispara> — entrypoint `arquivo:linha`.

## Happy path
<passo a passo seguindo o grafo, cada passo com `arquivo:linha`>

## Error paths
<um subtítulo por caminho de erro real encontrado, com `arquivo:linha`>

## Chamadas externas
<cada fronteira externa cruzada: qual, onde `arquivo:linha`, o que acontece se ela falhar/demorar>

## Transições de estado · idempotência · timeout/retry · compensação
<o que o interrogatório do 20% achou, com `arquivo:linha`; N/A explícito onde não se aplica>

## Divergências (achados)
<humano × código, atribuído + `arquivo:linha` do que o código realmente faz; ou "nenhuma">

## Diagrama
```mermaid
sequenceDiagram
  participant ...
  ...
```
```

**O `sequenceDiagram` é fiel ao grafo rastreado:** cada mensagem = uma aresta; error paths viram `alt`/`opt`. Nada de seta que não exista no grafo. (Subset seguro: só `sequenceDiagram`/`flowchart`, labels entre aspas, IDs alfanuméricos, sem `<>`/parênteses/HTML dentro de nó — o `grill-mermaid` confere.)

### 3 · Atualize o mapa

Promova os nós tocados para `verificado`/`corrigido`, e na tabela de cobertura do `_indice.md` marque este fluxo na coluna "Fluxos que cobriram" dos módulos que ele atravessou.

## Critério de conclusão (checável e exaustivo)

- `docs/03-fluxos/<slug>.md` e `.arquitetura/mapa/fluxos/<slug>.grafo.md` existem.
- **Toda** chamada que você seguiu é uma **aresta** no grafo, com caller→callee em `arquivo:linha`.
- **Toda** frase de comportamento no doc é `[verificado: arquivo:linha]` — **zero** `[inferido]` virou afirmação.
- **Toda** chamada não seguida está marcada `fora-de-escopo` com motivo (nem um salto some no silêncio).
- Em **cada** nó, os **6** do interrogatório foram respondidos ou marcados N/A com motivo.
- Divergências humano×código registradas como achados (ou "nenhuma").
- O `sequenceDiagram` não tem nenhuma seta fora do grafo rastreado.

## Handoff

Imprima ao humano, literalmente:

> Doc gravado em `docs/03-fluxos/<slug>.md` e grafo em `.arquitetura/mapa/fluxos/<slug>.grafo.md`. Próximo passo: rode **`grill-doc`** apontando para esses dois arquivos.
