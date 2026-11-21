# 5. Arriba del todo: pedestal a ras, rendija con marco y meseta, disco contra el ala, y cabeceo con los juegos reales
from comun import *
G = p['giro_tubo']
UMB = 1e-3
for tau in (335.0, 340.0, G):
    pl = puesta('plataforma', tau)
    b = pl.bounding_box()
    print('tau %.0f: cara de arriba del pedestal z = %.4f ; disco de z = %.2f a %.2f ; ala del marco de %.2f a %.2f -> el disco queda %.2f por debajo del ala' % (tau, b[5], d['z_disco0_abajo'] + 88, d['z_disco1_abajo'] + 88, d['z_ala0'], d['z_ala1'], d['z_ala0'] - (d['z_disco1_abajo'] + 88)))
    for o in ('marco', 'meseta', 'aro_puertas', 'puerta_derecha', 'puerta_izquierda', 'base', 'tubo', 'plato', 'teton', 'rueda_central'):
        print('     plataforma - %-16s vol %.4f  dist min %.3f' % (o, vol(pl, puesta(o, tau)), gap(pl, puesta(o, tau), 3.0)))
# seccion: rendija alrededor del pedestal a varias alturas
pl = puesta('plataforma', G)
for z in (-0.5, -4.0, -8.5, -12.0, -17.0, -20.0):
    fila = []
    for o in ('marco', 'meseta', 'aro_puertas', 'puerta_derecha'):
        A = puesta(o, G)
        reb = mf.Manifold.cube([400, 400, 0.2]).translate([-200, -200, z - 0.1])
        a_, b_ = pl ^ reb, A ^ reb
        fila.append('%s %.3f' % (o, a_.min_gap(b_, 5.0)) if (a_.volume() > 0 and b_.volume() > 0) else '%s -' % o)
    print('  rendija a z = %6.1f: ' % z, '; '.join(fila))
# posturas posibles de la plataforma arriba: (dx, dy, dz, giro en Z, cabeceo en X, cabeceo en Y) que NO pisan ni tubo ni base (lo que la guia)
rng = np.random.default_rng(1)
zc = d2['zc0'] + d['recorrido']
tu = puesta('tubo', G); ba = S['base']
otros = {o: puesta(o, G) for o in ('marco', 'meseta', 'aro_puertas', 'puerta_derecha', 'puerta_izquierda')}
def postura(v):
    dx, dy, dz, gz, cx, cy = v
    return pl.translate([0, 0, -zc]).rotate([cx, cy, gz]).translate([dx, dy, zc + dz])
def vale(v):
    q = postura(v)
    return vol(q, tu) <= UMB and vol(q, ba) <= UMB
# extremos de cada grado de libertad por separado
nombres = ['dx', 'dy', 'dz', 'giro Z', 'cabeceo X', 'cabeceo Y']
print('\nJuego de la plataforma ARRIBA (tau = 345), cada movimiento por separado, guiada solo por tubo y columnas:')
lim = []
for i in range(6):
    r = []
    for sg in (1, -1):
        v = 0.0
        while v < 2.0:
            w = [0.0] * 6; w[i] = sg * (v + 0.01)
            if not vale(w): break
            v += 0.01
        r.append(v)
    lim.append(max(r))
    print('   %-10s +%.2f / -%.2f %s' % (nombres[i], r[0], r[1], 'mm' if i < 3 else 'grados'))
# busqueda al azar de posturas validas y de lo que tocan
print('\nBusqueda al azar (6000 posturas dentro de esos limites): entre las que la guia permite, lo mas cerca / lo que pisa a cada pieza')
peor = {o: (9.0, None) for o in otros}; pisa = {o: (0.0, None) for o in otros}; validas = 0
alto = (0.0, None)
for it in range(6000):
    v = [rng.uniform(-1, 1) * lim[i] * 1.05 for i in range(6)]
    if not vale(v): continue
    validas += 1
    q = postura(v)
    zt = q.bounding_box()[5]
    if zt > alto[0]: alto = (zt, v)
    for o, A in otros.items():
        vv = vol(q, A)
        if vv > pisa[o][0]: pisa[o] = (vv, v)
        g = q.min_gap(A, 1.0)
        if g < peor[o][0]: peor[o] = (g, v)
print('   posturas validas: %d' % validas)
for o in otros:
    print('   %-16s dist min %.3f %s | volumen maximo pisado %.3f mm3 %s' % (o, peor[o][0], '' if peor[o][1] is None else '(postura %s)' % ', '.join('%.2f' % x for x in peor[o][1]), pisa[o][0], '' if pisa[o][1] is None else '(postura %s)' % ', '.join('%.2f' % x for x in pisa[o][1])))
print('   lo mas alto que queda una esquina del pedestal: z = +%.3f mm sobre el ras %s' % (alto[0], '(postura %s)' % ', '.join('%.2f' % x for x in alto[1])))
# cabeceo puro maximo y lo que supone
print('\nCabeceo: maximo en X %.2f y en Y %.2f grados; en lo alto del reloj (%.0f mm sobre los tetones) son %.2f mm de lado' % (lim[4], lim[5], p['reloj_alto'] + d['pedestal_alto'] + 3, math.radians(max(lim[4], lim[5])) * (p['reloj_alto'] + d['pedestal_alto'] + 3)))
