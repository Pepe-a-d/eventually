// Eventually, caja v5: la animacion. node anim.mjs <k> <n>   dibuja los trozos cuyo numero da resto k al dividir entre n (para repartir entre procesos).
// Cada trozo (90 cuadros) va directo a un .mp4; los que ya existen se saltan. Al final, junta.sh los une sin recodificar.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { spawn } from 'node:child_process'; import puppeteer from 'puppeteer-core';
const RAIZ = '/home/claude/work/video', DATOS = '/home/claude/work/anim', SAL = path.join(DATOS, 'trozos'); fs.mkdirSync(SAL, { recursive: true });
const K = parseInt(process.argv[2] || '0'), N = parseInt(process.argv[3] || '1'), LIMITE = parseFloat(process.env.LIMITE || '500') * 1000, T0 = Date.now();
const FPS = 30, TROZO = 90;
const ss = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); }, mix = (a, b, t) => a + (b - a) * t, mix3 = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
const tramos = (t, P) => { for (let i = 1; i < P.length; i++) if (t <= P[i][0]) return mix(P[i - 1][1], P[i][1], ss((t - P[i - 1][0]) / (P[i][0] - P[i - 1][0]))); return P[P.length - 1][1]; };
const orb = (az, r, z) => [r * Math.cos(az * Math.PI / 180), r * Math.sin(az * Math.PI / 180), z];
const DENTRO = ['cuerpo', 'base', 'tubo', 'plataforma', 'soporte', 'reloj_de_pega'], SAT = [1, 2, 3, 4, 5, 6].map((i) => 'satelite_' + i);
const LEY = { bisel: ['#9db7dd', 'bisel: lo que se gira'], rueda: ['#b7b3d9', 'rueda central, fija'], plato: ['#8fbf98', 'plato: lleva los satélites'], sat: ['#eef0f3', 'satélites (uno, azul)'], aro: ['#f0b46a', 'aro de las puertas'],
  teton: ['#c7641a', 'tetón'], tubo: ['#b9d4bd', 'tubo, con la rampa'], plat: ['#e7c1bb', 'plataforma'], base: ['#c9ccd1', 'base y columnas'], meseta: ['#f1e7b6', 'meseta, fija'], marco: ['#d9cfa8', 'marco, fijo'] };
const CORTE = { esquema: true, corte: [0, 1, 0, 0], sinSombra: true, cam: [108, -420, 118], mira: [0, 0, -66] };
const E = [
  { n: 'titulo', s: 3.5, f: (t, u) => ({ tau: 0, fundaZ: 0, cam: orb(-57 + 3 * u, 520, 300), mira: [0, 0, -80], titulo: ['Cómo funciona la caja', 'Eventually · Late Edition · 1 of 1'], velo: 0.62 * (1 - ss((t - 2.8) / 0.7)) }) },
  { n: 'funda', s: 4.5, f: (t, u) => ({ tau: 0, fundaZ: t < 3.1 ? 190 * ss(t / 3.0) : undefined, opaco: { funda: 1 - ss((t - 1.5) / 1.4), frase: 1 - ss((t - 1.5) / 1.4) }, cam: orb(-54 - 2 * u, 520, 300), mira: [0, 0, -80],
      t1: 'Se levanta la funda', t2: 'Debajo hay un cubo blanco. Arriba, un bisel redondo y, en el centro, dos puertas cerradas' }) },
  { n: 'apertura', s: 15, f: (t, u) => { const tau = tramos(t, [[0, 0], [0.8, 0], [3.2, 45], [3.6, 50], [6.8, 92], [13.4, 345], [15, 345]]);
      const tx = tau < 45 ? ['Se gira el bisel', 'Primer tramo: los engranajes giran y no pasa nada más'] : tau < 92 ? ['Las puertas se abren solas', 'Van por delante del reloj: no lo tocan nunca']
        : tau < 335 ? ['El reloj sube', 'De tope a tope, una vuelta y dos tercios de bisel'] : ['Arriba, tope', 'El reloj queda entre las dos puertas, que están de pie'];
      return { tau, cam: orb(-56 + 14 * u, 505, 300 + 25 * u), mira: [0, 0, -78 + 22 * ss((tau - 92) / 250)], t1: tx[0], t2: tx[1] }; } },
  { n: 'planetario', s: 9, f: (t, u) => ({ tau: tramos(t, [[0, 0], [0.8, 0], [8.4, 62], [9, 62]]), esquema: true, corte: [0, 0, -1, 6.4], sinSombra: true, oculta: DENTRO, cam: [0, -110, 360], mira: [0, -28, -10],
      t1: 'Por dentro: los engranajes', t2: t < 4.6 ? 'El bisel empuja seis satélites. La rueda central está fija: los satélites ruedan sobre ella y dan vueltas alrededor del hueco'
        : 'Sus ejes van en el plato, que gira a poco más de la mitad que el bisel. El plato es el que mueve todo lo demás', leyenda: [LEY.bisel, LEY.sat, LEY.rueda, LEY.plato] }) },
  { n: 'aro', s: 8, f: (t, u) => ({ tau: tramos(t, [[0, 40], [0.8, 40], [6.6, 100], [8, 100]]), esquema: true, sinSombra: true, oculta: ['cuerpo', 'bisel', 'meseta', 'rueda_central', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo', 'reloj_de_pega', 'soporte'].concat(SAT),
      opaco: { plato: 0.28 }, cam: [0, -185, 360], mira: [0, -20, -22], t1: 'Qué abre las puertas',
      t2: 'Bajo el plato hay una espiral. Al girar, mete un tetón hacia dentro, y el tetón hace girar 11° un aro escondido alrededor del hueco', leyenda: [LEY.plato, LEY.teton, LEY.aro, LEY.marco] }) },
  { n: 'manivela', s: 9, f: (t, u) => ({ tau: tramos(t, [[0, 55], [0.6, 55], [4.8, 95], [5.8, 95], [8.6, 55], [9, 55]]), esquema: true, corte: [0, 1, 0, 33.75], sinSombra: true,
      oculta: ['cuerpo', 'bisel', 'tubo', 'base', 'plataforma', 'soporte', 'reloj_de_pega', 'plato'].concat(SAT), cam: [0, -165, 22], mira: [0, 0, -14], t1: 'El aro mueve las dos puertas a la vez',
      t2: t < 4.8 ? 'Cada puerta lleva una bola metida en una pista del aro. La pista empuja la bola, y la puerta gira'
        : 'En los dos extremos de la pista la bola queda encajada: la puerta no se mueve aunque la empujen', leyenda: [LEY.aro, LEY.meseta, LEY.marco, LEY.rueda] }) },
  { n: 'ascensor', s: 10, f: (t, u) => ({ ...CORTE, tau: tramos(t, [[0, 85], [1.2, 92], [9, 345], [10, 345]]), t1: 'Qué sube el reloj',
      t2: t < 5 ? 'El tubo gira con el plato. Por dentro lleva tres ranuras en espiral, como un pintalabios'
        : 'La plataforma tiene un tetón en cada ranura y no puede girar, porque corre por tres columnas: solo puede subir', leyenda: [LEY.tubo, LEY.plat, LEY.base, LEY.plato] }) },
  { n: 'cierre', s: 9, f: (t, u) => ({ ...CORTE, tau: tramos(t, [[0, 345], [0.6, 345], [5.6, 92], [8.2, 0], [9, 0]]), t1: 'Para cerrar, se gira al revés',
      t2: 'El reloj baja y las puertas se cierran detrás. Lo hace la forma de las piezas: no hay muelles ni imanes que muevan nada' }) },
  { n: 'final', s: 4, f: (t, u) => ({ tau: 0, cam: orb(-50 - 3 * u, 520, 300), mira: [0, 0, -80], titulo: ['Es el modelo, no la caja', 'Dibujado el 21 de noviembre de 2026. Nada está impreso todavía: que funcione así lo dirán las probetas.'], velo: 0.8 * ss(t / 0.8) }) },
];
// lista de trozos
const trozos = []; E.forEach((e, ie) => { const nf = Math.round(e.s * FPS); for (let a = 0; a < nf; a += TROZO) trozos.push({ e, ie, a, b: Math.min(nf, a + TROZO), nf }); });
trozos.forEach((x, i) => { x.fichero = path.join(SAL, String(i).padStart(3, '0') + '-' + x.e.n + '.mp4'); });
if (process.argv[2] === 'lista') { console.log(trozos.map((x) => x.fichero).join('\n')); process.exit(0); }
if (process.argv[2] === 'fotos') { /* unas pocas fotos de prueba: node anim.mjs fotos "0:1.0,2:5.0" */ }
const srv = http.createServer((req, res) => { let u = decodeURIComponent(req.url.split('?')[0]); const f = u.startsWith('/datos/') ? path.join(DATOS, u.slice(7)) : path.join(RAIZ, u);
  if (!fs.existsSync(f)) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : 'application/json' }); fs.createReadStream(f).pipe(res); });
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const browser = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage(); await page.setViewport({ width: 1280, height: 720 }); page.on('pageerror', (e) => console.log('ERR', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/anim.html`); await page.waitForFunction('window.listo === true', { timeout: 120000 });
const estado = (x, k) => { const t = k / FPS; return x.e.f(t, k / (x.nf - 1)); };
if (process.argv[2] === 'fotos') {
  for (const par of process.argv[3].split(',')) { const [ie, t] = par.split(':').map(Number); const e = E[ie]; const nf = Math.round(e.s * FPS);
    await page.evaluate((s) => window.cuadro(s), e.f(t, t * FPS / (nf - 1))); await page.screenshot({ path: path.join(DATOS, `foto-${e.n}-${t}.jpg`), type: 'jpeg', quality: 92 }); }
} else {
  for (let i = 0; i < trozos.length; i++) {
    if (i % N !== K) continue; const x = trozos[i];
    if (fs.existsSync(x.fichero)) continue;
    if (Date.now() - T0 > LIMITE) { console.log('sin tiempo; quedan trozos'); break; }
    const tmp = x.fichero.replace('.mp4', '.tmp.mp4'), t1 = Date.now();
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', String(FPS), tmp]);
    const fin = new Promise((r) => ff.on('exit', r));
    for (let k = x.a; k < x.b; k++) { await page.evaluate((s) => window.cuadro(s), estado(x, k)); const buf = await page.screenshot({ type: 'jpeg', quality: 92 }); if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r)); }
    ff.stdin.end(); const cod = await fin;
    if (cod === 0) { fs.renameSync(tmp, x.fichero); console.log(path.basename(x.fichero), x.b - x.a, 'cuadros', ((Date.now() - t1) / 1000).toFixed(0), 's'); } else console.log('FALLO ffmpeg', cod, x.fichero);
  }
}
await browser.close(); srv.close();
