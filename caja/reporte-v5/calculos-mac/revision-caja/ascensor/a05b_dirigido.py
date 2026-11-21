# 5 (bis). Arriba: busqueda dirigida. Se empuja la plataforma hacia una direccion (con giro y cabeceo a favor) hasta donde la dejan
# el tubo y las columnas, y se mira si el pedestal llega a tocar el marco / la meseta (rendija nominal 0.40).
from comun import *
G = p['giro_tubo']; UMB = 1e-3
pl = puesta('plataforma', G); tu = puesta('tubo', G); ba = S['base']
zc = d2['zc0'] + d['recorrido']
otros = {o: puesta(o, G) for o in ('marco', 'meseta')}
def postura(dx, dy, dz, gz, cx, cy):
    return pl.translate([0, 0, -zc]).rotate([cx, cy, gz]).translate([dx, dy, zc + dz])
def vale(q): return vol(q, tu) <= UMB and vol(q, ba) <= UMB
peor = (9, None); toca = None
for phi in range(0, 360, 15):
    ux, uy = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    for gz in (-0.25, -0.15, 0.0, 0.15, 0.25):
        for cab in (0.0, 0.1, 0.2):
            # cabeceo que inclina la cabeza del pedestal hacia (ux, uy): giro alrededor del eje horizontal perpendicular
            cx, cy = -cab * uy, cab * ux
            for dz in (-0.2, 0.0, 0.2):
                e = 0.0
                while e < 1.0:
                    if not vale(postura((e + 0.02) * ux, (e + 0.02) * uy, dz, gz, cx, cy)): break
                    e += 0.02
                if e == 0.0 and not vale(postura(0, 0, dz, gz, cx, cy)): continue
                q = postura(e * ux, e * uy, dz, gz, cx, cy)
                for o, A_ in otros.items():
                    v = vol(q, A_); g = q.min_gap(A_, 1.0)
                    if v > UMB and (toca is None or v > toca[0]): toca = (v, o, phi, e, dz, gz, cab)
                    if g < peor[0]: peor = (g, o, phi, e, dz, gz, cab)
print('lo mas cerca: %.3f mm de %s (direccion %d grados, desplazada %.2f mm, dz %.1f, giro %.2f, cabeceo %.1f grados)' % peor)
print('pisa:', 'NO en ninguna de las posturas probadas' if toca is None else '%.3f mm3 a %s (direccion %d, desplazada %.2f, dz %.1f, giro %.2f, cabeceo %.1f)' % toca)
