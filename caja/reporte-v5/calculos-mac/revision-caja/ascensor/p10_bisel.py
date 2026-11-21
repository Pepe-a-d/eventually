# 10. El bisel: que lo sostiene, que le impide salir, superficies de apoyo tubo -> plato -> bisel, y que lo centra de verdad
from comun import *
UMB = 1e-3
def seccion(m, z):
    return m.slice(z)
def area_comun(a, za, b, zb):
    return (a.slice(za) ^ b.slice(zb)).area()
bi, pl, tu, ba, cu, ce = S['bisel'], S['plato'], S['tubo'], S['base'], S['cuerpo'], S['rueda_central']
e = 0.02
print('ALTURAS: bisel de z = %.2f a %.2f ; plato de %.2f a %.2f ; tubo de %.2f a %.2f (almenas hasta %.2f) ; pista de la base hasta %.2f' % (bi.bounding_box()[2], bi.bounding_box()[5], d['z_plato0'], d['z_plato1'], d['z_suelo'] + 0.6, d['z_plato0'], d['z_plato0'] + 2.8, d['z_suelo'] + 0.6))
print('APOYOS (superficie comun de las dos caras que se tocan, mm2):')
print('   bisel sobre plato, en z = %.2f: %.1f mm2 (anillo de r %.3f a %.3f)' % (d['z_plato1'], area_comun(bi, d['z_plato1'] + e, pl, d['z_plato1'] - e), d['bisel_fondo'] + 0.2, d['tubo_r_ext']))
print('   plato sobre tubo, en z = %.2f: %.1f mm2' % (d['z_plato0'], area_comun(pl, d['z_plato0'] + e, tu, d['z_plato0'] - e)))
print('      (cara de abajo del plato %.1f mm2, de la que estan sobre el tubo las de arriba; canto del tubo %.1f mm2)' % (pl.slice(d['z_plato0'] + e).area(), tu.slice(d['z_plato0'] - e).area()))
print('   tubo sobre la pista de la base, en z = %.2f: %.1f mm2 (canto de abajo del tubo: %.1f mm2 a 0.02 del canto, %.1f a 0.2)' % (d['z_suelo'] + 0.6, area_comun(tu, d['z_suelo'] + 0.6 + e, ba, d['z_suelo'] + 0.6 - e), tu.slice(d['z_suelo'] + 0.6 + e).area(), tu.slice(d['z_suelo'] + 0.8).area()))
print('   holgura en altura almena-cajera: %.2f' % 0.2)
print('DISTANCIAS en su sitio: bisel-plato %.4f ; plato-tubo %.4f ; tubo-base %.4f ; bisel-cuerpo %.4f ; bisel-rueda_central %.4f ; bisel-tubo %.4f ; plato-rueda_central %.4f ; plato-marco %.4f ; plato-aro %.4f' % (
    gap(bi, pl, 2), gap(pl, tu, 2), gap(tu, ba, 2), gap(bi, cu, 2), gap(bi, ce, 2), gap(bi, tu, 2), gap(pl, ce, 2), gap(pl, S['marco'], 2), gap(pl, S['aro_puertas'], 2)))
print('QUE LE IMPIDE SALIR: ala del bisel hasta r = %.3f, cara de arriba z = %.2f ; labio del cuerpo: agujero r = %.3f, cara de abajo z = %.2f -> sube %.2f y solapa %.3f mm de radio' % (
    d['bisel_ala_r'], d['z_cuerpo_arriba'] - 3.0 - p['aire'], d['bisel_r_ext'] + 0.4, d['z_cuerpo_arriba'] - 3.0, p['aire'], d['bisel_ala_r'] - (d['bisel_r_ext'] + 0.4)))
print('   con el bisel descentrado 0.4: solape minimo del ala bajo el labio = %.3f mm' % (d['bisel_ala_r'] - (d['bisel_r_ext'] + 0.4) - 0.4))
# apretar hacia abajo: bajar el bisel 0.1 y ver que pisa
print('APRETAR HACIA ABAJO: bisel 0.1 mm mas abajo, volumen que pisa a cada pieza:')
for n in ('plato', 'tubo', 'rueda_central', 'cuerpo', 'base', 'satelite_1', 'satelite_2', 'meseta', 'marco'):
    print('   %-14s %.3f mm3' % (n, vol(bi.translate([0, 0, -0.1]), S[n])))
print('   (los satelites: la cara de arriba, z = %.2f, coincide con el techo del bisel; debajo tienen %.2f hasta el plato)' % (d['z_engr1'], d['z_engr0'] - d['z_plato1']))
# empujar de lado: que toca primero
print('EMPUJAR EL BISEL DE LADO (todo lo demas en su sitio, tau = 0): desplazamiento al que empieza a pisar cada pieza, por direccion')
for phi in (0.0, 15.0, 30.0, 90.0, 270.0, 300.0):
    fila = []
    for n in ('rueda_central', 'cuerpo', 'plato', 'satelite_1', 'satelite_2', 'satelite_3', 'satelite_4', 'satelite_5', 'satelite_6'):
        v = 0.0
        while v < 1.0:
            v2 = v + 0.01
            if vol(bi.translate([v2 * math.cos(math.radians(phi)), v2 * math.sin(math.radians(phi)), 0]), S[n]) > UMB: break
            v = v2
        fila.append('%s %.2f' % (n.replace('satelite_', 's').replace('rueda_central', 'dedos'), v))
    print('   phi %5.1f: %s' % (phi, ' | '.join(fila)))
print('   dedos de la rueda central: punta arriba r = %.2f, abajo r = %.2f ; cono del techo del bisel: arriba r = %.2f, abajo (z = %.2f) r = %.2f' % (d2['r_dedo0'], d2['r_dedo0'] + p['esqueleto_grueso'], d2['r_techo0'], d['z_engr1'], d['bisel_punta']))
# donde pisa el bisel a la rueda central al empujarlo 0.35 hacia un dedo
I = bi.translate([-0.36, 0, 0]) ^ ce
print('   bisel 0.36 hacia -X (dedo de 0 grados): pisa a la rueda central %.3f mm3 en %s' % (I.volume(), bb(I)))
# lo mismo en otros giros del bisel (el bisel es de revolucion ahi: no cambia)
# subir la rueda central / bajar el bisel: holgura vertical cono-cono
for dz in (0.1, 0.2, 0.25, 0.3, 0.35):
    print('   bisel %.2f mas bajo que la rueda central: pisa %.3f mm3' % (dz, vol(bi.translate([0, 0, -dz]), ce)))
