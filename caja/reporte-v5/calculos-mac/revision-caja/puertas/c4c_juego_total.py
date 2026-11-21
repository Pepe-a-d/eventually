# Comprobacion 4 (tercera parte): juego de la puerta contando con que el aro se desplaza dentro de su holgura (0,3 mm) con el teton puesto
from comun import *
EPS = 1e-4
def teton_cabe(A, tau):
    """Hay alguna posicion del teton, dentro de sus holguras, que no pise aro, marco ni plato?"""
    T0 = mv('teton', tau); PL = mv('plato', tau)
    for ex in (0, 0.1, -0.1, 0.19, -0.19):
        for ey in (0, 0.1, -0.1, 0.19, -0.19):
            T = T0.translate([ex, ey, 0])
            if vol(T, A) + vol(T, S['marco']) + vol(T, PL) <= EPS: return True
    return False
def rango_puerta(sx, ang0, A, contra=()):
    f = lambda sg: lambda dl: sum(vol(puerta(sx, ang0 + sg * dl), c) for c in [A] + list(contra)) > EPS
    def lim(sg):
        prev = 0.0
        for i in range(1, 161):
            dl = 0.25 * i
            if f(sg)(dl): return bisec(f(sg), prev, dl, 8)
            prev = dl
        return 40.0
    return lim(1), lim(-1)
for nom, tau, ang0 in (('CERRADO (tubo 0)', 0.0, 0.0), ('ABIERTO (tubo 345)', 345.0, 90.0), ('ABIERTO, cuando el reloj empieza a subir (tubo 92)', 92.0, 90.0)):
    psi = D.movimiento(p, d, tau)[1]
    print(nom, 'psi = %.2f' % psi)
    peor_up = {1: (0, None), -1: (0, None)}; peor_dn = {1: (0, None), -1: (0, None)}
    for e in (0.0, 0.15, 0.29):
        for k in range(0, 360, 30) if e > 0 else [0]:
            dx, dy = e * math.cos(math.radians(k)), e * math.sin(math.radians(k))
            for rot in (0.0, 0.24, -0.24):
                A = aro(psi + rot, dx, dy)
                if vol(A, S['marco']) + vol(A, S['meseta']) > EPS: continue
                if not teton_cabe(A, tau): continue
                for sx in (1, -1):
                    # la puerta nominal tiene que caber; si no cabe (el aro la ha empujado), se busca el angulo mas cercano que quepa
                    base = ang0
                    if vol(puerta(sx, base), A) > EPS:
                        cand = [base + s_ * 0.25 * i for i in range(1, 80) for s_ in (1, -1)]
                        cand = [c for c in cand if c >= -0.001]
                        base = next((c for c in cand if vol(puerta(sx, c), A) + (vol(puerta(sx, c), S['meseta']) if c < 1 else 0) <= EPS), None)
                        if base is None: continue
                    up, dn = rango_puerta(sx, base, A, [S['meseta']])
                    hi, lo = base + up, base - dn
                    if hi - ang0 > peor_up[sx][0]: peor_up[sx] = (hi - ang0, (e, k, rot))
                    if ang0 - lo > peor_dn[sx][0]: peor_dn[sx] = (ang0 - lo, (e, k, rot))
            if e == 0.0: print('   aro centrado: derecha puede abrir %.2f / cerrar %.2f mas; izquierda %.2f / %.2f' % (peor_up[1][0], peor_dn[1][0], peor_up[-1][0], peor_dn[-1][0]))
    for sx in (1, -1):
        print('   puerta %s: contando el juego del aro, llega a %.2f grados por encima del nominal (aro desplazado %.2f mm hacia %d grados, girado %+.2f) y a %.2f por debajo (aro %.2f mm hacia %d, girado %+.2f)' % (
            'derecha' if sx > 0 else 'izquierda', peor_up[sx][0], peor_up[sx][1][0], peor_up[sx][1][1], peor_up[sx][1][2], peor_dn[sx][0], peor_dn[sx][1][0], peor_dn[sx][1][1], peor_dn[sx][1][2]))
