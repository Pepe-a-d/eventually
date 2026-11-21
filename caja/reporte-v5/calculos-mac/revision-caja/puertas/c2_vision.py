# Comprobacion 2: linea de vision con las puertas cerradas. Proyeccion de puertas + meseta, vertical e inclinada.
from comun import *
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
def proy(m):
    cs = m.project()
    polys = cs.to_polygons()
    # to_polygons da contornos sueltos (exteriores CCW, agujeros CW): se montan con regla par-impar
    g = None
    from shapely.geometry import Polygon as Pg
    ext = [Pg(q) for q in polys if len(q) >= 3]
    out = None
    for q in sorted(ext, key=lambda q: -q.area):
        q = q.buffer(0)
        out = q if out is None else out.symmetric_difference(q)
    return out
def cizalla(m, tx, ty):
    # rayo inclinado: un punto (x,y,z) se ve en (x - z*tx, y - z*ty) sobre el plano z=0
    M = np.array([[1, 0, -tx, 0], [0, 1, -ty, 0], [0, 0, 1, 0]], dtype=float)
    return m.transform(M)
hx, hy = d['hueco_x']/2, d['hueco_y']/2
hueco = box(-hx, -hy, hx, hy)
tapan = ['puerta_derecha', 'puerta_izquierda', 'meseta']
print('VERTICAL')
u = unary_union([proy(S[n]) for n in tapan])
libre = hueco.difference(u)
print('  area sin tapar dentro del hueco 50x59: %.4f mm2' % libre.area)
for q in (libre.geoms if hasattr(libre, 'geoms') else [libre]):
    if q.area > 1e-6: print('   trozo de %.4f mm2, caja x %.3f..%.3f  y %.3f..%.3f' % ((q.area,) + (q.bounds[0], q.bounds[2], q.bounds[1], q.bounds[3])))
# que hay debajo de ese agujero: todas las piezas
for n in S:
    if P[n].mueve in ('funda', 'probeta') or n in tapan: continue
    pr = proy(S[n])
    if pr is not None and pr.intersection(libre).area > 1e-6:
        print('   debajo del agujero esta: %s (z max %.2f)' % (n, S[n].bounding_box()[5]))
# tambien fuera del hueco: todo el rectangulo de las puertas (62 x 73.6), que se ve por las rendijas
rect = box(-d['puertas_x']/2 - 0.5, -d['puerta_y']/2 - 0.5, d['puertas_x']/2 + 0.5, d['puerta_y']/2 + 0.5)
u2 = unary_union([proy(S[n]) for n in ('puerta_derecha', 'puerta_izquierda')])
print('  (rendijas alrededor de las puertas, por donde se ve la meseta o lo de debajo: %.2f mm2)' % rect.difference(u2).area)
u3 = unary_union([proy(S[n]) for n in tapan])
r3 = rect.difference(u3)
print('  dentro del rectangulo de las puertas, area por la que la vertical no toca ni puertas ni meseta: %.4f mm2' % r3.area)
for q in (r3.geoms if hasattr(r3, 'geoms') else [r3]):
    if q.area > 1e-4: print('   trozo de %.4f mm2, caja x %.3f..%.3f  y %.3f..%.3f' % ((q.area,) + (q.bounds[0], q.bounds[2], q.bounds[1], q.bounds[3])))
print('INCLINADA (grados respecto a la vertical; ax = inclinacion hacia X, ay = hacia Y)')
import itertools
res = []
for ax in (0, 5, 10, 15, 20, 25, 30, -10, -20, -30):
    for ay in (0, 5, 10, 15, 20, 22, 24, 26, 28, 30, -10, -20, -30):
        tx, ty = math.tan(math.radians(ax)), math.tan(math.radians(ay))
        # el hueco, a la altura z=0 (plano de arriba). Un rayo que entra por (x,y,0) con esa inclinacion
        u = unary_union([proy(cizalla(S[n], tx, ty)) for n in tapan])
        # zona a mirar: la raya del centro y sus alrededores, en z = 0
        zona = box(-6, -hy + 6, 6, hy - 6)
        lib = zona.difference(u)
        res.append((ax, ay, lib.area, lib.bounds if lib.area > 1e-6 else None))
for ax, ay, a, b in res:
    if a > 1e-6: print('  ax %4d ay %4d: %.4f mm2 sin tapar  %s' % (ax, ay, a, [round(v, 2) for v in b]))
print('  inclinaciones sin linea de vision:', [(ax, ay) for ax, ay, a, b in res if a <= 1e-6])
