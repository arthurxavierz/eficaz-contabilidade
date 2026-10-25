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
    $$(".reveal, .img-reveal").forEach(function (el) { io.observe(el); });
  } else {
    $$(".reveal, .img-reveal").forEach(function (el) { el.classList.add("in"); });
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

  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var small = window.matchMedia("(max-width: 760px)");

  /* ---------- Títulos que sobem palavra a palavra ---------- */
  var splitEls = $$("[data-split], .sec-head h2.display");
  splitEls.forEach(function (el) {
    var w = 0;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
            var o = document.createElement("span"); o.className = "wd";
            var i = document.createElement("span"); i.textContent = part; i.style.setProperty("--w", w++);
            o.appendChild(i); frag.appendChild(o);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") walk(n);
      });
    };
    walk(el);
  });
  if (splitEls.length) {
    if (reduce || !("IntersectionObserver" in window)) splitEls.forEach(function (el) { el.classList.add("split-in"); });
    else {
      var sio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("split-in"); sio.unobserve(en.target); } });
      }, { rootMargin: "0px 0px -10% 0px" });
      splitEls.forEach(function (el) { sio.observe(el); });
    }
  }

  /* ---------- Contadores ---------- */
  var counters = $$("[data-count]");
  function runCount(el) {
    var to = parseFloat(el.getAttribute("data-count"));
    var dec = parseInt(el.getAttribute("data-dec") || "0", 10);
    var t0 = null, dur = 1800;
    var fmt = function (v) { return v.toLocaleString("pt-BR", { minimumFractionDigits: dec, maximumFractionDigits: dec }); };
    if (reduce) { el.textContent = fmt(to); return; }
    var step = function (ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur);
      el.textContent = fmt(to * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  if (counters.length && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); } });
    }, { threshold: .4 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- Vídeo do hero ---------- */
  var heroVid = $(".hero-media video");
  if (heroVid) {
    var pickSrc = function () { return small.matches ? heroVid.getAttribute("data-mobile") : heroVid.getAttribute("data-desktop"); };
    if (!reduce) {
      heroVid.src = pickSrc();
      heroVid.play().catch(function () {});
    }
  }

  /* ---------- Movimento ligado à rolagem ---------- */
  var heroEl = $(".hero");
  var parallax = $$("[data-parallax]");
  var stackCards = $$(".stack-card");
  var ticking = false;
  function onFrame() {
    ticking = false;
    var vh = window.innerHeight;
    if (heroEl && heroVid) {
      var y = Math.min(window.scrollY, vh);
      heroEl.style.setProperty("--hs", (1.06 + y / vh * .12).toFixed(4));
      heroEl.style.setProperty("--hy", (y * .25).toFixed(1) + "px");
    }
    parallax.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var c = (r.top + r.height / 2 - vh / 2) / vh;
      el.style.setProperty("--py", (c * -parseFloat(el.getAttribute("data-parallax") || "60")).toFixed(1) + "px");
    });
    for (var i = 0; i < stackCards.length - 1; i++) {
      var next = stackCards[i + 1].getBoundingClientRect();
      var cur = stackCards[i].getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (cur.bottom - next.top) / cur.height));
      stackCards[i].style.setProperty("--sc", (1 - p * .06).toFixed(4));
    }
  }
  function requestFrame() { if (!ticking) { ticking = true; requestAnimationFrame(onFrame); } }
  if (!reduce && (heroEl || parallax.length || stackCards.length)) {
    window.addEventListener("scroll", requestFrame, { passive: true });
    window.addEventListener("resize", requestFrame);
    onFrame();
  }

  /* ---------- Nota fiscal sendo conferida ---------- */
  var receipt = $(".receipt");
  if (receipt) {
    var DOCS = [
      { head: "NF-e 001.284", kind: "Nota fiscal de serviço", items: [["Honorários contábeis", 1850], ["Escrita fiscal", 640], ["Folha de pagamento", 920], ["ISS retido", -92.5]] },
      { head: "FOLHA 10/2026", kind: "Folha de pagamento", items: [["Salários", 18400], ["FGTS Digital", 1472], ["INSS patronal", 3680], ["Vale transporte", 610]] },
      { head: "DAS 10/2026", kind: "Simples Nacional", items: [["Receita do mês", 48200], ["Anexo III", 0], ["Alíquota efetiva", 0], ["Guia conferida", 2892]] }
    ];
    var kindEl = $(".receipt-kind", receipt), headEl = $(".receipt-head b", receipt), list = $(".r-lines", receipt);
    var totalEl = $(".r-total strong", receipt), bar = $(".r-bar", receipt), stamp = $(".stamp", receipt);
    var money = function (v) { return "R$ " + v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
    var di = 0, timers = [];
    var later = function (fn, ms) { timers.push(setTimeout(fn, ms)); };
    var cycle = function () {
      var d = DOCS[di++ % DOCS.length];
      stamp.classList.remove("on");
      headEl.textContent = d.head; kindEl.textContent = d.kind;
      list.innerHTML = d.items.map(function (it) {
        var val = it[1] === 0 ? (it[0] === "Anexo III" ? "serviços" : "6,00%") : money(it[1]);
        return "<li><i>" + it[0] + "</i><span>" + val + "</span></li>";
      }).join("");
      totalEl.textContent = money(0); bar.style.setProperty("--p", "0%");
      var total = d.items[d.items.length - 1][0] === "Guia conferida" ? d.items[3][1] : d.items.reduce(function (a, b) { return a + b[1]; }, 0);
      $$("li", list).forEach(function (li, k) {
        later(function () { li.classList.add("on"); bar.style.setProperty("--p", ((k + 1) / d.items.length * 100) + "%"); }, 500 + k * 520);
      });
      later(function () {
        var t0 = null;
        var tick = function (ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / 900);
          totalEl.textContent = money(total * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      }, 500 + d.items.length * 520);
      later(function () { stamp.classList.add("on"); }, 1700 + d.items.length * 520);
      later(cycle, 6200 + d.items.length * 520);
    };
    if (reduce) { cycle(); timers.forEach(clearTimeout); $$("li", list).forEach(function (li) { li.classList.add("on"); }); stamp.classList.add("on"); }
    else setTimeout(cycle, document.documentElement.classList.contains("intro") ? 2600 : 1500);
  }

  /* ---------- Vídeos verticais e modal ---------- */
  var modal = $("#vmodal");
  var mVideo = modal ? $("video", modal) : null;
  var lastFocus = null;
  function openVideo(src, title, link) {
    if (!modal) return;
    lastFocus = document.activeElement;
    mVideo.src = src;
    $(".vmodal-title", modal).textContent = title || "";
    if (link) $(".vmodal-link", modal).href = link;
    modal.setAttribute("aria-hidden", "false"); modal.removeAttribute("inert");
    document.body.classList.add("modal-open");
    mVideo.play().catch(function () {});
    $(".vmodal-close", modal).focus();
  }
  function closeVideo() {
    if (!modal || modal.getAttribute("aria-hidden") === "true") return;
    mVideo.pause(); mVideo.removeAttribute("src"); mVideo.load();
    modal.setAttribute("aria-hidden", "true"); modal.setAttribute("inert", "");
    document.body.classList.remove("modal-open");
    if (lastFocus) lastFocus.focus();
  }
  if (modal) {
    $(".vmodal-close", modal).addEventListener("click", closeVideo);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeVideo(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeVideo(); });
  }
  $$("[data-video]").forEach(function (b) {
    b.addEventListener("click", function () { openVideo(b.getAttribute("data-video"), b.getAttribute("data-title"), b.getAttribute("data-link")); });
  });
  var reels = $$(".reel");
  function startPrev(r) {
    var v = $("video", r);
    if (!v) return;
    if (!v.src) v.src = v.getAttribute("data-src");
    v.play().then(function () { r.classList.add("playing"); }).catch(function () {});
  }
  function stopPrev(r) { var v = $("video", r); if (v) { v.pause(); r.classList.remove("playing"); } }
  if (!reduce) {
    if (fine) reels.forEach(function (r) {
      r.addEventListener("mouseenter", function () { startPrev(r); });
      r.addEventListener("mouseleave", function () { stopPrev(r); });
    });
    else if ("IntersectionObserver" in window) {
      var rio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.intersectionRatio > .7) startPrev(en.target); else stopPrev(en.target); });
      }, { threshold: [0, .7] });
      reels.forEach(function (r) { rio.observe(r); });
    }
  }
  $$(".autoplay").forEach(function (v) {
    if (reduce) return;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { if (!v.src) v.src = v.getAttribute("data-src"); v.play().catch(function () {}); } else v.pause();
        });
      }).observe(v);
    }
  });

  /* ---------- Avaliações em faixa contínua ---------- */
  $$(".review-marquee .reviews").forEach(function (track) {
    Array.prototype.slice.call(track.children).forEach(function (c) {
      var k = c.cloneNode(true); k.setAttribute("aria-hidden", "true"); k.classList.add("in"); track.appendChild(k);
    });
    $$(".reveal", track).forEach(function (c) { c.classList.add("in"); });
  });

  /* ---------- Botões magnéticos ---------- */
  if (fine && !reduce) {
    $$(".magnetic").forEach(function (b) {
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty("--mx", ((e.clientX - r.left - r.width / 2) * .25).toFixed(1) + "px");
        b.style.setProperty("--my", ((e.clientY - r.top - r.height / 2) * .35).toFixed(1) + "px");
      });
      b.addEventListener("pointerleave", function () { b.style.setProperty("--mx", "0px"); b.style.setProperty("--my", "0px"); });
    });
  }

  /* ---------- Ano no rodapé ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
