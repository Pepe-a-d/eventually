"""Sesion del Mac, 21-nov-2026. Solo necesita numpy.

Cuanto ocuparia una tapa de "gajos al ras": n piezas gruesas, todas en un
mismo plano, que cerradas forman un disco sin agujero y se apartan deslizando
de lado. Es una cuenta en plano, sin dibujar en CAD y sin pieza impresa.

Cada gajo es un sector con la punta en el centro. Para que los cantos de dos
vecinos sigan tocandose mientras se abren, cada gajo tiene que deslizar en
linea recta, perpendicular a su propio eje. El hueco abierto es un poligono
de n lados; r es el radio del circulo que cabe dentro.
"""
import numpy as np

R_HUECO = 37.5      # mm, hueco libre de 75 (estimado en el brief)
HOLGURA = 0.3       # mm, entre el gajo y la pared
PARED = 1.2         # mm

for n in (6, 8, 10, 12):
    a = np.pi / n
    desliza = R_HUECO / np.cos(a)
    for largo in (39.5, 41.0):          # radio del disco cerrado: hueco + 2 o 3,5 mm de apoyo
        lejos = np.sqrt(largo**2 + desliza**2 + 2 * largo * desliza * np.cos(np.pi / 2 - a))
        print(f"{n:2d} gajos de {largo} mm: cada uno desliza {desliza:4.1f} mm, "
              f"llega a {lejos:4.1f} mm del centro, carcasa de unos {2 * (lejos + HOLGURA + PARED):5.1f} mm")

# Comprobacion punto a punto con 8 gajos: abiertos no se pisan y dejan libre el circulo de 75
n, largo = 8, 41.0
a = np.pi / n
t = R_HUECO / np.cos(a)

def gajo(k, abierto, p):
    ang = 2 * a * k
    d = t * np.array([np.cos(ang + a - np.pi / 2), np.sin(ang + a - np.pi / 2)]) if abierto else np.zeros(2)
    q = p - d
    rel = (np.arctan2(q[:, 1], q[:, 0]) - ang) % (2 * np.pi)
    return (rel > 1e-6) & (rel < 2 * a - 1e-6) & (np.hypot(q[:, 0], q[:, 1]) < largo)

g = np.linspace(-80, 80, 1601)
X, Y = np.meshgrid(g + 0.013, g + 0.037)     # desplazada para que ningun punto caiga justo en una junta
P = np.c_[X.ravel(), Y.ravel()]
R = np.hypot(P[:, 0], P[:, 1])
ab = sum(gajo(k, True, P).astype(int) for k in range(n))
ce = sum(gajo(k, False, P).astype(int) for k in range(n))
print("8 gajos abiertos: puntos pisados por dos gajos:", int((ab > 1).sum()),
      "| puntos tapados dentro del circulo de 75:", int(((ab > 0) & (R < 37.4)).sum()))
print("8 gajos cerrados: puntos sin tapar dentro de 81,8 mm de diametro:", int(((ce == 0) & (R < 40.9)).sum()))

# Dos compuertas (D-22): dos medios discos que se apartan en linea recta
print(f"dos compuertas de 41 mm de radio: llegan a {41 + R_HUECO:.1f} mm del centro, "
      f"carcasa de unos {2 * (41 + R_HUECO + HOLGURA + PARED):.0f} mm")
