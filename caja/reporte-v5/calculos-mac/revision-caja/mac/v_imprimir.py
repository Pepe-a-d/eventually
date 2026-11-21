"""Sesion del Mac: voladizos por capas, comprobacion propia. Uso: python v_imprimir.py pieza [boca_abajo]"""
import sys, os
sys.path.insert(0, os.environ.get('CAJA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
import manifold3d as mf, numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
import caja_piezas_v5 as CP
p, d, d2, P = CP.piezas()
def capa(M, z):
    pols = [Polygon(q) for q in M.slice(z).to_polygons() if len(q) >= 3]
    # regla par-impar: los contornos interiores son agujeros
    out = None
    for q in sorted(pols, key=lambda g: -g.area):
        q = q.buffer(0)
        out = q if out is None else out.symmetric_difference(q)
    return out if out is not None else Polygon()
def voladizos(nombre, boca_abajo, paso=0.2, apoyo=0.25):
    M = CP.solido(P[nombre].ops)
    if boca_abajo: M = M.rotate([180, 0, 0])
    b = M.bounding_box(); M = M.translate([0, 0, -b[2]]); alto = b[5] - b[2]
    ant = None; res = []
    for i in range(int(round(alto / paso))):
        z = paso * i + paso / 2
        c = capa(M, z)
        if ant is not None:
            aire = c.difference(ant.buffer(apoyo))
            if aire.area > 1.0:
                res.append((z, aire.area, max((g.area for g in (aire.geoms if hasattr(aire, 'geoms') else [aire])))))
        ant = c
    return res
for arg in sys.argv[1:]:
    nombre, ba = arg.split(':') if ':' in arg else (arg, '0')
    r = voladizos(nombre, ba == '1')
    print('%s (%s): capas con mas de 1 mm2 sin apoyo a 0,25 mm de la capa anterior: %d' % (nombre, 'boca abajo' if ba == '1' else 'de pie', len(r)))
    for z, a, mx in sorted(r, key=lambda t: -t[1])[:6]:
        print('   z de impresion %.1f: %.1f mm2 sin apoyo (el trozo mayor, %.1f)' % (z, a, mx))
