# 7 (bis). Distancia LATERAL entre dientes satelite-bisel y satelite-central (quitando las caras de arriba, que estan en el mismo plano
# que el techo del bisel: satelite hasta z = -3.4 y techo del bisel desde z = -3.4, distancia 0 por construccion)
from comun import *
def rebanada(z0, z1):
    return mf.Manifold.cube([400, 400, z1 - z0]).translate([-200, -200, z0])
R_s = rebanada(-8.0, -5.0); R_b = rebanada(-9.39, -3.45)
sats = ['satelite_%d' % i for i in range(1, 7)]
ce = S['rueda_central'] ^ R_b; bi0 = S['bisel'] ^ R_b
print('satelite arriba z = %.3f ; techo del bisel abajo z = %.3f ; placa de la rueda central abajo z = %.3f ; plato arriba z = %.3f' % (S['satelite_1'].bounding_box()[5], d['z_engr1'], -p['esqueleto_grueso'], d['z_plato1']))
filas = []
for i in range(241):
    tau = 0.05 * i
    bi = bi0.rotate([0, 0, ROT * tau / d['relacion']])
    for s in sats[:2]:
        m = puesta(s, tau) ^ R_s
        filas.append((tau, int(s[-1]), vol(m, ce), gap(m, ce, 1.0), vol(m, bi), gap(m, bi, 1.0)))
a = np.array(filas)
for k in (1, 2):
    s = a[a[:, 1] == k]
    print('  satelite %d (dientes, sin caras): con central vol max %.5f, dist min %.4f (tau %.2f) max %.4f | con bisel vol max %.5f, dist min %.4f (tau %.2f) max %.4f' % (
        k, s[:, 2].max(), s[:, 3].min(), s[s[:, 3].argmin(), 0], s[:, 3].max(), s[:, 4].max(), s[:, 5].min(), s[s[:, 5].argmin(), 0], s[:, 5].max()))
s = a[a[:, 1] == 1]
print('  perfil de la distancia lateral satelite 1 - bisel a lo largo de un paso de diente (cada 0.25 grados de tubo):')
print('   ', ' '.join('%.3f' % v for v in s[::5, 5][:40]))
print('  idem satelite 1 - central:')
print('   ', ' '.join('%.3f' % v for v in s[::5, 3][:40]))
# holguras de fondo: punta de satelite a fondo de bisel y a fondo de central; punta de central y de bisel a fondo de satelite
m_ = p['modulo']
print('  radial: punta sat %.3f; fondo sat %.3f; punta central %.3f; fondo central %.3f; punta bisel %.3f; fondo bisel %.3f; ejes a %.3f' % (d['r_satelite'] + m_, d['r_satelite'] - 1.25 * m_, d['central_punta'], d['central_fondo'], d['bisel_punta'], d['bisel_fondo'], d['r_ejes']))
print('  holgura de fondo: sat-punta/bisel-fondo %.3f; bisel-punta/sat-fondo %.3f; sat-punta/central-fondo %.3f; central-punta/sat-fondo %.3f' % (
    d['bisel_fondo'] - (d['r_ejes'] + d['r_satelite'] + m_), d["bisel_punta"] - (d["r_ejes"] + d["r_satelite"] - 1.25 * m_), (d['r_ejes'] - d['r_satelite'] - m_) - d['central_fondo'], (d['r_ejes'] - (d['r_satelite'] - 1.25 * m_)) - d['central_punta']))
# interferencia teorica de evolvente
al = math.radians(20); a_c = d['r_ejes']
rb_s = d['r_central'] * math.cos(al); rb_r = d['r_bisel'] * math.cos(al); rb_p = d['r_satelite'] * math.cos(al)
print('  teoria: radio de base del satelite %.3f (su fondo esta a %.3f: por debajo de la base el flanco del modelo es radial)' % (rb_p, d['r_satelite'] - 1.25 * m_))
print('  teoria: la punta de la central no deberia pasar de %.3f para no tocar por debajo de la base del satelite; esta a %.3f' % (math.hypot(rb_s, a_c * math.sin(al)), d['central_punta']))
print('  teoria: la punta del bisel no deberia bajar de %.3f; esta a %.3f' % (math.hypot(rb_r, a_c * math.sin(al)), d['bisel_punta']))
