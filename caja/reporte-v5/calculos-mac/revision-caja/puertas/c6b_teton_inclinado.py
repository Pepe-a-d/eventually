# Comprobacion 6 (segunda parte): cuanto puede inclinarse el teton dentro de sus tres ranuras
from comun import *
import itertools
EPS = 2e-4
def recorta(m, c, r=9.0):
    return m ^ mf.Manifold.cube([2 * r, 2 * r, 14]).translate([c[0] - r, c[1] - r, -23.0])
def inclinado(T0, c, eje, alfa, dx, dy, dz):
    """El teton girado 'alfa' grados alrededor de un eje horizontal que pasa por su centro, y desplazado."""
    m = T0.translate([-c[0], -c[1], -c[2]])
    m = m.rotate([alfa, 0, 0]) if eje == 'x' else m.rotate([0, alfa, 0])
    return m.translate([c[0] + dx, c[1] + dy, c[2] + dz])
def cabe(T0, c, eje, alfa, piezas, grid):
    mejor = (9e9, None)
    for dx, dy, dz in grid:
        T = inclinado(T0, c, eje, alfa, dx, dy, dz)
        v = sum(vol(T, q) for q in piezas)
        if v < mejor[0]: mejor = (v, (dx, dy, dz))
        if v <= EPS: return True, (dx, dy, dz)
    return False, mejor
def rejilla(ax, ay, az):
    return sorted(itertools.product(ax, ay, az), key=lambda t: abs(t[0]) + abs(t[1]) + abs(t[2]))
G1 = rejilla(np.arange(-0.4, 0.401, 0.1), np.arange(-0.6, 0.601, 0.1), (-0.3, -0.15, 0.0, 0.2, 0.4))
for tau in (0.0, 62.0, 72.5, 83.0, 345.0):
    s, psi, ang, h = D.movimiento(p, d, tau)
    T0 = mv('teton', tau); b = T0.bounding_box(); c = ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2)
    MA = recorta(S['marco'], c); PL = recorta(mv('plato', tau), c); AR = recorta(mv('aro_puertas', tau), c)
    print('tubo %.1f (teton en radio %.2f):' % (tau, c[1]))
    for nom, eje in (('en el plano radial (cabecea hacia dentro/fuera; gira sobre el eje X)', 'x'), ('en el plano tangencial (se tumba de lado; gira sobre el eje Y)', 'y')):
        for cual, piezas in (('con las tres ranuras (aro quieto)', [MA, PL, AR]), ('solo marco y plato (el aro cede)', [MA, PL]), ('solo marco y aro (sin plato: durante el montaje)', [MA, AR])):
            res = []
            for sg in (1, -1):
                ult = 0.0
                for a in np.arange(0.5, 25.01, 0.5):
                    ok, _ = cabe(T0, c, eje, sg * a, piezas, G1)
                    if not ok: break
                    ult = a
                res.append(ult)
            print('   %s, %s: hasta %+.1f / -%.1f grados' % (nom, cual, res[0], res[1]))
