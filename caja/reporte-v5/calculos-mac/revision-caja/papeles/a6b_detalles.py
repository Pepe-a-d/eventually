# Detalles sueltos: ala del bisel, pared entre ranuras del tubo, rendijas pasantes de la tapa, punta del diente, json viejo
from comun import *
import json
from shapely.geometry import Polygon, box as sbox
def cs2shp(cs):
    out = [Polygon(q) for q in cs.to_polygons() if len(q) >= 3]
    out.sort(key=lambda g: -g.area); res = None
    for g in out:
        g = g.buffer(0); res = g if res is None else res.symmetric_difference(g)
    return res if res is not None else Polygon()
print('--- ala del bisel (el codigo dice "en escalera: se imprime sin soportes")')
for z in (-11.3, -11.45, -11.6, -12.0, -12.3, -13.1, -14.3):
    pol = S['bisel'].slice(z).to_polygons(); print('   z=%.2f  radio exterior %.3f' % (z, max(np.hypot(q[:, 0], q[:, 1]).max() for q in pol)))
print('   cuerpo: agujero del labio r=%.3f ; ala r=%.3f ; cara de arriba del ala z=%.2f ; cara de abajo del labio z=%.2f' % (d['bisel_r_ext'] + 0.4, d['bisel_ala_r'], d['z_cuerpo_arriba'] - 3.0 - p['aire'], d['z_cuerpo_arriba'] - 3.0))
print('--- punta del diente del satelite (exacto, de la formula de engranaje())')
m_, z_ = p['modulo'], int(p['z_satelite']); rp = m_ * z_ / 2; rb_ = rp * math.cos(math.radians(20)); inv = lambda a: math.tan(a) - a
medio = (math.pi * m_ / 2 - p['juego_dientes'] / 2) / 2 / rp
for nom, r in (('punta', rp + m_), ('primitivo', rp), ('media altura', (rp + m_ + rp - 1.25 * m_) / 2)):
    semi = medio + inv(math.radians(20)) - inv(math.acos(rb_ / max(r, rb_))); print('   %s (r=%.3f): grueso %.3f mm (medio grueso %.3f)' % (nom, r, 2 * semi * r, semi * r))
print('--- tubo: pared minima entre ranuras, medida en el solido (columna de 0,1 x 0,1 pegada a la cara interior, cada grado)')
tu = S['tubo']; peor = (9e9, 0, 0)
for r_ in (76.05, 77.0, 78.0):
    peor = (9e9, 0, 0)
    for a in np.arange(0, 360, 1.0):
        col = caja(r_, -0.05, -130, r_ + 0.1, 0.05, 0).rotate([0, 0, float(a)])
        tr = (tu ^ col).decompose()
        runs = sorted((bb(t)[2], bb(t)[5]) for t in tr if t.volume() > 1e-6)
        for z0, z1 in runs:
            if z0 > d['z_suelo'] + 0.7 and z1 < d['z_plato0'] - 0.1 and z1 - z0 < peor[0]: peor = (z1 - z0, float(a), z0)
    print('   a r=%.2f: tramo de pared mas corto entre dos ranuras: %.2f mm (angulo %g, z de %.2f a %.2f)' % (r_, peor[0], peor[1], peor[2], peor[2] + peor[0]))
print('   grueso de pared que queda detras de la ranura: %.2f mm (pared %.1f, fondo de ranura a r=%.2f)' % (d['tubo_r_ext'] - (p['tubo_r'] + p['rampa_fondo'] - 0.4 + p['holg_desliza'] + 0.1), p['tubo_pared'], p['tubo_r'] + p['rampa_fondo'] - 0.4 + p['holg_desliza'] + 0.1))
print('--- tapa cerrada: lineas de vision verticales que atraviesan puertas + meseta dentro del rebaje')
proy = cs2shp((S['puerta_derecha'] + S['puerta_izquierda'] + S['meseta']).project())
zona = sbox(-d['eje_x'] - 4.5, -d['puerta_y'] / 2 - 0.3, d['eje_x'] + 4.5, d['puerta_y'] / 2 + 0.3)
hue = zona.difference(proy)
for g in (hue.geoms if hasattr(hue, 'geoms') else [hue]):
    if g.area > 1e-4:
        col = caja(g.bounds[0], g.bounds[1], -200, g.bounds[2], g.bounds[3], 5)
        debajo = sorted(((bb(col ^ puesta(n, 0))[5], n) for n in CAJA if vol(col, puesta(n, 0)) > 1e-6), reverse=True)[:3]
        print('   rendija pasante x %.2f..%.2f  y %.2f..%.2f  area %.3f mm2 ; debajo: %s' % (g.bounds[0], g.bounds[2], g.bounds[1], g.bounds[3], g.area, [(n, round(z, 1)) for z, n in debajo]))
print('--- caja-v5.json del repo: juego de las puertas que guarda (formula de la fase 1) frente al 3D')
Jd = json.load(open('<repositorio>/caja/caja-v5.json', encoding='utf-8'))
print('   baile_abierta %.2f, baile_cerrada %.2f ; parametros en P_DEF del json: %d (en el codigo: %d) ; falta: %s' % (Jd['d'].get('baile_abierta', -1), Jd['d'].get('baile_cerrada', -1), len(Jd['P_DEF']), len(D.P_DEF), {q[0] for q in D.P_DEF} - {q[0] for q in Jd['P_DEF']}))
print('   seccion_puerta_a del json: %d puntos; x min %.2f (labio rectangular de media madera: %s)' % (len(Jd['seccion_puerta_a']), min(q[0] for q in Jd['seccion_puerta_a']), 'si' if any(abs(q[1] - (-2.5 + 1.0)) < 1e-6 for q in Jd['seccion_puerta_a']) else 'no'))
print('--- parametros de la lista que no cambian nada en las piezas')
import importlib, os
base_ops = json.dumps({n: q.ops for n, q in P.items()}, sort_keys=True)
for nombre in ('labio_grueso', 'labio_largo', 'labio_hueco', 'reloj_cabeza_d', 'reloj_ancho', 'reloj_grueso', 'margen_reloj_abajo'):
    v0 = p[nombre]; os.environ['CAJA_PRUEBA'] = '%s=%g' % (nombre, v0 + 0.5)
    try:
        p2, d_2, d2_2, P2 = CP.piezas(); camb = [n for n in P if json.dumps(P2[n].ops, sort_keys=True) != json.dumps(P[n].ops, sort_keys=True)]
        print('   %s +0.5: cambian %d piezas %s' % (nombre, len(camb), camb[:8]))
    except Exception as e: print('   %s: error %s' % (nombre, e))
os.environ['CAJA_PRUEBA'] = ''
