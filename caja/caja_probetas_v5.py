# Eventually, caja v5: escribe los .3mf directamente desde el programa (sin Fusion), ya orientados como se imprimen.
#   python3 caja_probetas_v5.py            Deja la caja entera, bandeja a bandeja, en imprimir-v5/, y las probetas en probetas-v5/
#                                          y, las mismas, numeradas en el orden de imprimir, en pruebas-v5/.
#   Las mallas son cerradas (un solo cuerpo estanco por pieza).
import os
import numpy as np, trimesh
import caja_piezas_v5 as C

AQUI = os.path.dirname(os.path.abspath(__file__))
def a_la_cama(m, boca_abajo=False, dx=0.0, dy=0.0):
    """La pieza apoyada en Z = 0 como se imprime; boca_abajo la voltea (media vuelta alrededor del eje X); 'lado' la tumba sobre su costado derecho."""
    if boca_abajo == 'lado': m = m.rotate([0, 90, 0])
    elif boca_abajo: m = m.rotate([180, 0, 0])
    b = m.bounding_box()
    return m.translate([dx - (b[0] + b[3]) / 2, dy - (b[1] + b[4]) / 2, -b[2]])
def malla(m, nombre):
    """La malla de una pieza, limpia: sin triangulos de area cero y con cada arista compartida por dos caras exactamente, tambien despues de fundir
    los vertices que coinciden (que es lo que hace un laminador al abrirla). Si no sale asi, se para."""
    me = m.simplify(1e-4).to_mesh()
    t = trimesh.Trimesh(np.asarray(me.vert_properties)[:, :3].astype(np.float32).astype(np.float64), np.asarray(me.tri_verts), process=False)
    t.merge_vertices(digits_vertex=5)
    t.update_faces(t.nondegenerate_faces(height=1e-9)); t.remove_unreferenced_vertices()
    e = t.edges_sorted; u, c = np.unique(e, axis=0, return_counts=True)
    assert t.is_watertight and (c == 2).all() and not (t.area_faces < 1e-9).any(), (nombre, int((c != 2).sum()))
    assert abs(t.volume - m.volume()) < 1e-3 * m.volume(), nombre
    t.metadata['name'] = nombre
    return t

# Las probetas, bandeja a bandeja: (pieza, como va, x, y). 'como va': False = tal cual, True = boca abajo, 'lado' = tumbada sobre su costado derecho.
B = {
    'caja-probeta-puertas-bandeja-A': [('marco', False, -45, 0), ('puerta_derecha', True, 57, 42), ('puerta_izquierda', True, 57, -42), ('pasador_derecho', False, 88, 0),
                                       ('pasador_izquierdo', False, 96, 0), ('probeta_teton', True, 108, 60)],          # el teton con pomo, con el pomo en la cama
    'caja-probeta-puertas-bandeja-B': [('meseta', False, -60, 60), ('aro_puertas', False, 60, 55), ('probeta_anillo', True, -25, -62)],
    'caja-probeta-ascensor-soporte-y-pestillos': [('soporte', 'lado', 0, 0), ('pestillo_derecho', False, 68, 0), ('pestillo_izquierdo', False, 83, 0)],
    'caja-probeta-ascensor-base': [('base', False, 0, 0)], 'caja-probeta-ascensor-tubo': [('tubo', False, 0, 0)], 'caja-probeta-ascensor-plataforma': [('plataforma', False, 0, 0)],
    'caja-probeta-planetario-plato': [('plato', False, 0, 0)], 'caja-probeta-planetario-rueda-central': [('rueda_central', True, 0, 0)], 'caja-probeta-planetario-bisel': [('bisel', True, 0, 0)],
    'caja-probeta-planetario-satelites': [('satelite_%d' % (k + 1), False, -26 + 26 * (k % 3), -13 + 26 * (k // 3)) for k in range(6)] + [('teton', False, 52, 0)],
}
# Las mismas bandejas, en el orden en que conviene imprimirlas para ir probando (pruebas-v5/). La guia esta en pruebas-v5/GUIA.md.
ORDEN = [('01-puertas-bandeja-A', 'caja-probeta-puertas-bandeja-A'), ('02-puertas-bandeja-B', 'caja-probeta-puertas-bandeja-B'),
         ('03-ascensor-plataforma', 'caja-probeta-ascensor-plataforma'), ('04-ascensor-soporte-y-pestillos', 'caja-probeta-ascensor-soporte-y-pestillos'),
         ('05-ascensor-base', 'caja-probeta-ascensor-base'), ('06-ascensor-tubo', 'caja-probeta-ascensor-tubo'),
         ('07-planetario-plato', 'caja-probeta-planetario-plato'), ('08-planetario-satelites-y-teton', 'caja-probeta-planetario-satelites'),
         ('09-planetario-rueda-central', 'caja-probeta-planetario-rueda-central'), ('10-planetario-bisel', 'caja-probeta-planetario-bisel')]
assert sorted(b for a, b in ORDEN) == sorted(B)

if __name__ == '__main__':
    p, d, d2, P = C.piezas(); S = {n: C.solido(q.ops) for n, q in P.items()}
    # La caja entera, bandeja a bandeja (imprimir-v5/). Las piezas de probeta (anillo y teton con pomo) no entran.
    azul = [n for n in P if n.startswith('satelite_') and P[n].color == 'azul']; blancos = [n for n in P if n.startswith('satelite_') and P[n].color != 'azul']
    assert len(azul) == 1 and len(blancos) == 5
    I = {
        'caja-01-base': [('base', False, 0, 0)],
        'caja-02-tubo': [('tubo', False, 0, 0)],
        'caja-03-cuerpo': [('cuerpo', True, 0, 0)],
        'caja-04-funda-y-frase': [('funda', True, 0, 0), ('frase', 'con:funda', 0, 0)],
        'caja-05-plataforma': [('plataforma', False, 0, 0)],
        'caja-06-bisel': [('bisel', True, 0, 0)],
        'caja-07-plato': [('plato', False, 0, 0)],
        'caja-08-marco-y-piezas-pequenas': [('marco', False, -45, 0)] + [(n, False, 48 + 26 * (k % 2), -52 + 26 * (k // 2)) for k, n in enumerate(blancos)] + [('teton', False, 74, 0), ('pasador_derecho', False, 96, 0),
                                            ('pasador_izquierdo', False, 104, 0), ('pestillo_derecho', 'gira90', 48, 62), ('pestillo_izquierdo', 'gira90', 62, 62)],
        'caja-09-rueda-central-y-puertas': [('rueda_central', True, -48, 0), ('puerta_derecha', True, 62, 42), ('puerta_izquierda', True, 62, -42)],
        'caja-10-meseta-y-aro': [('meseta', False, -62, 0), ('aro_puertas', False, 62, 0)],
        'caja-11-satelite-azul': [(azul[0], False, 0, 0)],
        'caja-12-soporte': [('soporte', 'lado', 0, 0)],
    }
    todas = set(n for b_ in I.values() for n, *_ in b_)
    assert todas == set(n for n in P if P[n].mueve != 'probeta' and n != 'reloj_de_pega'), sorted(set(n for n in P if P[n].mueve != 'probeta' and n != 'reloj_de_pega') ^ todas)
    sal = os.path.join(AQUI, 'imprimir-v5'); os.makedirs(sal, exist_ok=True)
    for fichero, piezas in I.items():
        esc = trimesh.Scene(); puestas = {}
        for n, ba, dx, dy in piezas:
            if isinstance(ba, str) and ba.startswith('con:'):                 # misma colocacion que otra pieza: van una dentro de otra
                m0 = S[ba[4:]].rotate([180, 0, 0]); b0 = m0.bounding_box()
                m = S[n].rotate([180, 0, 0]).translate([-(b0[0] + b0[3]) / 2, -(b0[1] + b0[4]) / 2, -b0[2]])
            elif ba == 'gira90': m = a_la_cama(S[n].rotate([0, 0, 90]), False, dx, dy)
            else: m = a_la_cama(S[n], ba, dx, dy)
            puestas[n] = m
            esc.add_geometry(malla(m, n), node_name=n, geom_name=n)
        b = esc.bounds
        assert b[0][0] > -124 and b[1][0] < 124 and b[0][1] > -124 and b[1][1] < 124 and abs(b[0][2]) < 1e-6 and b[1][2] < 250, (fichero, b)
        ns = list(puestas)
        for i_, a_ in enumerate(ns):                                          # en la bandeja, las piezas no se tocan (menos la frase, que va dentro de la funda)
            for b_ in ns[i_ + 1:]:
                if 'frase' in (a_, b_): continue
                assert puestas[a_].min_gap(puestas[b_], 3.0) >= 3.0, (fichero, a_, b_)
        esc.export(os.path.join(sal, fichero + '.3mf'))
        print('%-44s %d piezas  %.0f x %.0f x %.0f mm' % (fichero + '.3mf', len(piezas), b[1][0] - b[0][0], b[1][1] - b[0][1], b[1][2] - b[0][2]))
    sal = os.path.join(AQUI, 'probetas-v5')
    for fichero, piezas in B.items():
        esc = trimesh.Scene()
        for n, ba, dx, dy in piezas:
            esc.add_geometry(malla(a_la_cama(S[n], ba, dx, dy), n), node_name=n, geom_name=n)
        b = esc.bounds
        assert b[0][0] > -124 and b[1][0] < 124 and b[0][1] > -124 and b[1][1] < 124 and abs(b[0][2]) < 1e-6, fichero
        esc.export(os.path.join(sal, fichero + '.3mf'))
        num = [a for a, b_ in ORDEN if b_ == fichero][0]
        os.makedirs(os.path.join(AQUI, 'pruebas-v5'), exist_ok=True); esc.export(os.path.join(AQUI, 'pruebas-v5', num + '.3mf'))
        print('%-44s %d piezas  %.0f x %.0f x %.0f mm   -> pruebas-v5/%s.3mf' % (fichero + '.3mf', len(piezas), b[1][0] - b[0][0], b[1][1] - b[0][1], b[1][2] - b[0][2], num))
