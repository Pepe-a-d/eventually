# Orden alternativo: ... pasadores, cerrar puertas, teton, PLATO, SATELITES, RUEDA CENTRAL, bisel + cuerpo.
from comun import *
from t1_pasos_fn import camino, informe
M = {n: puesta(n, 0) for n in ('base', 'plataforma', 'tubo', 'marco', 'aro_puertas', 'meseta', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo')}
informe('teton (sin rueda central)', camino(puesta('teton', 0), M)); M['teton'] = puesta('teton', 0)
informe('plato', camino(puesta('plato', 0), M)); M['plato'] = puesta('plato', 0)
for k in range(1, 7):
    n = 'satelite_%d' % k; informe(n, camino(S[n], M)); M[n] = S[n]
informe('rueda central, con plato y satelites puestos', camino(S['rueda_central'], M)); M['rueda_central'] = S['rueda_central']
informe('bisel', camino(S['bisel'], M)); informe('cuerpo', camino(S['cuerpo'], M))
# y con las puertas de pie (abiertas) en vez de cerradas, por si se prefiere poner la rueda central antes de cerrar
