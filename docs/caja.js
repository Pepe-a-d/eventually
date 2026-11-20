/* Eventually — la caja: cómo se abre. Segunda película, también movida por el scroll.
   Sigue las tres reglas de app.js (fotogramas como <img>, todo dentro de
   requestAnimationFrame, el fotograma persigue al objetivo) y no toca nada suyo:
   usa sus propios atributos (data-caja…) y sus propias variables.
   Diferencias con la película del reloj:
   - los fotogramas tienen fondo transparente, así que el papel es siempre el de la página;
   - no se cargan hasta que la sección se acerca a la pantalla. */

(() => {
  'use strict';

  const wrap = document.querySelector('[data-caja]');
  if (!wrap) return;
  const stage = wrap.querySelector('.stage');
  const canvas = wrap.querySelector('[data-caja-canvas]');
  const sections = Array.from(wrap.querySelectorAll('[data-caja-range]'));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);

  /* Sin película: los textos quedan uno debajo de otro, con una foto fija. */
  function staticBlock() {
    wrap.dataset.motion = 'reduced';
    sections.forEach((el) => {
      el.style.setProperty('--p', 0.5);
      el.style.setProperty('--in', 1);
    });
  }

  if (reduced || !stage || !canvas) {
    staticBlock();
    return;
  }

  const getJson = (url) => fetch(url, { cache: 'no-cache' }).then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.status))));

  // La versión de la película del reloj se usa en la dirección de los fotogramas para que
  // el service worker los guarde en la misma copia y no los borre al limpiar las viejas.
  Promise.all([
    getJson('frames/caja/manifest.json'),
    getJson('frames/manifest.json').then((m) => m.version || 0).catch(() => 0),
  ]).then(([manifest, mainVersion]) => run(manifest, mainVersion)).catch(staticBlock);

  function run(manifest, mainVersion) {
    const tiers = manifest.tiers.slice().sort((a, b) => b.minViewportWidth - a.minViewportWidth);
    const pickTier = () => tiers.find((t) => window.innerWidth >= t.minViewportWidth) || tiers[tiers.length - 1];
    let tier = pickTier();

    const frameCount = manifest.frameCount;
    const timeline = manifest.timeline;
    const pad = (n) => String(n).padStart(4, '0');
    const frameUrl = (i) => `${tier.path}/${tier.pattern.replace('%04d', pad(i + 1))}?v=${mainVersion}&c=${manifest.version || 0}`;

    let frames = new Array(frameCount).fill(null);
    let generation = 0;
    let started = false;
    let target = 0;
    let current = 0;
    let lastDrawn = -1;
    let running = false;

    const ctx = canvas.getContext('2d');
    let cw = 0;
    let ch = 0;

    function sizeCanvas() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
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
      const scale = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);   // object-fit: cover
      const dw = img.naturalWidth * scale;
      const dh = img.naturalHeight * scale;
      ctx.clearRect(0, 0, cw, ch);                                           // el fondo es transparente
      ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
      lastDrawn = i;
    }

    function progress() {
      const rect = stage.getBoundingClientRect();
      const total = rect.height - window.innerHeight;
      return total <= 0 ? 0 : clamp(-rect.top / total, 0, 1);
    }

    // Cada gesto ocurre en un tramo corto de scroll y luego la imagen espera mientras se lee.
    function frameAt(p) {
      for (let i = 1; i < timeline.length; i++) {
        if (p <= timeline[i][0]) {
          const [p0, f0] = timeline[i - 1];
          const [p1, f1] = timeline[i];
          let t = (p - p0) / Math.max(p1 - p0, 1e-6);
          t = t * t * (3 - 2 * t);
          return f0 + (f1 - f0) * t;
        }
      }
      return timeline[timeline.length - 1][1];
    }

    function applySections(p) {
      sections.forEach((el) => {
        const [a, b] = el.dataset.cajaRange.split(',').map(Number);
        const local = clamp((p - a) / Math.max(b - a, 0.0001), 0, 1);
        const inside = p >= a && p <= b;
        el.style.setProperty('--p', local.toFixed(4));
        el.style.setProperty('--in', inside ? 1 : 0);
        if (el.dataset.active !== String(inside)) {
          el.dataset.active = String(inside);
          el.style.pointerEvents = inside ? 'auto' : 'none';
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
      wrap.style.setProperty('--caja-progress', p.toFixed(4));
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

    function loadFrame(index, gen) {
      return new Promise((resolve) => {
        if (frames[index]) return resolve();
        const img = new Image();
        img.decoding = 'async';
        let settled = false;
        const done = () => {
          if (settled) return;
          settled = true;
          if (gen === generation) frames[index] = img;
          resolve();
        };
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
          if (Math.abs(i - Math.round(current)) <= 1) {
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

      // Primero el fotograma que toca ahora (se puede llegar aquí desde un enlace, a mitad de página).
      const first = Math.round(frameAt(progress()));
      current = first;
      await loadFrame(first, gen);
      if (gen !== generation) return;
      if (!frames[first]) {
        generation++;
        staticBlock();
        return;
      }
      wrap.dataset.sequence = 'ready';
      draw(first);
      applySections(progress());

      // Después los fotogramas en los que la imagen se para, y luego el resto, de cerca a lejos.
      const stops = Array.from(new Set(timeline.map(([, f]) => f)));
      await runQueue(stops, 4, gen);
      if (gen !== generation) return;
      schedule();
      const rest = [];
      for (let i = 0; i < frameCount; i++) rest.push(i);
      rest.sort((a, b) => Math.abs(a - first) - Math.abs(b - first));
      await runQueue(rest, 5, gen);
    }

    /* La película no se descarga hasta que la sección se acerca: no compite con la del reloj. */
    function start() {
      if (started) return;
      started = true;
      window.addEventListener('scroll', schedule, { passive: true });
      let resizeTimer;
      window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
          const next = pickTier();
          if (next !== tier) {
            tier = next;
            frames = new Array(frameCount).fill(null);
            boot();
            return;
          }
          sizeCanvas();
          schedule();
        }, 200);
      });
      boot();
    }

    applySections(0);
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          io.disconnect();
          start();
        }
      }, { rootMargin: '150% 0px 150% 0px' });
      io.observe(wrap);
    } else {
      start();
    }
  }
})();
