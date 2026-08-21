#!/usr/bin/env python3
"""
factory_engine.py — Motor genérico da KE Sites Template Factory.

Compartilhado por TODOS os produtos (Salão de Beleza, CT de Vôlei, e futuros
nichos). Não contém nenhuma palavra, cor ou dado específico de nicho — tudo
isso vem do config/dados de cada produto. Esta é a peça "estrutura" da
separação estrutura / conteúdo / configuração / tema exigida pela KE Sites.

Cada produto tem seu próprio build.py, curto, que importa este módulo e passa:
  - NAV_ITEMS / FOOTER_LINKS (rótulos e rotas daquele nicho)
  - PAGES (quais templates viram quais arquivos, em qual nível mínimo)
  - TIER_LABELS
  - jsonld_type (tipo Schema.org apropriado ao nicho, ex: BeautySalon, SportsActivityLocation)
"""
import json
import shutil
import urllib.parse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

TIER_RANK = {"basico": 1, "intermediario": 2, "avancado": 3}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_data_dir(data_dir, files):
    """files: dict {nome_no_template: nome_do_arquivo_sem_extensao}"""
    return {key: load_json(Path(data_dir) / f"{fname}.json") for key, fname in files.items()}


def make_placeholder_fn(config):
    """Gera um <img> placeholder (SVG inline em data URI) com alt real,
    loading=lazy e decoding=async — pronto para ser trocado por fotos reais
    do cliente sem alterar HTML/CSS. Genérico: usa só as cores do tema."""
    primary_light = config["tema"]["corPrimariaClara"]
    secondary = config["tema"]["corSecundaria"]

    def ph(alt, ratio="4/3", monogram=None, w=480, h=360):
        label = (monogram or alt or "?").strip()[:2].upper()
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{primary_light}"/><stop offset="1" stop-color="{secondary}"/>
</linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/>
<circle cx="{w*0.82}" cy="{h*0.18}" r="{h*0.22}" fill="#ffffff" opacity="0.12"/>
<circle cx="{w*0.12}" cy="{h*0.88}" r="{h*0.30}" fill="#000000" opacity="0.08"/>
<text x="50%" y="53%" font-family="Georgia, 'Times New Roman', serif" font-size="{h*0.22}" fill="#fff" fill-opacity="0.92" text-anchor="middle" dominant-baseline="middle">{label}</text>
</svg>'''
        data_uri = "data:image/svg+xml," + urllib.parse.quote(svg.replace("\n", ""))
        alt_escaped = alt.replace('"', "&quot;")
        # Markup(): essencial — sem isso o autoescape do Jinja2 transforma o
        # <img> em texto literal escapado, quebrando o layout (bug real
        # encontrado e corrigido na v1 do Salão de Beleza).
        return Markup(
            f'<img src="{data_uri}" alt="{alt_escaped}" loading="lazy" decoding="async" '
            f'style="--ratio:{ratio}">'
        )

    return ph


def make_i18n_fn(dictionary):
    """Tradutor genérico por caminho de chave com pontos ("nav.inicio").
    Usado por qualquer produto/plataforma que precise de múltiplos idiomas
    a partir de uma única arquitetura (config/i18n/<locale>.json). Se a
    chave não existir, devolve a própria chave (facilita depurar textos
    esquecidos em vez de quebrar o build)."""

    def t(key, **kwargs):
        node = dictionary
        for part in key.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return key
        if isinstance(node, str) and kwargs:
            try:
                return node.format(**kwargs)
            except (KeyError, IndexError):
                return node
        return node

    return t


def make_money_fn(currency, thousands_sep="."):
    """Formata um valor em BRL (moeda-base dos dados) para a moeda ativa,
    usando a taxa demonstrativa do config/data/moedas.json do produto/
    plataforma. Sempre com aviso de que a cotação é ilustrativa — nunca
    usada como fonte real de câmbio. thousands_sep: "." (pt-BR/es-ES) ou
    "," (en-US) — separador de milhar apropriado ao locale."""
    simbolo = currency["simbolo"]
    taxa = currency["taxaDemoDeBRL"]

    def money(amount_brl):
        converted = round(amount_brl * taxa)
        formatted = f"{converted:,.0f}"  # sempre vem com vírgula do Python
        if thousands_sep != ",":
            formatted = formatted.replace(",", thousands_sep)
        return f"{simbolo} {formatted}"

    return money


def make_whatsapp_fn(config):
    base = f"https://wa.me/{config['identidade']['whatsapp']}"
    default_msg = config["identidade"]["whatsappMensagemPadrao"]

    def whatsapp_link(msg=None):
        text = msg or default_msg
        return f"{base}?text={urllib.parse.quote(text)}"

    return whatsapp_link


def build_jsonld(config, tier_rank, jsonld_type="LocalBusiness", member_org_suffix=None):
    """JSON-LD genérico — o @type vem de cada produto (BeautySalon,
    SportsActivityLocation, ...), o resto é sempre a mesma forma."""
    identidade = config["identidade"]
    ld = {
        "@context": "https://schema.org",
        "@type": jsonld_type,
        "name": identidade["nome"],
        "description": identidade["descricaoCurta"],
        "image": config["seo"]["ogImage"],
        "telephone": identidade["telefone"],
        "email": identidade["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": identidade["enderecoCompleto"],
            "addressLocality": identidade["cidade"],
            "addressRegion": identidade["estado"],
            "postalCode": identidade["cep"],
            "addressCountry": "BR",
        },
        "sameAs": [identidade["instagramLink"]],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "description": h["dias"], "opens": "", "closes": "", "name": h["horas"]}
            for h in identidade["horario"]
        ],
        "priceRange": "$$",
    }
    if tier_rank >= 3 and member_org_suffix:
        ld["memberOf"] = {"@type": "Organization", "name": f"{identidade['nomeCurto']} {member_org_suffix}"}
    return json.dumps(ld, ensure_ascii=False, indent=2)


def make_env(templates_dir):
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_tier(*, env, config, data, tier, tier_dir, templates_dir, assets_dir,
                 nav_items, footer_links, pages, tier_labels, jsonld_type,
                 member_org_suffix=None, canonical_base="https://seusite.exemplo"):
    """Gera um nível (basico/intermediario/avancado) completo em tier_dir.

    pages: lista de tuplas (template_relpath, output_filename, page_id, min_tier, title, description_template_or_None)
    """
    tier_rank = TIER_RANK[tier]
    if tier_dir.exists():
        shutil.rmtree(tier_dir)
    tier_dir.mkdir(parents=True)

    shutil.copytree(assets_dir, tier_dir / "assets", dirs_exist_ok=True)
    theme_tpl = env.get_template("theme.css.j2")
    (tier_dir / "assets" / "css" / "theme.css").write_text(
        theme_tpl.render(tema=config["tema"]), encoding="utf-8"
    )

    ph = make_placeholder_fn(config)
    whatsapp_link = make_whatsapp_fn(config)
    env.globals["ph"] = ph
    env.globals["whatsapp_link"] = whatsapp_link

    generated = []
    for tpl_name, out_name, page_id, min_tier, title, desc_tpl in pages:
        if min_tier > tier_rank:
            continue

        booking_file = config.get("_bookingPageFilename", "agendamento.html")
        primary_cta_href = booking_file if tier_rank >= 2 else "#"
        primary_cta_attrs = "" if tier_rank >= 2 else 'data-modal-open="modal-agendar"'

        description = (desc_tpl or config["seo"]["descricaoPadrao"])
        if desc_tpl:
            description = desc_tpl.format(nome=config["identidade"]["nome"])
        seo_desc_default = (
            config["seo"].get("descricaoPadraoAvancado", config["seo"]["descricaoPadrao"])
            if tier_rank >= 3 else config["seo"]["descricaoPadrao"]
        )
        if not desc_tpl:
            description = seo_desc_default
        seo_keywords = (
            config["seo"].get("palavrasChaveAvancado", config["seo"]["palavrasChave"])
            if tier_rank >= 3 else config["seo"]["palavrasChave"]
        )

        context = dict(
            config=config,
            tier=tier,
            tier_rank=tier_rank,
            tier_label=tier_labels[tier],
            page_id=page_id,
            page_title=title,
            page_description=description,
            page_keywords=seo_keywords,
            canonical_url=f"{canonical_base}/{tier}/{out_name}",
            nav_items=nav_items,
            footer_links=footer_links,
            primary_cta_href=primary_cta_href,
            primary_cta_attrs=primary_cta_attrs,
            jsonld_localbusiness=build_jsonld(config, tier_rank, jsonld_type, member_org_suffix),
            jsonld_extra=None,
            **data,
        )

        template = env.get_template(tpl_name)
        html = template.render(**context)
        (tier_dir / out_name).write_text(html, encoding="utf-8")
        generated.append(out_name)

    sitemap_urls = "\n".join(f"  <url><loc>{canonical_base}/{name}</loc></url>" for name in generated)
    (tier_dir / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>\n',
        encoding="utf-8",
    )
    (tier_dir / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", encoding="utf-8")

    print(f"[{tier}] {len(generated)} páginas geradas em {tier_dir}/")
    return generated


def build_product(*, root, config_path, data_dir, data_files, templates_dir, assets_dir,
                   dist_dir, nav_items, footer_links, pages, tier_labels, jsonld_type,
                   member_org_suffix=None, canonical_base="https://seusite.exemplo", tiers=None):
    """Ponto de entrada único usado por todo build.py de produto."""
    config = load_json(config_path)
    data = load_data_dir(data_dir, data_files)
    env = make_env(templates_dir)

    tiers = tiers or list(TIER_RANK.keys())
    for tier in tiers:
        render_tier(
            env=env, config=config, data=data, tier=tier, tier_dir=dist_dir / tier,
            templates_dir=templates_dir, assets_dir=assets_dir,
            nav_items=nav_items, footer_links=footer_links, pages=pages,
            tier_labels=tier_labels, jsonld_type=jsonld_type,
            member_org_suffix=member_org_suffix, canonical_base=canonical_base,
        )
