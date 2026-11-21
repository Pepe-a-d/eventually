# Entorno comun de los programas de la revision de montaje.
import sys, os, math, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import numpy as np
import manifold3d as mf
import caja_piezas_v5 as CP, caja_diseno_v5 as D
p, d, d2, P = CP.piezas()
S = {n: CP.solido(q.ops) for n, q in P.items()}
G = p['giro_tubo']
CAJA = [n for n in P if P[n].mueve not in ('probeta',) and n != 'frase']          # las 25 piezas + reloj de pega (funda incluida)
DENTRO = [n for n in CAJA if n != 'funda']
def puesta(n, tau=0.0):
    return CP.mover(S[n], n, P[n].mueve, p, d, tau)
def vol(a, b):
    return (a ^ b).volume()
def bb_solapan(a, b, e=0.0):
    A = a.bounding_box(); B = b.bounding_box()
    return all(A[i] - e < B[i + 3] and B[i] - e < A[i + 3] for i in range(3))
def choque(a, otros, umbral=0.05):
    """otros: dict nombre -> solido. Devuelve lista (nombre, volumen) de los que pisa mas que el umbral."""
    out = []
    for n, b in otros.items():
        if not bb_solapan(a, b): continue
        v = vol(a, b)
        if v > umbral: out.append((n, round(v, 3)))
    return out
def puerta(sx, ang, dz=0.0):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    return S[n].translate([-sx * d['eje_x'], 0, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z'] + dz])
def volcada(s):
    """Cara de arriba hacia abajo: giro de 180 alrededor del eje X que pasa por el centro en Z de su caja."""
    b = s.bounding_box(); zc = (b[2] + b[5]) / 2
    return s.translate([0, 0, -zc]).rotate([180, 0, 0]).translate([0, 0, zc])
