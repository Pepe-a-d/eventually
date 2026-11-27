// Sirve la web (la carpeta docs) y hace capturas del tutorial de la caja a varias alturas de scroll, en movil y en escritorio.
// Uso: node prueba5.mjs <docs> <salida> [movil,escritorio,iphone,estrecho,portatil,tumbado,grande] [0,0.04,0.19,...] [caja|reloj]
// Variables de entorno: MODULOS (carpeta node_modules, si no esta aqui) y CHROME (ruta de Google Chrome).
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const AQUI = path.dirname(new URL(import.meta.url).pathname);
const MODULOS = process.env.MODULOS || path.join(AQUI, 'node_modules');
const puppeteer = createRequire(path.join(MODULOS, 'x.js'))('puppeteer-core');
const RAIZ = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.css': 'text/css', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.webmanifest': 'application/manifest+json' };
const srv = http.createServer((req, res) => { let u = decodeURIComponent(req.url.split('?')[0]); if (u.endsWith('/')) u += 'index.html';
  const f = path.join(RAIZ, u); if (!f.startsWith(RAIZ) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); });
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const modo = process.argv[6] || 'caja';
const url = `http://127.0.0.1:${srv.address().port}/?${modo}`;
const browser = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox', '--hide-scrollbars', '--force-color-profile=srgb'] });
fs.mkdirSync(out, { recursive: true });
const modos = { movil: { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }, escritorio: { width: 1440, height: 900, deviceScaleFactor: 1 },
  iphone: { width: 390, height: 664, deviceScaleFactor: 2, isMobile: true, hasTouch: true }, estrecho: { width: 360, height: 800, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
  portatil: { width: 1024, height: 768, deviceScaleFactor: 1 }, tumbado: { width: 844, height: 390, deviceScaleFactor: 2, isMobile: true, hasTouch: true }, grande: { width: 1920, height: 1080, deviceScaleFactor: 1 } };
const ps = (process.argv[5] || '0,0.04,0.19,0.35,0.53,0.67,0.8,0.97').split(',').map(Number);
for (const nombre of (process.argv[4] || 'movil,escritorio').split(',')) {
  const page = await browser.newPage(); await page.setViewport(modos[nombre]);
  const errores = []; page.on('pageerror', (e) => errores.push(e.message)); page.on('console', (m) => { if (m.type() === 'error') errores.push(m.text()); });
  await page.goto(url, { waitUntil: 'networkidle2' }); await new Promise((r) => setTimeout(r, 1500));
  for (const p of ps) {
    await page.evaluate((p) => { const st = document.querySelector('[data-caja] .stage'); const top = st.getBoundingClientRect().top + scrollY; scrollTo(0, top + p * (st.offsetHeight - innerHeight)); }, p);
    await new Promise((r) => setTimeout(r, 2500));
    await page.screenshot({ path: `${out}/${modo}-${nombre}-${p.toFixed(2)}.jpg`, type: 'jpeg', quality: 85 });
  }
  const info = await page.evaluate(() => ({ seq: document.querySelector('[data-caja]').dataset.sequence, motion: document.querySelector('[data-caja]').dataset.motion || '', main: document.documentElement.dataset.sequence || '', imgs: performance.getEntriesByType('resource').filter((e) => e.name.includes('/frames/caja/')).length,
    malas: performance.getEntriesByType('resource').filter((e) => e.responseStatus >= 400).map((e) => e.name) }));
  console.log(nombre, JSON.stringify(info), 'errores:', JSON.stringify(errores.slice(0, 5)));
  await page.close();
}
await browser.close(); srv.close();
