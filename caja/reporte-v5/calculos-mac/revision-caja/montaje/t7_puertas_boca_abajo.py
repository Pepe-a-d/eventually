# Boca abajo, caja cerrada: cuanto se descuelgan las puertas (giran en su bisagra hacia fuera) y que les pasa
# cuando el soporte y el reloj (que nada sujeta salvo un iman) les caen encima.
from comun import *
M0 = {n: puesta(n, 0) for n in DENTRO}
xh, ze = d['eje_x'], d['eje_z']
def puerta_(sx, ang, dz=0.0, dx=0.0):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    return S[n].translate([-sx * xh, 0, -ze]).rotate([0, sx * ang, 0]).translate([sx * xh + dx, 0, ze + dz])
def limite(sx, otros, dz=0.0, dx=0.0, paso=0.25, umbral=0.05):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    v0 = {k: vol(puerta_(sx, 0.0, dz, dx), o) for k, o in otros.items() if k != n}
    for i in range(1, 121):
        a = paso * i; q = puerta_(sx, a, dz, dx)
        c = [(k, round(vol(q, o) - v0[k], 3)) for k, o in otros.items() if k != n and vol(q, o) - v0[k] > umbral]
        if c: return a - paso, c
    return 99.0, []
punta = xh - p['junta'] / 2
print('Puertas cerradas, boca abajo. Giro libre hacia fuera antes de pisar algo (pasos de 0,25 grados, umbral 0,05 mm3):')
for sx in (1, -1):
    otros = {k: v for k, v in M0.items() if k not in ('reloj_de_pega', 'soporte')}
    a, c = limite(sx, otros); print('   puerta %s, todo en su sitio: %.2f grados (%.2f mm en la punta); la para %s' % ('derecha' if sx > 0 else 'izquierda', a, math.radians(a) * punta, c))
    # con la otra puerta tambien descolgada lo mismo (se mueven a la vez)
    o2 = dict(otros); otra = 'puerta_izquierda' if sx > 0 else 'puerta_derecha'
    for dz, dxa in ((0.25, 0.0), (0.40, 0.0), (0.0, -0.3 * sx), (0.40, -0.3 * sx)):
        o3 = dict(o2); o3['aro_puertas'] = M0['aro_puertas'].translate([dxa, 0, 0])
        del o3[otra]
        a, c = limite(sx, o3, dz=dz)
        print('      bisagra subida %.2f mm (holgura del pasador), aro desplazado %.2f mm en X (su holgura en el cuello es %.2f): %.2f grados -> punta %.2f mm; la para %s' % (dz, dxa, d['cuello_r_in'] - d['aro_r_ext'], a, dz + math.radians(a) * punta, c))
# pasadores: recorrido a lo largo de Y
for n in ('pasador_derecho', 'pasador_izquierdo'):
    for sg in (1, -1):
        e = 0.0
        while e < 20:
            c = choque(M0[n].translate([0, sg * (e + 0.05), 0]), {k: v for k, v in M0.items() if k != n}, 0.02)
            if c: break
            e += 0.05
        print('   %s hacia %sY: se desplaza %.2f mm y lo para %s' % (n, '+' if sg > 0 else '-', e, c))
    sin_rc = {k: v for k, v in M0.items() if k not in (n, 'rueda_central')}
    e = 0.0
    while e < 120:
        if choque(M0[n].translate([0, e + 0.5, 0]), sin_rc, 0.02): break
        e += 0.5
    print('   %s sin la rueda central: sale %.0f mm hacia +Y sin que nada lo pare%s' % (n, e, ' (libre)' if e >= 120 else ''))
# soporte + reloj cayendo sobre las puertas cerradas
print('Soporte y reloj, boca abajo, caja cerrada:')
grupo = ('soporte', 'reloj_de_pega')
def cae(otros, lim=20.0, paso=0.1):
    e = 0.0
    while e < lim:
        c = []
        for g_ in grupo: c += choque(M0[g_].translate([0, 0, e + paso]), otros, 0.05)
        if c: return e, c
        e += paso
    return e, []
otros = {k: v for k, v in M0.items() if k not in grupo}
e, c = cae(otros); print('   con las puertas en su sitio: el soporte con el reloj cae %.1f mm y lo paran %s' % (e, c))
e_r = 0.0
while e_r < 5 and not choque(M0['reloj_de_pega'].translate([0, 0, e_r + 0.05]), {'soporte': M0['soporte']}, 0.05): e_r += 0.05
print('   el reloj de pega dentro del soporte se mueve %.2f mm hacia arriba hasta tocar el travesano' % e_r)
e_s, c = 0.0, []
while e_s < 20:
    c = choque(M0['soporte'].translate([0, 0, e_s + 0.1]), {k: v for k, v in otros.items()}, 0.05)
    if c: break
    e_s += 0.1
print('   el soporte solo (sin reloj) cae %.1f mm y lo para %s' % (e_s, c or 'nada en 20 mm'))
for a in (2.0, 3.0):
    o2 = dict(otros); o2['puerta_derecha'] = puerta_(1, a); o2['puerta_izquierda'] = puerta_(-1, a)
    e, c = cae(o2); print('   con las dos puertas descolgadas %.1f grados: cae %.1f mm y lo paran %s' % (a, e, c))
# que sujeta a las puertas cuando el reloj empuja: solo la bola en su pista
q = puerta_(1, 3.5); c = choque(q, {k: v for k, v in M0.items() if k not in ('puerta_derecha', 'reloj_de_pega', 'soporte')}, 0.02)
print('   puerta derecha forzada a 3,5 grados: pisa %s' % c)
# con la caja abierta, boca abajo: soporte y reloj
for tau in (100.0, 200.0, 345.0):
    Mt = {n: puesta(n, tau) for n in DENTRO}
    e = 0.0; c = []
    while e < 150:
        c = []
        for g_ in grupo: c += choque(Mt[g_].translate([0, 0, e + 0.5]), {k: v for k, v in Mt.items() if k not in grupo}, 0.05)
        if c: break
        e += 0.5
    print('   tubo a %.0f (puertas abiertas), boca abajo: soporte + reloj caen %s' % (tau, ('%.1f mm y los para %s' % (e, c)) if c else 'mas de 150 mm: salen de la caja, nada los para'))
