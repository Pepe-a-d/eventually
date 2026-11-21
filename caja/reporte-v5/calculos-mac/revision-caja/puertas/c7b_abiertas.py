# Comprobacion 7 (segunda parte): que sujeta las puertas abiertas; juego a lo largo del pasador; juego radial de la bisagra
from comun import *
EPS = 1e-4
G = 345.0
A = mv('aro_puertas', G)
def trozos(ang, dy=0.0, dz=0.0, dxx=0.0, sx=1):
    return {n: gira_puerta(m, sx, ang, dy).translate([dxx, 0, dz]) for n, m in (('bola', BOLA_D), ('varilla', VARILLA_D), ('cuerpo', CUERPO_D))}
def primero(f_trozos, contra, lo, hi):
    """primer valor del parametro en que algo pisa; devuelve (valor, que pisa)"""
    def pisa(v):
        return sum(vol(m, c) for m in f_trozos(v).values() for c in contra.values()) > EPS
    prev = lo; n = 200
    for i in range(1, n + 1):
        v = lo + (hi - lo) * i / n
        if pisa(v):
            v1 = bisec(pisa, prev, v, 10)
            T = f_trozos(v1 + (hi - lo) / n * 0.3)
            q = ['%s-%s %.4f' % (a, b, vol(m, c)) for a, m in T.items() for b, c in contra.items() if vol(m, c) > 0]
            return v1, ', '.join(q)
        prev = v
    return None, ''
print('PUERTA ABIERTA (aro en abierto, en su sitio exacto)')
for nom, contra in (('solo el aro', {'aro': A}), ('solo la meseta', {'meseta': S['meseta']}), ('solo el pasador', {'pasador': S['pasador_derecho']}), ('solo el marco', {'marco': S['marco']}), ('solo la rueda central', {'rueda': S['rueda_central']})):
    v1, q1 = primero(lambda v: trozos(90 + v), contra, 0.0, 40.0)
    v2, q2 = primero(lambda v: trozos(90 - v), contra, 0.0, 40.0)
    print('  %-22s: hacia fuera para a %s grados (%s) | hacia dentro para a %s grados (%s)' % (nom, '%.2f' % (90 + v1) if v1 is not None else '>130', q1, '%.2f' % (90 - v2) if v2 is not None else '<50', q2))
# huella de contacto de la bola al empujar
print('huella de la bola en la pared de la pista al pasarse del punto de contacto (puerta abierta, hacia fuera y hacia dentro):')
for sg, base in ((1, 93.03), (-1, 87.15)):
    for extra in (0.25, 0.5, 1.0):
        ang = base + sg * extra
        b = gira_puerta(BOLA_D, 1, ang); I = b ^ A
        if I.volume() <= 0: print('   %.2f: nada' % ang); continue
        bb_ = I.bounding_box()
        print('   puerta a %.2f (%.2f grados pasada): volumen pisado %.4f mm3, caja de la huella %.2f x %.2f x %.2f mm, a z %.2f..%.2f; centro bola z %.2f' % (ang, extra, I.volume(), bb_[3] - bb_[0], bb_[4] - bb_[1], bb_[5] - bb_[2], bb_[2], bb_[5], d['eje_z'] - 8 * math.cos(math.radians(45 - ang))))
print('  la bola esta a %.1f mm del eje; el canto libre de la puerta, a %.2f: una fuerza en el canto llega a la bola multiplicada por %.2f' % (p['manivela_r'], d['eje_x'] - p['junta'] / 2, (d['eje_x'] - p['junta'] / 2) / p['manivela_r']))
lv = p['manivela_r'] - math.hypot(p['puerta_grueso'] / 2, p['puerta_grueso'] / 2)
print('  varilla: diametro %.1f; de la cara de la puerta al centro de la bola, %.2f mm al aire' % (p['manivela_d'], lv))
print('JUEGO A LO LARGO DEL PASADOR (Y), puerta derecha, con todo lo demas en su sitio exacto')
for nom, tau in (('cerrada', 0.0), ('a medio abrir (tubo 72,5)', 72.5), ('abierta', 345.0)):
    ang = D.movimiento(p, d, tau)[2]
    contra = {'aro': mv('aro_puertas', tau), 'meseta': S['meseta'], 'marco': S['marco'], 'otra puerta': mv('puerta_izquierda', tau), 'rueda': S['rueda_central']}
    for sg in (1, -1):
        v, q = primero(lambda v: trozos(ang, dy=sg * v), contra, 0.0, 1.0)
        print('  %-26s hacia %s: %s mm hasta tocar (%s)' % (nom, 'atras (+Y)' if sg > 0 else 'delante (-Y)', '%.3f' % v if v is not None else '>1', q))
        for c_nom in ('meseta',):
            v, q = primero(lambda v: trozos(ang, dy=sg * v), {c_nom: contra[c_nom]}, 0.0, 1.0)
            print('  %-26s        sin contar el aro: %s mm (%s)' % ('', '%.3f' % v if v is not None else '>1', q))
print('JUEGO RADIAL DE LA BISAGRA: agujero de la puerta %.2f de radio, pasador %.2f -> %.2f mm por lado; agujeros de meseta y marco %.2f -> %.2f por lado' % (p['pasador_d'] / 2 + p['holg_gira'], p['pasador_d'] / 2, p['holg_gira'], p['pasador_d'] / 2 + p['holg_fija'], p['holg_fija']))
for nom, tau in (('cerrada', 0.0), ('abierta', 345.0)):
    ang = D.movimiento(p, d, tau)[2]
    contra = {'aro': mv('aro_puertas', tau), 'meseta': S['meseta'], 'pasador': S['pasador_derecho'], 'otra puerta': mv('puerta_izquierda', tau), 'rueda': S['rueda_central'], 'marco': S['marco']}
    for eje, vec in (('arriba (+Z)', (0, 1)), ('abajo (-Z)', (0, -1)), ('afuera (+X)', (1, 0)), ('adentro (-X)', (-1, 0))):
        v, q = primero(lambda v: trozos(ang, dxx=vec[0] * v, dz=vec[1] * v), contra, 0.0, 1.0)
        print('  %-8s hacia %-12s: %s mm hasta tocar (%s)' % (nom, eje, '%.3f' % v if v is not None else '>1', q))
