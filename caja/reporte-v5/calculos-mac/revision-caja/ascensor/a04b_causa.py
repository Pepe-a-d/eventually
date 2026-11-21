# 4 (bis). De donde sale que el teton quede casi sin juego en la helice. Geometria exacta, un solo teton (el de 90), tau = 200.
import a04_teton_v as A
from comun import *
from shapely.geometry import Polygon
import shapely
p_, d_ = p, d
rt = A.rt; zc0 = A.zc0; k_h = A.k_h; hv0, hv1, r0, r1, r2, g0, g1 = A.hv0, A.hv1, A.r0, A.r1, A.r2, A.g0, A.g1
af = 90.0; tau = 200.0
a_sub = af + p['giro_sube']; centro0 = a_sub - g0
def trap_modelo():
    return Polygon([CP.pol(r0, centro0 - g0), CP.pol(r1, centro0 - g0), CP.pol(r2, centro0 - g1), CP.pol(r2, centro0 + g1), CP.pol(r1, centro0 + g0), CP.pol(r0, centro0 + g0)])
def trap_v_verdadera(n=60):
    """La misma V, pero con los lados curvos en planta para que en cada corte radial la pared sea una recta (angulo proporcional al radio)."""
    izq = [CP.pol(r1 + (r2 - r1) * i / n, centro0 - (g0 + (g1 - g0) * i / n)) for i in range(n + 1)]
    der = [CP.pol(r1 + (r2 - r1) * i / n, centro0 + (g0 + (g1 - g0) * i / n)) for i in range(n, -1, -1)]
    return Polygon([CP.pol(r0, centro0 - g0)] + izq + der + [CP.pol(r0, centro0 + g0)])
def juego_vertical(trap, signo, radio_teton_extra=0.0):
    X, Y, Z, AA, PH = A.puntos_teton(af, na=60, nphi=720)
    h = D.movimiento(p, d, tau)[3]
    a = math.radians(-ROT * tau)
    xt = X * math.cos(a) - Y * math.sin(a); yt = X * math.sin(a) + Y * math.cos(a)
    zz0 = zc0 - hv0; zz1 = zc0 + d['recorrido'] + hv0; giro = (d['recorrido'] + 2 * hv0) / k_h
    def libre(dz):
        z = Z + h + dz
        tw = np.radians(giro * (z - zz0) / (zz1 - zz0))
        xr = xt * np.cos(-tw) - yt * np.sin(-tw); yr = xt * np.sin(-tw) + yt * np.cos(-tw)
        return bool((shapely.contains_xy(trap, xr, yr) | (np.hypot(xt, yt) < p['tubo_r'])).all())
    lo, hi = 0.0, 0.6
    if not libre(0.0): return -1.0
    while hi - lo > 0.0005:
        m_ = (lo + hi) / 2
        if libre(signo * m_): lo = m_
        else: hi = m_
    return lo
beta = math.degrees(math.atan(d['rampa_paso'] / (2 * math.pi * p['tubo_r'])))
print('pendiente de la helice en la boca (r = 76): %.2f grados' % beta)
print('holgura vertical que da el diseno en un tramo SIN pendiente (V del modelo): %.3f mm en la boca' % (hv0 - rt))
print('efecto de la pendiente sobre un teton redondo de radio 3: 3 x (1/cos(beta) - 1) = %.3f mm' % (rt * (1 / math.cos(math.radians(beta)) - 1)))
P1 = np.array(CP.pol(r1, -g0)); P2 = np.array(CP.pol(r2, -g1)); M = (P1 + P2) / 2
rm = np.hypot(*M); am = -math.degrees(math.atan2(M[1], M[0]))
g_nom = g0 + (g1 - g0) * (rm - r1) / (r2 - r1)
print('lado de la V en planta: recta de (r %.1f, %.2f grados) a (r %.1f, %.2f grados); en su punto medio (r = %.3f) queda a %.3f grados del centro, y la V recta pediria %.3f: %.3f grados menos = %.3f mm menos de media altura' % (r1, g0, r2, g1, rm, am, g_nom, g_nom - am, (g_nom - am) * k_h))
for nombre, t in (('V del modelo (lados rectos en planta)', trap_modelo()), ('V con lados curvos en planta (pared recta en el corte radial)', trap_v_verdadera())):
    print('%-62s juego vertical exacto: baja %.3f  sube %.3f mm' % (nombre, juego_vertical(t, -1), juego_vertical(t, 1)))
