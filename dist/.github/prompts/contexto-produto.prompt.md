---
description: 'Você produz .arquitetura/contexto-produto.md: um modelo de domínio voltado a produto, com personas, jobs, termos, regras e lacunas.'
agent: 'agent'
---

# Prompt · `contexto-produto`

> Abre o track de negócio. Portável (Amazon Q / Copilot / Kiro), **standalone**,
> sem subagente e sem parser. Roda uma vez por projeto depois de pelo menos um fluxo
> técnico passar nos dois gates.

Você produz `.arquitetura/contexto-produto.md`: um modelo de domínio voltado a produto,
com personas, jobs, termos, regras e lacunas. Ele dá linguagem consistente aos docs de
negócio sem transformar inferência técnica em verdade de produto.

## Contrato de execução

- Insumos: `.arquitetura/contexto.md`, mapa, docs técnicos e, para cada fluxo usado,
  `grill-doc.<slug>.md` + `grill-mermaid.<slug>.md` aprovados no mesmo snapshot.
- Fluxo sem os dois gates pode aparecer apenas em **lacunas**, nunca como base aprovada.
- Pode escrever somente `.arquitetura/contexto-produto.md`.
- Não reabre nem reinterpretará código para criar propósito. O QUÊ vem do doc técnico;
  o PORQUÊ vem do humano ou permanece inferência marcada.
- Se nenhum fluxo técnico estiver aprovado, pare `BLOQUEADO`.

## Jurisdição e estados de conhecimento

Cada afirmação usa exatamente um estado:

- `atribuído` — verbatim + quem + quando;
- `herdado-verificado` — comportamento vindo de doc técnico aprovado, apontado por
  `FLUXO/PASSO/ARESTA/FRONTEIRA`;
- `[inferido do código · a confirmar]` — hipótese de produto com base explícita no doc
  técnico/contexto; nunca no mapa isolado;
- `[PENDENTE]` — não há base suficiente ou falta decisão humana.

Mapa e entrypoint ajudam a localizar; não provam persona, job ou regra de negócio.
Preserve `ARC-###` e `CON-###`. Conflito vira divergência, não uma redefinição silenciosa.

## Fase 1 · Delimite o domínio observado

Leia o contexto inteiro e apenas os fluxos tecnicamente aprovados. Registre:

- **bounded context observado:** que parte do negócio esses fluxos cobrem;
- **fora da amostra:** entrypoints/áreas ainda sem fluxo aprovado;
- **linguagem existente:** termos humanos do contexto e termos técnicos a traduzir;
- **invariantes/regras candidatas:** só quando atribuídas ou inferidas com base.

Não chame a amostra de “produto inteiro”.

## Fase 2 · Modele com IDs estáveis

### Personas `PER-###`

Nome no vocabulário do domínio, job de alto nível e relação com os fluxos. “Usuário”
genérico só vale se o contexto realmente não distinguir papéis.

### Jobs `JOB-###`

Formato: “Quando <situação>, <persona> quer <resultado>, para <valor>”. Resultado e
valor são coisas diferentes; o fluxo pode provar o primeiro e não o segundo.

### Termos `TERMO-###`

Definição simples, sinônimos proibidos/ambíguos e par técnico→produto quando útil. Se a
mesma palavra tiver dois sentidos, crie duas entradas e delimite contexto.

### Regras/invariantes `REGRA-###`

Regra, motivo, consequência de violação e fonte. Não promova um guard técnico a política
de negócio sem confirmação; mantenha como inferência.

### Lacunas `LACUNA-###`

Pergunta concreta, por que importa, base disponível, dono da resposta e artefatos que
precisarão ser revistos quando resolvida. Toda lacuna cita os `FLUXO/PASSO/PER/JOB/TERMO`
que a revelaram; “confirmar persona” ou “qual é o valor?” sem gatilho específico é inválido.

## Checkpoint humano

Se um dono de produto estiver disponível, apresente personas, jobs, termos ambíguos e
regras inferidas por meio das `LACUNA-###` concretas e peça confirmação. Não faça
pergunta genérica fora dessas lacunas. Se não estiver disponível, grave inferências e
lacunas; não simule aprovação.

## Saída

```md
# Contexto de Produto — <projeto>
> Interno. Modelo observado, não descrição total do produto.
> Frescor: <data-hora> · snapshots técnicos aprovados: <lista fluxo→snapshot>

## Limite do domínio observado
- Bounded context: <descrição + base>
- Fora da amostra: <ENTRY-IDs/áreas>

## Personas
| ID | Persona | Job de alto nível | Fluxos/base | Estado |
|---|---|---|---|---|
| `PER-001` | <nome> | <job> | <fonte> | atribuído / inferido-a-confirmar |

## Jobs (JTBD)
| ID | Job | Persona | Base | Estado |
|---|---|---|---|---|
| `JOB-001` | Quando..., quer..., para... | `PER-###` | <fonte> | <estado> |

## Glossário de produto
| ID | Termo | Definição simples | Evitar/ambiguidade | Par técnico | Base/estado |
|---|---|---|---|---|---|
| `TERMO-001` | <termo> | <definição> | <sinônimo a evitar> | `<par>` | <fonte/estado> |

## Regras e invariantes
| ID | Regra | Porquê/consequência | Base | Estado |
|---|---|---|---|---|
| `REGRA-001` | <regra> | <valor/risco> | <fonte> | atribuído / inferido-a-confirmar |

## Restrições e compromissos relevantes
- `CON-###` / `ARC-###` — <como limita a linguagem/decisão de produto>

## Lacunas e decisões humanas
| ID | Pergunta | Por que importa | Dono | Impacta |
|---|---|---|---|---|
| `LACUNA-001` | <pergunta> | <risco> | <quem/desconhecido> | <artefatos> |
```

## Critério de conclusão

- Todo fluxo usado tem os dois gates técnicos aprovados no mesmo snapshot.
- Toda persona/job/termo/regra tem ID, base e estado explícito.
- O limite observado e o fora-da-amostra estão declarados.
- Termos ambíguos e invariantes têm tratamento explícito.
- Toda `LACUNA-###` aponta os sinais específicos que a geraram; zero pergunta genérica.
- Decisões humanas não foram ratificadas pela IA.
- Zero nome de arquivo/`arquivo:linha` na prosa de produto; bases referem IDs/seções dos
  artefatos aprovados.

## Handoff

> Contexto de produto gravado em `.arquitetura/contexto-produto.md` com <n> lacunas humanas. Próximo passo: rode **`documentar-negocio`** para um `FLUXO-<slug>` tecnicamente aprovado.
