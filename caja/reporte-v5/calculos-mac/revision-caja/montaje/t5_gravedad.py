# Boca abajo y de lado. Para cada pareja de piezas (a, b) se calcula cuanto puede desplazarse a respecto a b en la direccion
# de la gravedad antes de pisarla (> 0,05 mm3): T[a][b]. Con eso, lo que se desplaza cada pieza cuando todo cae a la vez es el
# camino mas corto desde la pieza que se sujeta con la mano (o la mesa): dz[a] = min sobre b de (dz[b] + T[a][b]).
# Solo traslaciones. El giro de las puertas (que cuelgan de su bisagra) se mira aparte en t6_puertas.py.
# Uso: python t5_gravedad.py  ->  escribe t5_gravedad.txt
from comun import *
import sys, json
def recorrido(a, b, g, lim, fino, grueso=0.5):
    """Cuanto se mueve a (solido) en la direccion g antes de pisar a b. None si no la pisa en 'lim' mm."""
    A = a.bounding_box(); B = b.bounding_box()
    # caja de a barrida
    lo = [min(A[i], A[i] + g[i] * lim) for i in range(3)]; hi = [max(A[i + 3], A[i + 3] + g[i] * lim) for i in range(3)]
    if not all(lo[i] < B[i + 3] and B[i] < hi[i] for i in range(3)): return None
    v0 = vol(a, b)                         # lo que ya comparten en su sitio (artefactos de malla o apoyos): se descuenta
    n = int(round(lim / grueso)); e_c = None
    for i in range(1, n + 1):
        e = grueso * i
        if vol(a.translate([g[0] * e, g[1] * e, g[2] * e]), b) > v0 + 0.05: e_c = e; break
    if e_c is None: return None
    m = int(round(grueso / fino))
    for j in range(1, m + 1):
        e = e_c - grueso + fino * j
        if vol(a.translate([g[0] * e, g[1] * e, g[2] * e]), b) > v0 + 0.05: return round(e - fino, 4)
    return round(e_c - fino, 4)
def tabla(M, g, lim, fino):
    T = {a: {} for a in M}
    ns = list(M)
    for a in ns:
        for b in ns:
            if a == b: continue
            r = recorrido(M[a], M[b], g, lim, fino)
            if r is not None: T[a][b] = r
    return T
def asienta(T, fijas, lim):
    dz = {a: (0.0 if a in fijas else 1e9) for a in T}; por = {a: None for a in T}
    cambio = True
    while cambio:
        cambio = False
        for a in T:
            if a in fijas: continue
            for b, t in T[a].items():
                if dz[b] + t < dz[a] - 1e-9: dz[a] = dz[b] + t; por[a] = b; cambio = True
    return dz, por
def cadena(a, por):
    out = []
    while por.get(a): a = por[a]; out.append(a)
    return ' <- '.join(out)
def informe(titulo, M, g, fijas, lim, fino, aviso, T=None):
    T = T or tabla(M, g, lim, fino)
    dz, por = asienta(T, fijas, lim)
    print(titulo)
    for a in M:
        if a in fijas: continue
        directo = min(T[a].values()) if T[a] else None
        quien = [b for b, t in T[a].items() if t == directo] if T[a] else []
        if dz[a] > 1e8:
            print('   %-18s NO LA PARA NADA en %.0f mm (solo, sin contar a las demas: %s)' % (a, lim, 'nada' if directo is None else '%.2f mm contra %s' % (directo, ', '.join(quien))))
        else:
            print('   %-18s %s%5.2f mm en total; ella sola %.2f mm hasta tocar %s; cadena: %s' % (a, '!! ' if dz[a] > aviso + 1e-9 else '   ', dz[a], directo, ', '.join(quien), cadena(a, por)))
    return T, dz, por
if __name__ == '__main__':
    t0 = time.time()
    mesa = mf.Manifold.cube([400, 400, 5]).translate([-200, -200, 0.0])          # una mesa en Z = 0: la caja boca abajo apoyada en su tapa
    for tau in (0.0, 70.0, 100.0, 200.0, 345.0):
        s_, psi, ang, h = D.movimiento(p, d, tau)
        M = {n: puesta(n, tau) for n in DENTRO}
        print('==== BOCA ABAJO, tubo a %.0f grados (teton %.1f mm, aro %.1f, puertas %.1f grados, plataforma %.1f mm) ====' % (tau, s_, psi, ang, h))
        T = tabla(M, (0, 0, 1), 10.0, 0.1)
        informe(' -- cogida por el cuerpo (el cuerpo no se mueve)', M, (0, 0, 1), {'cuerpo'}, 10.0, 0.1, 1.5, T)
        informe(' -- cogida por la base (la base no se mueve)', M, (0, 0, 1), {'base'}, 10.0, 0.1, 1.5, T)
        if tau == 0.0:
            M2 = dict(M); M2['mesa'] = mesa
            informe(' -- apoyada boca abajo en una mesa (plano en Z = 0)', M2, (0, 0, 1), {'mesa'}, 10.0, 0.1, 1.5)
            M3 = dict(M); M3['funda'] = S['funda']
            informe(' -- con la funda puesta, cogida por la funda', M3, (0, 0, 1), {'funda'}, 10.0, 0.1, 1.5)
            Tf = tabla(M3, (0, 0, 1), 140.0, 0.1)
            informe(' -- con la funda puesta, cogida por el cuerpo o por la base: la funda (hasta 140 mm)', {'funda': S['funda'], 'cuerpo': S['cuerpo'], 'base': S['base']}, (0, 0, 1), {'cuerpo', 'base'}, 140.0, 0.1, 1.5)
        print('   (%.0f s)' % (time.time() - t0)); sys.stdout.flush()
    for tau in (0.0, 345.0):
        M = {n: puesta(n, tau) for n in DENTRO}
        for nombre, g in (('+X (hacia la derecha)', (1, 0, 0)), ('-X', (-1, 0, 0)), ('+Y (hacia atras)', (0, 1, 0)), ('-Y (hacia el frente)', (0, -1, 0))):
            informe('==== DE LADO, gravedad hacia %s, tubo a %.0f grados; el cuerpo no se mueve ====' % (nombre, tau), M, g, {'cuerpo'}, 6.0, 0.05, 0.5)
            print('   (%.0f s)' % (time.time() - t0)); sys.stdout.flush()
