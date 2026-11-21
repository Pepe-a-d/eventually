# 3(c): convenios de solido() (manifold3d) frente a lo que hace generador_caja_v5.py, y uso de cada tipo de operacion
import json, math, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, manifold3d as mf
import caja_piezas_v5 as CP
from shapely.geometry import Polygon
from shapely.ops import unary_union
R = '<repositorio>/caja/'
J = json.load(open(R + 'caja-v5-piezas.json', encoding='utf-8')); Jr = json.load(open('regen/caja-v5-piezas.json', encoding='utf-8'))
uso = collections.Counter(); primera = []
for n, q in J['piezas'].items():
    if q['ops'][0]['op'] != '+': primera.append(n)
    for o in q['ops']: uso[(o['t'], o.get('eje', ''), o['op'])] += 1
print('uso de operaciones (tipo, eje, signo):', dict(uso))
print('piezas cuya primera operacion no es suma (el generador la trataria como suma):', primera or 'ninguna')
# sentido de revolve y de twist en manifold3d
s = mf.CrossSection([[(5, 0), (6, 0), (6, 1), (5, 1)]], mf.FillRule.EvenOdd).revolve(16, 90.0); b = s.bounding_box()
print('revolve 90 grados de un perfil en r=5..6: x %.2f..%.2f, y %.2f..%.2f -> %s' % (b[0], b[3], b[1], b[4], 'va de +X hacia +Y (contra el reloj): como supone el generador' if b[4] > 4 and b[1] > -0.1 else 'OJO: sentido contrario'))
s = mf.CrossSection([[(5, -0.5), (6, -0.5), (6, 0.5), (5, 0.5)]], mf.FillRule.EvenOdd).extrude(10.0, 16, 90.0)
top = s.slice(9.999).to_polygons()[0]; c = top.mean(0)
print('extrude con giro +90: el centro de la seccion de arriba queda en (%.2f, %.2f) -> %s' % (c[0], c[1], 'gira contra el reloj: igual que el punto de prueba del generador' if c[1] > 4 else 'OJO: sentido contrario'))
# prisma en eje y / x: se comprueba que solido() pone los puntos (x,z) y (y,z) donde dice el comentario
for eje, esperado in (('y', (1, 5, 2, 3, 7, 4)), ('x', (5, 1, 2, 7, 3, 4))):
    o = {'t': 'prisma', 'eje': eje, 'c0': 5.0, 'c1': 7.0, 'pol': [[[[1, 2], [3, 2], [3, 4], [1, 4]], []]], 'op': '+'}
    b = CP.solido([o]).bounding_box(); print('prisma eje %s, poligono (1..3, 2..4), de 5 a 7: caja' % eje, [round(v, 3) for v in b], 'esperado', esperado, 'BIEN' if all(abs(a - e) < 1e-6 for a, e in zip(b, esperado)) else 'MAL')
# lo mismo con la matriz del generador: eje y: (a,b,c)->(a,-c,b) con c en [-c1,-c0]; eje x: (a,b,c)->(c,a,b)
print('generador, eje y: c en [-7,-5] -> Y = -c en [5,7]; eje x: X = c en [5,7]: mismas cajas (por lectura del codigo); bases a derechas (sin espejo): x^y=z ->', np.cross([1, 0, 0], [0, 0, 1]), '= (0,-1,0) ;', np.cross([0, 1, 0], [0, 0, 1]), '= (1,0,0)')
# cilindros y esferas: 48 caras inscritas -> el programa da menos volumen
print('cilindro de 48 caras inscrito / cilindro exacto: %.5f (-%.2f %%) ; esfera de manifold(48): %.5f' % (48 / (2 * math.pi) * math.sin(2 * math.pi / 48), 100 * (1 - 48 / (2 * math.pi) * math.sin(2 * math.pi / 48)), mf.Manifold.sphere(1, 48).volume() / (4 / 3 * math.pi)))
# la operacion del bisel que difiere entre el JSON del repo y el regenerado: es la misma figura?
a = J['piezas']['bisel']['ops'][7]; b = Jr['piezas']['bisel']['ops'][7]
ga = unary_union([Polygon(q[0], q[1]) for q in a['pol']]); gb = unary_union([Polygon(q[0], q[1]) for q in b['pol']])
print('bisel, operacion 7 (estrias): repo %d poligonos, regenerado %d; area repo %.4f, regen %.4f, diferencia simetrica %.6f mm2; c0,c1 iguales: %s' % (len(a['pol']), len(b['pol']), ga.area, gb.area, ga.symmetric_difference(gb).area, (a['c0'], a['c1']) == (b['c0'], b['c1'])))
# helices: datos
for n, q in J['piezas'].items():
    for i, o in enumerate(q['ops']):
        if o['t'] == 'helice': print('helice en %s op %d: z %.2f..%.2f giro %.3f grados, %d poligonos de %d vertices' % (n, i, o['z0'], o['z1'], o['giro'], len(o['pol']), len(o['pol'][0][0])))
        if o['t'] == 'revol' and abs(o['a1'] - o['a0']) >= 359.999: print('revol completo en %s op %d' % (n, i))
        if o['t'] == 'revol' and (o['a1'] - o['a0']) > 180 and (o['a1'] - o['a0']) < 359.999: print('revol de mas de 180 grados en %s op %d: %.1f' % (n, i, o['a1'] - o['a0']))
# parametros: unidades que usa el generador
unid = collections.Counter(q[1] for q in J['P']); print('unidades en P:', dict(unid), '-> el generador solo traduce "mm" y "grados"; "deg" se queda sin unidad')
