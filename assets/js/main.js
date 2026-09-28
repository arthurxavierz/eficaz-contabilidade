/* Escritório Eficaz · interações do site */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Cabeçalho ---------- */
  var header = $(".site-header");
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (!header) return;
    header.classList.toggle("is-solid", y > 40);
    if (!document.body.classList.contains("menu-open")) {
      header.classList.toggle("is-hidden", y > 400 && y > lastY + 4);
      if (y < lastY - 4) header.classList.remove("is-hidden");
    }
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Menu tela cheia ---------- */
  var toggle = $(".menu-toggle");
  var overlay = $(".overlay");
  function setMenu(open) {
    if (!overlay) return;
    overlay.setAttribute("data-open", open ? "true" : "false");
    overlay.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) overlay.removeAttribute("inert"); else overlay.setAttribute("inert", "");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.querySelector(".t").textContent = open ? "Fechar" : "Menu";
    document.body.classList.toggle("menu-open", open);
    if (open) header.classList.remove("is-hidden");
  }
  if (toggle) {
    toggle.addEventListener("click", function () { setMenu(overlay.getAttribute("data-open") !== "true"); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    $$(".overlay a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  }

  /* ---------- Revelação ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: .08 });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Hero: título letra a letra ---------- */
  var title = $(".hero-title");
  if (title && !reduce) {
    var idx = 0;
    $$(".line", title).forEach(function (line) {
      var walk = function (node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var frag = document.createDocumentFragment();
            n.textContent.split("").forEach(function (c) {
              if (c === " ") { frag.appendChild(document.createTextNode(" ")); return; }
              var sp = document.createElement("span");
              sp.className = "ch"; sp.textContent = c; sp.style.setProperty("--i", idx++);
              sp.setAttribute("aria-hidden", "true");
              frag.appendChild(sp);
            });
            n.parentNode.replaceChild(frag, n);
          } else if (n.nodeType === 1) walk(n);
        });
      };
      walk(line);
    });
    title.setAttribute("aria-label", "Contabilizando o sucesso");
  }

  /* ---------- Hero: gráfico de crescimento ---------- */
  var chartBox = $(".hero-chart");
  function drawChart() {
    var W = Math.max(280, Math.round(chartBox.clientWidth)), H = Math.max(170, Math.round(chartBox.clientHeight)), padB = 28, n = 12;
    var vals = [22, 30, 27, 38, 35, 46, 52, 49, 61, 68, 74, 86];
    var bw = W / n, gap = bw * .34;
    var xs = [], ys = [];
    var svg = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Gráfico ilustrativo de crescimento">' +
      '<defs><linearGradient id="heroArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2661b" stop-opacity=".28"/><stop offset="1" stop-color="#f2661b" stop-opacity="0"/></linearGradient></defs><g class="chart-grid">';
    for (var g = 0; g <= 4; g++) { var gy = (H - padB) * g / 4; svg += '<line x1="0" x2="' + W + '" y1="' + gy + '" y2="' + gy + '"/>'; }
    svg += "</g><g>";
    var MS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
    vals.forEach(function (v, k) {
      var h = (H - padB) * v / 100, x = k * bw + gap / 2, y = H - padB - h;
      xs.push(x + (bw - gap) / 2); ys.push(y);
      svg += '<rect class="chart-bar' + (k === n - 1 ? " hi" : "") + '" style="--i:' + k + '" x="' + x + '" y="' + y + '" width="' + (bw - gap) + '" height="' + h + '" rx="2"/>';
      svg += '<text class="chart-label" x="' + (x + (bw - gap) / 2) + '" y="' + (H - 8) + '" text-anchor="middle">' + MS[k] + "</text>";
    });
    svg += "</g>";
    var d = "M" + xs[0] + " " + (ys[0] - 14);
    for (var k2 = 1; k2 < n; k2++) {
      var cx = (xs[k2 - 1] + xs[k2]) / 2;
      d += " C" + cx + " " + (ys[k2 - 1] - 14) + " " + cx + " " + (ys[k2] - 14) + " " + xs[k2] + " " + (ys[k2] - 14);
    }
    var ex = xs[n - 1], ey = ys[n - 1] - 14;
    svg += '<path class="chart-area" d="' + d + " L" + ex + " " + (H - padB) + " L" + xs[0] + " " + (H - padB) + ' Z"/>';
    svg += '<path class="chart-line" pathLength="1000" style="--len:1000" d="' + d + '"/>';
    svg += '<circle class="chart-pulse" cx="' + ex + '" cy="' + ey + '" r="6"/><circle class="chart-dot" cx="' + ex + '" cy="' + ey + '" r="5"/>';
    svg += '<g class="chart-tag" transform="translate(' + (ex - 132) + " " + (ey - 44) + ')"><rect width="118" height="26" rx="13"/><text x="59" y="17" text-anchor="middle">RESULTADO</text></g>';
    svg += "</svg>";
    chartBox.innerHTML = svg;
    chartBox.setAttribute("data-w", W);
  }
  if (chartBox) {
    drawChart();
    var rt;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { if (Math.abs(chartBox.clientWidth - chartBox.getAttribute("data-w")) > 40) drawChart(); }, 250);
    });
  }

  /* ---------- Hero: brilho que acompanha o cursor ---------- */
  var heroEl = $(".hero");
  var glow = $(".hero-glow");
  if (heroEl && glow && !reduce && window.matchMedia("(hover: hover)").matches) {
    heroEl.addEventListener("pointermove", function (e) {
      var r = heroEl.getBoundingClientRect();
      glow.style.setProperty("--gx", ((e.clientX - r.left) / r.width * 100) + "%");
      glow.style.setProperty("--gy", ((e.clientY - r.top) / r.height * 100) + "%");
    });
  }

  /* ---------- Manifesto lido na rolagem ---------- */
  var mani = $(".manifesto [data-words]");
  if (mani) {
    var words = [];
    $$("[data-words]").forEach(function (p) {
      var out = [];
      p.childNodes.forEach(function (node) {
        var isHl = node.nodeType === 1 && node.tagName === "EM";
        var text = node.textContent;
        text.split(/(\s+)/).forEach(function (w) {
          if (!w.trim()) { out.push(w); return; }
          out.push('<span class="w' + (isHl ? " hl" : "") + '">' + w + "</span>");
        });
      });
      p.innerHTML = out.join("");
      words = words.concat($$(".w", p));
    });
    var section = mani.closest(".manifesto");
    var paint = function () {
      var r = section.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = (vh * .78 - r.top) / (r.height * .72);
      p = Math.max(0, Math.min(1, p));
      var n = Math.round(p * words.length);
      for (var k = 0; k < words.length; k++) words[k].classList.toggle("on", k < n);
    };
    if (reduce) words.forEach(function (w) { w.classList.add("on"); });
    else { window.addEventListener("scroll", paint, { passive: true }); window.addEventListener("resize", paint); paint(); }
  }

  /* ---------- Agenda de vencimentos ---------- */
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var MES_C = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
  var SEMANA = ["dom", "seg", "ter", "qua", "qui", "sex", "sáb"];
  var OBRIGACOES = [
    { dia: "util5", titulo: "Pagamento de salários", quem: "Até o quinto dia útil, para quem tem funcionários" },
    { dia: 15, titulo: "eSocial e DCTFWeb", quem: "Envio dos eventos da folha do mês anterior" },
    { dia: 20, titulo: "DAS do Simples Nacional", quem: "Empresas optantes e MEI" },
    { dia: 20, titulo: "FGTS Digital", quem: "Depósito mensal dos empregados" },
    { dia: 20, titulo: "INSS e IRRF sobre a folha", quem: "Guia única gerada pela DCTFWeb" },
    { dia: 25, titulo: "PIS e COFINS", quem: "Empresas do Lucro Presumido e do Lucro Real" },
    { dia: "ultimo", titulo: "IRPJ e CSLL", quem: "Estimativa mensal ou quota trimestral" }
  ];
  function dataDe(ano, mes, regra) {
    if (regra === "ultimo") {
      var d = new Date(ano, mes + 1, 0);
      while (d.getDay() === 0 || d.getDay() === 6) d.setDate(d.getDate() - 1);
      return d;
    }
    if (regra === "util5") {
      var n = 0, dd = new Date(ano, mes, 1);
      for (;;) { if (dd.getDay() !== 0) { n++; if (n === 5) return dd; } dd.setDate(dd.getDate() + 1); }
    }
    return new Date(ano, mes, regra);
  }
  function proximas(hoje) {
    var lista = [];
    OBRIGACOES.forEach(function (o) {
      var d = dataDe(hoje.getFullYear(), hoje.getMonth(), o.dia);
      if (d < hoje) d = dataDe(hoje.getFullYear(), hoje.getMonth() + 1, o.dia);
      lista.push({ o: o, d: d, faltam: Math.round((d - hoje) / 864e5) });
    });
    return lista.sort(function (a, b) { return a.d - b.d; });
  }
  var hoje = new Date(); hoje.setHours(0, 0, 0, 0);
  var prox = proximas(hoje);
  function faltamTxt(n) { return n === 0 ? "hoje" : n === 1 ? "amanhã" : "em " + n + " dias"; }

  var nd = $("#next-due");
  if (nd) {
    var f = prox[0];
    nd.innerHTML = '<span class="n">' + String(f.d.getDate()).padStart(2, "0") + "." + String(f.d.getMonth() + 1).padStart(2, "0") + "</span>" +
      '<span class="t"><small>Próximo vencimento, ' + faltamTxt(f.faltam) + "</small>" + f.o.titulo + "</span>";
  }

  var agenda = $("#agenda");
  if (agenda) {
    var first = prox[0];
    $("#agenda-count").innerHTML = (first.faltam === 0 ? "0" : first.faltam) +
      "<small>" + (first.faltam === 1 ? "dia" : "dias") + "<br>para o<br>próximo prazo</small>";
    $("#agenda-title").textContent = first.o.titulo;
    $("#agenda-sub").textContent = first.o.quem + ". Vence em " + first.d.getDate() + " de " + MESES[first.d.getMonth()] + ".";
    var ul = $("#due-list");
    ul.innerHTML = prox.map(function (it) {
      return '<li class="' + (it.faltam <= 5 ? "soon" : "") + '"><span class="d">' + String(it.d.getDate()).padStart(2, "0") +
        "<small>" + MES_C[it.d.getMonth()] + " · " + SEMANA[it.d.getDay()] + "</small></span>" +
        "<span><strong>" + it.o.titulo + '</strong><span class="who">' + it.o.quem + "</span></span>" +
        '<span class="left">' + faltamTxt(it.faltam) + "</span></li>";
    }).join("");
    var strip = $("#month-strip");
    if (strip) {
      var y = hoje.getFullYear(), m = hoje.getMonth();
      var dias = {};
      OBRIGACOES.forEach(function (o) { dias[dataDe(y, m, o.dia).getDate()] = true; });
      var h = SEMANA.map(function (s) { return '<span class="h">' + s.charAt(0).toUpperCase() + "</span>"; }).join("");
      var start = new Date(y, m, 1).getDay();
      for (var e = 0; e < start; e++) h += "<span></span>";
      var total = new Date(y, m + 1, 0).getDate();
      for (var dd = 1; dd <= total; dd++) {
        var wd = new Date(y, m, dd).getDay();
        var cls = "c" + (wd === 0 || wd === 6 ? " we" : "") + (dias[dd] ? " due" : "") + (dd === hoje.getDate() ? " today" : "") + (dd < hoje.getDate() ? " past" : "");
        h += '<span class="' + cls + '">' + dd + "</span>";
      }
      strip.innerHTML = h;
      var cap = $("#month-name"); if (cap) cap.textContent = MESES[m] + " de " + y;
    }
  }

  /* ---------- Seletor "qual é o seu momento" ---------- */
  var chips = $$(".chip");
  var out = $("#chooser-out");
  if (chips.length && out) {
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
        var alvos = c.getAttribute("data-target").split(",");
        out.innerHTML = "<span>" + c.getAttribute("data-say") + "</span>" + alvos.map(function (a) {
          var sec = document.getElementById(a);
          return sec ? '<a href="#' + a + '">' + sec.getAttribute("data-name") + "</a>" : "";
        }).join("");
      });
    });
  }

  /* ---------- Índice lateral de serviços ---------- */
  var navLinks = $$(".svc-nav a");
  if (navLinks.length && "IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          navLinks.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id); });
        }
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    $$(".svc-block").forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Linha do tempo ---------- */
  var tl = $$(".timeline li");
  if (tl.length && "IntersectionObserver" in window) {
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) en.target.classList.add("on"); });
    }, { rootMargin: "0px 0px -45% 0px" });
    tl.forEach(function (li) { tio.observe(li); });
  }

  /* ---------- Links úteis: busca e filtro ---------- */
  var search = $("#link-search");
  var cards = $$(".link-card");
  if (search && cards.length) {
    var cat = "todos";
    var empty = $("#links-empty");
    var norm = function (s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
    var apply = function () {
      var q = norm(search.value.trim());
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === "todos" || c.getAttribute("data-cat") === cat) && (!q || norm(c.textContent).indexOf(q) > -1);
        c.hidden = !ok; if (ok) shown++;
      });
      empty.classList.toggle("show", shown === 0);
    };
    search.addEventListener("input", apply);
    $$(".filter").forEach(function (b) {
      b.addEventListener("click", function () {
        cat = b.getAttribute("data-cat");
        $$(".filter").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        apply();
      });
    });
  }

  /* ---------- Contato ---------- */
  var form = $("#contact-form");
  if (form) {
    var unidadeSel = form.querySelector("[name=unidade]");
    var params = new URLSearchParams(location.search);
    if (params.get("assunto")) {
      var r = form.querySelector('input[name=assunto][value="' + params.get("assunto") + '"]');
      if (r) r.checked = true;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var fd = new FormData(form);
      var destino = fd.get("unidade") === "abadia" ? "solimar@escritorioeficaz.com.br" : "marcio@escritorioeficaz.com.br";
      var corpo = "Nome: " + fd.get("nome") + "\nTelefone: " + (fd.get("telefone") || "não informado") +
        "\nE-mail: " + fd.get("email") + "\nEmpresa: " + (fd.get("empresa") || "não informada") +
        "\nUnidade: " + (fd.get("unidade") === "abadia" ? "Abadia dos Dourados" : "Patrocínio") +
        "\nAssunto: " + (fd.get("assunto") || "Outro") + "\n\n" + fd.get("mensagem");
      var link = "mailto:" + destino + "?cc=ricardo@escritorioeficaz.com.br&subject=" +
        encodeURIComponent("Contato pelo site: " + (fd.get("assunto") || "mensagem")) + "&body=" + encodeURIComponent(corpo);
      window.location.href = link;
      $("#form-status").textContent = "Abrimos o seu aplicativo de e-mail com a mensagem pronta. É só enviar.";
    });
    if (unidadeSel) unidadeSel.addEventListener("change", function () {
      var t = $('.map-tabs [data-map="' + unidadeSel.value + '"]'); if (t) t.click();
    });
  }
  var mapTabs = $$(".map-tabs .filter");
  if (mapTabs.length) {
    var frame = $(".map-frame");
    var info = $("#map-addr");
    mapTabs.forEach(function (b) {
      b.addEventListener("click", function () {
        mapTabs.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        frame.src = b.getAttribute("data-src");
        if (info) info.textContent = b.getAttribute("data-addr");
      });
    });
  }

  /* ---------- Voltar ao topo ---------- */
  $$("[data-top]").forEach(function (b) { b.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); }); });

  /* ---------- Envio por WhatsApp ---------- */
  var waBtn = $("#send-wa");
  if (waBtn && form) {
    waBtn.addEventListener("click", function () {
      if (!form.reportValidity()) return;
      var fd = new FormData(form);
      var txt = "Olá! Sou " + fd.get("nome") + (fd.get("empresa") ? ", da " + fd.get("empresa") : "") + ".\n" +
        "Assunto: " + (fd.get("assunto") || "Outro") + "\n\n" + fd.get("mensagem");
      window.open(waBtn.getAttribute("data-wa").split("?")[0] + "?text=" + encodeURIComponent(txt), "_blank", "noopener");
    });
  }

  /* ---------- Ano no rodapé ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
