# Trilha de Documentação de Arquitetura — Design

> Resultado de uma sessão de `/grill-me`. Alvo: gerar `.md` para Docusaurus a partir
> de qualquer codebase, de forma **completa** e **precisa**, rodando em **Amazon Q +
> GitHub Copilot + Kiro** (sem Claude Code / sem subagentes).
>
> Referência de origem (a evoluir, não copiar): `matheus3006/arquitetura-amazonq` (gerava HTML, raso).

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

- **O mapa** — aid de leitura barato, **nível declaração**: nomes de pasta/arquivo/classe/método + assinaturas + inferência marcada `[inferido]`. **Nunca abre corpo de método.** É **interno** (NÃO publicado no Docusaurus), **persistente**, e **cresce progressivo** logo à frente das docs. Mantém duas unidades distintas: cobertura estrutural por módulo e inventário de entrypoints `ENTRY-###`; fluxo confirmado é `FLUXO-<slug>` e nunca é contado como sinônimo de módulo/entrypoint. **Language-agnostic**: vocabulário `entrypoint/módulo/unidade/aresta-de-dependência`, lido nativamente pelo LLM (sem parser/ctags/tree-sitter — quebraria a portabilidade).
- **Grill dinâmico com docs** — leitura **profunda (corpo do método), lazy**, só na fatia que a doc precisa. Primeiro extrai sinais reais (`PASSO/BRANCH/FRONTEIRA`, termos, contratos e ausências), depois gera `PERG-###` específicas; as rubricas são lentes, nunca perguntas literais. Promove `[inferido]` → `[verificado: arquivo:linha]` e produz o grafo usado nos gates.

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

Camada humana **elevada** a primeira classe (⭐ = novo/elevado vs. a referência arquitetura-amazonq):

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

Runtime: **sessão = unidade de isolamento**; cada passo é um **prompt standalone**; **handoff explícito** no fim de cada prompt. `.arquitetura/grills/` persiste perguntas/respostas, o mapa mantém progresso e `.arquitetura/gates/` mantém aprovações.

Sequência (um run por projeto):

| # | Etapa | Fonte |
|---|---|---|
| 0 | **Bootstrap de contexto** — detecta sinais do repo e gera `PERG-CTX` específicas para domínio, operação, restrições e compromissos. | ambas |
| 1 | **Semente do mapa** — inventário L0-L1 + header de cobertura, uma vez. Camadas fundas enchem por-doc (lazy). | extração |
| 2 | **Fundação** — Glossário + Restrições + Regras (vocabulário e limites que todos respeitam). | elicitação |
| 3 | **Estrutura + Topologia** — organização, dados, config, serviços & deps externas. | extração |
| 4 | **Fluxos** ⭐ — extração profunda + gates. | extração |
| 5 | **Operação** — runbook, como estender. | mista |
| 6 | **Rastreabilidade** — matriz por último. ADRs acumulam o tempo todo. | mista |

**Estratégia: depth-first após fundação fina.** Faz a fundação compartilhada uma vez (glossário-semente + restrições + topologia), depois vai **depth-first pela joia** — pega o fluxo mais crítico, produz inteiro, **valida toda a maquinaria numa fatia antes de escalar**.

No slice construído, a sequência operacional ganhou um checkpoint opcional entre a base
técnica verificada e a tradução de produto:

```text
bootstrap → mapa → fluxo → gates técnicos
                         ├─→ revisão arquitetural opcional → escolha humana → blueprint
                         └─→ track de negócio → visão progressiva
```

A revisão não é gate para publicar nem para iniciar negócio. Ela usa o trace aprovado
como base confiável para localizar fricção, sem transformar uma sugestão de refactor em
decisão automática.

---

## 7. Gates de qualidade

| Gate | Mecanismo | Rigor |
|---|---|---|
| **Contrato & frescor** | fluxo/entrypoint/snapshot/escopo coincidem; artefato stale não herda aprovação | bloqueante |
| **Qualidade do grill** | pergunta cita gatilho real, jurisdição, impacto e critério; pergunta genérica/sem base ou respondível pelos artefatos ainda aberta | bloqueante |
| **Precisão** | citação aberta e validada semanticamente + jurisdição (§2, §4); presença de `arquivo:linha` sozinha não basta | bloqueante |
| **Completude estrutural** | IDs `PASSO/ARESTA/BRANCH/FRONTEIRA` do ledger cobertos OU fora-de-escopo | **bloqueante** |
| **Visão sistêmica** | fronteiras declaram falha, recuperação, ownership/observabilidade e compliance ou pendência explícita | **bloqueante por omissão** |
| **Completude por rubrica** | contrato, fluxo, erros, fronteiras, consistência, concorrência, resiliência, operação e compliance | consultivo |
| **Mermaid — prevenir** | subset seguro no style rule (só `flowchart`/`sequenceDiagram`, labels entre aspas, IDs alfanuméricos, sem `<>`/parênteses/HTML em nó) | — |
| **Mermaid — detectar** | skill `grill-mermaid` in-session: sintaxe + **escaping MDX** + **fidelidade ao grafo rastreado** | agora |
| **Mermaid — gate duro** | `docusaurus build` (build verde = renderiza) | *futuro, com o time* |
| **Revisão de deepening** | candidato exige evidência `arquivo:linha`, deletion test e conflito `ARC/CON/ADR`; interface só depois da escolha humana | bloqueante dentro do step opcional |

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
20. **Camada 0 elevada — Visão de Produto (`documentar-visao` + `grill-visao`):** uma visão progressiva para uma **PO nova** entender o domínio já observado, sem confundi-lo com o produto inteiro. Roda **por último** no track de negócio, liga somente docs aprovados e re-roda quando a cobertura cresce.
21. **Âncora de síntese + honestidade de cobertura (decisão inicial, refinada pela #24):** a visão ancora cada fluxo no **doc de negócio**, herda o "Em uma frase" sem reescrever e marca a síntese como `[inferido do código · a confirmar]`. A fórmula inicial `N de ~M` foi substituída por medidas dimensionais na decisão #24.
22. **Constituição operacional:** compromissos vigentes usam `ARC-###`; restrições usam `CON-###`; melhoria incompatível vira `DECISAO-PENDENTE-###`. O agente não ratifica mudança humana no silêncio.
23. **Identidade estável:** `ENTRY-###` (entrypoint candidato), `FLUXO-<slug>` (intenção confirmada), `PASSO/ARESTA/BRANCH/FRONTEIRA` (trace) e `NEG/VISAO` (claims) substituem comparação por semelhança textual.
24. **Cobertura dimensional:** visão publica `N` docs aprovados e `C/E` entrypoints cobertos separadamente. Módulo, entrypoint, fluxo e doc são unidades diferentes; o antigo `N de ~M fluxos/entrypoints` fica revogado.
25. **Gate persistente:** todo gate grava `.arquitetura/gates/*.md` no hash auditado. Etapa posterior falha fechada se aprovação, identidade ou frescor não puderem ser provados.
26. **Citação semântica:** gate abre o código e verifica se a linha sustenta verbo, condição e resultado. Uma coordenada existente, mas irrelevante, reprova.
27. **Arquitetura por fronteiras:** doc técnico explicita contrato, propagação de falha, consistência, concorrência, retry, recuperação, observabilidade, ownership, segurança e compliance; desconhecido explícito é aceitável, omissão silenciosa não.
28. **Snapshot verificável:** commit só prova conteúdo com working tree limpo. Em árvore alterada ou sem VCS, mapa/ledger guardam manifest de fingerprints dos arquivos inspecionados/citados; ausência ou divergência bloqueia o gate como `STALE`.
29. **Rubrica fixa, pergunta dinâmica:** os eixos arquiteturais garantem cobertura, mas cada pergunta nasce de um sinal concreto do projeto e usa `PERG-CTX/TEC/ARQ/NEG/VISAO-###`. Filas persistem em `.arquitetura/grills/`; pergunta genérica, sem gatilho ou ainda respondível pelos artefatos reprova o gate ou o critério de conclusão do step.
30. **Grill ≠ gate:** `bootstrap-contexto`, `documentar-*` e `revisar-arquitetura` geram e resolvem perguntas dinâmicas; os arquivos históricos chamados `grill-*` permanecem gates fixos e auditam a qualidade/ancoragem dessas perguntas.
31. **Revisão arquitetural é opcional e pós-gate:** `revisar-arquitetura` começa em um
    `FLUXO` tecnicamente aprovado (ou no conjunto de fluxos aprovados), encontra
    `OPORT-ARQ-###` por evidência e deletion test, mas não bloqueia publicação nem negócio.
32. **Escolha humana antes da interface:** relatório Before/After vem primeiro; só o
    candidato escolhido recebe grill `PERG-ARQ-###`, uma pergunta específica por vez.
    Rejeitar/adiar é decisão válida; código não muda nesse step.
33. **Adapter portátil, não acoplamento de runtime:** a semântica de
    `improve-codebase-architecture`, `codebase-design`, `grilling` e `domain-modeling` é
    encodada no prompt. O comportamento que dependia de subagente vira passes independentes
    na mesma sessão. O `CONTEXT.md` esperado é adaptado para o contexto canônico já
    existente, evitando uma segunda fonte de verdade. HTML fica em temp; ledger e decisões
    ficam em `.arquitetura/`.

---

## 9. Estado mecânico e itens em aberto

- **Docusaurus** — categorias da sidebar = as 6 camadas (§5); frontmatter com `sidebar_position`; mermaid via `@docusaurus/theme-mermaid`; mapa em `.arquitetura/mapa/` (fora de `docs/`); registro de divergências como doc própria em `Referência`.
- **Empacotamento por assistente** (triplo-write a partir de uma fonte canônica única = `prompts/*.md`; gerador `tools/empacotar.py` → `dist/`). Todos são **invocáveis (inclusão manual)**, não always-on — rodam em sequência, um por vez. Convenções **confirmadas nos docs/fonte oficiais (2026-07)**:
  - `.amazonq/prompts/<nome>.md` — Markdown puro, **sem frontmatter**; invoca `@<nome>` no `q chat` (pasta do projeto é **CLI-only**; o IDE lê só `~/.aws/amazonq/prompts/`).
  - `.github/prompts/<nome>.prompt.md` — frontmatter `agent: 'agent'` + `description` (`mode` foi **depreciado** → `agent`); invoca `/<nome>` no Copilot Chat.
  - `.kiro/steering/<nome>.md` — frontmatter `inclusion: manual`; referencia `#<nome>`.
  - _As always-on (`.amazonq/rules/*`, `.github/instructions/* applyTo:"**"`, `inclusion: always`) NÃO servem para invocável e ficam para uma futura regra always-on separada, se um run real exigir — hoje o princípio-norte vai embutido em cada prompt._
- **Schema do mapa** — `_indice.md` (árvore L0-L1 + cobertura estrutural por módulo + inventário `ENTRY-###`) + um arquivo por módulo top-level (L2-L4) + ledger por `FLUXO-<slug>`; status de nó `esqueleto → inferido → verificado | corrigido`, marcador `stale` e carimbo commit/hash.
- **Schema do grill** — `.arquitetura/grills/` guarda filas específicas por contexto,
  fluxo técnico, oportunidade arquitetural, fluxo de negócio e visão. Cada pergunta contém
  gatilho, jurisdição, impacto, critério de encerramento, derivação, estado e
  resposta/evidência. O grill arquitetural acrescenta recomendação e avança uma pergunta
  por vez.
- **Schema da revisão** — `.arquitetura/revisoes/arquitetura.<escopo>.md` guarda snapshot,
  fontes de domínio/ADRs, `OPORT-ARQ-###`, resultado do deletion test, força, escolha
  humana e blueprint. O HTML `architecture-review-<timestamp>.html` é projeção visual
  efêmera desse ledger, em `$TMPDIR`/`/tmp`.
- **Inventário de prompts:**
  - **Track técnico (construído):** `bootstrap-contexto` · `mapear-estrutura` · `documentar-fluxo` · `grill-doc` · `grill-mermaid`
  - **Revisão arquitetural opcional (construída):** `revisar-arquitetura` — exploração
    orgânica + relatório visual + escolha humana + grill específico + blueprint, sem código.
  - **Track de negócio (construído):** `contexto-produto` (lente de PO) · `documentar-negocio` (a joia de negócio) · `grill-negocio` (gate) → doc em `docs/00-dominio/fluxos-negocio/<slug>.md`
  - **Camada 0 · Visão de Produto (construído):** `documentar-visao` (overview de app; cita o "Em uma frase" de cada fluxo + mapa de cobertura honesto) · `grill-visao` (gate: âncora + zero-jargão + **mapa-fiel**) → doc em `docs/00-dominio/visao-de-produto.md`
  - **Geradores por tipo de doc (a construir):** `glossario` · `restricoes` · `regras` · `estrutura` · `topologia` · `runbook` · `adr` · `rastreabilidade`

---

## 10. Leitura pelos pilares arquiteturais

| Pilar | Como aparece nos prompts |
|---|---|
| **Lealdade arquitetural** | `ARC-###` preserva compromisso vigente; mudança incompatível vira `DECISAO-PENDENTE-###`. |
| **Modelagem de domínio** | Bootstrap captura vocabulário, atores, invariantes e casos-limite; contexto-produto cria `PER/JOB/TERMO/REGRA`; revisão atualiza o glossário canônico quando o humano resolve um termo. |
| **Pensamento sistêmico** | Trace explicita `FRONTEIRA-###`, falha, consistência, recuperação, ownership, observabilidade e blast radius. |
| **Navegação de restrições** | `CON-###` registra tipo, rigidez, aprovação e consequência; o agente não decide política/compliance. |
| **Decomposição AI-aware** | Cada prompt tem precondição, escopo de escrita, IDs estáveis e saída verificável; grills transformam sinais do projeto em perguntas atômicas com critério de encerramento; revisão separa explorar, escolher, aprofundar e implementar. |
| **AI-first pragmático** | Arquivos persistem contexto/gates/decisões entre sessões; o relatório visual é projeção efêmera; não se adiciona parser, subagente ou serviço que rompa a portabilidade sem ganho provado. |

## 11. Próximos passos

1. Reexecutar o piloto depth-first com os contratos atuais, incluindo uma revisão
   arquitetural do fluxo aprovado, e comparar taxa de bloqueio, qualidade dos candidatos,
   pendências descobertas e cobertura `C/E` com a baseline histórica.
2. Ratificar os defaults ainda abertos do §9, em especial Docusaurus/build-gate.
3. Construir os geradores por tipo de doc sem romper a constituição operacional.
