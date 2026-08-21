# Template-Mestre KE Sites — Salão de Beleza

Template Factory comercial e reutilizável para o nicho de salão de beleza, em 3 níveis: **Básico**, **Intermediário** e **Avançado / Template-Mestre**. Arquitetura copiada do Template-Mestre de CT de Vôlei (teoria de níveis, configuração central, reutilização), com todo o conteúdo adaptado para salão de beleza.

## Como gerar o site

```
pip install jinja2 markupsafe   # se necessário
python3 build.py                # gera os 3 níveis em dist/
python3 build.py --tier basico  # gera só um nível
```

Cada nível sai pronto para publicar em `dist/basico/`, `dist/intermediario/`, `dist/avancado/` — HTML/CSS/JS estático, sem necessidade de servidor ou build extra no destino.

## Como criar um NOVO salão (Template Factory)

Edite **apenas**:

- `config/salon.config.json` — identidade, contato, cores, tipografia, CTAs, mensagens comerciais, SEO.
- `config/data/*.json` — serviços, profissionais, depoimentos, promoções/combos, FAQ, planos do Beauty Club, vouchers, eventos, produtos.

Rode `python3 build.py` novamente. Nenhum template precisa ser tocado — cores, textos, preços, WhatsApp e todo o conteúdo vêm do config. Isso é o que torna o projeto uma fábrica de templates, não um site único.

## Estrutura

```
config/            → dados do cliente (a única coisa que muda entre salões)
templates/          → Jinja2: base + partials + páginas (nunca tem dado de cliente hardcoded)
assets/             → CSS/JS/imagens, compartilhados pelos 3 níveis
build.py            → gera dist/{basico,intermediario,avancado}/
dist/                → saída estática final, por nível
```

## Níveis

- **Básico**: presença digital completa (Home, Sobre, Serviços, Profissionais, Galeria, Localização, Contato, FAQ), CTA de agendamento via modal + WhatsApp.
- **Intermediário**: Básico + Depoimentos, Promoções/Combos, Agendamento demonstrativo (4 passos), Eventos, FAQ avançado, perfis de profissionais completos.
- **Avançado / Template-Mestre**: Intermediário + Beauty Club (planos), Área da Cliente (demo), Beauty Shop, Eventos & Noivas, Painel Administrativo (demo), Gift Cards/Vouchers, Pix simulado.

## Avisos DEMO ONLY

Agendamento, Área da Cliente, Painel Admin e pagamento via Pix são simulações client-side (sem backend, sem banco de dados, sem autenticação real, sem cobrança real), sinalizadas com o selo ⚠️ DEMO ONLY na interface. Para produção, integrar a um provedor real de agenda/pagamento/autenticação.
