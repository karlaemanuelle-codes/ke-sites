# COMO EXECUTAR — passo a passo

## O que você precisa ter instalado

- Python 3.11 ou mais novo.
- As bibliotecas Python do projeto: `Jinja2`, `markupsafe` (vêm juntas), e, só para rodar os testes automatizados, `pytest` e `playwright`.

Para instalar tudo de uma vez (rode um destes comandos no terminal, dentro da pasta do projeto):

```
pip install jinja2 markupsafe pytest playwright --break-system-packages
python3 -m playwright install chromium
```

(O `playwright install` só é necessário se você quiser rodar os testes visuais — não é necessário para apenas gerar os sites.)

## Gerar o Template-Mestre do Salão de Beleza

```
cd products/salao-de-beleza
python3 build.py
```

Isso gera os 3 níveis dentro de `products/salao-de-beleza/dist/` (`basico/`, `intermediario/`, `avancado/`). Para gerar só um nível:

```
python3 build.py --tier basico
```

## Gerar o Template-Mestre do CT de Vôlei

```
cd products/ct-de-volei
python3 build.py
```

Mesmo funcionamento do Salão — gera `dist/basico/`, `dist/intermediario/`, `dist/avancado/`, com a opção `--tier`.

## Gerar a plataforma comercial (site da KE Sites)

```
cd platform
python3 build.py
```

Isso gera as 3 versões de idioma dentro de `platform/dist/` (`pt-br/`, `en-us/`, `es-es/`), e também copia os dois templates prontos para `platform/dist/demos/` (é o que faz os botões "Ver demonstração" do site da KE Sites funcionarem).

⚠️ **Importante**: gere sempre os dois templates (Salão e Vôlei) *antes* de gerar a plataforma, porque a plataforma copia o resultado deles para dentro de si. Se você gerar só a plataforma sem antes gerar os templates, vai aparecer um aviso no terminal e as demonstrações não vão funcionar.

Ordem recomendada, sempre que quiser gerar tudo do zero:

```
cd products/salao-de-beleza && python3 build.py && cd ../..
cd products/ct-de-volei && python3 build.py && cd ../..
cd platform && python3 build.py && cd ..
```

## Como ver o resultado

Depois de gerar, abra o arquivo `index.html` da pasta `dist/` correspondente diretamente no seu navegador (duplo clique, ou arrastar para o navegador). Exemplos:

- `products/salao-de-beleza/dist/intermediario/index.html`
- `products/ct-de-volei/dist/basico/index.html`
- `platform/dist/pt-br/index.html`

Não é necessário nenhum servidor rodando — são páginas HTML comuns.

## Como rodar os testes do motor de pagamentos

```
cd /home/claude/ke-sites
python3 -m pytest commerce/tests/ -v
```

Isso roda 42 testes que verificam se a calculadora de parcelamento, o motor de comissão e o motor de promoções estão calculando corretamente. Se algum teste falhar depois de uma alteração no código de `commerce/`, é sinal de que algo quebrou.

## Erros comuns

- **`ModuleNotFoundError: No module named 'jinja2'`** → falta instalar as dependências (veja o primeiro comando desta página).
- **`FileNotFoundError` apontando para `engine/factory_engine.py`** → você rodou o `build.py` de fora da pasta do projeto, ou moveu a pasta `engine/` sem atualizar o caminho. Os `build.py` esperam encontrar `engine/` um nível acima da pasta `products/`/`platform/` (veja `MAPA_DO_PROJETO.md`).
- **Demonstrações não abrem no site da plataforma** → os templates (Salão/Vôlei) não foram gerados antes da plataforma. Rode os dois primeiros comandos da "ordem recomendada" acima antes de gerar a plataforma.
