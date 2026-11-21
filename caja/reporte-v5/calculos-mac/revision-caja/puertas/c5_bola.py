# Comprobacion 5: la bola en la pista y la varilla, a lo largo de todo el movimiento
from comun import *
import trimesh
z_cuerno1 = S['aro_puertas'].bounding_box()[5]
z_pista0 = d['z_corr0'] + 1.2
print('pared de la pista: de z = %.3f (suelo de la pista) a z = %.3f (canto de arriba de los cuernos). Anillo del aro: %.2f a %.2f' % (z_pista0, z_cuerno1, d['z_corr0'], d['z_corr1']))
print('techo de la ventana de la meseta sobre los cuernos: z = %.3f  -> el aro puede subir %.2f mm hasta tocarlo; bajo el aro hay %.2f mm hasta el ala; sobre el brazo, %.2f hasta el plato' % (z_cuerno1 + 0.6, 0.6, d['z_corr0'] - d['z_ala1'], d['z_plato0'] - d['z_corr1']))
print(' tubo  psi  puerta | centro bola z | ecuador bajo el canto del cuerno | bola dentro de la pista (alto) | bola-aro  varilla-aro  bola-meseta  varilla-meseta  cuerpo-aro (mm)')
peor = {}
for tau in [0, 45, 55, 60, 62, 63, 64, 65, 66, 68, 70, 72, 74, 76, 78, 80, 81, 82, 83, 84, 86, 90, 100]:
    s, psi, ang, h = D.movimiento(p, d, tau)
    A = mv('aro_puertas', tau)
    zc = d['eje_z'] - p['manivela_r'] * math.cos(math.radians(45 - ang))
    b = gira_puerta(BOLA_D, 1, ang); v = gira_puerta(VARILLA_D, 1, ang); c = gira_puerta(CUERPO_D, 1, ang)
    g = [b.min_gap(A, 3), v.min_gap(A, 3), b.min_gap(S['meseta'], 3), v.min_gap(S['meseta'], 3), c.min_gap(A, 3)]
    print(' %5.1f %5.2f %6.2f | %7.3f | %6.3f | %5.2f de 5.00 | %s' % (tau, psi, ang, zc, z_cuerno1 - zc, z_cuerno1 - (zc - 2.5), '  '.join('%6.3f' % x for x in g)))
# barrido fino de las distancias
gm = {'bola-aro': (9, 0), 'varilla-aro': (9, 0), 'bola-meseta': (9, 0), 'varilla-meseta': (9, 0), 'cuerpo-aro': (9, 0)}
for tau in np.arange(40, 105.01, 0.25):
    s, psi, ang, h = D.movimiento(p, d, tau)
    A = mv('aro_puertas', tau)
    b = gira_puerta(BOLA_D, 1, ang); v = gira_puerta(VARILLA_D, 1, ang); c = gira_puerta(CUERPO_D, 1, ang)
    for k, g in (('bola-aro', b.min_gap(A, 3)), ('varilla-aro', v.min_gap(A, 3)), ('bola-meseta', b.min_gap(S['meseta'], 3)), ('varilla-meseta', v.min_gap(S['meseta'], 3)), ('cuerpo-aro', c.min_gap(A, 3))):
        if g < gm[k][0]: gm[k] = (g, tau)
print('minimos en el barrido fino (tubo 40..105 de 0,25 en 0,25):', {k: (round(g, 3), t) for k, (g, t) in gm.items()})
# cerrada: que toca primero al levantar la puerta
print('cerrada (psi 0): al levantar la puerta, distancias segun el angulo')
A = aro(0.0)
for ang in (0, 0.5, 1.0, 1.5, 1.8, 1.9, 2.0, 2.2, 2.5):
    b = gira_puerta(BOLA_D, 1, ang); v = gira_puerta(VARILLA_D, 1, ang)
    print('   %.1f grados: bola-aro %.3f (vol %.4f)   varilla-aro %.3f (vol %.4f)' % (ang, b.min_gap(A, 2), vol(b, A), v.min_gap(A, 2), vol(v, A)))
g, cj = localiza(gira_puerta(VARILLA_D, 1, 0.0), A); print('   punto de la varilla mas cercano al aro (puerta a 0): distancia %.3f en la caja %s' % (g, cj))
# con el aro apoyado en el ala (0,4 mm mas abajo que en el modelo)
A2 = aro(0.0).translate([0, 0, -0.4])
print('aro apoyado en el ala (0,4 mas abajo): canto de los cuernos a z = %.3f; ecuador de la bola %.3f por debajo (cerrada/abierta) y %.3f (a 45 grados)' % (z_cuerno1 - 0.4, z_cuerno1 - 0.4 - (d['eje_z'] - 8 * math.cos(math.radians(45))), z_cuerno1 - 0.4 - (d['eje_z'] - 8)))
for ang in (0, 1.0, 1.5, 2.0, 2.2, 2.5, 3.0):
    b = gira_puerta(BOLA_D, 1, ang); v = gira_puerta(VARILLA_D, 1, ang)
    print('   %.1f grados: bola-aro %.3f (vol %.4f)   varilla-aro %.3f (vol %.4f)' % (ang, b.min_gap(A2, 2), vol(b, A2), v.min_gap(A2, 2), vol(v, A2)))
# centro de gravedad de la puerta abierta: hacia donde cae
m = puerta(1, 90.0).to_mesh()
tm = trimesh.Trimesh(vertices=np.array(m.vert_properties)[:, :3], faces=np.array(m.tri_verts))
print('puerta derecha a 90 grados: centro de gravedad x = %.3f (el eje esta en %.1f), z = %.2f; volumen %.0f mm3 -> cae hacia %s' % (tm.center_mass[0], d['eje_x'], tm.center_mass[2], tm.volume, 'DENTRO (a cerrar)' if tm.center_mass[0] < d['eje_x'] else 'FUERA'))
for ang in (82.33, 87.15, 93.0, 95.6):
    m = puerta(1, ang).to_mesh(); tm = trimesh.Trimesh(vertices=np.array(m.vert_properties)[:, :3], faces=np.array(m.tri_verts))
    print('   a %.2f grados: centro de gravedad x - eje = %+.3f mm' % (ang, tm.center_mass[0] - d['eje_x']))
