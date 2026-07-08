# grill-mermaid — wakeup-run-settle

Insumos: `docs/03-fluxos/wakeup-run-settle.md` (1 bloco ` ```mermaid `) × grafo rastreado.

## Bloco 1 — `sequenceDiagram`

**Eixo 1 · Sintaxe (subset seguro):** LIMPO
- Tipo `sequenceDiagram`; fence exatamente ` ```mermaid `, fechada.
- IDs de participante alfanuméricos (`Ctl Svc Lin Fan Bud Q Sched Disp Store Exec Vol Adp Iss Reap`); `actor Board`.
- Mensagens no formato `A->>B: texto` sem aspas; aliases (`as ...`) sem caractere especial.
- **Zero** `< > ( ) { }` em qualquer label — `>=` escrito "maior igual", `>` escrito "maior que", `+1` escrito "mais 1", sem parênteses. `arquivo:linha` dentro do texto (o `:` é parte do label).
- `alt/else/end` balanceados (8 blocos `alt`, 8 `end`).

**Eixo 2 · Escaping MDX:** LIMPO
- Nenhum `{`/`}` cru; nenhum `<algo>` (as setas `->>`/`-->>` não abrem tag JSX); cerca fechada.

**Eixo 3 · Fidelidade ao grafo:** LIMPO (após ajuste)
- **Nenhuma seta inventada:** as 37 mensagens mapeiam 1-para-1 em arestas do grafo (A/B/C).
- **Cobre o que importa:** branches (coalesce/defer; PENDING_REVIEW/DONE/BLOCKED; success/failure) e error paths (409 de linhagem, checkout falho, adapter falho) presentes; **chamadas externas** representadas — CLI no container (`B22`) e **volume Docker** (`B21`, adicionado neste gate: era a única fronteira externa ausente do diagrama).
- **Participantes batem:** todos aparecem no grafo; ordem segue o trace (enqueue → dispatch → settle → reaper).

Ajuste aplicado antes do veredito: incluído `participant Vol` + a mensagem `escreve arvore no volume AdapterRunExecutor.java:172`. É a evidência do Eixo 3 funcionando (pegou uma chamada externa que a prosa cobria mas o diagrama omitia).

## Resultado: **LIMPO**

O doc `docs/03-fluxos/wakeup-run-settle.md` passou nos gates do slice (precisão, completude estrutural, mermaid). Pronto pra revisão humana / publicação.
