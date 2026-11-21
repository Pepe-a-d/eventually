# El mismo analisis por capas de capas.py, pero sobre los cuerpos de los .3mf tal como vienen colocados (lo que de verdad se va a imprimir).
# Uso: python -I capas3mf.py
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trimesh
from comun import *
import tresmf, capas
for fn in sorted(glob.glob(os.path.join(tresmf.CARPETA, 'caja-probeta-*.3mf'))):
    _, cuerpos = tresmf.lee_3mf(fn)
    for k, (nombre, V, T) in enumerate(cuerpos):
        s = tresmf.a_manifold(trimesh.Trimesh(V, T, process=True))
        if s is None:
            print('%s cuerpo %d: no es variedad, no se analiza' % (os.path.basename(fn), k + 1)); continue
        if 'satelites' in fn and k > 0: continue                    # los seis satelites son iguales
        res = capas.analiza('%s#%d' % (os.path.basename(fn).replace('caja-probeta-', '').replace('.3mf', ''), k + 1), boca_abajo=False, solido=s)
        capas.resumen(res)
