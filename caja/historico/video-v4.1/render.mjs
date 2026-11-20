// Uso:  node render.mjs fotos 3 12.8 22 ...      -> fotos/f-<t>.jpg
//       node render.mjs escena <nombre> <t0> <t1> -> escenas/<nombre>.mp4
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import puppeteer from 'puppeteer-core';

const RAIZ = path.dirname(new URL(import.meta.url).pathname);
const FPS = 30;
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2' };
const srv = http.createServer((req, res) => {
  const f = path.join(RAIZ, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(RAIZ) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const puerto = srv.address().port;

const browser = await puppeteer.launch({
  executablePath: '/usr/bin/google-chrome', headless: true,
  args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--hide-scrollbars', '--force-color-profile=srgb', '--window-size=1920,1080'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
page.on('console', (m) => console.log('[pagina]', m.text()));
page.on('pageerror', (e) => console.log('[error]', e.message));
await page.goto(`http://127.0.0.1:${puerto}/escena.html`);
await page.waitForFunction('window.listo === true', { timeout: 180000 });

const [modo, ...resto] = process.argv.slice(2);
if (modo === 'fotos') {
  fs.mkdirSync(path.join(RAIZ, 'fotos'), { recursive: true });
  for (const ts of resto) {
    const t0 = Date.now();
    await page.evaluate((t) => window.renderAt(t), Number(ts));
    await page.screenshot({ path: path.join(RAIZ, 'fotos', `f-${Number(ts).toFixed(1).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
    console.log('foto', ts, Date.now() - t0, 'ms');
  }
} else if (modo === 'escena') {
  const [nombre, a, b] = resto;
  fs.mkdirSync(path.join(RAIZ, 'escenas'), { recursive: true });
  const tmp = path.join(RAIZ, 'escenas', `${nombre}.tmp.mp4`), fin = path.join(RAIZ, 'escenas', `${nombre}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
  const salida = new Promise((r) => ff.on('exit', r));
  const n0 = Math.round(Number(a) * FPS), n1 = Math.round(Number(b) * FPS);
  const ini = Date.now();
  for (let n = n0; n < n1; n++) {
    await page.evaluate((t) => window.renderAt(t), n / FPS);
    const img = await page.screenshot({ type: 'jpeg', quality: 92, optimizeForSpeed: true });
    if (!ff.stdin.write(img)) await new Promise((r) => ff.stdin.once('drain', r));
    if ((n - n0) % 30 === 29) console.log(nombre, n - n0 + 1, '/', n1 - n0, ((Date.now() - ini) / (n - n0 + 1)).toFixed(0), 'ms/fotograma');
  }
  ff.stdin.end();
  const cod = await salida;
  if (cod === 0) { fs.renameSync(tmp, fin); console.log('hecho', fin); } else { console.log('ffmpeg fallo', cod); process.exitCode = 1; }
}
await browser.close();
srv.close();
