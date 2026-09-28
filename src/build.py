"""
Gera as páginas do site a partir de src/pages/*.html.

Cada página começa com um comentário de metadados:
<!--meta {"title": "...", "description": "...", "nav": "empresa", "theme": "dark"} -->

Marcadores disponíveis dentro das páginas:
  {{ARROW}}             seta dos botões
  {{ICON:nome}}         ícone (phone, mail, whatsapp, instagram, facebook, pin, clock, route, up)
  {{MAPS}}              os dois mapas com botões de rota
  {{CHANNELS}}          grade completa de canais de contato

Uso:  python src/build.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
SITE = "https://escritorioeficaz.com.br"

# ------------------------------------------------------------------
# Dados do escritório. Altere aqui e rode o build de novo.
# ------------------------------------------------------------------
EMPRESA = {
    "razao": "Escritório de Contabilidade Eficaz Ltda",
    "cnpj": "18.502.596/0001-93",
    "instagram": "https://www.instagram.com/escritorioeficaz/",
    "instagram_user": "@escritorioeficaz",
    "facebook": "https://www.facebook.com/EscritorioEficaz/",
    # CONFIRMAR: número de WhatsApp do escritório (somente dígitos, com 55 e DDD)
    "whatsapp": "553438399500",
    "whatsapp_label": "(34) 3839-9500",
    # CONFIRMAR: horário de atendimento
    "horario": "Segunda a sexta, em horário comercial",
}

UNIDADES = [
    {
        "slug": "patrocinio",
        "tipo": "Matriz",
        "nome": "Patrocínio",
        "rua": "Av. José Maria Alckmin, 860, Centro",
        "cidade": "Patrocínio, MG",
        "cep": "38740-068",
        "fones": [("(34) 3839-9500", "+553438399500")],
        "email": "marcio@escritorioeficaz.com.br",
        "q": "Av. José Maria Alckmin, 860, Centro, Patrocínio, MG, 38740-068",
    },
    {
        "slug": "abadia",
        "tipo": "Unidade",
        "nome": "Abadia dos Dourados",
        "rua": "Rua Tiradentes, 250, Centro",
        "cidade": "Abadia dos Dourados, MG",
        "cep": "38540-000",
        "fones": [("(34) 3847-1550", "+553438471550"), ("(34) 3847-1833", "+553438471833")],
        "email": "solimar@escritorioeficaz.com.br",
        "q": "Rua Tiradentes, 250, Centro, Abadia dos Dourados, MG, 38540-000",
    },
]

RESPONSAVEIS = ["marcio", "solimar", "ricardo"]

NAV = [
    ("index", "Início", "index.html"),
    ("empresa", "Empresa", "empresa.html"),
    ("servicos", "Serviços", "servicos.html"),
    ("caixa", "Caixa Aqui", "correspondente-caixa.html"),
    ("noticias", "Notícias", "noticias.html"),
    ("links", "Links úteis", "links-uteis.html"),
    ("contato", "Contato", "contato.html"),
]

_S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONS = {
    "arrow": f'<svg {_S.replace("1.6", "2")}><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "phone": f'<svg {_S}><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "mail": f'<svg {_S}><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "whatsapp": f'<svg {_S}><path d="M3.5 20.5 5 16a8.5 8.5 0 1 1 3.3 3.2z"/><path d="M9 8.5c0 3.5 2.5 6.5 6.5 6.5l1-1.6-2-1-1 .9c-1.2-.5-2.2-1.5-2.8-2.8l.9-1-1-2z"/></svg>',
    "instagram": f'<svg {_S}><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>',
    "facebook": f'<svg {_S}><path d="M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V10H6.5v3.5H9V21h3.5v-7.5H15l.5-3.5h-3V7a1 1 0 0 1 1-1H15z"/></svg>',
    "pin": f'<svg {_S}><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "clock": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "route": f'<svg {_S}><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H16a3 3 0 0 0 0-6H8a3 3 0 0 1 0-6h7.5"/></svg>',
    "up": f'<svg {_S.replace("1.6", "2")}><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
}
ARROW = ICONS["arrow"]

MARK = (
    '<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">'
    '<circle cx="20" cy="20" r="20" fill="#f2661b"/>'
    '<path d="M9.5 20h21" stroke="#fffdf8" stroke-width="4.2"/>'
    '<path d="M30.5 20a10.5 10.5 0 1 0-3.1 7.4" fill="none" stroke="#fffdf8" stroke-width="4.2"/>'
    "</svg>"
)
BRAND = f'{MARK}<span class="brand-text"><small>Escritório</small><strong>EF<i>I</i>CAZ</strong></span>'


def enc(s):
    from urllib.parse import quote_plus
    return quote_plus(s)


def map_embed(u):
    return f"https://maps.google.com/maps?q={enc(u['q'])}&amp;z=16&amp;output=embed"


def map_link(u):
    return f"https://www.google.com/maps/search/?api=1&amp;query={enc(u['q'])}"


def route_link(u):
    return f"https://www.google.com/maps/dir/?api=1&amp;destination={enc(u['q'])}"


def wa_link(msg="Olá! Vim pelo site do Escritório Eficaz."):
    return f"https://wa.me/{EMPRESA['whatsapp']}?text={enc(msg)}"


def fones_html(u, sep="<br>"):
    return sep.join(f'<a href="tel:{t}">{label}</a>' for label, t in u["fones"])


def maps_block():
    cards = []
    for u in UNIDADES:
        cards.append(f"""<figure class="map-card reveal">
        <div class="map-wrap"><iframe class="map-frame" title="Mapa da unidade {u['nome']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{map_embed(u)}"></iframe></div>
        <figcaption>
          <div>
            <span class="label accent">{u['tipo']}</span>
            <h3>{u['nome']}</h3>
            <p>{u['rua']}<br>{u['cidade']} · CEP {u['cep']}</p>
          </div>
          <div class="map-actions">
            <a class="btn btn-solid btn-sm" href="{route_link(u)}" target="_blank" rel="noopener">Traçar rota {ICONS['route']}</a>
            <a class="btn btn-ghost btn-sm" href="{map_link(u)}" target="_blank" rel="noopener">Abrir no Google Maps</a>
          </div>
        </figcaption>
      </figure>""")
    return '<div class="maps">\n      ' + "\n      ".join(cards) + "\n    </div>"


def channels_block():
    p, a = UNIDADES
    items = [
        ("phone", "Telefone Patrocínio", fones_html(p), "Matriz"),
        ("phone", "Telefones Abadia dos Dourados", fones_html(a), "Unidade"),
        ("whatsapp", "WhatsApp", f'<a href="{wa_link()}" target="_blank" rel="noopener">{EMPRESA["whatsapp_label"]}</a>', "Resposta em horário de atendimento"),
        ("mail", "E-mails", "<br>".join(f'<a href="mailto:{r}@escritorioeficaz.com.br">{r}@escritorioeficaz.com.br</a>' for r in RESPONSAVEIS), "Responsáveis"),
        ("instagram", "Instagram", f'<a href="{EMPRESA["instagram"]}" target="_blank" rel="noopener">{EMPRESA["instagram_user"]}</a>', "Dicas e avisos"),
        ("facebook", "Facebook", f'<a href="{EMPRESA["facebook"]}" target="_blank" rel="noopener">/EscritorioEficaz</a>', "Página oficial"),
        ("pin", "Presencial", f'{p["rua"]}, {p["cidade"]}<br>{a["rua"]}, {a["cidade"]}', "Duas unidades"),
        ("clock", "Horário", EMPRESA["horario"], "Atendimento"),
    ]
    cells = "\n      ".join(
        f'<div class="channel reveal"><span class="ch-ico">{ICONS[i]}</span><span class="label muted">{t}</span><p>{v}</p><small>{s}</small></div>'
        for i, t, v, s in items
    )
    return f'<div class="channels">\n      {cells}\n    </div>'


def cur(key, current):
    return ' aria-current="page"' if key == current else ""


def header(current, theme):
    links = "".join(
        f'<a class="nav-link" href="{href}"{cur(key, current)}>{label}</a>'
        for key, label, href in NAV[1:-1]
    )
    over = "".join(
        f'<li><a href="{href}"{cur(key, current)}>{label}</a></li>'
        for key, label, href in NAV
    )
    return f"""<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="progress-bar" aria-hidden="true"></div>
<header class="site-header" data-theme="{theme}">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Escritório Eficaz, página inicial">{BRAND}</a>
    <nav class="nav" aria-label="Principal">
      {links}
      <a class="btn btn-solid btn-sm" href="contato.html">Fale conosco {ARROW}</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu"><span class="t">Menu</span><span class="bars"></span></button>
    </nav>
  </div>
</header>
<div class="overlay" id="menu" data-open="false" aria-hidden="true" inert>
  <ol>{over}</ol>
  <div class="overlay-foot">
    <a href="tel:+553438399500">{ICONS['phone']} Patrocínio (34) 3839-9500</a>
    <a href="tel:+553438471550">{ICONS['phone']} Abadia (34) 3847-1550</a>
    <a href="{wa_link()}" target="_blank" rel="noopener">{ICONS['whatsapp']} WhatsApp</a>
    <a href="{EMPRESA['instagram']}" target="_blank" rel="noopener">{ICONS['instagram']} Instagram</a>
  </div>
</div>
"""


def footer():
    p, a = UNIDADES
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-cta">
        <p class="label muted">Vamos conversar</p>
        <p class="foot-lead">Tem uma dúvida sobre a sua empresa? Fale com quem entende do assunto.</p>
        <div class="foot-actions">
          <a class="btn btn-solid" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['whatsapp']} Chamar no WhatsApp</a>
          <a class="btn btn-ghost" href="contato.html">Outros canais {ARROW}</a>
        </div>
      </div>
      <div class="foot-social" aria-label="Redes sociais">
        <a href="{EMPRESA['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ICONS['instagram']}</a>
        <a href="{EMPRESA['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{ICONS['facebook']}</a>
        <a href="{wa_link()}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICONS['whatsapp']}</a>
        <a href="mailto:marcio@escritorioeficaz.com.br" aria-label="E-mail">{ICONS['mail']}</a>
      </div>
    </div>

    <div class="foot-grid">
      <div class="intro">
        <a class="brand" href="index.html" aria-label="Escritório Eficaz">{BRAND}</a>
        <p>Contabilidade e assessoria para empresas de Patrocínio, Abadia dos Dourados e de toda a região do Alto Paranaíba.</p>
        <p class="label muted" style="margin:24px 0 10px">Credenciais</p>
        <ul class="creds">
          <li>Correspondente Caixa Aqui</li>
          <li>Credenciado BDMG</li>
          <li>Credenciado Pluxee</li>
        </ul>
      </div>
      <div>
        <h4>Navegação</h4>
        <ul>
          <li><a href="index.html">Início</a></li>
          <li><a href="empresa.html">Empresa</a></li>
          <li><a href="servicos.html">Serviços</a></li>
          <li><a href="correspondente-caixa.html">Caixa Aqui</a></li>
          <li><a href="noticias.html">Notícias</a></li>
          <li><a href="links-uteis.html">Links úteis</a></li>
          <li><a href="contato.html">Contato</a></li>
        </ul>
      </div>
      <div>
        <h4>Serviços</h4>
        <ul>
          <li><a href="servicos.html#constituicao">Abertura de empresas</a></li>
          <li><a href="servicos.html#escrita-fiscal">Escrita fiscal</a></li>
          <li><a href="servicos.html#pessoal">Departamento pessoal</a></li>
          <li><a href="servicos.html#contabil">Contabilidade e perícia</a></li>
          <li><a href="servicos.html#tributario">Planejamento tributário</a></li>
          <li><a href="servicos.html#parcerias">Crédito e benefícios</a></li>
        </ul>
      </div>
      <div>
        <h4>{p['nome']}</h4>
        <ul>
          <li>{p['rua']}<br>CEP {p['cep']}</li>
          <li>{fones_html(p)}</li>
          <li><a href="mailto:{p['email']}">{p['email']}</a></li>
          <li><a class="foot-route" href="{route_link(p)}" target="_blank" rel="noopener">{ICONS['route']} Como chegar</a></li>
        </ul>
      </div>
      <div>
        <h4>{a['nome']}</h4>
        <ul>
          <li>{a['rua']}<br>CEP {a['cep']}</li>
          <li>{fones_html(a)}</li>
          <li><a href="mailto:{a['email']}">{a['email']}</a></li>
          <li><a class="foot-route" href="{route_link(a)}" target="_blank" rel="noopener">{ICONS['route']} Como chegar</a></li>
        </ul>
      </div>
      <div>
        <h4>Atendimento</h4>
        <ul>
          <li>{EMPRESA['horario']}</li>
          <li><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {EMPRESA['whatsapp_label']}</a></li>
          <li><a href="mailto:ricardo@escritorioeficaz.com.br">ricardo@escritorioeficaz.com.br</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot-word" aria-hidden="true">Ef<i>i</i>caz</div>
  <div class="wrap">
    <div class="foot-bottom">
      <span>&copy; <span data-year>2026</span> {EMPRESA['razao']} · CNPJ {EMPRESA['cnpj']}</span>
      <span class="foot-links"><a href="privacidade.html">Política de privacidade</a><a href="privacidade.html#termos">Termos de uso</a></span>
      <button class="to-top" type="button" data-top>Voltar ao topo {ICONS['up']}</button>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Conversar no WhatsApp">{ICONS['whatsapp']}<span>Fale no WhatsApp</span></a>
"""


def page(meta, body, name):
    title = meta["title"]
    full_title = f"{title} | Escritório Eficaz" if name != "index" else title
    url = f"{SITE}/" if name == "index" else f"{SITE}/{name}.html"
    extra = meta.get("head", "")
    p = UNIDADES[0]
    ld = {
        "@context": "https://schema.org",
        "@type": "AccountingService",
        "name": "Escritório Eficaz",
        "legalName": EMPRESA["razao"],
        "taxID": EMPRESA["cnpj"],
        "url": SITE,
        "telephone": "+55 34 3839-9500",
        "sameAs": [EMPRESA["instagram"], EMPRESA["facebook"]],
        "address": {"@type": "PostalAddress", "streetAddress": "Av. José Maria Alckmin, 860, Centro",
                    "addressLocality": "Patrocínio", "addressRegion": "MG", "postalCode": p["cep"], "addressCountry": "BR"},
    }
    return f"""<!doctype html>
<html lang="pt-BR" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{meta['description']}">
<meta name="theme-color" content="#0a1230">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{url}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Geist:wght@200..600&family=Geist+Mono:wght@300..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{extra}</head>
<body data-page="{name}">
{header(meta.get('nav', name), meta.get('theme', 'light'))}
<main id="conteudo">
{body.strip()}
</main>
{footer()}<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def render(body):
    body = body.replace("{{ARROW}}", ARROW)
    body = body.replace("{{MAPS}}", maps_block())
    body = body.replace("{{CHANNELS}}", channels_block())
    body = body.replace("{{WA}}", wa_link())
    body = re.sub(r"\{\{ICON:(\w+)\}\}", lambda m: ICONS[m.group(1)], body)
    return body


def main():
    for src in sorted(PAGES.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
        if not m:
            raise SystemExit(f"{src.name}: faltando bloco <!--meta-->")
        meta = json.loads(m.group(1))
        html = page(meta, render(raw[m.end():]), src.stem)
        for bad in ("—", "–"):
            if bad in html:
                raise SystemExit(f"{src.name}: contém travessão ({bad!r}); troque por outra pontuação")
        if "{{" in html:
            raise SystemExit(f"{src.name}: marcador não substituído")
        (ROOT / f"{src.stem}.html").write_text(html, encoding="utf-8")
        print("ok", src.stem + ".html")


if __name__ == "__main__":
    main()
