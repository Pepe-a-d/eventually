# Comprobacion 3 (umbral): diferencia de angulo entre las dos puertas a partir de la cual se pisan, para cada angulo de la mas baja
from comun import *
print('puerta baja (grados) | la otra puede ir por delante hasta ... antes de pisarse (paso 0,05) | y deja de pisarse a partir de')
for bajo in [0, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 25]:
    prim = None; ult = None; vmax = 0
    for i in range(1, 400):
        dif = 0.05 * i
        v = vol(puerta(1, bajo + dif), puerta(-1, bajo))
        if v > 1e-5:
            if prim is None: prim = dif
            ult = dif; vmax = max(vmax, v)
        elif prim is not None: break
    if prim is None: print('  %5.1f | no se pisan con ninguna diferencia hasta 20' % bajo)
    else: print('  %5.1f | se pisan si la otra va %.2f grados o mas por delante (hasta %.2f; volumen max %.1f mm3)' % (bajo, prim, ult, vmax))
# donde
A, B = puerta(1, 5 + 2.2), puerta(-1, 5)
print('ejemplo: derecha a 7,2 e izquierda a 5,0: volumen %.2f mm3 en la caja %s' % (vol(A, B), centro_inter(A, B)))
A, B = puerta(1, 5), puerta(-1, 5 + 2.2)
print('ejemplo: derecha a 5,0 e izquierda a 7,2: volumen %.2f mm3 en la caja %s' % (vol(A, B), centro_inter(A, B)))
