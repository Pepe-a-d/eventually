import sys, os, math
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import numpy as np
import caja_piezas_v5 as CP, caja_diseno_v5 as D
import manifold3d as mf
p, d, d2, P = CP.piezas()
S = {n: CP.solido(q.ops) for n, q in P.items()}
def mv(n, tau): return CP.mover(S[n], n, P[n].mueve, p, d, tau)
def puerta(sx, ang, dy=0.0):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    return S[n].translate([-sx * d['eje_x'], dy, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z']])
def aro(psi, dx=0.0, dy=0.0): return S['aro_puertas'].rotate([0, 0, p['aro_sentido'] * psi]).translate([dx, dy, 0])
def vol(a, b): return (a ^ b).volume()
def bb(m): return m.bounding_box()
def solapan(a, b, e=0.0):
    return all(a[i] - e < b[i + 3] and b[i] - e < a[i + 3] for i in range(3))
def centro_inter(a, b):
    i = a ^ b
    if i.volume() <= 0: return None
    return [round(v, 2) for v in i.bounding_box()]

def caja_m(b):
    return mf.Manifold.cube([b[3]-b[0], b[4]-b[1], b[5]-b[2]]).translate([b[0], b[1], b[2]])
def localiza(a, b, r=1.0, niv=14):
    """Donde esta el punto de 'a' mas cercano a 'b': parte la caja de 'a' en dos, se queda con la mitad mas cercana. Devuelve (gap, caja)."""
    g0 = a.min_gap(b, r)
    box_ = list(a.bounding_box())
    # recorta primero a la zona cercana a b
    bbx = b.bounding_box()
    box_ = [max(box_[i], bbx[i]-r) for i in range(3)] + [min(box_[i+3], bbx[i+3]+r) for i in range(3)]
    for _ in range(niv):
        ej = int(np.argmax([box_[i+3]-box_[i] for i in range(3)]))
        m = (box_[ej] + box_[ej+3]) / 2
        b1 = list(box_); b1[ej+3] = m; b2 = list(box_); b2[ej] = m
        cands = []
        for bx in (b1, b2):
            pa = a ^ caja_m(bx)
            if pa.is_empty(): cands.append((9e9, bx)); continue
            cands.append((pa.min_gap(b, r), bx))
        box_ = min(cands, key=lambda c: c[0])[1]
    return g0, [round(v, 2) for v in box_]

# la puerta derecha en trozos: cuerpo (losa, canto, labio), varilla (solo lo que asoma por debajo de la losa, sin la bola) y bola
_ops = P['puerta_derecha'].ops
CUERPO_D = CP.solido([_ops[0], _ops[1], _ops[2], _ops[5]])
BOLA_D = CP.solido([_ops[4]])
VARILLA_D = CP.solido([_ops[3]]) - CUERPO_D - BOLA_D - CP.solido([{'t': 'cil', 'a': _ops[5]['a'], 'b': _ops[5]['b'], 'r': _ops[5]['r'], 'op': '+'}])
VARILLA_D = VARILLA_D ^ mf.Manifold.cube([100, 100, 100]).translate([-50, -50, -105.0])      # solo por debajo de z = -5
def gira_puerta(m, sx, ang, dy=0.0):
    """m esta descrito como la puerta derecha cerrada; para sx=-1 se gira antes media vuelta en Z."""
    if sx < 0: m = m.rotate([0, 0, 180])
    return m.translate([-sx * d['eje_x'], dy, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z']])
def bisec(f, lo, hi, n=16):
    """f(lo) falso, f(hi) cierto: devuelve el primer valor en que f es cierto."""
    for _ in range(n):
        m = (lo + hi) / 2
        if f(m): hi = m
        else: lo = m
    return hi
def tau_de_psi(psi):
    return bisec(lambda t: D.movimiento(p, d, t)[1] >= psi, 0.0, p['giro_puertas_fin'], 40)
