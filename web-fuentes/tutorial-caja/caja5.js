// Eventually — tutorial de la caja v5 para la web. Escena en three.js.
// Las piezas y su movimiento salen del modelo (mallas_v5.py -> /datos/piezas.json). Aqui van la luz, la camara y el guion (funcion estado).
// window.renderAt(t) dibuja el instante t (segundos, de 0 a DUR). El fondo es transparente.
// Con ?enlace en la direccion, el lienzo es de 1200 x 630 y el fondo es el papel de la web: es la imagen de la vista previa del enlace.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const ENLACE = /[?&]enlace\b/.test(location.search);
const W = ENLACE ? 1200 : 1080, H = ENLACE ? 630 : 1934;
export const DUR = 13;
const rad = THREE.MathUtils.degToRad;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ease = (x) => { x = clamp(x); return x * x * x * (x * (6 * x - 15) + 10); };
const k = (t, a, b) => ease((t - a) / (b - a));
const lerp = (a, b, x) => a + (b - a) * x;

const datos = await (await fetch('/datos/piezas.json')).json();
const K = datos.cte, MOV = datos.mov;
const ALTO = K.alto;                                  // la caja va de z = -ALTO (la mesa) a z = 0 (la tapa)

// ------------------------------------------------------------ render
const canvas = document.getElementById('c');
canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: false });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.setClearColor(ENLACE ? 0xeceef0 : 0x000000, ENLACE ? 1 : 0);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(ENLACE ? 20 : 26, W / H, 10, 6000);
camera.up.set(0, 0, 1);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.5;

const sol = new THREE.DirectionalLight(0xffffff, 2.5);
sol.position.set(-455, -365, 400 - ALTO / 2);          // de la izquierda y un poco de frente: la sombra cae a la derecha, donde se ve
sol.target.position.set(-20, -50, -ALTO / 2);
sol.castShadow = true;
sol.shadow.mapSize.set(2048, 2048);
Object.assign(sol.shadow.camera, { left: -380, right: 380, top: 380, bottom: -380, near: 50, far: 1600 });
sol.shadow.bias = -0.0004;
sol.shadow.normalBias = 0.6;
sol.shadow.radius = 5;
scene.add(sol, sol.target);
scene.add(new THREE.HemisphereLight(0xffffff, 0xcfcabb, 0.4));
const relleno = new THREE.DirectionalLight(0xffffff, 0.35);
relleno.position.set(300, -150, -260);
scene.add(relleno);

const suelo = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000), new THREE.ShadowMaterial({ opacity: 0.2, transparent: true }));
suelo.position.z = -ALTO - 0.05;
suelo.receiveShadow = true;
scene.add(suelo);

// ------------------------------------------------------------ piezas
const COL = { blanco: 0xf7f6f2, marmol: 0xecebe7, azul: 0x1f3fa8, gris: 0x565a62, linea: 0x33353b };
const LINEA = { bisel: 0.2, rueda_central: 0.24, satelite: 0.3, funda: 0.4, frase: 0, reloj_de_pega: 0.25 };      // cuanto se marcan las aristas
const piezas = {};
for (const q of datos.piezas) {
  let geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(q.v, 3));
  geo.setIndex(q.t);
  geo = geo.toNonIndexed();
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({ color: COL[q.color], roughness: q.color === 'gris' ? 0.6 : 0.82, metalness: q.color === 'gris' ? 0.15 : 0,
    polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.castShadow = mesh.receiveShadow = true;
  const clave = Object.keys(LINEA).find((c) => q.n.startsWith(c));
  const lineaBase = clave ? LINEA[clave] : 0.42;
  const lines = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 30), new THREE.LineBasicMaterial({ color: COL.linea, transparent: true, opacity: lineaBase }));
  const g = new THREE.Group();
  g.add(mesh, lines);
  g.matrixAutoUpdate = false;
  g.userData = { mesh, lines, lineaBase, mueve: q.mueve };
  scene.add(g);
  piezas[q.n] = g;
}
if (piezas.frase) piezas.frase.userData.mesh.castShadow = false;

function setOp(g, op) {
  const { mesh, lines, lineaBase } = g.userData;
  g.visible = op > 0.004;
  if (!g.visible) return;
  const tr = op < 0.995, m = mesh.material;
  if (m.transparent !== tr) { m.transparent = tr; m.depthWrite = !tr; m.needsUpdate = true; }
  m.opacity = op;
  mesh.castShadow = op > 0.5;
  lines.material.opacity = lineaBase * op;
}

// La flecha azul que dice hacia donde se gira: un arco plano con punta, delante de la caja.
function flecha(sentido) {
  const R = 104, ancho = 3.4, a0 = rad(-52), a1 = rad(-128);              // de la derecha a la izquierda pasando por delante = como las agujas del reloj, visto desde arriba
  const [ini, fin] = sentido < 0 ? [a0, a1] : [a1, a0];
  const forma = new THREE.Shape();
  const n = 40, punta = rad(9) * Math.sign(fin - ini);
  const cuerpoFin = fin - punta;
  for (let i = 0; i <= n; i++) { const a = lerp(ini, cuerpoFin, i / n); const x = (R + ancho / 2) * Math.cos(a), y = (R + ancho / 2) * Math.sin(a); i ? forma.lineTo(x, y) : forma.moveTo(x, y); }
  forma.lineTo((R + ancho * 2.1) * Math.cos(cuerpoFin), (R + ancho * 2.1) * Math.sin(cuerpoFin));
  forma.lineTo(R * Math.cos(fin), R * Math.sin(fin));
  forma.lineTo((R - ancho * 2.1) * Math.cos(cuerpoFin), (R - ancho * 2.1) * Math.sin(cuerpoFin));
  for (let i = n; i >= 0; i--) { const a = lerp(ini, cuerpoFin, i / n); forma.lineTo((R - ancho / 2) * Math.cos(a), (R - ancho / 2) * Math.sin(a)); }
  const m = new THREE.Mesh(new THREE.ShapeGeometry(forma), new THREE.MeshBasicMaterial({ color: COL.azul, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
  m.position.z = 1.5;
  m.renderOrder = 5;
  scene.add(m);
  return m;
}
const flechaAbrir = flecha(-1), flechaCerrar = flecha(1);

// ------------------------------------------------------------ movimiento (lo mismo que 'mover' de caja_piezas_v5.py)
function movimiento(tau) {
  const x = clamp(tau, 0, K.giro_tubo) / K.paso, i = Math.min(Math.floor(x), MOV.length - 2), f = x - i;
  return MOV[i].map((v, j) => lerp(v, MOV[i + 1][j], f));       // [s, psi, ang, h]
}
const M = new THREE.Matrix4(), A = new THREE.Matrix4(), B = new THREE.Matrix4();
function coloca(g, tau, mv) {
  const [s, psi, ang, h] = mv, mueve = g.userData.mueve, m = g.matrix;
  m.identity();
  if (mueve === 'tubo') m.makeRotationZ(rad(K.rot * tau));
  else if (mueve === 'bisel') m.makeRotationZ(rad(K.rot * tau / K.relacion));
  else if (mueve === 'plataforma') m.makeTranslation(0, 0, h);
  else if (mueve.startsWith('pestillo')) {
    const a = rad(Number(mueve.split(':')[1])), q = Math.min(2.7, Math.max(0, h - K.recorrido + K.pestillo_libre + 3.2));
    m.makeTranslation(q * Math.cos(a), q * Math.sin(a), h);
  } else if (mueve === 'aro') m.makeRotationZ(rad(K.aro_sentido * psi));
  else if (mueve === 'teton') m.makeTranslation(0, -s, 0);
  else if (mueve === 'puerta_derecha' || mueve === 'puerta_izquierda') {
    const sx = mueve === 'puerta_derecha' ? 1 : -1;
    m.makeTranslation(sx * K.eje_x, 0, K.eje_z).multiply(A.makeRotationY(rad(sx * ang))).multiply(B.makeTranslation(-sx * K.eje_x, 0, -K.eje_z));
  } else if (mueve.startsWith('satelite')) {
    const th = rad(Number(mueve.split(':')[1])), cx = K.r_ejes * Math.cos(th), cy = K.r_ejes * Math.sin(th), dth = K.rot * tau;
    m.makeRotationZ(rad(dth)).multiply(A.makeTranslation(cx, cy, 0)).multiply(B.makeRotationZ(rad(dth * K.z_central / K.z_satelite))).multiply(M.makeTranslation(-cx, -cy, 0));
  }
}

// ------------------------------------------------------------ guion
// Los tramos (segundos). Cada uno es un gesto; render5.mjs reparte los fotogramas con estos mismos limites.
export const T = { funda: [0, 1.5], vacio: [1.5, 3.5], puertas: [3.5, 5.7], sube: [5.7, 7.7], coger: [7.7, 9.3], cerrar: [9.3, 13] };
const TAU_VACIO = 45, TAU_PUERTAS = 100, GIRO = K.giro_tubo;
const FUERA = { x: -128, y: -168 };                    // donde queda el soporte fuera de la caja: delante y a la izquierda, en la mesa
const FUNDA_SUBE = 440;                                // la funda sube hasta salirse del fotograma

// Camaras: [direccion desde el punto que se mira, distancia, punto que se mira]
const CAM = {
  cerrada: { dir: [-0.50, -0.80, 0.52], dist: 1400, mira: [0, 0, -ALTO * 0.52] },
  arriba:  { dir: [-0.30, -0.66, 0.78], dist: 1340, mira: [0, 0, -30] },
  frente:  { dir: [-0.42, -0.84, 0.40], dist: 1440, mira: [0, 0, -30] },
  fuera:   { dir: [-0.36, -0.86, 0.44], dist: 1600, mira: [-42, -40, -50] },
};
function mezcla(a, b, x) {
  const d = new THREE.Vector3(...a.dir).normalize().lerp(new THREE.Vector3(...b.dir).normalize(), x).normalize();
  return { dir: d, dist: lerp(a.dist, b.dist, x), mira: new THREE.Vector3(...a.mira).lerp(new THREE.Vector3(...b.mira), x) };
}

function estado(t) {
  const e = { tau: 0, fundaZ: 0, fundaOp: 1, sop: [0, 0, 0], abrir: 0, cerrar: 0, cam: null };
  const sopFuera = (x) => {                           // el soporte con el reloj: primero sube recto, luego viene hacia delante y baja a la mesa
    const sube = ease(clamp(x / 0.42)), va = ease(clamp((x - 0.30) / 0.70));
    const zArriba = 66, zMesa = -K.recorrido - (ALTO - 108.4) + 0;      // al acabar, su pie apoya en la mesa
    return [FUERA.x * va, FUERA.y * va, lerp(zArriba * sube, zMesa, va)];
  };
  if (t <= T.funda[1]) {
    const x = k(t, 0.05, T.funda[1]);
    e.fundaZ = FUNDA_SUBE * x; e.fundaOp = 1 - k(t, 1.05, 1.42);
    e.cam = mezcla(CAM.cerrada, CAM.arriba, k(t, 0.55, T.funda[1]));
  } else if (t <= T.vacio[1]) {
    e.fundaOp = 0; e.tau = TAU_VACIO * k(t, T.vacio[0] + 0.15, T.vacio[1]);
    e.abrir = k(t, T.vacio[0], T.vacio[0] + 0.45);
    e.cam = mezcla(CAM.arriba, CAM.arriba, 0);
  } else if (t <= T.puertas[1]) {
    e.fundaOp = 0; e.tau = lerp(TAU_VACIO, TAU_PUERTAS, k(t, T.puertas[0], T.puertas[1])); e.abrir = 1;
    e.cam = mezcla(CAM.arriba, CAM.arriba, 0);
  } else if (t <= T.sube[1]) {
    e.fundaOp = 0; e.tau = lerp(TAU_PUERTAS, GIRO, k(t, T.sube[0], T.sube[1] - 0.1));
    e.abrir = 1 - k(t, T.sube[1] - 0.55, T.sube[1] - 0.1);
    e.cam = mezcla(CAM.arriba, CAM.frente, k(t, T.sube[0], T.sube[1] - 0.2));
  } else if (t <= T.coger[1]) {
    e.fundaOp = 0; e.tau = GIRO; e.sop = sopFuera(k(t, T.coger[0], T.coger[1]));
    e.cam = mezcla(CAM.frente, CAM.fuera, k(t, T.coger[0], T.coger[1] - 0.2));
  } else {
    const a = T.cerrar[0];                             // al reves: el soporte vuelve, el reloj baja, las puertas se cierran y vuelve la funda
    e.sop = sopFuera(1 - k(t, a, a + 0.95));
    e.tau = GIRO * (1 - k(t, a + 0.85, a + 2.75));
    e.cerrar = k(t, a + 0.8, a + 1.1) * (1 - k(t, a + 2.4, a + 2.75));
    e.fundaOp = k(t, a + 2.5, a + 2.85); e.fundaZ = FUNDA_SUBE * (1 - k(t, a + 2.45, a + 3.6));
    const c1 = mezcla(CAM.fuera, CAM.frente, k(t, a, a + 0.9));
    const c2 = mezcla(CAM.frente, CAM.arriba, k(t, a + 0.9, a + 2.0));
    const c3 = mezcla(CAM.arriba, CAM.cerrada, k(t, a + 2.3, a + 3.5));
    e.cam = t < a + 0.9 ? c1 : t < a + 2.3 ? c2 : c3;
  }
  return e;
}

// Lo que se mira queda en el tercio de arriba del fotograma: debajo va el texto de la pagina.
const SUBE_PX = ENLACE ? 0 : 0.165 * H;
function ponCamara(c) {
  camera.position.copy(c.mira).addScaledVector(c.dir, c.dist);
  camera.lookAt(c.mira);
  if (SUBE_PX) camera.setViewOffset(W, H, 0, SUBE_PX, W, H);
  camera.updateProjectionMatrix();
}

window.renderAt = (t) => {
  const e = estado(clamp(t, 0, DUR)), mv = movimiento(e.tau);
  for (const [n, g] of Object.entries(piezas)) {
    coloca(g, e.tau, mv);
    if (n === 'funda' || n === 'frase') {
      g.matrix.makeTranslation(0, 0, e.fundaZ); setOp(g, e.fundaOp);
      g.userData.mesh.castShadow = n === 'funda' && e.fundaZ < 0.5 && e.fundaOp > 0.5;      // levantada no da sombra: taparia la caja
    }
    if (n === 'soporte' || n === 'reloj_de_pega') g.matrix.premultiply(A.makeTranslation(e.sop[0], e.sop[1], e.sop[2]));
    g.matrixWorldNeedsUpdate = true;
  }
  flechaAbrir.material.opacity = 0.9 * e.abrir; flechaAbrir.visible = e.abrir > 0.004;
  flechaCerrar.material.opacity = 0.9 * e.cerrar; flechaCerrar.visible = e.cerrar > 0.004;
  ponCamara(ENLACE ? { dir: new THREE.Vector3(...CAM.cerrada.dir).normalize(), dist: 1010, mira: new THREE.Vector3(8, 0, -ALTO * 0.5) } : e.cam);
  renderer.render(scene, camera);
  return { tau: e.tau };
};
window.DUR = DUR; window.TRAMOS_T = T;
window.renderAt(0);
window.listo = true;
