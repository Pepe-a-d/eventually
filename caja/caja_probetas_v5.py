# Eventually, caja v5: escribe los .3mf de las probetas directamente desde el programa (sin Fusion), ya orientados.
#   python3 caja_probetas_v5.py            Los deja en probetas-v5/. Las mallas son cerradas (un solo cuerpo estanco por pieza).
import os
import numpy as np, trimesh
import caja_piezas_v5 as C

AQUI = os.path.dirname(os.path.abspath(__file__))
def a_la_cama(m, boca_abajo=False, dx=0.0, dy=0.0):
    """La pieza apoyada en Z = 0 como se imprime; boca_abajo la voltea (media vuelta alrededor del eje X)."""
    if boca_abajo: m = m.rotate([180, 0, 0])
    b = m.bounding_box()
    return m.translate([dx - (b[0] + b[3]) / 2, dy - (b[1] + b[4]) / 2, -b[2]])
def malla(m, nombre):
    me = m.to_mesh()
    t = trimesh.Trimesh(np.asarray(me.vert_properties)[:, :3], np.asarray(me.tri_verts), process=False); t.metadata['name'] = nombre
    assert t.is_watertight, nombre
    return t

if __name__ == '__main__':
    p, d, d2, P = C.piezas(); S = {n: C.solido(q.ops) for n, q in P.items()}
    B = {
        'caja-probeta-puertas-bandeja-A': [('marco', False, -45, 0), ('puerta_derecha', True, 57, 42), ('puerta_izquierda', True, 57, -42), ('pasador_derecho', False, 88, 0),
                                           ('pasador_izquierdo', False, 96, 0), ('probeta_teton', True, 108, 60)],          # el teton con pomo, con el pomo en la cama
        'caja-probeta-puertas-bandeja-B': [('meseta', False, -60, 60), ('aro_puertas', False, 60, 55), ('probeta_anillo', True, -25, -62)],
        'caja-probeta-ascensor-soporte-y-pestillos': [('soporte', False, 0, 0), ('pestillo_derecho', False, 40, 0), ('pestillo_izquierdo', False, 55, 0)],
        'caja-probeta-ascensor-base': [('base', False, 0, 0)], 'caja-probeta-ascensor-tubo': [('tubo', False, 0, 0)], 'caja-probeta-ascensor-plataforma': [('plataforma', False, 0, 0)],
        'caja-probeta-planetario-plato': [('plato', False, 0, 0)], 'caja-probeta-planetario-rueda-central': [('rueda_central', True, 0, 0)], 'caja-probeta-planetario-bisel': [('bisel', True, 0, 0)],
        'caja-probeta-planetario-satelites': [('satelite_%d' % (k + 1), False, -26 + 26 * (k % 3), -13 + 26 * (k // 3)) for k in range(6)] + [('teton', False, 52, 0)],
    }
    sal = os.path.join(AQUI, 'probetas-v5')
    for fichero, piezas in B.items():
        esc = trimesh.Scene()
        for n, ba, dx, dy in piezas:
            esc.add_geometry(malla(a_la_cama(S[n], ba, dx, dy), n), node_name=n, geom_name=n)
        b = esc.bounds
        assert b[0][0] > -124 and b[1][0] < 124 and b[0][1] > -124 and b[1][1] < 124 and abs(b[0][2]) < 1e-6, fichero
        esc.export(os.path.join(sal, fichero + '.3mf'))
        print('%-44s %d piezas  %.0f x %.0f x %.0f mm' % (fichero + '.3mf', len(piezas), b[1][0] - b[0][0], b[1][1] - b[0][1], b[1][2] - b[0][2]))
