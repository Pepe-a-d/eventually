# Donde se acercan las parejas a menos de 0,15
from comun import *
print('--- puerta derecha / puerta izquierda, sincronizadas, por angulo de puerta')
peor = (9, 0)
for i in range(0, 361):
    a = i * 0.25
    g = puerta(1, a).min_gap(puerta(-1, a), 1.0)
    if g < peor[0]: peor = (g, a)
    if i % 8 == 0 or (a <= 12 and i % 2 == 0): print('  ang %.2f  gap %.3f' % (a, g))
print('  minimo %.4f a %.2f grados' % peor)
g, c = localiza(puerta(1, peor[1]), puerta(-1, peor[1]))
print('  lugar (caja x0,y0,z0,x1,y1,z1):', c)
g, c = localiza(puerta(1, 0), puerta(-1, 0)); print('  cerradas: gap %.3f en' % g, c)
print('--- puerta derecha / aro, por tau')
for tau in (0, 40, 50, 60, 63, 66, 70, 75, 80, 83, 86, 92, 100):
    A = mv('puerta_derecha', tau); R = mv('aro_puertas', tau)
    g, c = localiza(A, R)
    print('  tau %5.1f  gap %.3f  en' % (tau, g), c)
print('--- puerta derecha / meseta por angulo (sin el asiento: a partir de 0,5 grados)')
peor = (9, 0)
for i in range(1, 185):
    a = i * 0.5
    g = puerta(1, a).min_gap(S['meseta'], 1.0)
    if g < peor[0]: peor = (g, a)
    if i % 10 == 0 or i < 6: print('  ang %.1f gap %.3f' % (a, g))
print('  minimo %.4f a %.1f' % peor)
g, c = localiza(puerta(1, peor[1]), S['meseta']); print('   lugar', c)
