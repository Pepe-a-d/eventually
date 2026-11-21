# Comun a todos los programas de la revision del ascensor y del planetario
import sys, os, math, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import numpy as np
import manifold3d as mf
import caja_piezas_v5 as CP, caja_diseno_v5 as D
p, d, d2, P = CP.piezas()
S = {n: CP.solido(q.ops) for n, q in P.items()}
ROT = CP.ROT
def puesta(n, tau):
    return CP.mover(S[n], n, P[n].mueve, p, d, tau)
def vol(a, b):
    return (a ^ b).volume()
def gap(a, b, r=2.0):
    return a.min_gap(b, r)
def bb(m):
    return [round(v, 3) for v in m.bounding_box()]
def donde(a, b):
    """caja del volumen comun"""
    i = a ^ b
    return bb(i) if i.volume() > 0 else None
def pol(r, a):
    return (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
