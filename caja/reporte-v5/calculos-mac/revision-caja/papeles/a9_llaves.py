# Cuanto "muerde" cada llave que impide montar una pieza girada: volumen pisado en las posiciones equivocadas, y si se salva con la holgura
from comun import *
print('funda girada y desplazada (tiene 0,5 mm de holgura por lado):')
for a in (90, 180, 270):
    f = S['funda'].rotate([0, 0, a]); mejor = min((vol(f.translate([dx, dy, 0]), S['cuerpo']) + vol(f.translate([dx, dy, 0]), S['base']) + vol(f.translate([dx, dy, 0]), S['bisel']), dx, dy) for dx in (-0.3, -0.15, 0, 0.15, 0.3) for dy in (-0.3, -0.15, 0, 0.15, 0.3))
    print('   %d grados: centrada pisa %.2f mm3; desplazada (%.2f, %.2f) pisa %.3f mm3 -> %s' % (a, vol(f, S['cuerpo']), mejor[1], mejor[2], mejor[0], 'ENTRA' if mejor[0] < 0.01 else 'no entra'))
b = bb(S['cuerpo']); print('   indice: sobresale %.2f mm del cuerpo; holgura de la funda %.2f por lado; canal de la funda %.1f de hondo' % (-b[1] - d['cuerpo_lado'] / 2, 0.5, 1.0))
print('otras llaves, en las posiciones equivocadas (mm3 pisados):')
for n, contra, angs, dz in (('cuerpo', ['base'], (90, 180, 270), 0.0), ('tubo', ['plataforma'], (120, 240, 118, 122, 238, 242), 2.0), ('plato', ['tubo'], (120, 240, 115, 125), 0.0), ('rueda_central', ['meseta'], (120, 240, 115, 125, 180), 0.0),
                           ('marco', ['base'], (120, 240, 112, 128), 0.0), ('plataforma', ['base'], (120, 240, 112, 128), 0.0), ('meseta', ['marco'], (90, 180), 0.0), ('probeta_anillo', ['meseta'], (120, 240, 180), 0.0)):
    print('   %-14s' % n, {a: round(sum(vol(S[n].rotate([0, 0, a]).translate([0, 0, dz]), S[q]) for q in contra), 1) for a in angs})
# el cuerpo girado: se salva con la holgura de las cajeras?
for a in (90, 180, 270):
    c = S['cuerpo'].rotate([0, 0, a]); print('   cuerpo a %d: pestillo ancho 20 mm contra cajera de %.1f mm -> pisa %.1f mm3' % (a, 12.6, vol(c, S['base'])))
