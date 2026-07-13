---
inclusion: manual
---

# Prompt · `documentar-negocio`

> A joia do track de negócio. Portável (Amazon Q / Copilot / Kiro), **standalone**,
> sem subagente e sem parser. Roda uma vez por fluxo tecnicamente aprovado.

Você traduz um fluxo técnico para linguagem de negócio. Não é resumo livre: cada
afirmação recebe `NEG-###` e aponta uma base aprovada. O texto explica o resultado para
uma PO nova, sem expor implementação e sem inventar valor ou causalidade.

## Contrato de execução

- Insumos: contexto, contexto-produto, doc/ledger do fluxo e seus dois gates técnicos
  aprovados no mesmo snapshot.
- Pode escrever `.arquitetura/grills/negocio.<slug>.md` e
  `docs/00-dominio/fluxos-negocio/<slug>.md`.
- Não pode reabrir código para reinterpretar negócio, alterar o fluxo, criar conexão com
  outro fluxo ou promover inferência a decisão.
- Slug/`FLUXO`/`ENTRY` devem coincidir. Falha de gate, snapshot ou identidade → `BLOQUEADO`.

## Modelo de verdade

- **O QUÊ:** herdado do doc técnico aprovado; Trace aponta `PASSO/BRANCH/FRONTEIRA`.
- **O PORQUÊ:** `REGRA-###`/humano atribuído ou `[inferido do código · a confirmar]`
  com base. Código não prova valor por si só.
- **Linguagem:** usa apenas `PER/JOB/TERMO` do contexto-produto. Termo necessário mas
  ausente vira `LACUNA`, não sinônimo improvisado.
- **Compromissos:** preserve `ARC/CON`; sugestão incompatível vira decisão pendente.
- **Zero código na prosa:** nomes técnicos e `arquivo:linha` só podem aparecer no Trace.

## Fase 1 · Gere o grill de negócio específico deste fluxo

Use `job`, `resultado percebido`, `erro/impacto`, `regra`, `porquê/trade-off` e `limite`
como **lentes**, nunca como perguntas prontas.

### 1.1 · Encontre gatilhos reais

Cruze `PASSO/BRANCH/FRONTEIRA` com `PER/JOB/TERMO/REGRA`, `ARC/CON`, inferências e
lacunas do contexto-produto. Procure, por exemplo:

- efeito técnico sem resultado perceptível associado a uma persona concreta;
- branch de erro cujo impacto para `PER-###` não foi explicado;
- condição técnica apresentada como `REGRA-###` sem dono ou porquê;
- duas personas afetadas de formas diferentes pelo mesmo resultado;
- fronteira externa cujo fracasso ameaça um job/restrição específica;
- ponto em que a narrativa tenta atravessar o limite de `FLUXO-<slug>`.

### 1.2 · Gere `PERG-NEG-###`

Cada pergunta deve nomear IDs/termos deste projeto, apontar o artefato que a disparou,
declarar jurisdição `artefato-aprovado` ou `humano`, explicar o impacto e definir o que a
encerra. Pergunta filha registra `derivada-de`.

É proibido perguntar genericamente “qual o job?”, “quem sente?” ou “por que foi feito
assim?”. Uma pergunta válida seria da forma: “Quando `BRANCH-004` leva o pedido de
`PER-002` para revisão, `REGRA-003` exige esse bloqueio por risco financeiro ou por
compliance? Quem ratifica esse porquê?”. Os IDs/termos usados devem existir no projeto.

Lente sem gatilho após inspeção fica `não acionada` com os IDs examinados. Não gere
pergunta para preencher tabela e não use `N/A` como atalho.

### 1.3 · Resolva em loop

1. Responda primeiro usando apenas artefatos aprovados; não reabra código nem extrapole.
2. Resposta que revela ambiguidade cria `PERG-NEG-###` filha.
3. Apresente ao humano somente perguntas materiais que dependem de valor, regra,
   significado ou autoridade, já acompanhadas da base e do impacto. Persista a fila e espere.
4. Registre resposta verbatim no grill ou `aguardando-humano` com dono/impacto antes de continuar.
5. Pergunta de jurisdição dos artefatos ainda aberta bloqueia a tradução; pendência
   humana pode seguir marcada e visível.

### 1.4 · Grave o grill

Grave `.arquitetura/grills/negocio.<slug>.md`:

```md
# Grill de negócio — `FLUXO-<slug>`
> Snapshot técnico: <snapshot> · Contexto-produto: <frescor>

## Cobertura das lentes
| Lente | Sinais concretos inspecionados | Estado | Perguntas |
|---|---|---|---|
| <lente> | <IDs/termos/artefatos> | acionada / não acionada com evidência | `PERG-NEG-###` / — |

## Perguntas específicas
| ID | Pergunta | Gatilho/base | Jurisdição | Por que importa | Critério de encerramento | Derivada de | Estado | Resposta/base |
|---|---|---|---|---|---|---|---|---|
| `PERG-NEG-001` | <pergunta com IDs/termos reais> | <base aprovada> | artefato-aprovado/humano | <impacto> | <prova/decisão> | — | aberta / resolvida / aguardando-humano / descartada | <resposta> |
```

Preserve IDs em reexecuções e acrescente novas perguntas no fim.

## Fase 2 · Linguística

- Voz ativa, ator nomeado e uma ideia por frase.
- POV da persona: “a pessoa vê a solicitação em análise”, não “o controller responde”.
- Traduza efeitos, não apenas palavras: idempotência vira o resultado “não duplica”.
- Um exemplo concreto rotulado `Exemplo:`. Valores podem ser ilustrativos, mas persona,
  sequência, branches e desfechos devem existir no fluxo.
- Não suavize falhas. Incerteza explícita é melhor que uma jornada idealizada.

## Saída

```md
---
sidebar_position: <n>
title: "Negócio: <nome>"
description: "<job/resultado em uma linha>"
---

# <nome> — para o negócio
> Companheiro do fluxo técnico: [<slug>](../../03-fluxos/<slug>.md).
> Escopo: `FLUXO-<slug>` · EntryPoints cobertos: <ENTRY-IDs>.

## Em uma frase
<job que o fluxo resolve>

## Quem usa e qual resultado busca
<PER/JOB em linguagem natural, preservando o estado atribuído/inferido>

## Como funciona
<happy path + Exemplo:, cada afirmação comportamental associada a NEG-### no Trace>

## Quando dá errado
<branches, efeito percebido, recuperação/ação humana e limites>

## Regras, porquês e trade-offs
<REGRA/CON/ARC; todo porquê atribuído, inferido-a-confirmar ou pendente>

## Limites e lacunas
<fora de escopo, `PERG-NEG-###` humanas pendentes e DECISAO-PENDENTE>

## Trace
<details>
<summary>Trace — cada afirmação e sua base</summary>

| ID | Afirmação/seção | Tipo | Base | Estado |
|---|---|---|---|---|
| `NEG-001` | <afirmação> | o quê / regra / porquê | `PASSO-###` / `BRANCH-###` / `FRONTEIRA-###` / `REGRA-###` / fonte humana | herdado-verificado / atribuído / inferido-a-confirmar / pendente |

</details>
```

## Critério de conclusão

- Insumos técnicos estão aprovados e no mesmo snapshot.
- `.arquitetura/grills/negocio.<slug>.md` existe e usa os mesmos artefatos da tradução.
- Toda `PERG-NEG-###` cita gatilho real, jurisdição, impacto e critério de encerramento;
  zero pergunta genérica copiada das lentes.
- Perguntas de artefato estão resolvidas; humanas pendentes aparecem no doc.
- As 6 lentes estão acionadas ou não acionadas com evidência.
- Toda frase comportamental tem `NEG-###` no Trace, base existente e equivalência de
  significado com o técnico.
- Todo porquê/trade-off tem estado e base; nenhuma decisão foi inventada.
- Exemplo cobre somente caminhos reais.
- Termos vêm do glossário; código não vazou para a prosa.
- Limites e lacunas estão explícitos.

## Handoff

> Grill específico gravado em `.arquitetura/grills/negocio.<slug>.md` e doc de negócio em `docs/00-dominio/fluxos-negocio/<slug>.md`, com <n> pendências humanas. Próximo passo: rode **`grill-negocio`** apontando para o grill, o doc e os artefatos técnicos do mesmo fluxo.
