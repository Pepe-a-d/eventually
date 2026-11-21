# Comprobacion 4 (segunda parte): juego del propio aro, y juego de las puertas contando con el
from comun import *
EPS = 1e-4
FIJOS = [S['marco'], S['meseta']]
def aro_libre(psi, dx, dy, extra=()):
    A = aro(psi, dx, dy)
    return sum(vol(A, c) for c in FIJOS + list(extra)) <= EPS
print('B1) aro SIN teton: cuanto puede desplazarse en cada direccion (marco + meseta), en psi = 0, 5.5 y 11')
for psi in (0.0, 5.5, 11.0):
    r = []
    for k in range(0, 360, 30):
        ux, uy = math.cos(math.radians(k)), math.sin(math.radians(k))
        e = bisec(lambda e: not aro_libre(psi, e * ux, e * uy), 0.0, 2.0, 12)
        r.append('%d:%.2f' % (k, e))
    print('   psi %.1f  direccion(grados):mm  ' % psi + '  '.join(r))
print('B2) aro SIN teton: cuanto puede girar mas alla de sus extremos (topes de montaje)')
f = lambda e: not aro_libre(-e, 0, 0); print('   mas alla de cerrado: %.2f grados' % bisec(f, 0.0, 8.0, 12))
f = lambda e: not aro_libre(11 + e, 0, 0); print('   mas alla de abierto: %.2f grados' % bisec(f, 0.0, 8.0, 12))
print('B3) aro CON teton. Giro libre del aro con el teton quieto en su sitio, y con el teton movido dentro de sus holguras')
for tau in (0.0, 55.0, 62.0, 66.0, 72.5, 78.0, 83.0, 90.0, 345.0):
    s, psi, ang, h = D.movimiento(p, d, tau)
    T0 = mv('teton', tau); PL = mv('plato', tau)
    def giro_lim(T, signo):
        return bisec(lambda e: vol(aro(psi + signo * e), T) > EPS or not aro_libre(psi + signo * e, 0, 0), 0.0, 3.0, 12)
    a1, a2 = giro_lim(T0, 1), giro_lim(T0, -1)
    # teton movido de lado (ranura del marco) y a lo largo (espiral del plato): hasta donde llega sin pisar marco ni plato
    def teton_lim(ux, uy):
        return bisec(lambda e: vol(T0.translate([e * ux, e * uy, 0]), S['marco']) + vol(T0.translate([e * ux, e * uy, 0]), PL) > EPS, 0.0, 1.5, 12)
    tx1, tx2 = teton_lim(1, 0), teton_lim(-1, 0); ty1, ty2 = teton_lim(0, 1), teton_lim(0, -1)
    # peor caso: rejilla de posiciones del teton dentro de su holgura
    mejor1 = mejor2 = 0.0
    for ex in np.linspace(-tx2, tx1, 5):
        for ey in np.linspace(-ty2, ty1, 5):
            T = T0.translate([ex * 0.98, ey * 0.98, 0])
            if vol(T, S['marco']) + vol(T, PL) > EPS: continue
            mejor1 = max(mejor1, giro_lim(T, 1)); mejor2 = max(mejor2, giro_lim(T, -1))
    print('   tubo %5.1f (psi %5.2f, puerta %5.1f): teton quieto: aro +%.2f / -%.2f grados | teton se mueve X +%.2f/-%.2f mm, Y +%.2f/-%.2f mm | con eso el aro gira +%.2f / -%.2f grados' % (tau, psi, ang, a1, a2, tx1, tx2, ty1, ty2, mejor1, mejor2))
