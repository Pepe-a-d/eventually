# 4. El teton conico en la V. Dos metodos independientes:
#   (A) mallas de manifold3d (helice por facetas): se mueve la plataforma hasta que pisa el tubo
#   (B) geometria EXACTA (sin facetas): puntos de la superficie del teton contra la definicion matematica de la ranura
#       (poligono en planta que sube girando = lo mismo que hace el 'sweep' con giro de Fusion)
from comun import *
from shapely.geometry import Polygon
import shapely
print('shapely', shapely.__version__)
hd = p['holg_desliza']; fondo = p['rampa_fondo']; rt = p['teton_plat_d'] / 2
zc0 = d2['zc0']; k_h = d['recorrido'] / (p['giro_arriba'] - p['giro_sube'])
hv0 = rt + hd; hv1 = hv0 - (fondo - 0.4)
r0 = p['tubo_r'] - 0.5; r1 = p['tubo_r']; r2 = p['tubo_r'] + fondo - 0.4 + hd
g0, g1 = hv0 / k_h, hv1 / k_h
print('k_h %.5f mm/grado; hv0 %.2f hv1 %.2f; r1 %.2f r2 %.2f; g0 %.3f g1 %.3f grados' % (k_h, hv0, hv1, r1, r2, g0, g1))
AF = (90.0, 212.0, 330.0)
perfil_v = [(r0, -hv0 - 0.05), (r1, -hv0 - 0.05), (r2 + 0.1, -hv1 - 0.05), (r2 + 0.1, hv1 + 0.05), (r1, hv0 + 0.05), (r0, hv0 + 0.05)]
PV = Polygon(perfil_v)
def en_hueco(x, y, z, af_list=AF):
    """True si el punto (coordenadas del TUBO) esta en aire: dentro del anima (r<76) o dentro de alguna ranura. Exacto."""
    r = np.hypot(x, y); th = np.degrees(np.arctan2(y, x))
    aire = r < p['tubo_r']
    for af in af_list:
        a_ini, a_sub, a_arr, a_fin = af - 3.0, af + p['giro_sube'], af + p['giro_arriba'], af + p['giro_tubo'] + 3.0
        # tramos planos (revolucion exacta)
        for (aa, ab, zz) in ((a_ini, a_sub, zc0), (a_arr, a_fin, zc0 + d['recorrido'])):
            dth = (th - aa) % 360.0
            dentro_ang = dth <= (ab - aa)
            aire |= dentro_ang & shapely.contains_xy(PV, r, z - zz)
        # helice exacta
        centro0 = a_sub - g0
        trap = Polygon([CP.pol(r0, centro0 - g0), CP.pol(r1, centro0 - g0), CP.pol(r2, centro0 - g1), CP.pol(r2, centro0 + g1), CP.pol(r1, centro0 + g0), CP.pol(r0, centro0 + g0)])
        zz0 = zc0 - hv0; zz1 = zc0 + d['recorrido'] + hv0; giro = (d['recorrido'] + 2 * hv0) / k_h
        tw = np.radians(giro * (z - zz0) / (zz1 - zz0))
        xr = x * np.cos(-tw) - y * np.sin(-tw); yr = x * np.sin(-tw) + y * np.cos(-tw)
        aire |= (z >= zz0) & (z <= zz1) & shapely.contains_xy(trap, xr, yr)
        # entrada
        dth = (th - (af - 2.7)) % 360.0
        aire |= (dth <= 5.4) & (r >= r0) & (r <= r2) & (z <= zc0)
    return aire
def puntos_teton(af, na=40, nphi=360):
    """Puntos de la superficie del teton (cilindro de r=75.3 a 76 y cono de 76 a 78.6) con la plataforma abajo, en el mundo."""
    a = np.concatenate([np.linspace(75.0, 76.0, 6), np.linspace(76.0, 78.6, na)])
    rho = np.where(a <= 76.0, rt, rt - (a - 76.0))
    phi = np.linspace(0, 2 * np.pi, nphi, endpoint=False)
    A, PH = np.meshgrid(a, phi, indexing='ij'); RHO = np.meshgrid(rho, phi, indexing='ij')[0]
    er = np.array([math.cos(math.radians(af)), math.sin(math.radians(af))]); et = np.array([-er[1], er[0]])
    X = A * er[0] + RHO * np.cos(PH) * et[0]; Y = A * er[1] + RHO * np.cos(PH) * et[1]; Z = zc0 + RHO * np.sin(PH)
    # la punta: disco de radio 0.4 en a = 78.6
    return X.ravel(), Y.ravel(), Z.ravel(), A.ravel(), PH.ravel()
def libre(tau, dz=0.0, dr=0.0, dx=0.0, dy=0.0, dth=0.0, afs=AF):
    """True si los tetones, con la plataforma a la altura de diseno + dz (y desplazada), no tocan material del tubo. Exacto."""
    h = D.movimiento(p, d, tau)[3]
    for af in afs:
        X, Y, Z, A, PH = puntos_teton(af)
        c, s = math.cos(math.radians(dth)), math.sin(math.radians(dth))
        X, Y = X * c - Y * s, X * s + Y * c
        er = (math.cos(math.radians(af)), math.sin(math.radians(af)))
        X = X + dx + dr * er[0]; Y = Y + dy + dr * er[1]; Z = Z + h + dz
        # al mundo -> al tubo: el tubo ha girado ROT*tau, asi que en el tubo el punto esta girado -ROT*tau
        a = math.radians(-ROT * tau)
        xt = X * math.cos(a) - Y * math.sin(a); yt = X * math.sin(a) + Y * math.cos(a)
        if not en_hueco(xt, yt, Z, (af,)).all(): return False
    return True
def juego(tau, eje, signo, paso=0.001, tope=1.5, **k):
    """Biseccion: mayor desplazamiento sin tocar (se supone que una vez toca, sigue tocando)."""
    def ok(v):
        kk = dict(k); kk[eje] = signo * v
        return libre(tau, **kk)
    if ok(tope): return tope
    lo, hi = 0.0, tope
    # primero un barrido basto para no saltarse el primer contacto
    v = 0.05
    while v < tope and ok(v): v += 0.05
    lo, hi = max(0.0, v - 0.05), min(v, tope)
    while hi - lo > paso:
        m = (lo + hi) / 2
        if ok(m): lo = m
        else: hi = m
    return lo
if __name__ == '__main__':
    print('\n(B) EXACTO. Juego de los tres tetones en sus ranuras con la plataforma a la altura de diseno:')
    print('  tau    baja    sube   (mm, hasta tocar el tubo; busqueda de 0.002 en 0.002)')
    for tau in (0, 45, 80, 90, 91, 92, 93, 94, 96, 100, 120, 150, 200, 250, 300, 330, 333, 334, 335, 336, 338, 340, 345):
        ok = libre(tau)
        print('  %5.1f  %s  %.3f  %.3f' % (tau, 'libre' if ok else 'PISA ', juego(tau, 'dz', -1) if ok else -1, juego(tau, 'dz', +1) if ok else -1))
    print('\n  Un solo teton (el de 90), juego hacia fuera en su radio (dr>0) y de toda la plataforma en X, Y:')
    for tau in (45, 200, 340):
        print('  tau %5.1f  un teton hacia fuera %.3f  hacia dentro %.3f | plataforma +X %.3f -X %.3f +Y %.3f -Y %.3f' % (tau, juego(tau, 'dr', 1, afs=(90.0,)), juego(tau, 'dr', -1, afs=(90.0,), tope=0.6),
              juego(tau, 'dx', 1), juego(tau, 'dx', -1), juego(tau, 'dy', 1), juego(tau, 'dy', -1)))
    # (A) mallas
    print('\n(A) MALLAS manifold3d (plataforma contra tubo, volumen comun > 0.001 mm3):')
    def juego_m(tau, signo, paso=0.005):
        pl = puesta('plataforma', tau); tu = puesta('tubo', tau)
        v = 0.0
        while v < 1.5:
            if vol(pl.translate([0, 0, signo * (v + paso)]), tu) > 1e-3: return v
            v += paso
        return 1.5
    for tau in (0, 45, 90, 93, 100, 150, 200, 250, 300, 333, 336, 340, 345):
        pl = puesta('plataforma', tau); tu = puesta('tubo', tau)
        print('  tau %5.1f  dist min %.4f  baja %.3f  sube %.3f' % (tau, gap(pl, tu, 1.0), juego_m(tau, -1), juego_m(tau, 1)))
