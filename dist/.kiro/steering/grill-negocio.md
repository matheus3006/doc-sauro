---
inclusion: manual
---

# Prompt · `grill-negocio`

> Gate do track de negócio. Portável (Amazon Q / Copilot / Kiro), **standalone**,
> sem subagente e sem parser. Roda depois de `documentar-negocio`.

Você audita tradução, domínio e honestidade. Não reescreve o doc. Grava
`.arquitetura/gates/grill-negocio.<slug>.md` para que a visão de produto possa depender
de um resultado persistente.

## Pré-condições

- Grill `.arquitetura/grills/negocio.<slug>.md`, doc de negócio, contexto-produto,
  doc/ledger técnico e os dois gates técnicos existem.
- Slug, `FLUXO`, `ENTRY` e snapshot coincidem.
- Gate técnico reprovado/stale → `BLOQUEADO-PRECONDICAO`.

## Gate 0 · Identidade e cadeia de confiança — BLOQUEANTE

Confirme a cadeia `PERG-NEG → NEG → PASSO/BRANCH/FRONTEIRA ou REGRA/humano → artefato
aprovado`. Cada base deve existir e dizer o que o Trace afirma. Base por nome parecido
não vale.

Toda `PERG-NEG-###` precisa nomear IDs/termos do projeto, ter gatilho, jurisdição,
impacto e critério. Pergunta que copia uma lente recebe `PERGUNTA-GENERICA`; sem base,
`PERGUNTA-SEM-GATILHO`; jurisdição `artefato-aprovado` ainda aberta,
`PERGUNTA-ARTEFATO-ABERTA`. Pendência humana passa apenas se estiver visível no doc.

Falhas: `ID-INEXISTENTE`, `HASH-DIVERGENTE`, `BASE-NAO-SUSTENTA`, `SEM-ANCORA`.

## Gate 1 · Honestidade de produto — BLOQUEANTE

- Todo comportamento tem `NEG-###` e base técnica semanticamente equivalente.
- Todo porquê/trade-off é atribuído, inferido-com-base ou pendente.
- Inferência não aparece em outro trecho como fato confirmado.
- Limites/falhas não foram suavizados nem omitidos para melhorar a narrativa.

Falhas: `FICCAO`, `INFERENCIA-PROMOVIDA`, `RISCO-OCULTO`, `LIMITE-APAGADO`.
Liste inferências e pendências em fila própria; ser pendência não reprova, escondê-la sim.

## Gate 2 · Coerência de domínio — BLOQUEANTE

- Personas/jobs/termos/regras existem no contexto-produto e preservam significado/estado.
- Termo ambíguo respeita o contexto delimitado.
- `ARC/CON` relevante não foi contradito nem transformado em benefício inventado.

Falhas: `TERMO-FORA-DO-MODELO`, `DRIFT-DE-DOMINIO`, `REGRA-INVENTADA`,
`COMPROMISSO-TRAIDO`.

## Gate 3 · Linguagem e exemplo — BLOQUEANTE

- Fora do Trace, zero classe, método, arquivo, `arquivo:linha` ou jargão técnico cru.
- Exemplo usa persona, sequência, branch e desfecho presentes no fluxo.
- Resultado é narrado do ponto de vista humano; mecanismo não se disfarça de valor.

Falhas: `JARGAO`, `EXEMPLO-INFIEL`, `MECANISMO-COMO-VALOR`.

## Gate 4 · Legibilidade — CONSULTIVO

Marque `ok/fraco/N/A`: Em uma frase; persona/job; happy path com exemplo; falhas e
recuperação; regras/porquês; limites/lacunas; voz ativa e consistência de vocabulário.

## Veredito persistente

```md
# grill-negocio — <slug>
> Snapshot <commit:hash|manifest:digest> · auditado em <data-hora>

## Gate 0 · Identidade/cadeia: PASSA/REPROVA
PERGUNTA-GENERICA: <n> · PERGUNTA-SEM-GATILHO: <n> · PERGUNTA-ARTEFATO-ABERTA: <n>
## Gate 1 · Honestidade: PASSA/REPROVA
## Gate 2 · Domínio: PASSA/REPROVA
## Gate 3 · Linguagem/exemplo: PASSA/REPROVA
<cada violação: código, NEG-ID, frase, base, correção esperada>
## Gate 4 · Legibilidade consultiva
<checklist>
## Inferências e pendências humanas
<lista com dono/impacto>
## Resultado: APROVADO / BLOQUEADO / BLOQUEADO-PRECONDICAO
## Correções necessárias
<lista exata por ID>
```

Ao aprovar, associe este gate à relação `FLUXO-<slug> ↔ ENTRY-###`. Não marque o
entrypoint inteiro como “negócio aprovado”: ele pode iniciar outros fluxos não auditados.

## Critério de conclusão

- Todo `PERG-NEG-###`, `NEG-###`, porquê, termo, regra e exemplo foi classificado contra
  uma base real.
- O grill não contém pergunta genérica/sem gatilho nem pergunta de artefato aberta.
- Inferências e pendências humanas estão listadas com impacto/dono quando conhecido.
- O arquivo de gate existe no snapshot auditado e o resultado respeita os gates bloqueantes.
- A associação fluxo↔entrypoint só recebeu o gate se o resultado foi aprovado.

## Handoff

- **APROVADO:** `grill-negocio aprovado e gravado em .arquitetura/gates/grill-negocio.<slug>.md. O fluxo está apto a compor a visão de produto.`
- **BLOQUEADO:** `Volte ao documentar-negocio e corrija a lista por NEG-ID.`
- **BLOQUEADO-PRECONDICAO:** `Recupere a aprovação/frescor técnico antes de auditar negócio.`
