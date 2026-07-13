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
- **Tenha contexto humano à mão.** O Passo 0 pergunta domínio, invariantes, casos-limite,
  operação, fronteiras, restrições, compromissos e decisores — e para até receber resposta.
- **Escolha UM fluxo crítico + seu entrypoint** para o Passo 2 (ex.: `"autorização de pagamento" — POST /payments`).
- **(Recomendado) Use um commit limpo.** Commit com working tree sujo não identifica o
  conteúdo citado. Se precisar documentar alterações locais, a trilha registra fingerprint
  de cada arquivo citado; sem snapshot verificável, o gate técnico bloqueia.

## A sequência (você só digita o 1º comando)

Cada passo termina imprimindo o **próximo comando** (handoff); `.arquitetura/grills/`
mantém perguntas/respostas específicas, o mapa mantém o ledger e `.arquitetura/gates/`
mantém as aprovações. Você dispara só o Passo 0.

| Passo | Prompt | Produz |
|---|---|---|
| 0 | `bootstrap-contexto` | grill contextual + `.arquitetura/contexto.md` |
| 1 | `mapear-estrutura` | `.arquitetura/mapa/` (estrutura + inventário `ENTRY-###`) |
| 2 | `documentar-fluxo` ⭐ | grill `PERG-TEC` + doc + ledger técnico |
| 3 | `grill-doc` | `.arquitetura/gates/grill-doc.<slug>.md` |
| 4 | `grill-mermaid` | `.arquitetura/gates/grill-mermaid.<slug>.md` |

> **Sessão = unidade de isolamento.** Rode cada passo numa conversa limpa; o estado vive
> nos arquivos (`.arquitetura/`, `docs/`), não no histórico do chat.

### Step 5 · Revisão arquitetural — opcional, depois do técnico

Com um fluxo aprovado nos dois gates, você pode rodar uma revisão de arquitetura antes
do track de negócio:

| Passo | Prompt | Produz |
|---|---|---|
| 5 | `revisar-arquitetura` | HTML visual temporário + `.arquitetura/revisoes/arquitetura.<escopo>.md` + grill `PERG-ARQ` do candidato escolhido |

O step começa no trace verificado, percorre o código em busca de modules shallow e
oportunidades de deepening, aplica o deletion test e apresenta somente candidatos com
evidência `arquivo:linha`. Depois **para para você escolher**. O grill seguinte continua
uma pergunta por vez, sempre derivada do candidato e do projeto — não há questionário
estático. Nenhum código é alterado; o resultado é um blueprint para uma decisão posterior.

O relatório fica em `$TMPDIR`/`/tmp` e pode desaparecer; ledger, escolha e respostas ficam
persistidos em `.arquitetura/`, então o prompt consegue retomar com segurança.

### Track de negócio — opcional, depois do técnico

Com o track técnico de um fluxo **completo**, você pode gerar a **versão de negócio** dele — pra uma **PO nova** entender o que o app faz, em linguagem simples, sem ver código. Você **inicia à mão** (não é encadeado pelo handoff do técnico):

| Passo | Prompt | Produz |
|---|---|---|
| 6 | `contexto-produto` (1×) | `.arquitetura/contexto-produto.md` (personas, jobs, glossário) |
| 7 | `documentar-negocio` ⭐ | grill `PERG-NEG` + doc de negócio |
| 8 | `grill-negocio` | `.arquitetura/gates/grill-negocio.<slug>.md` |
| 9 | `documentar-visao` | grill `PERG-VISAO` + visão progressiva |
| 10 | `grill-visao` | `.arquitetura/gates/grill-visao.md` |

Roda **depois** do técnico de propósito: quando o "porquê" de negócio não tem dono humano à mão, o `documentar-negocio` **infere da base técnica já verificada** e marca `[inferido do código · a confirmar]` — nunca inventa. Exemplo real (doc técnico + doc de negócio do mesmo fluxo) no [piloto](piloto/docs/00-dominio/fluxos-negocio/wakeup-run-settle.md).

Os passos **9-10** são a **Visão de Produto progressiva** — a porta de entrada de Camada 0. Rode **por último**, depois de pelo menos um gate de negócio aprovado. A visão liga só fluxos aprovados, cita o "Em uma frase" e publica duas medidas distintas: **N docs aprovados** e **C/E entrypoints cobertos**. Re-rode quando a cobertura crescer. O [piloto](piloto/docs/00-dominio/visao-de-produto.md) demonstra a versão anterior do slice; a revalidação com os novos contratos está pendente.

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
- ✅ **Deixe os gates bloquearem e grave os vereditos.** Etapas posteriores só aceitam
  `.arquitetura/gates/*.md` aprovado no mesmo snapshot.
- ✅ **Use IDs, não nomes parecidos.** `ENTRY` não é fluxo; `FLUXO` não é módulo; `PASSO/ARESTA/FRONTEIRA` mantêm o trace estável.
- ✅ **Exija perguntas específicas.** Toda `PERG-###` deve citar o sinal do projeto que
  a disparou; rubricas são lentes, não questionários para copiar.
- ✅ **Escolha o deepening conscientemente.** `revisar-arquitetura` não propõe interface
  antes de você selecionar um `OPORT-ARQ-###`; rejeitar ou adiar também é decisão válida.
- ✅ **Trate cobertura em duas dimensões.** `N` docs aprovados e `C/E` entrypoints cobertos.
- ✅ **Responda a elicitação de verdade.** Um `[PENDENTE: ...]` honesto vale mais que um chute; "padrões que não se aplicam" é o anti-template mais barato.
- ✅ **Um fluxo, depois repita.** Para o próximo fluxo crítico, rode de novo a partir do Passo 2 — contexto e mapa já existem.
- ❌ **Não edite `.arquitetura/` à mão** para "adiantar". O mapa é ledger; só o `documentar-fluxo` promove nós lendo o corpo do código.
- ❌ **Não publique o mapa.** `.arquitetura/` é interno (fora de `docs/`); só `docs/` vai pro Docusaurus.
- ❌ **Não confie em commit com working tree sujo.** Use commit limpo ou fingerprints;
  se o repo muda sob você, `arquivo:linha` drifta silenciosamente.

## Quando algo trava

- **Stack não detectada (Passo 0/1)** → confirme que rodou na raiz certa; a detecção usa manifestos (`package.json`, `pom.xml`, `go.mod`, …), não adivinhação.
- **`grill-doc` BLOQUEADO** → o veredito lista exatamente o que falta; volte ao `documentar-fluxo` e cubra cada AUSENTE / citação.
- **`STALE` / hash divergente** → regenere o artefato a partir do código atual; não recicle aprovação antiga.
- **`grill-mermaid` AJUSTAR** → corrija só o(s) bloco(s) apontado(s) no doc e rode o gate de novo; não precisa refazer o doc inteiro.
- **Relatório arquitetural não abriu** → use o caminho absoluto impresso; se o arquivo
  temporário sumiu, rode `revisar-arquitetura` de novo no mesmo snapshot para regenerá-lo
  a partir do ledger.
- **Amazon Q não acha o prompt** → no IDE, os prompts de projeto não são lidos; copie os `.md` para `~/.aws/amazonq/prompts/` (detalhe em [dist/README.md](dist/README.md)).
