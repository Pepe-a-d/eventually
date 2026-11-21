# Comprobacion 4: juego real de cada puerta segun la posicion del aro, y juego del propio aro
from comun import *
EPS = 1e-4
def limite(sx, psi, ang0, signo, aro_m, contra_extra=(), tope=30.0):
    """Cuantos grados gira la puerta desde ang0 en el sentido 'signo' hasta pisar el aro (o lo de contra_extra). Paso fino + biseccion."""
    cuerpos = [aro_m] + list(contra_extra)
    f = lambda dl: sum(vol(puerta(sx, ang0 + signo * dl), c) for c in cuerpos) > EPS
    prev = 0.0
    for i in range(1, int(tope / 0.25) + 1):
        dl = 0.25 * i
        if f(dl): return bisec(f, prev, dl, 10)
        prev = dl
    return None
def quien(sx, psi, ang, aro_m):
    r = []
    for nom, m in (('bola', BOLA_D), ('varilla', VARILLA_D), ('cuerpo', CUERPO_D)):
        v = vol(gira_puerta(m, sx, ang), aro_m)
        if v > 0: r.append('%s-aro %.4f' % (nom, v))
        v = vol(gira_puerta(m, sx, ang), S['meseta'])
        if v > 0: r.append('%s-meseta %.4f' % (nom, v))
    return ', '.join(r)
print('A) aro en su sitio exacto (sin su juego). Angulo nominal de la puerta y lo que se deja mover en cada sentido')
casos = [('psi = 0 (cerrado, tubo 0..45)', 0.0), ('mitad del reposo de cerrado', 1.25), ('final del reposo de cerrado', 2.5), ('cambio, 1/4', 4.0), ('mitad del cambio', 5.5), ('cambio, 3/4', 7.0),
         ('principio del reposo de abierto', 8.5), ('mitad del reposo de abierto', 9.75), ('psi = 11 (abierto)', 11.0)]
for nom, psi in casos:
    ang0 = 45.0 - math.degrees(math.asin(D.bola_x(p, d, psi) / p['manivela_r']))
    for sx in (1, -1):
        A = aro(psi)
        v0 = vol(puerta(sx, ang0), A)
        up = limite(sx, psi, ang0, +1, A); dn = limite(sx, psi, ang0, -1, A)
        upm = limite(sx, psi, ang0, +1, A, [S['meseta']]); dnm = limite(sx, psi, ang0, -1, A, [S['meseta']])
        f = lambda v: ('%.2f' % v) if v is not None else '>30'
        print('  %-34s %s  nominal %6.2f  | solo aro: abre %s, cierra %s | aro+meseta: abre %s, cierra %s | toca al abrir: %s | al cerrar: %s' % (
            nom, 'D' if sx > 0 else 'I', ang0, f(up), f(dn), f(upm), f(dnm),
            quien(sx, psi, ang0 + (upm or 0) + 0.3, A) if upm is not None else '-', quien(sx, psi, ang0 - (dnm or 0) - 0.3, A) if dnm is not None else '-'))
