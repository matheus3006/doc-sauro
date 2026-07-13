---
description: 'Você escreve a porta de entrada do domínio sem fingir completude.'
agent: 'agent'
---

# Prompt · `documentar-visao`

> Síntese progressiva do track de negócio. Portável (Amazon Q / Copilot / Kiro),
> **standalone**, sem subagente e sem parser. Roda depois de pelo menos um
> `grill-negocio` aprovado e re-roda à medida que a cobertura cresce.

Você escreve a porta de entrada do domínio sem fingir completude. A visão liga somente
fluxos de negócio aprovados, sintetiza o domínio observado com marcação de incerteza e
mostra cobertura em duas medidas que não se confundem: quantidade de docs e entrypoints
cobertos.

## Contrato de execução

- Insumos: contexto, contexto-produto, `_indice.md`, docs de negócio e seus
  `grill-negocio.<slug>.md` aprovados.
- Um doc sem gate aprovado não entra como fluxo documentado; aparece em “em revisão”.
- Pode escrever `.arquitetura/grills/visao.md` e
  `docs/00-dominio/visao-de-produto.md`.
- Não cria narrativa entre fluxos, não inventa jornada, não reescreve one-liner aprovado
  e não chama inventário de entrypoints de “total de fluxos do produto”.
- Se não houver nenhum fluxo de negócio aprovado, pare `BLOQUEADO`.

## Modelo de verdade

- O one-liner de cada fluxo é cópia exata do `## Em uma frase` do doc aprovado.
- A síntese do produto é `[inferido do código · a confirmar]`, baseada no propósito
  atribuído + conjunto explicitamente listado de fluxos aprovados.
- Personas, jobs, termos e regras preservam IDs e estados do contexto-produto.
- Toda afirmação recebe `VISAO-###` no Trace.
- `ARC/CON` continuam vigentes; a visão não vende restrição como benefício sem fonte.

## Cobertura sem falsa precisão

Calcule e publique separadamente:

1. **Docs aprovados `N`:** quantidade de `FLUXO-<slug>` com gate de negócio aprovado.
2. **Entrypoints cobertos `C/E`:** `E` = entrypoints concretos `ENTRY-###` do inventário;
   `C` = entrypoints associados a pelo menos um desses fluxos aprovados.
3. **Limitações:** `ENTRY-DINAMICO-###` não entra em `E`, pois representa cardinalidade
   desconhecida. Liste-o, além de duplicidades, relações muitos-para-muitos e áreas que
   o inventário admite não enxergar.

Nunca escreva “N de M fluxos” usando `M` de módulos ou entrypoints. Um doc pode cobrir
vários entrypoints e um entrypoint pode iniciar mais de um fluxo.

## Fase 1 · Gere o grill sistêmico específico deste projeto

Use `síntese`, `personas/jobs`, `fronteiras compartilhadas`, `compromissos`, `cobertura`
e `lacunas` como **lentes**, não como perguntas prontas.

### 1.1 · Encontre gatilhos cross-flow reais

Cruze os `FLUXO/ENTRY`, one-liners, `PER/JOB/TERMO/REGRA`, `ARC/CON`, fronteiras e
pendências dos grills de negócio. Gatilhos típicos:

- dois fluxos usam o mesmo termo com resultados ou regras diferentes;
- a mesma `FRONTEIRA` aparece em vários ledgers com ownership/falha divergente;
- persona/job existe no contexto, mas nenhum fluxo aprovado a representa;
- um `ARC/CON` afeta vários fluxos de formas diferentes;
- a síntese proposta depende de uma conexão que nenhum artefato prova;
- `ENTRY-###` descoberto torna uma afirmação de completude enganosa.

### 1.2 · Gere `PERG-VISAO-###`

Cada pergunta deve citar os fluxos, IDs, termos ou documentos concretos que a dispararam;
declarar jurisdição `artefato-aprovado` ou `humano`; explicar o efeito sobre síntese,
risco ou cobertura; e definir a prova/decisão que a encerra.

Não pergunte genericamente “o que é o produto?” ou “quem ficou fora?”. Pergunte, por
exemplo: “`JOB-004` pertence a `PER-002`, mas nenhum dos fluxos aprovados associados aos
`ENTRY-003/007` o cobre: ele está fora do produto observado ou falta priorizar um fluxo
de documentação?”. Só use IDs que existam no projeto.

Lente sem sinal fica `não acionada` com as fontes inspecionadas. Ausência só gera pergunta
quando muda materialmente a honestidade da visão.

### 1.3 · Resolva em loop

1. Resolva o que os artefatos aprovados conseguem provar.
2. Gere follow-ups quando a comparação revelar contradição ou nova lacuna.
3. Pergunte ao humano apenas sobre significado, prioridade, risco aceito ou autoridade,
   sempre com os casos concretos já comparados. Persista a fila, espere e registre a
   resposta antes de sintetizar.
4. Pergunta de artefato aberta bloqueia a visão; pergunta humana pode permanecer
   `aguardando-humano` se a síntese declarar a limitação.
5. Síntese não é soma de one-liners e não cria causalidade entre fluxos.

### 1.4 · Grave o grill

Grave `.arquitetura/grills/visao.md`:

```md
# Grill sistêmico — visão de produto
> Mapa: <snapshot/frescor> · Gates de negócio: <lista>

## Cobertura das lentes
| Lente | Sinais concretos inspecionados | Estado | Perguntas |
|---|---|---|---|
| <lente> | <FLUXO/ENTRY/PER/JOB/FRONTEIRA/ARC/CON> | acionada / não acionada com evidência | `PERG-VISAO-###` / — |

## Perguntas específicas
| ID | Pergunta | Gatilho/base | Jurisdição | Por que importa | Critério de encerramento | Derivada de | Estado | Resposta/base |
|---|---|---|---|---|---|---|---|---|
| `PERG-VISAO-001` | <pergunta cross-flow concreta> | <IDs/docs> | artefato-aprovado/humano | <efeito> | <prova/decisão> | — | aberta / resolvida / aguardando-humano / descartada | <resposta> |
```

Preserve IDs em reexecuções; perguntas sobre novos fluxos são anexadas.

## Fase 2 · Linguagem

- Use o glossário e preserve IDs no Trace, não necessariamente na prosa.
- Voz ativa, ator nomeado, uma ideia por frase.
- Zero código na prosa. Pares técnico→produto só na seção Vocabulário, se já aprovados.
- One-liner é citado literalmente; discrepância deve ser resolvida no doc de origem.
- Se cobertura for parcial, diga “visão atual/observada”, nunca “o app inteiro”.

## Saída

```md
---
sidebar_position: 1
title: "Visão de Produto: <nome>"
description: "<síntese do domínio observado e público>"
---

# <nome> — visão de produto
> Visão progressiva do domínio. Base atual: <N> fluxos de negócio aprovados.

## O que é
<síntese [inferido do código · a confirmar] + indicação de base>

## Pra quem é
<personas/jobs e estado herdado; ausências relevantes>

## Vocabulário e regras essenciais
<termos/regras do contexto-produto usados nesta visão>

## Fluxos documentados
| Fluxo | O que faz pra você | EntryPoints cobertos | Doc |
|---|---|---|---|
| <nome> | <cópia exata de Em uma frase> | `ENTRY-###` | [ver fluxo](fluxos-negocio/<slug>.md) |

## Fronteiras e riscos compartilhados
<somente relações comprovadas pelos ledgers; ownership/pendências visíveis>

## Cobertura e fila de documentação
- Docs de negócio aprovados: **<N>**.
- EntryPoints candidatos cobertos: **<C>/<E>**.
- Em revisão: <docs sem gate aprovado>.
- Descobertos sem doc aprovado: <ENTRY-IDs + hipótese marcada>.
- Limitações do inventário: <lista>.

## Decisões e lacunas humanas
<`PERG-VISAO-###` / LACUNA / DECISAO-PENDENTE com dono e impacto>

## Trace
<details>
<summary>Trace — cada afirmação e sua base</summary>

| ID | Afirmação/seção | Tipo | Base | Estado |
|---|---|---|---|---|
| `VISAO-001` | <one-liner> | fluxo | `<doc>` §Em uma frase + `<gate>` | herdado-verificado |
| `VISAO-002` | <síntese> | síntese | <propósito + lista de fluxos> | inferido-a-confirmar |
| `VISAO-003` | cobertura C/E | cobertura | `_indice.md` + associações dos fluxos | calculado-verificado |

</details>
```

## Critério de conclusão

- Todo fluxo listado tem gate de negócio aprovado e link resolvível.
- `.arquitetura/grills/visao.md` existe e referencia exatamente os artefatos sintetizados.
- Toda `PERG-VISAO-###` nasce de sinais concretos, com jurisdição, impacto e critério;
  zero pergunta genérica copiada das lentes.
- Perguntas de artefato estão resolvidas; pendências humanas limitam a síntese de modo visível.
- As 6 lentes estão acionadas ou não acionadas com evidência.
- Todo one-liner é byte a byte igual ao doc de origem.
- `N` e `C/E` estão separados, recalculáveis e acompanhados das limitações.
- Síntese, personas, jobs, regras e lacunas preservam estado/base.
- Fronteiras compartilhadas só aparecem quando mais de um ledger as comprova.
- Zero código/narrativa cross-flow inventada na prosa.
- Todo conteúdo material tem `VISAO-###` no Trace.

## Handoff

> Grill sistêmico gravado em `.arquitetura/grills/visao.md` e visão gravada com <N> docs aprovados e cobertura <C>/<E>. Próximo passo: rode **`grill-visao`** com o grill, a visão, o índice, os docs e os gates de negócio.
