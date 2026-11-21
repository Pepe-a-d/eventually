# Piezas volcadas (cara de arriba hacia abajo): en t4 se comparaban ocupando la misma franja de altura, que no es donde
# se quedarian de verdad. Aqui se dejan caer de verdad: se bajan de 0,25 en 0,25 hasta el primer choque y se dice donde
# se quedan y si la pieza siguiente todavia entra.
from comun import *
def vx(s): return volcada(s)
def vy(s):
    b = s.bounding_box(); zc = (b[2] + b[5]) / 2
    return s.translate([0, 0, -zc]).rotate([0, 180, 0]).translate([0, 0, zc])
def cae(s, M, desde=40.0, hasta=-60.0, paso=0.25):
    e = desde
    while e >= hasta:
        c = choque(s.translate([0, 0, e]), M, 0.05)
        if c: return e + paso, c
        e -= paso
    return None, []
def dice(txt, s, M, angs=(0,)):
    for a in angs:
        q = s.rotate([0, 0, a]); e, c = cae(q, M)
        if e is None: print('   %s%s: cae sin que nada la pare' % (txt, ' girada %d' % a if a else '')); continue
        b = q.translate([0, 0, e]).bounding_box()
        print('   %s%s: se queda con su franja de altura de %.2f a %.2f (la pieza bien puesta va de %.2f a %.2f); la para %s' % (txt, ' girada %d' % a if a else '', b[2], b[5], s.bounding_box()[2], s.bounding_box()[5], [x[0] for x in c]))
    return e
M = {n: puesta(n, 0) for n in ('base', 'plataforma', 'tubo')}
print('MARCO volcado, sobre base + plataforma + tubo:')
dice('volcado sobre X', vx(S['marco']), M, (0, 60, 90, 180)); dice('volcado sobre Y', vy(S['marco']), M)
M['marco'] = S['marco']
print('ARO volcado, sobre el marco:')
dice('volcado sobre X (brazo al frente)', vx(S['aro_puertas']), M)
e = dice('volcado sobre Y (brazo atras)', vy(S['aro_puertas']), M)
aro_v = vy(S['aro_puertas']).translate([0, 0, e])
for a in (-11.0, 11.0):
    print('      aro volcado girado %+.0f grados: pisa al marco %.2f mm3' % (a, vol(aro_v.rotate([0, 0, a]), S['marco'])))
M2 = dict(M); M2['aro_puertas'] = aro_v
print('   con el aro volcado puesto, la meseta:')
em = dice('meseta', S['meseta'], M2)
M2['meseta'] = S['meseta'].translate([0, 0, em])
print('   meseta %.2f mm alta. Pasador en su sitio respecto a la meseta: pisa al marco %.2f mm3' % (em, vol(S['pasador_derecho'].translate([0, 0, em]), S['marco'])))
for a in (-11.0, -5.0, 0.0, 5.0, 11.0):
    M3 = dict(M2); M3['aro_puertas'] = aro_v.rotate([0, 0, a])
    ep, c = cae(puerta(1, 90).translate([0, 0, em]), M3, desde=20.0, hasta=0.0)
    print('      puerta de pie con el aro volcado girado %+.0f: %s' % (a, 'entra hasta el fondo' if ep is None else 'se queda %.2f mm alta; la para %s' % (ep, [x[0] for x in c])))
print('PLATO volcado, sobre tubo + marco + aro + teton + meseta:')
M4 = {n: puesta(n, 0) for n in ('tubo', 'marco', 'aro_puertas', 'teton', 'meseta')}
dice('volcado sobre X', vx(S['plato']), M4, (0, 30)); dice('volcado sobre Y', vy(S['plato']), M4)
print('PLATAFORMA volcada, sobre la base:')
dice('volcada sobre X', vx(S['plataforma']), {'base': S['base']}, (0, 60, 120))
print('PUERTA cara abajo (derecha), tumbada, sobre marco + aro (cerrado) + meseta, sin la otra puerta:')
ze = d['eje_z']
pdf = S['puerta_derecha'].translate([0, 0, -ze]).rotate([180, 0, 0]).translate([0, 0, ze])
Mp = {'marco': S['marco'], 'aro_puertas': S['aro_puertas'], 'meseta': S['meseta']}
for dx in (0.0, -0.6, -1.0, -2.0):
    e, c = cae(pdf.translate([dx, 0, 0]), Mp, desde=12.0, hasta=0.0)
    print('   bajandola plana, corrida %.1f mm hacia el centro: %s' % (dx, 'llega al fondo' if e is None else 'se queda %.2f mm alta; la para %s' % (e, c)))
peor = max(sum(v for _, v in choque(pdf.translate([-1.0 + 0.1 * i, 0, 0]), Mp, 0.0)) for i in range(11))
print('   y deslizandola despues 1 mm hacia fuera hasta su sitio: lo que mas pisa, %.2f mm3' % peor)
for q in (pdf ^ S['meseta']).decompose():
    b = q.bounding_box(); print('      en su sitio comparte con la meseta %.3f mm3 en x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f' % (q.volume(), b[0], b[3], b[1], b[4], b[2], b[5]))
print('   pasador con la puerta cara abajo en su sitio: pisa a la puerta %.3f mm3' % vol(S['pasador_derecho'], pdf))
print('   la varilla asoma %.1f mm por encima de la tapa' % pdf.bounding_box()[5])
print('   puerta cara abajo cerrada contra la otra puerta bien puesta: se pisan %.1f mm3' % vol(pdf, S['puerta_izquierda']))
print('   puerta BIEN puesta, bajandola plana corrida 1 mm al centro: %s' % (lambda r: 'llega al fondo' if r[0] is None else 'se queda %.2f mm alta; la para %s' % r)(cae(S['puerta_derecha'].translate([-1.0, 0, 0]), Mp, desde=12.0, hasta=0.0)))
print('RUEDA CENTRAL frente a su copia girada 180: donde se diferencian')
r180 = S['rueda_central'].rotate([0, 0, 180])
for q in ((S['rueda_central'] - r180) + (r180 - S['rueda_central'])).decompose():
    b = q.bounding_box()
    if q.volume() > 0.5: print('   %.1f mm3 a radio %.1f..%.1f, angulo %.0f, z %.1f..%.1f' % (q.volume(), min(math.hypot(b[0], b[1]), math.hypot(b[3], b[4])), max(math.hypot(b[0], b[1]), math.hypot(b[3], b[4]), math.hypot(b[0], b[4]), math.hypot(b[3], b[1])), math.degrees(math.atan2((b[1] + b[4]) / 2, (b[0] + b[3]) / 2)) % 360, b[2], b[5]))
