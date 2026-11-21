# Comprobacion 8: montaje de aro, meseta, puertas, pasadores, rueda central, teton y plato (pasos 4 a 10 del reporte), en pasos de 0,25 mm
from comun import *
EPS = 1e-4
def baja(nombre_m, m, contra, alto=30.0, paso=0.25, vec=(0, 0, 1)):
    """m baja desde 'alto' mm por encima de su sitio. Devuelve lo peor que pisa."""
    peor = (0.0, None, None)
    for i in range(int(alto / paso), -1, -1):
        hh = i * paso
        mm = m.translate([vec[0] * hh, vec[1] * hh, vec[2] * hh])
        for n, c in contra.items():
            v = vol(mm, c)
            if v > peor[0]: peor = (v, n, hh)
    return peor
def inf(txt, peor):
    print('  %-78s %s' % (txt, 'no pisa nada' if peor[0] <= EPS else 'PISA %s: %.2f mm3 cuando esta %.2f mm por encima de su sitio' % (peor[1], peor[0], peor[2])))
print('PASO 4: el aro baja sobre el marco')
for psi in (0.0, 5.5, 11.0):
    inf('aro en psi = %.1f' % psi, baja('aro', aro(psi), {'marco': S['marco']}))
inf('aro girado 180 grados (brazo al frente)', baja('aro', S['aro_puertas'].rotate([0, 0, 180]), {'marco': S['marco']}))
for g in (90, 270, 120, 240, 60, 300):
    inf('aro girado %d grados' % g, baja('aro', S['aro_puertas'].rotate([0, 0, g]), {'marco': S['marco']}))
inf('aro boca abajo (cuernos hacia abajo), brazo atras', baja('aro', S['aro_puertas'].translate([0, 0, 16.7]).rotate([0, 180, 0]).translate([0, 0, -16.7]), {'marco': S['marco']}))
print('PASO 5: la meseta baja sobre el cuello, con el aro puesto')
for psi in (0.0, 5.5, 11.0):
    inf('meseta, aro en psi = %.1f' % psi, baja('meseta', S['meseta'], {'marco': S['marco'], 'aro': aro(psi)}))
inf('meseta girada 180 grados, aro en 0', baja('meseta', S['meseta'].rotate([0, 0, 180]), {'marco': S['marco'], 'aro': aro(0)}))
for g in (90, 5, 115.4):
    inf('meseta girada %s grados, aro en 0' % g, baja('meseta', S['meseta'].rotate([0, 0, g]), {'marco': S['marco'], 'aro': aro(0)}))
inf('meseta boca abajo', baja('meseta', S['meseta'].translate([0, 0, 4]).rotate([180, 0, 0]).translate([0, 0, -4]), {'marco': S['marco'], 'aro': aro(0)}))
M180 = S['meseta'].rotate([0, 0, 180])
print('   la meseta girada 180 grados y la meseta en su sitio difieren en %.2f mm3 (0 = identicas)' % ((S['meseta'] - M180).volume() + (M180 - S['meseta']).volume()))
print('PASO 6: cada puerta entra de pie, desde arriba')
def de_pie(sx, ang=90.0):
    return puerta(sx, ang)
for psi_m, nota in ((11.0, 'aro en abierto exacto (11,0)'), (11.6, 'aro a tope de verdad, sin teton (11,6)'), (10.5, 'aro en 10,5'), (9.0, 'aro en 9,0'), (8.5, 'aro en 8,5'), (5.5, 'aro a medio camino'), (0.0, 'aro en cerrado')):
    A = aro(psi_m)
    for sx in (1, -1):
        contra = {'meseta': S['meseta'], 'aro': A, 'marco': S['marco'], 'otra puerta': de_pie(-sx)}
        inf('puerta %s, %s' % ('derecha' if sx > 0 else 'izquierda', nota), baja('p', de_pie(sx), contra, alto=30.0))
A = aro(11.0)
for incl in (88.0, 92.0, 85.0, 95.0):
    inf('puerta derecha inclinada a %.0f grados mientras baja, aro en 11' % incl, baja('p', de_pie(1, incl), {'meseta': S['meseta'], 'aro': A, 'marco': S['marco']}, alto=30.0))
for dyy in (0.3, -0.3):
    inf('puerta derecha desplazada %.1f mm en Y mientras baja' % dyy, baja('p', puerta(1, 90.0, dyy), {'meseta': S['meseta'], 'aro': A, 'marco': S['marco']}, alto=30.0))
# otras maneras de meterla
inf('puerta derecha tumbada (cerrada, 0 grados) bajando recta, aro en cerrado', baja('p', puerta(1, 0.0), {'meseta': S['meseta'], 'aro': aro(0.0), 'marco': S['marco']}, alto=20.0))
# puerta al reves: la misma pieza con la manivela delante (girada 180 sobre X: queda boca arriba) o cambiada de lado
print('   puerta derecha puesta en el lado izquierdo (girada media vuelta en Z) = puerta izquierda: diferencia %.3f mm3' % ((S['puerta_derecha'].rotate([0, 0, 180]) - S['puerta_izquierda']).volume()))
volteada = S['puerta_derecha'].translate([0, 0, 2.5]).rotate([180, 0, 0]).translate([0, 0, -2.5])      # cara vista hacia abajo, manivela hacia arriba y delante
b = volteada.bounding_box(); print('   puerta con la cara vista hacia abajo: sobresale hasta z = %.2f (la manivela queda %.1f mm por encima de la tapa): se ve' % (b[5], b[5]))
espejo_y = S['puerta_derecha'].rotate([0, 0, 180]).translate([2 * 0, 0, 0])   # es la izquierda
print('PASO 7: pasadores, entrando a lo largo de Y con las puertas de pie')
for nom, sg in (('desde atras', 1), ('desde delante', -1)):
    contra = {'meseta': S['meseta'], 'marco': S['marco'], 'puerta': de_pie(1), 'aro': aro(11.0), 'tubo': S['tubo']}
    inf('pasador derecho %s' % nom, baja('pas', S['pasador_derecho'], contra, alto=100.0, paso=0.25, vec=(0, sg, 0)))
contra = {'meseta': S['meseta'], 'marco': S['marco'], 'puerta': puerta(1, 0.0), 'aro': aro(0.0)}
inf('pasador derecho desde atras con la puerta cerrada', baja('pas', S['pasador_derecho'], contra, alto=100.0, vec=(0, 1, 0)))
print('PASO 8: rueda central sobre la meseta (puertas de pie, aro en abierto)')
contra = {'meseta': S['meseta'], 'marco': S['marco'], 'puerta D': de_pie(1), 'puerta I': de_pie(-1), 'pasador D': S['pasador_derecho'], 'pasador I': S['pasador_izquierdo'], 'aro': aro(11.0), 'tubo': S['tubo']}
inf('rueda central en su posicion', baja('rc', S['rueda_central'], contra, alto=40.0))
for g in (180, 120, 240, 115, 235):
    inf('rueda central girada %d grados' % g, baja('rc', S['rueda_central'].rotate([0, 0, g]), contra, alto=40.0))
print('PASO 9: teton (aro en cerrado, puertas cerradas)')
contra = {'marco': S['marco'], 'aro': aro(0.0), 'rueda central': S['rueda_central'], 'meseta': S['meseta'], 'tubo': S['tubo']}
inf('teton bajando recto a su sitio (con la rueda central ya puesta, como dice el reporte)', baja('t', S['teton'], contra, alto=30.0))
print('PASO 10: plato sobre el tubo')
contra = {'marco': S['marco'], 'aro': aro(0.0), 'rueda central': S['rueda_central'], 'meseta': S['meseta'], 'tubo': S['tubo'], 'teton': S['teton']}
inf('plato bajando, CON la rueda central ya puesta (orden del reporte: 8 antes que 10)', baja('pl', S['plato'], contra, alto=30.0))
contra.pop('rueda central')
inf('plato bajando, SIN la rueda central', baja('pl', S['plato'], contra, alto=30.0))
contra = {'meseta': S['meseta'], 'marco': S['marco'], 'plato': S['plato'], 'pasador D': S['pasador_derecho'], 'pasador I': S['pasador_izquierdo'], 'puerta D': puerta(1, 0), 'puerta I': puerta(-1, 0)}
inf('rueda central bajando DESPUES del plato (puertas cerradas)', baja('rc', S['rueda_central'], contra, alto=40.0))
