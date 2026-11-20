/* Eventually — la película avanza con el scroll.
   Sin dependencias. Tres reglas que no conviene tocar:
   - los fotogramas se guardan como <img>, no como ImageBitmap (memoria en móviles);
   - el scroll solo avisa: todo se lee y se dibuja dentro de requestAnimationFrame;
   - el fotograma mostrado persigue al objetivo con suavidad (lerp). */

(() => {
  'use strict';

  const root = document.documentElement;
  const stage = document.querySelector('[data-stage]');
  const canvas = document.querySelector('[data-canvas]');
  const loader = document.querySelector('[data-loader]');
  const loaderBar = document.querySelector('[data-loader-bar]');
  const draft = document.querySelector('[data-draft]');
  const sections = Array.from(document.querySelectorAll('[data-range]'));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const themeMeta = document.querySelector('meta[name="theme-color"]');
  let litTheme = themeMeta?.getAttribute('content') || '#ECEEF0';   // color de la barra del navegador con la luz encendida

  const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);

  /* ---------- la hora de verdad ---------- */

  function startClock() {
    const clock = document.querySelector('[data-clock]');
    const label = document.querySelector('[data-now]');
    if (!clock || !label) return;

    const now = new Date();
    const s = now.getSeconds() + now.getMilliseconds() / 1000;
    clock.style.setProperty('--s', (s * 6).toFixed(2)); // el barrido lo sigue el CSS

    const update = () => {
      const d = new Date();
      const h = d.getHours();
      const m = d.getMinutes();
      clock.style.setProperty('--m', ((m + d.getSeconds() / 60) * 6).toFixed(2));
      clock.style.setProperty('--h', (((h % 12) + m / 60) * 30).toFixed(2));
      if (reduced) clock.style.setProperty('--s', d.getSeconds() * 6); // sin barrido: salta cada 5 s
      const mm = String(m).padStart(2, '0');
      label.textContent = h === 1 ? `Es la 1:${mm}.` : `Son las ${h}:${mm}.`;
    };
    update();
    setInterval(update, 5000);
  }

  /* ---------- sin película: página normal ---------- */

  function staticPage() {
    root.dataset.motion = 'reduced';
    loader?.remove();
    sections.forEach((el) => {
      el.style.setProperty('--p', 0.5);
      el.style.setProperty('--in', 1);
    });
  }

  /* ---------- «Llevas 3 minutos aquí. Ya llegas tarde.» ---------- */

  function startLate() {
    const el = document.querySelector('[data-late]');
    if (!el) return;
    const t0 = Date.now();
    const update = () => {
      const m = Math.floor((Date.now() - t0) / 60000);
      el.textContent = m < 1
        ? 'Acabas de llegar. Tarde, seguro.'
        : `Llevas ${m} ${m === 1 ? 'minuto' : 'minutos'} aquí. Ya llegas tarde.`;
    };
    update();
    setInterval(update, 10000);
  }

  /* ---------- apagar la luz: solo brillan las agujas ---------- */

  function setupLights() {
    const btn = document.querySelector('[data-lights-toggle]');
    const section = document.querySelector('[data-now-section]');
    if (!btn) return;
    const set = (off) => {
      if (off) root.dataset.lights = 'off';
      else delete root.dataset.lights;
      btn.setAttribute('aria-pressed', String(off));
      btn.textContent = off ? 'Encender la luz' : 'Apagar la luz';
      themeMeta?.setAttribute('content', off ? '#090A0C' : litTheme);
    };
    btn.addEventListener('click', () => set(root.dataset.lights !== 'off'));
    // La luz vuelve sola al salir de esta parte: la película no está hecha para verse a oscuras.
    if (section) {
      window.addEventListener('scroll', () => {
        if (root.dataset.lights !== 'off') return;
        const rect = section.getBoundingClientRect();
        if (rect.bottom < 0 || rect.top > window.innerHeight) set(false);
      }, { passive: true });
    }
  }

  /* ---------- la nota se escribe renglón a renglón al llegar a ella ---------- */

  function setupNote() {
    const note = document.querySelector('[data-note]');
    if (!note || reduced || !('IntersectionObserver' in window)) return;
    note.querySelectorAll('.write__line').forEach((line, i) => line.style.setProperty('--i', i));
    note.classList.add('will-write');
    const io = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      note.classList.add('is-written');
      io.disconnect();
    }, { threshold: 0.35 });
    io.observe(note);
  }

  /* ---------- copia sin conexión ---------- */

  const canWorkOffline = 'serviceWorker' in navigator;
  if (canWorkOffline) {
    window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
  }

  startLate();

  // Primera visita: solo se enseña la caja (lo decide el script de la cabecera de
  // index.html). La película del reloj ni se descarga.
  if (root.dataset.mode === 'caja') {
    loader?.remove();
    return;
  }

  startClock();
  setupLights();
  setupNote();

  if (reduced) {
    staticPage();
    return;
  }

  fetch('frames/manifest.json', { cache: 'no-cache' })
    .then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.status))))
    .then(run)
    .catch(() => staticPage());

  /* ---------- la película ---------- */

  function run(manifest) {
    if (manifest.placeholder && draft) draft.hidden = false;

    const tiers = manifest.tiers.slice().sort((a, b) => b.minViewportWidth - a.minViewportWidth);
    const pickTier = () => tiers.find((t) => window.innerWidth >= t.minViewportWidth) || tiers[tiers.length - 1];
    let tier = pickTier();

    const frameCount = manifest.frameCount;
    const timeline = manifest.timeline || [[0, 0], [1, frameCount - 1]];
    const pad = (n) => String(n).padStart(4, '0');
    const version = manifest.version || 0;       // cambia al rehacer la película
    const frameUrl = (i) => `${tier.path}/${tier.pattern.replace('%04d', pad(i + 1))}?v=${version}`;

    let frames = new Array(frameCount).fill(null);
    let loadedCount = 0;
    let generation = 0;       // cambia si se recarga otro tamaño a mitad de carga
    let target = 0;
    let current = 0;
    let lastDrawn = -1;
    let running = false;

    const ctx = canvas.getContext('2d', { alpha: false });
    let cw = 0;
    let ch = 0;

    function sizeCanvas() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2); // a 3x cuesta 9 veces más y no se nota
      const rect = canvas.getBoundingClientRect();
      cw = rect.width;
      ch = rect.height;
      canvas.width = Math.round(cw * dpr);
      canvas.height = Math.round(ch * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      lastDrawn = -1;
    }

    function nearestLoaded(index) {
      if (frames[index]) return index;
      for (let d = 1; d < frameCount; d++) {
        if (index - d >= 0 && frames[index - d]) return index - d;
        if (index + d < frameCount && frames[index + d]) return index + d;
      }
      return -1;
    }

    function draw(index) {
      const i = nearestLoaded(index);
      if (i < 0 || i === lastDrawn) return;
      const img = frames[i];
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;
      const scale = Math.max(cw / iw, ch / ih);          // object-fit: cover, a mano
      const dw = iw * scale;
      const dh = ih * scale;
      ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
      lastDrawn = i;
    }

    /* El papel de la página toma el color del papel de la película, para que
       no se note dónde acaba una y empieza el otro. */
    function matchPaper(img) {
      try {
        const c = document.createElement('canvas');
        c.width = 24;
        c.height = 24;
        const x = c.getContext('2d', { willReadFrequently: true });
        x.drawImage(img, 0, 0, 24, 24);
        const px = x.getImageData(0, 0, 24, 24).data;
        let r = 0, g = 0, b = 0, n = 0;
        for (let y = 2; y < 22; y++) {
          for (const col of [0, 1, 22, 23]) {     // bordes izquierdo y derecho
            const k = (y * 24 + col) * 4;
            r += px[k]; g += px[k + 1]; b += px[k + 2]; n++;
          }
        }
        r = Math.round(r / n); g = Math.round(g / n); b = Math.round(b / n);
        const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b;
        if (luma > 205) {                          // solo si de verdad es papel claro
          const color = `rgb(${r} ${g} ${b})`;
          root.style.setProperty('--paper-film', color);
          litTheme = color;
          if (root.dataset.lights !== 'off') themeMeta?.setAttribute('content', color);
        }
      } catch (_) { /* si no se puede leer, se queda el color por defecto */ }
    }

    /* ---------- del scroll al fotograma ---------- */

    function progress() {
      const rect = stage.getBoundingClientRect();
      const total = rect.height - window.innerHeight;
      return total <= 0 ? 0 : clamp(-rect.top / total, 0, 1);
    }

    // La película no avanza a ritmo fijo: cada pieza llega en un tramo corto de
    // scroll y luego la imagen se queda quieta mientras se lee el texto.
    function frameAt(p) {
      for (let i = 1; i < timeline.length; i++) {
        if (p <= timeline[i][0]) {
          const [p0, f0] = timeline[i - 1];
          const [p1, f1] = timeline[i];
          let t = (p - p0) / Math.max(p1 - p0, 1e-6);
          t = t * t * (3 - 2 * t);                 // llega y se posa con suavidad
          return f0 + (f1 - f0) * t;
        }
      }
      return timeline[timeline.length - 1][1];
    }

    function applySections(p) {
      sections.forEach((el) => {
        const [a, b] = el.dataset.range.split(',').map(Number);
        const local = clamp((p - a) / Math.max(b - a, 0.0001), 0, 1);
        const inside = p >= a && p <= b;
        el.style.setProperty('--p', local.toFixed(4));
        el.style.setProperty('--in', inside ? 1 : 0);
        if (el.dataset.active !== String(inside)) {
          el.dataset.active = String(inside);
          el.style.pointerEvents = inside ? 'auto' : 'none'; // el texto invisible no debe comerse los toques
          // ni quedarse con el foco del teclado (el enlace de la portada, cuando ya no se ve)
          el.querySelectorAll('a, button').forEach((x) => { x.tabIndex = inside ? 0 : -1; });
        }
      });
    }

    function tick() {
      const p = progress();
      target = frameAt(p);
      current += (target - current) * 0.16;
      if (Math.abs(target - current) < 0.01) current = target;
      draw(Math.round(current));
      applySections(p);
      root.style.setProperty('--progress', p.toFixed(4));
      if (Math.abs(target - current) > 0.01) {
        requestAnimationFrame(tick);
      } else {
        running = false;
      }
    }

    function schedule() {
      if (!running) {
        running = true;
        requestAnimationFrame(tick);
      }
    }

    /* ---------- carga ---------- */

    function loadFrame(index, gen) {
      return new Promise((resolve) => {
        if (frames[index]) return resolve();
        const img = new Image();
        img.decoding = 'async';
        let settled = false;
        const done = () => {
          if (settled) return;
          settled = true;
          if (gen !== generation) return resolve();
          frames[index] = img;
          loadedCount++;
          loaderBar?.style.setProperty('--loaded', (loadedCount / frameCount).toFixed(3));
          resolve();
        };
        // Con la imagen descargada basta. Se intenta decodificar antes de dibujarla
        // (evita un tirón), pero sin esperar: el navegador puede aplazar ese paso.
        img.onload = () => {
          Promise.race([
            img.decode().catch(() => {}),
            new Promise((r) => setTimeout(r, 500)),
          ]).then(done);
        };
        img.onerror = () => resolve();
        img.src = frameUrl(index);
      });
    }

    async function runQueue(indices, concurrency, gen) {
      let cursor = 0;
      const workers = new Array(Math.min(concurrency, indices.length)).fill(0).map(async () => {
        while (cursor < indices.length && gen === generation) {
          const i = indices[cursor++];
          await loadFrame(i, gen);
          if (i === Math.round(current)) {
            lastDrawn = -1;
            schedule();
          }
        }
      });
      await Promise.all(workers);
    }

    async function boot() {
      const gen = ++generation;
      sizeCanvas();

      await loadFrame(0, gen);                     // una imagen cuanto antes
      if (gen !== generation) return;
      if (!frames[0]) {
        // Sin película (sin conexión y sin copia): página normal con la foto fija.
        generation++;
        staticPage();
        return;
      }
      matchPaper(frames[0]);
      draw(0);

      const head = Math.max(6, Math.round(frameCount * 0.12));
      await runQueue(Array.from({ length: head }, (_, i) => i), 6, gen);
      if (gen !== generation) return;

      root.dataset.sequence = 'ready';
      loader?.classList.add('is-done');
      setTimeout(() => loader?.remove(), 700);
      schedule();

      const rest = [];
      for (let i = head; i < frameCount; i++) rest.push(i);
      await runQueue(rest, 6, gen);
      if (gen !== generation || !canWorkOffline) return;
      // Con toda la película cargada, se le pasa al service worker para que la guarde.
      const urls = frames.map((_, i) => new URL(frameUrl(i), location.href).href);
      navigator.serviceWorker.ready
        .then((reg) => reg.active?.postMessage({ type: 'frames', version, urls }))
        .catch(() => {});
    }

    /* ---------- eventos ---------- */

    window.addEventListener('scroll', schedule, { passive: true });

    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        const next = pickTier();
        if (next !== tier) {                       // solo al cruzar de tamaño, no en cada píxel
          tier = next;
          frames = new Array(frameCount).fill(null);
          loadedCount = 0;
          boot();
          return;
        }
        sizeCanvas();
        schedule();
      }, 200);
    });

    boot();
  }
})();
