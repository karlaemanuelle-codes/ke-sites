# Regras deste repositório

## A regra que não se quebra: não misturar as coisas da Karla com as da Raíssa

Em 21/10/2026 as duas se misturaram e custou uma tarde de trabalho da Karla.
Antes de gravar qualquer dado, confira em qual dos dois mundos você está.

| | Karla | Raíssa |
|---|---|---|
| Onde os dados moram | **A planilha**, o artifact *Finanças da Karla* | Tabelas `rai_` no Supabase |
| O que tem dentro | Consignado, Rayka Viagens e Pessoal | Só consignado |
| Aplicativo | nenhum — foi retirado do ar | `apps/vendas-raissa` |

**Nunca copie dado de um lado para o outro.** A aba Pessoal da Karla tem
benefício da mãe dela, dívida de cartão e o que amigos lhe devem; a Raíssa é
funcionária dela e vai ser cliente do programa. Esses dados não podem aparecer
no aplicativo que será vendido a ela.

Se a Karla pedir para "passar o banco de dados para a Raíssa", ela está
pensando em não desperdiçar estrutura, não em entregar os dados dela. As
tabelas `rai_` já existem: diga isso e ofereça carregar os contratos da própria
Raíssa.

## A planilha Finanças da Karla é a fonte da verdade

Fica no artifact `https://claude.ai/artifact/BbBekTNBBSpBUzZLmmkvUZ`, lida e
escrita pela ferramenta `ArtifactData`. Abas, nesta ordem: Painel, **Pessoal**,
Atender, Entradas, Consignado, Carteira, Rayka, Emissões, Clientes e
Pendências.

A Pessoal era a última da fileira e a Karla não a encontrava — no celular ela
ficava fora da tela. Passou para o segundo lugar em 21/10/2026. Se for mexer na
ordem das abas de novo, lembre que a fileira rola na horizontal e o que fica
depois da quarta aba some da vista num telefone.

Houve um aplicativo espelho em `apps/financas-karla`, publicado no Cloudflare
com tabelas `fin_` no Supabase. **Foi aposentado**: mostrava números diferentes
da planilha e confundia. As tabelas `fin_` ficam como backup — não são lidas por
nada e não devem ser atualizadas.

### Duas conversas escrevem nesta planilha

Esta sessão e a das rotinas diárias da Karla. Já houve conflito: uma desfez a
correção da outra. Antes de gravar, **releia o documento e use `if_version`**
com a versão que acabou de ler. Se o servidor recusar, releia e refaça — nunca
force por cima sem olhar o que mudou.

## Comissões do consignado (regra da Karla, 21/10/2026)

- Ao lançar um contrato novo, estime a comissão em **2,5%** do valor liberado.
- **Margem nova de espécie 32: 1%.**
- Quando o pagamento cair, a Karla manda o valor por cliente. Aí **troque pelo
  valor real** — na tabela `contratos` e também na `entradas`, que é de onde sai
  o "Entrou na conta". Esquecer a segunda já deixou o painel R$ 44,72 errado.
- A tabela do banco diz 2%, mas o que cai fica entre 2,25% e 2,81%. Valor real
  sempre ganha de estimativa.

## Cartões da Karla (aba Pessoal) — o que "quitei" quer dizer

Quando a Karla diz **"quitei o cartão X"**, ela quer dizer que pagou **a
parcela daquele mês** — não o cartão inteiro. Zere só a coluna do mês na lista
`valores` daquele cartão e recalcule o `total`; as parcelas seguintes ficam.

Para quitar o cartão por inteiro ela vai dizer com todas as letras, do tipo
"quitei o PicPay inteiro". Na dúvida, faça o caminho conservador (só o mês) e
pergunte: errar para menos mostra uma dívida menor do que a real.

Os dados ficam no documento `pessoal/dados` da planilha — uma lista `cards`,
cada um com `nome`, `valores` (um por mês, na ordem de `meses`) e `total`, mais
o `totalFalta` geral, que é a soma dos totais.

## O aplicativo da Raíssa

`apps/vendas-raissa` — site estático, publicado pelo Cloudflare, dados nas
tabelas `rai_`. Detalhes em `apps/vendas-raissa/LEIA-ME.md`.

A chave do Supabase no HTML é a **publicável** e pode ficar à vista; quem
protege é o RLS. **A chave `service_role` nunca entra em código publicado.** Uma
chave de API de modelo (OpenAI, Anthropic) também não — essa precisa ficar num
servidor, nunca no HTML.

## Testes

`apps/vendas-raissa` tem teste de navegador com Playwright. O painel original
teve um bug em que todas as abas abriam ao mesmo tempo — o teste cobre isso.
Rode antes de publicar mudança de tela.

Playwright está em `/opt/pw-browsers`; importe assim:

```js
import pkg from '/opt/node-tools/node_modules/playwright/index.js';
const { chromium } = pkg;
```
