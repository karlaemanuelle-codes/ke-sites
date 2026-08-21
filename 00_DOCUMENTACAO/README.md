# KE Sites — Template Factory

## O que é isto

A KE Sites é uma fábrica de sites profissionais. Em vez de construir um site do zero para cada cliente, existem **Templates-Mestre** (hoje: um para Salão de Beleza e um para CT/Escolinha de Vôlei) que já vêm prontos em 3 níveis de recurso (Básico, Intermediário, Avançado). Além disso, existe a **plataforma comercial da própria KE Sites** — o site que vende esses templates, mostra demonstrações, planos, preços e formas de pagamento.

Tudo isso é gerado por código (não é editado visualmente em uma ferramenta tipo Wix). Isso tem uma vantagem grande: corrigir ou melhorar algo no motor compartilhado melhora automaticamente todos os templates que o usam.

## Tecnologia usada

- **Python 3** — a linguagem que gera os sites.
- **Jinja2** — o "motor de templates" que transforma arquivos `.html` com variáveis (tipo `{{ nome_do_salao }}`) em páginas HTML finais e prontas.
- **Nenhum banco de dados, nenhum servidor rodando** — os sites gerados são arquivos HTML/CSS/JS comuns ("site estático"), o que os torna simples e baratos de hospedar.
- **Playwright + pytest** — usados só durante o desenvolvimento, para testar automaticamente se os sites funcionam bem em celular/tablet/desktop e se os cálculos de pagamento estão corretos. Não fazem parte do site final.

Não existe hoje nenhum código rodando em produção o tempo todo (nenhum "backend"). O motor de pagamentos (`commerce/`) está pronto e testado, mas ainda não está conectado a nenhuma conta real de gateway de pagamento — veja `commerce/README.md` e `PROBLEMAS_E_PENDENCIAS.md`.

## Como o projeto funciona, resumidamente

1. Cada template (Vôlei, Salão) e a plataforma comercial têm sua própria pasta com: configuração (textos, preços, dados do negócio), templates HTML, e um script `build.py`.
2. Rodar `python3 build.py` lê essa configuração e gera um site pronto dentro de uma pasta `dist/`.
3. `dist/` é sempre gerado — nunca deve ser editado à mão, porque qualquer alteração ali se perde no próximo build.
4. Para mudar algo (um preço, um texto, uma cor), edita-se o arquivo de configuração ou o template-fonte, e roda-se o build de novo.

Passo a passo detalhado: veja `COMO_EXECUTAR.md`.

## Como alterar o projeto

Depende do que você quer mudar:

- **Texto ou preço** → arquivo `.json` dentro de `config/` do projeto correspondente.
- **Layout de uma página** → arquivo `.html` dentro de `templates/pages/`.
- **Cor, fonte, visual geral** → `config/*.config.json` (campo `tema`) + `templates/theme.css.j2`.
- **Regra de negócio nova** (ex.: uma nova forma de calcular parcelamento) → dentro de `commerce/`.

Depois de qualquer alteração, rode o build de novo (veja `COMO_EXECUTAR.md`) para ver o resultado.

## Como criar um novo template

Veja o passo a passo completo em `PADRAO_DE_DESENVOLVIMENTO.md`. Resumo: copia-se a estrutura de um template existente (`products/salao-de-beleza/` é o exemplo mais simples), adapta-se a configuração e as páginas para o novo nicho, e escreve-se um `build.py` seguindo o mesmo padrão dos outros dois.

**Nenhum template novo foi criado nesta rodada** — isso foi propositalmente deixado de fora, conforme pedido.

## Como fazer deploy

Veja `COMO_FAZER_DEPLOY.md`. Resumo: como o site gerado é HTML/CSS/JS puro, ele pode ser hospedado em qualquer serviço de hospedagem estática. **Isso ainda não foi configurado neste projeto** — não existe hoje nenhum domínio real conectado nem hospedagem ativa.

## Outros documentos deste projeto

- `MAPA_DO_PROJETO.md` — onde está cada pasta e por quê.
- `COMO_EXECUTAR.md` — comandos exatos para gerar os sites.
- `COMO_FAZER_DEPLOY.md` — como publicar quando estiver pronto.
- `PADRAO_DE_DESENVOLVIMENTO.md` — como criar/manter templates seguindo o mesmo padrão.
- `HISTORICO_DE_ALTERACOES.md` — o que já foi feito, em ordem.
- `../CONTROLE_DA_KE_SITES.md` — painel com o status de cada template.
- `../PROBLEMAS_E_PENDENCIAS.md` — o que precisa de atenção, por prioridade.
