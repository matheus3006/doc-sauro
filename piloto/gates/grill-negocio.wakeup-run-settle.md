# grill-negocio — wakeup-run-settle

Auditoria de `docs/00-dominio/fluxos-negocio/wakeup-run-settle.md` contra o doc técnico `docs/03-fluxos/wakeup-run-settle.md` + o grafo.

## Gate 1 · Âncora & honestidade (bloqueante): **PASSA**

- **10 frases de comportamento**, **10 com linha no Trace**, cada uma apontando uma seção real do doc técnico + aresta do grafo (A2, B1–B2, B3–B6, B17–B18, B22, B26/B29/B30, A17/A18, A12, A5). **SEM-ÂNCORA: 0.**
- **5 porquês**, todos classificados: **2 atribuídos** (deny-by-default; anti-loop cap 5 — operador via CONTEXT.md) + **3 inferidos-com-base**. **FICÇÃO: 0.**
- Spot-check das bases (verificação automática): as **11 arestas do grafo** citadas (A2…B30) existem todas. Os rótulos de seção foram **ajustados após a checagem** — `§Idempotência`/`§Compensação`/`§Settle` (que não eram cabeçalhos literais) viraram os headers reais `§Transições·idempotência·compensação` e `§Happy path·C·Settle`, pra um cético achar exatamente. Nenhuma base inventada. *(O gate pegou a imprecisão antes do veredito — como o técnico pegou B14/B21.)*

**Inferências a confirmar** (fila do dono de produto — não travam, mas não são fato):
1. "Um trabalho por agente ⇒ para não duplicar custo" (base: serialização + coalescing).
2. "Cobra uma vez ⇒ previsibilidade de orçamento" (base: cobrança de abertura só na 1ª tentativa).
3. "Drena, não mata ⇒ não perder trabalho já pago" (base: cancela só o não-iniciado; em-voo termina).

## Gate 2 · Zero jargão na prosa (bloqueante): **PASSA**

- **0** nome de classe/arquivo/método na prosa. **0** `arquivo:linha`. **0** enum cru (usa "feito / esperando revisão / bloqueado", não `DONE`/`PENDING_REVIEW`/`BLOCKED`).
- **0** termo técnico cru da lista proibida (`idempotente`, `mutex`, `CAS`, `lock`, `thread`) — cada um traduzido ("não cobra duas vezes", "reserva a tarefa").
- Código só aparece dentro do bloco **Trace** (recolhível) e como **par técnico** no glossário — permitido.

## Gate 3 · Exemplo fiel (bloqueante): **PASSA**

- Exemplo da Maria (*Redator*): recebe → em processamento → confere orçamento → reserva → trabalha → **feito**; ramo alternativo **esperando revisão** se sensível.
- Todos os desfechos existem no grafo: enqueue/202 (A), preflights (B3–B6), checkout (B17), execução (B22), **feito** (B29), **esperando revisão** (B26). **EXEMPLO-INFIEL: 0** (nenhum caminho fora do grafo).

## Gate 4 · Legibilidade (consultiva)

- [x] **Em uma frase** diz o job sem rodeio — ok.
- [x] **POV do usuário** ("você pede… vê 'recebido'") — ok.
- [x] **Voz ativa**, ator nomeado — ok.
- [x] **Vocabulário** só do glossário, consistente — ok.
- [x] **Esqueleto completo** (6 seções) — ok.

**Recomendações (não travam):**
- "drena **até o checkpoint**" ainda é meio técnico pra PO — trocar por "para de gastar assim que estoura, sem cortar o que já começou".
- Atribuição "via **CONTEXT.md**" — suavizar pra "documento de contexto do operador" (a PO não sabe o que é CONTEXT.md).

## Resultado: **APROVADO** (os 3 gates bloqueantes PASSAM)

O doc de negócio está **ancorado** (toda afirmação rastreável), **sem jargão** e **fiel ao fluxo**. Pronto pra PO / publicação. Confirme as 3 inferências marcadas quando um dono de produto puder — elas são hipóteses do modelo, não fato.
