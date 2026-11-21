# Eventually, caja v5. Revision de la probeta del iris por la sesion del Mac (21-nov-2026).
# Solo necesita numpy. Se ejecuta desde la raiz del repositorio:
#     python3 caja/reporte-v5/calculos-mac/apilado_iris.py
# Lee caja/iris-v5.json (lo escribe iris_diseno_v5.py) y hace dos cosas:
#   1. Repite el apilado de las laminas punto a punto, en una rejilla, sin shapely.
#   2. Calcula cuanto tiene que inclinarse de lado cada lamina segun lo cerrado que este el iris,
#      y estima la fuerza entre laminas. ESTIMADO: lo tiene que confirmar la pieza impresa.
import json, math, os
import numpy as np

RAIZ = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(RAIZ, '..', '..', 'iris-v5.json'), encoding='utf-8'))
lam0 = np.array(D['lamina']); E = np.array(D['eje']); N = 8; paso = 360.0 / N
RA = D['d']['RA']

def rotm(a):
    a = math.radians(a); return np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])

def dentro(P, poly):
    x, y = P[:, 0], P[:, 1]; c = np.zeros(len(P), bool)
    x1, y1 = poly[:, 0], poly[:, 1]; x2, y2 = np.roll(x1, -1), np.roll(y1, -1)
    for i in range(len(poly)):
        cond = ((y1[i] > y) != (y2[i] > y))
        xi = (x2[i] - x1[i]) * (y - y1[i]) / (y2[i] - y1[i] + 1e-30) + x1[i]
        c ^= cond & (x < xi)
    return c

h = 0.35                                                   # paso de la rejilla, mm
gx = np.arange(-68, 68.01, h); X, Y = np.meshgrid(gx, gx); G = np.c_[X.ravel(), Y.ravel()]
G = G[np.hypot(G[:, 0], G[:, 1]) < 66]

def mascara(giro, k):
    """Puntos de la rejilla que caen dentro de la lamina k cuando ha girado 'giro' grados."""
    Gk = (rotm(-paso * k) @ G.T).T
    return dentro((rotm(-giro) @ (Gk - E).T).T + E, lam0)

def z_k(abc, k, pts):
    """Altura del plano medio de la lamina k (plano de la lamina 0, girado)."""
    q = (rotm(-paso * k) @ pts.T).T
    return abc[0] * q[:, 0] + abc[1] * q[:, 1] + abc[2]

print('1. APILADO, punto a punto')
for juego, t in (('A', 1.2), ('B', 0.8)):
    print('  juego %s, grosor %.1f mm' % (juego, t))
    filas = D['planos'][juego]
    for i, (g, cede, abc) in enumerate(filas):
        if i % 3 and i != len(filas) - 1: continue
        M = [mascara(g, k) for k in range(N)]
        txt = []
        for k in (1, 2, 3):
            ov = M[0] & M[k]
            if ov.sum() * h * h < 0.05:
                txt.append('con la %d no se toca' % k); continue
            pts = G[ov]; dif = z_k(abc, k, pts) - z_k(abc, 0, pts); j = dif.argmin()
            txt.append('con la %d: %.0f mm2, se pisan %.2f mm a %.0f mm del centro' % (k, ov.sum() * h * h, t - dif.min(), math.hypot(*pts[j])))
        pts = G[M[0]]; zb = z_k(abc, 0, pts) - t / 2
        print('    giro %4.1f (el PC da %.2f) | %s | la cara de abajo queda a %.2f mm o mas del plato' % (g, cede, ' ; '.join(txt), zb.min()))

print()
print('2. LA ESCALERA DE CARACOL')
print('  Ocho laminas en rueda, cada una sobre la anterior: cada lamina tiene que bajar un grueso dentro de su ancho.')
G_PLA = 1100.0                                              # MPa, modulo de torsion del PLA. SUPUESTO
INTEGRAL = 4.0                                              # integral de ds/ancho a lo largo de la lamina. ESTIMADO
tope = 0.2 / (2.6 + 3.3)                                    # inclinacion que deja la cola: 0,2 de juego entre isla (2,6) y cola (3,3)
baja = tope * 2 * math.sin(math.radians(paso / 2))          # lo que baja un plano rigido en 45 grados, por mm de radio
print('  La cola deja inclinar la lamina %.2f grados.' % math.degrees(tope))
for t in (1.2, 0.8, 0.6, 0.4):
    print('  grosor %.1f mm: apila sin deformarse con el agujero por encima de %.0f mm' % (t, 2 * t / baja))
    for rho in (20, 15, 10, 7.5, 5, 2.5):
        s = N * t / (2 * math.pi * rho)                     # pendiente a lo largo de la circunferencia
        phi = max(0.0, s - baja / (2 * math.pi / N))        # lo que tiene que poner la torsion
        T = phi * G_PLA * t ** 3 / (3 * INTEGRAL)           # par de torsion, N.mm
        F = T / (2 * math.pi * rho / N)                     # fuerza entre laminas, N
        print('      agujero de %4.0f mm: inclinacion %4.1f grados; fuerza entre laminas, unos %.2f N (%.0f g)' % (2 * rho, math.degrees(math.atan(s)), F, F * 1000 / 9.81))

print()
print('3. LO QUE EMPUJA EL DEDO')
brazo = math.hypot(E[0] - D['teton'][0], E[1] - D['teton'][1])
print('  El aro gira %.1f grados y la lamina %.1f: relacion %.2f. Brazo del teton, %.1f mm.' % (abs(D['giro_aro']), D['giro_lamina'], D['giro_lamina'] / abs(D['giro_aro']), brazo))
for F in (3, 5, 10):
    Tb = F * 75.75 / N / 43.0 * brazo * 0.8                 # par en cada lamina, N.mm (rendimiento 0,8)
    print('  dedo de %2d N en la orejeta: %.0f N.mm por lamina; vence unos %.2f N entre laminas (rozamiento 0,3; dos contactos a 60 mm del poste)' % (F, Tb, Tb / (2 * 0.3 * 60)))
