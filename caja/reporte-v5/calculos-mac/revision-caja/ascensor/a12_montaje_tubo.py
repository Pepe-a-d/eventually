# Montaje: el tubo baja desde arriba sobre la plataforma (que ya esta en la base). Entra? Y girado 120 o 240 grados, se queda fuera?
from comun import *
pl = S['plataforma']; ba = S['base']
for giro in (0.0, 120.0, 240.0, 2.0, -2.0, 0.4, -0.4):
    tu = S['tubo'].rotate([0, 0, giro])
    peor = (0.0, None); primero = None; gmin = (9.0, None)
    for i in range(0, 221):
        dz = 110.0 - 0.5 * i
        t = tu.translate([0, 0, dz])
        v = vol(t, pl) + vol(t, ba)
        if v > 1e-3 and primero is None: primero = dz
        if v > peor[0]: peor = (v, dz)
        if giro == 0.0:
            g = t.min_gap(pl, 1.0)
            if g < gmin[0]: gmin = (g, dz)
    print('tubo girado %6.1f: %s' % (giro, 'baja hasta su sitio sin pisar nada' if primero is None else 'se para %.1f mm antes de llegar (pisa %.1f mm3 como mucho)' % (primero, peor[0])), ('; al bajar pasa a %.3f mm de la plataforma como minimo (a %.1f mm de su sitio)' % gmin) if giro == 0.0 else '')
print('entrada: +-2.7 grados a r = 76 son +-%.2f mm; teton de radio 3 -> %.2f mm por lado' % (76 * math.sin(math.radians(2.7)), 76 * math.sin(math.radians(2.7)) - 3))
