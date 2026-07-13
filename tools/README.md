# `tools/empacotar.py` — empacotador canônico → 3 runtimes

Transforma a **fonte canônica única** `prompts/*.md` nos 3 empacotamentos portáveis
sob `dist/`, um por runtime-alvo. Repetível: quando novos geradores da trilha
entrarem em `prompts/`, são empacotados sem tocar neste código.

```bash
python3 tools/empacotar.py            # (re)gera dist/ a partir de prompts/
python3 tools/empacotar.py --verify   # paridade + frontmatter (não escreve nada)
```

## O invariante (o que mata o drift)

> O **corpo** de cada alvo é **byte-a-byte** o prompt canônico. A **única** adição é o
> frontmatter que cada ferramenta exige para invocação-manual.

Tirar o frontmatter de qualquer alvo devolve o canônico, caractere a caractere. Logo:
**nunca edite nada em `dist/` à mão** — edite o canônico em `prompts/` e rode o gerador.
O `--verify` regenera num tmp e compara byte-a-byte com `dist/`, então um alvo editado à
mão (ou um `dist/` stale) reprova. Ele também valida o contrato arquitetural mínimo de
cada canônico: título, marcador standalone, precondições/contrato, critério verificável,
handoff, marcadores semânticos, persistência dos grills dinâmicos e saída persistente
para todo gate. O step `revisar-arquitetura` também é validado por seus IDs de
oportunidade/pergunta, deletion test, relatório temporário e forças de recomendação.

## Os 3 alvos (convenções confirmadas nos docs/fonte oficiais — 2026-07)

Os prompts da cadeia são **invocáveis (inclusão manual)**, não always-on: rodam em **sequência, um por
vez** (cada prompt imprime o próximo comando; `.arquitetura/grills/` mantém perguntas,
o mapa mantém o ledger e `.arquitetura/gates/` mantém aprovações persistentes).
Always-on injetaria todos em toda interação — bloat de contexto e quebra da sequência.

| Runtime | Arquivo gerado | Frontmatter | Invocação |
|---|---|---|---|
| **Amazon Q Developer** | `.amazonq/prompts/<nome>.md` | **nenhum** (arquivo inteiro = prompt) | `@<nome>` no `q chat` |
| **GitHub Copilot** | `.github/prompts/<nome>.prompt.md` | `description` + `agent: 'agent'` | `/<nome>` no Copilot Chat |
| **Kiro** | `.kiro/steering/<nome>.md` | `inclusion: manual` | `#<nome>` (ou slash `/<nome>`) |

Notas de precisão que o código encoda:

- **Amazon Q** — Markdown puro, **sem frontmatter** (um bloco `---` viraria texto literal
  do prompt). Pasta do projeto `.amazonq/prompts/` só é lida pela **CLI `q chat`**; o
  **IDE plugin lê só a global** `~/.aws/amazonq/prompts/` — deploy no IDE = copiar para
  lá ou colar à mão. Nome: 1–50 chars, letras/números/hífen/underscore.
  _(distinto de `.amazonq/rules/*`, que é always-on e não serve para invocável.)_
- **Copilot** — o campo `mode:` foi **depreciado**; a convenção atual é `agent:`
  (`ask`/`agent`/`plan`). Usamos `agent: 'agent'` porque `bootstrap`/`mapear`/`documentar`
  **escrevem arquivos** (precisam de modo agente); nos gates é superset inócuo. O
  `description` é **derivado** da 1ª frase do canônico (regenerado a cada run → sem drift).
- **Kiro** — no modo `manual`, o frontmatter é **só** `inclusion: manual` (os campos
  `name`/`description` são exigidos só no modo `auto`).

Fontes: Amazon Q CLI v1.19.7 (`crates/chat-cli/src/util/paths.rs`) + IDE
`context-prompt-library.html`; VS Code prompt-files docs + validador `promptValidator.ts`
(`mode`→`agent`); Kiro `kiro.dev/docs/steering`.

## Adicionar um prompt novo (a fatia dos geradores futuros)

1. Escreva o canônico em `prompts/<nome>.md` (mesma forma dos demais: `# Prompt · \`<nome>\``
   + corpo com princípio-norte embutido + handoff).
2. `python3 tools/empacotar.py` — os 3 alvos aparecem em `dist/`.
3. `python3 tools/empacotar.py --verify` — confirma paridade + frontmatter.

Nada além de largar o arquivo em `prompts/`. O `README.md` de `prompts/` continua fora
(é a doc da cadeia, não um prompt — única exclusão do glob).
