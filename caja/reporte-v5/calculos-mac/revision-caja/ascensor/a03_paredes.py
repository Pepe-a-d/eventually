# 3. Pared que queda entre las ranuras del tubo (angulos reales 90, 212, 330), con la cara exterior y con el canto de abajo
from comun import *
from shapely.geometry import Polygon
ops = P['tubo'].ops
for i, o in enumerate(ops): print(i, o['t'], o['op'], {k: v for k, v in o.items() if k in ('c0', 'c1', 'a0', 'a1', 'z0', 'z1', 'giro')})
anillo = CP.solido([{'t': 'prisma', 'eje': 'z', 'c0': -130, 'c1': 0, 'pol': CP.geo(CP.corona(p['tubo_r'], d['tubo_r_ext'])), 'op': '+'}])
cort = {}
i0 = [i for i, o in enumerate(ops) if o['t'] == 'revol' and o['op'] == '-'][0]
for k in range(3):
    b = i0 + 4 * k
    for nombre, o in zip(('plano_abajo', 'plano_arriba', 'helice', 'entrada'), ops[b:b + 4]):
        o2 = dict(o); o2['op'] = '+'
        cort[(k + 1, nombre)] = CP.solido([o2]) ^ anillo
        print(k + 1, nombre, bb(cort[(k + 1, nombre)]))
claves = list(cort)
print('\nPared entre cortes de ranuras DISTINTAS (distancia minima entre los huecos, dentro de la pared del tubo):')
res = []
for i, a in enumerate(claves):
    for b in claves[i + 1:]:
        if a[0] == b[0]: continue
        g = cort[a].min_gap(cort[b], 12.0)
        if g < 12.0: res.append((g, a, b))
for g, a, b in sorted(res): print('   %.3f mm  ranura %d %s  /  ranura %d %s' % (g, a[0], a[1], b[0], b[1]))
# donde esta el minimo: se busca por angulo
def donde_min(a, b, g):
    A, B = cort[a], cort[b]
    mejor = None
    for ang in np.arange(0, 360, 1.0):
        cuna = CP.solido([{'t': 'revol', 'perfil': [[70, -125], [85, -125], [85, -5], [70, -5]], 'a0': ang, 'a1': ang + 1.0, 'op': '+'}])
        a_, b_ = A ^ cuna, B ^ cuna
        if a_.volume() > 0 and b_.volume() > 0:
            gg = a_.min_gap(b_, g + 0.3)
            if mejor is None or gg < mejor[0]: mejor = (gg, ang, bb(a_), bb(b_))
    return mejor
for g, a, b in sorted(res)[:4]:
    print('   minimo de', a, b, '->', donde_min(a, b, g))
print('\nCara exterior del tubo: radio maximo de los cortes y pared que queda')
for kx in claves:
    m = cort[kx].to_mesh(); v = np.array(m.vert_properties)[:, :3]
    r = np.hypot(v[:, 0], v[:, 1])
    print('   ranura %d %-12s r max %.3f -> pared exterior %.3f mm ; z min %.3f -> sobre el canto de abajo (z_t0 = %.2f): %.3f mm ; z max %.3f -> bajo el canto de arriba (%.2f): %.3f' % (kx[0], kx[1], r.max(), d['tubo_r_ext'] - r.max(), v[:, 2].min(), d['z_suelo'] + 0.6, v[:, 2].min() - (d['z_suelo'] + 0.6), v[:, 2].max(), d['z_plato0'], d['z_plato0'] - v[:, 2].max()))
# seccion de la pared bajo el plano de abajo: grosor en funcion del radio
print('\nBajo el tramo plano de abajo, material del tubo entre el suelo de la V y el canto de abajo (z_t0):')
zc0 = d2['zc0']
for r in (76.0, 76.5, 77.0, 78.0, 78.9):
    hv = 3.25 - (r - 76.0) * (3.25 - 0.65) / (78.9 - 76.0)
    print('   r = %.1f: %.2f mm' % (r, zc0 - hv - (d['z_suelo'] + 0.6)))
# lo que dice la comprobacion del autor frente a lo real
k_h = d['recorrido'] / (p['giro_arriba'] - p['giro_sube'])
print('\nAutor (caja_diseno_v5, comprobacion 6): supone 120 grados entre ranuras y plano que empieza justo en la siguiente:')
print('   sube_al_cruce - ranura_alto = %.2f mm' % (d['recorrido'] * (120.0 - p['giro_sube']) / (p['giro_arriba'] - p['giro_sube']) - d['ranura_alto']))
for sep, quien in ((122.0, 'helice 1 / plano 2'), (118.0, 'helice 2 / plano 3'), (120.0, 'helice 3 / plano 1')):
    print('   real, %s (separacion %.0f, el plano empieza 3 grados antes y es 0.05 mas alto): en la boca %.2f mm' % (quien, sep, (sep - 3.0 - p['giro_sube']) * k_h - 3.2 - 3.25))
