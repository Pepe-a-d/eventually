# 2. En cada giro de tubo: cuanto baja, sube y gira la plataforma por su cuenta antes de chocar (mallas; umbral 0.001 mm3)
from comun import *
UMB = 1e-3
def busca(pl, contra, mov, pasos):
    ant = 0.0
    for v in pasos:
        q = mov(pl, v)
        for nombre, c in contra:
            if vol(q, c) > UMB: return ant, nombre
        ant = v
    return ant, '-'
pasos_z = [round(0.02 * i, 3) for i in range(1, 31)] + [round(0.6 + 0.1 * i, 3) for i in range(1, 45)]
pasos_g = [round(0.02 * i, 3) for i in range(1, 101)]
filas = []
t0 = time.time()
for tau in [float(t) for t in range(0, 346)]:
    pl = puesta('plataforma', tau)
    contra = [(n, puesta(n, tau)) for n in ('tubo', 'base', 'marco', 'meseta', 'aro_puertas', 'puerta_derecha', 'puerta_izquierda')]
    b, nb = busca(pl, contra, lambda m, v: m.translate([0, 0, -v]), pasos_z)
    s, ns = busca(pl, contra, lambda m, v: m.translate([0, 0, v]), pasos_z)
    g1, n1 = busca(pl, contra, lambda m, v: m.rotate([0, 0, v]), pasos_g)
    g2, n2 = busca(pl, contra, lambda m, v: m.rotate([0, 0, -v]), pasos_g)
    filas.append((tau, b, nb, s, ns, g1, n1, g2, n2))
print('tiempo %.0f s' % (time.time() - t0))
import json
json.dump(filas, open('a02_res.json', 'w'))
print(' tau   baja(mm) contra   sube(mm) contra   gira+ (grados) contra   gira- contra')
ant = None
for f in filas:
    clave = (f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8])
    if clave != ant: print(' %5.0f  %5.2f %-8s  %5.2f %-8s  %5.2f %-8s  %5.2f %-8s' % f)
    ant = clave
print('giros donde baja mas de 0.5 mm:', [f[0] for f in filas if f[1] > 0.5])
print('giros donde sube mas de 0.5 mm:', [f[0] for f in filas if f[3] > 0.5])
