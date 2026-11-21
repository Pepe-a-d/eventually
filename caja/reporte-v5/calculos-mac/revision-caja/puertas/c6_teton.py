# Comprobacion 6: el teton suelto
from comun import *
from shapely.geometry import Polygon
EPS = 1e-4
bt = S['teton'].bounding_box()
z_ala1 = d['z_ala1']; z_ran = z_ala1 - 2.8; z_a0, z_a1 = d['z_corr0'], d['z_corr1']; z_p0 = d['z_plato0']; z_esp1 = z_p0 + p['espiral_fondo']
print('teton: diametro %.1f, largo %.2f, de z = %.2f a %.2f' % (bt[3] - bt[0], bt[5] - bt[2], bt[2], bt[5]))
print('ranura del marco: z %.2f a %.2f | brazo del aro: z %.2f a %.2f | espiral del plato: z %.2f a %.2f' % (z_ran, z_ala1, z_a0, z_a1, z_p0, z_esp1))
for nom, dz in (('como esta dibujado (flotando 0,3 sobre el suelo de la ranura)', 0.0), ('apoyado en el suelo de la ranura del marco (lo real, de pie)', z_ran - bt[2]), ('contra el techo de la espiral (boca abajo)', z_esp1 - bt[5])):
    z0, z1 = bt[2] + dz, bt[5] + dz
    print('  %s: metido %.2f mm en el marco, %.2f en el brazo, %.2f en la espiral; al aire entre ranuras %.2f' % (nom, z_ala1 - z0, min(z1, z_a1) - max(z0, z_a0), z1 - z_p0, (z_a0 - z_ala1) + (z_p0 - z_a1)))
# margenes en los extremos del recorrido: cuanto puede seguir el teton en cada ranura mas alla de su sitio
print('extremos: cuanto mas puede moverse el teton a lo largo de cada ranura, desde su sitio')
for tau in (0.0, 345.0):
    s, psi, ang, h = D.movimiento(p, d, tau)
    T = mv('teton', tau); A = mv('aro_puertas', tau); PL = mv('plato', tau)
    fuera = bisec(lambda e: vol(T.translate([0, e, 0]), S['marco']) > EPS, 0, 4, 12); dentro = bisec(lambda e: vol(T.translate([0, -e, 0]), S['marco']) > EPS, 0, 20, 14)
    print('  tubo %.0f: en la ranura del marco puede ir %.2f mm mas hacia fuera y %.2f hacia dentro' % (tau, fuera, dentro))
    # en el brazo: a lo largo de la ranura (se gira el aro lo que haga falta): se mide la distancia del teton al fondo de la ranura en su direccion
    fuera = bisec(lambda e: vol(T.translate([0, e, 0]), PL) > EPS, 0, 4, 12); dentro = bisec(lambda e: vol(T.translate([0, -e, 0]), PL) > EPS, 0, 4, 12)
    print('           en la espiral (plato quieto) puede moverse %.2f mm hacia fuera y %.2f hacia dentro (holgura radial)' % (fuera, dentro))
    g1 = T.min_gap(A, 3); print('           distancia teton-aro %.3f' % g1)
# giro del plato mas alla de los topes (la espiral sigue 3 grados)
for tau, sg in ((0.0, -1), (345.0, 1)):
    T = mv('teton', tau)
    e = bisec(lambda e: vol(T, S['plato'].rotate([0, 0, CP.ROT * (tau + sg * e)])) > EPS, 0, 6, 12)
    print('  tubo %.0f: la espiral sigue %.2f grados mas alla del tope antes de tocar el teton' % (tau, e))
# la ranura del brazo y la del marco: estan cerradas por fuera?
sec = S['aro_puertas'].slice((z_a0 + z_a1) / 2).to_polygons()
print('planta del aro a media altura: %d contornos (1 exterior + agujeros). Areas: %s' % (len(sec), [round(Polygon(q).area, 1) for q in sec]))
Rt0 = d['espiral_r_cerrada']; wt = p['teton_d'] / 2 + p['holg_desliza']
print('  la ranura del brazo llega a radio %.2f; el brazo se recorta a radio %.2f  -> %s' % (Rt0 + 13 * 3 / 40 + wt, p['tubo_r'] - 0.8, 'la ranura queda ABIERTA por la punta del brazo (horquilla)' if Rt0 + 13 * 3 / 40 + wt > p['tubo_r'] - 0.8 else 'cerrada'))
print('  la ranura del marco llega a radio %.2f; el ala mide %.2f de radio -> %s' % (Rt0 + 1.0 + wt, p['tubo_r'] - 0.8, 'ABIERTA por el borde del ala' if Rt0 + 1 + wt > p['tubo_r'] - 0.8 else 'cerrada'))
# ancho de la boca abierta
caja_boca = mf.Manifold.cube([8, 3, 2.0]).translate([-4 + 0, p['tubo_r'] - 0.8 - 3 + 0.001, z_a0 + 0.5])
tip = (S['aro_puertas'] ^ caja_boca)
print('  punta del brazo (ultimos 3 mm): %d trozos sueltos' % len(tip.decompose()))
for q in tip.decompose():
    b = q.bounding_box(); print('     trozo x %.2f..%.2f  y %.2f..%.2f  vol %.1f' % (b[0], b[3], b[1], b[4], q.volume()))
tip = (S['marco'] ^ mf.Manifold.cube([8, 1.0, 1.0]).translate([-4, p['tubo_r'] - 0.8 - 1.0, z_ala1 - 1.5]))
for q in tip.decompose():
    b = q.bounding_box(); print('  borde del ala junto a la ranura: trozo x %.2f..%.2f  y %.2f..%.2f' % (b[0], b[3], b[1], b[4]))
