"""
Gera as páginas do site a partir de src/pages/*.html.

Cada página começa com um comentário de metadados:
<!--meta {"title": "...", "description": "...", "nav": "sobre", "theme": "dark"} -->

Marcadores disponíveis dentro das páginas:
  {{ARROW}}             seta dos botões
  {{ICON:nome}}         ícone (phone, mail, whatsapp, instagram, facebook, pin, clock, route, up, play, star, google)
  {{MAPS}}              os dois mapas com botões de rota
  {{CHANNELS}}          grade completa de canais de contato
  {{REELS}}             vídeos do Instagram em formato vertical
  {{IGFEED}}            grade de posts do Instagram
  {{REVIEWS}}           avaliações do Google em cartões
  {{QUOTES}}            trechos destacados das avaliações
  {{STARS}}             cinco estrelas
  {{WA}}                link do WhatsApp com mensagem pronta
  {{GOOGLE}}            link da ficha do escritório no Google

Uso:  python src/build.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
SITE = "https://escritorioeficaz.com.br"
V = "3"  # versão dos arquivos estáticos; aumente a cada publicação de CSS ou JS

# ------------------------------------------------------------------
# Dados do escritório. Altere aqui e rode o build de novo.
# ------------------------------------------------------------------
EMPRESA = {
    "razao": "Escritório de Contabilidade Eficaz Ltda",
    "cnpj": "18.502.596/0001-93",
    "fundacao": 1996,
    "instagram": "https://www.instagram.com/escritorioeficaz/",
    "instagram_user": "@escritorioeficaz",
    "facebook": "https://www.facebook.com/EscritorioEficaz/",
    "whatsapp": "553438399500",
    "whatsapp_label": "(34) 3839-9500",
    "horario": "Segunda a quinta, 7h30 às 17h30<br>Sexta, 7h30 às 17h",
    "google": "https://www.google.com/maps/place/Escrit%C3%B3rio+de+Contabilidade+Eficaz/@-18.9405656,-46.9908627,17z/data=!4m6!3m5!1s0x94ae52b59cbed981:0x45373380555af89d!8m2!3d-18.9405656!4d-46.9908627!16s%2Fg%2F1pv17jwxx",
    "nota": "5,0",
    "avaliacoes": 32,
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

# Vídeos publicados no Instagram do escritório (assets/video/reel-N.mp4)
REELS = [
    {"n": 1, "tag": "30 anos", "titulo": "Três décadas de confiança", "texto": "Excelência, lealdade e dedicação a cada cliente desde 1996.", "url": "https://www.instagram.com/escritorioeficaz/reel/DaDzhOZxLgu/"},
    {"n": 2, "tag": "Bastidores", "titulo": "Entre reuniões, cafés e números", "texto": "Uma equipe unida em que cada detalhe importa.", "url": "https://www.instagram.com/escritorioeficaz/reel/DRNBpSAkRh9/"},
    {"n": 3, "tag": "Quem somos", "titulo": "Uma equipe que cuida de tudo", "texto": "Contabilidade, folha, consultoria e regularização em um só lugar.", "url": "https://www.instagram.com/escritorioeficaz/reel/DVrcRqjj6HX/"},
    {"n": 4, "tag": "Dica", "titulo": "Conta pessoal não é conta da empresa", "texto": "Separar as contas é o primeiro passo para ter controle de verdade.", "url": "https://www.instagram.com/escritorioeficaz/reel/Dd7I-wdP2mv/"},
]

# Posts recentes do Instagram (assets/img/ig/*.jpg)
IG_POSTS = [
    ("escala-6x1", "Fim da escala 6x1: o que muda na sua empresa", "https://www.instagram.com/escritorioeficaz/p/DexATG5h2jA/"),
    ("custo-funcionario", "Salário de R$ 2.000 não significa custo de R$ 2.000", "https://www.instagram.com/escritorioeficaz/p/De0DeSrPGl-/"),
    ("profissional-liberal", "Profissional liberal ainda recebendo como pessoa física?", "https://www.instagram.com/escritorioeficaz/p/DekL8Z-B97a/"),
    ("creditos-ibs-cbs", "Créditos de IBS e CBS na Reforma Tributária", "https://www.instagram.com/escritorioeficaz/p/Debn4mGER1g/"),
    ("pro-labore", "O caixa da empresa não é o seu salário", "https://www.instagram.com/escritorioeficaz/p/DePgGtlx0GB/"),
    ("extrato", "Aquele lançamento estranho no extrato da empresa", "https://www.instagram.com/escritorioeficaz/p/DeCNS2AxpaU/"),
]

# Avaliações públicas na ficha do Google
REVIEWS = [
    {"nome": "Ricardo Siqueira Jr", "quando": "Avaliação no Google", "texto": "Excelente escritório de contabilidade! Profissionais altamente qualificados, sempre disponíveis para esclarecer dúvidas e oferecer soluções práticas. O atendimento é ágil, transparente e personalizado, transmitindo total confiança. Os relatórios e análises são precisos, o que facilita muito a tomada de decisões estratégicas."},
    {"nome": "Liamar Campos", "quando": "Avaliação no Google", "texto": "Atendimento de alta qualidade, equipe extremamente preparada, atualizada e comprometida com a melhor solução para cada situação. Sempre muito atenciosos, ágeis e transparentes em todas as etapas. Profissionais competentes que transmitem segurança e confiança."},
    {"nome": "Fernanda Rosa", "quando": "Avaliação no Google", "texto": "Parabenizo toda a equipe pelo excelente atendimento, profissionalismo, competência e dedicação. É um prazer contar com um serviço de tanta qualidade e confiança."},
]
QUOTES = [
    "Excelentes profissionais, bom atendimento, agilidade no serviço prestado.",
    "Equipe muito bem preparada, educação e qualidade no atendimento!",
    "Estabelecimento e atendimento nota mil!",
]

# (chave, rótulo, arquivo, aparece no menu do topo)
NAV = [
    ("index", "Início", "index.html", False),
    ("sobre", "Sobre", "sobre.html", True),
    ("servicos", "Serviços", "servicos.html", True),
    ("depoimentos", "Depoimentos", "depoimentos.html", True),
    ("caixa", "Caixa Aqui", "correspondente-caixa.html", True),
    ("links", "Links úteis", "links-uteis.html", True),
    ("contato", "Contato", "contato.html", False),
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
    "play": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2.8 2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4-4.7-4.4 6.4-.8z" fill="currentColor"/></svg>',
    "google": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z"/><path fill="#34A853" d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z"/><path fill="#FBBC05" d="M6.4 14c-.2-.6-.3-1.3-.3-2s.1-1.4.3-2V7.4H3.1a10 10 0 0 0 0 9.2z"/><path fill="#EA4335" d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.4L6.4 10C7.2 7.7 9.4 6 12 6z"/></svg>',
    "camera": f'<svg {_S}><path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/></svg>',
    "close": f'<svg {_S.replace("1.6", "2")}><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "sound": f'<svg {_S}><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/></svg>',
}
ARROW = ICONS["arrow"]

# Marca: círculo com o "e" atravessado, como no logo do escritório
MARK = (
    '<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true">'
    '<circle class="m-bg" cx="24" cy="24" r="24"/>'
    '<path class="m-e" pathLength="100" d="M37.2 30.2A14.2 14.2 0 1 1 38.4 24" fill="none" stroke-width="5.4"/>'
    '<rect class="m-bar" x="0" y="21.3" width="38.6" height="5.4"/>'
    "</svg>"
)
# Logo completo em um único SVG, com posições fixas para o alinhamento não depender da fonte
BRAND = (
    '<svg class="brand-logo" viewBox="0 0 192 56" aria-hidden="true">'
    '<g transform="translate(0 4)">'
    '<circle class="m-bg" cx="24" cy="24" r="24"/>'
    '<path class="m-e" d="M37.2 30.2A14.2 14.2 0 1 1 38.4 24" fill="none" stroke-width="5.4"/>'
    '<rect class="m-bar" x="0" y="21.3" width="38.6" height="5.4"/>'
    "</g>"
    '<text class="lg-top" x="184" y="15" text-anchor="end">Escritório</text>'
    '<text class="lg-word" x="54" y="41" textLength="126" lengthAdjust="spacingAndGlyphs">EF<tspan class="lg-i">I</tspan>CAZ</text>'
    '<text class="lg-sub" x="180" y="53" text-anchor="end">Contabilidade / Assessoria</text>'
    "</svg>"
)


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


def stars():
    return '<span class="stars" aria-label="5 de 5 estrelas">' + ICONS["star"] * 5 + "</span>"


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
        ("clock", "Horário", EMPRESA["horario"], "Sábado e domingo fechado"),
    ]
    cells = "\n      ".join(
        f'<div class="channel reveal"><span class="ch-ico">{ICONS[i]}</span><span class="label muted">{t}</span><p>{v}</p><small>{s}</small></div>'
        for i, t, v, s in items
    )
    return f'<div class="channels">\n      {cells}\n    </div>'


def reels_block():
    cards = []
    for k, r in enumerate(REELS):
        n = r["n"]
        cards.append(f"""<button class="reel reveal reveal-d{k}" type="button" data-video="assets/video/reel-{n}.mp4" data-title="{r['titulo']}" data-link="{r['url']}">
        <span class="reel-media">
          <img src="assets/video/reel-{n}.jpg" alt="" loading="lazy" width="540" height="960">
          <video muted loop playsinline preload="none" data-src="assets/video/reel-{n}-prev.mp4"></video>
        </span>
        <span class="reel-play">{ICONS['play']}</span>
        <span class="reel-cap">
          <span class="label">{r['tag']}</span>
          <strong>{r['titulo']}</strong>
          <small>{r['texto']}</small>
        </span>
      </button>""")
    return '<div class="reels">\n      ' + "\n      ".join(cards) + "\n    </div>"


def igfeed_block():
    cells = []
    for k, (img, alt, url) in enumerate(IG_POSTS):
        cells.append(f"""<a class="ig-post reveal reveal-d{k % 3}" href="{url}" target="_blank" rel="noopener">
        <img src="assets/img/ig/{img}.jpg" alt="{alt}" loading="lazy" width="640" height="800">
        <span class="ig-over"><span>{ICONS['instagram']}</span><strong>{alt}</strong></span>
      </a>""")
    return '<div class="ig-grid">\n      ' + "\n      ".join(cells) + "\n    </div>"


def reviews_block():
    cards = []
    for k, r in enumerate(REVIEWS):
        ini = "".join(w[0] for w in r["nome"].split()[:2]).upper()
        cards.append(f"""<figure class="review reveal reveal-d{k}">
        <div class="review-top">{stars()}<span class="g-ico">{ICONS['google']}</span></div>
        <blockquote>{r['texto']}</blockquote>
        <figcaption><span class="avatar" aria-hidden="true">{ini}</span><span><strong>{r['nome']}</strong><small>{r['quando']}</small></span></figcaption>
      </figure>""")
    return '<div class="reviews">\n      ' + "\n      ".join(cards) + "\n    </div>"


def quotes_block():
    return '<ul class="quotes">' + "".join(
        f'<li class="reveal reveal-d{k}"><span class="q" aria-hidden="true">&ldquo;</span>{q}<small>Trecho de avaliação no Google</small></li>'
        for k, q in enumerate(QUOTES)
    ) + "</ul>"


def cur(key, current):
    return ' aria-current="page"' if key == current else ""


def header(current, theme):
    links = "".join(
        f'<a class="nav-link" href="{href}"{cur(key, current)}>{label}</a>'
        for key, label, href, top in NAV if top
    )
    over = "".join(
        f'<li><a href="{href}"{cur(key, current)}>{label}</a></li>'
        for key, label, href, _ in NAV
    )
    return f"""<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="progress-bar" aria-hidden="true"></div>
<div class="curtain" aria-hidden="true"><span class="curtain-mark">{MARK}</span></div>
<header class="site-header" data-theme="{theme}">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Escritório Eficaz, página inicial">{BRAND}</a>
    <nav class="nav" aria-label="Principal">
      {links}
      <a class="btn btn-solid btn-sm magnetic" href="contato.html">Fale conosco {ARROW}</a>
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
        <p class="foot-lead">Tem uma dúvida sobre a sua empresa? Fale com quem cuida de números há 30 anos.</p>
        <div class="foot-actions">
          <a class="btn btn-solid magnetic" href="{wa_link()}" target="_blank" rel="noopener">{ICONS['whatsapp']} Chamar no WhatsApp</a>
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
        <p>Há 30 anos transformando números em resultados para empresas de Patrocínio, Abadia dos Dourados e de toda a região do Alto Paranaíba.</p>
        <a class="foot-rating" href="{EMPRESA['google']}" target="_blank" rel="noopener">{ICONS['google']}<span><strong>{EMPRESA['nota']}</strong> {stars()}</span><small>{EMPRESA['avaliacoes']} avaliações no Google</small></a>
      </div>
      <div>
        <h4>Navegação</h4>
        <ul>
          {"".join(f'<li><a href="{href}">{label}</a></li>' for _, label, href, _t in NAV)}
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
          <li class="creds-title">Credenciais</li>
          <li class="cred">Correspondente Caixa Aqui</li>
          <li class="cred">Credenciado BDMG</li>
          <li class="cred">Credenciado Pluxee</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot-word" aria-hidden="true">Ef<i>i</i>caz</div>
  <div class="wrap">
    <div class="foot-bottom">
      <span>&copy; <span data-year>2026</span> {EMPRESA['razao']} · CNPJ {EMPRESA['cnpj']}</span>
      <span class="foot-links"><a href="privacidade.html">Política de privacidade</a><a href="privacidade.html#termos">Termos de uso</a></span>
      <a class="dev-by" href="https://achillesmedia.com.br" target="_blank" rel="noopener">Desenvolvido por <strong>Achilles</strong></a>
      <button class="to-top" type="button" data-top>Voltar ao topo {ICONS['up']}</button>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Conversar no WhatsApp">{ICONS['whatsapp']}<span>Fale no WhatsApp</span></a>
<div class="vmodal" id="vmodal" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Vídeo" inert>
  <div class="vmodal-box">
    <video controls playsinline preload="none"></video>
    <div class="vmodal-bar">
      <strong class="vmodal-title"></strong>
      <a class="vmodal-link" href="{EMPRESA['instagram']}" target="_blank" rel="noopener">{ICONS['instagram']} Ver no Instagram</a>
    </div>
  </div>
  <button class="vmodal-close" type="button" aria-label="Fechar vídeo">{ICONS['close']}</button>
</div>
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
        "foundingDate": str(EMPRESA["fundacao"]),
        "url": SITE,
        "telephone": "+55 34 3839-9500",
        "sameAs": [EMPRESA["instagram"], EMPRESA["facebook"]],
        "openingHours": ["Mo-Th 07:30-17:30", "Fr 07:30-17:00"],
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
<meta property="og:image" content="{SITE}/assets/video/hero.jpg">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:ital,wght@1,900&family=Geist:wght@200..600&family=Geist+Mono:wght@300..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={V}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{extra}</head>
<body data-page="{name}">
{header(meta.get('nav', name), meta.get('theme', 'light'))}
<main id="conteudo">
{body.strip()}
</main>
{footer()}<script src="assets/js/main.js?v={V}" defer></script>
</body>
</html>
"""


def render(body):
    body = body.replace("{{ARROW}}", ARROW)
    body = body.replace("{{MAPS}}", maps_block())
    body = body.replace("{{CHANNELS}}", channels_block())
    body = body.replace("{{REELS}}", reels_block())
    body = body.replace("{{IGFEED}}", igfeed_block())
    body = body.replace("{{REVIEWS}}", reviews_block())
    body = body.replace("{{QUOTES}}", quotes_block())
    body = body.replace("{{STARS}}", stars())
    body = body.replace("{{WA}}", wa_link())
    body = body.replace("{{GOOGLE}}", EMPRESA["google"])
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
