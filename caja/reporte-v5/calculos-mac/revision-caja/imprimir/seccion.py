# Seccion vertical de una pieza en postura de impresion, por un plano que pasa por el eje Z con un angulo dado. Escribe SVG y lista los vertices.
# Uso: python seccion.py <pieza|3mf:n> angulo_grados salida.svg [r0 z0 r1 z1]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
import detalle, dibuja

def seccion(arg, ang, y=0.0):
    s, inv = detalle.carga(arg)
    t = s.rotate([0, 0, -ang]).translate([0, -y, 0]).rotate([-90, 0, 0])      # el plano Y = y pasa a ser Z = 0
    g = a_shapely(t.slice(1e-4))
    return g                                                          # (r, z) con z hacia arriba: girar -90 sobre X lleva z a y'

if __name__ == '__main__':
    a = sys.argv
    g = seccion(a[1], float(a[2]))
    v = [float(x) for x in a[4:8]] if len(a) >= 8 else None
    if v: g = g.intersection(box(*v))
    for q in trozos(g, 1e-6):
        print('trozo de %.2f mm2:' % q.area, ' '.join('(%.2f, %.2f)' % c for c in list(q.exterior.coords)[:-1][:60]))
    x0, y0, x1, y1 = v or g.bounds
    w, h = x1 - x0, y1 - y0; esc = 1000.0 / max(w, h)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%.3f %.3f %.3f %.3f">' % (w * esc, max(h * esc, 50), x0, -y1, w, h),
           '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="white"/>' % (x0, -y1, w, h)]
    k = 0.0
    while k <= y1:
        if k >= y0: svg.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#ddd" stroke-width="%g"/>' % (x0, -k, x1, -k, 0.3 / esc))
        k += 0.2
    svg.append('<path d="%s" fill="#3478f6" fill-opacity="0.6" fill-rule="evenodd" stroke="#1a4fb0" stroke-width="%g"/>' % (dibuja.camino(g), 0.8 / esc))
    svg.append('</svg>'); open(a[3], 'w').write('\n'.join(svg))
