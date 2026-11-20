import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const W = 1920, H = 1080;
export const DUR = 68;
const rad = THREE.MathUtils.degToRad;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ease = (x) => { x = clamp(x); return x * x * x * (x * (6 * x - 15) + 10); };
const k = (t, a, b) => ease((t - a) / (b - a));
const lerp = (a, b, x) => a + (b - a) * x;

const datos = await (await fetch('/mallas/datos.json')).json();
const P = datos.P, D = datos.D;
const Do = D.Do, Ho = D.Ho;

// ------------------------------------------------------------ render
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: false });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.setClearColor(0x000000, 0);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(26, W / H, 10, 6000);
camera.up.set(0, 0, 1);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.5;

const sol = new THREE.DirectionalLight(0xffffff, 2.5);
sol.position.set(-330, -470, 380);
sol.target.position.set(-20, -50, 30);
sol.castShadow = true;
sol.shadow.mapSize.set(2048, 2048);
Object.assign(sol.shadow.camera, { left: -330, right: 330, top: 330, bottom: -330, near: 50, far: 1600 });
sol.shadow.bias = -0.0004;
sol.shadow.normalBias = 0.6;
sol.shadow.radius = 5;
scene.add(sol, sol.target);
scene.add(new THREE.HemisphereLight(0xffffff, 0xcfcabb, 0.32));
const relleno = new THREE.DirectionalLight(0xffffff, 0.35);
relleno.position.set(300, -150, -260);
scene.add(relleno);

const suelo = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000), new THREE.ShadowMaterial({ opacity: 0.2, transparent: true }));
suelo.position.z = -0.05;
suelo.receiveShadow = true;
scene.add(suelo);

// ------------------------------------------------------------ piezas
const COL = { papel: 0xf7f6f2, marmol: 0xecebe7, azul: 0x1f3fa8, petg: 0xd6dbe0, acero: 0x70747a, ambar: 0xdd8a1c, verde: 0x2f9e6e, iman: 0x8f959d, linea: 0x33353b };

async function bin(n, ext, T) { return new T(await (await fetch(`/mallas/${n}.${ext}`)).arrayBuffer()); }

function conLineas(geo, mat, lineGeo) {
  const mesh = new THREE.Mesh(geo, mat);
  mesh.castShadow = mesh.receiveShadow = true;
  mat.polygonOffset = true; mat.polygonOffsetFactor = 1; mat.polygonOffsetUnits = 1;
  const lines = new THREE.LineSegments(lineGeo, new THREE.LineBasicMaterial({ color: COL.linea, transparent: true, opacity: 0.5 }));
  const g = new THREE.Group();
  g.add(mesh, lines);
  g.userData = { mesh, lines, lineaBase: 0.5 };
  return g;
}

async function parte(n, color, o = {}) {
  const [pos, nor, idx, edg] = await Promise.all([bin(n, 'pos', Float32Array), bin(n, 'nor', Float32Array), bin(n, 'idx', Uint32Array), bin(n, 'edg', Float32Array)]);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  geo.setIndex(new THREE.BufferAttribute(idx, 1));
  const lg = new THREE.BufferGeometry();
  lg.setAttribute('position', new THREE.BufferAttribute(edg, 3));
  const mat = new THREE.MeshStandardMaterial({ color, roughness: o.rough ?? 0.82, metalness: o.metal ?? 0.0 });
  const g = conLineas(geo, mat, lg);
  if (o.linea !== undefined) g.userData.lineaBase = o.linea;
  return g;
}

function setOp(g, op) {
  const { mesh, lines, lineaBase } = g.userData;
  g.visible = op > 0.004;
  if (!g.visible) return;
  const tr = op < 0.995, m = mesh.material;
  if (m.transparent !== tr) { m.transparent = tr; m.needsUpdate = true; }
  m.opacity = op;
  m.depthWrite = !tr;
  mesh.castShadow = op > 0.6;
  mesh.renderOrder = tr ? 2 : 0;
  lines.material.opacity = lineaBase * Math.min(1, op * 3.2);
}

const [base, tapa, tapeta, rotor, aguja, peana, pinza, funda, frase, reloj, tarjeta] = await Promise.all([
  parte('base', COL.papel), parte('tapa', COL.papel), parte('tapeta', COL.papel), parte('rotor_sin_muelle', COL.ambar, { rough: 0.7 }),
  parte('aguja', COL.azul, { rough: 0.6, linea: 0.35 }), parte('peana', COL.papel), parte('pinza', COL.petg, { rough: 0.45 }),
  parte('funda', COL.marmol), parte('frase', COL.azul, { rough: 0.6, linea: 0.0 }), parte('reloj_referencia', COL.acero, { rough: 0.42, metal: 0.75, linea: 0.3 }),
  parte('tarjeta_referencia', 0xfdfdfb)]);

// sistema L (caja tumbada) -> mundo
const ML = new THREE.Matrix4().makeBasis(new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 1), new THREE.Vector3(0, -1, 0)).setPosition(0, Do / 2, Ho / 2);
const MLi = ML.clone().invert();
function grupoL() { const g = new THREE.Group(); g.matrixAutoUpdate = false; g.matrix.copy(ML); return g; }
function enL(obj) { const g = new THREE.Group(); g.matrixAutoUpdate = false; g.matrix.copy(MLi); g.add(obj); return g; }

// imanes
const matIman = new THREE.MeshStandardMaterial({ color: COL.iman, roughness: 0.3, metalness: 0.9, transparent: true });
const geoImanZ = new THREE.CylinderGeometry(P.iman_d / 2, P.iman_d / 2, P.iman_h, 36).rotateX(Math.PI / 2);
function iman(x, y, z) { const m = new THREE.Mesh(geoImanZ, matIman); m.position.set(x, y, z); m.renderOrder = 1; return m; }

const zt = D.cb + P.rotor_grosor;
const fundaG = new THREE.Group(), fraseG = new THREE.Group(), baseG = new THREE.Group(), panelG = new THREE.Group();
const tapaG = new THREE.Group(), rotG = new THREE.Group(), tapetaG = new THREE.Group(), tarjetaG = new THREE.Group();
const standG = new THREE.Group(), upG = new THREE.Group(), agujaG = new THREE.Group();
fraseG.add(frase); fundaG.add(funda, fraseG);
const baseL = grupoL();
for (const [sx, sy] of [[-1, 1], [1, -1]]) baseL.add(iman(sx * D.mx, sy * D.my, D.zs - P.iman_cubierta - P.iman_aloj_h / 2));
baseG.add(base, baseL);
const tapaL = grupoL();
tapaL.add(iman(0, 0, D.ct - P.iman_central_retiro - P.iman_h / 2));
for (const [sx, sy] of [[-1, 1], [1, -1]]) tapaL.add(iman(sx * D.mx, sy * D.my, D.zs + P.iman_cubierta + P.iman_aloj_h / 2));
tapaG.add(tapa, tapaL);
const rotL = grupoL(), pivote = new THREE.Group();
pivote.add(enL(rotor), iman(0, -P.rotor_radio_iman, zt - P.iman_aloj_h / 2));
rotL.add(pivote);
rotG.add(rotL);
tapetaG.add(tapeta); tarjetaG.add(tarjeta);
panelG.add(tapaG, rotG, tapetaG, tarjetaG);
panelG.matrixAutoUpdate = false;
upG.add(pinza, reloj); standG.add(peana, upG);

// muelle en espiral (se recalcula con el giro) y su taco con ojo
const matMuelle = new THREE.MeshStandardMaterial({ color: COL.ambar, roughness: 0.7 });
const matLineaM = new THREE.LineBasicMaterial({ color: COL.linea, transparent: true, opacity: 0.45 });
const muelle = new THREE.Mesh(new THREE.BufferGeometry(), matMuelle);
muelle.castShadow = true;
const muelleLin = new THREE.LineSegments(new THREE.BufferGeometry(), matLineaM);
rotL.add(muelle, muelleLin);
{
  const x1 = P.muelle_radio_ext + P.muelle_ancla_largo, a = P.muelle_ancla_ancho / 2;
  const s = new THREE.Shape();
  s.moveTo(-x1, -a); s.lineTo(-P.muelle_radio_ext + P.muelle_grosor, -a); s.lineTo(-P.muelle_radio_ext + P.muelle_grosor, a); s.lineTo(-x1, a); s.closePath();
  const h = new THREE.Path(); h.absarc(-D.rojo, 0, P.ancla_ojo_d / 2, 0, Math.PI * 2, true); s.holes.push(h);
  const g = new THREE.ExtrudeGeometry(s, { depth: P.muelle_alto, bevelEnabled: false, curveSegments: 20 });
  const taco = new THREE.Mesh(g, matMuelle);
  taco.position.z = zt - P.muelle_alto; taco.rotation.z = rad(P.muelle_ancla_ang); taco.castShadow = true;
  const tl = new THREE.LineSegments(new THREE.EdgesGeometry(g, 30), matLineaM);
  tl.position.copy(taco.position); tl.rotation.copy(taco.rotation);
  rotL.add(taco, tl);
}
let thetaMuelle = null;
function ponMuelle(theta) {
  if (thetaMuelle !== null && Math.abs(theta - thetaMuelle) < 0.02) return;
  thetaMuelle = theta;
  const g = P.muelle_grosor, r0 = P.cubo_radio - 0.4, r1 = P.muelle_radio_ext - g / 2, tot = 360 * P.muelle_vueltas, n = Math.floor(tot / 4) + 1;
  const c = [];
  for (let i = 0; i <= n; i++) {
    const f = i / n, an = rad(180 - tot + tot * f + P.muelle_ancla_ang - theta * (1 - f)), r = r0 + (r1 - r0) * f;
    c.push([r * Math.cos(an), r * Math.sin(an)]);
  }
  const ext = [], itr = [];
  for (let i = 0; i <= n; i++) {
    const a = c[Math.max(0, i - 1)], b = c[Math.min(n, i + 1)];
    let nx = b[1] - a[1], ny = -(b[0] - a[0]);
    const l = Math.hypot(nx, ny); nx /= l; ny /= l;
    if (nx * c[i][0] + ny * c[i][1] < 0) { nx = -nx; ny = -ny; }
    ext.push([c[i][0] + nx * g / 2, c[i][1] + ny * g / 2]);
    itr.push([c[i][0] - nx * g / 2, c[i][1] - ny * g / 2]);
  }
  const s = new THREE.Shape();
  [...ext, ...itr.reverse()].forEach((p, i) => (i ? s.lineTo(p[0], p[1]) : s.moveTo(p[0], p[1])));
  s.closePath();
  const geo = new THREE.ExtrudeGeometry(s, { depth: P.muelle_alto, bevelEnabled: false });
  geo.translate(0, 0, zt - P.muelle_alto);
  muelle.geometry.dispose(); muelle.geometry = geo;
  muelleLin.geometry.dispose(); muelleLin.geometry = new THREE.EdgesGeometry(geo, 50);
}

// aguja: en local u = eje, v = ancho, w = grosor
const poseGuardada = { o: new THREE.Vector3(D.xn, D.yh, D.zr), u: new THREE.Vector3(0, -1, 0), v: new THREE.Vector3(1, 0, 0), w: new THREE.Vector3(0, 0, 1) };
const mPose = (p) => new THREE.Matrix4().makeBasis(p.u, p.v, p.w).setPosition(p.o);
{
  const inv = new THREE.Group(); inv.matrixAutoUpdate = false; inv.matrix.copy(mPose(poseGuardada).invert()); inv.add(aguja);
  agujaG.add(inv);
  for (const u of [0, -P.rotor_radio_iman]) agujaG.add(iman(u, 0, P.aguja_suelo + P.iman_h / 2));
  agujaG.matrixAutoUpdate = false;
}

// clip de emergencia
const ye = Do / 2 - (D.cb + P.rotor_grosor / 2);
const clip = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 46, 16).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x5d6168, roughness: 0.3, metalness: 0.9 }));
clip.castShadow = true;

scene.add(fundaG, baseG, panelG, standG, agujaG, clip);

// ------------------------------------------------------------ rotulos
const ui = { titulo: document.getElementById('titulo'), paso: document.getElementById('paso'), estado: document.getElementById('estado'), fin: document.getElementById('fin'), lineas: document.getElementById('lineas') };
const pasoN = ui.paso.querySelector('.n'), pasoH = ui.paso.querySelector('.h'), pasoS = ui.paso.querySelector('.s');
const estP = ui.estado.querySelector('.p'), estG = ui.estado.querySelector('.g');
Object.assign(ui.paso.style, { background: 'rgba(250,249,245,.84)', padding: '26px 40px 28px 30px', borderRadius: '30px', boxShadow: '0 2px 24px rgba(60,55,40,.08)' });

const PASOS = [
  [4.7, 8.8, '1', 'Levanta la funda', 'Dos nervios la retienen: basta un tirón suave.'],
  [9.2, 14.7, '2', 'La aguja va al centro del frente, punta arriba', 'Está guardada encima de la caja, a ras.'],
  [15.2, 19.9, '', 'Dentro del panel hay un rotor con dos pestillos', 'Sus puntas entran 2 mm en el techo y en el suelo de la caja. El imán de la aguja arrastra al del rotor a través del panel.'],
  [20.2, 26.6, '3', 'Gira la aguja a la derecha hasta el tope', 'A partir de 23° las puntas salen de sus ranuras y el panel queda libre.'],
  [27.1, 32.2, '4', 'Tira de la aguja: el panel sale con ella', 'Dos imanes de esquina lo sujetan; la aguja agarra más fuerte.'],
  [32.7, 39.3, '5', 'Tira del reloj: sale con su pinza y su peana', 'Fuera de la caja hace de expositor.'],
  [39.8, 47.2, '', 'Para cerrar', 'Peana dentro hasta el clic, panel dentro con la aguja girada, aguja de vuelta y a su sitio.'],
  [47.8, 54.2, '', 'Si se pierde la aguja', 'Un clip por la ranura de la base empuja el pestillo de abajo y el panel sale igual.'],
  [54.9, 61.7, '', 'Nueve piezas impresas y ocho imanes embutidos', ''],
];

const etiquetas = [];
function etiqueta(texto, grupo, p, dx, dy) {
  const el = document.createElement('div'); el.className = 'et'; el.textContent = texto; document.getElementById('ui').appendChild(el);
  const ln = document.createElementNS('http://www.w3.org/2000/svg', 'line'); ln.setAttribute('stroke', '#22242a'); ln.setAttribute('stroke-width', '2');
  const pt = document.createElementNS('http://www.w3.org/2000/svg', 'circle'); pt.setAttribute('r', '5'); pt.setAttribute('fill', '#22242a');
  ui.lineas.append(ln, pt);
  etiquetas.push({ el, ln, pt, grupo, p: new THREE.Vector3(...p), dx, dy });
}
etiqueta('Funda', fundaG, [49.3, 10, 70], 80, -50);
etiqueta('Frase', fraseG, [-30, -8, 95.4], -90, -40);
etiqueta('Aguja', agujaG, [-16, 0, 2.6], 150, -10);
etiqueta('Caja', baseG, [47.8, 20, 20], 70, 70);
etiqueta('Panel', tapaG, [-43.8, -35.7, 30], -110, 50);
etiqueta('Rotor y muelle', rotG, [-4, -34, 70], -200, -30);
etiqueta('Tapa trasera', tapetaG, [-38, -31, 83.5], -150, -70);
etiqueta('Tarjeta', tarjetaG, [-30, -28.6, 73.8], -70, -120);
etiqueta('Pinza', upG, [18, 15, 83], 120, -75);
etiqueta('Reloj', upG, [23.5, -12, 48], 110, 0);
etiqueta('Peana', standG, [25, -10, 6], 100, 40);

// ------------------------------------------------------------ camara
const CAM = [
  [0, -34, 20, 450, -52, 0, 60], [4.4, -25, 22, 450, -42, 0, 60], [6.6, -20, 25, 520, -5, 0, 70], [9.0, -8, 30, 490, 5, 0, 40],
  [11.6, 20, 30, 470, 10, -15, 50], [14.6, 22, 20, 440, 0, -25, 40], [17.0, 26, 10, 405, 0, -30, 52], [20.5, 22, 9, 400, 0, -30, 52],
  [25.0, 14, 9, 400, 0, -30, 52], [27.2, 26, 22, 480, -15, -45, 46], [30.0, 24, 26, 570, -45, -60, 40], [32.5, 22, 26, 590, -45, -65, 38],
  [35.5, 30, 22, 570, -35, -75, 38], [37.6, 5, 18, 480, -5, -95, 42], [39.5, -18, 18, 480, -5, -90, 42], [41.0, 16, 24, 590, -40, -65, 40],
  [44.0, 20, 22, 480, 0, -30, 50], [47.4, 12, 26, 450, 0, -5, 54], [49.3, 16, -34, 390, 0, -20, 30], [53.4, 22, -36, 380, -5, -22, 28],
  [55.6, 50, 24, 960, 50, -90, 96], [58.5, 46, 25, 980, 50, -90, 100], [61.6, 43, 25, 980, 50, -90, 100], [64.4, -26, 22, 480, -50, 0, 62], [68, -32, 20, 450, -52, 0, 60],
];
function camAt(t) {
  let i = 0;
  while (i < CAM.length - 2 && CAM[i + 1][0] <= t) i++;
  const p1 = CAM[i], p2 = CAM[i + 1], p0 = CAM[Math.max(0, i - 1)], p3 = CAM[Math.min(CAM.length - 1, i + 2)];
  const h = p2[0] - p1[0], s = clamp((t - p1[0]) / h), s2 = s * s, s3 = s2 * s;
  const out = [];
  for (let j = 1; j < 7; j++) {
    const m1 = p2[0] === p0[0] ? 0 : (p2[j] - p0[j]) / (p2[0] - p0[0]), m2 = p3[0] === p1[0] ? 0 : (p3[j] - p1[j]) / (p3[0] - p1[0]);
    out.push((2 * s3 - 3 * s2 + 1) * p1[j] + (s3 - 2 * s2 + s) * h * m1 + (-2 * s3 + 3 * s2) * p2[j] + (s3 - s2) * h * m2);
  }
  return out;
}

// desplazamiento lateral y vertical del encuadre, en mm de escena: [derecha, arriba]
const ENC = [[0, 0, 0], [4.4, 0, 0], [6.6, 30, 10], [14.6, 30, 10], [17.0, 4, 22], [25.0, 4, 22], [27.2, 30, 10], [47.4, 30, 10], [49.3, 14, 12], [53.6, 14, 12], [55.6, 0, 26], [61.6, 0, 26], [64.4, 0, 0], [68, 0, 0]];
function encuadre(t) {
  let i = 0;
  while (i < ENC.length - 2 && ENC[i + 1][0] <= t) i++;
  const a = ENC[i], b = ENC[i + 1], x = k(t, a[0], b[0]);
  return [lerp(a[1], b[1], x), lerp(a[2], b[2], x)];
}

// ------------------------------------------------------------ linea de tiempo
const hEm = Ho / 2 - (D.zf + 1.0);
function thetaClip(xc) {
  const obj = xc - 0.5;
  if (obj >= D.hw) return 0;
  let a = 0, b = rad(60);
  for (let i = 0; i < 40; i++) { const m = (a + b) / 2; (D.hw / Math.cos(m) - hEm * Math.tan(m) > obj) ? (a = m) : (b = m); }
  return THREE.MathUtils.radToDeg((a + b) / 2);
}

function estado(t) {
  const s = {};
  s.funda = k(t, 4.9, 8.0) - k(t, 64.3, 66.4);
  s.fundaOp = clamp(1 - k(t, 6.8, 8.0) + k(t, 55.0, 56.2));
  s.a1 = k(t, 9.5, 10.3) - k(t, 46.5, 47.2);
  s.a2 = k(t, 10.3, 12.5) - k(t, 44.9, 46.5);
  s.a3 = k(t, 12.5, 13.1) - k(t, 44.4, 44.9);
  s.x = k(t, 15.3, 16.8) - k(t, 25.0, 26.6);
  s.x2 = k(t, 47.8, 49.0) - k(t, 53.7, 54.7);
  s.clipSube = k(t, 49.3, 50.1) - k(t, 53.5, 54.2);
  s.clipX = D.hw + 1 + (-21.6 - (D.hw + 1)) * k(t, 50.3, 52.4);
  s.clipVis = t > 49.2 && t < 54.25;
  const thE = thetaClip(s.clipX) * (1 - k(t, 53.5, 54.3)) * (t > 50.2 ? 1 : 0);
  s.theta = P.rotor_giro * (k(t, 20.6, 24.4) - k(t, 43.0, 44.2)) + thE;
  s.pa = k(t, 27.5, 29.2) - k(t, 42.0, 42.9);
  s.pb = k(t, 29.5, 31.8) - k(t, 40.9, 42.0);
  s.empuje = k(t, 52.6, 53.1) - k(t, 53.5, 54.2);
  s.st = k(t, 33.2, 35.6) - k(t, 39.8, 40.9);
  s.e = k(t, 55.0, 57.6) - k(t, 61.8, 64.2);
  return s;
}

const cPanel = new THREE.Vector3(0, -Do / 2 + P.tapa_alto / 2 + 1, Ho / 2);
const cAmbar = new THREE.Color(COL.ambar), cVerde = new THREE.Color(COL.verde);
const tmpV = new THREE.Vector3();

window.renderAt = function (t) {
  const s = estado(t);
  const th = s.theta;
  // funda
  fundaG.position.z = (t < 54.9 ? 150 : 132) * s.funda;
  setOp(funda, s.fundaOp); setOp(frase, s.fundaOp);
  fraseG.position.z = 18 * s.e;
  // fantasma
  const xr = Math.max(s.x, s.x2);
  setOp(base, 1 - 0.83 * xr);
  setOp(tapa, 1 - 0.76 * xr);
  setOp(tapeta, 1 - xr); setOp(tarjeta, 1 - xr);
  setOp(peana, 1 - xr); setOp(pinza, 1 - xr); setOp(reloj, 1 - xr);
  setOp(aguja, 1 - 0.3 * s.x);
  matIman.opacity = xr; matIman.depthWrite = xr > 0.99;
  for (const g of [baseL, tapaL]) g.visible = xr > 0.01;
  pivote.children[1].visible = xr > 0.01; agujaG.children[1].visible = agujaG.children[2].visible = xr > 0.01;
  suelo.material.opacity = 0.2 * (1 - s.x2);
  // rotor y muelle
  pivote.rotation.z = -rad(th);
  ponMuelle(th);
  const libre = clamp((th - 21) / 4);
  rotor.userData.mesh.material.color.copy(cAmbar).lerp(cVerde, libre);
  matMuelle.color.copy(rotor.userData.mesh.material.color);
  // panel: sale recto y luego se tumba a la izquierda
  const off = new THREE.Vector3(0, -70 * s.pa - 10 * s.empuje, 0).lerp(new THREE.Vector3(-118, -40.5, 4.4 - Ho / 2), s.pb);
  off.z += 26 * Math.sin(Math.PI * s.pb);
  panelG.matrix.makeTranslation(cPanel.x + off.x, cPanel.y + off.y, cPanel.z + off.z)
    .multiply(new THREE.Matrix4().makeRotationX(-Math.PI / 2 * s.pb))
    .multiply(new THREE.Matrix4().makeTranslation(-cPanel.x, -cPanel.y, -cPanel.z));
  tapaG.position.y = -180 * s.e; rotG.position.y = -128 * s.e; tapetaG.position.y = -86 * s.e; tarjetaG.position.y = -46 * s.e;
  // peana
  standG.position.set(150 * s.e, -100 * s.st - 25 * s.e, 0);
  upG.position.z = 64 * s.e;
  // aguja
  const sth = Math.sin(rad(th)), cth = Math.cos(rad(th));
  const mF = panelG.matrix.clone().multiply(mPose({ o: new THREE.Vector3(0, -Do / 2, Ho / 2), u: new THREE.Vector3(sth, 0, cth), v: new THREE.Vector3(-cth, 0, sth), w: new THREE.Vector3(0, -1, 0) }));
  const pS = poseGuardada.o.clone(); pS.z += 15 * s.e;
  const qS = new THREE.Quaternion().setFromRotationMatrix(mPose(poseGuardada));
  const pF = new THREE.Vector3(), qF = new THREE.Quaternion(), sc = new THREE.Vector3();
  mF.decompose(pF, qF, sc);
  const A = pS.clone().add(new THREE.Vector3(0, 0, 20)), B = pF.clone().add(new THREE.Vector3(0, -24, 0).applyQuaternion(new THREE.Quaternion().setFromRotationMatrix(panelG.matrix)));
  const p1 = pS.clone().lerp(A, s.a1), p2 = B.clone().lerp(pF, s.a3);
  const pos = p1.lerp(p2, s.a2);
  pos.z += 34 * Math.sin(Math.PI * s.a2); pos.y -= 30 * Math.sin(Math.PI * s.a2);
  agujaG.matrix.compose(pos, qS.clone().slerp(qF, s.a2), new THREE.Vector3(1, 1, 1));
  // clip
  clip.visible = s.clipVis;
  clip.position.set(s.clipX, ye - 10 * s.empuje, D.zf + 1.5 - 23 - 60 * (1 - s.clipSube));
  // camara
  const [az, el, dist, tx, ty, tz] = camAt(t);
  const ca = rad(az), ce = rad(el);
  camera.position.set(tx + dist * Math.sin(ca) * Math.cos(ce), ty - dist * Math.cos(ca) * Math.cos(ce), tz + dist * Math.sin(ce));
  camera.lookAt(tx, ty, tz);
  camera.updateMatrixWorld();
  const dR = encuadre(t);
  camera.position.addScaledVector(new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0), -dR[0]).addScaledVector(new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1), -dR[1]);
  scene.updateMatrixWorld(true);
  renderer.render(scene, camera);
  // rotulos
  ui.titulo.style.opacity = k(t, 0.3, 1.1) * (1 - k(t, 3.6, 4.3));
  ui.fin.style.opacity = k(t, 65.4, 66.4);
  let op = 0;
  for (const [a, b, n, h, sub] of PASOS) {
    if (t >= a && t <= b) {
      op = k(t, a, a + 0.4) * (1 - k(t, b - 0.4, b));
      pasoN.textContent = n; pasoN.style.display = n ? 'flex' : 'none'; pasoH.textContent = h; pasoS.textContent = sub; pasoS.style.display = sub ? 'block' : 'none';
    }
  }
  ui.paso.style.opacity = op;
  ui.estado.style.opacity = xr;
  const esLibre = th >= 23;
  estP.textContent = esLibre ? 'PANEL LIBRE' : 'PESTILLO ECHADO';
  estP.style.background = esLibre ? '#2f9e6e' : '#dd8a1c';
  estG.textContent = (s.x2 > 0.01 ? 'giro del rotor: ' : 'giro de la aguja: ') + Math.round(th) + '°';
  for (const q of etiquetas) {
    tmpV.copy(q.p).applyMatrix4(q.grupo.matrixWorld).project(camera);
    const x = (tmpV.x + 1) / 2 * W, y = (1 - tmpV.y) / 2 * H, lx = x + q.dx, ly = y + q.dy;
    q.el.style.opacity = s.e; q.ln.style.opacity = s.e; q.pt.style.opacity = s.e;
    if (q.dx > 0) { q.el.style.left = (lx + 8) + 'px'; q.el.style.right = ''; } else { q.el.style.left = ''; q.el.style.right = (W - lx + 8) + 'px'; }
    q.el.style.top = ly + 'px';
    q.ln.setAttribute('x1', x); q.ln.setAttribute('y1', y); q.ln.setAttribute('x2', lx); q.ln.setAttribute('y2', ly);
    q.pt.setAttribute('cx', x); q.pt.setAttribute('cy', y);
  }
  return true;
};

await document.fonts.load('60px "Instrument Serif"'); await document.fonts.load('600 40px "Instrument Sans"'); await document.fonts.load('40px "Instrument Sans"'); await document.fonts.load('500 40px "Instrument Sans"'); await document.fonts.load('40px "Reenie Beanie"');
await document.fonts.ready;
window.renderAt(0);
window.listo = true;
