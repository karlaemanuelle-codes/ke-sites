# COMO FAZER DEPLOY

## Situação atual — leia isto primeiro

**Nenhum deploy foi configurado ainda neste projeto.** Não existe domínio real conectado, nem conta em nenhum serviço de hospedagem. Este documento explica *como fazer* quando você decidir publicar — não descreve algo que já está no ar.

## Por que isso é simples

Cada projeto (`products/salao-de-beleza`, `products/ct-de-volei`, `platform`) gera, dentro da sua pasta `dist/`, um conjunto de arquivos HTML, CSS, JS e imagens — nada mais. Não existe banco de dados, não existe um programa que precisa "ficar ligado" o tempo todo. Isso é chamado de **site estático**, e é o tipo mais simples e barato de publicar na internet.

## Passo a passo genérico

1. Gere o site (veja `COMO_EXECUTAR.md`) — o resultado fica em uma pasta `dist/...`.
2. Escolha um serviço de hospedagem de sites estáticos. Alguns exemplos comuns no mercado (nenhum deles está configurado aqui — é só para você conhecer as opções): Netlify, Vercel, GitHub Pages, Cloudflare Pages, ou uma hospedagem tradicional que aceite upload de arquivos (via FTP/painel).
3. Envie o **conteúdo de dentro da pasta `dist/<versão que você quer publicar>`** (não a pasta `dist/` inteira, o conteúdo de dentro dela) para o serviço escolhido.
4. Configure o domínio (se você tiver um) apontando para esse serviço, seguindo as instruções do próprio serviço escolhido.

## O que publicar de cada projeto

- **Salão de Beleza**: publicar o conteúdo de `products/salao-de-beleza/dist/<nível>/` — um nível por vez (cada nível é um site completo e independente).
- **CT de Vôlei**: mesma lógica, `products/ct-de-volei/dist/<nível>/`.
- **Plataforma comercial (site da KE Sites)**: publicar o conteúdo de `platform/dist/<idioma>/` — mas veja a nota abaixo antes.

⚠️ **Nota sobre a plataforma**: hoje, a plataforma gera 3 pastas separadas (`pt-br/`, `en-us/`, `es-es/`) e os links entre idiomas assumem que as três ficam publicadas lado a lado no mesmo domínio (o seletor de idioma no topo do site linka para `../en-us/...`, por exemplo). Isso significa que, para publicar a plataforma completa com troca de idioma funcionando, as três pastas precisam ir juntas para o mesmo lugar, mantendo essa estrutura de pastas irmãs. Publicar só uma delas isoladamente funciona, mas o seletor de idioma vai apontar para um link que não existe.

## O que NÃO fazer

- Não publicar a pasta `dist/` de um template junto com a de outro nível misturados na mesma pasta — cada nível é um site independente.
- Não publicar as pastas-fonte (`templates/`, `config/`, `build.py`) — isso é o material de construção, não o site pronto. Só o conteúdo de `dist/` deve ir para a hospedagem.
- Não publicar `commerce/` — é o motor de pagamentos em Python, não faz parte do site estático, e hoje ele não está conectado a uma conta real de pagamento (veja `commerce/README.md`).

## Checklist antes de publicar de verdade

- [ ] Gerar o build mais recente (não publicar uma versão antiga esquecida em `dist/`).
- [ ] Conferir se os textos "DEMO ONLY" e os dados fictícios (depoimentos de exemplo, números de exemplo no checkout) ainda são aceitáveis para o público que vai ver o site, ou se precisam ser substituídos por conteúdo real antes de publicar para um cliente de verdade.
- [ ] Decidir a forma de pagamento real (Ton, Stripe, Mercado Pago ou outra) e conectar de verdade — hoje o checkout é só uma simulação visual (veja `commerce/README.md` e `PROBLEMAS_E_PENDENCIAS.md`).
