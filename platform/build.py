#!/usr/bin/env python3
"""
build.py — KE Sites / Plataforma Comercial (Template Factory + Multinicho)

Gera a plataforma em 3 idiomas (pt-BR, en-US, es-ES) a partir de UMA ÚNICA
arquitetura: mesmos templates, mesmo motor de tema (theme.css.j2), mesmos
componentes (base.css/components.css reaproveitados dos produtos) — o que
muda por idioma é só o dicionário em config/i18n/<locale>.json e a moeda
ativa (config/data/moedas.json). Não existem 3 plataformas: existe 1
plataforma com 3 saídas.

Também copia as demonstrações reais dos dois Templates-Mestre oficiais
(Salão de Beleza e CT de Vôlei) para dist/demos/, para que os botões
"VER DEMONSTRAÇÃO" apontem para sites de verdade, não para imagens.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PRODUCTS_DIR = ROOT.parent / "products"
sys.path.insert(0, str(ROOT.parent / "engine"))
sys.path.insert(0, str(ROOT.parent))
import factory_engine as engine  # noqa: E402
from commerce.config import default_commerce_config  # noqa: E402
from commerce.pricing import calculate_installment_table, calculate_pix_price, calculate_price  # noqa: E402

LOCALES = ["pt-BR", "en-US", "es-ES"]
LOCALE_SLUG = {"pt-BR": "pt-br", "en-US": "en-us", "es-ES": "es-es"}
THOUSANDS_SEP = {"pt-BR": ".", "en-US": ",", "es-ES": "."}

PAGES = [
    ("pages/home.html", "index.html", "home", "hero.titulo", "hero.subtitulo", None),
    ("pages/personalizar.html", "personalizar.html", "personalizar", "form.titulo", "form.subtitulo", None),
    ("pages/obrigado.html", "obrigado.html", "obrigado", "obrigado.titulo", "obrigado.texto", None),
    ("pages/contato.html", "contato.html", "contato", "nav.contato", "ctaFinalSection.subtitulo", None),
    ("pages/parceria.html", "afiliados.html", "afiliados", "parceria.afiliado.titulo", "parceria.afiliado.subtitulo", {"tipo": "afiliado"}),
    ("pages/parceria.html", "partners.html", "partners", "parceria.partner.titulo", "parceria.partner.subtitulo", {"tipo": "partner"}),
    ("pages/checkout.html", "checkout.html", "checkout", "checkout.titulo", "checkout.subtitulo", None),
]

# Métodos de pagamento realmente disponíveis por mercado (seção 55 do
# adendo de pagamentos: "nunca mostrar um método indisponível"). Pix e
# parcelamento em cartão brasileiro são práticas específicas do mercado
# brasileiro — não fazem sentido fora do Brasil, então não são simulados
# para en-US/es-ES.
PAYMENT_METHODS_BY_LOCALE = {
    "pt-BR": ["pix", "cartao_avista", "cartao_parcelado"],
    "en-US": ["cartao_avista"],
    "es-ES": ["cartao_avista"],
}


def build_checkout_pricing(*, locale, planos_comparacao, manutencao, money, commerce_config):
    """Pré-calcula, no build (Python, testado em commerce/tests/), os
    valores de Pix/à vista/parcelado de cada plano — o checkout.html só
    exibe esses números prontos via JS, nunca inventa um cálculo no
    navegador. Só o mercado brasileiro recebe Pix/parcelamento; os demais
    mercados recebem apenas o preço à vista no cartão, na moeda local."""
    is_brazil = locale == "pt-BR"
    data = {"planos": {}, "manutencao": {}}

    for plano in planos_comparacao["planos"]:
        amount_brl = plano["precoPromoBRL"]
        entry = {"nomeKey": plano["nomeKey"], "precoDisplay": money(amount_brl)}
        if is_brazil:
            pix = calculate_pix_price(amount=amount_brl, config=commerce_config)
            avista = calculate_price(amount=amount_brl, method="CREDIT_AVISTA", installments=1, config=commerce_config)
            parcelas = calculate_installment_table(amount=amount_brl, config=commerce_config)
            entry["pix"] = {"total": pix.customer_total, "label": pix.label}
            entry["avista"] = {"total": avista.customer_total, "label": avista.label}
            entry["parcelas"] = [
                {"n": opt.installments, "valor": opt.installment_value, "total": opt.customer_total, "label": opt.label}
                for opt in parcelas if opt.installments > 1
            ]
        data["planos"][plano["id"]] = entry

    for plano in manutencao:
        amount_brl = plano["precoMesBRL"]
        entry = {"nomeKey": plano["nomeKey"], "precoDisplay": money(amount_brl) + "/mês"}
        if is_brazil:
            pix = calculate_pix_price(amount=amount_brl, config=commerce_config)
            avista = calculate_price(amount=amount_brl, method="CREDIT_AVISTA", installments=1, config=commerce_config)
            entry["pix"] = {"total": pix.customer_total, "label": pix.label}
            entry["avista"] = {"total": avista.customer_total, "label": avista.label}
            entry["parcelas"] = []  # assinatura recorrente — não parcelamos uma cobrança mensal (seção 17)
        data["manutencao"][plano["id"]] = entry

    return data

OFFICIAL_PRODUCTS = ["salao-de-beleza", "ct-de-volei"]


def copy_demos(dist_dir):
    """Copia o dist/ (já buildado) de cada Template-Mestre oficial para
    dist/demos/<produto>/ — os botões "VER DEMONSTRAÇÃO" da plataforma
    apontam para essas cópias, sites reais e navegáveis nos 3 níveis."""
    demos_dir = dist_dir / "demos"
    if demos_dir.exists():
        shutil.rmtree(demos_dir)
    demos_dir.mkdir(parents=True)
    for product in OFFICIAL_PRODUCTS:
        src = PRODUCTS_DIR / product / "dist"
        if not src.exists():
            print(f"[aviso] {product}: dist/ não encontrado — rode o build.py do produto antes.")
            continue
        shutil.copytree(src, demos_dir / product)
        print(f"[demos] {product} copiado para dist/demos/{product}/")


def build_jsonld_org(config, description, site_url):
    import json
    ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": config["identidade"]["nome"],
        "url": site_url,
        "description": description,
        "logo": f"{site_url}/{config['identidade']['favicon']}",
        "sameAs": [config["identidade"]["instagramLink"]],
    }
    return json.dumps(ld, ensure_ascii=False, indent=2)


def render_locale(*, env, config, locale, data, dist_dir):
    slug = LOCALE_SLUG[locale]
    locale_dir = dist_dir / slug
    if locale_dir.exists():
        shutil.rmtree(locale_dir)
    locale_dir.mkdir(parents=True)

    shutil.copytree(ROOT / "assets", locale_dir / "assets", dirs_exist_ok=True)
    theme_tpl = env.get_template("theme.css.j2")
    (locale_dir / "assets" / "css" / "theme.css").write_text(
        theme_tpl.render(tema=config["tema"]), encoding="utf-8"
    )

    i18n_dict = engine.load_json(ROOT / "config" / "i18n" / f"{locale}.json")
    t = engine.make_i18n_fn(i18n_dict)

    moeda_codigo = config["moedaPadraoPorLocale"][locale]
    moedas = data["moedas"]
    money = engine.make_money_fn(moedas[moeda_codigo], thousands_sep=THOUSANDS_SEP[locale])

    ph = engine.make_placeholder_fn(config)
    whatsapp_link = engine.make_whatsapp_fn(config)

    commerce_config = default_commerce_config()
    checkout_pricing = build_checkout_pricing(
        locale=locale,
        planos_comparacao=data["planos_comparacao"],
        manutencao=data["manutencao"],
        money=money,
        commerce_config=commerce_config,
    )
    payment_methods = PAYMENT_METHODS_BY_LOCALE[locale]

    def locale_href(target_locale):
        target_slug = LOCALE_SLUG[target_locale]
        return f"../{target_slug}/{env.globals.get('_current_out_name', 'index.html')}"

    env.globals["t"] = t
    env.globals["money"] = money
    env.globals["ph"] = ph
    env.globals["whatsapp_link"] = whatsapp_link
    env.globals["locale_href"] = locale_href
    env.globals["locales"] = LOCALES

    site_url = config["seo"]["siteUrl"]
    generated = []
    for tpl_name, out_name, page_id, title_key, desc_key, extra_context in PAGES:
        env.globals["_current_out_name"] = out_name
        description = t(desc_key)
        context = dict(
            config=config,
            locale=locale,
            page_id=page_id,
            page_id_path=out_name,
            page_title=t(title_key),
            page_description=description,
            canonical_url=f"{site_url}/{slug}/{out_name}",
            jsonld_org=build_jsonld_org(config, description, site_url),
            nichos=data["nichos"],
            templates_catalog=data["templates_catalog"],
            planos_comparacao=data["planos_comparacao"],
            manutencao=data["manutencao"],
            depoimentos=data["depoimentos"],
            faq=data["faq"],
            checkout_pricing_json=json.dumps(checkout_pricing, ensure_ascii=False),
            payment_methods=payment_methods,
            is_brazil=(locale == "pt-BR"),
        )
        if extra_context:
            context.update(extra_context)
        template = env.get_template(tpl_name)
        html = template.render(**context)
        (locale_dir / out_name).write_text(html, encoding="utf-8")
        generated.append(out_name)

    sitemap_urls = "\n".join(f"  <url><loc>{site_url}/{slug}/{name}</loc></url>" for name in generated)
    (locale_dir / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>\n',
        encoding="utf-8",
    )
    (locale_dir / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", encoding="utf-8")

    print(f"[{locale}] {len(generated)} páginas geradas em {locale_dir}/")
    return generated


def main():
    config = engine.load_json(ROOT / "config" / "platform.config.json")
    data = {
        "nichos": engine.load_json(ROOT / "config" / "data" / "nichos.json")["nichos"],
        "templates_catalog": engine.load_json(ROOT / "config" / "data" / "templates_catalog.json")["templates"],
        "planos_comparacao": engine.load_json(ROOT / "config" / "data" / "planos_comparacao.json"),
        "manutencao": engine.load_json(ROOT / "config" / "data" / "manutencao.json")["planos"],
        "depoimentos": engine.load_json(ROOT / "config" / "data" / "depoimentos.json")["depoimentos"],
        "faq": engine.load_json(ROOT / "config" / "data" / "faq.json")["faq"],
        "moedas": engine.load_json(ROOT / "config" / "data" / "moedas.json"),
    }
    env = engine.make_env(ROOT / "templates")
    dist_dir = ROOT / "dist"

    for locale in LOCALES:
        render_locale(env=env, config=config, locale=locale, data=data, dist_dir=dist_dir)

    copy_demos(dist_dir)


if __name__ == "__main__":
    main()
