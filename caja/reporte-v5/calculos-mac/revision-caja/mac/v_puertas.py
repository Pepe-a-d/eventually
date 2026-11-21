"""Sesion del Mac: comprobacion propia de los hallazgos de puertas (E1, E3, E4)."""
import sys, os
sys.path.insert(0, os.environ.get('CAJA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
import manifold3d as mf, numpy as np
import caja_piezas_v5 as CP, caja_diseno_v5 as D
p, d, d2, P = CP.piezas(); S = {n: CP.solido(q.ops) for n, q in P.items()}
G = p['giro_tubo']
def puesta(n, tau): return CP.mover(S[n], n, P[n].mueve, p, d, tau)
def puerta(sx, ang):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    return S[n].translate([-sx*d['eje_x'], 0, -d['eje_z']]).rotate([0, sx*ang, 0]).translate([sx*d['eje_x'], 0, d['eje_z']])
# E1: columna vertical fina por la junta, puertas cerradas
print('E1. Agujero en la junta (puertas cerradas): volumen que una aguja vertical de 0,1 x 0,1 mm comparte con puertas y meseta')
tapa = S['puerta_derecha'] + S['puerta_izquierda'] + S['meseta']
for y in (-3.0, -0.7, -0.5, -0.3, 0.0, 0.3, 0.5, 0.7, 3.0, 20.0):
    aguja = mf.Manifold.cube([0.1, 0.1, 40.0]).translate([-0.05, y - 0.05, -30.0])
    print('   y = %5.1f: %.5f mm3 %s' % (y, (aguja ^ tapa).volume(), '<-- pasa la luz' if (aguja ^ tapa).volume() < 1e-9 else ''))
# area sin tapar dentro del hueco, vista desde arriba (proyeccion)
hx, hy = d['hueco_x']/2, d['hueco_y']/2
pr = tapa.project()
hueco = mf.CrossSection([[(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]])
libre = hueco - pr
print('   area del hueco de %.0f x %.0f sin tapar, mirando en vertical: %.3f mm2; trozos: %s' % (2*hx, 2*hy, libre.area(), [[round(float(v), 2) for v in np.r_[np.min(q, 0), np.max(q, 0)]] for q in libre.to_polygons()]))
# E3: reloj contra puerta inclinada hacia dentro
print('E3. Reloj de pega contra una puerta abierta que cede hacia dentro (minimo en todo el recorrido de subida)')
for inc in (0.0, 2.85, 3.75, 5.0, 7.5):
    peor = (9e9, 0)
    for tau in np.arange(92, G + 0.1, 4.0):
        r = puesta('reloj_de_pega', tau)
        for sx in (1, -1):
            pt = puerta(sx, 90 - inc)
            g = r.min_gap(pt, 8.0); v = (r ^ pt).volume()
            if v > 1e-6: g = -v
            if g < peor[0]: peor = (g, tau)
    print('   puerta a %.2f grados: %s (tubo a %.0f)' % (90 - inc, ('%.2f mm' % peor[0]) if peor[0] >= 0 else ('SE PISAN %.2f mm3' % -peor[0]), peor[1]))
# E4: plato bajando con la rueda central ya puesta
print('E4. Montaje: bajar el plato con la rueda central ya puesta (paso 10 despues del paso 8)')
peor = max(((S['plato'].translate([0, 0, h]) ^ S['rueda_central']).volume(), h) for h in np.arange(0, 60.01, 0.25))
print('   lo mas que se pisan: %.0f mm3, con el plato %.2f mm por encima de su sitio' % peor)
print('   radio interior del plato %.2f; la rueda central llega a radio %.2f (placa) y sus dientes a %.2f' % (d['plato_r_in'], d2['R_placa'], d['central_punta']))
peor2 = max(((S['rueda_central'].translate([0, 0, h]) ^ (S['plato'] + S['meseta'] + S['marco'] + S['teton'])).volume(), h) for h in np.arange(0.25, 60.01, 0.25))
print('   orden contrario (plato antes, rueda central despues): lo mas que se pisan %.3f mm3' % peor2[0])
