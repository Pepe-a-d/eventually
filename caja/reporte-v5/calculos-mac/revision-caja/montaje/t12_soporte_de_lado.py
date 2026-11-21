# El soporte con el reloj, de lado: cuanto resbalan sobre el pedestal (nada los guia salvo un iman) y que los para.
from comun import *
for tau in (0.0, 345.0):
    Mt = {n: puesta(n, tau) for n in DENTRO}
    otros = {k: v for k, v in Mt.items() if k not in ('soporte', 'reloj_de_pega')}
    for nombre, g in (('+X', (1, 0, 0)), ('-X', (-1, 0, 0)), ('+Y', (0, 1, 0)), ('-Y', (0, -1, 0))):
        e = 0.0; c = []
        while e < 60:
            c = []
            for n in ('soporte', 'reloj_de_pega'): c += choque(Mt[n].translate([g[0] * (e + 0.25), g[1] * (e + 0.25), 0]), otros, 0.05)
            if c: break
            e += 0.25
        print('tubo a %3.0f, gravedad hacia %s: soporte + reloj resbalan %s' % (tau, nombre, ('%.2f mm y los para %s' % (e, sorted(set(x[0] for x in c)))) if c else 'mas de 60 mm: nada los para'))
