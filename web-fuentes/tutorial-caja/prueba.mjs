// Sirve el sitio y hace capturas a varias alturas de scroll del tutorial, en movil y en escritorio.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import puppeteer from 'puppeteer-core';
const RAIZ = '/home/claude/work/sitio';
const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.css': 'text/css', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.webmanifest': 'application/manifest+json' };
const srv = http.createServer((req, res) => { let u = decodeURIComponent(req.url.split('?')[0]); if (u.endsWith('/')) u += 'index.html';
  const f = path.join(RAIZ, u); if (!f.startsWith(RAIZ) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); });
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const url = `http://127.0.0.1:${srv.address().port}/`;
const browser = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox', '--hide-scrollbars', '--force-color-profile=srgb'] });
const out = '/home/claude/work/capturas-web'; fs.mkdirSync(out, { recursive: true });
const modos = { movil: { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }, escritorio: { width: 1440, height: 900, deviceScaleFactor: 1 } };
const ps = (process.argv[3] || '0,0.04,0.19,0.35,0.53,0.67,0.8,0.97').split(',').map(Number);
for (const nombre of (process.argv[2] || 'movil,escritorio').split(',')) {
  const page = await browser.newPage(); await page.setViewport(modos[nombre]);
  const errores = []; page.on('pageerror', (e) => errores.push(e.message)); page.on('console', (m) => { if (m.type() === 'error') errores.push(m.text()); });
  await page.goto(url, { waitUntil: 'networkidle2' }); await new Promise((r) => setTimeout(r, 1500));
  for (const p of ps) {
    await page.evaluate((p) => { const st = document.querySelector('[data-caja] .stage'); const top = st.getBoundingClientRect().top + scrollY; scrollTo(0, top + p * (st.offsetHeight - innerHeight)); }, p);
    await new Promise((r) => setTimeout(r, 2500));
    await page.screenshot({ path: `${out}/${nombre}-${p.toFixed(2)}.jpg`, type: 'jpeg', quality: 85 });
  }
  const info = await page.evaluate(() => ({ seq: document.querySelector('[data-caja]').dataset.sequence, motion: document.querySelector('[data-caja]').dataset.motion || '', main: document.documentElement.dataset.sequence || '', imgs: performance.getEntriesByType('resource').filter((e) => e.name.includes('/frames/caja/')).length }));
  console.log(nombre, JSON.stringify(info), 'errores:', JSON.stringify(errores.slice(0, 5)));
  await page.close();
}
await browser.close(); srv.close();
