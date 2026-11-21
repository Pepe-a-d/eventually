# 2. Requisitos del brief medidos en el modelo
from comun import *
from shapely.geometry import Polygon, box as sbox, MultiPolygon
from shapely.ops import unary_union
def cs2shp(cs):
    out = []
    for q in cs.to_polygons():
        if len(q) >= 3: out.append(Polygon(q))
    # EvenOdd: componer por paridad
    out.sort(key=lambda g: -g.area); res = None
    for g in out:
        g = g.buffer(0)
        res = g if res is None else res.symmetric_difference(g)
    return res if res is not None else Polygon()
hx, hy = d['hueco_x']/2, d['hueco_y']/2
print('=== A. junta del centro, puertas cerradas: lineas de vision verticales')
pd_, pi_ = S['puerta_derecha'], S['puerta_izquierda']
proy = cs2shp((pd_ + pi_).project())
rect = sbox(-d['eje_x'] + 0.5, -d['puerta_y']/2 + 0.2, d['eje_x'] - 0.5, d['puerta_y']/2 - 0.2)
hue = rect.difference(proy)
for g in (hue.geoms if hasattr(hue, 'geoms') else [hue]):
    if g.area > 1e-6: print('  AGUJERO pasante entre las dos puertas: bbox x %.3f..%.3f  y %.3f..%.3f  area %.4f mm2' % (g.bounds[0], g.bounds[2], g.bounds[1], g.bounds[3], g.area))
if hue.area < 1e-6: print('  sin agujero pasante entre las puertas')
# y debajo de ese agujero, que hay con la caja cerrada?
col = caja(-0.14, -0.55, -200, 0.14, 0.55, 5)
for n in CAJA:
    v = vol(col, puesta(n, 0))
    if v > 1e-6: print('   bajo el agujero (columna 0.28 x 1.1): %s  z max %.2f' % (n, bb(col ^ puesta(n,0))[5]))
# raya junto a bisagra y extremos: proyeccion puertas + meseta
proy2 = cs2shp((pd_ + pi_ + S['meseta']).project())
hue2 = sbox(-40, -40, 40, 40).difference(proy2)
print('  puertas + meseta, agujeros pasantes en +-40: area %.4f' % hue2.area, [tuple(round(v,2) for v in g.bounds) for g in (hue2.geoms if hasattr(hue2,'geoms') else [hue2]) if g.area>1e-6])
for z in (-0.05, -1.0, -2.4, -4.0, -4.9):
    a = cs2shp(pd_.slice(z)); b = cs2shp(pi_.slice(z))
    print('  z=%.2f: distancia entre puertas %.3f ; x max izq %.3f, x min der %.3f' % (z, a.distance(b), b.bounds[2], a.bounds[0]))
# canto en la mitad del rebaje
c = pd_ ^ caja(-1, -30, -6, 3, -5, 1); print('  mitad del rebaje (y<0), puerta derecha: z min en x<0.3 -> %.2f ; grueso del canto %.2f' % (bb(pd_ ^ caja(0.1, -30, -6, 0.3, -5, 1))[2], -bb(pd_ ^ caja(0.1, -30, -6, 0.3, -5, 1))[2]))

print('=== B. hueco libre 50 x 59 con las puertas abiertas (tau = 345)')
prisma = caja(-hx, -hy, d['z_ala0'], hx, hy, 60)
for n in CAJA:
    if n in ('plataforma', 'soporte', 'reloj_de_pega'): continue
    v = vol(prisma, puesta(n, G))
    if v > 1e-6: print('  ENTRA en el prisma (nominal): %s %.3f mm3' % (n, v))
print('  nominal: distancia minima del prisma a cada puerta: %.3f / %.3f' % (prisma.min_gap(puesta('puerta_derecha', G), 5), prisma.min_gap(puesta('puerta_izquierda', G), 5)))
for ang in (90, 89, 88.5, 88, 87, 86.25):
    a = puerta(1, ang); v = vol(prisma, a); c = prisma ^ a
    print('  puerta derecha a %.2f grados: entra %.2f mm3; x min dentro del prisma %s' % (ang, v, ('%.2f (se mete %.2f mm)' % (bb(c)[0], hx - bb(c)[0])) if v > 1e-6 else '-'))
taco = caja(-hx, -hy, -5, hx, hy, 40)
print('  taco de 50 x 59 entre las puertas a 90: pisa %.3f mm3; a 86.25: %.3f mm3' % (vol(taco, puerta(1,90)) + vol(taco, puerta(-1,90)), vol(taco, puerta(1,86.25)) + vol(taco, puerta(-1,86.25))))

print('=== C. reloj y soporte: distancias reales (paso 1 grado, radio de busqueda 30)')
pares = {}
objs = ['puerta_derecha', 'puerta_izquierda', 'meseta', 'marco', 'rueda_central', 'aro_puertas', 'pasador_derecho', 'pasador_izquierdo', 'plato', 'bisel', 'satelite_1', 'teton']
for tau in np.arange(0, G + 0.01, 1.0):
    M = {n: puesta(n, tau) for n in objs + ['reloj_de_pega', 'soporte']}
    for a in ('reloj_de_pega', 'soporte'):
        for b in objs:
            g = M[a].min_gap(M[b], 30.0)
            if g < pares.get((a, b), (9e9, 0))[0]: pares[(a, b)] = (g, tau)
for k, v in sorted(pares.items(), key=lambda kv: kv[1][0]): print('  %-14s %-18s %.3f mm (tau %g)' % (k[0], k[1], v[0], v[1]))
# con el juego declarado de las puertas (86.25 grados)
peor = (9e9, 0)
for tau in np.arange(84, G + 0.01, 1.0):
    for a in ('reloj_de_pega', 'soporte'):
        for sx in (1, -1):
            g = puesta(a, tau).min_gap(puerta(sx, 86.25), 10.0)
            if g < peor[0]: peor = (g, tau, a, sx)
print('  con la puerta inclinada a 86.25 (juego declarado): lo mas cerca %.3f mm' % peor[0], peor[1:])
for ang in (89, 88, 87):
    g = min(puesta('reloj_de_pega', tau).min_gap(puerta(1, ang), 10.0) for tau in np.arange(84, G + 0.01, 2.0)); print('     puerta a %g: reloj a %.3f' % (ang, g))

print('=== D. imanes: distancia a la cabeza del reloj')
rel = P['reloj_de_pega']
cabeza = CP.solido(rel.ops[1:2]); corona = CP.solido(rel.ops[2:3]); print('  cabeza bbox', [round(v,2) for v in bb(cabeza)], ' corona', [round(v,2) for v in bb(corona)])
cab = cabeza + corona
z_p = d['z_disco1_abajo'] + d['pedestal_alto']
L = d['cuerpo_lado']/2; c_im = L - 9.0; z_pie = d['z_cuerpo_arriba'] + 0.6
z_t0 = d['z_suelo'] + 0.6; z_im0 = z_t0 + 9.4; r_im = d['tubo_r_ext'] + 0.3; r_or1 = d['tubo_r_ext'] + 5.3
gi = math.degrees((0.7 + 0.875) / (d['tubo_r_ext'] + 2.8)); a_tope = 45.0; a_or = a_tope - 7.5
def iman_canto(a):  # 5 x 1.6, de canto en la ranura radial
    return mf.Manifold.cylinder(1.6, 2.5, 2.5, 48).translate([0,0,-0.8]).rotate([90,0,0]).translate([r_im + 2.5, 0, z_im0 + 2.5]).rotate([0,0,a])
IM = {'soporte': (mf.Manifold.cylinder(1.6, 2.5, 2.5, 48).translate([0, 12, z_p]), 'plataforma'),
      'pedestal': (mf.Manifold.cylinder(1.6, 2.5, 2.5, 48).translate([0, 12, z_p - 1.6]), 'plataforma'),
      'tubo_1': (iman_canto(a_or + (3.5 - gi)), 'tubo'), 'tubo_2': (iman_canto(a_or - (3.5 - gi)), 'tubo'),
      'base_1': (iman_canto(a_tope + (4 - gi)), 'fijo'), 'base_2': (iman_canto(a_tope - (4 - gi)), 'fijo'),
      'cuerpo_1': (mf.Manifold.cylinder(1.6, 2.5, 2.5, 48).translate([c_im, c_im, d['z_cuerpo_arriba'] - 1.2 - 1.6]), 'fijo'), 'cuerpo_2': (mf.Manifold.cylinder(1.6, 2.5, 2.5, 48).translate([-c_im, -c_im, d['z_cuerpo_arriba'] - 1.2 - 1.6]), 'fijo'),
      'funda_1': (mf.Manifold.cylinder(1.6, 2.5, 2.5, 48).translate([c_im, c_im, z_pie + 0.2]), 'fijo'), 'funda_2': (mf.Manifold.cylinder(1.6, 2.5, 2.5, 48).translate([-c_im, -c_im, z_pie + 0.2]), 'fijo')}
# cada iman esta dentro de su cajera? (no pisa la pieza)
duenos = {'soporte': 'soporte', 'pedestal': 'plataforma', 'tubo_1': 'tubo', 'tubo_2': 'tubo', 'base_1': 'base', 'base_2': 'base', 'cuerpo_1': 'cuerpo', 'cuerpo_2': 'cuerpo', 'funda_1': 'funda', 'funda_2': 'funda'}
for n, (m, mu) in IM.items(): print('  iman %-9s pisa su pieza %.3f mm3 (0 = cabe en la cajera); bbox %s' % (n, vol(m, S[duenos[n]]), [round(v,1) for v in bb(m)]))
for n, (m, mu) in IM.items():
    peor = (9e9, 0)
    for tau in np.arange(0, G + 0.01, 1.0):
        mm = CP.mover(m, n, mu, p, d, tau); cc = CP.mover(cab, 'c', 'plataforma', p, d, tau); c2 = CP.mover(cabeza, 'c', 'plataforma', p, d, tau)
        g = mm.min_gap(cc, 400.0)
        if g < peor[0]: peor = (g, tau, mm.min_gap(c2, 400.0))
    print('  iman %-9s a la cabeza (con corona): min %.2f mm (tau %g); a la cabeza sin corona %.2f; reloj abajo %.2f; arriba %.2f' % (n, peor[0], peor[1], peor[2], m.min_gap(cab, 400), CP.mover(m, n, mu, p, d, G).min_gap(CP.mover(cab, 'c', 'plataforma', p, d, G), 400)))
print('  pareja tubo-base cerrado: %.2f mm ; abierto: %.2f mm' % (min(IM['tubo_%d'%i][0].min_gap(IM['base_%d'%j][0], 50) for i in (1,2) for j in (1,2)), min(IM['tubo_%d'%i][0].rotate([0,0,-G]).min_gap(IM['base_%d'%j][0], 50) for i in (1,2) for j in (1,2))))
print('  pareja cuerpo-funda: %.2f mm ; pedestal-soporte %.2f' % (IM['cuerpo_1'][0].min_gap(IM['funda_1'][0], 20), IM['soporte'][0].min_gap(IM['pedestal'][0], 20)))

print('=== E. pedestal arriba: rendijas a ras (tau = 345)')
M = {n: puesta(n, G) for n in CAJA if n not in ('reloj_de_pega', 'soporte')}
for z in (-0.05, -2.5, -4.9, -5.1, -7.9):
    todo = None
    for n, m in M.items():
        g = cs2shp(m.slice(z))
        if n == 'plataforma': ped = g
        elif not g.is_empty: todo = g if todo is None else todo.union(g)
    libre = sbox(-45, -45, 45, 45).difference(todo).difference(ped)
    # el trozo de hueco conectado al pedestal
    con = [g for g in (libre.geoms if hasattr(libre, 'geoms') else [libre]) if g.distance(ped) < 0.01 and g.area > 0.01]
    u = unary_union(con) if con else Polygon()
    print('  z=%.2f: pedestal %s ; hueco libre pegado al pedestal: area %.1f mm2, bbox %s' % (z, tuple(round(v,2) for v in ped.bounds), u.area, tuple(round(v,2) for v in u.bounds) if con else '-'))
    if con:
        # rendija en +X, -X, +Y, -Y medida por el centro
        from shapely.geometry import LineString
        for nom, ln in (('+X', LineString([(0, 0), (60, 0)])), ('+Y', LineString([(0, 0), (0, 60)])), ('-Y', LineString([(0, 0), (0, -60)])), ('+Y en x=20', LineString([(20, 0), (20, 60)]))):
            s_ = ln.intersection(u); print('      rendija %s: %.2f mm' % (nom, s_.length))
