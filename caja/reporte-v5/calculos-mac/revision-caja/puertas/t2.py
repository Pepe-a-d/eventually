from comun import *
from shapely.geometry import Polygon, Point, LineString
from c7_paredes import planta, bola_en_aro, anillo, cuern
c = bola_en_aro(0.0)
print('bola', c, 'cuern tipo', cuern.geom_type, 'n', len(list(cuern.geoms)) if hasattr(cuern, 'geoms') else 1)
for g in (cuern.geoms if hasattr(cuern, 'geoms') else [cuern]):
    print('  trozo area %.1f bounds %s agujeros %d' % (g.area, [round(v, 1) for v in g.bounds], len(g.interiors)))
for L in np.arange(0, 14, 0.5):
    q = Point(c[0] - L, c[1]); print('%.1f %s r=%.2f' % (L, cuern.contains(q), math.hypot(q.x, q.y)), end=' | ')
print()
# en 3D directamente
for L in np.arange(0, 8, 0.5):
    cubo = mf.Manifold.cube([0.02, 0.02, 0.02]).translate([c[0] - L, c[1], -10])
    print('%.1f %s' % (L, (cubo ^ S['aro_puertas']).volume() > 0), end=' | ')
print()
cs = S['aro_puertas'].slice(-10.0).to_polygons()
print([ (len(q), round(Polygon(q).area,1), Polygon(q).exterior.is_ccw) for q in cs])
