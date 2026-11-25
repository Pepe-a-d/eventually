# Eventually, caja v5: mira, capa a capa (0,2 mm), cuanto de cada pieza se imprimiria en el aire, tal como va orientada.
# Cuenta lo que no tiene debajo la capa anterior ensanchada 0,25 mm (el mismo criterio que la revision de la sesion del Mac).
#   python3 caja_voladizos_v5.py
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
import caja_piezas_v5 as C

BOCA_ABAJO = {'cuerpo', 'funda', 'frase', 'bisel', 'rueda_central', 'puerta_derecha', 'puerta_izquierda', 'probeta_anillo', 'probeta_teton'}
DE_LADO = {'soporte'}        # tumbado sobre su costado derecho
def capa(m, z):
    ps = [Polygon(np.asarray(a)) for a in m.slice(z).to_polygons()]
    ps = [q.buffer(0) for q in ps if len(q.exterior.coords) > 3]
    out = None
    for q in sorted(ps, key=lambda q: -q.area):                 # los contornos de dentro son agujeros
        out = q if out is None else (out.symmetric_difference(q))
    return out
def peor(m):
    b = m.bounding_box(); m = m.translate([0, 0, -b[2]]); alto = b[5] - b[2]
    ant = None; res = (0.0, 0.0); z = 0.1
    while z < alto:
        g = capa(m, z)
        if g is not None and ant is not None:
            a = g.difference(ant.buffer(0.25)).area
            if a > res[0]: res = (a, z)
        ant = g if g is not None else ant; z += 0.2
    return res

if __name__ == '__main__':
    p, d, d2, P = C.piezas()
    for n, q in P.items():
        if n in ('reloj_de_pega', 'frase') or n.startswith('satelite_') and n != 'satelite_1' or n in ('pasador_izquierdo', 'pestillo_izquierdo'): continue
        m = C.solido(q.ops)
        if n in BOCA_ABAJO: m = m.rotate([180, 0, 0])
        if n in DE_LADO: m = m.rotate([0, 90, 0])
        a, z = peor(m)
        print('%s %-18s %-10s lo que mas queda al aire en una capa: %7.1f mm2, a %5.1f mm de la cama' % ('bien ' if a < 20 else 'OJO  ', n, 'boca abajo' if n in BOCA_ABAJO else 'de lado' if n in DE_LADO else 'de pie', a, z))
