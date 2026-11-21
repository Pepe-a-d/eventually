# Comprobacion 7 (primera parte): la pared de la pista que hace de tope a la puerta, en la planta del aro
from comun import *
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import unary_union
from shapely.affinity import rotate as srot
def planta(z):
    cs = S['aro_puertas'].slice(z).to_polygons()
    out = None
    for q in sorted([Polygon(q).buffer(0) for q in cs], key=lambda q: -q.area):
        out = q if out is None else out.symmetric_difference(q)
    return out
anillo = planta(d['z_corr0'] + 0.6)          # el anillo macizo, por debajo del suelo de la pista
medio = planta(d['z_corr0'] + 2.0)           # el anillo, con la pista ya cortada
cuern = planta(-10.0)                        # los cuernos, a la altura de la bola
print('areas: anillo macizo %.0f, anillo con pistas %.0f, cuernos %.0f mm2' % (anillo.area, medio.area, cuern.area))
sen = p['aro_sentido']; xh = d['eje_x']; yb = d['bola_y']; rb = p['bola_d'] / 2
def bola_en_aro(psi):
    x = xh + D.bola_x(p, d, psi); a = -math.radians(sen * psi)
    return (x * math.cos(a) - yb * math.sin(a), x * math.sin(a) + yb * math.cos(a))
print('pared a cada lado de la bola (medida en la planta de los cuernos, a z = -10), y cuanta de esa pared tiene anillo debajo')
print('  psi | bola en el aro (x, y) r | pared hacia el centro: grueso, con anillo debajo | pared hacia fuera: grueso, con anillo debajo')
for psi in (0.0, 1.25, 2.5, 4.0, 5.5, 7.0, 8.5, 9.75, 11.0):
    c = bola_en_aro(psi); r = math.hypot(*c)
    # normal a la pista: direccion perpendicular a la tangente de la trayectoria
    c2 = bola_en_aro(psi + 0.01) if psi < 10.9 else bola_en_aro(psi - 0.01)
    tx, ty = c2[0] - c[0], c2[1] - c[1]; n = math.hypot(tx, ty)
    if n < 1e-9: tx, ty = -c[1], c[0]; n = math.hypot(tx, ty)
    nx, ny = -ty / n, tx / n
    if nx * c[0] + ny * c[1] < 0: nx, ny = -nx, -ny             # normal hacia fuera
    res = []
    for sg in (-1, 1):
        ray = LineString([(c[0], c[1]), (c[0] + sg * nx * 12, c[1] + sg * ny * 12)])
        w = ray.intersection(cuern); wa = ray.intersection(cuern).intersection(anillo)
        # primer tramo de pared
        tr = [g for g in (w.geoms if hasattr(w, 'geoms') else [w]) if g.length > 1e-6]
        if not tr: res.append('NO HAY PARED'); continue
        tr.sort(key=lambda g: Point(c).distance(g)); g0 = tr[0]
        res.append('empieza a %.2f mm del centro de la bola, grueso %.2f, con anillo debajo %.2f' % (Point(c).distance(g0), g0.length, g0.intersection(anillo).length))
    print('  %5.2f | (%.2f, %.2f) r=%.2f | %s | %s' % (psi, c[0], c[1], r, res[0], res[1]))
print('radio interior del anillo %.2f; la pista (ancho %.2f) con la bola en abierto llega a radio %.2f -> rompe el borde interior del anillo: %s' % (d['aro_r_in'], 2 * (rb + p['bola_holgura']), d['bola_r_abierta'] - rb - p['bola_holgura'], d['bola_r_abierta'] - rb - p['bola_holgura'] < d['aro_r_in']))
vol_cuernos = cuern.area
en_aire = cuern.difference(anillo)
print('planta de los cuernos que NO tiene anillo debajo (vuela sobre el hueco del centro): %.1f mm2 de %.1f; trozos: %s' % (en_aire.area, cuern.area, [(round(g.area, 1), [round(v, 1) for v in g.bounds]) for g in (en_aire.geoms if hasattr(en_aire, 'geoms') else [en_aire]) if g.area > 0.05]))
# cuanto vuela como mucho
vuelo = max((Point(q).distance(anillo) for g in (en_aire.geoms if hasattr(en_aire, 'geoms') else [en_aire]) for q in g.exterior.coords), default=0)
print('   lo que mas se aleja del anillo: %.2f mm' % vuelo)
# suelo de la pista
print('suelo de la pista: %.2f mm de grueso (de z %.2f a %.2f); bajo la bola en abierto, %s' % (1.2, d['z_corr0'], d['z_corr0'] + 1.2, 'hay anillo' if anillo.contains(Point(bola_en_aro(11.0))) else 'NO hay anillo: la pista no tiene suelo ahi'))
