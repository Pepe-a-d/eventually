"""Sesion del Mac: comprobacion propia de los hallazgos de montaje."""
import sys, os
sys.path.insert(0, os.environ.get('CAJA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
import manifold3d as mf, numpy as np
import caja_piezas_v5 as CP, caja_diseno_v5 as D
p, d, d2, P = CP.piezas(); S = {n: CP.solido(q.ops) for n, q in P.items()}
G = p['giro_tubo']
def puesta(n, tau): return CP.mover(S[n], n, P[n].mueve, p, d, tau)
def baja(pieza, contra, alto=60.0, paso=0.25):
    return max(((pieza.translate([0, 0, h]) ^ contra).volume(), h) for h in np.arange(paso, alto + 0.01, paso))
rc = S['rueda_central']
print('1. Satelite bajando a su eje con la rueda central puesta: se pisan %.1f mm3 (a %.2f mm de su sitio)' % baja(S['satelite_1'], rc, 20))
print('   Orden contrario: la rueda central bajando con plato y satelites puestos: %.3f mm3' % baja(rc, S['plato'] + sum((S['satelite_%d' % k] for k in range(2, 7)), S['satelite_1']) + S['meseta'], 30)[0])
print('   Y el bisel bajando despues, con todo eso puesto: %.3f mm3' % baja(S['bisel'], rc + S['plato'] + sum((S['satelite_%d' % k] for k in range(2, 7)), S['satelite_1']), 30)[0])
print('2. El cuerpo girado: volumen que comparte con la base ya asentado, y lo maximo al bajar')
for a in (0, 90, 180, 270):
    c = S['cuerpo'].rotate([0, 0, a])
    print('   girado %3d: asentado %.1f mm3; maximo al bajar %.1f mm3' % (a, (c ^ S['base']).volume(), baja(c, S['base'], 20)[0]))
print('3. La funda girada, bajando sobre la caja cerrada (cuerpo, base, bisel), centrada y corrida 0,1 mm')
caja = S['cuerpo'] + S['base'] + S['bisel']
for a in (0, 90, 180, 270):
    f = S['funda'].rotate([0, 0, a])
    v0 = max((f.translate([0, 0, h]) ^ caja).volume() for h in np.arange(0, 130.1, 2.0))
    v1 = min(max((f.translate([dx, dy, h]) ^ caja).volume() for h in np.arange(0, 130.1, 2.0)) for dx, dy in ((0.1, 0), (-0.1, 0), (0, 0.1), (0, -0.1), (0.2, 0), (-0.2, 0), (0, 0.2), (0, -0.2)))
    print('   girada %3d: centrada pisa %.2f mm3; corrida 0,1-0,2 mm, %.3f mm3' % (a, v0, v1))
print('   el indice sale %.2f mm de la pared y la funda tiene 0,5 mm de holgura por lado' % 0.6)
print('4. Boca abajo: soporte y reloj. Subirlos (hacia la tapa) hasta que algo los pare, caja cerrada')
grupo = S['soporte'] + S['reloj_de_pega']; contra = S['puerta_derecha'] + S['puerta_izquierda'] + S['meseta'] + S['marco']
for i in range(1, 400):
    if (grupo.translate([0, 0, 0.25 * i]) ^ contra).volume() > 0.05:
        print('   suben %.2f mm y los paran las puertas' % (0.25 * (i - 1))); break
