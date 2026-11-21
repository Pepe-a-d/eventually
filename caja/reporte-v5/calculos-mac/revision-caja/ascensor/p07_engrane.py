# 7. Planetario: barrido fino del engrane y juego real
from comun import *
sats = ['satelite_%d' % i for i in range(1, 7)]
ce = S['rueda_central']
print('Barrido: tubo de 0 a 12 grados en pasos de 0.05 (los satelites giran 78 grados sobre su eje: 2.6 pasos de diente)')
filas = []
t0 = time.time()
for i in range(241):
    tau = 0.05 * i
    bi = puesta('bisel', tau)
    for s in sats:
        m = puesta(s, tau)
        filas.append((tau, int(s[-1]), vol(m, ce), gap(m, ce, 1.0), vol(m, bi), gap(m, bi, 1.0)))
a = np.array(filas)
print('tiempo %.0f s' % (time.time() - t0))
for k in range(1, 7):
    s = a[a[:, 1] == k]
    print('  satelite %d: con rueda central vol max %.4f mm3 (tau %.2f), dist min %.4f (tau %.2f), dist max %.4f | con bisel vol max %.4f (tau %.2f), dist min %.4f (tau %.2f), dist max %.4f' % (
        k, s[:, 2].max(), s[s[:, 2].argmax(), 0], s[:, 3].min(), s[s[:, 3].argmin(), 0], s[:, 3].max(), s[:, 4].max(), s[s[:, 4].argmax(), 0], s[:, 5].min(), s[s[:, 5].argmin(), 0], s[:, 5].max()))
np.save('p07_res.npy', a)
# otros giros de tubo sueltos, para ver que la fase se mantiene en todo el recorrido
print('Otros giros (cada 7.3 grados hasta 345), todos los satelites: ', end='')
pv = 0; pg = 9
for tau in np.arange(0, 345.01, 7.3):
    bi = puesta('bisel', tau)
    for s in sats:
        m = puesta(s, tau)
        pv = max(pv, vol(m, ce), vol(m, bi)); pg = min(pg, gap(m, ce, 1.0), gap(m, bi, 1.0))
print('vol max %.4f, dist min %.4f' % (pv, pg))
# juego real
def gira_sat(k, tau, ang):
    th = 270.0 + 60.0 * (k - 1); c = pol(d['r_ejes'], th + ROT * tau)
    return puesta('satelite_%d' % k, tau).translate([-c[0], -c[1], 0]).rotate([0, 0, ang]).translate([c[0], c[1], 0])
UMB = 1e-3
def juego_sat(k, tau, contra, signo, paso=0.01):
    v = 0.0
    while v < 6:
        if any(vol(gira_sat(k, tau, signo * (v + paso)), c) > UMB for c in contra): return v
        v += paso
    return v
print('\nJuego de un satelite girando sobre su eje con todo lo demas quieto (grados; en mm en su primitivo r=9):')
for tau in (0.0, 0.7, 1.3, 2.0, 100.0, 233.3, 345.0):
    bi = puesta('bisel', tau)
    for k in (1, 2, 4):
        jc = (juego_sat(k, tau, [ce], 1), juego_sat(k, tau, [ce], -1)); jb = (juego_sat(k, tau, [bi], 1), juego_sat(k, tau, [bi], -1)); jt = (juego_sat(k, tau, [ce, bi], 1), juego_sat(k, tau, [ce, bi], -1))
        print('  tau %6.1f sat %d: solo contra central +%.2f/-%.2f (total %.3f mm) | solo contra bisel +%.2f/-%.2f (total %.3f mm) | contra los dos +%.2f/-%.2f (total %.3f mm)' % (
            tau, k, jc[0], jc[1], math.radians(sum(jc)) * 9, jb[0], jb[1], math.radians(sum(jb)) * 9, jt[0], jt[1], math.radians(sum(jt)) * 9))
print('\nJuego del bisel con el tubo (y el plato) quieto: se gira el bisel y se busca si el satelite 1 encuentra algun giro en el que no pise ni al bisel ni a la central')
for tau in (0.0, 1.3, 100.0, 345.0):
    out = []
    for signo in (1, -1):
        v = 0.0
        while v < 3:
            v2 = v + 0.01
            bi = puesta('bisel', tau).rotate([0, 0, signo * v2])
            # el satelite sigue al bisel: giro del satelite = -giro_bisel * zr/zp (engrane interior: mismo sentido) -> se prueba un abanico
            ok = False
            for ang in np.arange(-1.5, 1.501, 0.02):
                m = gira_sat(1, tau, signo * v2 * d['z_bisel'] / p['z_satelite'] + ang)
                if vol(m, bi) <= UMB and vol(m, ce) <= UMB: ok = True; break
            if not ok: break
            v = v2
        out.append(v)
    print('  tau %6.1f: bisel +%.2f / -%.2f grados (total %.2f grados = %.2f mm en el canto del bisel, r=%.1f)' % (tau, out[0], out[1], sum(out), math.radians(sum(out)) * d['bisel_r_ext'], d['bisel_r_ext']))
