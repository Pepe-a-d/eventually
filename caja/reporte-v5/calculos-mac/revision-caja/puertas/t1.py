from comun import *
# columna vertical fina en (x, y): que piezas atraviesa y a que alturas
def columna(x, y, r=0.02):
    c = mf.Manifold.cube([2*r, 2*r, 200]).translate([x-r, y-r, -150])
    out = []
    for n in S:
        if P[n].mueve in ('funda', 'probeta'): continue
        i = S[n] ^ c
        if i.volume() > 0:
            parts = sorted((q.bounding_box()[2], q.bounding_box()[5]) for q in i.decompose())
            out.append((n, [(round(a, 2), round(b, 2)) for a, b in parts]))
    return sorted(out, key=lambda t: -t[1][-1][1])
for pt in ((0.0, 0.0), (0.0, 0.3), (0.0, -0.5), (0.0, 0.7), (25.0, 36.7), (22.0, 36.65), (30.0, 36.7), (10.0, 36.7), (31.2, 10.0)):
    print(pt, columna(*pt)[:5])
# asiento de la puerta cerrada: area de apoyo sobre la meseta
A = S['puerta_derecha'].translate([0, 0, -0.05]) ^ S['meseta']
print('asiento puerta derecha: %.1f mm2 (volumen al bajar 0,05: %.2f mm3); caja %s' % (A.volume() / 0.05, A.volume(), [round(v, 1) for v in A.bounding_box()]))
for q in A.decompose():
    b = q.bounding_box(); print('    trozo %.1f mm2  x %.1f..%.1f  y %.1f..%.1f' % (q.volume() / 0.05, b[0], b[3], b[1], b[4]))
# rueda central girada 180 con meseta girada 180: contra marco y pasadores
rc = S['rueda_central'].rotate([0, 0, 180])
print('rueda central girada 180: pisa marco %.4f, pasadores %.4f, meseta girada 180 %.4f, plato %.4f' % (vol(rc, S['marco']), vol(rc, S['pasador_derecho']) + vol(rc, S['pasador_izquierdo']), vol(rc, S['meseta'].rotate([0, 0, 180])), vol(rc, S['plato'])))
print('rueda central girada 180 frente a la normal: difieren en %.1f mm3' % ((rc - S['rueda_central']).volume() + (S['rueda_central'] - rc).volume()))
print(open('../fase1.txt').read()[:3000])
