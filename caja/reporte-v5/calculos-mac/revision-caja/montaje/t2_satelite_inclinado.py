# Paso 11 con la rueda central ya puesta: en vertical el satelite pisa la placa de la rueda central (t1_pasos).
# Aqui se busca si hay ALGUN camino inclinando el satelite (giro th alrededor del eje tangencial que pasa por su centro,
# la parte de dentro hacia abajo), desplazandolo en radio (dr, + hacia fuera), en altura (h) y girandolo sobre si mismo (fi).
# Busqueda en anchura desde el sitio final en la rejilla (th, dr, h, fi); una posicion vale si pisa menos de 0,05 mm3
# al plato (con su eje) y a la rueda central. Se da por 'fuera' en cuanto el satelite ha salido del eje (dr >= 8 mm o h >= 7 mm).
from comun import *
from collections import deque
sat = S['satelite_1']; c = np.array([0.0, -d['r_ejes'], (d['z_engr0'] + d['z_engr1']) / 2])
caja_ = mf.Manifold.cube([40, 50, 30]).translate([-20, -100, -20])
obst = {'plato': S['plato'] ^ caja_, 'rueda_central': S['rueda_central'] ^ caja_}
base_sat = sat.translate(list(-c))
def corre(TH, DR, DH, FI, con_giro, lim_th=45.0, tope=400000):
    cache = {}
    def libre(n):
        if n not in cache:
            th, dr, h, fi = n[0] * TH, n[1] * DR, n[2] * DH, n[3] * FI
            s = base_sat.rotate([0, 0, fi]).rotate([-th, 0, 0]).translate([c[0], c[1] - dr, c[2] + h])
            cache[n] = all(vol(s, o) <= 0.05 for o in obst.values())
        return cache[n]
    fin = (0, 0, 0, 0); cola = deque([fin]); visto = {fin: None}; sale = None
    while cola and len(visto) < tope:
        n = cola.popleft()
        if n[1] * DR >= 8.0 or n[2] * DH >= 7.0: sale = n; break
        i, j, k, l = n
        vec = [(i + 1, j, k, l), (i - 1, j, k, l), (i, j + 1, k, l), (i, j - 1, k, l), (i, j, k + 1, l), (i, j, k - 1, l)]
        if con_giro: vec += [(i, j, k, l + 1), (i, j, k, l - 1)]
        for m in vec:
            if not (abs(m[0] * TH) <= lim_th and -2.0 <= m[1] * DR and -1.0 <= m[2] * DH and abs(m[3] * FI) <= 15.0): continue
            if m in visto or not libre(m): continue
            visto[m] = n; cola.append(m)
    V = list(visto)
    print('  rejilla %.2f grados, %.2f mm, %.2f mm%s: posiciones libres alcanzadas desde su sitio: %d. Sale del eje: %s' % (TH, DR, DH, ', con giro propio de %.1f en %.1f' % (FI, FI) if con_giro else '', len(V), 'SI' if sale else ('NO' if not cola else 'sin terminar')))
    print('     alcance: inclinacion de %.1f a %.1f grados; radio de %.2f a %.2f mm; altura de %.2f a %.2f mm' % (min(n[0] for n in V) * TH, max(n[0] for n in V) * TH, min(n[1] for n in V) * DR, max(n[1] for n in V) * DR, min(n[2] for n in V) * DH, max(n[2] for n in V) * DH))
    if sale:
        cam = []; n = sale
        while n is not None: cam.append(n); n = visto[n]
        for n in cam[::max(1, len(cam) // 12)]: print('       %5.1f grados, %6.2f mm afuera, %6.2f mm arriba, giro %5.1f' % (n[0] * TH, n[1] * DR, n[2] * DH, n[3] * FI))
    return sale
t0 = time.time()
corre(1.0, 0.1, 0.1, 3.0, False); print('  %.0f s' % (time.time() - t0))
corre(0.5, 0.05, 0.05, 3.0, False); print('  %.0f s' % (time.time() - t0))
corre(1.0, 0.1, 0.1, 2.5, True); print('  %.0f s' % (time.time() - t0))
