# Como usar a trilha — do zero à doc de fluxo

> **Start here.** Runbook de operação da trilha de documentação de arquitetura.
> Roda em **Amazon Q, GitHub Copilot ou Kiro** — sem Claude.
>
> Rationale → [DESIGN.md](DESIGN.md) · Cadeia canônica → [prompts/README.md](prompts/README.md) · Deploy + smoke-test → [dist/README.md](dist/README.md)

## O que a trilha faz

De qualquer codebase, gera documentação de arquitetura `.md` (para Docusaurus) que é
**completa** (não pula o 20% difícil: error paths, chamada externa, compensação) e
**precisa** (só afirma sobre o código o que o código comprova). Esta fatia entrega a
**joia**: um doc de fluxo ponta-a-ponta, com diagrama, passado por dois gates.

## O princípio que a doc garante (leia antes de rodar)

> O mapa e o depoimento humano são **hipóteses** — nunca citados. A única fonte citável
> sobre o que o código FAZ é o próprio código, como **`arquivo:linha`**.

Toda frase de comportamento na doc final carrega `arquivo:linha`. É isso que separa esta
trilha de um gerador raso — e é o que os gates protegem.

## Antes de começar (pré-requisitos)

- **Rode na raiz do repositório** que você quer documentar.
- **Instale os prompts** no seu runtime — copie a pasta certa de `dist/` (ver [dist/README.md](dist/README.md)). Sem instalar, dá pra colar o conteúdo do prompt à mão (ver abaixo).
- **Um fluxo por vez.** A trilha é depth-first: fundação fina → um fluxo crítico inteiro → gates. Depois repita para o próximo fluxo.
- **Tenha o contexto de negócio à mão.** O Passo 0 te pergunta tier, propósito, blast radius, restrições e "padrões que NÃO se aplicam" — e espera resposta (não inventa).
- **Escolha UM fluxo crítico + seu entrypoint** para o Passo 2 (ex.: `"autorização de pagamento" — POST /payments`).
- **(Recomendado) Fixe um commit.** Cite contra um hash imutável: o piloto provou que um working tree editado ao vivo faz `arquivo:linha` driftar. Rode `git log -1`, anote o hash, trabalhe sobre ele.

## A sequência (você só digita o 1º comando)

Cada passo termina imprimindo o **próximo comando** (handoff); o mapa em `.arquitetura/`
é a memória entre as sessões. Você dispara só o Passo 0 — o resto se encadeia.

| Passo | Prompt | Produz |
|---|---|---|
| 0 | `bootstrap-contexto` | `.arquitetura/contexto.md` |
| 1 | `mapear-estrutura` | `.arquitetura/mapa/` (semente L0-L1 + cobertura) |
| 2 | `documentar-fluxo` ⭐ | `docs/03-fluxos/<slug>.md` + grafo rastreado |
| 3 | `grill-doc` | veredito: completude estrutural + citação (bloqueantes) |
| 4 | `grill-mermaid` | veredito: sintaxe + MDX + fidelidade ao grafo |

> **Sessão = unidade de isolamento.** Rode cada passo numa conversa limpa; o estado vive
> nos arquivos (`.arquitetura/`, `docs/`), não no histórico do chat.

## O prompt inicial (copiar e colar)

O fluxo começa no **Passo 0**. Com os prompts instalados, o "prompt inicial" é só invocar
`bootstrap-contexto` na raiz do repo:

| Runtime | Digite no chat |
|---|---|
| Amazon Q (`q chat`) | `@bootstrap-contexto` |
| GitHub Copilot | `/bootstrap-contexto` |
| Kiro | `#bootstrap-contexto` |

**Sem instalar (colar à mão)** — abra o arquivo do passo (`prompts/bootstrap-contexto.md`,
ou o alvo do seu runtime em `dist/…`), copie **todo** o conteúdo e cole no chat precedido
de uma linha de contexto:

```text
Vamos documentar a arquitetura deste repositório seguindo a trilha, um passo por vez.
Estamos na raiz do repo. Execute agora o Passo 0 exatamente como especificado abaixo,
inclusive parando para me fazer as perguntas de elicitação:

<cole aqui o conteúdo inteiro de bootstrap-contexto>
```

A partir daí **siga o handoff**: cada passo imprime o próximo comando. Você não precisa
decorar a ordem — no Passo 1 o handoff vai te pedir o fluxo + entrypoint do Passo 2.

## Diretrizes de uso

- ✅ **Siga o handoff, não pule passos.** O mapa de um passo é insumo do próximo.
- ✅ **Deixe os gates bloquearem.** `grill-doc` acusando aresta AUSENTE ou citação faltando é o gate funcionando — volte ao `documentar-fluxo` e cubra a lista exata do veredito.
- ✅ **Responda a elicitação de verdade.** Um `[PENDENTE: ...]` honesto vale mais que um chute; "padrões que não se aplicam" é o anti-template mais barato.
- ✅ **Um fluxo, depois repita.** Para o próximo fluxo crítico, rode de novo a partir do Passo 2 — contexto e mapa já existem.
- ❌ **Não edite `.arquitetura/` à mão** para "adiantar". O mapa é ledger; só o `documentar-fluxo` promove nós lendo o corpo do código.
- ❌ **Não publique o mapa.** `.arquitetura/` é interno (fora de `docs/`); só `docs/` vai pro Docusaurus.
- ❌ **Não confie em citação sem commit fixo.** Se o repo muda sob você, `arquivo:linha` drifta silenciosamente.

## Quando algo trava

- **Stack não detectada (Passo 0/1)** → confirme que rodou na raiz certa; a detecção usa manifestos (`package.json`, `pom.xml`, `go.mod`, …), não adivinhação.
- **`grill-doc` BLOQUEADO** → o veredito lista exatamente o que falta; volte ao `documentar-fluxo` e cubra cada AUSENTE / citação.
- **`grill-mermaid` AJUSTAR** → corrija só o(s) bloco(s) apontado(s) no doc e rode o gate de novo; não precisa refazer o doc inteiro.
- **Amazon Q não acha o prompt** → no IDE, os prompts de projeto não são lidos; copie os `.md` para `~/.aws/amazonq/prompts/` (detalhe em [dist/README.md](dist/README.md)).
