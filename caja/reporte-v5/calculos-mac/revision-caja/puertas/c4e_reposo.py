# Cuanto bloquea de verdad el tramo de reposo: juego de la puerta segun psi dentro del reposo (aro centrado)
from comun import *
EPS = 1e-4
def lim(sx, ang0, sg, A, extra=()):
    f = lambda dl: sum(vol(puerta(sx, ang0 + sg * dl), c) for c in [A] + list(extra)) > EPS
    prev = 0.0
    for i in range(1, 241):
        dl = 0.25 * i
        if f(dl): return bisec(f, prev, dl, 8)
        prev = dl
    return 60.0
print('reposo de CERRADO: cuanto se deja levantar la puerta')
for psi in (-0.5, 0.0, 0.5, 1.0, 1.5, 1.75, 2.0, 2.25, 2.5):
    print('   psi %5.2f (tubo %5.1f): %.2f grados' % (psi, tau_de_psi(max(psi, 0)), lim(1, 0.0, 1, aro(psi))))
print('reposo de ABIERTO: cuanto se deja mover hacia dentro / hacia fuera (aro + meseta)')
for psi in (8.5, 8.75, 9.0, 9.25, 9.5, 10.0, 10.44, 11.0, 11.5):
    print('   psi %5.2f (tubo %5.1f): hacia dentro %.2f, hacia fuera %.2f' % (psi, tau_de_psi(min(psi, 10.999)), lim(1, 90.0, -1, aro(psi)), lim(1, 90.0, 1, aro(psi), [S['meseta']])))
s92 = D.movimiento(p, d, 92.0); print('cuando la plataforma empieza a subir (tubo 92): psi = %.2f; con el juego de giro del aro (0,55) puede estar en psi = %.2f' % (s92[1], s92[1] - 0.55))
