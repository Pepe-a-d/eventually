# Eventually, caja v5: saca las mallas de la caja en varias posiciones para hacer dibujos.
# python3 caja_render_v5.py <carpeta>      Escribe estado_N.json. Los dibuja render_caja.mjs (three.js en un navegador sin pantalla).
import json, os, sys
import numpy as np
import manifold3d as mf
import caja_piezas_v5 as C

COLORES = {'blanco': '#f4f2ec', 'azul': '#1f3fa8', 'gris': '#8d949c'}
TINTE = {'tubo': '#dfe9df', 'plato': '#dfe9df', 'bisel': '#ffffff', 'aro_puertas': '#f1dcc0', 'teton': '#d08a2a', 'plataforma': '#f0dedb', 'rueda_central': '#e9e7e0',
         'puerta_derecha': '#ffffff', 'puerta_izquierda': '#ffffff', 'pasador_derecho': '#b7bcc4', 'pasador_izquierdo': '#b7bcc4', 'marco': '#eceae2', 'meseta': '#f7f6f1'}

DESPIECE = {'base': 0, 'plataforma': 22, 'soporte': 22, 'reloj_de_pega': 22, 'tubo': 150, 'marco': 275, 'aro_puertas': 300, 'teton': 318, 'plato': 335, 'meseta': 365,
            'pasador_derecho': 380, 'pasador_izquierdo': 380, 'puerta_derecha': 398, 'puerta_izquierda': 398, 'rueda_central': 440, 'bisel': 470, 'cuerpo': 610}
COLORES['marmol'] = '#d9d6cf'

def estado(S, P, p, d, tau, corte=None, quita=(), despiece=False, solo=None):
    """corte = (nx, ny, nz, d0): se queda con el lado en que n.x >= d0."""
    out = []
    for n, q in P.items():
        if n in quita or (solo and n not in solo) or (q.mueve == 'probeta' and not (solo and n in solo)): continue
        m = C.mover(S[n], n, q.mueve, p, d, tau)
        if despiece:
            m = m.translate([0, 0, DESPIECE.get(n, 418 if n.startswith('satelite') else 0)])
        if corte is not None:
            m = m.trim_by_plane(list(corte[:3]), corte[3])
        if m.is_empty(): continue
        me = m.to_mesh()
        v = np.asarray(me.vert_properties)[:, :3]; t = np.asarray(me.tri_verts)
        out.append({'n': n, 'c': TINTE.get(n, COLORES[q.color]) if q.color == 'blanco' else COLORES[q.color], 'v': np.round(v, 3).ravel().tolist(), 't': t.ravel().tolist()})
    return out

if __name__ == '__main__':
    sal = sys.argv[1]
    p, d, d2, P = C.piezas(); S = {n: C.solido(q.ops) for n, q in P.items()}
    F = ('funda', 'frase')
    atras = (0, 1, 0, 0.0)                      # se quita la mitad de delante: se ve el corte desde el frente
    yb = d['bola_y']; man = (0, 1, 0, yb)       # corte por la manivela de la puerta derecha
    tapas = F + ('cuerpo', 'bisel', 'meseta', 'rueda_central', 'puerta_derecha', 'puerta_izquierda', 'plato', 'pasador_derecho', 'pasador_izquierdo') + tuple('satelite_%d' % i for i in range(1, 7))
    V = [('con-funda', 0, None, (), {}), ('cerrada', 0, None, F, {}), ('corte-cerrada', 0, atras, F, {}), ('corte-arriba', 345, atras, F, {}), ('despiece', 0, None, F, {'despiece': True}),
         ('aro-cerrado', 0, None, tapas, {}), ('aro-abierto', 345, None, tapas, {})]
    V += [('paso-%d' % (i + 1), t, None, F, {}) for i, t in enumerate((0, 45, 72, 100, 220, 345))]
    V += [('manivela-%d' % (i + 1), t, man, F + ('cuerpo', 'bisel', 'tubo', 'base', 'plataforma', 'soporte', 'reloj_de_pega'), {}) for i, t in enumerate((0, 72, 100))]
    V += [('probeta-puertas', 76, None, (), {'solo': ('marco', 'aro_puertas', 'meseta', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo', 'probeta_anillo', 'probeta_teton')})]
    for nombre, tau, corte, quita, kw in V:
        json.dump(estado(S, P, p, d, tau, corte, quita, **kw), open(os.path.join(sal, nombre + '.json'), 'w'))
        print(nombre)
