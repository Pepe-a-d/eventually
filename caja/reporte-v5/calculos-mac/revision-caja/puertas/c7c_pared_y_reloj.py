# Grueso de la pared de la pista que empuja o sujeta la bola en cada momento, y a que inclinacion toca la puerta abierta al reloj de pega
from comun import *
from shapely.geometry import Polygon, Point, LineString
from c7_paredes import planta, bola_en_aro, anillo, cuern
print('grueso de pared a cada lado de la bola, en la direccion en que la bola empuja (la bola solo se mueve en X del mundo)')
print('  psi  puerta | pared del lado de DENTRO (hacia -X: la que para a la puerta al abrirse de mas / la que la cierra) | pared del lado de FUERA (+X: la que la abre / la que impide que se cierre)')
sen = p['aro_sentido']
for psi in (0.0, 1.0, 2.0, 2.5, 2.75, 3.0, 3.25, 3.5, 4.0, 5.5, 7.0, 7.5, 8.0, 8.5, 9.0, 10.0, 10.44, 11.0):
    c = bola_en_aro(psi)
    # direccion X del mundo, vista desde el aro: el aro ha girado sen*psi, asi que en el aro X del mundo es (cos(-sen*psi), sin(-sen*psi))
    a = -math.radians(sen * psi); ux, uy = math.cos(a), math.sin(a)
    ang = 45.0 - math.degrees(math.asin(D.bola_x(p, d, psi) / p['manivela_r']))
    res = []
    for sg in (-1, 1):
        ray = LineString([c, (c[0] + sg * ux * 14, c[1] + sg * uy * 14)])
        w = ray.intersection(cuern)
        tr = sorted([g for g in (w.geoms if hasattr(w, 'geoms') else [w]) if g.length > 1e-6], key=lambda g: Point(c).distance(g))
        if not tr: res.append('NO HAY PARED en esa direccion'); continue
        g0 = tr[0]
        res.append('a %.2f mm del centro de la bola, %.2f mm de pared, %.2f con anillo debajo' % (Point(c).distance(g0), g0.length, g0.intersection(anillo).length))
    print('  %5.2f %6.1f | %s | %s' % (psi, ang, res[0], res[1]))
print('PUERTA ABIERTA INCLINADA HACIA DENTRO Y RELOJ DE PEGA (medidas del reloj supuestas)')
def gap_reloj(ang):
    peor = (99, 0, 0)
    for tau in np.arange(92, 345.01, 1.0):
        R = mv('reloj_de_pega', tau)
        for sx in (1, -1):
            g = R.min_gap(puerta(sx, ang), 8.0)
            if g < peor[0]: peor = (g, tau, sx)
    return peor
for ang in (90.0, 88.0, 87.15, 86.25, 85.0, 84.0, 83.0, 82.5, 82.33):
    g, tau, sx = gap_reloj(ang)
    vmax = 0
    if g <= 1e-9:
        vmax = max(vol(mv('reloj_de_pega', t), puerta(sx, ang)) for t in np.arange(tau - 15, tau + 15, 1.0))
    print('  puertas a %.2f grados (inclinadas %.2f hacia dentro): reloj a %.2f mm de la puerta %s (tubo %.0f)%s' % (ang, 90 - ang, g, 'derecha' if sx > 0 else 'izquierda', tau, ('; volumen pisado %.3f mm3' % vmax) if g <= 1e-9 else ''))
b = mv('reloj_de_pega', 0).bounding_box(); print('  reloj de pega: x de %.2f a %.2f; cara de dentro de la puerta abierta a +-%.2f' % (b[0], b[3], d['cara_dentro_abierta']))
