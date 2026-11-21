# Mira de cerca una pieza entre dos alturas de impresion: capa a capa, lo que cada capa saca por fuera de la de debajo.
# Uso:  python detalle.py <pieza | fichero.3mf:n> z0 z1 [x0 y0 x1 y1]      (alturas y ventana en coordenadas de impresion)
#       con 'pieza:pie' o 'pieza:abajo' se fuerza la postura
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from shapely.geometry import box
from comun import *

def carga(arg):
    """Devuelve (solido colocado con z minimo 0, inversa o None)."""
    if '.3mf' in arg:
        import trimesh, tresmf
        fn, k = arg.rsplit(':', 1)
        if not os.path.isabs(fn): fn = os.path.join(tresmf.CARPETA, fn)
        _, cuerpos = tresmf.lee_3mf(fn)
        nombre, V, T = cuerpos[int(k) - 1]
        s = tresmf.a_manifold(trimesh.Trimesh(V, T, process=True))
        assert s is not None, 'no es variedad'
        return s, None
    if ':' in arg:
        n, post = arg.split(':')
        return colocada(n, post == 'abajo')
    return colocada(arg)

def mira(arg, z0, z1, ventana=None, amin=0.02):
    s, inv = carga(arg)
    L = capas(s)
    prev = None
    for z, g in L:
        if ventana is not None: g = g.intersection(box(*ventana))
        if prev is not None and z0 - 1e-6 <= z <= z1 + 1e-6:
            fuera = g.difference(prev.buffer(0.001))
            f45 = g.difference(prev.buffer(0.22, 8))
            print('z %.2f  area capa %.2f  trozos %d | fuera de la de debajo %.2f mm2, mas alla de 0,2 mm: %.2f mm2' % (z, g.area, len(trozos(g)), fuera.area, f45.area))
            for q in sorted(trozos(fuera, amin), key=lambda q: -q.area)[:8]:
                al = alcance(q, prev)
                if al < 0.25: continue
                una, pp, frac = puente(q, prev)
                cx, cy = q.representative_point().coords[0]
                print('      trozo %.2f mm2  caja (%.2f %.2f %.2f %.2f)  alcance %.2f  luz %s  punto a punto %s (%.0f %%)%s' % (
                    q.area, *q.bounds, al, '%.1f' % una if math.isfinite(una) else '-', '%.1f' % pp if math.isfinite(pp) else '-', 100 * frac,
                    ('  pieza (%.1f, %.1f, %.1f)' % inv(cx, cy, z)) if inv else ''))
        prev = g

if __name__ == '__main__':
    a = sys.argv
    mira(a[1], float(a[2]), float(a[3]), [float(x) for x in a[4:8]] if len(a) >= 8 else None)
