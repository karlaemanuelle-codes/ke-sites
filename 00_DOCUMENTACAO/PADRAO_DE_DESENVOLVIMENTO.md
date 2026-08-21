# PADRÃO DE DESENVOLVIMENTO — como manter a consistência ao crescer

Este documento explica as regras não-escritas que os dois Templates-Mestre existentes (Salão de Beleza, CT de Vôlei) já seguem, para que um template novo (Futebol, Barbearia, etc.) siga o mesmo padrão em vez de reinventar a estrutura.

## Regra 1 — Um template = uma pasta em `products/`, com 3 níveis gerados, nunca 3 pastas de código

Cada template tem: `build.py`, `config/` (dados + configuração visual), `templates/` (páginas Jinja2), `assets/` (CSS/JS/imagens-fonte). O `build.py` lê um `TIER_RANK` (`basico=1, intermediario=2, avancado=3`) e cada página/seção decide se aparece ou não comparando com esse número. **Nunca duplique o HTML de uma página para cada nível** — use a lógica de nível dentro do mesmo template.

## Regra 2 — O motor compartilhado (`engine/factory_engine.py`) é o lugar certo para lógica genérica

Se uma função vai ser útil para qualquer template futuro (gerar um link de WhatsApp, formatar dinheiro, montar um placeholder de imagem, montar JSON-LD), ela entra em `engine/factory_engine.py` — não é reescrita dentro de cada `build.py`. Isso já aconteceu com `make_i18n_fn` e `make_money_fn`, criadas para a plataforma e reaproveitáveis por qualquer produto futuro que precise de idiomas/moedas.

## Regra 3 — Nunca inventar conteúdo, preço ou funcionalidade

Todo conteúdo fictício (depoimentos de exemplo, números de exemplo, funcionalidades ainda não implementadas) precisa ser claramente identificado como demonstração — o padrão usado é a badge visual `.badge-demo` com o texto "⚠️ DEMO ONLY". Um painel administrativo de demonstração, por exemplo, precisa deixar claro que é uma simulação, não um sistema real.

## Regra 4 — Preços e textos comerciais ficam em `config/`, nunca no meio do HTML

Nenhum preço, taxa de comissão ou condição comercial deve estar escrito diretamente dentro de um arquivo `.html`. Eles vivem em arquivos `.json` dentro de `config/` (ex.: `planos_comparacao.json`, `manutencao.json`), e o template só lê essas variáveis. Isso é o que permite mudar um preço em um lugar só, sem procurar em 16 páginas.

## Regra 5 — Textos visíveis passam pela função `t()`, nunca ficam hardcoded (na plataforma)

A plataforma comercial (que precisa funcionar em 3 idiomas) nunca escreve um texto direto no HTML — sempre usa `{{ t('chave.do.texto') }}`, e o texto real mora nos arquivos `config/i18n/*.json`. Se uma chave não existir em algum idioma, ela aparece literalmente na tela (isso é proposital — torna o erro visível em vez de escondido). Os dois Templates-Mestre (Salão, Vôlei) hoje são só em português e não usam esse sistema — se um dia precisarem virar multilíngue, esse é o padrão a seguir.

## Regra 6 — `dist/` nunca é editado à mão

Qualquer edição direta dentro de uma pasta `dist/` se perde no próximo build. Se algo está errado no resultado gerado, o conserto é sempre no arquivo-fonte (`templates/`, `config/`, `assets/`) seguido de um novo build.

## Passo a passo para criar um template novo (ex.: Futebol)

1. Copie a pasta `products/salao-de-beleza/` inteira para `products/futebol/` (ela é o exemplo mais simples dos dois existentes).
2. Renomeie o arquivo de configuração principal (`config/salon.config.json` → algo como `config/futebol.config.json`) e ajuste seu conteúdo (nome do negócio, cores do tema, textos).
3. Ajuste os arquivos dentro de `config/data/` para os dados reais do nicho (nomes de serviços, profissionais/treinadores, planos).
4. Ajuste as páginas dentro de `templates/pages/` para o vocabulário do nicho (ex.: "agendamento" pode virar "matrícula", como já foi feito no Vôlei).
5. Ajuste `build.py` — ele referencia os nomes de arquivo de `config/data/` e a lista de páginas; precisa bater com o que existe de verdade na pasta.
6. Rode `python3 build.py` e confira o resultado nos 3 níveis antes de considerar pronto.
7. Registre o novo template em `CONTROLE_DA_KE_SITES.md`.

**Nenhum template novo foi criado nesta rodada** — este é só o roteiro para quando decidirem fazer.

## Padrão de commits/histórico

Hoje o projeto não tem controle de versão (git) configurado — veja `PROBLEMAS_E_PENDENCIAS.md`. Enquanto isso não existir, o registro de mudanças importantes deve ser feito manualmente em `HISTORICO_DE_ALTERACOES.md`.
