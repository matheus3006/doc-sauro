# `dist/` — empacotamento portável dos prompts (GERADO)

> **Não edite nada aqui à mão.** Tudo em `dist/` é saída de `tools/empacotar.py`
> a partir da fonte canônica `prompts/*.md`. Editar um alvo é drift garantido.
> Para mudar um prompt, edite o canônico e rode `python3 tools/empacotar.py`.

Prompts empacotados (5) — a ordem da cadeia está na seção de smoke-test abaixo e em `../prompts/README.md`:

- `bootstrap-contexto`
- `documentar-fluxo`
- `grill-doc`
- `grill-mermaid`
- `mapear-estrutura`

## Como implantar no projeto-alvo

Copie a pasta da ferramenta que você usa para a **raiz do repositório-alvo**:

| Ferramenta | Copie | Vira |
|---|---|---|
| Amazon Q Developer | `dist/.amazonq/` | `<repo>/.amazonq/` |
| GitHub Copilot | `dist/.github/` | `<repo>/.github/` |
| Kiro | `dist/.kiro/` | `<repo>/.kiro/` |

## Como invocar cada prompt (+ smoke-test manual)

A cadeia roda **em sequência, um prompt por vez** — cada prompt termina imprimindo o
próximo comando (handoff) e o mapa em `.arquitetura/` é o ledger entre as sessões:

    bootstrap-contexto → mapear-estrutura → documentar-fluxo → grill-doc → grill-mermaid

Por isso os 5 são **invocáveis (inclusão manual)**, não always-on: always-on injetaria
os 5 em toda interação — bloat de contexto e quebra da sequência.

> Rodar os prompts de ponta a ponta dentro de cada ferramenta é **passo humano**. Este
> checklist só confirma que cada prompt está **invocável** no runtime certo.

### Amazon Q Developer — `.amazonq/prompts/`
Markdown puro, sem frontmatter: o arquivo inteiro é o prompt. Nome invocado = arquivo sem `.md`.

- **CLI `q chat`** (lê a pasta do projeto): na raiz do repo, rode `q chat` e invoque `@bootstrap-contexto`.
- **IDE plugin (VS Code/JetBrains)**: lê **só a pasta global** — copie os `.md` para `~/.aws/amazonq/prompts/` (ou cole o conteúdo à mão). Requer um `q`/plugin atual.

- [ ] `/prompts list` (CLI) ou o menu `@` (IDE) mostra os 5 nomes.
- [ ] `@bootstrap-contexto` injeta o prompt e ele começa a rodar.

### GitHub Copilot — `.github/prompts/`
Arquivo `<nome>.prompt.md`; frontmatter `agent: 'agent'` (modo agente, para os prompts que escrevem arquivos) + `description`.

- Em **VS Code / Visual Studio / JetBrains**, abra o Copilot Chat e digite `/bootstrap-contexto` (nome = arquivo sem `.prompt.md`). Recurso em public preview.

- [ ] Digitar `/` no chat lista os 5 prompts.
- [ ] `/bootstrap-contexto` roda e produz `.arquitetura/contexto.md`.

### Kiro — `.kiro/steering/`
Frontmatter `inclusion: manual` — o doc só entra quando você o chama (não é always-on).

- No chat do **Kiro**, referencie `#bootstrap-contexto` (nome sem `.md`) ou escolha o slash-command `/bootstrap-contexto`.

- [ ] `#` (ou `/`) no chat mostra `bootstrap-contexto` entre os manuais.
- [ ] Referenciar `#bootstrap-contexto` injeta o conteúdo na conversa.

