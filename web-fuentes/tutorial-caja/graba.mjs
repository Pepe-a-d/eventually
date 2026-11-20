// Graba una vista previa: recorre con el scroll el tutorial de la caja dentro de la web, en tamaño de móvil.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { spawn } from 'node:child_process';
import puppeteer from 'puppeteer-core';
const RAIZ = '/home/claude/work/sitio';
const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.css': 'text/css', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.webmanifest': 'application/manifest+json' };
const srv = http.createServer((req, res) => { let u = decodeURIComponent(req.url.split('?')[0]); if (u.endsWith('/')) u += 'index.html';
  const f = path.join(RAIZ, u); if (!f.startsWith(RAIZ) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); });
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const browser = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox', '--hide-scrollbars', '--force-color-profile=srgb'] });
const page = await browser.newPage();
await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await page.goto(`http://127.0.0.1:${srv.address().port}/`, { waitUntil: 'networkidle2' });
const salida = process.argv[2];
const tmp = salida.replace(/\.mp4$/, '.tmp.mp4');
const FPS = 30, SEG = Number(process.argv[3] || 34);
// llegar a la seccion y esperar a que cargue toda la pelicula
await page.evaluate(() => { const st = document.querySelector('[data-caja] .stage'); scrollTo(0, st.getBoundingClientRect().top + scrollY - innerHeight * 0.9); });
await new Promise((r) => setTimeout(r, 9000));
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
const fin = new Promise((r) => ff.on('exit', r));
const n = FPS * SEG;
for (let i = 0; i < n; i++) {
  const x = i / (n - 1);
  // de 0,9 pantallas antes de la seccion a media pantalla despues, a ritmo constante
  await page.evaluate((x) => { const st = document.querySelector('[data-caja] .stage'); const top = st.getBoundingClientRect().top + scrollY; const a = top - innerHeight * 0.9, b = top + st.offsetHeight - innerHeight * 0.5; scrollTo(0, a + (b - a) * x); }, x);
  await new Promise((r) => setTimeout(r, 34));
  const img = await page.screenshot({ type: 'jpeg', quality: 90, optimizeForSpeed: true });
  if (!ff.stdin.write(img)) await new Promise((r) => ff.stdin.once('drain', r));
}
ff.stdin.end();
if ((await fin) === 0) { fs.renameSync(tmp, salida); console.log('hecho', salida); } else { console.log('ffmpeg fallo'); process.exitCode = 1; }
await browser.close(); srv.close();
