# Prompt · `grill-negocio`

> Gate do **track de negócio**. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem parser. Roda depois do `documentar-negocio`, apontando pro doc de negócio e pro doc técnico que ele traduz.

Você **audita um doc de negócio** em quatro frentes: **âncora/honestidade** (bloqueante), **zero jargão** (bloqueante), **exemplo fiel** (bloqueante) e **legibilidade** (consultiva). Você não reescreve — emite um **veredito** com a lista exata do que consertar.

## Insumos

- O doc de negócio: `docs/00-dominio/fluxos-negocio/<slug>.md` (com o bloco Trace).
- O doc técnico: `docs/03-fluxos/<slug>.md` + o grafo `.arquitetura/mapa/fluxos/<slug>.grafo.md`.
- `.arquitetura/contexto-produto.md` (o glossário — a lista de vocabulário permitido).

## Gate 1 · Âncora & honestidade — **BLOQUEANTE**

A tese: **nada no doc é ficção — toda afirmação é rastreável.** Varra o doc frase a frase:

- Toda **frase de comportamento** (o quê) tem linha no **Trace** apontando o doc técnico, com estado `herdado-verificado`, **e a base existe mesmo** no doc técnico? Sem linha, ou base inexistente → **SEM-ÂNCORA** (reprova).
- Todo **porquê** é `atribuído` (com quem/quando) OU `[inferido do código · a confirmar]` **com base real**? Um porquê afirmado como fato, sem atribuição nem marca → **FICÇÃO** (reprova).
- Liste **todas as inferências a confirmar** num bloco à parte — é a fila de trabalho do dono de produto. (Registra-e-segue: não reprova por *ser* inferência; reprova por inferência **sem base** ou fato inventado.)

## Gate 2 · Zero jargão na prosa — **BLOQUEANTE**

A PO não pode topar com código. Fora do bloco Trace (recolhível), a prosa tem algum **nome de classe/arquivo/método**, `arquivo:linha`, ou **termo técnico cru** (`idempotente`, `mutex`, `PENDING_REVIEW`, `CAS`, `lock`, `thread`)? Cada ocorrência → **JARGÃO** (reprova), com a frase e a sugestão em linguagem de gente.

## Gate 3 · Exemplo fiel — **BLOQUEANTE**

O(s) exemplo(s) mostram algum **desfecho ou caminho que o grafo não tem**? Uma seta/resultado inventado → **EXEMPLO-INFIEL** (reprova). Valores ilustrativos são OK; **estrutura** fora do fluxo, não.

## Gate 4 · Legibilidade — **CONSULTIVA**

Marque cada item `ok` / `fraco` / `N/A`:

- [ ] **Em uma frase** diz o job sem rodeio.
- [ ] **POV do usuário** (não da máquina).
- [ ] **Voz ativa**, ator nomeado, uma ideia por frase.
- [ ] **Vocabulário** só do glossário, consistente.
- [ ] **Esqueleto completo** (*Em uma frase · Quem usa · Como funciona c/ exemplo · Quando dá errado · Regras & porquês · Trace*).

Consultivo = **não reprova**, mas todo `fraco` vira **recomendação**.

## Veredito

```md
# grill-negocio — <slug>
## Gate 1 · Âncora & honestidade (bloqueante): PASSA / REPROVA
SEM-ÂNCORA: <n> · FICÇÃO: <n>  — Inferências a confirmar: <lista>
## Gate 2 · Zero jargão (bloqueante): PASSA / REPROVA
JARGÃO: <n>  — <frase + sugestão>
## Gate 3 · Exemplo fiel (bloqueante): PASSA / REPROVA
EXEMPLO-INFIEL: <n>
## Gate 4 · Legibilidade (consultiva)
<checklist>  — recomendações: <lista>
## Resultado: APROVADO  (só se os 3 bloqueantes PASSAM)
        ou   BLOQUEADO  → conserte: <lista exata>
```

## Critério de conclusão (checável)

- **Toda** frase de comportamento classificada (ancorada / SEM-ÂNCORA).
- **Todo** porquê classificado (atribuído / inferido-com-base / FICÇÃO).
- **Toda** ocorrência de jargão listada; exemplos checados contra o grafo.
- Os **5** itens de legibilidade marcados.
- Veredito final coerente com os **3** gates bloqueantes.

## Handoff

- **APROVADO** → imprima: *"grill-negocio aprovado. O doc `docs/00-dominio/fluxos-negocio/<slug>.md` está ancorado, sem jargão e fiel ao fluxo — pronto pra PO / publicação. Confirme as inferências marcadas quando um dono de produto puder."*
- **BLOQUEADO** → imprima: *"grill-negocio bloqueado por <n> âncora / <n> jargão / <n> exemplo. Volte ao **`documentar-negocio`** e cubra a lista acima."*
