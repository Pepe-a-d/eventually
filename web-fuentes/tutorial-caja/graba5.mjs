// Graba la web recorriendo el tutorial de la caja a velocidad constante, para ver el ritmo: un JPG por instante, que luego se juntan con ffmpeg.
// Uso: node graba5.mjs <docs> <salida> [pantallas por segundo, 0.5] [fotogramas por segundo, 12]
//   ffmpeg -framerate 12 -i <salida>/g_%04d.jpg -vf scale=540:-2,format=yuv420p -c:v libx264 -crf 20 ritmo.mp4
// Variables de entorno: MODULOS (carpeta node_modules, si no esta aqui) y CHROME (ruta de Google Chrome).
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const AQUI = path.dirname(new URL(import.meta.url).pathname);
const MODULOS = process.env.MODULOS || path.join(AQUI, 'node_modules');
const puppeteer = createRequire(path.join(MODULOS, 'x.js'))('puppeteer-core');
const RAIZ = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
const VEL = Number(process.argv[4] || 0.5), FPS = Number(process.argv[5] || 12);
const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.css': 'text/css', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.webmanifest': 'application/manifest+json' };
const srv = http.createServer((req, res) => { let u = decodeURIComponent(req.url.split('?')[0]); if (u.endsWith('/')) u += 'index.html';
  const f = path.join(RAIZ, u); if (!f.startsWith(RAIZ) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); });
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const browser = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox', '--hide-scrollbars', '--force-color-profile=srgb'] });
fs.mkdirSync(out, { recursive: true });
const page = await browser.newPage(); await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 1.5, isMobile: true, hasTouch: true });
await page.goto(`http://127.0.0.1:${srv.address().port}/?caja`, { waitUntil: 'networkidle2' });
// se recorre una vez deprisa para que carguen todos los fotogramas
const largo = await page.evaluate(() => { const st = document.querySelector('[data-caja] .stage'); return st.offsetHeight - innerHeight; });
for (let y = 0; y <= largo; y += 400) { await page.evaluate((y) => scrollTo(0, y), y); await new Promise((r) => setTimeout(r, 120)); }
await page.evaluate(() => scrollTo(0, 0)); await new Promise((r) => setTimeout(r, 3000));
const n = Math.ceil(largo / (VEL * 844) * FPS) + FPS;                 // un segundo quieto al final
for (let i = 0; i < n; i++) {
  const t0 = Date.now();
  await page.evaluate((y) => scrollTo(0, y), Math.min(largo, i * VEL * 844 / FPS));
  await new Promise((r) => setTimeout(r, Math.max(10, 1000 / FPS - 45)));
  await page.screenshot({ path: path.join(out, `g_${String(i + 1).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 92 });
}
console.log('fotogramas', n, 'largo', largo);
await browser.close(); srv.close();
