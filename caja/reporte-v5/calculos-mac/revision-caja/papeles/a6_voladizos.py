# 6. "Todas, sin soportes": capa a capa (0,2 mm), en la orientacion de imprimir que da el reporte, lo que cada capa tiene
#    fuera de la anterior mas alla de 45 grados (0,2 mm de vuelo por capa; se toma 0,3 para no contar redondeos).
import sys
from comun import *
from shapely.geometry import Polygon
from shapely.ops import unary_union
def cs2shp(cs):
    out = [Polygon(q) for q in cs.to_polygons() if len(q) >= 3]
    out.sort(key=lambda g: -g.area); res = None
    for g in out:
        g = g.buffer(0); res = g if res is None else res.symmetric_difference(g)
    return res if res is not None else Polygon()
ORI = {'base': False, 'tubo': False, 'cuerpo': True, 'funda': True, 'plataforma': False, 'bisel': True, 'plato': False, 'marco': False, 'satelite_1': False, 'teton': False,
       'soporte': False, 'rueda_central': True, 'puerta_derecha': True, 'meseta': False, 'aro_puertas': False, 'probeta_anillo': True, 'probeta_teton': False}
solo = sys.argv[1:] or list(ORI)
for n in solo:
    m = S[n]
    if n == 'funda': m = m + S['frase']
    if ORI[n]: m = m.rotate([180, 0, 0])
    b = bb(m); m = m.translate([0, 0, -b[2]]); H = b[5] - b[2]
    prev = cs2shp(m.slice(0.1)); hall = []
    z = 0.3
    while z < H:
        cur = cs2shp(m.slice(z))
        if not cur.is_empty:
            U = cur.difference(prev.buffer(0.3, 8)) if not prev.is_empty else cur
            if U.area > 0.5:
                for g in (U.geoms if hasattr(U, 'geoms') else [U]):
                    if g.area < 0.3: continue
                    # vuelo: lo mas lejos que queda un punto de la zona sin apoyo de lo que habia debajo; y si es un puente (apoya en dos lados opuestos)
                    vuelo = 0.3 + max(prev.distance(__import__('shapely').geometry.Point(q)) - 0.3 for q in list(g.exterior.coords)[::max(1, len(g.exterior.coords) // 60)]) if not prev.is_empty else 99
                    # ancho libre: el doble del mayor circulo inscrito (aprox. por erosion)
                    k = 0.0
                    while k < 30 and not g.buffer(-(k + 0.25)).is_empty: k += 0.25
                    hall.append((z, g.area, vuelo, 2 * k, g.bounds))
        prev = cur if not cur.is_empty else prev
        z += 0.2
    # resumen: agrupar por altura
    print('== %-15s %s, alto %.1f: %d zonas sin apoyo' % (n, 'BOCA ABAJO' if ORI[n] else 'de pie', H, len(hall)))
    porz = {}
    for z, a, v, w, bnd in hall: porz.setdefault(round(z, 1), []).append((a, v, w, bnd))
    for z in sorted(porz):
        L = porz[z]; A = sum(q[0] for q in L); V = max(q[1] for q in L); W = max(q[2] for q in L)
        if A > 3.0 or V > 1.2: print('     capa a %.1f mm: %d zonas, %.0f mm2 en total; vuelo hasta %.1f mm; ancho libre hasta %.1f mm; caja de la mayor %s' % (z, len(L), A, V, W, tuple(round(v, 1) for v in max(L, key=lambda q: q[0])[3])))
    sys.stdout.flush()
