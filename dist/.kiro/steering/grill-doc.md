---
inclusion: manual
---

# Prompt · `grill-doc`

> Gate técnico. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente
> e sem parser. Roda depois de `documentar-fluxo`.

Você audita um doc contra seu ledger **e contra o código citado**. Não reescreve o doc,
não corrige código e não flexibiliza compromisso: grava um veredito persistente com a
lista exata de correções.

## Contrato e saída

- Insumos: `docs/03-fluxos/<slug>.md`, `.arquitetura/grills/tecnico.<slug>.md`,
  `.arquitetura/mapa/fluxos/<slug>.grafo.md`, `.arquitetura/contexto.md` e o código.
- Saída obrigatória: `.arquitetura/gates/grill-doc.<slug>.md`.
- Se algum insumo falta, IDs/slug divergem ou o código não corresponde ao snapshot sem
  nova leitura, resultado `BLOQUEADO-PRECONDICAO`. Não audite por memória.
- Quando aprovado, anexe o gate à associação `FLUXO-<slug> ↔ ENTRY-###` no mapa. Não
  marque o entrypoint inteiro como aprovado: ele pode iniciar outros fluxos ainda crus.

## Gate 0 · Identidade, escopo e frescor — BLOQUEANTE

- `FLUXO-<slug>`, `ENTRY-###`, doc e ledger referem o mesmo fluxo?
- Grill, ledger e doc usam o mesmo snapshot?
- O snapshot permite abrir exatamente o conteúdo citado? Commit só vale com árvore limpa.
  Em árvore alterada/sem VCS, recalcule todos os fingerprints; ausência ou divergência
  torna o artefato `stale` até novo trace.
- Precondições, pós-condições, dentro/fora do escopo estão explícitos?
- `DECISAO-PENDENTE-###` não foi tratada como decisão ratificada?
- Cada `PERG-TEC-###` nomeia sinal concreto deste projeto, aponta gatilho, jurisdição,
  impacto e critério de encerramento? Pergunta que apenas repete uma lente recebe
  `PERGUNTA-GENERICA`; pergunta sem base recebe `PERGUNTA-SEM-GATILHO`.
- Toda pergunta de jurisdição `código` está resolvida com evidência? Aberta recebe
  `PERGUNTA-CODIGO-ABERTA`. Pendência humana só passa se estiver visível no doc.

Cada falha recebe `CONTRATO-INVALIDO` ou `STALE` e reprova.

## Gate 1 · Completude estrutural por ID — BLOQUEANTE

Classifique **todos** os IDs do ledger:

- `PASSO-###`: aparece na prosa com mesmo significado e evidência.
- `ARESTA-###`: está narrada/coberta ou explicitamente fora de escopo.
- `BRANCH-###`: os dois resultados estão descritos, inclusive erro/retorno.
- `FRONTEIRA-###`: dependência, direção, contrato e comportamento de falha aparecem.

Sem representação → `AUSENTE`. ID citado com outro significado → `DRIFT-SEMANTICO`.

```md
| ID | Tipo | Classe | Onde no doc | Observação |
|---|---|---|---|---|
| `PASSO-001` | passo | coberto/AUSENTE/DRIFT-SEMANTICO | <seção> | <motivo> |
```

## Gate 2 · Evidência e jurisdição — BLOQUEANTE

Varra a prosa frase a frase e **abra o código citado**:

- citação ausente → `SEM-CITACAO`;
- arquivo/linha inexistente ou stale → `CITACAO-INVALIDA`;
- linha existe, mas não sustenta verbo, condição ou resultado → `CITACAO-NAO-SUSTENTA`;
- mapa/depoimento usado como fato de código → `FONTE-ERRADA`;
- porquê/restrição humana sem atribuição → `SEM-ATRIBUICAO`.

Presença de `arquivo:linha` não basta. O gate valida suporte semântico e usa o menor
trecho necessário.

## Gate 3 · Visão sistêmica — BLOQUEANTE POR OMISSÃO

Para cada `FRONTEIRA-###`, confirme que o doc declara:

- upstream/downstream e contrato;
- falha/propagação, timeout/retry e recuperação;
- ownership/observabilidade conhecidos **ou** `[PENDENTE]` explícito;
- segurança/dados/compliance e `CON-###` aplicáveis **ou** `N/A` motivado.

Pendência honesta não reprova. Omissão silenciosa recebe `RISCO-OCULTO` e reprova.
Confirme também que nenhum `ARC-###` foi contradito sem decisão pendente.

## Gate 4 · Rubrica arquitetural — CONSULTIVA

Marque `presente`, `fraco`, `N/A (motivo)`:

- contrato/escopo; happy path; branches/error paths; fronteiras;
- estado/consistência; idempotência/concorrência; timeout/retry;
- compensação/recuperação; observabilidade/ownership; segurança/compliance;
- divergências/decisões pendentes.

Todo `fraco` vira recomendação; não muda sozinho os gates bloqueantes.

## Veredito persistente

Grave:

```md
# grill-doc — <slug>
> Auditou snapshot <commit:hash|manifest:digest> em <data-hora>

## Gate 0 · Contrato/frescor: PASSA / REPROVA
PERGUNTA-GENERICA: <n> · PERGUNTA-SEM-GATILHO: <n> · PERGUNTA-CODIGO-ABERTA: <n>
## Gate 1 · Completude por ID: PASSA / REPROVA
<tabela completa> — AUSENTE: <n> · DRIFT-SEMANTICO: <n>
## Gate 2 · Evidência/jurisdição: PASSA / REPROVA
<violações com seção, frase, citação e correção esperada>
## Gate 3 · Visão sistêmica: PASSA / REPROVA
RISCO-OCULTO: <n> · pendências explícitas: <lista>
## Gate 4 · Rubrica consultiva
<checklist e recomendações>
## Resultado: APROVADO / BLOQUEADO
## Correções necessárias
<lista exata ordenada por ID>
```

`APROVADO` exige Gates 0–3 passando. Um veredito anterior nunca substitui a auditoria
do snapshot atual.

## Critério de conclusão

- Todo ID, toda `PERG-TEC-###` e toda frase comportamental foram classificados.
- O grill não contém perguntas genéricas/sem gatilho nem pergunta de código aberta.
- Todas as citações foram abertas e validadas semanticamente.
- Todas as fronteiras foram auditadas; desconhecido está explícito, não oculto.
- O arquivo de gate existe e o resultado é coerente.
- A associação fluxo↔entrypoint recebeu o gate somente se aprovado.

## Handoff

- **APROVADO:** `grill-doc aprovado e gravado em .arquitetura/gates/grill-doc.<slug>.md. Próximo passo: rode grill-mermaid.`
- **BLOQUEADO:** `grill-doc bloqueado. Volte ao documentar-fluxo e corrija a lista por ID; depois rode este gate novamente.`
