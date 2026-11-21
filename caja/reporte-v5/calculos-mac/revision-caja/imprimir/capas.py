# Corta cada pieza, en su postura de impresion, en capas de 0,2 mm y busca:
#   voladizos (lo que no tiene debajo la capa anterior ensanchada 0,2 o 0,3 mm), puentes, islas que empiezan en el aire,
#   detalles finos (<0,4 y <0,8 mm de ancho), laminas de una sola capa, primera capa y tamano.
# Uso:  python capas.py [pieza ...]      (sin argumentos: todas). Escribe capas-<pieza>.json y un resumen por pantalla.
import sys, json, math, time, os
import numpy as np
import shapely
from shapely.geometry import Point
from shapely.ops import unary_union
from comun import *

TOL = 0.02                       # tolerancia: un voladizo de 45 grados exactos hecho de facetas no cuenta
A_MIN = 0.03                     # mm2: trozos mas pequenos que esto no se miran

def analiza(nombre, boca_abajo=None, verbose=True, solido=None):
    s, inv = colocada(nombre if solido is None else solido, ORIENT.get(nombre) if boca_abajo is None else boca_abajo)
    bb = s.bounding_box()
    L = capas(s)
    res = {'pieza': nombre, 'caja': [bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]], 'n_capas': len(L), 'cuerpos': len(s.decompose()),
           'volumen': s.volume(), 'hallazgos': [], 'finos': [], 'laminas': [], 'por_capa': []}
    # primera capa
    z0, g0 = L[0]
    m = s.to_mesh(); V = np.asarray(m.vert_properties)[:, :3]; T = np.asarray(m.tri_verts)
    a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    vol6 = np.einsum('ij,ij->i', a, np.cross(b, c)); cdg = ((a + b + c) * vol6[:, None]).sum(0) / (4 * vol6.sum())
    casco = g0.convex_hull
    res['primera'] = {'area': g0.area, 'trozos': len(trozos(g0)), 'area_caja': (bb[3] - bb[0]) * (bb[4] - bb[1]),
                      'cdg': [float(x) for x in cdg], 'cdg_dentro': bool(casco.contains(Point(cdg[0], cdg[1]))),
                      'margen_cdg': float(casco.exterior.distance(Point(cdg[0], cdg[1]))) if casco.geom_type == 'Polygon' else 0.0,
                      'ancho_min_apoyo': float(min(casco.minimum_rotated_rectangle.exterior.coords[i][0] for i in range(1)) if False else ancho_min(casco)),
                      'alto': bb[5]}
    prev = None
    for i, (z, g) in enumerate(L):
        fila = {'i': i, 'z': round(z, 3), 'area': g.area, 'u45': 0.0, 'u56': 0.0}
        if prev is not None:
            u45 = g.difference(prev.buffer(CAPA + TOL, 8))
            u56 = g.difference(prev.buffer(0.3 + TOL, 8))
            fila['u45'] = u45.area; fila['u56'] = u56.area
            # islas: trozos enteros de la capa que no tocan la de debajo
            for q in trozos(g, A_MIN):
                if not q.intersects(prev.buffer(0.01)):
                    cx, cy = q.representative_point().coords[0]
                    res['hallazgos'].append({'tipo': 'isla', 'i': i, 'z': round(z, 3), 'area': q.area, 'xy': [cx, cy], 'pieza_xyz': inv(cx, cy, z), 'caja': q.bounds})
            for q in trozos(u45, A_MIN):
                al = alcance(q, prev)
                if al < 0.45: continue                        # menos de 0,45 mm fuera de la capa de debajo: ni se mira
                una, pp, frac = puente(q, prev)
                cx, cy = q.representative_point().coords[0]
                a56 = q.intersection(u56).area if not u56.is_empty else 0.0
                res['hallazgos'].append({'tipo': 'puente' if math.isfinite(una) else ('medio' if frac > 0.5 else 'voladizo'), 'i': i, 'z': round(z, 3),
                                         'area': q.area, 'area56': a56, 'alcance': al, 'luz': una, 'luz_pp': pp, 'frac': frac,
                                         'xy': [cx, cy], 'pieza_xyz': inv(cx, cy, z), 'caja': q.bounds})
        # finos en planta
        for r, clave in ((0.2, 'f04'), (0.4, 'f08')):
            fino = g.difference(abrir(g, r).buffer(0.01))
            fila[clave] = fino.area
            for q in trozos(fino, 0.02):
                cx, cy = q.representative_point().coords[0]
                res['finos'].append({'r': r, 'i': i, 'z': round(z, 3), 'area': q.area, 'xy': [cx, cy], 'pieza_xyz': inv(cx, cy, z), 'caja': q.bounds})
        # ranuras estrechas (<0,3 mm) dentro de la propia pieza: se sueldan
        cierre = g.buffer(0.15, join_style=2, mitre_limit=5).buffer(-0.15, join_style=2, mitre_limit=5).difference(g.buffer(0.01))
        fila['ranura03'] = cierre.area
        # laminas de una sola capa: material que no tiene material ni debajo ni encima
        arriba = L[i + 1][1] if i + 1 < len(L) else None
        if prev is not None and arriba is not None:
            lam = abrir(g.difference(prev).difference(arriba), 0.2)
            fila['lamina1'] = lam.area
            for q in trozos(lam, 0.1):
                cx, cy = q.representative_point().coords[0]
                res['laminas'].append({'i': i, 'z': round(z, 3), 'area': q.area, 'xy': [cx, cy], 'pieza_xyz': inv(cx, cy, z), 'caja': q.bounds})
        res['por_capa'].append(fila)
        prev = g
    return res

def ancho_min(casco):
    if casco.is_empty or casco.geom_type != 'Polygon': return 0.0
    r = casco.minimum_rotated_rectangle
    if r.geom_type != 'Polygon': return 0.0
    c = list(r.exterior.coords)
    return float(min(math.dist(c[0], c[1]), math.dist(c[1], c[2])))

def resumen(res):
    n = res['pieza']; pr = res['primera']
    print('=' * 110)
    print('%s   caja %.1f x %.1f x %.1f mm   capas %d   cuerpos %d   volumen %.0f mm3' % (n, *res['caja'], res['n_capas'], res['cuerpos'], res['volumen']))
    print('  primera capa: %.0f mm2 en %d trozos (%.0f %% de la caja envolvente); ancho minimo del apoyo %.1f mm; alto %.1f; centro de gravedad %s el apoyo (a %.1f mm del borde)' % (
        pr['area'], pr['trozos'], 100 * pr['area'] / pr['area_caja'], pr['ancho_min_apoyo'], pr['alto'], 'DENTRO de' if pr['cdg_dentro'] else 'FUERA de', pr['margen_cdg']))
    H = res['hallazgos']
    for tipo in ('isla', 'voladizo', 'medio', 'puente'):
        hs = [h for h in H if h['tipo'] == tipo]
        if not hs: continue
        # agrupar por capas seguidas y sitio parecido
        grupos = []
        for h in sorted(hs, key=lambda h: (h['i'])):
            for g in grupos:
                if h['i'] - g[-1]['i'] <= 1 and math.dist(h['xy'], g[-1]['xy']) < 6.0 and h['i'] != g[-1]['i']:
                    g.append(h); break
            else:
                grupos.append([h])
        print('  %s: %d trozos en %d grupos' % (tipo.upper(), len(hs), len(grupos)))
        grupos.sort(key=lambda g: -max(h.get('alcance', 99) for h in g))
        for g in grupos[:40]:
            peor = max(g, key=lambda h: h.get('alcance', 99))
            print('     z %.1f..%.1f (%d capas)  en impresion xy (%.1f, %.1f)  en la pieza (%.1f, %.1f, %.1f)  area max %.2f mm2 (suma %.1f)  alcance max %.2f mm  luz %s  luz punto a punto %s  caja %s' % (
                g[0]['z'], g[-1]['z'], len(g), peor['xy'][0], peor['xy'][1], *peor['pieza_xyz'], max(h['area'] for h in g), sum(h['area'] for h in g),
                peor.get('alcance', float('nan')), ('%.1f' % peor['luz']) if math.isfinite(peor.get('luz', math.inf)) else '-',
                ('%.1f' % peor['luz_pp']) if math.isfinite(peor.get('luz_pp', math.inf)) else '-', '(%.1f %.1f %.1f %.1f)' % tuple(peor['caja'])))
        if len(grupos) > 40: print('     ... y %d grupos mas' % (len(grupos) - 40))
    for r in (0.2, 0.4):
        fs = [f for f in res['finos'] if f['r'] == r]
        if fs:
            zs = sorted(set(f['z'] for f in fs))
            peor = max(fs, key=lambda f: f['area'])
            print('  FINOS de menos de %.1f mm: %d trozos en %d capas (z %.1f..%.1f); el mayor %.2f mm2 en z %.1f, pieza (%.1f, %.1f, %.1f); area total por capa hasta %.2f mm2' % (
                2 * r, len(fs), len(zs), zs[0], zs[-1], peor['area'], peor['z'], *peor['pieza_xyz'], max(c['f04' if r == 0.2 else 'f08'] for c in res['por_capa'])))
    ra = max(c['ranura03'] for c in res['por_capa'])
    if ra > 0.05: print('  RANURAS de menos de 0,3 mm dentro de la pieza: hasta %.2f mm2 por capa (capa z %.1f)' % (ra, max(res['por_capa'], key=lambda c: c['ranura03'])['z']))
    if res['laminas']:
        peor = max(res['laminas'], key=lambda f: f['area'])
        print('  LAMINAS de una capa: %d trozos; la mayor %.2f mm2 en z %.1f, pieza (%.1f, %.1f, %.1f)' % (len(res['laminas']), peor['area'], peor['z'], *peor['pieza_xyz']))

if __name__ == '__main__':
    nombres = sys.argv[1:] or list(ORIENT)
    for n in nombres:
        t = time.time()
        res = analiza(n)
        json.dump(res, open(os.path.join(AQUI, 'capas-%s.json' % n), 'w'), default=float)
        resumen(res)
        print('  (%.0f s)' % (time.time() - t))
