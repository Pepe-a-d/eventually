# Eventually, caja v5: auditoria del modelo entero (25-nov-2026, sesion del PC). Cada linea dice 'bien', 'OJO' o 'FALLA'.
#   python3 caja_auditoria_v5.py > reporte-v5/caja-auditoria.txt
# Mira lo que no miran caja_piezas_v5.py ni la revision de la sesion del Mac:
#   A. MONTAJE: cada pieza recorre su camino de entrada, en el orden del reporte, sin pisar a las que ya estan puestas.
#   B. IMPRESION: cada pieza, orientada como se imprime, capa a capa: islas en el aire, voladizos, puentes largos, paredes finas, y que quepa.
#   C. HOLGURAS: en todo el recorrido, que distancia queda entre cada dos piezas que se mueven una respecto de otra.
# Son pruebas de geometria. 'bien' quiere decir que el dibujo cumple, no que la pieza impresa funcione.
import math, sys
import numpy as np
import manifold3d as mf
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union, polylabel
import caja_piezas_v5 as C

D = C.D
p, d, d2, P = C.piezas()
S = {n: C.solido(q.ops) for n, q in P.items()}
G = p['giro_tubo']
cuenta = {'FALLA': 0, 'OJO': 0}
def linea(estado, txt):
    if estado in cuenta: cuenta[estado] += 1
    print('  %-5s %s' % (estado, txt)); sys.stdout.flush()
def puesta(n, tau): return C.mover(S[n], n, P[n].mueve, p, d, tau)
def puerta(sx, ang):
    n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
    return S[n].translate([-sx * d['eje_x'], 0, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z']])
def caja(m): return m.bounding_box()
def lejos(a, b, h=0.0):
    A, B = caja(a), caja(b)
    return A[0] > B[3] + h or B[0] > A[3] + h or A[1] > B[4] + h or B[1] > A[4] + h or A[2] > B[5] + h or B[2] > A[5] + h
def pisa(a, b): return 0.0 if lejos(a, b) else (a ^ b).volume()
SAT = ['satelite_%d' % i for i in range(1, 7)]

# ================================================================ A. MONTAJE
print('A. MONTAJE, en el orden del apartado 7 del reporte. Cada pieza baja (o entra) por su camino; se mira cuanto pisa a las ya puestas.')
def camino(movil, fijos, vec, dist, admite=0.05):
    """movil: lista de solidos ya en su sitio final. Devuelve (lo que mas pisa, a que distancia del final)."""
    pasos = [dist - i * 1.0 for i in range(int(dist) - 2)] + [3.0 - 0.2 * i for i in range(16)]
    peor = (0.0, 0.0)
    for s in pasos:
        v = 0.0
        for m in movil:
            mm = m.translate([vec[0] * s, vec[1] * s, vec[2] * s])
            v += sum(pisa(mm, f) for f in fijos)
        if v > peor[0]: peor = (v, s)
    return peor
def paso(txt, movil, fijos, vec, dist, admite=0.05):
    v, s = camino(movil, fijos, vec, dist)
    linea('bien' if v <= admite else 'FALLA', '%s: lo que mas pisa por el camino, %.3f mm3%s' % (txt, v, '' if v <= admite else ' (a %.1f mm de su sitio)' % s))
    return v, s
Z = (0, 0, 1)
pd0, pi0 = S['pestillo_derecho'], S['pestillo_izquierdo']
paso('1a. pestillo derecho, por el extremo de fuera de su canal', [pd0], [S['plataforma']], (1, 0, 0), 48)
paso('1a. pestillo izquierdo', [pi0], [S['plataforma']], (-1, 0, 0), 48)
paso('1b. plataforma con sus pestillos, bajando sobre la base', [S['plataforma'], pd0, pi0], [S['base']], Z, 105)
paso('2.  tubo, bajando por fuera de las columnas hasta coger los tetones', [S['tubo']], [S['base'], S['plataforma'], pd0, pi0], Z, 105)
paso('3.  marco, sobre las columnas', [S['marco']], [S['base'], S['tubo'], S['plataforma']], Z, 40)
aroG, aro0 = puesta('aro_puertas', G), S['aro_puertas']
paso('4.  aro de las puertas, sobre el marco (girado a abierto)', [aroG], [S['marco'], S['tubo'], S['base']], Z, 40)
paso('4.  aro de las puertas, sobre el marco (girado a cerrado)', [aro0], [S['marco'], S['tubo'], S['base']], Z, 40)
paso('5.  meseta, sobre el cuello del marco', [S['meseta']], [S['marco'], aroG, S['tubo']], Z, 40)
TH = p['puerta_abierta']
pdA, piA = puerta(1, TH), puerta(-1, TH)
paso('6.  puerta derecha, de pie, con el aro en abierto', [pdA], [S['meseta'], aroG, S['marco']], Z, 40)
paso('6.  puerta izquierda, de pie, con la derecha ya puesta', [piA], [S['meseta'], aroG, S['marco'], pdA], Z, 40)
for n in ('pasador_derecho', 'pasador_izquierdo'):
    r = [camino([S[n]], [S['meseta'], S['marco'], pdA, piA, aroG, S['tubo'], S['base']], (0, sg, 0), 100) for sg in (1, -1)]
    linea('bien' if min(r)[0] <= 0.05 else 'FALLA', '7.  %s, metido de lado: por detras pisa %.3f mm3 y por delante %.3f (basta con que uno sea cero)' % (n.replace('_', ' '), r[0][0], r[1][0]))
pd_, pi_ = S['puerta_derecha'], S['puerta_izquierda']
paso('8.  teton, desde arriba, con las puertas cerradas', [S['teton']], [S['marco'], aro0, S['meseta'], pd_, pi_], Z, 30)
puesto = [S['base'], S['plataforma'], pd0, pi0, S['tubo'], S['marco'], aro0, S['meseta'], pd_, pi_, S['pasador_derecho'], S['pasador_izquierdo'], S['teton']]
paso('9.  plato, sobre el tubo', [S['plato']], puesto, Z, 30)
puesto.append(S['plato'])
for n in SAT:
    v, s = camino([S[n]], puesto, Z, 20)
    if v > 0.05: linea('FALLA', '10. %s en su eje: pisa %.3f mm3 a %.1f mm de su sitio' % (n, v, s))
    puesto.append(S[n])
linea('bien', '10. los seis satelites, cada uno en su eje (los que fallan, si alguno, estan en la linea de encima)')
paso('11. rueda central, sobre la meseta, despues del plato y los satelites', [S['rueda_central']], puesto, Z, 20)
puesto.append(S['rueda_central'])
paso('12a. bisel dentro del cuerpo, entrando por debajo', [S['bisel']], [S['cuerpo']], (0, 0, -1), 110)
v, s = camino([S['cuerpo'], S['bisel']], puesto, Z, 110)
linea('bien' if v <= 80 and s <= 4.0 else 'FALLA', '12b. cuerpo con el bisel dentro, bajando sobre todo lo demas: lo que mas pisa, %.1f mm3, a %.1f mm de su sitio. Son las cuatro pestanas de la base, donde entra a presion; en su sitio pisa %.3f' % (v, s, sum(pisa(S['cuerpo'], f) + pisa(S['bisel'], f) for f in puesto)))
puesto += [S['cuerpo'], S['bisel']]
paso('14. funda, bajando sobre la caja cerrada', [S['funda'], S['frase']], puesto, Z, 125)
# el soporte: entra con la caja abierta
abierto = [puesta(n, G) for n in P if n not in ('soporte', 'reloj_de_pega', 'funda', 'frase') and P[n].mueve != 'probeta']
paso('13. soporte con el reloj, bajando a su cajeado con la caja abierta del todo', [puesta('soporte', G), puesta('reloj_de_pega', G)], abierto, Z, 60)

# ================================================================ B. IMPRESION
print('B. IMPRESION. Cada pieza, orientada como se imprime, en capas de 0,2 mm. "Al aire" es lo que no tiene debajo la capa anterior ensanchada 0,25 mm.')
BOCA_ABAJO = {'cuerpo', 'funda', 'frase', 'bisel', 'rueda_central', 'puerta_derecha', 'puerta_izquierda', 'probeta_anillo', 'probeta_teton'}
DE_LADO = {'soporte'}
def capa(m, z):
    ps = [Polygon(np.asarray(a)) for a in m.slice(z).to_polygons()]
    ps = [q.buffer(0) for q in ps if len(q.exterior.coords) > 3]
    out = None
    for q in sorted(ps, key=lambda q: -q.area):
        out = q if out is None else out.symmetric_difference(q)
    return out
def trozos(g): return [q for q in getattr(g, 'geoms', [g]) if q.area > 0]
def mira_voladizo(U, apoyo, capa_g):
    """Clasifica un trozo al aire. Devuelve (tipo, medida en mm):
       isla      no toca nada apoyado                                   -> lado del trozo
       techo     apoyado en casi todo su contorno (un cajeado cerrado)  -> su ancho mayor (lo que hay que salvar en puente)
       puente    apoyado en dos lados enfrentados                       -> la luz
       voladizo  apoyado por un lado                                    -> lo que vuela"""
    borde = U.buffer(0.3).intersection(apoyo)
    if borde.is_empty or borde.area < 0.02: return 'isla', math.sqrt(U.area)
    try: polo = polylabel(U, 0.2)
    except Exception: polo = U.representative_point()
    ancho = 2 * polo.distance(U.exterior)
    contorno = U.exterior.length; tocado = U.exterior.intersection(apoyo.buffer(0.3)).length
    if tocado / contorno >= 0.75: return 'techo', ancho
    pm = polo; r = polo.distance(apoyo)
    for q in list(U.exterior.coords)[::max(1, len(U.exterior.coords) // 200)]:
        dq = Point(q).distance(apoyo)
        if dq > r: r, pm = dq, Point(q)
    mejor = None
    for pt in (polo, U.representative_point()):
        for k in range(18):
            a = math.pi * k / 18; dx, dy = math.cos(a), math.sin(a)
            dist = []
            for sg in (1, -1):
                hit = LineString([(pt.x, pt.y), (pt.x + sg * 60 * dx, pt.y + sg * 60 * dy)]).intersection(apoyo)
                dist.append(None if hit.is_empty else pt.distance(hit))
            if dist[0] is not None and dist[1] is not None:
                seg = LineString([(pt.x - dist[1] * dx, pt.y - dist[1] * dy), (pt.x + dist[0] * dx, pt.y + dist[0] * dy)])
                if seg.difference(capa_g.buffer(0.05)).length < 0.05 and (mejor is None or dist[0] + dist[1] < mejor): mejor = dist[0] + dist[1]
    if mejor is not None: return 'puente', mejor
    return 'voladizo', r
resumen = {}; DET = {}
SABIDO = {'tubo': 'La pared fina es la que separa cada iman del tope de su cara: 0,7 mm, a proposito, para que los imanes queden cerca', 'base': 'La pared fina es la que separa cada iman del tope de su cara: 0,7 mm, a proposito',
          'frase': 'Son los trazos de las letras: miden de 0,8 a 1,0 mm (1 % del area, menos de 0,7)',
          'soporte': 'Lo fino es la arista del hombro que agarran los pestillos (un canto de 90 grados, que nace en filo): a proposito'}
for n, q in P.items():
    if n in ('reloj_de_pega',) or (n.startswith('satelite_') and n != 'satelite_1') or n in ('pasador_izquierdo', 'pestillo_izquierdo') or q.mueve == 'probeta': continue
    m = S[n]
    if n in BOCA_ABAJO: m = m.rotate([180, 0, 0])
    if n in DE_LADO: m = m.rotate([0, 90, 0])
    b = m.bounding_box(); m = m.translate([0, 0, -b[2]]); alto = b[5] - b[2]
    ant = None; z = 0.1; islas = []; vol = []; pte = []; fina = (9.9, 0.0); base_a = 0.0
    while z < alto:
        g = capa(m, z)
        if g is None or g.is_empty: z += 0.2; continue
        if ant is None: base_a = g.area
        else:
            apoyo = g.intersection(ant.buffer(0.25))
            for U in trozos(g.difference(ant.buffer(0.25))):
                if U.area < 0.3: continue
                t, medida = mira_voladizo(U, apoyo, g)
                (islas if t == 'isla' else pte if t in ('puente', 'techo') else vol).append((medida, z, U.area, tuple(round(v_, 1) for v_ in U.bounds), t))
        # paredes finas: lo que desaparece al comer 0,35 por cada lado tiene menos de 0,7 mm de ancho
        if int(round(z * 10)) % 10 == 1:
            for e in (0.2, 0.3, 0.35):
                resto = g.difference(g.buffer(-e).buffer(e * 1.05))
                if max([t.area for t in trozos(resto)] + [0]) > 1.0 and 2 * e < fina[0]: fina = (2 * e, z)
        ant = g; z += 0.2
    pv = max(vol, default=(0, 0, 0, (), '')); pp = max(pte, default=(0, 0, 0, (), '')); pi = max(islas, default=(0, 0, 0, (), ''))
    DET[n] = {'vol': sorted(vol, reverse=True)[:6], 'pte': sorted(pte, reverse=True)[:4], 'islas': sorted(islas, reverse=True)[:4]}
    est = 'FALLA' if islas or pv[0] > 1.5 or pp[0] > 30 or b[3] - b[0] > 250 or b[4] - b[1] > 250 or alto > 250 else 'OJO' if pv[0] > 1.0 or pp[0] > 18 or fina[0] < 0.75 else 'bien'
    txt = '%-17s %-10s %5.0f x %5.0f x %5.0f mm; apoyo en la cama %6.0f mm2' % (n, 'boca abajo' if n in BOCA_ABAJO else 'de lado' if n in DE_LADO else 'de pie', b[3] - b[0], b[4] - b[1], alto, base_a)
    txt += '; islas en el aire: %s' % ('ninguna' if not islas else '%d (la mayor, %.1f mm, a %.1f mm de la cama)' % (len(islas), pi[0], pi[1]))
    txt += '; voladizo mayor: %s' % ('ninguno' if not vol else '%.1f mm, a %.1f mm de la cama' % (pv[0], pv[1]))
    txt += '; puente o techo mas largo: %s' % ('ninguno' if not pte else '%.1f mm (%s), a %.1f mm de la cama' % (pp[0], pp[4], pp[1]))
    txt += '; pared mas fina vista: %s' % ('0,75 mm o mas' if fina[0] > 9 else 'menos de %.1f mm, a %.1f mm de la cama' % (fina[0], fina[1]))
    if est == 'OJO' and n in SABIDO: txt += '. ' + SABIDO[n]
    linea(est, txt)

# ================================================================ C. HOLGURAS
print('C. HOLGURAS. De tope a tope, cada 5 grados de tubo: lo mas cerca que quedan dos piezas que se mueven una respecto de otra (se mira hasta 0,6 mm).')
nombres = [n for n in P if P[n].mueve not in ('funda', 'probeta')]
def grupo(n):
    mu = P[n].mueve
    return 'plataforma' if mu == 'plataforma' else mu
cerca = {}
taus = [float(t) for t in range(0, int(G), 5)] + [G]
for tau in taus:
    M = {n: puesta(n, tau) for n in nombres}
    for i, a in enumerate(nombres):
        for b in nombres[i + 1:]:
            if grupo(a) == grupo(b): continue
            if lejos(M[a], M[b], 0.6): continue
            g = M[a].min_gap(M[b], 0.6)
            k = (a, b)
            if k not in cerca or g < cerca[k][0]: cerca[k] = (g, tau)
# pares que se tocan a proposito (una apoya o desliza sobre la otra): se listan aparte
APROPOSITO = {('puerta_derecha', 'meseta'): 'A proposito: cerrada, la puerta descansa en su asiento', ('puerta_izquierda', 'meseta'): 'A proposito: cerrada, la puerta descansa en su asiento',
              ('plato', 'bisel'): 'A proposito: el bisel descansa y gira sobre el plato', ('tubo', 'base'): 'A proposito: el tubo descansa y gira sobre su pista de la base',
              ('satelite', 'bisel'): 'Es por arriba: en el dibujo el satelite toca el techo del bisel; de verdad descansa en el plato, 0,4 mm mas abajo. Entre flancos de diente quedan de 0,16 a 0,19',
              ('puerta_derecha', 'aro_puertas'): 'La bola en su pista: holgura de diseno', ('puerta_izquierda', 'aro_puertas'): 'La bola en su pista: holgura de diseno',
              ('plataforma', 'base'): 'A proposito: abajo, la plataforma queda a 0,15 de su asiento', ('tubo', 'plataforma'): 'Los tetones en la rampa'}
for (a, b), (g, tau) in sorted(cerca.items(), key=lambda kv: kv[1][0]):
    if g >= 0.6: continue
    a_ = a if not a.startswith('satelite') else 'satelite'; b_ = b if not b.startswith('satelite') else 'satelite'
    if (a.startswith('satelite') and a != 'satelite_1') or (b.startswith('satelite') and b != 'satelite_1'): continue
    linea('nota', '%-17s y %-17s lo mas cerca, %.3f mm (tubo a %3.0f grados)%s' % (a_, b_, g, tau, ('. ' + APROPOSITO[(a_, b_)]) if (a_, b_) in APROPOSITO else ''))
print('RESUMEN: %d FALLA y %d OJO' % (cuenta['FALLA'], cuenta['OJO']))
