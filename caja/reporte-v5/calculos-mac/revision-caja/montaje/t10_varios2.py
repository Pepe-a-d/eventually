# a) boca abajo con el tubo a 70 grados (puertas a medio abrir): hasta donde caen soporte + reloj
# b) de lado: la oreja del tubo y la pared del cuerpo; el bisel y el labio del cuerpo
# c) el pasillo de montaje de las puertas: con que holgura entra la puerta de pie (se desplaza la puerta en X e Y y se repite el camino)
from comun import *
from t1_pasos_fn import camino
print('a) boca abajo, tubo a 70 grados')
Mt = {n: puesta(n, 70.0) for n in DENTRO}
e = 0.0; c = []
while e < 150:
    c = []
    for g_ in ('soporte', 'reloj_de_pega'): c += choque(Mt[g_].translate([0, 0, e + 0.25]), {k: v for k, v in Mt.items() if k not in ('soporte', 'reloj_de_pega')}, 0.05)
    if c: break
    e += 0.25
print('   soporte + reloj caen %.2f mm y los para %s' % (e, c))
print('b) holgura minima entre la oreja del tubo y el cuerpo al girar (tubo centrado), y con el tubo desplazado 0,5 mm hacia la pared:')
for tau in (37.5, 127.5, 217.5, 307.5):
    tb = puesta('tubo', tau); ang = math.radians(37.5 - tau)
    g0 = tb.min_gap(S['cuerpo'], 3.0)
    g1 = tb.translate([0.5 * math.cos(ang), 0.5 * math.sin(ang), 0]).min_gap(S['cuerpo'], 3.0)
    print('   tubo a %.1f (oreja hacia %4.0f grados): %.3f mm centrado; %.3f mm desplazado' % (tau, math.degrees(ang) % 360, g0, g1))
print('   bisel y cuerpo: holgura radial %.3f mm (labio) ; faldon del bisel y plato: %.3f mm' % (S['bisel'].min_gap(S['cuerpo'], 2.0), 0.5))
print('c) puerta de pie bajando 20 mm con el aro en abierto, desplazada (dx, dy) -> mm3 maximo que pisa (marco, meseta, aro)')
M = {'marco': S['marco'], 'meseta': S['meseta'], 'aro_puertas': puesta('aro_puertas', G)}
for dx, dy in ((0.1, 0), (-0.1, 0), (0.2, 0), (-0.2, 0), (0.25, 0), (-0.25, 0), (0, 0.2), (0, -0.2), (0, 0.3), (0, -0.3)):
    r = camino(puerta(1, 90).translate([dx, dy, 0]), M, desde=20.0)
    print('   dx %5.2f dy %5.2f: %s' % (dx, dy, {k: (v[0], v[1]) for k, v in r.items()} or 'no pisa'))
for da in (-2.0, -1.0, 1.0, 2.0):
    r = camino(puerta(1, 90 + da), M, desde=20.0)
    print('   puerta inclinada %+.0f grados respecto a la vertical: %s' % (da, {k: (v[0], v[1]) for k, v in r.items()} or 'no pisa'))
