# doc-sauro — trilha de documentação de arquitetura

Uma trilha de **prompts portáveis** que, a partir de qualquer codebase, gera documentação
de arquitetura `.md` (para Docusaurus) **completa** (não pula o 20% difícil: error paths,
chamada externa, compensação) e **precisa** (só afirma sobre o código o que o código
comprova, citado como `arquivo:linha`). Os grills usam rubricas fixas como lentes, mas
geram perguntas a partir dos sinais reais de cada projeto — nunca um questionário genérico.

Roda em **Amazon Q Developer · GitHub Copilot · Kiro** — o resultado **não usa nada de
Claude**. Sem subagente, sem parser (leitura LLM-native), portável entre os 3 runtimes.
Depois dos gates técnicos, um step opcional revisa a arquitetura por evidência, mostra
oportunidades de modules mais deep e exige escolha humana antes de aprofundar qualquer uma.

## Comece por aqui

- **[COMO-USAR.md](COMO-USAR.md)** — runbook de operação: pré-requisitos, a sequência e o **prompt inicial** para disparar o fluxo.

## Mapa do repositório

| Caminho | O que é |
|---|---|
| [DESIGN.md](DESIGN.md) | o design e o porquê (princípio-norte, duas trilhas, gates, log de decisões) |
| [prompts/](prompts/) | os **11 prompts canônicos** (fonte única), sua constituição operacional e as cadeias técnica + revisão arquitetural opcional + negócio |
| [tools/](tools/) | `empacotar.py` — gerador canônico → 3 runtimes, com `--verify` de paridade |
| [dist/](dist/) | os empacotamentos **prontos para copiar** no projeto-alvo (`.amazonq/` · `.github/` · `.kiro/`) + deploy/smoke-test |
| [piloto/](piloto/) | baseline de campo do slice original; reexecução nos novos contratos arquiteturais está pendente |

## Em uma frase

Mapa barato (nível-declaração) + leitura forçada (segue o corpo do código) + gates de
completude e citação ⇒ some o gap da doc rasa. A tese original está demonstrada no
[piloto](piloto/EVIDENCIA.md); os novos contratos ainda pedem uma rodada de campo.
