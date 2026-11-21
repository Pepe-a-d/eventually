# Lo que quedo sin hacer de a4 (funda, piezas de probeta) y unas medidas sueltas
import sys, zipfile
import xml.etree.ElementTree as ET
from comun import *
def libre(f, paso, tope, umbral=0.02):
    x = paso
    while x <= tope + 1e-9:
        if f(x) > umbral: return x - paso
        x += paso
    return float('inf')
fm = lambda v: ('%.2f mm' % v) if v < 1e9 else 'NADA LO PARA'
print('=== funda')
for a in (90, 180, 270):
    print('  funda girada %d grados: pisa %.1f mm3 al cuerpo' % (a, vol(S['funda'].rotate([0, 0, a]), S['cuerpo'])))
print('  funda con la caja ABIERTA: pisa puertas %.1f mm3 y reloj %.1f mm3 (solo cabe cerrada)' % (vol(S['funda'], puerta(1, 90)) + vol(S['funda'], puerta(-1, 90)), vol(S['funda'], puesta('reloj_de_pega', G))))
print('=== bisel y cuerpo: holgura minima %.3f mm ; bisel y plato %.3f ; bisel y rueda central %.3f ; bisel y tubo %.3f' % (S['bisel'].min_gap(S['cuerpo'], 5), S['bisel'].min_gap(S['plato'], 5), S['bisel'].min_gap(S['rueda_central'], 5), S['bisel'].min_gap(S['tubo'], 5)))
print('=== boca abajo, soporte + reloj juntos (van sueltos sobre el pedestal)')
grupo = S['soporte'] + S['reloj_de_pega']
otros = [S[n] for n in CAJA if n not in ('soporte', 'reloj_de_pega')]
print('  caja cerrada: suben %s hasta dar con algo (las puertas, por dentro)' % fm(libre(lambda e: sum(vol(grupo.translate([0, 0, e]), o) for o in otros), 0.1, 30.0)))
otrosG = [puesta(n, G) for n in CAJA if n not in ('soporte', 'reloj_de_pega')]; grupoG = puesta('soporte', G) + puesta('reloj_de_pega', G)
print('  caja abierta: suben %s' % fm(libre(lambda e: sum(vol(grupoG.translate([0, 0, e]), o) for o in otrosG), 0.5, 30.0)))
print('=== tetones en la helice: holgura real')
for tau_ in (150.0, 200.0, 250.0):
    pf = puesta('plataforma', tau_); tu = puesta('tubo', tau_)
    for umb in (0.02, 0.002):
        ab = libre(lambda e: vol(pf.translate([0, 0, -e]), tu), 0.005, 1.0, umb); ar = libre(lambda e: vol(pf.translate([0, 0, e]), tu), 0.005, 1.0, umb)
        print('  tau %g, umbral %.3f mm3: baja %.3f y sube %.3f mm' % (tau_, umb, ab, ar))
alfa = math.atan(d['rampa_paso'] / (2 * math.pi * p['tubo_r'])); hv0 = p['teton_plat_d'] / 2 + p['holg_desliza']
print('  cuenta: la ranura mide %.2f mm de media altura EN VERTICAL; perpendicular a la rampa (%.1f grados en la boca) son %.3f; el teton mide %.2f de radio -> holgura %.3f mm por lado (no %.2f)' % (hv0, math.degrees(alfa), hv0 * math.cos(alfa), p['teton_plat_d'] / 2, hv0 * math.cos(alfa) - p['teton_plat_d'] / 2, p['holg_desliza']))
print('=== tubo: pared entre la helice de una ranura y el tramo plano de la siguiente (por encima del tramo plano de abajo)')
tu = S['tubo']; zc0 = d2['zc0']
for r_ in (76.05, 77.0):
    peor = (9e9, 0, 0)
    for a in np.arange(0, 360, 1.0):
        col = caja(r_, -0.05, -130, r_ + 0.1, 0.05, 0).rotate([0, 0, float(a)])
        for t in (tu ^ col).decompose():
            if t.volume() < 1e-6: continue
            z0, z1 = bb(t)[2], bb(t)[5]
            if z0 > zc0 + 0.5 and z1 < d['z_plato0'] - 0.5 and z1 - z0 < peor[0]: peor = (z1 - z0, float(a), z0)
    print('  a r=%.2f: pared mas corta %.2f mm (angulo %g, z %.2f a %.2f). La fase 1 dice "queda 3.7 de pared"' % (r_, peor[0], peor[1], peor[2], peor[2] + peor[0]))
print('=== piezas de la probeta de puertas (el autor no las mete en ningun barrido)')
an = S['probeta_anillo']; tp = S['probeta_teton']; peor = {}
for tau_ in np.arange(0, 101, 1.0):
    s_, psi, ang, h = D.movimiento(p, d, float(tau_)); tpm = tp.translate([0, -s_, 0])
    for q in ('marco', 'meseta', 'aro_puertas', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo'):
        m = puesta(q, float(tau_))
        for nom, o in (('anillo', an), ('teton_pomo', tpm)):
            v = vol(o, m)
            if v > peor.get((nom, q), (0, 0))[0]: peor[(nom, q)] = (v, float(tau_))
    v = vol(an, tpm)
    if v > peor.get(('anillo', 'teton_pomo'), (0, 0))[0]: peor[('anillo', 'teton_pomo')] = (v, float(tau_))
print('  parejas que se pisan (tau 0..100):', {k: (round(v[0], 3), v[1]) for k, v in peor.items() if v[0] > 1e-4} or 'ninguna')
tp13 = tp.translate([0, -p['teton_recorrido'], 0])
print('  teton con pomo: distancia a la meseta %.2f (cerrado) / %.2f (abierto); al anillo %.2f / %.2f; al marco %.2f / %.2f' % (tp.min_gap(S['meseta'], 30), tp13.min_gap(S['meseta'], 30), tp.min_gap(an, 30), tp13.min_gap(an, 30), tp.min_gap(S['marco'], 30), tp13.min_gap(S['marco'], 30)))
for nom, o, aro in (('cerrado', tp, puesta('aro_puertas', 0)), ('abierto', tp13, puesta('aro_puertas', G))):
    print('  probeta boca abajo, teton con pomo (%s): sube %s' % (nom, fm(libre(lambda e: vol(o.translate([0, 0, e]), S['meseta']) + vol(o.translate([0, 0, e]), an) + vol(o.translate([0, 0, e]), aro) + vol(o.translate([0, 0, e]), S['marco']), 0.1, 30.0))))
    bo = bb(o); print('     (el vastago mide de z %.2f a %.2f; la ranura del marco llega hasta z %.2f y el aro hasta %.2f)' % (bo[2], d['z_corr1'] + 0.61, d['z_ala1'], d['z_corr1']))
print('  anillo boca abajo: sube %s' % fm(libre(lambda e: sum(vol(an.translate([0, 0, e]), S[q]) for q in ('meseta', 'marco', 'pasador_derecho', 'puerta_derecha')), 0.1, 30.0)))
print('  marco de la probeta boca abajo (sin base): sube %s contra meseta y pasadores' % fm(libre(lambda e: sum(vol(S['marco'].translate([0, 0, -e]), S[q]) for q in ('meseta', 'pasador_derecho', 'pasador_izquierdo', 'aro_puertas')), 0.1, 30.0)))
print('  el teton con pomo pisa al plato %.1f mm3 y a la rueda central %.1f: con el puesto no se monta la probeta 3' % (vol(tp, S['plato']), vol(tp, S['rueda_central'])))
print('  pasadores en la probeta, con el anillo: corren %s' % fm(libre(lambda e: vol(S['pasador_derecho'].translate([0, e, 0]), an) + vol(S['pasador_derecho'].translate([0, e, 0]), S['meseta']), 0.05, 20)))
print('=== ficheros 3mf: detalles')
NS = '{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
def lee(fn):
    root = ET.fromstring(zipfile.ZipFile(fn).read('3D/3dmodel.model')); out = []
    for ob in root.iter(NS + 'object'):
        me = ob.find(NS + 'mesh')
        out.append((np.array([[float(q.get('x')), float(q.get('y')), float(q.get('z'))] for q in me.find(NS + 'vertices')]), np.array([[int(q.get('v1')), int(q.get('v2')), int(q.get('v3'))] for q in me.find(NS + 'triangles')])))
    return out
R = '<repositorio>/caja/probetas-v5/'
A = lee(R + 'caja-probeta-puertas-bandeja-A.3mf'); v, t = A[5]
r_abajo = np.hypot(*(v[v[:, 2] < 0.5][:, :2] - v[:, :2].mean(0)).T).max(); r_arriba = np.hypot(*(v[v[:, 2] > v[:, 2].max() - 0.5][:, :2] - v[:, :2].mean(0)).T).max()
print('  teton con pomo en la bandeja A: radio en la cama %.2f, radio arriba %.2f -> %s' % (r_abajo, r_arriba, 'vastago abajo y pomo arriba: el pomo vuela 2,5 mm todo alrededor' if r_abajo < r_arriba else 'pomo en la cama'))
B = lee(R + 'caja-probeta-puertas-bandeja-B.3mf')
ms = [mf.Manifold(mf.Mesh(vert_properties=np.asarray(v, dtype=np.float32), tri_verts=np.asarray(t, dtype=np.uint32))) for v, t in B]
print('  bandeja B: distancias entre cuerpos: meseta-aro %.2f, meseta-anillo %.2f, aro-anillo %.2f mm; se pisan aro y anillo %.3f mm3' % (ms[0].min_gap(ms[1], 50), ms[0].min_gap(ms[2], 50), ms[1].min_gap(ms[2], 50), vol(ms[1], ms[2])))
for i, (v, t) in enumerate(B): print('     cuerpo %d: x %.1f..%.1f y %.1f..%.1f' % (i + 1, v[:, 0].min(), v[:, 0].max(), v[:, 1].min(), v[:, 1].max()))
import trimesh
for f in ('caja-probeta-ascensor-tubo.3mf', 'caja-probeta-ascensor-plataforma.3mf'):
    v, t = lee(R + f)[0]
    for proc in (False, True):
        m = trimesh.Trimesh(v, t, process=proc)
        e = np.sort(m.edges, axis=1); u, cnt = np.unique(e, axis=0, return_counts=True)
        sueltas = u[cnt == 1]; L = np.linalg.norm(m.vertices[sueltas[:, 0]] - m.vertices[sueltas[:, 1]], axis=1) if len(sueltas) else np.array([0.0])
        print('  %s (fusionando vertices: %s): %d vertices, %d caras; aristas con 1 cara %d (largo total %.2f mm, la mayor %.3f), con mas de 2 caras %d; z de las sueltas %.1f..%.1f' % (f, proc, len(m.vertices), len(m.faces), int((cnt == 1).sum()), L.sum(), L.max(), int((cnt > 2).sum()), m.vertices[sueltas.ravel()][:, 2].min() if len(sueltas) else 0, m.vertices[sueltas.ravel()][:, 2].max() if len(sueltas) else 0))
