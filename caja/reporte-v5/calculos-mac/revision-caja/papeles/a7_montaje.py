# Orden de montaje del apartado 7 del reporte: cada pieza baja desde arriba (o entra de lado) con lo anterior ya puesto
import sys
from comun import *
def baja(n, puestas, tau=0.0, H=140.0, paso=0.5, pieza=None):
    """Peor volumen pisado al bajar la pieza n (en vertical) con las 'puestas' ya montadas. Devuelve (vol max, altura, contra quien)."""
    m0 = pieza if pieza is not None else puesta(n, tau); peor = (0.0, 0.0, '')
    otros = {q: (puesta(q, tau) if not isinstance(q, tuple) else q[1]) for q in puestas}
    h = paso
    while h <= H:
        m = m0.translate([0, 0, h]); B = bb(m)
        for q, o in otros.items():
            b = bb(o)
            if B[0] > b[3] or b[0] > B[3] or B[1] > b[4] or b[1] > B[4] or B[2] > b[5] or b[2] > B[5]: continue
            v = vol(m, o)
            if v > peor[0]: peor = (v, h, q if not isinstance(q, tuple) else q[0])
        h += paso
    return peor
G_ = G
abiertas = [('puerta_derecha@90', puerta(1, 90.0)), ('puerta_izquierda@90', puerta(-1, 90.0))]
aroG = ('aro@abierto', puesta('aro_puertas', G_))
print('--- orden del reporte (apartado 7)')
pasos = [
 ('1 plataforma', 'plataforma', ['base'], None),
 ('2 tubo', 'tubo', ['base', 'plataforma'], None),
 ('3 marco', 'marco', ['base', 'plataforma', 'tubo'], None),
 ('4 aro', 'aro_puertas', ['marco', 'tubo'], None),
 ('5 meseta', 'meseta', ['marco', 'aro_puertas', 'tubo'], None),
 ('8 rueda central (puertas de pie, pasadores puestos)', 'rueda_central', ['meseta', 'marco', 'pasador_derecho', 'pasador_izquierdo', aroG] + abiertas, None),
 ('9 teton (puertas cerradas)', 'teton', ['marco', 'aro_puertas', 'meseta', 'rueda_central'], None),
 ('10 plato, con la rueda central YA puesta (orden del reporte)', 'plato', ['tubo', 'marco', 'aro_puertas', 'teton', 'meseta', 'rueda_central', 'puerta_derecha', 'puerta_izquierda'], None),
 ('11 satelite_1, con la rueda central YA puesta (orden del reporte)', 'satelite_1', ['plato', 'rueda_central'], None),
 ('11 satelite_2, con la rueda central YA puesta', 'satelite_2', ['plato', 'rueda_central'], None),
 ('12 bisel sobre todo (sin cuerpo)', 'bisel', ['plato', 'rueda_central', 'tubo'] + ['satelite_%d' % i for i in range(1, 7)], None),
 ('12 cuerpo', 'cuerpo', ['base', 'tubo', 'plato'], None),
]
for nombre, n, puestas, _ in pasos:
    v, h, q = baja(n, puestas)
    print('  %-62s %s' % (nombre, 'entra sin pisar nada' if v < 0.02 else 'NO ENTRA: pisa %.1f mm3 a %s cuando esta %.1f mm por encima de su sitio' % (v, q, h)))
# el bisel tiene que bajar junto con el cuerpo (entra por debajo en el cuerpo): se comprueba el bisel dentro del cuerpo
v = max(vol(S['bisel'].translate([0, 0, -h]), S['cuerpo']) for h in np.arange(0.5, 120, 0.5)); print('  bisel entrando en el cuerpo por debajo: pisa %.2f mm3' % v)
print('--- orden alternativo: plato y satelites ANTES que la rueda central')
alt = [
 ('plato sin rueda central (puertas cerradas, teton puesto)', 'plato', ['tubo', 'marco', 'aro_puertas', 'teton', 'meseta', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo']),
 ('satelite_1 sin rueda central', 'satelite_1', ['plato', 'meseta']),
 ('rueda central con plato y satelites ya puestos', 'rueda_central', ['meseta', 'marco', 'pasador_derecho', 'pasador_izquierdo', 'plato', 'puerta_derecha', 'puerta_izquierda'] + ['satelite_%d' % i for i in range(1, 7)]),
 ('bisel despues', 'bisel', ['plato', 'rueda_central', 'tubo'] + ['satelite_%d' % i for i in range(1, 7)]),
]
for nombre, n, puestas in alt:
    v, h, q = baja(n, puestas)
    print('  %-62s %s' % (nombre, 'entra sin pisar nada' if v < 0.02 else 'NO ENTRA: pisa %.1f mm3 a %s a %.1f mm' % (v, q, h)))
print('    radios: plato por dentro %.2f ; rueda central por fuera: dientes %.2f, placa %.2f, dedos hasta %.2f ; satelite de %.2f a %.2f' % (d['plato_r_in'], d['central_punta'], d2['R_placa'], d2['r_dedo0'] + p['esqueleto_grueso'], d['r_ejes'] - d['r_satelite'] - p['modulo'], d['r_ejes'] + d['r_satelite'] + p['modulo']))
# pasadores: entran de lado (en Y), con las puertas de pie
for sx, n in ((1, 'pasador_derecho'), (-1, 'pasador_izquierdo')):
    for sg in (1, -1):
        peor = 0
        for h in np.arange(1, 100, 1.0):
            m = S[n].translate([0, sg * h, 0])
            peor = max(peor, sum(vol(m, o) for o in (S['meseta'], S['marco'], puerta(sx, 90.0), puesta('aro_puertas', G_))))
        print('  %s metido desde %s, sin rueda central: pisa %.3f mm3 ; con el tubo puesto pisa %.3f' % (n, 'atras' if sg > 0 else 'delante', peor, max(vol(S[n].translate([0, sg * h, 0]), S['tubo']) for h in np.arange(1, 100, 1.0))))
print('--- posiciones equivocadas: se gira la pieza alrededor del eje y se mira en que angulos entra (pisa < 0,05 mm3)')
def angulos_libres(n, contra, dz=0.0, paso=0.5, tau=0.0):
    libres = []
    otros = [puesta(q, tau) for q in contra]
    for a in np.arange(0, 360, paso):
        m = S[n].rotate([0, 0, float(a)]).translate([0, 0, dz])
        if sum(vol(m, o) for o in otros) < 0.05: libres.append(float(a))
    # agrupar
    grupos = []
    for a in libres:
        if grupos and a - grupos[-1][1] <= paso + 1e-9: grupos[-1][1] = a
        else: grupos.append([a, a])
    return grupos
for n, contra, dz in (('plataforma', ['base'], 0.0), ('tubo', ['plataforma'], 2.0), ('tubo', ['plataforma'], 0.0), ('marco', ['base'], 0.0), ('aro_puertas', ['marco'], 0.0), ('meseta', ['marco', 'pasador_derecho', 'pasador_izquierdo'], 0.0),
                      ('rueda_central', ['meseta'], 0.0), ('plato', ['tubo'], 0.0), ('cuerpo', ['base'], 0.0), ('funda', ['cuerpo', 'bisel', 'base'], 0.0), ('probeta_anillo', ['meseta'], 0.0)):
    print('  %-14s contra %-40s (subida %.0f mm): entra en %s' % (n, '+'.join(contra), dz, angulos_libres(n, contra, dz)))
print('  meseta girada 180 es igual a si misma? volumen distinto: %.2f mm3' % ((S['meseta'] - S['meseta'].rotate([0, 0, 180])).volume()))
print('  rueda central girada 180: volumen distinto %.2f mm3' % ((S['rueda_central'] - S['rueda_central'].rotate([0, 0, 180])).volume()))
# la plataforma del reves / el soporte
so = S['soporte']; pf = S['plataforma']
print('  soporte girado 180 sobre el pedestal: pisa %.3f mm3 con la plataforma; girado 90: %.3f; desplazado 5 mm en X: %.3f  (0 = nada lo impide)' % (vol(so.rotate([0, 0, 180]), pf), vol(so.rotate([0, 0, 90]), pf), vol(so.translate([5, 0, 0]), pf)))
# satelites: iguales entre si y simetricos arriba/abajo
c1 = CP.pol(d['r_ejes'], 270.0)
s1 = S['satelite_1'].translate([-c1[0], -c1[1], 0])
for k in range(2, 7):
    c = CP.pol(d['r_ejes'], 270.0 + 60 * (k - 1)); sk = S['satelite_%d' % k].translate([-c[0], -c[1], 0])
    print('  satelite_%d contra satelite_1 (llevados al origen): volumen distinto %.3f mm3' % (k, (sk - s1).volume() + (s1 - sk).volume()), end=';')
print()
zc = (d['z_engr0'] + d['z_engr1']) / 2
vuelto = s1.translate([0, 0, -zc]).rotate([180, 0, 0]).translate([0, 0, zc])
print('  satelite dado la vuelta (cara de arriba abajo): volumen distinto %.3f mm3 -> %s' % ((vuelto - s1).volume() + (s1 - vuelto).volume(), 'se puede montar con cualquiera de las dos caras'))
