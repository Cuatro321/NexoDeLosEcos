// ================== Service Worker ==================
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/service-worker.js")
    .catch((err) => {
      console.warn("[SW] Registro falló", err);
    });
}

// ================== PWA Install (nav, hero, footer) ==================
let deferredPrompt = null;

const installBtnNav = document.getElementById("btn-install");          // menú
const installBtnHero = document.getElementById("btn-install-hero");    // botón en el hero (si existe)
const installBtnFooter = document.getElementById("btn-install-footer");// footer

function showInstallButtons() {
  [installBtnNav, installBtnHero, installBtnFooter].forEach((btn) => {
    if (btn) btn.classList.remove("hidden");
  });
}

function hideInstallButtons() {
  [installBtnNav, installBtnHero, installBtnFooter].forEach((btn) => {
    if (btn) btn.classList.add("hidden");
  });
}

// Mensaje detallado según dispositivo/navegador
function buildInstallHelpMessage() {
  const ua = navigator.userAgent.toLowerCase();
  const isAndroid = ua.includes("android");
  const isIOS = /iphone|ipad|ipod/.test(ua);
  const isEdge = ua.includes("edg/");
  const isChrome = ua.includes("chrome") && !ua.includes("edg");
  const isSafari = (!isChrome && !isEdge) && ua.includes("safari");

  // Android: Chrome / Edge
  if (isAndroid && (isChrome || isEdge)) {
    return (
      "Para instalar «El Nexo de los Ecos» en tu móvil Android:\n\n" +
      "1) Toca el botón de menú (⋮) en la esquina superior derecha del navegador.\n" +
      "2) Elige la opción «Añadir a la pantalla principal» o «Instalar aplicación».\n" +
      "3) Confirma tocando «Instalar».\n\n" +
      "La app aparecerá como un icono más en tu pantalla de inicio."
    );
  }

  // iPhone / iPad: Safari
  if (isIOS) {
    return (
      "Para instalar «El Nexo de los Ecos» en tu iPhone o iPad:\n\n" +
      "1) Toca el botón Compartir (cuadro con una flecha hacia arriba) en la barra inferior.\n" +
      "2) Desplázate y toca «Añadir a pantalla de inicio».\n" +
      "3) Opcional: cambia el nombre si quieres y luego toca «Añadir».\n\n" +
      "La app se abrirá a pantalla completa como si fuera una aplicación nativa."
    );
  }

  // PC / portátil: Chrome / Edge
  if (!isAndroid && (isChrome || isEdge)) {
    return (
      "Para instalar «El Nexo de los Ecos» en tu computadora:\n\n" +
      "1) Mira la parte derecha de la barra de direcciones.\n" +
      "   • Si ves un icono de monitor con flecha o un «+», haz clic en él.\n" +
      "2) Si no ves el icono, abre el menú (tres puntos verticales o «…» arriba a la derecha).\n" +
      "3) Busca y selecciona «Instalar aplicación» o «Instalar El Nexo de los Ecos».\n" +
      "4) Confirma en la ventana que se abre.\n\n" +
      "Tendrás un acceso directo a la app en tu escritorio o menú de aplicaciones."
    );
  }

  // Fallback genérico
  return (
    "Para instalar «El Nexo de los Ecos» en tu dispositivo:\n\n" +
    "1) Abre el menú principal de tu navegador (icono de tres puntos o «Compartir»).\n" +
    "2) Busca la opción «Instalar aplicación» o «Añadir a pantalla de inicio».\n" +
    "3) Confirma la instalación.\n\n" +
    "Después podrás abrir el Nexo desde el icono que se cree en tu dispositivo."
  );
}

window.addEventListener("beforeinstallprompt", (e) => {
  console.log("➡️ beforeinstallprompt disparado");
  e.preventDefault();
  deferredPrompt = e;
  showInstallButtons();
});

function triggerInstall(ev) {
  if (ev) ev.preventDefault();

  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice
      .catch(() => {})
      .finally(() => {
        deferredPrompt = null;
        hideInstallButtons();
      });
  } else {
    alert(buildInstallHelpMessage());
  }
}

[installBtnNav, installBtnHero, installBtnFooter].forEach((btn) => {
  if (btn) btn.addEventListener("click", triggerInstall);
});

// ================== Nav responsive + header scrolled ==================
document.getElementById("navToggle")?.addEventListener("click", () => {
  document.getElementById("navList")?.classList.toggle("open");
});
const header = document.getElementById("siteHeader");
const onScrollHeader = () => {
  const y = window.pageYOffset || 0;
  if (!header) return;
  if (y > 10) header.classList.add("scrolled");
  else header.classList.remove("scrolled");
};
window.addEventListener("scroll", onScrollHeader, { passive: true });
onScrollHeader();

// ================== Resaltar pestaña activa en el menú ==================
function setActiveNav() {
  const pathRaw = location.pathname || "/";
  const path = pathRaw === "/" ? "/" : pathRaw.replace(/\/+$/, "/");

  const links = document.querySelectorAll(".nav-list a.nav-link");
  let best = null;

  links.forEach((a) => {
    const hrefRaw = a.getAttribute("href") || "";
    if (!hrefRaw || hrefRaw.startsWith("http")) return;

    const route = hrefRaw === "/" ? "/" : hrefRaw.replace(/\/+$/, "/");

    if (route === "/" && path === "/") {
      best = a;
      return;
    }
    if (route !== "/" && path.startsWith(route)) {
      if (!best) best = a;
      else {
        const prevLen = (best.getAttribute("href") || "").length;
        if (route.length > prevLen) best = a;
      }
    }
  });

  links.forEach((a) => {
    a.classList.remove("is-active");
    a.removeAttribute("aria-current");
  });

  if (best) {
    best.classList.add("is-active");
    best.setAttribute("aria-current", "page");
  }
}
document.addEventListener("DOMContentLoaded", setActiveNav);
window.addEventListener("popstate", setActiveNav);
document.addEventListener("htmx:afterSettle", setActiveNav);

// ================== Barra de progreso + scroll-top + reveal ==================
document.addEventListener("DOMContentLoaded", () => {
  const scrollTopBtn = document.getElementById("scrollTop");
  const progress = document.querySelector(".progress-bar");

  const onScroll = () => {
    const y = window.pageYOffset || 0;
    if (scrollTopBtn) {
      if (y > 300) scrollTopBtn.classList.add("visible");
      else scrollTopBtn.classList.remove("visible");
    }
    if (progress) {
      const winH = window.innerHeight;
      const docH = document.documentElement.scrollHeight;
      const pct = Math.min(100, (y / (docH - winH)) * 100);
      progress.style.width = pct + "%";
    }
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  scrollTopBtn?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Reveal (fade-in)
  const fades = document.querySelectorAll(".fade-in");
  const ioReveal = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        ioReveal.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });
  fades.forEach((el) => ioReveal.observe(el));
});

// ================== LAZY: imágenes de fondo de cards + hero video ==================
(function lazyEverything(){
  // 1) Fondos de las concept-cards
  const cards = document.querySelectorAll(".concept-card.has-bg");
  const ioCards = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const card = entry.target;
      const bgUrl = card.getAttribute("data-bg");
      const bgDiv = card.querySelector(".card-bg");
      if (bgUrl && bgDiv && !bgDiv.dataset.loaded) {
        bgDiv.classList.add("lazy-blur");
        const img = new Image();
        img.onload = () => {
          bgDiv.style.backgroundImage = `url('${bgUrl}')`;
          bgDiv.dataset.loaded = "1";
          bgDiv.classList.remove("lazy-blur");
          card.classList.add("ready");
          card.classList.remove("is-loading");
          ioCards.unobserve(card);
        };
        img.onerror = () => { card.classList.remove("is-loading"); ioCards.unobserve(card); };
        img.src = bgUrl;
      }
    });
  }, { rootMargin: "200px 0px 200px 0px", threshold: 0.05 });
  cards.forEach((c) => ioCards.observe(c));

  // 2) Hero video (inyecta las fuentes al entrar en viewport)
  const heroVideo = document.querySelector(".hero-video");
  if (heroVideo) {
    const ioVideo = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const mp4  = heroVideo.getAttribute("data-src-mp4");
        const webm = heroVideo.getAttribute("data-src-webm");
        if (mp4 || webm) {
          if (webm) {
            const sWebm = document.createElement("source");
            sWebm.src = webm; sWebm.type = "video/webm";
            heroVideo.appendChild(sWebm);
          }
          if (mp4) {
            const sMp4 = document.createElement("source");
            sMp4.src = mp4; sMp4.type = "video/mp4";
            heroVideo.appendChild(sMp4);
          }
          heroVideo.load();
          if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            heroVideo.play().catch(()=>{});
          }
          heroVideo.removeAttribute("data-src-mp4");
          heroVideo.removeAttribute("data-src-webm");
        }
        ioVideo.unobserve(heroVideo);
      });
    }, { rootMargin: "200px 0px", threshold: 0.01 });
    ioVideo.observe(heroVideo);
  }

  // 3) <img data-src> genérico
  const imgs = document.querySelectorAll("img[data-src]");
  const ioImgs = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const img = en.target;
      img.src = img.dataset.src;
      img.onload = () => img.classList.add("lazy-loaded");
      img.removeAttribute("data-src");
      ioImgs.unobserve(img);
    });
  }, { rootMargin: "200px 0px", threshold: 0.01 });
  imgs.forEach((im) => ioImgs.observe(im));
})();

// ================== Performance extra ==================
if ("requestIdleCallback" in window) {
  requestIdleCallback(() => {
    document.querySelectorAll(".concept-card.has-bg:not(.ready)").forEach((card) => {
      const url = card.getAttribute("data-bg");
      if (!url) return;
      const link = document.createElement("link");
      link.rel = "prefetch"; link.as = "image"; link.href = url;
      document.head.appendChild(link);
    });
  }, { timeout: 2000 });
}

/* ===== Artefactos: lazy + blur-up + toggle GIF ===== */
(function(){
  const prefersReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(!entry.isIntersecting) return;
      const img = entry.target;
      const card = img.closest('.artifact-card');

      const webp = img.getAttribute('data-still-webp');
      const jpg  = img.getAttribute('data-still-fallback');
      const png  = img.getAttribute('data-still-fallback2');

      const applyLoaded = () => {
        img.classList.add('is-loaded');
        card?.classList.remove('is-loading');
        const sk = card?.querySelector('.artifact-skeleton');
        if(sk) sk.style.display = 'none';
      };

      const tryPng = () => {
        if(png){ img.src = png; img.onload = applyLoaded; img.onerror = null; }
      };
      const tryJpg = () => {
        if(jpg){ img.src = jpg; img.onload = applyLoaded; img.onerror = () => tryPng(); }
        else { tryPng(); }
      };
      const tryWebp = () => {
        if(webp){ img.src = webp; img.onload = applyLoaded; img.onerror = () => tryJpg(); }
        else { tryJpg(); }
      };

      tryWebp();
      io.unobserve(img);
    });
  }, { rootMargin: '300px 0px 300px 0px', threshold: 0.01 });

  document.querySelectorAll('.artifact-img.lazy-blur').forEach(img => io.observe(img));

  const enableGif = (mediaEl, play) => {
    const img = mediaEl.querySelector('.artifact-img');
    const badge = mediaEl.querySelector('.gif-toggle');
    if(!img) return;

    const gif = img.getAttribute('data-gif');
    if(!gif) return;

    if(play){
      img.src = gif + ((gif.indexOf('?')>-1 ? '&' : '?') + 't=' + Date.now());
      badge && badge.classList.add('is-playing');
    }else{
      const ev = new Event('revertStill');
      img.dispatchEvent(ev);
      badge && badge.classList.remove('is-playing');
    }
  };

  document.addEventListener('mouseover', (e)=>{
    const media = e.target.closest('.artifact-media');
    if(!media || prefersReduce) return;
    enableGif(media, true);
  });
  document.addEventListener('mouseout', (e)=>{
    const media = e.target.closest('.artifact-media');
    if(!media || prefersReduce) return;
    enableGif(media, false);
  });

  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('.gif-toggle');
    if(!btn) return;
    e.preventDefault();
    const media = btn.closest('.artifact-media');
    const playing = btn.classList.contains('is-playing');
    enableGif(media, !playing);
  });

  document.addEventListener('revertStill', (e)=>{
    const img = e.target;
    if(!img.classList.contains('artifact-img')) return;
    const webp = img.getAttribute('data-still-webp');
    const jpg  = img.getAttribute('data-still-fallback');
    const png  = img.getAttribute('data-still-fallback2');

    const applyLoaded = () => { img.classList.add('is-loaded'); };
    const tryPng = () => { if(png){ img.src = png; img.onload = applyLoaded; img.onerror = null; } };
    const tryJpg = () => { if(jpg){ img.src = jpg; img.onload = applyLoaded; img.onerror = () => tryPng(); } else { tryPng(); } };
    if(webp){ img.src = webp; img.onload = applyLoaded; img.onerror = () => tryJpg(); } else { tryJpg(); }
  }, true);
})();

// ===== Modal ligero (carga GET en #nx-modal-body) =====
(function(){
  const modal = document.getElementById('nx-modal');
  const body  = document.getElementById('nx-modal-body');
  if(!modal || !body) return;

  document.addEventListener('click', async (e) => {
    const a = e.target.closest('[data-modal]');
    const close = e.target.closest('[data-modal-close]');
    if (a) {
      e.preventDefault();
      try {
        const res = await fetch(a.getAttribute('href'), { headers: { 'X-Requested-With':'fetch' }});
        body.innerHTML = await res.text();
        modal.classList.remove('hidden');
      } catch { /* noop */ }
    }
    if (close) {
      modal.classList.add('hidden');
      body.innerHTML = '';
    }
  });

  document.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape') {
      modal.classList.add('hidden');
      body.innerHTML = '';
    }
  });
})();
