---
description: 'Você audita a síntese, a cadeia de confiança e a honestidade de cobertura.'
agent: 'agent'
---

# Prompt · `grill-visao`

> Gate da visão de produto. Portável (Amazon Q / Copilot / Kiro), **standalone**,
> sem subagente e sem parser. Roda depois de `documentar-visao`.

Você audita a síntese, a cadeia de confiança e a honestidade de cobertura. Não reescreve
a visão. Grava `.arquitetura/gates/grill-visao.md`.

## Pré-condições

- Grill `.arquitetura/grills/visao.md`, visão, contexto-produto, `_indice.md`, docs nela
  ligados e respectivos gates existem.
- Se não houver fluxo de negócio aprovado, resultado `BLOQUEADO-PRECONDICAO`.
- Se o mapa ou um doc mudou desde a geração, resultado `STALE`; recalcule antes de auditar.

## Gate 0 · Identidade e cadeia — BLOQUEANTE

Para cada `PERG-VISAO-###` e `VISAO-###`, confira base e estado. Toda pergunta precisa
nomear sinais cross-flow reais, declarar jurisdição/impacto/critério e apontar o gatilho.
Pergunta que apenas repete uma lente recebe `PERGUNTA-GENERICA`; sem base,
`PERGUNTA-SEM-GATILHO`; jurisdição `artefato-aprovado` aberta,
`PERGUNTA-ARTEFATO-ABERTA`. Pendência humana só passa se limitar a síntese visivelmente.

Todo fluxo linkado precisa de:

- doc existente e link relativo resolvível;
- `grill-negocio.<slug>.md` aprovado;
- mesmo `FLUXO/ENTRY/snapshot` dos artefatos técnicos;
- linha de Trace apontando fonte real.

Falhas: `SEM-ANCORA`, `GATE-AUSENTE`, `LINK-QUEBRADO`, `HASH-DIVERGENTE`.

## Gate 1 · Honestidade de síntese — BLOQUEANTE

- “O que é” está inferido-a-confirmar e sua base lista os fluxos usados.
- Persona/job/regra preserva ID e estado do contexto-produto.
- Fronteira compartilhada é comprovada por pelo menos dois ledgers; sem isso, é
  `GENERALIZACAO-INDEVIDA`.
- Nenhuma narrativa liga fluxos sem contrato/aresta que prove a relação.
- Inferências, limitações e decisões humanas estão visíveis.

Falhas: `FICCAO`, `INFERENCIA-PROMOVIDA`, `CROSS-FLOW-INVENTADO`,
`GENERALIZACAO-INDEVIDA`, `LACUNA-OCULTA`.

## Gate 2 · Mapa e cobertura — BLOQUEANTE

Recalcule a partir dos arquivos, sem confiar nos números escritos:

- `N` = docs com gate de negócio aprovado;
- `E` = entrypoints concretos `ENTRY-###`; `ENTRY-DINAMICO-###` fica fora do denominador
  e aparece nas limitações porque sua cardinalidade é desconhecida;
- `C` = `ENTRY-###` associados a ao menos um dos `N` fluxos aprovados.

Confirme também:

- cada one-liner é byte a byte igual ao `## Em uma frase` de origem;
- entrypoints em revisão/não cobertos aparecem na fila correta;
- nenhum módulo, doc ou entrypoint foi contado como se fosse “fluxo total”.

Falhas: `ONE-LINER-DRIFT`, `COBERTURA-FALSA`, `UNIDADE-MISTURADA`,
`ENTRYPOINT-SEM-MAPEAMENTO`.

## Gate 3 · Domínio e linguagem — BLOQUEANTE

- Zero código/jargão cru fora do Trace e de pares aprovados no Vocabulário.
- Termos preservam o glossário; `ARC/CON` não viram benefício sem fonte.
- “Visão completa/app inteiro” não aparece quando `C/E`, limitações ou lacunas mostram
  cobertura parcial.

Falhas: `JARGAO`, `DRIFT-DE-DOMINIO`, `COMPROMISSO-TRAIDO`, `COMPLETUDE-FINGIDA`.

## Gate 4 · Legibilidade — CONSULTIVO

Marque `ok/fraco/N/A`: síntese; personas/jobs; vocabulário/regras; mapa de fluxos;
fronteiras/riscos; cobertura/fila; decisões/lacunas; voz ativa e clareza.

## Veredito persistente

```md
# grill-visao — visao-de-produto
> Auditada em <data-hora> contra mapa <snapshot/frescor>

## Gate 0 · Cadeia: PASSA/REPROVA
PERGUNTA-GENERICA: <n> · PERGUNTA-SEM-GATILHO: <n> · PERGUNTA-ARTEFATO-ABERTA: <n>
## Gate 1 · Síntese: PASSA/REPROVA
## Gate 2 · Mapa/cobertura: PASSA/REPROVA
- Recalculado: N=<n> · C/E=<c>/<e> · limitações=<lista>
## Gate 3 · Domínio/linguagem: PASSA/REPROVA
<violações com VISAO-ID, fonte e correção>
## Gate 4 · Legibilidade consultiva
<checklist>
## Inferências, decisões e lacunas humanas
<fila com dono/impacto>
## Resultado: APROVADO / BLOQUEADO / STALE / BLOQUEADO-PRECONDICAO
## Correções necessárias
<lista exata por ID>
```

## Critério de conclusão

- Todo `PERG-VISAO-###`, `VISAO-###`, link, one-liner, gate de origem e estado foi conferido.
- O grill não contém pergunta genérica/sem gatilho nem pergunta de artefato aberta.
- `N` e `C/E` foram recalculados; dinâmicos e limitações ficaram fora do denominador.
- Toda síntese, generalização e relação cross-flow foi classificada.
- O arquivo persistente existe e o resultado respeita os gates bloqueantes/frescor.

## Handoff

- **APROVADO:** `grill-visao aprovado e gravado em .arquitetura/gates/grill-visao.md. A visão está apta à revisão humana/publicação dentro da cobertura declarada.`
- **BLOQUEADO:** `Volte ao documentar-visao e corrija a lista por VISAO-ID.`
- **STALE/PRECONDICAO:** `Atualize mapa/docs/gates de origem antes de regenerar e auditar a visão.`
