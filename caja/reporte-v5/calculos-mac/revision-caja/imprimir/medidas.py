# Medidas sueltas de detalles finos: dientes, letras de la frase, paredes junto a las ranuras de iman, pared de la pista del aro,
# alma de las muescas de la plataforma, canto en filo de la meseta, pasador tumbado.
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from shapely.geometry import Point, LineString, box
from shapely.ops import unary_union
from comun import *
p, d, d2, P, S = modelo()

def ancho_local(g, r):
    """Area de lo que tiene menos de 2r de ancho (apertura con esquinas redondas, quitando el redondeo de las esquinas con un margen)."""
    ab = g.buffer(-r).buffer(r * 1.02)
    return g.difference(ab)

print('--- DIENTES (grueso del diente medido en el corte de la pieza, a varias distancias de la punta)')
def grueso_diente(nombre, centro, r_punta, hacia_dentro=False, z=None):
    s, inv = colocada(nombre)
    bb = s.bounding_box(); z = z if z is not None else (bb[5] - 1.0)
    g = a_shapely(s.slice(z))
    out = []
    for dr in (0.02, 0.1, 0.2, 0.3, 0.5, 1.0):
        r = r_punta + dr if hacia_dentro else r_punta - dr
        circ = Point(centro).buffer(r, 720).exterior
        it = circ.intersection(g)
        segs = [q.length for q in (it.geoms if hasattr(it, 'geoms') else [it]) if q.length > 1e-6]
        if hacia_dentro:    # corona interior: el diente es material entre huecos; el circulo corta dientes y fondo
            out.append((dr, min(segs) if segs else 0, len(segs)))
        else:
            out.append((dr, min(segs) if segs else 0, len(segs)))
    return z, out
c1 = CP.pol(d['r_ejes'], 270.0)
for nombre, centro, rp, dentro, z in (('satelite_1', c1, d['r_satelite'] + p['modulo'], False, 3.0), ('rueda_central', (0, 0), d['central_punta'], False, 6.0), ('bisel', (0, 0), d['bisel_punta'], True, 6.0)):
    z, out = grueso_diente(nombre, centro, rp, dentro, z)
    print('  %-14s corte a z %.1f de impresion: ' % (nombre, z), '; '.join('a %.2f mm de la punta: %.2f mm (%d dientes)' % o for o in out))

print('--- FRASE: ancho de los trazos (area de letra que tiene menos de X de ancho) y contraformas')
fr = a_shapely(colocada('frase')[0].slice(0.3))
fu = a_shapely(colocada('funda')[0].slice(0.3))
print('  frase: %d trozos, area %.1f mm2, caja %s' % (len(trozos(fr)), fr.area, [round(v, 1) for v in fr.bounds]))
for w in (0.3, 0.4, 0.45, 0.5, 0.6, 0.8, 1.0, 1.2):
    f = ancho_local(fr, w / 2)
    print('   trazo de menos de %.2f mm: %.2f mm2 (%.1f %% de la letra), en %d trozos de mas de 0,05 mm2' % (w, f.area, 100 * f.area / fr.area, len(trozos(f, 0.05))))
# ancho maximo de trazo (lo que queda al encoger)
for w in (1.0, 1.5, 2.0, 2.5, 3.0):
    print('   queda algo al encoger %.2f por lado (trazos de mas de %.1f mm): %s' % (w / 2, w, 'si' if fr.buffer(-w / 2).area > 0 else 'no'))
islas = sorted(trozos(fu), key=lambda q: q.area)
print('  funda, primera capa: %d trozos; los pequenos (contraformas de las letras): %s' % (len(islas), ', '.join('%.2f mm2 (%.1f x %.1f mm)' % (q.area, q.bounds[2] - q.bounds[0], q.bounds[3] - q.bounds[1]) for q in islas[:-1])))
for w in (0.4, 0.6, 0.8, 1.0):
    f = ancho_local(fu, w / 2)
    print('   funda entre letras de menos de %.2f mm: %.2f mm2 en %d trozos' % (w, f.area, len(trozos(f, 0.05))))
un = fu.union(fr.buffer(0.001))
print('  funda + frase juntas en la primera capa: %d trozo(s), huecos %d, area %.1f (cuadrado %.1f)' % (len(trozos(un)), sum(len(q.interiors) for q in trozos(un)), un.area, d2['funda_lado'] ** 2))

print('--- ARO: pared entre la pista y el borde de fuera del aro (extremo de cerrado), y voladizo del cuerno por dentro')
s, inv = colocada('aro_puertas')
g = a_shapely(s.slice(6.0))
for w in (0.3, 0.4, 0.6, 0.8, 1.2, 1.6):
    f = ancho_local(g, w / 2)
    print('   pared de menos de %.2f mm: %.2f mm2 en %d trozos; el mayor mide %s' % (w, f.area, len(trozos(f, 0.03)), ', '.join('%.1f x %.1f en (%.1f, %.1f)' % (q.bounds[2] - q.bounds[0], q.bounds[3] - q.bounds[1], q.centroid.x, q.centroid.y) for q in sorted(trozos(f, 0.03), key=lambda q: -q.area)[:2])))
r_bola_c = d['bola_r_cerrada']; print('   radio de la bola cerrada %.2f + media pista %.2f = %.2f; radio de fuera del aro %.2f -> pared %.2f mm' % (r_bola_c, p['bola_d'] / 2 + p['bola_holgura'], r_bola_c + p['bola_d'] / 2 + p['bola_holgura'], d['aro_r_ext'], d['aro_r_ext'] - r_bola_c - p['bola_d'] / 2 - p['bola_holgura']))
print('   capa z 6.0: trozos %s' % ', '.join('%.1f mm2' % q.area for q in trozos(g)))
anillo = a_shapely(s.slice(2.9)); c1_ = a_shapely(s.slice(3.1))
vol = c1_.difference(anillo)
for q in trozos(vol, 0.05):
    print('   cuerno fuera del anillo (sin apoyo): %.2f mm2, caja %s, lo mas lejos del anillo %.2f mm' % (q.area, [round(v, 1) for v in q.bounds], alcance(q, anillo)))

print('--- PLATAFORMA: alma que cierra por fuera cada muesca de columna')
s, inv = colocada('plataforma'); g = a_shapely(s.slice(3.0))
for w in (0.4, 0.6, 0.8, 1.0):
    f = ancho_local(g, w / 2)
    print('   de menos de %.2f mm: %.2f mm2 en %d trozos: %s' % (w, f.area, len(trozos(f, 0.05)), ', '.join('%.1f mm2 caja %.1f x %.1f' % (q.area, q.bounds[2] - q.bounds[0], q.bounds[3] - q.bounds[1]) for q in sorted(trozos(f, 0.05), key=lambda q: -q.area)[:3])))
print('   radio del disco %.2f - radio de fuera de la muesca %.2f = %.2f mm de alma; largo del arco %.1f mm; alto %.1f mm' % (p['tubo_r'] - 0.7, 74.2 + p['holg_gira'] + 0.1, p['tubo_r'] - 0.7 - 74.2 - p['holg_gira'] - 0.1, math.radians(16 + 2 * math.degrees(0.35 / 70)) * 75, p['disco_grueso']))

print('--- RANURAS DE IMAN: paredes alrededor (tubo y base)')
for nombre, z in (('tubo', 12.0), ('base', 16.5)):
    s, inv = colocada(nombre); g = a_shapely(s.slice(z))
    for w in (0.4, 0.6, 0.8, 1.0, 1.2):
        f = ancho_local(g, w / 2)
        print('   %s z %.1f: de menos de %.2f mm: %.2f mm2 en %d trozos: %s' % (nombre, z, w, f.area, len(trozos(f, 0.05)), ', '.join('%.1f mm2 caja %.1f x %.1f en (%.1f, %.1f)' % (q.area, q.bounds[2] - q.bounds[0], q.bounds[3] - q.bounds[1], q.centroid.x, q.centroid.y) for q in sorted(trozos(f, 0.05), key=lambda q: -q.area)[:4])))

print('--- MESETA: aleta entre el hueco y la cuna de la bisagra (ancho capa a capa en x, a y = 0)')
s, inv = colocada('meseta')
for i in range(5, 14):
    z = (i + 0.5) * CAPA + EPS_Z; g = a_shapely(s.slice(z))
    it = LineString([(20, 0.5), (34, 0.5)]).intersection(g)
    print('   z %.1f (pieza %.1f): material en x: %s' % (z, z - 8.0, ', '.join('%.2f..%.2f (%.2f)' % (q.bounds[0], q.bounds[2], q.length) for q in (it.geoms if hasattr(it, 'geoms') else [it]) if q.length > 1e-6)))

print('--- PASADOR tumbado: ancho de cada capa')
s, inv = colocada('pasador_derecho')
ant = None
for i in range(15):
    z = (i + 0.5) * CAPA + EPS_Z; g = a_shapely(s.slice(z)); w = g.bounds[2] - g.bounds[0]
    print('   z %.1f: ancho %.2f mm%s' % (z, w, '' if ant is None else '  (sale %.2f mm por lado sobre la de debajo -> %.0f grados con la vertical)' % ((w - ant) / 2, math.degrees(math.atan2((w - ant) / 2, CAPA)))))
    ant = w
