---
sidebar_position: 1
title: "Visão de Produto: agente-orquestrator"
description: "A plataforma pra operar agentes de IA como funcionários — criar, dar trabalho e garantir que roda controlado, dentro do orçamento e com o arriscado revisado por gente."
---

# agente-orquestrator — visão de produto

> A porta de entrada do domínio. Pra uma PO nova entender o **app inteiro** — não um fluxo só. Sem código. Cada fluxo aponta pro seu doc de negócio.

## O que é

O agente-orquestrator é uma plataforma pra operar **agentes de IA como funcionários**: você monta uma empresa, cria seus agentes e dá trabalho a eles — e a plataforma garante que cada trabalho roda de forma **controlada** (uma vez só, dentro do orçamento, com o que é arriscado passando por revisão de gente antes de virar "feito"). Um **agente orquestrador** (o "CEO") coordena e delega; os agentes executam. — `[inferido do código · a confirmar]` — base: o fluxo já documentado (acordar → executar → liquidar) + o propósito elicitado do operador ("orquestrar agentes de IA como funcionários, mediando execução por aprovação humana").

## Pra quem é

- **O operador** (o dono da empresa) — opera a plataforma: aciona trabalho, aprova o que é arriscado e define o orçamento. O job dele: *acionar um agente e ter certeza de que roda uma vez só e termina com um desfecho seguro*.
- **O agente** (o "funcionário de IA") — executa as tarefas dentro de uma empresa.
- **O agente orquestrador** (o "CEO") — o agente-mestre que só delega: grelha, descobre, contrata e atribui, sem produzir conteúdo ele mesmo.

Dois desejos atravessam tudo que o produto faz: quando um trabalho é **arriscado**, ele **para pra revisão humana** antes de virar "feito"; e quando o **orçamento** aperta, o sistema **para de gastar sem jogar fora** trabalho que já foi pago. *(quem usa e o que quer: herdado do contexto de produto — atribuído ao operador.)*

## Vocabulário

Os termos que esta visão usa (a lista completa vive no glossário de produto):

- **Empresa** — a fronteira de isolamento; um dono opera várias, uma por produto. (técnico: `Company`)
- **Agente** — um funcionário de IA dentro de uma empresa. (técnico: `Agent`)
- **Agente orquestrador (CEO)** — o agente-mestre que só delega, não produz conteúdo.
- **Tarefa** — a unidade de trabalho a ser feita e concluída. (técnico: `Issue`)
- **Acordar** — disparar um trabalho pra um agente. (técnico: `wakeup`)
- **Orçamento** — limite de custo por escopo; se estoura, o sistema para de criar coisa nova. (técnico: `Budget`)

*(vocabulário e definições: herdados do glossário de produto.)*

## Os fluxos principais

O que já tem doc de negócio — clique pra ver cada fluxo por dentro, em linguagem de gente:

| Fluxo | O que faz pra você | Doc |
|---|---|---|
| Acordar um agente e concluir o trabalho | Acionar um agente pra fazer uma tarefa — garantindo que ela roda **uma vez só**, dentro do **orçamento**, e termina com um **desfecho seguro**: feito, esperando revisão, ou bloqueado. | [ver fluxo](fluxos-negocio/wakeup-run-settle.md) |

**Cobertura:** esta visão cobre **1** fluxo de negócio documentado — que toca 3 áreas do produto (acionamento, tarefa e orçamento), sendo a **governança** coberta só em parte: o orçamento sim, a **aprovação prévia** (a decisão humana que libera o que é sensível) ainda não. O mapa conhece **~12** áreas de produto no total; as **9** abaixo — mais essa aprovação prévia — ainda **não têm doc de negócio**, e são a fila de trabalho (não um recorte do que o app faz):

- **Criar e configurar uma empresa** — abrir e ajustar a empresa onde tudo acontece.
- **Montar a organização** — criar agentes, times e papéis; escolher o motor de cada um.
- **Acompanhar o trabalho num painel** — ver as execuções e o passo a passo do que os agentes fizeram.
- **Conversar com um agente** — um turno de conversa que vira um trabalho.
- **Habilidades dos agentes** — o catálogo de habilidades e como instalá-las num agente.
- **Memória da empresa** — o "segundo cérebro": decisões e histórico que a empresa guarda.
- **Pré-visualizar um protótipo** — ver de pé o protótipo que um agente montou.
- **Passar o bastão de contexto** — a passagem de contexto de uma sessão pra outra quando ela fica longa.
- **Histórico durável de ações** — o registro do que cada agente mudou.

*(todos os itens acima: `[inferido do código · a confirmar]` — base: o inventário de áreas do produto no índice do mapa; algumas podem ser internas, não fluxos de produto — a confirmar. Duas áreas puramente técnicas — segurança e utilitários — não viram fluxo de produto e ficam de fora.)*

## Trace

<details>
<summary>Trace — cada afirmação e sua base (a PO não precisa; o cético clica)</summary>

Base = seção de um doc de negócio já aprovado, do contexto elicitado, ou do índice do mapa. Nenhuma afirmação de comportamento é feita aqui direto do código — a visão liga docs, não os inventa.

| Afirmação (seção) | Tipo | Base | Estado |
|---|---|---|---|
| "Acordar um agente e concluir o trabalho" — o one-liner do fluxo (*Os fluxos principais*) | o quê | [wakeup-run-settle](fluxos-negocio/wakeup-run-settle.md) §Em uma frase (citado, não reescrito) | herdado-verificado |
| O que o produto é no todo (*O que é*) | síntese | fluxo documentado (acordar → executar → liquidar) + `contexto.md` §Elicitação (Propósito, Tier) | inferido-a-confirmar |
| Cobre 1 fluxo; ~12 áreas de produto; ~9 ainda sem doc (*Cobertura*) | cobertura | `.arquitetura/mapa/_indice.md` (tabela de cobertura: 3 módulos `parcial`, 9 `esqueleto`, 2 transversais) | inferido-a-confirmar |
| Cada área "ainda sem doc" (*Cobertura*) | cobertura | `.arquitetura/mapa/_indice.md` (entrypoints inferidos por módulo: `identity`, `org`, `board`, `conversation`, `governance/approval`, `skills`, `memory`, `preview`, `handoff`/`activitylog`) | inferido-a-confirmar |
| Operador, agente, agente orquestrador — quem são e o que querem (*Pra quem é*) | pra quem | `contexto-produto.md` §Personas / §Jobs | herdado (atribuído: operador) |
| "Arriscado espera revisão" e "orçamento estoura → para de gastar sem perder trabalho" (*Pra quem é*) | pra quem | `contexto-produto.md` §Jobs | herdado (atribuído: operador) |
| Empresa, Agente, Tarefa, Acordar, Orçamento — definições (*Vocabulário*) | vocabulário | `contexto-produto.md` §Glossário de produto | herdado (atribuído/inferido lá) |

</details>
