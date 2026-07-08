# doc-sauro — trilha de documentação de arquitetura

Uma trilha de **prompts portáveis** que, a partir de qualquer codebase, gera documentação
de arquitetura `.md` (para Docusaurus) **completa** (não pula o 20% difícil: error paths,
chamada externa, compensação) e **precisa** (só afirma sobre o código o que o código
comprova, citado como `arquivo:linha`).

Roda em **Amazon Q Developer · GitHub Copilot · Kiro** — o resultado **não usa nada de
Claude**. Sem subagente, sem parser (leitura LLM-native), portável entre os 3 runtimes.

## Comece por aqui

- **[COMO-USAR.md](COMO-USAR.md)** — runbook de operação: pré-requisitos, a sequência e o **prompt inicial** para disparar o fluxo.

## Mapa do repositório

| Caminho | O que é |
|---|---|
| [DESIGN.md](DESIGN.md) | o design e o porquê (princípio-norte, duas trilhas, gates, log de decisões) |
| [prompts/](prompts/) | os **5 prompts canônicos** (fonte única) + a cadeia — `bootstrap-contexto` → `mapear-estrutura` → `documentar-fluxo` → `grill-doc` → `grill-mermaid` |
| [tools/](tools/) | `empacotar.py` — gerador canônico → 3 runtimes, com `--verify` de paridade |
| [dist/](dist/) | os empacotamentos **prontos para copiar** no projeto-alvo (`.amazonq/` · `.github/` · `.kiro/`) + deploy/smoke-test |
| [piloto/](piloto/) | a prova de campo: um fluxo real documentado ponta-a-ponta, passando os gates |

## Em uma frase

Mapa barato (nível-declaração) + leitura forçada (segue o corpo do código) + gates de
completude e citação ⇒ some o gap da doc rasa. A tese está provada no [piloto](piloto/EVIDENCIA.md).
