#!/usr/bin/env python3
"""
build.py — CT de Vôlei / Template-Mestre (produto KE Sites)

Mesma engine do Salão de Beleza (engine/factory_engine.py) — prova viva de
que a arquitetura da Template Factory é genérica: só o que está neste
arquivo (rótulos, mapa de páginas, tipo de negócio) e em config/ muda entre
nichos. CSS, JS e o motor de geração são 100% reaproveitados.

PARA CRIAR UM NOVO CT: edite só config/volei.config.json e config/data/*.json.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "engine"))
import factory_engine as engine  # noqa: E402

NAV_ITEMS = [
    {"id": "home", "label": "Início", "href": "index.html", "min_tier": 1},
    {"id": "modalidades", "label": "Modalidades", "href": "modalidades.html", "min_tier": 1},
    {"id": "treinadores", "label": "Treinadores", "href": "treinadores.html", "min_tier": 1},
    {"id": "galeria", "label": "Galeria", "href": "galeria.html", "min_tier": 1},
    {"id": "planos-combos", "label": "Planos & Combos", "href": "planos-combos.html", "min_tier": 2},
    {"id": "clube-do-atleta", "label": "Clube do Atleta", "href": "clube-do-atleta.html", "min_tier": 3},
    {"id": "contato", "label": "Contato", "href": "contato.html", "min_tier": 1},
]

FOOTER_LINKS = [
    {"id": "home", "label": "Início", "href": "index.html", "min_tier": 1},
    {"id": "sobre", "label": "Sobre o Clube", "href": "sobre.html", "min_tier": 1},
    {"id": "modalidades", "label": "Modalidades", "href": "modalidades.html", "min_tier": 1},
    {"id": "treinadores", "label": "Treinadores", "href": "treinadores.html", "min_tier": 1},
    {"id": "galeria", "label": "Galeria", "href": "galeria.html", "min_tier": 1},
    {"id": "localizacao", "label": "Localização", "href": "localizacao.html", "min_tier": 1},
    {"id": "faq", "label": "Perguntas Frequentes", "href": "faq.html", "min_tier": 1},
    {"id": "contato", "label": "Contato", "href": "contato.html", "min_tier": 1},
    {"id": "depoimentos", "label": "Depoimentos", "href": "depoimentos.html", "min_tier": 2},
    {"id": "planos-combos", "label": "Planos & Combos", "href": "planos-combos.html", "min_tier": 2},
    {"id": "matricula", "label": "Matrícula", "href": "matricula.html", "min_tier": 2},
    {"id": "eventos", "label": "Eventos & Torneios", "href": "eventos.html", "min_tier": 2},
    {"id": "clube-do-atleta", "label": "Clube do Atleta", "href": "clube-do-atleta.html", "min_tier": 3},
    {"id": "area-do-atleta", "label": "Área do Atleta (demo)", "href": "area-do-atleta.html", "min_tier": 3},
    {"id": "loja", "label": "Loja do Atleta", "href": "loja.html", "min_tier": 3},
    {"id": "admin", "label": "Painel Admin (demo)", "href": "admin.html", "min_tier": 3},
]

PAGES = [
    ("pages/home.html", "index.html", "home", 1, "Centro de Treinamento de Vôlei no Rio de Janeiro", None),
    ("pages/sobre.html", "sobre.html", "sobre", 1, "Sobre o Clube", "Conheça a história, os valores e a comissão técnica do {nome}."),
    ("pages/modalidades.html", "modalidades.html", "modalidades", 1, "Modalidades", "Vôlei de quadra, vôlei de praia e turmas especiais — conheça todas as modalidades do {nome}."),
    ("pages/treinadores.html", "treinadores.html", "treinadores", 1, "Treinadores", "Conheça a comissão técnica do {nome}."),
    ("pages/galeria.html", "galeria.html", "galeria", 1, "Galeria", "Veja treinos, torneios e a estrutura do {nome}."),
    ("pages/localizacao.html", "localizacao.html", "localizacao", 1, "Localização", "Endereço, mapa e horário de funcionamento do {nome}."),
    ("pages/contato.html", "contato.html", "contato", 1, "Contato", "Fale com o {nome} pelo WhatsApp, e-mail ou formulário."),
    ("pages/faq.html", "faq.html", "faq", 1, "Perguntas Frequentes", "Tire suas dúvidas sobre matrícula, pagamento e modalidades do {nome}."),
    ("pages/depoimentos.html", "depoimentos.html", "depoimentos", 2, "Depoimentos", "Veja o que nossos alunos dizem sobre o {nome}."),
    ("pages/planos-combos.html", "planos-combos.html", "planos-combos", 2, "Planos & Combos", "Promoções ativas e combos especiais do {nome}."),
    ("pages/matricula.html", "matricula.html", "matricula", 2, "Matrícula", "Matricule-se no {nome} — simulação de matrícula online."),
    ("pages/eventos.html", "eventos.html", "eventos", 2, "Eventos & Torneios", "Eventos, torneios e pacotes especiais do {nome}."),
    ("pages/clube-do-atleta.html", "clube-do-atleta.html", "clube-do-atleta", 3, "Clube do Atleta", "Conheça os planos de assinatura Clube do Atleta do {nome}."),
    ("pages/area-do-atleta.html", "area-do-atleta.html", "area-do-atleta", 3, "Área do Atleta", "Acompanhe treinos, frequência e vouchers — ambiente de demonstração."),
    ("pages/loja.html", "loja.html", "loja", 3, "Loja do Atleta", "Materiais esportivos selecionados pelo {nome}."),
    ("pages/admin.html", "admin.html", "admin", 3, "Painel Administrativo", "Painel administrativo de demonstração do {nome}."),
]

TIER_LABELS = {"basico": "Básico", "intermediario": "Intermediário", "avancado": "Avançado / Template-Mestre"}

DATA_FILES = {
    "servicos": "modalidades", "treinadores": "treinadores", "depoimentos": "depoimentos",
    "promocoes": "planos_combos", "faq": "faq", "planos": "planos_clube", "vouchers": "creditos",
    "eventos": "eventos", "produtos": "produtos",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=list(engine.TIER_RANK.keys()), default=None)
    args = parser.parse_args()

    engine.build_product(
        root=ROOT,
        config_path=ROOT / "config" / "volei.config.json",
        data_dir=ROOT / "config" / "data",
        data_files=DATA_FILES,
        templates_dir=ROOT / "templates",
        assets_dir=ROOT / "assets",
        dist_dir=ROOT / "dist",
        nav_items=NAV_ITEMS,
        footer_links=FOOTER_LINKS,
        pages=PAGES,
        tier_labels=TIER_LABELS,
        jsonld_type="SportsActivityLocation",
        member_org_suffix="Clube do Atleta",
        canonical_base="https://volei.kesites.exemplo",
        tiers=[args.tier] if args.tier else None,
    )


if __name__ == "__main__":
    main()
