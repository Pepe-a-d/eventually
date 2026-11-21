# Dibuja una capa de una pieza en postura de impresion (SVG): en gris la capa de debajo, en azul la capa, en rojo lo que queda sin apoyo.
# Uso: python dibuja.py <pieza|3mf:n> z_capa salida.svg [x0 y0 x1 y1]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shapely.geometry import box
from comun import *
import detalle

def camino(g):
    d = []
    for q in trozos(g, 1e-9):
        for r in [q.exterior] + list(q.interiors):
            c = list(r.coords)
            d.append('M' + ' L'.join('%.3f,%.3f' % (x, -y) for x, y in c) + 'Z')
    return ' '.join(d)

def dibuja(arg, z, salida, ventana=None):
    s, inv = detalle.carga(arg)
    i = int(z / CAPA)
    g = a_shapely(s.slice((i + 0.5) * CAPA + EPS_Z)); prev = a_shapely(s.slice((i - 0.5) * CAPA + EPS_Z)) if i > 0 else Polygon()
    if ventana is None:
        b = g.union(prev).bounds; ventana = [b[0] - 2, b[1] - 2, b[2] + 2, b[3] + 2]
    x0, y0, x1, y1 = ventana; w, h = x1 - x0, y1 - y0; esc = 1000.0 / max(w, h)
    rojo = g.difference(prev.buffer(0.22))
    lw = 0.6 / esc
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%.3f %.3f %.3f %.3f">' % (w * esc, h * esc, x0, -y1, w, h),
           '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="white"/>' % (x0, -y1, w, h)]
    paso = 10 if max(w, h) > 60 else (5 if max(w, h) > 25 else 1)
    import math
    for k in range(int(math.floor(x0 / paso)), int(math.ceil(x1 / paso)) + 1):
        svg.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#ccc" stroke-width="%g"/><text x="%g" y="%g" font-size="%g" fill="#888">%g</text>' % (k * paso, -y1, k * paso, -y0, lw, k * paso, -y0 - 0.3 * paso * 0.3, 0.25 * paso, k * paso))
    for k in range(int(math.floor(y0 / paso)), int(math.ceil(y1 / paso)) + 1):
        svg.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#ccc" stroke-width="%g"/><text x="%g" y="%g" font-size="%g" fill="#888">%g</text>' % (x0, -k * paso, x1, -k * paso, lw, x0, -k * paso, 0.25 * paso, k * paso))
    svg.append('<path d="%s" fill="#999" fill-rule="evenodd" stroke="#555" stroke-width="%g"/>' % (camino(prev), lw))
    svg.append('<path d="%s" fill="#3478f6" fill-opacity="0.45" fill-rule="evenodd" stroke="#1a4fb0" stroke-width="%g"/>' % (camino(g), lw))
    svg.append('<path d="%s" fill="red" fill-rule="evenodd"/>' % camino(rojo))
    svg.append('</svg>')
    open(salida, 'w').write('\n'.join(svg))

if __name__ == '__main__':
    a = sys.argv
    dibuja(a[1], float(a[2]), a[3], [float(x) for x in a[4:8]] if len(a) >= 8 else None)
