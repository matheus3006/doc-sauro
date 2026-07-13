---
inclusion: manual
---

# Prompt · `bootstrap-contexto`

> Passo 0 da trilha de documentação de arquitetura. Portável: roda em Amazon Q,
> GitHub Copilot ou Kiro — **standalone**, sem subagente, sem parser/ctags/tree-sitter.
> Leitura **LLM-native**.

Você produz `.arquitetura/grills/contexto.md` e `.arquitetura/contexto.md`: detecta o que
o repositório comprova sem abrir corpos de método, gera perguntas específicas a partir
desses sinais e pede ao humano apenas o que domínio, operação e organização respondem.

## Contrato de execução

- **Escopo:** um repositório, executado a partir da raiz.
- **Pode escrever:** somente `.arquitetura/grills/contexto.md` e
  `.arquitetura/contexto.md`.
- **Não pode:** alterar código, escolher arquitetura nova, ratificar decisão humana ou
  afirmar comportamento de runtime.
- **Pré-condição:** a raiz deve ser identificável por manifestos, VCS ou estrutura.
  Se houver mais de uma raiz plausível, pare com `BLOQUEADO` e liste as candidatas.
- **Checkpoint humano obrigatório:** faça todas as perguntas de elicitação em um único
  bloco e **pare**. Só grave depois da resposta. Se o humano disser que um item é
  desconhecido/indisponível, registre `[PENDENTE: ...]`; silêncio não é resposta.

## Princípio-norte e jurisdição

> O mapa e o depoimento humano são hipóteses — nunca viram citação sobre o que o código
> faz. A única fonte citável sobre comportamento é o próprio código (`arquivo:linha`).

- **Extração:** stack e estrutura vêm de arquivos; cada afirmação aponta a evidência.
- **Elicitação:** propósito, domínio, operação, restrições e compromissos vêm do humano;
  registre **verbatim + quem + quando**.
- **Inferência estrutural:** convenção de nome/pasta pode sugerir um papel, mas entra
  `[inferido]`. Neste passo, nenhuma inferência descreve comportamento.
- **Conflito:** não escolha um lado em silêncio. Registre a divergência e sua jurisdição.

## Fase 1 · Extração barata, sem corpo de método

1. Liste a árvore até 2–3 níveis. Ignore `.git`, dependências, caches e artefatos de
   build (`node_modules`, `target`, `dist`, `build`, `.next`, `vendor`, `venv`,
   `__pycache__`).
2. Determine stack e tooling apenas por manifestos/sinais explícitos (`package.json`,
   `pom.xml`, `build.gradle`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `*.csproj`,
   `Dockerfile`, arquivos de CI etc.). Cada item aponta o arquivo que o comprova.
3. Liste módulos top-level e tipos de entrypoint visíveis por convenção: HTTP,
   consumidor/listener, job, CLI, evento ou outro. Marque o papel `[inferido]`.
4. Registre sinais de fronteira do sistema sem afirmar uso em runtime: SDKs, drivers,
   manifests de infraestrutura e configurações de rede/fila/banco. Tudo como
   `candidato [inferido]`, com evidência.
5. Registre o commit/hash atual e se há working tree alterado. Commit identifica conteúdo
   apenas com árvore limpa. Sem VCS ou com árvore alterada, declare que etapas com
   citações deverão guardar fingerprint dos arquivos lidos; nunca invente frescor.

**Concluído quando:** Stack, Estrutura e Fronteiras candidatas têm evidência e não há
afirmação de comportamento.

## Fase 2 · Gere a elicitação específica deste projeto

As dez dimensões de cobertura são lentes, não perguntas prontas:

`propósito/sucesso` · `usuários` · `vocabulário/invariantes` · `casos-limite` ·
`tier/blast radius` · `fronteiras/ownership` · `operabilidade` · `restrições` ·
`compromissos/exceções` · `decisores`.

### 2.1 · Cruze lentes com os sinais extraídos

Para cada lente, use nome do projeto, módulos, entrypoints candidatos, SDKs, bancos,
filas, manifests, CI e ausências materiais observadas. Gere `PERG-CTX-###` que mencione
esses elementos. Se não houver sinal positivo, a própria ausência inspecionada pode ser
o gatilho: “não encontrei owner/runbook nos caminhos X/Y” é específico; “quem monitora?”
isoladamente não é.

É proibido copiar perguntas genéricas como “qual é o propósito?”, “quais são as
restrições?” ou “quem aprova?”. Exemplo válido:

> `PERG-CTX-004` — O repositório `<nome>` declara `<SDK>` em `<manifesto>` e um consumer
> em `<módulo>`; esse fornecedor é uma fronteira crítica do fluxo ou apenas tooling? Quem
> é dono do contrato e qual resultado precisa sobreviver se ele ficar indisponível?

### 2.2 · Registre e resolva a fila

Grave `.arquitetura/grills/contexto.md` antes de perguntar:

```md
# Grill de contexto — <projeto>
> Frescor: <snapshot/estado da árvore> · Derivado da extração deste repositório

## Cobertura das lentes
| Lente | Sinais concretos inspecionados | Estado | Perguntas |
|---|---|---|---|
| <lente> | <módulos/manifests/fronteiras/ausências> | acionada / não acionada com evidência | `PERG-CTX-###` / — |

## Perguntas específicas
| ID | Pergunta | Gatilho/evidência | Jurisdição | Por que importa | Critério de encerramento | Derivada de | Estado | Resposta |
|---|---|---|---|---|---|---|---|---|
| `PERG-CTX-001` | <pergunta que nomeia este projeto> | <arquivo/módulo/ausência inspecionada> | arquivo/humano | <impacto> | <evidência/decisão> | — | aberta / resolvida / aguardando-humano / descartada | <verbatim + quem/quando> |
```

Resolva primeiro perguntas de jurisdição `arquivo`. Depois apresente em um único bloco
somente as perguntas humanas abertas, com seus IDs, contexto e impacto, e **pare**. Ao
receber respostas, preserve verbatim; ambiguidade relevante gera pergunta filha com novo
ID. Atualize o arquivo do grill antes de cada espera e depois de cada resposta, para a
fila não depender da memória do chat. Não transforme resposta em “boa prática”. Melhoria possível vira
`DECISAO-PENDENTE-###`, nunca compromisso vigente.

Uma lente pode ficar `não acionada` apenas com a evidência do que foi inspecionado. Não
gere pergunta artificial nem use resposta genérica para completar cobertura.

## Fase 3 · Grave `.arquitetura/contexto.md`

Use esta estrutura. IDs são estáveis: preserve-os em reexecuções; acrescente novos no
fim e nunca renumere itens já referenciados.

```md
# Contexto — <projeto>
> Interno. Extração tem evidência; elicitação é atribuída.
> Frescor: <data-hora> · commit <hash|indisponível> · working tree <limpo|alterado|desconhecido>
> Política de snapshot: commit limpo OU fingerprint por arquivo citado

## Stack
- <linguagem/framework/runtime> — evidência: `<arquivo>`

## Estrutura
- Raiz do código: `<path>`
- Módulos top-level:
  - `<módulo>` — entrypoints candidatos: <tipos> `[inferido]` — evidência: `<path>`

## Fronteiras candidatas (extração; ainda não provam runtime)
| ID | Candidato | Tipo | Evidência | Estado |
|---|---|---|---|---|
| `FRONTEIRA-CAND-001` | <sistema/SDK> | <rede/banco/fila/fs/...> | `<arquivo>` | `[inferido]` |

## Modelo de domínio (atribuído)
- **Propósito e sucesso:** "<verbatim>" — <quem>, <quando>
- **Usuários/atores:** "<verbatim>" — <quem>, <quando>
- **Termos:** "<verbatim>" — <quem>, <quando>
- **Invariantes:** "<verbatim>" — <quem>, <quando>
- **Casos-limite:** "<verbatim>" — <quem>, <quando>

## Sistema e operação (atribuído)
- **Tier / impacto:** "<verbatim>" — <quem>, <quando>
- **Blast radius / recuperação:** "<verbatim>" — <quem>, <quando>
- **Upstream / downstream / ownership:** "<verbatim>" — <quem>, <quando>
- **Sinais / alertas / SLO / runbook:** "<verbatim>" — <quem>, <quando>

## Restrições
| ID | Tipo | Restrição (verbatim) | Fixa/negociável | Aprovação | Consequência | Fonte |
|---|---|---|---|---|---|---|
| `CON-001` | técnica/organizacional/negócio/compliance/política | <texto> | <estado> | <quem> | <efeito> | <quem, quando> |

## Constituição arquitetural
| ID | Compromisso vigente | Rationale/fonte | Como pode mudar | Estado |
|---|---|---|---|---|
| `ARC-001` | <contrato/padrão a preservar> | <quem/artefato> | <aprovação necessária> | ratificado / pendente |

## Exceções ao padrão
- <verbatim> — <quem>, <quando>

## Decisores e revisão humana
- Contexto: <quem> · Autoridade: <quem> · Revisão da doc: <quem>

## Pendências e divergências
- `[PENDENTE: PERG-CTX-### — <pergunta concreta> · dono: <quem|desconhecido>]`
- `DECISAO-PENDENTE-001` — <melhoria/trade-off a decidir; não ratificada>
```

Para qualquer campo sem resposta explícita, use `[PENDENTE: pergunta · dono]`. Não use
“N/A” a menos que o humano tenha confirmado que não se aplica.

## Critério de conclusão

- `.arquitetura/grills/contexto.md` e `.arquitetura/contexto.md` existem e registram frescor.
- Toda `PERG-CTX-###` nomeia sinais/ausências reais do projeto, possui gatilho,
  jurisdição, impacto e critério de encerramento; zero pergunta estática copiada da lente.
- Perguntas de arquivo estão resolvidas; humanas abertas viram `[PENDENTE]` com dono/impacto.
- As 10 lentes estão acionadas ou não acionadas com evidência.
- Stack, módulos e fronteiras candidatas têm evidência; papéis inferidos estão marcados.
- As respostas necessárias ao contexto estão atribuídas ou `[PENDENTE]`.
- Restrições usam `CON-###` e distinguem fixa/negociável e aprovação, mesmo que pendente.
- Compromissos vigentes usam `ARC-###`; melhorias não aprovadas usam
  `DECISAO-PENDENTE-###`.
- Zero afirmação de comportamento do código.

## Handoff

Imprima literalmente:

> Grill específico gravado em `.arquitetura/grills/contexto.md` e contexto em `.arquitetura/contexto.md`. Pendências humanas: <n>. Próximo passo: rode **`mapear-estrutura`** na raiz do repositório.
