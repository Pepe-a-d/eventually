# Pieles finas en vertical: zonas donde el material solo dura 1, 2, 3 o 4 capas (0,2 a 0,8 mm) con aire (o la cama) por debajo y aire por encima.
# Uso: python laminas.py [pieza ...]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def laminas(nombre, kmax=4, amin=0.5):
    s, inv = colocada(nombre)
    L = [g for z, g in capas(s)]
    vacio = Polygon()
    out = []
    for i, g in enumerate(L):
        abajo = L[i - 1] if i > 0 else vacio
        empieza = g.difference(abajo.buffer(0.001)) if i > 0 else g
        if empieza.is_empty: continue
        vivo = empieza
        for k in range(1, kmax + 1):
            arriba = L[i + k] if i + k < len(L) else vacio
            acaba = abrir(vivo.difference(arriba.buffer(0.001)), 0.25)       # se quitan tiras de menos de 0,5 mm (pendientes)
            for q in trozos(acaba, amin):
                cx, cy = q.representative_point().coords[0]
                out.append((k, i, q.area, q.bounds, inv(cx, cy, (i + 0.5) * CAPA), i == 0, i + k >= len(L)))
            vivo = vivo.intersection(arriba)
            if vivo.is_empty: break
    return out

if __name__ == '__main__':
    for n in (sys.argv[1:] or list(ORIENT)):
        out = laminas(n)
        print('== %s: %d zonas de 4 capas o menos' % (n, len(out)))
        for k, i, a, b, pz, cama, techo in sorted(out, key=lambda o: (o[0], -o[2]))[:14]:
            print('   %d capa(s) (%.1f mm) desde z %.1f de impresion%s%s: %.1f mm2, caja (%.1f %.1f %.1f %.1f) = %.1f x %.1f, en la pieza (%.1f, %.1f, %.1f)' % (
                k, k * CAPA, i * CAPA, ' [sobre la cama]' if cama else '', ' [cara de arriba]' if techo else '', a, *b, b[2] - b[0], b[3] - b[1], *pz))
