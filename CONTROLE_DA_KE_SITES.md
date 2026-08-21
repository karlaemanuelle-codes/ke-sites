# CONTROLE DA KE SITES — painel técnico central

Última auditoria: 21/08/2026. Este documento é o ponto de partida para saber, rapidamente, o que existe e em que estado está.

## Templates

| Nicho | Nível | Status | Localização (fonte) | Localização (gerado) | Demo (URL pública) |
|---|---|---|---|---|---|
| Vôlei (CT/Escolinha) | Básico | Funcionando | `products/ct-de-volei/` | `products/ct-de-volei/dist/basico/` | Sem URL pública — sem hospedagem configurada, abrir o `index.html` localmente |
| Vôlei (CT/Escolinha) | Intermediário | Funcionando | `products/ct-de-volei/` | `products/ct-de-volei/dist/intermediario/` | Sem URL pública |
| Vôlei (CT/Escolinha) | Avançado | Funcionando | `products/ct-de-volei/` | `products/ct-de-volei/dist/avancado/` | Sem URL pública |
| Futebol | — | **NÃO CRIADO** | — | — | — |
| Salão de Beleza | Básico | Funcionando | `products/salao-de-beleza/` | `products/salao-de-beleza/dist/basico/` | Sem URL pública |
| Salão de Beleza | Intermediário | Funcionando | `products/salao-de-beleza/` | `products/salao-de-beleza/dist/intermediario/` | Sem URL pública |
| Salão de Beleza | Avançado | Funcionando | `products/salao-de-beleza/` | `products/salao-de-beleza/dist/avancado/` | Sem URL pública |

**Nota sobre "Localização"**: Vôlei e Salão são cada um **um único código-fonte** que gera os 3 níveis (veja `00_DOCUMENTACAO/MAPA_DO_PROJETO.md` para entender por quê). Por isso a coluna "fonte" repete a mesma pasta nas 3 linhas — a diferença real só existe depois de gerado (`dist/`).

**Nota sobre "Status"**: "Funcionando" aqui significa que o site abre, navega entre as páginas, passou nas 252 checagens automáticas de responsividade/links/acessibilidade da última auditoria, e não emite erros ao gerar. Não significa "pronto para vender para um cliente" — isso depende de personalizar o conteúdo (fotos, textos, preços reais do cliente) antes da entrega, o que ainda não foi feito para nenhum cliente real (veja a seção "Clientes" abaixo).

## Plataforma comercial (site da KE Sites)

| Item | Status | Localização |
|---|---|---|
| Home, Templates, Planos, Comparação | Funcionando | `platform/dist/<idioma>/index.html` |
| Formulário de personalização | Funcionando (demonstração — não envia dado real) | `personalizar.html` |
| Checkout (Pix/Cartão/Parcelamento) | Funcionando (demonstração — não processa pagamento real) | `checkout.html` |
| Páginas de Afiliados / Partners | Funcionando (captura de interesse — sem cadastro/dashboard real) | `afiliados.html` / `partners.html` |
| Idiomas | pt-BR, en-US, es-ES — todos gerando sem erro | `platform/dist/{pt-br,en-us,es-es}/` |

## Clientes

| Item | Status |
|---|---|
| Projetos personalizados para clientes reais | **NÃO CRIADO** — nenhum cliente ainda teve um template personalizado e entregue |

## Motor de pagamentos (`commerce/`)

| Item | Status |
|---|---|
| Calculadora de Pix/parcelamento | Funcionando e testada (42 testes automatizados) |
| Comissão de afiliado | Funcionando e testada |
| Conexão com gateway real (Ton/Stripe/Mercado Pago) | **NÃO CONECTADO** — precisa de conta e credenciais reais |

## Componentes reutilizáveis

| Componente | Reaproveitamento real |
|---|---|
| `main.js`, `modal.js` | Idênticos nos 3 projetos — 100% compartilhados na prática |
| `base.css`, `components.css` | ~99% idênticos nos 3 projetos |
| `header.html`, `footer.html`, `head.html`, `cta_final.html` | Parecidos, mas com lógica própria por projeto (a plataforma não tem o controle de nível que os produtos têm) |
| `engine/factory_engine.py` | Motor genérico, usado pelos 2 templates e pela plataforma |
| `commerce/` | Motor de pagamentos, pronto para qualquer template/plataforma usar |

## Infraestrutura

| Item | Status |
|---|---|
| Controle de versão (git) | **NÃO CONFIGURADO** |
| Backup | Criado em 21/08/2026 → `06_BACKUPS/ke-sites-BACKUP-2026-08-21_1136.tar.gz` |
| Hospedagem/domínio | **NÃO CONFIGURADO** |
