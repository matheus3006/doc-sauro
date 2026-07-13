---
inclusion: manual
---

# Prompt · `grill-mermaid`

> Gate de diagrama. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem
> subagente e sem build. Roda somente depois de `grill-doc` aprovado.

Você valida cada bloco Mermaid do doc contra o ledger. Não reescreve o diagrama: grava
`.arquitetura/gates/grill-mermaid.<slug>.md` com correções exatas.

## Pré-condições

- Doc, ledger e `.arquitetura/gates/grill-doc.<slug>.md` existem no mesmo snapshot.
- O gate técnico está `APROVADO`. Caso contrário: `BLOQUEADO-PRECONDICAO`.
- Deve existir ao menos um bloco Mermaid cercado e identificado como `mermaid`.
  Ausência é issue, não sucesso vazio.

## Eixo 1 · Sintaxe e subset seguro — BLOQUEANTE

- A cerca deve declarar exatamente `mermaid`; o tipo interno é apenas `flowchart` ou
  `sequenceDiagram`.
- IDs de nó/participante alfanuméricos, sem espaço/pontuação.
- `flowchart`: texto do nó entre aspas, por exemplo `A["texto"]`.
- `sequenceDiagram`: mensagem após `:` e sem aspas; alias de participante simples.
- Proibidos em labels: `<`, `>`, `{`, `}`, HTML. Parênteses devem ser evitados para
  manter o subset portável.
- Blocos, `alt`/`else`/`end`, `opt`/`end` e fences precisam fechar corretamente.

## Eixo 2 · Compatibilidade MDX — BLOQUEANTE

- `{}` crus, `<algo>` cru ou fence malfechada recebem issue.
- Verifique também frontmatter e blocos adjacentes: um fence anterior aberto pode fazer
  Mermaid válido quebrar o MDX.
- Acentos são permitidos; não os “corrija”.

## Eixo 3 · Fidelidade por identidade — BLOQUEANTE

Para cada mensagem/seta:

- associe-a a um `ARESTA-###` real e ao branch correto;
- participantes internos devem existir no ledger; externos devem corresponder a
  `FRONTEIRA-###`;
- ordem precisa respeitar o trace; `alt`/`opt` deve representar `BRANCH-###` real;
- nenhuma seta, retorno, erro ou participante pode ser inventado;
- todo branch, error path e fronteira relevante do ledger aparece. Arestas internas
  triviais podem ser resumidas, desde que a tabela do veredito diga quais foram
  condensadas e o diagrama não mude seu significado.

Classificações: `fiel`, `CONDENSADA`, `SETA-INVENTADA`, `ARESTA-AUSENTE`,
`PARTICIPANTE-INVALIDO`, `ORDEM-DIVERGENTE`.

## Eixo 4 · Leitura operacional — CONSULTIVO

O diagrama deixa visível quem inicia, onde cruza fronteira, onde falha e onde termina?
Complexidade visual que esconde o blast radius vira recomendação, não licença para
alterar o trace.

## Veredito persistente

```md
# grill-mermaid — <slug>
> Doc/ledger snapshot <commit:hash|manifest:digest> · auditado em <data-hora>

## Bloco <n>
- Sintaxe: PASSA/REPROVA — <issues com linha>
- MDX: PASSA/REPROVA — <issues com linha>
- Fidelidade: PASSA/REPROVA
| Elemento | ID do ledger | Classe | Correção |
|---|---|---|---|
- Leitura operacional: <recomendações>

## Resultado: APROVADO / AJUSTAR / BLOQUEADO-PRECONDICAO
## Correções necessárias
<lista exata>
```

`APROVADO` exige todos os blocos passando nos três eixos bloqueantes. Ao aprovar,
registre na associação `FLUXO-<slug> ↔ ENTRY-###` que o fluxo passou pelos dois gates
técnicos; não altere o entrypoint isolado nem o estado de negócio.

## Critério de conclusão

- Todos os blocos Mermaid foram auditados; ausência de bloco não passou em vazio.
- Cada elemento do diagrama foi associado a uma identidade do ledger ou classificado.
- Issues apontam linha, classe e correção esperada.
- O arquivo persistente existe, usa o mesmo snapshot e tem resultado coerente.

## Handoff

- **APROVADO:** `grill-mermaid aprovado e gravado em .arquitetura/gates/grill-mermaid.<slug>.md. O fluxo técnico está apto à revisão humana/publicação. Próximo step opcional: rode revisar-arquitetura para este FLUXO-<slug>; para documentação de produto, rode contexto-produto.`
- **AJUSTAR:** `Corrija somente os elementos listados e rode grill-mermaid novamente.`
- **BLOQUEADO-PRECONDICAO:** `Resolva o grill-doc ou o drift de hash antes deste gate.`
