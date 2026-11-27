# Eventually, tutorial de la caja en la web: saca del modelo de la caja v5 lo que necesita la escena (caja5.js).
#   python3 mallas_v5.py <carpeta>      Escribe <carpeta>/piezas.json
# No pasa por Fusion: usa caja/caja_piezas_v5.py, que es el modelo.
# piezas.json lleva: las piezas en reposo (caja cerrada), como se mueve cada una ('mueve'), la tabla del movimiento
# (cuanto se han abierto las puertas y cuanto ha subido el reloj para cada giro del tubo) y las constantes que usa el movimiento.
import json, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'caja'))
import caja_piezas_v5 as C

def main(sal):
    os.makedirs(sal, exist_ok=True)
    p, d, d2, P = C.piezas()
    G = p['giro_tubo']
    piezas = []
    for n, q in P.items():
        if q.mueve == 'probeta': continue                      # el anillo y el teton con pomo solo existen para las probetas
        m = C.solido(q.ops).to_mesh()
        v = np.asarray(m.vert_properties)[:, :3]; t = np.asarray(m.tri_verts)
        piezas.append({'n': n, 'mueve': q.mueve, 'color': q.color, 'v': np.round(v, 3).ravel().tolist(), 't': t.ravel().tolist()})
    paso = 0.5
    mov = [[round(float(x), 4) for x in C.D.movimiento(p, d, min(G, i * paso))] for i in range(int(G / paso) + 1)]      # [s, psi, ang, h]
    cte = {'giro_tubo': G, 'paso': paso, 'rot': C.ROT, 'relacion': d['relacion'], 'aro_sentido': p['aro_sentido'], 'eje_x': d['eje_x'], 'eje_z': d['eje_z'],
           'r_ejes': d['r_ejes'], 'z_central': p['z_central'], 'z_satelite': p['z_satelite'], 'recorrido': d['recorrido'], 'pestillo_libre': C.PESTILLO_LIBRE,
           'alto': -min(min(q['v'][2::3]) for q in piezas if q['n'] == 'base')}
    json.dump({'cte': cte, 'mov': mov, 'piezas': piezas}, open(os.path.join(sal, 'piezas.json'), 'w'))
    print('%d piezas, %d posiciones del movimiento, alto de la caja %.1f mm' % (len(piezas), len(mov), cte['alto']))

if __name__ == '__main__':
    main(sys.argv[1])
