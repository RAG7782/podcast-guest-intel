# Princípios do produto

Estas regras valem para todas as tasks, agentes e scripts do pacote.

## A decisão é sempre humana

O plugin **recomenda e alerta, nunca decide pelo usuário**. Gates (o do @guardian, a regra de
fontes do modo denúncia, `pronto_para_gravar`) emitem **recomendação + alerta de
responsabilidade**. Para seguir contra a recomendação, o usuário faz um **aceite explícito, que
fica registrado** (quem, quando e qual alerta viu) no formato
`references/contracts/human-decision.schema.json`.

## Coletar o máximo, descartar nada por conta própria

Independência de fontes vem com autor, veículo e agência quando houver, para o humano julgar.

## Regras rígidas (lei ou integridade, não opinião)

- Dado sensível só entra se o **próprio titular** o declarou, com aceite específico (LGPD art. 11, I).
  A pesquisa pública nunca infere dado sensível.
- Nenhum valor de credencial (chave, token, senha) fica em arquivo do show.
- Os artefatos precisam validar contra os schemas de `references/contracts/`.

## Produto × dados do usuário

Nome do programa, estúdio, endereço, linha editorial e perfil do host são **dados que o usuário
preenche** no `show-profile` e no `host-profile`. Nada disso vem embutido no pacote.
