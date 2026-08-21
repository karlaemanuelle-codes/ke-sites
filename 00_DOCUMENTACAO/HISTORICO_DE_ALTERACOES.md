# HISTÓRICO DE ALTERAÇÕES

## Aviso importante sobre este documento

Este projeto **não tem controle de versão (git)** configurado (veja `PROBLEMAS_E_PENDENCIAS.md`). Isso significa que não existe um histórico automático e confiável de "quem mudou o quê e quando" antes de hoje — o que segue é reconstruído a partir das datas reais dos arquivos no sistema e do que foi conversado. A partir de agora, a forma mais confiável de manter esse histórico é configurar o git (recomendado, pendente de autorização) ou continuar atualizando este arquivo manualmente a cada rodada de mudanças importantes.

## Linha do tempo verificável (datas reais dos arquivos, UTC)

**20/08/2026, a partir de ~22h30** — Construção da base do projeto: os dois Templates-Mestre (Salão de Beleza e CT de Vôlei) e a primeira versão da plataforma comercial (`platform/`), com arquitetura de 3 níveis, motor compartilhado (`engine/factory_engine.py`), internacionalização (pt-BR/en-US/es-ES) e sistema de moedas.

**20/08/2026, ~23h30** — Ajustes de consistência entre o CT de Vôlei e o Salão de Beleza (remoção de conteúdo de um template que havia vazado para o outro por engano), e correção de um bug real de layout (um painel administrativo de demonstração que "estourava" a largura da tela no celular, escondido por um efeito colateral de CSS que mascarava o problema nas checagens automáticas).

**21/08/2026, ~00h30–01h00** — Evolução comercial da plataforma ("V2"): preço oficial + preço promocional de lançamento lado a lado, opção "Sob Medida", seção de Manutenção (R$149/249/399), páginas de Afiliados e Partners, e um motor de pagamentos (`commerce/`) com calculadora de parcelamento, comissão de afiliado e promoções — tudo testado (42 testes automatizados) e claramente identificado como demonstração onde ainda não há conexão com um gateway de pagamento real.

**21/08/2026, a partir de ~11h30** — Auditoria técnica completa, backup do projeto, e criação desta documentação (`00_DOCUMENTACAO/`, `CONTROLE_DA_KE_SITES.md`, `PROBLEMAS_E_PENDENCIAS.md`). Nenhum código foi alterado nesta etapa — só organização e documentação.

## Sobre o que veio antes de 20/08/2026

Sei, pelo contexto da nossa conversa, que houve trabalho em fases anteriores a essa janela de tempo (referidas como pedidos anteriores sobre o Salão de Beleza e o CT de Vôlei). Não tenho como confirmar datas exatas dessas fases a partir dos arquivos atuais — por isso não estou inventando datas para elas aqui. Se você tiver esse histórico anotado em algum outro lugar (conversas anteriores, anotações pessoais), vale a pena colar aqui para completar esta linha do tempo.

## Como manter este arquivo daqui para frente

Sempre que uma mudança importante for feita (novo template, mudança de preço, nova página, correção de um bug relevante), adicione uma linha nova aqui, no topo, com a data e uma frase curta. Isso substitui, de forma manual, o que um `git log` faria automaticamente — por isso configurar o git é uma recomendação forte em `PROBLEMAS_E_PENDENCIAS.md`.
