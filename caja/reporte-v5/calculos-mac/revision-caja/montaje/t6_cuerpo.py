# El cuerpo y sus cuatro pestillos: interferencia, forma de las caras, superficie de enganche, y que mas lo sujeta.
from comun import *
cu, ba = S['cuerpo'], S['base']
L = d['cuerpo_lado'] / 2; pin = L - p['cuerpo_pared']; zs = d['z_suelo']
print('pared del cuerpo: cara interior a %.3f mm del eje; aro de la base por fuera a %.3f; pestillo llega a %.3f (escalon de arriba a %.3f)' % (pin, pin - p['holg_fija'], pin - p['holg_fija'] + 1.0, pin - p['holg_fija'] + 0.5))
print('interferencia que hay que vencer por lado: %.2f mm (primero %.2f mm en el escalon de arriba)' % (1.0 - p['holg_fija'], 0.5 - p['holg_fija']))
print('alturas sobre el suelo de la base: pestillo de 2,2 a 3,4 (1 mm) y de 3,4 a 4,0 (0,5 mm); cajera del cuerpo de 1,9 a 4,4')
print('bajando el cuerpo (mm sobre su sitio -> mm3 que pisa a la base):')
for e in (5.0, 4.5, 4.0, 3.9, 3.5, 3.4, 3.0, 2.5, 2.0, 1.5, 1.0, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0):
    print('   %.1f: %7.2f' % (e, vol(cu.translate([0, 0, e]), ba)))
# cara con la que el cuerpo se encuentra el pestillo al bajar: seccion de la interferencia justo al empezar
i0 = cu.translate([0, 0, 3.95]) ^ ba
for q in i0.decompose():
    b = q.bounding_box(); print('   al llegar (3,95 mm): trozo %.3f mm3, x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f' % (q.volume(), b[0], b[3], b[1], b[4], b[2], b[5]))
print('  -> el canto de abajo del cuerpo (arista viva) cae sobre un escalon horizontal de %.2f mm de ancho: no hay rampa de entrada' % (0.5 - p['holg_fija']))
# una vez puesto: subir el cuerpo
print('una vez puesto, subiendo el cuerpo (mm -> mm3 contra la base):')
for e in (0.1, 0.2, 0.3, 0.4, 0.5, 1.0):
    print('   %.1f: %7.2f' % (e, vol(cu.translate([0, 0, e]), ba)))
i1 = cu.translate([0, 0, 0.5]) ^ ba
area = 0.0
for q in i1.decompose():
    b = q.bounding_box(); a_ = (b[3] - b[0]) * (b[4] - b[1]); area += a_
    print('   enganche: trozo x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f -> %.1f mm2 en planta' % (b[0], b[3], b[1], b[4], b[2], b[5], a_))
print('   superficie total de enganche de los cuatro pestillos: %.1f mm2; fondo del enganche %.2f mm; juego en altura antes de engancharse %.2f mm' % (area, 1.0 - p['holg_fija'], 0.3))
# hueco para hacer palanca: distancia entre cuerpo y base por fuera
print('junta cuerpo/base por fuera: el cuerpo acaba en z = %.2f y la base empieza en z = %.2f; las dos caras exteriores estan a %.3f y %.3f mm del eje: enrasadas, sin ranura para palanca' % (cu.bounding_box()[2], zs, L, L))
# que mas impide subir al cuerpo: se quitan los pestillos de la cuenta (base sin pestillos = se compara contra todo menos la base)
M = {n: puesta(n, 0) for n in DENTRO if n not in ('cuerpo', 'base')}
print('subiendo el cuerpo solo, contra todo menos la base (mm -> lo que pisa):')
for e in (0.2, 0.4, 0.5, 1.0, 2.0):
    print('   %.1f: %s' % (e, choque(cu.translate([0, 0, e]), M) or 'nada'))
print('subiendo cuerpo + bisel juntos, contra todo lo demas menos la base:')
M2 = {n: v for n, v in M.items() if n != 'bisel'}
for e in (0.2, 0.3, 0.4, 0.5, 1.0, 2.0):
    print('   %.1f: %s' % (e, (choque(cu.translate([0, 0, e]), M2) + choque(S['bisel'].translate([0, 0, e]), M2)) or 'nada'))
M3 = {n: v for n, v in M2.items() if n != 'rueda_central'}
print('subiendo cuerpo + bisel + rueda central, contra el resto menos la base:')
for e in (0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 60.0, 120.0):
    c = choque(cu.translate([0, 0, e]), M3) + choque(S['bisel'].translate([0, 0, e]), M3) + choque(S['rueda_central'].translate([0, 0, e]), M3)
    print('   %.1f: %s' % (e, c or 'nada'))
# superficie del labio del cuerpo sobre el ala del bisel
ala = S['bisel'].translate([0, 0, 1.0]) ^ cu
b = ala.bounding_box(); print('labio del cuerpo sobre el ala del bisel: solape en planta %.0f mm2 (corona de %.2f a %.2f mm de radio); aire en altura %.2f mm' % (ala.volume() / (1.0 - 0.4), d['bisel_r_ext'] + 0.4, d['bisel_ala_r'], 0.4))
# volumen (peso si fuera macizo) que cuelga de los pestillos al levantar la caja de pie cogiendola por el cuerpo
cuelga = [n for n in DENTRO if n not in ('cuerpo',)]
vtot = sum(S[n].volume() for n in cuelga) / 1000.0
print('de pie, levantando la caja por el cuerpo, cuelga de los cuatro pestillos todo lo demas: %.0f cm3 si fuera macizo (%.2f kg a 1,24 g/cm3; con relleno, menos) mas el reloj de verdad' % (vtot - S['reloj_de_pega'].volume() / 1000.0, (vtot - S['reloj_de_pega'].volume() / 1000.0) * 1.24 / 1000.0))
