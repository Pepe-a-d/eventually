import sys, os, math
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import numpy as np
import manifold3d as mf
import caja_piezas_v5 as CP, caja_diseno_v5 as D
p, d, d2, P = CP.piezas()
S = {n: CP.solido(q.ops) for n, q in P.items()}
G = p['giro_tubo']
def puesta(n, tau): return CP.mover(S[n], n, P[n].mueve, p, d, tau)
def puerta(sx, ang, h=0.0):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    return S[n].translate([-sx * d['eje_x'], 0, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z'] + h])
def vol(a, b): return (a ^ b).volume()
def bb(m): return m.bounding_box()
def caja(x0, y0, z0, x1, y1, z1): return mf.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
def cil(c, r, z0, z1, n=96): return mf.Manifold.cylinder(z1 - z0, r, r, n).translate([c[0], c[1], z0])
CAJA = [n for n in P if P[n].mueve not in ('funda', 'probeta')]
