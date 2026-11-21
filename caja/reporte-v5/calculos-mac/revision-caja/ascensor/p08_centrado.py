# 8. Planetario: que centra cada cosa y si el engrane se acuna dentro de las holguras del modelo.
# Los engranajes son prismas: se trabaja en 2D con los MISMOS poligonos que usa caja_piezas_v5.py (CP.engranaje).
from comun import *
from shapely.geometry import Point
from shapely.affinity import rotate as srot, translate as strans
from shapely.prepared import prep
m_ = p['modulo']; jd = p['juego_dientes']; zs, zp, zr = int(p['z_central']), int(p['z_satelite']), int(d['z_bisel'])
SOL = CP.engranaje(zs, m_, jd, fase=0.0)
VACIO = CP.engranaje(zr, m_, -jd, add=1.25, ded=1.0, fase=180.0 / zr)      # el hueco dentado del bisel: el satelite tiene que quedar dentro
R_EJ = d['r_ejes']; hg = p['holg_gira']
print('HOLGURAS RADIALES QUE CENTRAN (del modelo):')
L = d['cuerpo_lado'] / 2; pared_in = L - p['cuerpo_pared']
print('  bisel en el agujero del labio del cuerpo: %.3f mm por lado (radio del agujero %.3f, bisel %.3f)' % (0.4, d['bisel_r_ext'] + 0.4, d['bisel_r_ext']))
print('  ala del bisel contra la pared interior del cuerpo: %.3f' % (pared_in - d['bisel_ala_r']))
print('  faldon del bisel alrededor del plato: %.3f' % (d['tubo_r_ext'] + 0.5 - d['tubo_r_ext']))
print('  plato alrededor del cuello del marco: %.3f' % (d['plato_r_in'] - d['cuello_r']))
print('  satelite en su eje: %.3f (agujero %.2f, eje %.2f)' % (hg, 2.75 + hg, 2.75))
print('  tubo, abajo, en el aro de la base: %.3f ; cuerpo en la base: %.3f ; almenas tubo-plato: %.3f' % (hg + 0.1, p['holg_fija'], p['holg_fija']))
print('  comprobacion por malla: bisel-cuerpo dist min %.3f ; bisel-plato (lateral, plato 0.2 mas bajo) %.3f ; plato-marco %.3f ; tubo-base (tubo 0.3 mas alto) %.3f' % (
    gap(S['bisel'], S['cuerpo'], 2.0), gap(S['bisel'], S['plato'].translate([0, 0, -0.2]), 2.0), gap(S['plato'], S['marco'], 2.0), gap(S['tubo'].translate([0, 0, 0.3]), S['base'], 2.0)))
TOL = 2e-4      # mm2
def sat_pol(k, tau):
    """poligono del satelite k (1..6) en su sitio para el giro tau, y su centro"""
    th = 270.0 + 60.0 * (k - 1)
    fase = th * (1 + zs / zp) + 180.0 - 180.0 / zp
    c = CP.pol(R_EJ, th)
    g = strans(CP.engranaje(zp, m_, jd, fase=fase), c[0], c[1])
    dth = ROT * tau
    g = srot(g, dth * zs / zp, origin=c); g = srot(g, dth, origin=(0, 0))
    return g, CP.pol(R_EJ, th + dth)
def entorno(k, tau, e_b=(0.0, 0.0)):
    g, c = sat_pol(k, tau)
    zona = Point(c).buffer(14.0)
    sol = SOL.intersection(zona)
    vac = strans(srot(VACIO, ROT * tau / d['relacion'], origin=(0, 0)), e_b[0], e_b[1])
    muro = zona.difference(vac)                 # material del bisel cerca del satelite
    return g, c, sol, muro
def pisa(g, sol, muro):
    return g.intersection(sol).area, g.intersection(muro).area
DIRS = [(0.0, 0.0)] + [(r * math.cos(a), r * math.sin(a)) for r in (0.125, 0.25) for a in np.radians(np.arange(0, 360, 30))]
PSI = np.arange(-1.6, 1.6001, 0.04)
def cabe(k, tau, e_b, juego_eje=0.25, e_plato=(0.0, 0.0), detalle=False):
    """Hay alguna postura del satelite (dentro del juego de su eje, girado lo que quiera) que no pise ni central ni bisel?"""
    g, c, sol, muro = entorno(k, tau, e_b)
    mejor = None
    for dx, dy in DIRS:
        dx2, dy2 = dx * juego_eje / 0.25 + e_plato[0], dy * juego_eje / 0.25 + e_plato[1]
        cc = (c[0] + dx2, c[1] + dy2)
        gt = strans(g, dx2, dy2)
        for ps in PSI:
            gg = srot(gt, ps, origin=cc)
            a1, a2 = pisa(gg, sol, muro)
            if a1 < TOL and a2 < TOL:
                return True
            if mejor is None or a1 + a2 < mejor: mejor = a1 + a2
        if juego_eje == 0.0: break
    return False
# 0. en su sitio
print('\nEN SU SITIO (todo centrado): area que pisa cada satelite (mm2) en varias fases de diente')
for tau in (0.0, 0.5, 1.1, 2.3, 3.4, 4.0):
    out = []
    for k in range(1, 7):
        g, c, sol, muro = entorno(k, tau)
        a1, a2 = pisa(g, sol, muro); out.append('%.5f/%.5f' % (a1, a2))
    print('  tau %.1f: central/bisel ' % tau, ' '.join(out))
# 1. el satelite, movido lo que le deja su eje, con todo lo demas en su sitio y SIN dejarle girar ni acomodarse / dejandole girar
print('\nSATELITE MOVIDO 0.25 mm (el juego de su eje) en 12 direcciones, lo demas centrado. Si puede girar para acomodarse, cabe?')
for tau in (0.0, 1.1, 2.3):
    g, c, sol, muro = entorno(1, tau)
    fila = []
    for a in np.arange(0, 360, 30):
        dx, dy = 0.25 * math.cos(math.radians(a)), 0.25 * math.sin(math.radians(a))
        gt = strans(g, dx, dy); cc = (c[0] + dx, c[1] + dy)
        libres = [ps for ps in PSI if max(pisa(srot(gt, ps, origin=cc), sol, muro)) < TOL]
        fila.append('%3d:%s' % (a, ('%.2f' % (max(libres) - min(libres) + 0.04)) if libres else 'NO'))
    print('  tau %.1f, sat 1 (direccion en grados : abanico de giro libre en grados, NO = no cabe): ' % tau, ' '.join(fila))
# 2. el bisel empujado de lado
print('\nBISEL EMPUJADO DE LADO e mm hacia la direccion phi. Maximo e en el que TODOS los satelites aun caben (paso 0.025):')
print('   (a) satelites en su sitio exacto (ejes sin juego)   (b) con el juego de 0.25 de sus ejes, plato quieto   (c) plato tambien libre 0.30')
for tau in (0.0, 1.1, 2.3, 3.4):
    for phi in (90.0, 105.0, 120.0):          # hacia fuera del satelite 1 (270): lo aprieta contra la central; 120: entre dos satelites
        res = []
        for modo in ('a', 'b', 'c'):
            e = 0.0; quien = '-'
            while e < 0.9:
                e2 = e + 0.025
                eb = (e2 * math.cos(math.radians(phi)), e2 * math.sin(math.radians(phi)))
                ok = True
                for k in range(1, 7):
                    if modo == 'a': c_ = cabe(k, tau, eb, 0.0)
                    elif modo == 'b': c_ = cabe(k, tau, eb, 0.25)
                    else: c_ = any(cabe(k, tau, eb, 0.25, (f * eb[0] / e2, f * eb[1] / e2)) for f in (0.0, 0.15, 0.30))
                    if not c_: ok = False; quien = 'sat %d' % k; break
                if not ok: break
                e = e2
            res.append('%.3f (%s)' % (e, quien))
        print('  tau %.1f phi %5.1f:  (a) %s   (b) %s   (c) %s' % (tau, phi, res[0], res[1], res[2]))
print('  El agujero del cuerpo deja al bisel 0.40 mm; si el cuerpo se va 0.15 en la base, 0.55.')
