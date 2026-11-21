"""Revision de la caja v5 por la sesion del Mac (22-nov-2026). Lista de comprobacion: cada linea dice 'bien' o 'FALLA'.

Vuelve a construir las piezas con el programa de la sesion del PC (caja/caja_piezas_v5.py) y les hace las pruebas
que ese programa no hace. Sirve para repetir la revision despues de cada arreglo: el objetivo es que no quede
ninguna linea en FALLA.

Necesita Python 3 con numpy, shapely y manifold3d. Desde la raiz del repositorio:
    python caja/reporte-v5/calculos-mac/revisar_caja_v5.py
Tarda unos dos minutos. No escribe ningun fichero.

Son pruebas de GEOMETRIA sobre el modelo: distancias, volumenes que se pisan, capas sin apoyo. No hay ninguna fuerza.
Que una linea diga 'bien' quiere decir que el dibujo cumple, no que la pieza impresa funcione.
"""
import os, sys, math
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get('CAJA_DIR', os.path.normpath(os.path.join(AQUI, '..', '..'))))
import numpy as np
import manifold3d as mf
from shapely.geometry import Polygon
import caja_piezas_v5 as CP, caja_diseno_v5 as D

p, d, d2, P = CP.piezas()
S = {n: CP.solido(q.ops) for n, q in P.items()}
G = p['giro_tubo']
fallos = 0
def linea(ok, txt):
    global fallos
    fallos += 0 if ok else 1
    print(('  bien  ' if ok else '  FALLA ') + txt)
def puesta(n, tau): return CP.mover(S[n], n, P[n].mueve, p, d, tau)
def puerta(sx, ang):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    return S[n].translate([-sx * d['eje_x'], 0, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z']])
def pisa(a, b): return (a ^ b).volume()
hx, hy = d['hueco_x'] / 2, d['hueco_y'] / 2

print('PUERTAS')
# 1. agujero en la junta
tapa = S['puerta_derecha'] + S['puerta_izquierda'] + S['meseta']
libre = mf.CrossSection([[(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]]) - tapa.project()
linea(libre.area() < 0.01, 'cerradas, mirando desde arriba no queda ningun agujero en el hueco de %.0f x %.0f: sin tapar, %.2f mm2' % (2 * hx, 2 * hy, libre.area()))
# 2. las dos puertas entre si mientras abren, y con una adelantada
peor = min((puerta(1, a).min_gap(puerta(-1, a), 3.0), a) for a in np.arange(0.25, 30.01, 0.25))
linea(peor[0] >= 0.2, 'al abrir a la vez, las dos puertas no se acercan a menos de 0,2 mm en la junta: lo mas cerca, %.3f mm, a %.2f grados' % peor)
des = max(pisa(puerta(1, a + 2.0), puerta(-1, a)) + pisa(puerta(1, a), puerta(-1, a + 2.0)) for a in np.arange(0.0, 20.01, 1.0))
linea(des < 0.02, 'con una puerta 2 grados por delante de la otra (el mecanismo deja mas), no se pisan en la junta: %.1f mm3' % des)
# 3. puerta abierta: entre que angulos se deja mover, con el aro en su sitio y con el aro corrido lo que le deja su holgura
aroG = puesta('aro_puertas', G); quieto = S['marco'] + S['meseta'] + puesta('teton', G)
def limite(sx, signo, aro, extra=None):
    for i in range(1, 80):
        a = 90.0 + signo * 0.25 * i
        if pisa(puerta(sx, a), aro) + (pisa(puerta(sx, a), extra) if extra is not None else 0.0) > 0.0005: return a - signo * 0.25
    return 90.0 + signo * 20.0
dentro = min(limite(sx, -1, aroG) for sx in (1, -1)); fuera = max(limite(sx, 1, aroG, S['meseta']) for sx in (1, -1))
linea(dentro >= 85.0 and fuera <= 95.0, 'abiertas, con el aro en su sitio: cada puerta se deja mover entre %.2f y %.2f grados (el brief pide entre 85 y 95)' % (dentro, fuera))
peor_d = 90.0; corr = 0.0
for ang in range(0, 360, 15):
    for r in (0.15, 0.29):
        a2 = aroG.translate([r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang)), 0])
        if pisa(a2, quieto) > 0.0005: continue
        for sx in (1, -1):
            l_ = limite(sx, -1, a2)
            if l_ < peor_d: peor_d, corr = l_, r
linea(peor_d >= 85.0, 'abiertas, con el aro corrido lo que le deja su holgura (%.2f mm, sin pisar marco, meseta ni teton): la puerta cede hacia dentro hasta %.2f grados' % (corr, peor_d))
def reloj_a(ang):
    peor = 9e9
    for tau in np.arange(p['giro_sube'], G + 0.1, 4.0):
        r = puesta('reloj_de_pega', tau)
        for sx in (1, -1):
            q = puerta(sx, ang); peor = min(peor, -pisa(r, q) if pisa(r, q) > 1e-6 else r.min_gap(q, 8.0))
    return peor
g1, g2 = reloj_a(dentro), reloj_a(peor_d)
linea(g1 >= p['reloj_margen'] and g2 >= p['reloj_margen'], 'el reloj de pega, a 3 mm o mas de una puerta que cede hacia dentro: a %.2f grados queda a %s; a %.2f grados, a %s' % (dentro, '%.2f mm' % g1 if g1 >= 0 else 'SE PISAN', peor_d, '%.2f mm' % g2 if g2 >= 0 else 'SE PISAN'))
prisma = mf.Manifold.cube([2 * hx, 2 * hy, 60.0]).translate([-hx, -hy, -20.0])
def entra(ang):                                    # cuanto se mete la puerta en el prisma libre del hueco, en mm
    q = puerta(1, ang) ^ prisma
    return 0.0 if q.volume() < 1e-6 else hx - q.bounding_box()[0]
linea(entra(dentro) < 0.01, 'con el juego de las puertas abiertas, ninguna entra en el prisma libre de %.0f x %.0f: a %.2f grados se mete %.2f mm; a %.2f grados, %.2f mm' % (2 * hx, 2 * hy, dentro, entra(dentro), peor_d, entra(peor_d)))
# 4. varilla y bola contra el aro, cerrada
a0 = puesta('aro_puertas', 0.0)
g = min(S['puerta_derecha'].min_gap(a0, 3.0), S['puerta_izquierda'].min_gap(a0, 3.0))
linea(g >= p['bola_holgura'] - 1e-3, 'cerradas, entre cada puerta (varilla y bola) y el aro quedan %.3f mm; la holgura de diseno de la bola es %.2f' % (g, p['bola_holgura']))

print('ASCENSOR')
peor = min((puesta('plataforma', t_).min_gap(puesta('tubo', t_), 2.0), t_) for t_ in (110.0, 150.0, 200.0, 250.0, 300.0, 330.0))
linea(peor[0] >= 0.15, 'en la rampa, entre los tetones de la plataforma y las ranuras del tubo quedan 0,15 mm o mas (el diseno dice %.2f): lo menos, %.3f mm, con el tubo a %.0f grados' % (p['holg_desliza'], peor[0], peor[1]))
arriba = puesta('plataforma', G) + S['meseta'] + S['marco'] + puerta(1, 90.0) + puerta(-1, 90.0)
rect = mf.CrossSection([[(-d['eje_x'], -d['puerta_y'] / 2 - 0.3), (d['eje_x'], -d['puerta_y'] / 2 - 0.3), (d['eje_x'], d['puerta_y'] / 2 + 0.3), (-d['eje_x'], d['puerta_y'] / 2 + 0.3)]])
ab = (rect - arriba.slice(-0.1)).area(); perim = 2 * (2 * hx + 2 * hy)
linea(ab <= perim * 1.0, 'reloj arriba: alrededor del pedestal, a ras, queda abierta una rendija de 1 mm o menos por lado (como mucho %.0f mm2): quedan abiertos %.0f mm2; delante y detras, una zanja de %.1f mm de ancho y %.1f de hondo' % (perim, ab, d['puerta_y'] / 2 + 0.3 - (hy - p['pedestal_holgura']), p['puerta_grueso']))

print('IMPRESION (capas de 0,2 mm; cuenta lo que no tiene debajo la capa anterior ensanchada 0,25 mm)')
def capa(M, z):
    out = None
    for q in sorted((Polygon(c).buffer(0) for c in M.slice(z).to_polygons() if len(c) >= 3), key=lambda g_: -g_.area):
        out = q if out is None else out.symmetric_difference(q)
    return out if out is not None else Polygon()
def peor_voladizo(nombre, boca_abajo, z0=None, z1=None):
    M = S[nombre].rotate([180, 0, 0]) if boca_abajo else S[nombre]
    b = M.bounding_box(); M = M.translate([0, 0, -b[2]]); ant = None; peor = (0.0, 0.0)
    for i in range(int(round((b[5] - b[2]) / 0.2))):
        z = 0.2 * i + 0.1; c = capa(M, z)
        if ant is not None and (z0 is None or z0 <= z <= z1):
            a = c.difference(ant.buffer(0.25)).area
            if a > peor[0]: peor = (a, z)
        ant = c
    return peor
v = peor_voladizo('bisel', True, 9.0, 14.0)
linea(v[0] < 20.0, 'bisel, boca abajo: el ala se imprime en escalera, sin repisa al aire: %.0f mm2 sin apoyo a %.1f mm de la cama' % v)
v = peor_voladizo('aro_puertas', False)
linea(v[0] < 3.0, 'aro de las puertas: los cuernos nacen sobre el anillo: %.1f mm2 sin apoyo a %.1f mm de la cama' % v)
pared = d['aro_r_ext'] - (d['bola_r_cerrada'] + p['bola_d'] / 2 + p['bola_holgura'])
linea(pared >= 0.8, 'aro de las puertas: la pared de fuera de la pista, en «cerrado», mide %.2f mm (el parametro pista_pared dice %.1f; la boquilla es de 0,4)' % (pared, p['pista_pared']))

print('MONTAJE Y BOCA ABAJO')
def baja(pieza, contra, alto=30.0): return max(pisa(pieza.translate([0, 0, h]), contra) for h in np.arange(0.5, alto + 0.01, 0.5))
print('  nota  ' + 'orden del reporte (rueda central antes que plato y satelites): bajar el plato con la rueda central puesta pisa %.0f mm3, y un satelite, %.1f mm3. En el otro orden (plato, satelites y despues rueda central), %.3f mm3. Es un error del TEXTO del reporte (apartado 7), no de las piezas' % (baja(S['plato'], S['rueda_central']), baja(S['satelite_1'], S['rueda_central']), baja(S['rueda_central'], S['plato'] + S['satelite_1'] + S['satelite_2'] + S['meseta'])))
v = min(pisa(S['cuerpo'].rotate([0, 0, a]), S['base']) for a in (90, 180, 270))
linea(v > 30.0, 'el cuerpo girado un cuarto o media vuelta no asienta en la base: girado pisa solo %.1f mm3 (bien puesto, a presion, hay que vencer %.0f)' % (v, baja(S['cuerpo'], S['base'], 12.0)))
caja = S['cuerpo'] + S['base'] + S['bisel']
v = min(max(pisa(S['funda'].rotate([0, 0, a]).translate([dx, dy, h]), caja) for h in np.arange(0, 130.1, 5.0)) for a in (90, 180, 270) for dx, dy in ((0.2, 0), (-0.2, 0), (0, 0.2), (0, -0.2)))
linea(v > 0.05, 'la funda girada no entra: girada y corrida 0,2 mm (tiene 0,5 de holgura) pisa %.3f mm3' % v)
grupo = S['soporte'] + S['reloj_de_pega']; contra = S['puerta_derecha'] + S['puerta_izquierda'] + S['meseta'] + S['marco']
sube = next((0.25 * (i - 1) for i in range(1, 400) if pisa(grupo.translate([0, 0, 0.25 * i]), contra) > 0.05), 99.0)
linea(sube <= 1.5, 'boca abajo y cerrada, el soporte con el reloj no se mueve mas de 1,5 mm: cae %.2f mm, hasta apoyarse en las puertas' % sube)

print('NINGUN FALLO' if fallos == 0 else 'FALLAN %d COMPROBACIONES' % fallos)
