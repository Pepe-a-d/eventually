# Se puede montar mal? Cada pieza, girada alrededor de Z y volcada, contra lo que ya esta montado cuando le toca.
# 'asiento': volumen comun en su sitio final. 'se queda a': altura sobre su sitio a la que deja de bajar (primer choque bajando desde 12 mm, de 0,5 en 0,5; 12.5 = ya pisa a 12 mm).
from comun import *
def gz(s, a): return s.rotate([0, 0, a])
def vx(s):                                   # volcada alrededor de X (delante <-> detras)
    return volcada(s)
def vy(s):                                   # volcada alrededor de Y (derecha <-> izquierda)
    b = s.bounding_box(); zc = (b[2] + b[5]) / 2
    return s.translate([0, 0, -zc]).rotate([0, 180, 0]).translate([0, 0, zc])
def asiento(s, M):
    c = choque(s, M, 0.05); return sum(v for _, v in c), c
def se_queda(s, M, desde=12.0, paso=0.5):
    e = desde
    while e >= -1e-9:
        if choque(s.translate([0, 0, e]), M, 0.05): return e + paso
        e -= paso
    return 0.0
def prueba(nombre, s, M, angs=(90, 120, 180, 240, 270), volcar=True, barrido=None, barrido_volcada=False):
    print('%s (ya montado: %s)' % (nombre, ', '.join(M)))
    v0, _ = asiento(s, M); print('   en su posicion: asiento %.2f mm3' % v0)
    casos = [('girada %d' % a, gz(s, a)) for a in angs]
    if volcar:
        casos += [('volcada sobre X', vx(s)), ('volcada sobre Y', vy(s))]
    for txt, q in casos:
        v, c = asiento(q, M)
        if v <= 0.05:
            h = se_queda(q, M)
            print('   %-18s ENTRA IGUAL (asiento 0,00 mm3; bajando se queda a %.2f mm)' % (txt, h))
        else:
            h = se_queda(q, M)
            print('   %-18s choca: %.1f mm3 en su sitio (%s); bajando se queda a %.2f mm de su sitio' % (txt, v, ', '.join('%s %.1f' % x for x in sorted(c, key=lambda x: -x[1])[:3]), h))
    if barrido:
        Mb = {k: M[k] for k in barrido}
        libres = [a for a in range(1, 360) if asiento(gz(s, a), Mb)[0] <= 0.05]
        txt = '   barrido de 1 en 1 grado contra %s: giros (aparte de 0) en que el asiento queda libre: %s' % (', '.join(barrido), libres or 'ninguno')
        if barrido_volcada:
            lv = [a for a in range(0, 360) if asiento(gz(vx(s), a), Mb)[0] <= 0.05]
            txt += '; volcada: %s' % (lv or 'ninguno')
        print(txt)
t0 = time.time()
M = {'base': S['base']}
prueba('PLATAFORMA', puesta('plataforma', 0), M, barrido=['base'], barrido_volcada=True); M['plataforma'] = puesta('plataforma', 0)
# el tubo: el asiento esta libre en muchos giros (tramo plano); lo que cuenta es si BAJA. Camino de 12 mm a 0 en pasos de 0,5
print('TUBO (ya montado: base, plataforma): se baja de 12 mm a 0 en pasos de 0,5 con cada giro')
def baja_tubo(q, alturas=None):
    peor = 0.0; donde = None
    for e in (alturas or [12.0 - 0.5 * i for i in range(25)]):
        v = sum(x for _, x in choque(q.translate([0, 0, e]), M, 0.05))
        if v > peor: peor, donde = v, e
    return peor, donde
for a in (90, 120, 180, 240, 270):
    v, e = baja_tubo(gz(S['tubo'], a)); print('   girado %d: %s' % (a, 'ENTRA IGUAL' if v <= 0.05 else 'choca, max %.1f mm3 a %.1f mm de su sitio' % (v, e)))
for txt, q in (('volcado sobre X', vx(S['tubo'])), ('volcado sobre Y', vy(S['tubo']))):
    v, c = asiento(q, M); print('   %s: %s' % (txt, 'ENTRA IGUAL' if v <= 0.05 else 'choca en su sitio %.1f mm3' % v))
libres = []; minimo = (9e9, 0)
for a in range(1, 360):
    v, e = baja_tubo(gz(S['tubo'], a), (6.0, 4.0, 2.0, 1.0, 0.0))
    if v <= 0.05: libres.append(a)
    if v < minimo[0]: minimo = (v, a)
print('   barrido de 1 en 1 grado (alturas 6, 4, 2, 1 y 0 mm): giros (aparte de 0) en que el tubo baja sin pisar: %s; el que menos pisa: %.1f mm3 a %d grados' % (libres or 'ninguno', minimo[0], minimo[1]))
fino = []
for a in [x / 10.0 for x in range(-30, 31)] + [120 + x / 10.0 for x in range(-30, 31)] + [240 + x / 10.0 for x in range(-30, 31)]:
    v, e = baja_tubo(gz(S['tubo'], a), (6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.5, 0.0))
    if v <= 0.05: fino.append(a)
for c0 in (0, 120, 240):
    g_ = [x for x in fino if abs(x - c0) <= 3.01]
    print('   barrido fino (0,1 grados) alrededor de %d: baja sin pisar %s' % (c0, ('de %.1f a %.1f grados' % (min(g_), max(g_))) if g_ else 'en ningun giro'))
print('   (%.0f s)' % (time.time() - t0))
M['tubo'] = S['tubo']
prueba('MARCO', S['marco'], M, barrido=['base'], barrido_volcada=True); M['marco'] = S['marco']
prueba('ARO DE PUERTAS (en cerrado)', puesta('aro_puertas', 0), M, barrido=['marco'], barrido_volcada=True)
prueba('ARO DE PUERTAS (en abierto)', puesta('aro_puertas', G), M)
M['aro_puertas'] = puesta('aro_puertas', G)
prueba('MESETA (aro en abierto)', S['meseta'], M, barrido=['marco'])
m180 = gz(S['meseta'], 180)
print('   meseta frente a su copia girada 180: volumen %.2f; comun %.2f; solo en la original %.2f mm3; solo en la girada %.2f mm3' % (S['meseta'].volume(), (S['meseta'] ^ m180).volume(), (S['meseta'] - m180).volume(), (m180 - S['meseta']).volume()))
dif = (S['meseta'] - m180) + (m180 - S['meseta'])
for q in dif.decompose():
    b = q.bounding_box()
    if q.volume() > 0.05: print('      trozo distinto: %.2f mm3, x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f (angulo %.0f, radio %.1f)' % (q.volume(), b[0], b[3], b[1], b[4], b[2], b[5], math.degrees(math.atan2((b[1] + b[4]) / 2, (b[0] + b[3]) / 2)) % 360, math.hypot((b[0] + b[3]) / 2, (b[1] + b[4]) / 2)))
M['meseta'] = S['meseta']
print('   (%.0f s)' % (time.time() - t0))
# puertas
print('PUERTAS (ya montado: marco, aro, meseta)')
ze, xh = d['eje_z'], d['eje_x']
def flipA(s):                                 # cara de arriba hacia abajo, con el agujero de la bisagra en el mismo eje: giro de 180 sobre el eje X que pasa por z = eje_z
    return s.translate([0, 0, -ze]).rotate([180, 0, 0]).translate([0, 0, ze])
def abre(s, sx, ang, dz=0.0):
    return s.translate([-sx * xh, 0, -ze]).rotate([0, sx * ang, 0]).translate([sx * xh, 0, ze + dz])
pdn = S['puerta_derecha']; pdf = flipA(pdn)
for txt, q in (('derecha, bien, de pie', abre(pdn, 1, 90)), ('derecha, cara abajo, de pie', abre(pdf, 1, 90)), ('derecha, cara abajo, tumbada (cerrada)', pdf), ('derecha, bien, tumbada (cerrada)', pdn), ('derecha, cara abajo, de pie al reves (-90)', abre(pdf, 1, -90))):
    v, c = asiento(q, M); h = se_queda(q, M)
    print('   %-42s asiento %.1f mm3 %s; bajando se queda a %.2f mm' % (txt, v, c[:3], h))
print('   puerta de pie con el aro en otras posiciones (giro del aro en grados -> asiento mm3):')
for psi in (0.0, 2.5, 5.5, 8.0, 8.5, 9.0, 10.0, 11.0):
    M2 = dict(M); M2['aro_puertas'] = S['aro_puertas'].rotate([0, 0, p['aro_sentido'] * psi])
    v, c = asiento(abre(pdn, 1, 90), M2); print('      aro a %.1f: %.2f mm3, se queda a %.2f mm' % (psi, v, se_queda(abre(pdn, 1, 90), M2)))
print('   puerta izquierda es la derecha girada 180: diferencia de volumen entre puerta_izquierda y derecha girada 180: %.4f mm3' % ((S['puerta_izquierda'] - gz(pdn, 180)).volume() + (gz(pdn, 180) - S['puerta_izquierda']).volume()))
for n in ('puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo'): M[n] = puesta(n, 0)
M['aro_puertas'] = puesta('aro_puertas', 0); M['teton'] = puesta('teton', 0)
# plato: contra tubo, teton, marco, aro, meseta (orden corregido: antes que la rueda central)
prueba('PLATO (sin rueda central; puertas cerradas)', puesta('plato', 0), M, barrido=['tubo', 'teton'])
M2 = {n: puesta(n, G) for n in ('tubo', 'teton', 'aro_puertas', 'marco', 'meseta')}
M2['tubo'] = S['tubo']
v, c = asiento(S['plato'], M2); print('   plato con el tubo en 0 y las puertas ABIERTAS (teton dentro): asiento %.1f mm3 %s; se queda a %.2f mm' % (v, c, se_queda(S['plato'], M2)))
for tt in (10.0, 30.0, 45.0, 50.0, 60.0, 80.0):
    M2 = {'tubo': puesta('tubo', tt), 'teton': puesta('teton', 0), 'aro_puertas': puesta('aro_puertas', 0), 'marco': S['marco'], 'meseta': S['meseta']}
    v, c = asiento(puesta('plato', tt), M2); print('   plato con el tubo girado %.0f y las puertas cerradas: asiento %.2f mm3 %s' % (tt, v, c))
M['plato'] = S['plato']
for k in range(1, 7): M['satelite_%d' % k] = S['satelite_%d' % k]
prueba('RUEDA CENTRAL (con plato y satelites)', S['rueda_central'], M)
Mm = {n: M[n] for n in ('meseta', 'marco', 'pasador_derecho', 'pasador_izquierdo')}
prueba('RUEDA CENTRAL (solo contra meseta, marco y pasadores)', S['rueda_central'], Mm, barrido=['meseta'])
Mm2 = dict(Mm); Mm2['meseta'] = m180
v, c = asiento(gz(S['rueda_central'], 180), Mm2); print('   meseta girada 180 y rueda central girada 180: asiento %.2f mm3' % v)
v, c = asiento(S['rueda_central'], Mm2); print('   meseta girada 180 y rueda central en su posicion: asiento %.2f mm3 %s' % (v, c))
r180 = gz(S['rueda_central'], 180)
dif = (S['rueda_central'] - r180).volume() + (r180 - S['rueda_central']).volume(); print('   rueda central frente a su copia girada 180: se diferencian en %.2f mm3 (las llaves)' % dif)
M['rueda_central'] = S['rueda_central']
print('   (%.0f s)' % (time.time() - t0))
# satelite del reves
c = np.array(CP.pol(d['r_ejes'], 270.0) + ((d['z_engr0'] + d['z_engr1']) / 2,))
s1 = S['satelite_1'].translate(list(-c)).rotate([0, 180, 0])
mejor = (9e9, 0)
for a10 in range(0, 300, 1):
    q = s1.rotate([0, 0, a10 / 10.0]).translate(list(c))
    v = vol(q, S['rueda_central']) + vol(q, S['bisel']) + vol(q, S['plato'])
    if v < mejor[0]: mejor = (v, a10 / 10.0)
print('SATELITE del reves (cara de arriba abajo): mejor giro propio %.1f grados, pisa %.3f mm3 a rueda central + bisel + plato  -> %s' % (mejor[1], mejor[0], 'vale igual' if mejor[0] <= 0.05 else 'no engrana igual'))
# pasadores y teton: simetria
for n in ('pasador_derecho', 'teton'):
    b = S[n].bounding_box(); cc = [(b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2]
    q = S[n].translate([-x for x in cc]).rotate([180, 0, 0] if n == 'teton' else [0, 0, 180]).translate(cc)
    print('%s dado la vuelta: se diferencia de si mismo en %.4f mm3' % (n, (S[n] - q).volume() + (q - S[n]).volume()))
# bisel volcado, dentro del cuerpo y sobre la caja
bv = vx(S['bisel'])
print('BISEL volcado: asiento contra todo lo demas %.1f mm3; se queda a %.2f mm; dentro del cuerpo pisa %.1f mm3' % (asiento(bv, M)[0], se_queda(bv, M), vol(bv, S['cuerpo'])))
M['bisel'] = S['bisel']
# cuerpo
print('CUERPO: en su sitio pisa a la base %.2f mm3; a medio entrar (2 mm) %.2f mm3' % (vol(S['cuerpo'], S['base']), vol(S['cuerpo'].translate([0, 0, 2.0]), S['base'])))
for a in (90, 180, 270):
    q = gz(S['cuerpo'], a); v, c = asiento(q, M)
    print('   girado %d: en su sitio pisa %.2f mm3 %s; a medio entrar (2 mm) %.2f mm3' % (a, v, c, sum(x for _, x in choque(q.translate([0, 0, 2.0]), M))))
    inter = q ^ S['base']
    for t_ in inter.decompose():
        b = t_.bounding_box()
        if t_.volume() > 0.01: print('        trozo %.2f mm3: x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f' % (t_.volume(), b[0], b[3], b[1], b[4], b[2], b[5]))
for txt, q in (('volcado sobre X', vx(S['cuerpo'])),):
    v, c = asiento(q, M); print('   %s: pisa %.1f mm3 %s' % (txt, v, c[:4]))
M['cuerpo'] = S['cuerpo']
# funda
print('FUNDA')
for a in (0, 90, 180, 270):
    q = gz(S['funda'], a); v, c = asiento(q, M)
    txt = '   girada %d: en su sitio pisa %.2f mm3 %s' % (a, v, c)
    if v > 0.05:
        mejor = None
        for dx in np.arange(-0.45, 0.46, 0.05):
            for dy in np.arange(-0.45, 0.46, 0.05):
                v2 = asiento(q.translate([dx, dy, 0]), M)[0]
                if v2 <= 0.05 and (mejor is None or abs(dx) + abs(dy) < abs(mejor[0]) + abs(mejor[1])): mejor = (dx, dy)
        txt += '; desplazandola dentro de su holgura: %s' % ('ENTRA con dx = %.2f, dy = %.2f mm' % mejor if mejor else 'no entra')
        if mejor:
            q2 = q.translate([mejor[0], mejor[1], 0]); peor = 0
            for i in range(0, 131):
                peor = max(peor, sum(x for _, x in choque(q2.translate([0, 0, 1.0 * i]), {'cuerpo': S['cuerpo'], 'base': S['base'], 'bisel': S['bisel']}, 0.05)))
            txt += '; bajando 130 mm asi desplazada, max %.2f mm3' % peor
    print(txt)
v, c = asiento(vx(S['funda']), M); print('   volcada: pisa %.0f mm3' % v)
print('tiempo %.0f s' % (time.time() - t0))
