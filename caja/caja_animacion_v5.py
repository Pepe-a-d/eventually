# Eventually, caja v5: saca las mallas de cada pieza (una vez, con la caja cerrada) y la tabla de movimiento,
# para la animacion que dibuja render-v5/anim.mjs.      python3 caja_animacion_v5.py <carpeta>
import json, os, sys
import numpy as np
import caja_piezas_v5 as C

# colores para las vistas en corte y de mecanismo (los mismos de los cortes del reporte)
COL = {'base': '#c9ccd1', 'cuerpo': '#e4e1d8', 'tubo': '#b9d4bd', 'plato': '#8fbf98', 'plataforma': '#e7c1bb', 'marco': '#d9cfa8', 'meseta': '#f1e7b6', 'aro_puertas': '#f0b46a',
       'teton': '#c7641a', 'rueda_central': '#b7b3d9', 'bisel': '#9db7dd', 'puerta_derecha': '#fbfaf6', 'puerta_izquierda': '#fbfaf6', 'pasador_derecho': '#555b66',
       'pasador_izquierdo': '#555b66', 'soporte': '#9aa0a8', 'reloj_de_pega': '#c5cad1', 'funda': '#dcd9d1', 'frase': '#1f3fa8'}
REAL = {'blanco': '#f4f2ec', 'azul': '#1f3fa8', 'gris': '#8d949c', 'marmol': '#dcd9d1'}

if __name__ == '__main__':
    sal = sys.argv[1]
    p, d, d2, P = C.piezas(); D = C.D
    out = []
    for n, q in P.items():
        if q.mueve == 'probeta': continue
        me = C.solido(q.ops).to_mesh()
        v = np.asarray(me.vert_properties)[:, :3]; t = np.asarray(me.tri_verts)
        out.append({'n': n, 'mueve': q.mueve, 'real': REAL[q.color], 'esquema': COL.get(n, '#2a4fb5' if n == 'satelite_1' else '#eef0f3'),
                    'v': np.round(v, 3).ravel().tolist(), 't': t.ravel().tolist()})
    mov = [[round(x, 4) for x in D.movimiento(p, d, float(t_))] for t_ in range(int(p['giro_tubo']) + 1)]
    cte = {'ROT': C.ROT, 'giro_tubo': p['giro_tubo'], 'relacion': d['relacion'], 'eje_x': d['eje_x'], 'eje_z': d['eje_z'], 'r_ejes': d['r_ejes'], 'z_central': p['z_central'],
           'z_satelite': p['z_satelite'], 'aro_sentido': p['aro_sentido'], 'bola_y': d['bola_y'], 'z_base': d['z_base']}
    json.dump({'piezas': out, 'mov': mov, 'cte': cte}, open(os.path.join(sal, 'mallas.json'), 'w'))
    print(len(out), 'piezas;', sum(len(o['t']) for o in out) // 3, 'triangulos')
