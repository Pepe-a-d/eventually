import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import puppeteer from 'puppeteer-core';
const RAIZ = '/home/claude/work/video', DATOS = process.argv[2], OUT = process.argv[3];
const srv = http.createServer((req, res) => { let u = decodeURIComponent(req.url.split('?')[0]); const f = u.startsWith('/datos/') ? path.join(DATOS, u.slice(7)) : path.join(RAIZ, u);
  if (!fs.existsSync(f)) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : 'application/json' }); fs.createReadStream(f).pipe(res); });
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const browser = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage(); await page.setViewport({ width: 1500, height: 1100 }); page.on('pageerror', (e) => console.log('ERR', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/caja.html`); await page.waitForFunction('window.listo === true', { timeout: 60000 });
const vistas = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
for (const [nombre, pos, mira, salida] of vistas) { const n = await page.evaluate((a, b, c) => window.pinta(a, b, c), nombre, pos, mira); await page.screenshot({ path: path.join(OUT, (salida || nombre) + '.png') }); console.log(salida || nombre, n); }
await browser.close(); srv.close();
