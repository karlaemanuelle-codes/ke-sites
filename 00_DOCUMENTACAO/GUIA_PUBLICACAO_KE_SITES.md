# GUIA DE PUBLICAÇÃO — KE Sites

Guia operacional para a Karla seguir, passo a passo, quando decidir publicar o primeiro site de verdade. Nada neste guia foi executado ainda — é o roteiro para quando você autorizar cada etapa.

## A. Preparação do projeto

Antes de publicar qualquer coisa: rode o build do produto desejado (`python3 build.py` dentro de `products/<produto>/` ou `platform/`), confira o resultado em `dist/<nível>/` abrindo o `index.html` localmente, e revise se ainda há conteúdo "DEMO ONLY" (depoimentos fictícios, preços de exemplo) que precisa virar real antes de mostrar a um cliente pagante.

## B. Git

O projeto já tem um repositório Git local (criado em 21/08/2026, commit inicial `chore: snapshot inicial da KE Sites antes da publicação`). A partir de agora, sempre que fizer uma mudança importante:

```
git add <arquivos alterados>
git commit -m "descrição curta da mudança"
```

Use `git status` a qualquer momento para ver o que mudou desde o último commit, e `git log --oneline` para ver o histórico.

## C. GitHub (quando decidir conectar)

1. Crie uma conta em github.com (ação seu/ChatGPT).
2. Crie um repositório novo, vazio (sem README/gitignore automático, já temos os nossos).
3. Copie a URL do repositório (formato `https://github.com/<usuario>/<repo>.git`).
4. Rode, dentro de `ke-sites/`:
   ```
   git remote add origin https://github.com/<usuario>/<repo>.git
   git push -u origin main
   ```
5. Quando o Git pedir autenticação, use um **Personal Access Token** (não a senha da conta) — o GitHub tem uma tela própria para gerar isso, com permissão mínima necessária (`repo`).

**Nunca** cole token/senha em conversa com IA nenhuma, nem salve em arquivo dentro do projeto. Se precisar automatizar isso no futuro (CI/CD), o token fica configurado como "secret" dentro das configurações do próprio GitHub/Cloudflare — nunca em texto no repositório.

## D. Cloudflare (quando decidir conectar)

1. Crie conta em cloudflare.com (ação sua).
2. No terminal, rode `npx wrangler login` — abre uma aba no navegador para você autorizar (autenticação seu, não da IA).
3. Crie um projeto Cloudflare Pages (via painel web ou `npx wrangler pages project create <nome>`).

## E. Build

Cada produto/plataforma tem seu próprio `build.py`. Rode com Python 3:
```
cd products/ct-de-volei && python3 build.py
cd products/salao-de-beleza && python3 build.py
cd platform && python3 build.py
```
O resultado sempre fica em `dist/` dentro da respectiva pasta.

## F. Publicação

Com o Wrangler autenticado (passo D), publicar o conteúdo de uma pasta `dist/<nível>` específica:
```
npx wrangler pages deploy products/ct-de-volei/dist/basico --project-name=<nome-do-projeto>
```
Isso sobe **o conteúdo estático** — não precisa de servidor, banco de dados ou backend.

## G. Domínio

Fluxo geral:
```
DOMÍNIO → DNS → CLOUDFLARE → SITE PUBLICADO
```
Ou seja: primeiro alguém precisa ser dono do domínio (registrador como Registro.br, GoDaddy, Namecheap etc.), depois os registros DNS desse domínio apontam para a Cloudflare, e só então a Cloudflare entrega o site publicado quando alguém acessa esse domínio.

## H. DNS

A Cloudflare, depois de o domínio ser adicionado à conta, fornece os registros DNS exatos a configurar (geralmente registros `CNAME` ou `NS`, dependendo se o domínio inteiro migra para a Cloudflare ou só um subdomínio é apontado). Isso é feito no painel da Cloudflare, com base nas instruções que ela mesma mostra para o domínio específico.

## I. SSL

O Cloudflare Pages fornece certificado SSL (HTTPS) automaticamente e de graça para qualquer domínio conectado a ele — não é preciso comprar nem configurar nada manualmente para isso.

## J. Testes pós-publicação

Depois de publicar, verificar manualmente: todas as páginas abrem sem erro 404; imagens carregam; formulários/WhatsApp/links de contato apontam para o número/e-mail certo do cliente; o site abre corretamente em celular (responsividade); o certificado HTTPS está ativo (cadeado no navegador).

## K. Como atualizar um cliente

1. Edite os dados do cliente em `config/data/*.json` e/ou `config/<produto>.config.json` (nunca direto no HTML gerado).
2. Rode o build de novo (passo E).
3. Rode o deploy de novo (passo F) — a Cloudflare substitui a versão publicada pela nova automaticamente.
4. Registre a mudança em `HISTORICO_DE_ALTERACOES.md` e faça um commit Git (passo B).

## L. Como fazer backup

Antes de qualquer mudança grande, gere uma cópia do projeto (`tar -czf` ou `zip`) e guarde fora deste ambiente (computador pessoal, nuvem própria). O Git (passo B) já guarda um histórico de versões do código, mas não substitui um backup externo do projeto inteiro — são proteções complementares.

## M. Como reverter uma publicação

- **Se o problema está no código**: use `git log` para achar o commit anterior bom, e `git checkout <commit> -- <arquivo>` para trazer de volta só aquele arquivo, ou `git revert <commit>` para desfazer uma mudança específica mantendo o histórico. Depois, rode build (E) e deploy (F) de novo.
- **Se o problema está só na publicação** (o código local está bom): a Cloudflare Pages mantém um histórico de deploys anteriores no próprio painel, com um botão de "Rollback"/"Reverter" para a versão publicada anterior — sem precisar mexer no código.
