# Finanças da Karla — aplicativo

Versão própria do painel **Finanças da Karla**, que antes vivia como artifact no
claude.ai. Aqui ele é um site comum, que instala na tela do celular e guarda os
dados no Supabase da Karla.

## O que tem nesta pasta

| Arquivo | Para que serve |
|---|---|
| `index.html` | O aplicativo inteiro — telas, cálculos, login e conexão com o banco |
| `app.webmanifest` | Faz o celular tratar como aplicativo (ícone, nome, tela cheia) |
| `icone.svg` | O ícone que aparece na tela de início |

É tudo estático: não tem build, não tem dependência, não precisa de servidor.

## Como publicar

No Cloudflare Pages, criando um projeto ligado a este repositório:

- **Framework preset:** None
- **Build command:** deixar vazio
- **Build output directory:** `apps/financas-karla`

Cada push na branch publicada republica sozinho.

## Como os dados são guardados

Supabase, projeto `nxppsfouinsyhfgbmhno`, nas tabelas com prefixo `fin_`:

```
fin_entradas  fin_contratos  fin_vendas     fin_clientes   fin_embarques
fin_pendencias  fin_atendimentos  fin_carteira  fin_rayka_resumo  fin_config
```

O prefixo existe para não encostar nas tabelas do CRM, que moram no mesmo projeto.

### Sobre a chave que está no código

O `index.html` traz a chave **publicável** do Supabase. Ela é pública por
natureza e pode ficar à vista: sozinha não abre nada.

Quem protege os dados é o RLS. Todas as tabelas `fin_` estão com
`force row level security` e só têm política para o papel `authenticated` —
ou seja, sem login não se lê nem se escreve uma linha.

**A chave `service_role` nunca pode entrar aqui.** Essa sim ignora o RLS.

## Login

E-mail e senha, pelo Supabase Auth. Na primeira vez usa-se
**"É a primeira vez — criar minha senha"**, que cria a conta; dependendo da
configuração do projeto, o Supabase manda um e-mail de confirmação antes de
liberar a entrada.

A sessão fica no `localStorage` do aparelho e se renova sozinha, então o login
não é pedido todo dia.

## Como o painel conversa com o banco

O miolo do `index.html` é o painel original, sem alteração. Toda a conversa com
os dados passa por um objeto `db` com três métodos:

```js
db.collection(nome).add(doc)      // insere
db.doc("colecao/id").set(obj)     // cria ou substitui
db.doc("colecao/id").update(obj)  // altera campos
```

A parte final do arquivo (“PONTE COM O BANCO”) é o que liga esses três métodos
ao Supabase. Para mexer na aparência ou nos cálculos, altere o painel; para
mexer em como os dados são lidos e gravados, altere só a ponte.

Os nomes `statusComissao`, `recebidoEm` e `feitoEm` viram `status_comissao`,
`recebido_em` e `feito_em` na ida e voltam na leitura — é o que `APELIDO` faz.
