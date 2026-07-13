---
inclusion: manual
---

# Prompt · `revisar-arquitetura`

> Step opcional de evolução arquitetural. Portável (Amazon Q / Copilot / Kiro),
> **standalone**, sem subagente e sem parser. Roda depois dos dois gates técnicos de
> pelo menos um fluxo e não altera código.

Você encontra oportunidades reais de aprofundar **modules**, apresenta um relatório visual,
espera o humano escolher uma oportunidade e só então conduz um grill específico do
projeto. O resultado é uma decisão arquitetural verificável — nunca um refactor automático.

## Contrato de execução

- Escopo obrigatório: um `FLUXO-<slug>` aprovado ou `projeto` (todos os fluxos técnicos
  aprovados). Se o usuário não informar e houver um único fluxo aprovado, use-o; se
  houver vários, liste os IDs reais e peça uma escolha antes de explorar.
- Insumos mínimos: `.arquitetura/contexto.md`, mapa/ledger, doc técnico e
  `.arquitetura/gates/grill-doc.<slug>.md` +
  `.arquitetura/gates/grill-mermaid.<slug>.md` aprovados no mesmo **snapshot**.
- Leia também `CONTEXT-MAP.md`/`CONTEXT.md`, se existirem, e os ADRs aplicáveis nas
  convenções encontradas no repositório (por exemplo, `docs/adr/`).
- Pode escrever somente:
  - `.arquitetura/revisoes/arquitetura.<escopo>.md`;
  - `.arquitetura/grills/arquitetura.<escopo>.<OPORT-ID>.md`;
  - o glossário/contexto canônico, somente quando uma decisão humana de domínio
    cristalizar;
  - um ADR, somente depois de oferecer e receber aprovação humana explícita.
- O relatório HTML vai para o diretório temporário do sistema, nunca para o repositório.
- Não altera código, testes, interfaces nem docs publicadas. Uma implementação posterior
  exige outro plano e aprovação.
- Insumo ausente, gate reprovado ou snapshot divergente produz `BLOQUEADO-PRECONDICAO`.

## Vocabulário obrigatório

Use estes termos exatamente nas sugestões e no relatório:

- **module** — algo com uma **interface** e uma implementação;
- **interface** — tudo que o chamador precisa saber, incluindo invariantes, ordem,
  erros, configuração e desempenho;
- **depth** — leverage entregue por unidade de interface;
- **deep** / **shallow** — muita ou pouca implementação útil atrás da interface;
- **seam** — lugar onde o comportamento pode variar sem editar o chamador;
- **adapter** — implementação concreta que ocupa uma seam;
- **leverage** — capacidade entregue aos chamadores por uma interface pequena;
- **locality** — mudança, conhecimento, bugs e verificação concentrados.

Não substitua esses termos por “component”, “service”, “API” ou “boundary” quando estiver
falando da arquitetura. Nomes literais do código podem ser citados na lista de arquivos.
`FRONTEIRA-###` continua sendo a identidade de uma dependência externa no trace; **seam**
é o lugar arquitetural e não é sinônimo dessa identidade.

Princípios:

- **deletion test:** imagine remover o module. Se a complexidade reaparece espalhada nos
  chamadores, ele concentra complexidade e ganha depth; se a complexidade desaparece ou
  era só repasse, ele é shallow;
- **the interface is the test surface:** chamadores e testes atravessam a mesma seam;
- **one adapter = hypothetical seam; two adapters = real seam:** não crie indirection sem
  variação concreta.

## Adapter de portabilidade e domínio

Este prompt encoda o comportamento de revisão, grilling, modelagem de domínio e design
de modules; não invoca skills externas. A exploração é feita nesta sessão, organicamente,
porque subagentes não existem no menor denominador comum dos três runtimes.

O `CONTEXT.md` esperado pela disciplina de modelagem tem um adapter para a constituição
já existente:

1. Se `CONTEXT-MAP.md` ou `CONTEXT.md` existir, ele é o glossário canônico.
2. Caso contrário, o “Modelo de domínio” de `.arquitetura/contexto.md` é o canônico; não
   crie uma segunda fonte de verdade apenas para satisfazer outro nome de arquivo.
3. `.arquitetura/contexto-produto.md`, se existir, complementa a linguagem com
   `PER/JOB/TERMO/REGRA`, sem substituir a fonte canônica.

Preserve `ARC-###` e `CON-###`. Sugestão incompatível vira
`DECISAO-PENDENTE-###`, nunca decisão silenciosa. Um ADR existente não é reaberto por
preferência teórica; só aparece quando há fricção comprovada forte o bastante.

## Retomada segura

Antes de começar, procure `.arquitetura/revisoes/arquitetura.<escopo>.md`:

- mesmo snapshot + `AGUARDANDO-ESCOLHA`: regenere o HTML a partir do ledger se o arquivo
  temporário sumiu, apresente os candidatos e espere a escolha;
- mesmo snapshot + `APROFUNDANDO`: abra o grill escolhido e retome a primeira
  `PERG-ARQ-###` aberta;
- `CONCLUIDA`, `REJEITADA` ou `SEM-CANDIDATO`: mostre o resultado e só inicie nova rodada
  com solicitação explícita;
- snapshot diferente: marque o ledger `STALE` e reexplore; não herde candidatos nem
  decisões factuais do código anterior.

## Fase 1 · Explore organicamente

Comece no trace aprovado do escopo e caminhe pelo código real. Expanda para modules
adjacentes somente quando uma chamada, dependência, teste ou vazamento pela seam exigir.
Não aplique uma lista rígida nem transforme as lentes abaixo em achados automáticos.

Durante a leitura, registre onde você de fato sentiu fricção:

- entender um conceito do domínio exige saltar entre muitos modules pequenos;
- um module é shallow porque sua interface se aproxima da implementação;
- lógica foi extraída só para teste, mas os bugs vivem na forma como os chamadores a
  coordenam e não há locality;
- detalhes vazam por uma seam e acoplam modules;
- testes atravessam a interface, verificam detalhes internos ou não cobrem o ponto onde
  o comportamento real se compõe.

Para cada suspeita, abra os corpos relevantes, testes e chamadores; aplique o deletion
test e cite `arquivo:linha`. Um padrão genérico sem evidência do projeto não é candidato.

Classifique dependências do possível module aprofundado:

1. `in-process` — computação/estado local; sem adapter;
2. `local-substitutable` — substituto local real; seam interna;
3. `ports & adapters` — dependência remota controlada; port na seam e pelo menos um
   adapter de produção + um de teste;
4. `mock` — dependência externa não controlada; port injetado + mock adapter em testes.

## Fase 2 · Forme candidatos evidenciados

Crie `OPORT-ARQ-###` somente quando houver evidência suficiente. Cada candidato contém:

- nome no vocabulário do domínio e files/modules envolvidos;
- problema observado e evidências `arquivo:linha`;
- resultado do deletion test;
- classificação da dependência e adapters que tornam a seam real;
- solução em linguagem simples, sem propor uma interface ainda;
- ganhos em locality, leverage e testes pela interface;
- conflitos com `ARC/CON/ADR` e `DECISAO-PENDENTE-###`, se aplicável;
- força `Strong`, `Worth exploring` ou `Speculative`, justificada pela evidência.

Prefira poucos candidatos distintos e fortes. Não crie variações cosméticas do mesmo
deepening. Se nenhum sobreviver ao deletion test, registre `SEM-CANDIDATO`; isso é um
resultado válido.

## Ledger persistente

Antes do HTML, grave `.arquitetura/revisoes/arquitetura.<escopo>.md`:

```md
# Revisão de arquitetura — <escopo>
> Snapshot: <commit:hash|manifest:digest> · executado em <data-hora>
> Status: AGUARDANDO-ESCOLHA / APROFUNDANDO / CONCLUIDA / REJEITADA / SEM-CANDIDATO / STALE
> Relatório temporário: <caminho absoluto ou ausente>

## Fontes de domínio e decisões lidas
- <contextos, ARC-###, CON-### e ADRs aplicáveis>

## Candidatos
### OPORT-ARQ-001 — <nome do deepening>
- Força: Strong / Worth exploring / Speculative
- Files/modules: <lista>
- Problema + evidência: <arquivo:linha>
- Deletion test: <resultado>
- Dependência/adapters: <categoria + evidência>
- Solução: <sem interface proposta>
- Locality/leverage/testes: <ganhos>
- Compromissos: <preservados/conflitos/DECISAO-PENDENTE>
- Estado humano: não escolhido / escolhido / rejeitado / adiado

## Top recommendation
- <OPORT-ID + porquê>

## Decisão humana
- Escolha: <pendente|OPORT-ID|nenhuma>
- Rationale atribuído: <quem, quando, verbatim ou pendente>
```

## Fase 3 · Relatório visual temporário

Resolva o diretório por `$TMPDIR`; se vazio, use `/tmp` em Unix/macOS ou `%TEMP%` no
Windows. Grave um arquivo novo em
`<tmpdir>/architecture-review-<timestamp>.html` e registre o caminho absoluto no ledger.

O HTML é um único arquivo self-contained e estático. Carregue Tailwind com
`https://cdn.tailwindcss.com` e Mermaid com
`https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`; inicialize Mermaid
com `startOnLoad: true`, tema `neutral` e `securityLevel: loose`. Inclua CSS local mínimo
para que o conteúdo textual continue legível se a rede estiver indisponível. Abra com
`open <path>` no macOS, `xdg-open <path>` no Linux ou `start <path>` no Windows; se não
puder abrir, informe o caminho absoluto sem tratar isso como falha da análise.

O relatório começa direto nos candidatos e contém:

- projeto, data e legenda: caixa sólida = module, linha tracejada = seam, seta vermelha =
  leakage, caixa escura espessa = deep module;
- um card por `OPORT-ARQ-###` com Files, Problem, Solution, Benefits, badge de dependência,
  força de recomendação e conflito de ADR quando aplicável;
- visualização **Before / After** lado a lado para cada candidato, usando Mermaid quando
  relações forem grafo/fluxo e HTML/SVG para depth, massa ou colapso;
- wins de até seis palavras usando locality, leverage e interface;
- uma seção final **Top recommendation**.

Os diagramas carregam a explicação; mantenha-os perto de 320px de altura e não use
parágrafos longos para compensar visual ruim. Use a linguagem do domínio canônico: nomeie
o module pelo conceito que ele representa, não pelo nome acidental de um handler. Não
proponha interfaces nesta fase.

## Checkpoint humano obrigatório

Depois de gravar e abrir o relatório, apresente os IDs e títulos reais e pergunte apenas:

> **Qual dessas oportunidades você quer explorar? / Which of these would you like to explore?**

Espere a resposta. Não escolha pelo humano e não continue para interfaces, migração ou
implementação antes da escolha. `nenhuma`, rejeição ou adiamento são respostas válidas e
devem ser persistidas com rationale atribuído quando fornecido.

## Fase 4 · Grill dinâmico do candidato escolhido

Ao receber a escolha, marque o ledger `APROFUNDANDO` e crie
`.arquitetura/grills/arquitetura.<escopo>.<OPORT-ID>.md`.

Não use **perguntas prontas**. Gere cada `PERG-ARQ-###` a partir de um sinal concreto do
candidato, faça **uma pergunta por vez**, inclua sua resposta recomendada e espere o
feedback antes da próxima. Se o código ou os artefatos puderem responder, explore-os em
vez de perguntar. O humano responde domínio, prioridade, restrição e trade-off.

Formato persistente:

```md
# Grill de arquitetura — <OPORT-ID>
> Escopo/snapshot: <escopo> · <snapshot>

## Cobertura das lentes
| Lente | Sinal específico | Estado | PERG-ARQ relacionada |
|---|---|---|---|
| problema de domínio | <sinal/não acionada + evidência> | <estado> | <ID/—> |
| restrições e compromissos | <CON/ARC/ADR> | <estado> | <ID/—> |
| dependencies e failure modes | <sinal> | <estado> | <ID/—> |
| depth/interface/seam/adapters | <sinal> | <estado> | <ID/—> |
| locality/leverage e testes | <sinal> | <estado> | <ID/—> |
| migração, reversão e operação | <sinal> | <estado> | <ID/—> |
| checkpoint e autoridade humana | <decisor> | <estado> | <ID/—> |

## Perguntas
| ID | Pergunta | Gatilho/evidência | Jurisdição | Recomendação | Por que importa | Critério de encerramento | Derivada de | Estado | Resposta/decisão |
|---|---|---|---|---|---|---|---|---|---|
| `PERG-ARQ-001` | <uma pergunta específica> | <arquivo:linha/ARC/CON/ADR/ausência concreta> | código/humano/mista | <resposta recomendada + trade-off> | <impacto> | <evidência/decisão que encerra> | `OPORT-ARQ-###` | aberta/respondida/bloqueada | <base/verbatim> |
```

As lentes garantem cobertura, mas não são um questionário. Marque uma lente não acionada
com evidência; não fabrique pergunta para preencher tabela.

## Modelagem de domínio e ADRs durante o grill

- Termo novo ou ambíguo resolvido: atualize imediatamente o contexto canônico definido
  no adapter acima. Glossário contém linguagem do domínio, nunca detalhe de implementação.
- Conflito entre fala, glossário e código: exponha a divergência; não normalize em silêncio.
- Candidato rejeitado por razão load-bearing: ofereça
  “Quer que eu registre isso como ADR para futuras revisões não sugerirem de novo?”.
- Só crie ADR quando a decisão for difícil de reverter, surpreendente sem contexto e
  resultado de trade-off real. Razão temporária como “não agora” não vira ADR.

## Interfaces alternativas — somente depois da escolha

Se o humano quiser comparar interfaces, faça três passes independentes, cada um com forma
radicalmente diferente: (1) interface mínima com 1–3 entradas, (2) flexibilidade para
casos variados, (3) caso comum trivial; acrescente uma alternativa `ports & adapters`
quando a dependência justificar.

Cada alternativa declara interface completa, exemplo de uso, implementação escondida,
seam/adapters e trade-offs. Compare por depth, locality, leverage e seam placement; dê
uma recomendação opinativa. Esta sequência é o adapter portátil do design-it-twice: não
usa subagentes e deixa essa limitação explícita no ledger.

## Blueprint final

Quando todas as perguntas acionadas estiverem encerradas e a escolha humana estiver
explícita, complete o ledger com:

- problema de domínio, objetivo e não-objetivos;
- module a aprofundar, interface escolhida (se discutida) e implementação escondida;
- seam, dependências, adapters e failure/recovery;
- como testes passam a usar a interface e quais testes shallow serão substituídos;
- tarefas atômicas, verificáveis e reversíveis para uma implementação futura;
- `ARC/CON/ADR` preservados e `DECISAO-PENDENTE` restantes;
- decisor, aprovação, riscos, observabilidade e rollback;
- recomendação `IMPLEMENTAR`, `NÃO IMPLEMENTAR` ou `ADIAR`, com rationale.

Marque `CONCLUIDA` somente após o checkpoint humano. O blueprint não autoriza alteração
de código.

## Critério de conclusão

- Escopo, gates e snapshot foram verificados; drift não herdou conclusões.
- Todo `OPORT-ARQ-###` tem evidência do projeto, deletion test, força e conflito explícito.
- O relatório HTML temporário contém cards, Before/After e Top recommendation, e seu
  caminho absoluto está no ledger.
- Nenhuma interface foi proposta antes da escolha humana.
- O grill usa `PERG-ARQ-###` específicas, uma por vez, com Gatilho, Jurisdição,
  Recomendação, Por que importa, Critério de encerramento, Derivada de e Estado.
- A Cobertura das lentes não virou perguntas estáticas.
- Decisões de domínio/ADR foram persistidas somente com autoridade humana.
- Código e docs publicadas permaneceram inalterados.

## Handoff

- **AGUARDANDO-ESCOLHA:** `Relatório de arquitetura aberto em <caminho absoluto> e ledger gravado em .arquitetura/revisoes/arquitetura.<escopo>.md. Escolha um OPORT-ARQ-### para continuar nesta sessão.`
- **CONCLUIDA:** `Revisão arquitetural concluída sem alterar código. Blueprint gravado em .arquitetura/revisoes/arquitetura.<escopo>.md. Próximo passo opcional: planejar a implementação; para documentação de produto, rode contexto-produto.`
- **SEM-CANDIDATO/REJEITADA/ADIADA:** `Revisão encerrada com o estado <estado> e rationale persistido. Para documentação de produto, rode contexto-produto.`
- **BLOQUEADO-PRECONDICAO:** `Resolva gates, escopo ou drift de snapshot antes de revisar a arquitetura.`
