---
inclusion: manual
---

# Prompt · `bootstrap-contexto`

> Passo 0 da trilha de documentação de arquitetura. Portável: roda em Amazon Q, GitHub Copilot ou Kiro — **standalone**, sem subagente, sem parser/ctags/tree-sitter. Leitura é **LLM-native**.

Você detecta **stack e estrutura** (retrato barato) e **elicita do humano** o que o código não conta. Produz `.arquitetura/contexto.md` — o arquivo que todo passo seguinte lê. Rode **uma vez por projeto**, na raiz do repositório.

## Princípio-norte (inegociável)

> O mapa e o depoimento humano são **hipóteses** — nunca viram citação sobre o que o código faz. A única fonte citável sobre **comportamento do código** é o próprio código (`arquivo:linha`). O que o humano diz entra **atribuído** (verbatim + quem + quando), nunca como "fato objetivo".

Neste passo você ainda **não abre corpo de método** — logo, não afirma comportamento. Você inventaria nomes e ouve o humano. Nada aqui é "o código faz X".

## Duas trilhas (não misture)

- **Extração** (código → contexto): enche **Stack** e **Estrutura**. Fonte = arquivos; toda afirmação carrega o arquivo que a comprova.
- **Elicitação** (humano → contexto): enche **Tier**, **Propósito**, **Blast radius**, **Restrições** e **Padrões-que-não-se-aplicam**. Fonte = humano; registro **verbatim + atribuído**.

## Passos

### 1 · Extração — retrato barato (sem abrir corpo de método)

1. Liste a árvore de pastas até ~2-3 níveis. Ignore build/deps: `node_modules`, `target`, `dist`, `build`, `.next`, `vendor`, `venv`, `__pycache__`, `.git`.
2. Determine a **stack** pelos **manifestos e sinais de convenção**, não por adivinhação: `package.json` · `pom.xml` · `build.gradle` · `go.mod` · `Cargo.toml` · `requirements.txt`/`pyproject.toml` · `*.csproj` · `composer.json` · `Gemfile` · `Dockerfile`/`docker-compose.yml`. **Cada linguagem/framework afirmado carrega o arquivo que o comprova.**
3. Inventarie os **tipos de entrypoint** por convenção — o vocabulário é **language-agnostic**: `entrypoint` (controller/handler/rota, listener de fila, job agendado, CLI `main`, consumer) · `módulo` (pasta/pacote top-level) · `unidade` (classe/arquivo) · `aresta-de-dependência` (uma unidade referencia outra). Liste os módulos top-level e, para cada um, o(s) tipo(s) de entrypoint que ele expõe.

**Concluído quando:** o bloco **Stack** (cada item com evidência = arquivo) e o bloco **Estrutura** (todos os módulos top-level + tipos de entrypoint) estão preenchidos, sem nenhuma afirmação de comportamento.

### 2 · Elicitação — pergunte ao humano

Pergunte e **espere a resposta** antes de gravar. Registre cada resposta **verbatim + quem + quando**. Cinco itens:

1. **Tier / criticidade** — crítico pra receita? interno? experimental? regulado?
2. **Propósito** — em uma frase, no vocabulário do **domínio** (o que faz), não da tecnologia (como faz).
3. **Blast radius** — o que quebra às 3h da manhã se isso cair? quem é paginado? qual dependência externa, se sumir amanhã, derruba tudo?
4. **Restrições fora do código** — compliance, política, contrato com vendor, prazo, orçamento. (O *porquê* puro o código não checa; só dá pra atribuir.)
5. **Padrões que NÃO se aplicam** — o que parece o padrão da casa mas aqui é diferente de propósito. (O anti-template mais barato: evita a doc assumir o convencional.)

Item sem resposta → marque `[PENDENTE: <pergunta>]` e siga (**registra-e-segue**). **Nunca invente a resposta.**

**Concluído quando:** o bloco **Elicitação** tem os 5 itens, cada um atribuído OU `[PENDENTE]`.

### 3 · Grave `.arquitetura/contexto.md`

Interno, **fora de `docs/`** (não vai pro site). Use exatamente esta forma:

```md
# Contexto — <nome do projeto>
> Interno. Insumo de toda a trilha. Extração carrega evidência; elicitação é atribuída.
> Frescor: <data-hora> · <commit/hash se houver>

## Stack
- <linguagem/framework/runtime> — evidência: `<arquivo>`
  ...

## Estrutura
- Raiz do código: `<path>`
- Módulos top-level:
  - `<módulo>` — entrypoints: <tipos> — evidência: `<arquivo/pasta>`
  ...

## Elicitação (atribuído)
- **Tier:** "<verbatim>" — <quem>, <quando>
- **Propósito:** "<verbatim>" — <quem>, <quando>
- **Blast radius:** "<verbatim>" — <quem>, <quando>
- **Restrições:** "<verbatim>" — <quem>, <quando>
- **Padrões que não se aplicam:** "<verbatim>" — <quem>, <quando>
  <ou> [PENDENTE: <pergunta>]
```

## Critério de conclusão (checável)

- `.arquitetura/contexto.md` existe.
- **Todo** item de Stack tem evidência (arquivo).
- Estrutura lista **todos** os módulos top-level.
- Elicitação tem os **5** itens — cada um atribuído ou `[PENDENTE]`.
- **Zero** afirmação de comportamento de código no arquivo.

## Handoff

Imprima ao humano, literalmente:

> Contexto gravado em `.arquitetura/contexto.md`. Próximo passo: rode o prompt **`mapear-estrutura`** na raiz do repositório.
