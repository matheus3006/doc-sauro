# Trilha de Documentação de Arquitetura — Design

> Resultado de uma sessão de `/grill-me`. Alvo: gerar `.md` para Docusaurus a partir
> de qualquer codebase, de forma **completa** e **precisa**, rodando em **Amazon Q +
> GitHub Copilot + Kiro** (sem Claude Code / sem subagentes).
>
> Referência de origem (a evoluir, não copiar): `matheus3006/arquitetura-amazonq-btg` (gerava HTML, raso).

---

## 1. Problema & diagnóstico

A doc de arquitetura sai **rasa** por **dois motivos ortogonais** — e antes a gente só atacava um:

| Eixo | Sintoma | O que resolve |
|---|---|---|
| **Profundidade** | análise não segue a execução; extrai metadado, não comportamento | mapa + leitura forçada (`grill-with-docs`) |
| **Completude** | omite o 20% difícil (error paths, chamada externa, contingência) | gate de completude |

**Causa-raiz da falta de profundidade:** prompts *template-driven* (preenchem campos) em vez de *trace-driven* (seguem o código real). O template vira "preencher lacuna", o agente faz passada superficial, o que não cabe em campo vira gap.

**Precisão ≠ completude.** Uma doc pode ser 100% verdadeira e ainda rasa (calou o que era difícil). As duas precisam de garantia própria.

---

## 2. Princípio-norte (inegociável)

> **O mapa e o depoimento humano são hipóteses. Nunca são citados numa doc.**
> **A única fonte que uma doc pode citar sobre o que o código faz é o próprio código (`arquivo:linha`).**

Tudo abaixo deriva disso.

---

## 3. Arquitetura da solução — duas trilhas

O que o código pode revelar e o que não pode têm mecanismos diferentes. Misturá-los é o que faz o agente **inventar**.

### Trilha de EXTRAÇÃO (código → doc)
Enche **Estrutura** e **Fluxos**. Fonte = código; citação = `arquivo:linha`.

- **O mapa** — aid de leitura barato, **nível declaração**: nomes de pasta/arquivo/classe/método + assinaturas + inferência marcada `[inferido]`. **Nunca abre corpo de método.** É **interno** (NÃO publicado no Docusaurus), **persistente**, e **cresce progressivo** logo à frente das docs. **Language-agnostic**: vocabulário `entrypoint/módulo/unidade/aresta-de-dependência`, lido nativamente pelo LLM (sem parser/ctags/tree-sitter — quebraria a portabilidade).
- **`grill-with-docs`** (`/grilling` + `/domain-modeling`) — leitura **profunda (corpo do método), lazy**, só na fatia que a doc precisa. Promove `[inferido]` → `[verificado: arquivo:linha]`. Ao rastrear um fluxo, descobre o **grafo de chamadas daquele fluxo** (subproduto) — usado depois nos gates.

### Trilha de ELICITAÇÃO (humano → doc)
Enche **Domínio**, **Restrições** e o conhecimento tribal de **Sistemas** (blast radius, "o que quebra às 3h"). Fonte = humano/postmortem/compliance; registro **verbatim** quando é decisão.

---

## 4. Modelo de verdade — jurisdição

Resolve tanto "o mapa não pode alucinar" quanto "o humano não pode mentir sobre o código".

| Regra | O que faz |
|---|---|
| **Jurisdição** | Fato-de-código → *código manda*. Porquê/restrição → *humano manda*, **atribuído**. |
| **Verificação independe da fonte** | Afirmação sobre o que o código FAZ — venha do mapa OU do humano — é verificada contra o código antes de entrar na doc. (Humano diz "retorna string", código diz `int` → humano **refutado** com `arquivo:linha`.) |
| **Atribuição** | Afirmação de jurisdição-humana entra atribuída (verbatim + quem + quando), nunca como "fato objetivo". |
| **Contradição = achado** | Humano contradiz código → não se resolve no silêncio: vira **divergência reportada** (detecção de drift entre o que o time acredita e o que o sistema faz). |

**Limite honesto:** o *porquê* puro (compliance, política) o código não checa — só dá pra **atribuir + cruzar com artefato**. Prometer verificação aí seria mentira.

**Política de divergência:** *registra-e-segue* — código vence a afirmação factual; a divergência vai pra um **registro de primeira classe**; a doc não trava.

---

## 5. Conjunto de documentos (arquitetura de informação)

Camada humana **elevada** a primeira classe (⭐ = novo/elevado vs. a referência BTG):

| Camada | Documentos |
|---|---|
| **0 · Domínio** | Visão geral · Glossário · ⭐Catálogo de regras (com *porquê*) · ⭐Registro de restrições · ⭐Fluxos de negócio (um por fluxo, pra PO — companheiro da Camada 3) |
| **1 · Topologia & Sistemas** | ⭐Mapa de serviços · ⭐Contratos de fronteira · ⭐Deps externas como risco · ⭐Modos de falha & blast radius |
| **2 · Estrutura** | Organização do código · Dados & persistência · Configurações |
| **3 · Fluxos** ⭐joia | Um por fluxo crítico, ponta-a-ponta, sequence + trace `arquivo:linha` + contratos de fronteira que cruza |
| **4 · Operação** | Runbook (SLO, alertas, degradação) · Como estender |
| **5 · Referência & Decisões** | ADRs (decisão + *rationale* + rejeitados) · Enums · ⭐Matriz de rastreabilidade |

---

## 6. Pipeline de execução

Runtime: **sessão = unidade de isolamento**; cada passo é um **prompt standalone**; **handoff explícito** no fim de cada prompt (imprime o próximo comando). **Mapa-é-ledger** (sem sistema de controle à parte): progresso de aprofundamento = status dos nós; progresso de doc = presença de arquivos.

Sequência (um run por projeto):

| # | Etapa | Fonte |
|---|---|---|
| 0 | **Bootstrap de contexto** — detecta stack/estrutura + elicita tier, propósito, blast radius, restrições, "padrões que NÃO se aplicam". Gera o contexto que todo passo lê. | ambas |
| 1 | **Semente do mapa** — inventário L0-L1 + header de cobertura, uma vez. Camadas fundas enchem por-doc (lazy). | extração |
| 2 | **Fundação** — Glossário + Restrições + Regras (vocabulário e limites que todos respeitam). | elicitação |
| 3 | **Estrutura + Topologia** — organização, dados, config, serviços & deps externas. | extração |
| 4 | **Fluxos** ⭐ — extração profunda + gates. | extração |
| 5 | **Operação** — runbook, como estender. | mista |
| 6 | **Rastreabilidade** — matriz por último. ADRs acumulam o tempo todo. | mista |

**Estratégia: depth-first após fundação fina.** Faz a fundação compartilhada uma vez (glossário-semente + restrições + topologia), depois vai **depth-first pela joia** — pega o fluxo mais crítico, produz inteiro, **valida toda a maquinaria numa fatia antes de escalar**.

---

## 7. Gates de qualidade

| Gate | Mecanismo | Rigor |
|---|---|---|
| **Precisão** | disciplina de citação + jurisdição (§2, §4) | bloqueante |
| **Completude estrutural** | toda aresta do grafo rastreado está na doc — coberta OU marcada fora-de-escopo | **bloqueante** |
| **Completude por rubrica** | checklist por tipo de doc (fluxo: gatilho, happy path, cada error path, cada chamada externa, transições, idempotência, timeout/retry, compensação) | consultivo |
| **Mermaid — prevenir** | subset seguro no style rule (só `flowchart`/`sequenceDiagram`, labels entre aspas, IDs alfanuméricos, sem `<>`/parênteses/HTML em nó) | — |
| **Mermaid — detectar** | skill `grill-mermaid` in-session: sintaxe + **escaping MDX** + **fidelidade ao grafo rastreado** | agora |
| **Mermaid — gate duro** | `docusaurus build` (build verde = renderiza) | *futuro, com o time* |

---

## 8. Log de decisões (ADR-style)

1. **Duas rasuras, não uma** — atacar profundidade E completude separadamente.
2. **Mapa nível-declaração, nunca corpo** — o corpo é lazy via grill.
3. **Profundidade lazy** — só a fatia que a doc usa.
4. **Mapa interno, fora de `docs/`** — não vaza pro site.
5. **Mapa persistente** — forçado pela ausência de subagente (arquivo é a única memória entre sessões).
6. **Runtime Q+Copilot+Kiro, sem Claude** — menor denominador comum manda.
7. **Mapa-é-ledger** — sem sistema de controle duplicado; handoff explícito por prompt.
8. **Princípio-norte: mapa nunca citado; citação = código** (§2).
9. **Duas trilhas: extração × elicitação** — não misturar (evita invenção).
10. **Poliglota = ferramenta language-agnostic** (LLM-native, sem parser), não mix intra-pacote.
11. **Jurisdição + verificação-independe-da-fonte** (§4).
12. **Divergência: registra-e-segue** + registro de primeira classe.
13. **Completude: estrutural bloqueante + rubrica consultiva.**
14. **Mermaid: prevenir + detectar (agora) + build-gate (futuro); fidelidade amarrada ao grafo rastreado.**
15. **Sequência + depth-first após fundação fina** (§6).
16. **Track de negócio: 2ª passada, após o técnico completo** — um doc "Fluxo de Negócio" por fluxo, pra uma PO nova, em linguagem simples; roda depois do técnico porque a inferência do porquê se apoia na base já verificada.
17. **3ª categoria de verdade: `[inferido do código · a confirmar]`** — além de *fato citado* e *atribuído ao humano*, o porquê de negócio pode ser inferido da base técnica, sempre com base explícita e marcado como não-confirmado. Nunca ficção.
18. **Doc de negócio: arquivo separado, zero código na prosa** — âncora via link pro doc técnico + tabela de trace recolhível; o QUÊ é herdado-verificado, o PORQUÊ é atribuído ou inferido-marcado.
19. **Gate de negócio (`grill-negocio`): âncora + zero-jargão + exemplo-fiel bloqueantes; legibilidade consultiva** — espelha o `grill-doc`.
20. **Camada 0 elevada — Visão de Produto (`documentar-visao` + `grill-visao`):** um overview de app pra uma **PO nova** entender o produto **inteiro** (não um fluxo só). Roda **por último** no track de negócio (liga os docs de negócio já escritos, **não os inventa**) e re-roda quando novos fluxos ganham doc. Publicável em `docs/00-dominio/visao-de-produto.md`.
21. **Âncora de síntese + honestidade de cobertura:** a visão ancora cada fluxo no **doc de negócio** (herda o "Em uma frase" **citado**, não reescrito; cadeia Visão→negócio→técnico), marca o "o que o app é no todo" como `[inferido do código · a confirmar]` (nenhum fluxo isolado prova o todo), e **declara cobertura** (N de ~M, com o que falta **listado** — mata o *silent-cap*, espelha a completude-estrutural). O gate `grill-visao` espelha o `grill-negocio` trocando "exemplo fiel" por **"mapa fiel"** (link resolve + one-liner idêntico ao "Em uma frase" + cobertura honesta).

---

## 9. Itens mecânicos em aberto (defaults recomendados — não ratificados)

- **Docusaurus** — categorias da sidebar = as 6 camadas (§5); frontmatter com `sidebar_position`; mermaid via `@docusaurus/theme-mermaid`; mapa em `.arquitetura/mapa/` (fora de `docs/`); registro de divergências como doc própria em `Referência`.
- **Empacotamento por assistente** (triplo-write a partir de uma fonte canônica única = `prompts/*.md`; gerador `tools/empacotar.py` → `dist/`). Todos são **invocáveis (inclusão manual)**, não always-on — rodam em sequência, um por vez. Convenções **confirmadas nos docs/fonte oficiais (2026-07)**:
  - `.amazonq/prompts/<nome>.md` — Markdown puro, **sem frontmatter**; invoca `@<nome>` no `q chat` (pasta do projeto é **CLI-only**; o IDE lê só `~/.aws/amazonq/prompts/`).
  - `.github/prompts/<nome>.prompt.md` — frontmatter `agent: 'agent'` + `description` (`mode` foi **depreciado** → `agent`); invoca `/<nome>` no Copilot Chat.
  - `.kiro/steering/<nome>.md` — frontmatter `inclusion: manual`; referencia `#<nome>`.
  - _As always-on (`.amazonq/rules/*`, `.github/instructions/* applyTo:"**"`, `inclusion: always`) NÃO servem para invocável e ficam para uma futura regra always-on separada, se um run real exigir — hoje o princípio-norte vai embutido em cada prompt._
- **Schema do mapa** — `_indice.md` (árvore L0-L1 + tabela de cobertura) + um arquivo por módulo top-level (L2-L4); campo de status por nó: `esqueleto → inferido → verificado | corrigido`, mais `stale`; carimbo de frescor (commit/hash do arquivo).
- **Inventário de prompts:**
  - **Track técnico (construído):** `bootstrap-contexto` · `mapear-estrutura` · `documentar-fluxo` · `grill-doc` · `grill-mermaid`
  - **Track de negócio (construído):** `contexto-produto` (lente de PO) · `documentar-negocio` (a joia de negócio) · `grill-negocio` (gate) → doc em `docs/00-dominio/fluxos-negocio/<slug>.md`
  - **Camada 0 · Visão de Produto (construído):** `documentar-visao` (overview de app; cita o "Em uma frase" de cada fluxo + mapa de cobertura honesto) · `grill-visao` (gate: âncora + zero-jargão + **mapa-fiel**) → doc em `docs/00-dominio/visao-de-produto.md`
  - **Geradores por tipo de doc (a construir):** `glossario` · `restricoes` · `regras` · `estrutura` · `topologia` · `runbook` · `adr` · `rastreabilidade`

---

## 10. Próximos passos

1. Ratificar/ajustar os defaults do §9.
2. Construir os arquivos de skill/prompt (pode ser aqui no Claude Code; o resultado é portável e roda em Q/Copilot/Kiro).
3. Piloto **depth-first**: escolher um projeto real + o fluxo mais crítico, rodar a maquinaria inteira nessa fatia, medir se some o gap.
