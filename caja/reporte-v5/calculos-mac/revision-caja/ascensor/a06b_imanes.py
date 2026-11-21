# 6 (bis). Ranuras de los imanes del tope: por donde estan abiertas
from comun import *
z = d['z_suelo'] + 0.6 + 9.4 + 2.65       # media altura de la ranura
for nombre, m in (('base (tope)', S['base']), ('tubo (oreja)', S['tubo'])):
    sec = m.slice(z)
    from shapely.geometry import Polygon, Point
    from shapely.ops import unary_union
    polys = sec.to_polygons()
    # material a lo largo del radio que pasa por el centro de cada ranura
    gi = math.degrees((0.7 + 0.875) / (d['tubo_r_ext'] + 2.8))
    centros = [45.0 + sg * (4 - gi) for sg in (1, -1)] if 'base' in nombre else [37.5 + sg * (3.5 - gi) for sg in (1, -1)]
    import shapely
    from shapely.geometry import LineString
    geom = None
    # construir con evenodd
    from shapely.geometry import MultiPolygon
    anillos = [Polygon(pp) for pp in polys if len(pp) >= 3]
    g = None
    for a in sorted(anillos, key=lambda q: -q.area):
        g = a if g is None else g.symmetric_difference(a)
    for c in centros:
        linea = LineString([CP.pol(79.0, c), CP.pol(90.0, c)])
        inter = g.intersection(linea)
        tramos = []
        for s in (inter.geoms if hasattr(inter, 'geoms') else [inter]):
            if s.length > 1e-6:
                rr = sorted(math.hypot(*pt) for pt in s.coords); tramos.append('%.2f-%.2f' % (rr[0], rr[-1]))
        print('%s, radio que pasa por el centro de la ranura (angulo %.2f): hay material en r = %s' % (nombre, c, ', '.join(sorted(tramos)) or 'NINGUNO'))
print('tubo: pared exterior en r = %.2f ; oreja hasta %.2f ; tope de la base de %.2f a %.2f ; pared del cuerpo (en la esquina) lejos' % (d['tubo_r_ext'], d['tubo_r_ext'] + 5.3, d['tubo_r_ext'] + 0.6, d['tubo_r_ext'] + 5.7))
print('ranura: 1.75 de ancho x 5.3 de alto para un iman de 1.6 x 5.0 -> %.3f por lado en grueso y %.2f en alto' % ((1.75 - 1.6) / 2, 0.15))
