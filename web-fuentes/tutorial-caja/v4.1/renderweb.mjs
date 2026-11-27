// Uso: node renderweb.mjs fotos <fondo> t1 t2 ...   |   node renderweb.mjs todo
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import puppeteer from 'puppeteer-core';
const RAIZ = path.dirname(new URL(import.meta.url).pathname);
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2' };
const srv = http.createServer((req, res) => { const f = path.join(RAIZ, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(RAIZ) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); });
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const browser = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: true,
  args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--hide-scrollbars', '--force-color-profile=srgb'] });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1934, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.log('[error]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/web.html`);
await page.waitForFunction('window.listo === true', { timeout: 180000 });
// tramos: [t0, t1, fotogramas]; el fotograma 0 es t = 0
export const TRAMOS = [[0, 1.5, 24], [1.5, 3.5, 30], [3.5, 5.7, 34], [5.7, 7.7, 30], [7.7, 9.3, 24], [9.3, 13.0, 46]];
const tiempos = [0];
for (const [a, b, n] of TRAMOS) for (let i = 1; i <= n; i++) tiempos.push(a + (b - a) * i / n);
const [modo, ...resto] = process.argv.slice(2);
if (modo === 'fotos') {
  fs.mkdirSync(path.join(RAIZ, 'fotosweb'), { recursive: true });
  for (const ts of resto) { await page.evaluate((t) => window.renderAt(t), Number(ts));
    await page.screenshot({ path: path.join(RAIZ, 'fotosweb', `w-${Number(ts).toFixed(2).padStart(5, '0')}.png`), type: 'png', omitBackground: true }); console.log('foto', ts); }
} else if (modo === 'todo') {
  const dir = path.join(RAIZ, 'webpng'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const ini = Date.now();
  for (let i = 0; i < tiempos.length; i++) { await page.evaluate((t) => window.renderAt(t), tiempos[i]);
    await page.screenshot({ path: path.join(dir, `f_${String(i + 1).padStart(4, '0')}.png`), type: 'png', omitBackground: true });
    if (i % 20 === 19) console.log(i + 1, '/', tiempos.length, ((Date.now() - ini) / (i + 1)).toFixed(0), 'ms'); }
  fs.writeFileSync(path.join(dir, 'tiempos.json'), JSON.stringify(tiempos)); console.log('hecho', tiempos.length);
}
await browser.close(); srv.close();
