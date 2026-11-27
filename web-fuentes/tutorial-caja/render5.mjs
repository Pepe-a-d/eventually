// Dibuja la escena del tutorial (caja5.html) en Chrome sin ventana y guarda un PNG transparente por fotograma.
// Uso:
//   node render5.mjs <datos> <salida> fotos t1 t2 ...   unas cuantas pruebas, en <salida>/w-<t>.png
//   node render5.mjs <datos> <salida> todo              los 189 fotogramas, en <salida>/f_0001.png ...
//   node render5.mjs <datos> <salida> enlace            la imagen de la vista previa del enlace (1200 x 630, con el papel de la web)
// <datos> es la carpeta donde mallas_v5.py dejo piezas.json.
// Variables de entorno: MODULOS (carpeta node_modules, si no esta aqui) y CHROME (ruta de Google Chrome).
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const RAIZ = path.dirname(new URL(import.meta.url).pathname);
const MODULOS = process.env.MODULOS || path.join(RAIZ, 'node_modules');
const puppeteer = createRequire(path.join(MODULOS, 'x.js'))('puppeteer-core');
const [DATOS, SALIDA, modo, ...resto] = process.argv.slice(2);
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json' };
const srv = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  const f = u.startsWith('/datos/') ? path.join(DATOS, u.slice(7)) : u.startsWith('/node_modules/') ? path.join(MODULOS, u.slice(14)) : path.join(RAIZ, u);
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const browser = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: true,
  args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--hide-scrollbars', '--force-color-profile=srgb'] });
const page = await browser.newPage();
const enlace = modo === 'enlace';
await page.setViewport(enlace ? { width: 1200, height: 630, deviceScaleFactor: 1 } : { width: 1080, height: 1934, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.log('[error]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/caja5.html${enlace ? '?enlace' : ''}`);
await page.waitForFunction('window.listo === true', { timeout: 180000 });
// tramos: [t0, t1, fotogramas]; el fotograma 0 es t = 0. Los limites son los de T en caja5.js, y los fotogramas en que
// acaba cada tramo son las paradas de 'timeline' en docs/frames/caja/manifest.json: 0, 24, 54, 88, 118, 142 y 188.
export const TRAMOS = [[0, 1.5, 24], [1.5, 3.5, 30], [3.5, 5.7, 34], [5.7, 7.7, 30], [7.7, 9.3, 24], [9.3, 13.0, 46]];
const tiempos = [0];
for (const [a, b, n] of TRAMOS) for (let i = 1; i <= n; i++) tiempos.push(a + (b - a) * i / n);
fs.mkdirSync(SALIDA, { recursive: true });
if (modo === 'fotos') {
  for (const ts of resto) { await page.evaluate((t) => window.renderAt(t), Number(ts));
    await page.screenshot({ path: path.join(SALIDA, `w-${Number(ts).toFixed(2).padStart(5, '0')}.png`), type: 'png', omitBackground: true }); console.log('foto', ts); }
} else if (modo === 'enlace') {
  await page.evaluate(() => window.renderAt(0));
  await page.screenshot({ path: path.join(SALIDA, 'enlace.png'), type: 'png' }); console.log('enlace');
} else if (modo === 'todo') {
  const ini = Date.now();
  for (let i = 0; i < tiempos.length; i++) { await page.evaluate((t) => window.renderAt(t), tiempos[i]);
    await page.screenshot({ path: path.join(SALIDA, `f_${String(i + 1).padStart(4, '0')}.png`), type: 'png', omitBackground: true });
    if (i % 20 === 19) console.log(i + 1, '/', tiempos.length, ((Date.now() - ini) / (i + 1)).toFixed(0), 'ms'); }
  fs.writeFileSync(path.join(SALIDA, 'tiempos.json'), JSON.stringify(tiempos)); console.log('hecho', tiempos.length);
}
await browser.close(); srv.close();
