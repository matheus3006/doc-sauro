---
inclusion: manual
---

# Prompt · `grill-mermaid`

> Lint de diagrama, in-session. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem subagente, sem build. Roda depois do `grill-doc` aprovar, no doc de fluxo.

Você **linta cada bloco Mermaid** do doc em três eixos: **sintaxe** (subset seguro), **escaping MDX** e **fidelidade ao grafo rastreado**. É o gate que hoje substitui o `docusaurus build` (build-gate é futuro): pega o erro que quebraria o render **antes** de ir pro site.

## Insumos

- O doc: `docs/03-fluxos/<slug>.md`.
- O grafo rastreado: `.arquitetura/mapa/fluxos/<slug>.grafo.md`.

Extraia **todos** os blocos ` ```mermaid ` do doc. Rode os três eixos em cada um.

## Eixo 1 · Sintaxe (subset seguro — sensível ao tipo)

O subset existe para nunca gerar diagrama que o parser recusa. As regras de **aspas** diferem por tipo — errar isso é bug: aspas num label de mensagem de `sequenceDiagram` **renderizam literais**.

- Tipo é **só** `flowchart` ou `sequenceDiagram`. Fence exatamente ` ```mermaid ` (não ` ```mmd `, não sem linguagem). Outro → issue.
- **IDs de nó/participante alfanuméricos** — sem espaço, sem pontuação (`A`, `svc1`, `WakeupSvc`).
- **`flowchart`:** todo texto de nó **entre aspas** — `A["texto"]`. É aqui que "labels entre aspas" vale.
- **`sequenceDiagram`:** o texto da mensagem vem **após `:` e SEM aspas** (`A->>B: texto`); o alias (`participant ID as Nome`) fica **sem aspas** e sem caractere especial. `arquivo:linha` no texto é permitido — o `:` faz parte do label.
- **Proibido em QUALQUER label** (os dois tipos): `<`, `>`, `(`, `)`, `{`, `}`, HTML. Troque parênteses por vírgula/traço.

## Eixo 2 · Escaping MDX

O Docusaurus renderiza `.md` como **MDX**; `<` e `{` disparam o parser JSX no pré-passe mesmo perto de diagrama:

- **`{` ou `}`** crus num label → expressão JSX → issue.
- **`<algo>`** cru → tag JSX → issue.
- Cerca ` ```mermaid ` malfechada (sem a cerca de fechamento) → issue.
- Acentos são OK; o problema é `{ } < > ( )` e cerca malfechada. (Eixo 1 já bane esses — aqui é o segundo par de olhos MDX.)

## Eixo 3 · Fidelidade ao grafo rastreado

O diagrama é um **resumo fiel** do grafo — não o substitui (a cobertura exaustiva aresta-a-aresta é do `grill-doc`, prosa × grafo). Fiel significa:

- **Nenhuma seta inventada:** toda mensagem do diagrama corresponde a uma aresta do `<slug>.grafo.md`. Esta é a checagem dura — seta sem aresta reprova.
- **Cobre o que importa:** cada **branch**, cada **error path** e cada **chamada externa** do grafo está representada (como mensagem ou dentro de um `alt`/`opt`). Arestas internas granulares (um `save`, um evento) podem ser resumidas — o que não pode é o diagrama **contradizer** o grafo.
- **Participantes batem:** cada `participant` é uma unidade que aparece no grafo. A ordem das mensagens segue a ordem do rastreamento.

Issue: seta a mais (invenção) **ou** branch/error-path/chamada-externa ausente **ou** ordem que contradiz o trace.

## Veredito

```md
# grill-mermaid — <slug>
## Bloco 1
- Sintaxe: LIMPO / issues: <lista com linha>
- MDX: LIMPO / issues: <lista com linha>
- Fidelidade: LIMPO / issues: <setas a mais / arestas a menos>
## Resultado: LIMPO  (todos os eixos, todos os blocos)
        ou   AJUSTAR → <lista exata de correções>
```

## Critério de conclusão (checável)

- **Todo** bloco Mermaid do doc foi extraído e checado nos **3** eixos.
- Cada issue aponta **linha** e **correção**.
- Veredito final coerente: `LIMPO` só se os três eixos passam em todos os blocos.

## Handoff

- **LIMPO** → imprima: *"grill-mermaid limpo. O doc `docs/03-fluxos/<slug>.md` passou nos gates do slice (precisão, completude estrutural, mermaid). Pronto pra revisão humana / publicação."*
- **AJUSTAR** → imprima: *"grill-mermaid pediu ajuste. Corrija o(s) bloco(s) no doc e rode `grill-mermaid` de novo."*
