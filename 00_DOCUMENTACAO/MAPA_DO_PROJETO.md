# MAPA DO PROJETO — KE Sites

Este documento mostra **onde cada coisa está de verdade** no projeto, hoje. Não é a estrutura ideal — é a estrutura real, auditada em 21/08/2026.

## Como o projeto pensa (leia isto antes do resto)

A KE Sites não guarda "Básico", "Intermediário" e "Avançado" como três pastas de código separadas. Cada template (Vôlei, Salão) tem **um único conjunto de arquivos-fonte**, e um script Python (`build.py`) gera os três níveis a partir dele, olhando um arquivo de configuração para decidir o que cada nível mostra ou esconde. Isso é proposital: é o que permite dizer "construímos uma vez, vendemos várias vezes" sem manter três cópias do mesmo código. Por isso, quando você procurar "onde está o Básico do Vôlei", a resposta é: no mesmo lugar que o Intermediário e o Avançado — a diferença só aparece depois de gerado, dentro da pasta `dist/`.

## Árvore real do projeto

```
ke-sites/
│
├── 00_DOCUMENTACAO/        ← você está aqui. Os 6 documentos pedidos.
├── 06_BACKUPS/             ← cópias de segurança completas do projeto (.tar.gz)
├── CONTROLE_DA_KE_SITES.md ← painel técnico central (templates, status, links)
├── PROBLEMAS_E_PENDENCIAS.md
│
├── engine/                          ← MOTOR COMPARTILHADO (Python)
│   └── factory_engine.py            usado pelos 2 templates E pela plataforma
│
├── commerce/                        ← MOTOR DE PAGAMENTOS (Python, testado)
│   ├── models.py, pricing.py, providers.py, commissions.py, promotions.py, webhooks.py, config.py
│   ├── tests/                       42 testes automatizados
│   └── README.md                    explica o que é real e o que não é
│
├── products/                        ← OS TEMPLATES-MESTRE (o produto que se vende)
│   │
│   ├── ct-de-volei/                 Template-Mestre "CT / Escolinha de Vôlei"
│   │   ├── build.py                 gera os 3 níveis a partir daqui
│   │   ├── config/                  dados do negócio (treinadores, modalidades, planos...)
│   │   ├── templates/               HTML (Jinja2) — 16 páginas-fonte
│   │   ├── assets/                  CSS, JS, ícones, imagens-fonte
│   │   └── dist/                    ⚠️ GERADO — não editar à mão
│   │       ├── basico/    (8 páginas)
│   │       ├── intermediario/  (12 páginas)
│   │       └── avancado/  (16 páginas)
│   │
│   └── salao-de-beleza/             Template-Mestre "Salão de Beleza"
│       └── (mesma estrutura acima — build.py, config/, templates/, assets/, dist/)
│
├── platform/                        ← A PLATAFORMA COMERCIAL (site da própria KE Sites)
│   ├── build.py                     gera pt-BR / en-US / es-ES
│   ├── config/                      preços, planos, i18n (3 idiomas), moedas
│   ├── templates/                   home, personalizar, checkout, afiliados, partners...
│   ├── assets/
│   └── dist/                        ⚠️ GERADO
│       ├── pt-br/ (7 páginas)
│       ├── en-us/ (7 páginas)
│       ├── es-es/ (7 páginas)
│       └── demos/                   cópia dos templates prontos, para os botões "Ver demonstração"
│
└── (fora deste projeto: /home/claude/entrega/ e /home/claude/entrega_docs/ — são
    os ZIPs e relatórios já enviados para você em conversas anteriores, não fazem
    parte do código-fonte do projeto)
```

## Onde está cada coisa, na prática

| Eu quero encontrar... | Está em... |
|---|---|
| O texto/preço/config de um template | `products/<template>/config/` |
| O visual (cores, fontes) de um template | `products/<template>/templates/theme.css.j2` + `config/*.config.json` |
| As páginas HTML de um template | `products/<template>/templates/pages/` |
| O site pronto do Vôlei, nível Básico | `products/ct-de-volei/dist/basico/index.html` (abrir no navegador) |
| Os preços oficiais da KE Sites (Básico/Intermediário/Avançado) | `platform/config/data/planos_comparacao.json` |
| Os textos em português/inglês/espanhol | `platform/config/i18n/pt-BR.json`, `en-US.json`, `es-ES.json` |
| A calculadora de parcelamento/Pix | `commerce/pricing.py` |
| O motor genérico que os dois templates usam | `engine/factory_engine.py` |

## Por que não usei a estrutura `01_TEMPLATES/ESPORTES/VOLEI/BASICO/INTERMEDIARIO/AVANCADO/` que você propôs

Você pediu para eu não mover nada que pudesse quebrar o projeto, e documentar em vez de mover às cegas — então é isso que estou fazendo aqui.

A estrutura que você desenhou pressupõe uma pasta de código separada para cada nível (Básico/Intermediário/Avançado). Se eu criasse isso fisicamente, eu precisaria **triplicar o código-fonte** de cada template — copiar os arquivos-fonte três vezes — porque hoje eles não existem em três versões: existem em uma, e o `build.py` decide o que aparece em cada nível. Fazer essa cópia física iria:

1. Quebrar o motivo de existir do `factory_engine.py` (ele existe justamente para evitar repetir código entre níveis);
2. Criar três lugares para corrigir o mesmo bug no futuro, em vez de um;
3. Contrariar a regra que você mesma definiu em outras conversas: "construir uma vez, personalizar muitas vezes".

Por isso eu **não movi nada** — mantive `products/ct-de-volei/` e `products/salao-de-beleza/` como estão, com um `dist/basico|intermediario|avancado/` gerado dentro de cada um (isso já entrega, na prática, a mesma coisa que você queria enxergar: um lugar por nível — só que são resultados gerados, não código duplicado).

**Se ainda assim você preferir pastas físicas por nicho** (por exemplo, um dia ter Vôlei e Futebol dentro de uma pasta comum `ESPORTES/`), isso é seguro de fazer e não quebra nada — porque hoje `ct-de-volei` e `salao-de-beleza` já são pastas irmãs dentro de `products/`, só falta agrupá-las por categoria se e quando existir um segundo template esportivo. Isso está registrado como pendência em `PROBLEMAS_E_PENDENCIAS.md`, aguardando sua decisão.

## Componentes verdadeiramente compartilhados (auditado nesta rodada)

- `main.js` e `modal.js` são **idênticos, byte a byte**, nos três projetos (`platform`, `ct-de-volei`, `salao-de-beleza`) — já são 100% reaproveitáveis, só existem em three cópias por causa de como cada `build.py` empacota os assets.
- `base.css` e `components.css` são **quase idênticos** entre os três (só mudam 2 linhas de comentário) — o sistema visual (cores, grid, responsividade) é o mesmo motor em todos.
- Os arquivos `header.html`, `footer.html`, `head.html`, `cta_final.html` **parecem** repetidos mas **não são cópias acidentais**: os templates de produto (`ct-de-volei`/`salao-de-beleza`) têm um menu que muda conforme o nível contratado (`tier_rank`), coisa que a plataforma comercial não precisa. São parecidos de propósito, mas com uma diferença funcional real.

Isso significa que existe uma oportunidade real de criar uma pasta única de componentes compartilhados de verdade (ao invés de 3 cópias de `main.js`/`modal.js`/CSS) — mas isso exigiria alterar os 3 `build.py` para apontar para um lugar comum, o que é uma mudança de código, não apenas de organização de pastas. Registrei essa oportunidade como melhoria futura em `PROBLEMAS_E_PENDENCIAS.md` — não fiz essa alteração agora porque você pediu para eu não refatorar código sem autorização.
