# Prompt · `grill-doc`

> Gate de qualidade da trilha. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem parser. Roda depois do `documentar-fluxo`, apontando para o doc e seu grafo.

Você **audita um doc de fluxo** em três frentes: **completude estrutural** (bloqueante), **disciplina de citação** (bloqueante) e **rubrica de fluxo** (consultiva). Você não reescreve o doc — você emite um **veredito** com a lista exata do que consertar.

## Insumos

- O doc: `docs/03-fluxos/<slug>.md`.
- O grafo rastreado: `.arquitetura/mapa/fluxos/<slug>.grafo.md`.

## Gate 1 · Completude estrutural — **BLOQUEANTE**

A tese do gate: **toda aresta do grafo rastreado está na doc — coberta OU marcada `fora-de-escopo`.** Nenhum salto some no silêncio.

Para **cada** aresta do `<slug>.grafo.md`, classifique:

- **coberta** — o `arquivo:linha` do callee (ou uma linha da mesma unidade) aparece na prosa do doc, e o papel do salto está narrado.
- **fora-de-escopo** — a aresta está marcada `fora-de-escopo` no grafo **e** listada como tal no doc, com motivo.
- **AUSENTE** — nem uma coisa nem outra. **Cada AUSENTE reprova o gate.**

Monte a **tabela de cobertura**:

```md
| # | Aresta (callee arquivo:linha) | Classe | Onde no doc |
|---|---|---|---|
| 1 | `<b:linha>` | coberta / fora-de-escopo / AUSENTE | <seção> |
```

## Gate 2 · Disciplina de citação — **BLOQUEANTE**

O princípio-norte: **a única fonte citável sobre o que o código faz é o código (`arquivo:linha`); o mapa e o humano nunca são citados como fato-de-código.** Varra o doc frase a frase:

- Toda **frase de comportamento** ("valida", "grava", "recusa", "chama", "muda o estado para…") carrega um `arquivo:linha`? Sem citação → **SEM-CITAÇÃO** (reprova).
- Alguma afirmação de comportamento está apoiada no **mapa** ou num **depoimento humano** como se fosse fato objetivo (em vez de `arquivo:linha`)? → **FONTE-ERRADA** (reprova). Depoimento humano só entra **atribuído**, para *porquê/restrição* — nunca para o que o código faz.

Liste cada violação com a frase e a seção.

## Gate 3 · Rubrica de fluxo — **CONSULTIVA**

O grafo garante que nenhum **salto rastreado** sumiu; a rubrica caça o **buraco semântico** que o grafo não enxerga (um error path que existe no código e nem virou aresta). Marque cada item `presente` / `ausente` / `N/A (motivo)`:

- [ ] **Gatilho** nomeado (quem/o quê dispara)
- [ ] **Happy path** completo, passo a passo
- [ ] **Cada error path** real coberto
- [ ] **Cada chamada externa** nomeada, com o que acontece se falhar/demorar
- [ ] **Transições de estado** (de→para, sob qual guarda)
- [ ] **Idempotência** (chamar 2× causa efeito duplo? o que protege?)
- [ ] **Timeout / retry** (prazo, re-tentativa, quem re-dispara)
- [ ] **Compensação** (o que desfaz/estanca se um passo depois falha)

Consultivo = **não reprova**, mas todo `ausente` vira **recomendação** no veredito. (Um `ausente` aqui costuma indicar que o rastreamento parou raso — vale voltar ao `documentar-fluxo`.)

## Veredito

```md
# grill-doc — <slug>
## Gate estrutural (bloqueante): PASSA / REPROVA
<tabela de cobertura>  — AUSENTES: <n>
## Gate de citação (bloqueante): PASSA / REPROVA
<violações>  — SEM-CITAÇÃO: <n> · FONTE-ERRADA: <n>
## Rubrica (consultiva)
<checklist>  — recomendações: <lista>
## Resultado: APROVADO  (só se os dois bloqueantes PASSAM)
        ou   BLOQUEADO  → conserte: <lista exata>
```

## Critério de conclusão (checável)

- **Toda** aresta do grafo está classificada (coberta / fora-de-escopo / AUSENTE).
- **Toda** frase de comportamento está classificada (citada / SEM-CITAÇÃO / FONTE-ERRADA).
- Os **8** itens da rubrica estão marcados.
- Veredito final emitido, coerente com os dois gates bloqueantes.

## Handoff

- **APROVADO** → imprima: *"grill-doc aprovado. Próximo passo: rode **`grill-mermaid`** no doc `docs/03-fluxos/<slug>.md`."*
- **BLOQUEADO** → imprima: *"grill-doc bloqueado por <n> aresta(s) AUSENTE(s) / <n> citação(ões). Volte ao **`documentar-fluxo`** e cubra a lista acima."*
