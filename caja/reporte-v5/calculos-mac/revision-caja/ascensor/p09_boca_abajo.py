# 9. Boca abajo / tirando hacia arriba: cuanto sube cada pieza antes de que algo la pare, y que la para
from comun import *
UMB = 1e-3
todas = [n for n in P if P[n].mueve not in ('funda', 'probeta')]
sats = ['satelite_%d' % i for i in range(1, 7)]
def sube(grupo, tau, M, tope=6.0):
    """El grupo de piezas sube junto (las demas, quietas). Devuelve cuanto y que lo para."""
    otras = [n for n in todas if n not in grupo]
    cajas = {n: M[n].bounding_box() for n in todas}
    def cerca(a, b):
        A, B = cajas[a], cajas[b]
        return A[0] < B[3] and B[0] < A[3] and A[1] < B[4] and B[1] < A[4] and A[2] - 0.5 < B[5] + 0.01 and B[2] < A[5] + tope
    pares = [(a, b) for a in grupo for b in otras if cerca(a, b)]
    v = 0.0
    while v < tope - 1e-9:
        v2 = round(v + 0.05, 3)
        quien = [(a, b) for a, b in pares if vol(M[a].translate([0, 0, v2]), M[b]) > UMB]
        if quien: return v, ', '.join(sorted(set(b for a, b in quien)))
        v = v2
    return tope, 'NADA en %.0f mm' % tope
for tau in (0.0, 30.0, 100.0, 200.0, 345.0):
    M = {n: puesta(n, tau) for n in todas}
    print('tau = %.0f' % tau)
    # nota: los satelites estan debajo de un dedo cuando (270 - tau) es multiplo de 60, es decir tau = 30, 90, ...
    for g in [[s] for s in sats] + [['bisel'], ['plato'], ['tubo'], ['rueda_central'], ['plataforma'], ['teton'],
              ['tubo', 'plato'], ['tubo', 'plato', 'bisel'] + sats, ['tubo', 'plato', 'bisel', 'rueda_central'] + sats, ['plataforma', 'soporte', 'reloj_de_pega']]:
        v, q = sube(g, tau, M)
        print('   %-55s sube %.2f mm; lo para: %s' % ('+'.join(x.replace('satelite_', 's') for x in g), v, q))
# satelites: con el bisel ya descolgado 0.4 (boca abajo todo cae hacia la tapa)
print('\nBoca abajo de verdad (el bisel cae 0.4 hasta el labio del cuerpo y todo lo demas cae sobre el):')
for tau in (0.0, 30.0, 200.0):
    M = {n: puesta(n, tau) for n in todas}
    M['bisel'] = M['bisel'].translate([0, 0, 0.4])
    for g in ([sats[0]], [sats[3]], ['rueda_central'], ['plato'], ['tubo', 'plato']):
        v, q = sube(g, tau, M)
        print('   tau %.0f  %-28s sube %.2f mm; lo para: %s' % (tau, '+'.join(g), v, q))
# el satelite: que tiene encima segun el radio
print('\nQue hay encima de cada satelite (z de la cara de abajo de lo que tiene encima, por radio desde el eje de la caja):')
print('   satelite: r de %.2f a %.2f, cara de arriba z = %.2f' % (d['r_ejes'] - 10.5, d['r_ejes'] + 10.5, d['z_engr1']))
print('   placa de la rueda central: hasta r = %.2f, cara de abajo z = %.2f (tapa %.2f mm del satelite, holgura %.2f)' % (d2['R_placa'], -p['esqueleto_grueso'], d2['R_placa'] - (d['r_ejes'] - 10.5), -p['esqueleto_grueso'] - d['z_engr1']))
print('   techo del bisel: desde r = %.2f, cara de abajo z = %.2f (tapa %.2f mm del satelite, holgura %.2f)' % (d['bisel_punta'], d['z_engr1'], d['r_ejes'] + 10.5 - d['bisel_punta'], 0.0))
print('   eje del plato: hasta z = %.2f; satelite de %.2f a %.2f' % (d['z_engr1'] - 0.2, d['z_engr0'], d['z_engr1']))
# el satelite puede salirse inclinandose? cuanto puede inclinarse entre plato, placa y techo
c = pol(d['r_ejes'], 270.0)
for tau in (0.0,):
    M = {n: puesta(n, tau) for n in todas}
    s1 = M['satelite_1'].translate([0, 0, -0.2])       # a media holgura
    for eje, nombre in (((1, 0, 0), 'cabeceo radial'), ((0, 1, 0), 'cabeceo tangencial')):
        for sg in (1, -1):
            a = 0.0
            while a < 20:
                a2 = a + 0.1
                q = s1.translate([-c[0], -c[1], 6.4]).rotate([sg * a2 * eje[0], sg * a2 * eje[1], 0]).translate([c[0], c[1], -6.4])
                if any(vol(q, M[b]) > UMB for b in ('plato', 'bisel', 'rueda_central')): break
                a = a2
            print('   satelite 1 a media holgura, %s %+d: se inclina %.1f grados hasta tocar' % (nombre, sg, a))
