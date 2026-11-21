# Boca abajo / levantar con la una: que para a la puerta cerrada segun la altura real del aro, y la probeta del teton con pomo
from comun import *
EPS = 1e-4
def tr(ang, dz=0.0):
    return {n: gira_puerta(m, 1, ang).translate([0, 0, dz]) for n, m in (('bola', BOLA_D), ('varilla', VARILLA_D), ('cuerpo', CUERPO_D))}
print('puerta cerrada que se levanta (o se descuelga boca abajo), aro en psi = 0 centrado: primer contacto')
for nom, dza, dzp in (('aro como en el modelo (flotando 0,4 sobre el ala)', 0.0, 0.0), ('aro apoyado en el ala (caja de pie)', -0.4, 0.0), ('boca abajo: aro contra el plato (+0,4) y puerta caida 0,25 en su pasador', 0.4, 0.25), ('boca abajo: aro +0,4, puerta +0,40 (pasador tambien caido 0,15)', 0.4, 0.40)):
    A = aro(0.0).translate([0, 0, dza])
    v0 = {n: vol(m, A) for n, m in tr(0.0, dzp).items()}
    def pisa(a): return sum(vol(m, A) for m in tr(a, dzp).values()) > EPS
    if pisa(0.0):
        print('  %s: YA SE PISAN a 0 grados: %s' % (nom, {k: round(v, 4) for k, v in v0.items() if v > 0})); continue
    prev = 0.0; lim = None
    for i in range(1, 80):
        a = 0.1 * i
        if pisa(a): lim = bisec(pisa, prev, a, 8); break
        prev = a
    q = {n: round(vol(m, A), 4) for n, m in tr(lim + 0.15, dzp).items() if vol(m, A) > 0}
    g = {n: round(m.min_gap(A, 2), 3) for n, m in tr(0.0, dzp).items()}
    print('  %s: se para a %.2f grados (%.2f mm en el canto); toca %s; distancias a 0 grados %s' % (nom, lim, math.radians(lim) * 27.85, q, g))
print('PROBETA: teton con pomo, a lo largo de su recorrido, contra aro, marco, meseta y anillo')
gm = {}
for i in range(0, 53):
    s = 13.0 * i / 52; psi = 11.0 * s / 13.0
    T = S['probeta_teton'].translate([0, -s, 0])
    for n, c in (('aro', aro(psi)), ('marco', S['marco']), ('meseta', S['meseta']), ('anillo', S['probeta_anillo'])):
        v = vol(T, c); g = T.min_gap(c, 2.0)
        if n not in gm or g < gm[n][0] or v > gm[n][2]: gm[n] = (min(g, gm.get(n, (9,))[0]), s, max(v, gm.get(n, (0, 0, 0))[2]))
print('  ', {n: 'distancia minima %.3f mm (recorrido %.1f), volumen pisado max %.4f' % (g, s, v) for n, (g, s, v) in gm.items()})
bpt = S['probeta_teton'].bounding_box(); print('   pomo: de z %.2f a %.2f, radio 5; meseta abajo en %.2f; anillo abajo en -6.00; brazo arriba en %.2f' % (d['z_corr1'] + 0.6, bpt[5], d['z_meseta0'], d['z_corr1']))
