# Verificacion directa del caso peor de puerta abierta que se inclina hacia dentro, y distancia al reloj de pega
from comun import *
psi = 11.0
dx, dy = 0.29 * math.cos(math.radians(60)), 0.29 * math.sin(math.radians(60))
A = aro(psi, dx, dy)
print('aro desplazado (%.3f, %.3f): pisa marco %.5f, meseta %.5f, teton(nominal) %.5f mm3' % (dx, dy, vol(A, S['marco']), vol(A, S['meseta']), vol(A, mv('teton', 345))))
print('   distancia aro-marco %.3f, aro-meseta %.3f, aro-teton %.3f' % (A.min_gap(S['marco'], 1), A.min_gap(S['meseta'], 1), A.min_gap(mv('teton', 345), 1)))
for ang in (90, 88, 86, 84, 83, 82.5, 82.3, 82.0):
    print('   derecha a %.1f: pisa aro %.5f, meseta %.5f' % (ang, vol(puerta(1, ang), A), vol(puerta(1, ang), S['meseta'])))
for ang in (88, 90, 92, 93, 94, 95, 96):
    print('   izquierda a %.1f: pisa aro %.5f, meseta %.5f' % (ang, vol(puerta(-1, ang), A), vol(puerta(-1, ang), S['meseta'])))
print('distancia minima de cada puerta al reloj de pega, soporte y plataforma mientras sube (tubo 92..345, paso 1), segun lo que se incline la puerta hacia dentro')
for ang in (90.0, 87.15, 86.25, 84.0, 82.33):
    peor = {}
    for tau in np.arange(92, 345.01, 1.0):
        for n in ('reloj_de_pega', 'soporte', 'plataforma'):
            M = mv(n, tau)
            for sx in (1, -1):
                g = M.min_gap(puerta(sx, ang), 8.0)
                k = (n, sx)
                if g < peor.get(k, (99, 0))[0]: peor[k] = (g, tau)
    print('  puertas a %.2f: ' % ang + '; '.join('%s-%s %.2f mm (tubo %.0f)' % (n[:6], 'D' if sx > 0 else 'I', g, t) for (n, sx), (g, t) in sorted(peor.items())))
