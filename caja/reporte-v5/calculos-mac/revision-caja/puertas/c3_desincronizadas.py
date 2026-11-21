# Comprobacion 3: puertas desincronizadas. Derecha a a+dl, izquierda a a-dl (dl de -4 a 4). Volumen comun y distancia.
from comun import *
def par(aR, aL, dyR=0.0, dyL=0.0):
    A = puerta(1, aR, dyR); B = puerta(-1, aL, dyL)
    v = vol(A, B)
    g = A.min_gap(B, 1.0) if v <= 0 else 0.0
    return v, g
print('a (medio)   delta minimo con el que se pisan (derecha adelantada)   [busqueda de 0 a 6 por biseccion]; por simetria vale igual al reves')
def umbral(a, signo):
    f = lambda dl: par(a + signo * dl, a - signo * dl)[0] > 1e-5
    if not f(8.0): return None
    lo, hi = 0.0, 8.0
    for _ in range(14):
        m = (lo + hi) / 2
        if f(m): hi = m
        else: lo = m
    return hi
tab = []
for a in [0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 45, 60, 75, 88, 90]:
    u1 = umbral(a, 1); u2 = umbral(a, -1)
    tab.append((a, u1, u2))
    print('  a = %5.1f   derecha adelantada: %s    izquierda adelantada: %s' % (a, ('se pisan desde delta = %.2f (diferencia %.2f)' % (u1, 2 * u1)) if u1 else 'no se pisan hasta delta 8', ('delta = %.2f' % u2) if u2 else 'no hasta 8'))
print('con la restriccion fisica de que ninguna puerta baja de 0 grados (asiento): una a 0 y la otra levantada x')
for sg, nom in ((1, 'derecha levantada, izquierda en su asiento'), (-1, 'izquierda levantada, derecha en su asiento')):
    f = lambda x: (par(x, 0.0) if sg > 0 else par(0.0, x))[0] > 1e-5
    lo, hi = 0.0, 10.0
    for _ in range(14):
        m = (lo + hi) / 2
        if f(m): hi = m
        else: lo = m
    A, B = (puerta(1, hi + 0.2), puerta(-1, 0.0)) if sg > 0 else (puerta(1, 0.0), puerta(-1, hi + 0.2))
    print('  %s: se pisan a partir de %.2f grados; donde: %s' % (nom, hi, centro_inter(A, B)))
print('rejilla: volumen comun (mm3) con derecha = a + dl, izquierda = a - dl')
print('   a \\ dl ' + ''.join('%8.1f' % dl for dl in (-4, -3, -2, -1.5, -1, 1, 1.5, 2, 3, 4)))
for a in (0, 2, 4, 6, 8, 10, 12, 15, 20, 30, 60, 90):
    fila = []
    for dl in (-4, -3, -2, -1.5, -1, 1, 1.5, 2, 3, 4):
        aR, aL = a + dl, a - dl
        if aR < -1e-9 or aL < -1e-9: fila.append('    --  '); continue
        v, g = par(aR, aL)
        fila.append('%8.3f' % v if v > 0 else '  (%.2f)' % g)
    print('   %4.0f   ' % a + ''.join(fila))
print('  (entre parentesis: distancia minima en mm cuando no se pisan)')
print('juego axial: puerta derecha desplazada dyR, izquierda dyL (mm), sincronizadas')
for dyR, dyL in ((0, 0), (-0.3, 0.3), (0.3, -0.3), (-0.2, 0.2), (-0.3, 0), (-0.35, 0.35)):
    peor = (0, None); gm = (9, None)
    for i in range(0, 61):
        a = i * 0.5
        v, g = par(a, a, dyR, dyL)
        if v > peor[0]: peor = (v, a)
        if g < gm[0]: gm = (g, a)
    print('  dyR %+.2f dyL %+.2f: volumen max %.4f mm3 a %s grados; distancia minima %.3f mm a %s grados' % (dyR, dyL, peor[0], peor[1], gm[0], gm[1]))
