# Tubo: cuanto saca cada capa sobre la de debajo en las ranuras en V (tramos planos y helice) y en la cartela de la oreja.
# Para cada capa: lo mas lejos que un punto nuevo queda de la capa de debajo (0,2 mm = 45 grados).
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, shapely
from shapely.geometry import Point
from comun import *
arg = sys.argv[1] if len(sys.argv) > 1 else 'tubo'
import detalle
s, inv = detalle.carga(arg)
L = capas(s)
peor = []
for i in range(1, len(L)):
    z, g = L[i]; prev = L[i - 1][1]
    f = g.difference(prev.buffer(0.0005))
    m = 0.0; donde = None
    for q in trozos(f, 0.002):
        pts = shapely.points(np.array(q.exterior.coords))
        dd = shapely.distance(pts, prev); k = int(dd.argmax())
        if dd[k] > m: m = float(dd[k]); donde = q.exterior.coords[k]
    peor.append((z, m, donde, f.area))
# resumen por tramos de altura
def tramo(z0, z1, nombre):
    v = [x for x in peor if z0 <= x[0] < z1]
    if not v: return
    mx = max(v, key=lambda x: x[1]); med = float(np.median([x[1] for x in v]))
    print('%-46s z %5.1f..%5.1f: saliente mediano %.3f mm (%.0f grados), maximo %.3f mm (%.0f grados) en z %.1f, punto (%.1f, %.1f)' % (
        nombre, z0, z1, med, math.degrees(math.atan2(med, CAPA)), mx[1], math.degrees(math.atan2(mx[1], CAPA)), mx[0], *(mx[2] or (0, 0))))
tramo(0.2, 3.0, 'tramo plano de abajo, suelo (no es voladizo)')
tramo(3.4, 6.6, 'tramo plano de abajo, techo en V')
tramo(7.0, 9.0, 'helice y cartela de la oreja')
tramo(9.0, 16.0, 'oreja y ranuras de iman')
tramo(16.0, 88.0, 'helice')
tramo(88.0, 94.6, 'tramo plano de arriba, techo en V')
tramo(94.6, 94.8, 'tapa plana de la helice')
tramo(94.8, 106.1, 'por encima (almenas)')
