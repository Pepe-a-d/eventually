"""Sesion del Mac: comprobacion propia. Pedestal arriba y holgura de los tetones en la rampa."""
import sys, os
sys.path.insert(0, os.environ.get('CAJA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
import manifold3d as mf, numpy as np
import caja_piezas_v5 as CP, caja_diseno_v5 as D
p, d, d2, P = CP.piezas(); S = {n: CP.solido(q.ops) for n, q in P.items()}
G = p['giro_tubo']
def puesta(n, tau): return CP.mover(S[n], n, P[n].mueve, p, d, tau)
# 1. arriba del todo: que queda abierto alrededor del pedestal, a ras (z = -0,1) y mas abajo
fijo = puesta('plataforma', G) + S['meseta'] + S['marco'] + puesta('puerta_derecha', G) + puesta('puerta_izquierda', G) + S['rueda_central']
print('1. Reloj arriba, puertas de pie. Hueco que queda abierto dentro del circulo de la meseta (radio %.1f), cortando a distintas alturas:' % d['cuello_r'])
for z in (-0.1, -2.5, -4.9, -5.1, -7.0):
    sec = fijo.slice(z)
    disco = mf.CrossSection.circle(d['cuello_r'] - 2.0, 180)
    libre = disco - sec
    trozos = sorted(([round(float(v), 2) for v in np.r_[np.min(q, 0), np.max(q, 0)]] for q in libre.to_polygons()), key=lambda b: -(b[2] - b[0]) * (b[3] - b[1]))[:4]
    print('   z = %5.1f: %.1f mm2 abiertos. Mayores (x0, y0, x1, y1): %s' % (z, libre.area(), trozos))
hx, hy = d['hueco_x'] / 2, d['hueco_y'] / 2
print('   pedestal: de x = +-%.2f, y = +-%.2f; el rebaje de las puertas en la meseta llega a y = +-%.2f y x = +-%.2f' % (hx - p['pedestal_holgura'], hy - p['pedestal_holgura'], d['puerta_y'] / 2 + 0.3, d['eje_x']))
# 2. holgura vertical de la plataforma en la rampa: cuanto sube y cuanto baja antes de pisar el tubo
print('2. Plataforma en la rampa: cuanto se deja subir y bajar (en vertical) antes de pisar el tubo mas de 0,02 mm3')
for tau in (60.0, 120.0, 200.0, 300.0, 340.0):
    pl, tu = puesta('plataforma', tau), puesta('tubo', tau)
    res = []
    for sg in (1, -1):
        r = 9.9
        for i in range(1, 80):
            if (pl.translate([0, 0, sg * 0.01 * i]) ^ tu).volume() > 0.02: r = 0.01 * (i - 1); break
        res.append(r)
    print('   tubo a %3.0f: sube %.2f mm, baja %.2f mm; distancia minima plataforma-tubo %.3f mm' % (tau, res[0], res[1], pl.min_gap(tu, 2.0)))
k_h = d['recorrido'] / (p['giro_arriba'] - p['giro_sube'])
print('   la ranura tiene %.2f mm de holgura en vertical por lado, pero va inclinada %.1f grados: en perpendicular quedan %.3f mm' % (p['holg_desliza'] + 0.0, d['rampa_pendiente'], p['holg_desliza'] * np.cos(np.radians(d['rampa_pendiente']))))
