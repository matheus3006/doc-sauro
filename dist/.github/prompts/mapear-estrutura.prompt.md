---
description: 'Você semeia o mapa: um aid de leitura barato, nível-declaração, interno.'
agent: 'agent'
---

# Prompt · `mapear-estrutura`

> Passo 1 da trilha. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem parser/ctags/tree-sitter. Leitura **LLM-native**. Roda **uma vez por projeto**, depois de `bootstrap-contexto`.

Você semeia o **mapa**: um aid de leitura barato, **nível-declaração**, interno. O mapa é o **ledger** da trilha — a única memória entre sessões. Ele **cresce progressivo, logo à frente das docs**: aqui você só faz a **semente L0-L1 + cobertura**; as camadas fundas enchem **lazy**, quando um fluxo passar por elas (isso é trabalho do `documentar-fluxo`, não seu).

## Princípio-norte (inegociável)

> O mapa é **hipótese**. **NUNCA é citado numa doc.** A única fonte citável sobre comportamento do código é o próprio código (`arquivo:linha`). O mapa acelera a leitura; ele não prova nada.

## Regras duras

- **Nunca abra corpo de método.** O mapa é nível-declaração: nomes de pasta/arquivo/classe/método + assinaturas visíveis + papel **inferido**. O corpo é lazy, via `documentar-fluxo`.
- **Toda inferência carrega `[inferido]`.** Papel deduzido de nome/tipo/assinatura (ex.: `*Controller` = entrypoint HTTP) é hipótese marcada — não fato.
- **Interno.** Grave em `.arquitetura/mapa/` — **fora de `docs/`**. Não vaza pro site.
- Vocabulário **language-agnostic**: `entrypoint` · `módulo` (pasta/pacote top-level) · `unidade` (classe/arquivo) · `aresta-de-dependência` (uma unidade referencia outra).

## Status de um nó (o ledger)

`esqueleto` (só o nome existe) → `inferido` (papel/aresta deduzido de assinatura) → `verificado` \| `corrigido` (só o `documentar-fluxo` promove, lendo o corpo) · `stale` (o arquivo mudou depois do carimbo de frescor).

## Passos

### 1 · Semente L0-L1 + cobertura

Leia `.arquitetura/contexto.md`. A partir da raiz do código que ele aponta:

1. Monte a árvore **L0** (repo) → **L1** (módulos top-level e um nível de submódulo). Não desça a arquivos ainda.
2. Para **cada** módulo top-level, deduza os tipos de `entrypoint` que ele expõe (por convenção de nome/pasta), marcando `[inferido]`.
3. Escreva a **tabela de cobertura** — uma linha por módulo top-level: `módulo | entrypoints (inferidos) | status | fluxos que já o cobriram | frescor`. No começo todo módulo é `esqueleto` e "fluxos" está vazio.

**Concluído quando:** `_indice.md` tem a árvore L0-L1 e a tabela de cobertura com **uma linha por módulo top-level**.

### 2 · Stubs por módulo — **lazy, no primeiro toque** (não eager)

A semente **não** enumera as unidades dos 14 módulos de uma vez — isso seria "mapear o repo inteiro", o oposto de barato. O stub de um módulo nasce **quando o primeiro fluxo o toca** (o `documentar-fluxo` cria/estende ao promover unidades). Aqui você só pode **adiantar** o stub de um módulo se ele for o alvo óbvio do próximo passo.

Um stub `.arquitetura/mapa/<módulo>.md`, quando criado, tem:

- as **unidades** visíveis (classes/arquivos — L2), status `esqueleto`;
- onde o **papel** for barato de inferir do nome/tipo (`*Controller`, `*Service`, `*Repository`, `*Listener`, `*Config`…), anotado com `[inferido]`;
- a nota: *"assinaturas (L3) e arestas (L4) enchem **lazy** quando um fluxo passar por aqui."*

Nunca liste membros/assinaturas de tudo. Liste só o que enxerga sem esforço; o resto é lazy.

**Concluído quando:** o módulo alvo do próximo passo tem stub (os demais nascem no toque); toda unidade listada tem status e todo papel/aresta inferido carrega `[inferido]`.

### 3 · Carimbo de frescor

Em cada arquivo do mapa, registre `Frescor: <data-hora> · <commit/hash se houver>`. É o que permite marcar `stale` depois.

## Forma dos arquivos

`_indice.md`:
```md
# Mapa — índice (L0-L1)
> Interno. Ledger da trilha. NUNCA citado numa doc. Frescor: <data-hora> · <hash>

## Árvore
- <repo>
  - `<módulo>/`
    - `<submódulo>/`
    ...

## Cobertura
| Módulo | Entrypoints (inferidos) | Status | Fluxos que cobriram | Frescor |
|---|---|---|---|---|
| `<módulo>` | <tipos> `[inferido]` | esqueleto | — | <hash> |
```

`<módulo>.md`:
```md
# Mapa — módulo `<módulo>`
> Nível-declaração. Assinaturas e arestas enchem lazy por-fluxo. Frescor: <data-hora> · <hash>

## Unidades
- `<Unidade>` — papel: <inferido> `[inferido]` — status: esqueleto
  ...
```

## Critério de conclusão (checável)

- `.arquitetura/mapa/_indice.md` existe, com árvore L0-L1 **e** tabela de cobertura cobrindo **todos** os módulos top-level.
- O módulo alvo do próximo passo tem stub; os demais nascem lazy no primeiro toque.
- **Todo** papel/aresta inferido carrega `[inferido]`.
- **Nenhum** corpo de método foi aberto; **nenhuma** afirmação de comportamento como fato.
- Todo arquivo do mapa tem carimbo de frescor.

## Handoff

Imprima ao humano, literalmente:

> Mapa semeado em `.arquitetura/mapa/`. Próximo passo: rode **`documentar-fluxo`** informando **um** fluxo crítico e seu entrypoint (ex.: `"autorização de pagamento" — POST /payments`).
