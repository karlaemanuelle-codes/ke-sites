#!/usr/bin/env python3
"""
build.py — Salão de Beleza / Template-Mestre (produto KE Sites)

Curto de propósito: toda a lógica genérica vive em engine/factory_engine.py.
Aqui só existe o que é ESPECÍFICO deste nicho — rótulos de navegação, mapa de
páginas e o tipo de negócio para o JSON-LD.

PARA CRIAR UM NOVO SALÃO: edite só config/salon.config.json e config/data/*.json.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "engine"))
import factory_engine as engine  # noqa: E402

NAV_ITEMS = [
    {"id": "home", "label": "Início", "href": "index.html", "min_tier": 1},
    {"id": "servicos", "label": "Serviços", "href": "servicos.html", "min_tier": 1},
    {"id": "profissionais", "label": "Profissionais", "href": "profissionais.html", "min_tier": 1},
    {"id": "galeria", "label": "Galeria", "href": "galeria.html", "min_tier": 1},
    {"id": "promocoes", "label": "Promoções", "href": "promocoes.html", "min_tier": 2},
    {"id": "beauty-club", "label": "Beauty Club", "href": "beauty-club.html", "min_tier": 3},
    {"id": "contato", "label": "Contato", "href": "contato.html", "min_tier": 1},
]

FOOTER_LINKS = [
    {"id": "home", "label": "Início", "href": "index.html", "min_tier": 1},
    {"id": "sobre", "label": "Sobre o Salão", "href": "sobre.html", "min_tier": 1},
    {"id": "servicos", "label": "Serviços", "href": "servicos.html", "min_tier": 1},
    {"id": "profissionais", "label": "Profissionais", "href": "profissionais.html", "min_tier": 1},
    {"id": "galeria", "label": "Galeria", "href": "galeria.html", "min_tier": 1},
    {"id": "localizacao", "label": "Localização", "href": "localizacao.html", "min_tier": 1},
    {"id": "faq", "label": "Perguntas Frequentes", "href": "faq.html", "min_tier": 1},
    {"id": "contato", "label": "Contato", "href": "contato.html", "min_tier": 1},
    {"id": "depoimentos", "label": "Depoimentos", "href": "depoimentos.html", "min_tier": 2},
    {"id": "promocoes", "label": "Promoções & Combos", "href": "promocoes.html", "min_tier": 2},
    {"id": "agendamento", "label": "Agendamento", "href": "agendamento.html", "min_tier": 2},
    {"id": "eventos", "label": "Eventos & Noivas", "href": "eventos.html", "min_tier": 2},
    {"id": "beauty-club", "label": "Beauty Club", "href": "beauty-club.html", "min_tier": 3},
    {"id": "area-cliente", "label": "Área da Cliente (demo)", "href": "area-cliente.html", "min_tier": 3},
    {"id": "beauty-shop", "label": "Beauty Shop", "href": "beauty-shop.html", "min_tier": 3},
    {"id": "admin", "label": "Painel Admin (demo)", "href": "admin.html", "min_tier": 3},
]

PAGES = [
    ("pages/home.html", "index.html", "home", 1, "Salão de Beleza Premium em São Paulo", None),
    ("pages/sobre.html", "sobre.html", "sobre", 1, "Sobre o Salão", "Conheça a história, os valores e a equipe por trás do {nome}."),
    ("pages/servicos.html", "servicos.html", "servicos", 1, "Serviços", "Cabelo, estética facial e corporal, mãos e pés — conheça todos os serviços do {nome}."),
    ("pages/profissionais.html", "profissionais.html", "profissionais", 1, "Profissionais", "Conheça a equipe de especialistas do {nome}."),
    ("pages/galeria.html", "galeria.html", "galeria", 1, "Galeria", "Veja transformações e o ambiente do {nome}."),
    ("pages/localizacao.html", "localizacao.html", "localizacao", 1, "Localização", "Endereço, mapa e horário de funcionamento do {nome}."),
    ("pages/contato.html", "contato.html", "contato", 1, "Contato", "Fale com o {nome} pelo WhatsApp, e-mail ou formulário."),
    ("pages/faq.html", "faq.html", "faq", 1, "Perguntas Frequentes", "Tire suas dúvidas sobre agendamento, pagamento e serviços do {nome}."),
    ("pages/depoimentos.html", "depoimentos.html", "depoimentos", 2, "Depoimentos", "Veja o que nossas clientes dizem sobre o {nome}."),
    ("pages/promocoes.html", "promocoes.html", "promocoes", 2, "Promoções & Combos", "Promoções ativas e combos especiais do {nome}."),
    ("pages/agendamento.html", "agendamento.html", "agendamento", 2, "Agendamento", "Agende seu horário no {nome} — simulação de agendamento online."),
    ("pages/eventos.html", "eventos.html", "eventos", 2, "Eventos & Noivas", "Eventos exclusivos e pacotes para noivas do {nome}."),
    ("pages/beauty-club.html", "beauty-club.html", "beauty-club", 3, "Beauty Club", "Conheça os planos de assinatura Beauty Club do {nome}."),
    ("pages/area-cliente.html", "area-cliente.html", "area-cliente", 3, "Área da Cliente", "Acompanhe agendamentos, pontos e vouchers — ambiente de demonstração."),
    ("pages/beauty-shop.html", "beauty-shop.html", "beauty-shop", 3, "Beauty Shop", "Produtos profissionais selecionados pelo {nome}."),
    ("pages/admin.html", "admin.html", "admin", 3, "Painel Administrativo", "Painel administrativo de demonstração do {nome}."),
]

TIER_LABELS = {"basico": "Básico", "intermediario": "Intermediário", "avancado": "Avançado / Template-Mestre"}

DATA_FILES = {
    "servicos": "servicos", "profissionais": "profissionais", "depoimentos": "depoimentos",
    "promocoes": "promocoes", "faq": "faq", "planos": "planos", "vouchers": "vouchers",
    "eventos": "eventos", "produtos": "produtos",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=list(engine.TIER_RANK.keys()), default=None)
    args = parser.parse_args()

    engine.build_product(
        root=ROOT,
        config_path=ROOT / "config" / "salon.config.json",
        data_dir=ROOT / "config" / "data",
        data_files=DATA_FILES,
        templates_dir=ROOT / "templates",
        assets_dir=ROOT / "assets",
        dist_dir=ROOT / "dist",
        nav_items=NAV_ITEMS,
        footer_links=FOOTER_LINKS,
        pages=PAGES,
        tier_labels=TIER_LABELS,
        jsonld_type="BeautySalon",
        member_org_suffix="Beauty Club",
        canonical_base="https://salao.kesites.exemplo",
        tiers=[args.tier] if args.tier else None,
    )


if __name__ == "__main__":
    main()
