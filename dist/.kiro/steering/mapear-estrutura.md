---
inclusion: manual
---

# Prompt · `mapear-estrutura`

> Passo 1 da trilha. Portável (Amazon Q / Copilot / Kiro), **standalone**, sem
> subagente, sem parser/ctags/tree-sitter. Leitura **LLM-native**. Roda uma vez por
> projeto, depois de `bootstrap-contexto`.

Você semeia `.arquitetura/mapa/`: um mapa interno, nível-declaração, que localiza o
sistema e mantém o ledger entre sessões. Aqui também nasce o inventário de entrypoints
candidatos — a unidade correta para medir cobertura sem confundir módulo com fluxo.

## Contrato de execução

- **Pode ler:** `.arquitetura/contexto.md`, árvore, manifestos e declarações/assinaturas.
- **Pode escrever:** somente `.arquitetura/mapa/`.
- **Não pode:** abrir corpo de método, afirmar comportamento, alterar código ou criar
  fluxo de negócio por inferência.
- **Pré-condição:** `.arquitetura/grills/contexto.md` e `.arquitetura/contexto.md`
  existem, compartilham frescor e identificam uma raiz única. Toda `PERG-CTX-###` de
  jurisdição `arquivo` está resolvida; pendência humana está refletida no contexto. Se
  faltar ou houver pergunta genérica/sem gatilho, pare `BLOQUEADO`. Se o snapshot mudou,
  marque o mapa anterior `stale`; nunca reutilize frescor antigo.
- **Snapshot:** commit só basta com árvore limpa. Em árvore alterada/sem VCS, crie um
  manifest com fingerprint dos arquivos de declaração inspecionados e use
  `manifest:<digest>` como Snapshot-ID do mapa.

## Princípio-norte e compromissos

> O mapa é hipótese e nunca é citado como prova de comportamento. Código aberto no
> ponto exato é a única evidência comportamental.

- Preserve todos os `ARC-###` e `CON-###` do contexto. Se a estrutura observada parece
  contrariá-los, registre uma divergência; não “corrija” o compromisso.
- Todo papel deduzido de nome, pasta, annotation ou assinatura recebe `[inferido]`.
- IDs são persistentes: nunca renumere `ENTRY-###` porque outro artefato pode referi-los.

## Unidades do mapa

- **Módulo:** unidade estrutural top-level.
- **`ENTRY-###`:** entrypoint candidato observável por declaração (rota/handler,
  listener/consumer, job, CLI, evento etc.). É hipótese até o corpo ser rastreado.
- **`FLUXO-<slug>`:** intenção ponta-a-ponta confirmada pelo humano e rastreada depois.
  Um fluxo pode começar em mais de um entrypoint; um entrypoint pode participar de mais
  de um fluxo. Por isso `ENTRY` e `FLUXO` nunca são contados como sinônimos.

Status de nó: `esqueleto → inferido → verificado | corrigido`; `stale` é um marcador
ortogonal de frescor. Status de entrypoint: apenas `candidato → confirmado`. Aprovação
pertence à relação `FLUXO ↔ ENTRY + gate`, não ao entrypoint isolado: um mesmo entrypoint
pode iniciar fluxos com maturidades diferentes.

## Fase 1 · Árvore e cobertura estrutural

1. Leia o contexto inteiro, inclusive modelo de domínio, restrições e constituição.
2. Monte árvore L0–L1: repo, módulos top-level e um nível de submódulo.
3. Crie uma linha de cobertura estrutural por módulo. Essa tabela responde “que parte do
   código foi tocada?”, não “quantos fluxos existem?”.

## Fase 2 · Inventário barato de entrypoints candidatos

Examine nomes, pastas, annotations e assinaturas, sem corpo. Liste cada entrypoint
candidato com localização exata. Se duas declarações parecem o mesmo entrypoint, não
mescle sem prova; registre relação provável. Se uma rota é gerada dinamicamente e não
pode ser enumerada, crie uma linha `ENTRY-DINAMICO-###` e declare a limitação.

Para cada candidato, registre:

- ID estável `ENTRY-###`;
- tipo e localização (`arquivo:linha` da declaração quando disponível);
- nome provável no domínio, sempre `[inferido]`;
- módulo proprietário e interface/contrato visível na assinatura;
- status e documentos associados, inicialmente vazios.

Esse inventário é deliberadamente nível-declaração. Ele fornece o denominador `E` de
entrypoints conhecidos; não promete conhecer todos os fluxos de negócio.

## Fase 3 · Stubs por módulo, lazy

Crie stub detalhado apenas para o módulo do próximo fluxo, se ele for conhecido. Os
demais nascem no primeiro toque. O stub lista unidades L2 visíveis, papéis `[inferido]`
e a nota de que assinaturas/arestas profundas serão preenchidas por fluxo. Não enumere
o repositório inteiro por zelo aparente.

## Forma dos arquivos

`.arquitetura/mapa/_indice.md`:

```md
# Mapa — índice
> Interno. Hipótese/ledger; NUNCA citado como prova de comportamento.
> Frescor: <data-hora> · Snapshot: `commit:<hash>` / `manifest:<digest>` · working tree <estado>

## Árvore L0-L1
- <repo>
  - `<módulo>/`

## Cobertura estrutural (módulos)
| Módulo | Papel `[inferido]` | Status | Fluxos que tocaram | Frescor |
|---|---|---|---|---|
| `<módulo>` | <papel> | esqueleto | — | <hash> |

## Inventário de entrypoints candidatos
| ID | EntryPoint / declaração | Tipo | Módulo | Hipótese de domínio | Status | Fluxos/docs/gates associados | Frescor |
|---|---|---|---|---|---|---|---|
| `ENTRY-001` | `<arquivo:linha>` | HTTP/fila/job/CLI/evento/outro | `<módulo>` | <nome> `[inferido]` | candidato | — | <hash> |

## Limitações do inventário
- <entrypoints dinâmicos, geração de código, módulos não inspecionáveis etc.>

## Divergências com contexto/constituição
- <observação × `ARC-###`/`CON-###`, sem resolver em silêncio; ou "nenhuma">
```

`.arquitetura/mapa/<módulo>.md`:

```md
# Mapa — módulo `<módulo>`
> Nível-declaração. Aprofundamento lazy por fluxo. Frescor: <hash>

## Unidades
- `<Unidade>` — papel: <papel> `[inferido]` — status: esqueleto

## Entrypoints
- `ENTRY-###` — `<declaração arquivo:linha>` — status: candidato

## Assinaturas e arestas
- Enchem lazy quando um fluxo passar por aqui.
```

## Critério de conclusão

- `_indice.md` existe, registra snapshot verificável e separa cobertura estrutural de inventário de
  entrypoints.
- Todos os módulos top-level aparecem na tabela estrutural.
- Cada entrypoint observável tem ID estável, evidência de declaração e hipótese marcada.
- Limitações/dinamicidade estão explícitas; `E` nunca é apresentado como total absoluto
  de fluxos do produto.
- Nenhum corpo de método foi aberto e nenhum comportamento foi afirmado.
- O módulo alvo tem stub, se o alvo já foi informado.

## Handoff

Imprima literalmente:

> Mapa semeado em `.arquitetura/mapa/`: <E> entrypoints candidatos, com limitações: <resumo>. Próximo passo: rode **`documentar-fluxo`** informando **um** fluxo crítico e o `ENTRY-###`/entrypoint que o inicia.
