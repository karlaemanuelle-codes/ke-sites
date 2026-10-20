# Vendas da Raíssa — aplicativo

Painel de consignado para a Raíssa, feito a partir do **Finanças da Karla**.
Mesmo jeito de funcionar: é um site comum, instala na tela do celular e guarda
os dados no Supabase.

A diferença é o recorte. Aqui é **só consignado**: saíram as abas de Entradas,
Rayka e Emissões, e entrou a **Biblioteca de Abordagens**.

## O que tem nesta pasta

| Arquivo | Para que serve |
|---|---|
| `public/index.html` | O aplicativo inteiro — telas, cálculos, login, scripts e conexão com o banco |
| `public/app.webmanifest` | Faz o celular tratar como aplicativo (ícone, nome, tela cheia) |
| `public/icone.svg` | O ícone que aparece na tela de início |
| `wrangler.toml` | Diz ao Cloudflare para publicar só a pasta `public/` |

É tudo estático: não tem build, não tem dependência, não precisa de servidor.

## As abas

| Aba | O que faz |
|---|---|
| Painel | Comissão e produção do mês, produção por banco, o que precisa de ação |
| Atender | Fila de atendimentos: quem retornar, simular, cobrar documento |
| Contratos | Lançar e acompanhar contrato por contrato, com a comissão calculada |
| **Biblioteca** | Os 24 scripts de consignado, com busca, filtro e placar de vendas |
| Carteira | Quem chamar hoje, quem está sem telefone, mensagem pronta de WhatsApp |
| Clientes | Cadastro: nome, telefone, nascimento, CPF |
| Pendências | O que ficou faltando |

## A Biblioteca

Os 24 scripts vêm da *Biblioteca de Abordagens* da Karla, só a parte de
consignado. **Os 5 scripts de taxa ficaram de fora** — a própria Biblioteca
avisa, em cada um deles, que cobrar valor do cliente por correspondente
bancário é vedado pelas regras do Banco Central, e este painel vai para uma
terceira pessoa. Os scripts de BPC/LOAS e de viagens também não entram, porque
a Raíssa só trabalha consignado.

O texto dos scripts mora no código, não no banco — é material fixo. O banco
guarda só o **placar**: quantas vezes cada script foi usado e quantas vendas
saíram dele, na tabela `rai_scripts`, uma linha por script. A lista se ordena
por venda, então com o tempo ela sobe o que funciona.

### O nome de quem vende

Os scripts foram escritos pela Karla e se apresentavam com o nome dela. Agora o
nome é uma ficha, `[SEU NOME]`, trocada na hora de mostrar e na hora de copiar.
O campo **"Seu nome nas mensagens"**, no alto da Biblioteca, define esse nome; ele
fica no aparelho (`localStorage`, chave `rv-vendedora`) e também entra nas
mensagens prontas da Carteira. O padrão é "Raíssa".

## Como os dados são guardados

Supabase, projeto `nxppsfouinsyhfgbmhno`, nas tabelas com prefixo `rai_`:

```
rai_contratos  rai_clientes  rai_carteira
rai_atendimentos  rai_pendencias  rai_scripts
```

O prefixo separa os dados dela dos da Karla (`fin_`) e dos do CRM, que moram no
mesmo projeto. Todas estão com `force row level security` e só têm política
para o papel `authenticated`: sem login não se lê nem se escreve uma linha.

A chave que está no `index.html` é a **publicável** — pode ficar à vista, sozinha
não abre nada. **A chave `service_role` nunca pode entrar aqui.**

> Se um dia os dados dela precisarem ficar num projeto separado do da Karla, o
> caminho é criar o projeto, repetir estas seis tabelas e trocar `SB_URL` e
> `SB_KEY`. O resto do código não muda.

## Como publicar

Projeto próprio no Cloudflare, ligado a este repositório — separado do
`financas-karla` e do worker `ke-sites`.

Pelo caminho **Workers**: **Root directory** `apps/vendas-raissa`, build command
vazio. Pelo caminho **Pages**: preset None, build vazio, output
`apps/vendas-raissa/public`. Cada push na branch publicada republica sozinho.

## Como o painel conversa com o banco

Igual ao da Karla: um objeto `db` com três métodos (`collection().add()`,
`doc().set()`, `doc().update()`) e a ponte no fim do arquivo os liga ao Supabase.

Uma diferença herdada da cópia: o `$()` daqui devolve um alvo de mentira quando
o id não existe. O `render()` veio inteiro do painel da Karla e ainda cita
alguns ids das abas que saíram; em vez de caçar linha por linha, a escrita
nesses ids simplesmente não faz nada. Se um dia o `render()` for reescrito só
para esta versão, dá para voltar ao `getElementById` puro.

## Testes

`teste.mjs` (no scratchpad da sessão) sobe a página num servidor local e
confere 22 pontos: que cada aba abre só ela — foi o bug da primeira versão do
painel da Karla, em que todas ficavam abertas ao mesmo tempo —, que as abas da
Karla sumiram, que os 24 scripts aparecem, que o filtro e a busca respondem,
que nenhum script continua assinado como "Karla" e que trocar o nome reescreve
os textos.
