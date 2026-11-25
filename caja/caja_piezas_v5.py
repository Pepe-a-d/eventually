# Eventually, caja v5 de puertas y ascensor. FASE 2: la forma de cada pieza y las comprobaciones en 3D.
#
# No necesita Fusion. Hace tres cosas:
#   1. Con las medidas de caja_diseno_v5.py describe cada pieza como una lista de operaciones sencillas
#      (prismas, cilindros, esferas y barridos con giro, que se suman o se restan).
#   2. Construye las piezas en 3D con la biblioteca manifold3d y las mueve grado a grado de tubo para
#      comprobar que no se pisan y que el reloj de pega queda a mas de 3 mm de todo.
#   3. Escribe caja-v5-piezas.json: las mismas operaciones, que es lo que lee generador_caja_v5.py en Fusion.
#
# Necesita Python 3 con numpy, shapely y manifold3d:   python3 caja_piezas_v5.py
#
# Todas las piezas se describen en su sitio, con la caja CERRADA (tubo a 0 grados). Ejes como en caja_diseno_v5.py:
# X a la derecha, Y hacia atras, Z hacia arriba, Z = 0 en la cara de arriba de las puertas.
# Al abrir, el bisel, el tubo y el plato giran A FAVOR de las agujas del reloj vistos desde arriba.
import json, math, os, sys
import numpy as np
from shapely.geometry import Polygon, Point, LineString, box
from shapely.affinity import rotate as srot, translate as strans, scale as escala
from shapely.ops import unary_union
import caja_diseno_v5 as D

AQUI = os.path.dirname(os.path.abspath(__file__))
ROT = -1.0                      # sentido de giro del tubo al abrir (-1: a favor de las agujas del reloj)
PESTILLO_LIBRE = 15.0      # mm del final de la subida en que los pestillos del soporte quedan libres: asi, quien pone el soporte sin abrir del todo no lo deja sin sujetar

# ---------------------------------------------------------------- formas planas
def pol(r, a):
    return (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))

def disco(r, c=(0.0, 0.0), n=None):
    n = n or max(24, int(4 * round(r * 0.9 + 6)))
    return Polygon([(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)])

def corona(ra, rb):
    return disco(rb).difference(disco(ra))

def sector(ra, rb, a0, a1, paso=1.0):
    n = max(2, int(abs(a1 - a0) / paso) + 1)
    angs = [a0 + (a1 - a0) * i / n for i in range(n + 1)]
    return Polygon([pol(rb, a) for a in angs] + [pol(ra, a) for a in reversed(angs)])

def partes(g):
    return [q for q in (list(g.geoms) if hasattr(g, 'geoms') else [g]) if q.geom_type == 'Polygon' and q.area > 1e-5]

def giro2(g, ang):
    return srot(g, ang, origin=(0, 0))

def geo(g):
    """Poligonos de shapely -> listas [[contorno, [agujeros]], ...] con 4 decimales."""
    return [[[[round(x, 4), round(y, 4)] for x, y in list(q.exterior.coords)[:-1]], [[[round(x, 4), round(y, 4)] for x, y in list(h.coords)[:-1]] for h in q.interiors]] for q in partes(g)]

def engranaje(z, m, juego, add=1.0, ded=1.25, pa=20.0, fase=0.0, n=7):
    """Rueda dentada de evolvente, dientes hacia fuera. 'fase' (grados): donde cae el centro de un diente."""
    rp = m * z / 2.0; rb = rp * math.cos(math.radians(pa)); ra = rp + add * m; rf = rp - ded * m
    inv = lambda a: math.tan(a) - a
    medio = (math.pi * m / 2.0 - juego / 2.0) / 2.0 / rp            # medio grueso del diente en el primitivo, en radianes
    def semi(r):                                                   # medio angulo del diente al radio r
        r = max(r, rb)
        return medio + inv(math.radians(pa)) - inv(math.acos(rb / r))
    radios = [rf] + [max(rb, rf) + (ra - max(rb, rf)) * i / (n - 1) for i in range(n)]
    pts = []
    for k in range(z):
        c = math.radians(fase) + 2 * math.pi * k / z
        pts.append((rf * math.cos(c - math.pi / z), rf * math.sin(c - math.pi / z)))
        for r in radios: pts.append((r * math.cos(c - semi(r)), r * math.sin(c - semi(r))))
        for r in reversed(radios): pts.append((r * math.cos(c + semi(r)), r * math.sin(c + semi(r))))
    return Polygon(pts).buffer(0)

# ---------------------------------------------------------------- piezas como listas de operaciones
class Pieza:
    def __init__(self, nombre, color='blanco', mueve='fijo', nota=''):
        self.nombre, self.color, self.mueve, self.nota, self.ops = nombre, color, mueve, nota, []
    def prisma(self, g, c0, c1, op='+', eje='z'):
        """Poligono plano extruido de c0 a c1. eje 'z': puntos (x, y). eje 'y': puntos (x, z). eje 'x': puntos (y, z)."""
        if g.is_empty: return self
        self.ops.append({'t': 'prisma', 'eje': eje, 'c0': round(min(c0, c1), 4), 'c1': round(max(c0, c1), 4), 'pol': geo(g), 'op': op})
        return self
    def cil(self, a, b, r, op='+'):
        self.ops.append({'t': 'cil', 'a': [round(v, 4) for v in a], 'b': [round(v, 4) for v in b], 'r': round(r, 4), 'op': op})
        return self
    def cono(self, a, b, ra, rb_, op='+'):
        """Tronco de cono de eje a-b: radio ra en a y rb_ en b."""
        self.ops.append({'t': 'cono', 'a': [round(v, 4) for v in a], 'b': [round(v, 4) for v in b], 'ra': round(ra, 4), 'rb': round(rb_, 4), 'op': op})
        return self
    def revol(self, perfil, a0, a1, op='+'):
        """Perfil en el plano (radio, z), como lista de puntos, girado alrededor del eje Z del angulo a0 al a1 (grados)."""
        self.ops.append({'t': 'revol', 'perfil': [[round(r, 4), round(z, 4)] for r, z in perfil], 'a0': round(min(a0, a1), 4), 'a1': round(max(a0, a1), 4), 'op': op})
        return self
    def esfera(self, c, r, op='+'):
        self.ops.append({'t': 'esfera', 'c': [round(v, 4) for v in c], 'r': round(r, 4), 'op': op})
        return self
    def helice(self, g, z0, z1, giro, op='+'):
        """Poligono en planta que sube de z0 a z1 girando 'giro' grados alrededor del eje Z."""
        self.ops.append({'t': 'helice', 'z0': round(z0, 4), 'z1': round(z1, 4), 'giro': round(giro, 5), 'pol': geo(g), 'op': op})
        return self

def piezas():
    p = D.params(); d = D.derivadas(p)
    P = {}
    def nueva(*a, **k):
        q = Pieza(*a, **k); P[q.nombre] = q; return q
    hg, hd, hf = p['holg_gira'], p['holg_desliza'], p['holg_fija']
    t = p['puerta_grueso']; xh = d['eje_x']; ze = d['eje_z']; rk = d['nudillo_r']; cola = p['puerta_cola']
    hx, hy = d['hueco_x'] / 2, d['hueco_y'] / 2
    py = d['puerta_y'] / 2
    rho = p['manivela_r']; rb = p['bola_d'] / 2; yb = d['bola_y']
    sen = p['aro_sentido']; PSI = d['aro_giro']
    zm0 = d['z_meseta0']                                      # cara de abajo de la meseta
    R_c = d['cuello_r']; R_ci = d['cuello_r_in']
    N3 = (0.0, 120.0, 240.0)
    ang_col = (0.0, 180.0, 262.0)                             # columnas: desiguales, para que nada entre girado. Dos van a derecha e izquierda: sujetan los pestillos del soporte
    ang_teton = (90.0, 212.0, 330.0)                          # tetones de la plataforma: uno va 2 grados fuera de sitio, para que el tubo solo entre en una posicion
    ang_llave = (20.0, 140.0, 255.0)                          # llaves de la rueda central en la meseta
    ang_almena = (15.0, 135.0, 250.0)                         # almenas del tubo en el plato
    d2 = {}                                                   # medidas que salen de aqui y usa el generador o el reporte

    # ============ PUERTAS (dos iguales; la izquierda es la derecha girada media vuelta) ============
    # seccion en X-Z de la puerta derecha, en su sitio y cerrada
    largo = xh - p['junta'] / 2
    losa = box(xh - largo, -t, xh, 0)
    canto = disco(rk, (xh, ze), 64).intersection(box(xh, -t, xh + 50, 0))
    cuerpo = unary_union([losa, canto]).buffer(0)
    ll, lg, lh = p['labio_largo'], p['labio_grueso'], p['labio_hueco']
    # junta en bisel (a 45 grados): el labio es una cuna y el rebaje de la otra mitad, su hueco. Asi la puerta se imprime
    # con la cara de arriba en la cama y sin soportes, y mirando por la raya solo se ve puerta
    j2 = p['junta'] / 2; punta = 0.4
    labio = Polygon([(j2 + 0.01, -t), (-j2 - ll, -t), (-j2 - ll, -t + punta), (j2 + 0.01, -t + punta + ll + 2 * j2 + 0.01)])
    rebaje = Polygon([(j2 - 0.01, -t - 0.01), (j2 + ll + punta + lh, -t - 0.01), (j2 - 0.01, -t + punta + ll + lh + 0.01)])
    d2['canto_junta'] = t - (punta + ll + lh)                    # grueso que le queda al canto de la puerta en la mitad del rebaje
    # Las dos puertas ya no son la misma pieza: con dos iguales, las dos medias cunas no podian tapar el centro de la raya (quedaba un agujero).
    # La derecha lleva la cuna a todo lo largo; la izquierda, el hueco a todo lo largo. Las dos se imprimen igual, con la cara de arriba en la cama.
    th_o = p['puerta_abierta']
    bx, bz = xh + rho * math.sin(math.radians(45)), ze - rho * math.cos(math.radians(45))
    y_m0, y_m1 = yb - rb, yb + rb
    def hoja(q, con_cuna):
        q.prisma(cuerpo, -py, py, eje='y')
        if con_cuna: q.prisma(labio, -py, py, eje='y')
        else: q.prisma(rebaje, -py - 0.01, py + 0.01, '-', eje='y')
        # manivela: una varilla redonda en diagonal, hacia fuera y hacia abajo, con una bola en la punta
        q.cil((xh, yb, ze), (bx, yb, bz), p['manivela_d'] / 2)
        q.esfera((bx, yb, bz), rb)
        q.cil((xh, -py - 1, ze), (xh, py + 1, ze), p['pasador_d'] / 2 + hg, '-')
        return q
    pd = hoja(nueva('puerta_derecha', mueve='puerta_derecha', nota='La de la cuna: su canto del centro se mete bajo la otra'), True)
    pi_ = nueva('puerta_izquierda', mueve='puerta_izquierda', nota='La del hueco. Es otra pieza: no vale poner dos iguales')
    pi_.ops = gira_ops(hoja(Pieza('aux'), False).ops, 180.0)

    # ============ ARO DE PUERTAS ============
    # pista de la bola, en coordenadas del aro (aro en su posicion de cerrado)
    def bola_en_aro(psi):
        x = xh + D.bola_x(p, d, psi)
        a = -math.radians(sen * psi)
        return (x * math.cos(a) - yb * math.sin(a), x * math.sin(a) + yb * math.cos(a))
    eje_pista = LineString([bola_en_aro(PSI * i / 60.0) for i in range(-6, 67)])       # con un poco de sobra en los dos extremos
    wb = rb + p['bola_holgura']
    pista = eje_pista.buffer(wb, 12)
    hueco_barrido = unary_union([giro2(box(-hx - 0.5, -hy - 0.5, hx + 0.5, hy + 0.5), -sen * PSI * i / 12.0) for i in range(13)])     # el hueco, visto desde el aro mientras gira
    cuerno = eje_pista.buffer(wb + p['pista_pared'], 12).intersection(disco(d['aro_r_ext'], n=240)).difference(hueco_barrido)
    z_a0, z_a1 = d['z_corr0'], d['z_corr1']
    z_cuerno1 = min(ze - rho * math.cos(math.radians(45)) + 0.5, ze - rk - 0.5)      # por encima del centro de la bola, y por debajo de lo que baja el canto de la puerta al abrir
    aro = nueva('aro_puertas', mueve='aro', nota='Gira %.1f grados alrededor del hueco y mueve las dos puertas' % PSI)
    anillo = corona(d['aro_r_in'], d['aro_r_ext'])
    # brazo del aro, hacia atras: lleva la ranura en diagonal del teton
    Rt0, Rt1 = d['espiral_r_cerrada'], d['espiral_r_abierta']
    def teton_en_aro(s):
        r = Rt0 - s; a = math.radians(90.0 - sen * PSI * s / p['teton_recorrido'])
        return (r * math.cos(a), r * math.sin(a))
    eje_ranura = LineString([teton_en_aro(p['teton_recorrido'] * i / 40.0) for i in range(-3, 44)])
    wt = p['teton_d'] / 2 + hd
    ranura_brazo = eje_ranura.buffer(wt, 12)
    brazo_aro = unary_union([eje_ranura.buffer(wt + 2.6, 12), sector(d['aro_r_ext'] - 2.0, Rt1 + 2.0, 90 - sen * PSI - 9 if sen > 0 else 90 - 9, 90 + 9 if sen > 0 else 90 - sen * PSI + 9)]).buffer(0)
    brazo_aro = brazo_aro.intersection(disco(p['tubo_r'] - 0.8, n=240))
    planta_aro = unary_union([anillo, brazo_aro, cuerno, giro2(cuerno, 180)]).difference(ranura_brazo)      # el anillo llega hasta debajo de todo el cuerno: nada nace en el aire
    aro.prisma(planta_aro, z_a0, z_a1)
    for k in (0, 180):
        aro.prisma(giro2(cuerno, k).difference(giro2(pista, k)), z_a1 - 0.01, z_cuerno1)
        aro.prisma(giro2(pista, k), z_a0 + 1.2, z_cuerno1 + 0.01, '-')          # la pista baja dentro del anillo: la bola llega mas abajo a medio giro
    d2['cuerno'] = geo(cuerno); d2['pista'] = geo(pista)

    # ============ TETON SUELTO ============
    z_ranura_ala = d['z_ala1'] - 2.8
    te = nueva('teton', mueve='teton', nota='Suelto: va en la espiral del plato, en la ranura del brazo del aro y en la ranura recta del marco')
    te.cil((0, Rt0, z_ranura_ala + 0.3), (0, Rt0, d['z_plato0'] + p['espiral_fondo'] - 0.4), p['teton_d'] / 2)

    # ============ MARCO: ala, cuello y cuatro orejas para los pasadores ============
    ma = nueva('marco', nota='Apoya en las tres columnas. Se imprime con el ala en la cama, sin soportes')
    R_ala = p['tubo_r'] - 0.8
    hueco = box(-hx, -hy, hx, hy)
    ma.prisma(disco(R_ala, n=240).difference(hueco), d['z_ala0'], d['z_ala1'])
    # hueco de atras del cuello, por donde sale el brazo del aro (abierto hasta arriba: el aro entra por arriba)
    a_b0 = min(90 - 9, 90 - sen * PSI - 9) - 2.5; a_b1 = max(90 + 9, 90 - sen * PSI + 9) + 2.5
    barrido_brazo = unary_union([giro2(brazo_aro, sen * PSI * i / 12.0) for i in range(13)]).buffer(0.6)
    paso_brazo = barrido_brazo.intersection(corona(R_ci - 1, R_c + 1))
    cuello = corona(R_ci, R_c).difference(paso_brazo.buffer(0.3))
    ma.prisma(cuello, d['z_ala1'] - 0.01, zm0)
    # orejas: suben del cuello por dentro de la meseta; por ellas pasan los pasadores
    y_or = math.sqrt(((R_ci + R_c) / 2) ** 2 - xh ** 2)
    a_or = math.degrees(math.atan2(y_or, xh)); z_or1 = -1.0
    orejas = unary_union([sector(R_ci, R_c, s_ * a_or + q - 6.5, s_ * a_or + q + 6.5) for q in (0, 180) for s_ in (1, -1)])
    ma.prisma(orejas, zm0 - 0.01, z_or1)
    for sx in (1, -1):
        ma.cil((sx * xh, -80, ze), (sx * xh, 80, ze), p['pasador_d'] / 2 + hf, '-')
    # ranura recta del teton, en la cara de arriba del ala
    ma.prisma(LineString([(0, Rt1 - 1.0), (0, Rt0 + 1.0)]).buffer(wt, 12), z_ranura_ala, d['z_ala1'] + 0.01, '-')
    # cajas para las espigas de las columnas
    rc_ = p['tubo_r'] - 5.65                                       # radio medio de las columnas: van pegadas al tubo, por dentro
    col = lambda a, e=0.0: sector(rc_ - 3.85 - e, rc_ + 3.85 + e, a - 8 - math.degrees(e / rc_), a + 8 + math.degrees(e / rc_))
    espiga = lambda a, e=0.0: sector(rc_ - 2.05 - e, rc_ + 2.05 + e, a - 4.5 - math.degrees(e / rc_), a + 4.5 + math.degrees(e / rc_))
    for a in ang_col:
        ma.prisma(espiga(a, hf), d['z_ala0'] - 0.01, d['z_ala0'] + 3.0, '-')

    # ============ MESETA: la pieza que rodea las puertas ============
    me = nueva('meseta', nota='Lleva las bisagras. Los dos pasadores la cosen al marco y a la rueda central')
    me.prisma(disco(R_c, n=240), zm0, 0.0)
    me.prisma(hueco, zm0 - 1, 1, '-')
    rec_x = xh + math.sqrt((rk + 0.3) ** 2 - (t / 2) ** 2)        # borde del rebaje arriba: la raya junto a la bisagra
    me.prisma(box(-xh, -py - 0.3, xh, py + 0.3), -t, 0.01, '-')    # rebaje de las puertas; su suelo es el asiento
    for sx in (1, -1):                                             # cuna redonda de cada bisagra
        cuna = disco(rk + 0.3, (sx * xh, ze), 64).intersection(box(min(0, sx * 60), -50, max(0, sx * 60), 0.01))
        me.prisma(cuna, -py - 0.3, py + 0.3, '-', eje='y')
        me.cil((sx * xh, -R_c - 1, ze), (sx * xh, 80, ze), p['pasador_d'] / 2 + hf, '-')
    # ventanas: por donde suben los cuernos del aro y bajan las manivelas
    barrido_cuerno = unary_union([giro2(cuerno, sen * PSI * i / 12.0) for i in range(13)]).buffer(0.5)
    def capsula(th):                                               # varilla y bola en X-Z con la puerta abierta th grados
        a = math.radians(45.0 - th)
        c = (xh + rho * math.sin(a), ze - rho * math.cos(a))
        return unary_union([LineString([(xh, ze), c]).buffer(p['manivela_d'] / 2, 12), disco(rb, c, 48)])
    # la ventana es lo que barre la manivela de -2 a 92 grados, mas un pasillo hacia arriba con la puerta de pie:
    # por ahi entra la puerta al montarla (de pie, desde arriba, con el aro en 'abierto')
    c90 = (xh + rho * math.sin(math.radians(45.0 - th_o)), ze - rho * math.cos(math.radians(45.0 - th_o)))        # la bola con la puerta abierta
    varilla90 = LineString([(xh, ze), c90]).buffer(p['manivela_d'] / 2 + 0.25, 12); bola90 = disco(rb + 0.25, c90, 48)
    pasillo = unary_union([unary_union([g_, strans(g_, 0, 14.0)]).convex_hull for g_ in (varilla90, bola90)])   # lo que barren al subir 14 mm
    barrido_manivela = unary_union([capsula(-2.0 + (th_o + 4.0) * i / 96.0) for i in range(97)]).buffer(0.02).union(pasillo).buffer(0.03).simplify(0.004)
    for k in (0, 180):
        me.prisma(giro2(barrido_cuerno, k), zm0 - 1, z_cuerno1 + 0.6, '-')
    me.prisma(barrido_manivela, y_m0 - 0.35, y_m1 + 0.35, '-', eje='y')
    me.prisma(escala(barrido_manivela, xfact=-1, yfact=1, origin=(0, 0)), -y_m1 - 0.35, -y_m0 + 0.35, '-', eje='y')
    # cajas de las orejas del marco y ranuras de las llaves de la rueda central
    me.prisma(orejas.buffer(hf), zm0 - 1, z_or1 + 0.3, '-')
    llave = lambda a, e=0.0: sector(R_c - 1.6 - e, R_c + 0.5, a - 4.5 - e * 0.6, a + 4.5 + e * 0.6)
    for a in ang_llave:
        me.prisma(llave(a, hf), zm0 - 1, 1, '-')
    r_reb = R_c - 1.5; z_reb = -0.8                                # escalon del borde: encima apoya el labio de la rueda central
    me.prisma(corona(r_reb, R_c + 1), z_reb, 1, '-')
    d2['rec_x'] = rec_x; d2['r_reb'] = r_reb

    # ============ PASADORES ============
    y_pas = math.sqrt(R_c ** 2 - (xh + p['pasador_d'] / 2) ** 2) - 0.15
    for nombre, sx in (('pasador_derecho', 1), ('pasador_izquierdo', -1)):
        nueva(nombre, nota='Se mete por un lado antes de poner la rueda central, que luego le tapa las dos puntas').cil((sx * xh, -y_pas, ze), (sx * xh, y_pas, ze), p['pasador_d'] / 2)
    d2['pasador_largo'] = 2 * y_pas

    # ============ RUEDA CENTRAL con su placa de arriba (esqueleto) ============
    ce = nueva('rueda_central', color='blanco', nota='Fija. Se imprime boca abajo: la placa de arriba, en la cama')
    zs_, zp_, zr_ = int(p['z_central']), int(p['z_satelite']), int(d['z_bisel'])
    m = p['modulo']; jd = p['juego_dientes']
    sol = engranaje(zs_, m, jd, fase=0.0)
    r_eje_sat = round(0.305 * m * zp_ / 2, 2)                      # eje de cada satelite: algo menos de un tercio de su radio
    agujero_c = disco(R_c + hf, n=240)
    ce.prisma(sol.difference(agujero_c), d['z_engr0'], -p['esqueleto_grueso'])
    R_placa = d['central_punta'] + 1.5
    eg = p['esqueleto_grueso']
    r_techo0 = d['bisel_punta'] + d['z_engr1']                     # borde de dentro del techo del bisel, arriba (el techo es un cono a 45 grados)
    r_dedo0 = r_techo0 - 0.3                                       # punta de los dedos, arriba; abajo llega 'eg' mas lejos y queda debajo del techo del bisel
    ce.prisma(disco(R_placa, n=240).difference(agujero_c), -eg - 0.01, 0.0)
    for a in (0, 60, 120, 180, 240, 300):                          # dedos (puentes): tapan a medias los satelites y enganchan la rueda bajo el bisel
        ce.revol([(R_placa - 1, 0.0), (r_dedo0, 0.0), (r_dedo0 + eg, -eg), (R_placa - 1, -eg)], a - 3.5, a + 3.5)
    ce.prisma(corona(r_reb + hf, R_c + hf + 0.01), z_reb, 0.0)     # labio: apoya en el escalon de la meseta y la sujeta boca abajo
    for a in ang_llave:
        ce.prisma(llave(a).intersection(disco(R_c + hf + 0.3, n=240)), zm0 + 0.0, 0.0)
    d2['R_placa'] = R_placa; d2['r_dedo0'] = r_dedo0; d2['r_techo0'] = r_techo0

    # ============ SATELITES ============
    for k in range(int(p['n_satelites'])):
        th = 270.0 + 60.0 * k                                   # el azul sale del frente
        fase = th * (1 + zs_ / zp_) + 180.0 - 180.0 / zp_
        c = pol(d['r_ejes'], th)
        sat = nueva('satelite_%d' % (k + 1), color='azul' if k == 0 else 'blanco', mueve='satelite:%g' % th)
        sat.prisma(strans(engranaje(zp_, m, jd, fase=fase), c[0], c[1]).difference(disco(r_eje_sat + hg, c, 32)), d['z_engr0'], d['z_engr1'])

    # ============ PLATO portasatelites ============
    pl = nueva('plato', mueve='tubo', nota='Gira con el tubo. Por debajo lleva la espiral que mueve las puertas')
    pl.prisma(corona(d['plato_r_in'], d['tubo_r_ext']), d['z_plato0'], d['z_plato1'])
    for k in range(int(p['n_satelites'])):
        c = pol(d['r_ejes'], 270.0 + 60.0 * k)
        pl.cil((c[0], c[1], d['z_plato1'] - 0.01), (c[0], c[1], d['z_engr1'] - 0.2), r_eje_sat)
    # espiral: el teton esta en el angulo 90 del mundo; en el plato, a 90 - ROT*tau
    def espiral_pt(tau):
        s = D.movimiento(p, d, min(max(tau, 0.0), p['giro_tubo']))[0]
        return pol(Rt0 - s, 90.0 - ROT * tau)
    eje_esp = LineString([espiral_pt(tau) for tau in np.arange(-3.0, p['giro_tubo'] + 3.01, 1.0)])
    pl.prisma(eje_esp.buffer(wt, 12), d['z_plato0'] - 0.01, d['z_plato0'] + p['espiral_fondo'], '-')
    almena = lambda a, e=0.0: sector(p['tubo_r'] + 0.9 - e, d['tubo_r_ext'] + (1 if e else 0), a - 6 - e * 0.5, a + 6 + e * 0.5)
    for a in ang_almena:
        pl.prisma(almena(a, hf), d['z_plato0'] - 0.01, d['z_plato0'] + 3.0, '-')

    # ============ TUBO ============
    tu = nueva('tubo', mueve='tubo', nota='Tres ranuras en helice por dentro. Se imprime de pie, sin soportes')
    z_t0 = d['z_suelo'] + 0.6; z_t1 = d['z_plato0']
    tu.prisma(corona(p['tubo_r'], d['tubo_r_ext']), z_t0, z_t1)
    for a in ang_almena:
        tu.prisma(almena(a), z_t1 - 0.01, z_t1 + 2.8)
    # tope: una oreja por fuera, abajo
    a_tope = 45.0; a_oreja0 = a_tope - 7.5                       # en una esquina del cuerpo, que es donde hay sitio
    r_or1 = d['tubo_r_ext'] + 5.3; r_im = d['tubo_r_ext'] + 0.3      # la oreja pasa a 0,6 mm de la pared del cuerpo en el centro de cada lado
    tu.prisma(sector(d['tubo_r_ext'] - 0.5, r_or1, a_oreja0 - 3.5, a_oreja0 + 3.5), z_t0 + 8.5, z_t0 + 15.5)
    tu.revol([(d['tubo_r_ext'] - 0.5, z_t0 + 2.7), (d['tubo_r_ext'] - 0.5, z_t0 + 8.51), (r_or1, z_t0 + 8.51)], a_oreja0 - 3.5, a_oreja0 + 3.5)   # cartela a 45 grados: la oreja se imprime sin soportes
    gi = math.degrees((0.7 + 0.875) / (d['tubo_r_ext'] + 2.8))     # del centro de la ranura del iman a la cara del tope
    ranura_iman = lambda a: giro2(box(r_im, -0.875, r_or1 + 2, 0.875), a)      # el iman (5 x 1,6) entra de canto, desde fuera
    z_im0 = z_t0 + 9.4
    for sg in (1, -1):
        tu.prisma(ranura_iman(a_oreja0 + sg * (3.5 - gi)), z_im0, z_im0 + 5.3, '-')
    # ranuras en V (suelo y techo a 45 grados): se imprimen sin soportes y centran la plataforma. Los tetones son conos
    zc0 = d['z_disco1_abajo'] - p['disco_grueso'] / 2            # centro del teton con la plataforma abajo
    k_h = d['recorrido'] / (p['giro_arriba'] - p['giro_sube'])   # mm que sube por grado de tubo
    fondo = p['rampa_fondo']; rt_ = p['teton_plat_d'] / 2
    r0 = p['tubo_r'] - 0.5; r1 = p['tubo_r']; r2 = p['tubo_r'] + fondo - 0.4 + hd
    # Media altura de la V a cada radio. La ranura sube inclinada, asi que para que el teton tenga 'hd' de holgura de verdad
    # (medida a traves de la ranura) la altura en vertical es (radio del teton + hd) / coseno de la pendiente a ese radio.
    def media_altura(r):
        r_teton = rt_ - min(max(r - r1, 0.0), fondo - 0.4)
        return (r_teton + hd) / math.cos(math.atan(k_h * 180.0 / math.pi / r)) + 0.03
    hv0, hv1 = media_altura(r1), media_altura(r2)
    # los tramos planos van 5 centesimas mas holgados que la helice (y 0,1 mas hondos): asi, donde se juntan, sus caras se cruzan en vez de coincidir
    perfil_v = [(r0, -hv0 - 0.05), (r1, -hv0 - 0.05), (r2 + 0.1, -hv1 - 0.05), (r2 + 0.1, hv1 + 0.05), (r1, hv0 + 0.05), (r0, hv0 + 0.05)]
    sgn = 1.0 if -ROT > 0 else -1.0                              # en el tubo, el teton avanza hacia angulos crecientes si ROT < 0
    radios = [r0] + [r1 + (r2 - r1) * i_ / 8.0 for i_ in range(9)]
    for af in ang_teton:
        a_ini, a_sub, a_arr, a_fin = [af - ROT * x for x in (-3.0, p['giro_sube'], p['giro_arriba'], p['giro_tubo'] + 3.0)]
        tu.revol([(r, zc0 + z) for r, z in perfil_v], a_ini, a_sub, '-')                       # tramo plano de abajo
        tu.revol([(r, zc0 + d['recorrido'] + z) for r, z in perfil_v], a_arr, a_fin, '-')     # tramo plano de arriba
        # helice: la V, vista en planta, es una cuna de angulos; sube girando. Sus flancos son curvos (lineales en radio y angulo): con lados rectos se metia 0,16 mm
        centro0 = a_sub - sgn * hv0 / k_h                        # cuando el barrido empieza (media altura por debajo), el centro va medio ancho por detras
        cuna_h = Polygon([pol(r, centro0 - media_altura(max(r, r1)) / k_h) for r in radios] + [pol(r, centro0 + media_altura(max(r, r1)) / k_h) for r in reversed(radios)])
        tu.helice(cuna_h, zc0 - hv0, zc0 + d['recorrido'] + hv0, sgn * (d['recorrido'] + 2 * hv0) / k_h, '-')
        # entrada: por donde suben los tetones al meter el tubo desde arriba (queda debajo del teton con la caja cerrada)
        tu.prisma(sector(r0, r2, af - 2.7, af + 2.7), z_t0 - 0.01, zc0, '-')
    d2['zc0'] = zc0

    # ============ PLATAFORMA con pedestal ============
    pf = nueva('plataforma', mueve='plataforma', nota='Sube %.0f mm. Tres tetones en las ranuras del tubo y tres muescas en las columnas' % d['recorrido'])
    R_disco = p['tubo_r'] - 0.7
    disco_p = disco(R_disco, n=240)
    for a in ang_col:
        disco_p = disco_p.difference(col(a, hg + 0.1))
    z_d0, z_d1 = d['z_disco0_abajo'], d['z_disco1_abajo']
    pf.prisma(disco_p, z_d0, z_d1)
    for a in ang_teton:
        c0, c1, c2 = pol(R_disco - 3.0, a), pol(p['tubo_r'], a), pol(p['tubo_r'] + p['rampa_fondo'] - 0.4, a)
        pf.cil((c0[0], c0[1], zc0), (c1[0], c1[1], zc0), rt_)
        pf.cono((c1[0], c1[1], zc0), (c2[0], c2[1], zc0), rt_, rt_ - (p['rampa_fondo'] - 0.4))
    ped = box(-hx + p['pedestal_holgura'], -hy + p['pedestal_holgura'], hx - p['pedestal_holgura'], hy - p['pedestal_holgura'])
    pf.prisma(ped, z_d1 - 0.01, z_d1 + d['pedestal_alto'])
    # D-34: el soporte entra en un cajeado del pedestal que baja hasta dentro del disco, y dos pestillos lo cogen por el pie.
    # Cada pestillo va en un canal en cola de milano del disco, de derecha a izquierda, y por fuera apoya en una columna de la base.
    z_p = z_d1 + d['pedestal_alto']                             # cara de arriba del pedestal
    px_, py_ = 21.0, 25.0                                       # media peana del soporte: casi como el pedestal, para que en la mesilla no vuelque (BRIEF 13.2)
    z_pf = z_d1 - 3.7                                           # suelo del cajeado, dentro del disco
    zl0, zl1 = z_d1 - 3.3, z_d1 - 0.3                           # el pestillo, de abajo a arriba
    r_col = rc_ - 3.85                                          # cara de dentro de las columnas
    pf.prisma(box(-px_ - 0.2, -py_ - 0.2, px_ + 0.2, py_ + 0.2), z_pf, z_p + 1, '-')
    pf.prisma(box(-3.3, py_ + 0.1, 3.3, py_ + 1.9), z_pf, z_p + 1, '-')                       # ranura de la llave: el soporte solo entra mirando al frente
    canal = Polygon([(-5.0, z_d1 - 3.5), (5.0, z_d1 - 3.5), (4.0, z_d1 + 0.01), (-4.0, z_d1 + 0.01)])
    x_tope = px_ + 3.8                                          # hasta aqui llega el canal ancho: la barra del pestillo hace tope y no puede meterse en el cajeado vacio
    paso = box(-3.2, z_d1 - 3.5, 3.2, z_d1 - 0.1)               # de ahi al cajeado solo pasa la nariz
    pf.prisma(canal, x_tope, r_col + 4.0, '-', eje='x'); pf.prisma(canal, -r_col - 4.0, -x_tope, '-', eje='x')
    pf.prisma(paso, px_ - 0.1, x_tope + 0.1, '-', eje='x'); pf.prisma(paso, -x_tope - 0.1, -px_ + 0.1, '-', eje='x')
    pf.cil((0, 12, z_pf - 1.8), (0, 12, z_pf + 0.01), 2.6, '-')                               # iman del soporte, en el suelo del cajeado

    # ============ RELOJ DE PEGA con su soporte (supuesto) ============
    so = nueva('soporte', mueve='plataforma', nota='Pie alto que entra en el cajeado del pedestal, zocalo y pinza simplificada. Se imprime en blanco, como el pedestal')
    so.prisma(box(-px_, -py_, px_, py_), z_pf, z_p)                          # pie: baja por el cajeado hasta dentro del disco y queda a ras del pedestal
    so.prisma(box(-17.0, -20.0, 17.0, 20.0), z_p - 0.4, z_p + 4.0)           # zocalo: lo que asoma sobre el pedestal, como antes (pasa a 3 mm o mas del marco)
    so.prisma(box(-3.0, py_ - 0.01, 3.0, py_ + 1.5), z_pf, z_p)             # llave, detras
    so.cil((0, 12, z_pf - 0.01), (0, 12, z_pf + 1.8), 2.6, '-')             # iman, por debajo
    # el pestillo de la derecha, metido: nariz en cuna (dos chaflanes a 45 grados) y barra en cola de milano
    zm_ = (zl0 + zl1) / 2; x_nar = px_ - 2.0; x_fin = r_col - 0.25
    nariz = Polygon([(x_nar, zm_ - 0.5), (x_nar, zm_ + 0.5), (x_nar + 1.0, zl1), (px_ + 5.0, zl1), (px_ + 5.0, zl0), (x_nar + 1.0, zl0)])
    muesca = unary_union([nariz.buffer(0.2, join_style=2), box(x_nar + 0.8, zl0 - 0.2, px_ + 0.1, zl1 + 0.2)])
    entrada = Polygon([(px_ + 0.01, z_pf - 0.01), (px_ + 0.01, z_pf + 1.3), (px_ - 1.3, z_pf - 0.01)])     # chaflan de abajo: al meter el soporte, aparta el pestillo
    for sg in (1, -1):
        so.prisma(escala(muesca, xfact=sg, yfact=1, origin=(0, 0)), -3.4, 3.4, '-', eje='y')
        so.prisma(escala(entrada, xfact=sg, yfact=1, origin=(0, 0)), -py_ - 0.1, py_ + 0.1, '-', eje='y')
    pt_ = Pieza('aux')
    pt_.prisma(Polygon([(-4.75, zl0), (4.75, zl0), (3.75, zl1), (-3.75, zl1)]), px_ + 4.0, x_fin, eje='x')
    pt_.prisma(nariz, -3.0, 3.0, eje='y')
    pt_.prisma(Polygon([(x_fin + 0.01, zl0 - 0.01), (x_fin - 0.5, zl0 - 0.01), (x_fin + 0.01, zl0 + 0.5)]), -6, 6, '-', eje='y')      # canto de fuera, por abajo: resbala en la rampa de la columna
    nueva('pestillo_derecho', mueve='pestillo:0', nota='Sujeta el soporte por el pie. La columna de la base lo mantiene metido; arriba del todo, una muesca lo deja salir').ops = pt_.ops
    nueva('pestillo_izquierdo', mueve='pestillo:180', nota='Igual que el derecho, girado media vuelta').ops = gira_ops(pt_.ops, 180.0)
    dx_r = -(p['reloj_con_corona'] - p['reloj_cabeza_d']) / 2      # el reloj va centrado contando la corona
    so.prisma(box(dx_r - 14.5, -3, dx_r + 14.5, 3), z_p + 3.99, z_p + 19.0)   # travesano: pasa por dentro del brazalete
    re = nueva('reloj_de_pega', color='gris', mueve='plataforma', nota='Medidas SUPUESTAS del apartado 5 del brief')
    z_br0 = z_p + p['reloj_alto'] - p['brazalete_alto']
    ovalo = lambda e: Polygon([(p['brazalete_fondo'] / 2 * e * math.cos(2 * math.pi * i / 72), z_br0 + p['brazalete_alto'] / 2 + (p['brazalete_alto'] / 2 - (1 - e) * p['brazalete_fondo'] / 2) * math.sin(2 * math.pi * i / 72)) for i in range(72)])
    re.prisma(ovalo(1.0).difference(ovalo(0.86)), dx_r - 11, dx_r + 11, eje='x')        # brazalete: un ovalo de pie, de 22 de ancho
    so.prisma(ovalo(1.0).buffer(0.4).difference(ovalo(0.86).buffer(-0.4)), dx_r - 11.6, dx_r + 11.6, '-', eje='x')   # el soporte deja paso al brazalete; las dos mejillas de los lados unen el travesano a la peana
    z_cab = z_br0 + p['brazalete_alto'] / 2
    re.cil((dx_r, -p['brazalete_fondo'] / 2 - 0.0, z_cab), (dx_r, -p['brazalete_fondo'] / 2 + p['reloj_grueso'], z_cab), p['reloj_cabeza_d'] / 2)
    re.cil((dx_r + p['reloj_cabeza_d'] / 2 - 0.5, -p['brazalete_fondo'] / 2 + p['reloj_grueso'] / 2, z_cab), (dx_r + p['reloj_con_corona'] - p['reloj_cabeza_d'] / 2, -p['brazalete_fondo'] / 2 + p['reloj_grueso'] / 2, z_cab), 3.0)

    # ============ BISEL ============
    bi = nueva('bisel', mueve='bisel', nota='Se imprime boca abajo. Entra en el cuerpo por debajo')
    corona_dentada = disco(d['bisel_r_ext'], n=300).difference(engranaje(zr_, m, -jd, add=1.25, ded=1.0, fase=180.0 / zr_))
    bi.prisma(corona_dentada, d['z_engr0'], d['z_engr1'] + 0.4)      # entra 0,4 en el techo: con solo una centesima, Fusion deja una lamina hueca al unirlos
    bi.revol([(r_techo0, 0.0), (d['bisel_r_ext'], 0.0), (d['bisel_r_ext'], d['z_engr1']), (d['bisel_punta'], d['z_engr1'])], 0.0, 360.0)   # techo: tapa los dientes; su borde en cono retiene la rueda central
    bi.prisma(corona(d['bisel_fondo'] + 0.2, d['bisel_r_ext']), d['z_plato1'], d['z_engr0'] + 0.01)  # apoya en el canto del plato
    z_ala_b1 = d['z_cuerpo_arriba'] - 3.0 - p['aire']; z_ala_b0 = z_ala_b1 - 3.0
    bi.prisma(corona(d['tubo_r_ext'] + 0.5, d['bisel_r_ext']), z_ala_b0, d['z_plato1'] + 0.01)  # faldon por fuera del plato
    # ala en cono a 45 grados (estrecha arriba, ancha abajo): boca abajo, cada capa apoya en la anterior. En escalera de 0,8 mm seguia quedando al aire
    ala_ = p['bisel_ala']
    bi.revol([(d['bisel_r_ext'] - 0.01, z_ala_b0), (d['bisel_r_ext'] + ala_, z_ala_b0), (d['bisel_r_ext'] + ala_, z_ala_b1 - ala_), (d['bisel_r_ext'] - 0.01, z_ala_b1)], 0.0, 360.0)
    # grafilado: estrias en el canto que asoma
    n_est = 120
    estria = unary_union([giro2(box(d['bisel_r_ext'] - 0.6, -1.0, d['bisel_r_ext'] + 1, 1.0), 360.0 * i / n_est) for i in range(n_est)])
    bi.prisma(estria, d['z_cuerpo_arriba'] + 1.0, 0.01, '-')

    # ============ BASE con columnas ============
    ba = nueva('base', nota='Fondo de la caja y jaula de tres columnas')
    L = d['cuerpo_lado'] / 2
    ba.prisma(box(-L, -L, L, L), d['z_base'], d['z_suelo'])
    for a in ang_col:
        ba.prisma(col(a), d['z_suelo'] - 0.01, d['z_ala0'])
        ba.prisma(espiga(a), d['z_ala0'] - 0.01, d['z_ala0'] + 2.7)
    # D-34: en los ultimos milimetros de subida, cada columna de los lados tiene un alivio de 2,9 mm donde el pestillo puede salir; por debajo, una rampa a 45 grados
    # lo vuelve a meter en cuanto la plataforma empieza a bajar
    zr1 = zl0 + d['recorrido'] - 0.3 - PESTILLO_LIBRE          # el alivio empieza PESTILLO_LIBRE mm antes del final de la subida
    rampa_c = Polygon([(r_col - 0.4, zr1 - 3.3), (r_col + 2.9, zr1 + 0.01), (r_col - 0.4, zr1 + 0.01)])
    for sg in (1, -1):
        ba.prisma(box(min(sg * (r_col - 0.4), sg * (r_col + 2.9)), -4.8, max(sg * (r_col - 0.4), sg * (r_col + 2.9)), 4.8), zr1, d['z_ala0'] + 0.01, '-')
        ba.prisma(escala(rampa_c, xfact=sg, yfact=1, origin=(0, 0)), -4.8, 4.8, '-', eje='y')
    ba.prisma(corona(d['tubo_r_ext'] + hg + 0.1, d['tubo_r_ext'] + 2.6), d['z_suelo'] - 0.01, d['z_suelo'] + 2.8)     # aro que centra el tubo por fuera
    ba.prisma(sector(d['tubo_r_ext'] + 0.6, r_or1 + 0.4, a_tope - 4, a_tope + 4), d['z_suelo'] - 0.01, d['z_suelo'] + 16.5)   # tope del tubo
    for sg in (1, -1):
        ba.prisma(ranura_iman(a_tope + sg * (4 - gi)), z_im0, z_im0 + 5.3, '-')
    ba.prisma(corona(p['tubo_r'] + 1.0, d['tubo_r_ext'] - 1.0), d['z_suelo'] - 0.01, z_t0)          # pista en la que apoya y resbala el tubo
    # asiento de la plataforma: abajo del todo descansa aqui (a 0,15 mm), no colgada de sus tetones. Sin el, con la caja cerrada los tetones
    # quedan sobre las entradas del tubo, la plataforma baja 1 mm y al empezar a girar tendria que subir un escalon
    ba.prisma(corona(p['tubo_r'] - 46.0, p['tubo_r'] - 14.0), d['z_suelo'] - 0.01, d['z_disco0_abajo'] - 0.15)
    pared_in = L - p['cuerpo_pared']
    ba.prisma(box(-pared_in + hf, -pared_in + hf, pared_in - hf, pared_in - hf).difference(box(-pared_in + 2.2, -pared_in + 2.2, pared_in - 2.2, pared_in - 2.2)), d['z_suelo'] - 0.01, d['z_suelo'] + 5.0)

    # cuatro pestillos; el del frente es mas ancho, para que el cuerpo solo entre con el indice al frente
    lat = lambda e=0.0, sal=1.0: unary_union([giro2(box(pared_in - hf - 0.01, -w_ - e, pared_in - hf + sal + e, w_ + e), a) for a, w_ in ((0, 6), (90, 6), (180, 6), (270, 10))])
    ba.prisma(lat(sal=1.0), d['z_suelo'] + 2.2, d['z_suelo'] + 3.4)       # cuatro pestillos: el cuerpo entra a presion y hace clic
    ba.prisma(lat(sal=0.5), d['z_suelo'] + 3.4, d['z_suelo'] + 4.0)

    # ============ CUERPO ============
    cu = nueva('cuerpo', nota='Piel cuadrada. Se imprime boca abajo; el bisel se mete por debajo antes de montarlo')
    cu.prisma(box(-L, -L, L, L).difference(box(-pared_in, -pared_in, pared_in, pared_in)), d['z_suelo'], d['z_cuerpo_arriba'])
    cu.prisma(box(-L, -L, L, L).difference(disco(d['bisel_r_ext'] + 0.4, n=300)), d['z_cuerpo_arriba'] - 3.0, d['z_cuerpo_arriba'])
    cu.prisma(box(-1.0, -L - 0.6, 1.0, -L + 0.01), d['z_cuerpo_arriba'] - 9.0, d['z_cuerpo_arriba'] - 1.5)      # indice del frente, en relieve
    cu.prisma(lat(e=0.3, sal=1.0), d['z_suelo'] + 1.9, d['z_suelo'] + 4.4, '-')                                  # cajeras de los pestillos
    # llave del cuerpo: un taco en la base, al frente y escondido en el grueso de la pared; el cuerpo tiene su caja solo ahi. Girado, no asienta
    ba.prisma(box(-9.0, -pared_in - 1.6, 9.0, -pared_in + hf), d['z_suelo'] - 0.01, d['z_suelo'] + 4.0)
    cu.prisma(box(-9.3, -pared_in - 1.9, 9.3, -pared_in + 0.01), d['z_suelo'] - 0.01, d['z_suelo'] + 4.3, '-')
    cu.prisma(box(-7.0, L - 1.2, 7.0, L + 0.1), d['z_suelo'] - 0.01, d['z_suelo'] + 1.6, '-')                    # detras: ranura para meter una una o una moneda y sacar el cuerpo
    # llave de la funda: en la esquina de delante a la derecha, la funda lleva un taco 1,5 mm mas largo que entra en un cajeado del cuerpo. Girada, no asienta
    llave_f = box(L - 13.0, -L + 5.0, L - 5.0, -L + 13.0)
    cu.prisma(llave_f.buffer(0.4), d['z_cuerpo_arriba'] - 1.9, d['z_cuerpo_arriba'] + 0.01, '-')

    c_im = L - 9.0                                                  # imanes de la funda: en dos esquinas opuestas, por debajo del labio del cuerpo
    for sg in (1, -1):
        cu.cil((sg * c_im, sg * c_im, d['z_cuerpo_arriba'] - 3.01), (sg * c_im, sg * c_im, d['z_cuerpo_arriba'] - 1.2), 2.6, '-')

    # ============ FUNDA (campana cuadrada) y FRASE ============
    gf, wf, tf = 0.5, 2.0, 2.4                                      # holgura por lado, pared y techo
    Li, Lo = L + gf, L + gf + wf
    z_f0 = 1.0; z_f1 = z_f0 + tf                                    # el techo queda 1 mm por encima del bisel
    fu = nueva('funda', color='marmol', mueve='funda', nota='Suelta. Se imprime boca abajo: el techo, con la frase, en la cama')
    fu.prisma(box(-Lo, -Lo, Lo, Lo).difference(box(-Li, -Li, Li, Li)), d['z_base'], z_f1)
    fu.prisma(box(-Lo, -Lo, Lo, Lo), z_f0, z_f1)
    esquina = lambda sx_, sy_: box(min(sx_ * (Li - 16), sx_ * Li + sx_ * 0.01), min(sy_ * (Li - 16), sy_ * Li + sy_ * 0.01), max(sx_ * (Li - 16), sx_ * Li + sx_ * 0.01), max(sy_ * (Li - 16), sy_ * Li + sy_ * 0.01))
    z_pie = d['z_cuerpo_arriba'] + 0.6                              # los pies de las esquinas bajan hasta casi tocar el cuerpo
    for sx_, sy_ in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
        fu.prisma(esquina(sx_, sy_).difference(disco(d['bisel_r_ext'] + p['bisel_ala'] + 2.0, n=240)), z_pie, z_f0 + 0.01)
    for sg in (1, -1):
        fu.cil((sg * c_im, sg * c_im, z_pie - 0.01), (sg * c_im, sg * c_im, z_pie + 1.8), 2.6, '-')
    fu.prisma(box(-1.6, -Li - 1.0, 1.6, -Li + 0.01), d['z_base'] - 1, z_f0, '-')       # canal del indice
    fu.prisma(llave_f, d['z_cuerpo_arriba'] - 1.5, z_pie + 0.01)                        # taco largo: la llave de la funda
    fu.cil((0, 0, z_f0 - 0.01), (0, 0, z_f0 + 0.4), 13.0, '-')                         # rebaje para la etiqueta NFC de 25 mm
    fr_json = json.load(open(os.path.join(AQUI, 'historico', 'frase-v3.json'), encoding='utf-8'))
    esc_f = 118.0 / fr_json['ancho_mm']
    fr_geo = unary_union([Polygon(q['outer'], q.get('holes', [])).buffer(0) for q in fr_json['poligonos']])
    bx0, by0, bx1, by1 = fr_geo.bounds
    fr_geo = escala(strans(fr_geo, -(bx0 + bx1) / 2, -(by0 + by1) / 2), xfact=esc_f, yfact=esc_f, origin=(0, 0)).simplify(0.03)
    fu.prisma(fr_geo, z_f1 - 0.6, z_f1 + 0.01, '-')
    fra = nueva('frase', color='azul', mueve='funda', nota='Incrustada en el techo de la funda, 0,6 mm (tres capas). Mismo fichero que la funda, otro color')
    fra.prisma(fr_geo, z_f1 - 0.6, z_f1)
    d2['funda_lado'] = 2 * Lo; d2['funda_alto'] = z_f1 - d['z_base']; d2['frase_ancho'] = 118.0

    # ============ PIEZAS SOLO PARA LA PROBETA DE LAS PUERTAS (no van en la caja) ============
    an = nueva('probeta_anillo', mueve='probeta', nota='Hace de rueda central en la probeta: tapa las puntas de los pasadores')
    an.prisma(corona(R_c + hf, R_c + hf + 6.0), -6.0, 0.0)
    an.prisma(corona(r_reb + hf, R_c + hf + 0.01), z_reb, 0.0)
    for a in ang_llave:
        an.prisma(llave(a).intersection(disco(R_c + hf + 0.3, n=240)), zm0 + 0.0, 0.0)
    tp = nueva('probeta_teton', mueve='probeta', nota='El teton con un pomo, para mover el aro con el dedo')
    tp.cil((0, Rt0, z_ranura_ala + 0.3), (0, Rt0, z_a1 + 0.61), p['teton_d'] / 2)
    tp.cil((0, Rt0, z_a1 + 0.6), (0, Rt0, z_a1 + 6.5), 5.0)      # el pomo queda por debajo de la meseta y del anillo

    # limpieza de operaciones vacias
    for q in P.values():
        q.ops = [o for o in q.ops if not (o['t'] in ('prisma', 'helice') and (not o['pol'] or abs(o.get('c1', 1) - o.get('c0', 0)) < 1e-9))]
    return p, d, d2, P

def gira_ops(ops, ang):
    """Las mismas operaciones, giradas 'ang' grados alrededor del eje Z. Solo vale para 180 grados si hay prismas en X o en Y."""
    assert abs(ang - 180.0) < 1e-9
    out = []
    for o in ops:
        o = json.loads(json.dumps(o))
        if o['t'] == 'prisma' and o['eje'] in ('x', 'y'):
            o['c0'], o['c1'] = -o['c1'], -o['c0']
            for q in o['pol']:
                q[0] = [[-x, z] for x, z in q[0]]; q[1] = [[[-x, z] for x, z in h] for h in q[1]]
        elif o['t'] in ('prisma', 'helice'):
            for q in o['pol']:
                q[0] = [[-x, -y] for x, y in q[0]]; q[1] = [[[-x, -y] for x, y in h] for h in q[1]]
        elif o['t'] == 'cil':
            o['a'] = [-o['a'][0], -o['a'][1], o['a'][2]]; o['b'] = [-o['b'][0], -o['b'][1], o['b'][2]]
        elif o['t'] == 'esfera':
            o['c'] = [-o['c'][0], -o['c'][1], o['c'][2]]
        elif o['t'] == 'cono':
            o['a'] = [-o['a'][0], -o['a'][1], o['a'][2]]; o['b'] = [-o['b'][0], -o['b'][1], o['b'][2]]
        elif o['t'] == 'revol':
            o['a0'] += 180.0; o['a1'] += 180.0
        out.append(o)
    return out

# ---------------------------------------------------------------- construccion en 3D con manifold3d
def solido(ops):
    import manifold3d as mf
    def seccion(pol_):
        cont = []
        for outer, holes in pol_:
            cont.append(outer)
            cont += holes
        return mf.CrossSection(cont, mf.FillRule.EvenOdd)
    cuerpo = None
    for o in ops:
        if o['t'] == 'prisma':
            h = o['c1'] - o['c0']
            s = seccion(o['pol']).extrude(h)
            if o['eje'] == 'z':
                s = s.translate([0, 0, o['c0']])
            elif o['eje'] == 'y':                                   # puntos (x, z): se levanta y se tumba
                s = s.rotate([90, 0, 0]).translate([0, o['c1'], 0])
            else:                                                   # 'x': puntos (y, z)
                s = s.rotate([90, 0, 0]).rotate([0, 0, 90]).translate([o['c0'], 0, 0])
        elif o['t'] == 'cil':
            a, b = np.array(o['a']), np.array(o['b']); v = b - a; L = float(np.linalg.norm(v))
            s = mf.Manifold.cylinder(L, o['r'], o['r'], 48)
            ez = v / L
            if abs(ez[2]) < 0.999:
                ex = np.cross([0, 0, 1], ez); ex /= np.linalg.norm(ex); ey = np.cross(ez, ex)
                M = np.column_stack([ex, ey, ez, a])
            else:
                M = np.column_stack([[1, 0, 0], [0, 1 if ez[2] > 0 else -1, 0], [0, 0, 1 if ez[2] > 0 else -1], a])
            s = s.transform(M)
        elif o['t'] == 'cono':
            a, b = np.array(o['a']), np.array(o['b']); v = b - a; L = float(np.linalg.norm(v))
            s = mf.Manifold.cylinder(L, o['ra'], o['rb'], 48)
            ez = v / L
            ex = np.cross([0, 0, 1], ez) if abs(ez[2]) < 0.999 else np.array([1.0, 0, 0]); ex /= np.linalg.norm(ex); ey = np.cross(ez, ex)
            s = s.transform(np.column_stack([ex, ey, ez, a]))
        elif o['t'] == 'revol':
            ang = o['a1'] - o['a0']
            s = mf.CrossSection([o['perfil']], mf.FillRule.EvenOdd).revolve(max(8, int(ang / 1.5)), ang).rotate([0, 0, o['a0']])
        elif o['t'] == 'esfera':
            s = mf.Manifold.sphere(o['r'], 48).translate(o['c'])
        elif o['t'] == 'helice':
            h = o['z1'] - o['z0']
            s = seccion(o['pol']).extrude(h, max(8, int(abs(o['giro']) / 1.5)), o['giro']).translate([0, 0, o['z0']])
        cuerpo = s if cuerpo is None else (cuerpo + s if o['op'] == '+' else cuerpo - s)
    return cuerpo

def mover(S, nombre, mueve, p, d, tau):
    """El solido de una pieza, colocado para un giro de tubo 'tau'."""
    import manifold3d as mf
    s, psi, ang, h = D.movimiento(p, d, tau)
    if mueve in ('fijo', 'funda', 'probeta'): return S
    if mueve == 'tubo': return S.rotate([0, 0, ROT * tau])
    if mueve == 'bisel': return S.rotate([0, 0, ROT * tau / d['relacion']])
    if mueve == 'plataforma': return S.translate([0, 0, h])
    if mueve.startswith('pestillo'):                              # sube con la plataforma; en los ultimos 3 mm la columna le deja salir 2,7
        a = math.radians(float(mueve.split(':')[1])); q = min(2.7, max(0.0, h - d['recorrido'] + PESTILLO_LIBRE + 3.2))
        return S.translate([q * math.cos(a), q * math.sin(a), h])
    if mueve == 'aro': return S.rotate([0, 0, p['aro_sentido'] * psi])
    if mueve == 'teton': return S.translate([0, -s, 0])
    if mueve in ('puerta_derecha', 'puerta_izquierda'):
        sx = 1 if mueve == 'puerta_derecha' else -1
        return S.translate([-sx * d['eje_x'], 0, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z']])
    if mueve.startswith('satelite'):
        th = float(mueve.split(':')[1]); c = pol(d['r_ejes'], th)
        dth = ROT * tau
        return S.translate([-c[0], -c[1], 0]).rotate([0, 0, dth * p['z_central'] / p['z_satelite']]).translate([c[0], c[1], 0]).rotate([0, 0, dth])
    raise ValueError(mueve)

def comprueba(paso=2.0, escribe=True):
    """Mueve la caja de tope a tope y mira que piezas se pisan y cuanto se acerca el reloj a cada cosa."""
    import time
    p, d, d2, P = piezas()
    S = {n: solido(q.ops) for n, q in P.items()}
    nombres = [n for n in P if P[n].mueve not in ('funda', 'probeta')]             # la funda solo esta puesta con la caja cerrada: se mira aparte
    out = []; ok_total = True
    def linea(ok, txt):
        nonlocal ok_total
        ok_total = ok_total and ok
        out.append(('  bien  ' if ok else '  FALLA ') + txt)
    grupo = lambda n: P[n].mueve
    taus = [paso * i for i in range(int(p['giro_tubo'] / paso) + 1)]
    if taus[-1] < p['giro_tubo']: taus.append(p['giro_tubo'])
    peor = {}; cerca = {}
    def caja(m):
        b = m.bounding_box(); return b
    def solapan(a, b, e=0.0):
        return all(a[i] - e < b[i + 3] and b[i] - e < a[i + 3] for i in range(3))
    t0 = time.time()
    for it, tau in enumerate(taus):
        M = {n: mover(S[n], n, P[n].mueve, p, d, tau) for n in nombres}
        B = {n: caja(M[n]) for n in nombres}
        for i, a in enumerate(nombres):
            for b in nombres[i + 1:]:
                if grupo(a) == grupo(b) and it > 0: continue          # se mueven juntas: basta mirarlas una vez
                if not solapan(B[a], B[b]): continue
                v = (M[a] ^ M[b]).volume()
                if v > peor.get((a, b), (0.0, 0.0))[0]: peor[(a, b)] = (v, tau)
        for b in ('puerta_derecha', 'puerta_izquierda', 'meseta', 'marco', 'rueda_central', 'aro_puertas'):
            for a in ('reloj_de_pega', 'soporte'):
                if solapan(B[a], B[b], 6.0):
                    g = M[a].min_gap(M[b], 6.0)
                    if g < cerca.get((a, b), (9e9, 0))[0]: cerca[(a, b)] = (g, tau)
    dt = time.time() - t0
    out.append('  nota  %d posiciones, de %.0f en %.0f grados de tubo; %.0f s' % (len(taus), paso, paso, dt))
    malos = sorted(((v, tau, a, b) for (a, b), (v, tau) in peor.items() if v > 0.02), reverse=True)
    linea(not malos, 'en todo el recorrido ninguna pieza pisa a otra (pares que se pisan mas de 0,02 mm3: %d)' % len(malos))
    for v, tau, a, b in malos:
        out.append('        %s y %s: %.2f mm3 con el tubo a %.0f grados' % (a, b, v, tau))
    for (a, b), (g, tau) in sorted(cerca.items(), key=lambda kv: kv[1][0]):
        linea(g >= p['reloj_margen'] - 1e-6, '%s y %s: lo mas cerca, %.2f mm (tubo a %.0f grados)' % (a, b, g, tau))
    # ---- que el mecanismo esta de verdad enganchado: se fuerza una pieza y tiene que chocar con la que la sujeta
    def puesta(n, tau): return mover(S[n], n, P[n].mueve, p, d, tau)
    def puerta(sx, ang):
        n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
        return S[n].translate([-sx * d['eje_x'], 0, -d['eje_z']]).rotate([0, sx * ang, 0]).translate([sx * d['eje_x'], 0, d['eje_z']])
    def choca(a, b): return (a ^ b).volume()
    G = p['giro_tubo']
    def juego(sx, desde, signo, contra):                           # cuantos grados se deja mover la puerta antes de tocar lo que la sujeta
        for i in range(1, 41):
            dl = 0.25 * i
            if sum(choca(puerta(sx, desde + signo * dl), c) for c in contra) > 0.02: return dl
        return 99.0
    a0, aG = puesta('aro_puertas', 0), puesta('aro_puertas', G); TH = p['puerta_abierta']
    j1 = max(juego(1, 0.0, 1, [a0]), juego(-1, 0.0, 1, [a0]))
    linea(j1 <= 5.0, 'cerradas y bloqueadas: con el aro quieto, una puerta solo se deja levantar %.2f grados (%.1f mm en la punta) antes de chocar con su pista' % (j1, math.radians(j1) * (d['eje_x'] - p['junta'] / 2)))
    j2 = max(juego(1, TH, -1, [aG]), juego(-1, TH, -1, [aG]))
    j3 = max(juego(1, TH, 1, [aG, S['meseta']]), juego(-1, TH, 1, [aG, S['meseta']]))
    linea(j2 <= 5.0 and j3 <= 5.0, 'abiertas y bloqueadas: una puerta abierta solo se deja mover %.2f grados hacia dentro y %.2f hacia fuera (queda entre %.1f y %.1f grados)' % (j2, j3, TH - j2, TH + j3))
    def de_pie(sx, h_):                                            # la puerta de pie (90 grados), h_ mm por encima de su sitio
        n = 'puerta_derecha' if sx > 0 else 'puerta_izquierda'
        return S[n].translate([-sx * d['eje_x'], 0, -d['eje_z']]).rotate([0, sx * TH, 0]).translate([sx * d['eje_x'], 0, d['eje_z'] + h_])
    v1 = max(choca(de_pie(sx, 0.5 * i), S['meseta']) + choca(de_pie(sx, 0.5 * i), aG) + choca(de_pie(sx, 0.5 * i), S['marco']) + choca(de_pie(sx, 0.5 * i), puesta('puerta_izquierda' if sx > 0 else 'puerta_derecha', G))
             for sx in (1, -1) for i in range(1, 41))
    linea(v1 < 0.02, 'montaje: cada puerta entra de pie, desde arriba, con el aro en abierto, sin pisar la meseta, el aro, el marco ni la otra puerta (lo que mas, %.3f mm3)' % v1)
    tm = (p['giro_muerto'] + p['giro_puertas_fin']) / 2
    v1 = min(choca(puesta('teton', tm).translate([0, e, 0]), puesta('plato', tm)) for e in (1.2, -1.2))
    v2 = min(choca(puesta('aro_puertas', tm).rotate([0, 0, e]), puesta('teton', tm)) for e in (2.0, -2.0))
    v3 = min(choca(puesta('teton', tm).translate([e, 0, 0]), S['marco']) for e in (1.2, -1.2))
    linea(min(v1, v2, v3) > 0.3, 'el teton va guiado por las tres ranuras: moverlo 1,2 mm fuera de la espiral, o de lado, o girar el aro 2 grados sin el, hace chocar (%.1f, %.1f y %.1f mm3)' % (v1, v3, v2))
    v1 = min(choca(puesta('plataforma', 200).translate([0, 0, e]), puesta('tubo', 200)) for e in (1.2, -1.2))
    v2 = min(choca(puesta('plataforma', 200).rotate([0, 0, e]), S['base']) for e in (2.0, -2.0))
    def baja(tau, dz=-0.3):
        return choca(puesta('plataforma', tau).translate([0, 0, dz]), puesta('tubo', tau)) + choca(puesta('plataforma', tau).translate([0, 0, dz]), S['base'])
    b1 = min(baja(t_) for t_ in (0.0, 30.0, 60.0, 76.0, 84.0, 90.0)); b2 = min(baja(t_, -0.6) for t_ in (96.0, 150.0, 250.0, 334.0, 340.0, G))
    linea(b1 > 0.5 and b2 > 0.5, 'la plataforma no se puede hundir: abajo, bajarla 0,3 mm choca con su asiento de la base (%.1f mm3); de ahi arriba, bajarla 0,6 mm choca con la rampa (%.1f mm3)' % (b1, b2))
    linea(v1 > 0.3 and v2 > 0.3, 'la plataforma va guiada: subirla o bajarla 1,2 mm sin girar el tubo choca con las ranuras (%.1f mm3), y girarla 2 grados choca con las columnas (%.1f mm3)' % (v1, v2))
    c = pol(d['r_ejes'], 270.0); sat = S['satelite_1'].translate([-c[0], -c[1], 0]).rotate([0, 0, 180.0 / p['z_satelite']]).translate([c[0], c[1], 0])
    v1 = choca(sat, S['rueda_central']); v2 = choca(sat, S['bisel'])
    linea(v1 > 0.5 and v2 > 0.5, 'los dientes engranan: girar un satelite medio diente lo mete en la rueda central (%.1f mm3) y en el bisel (%.1f mm3)' % (v1, v2))
    v1 = choca(S['tubo'].rotate([0, 0, ROT * -2.0]), S['base']); v2 = choca(S['tubo'].rotate([0, 0, ROT * (G + 2.0)]), S['base'])
    linea(v1 > 0.5 and v2 > 0.5, 'topes: 2 grados mas alla de cerrado o de abierto, la oreja del tubo choca con el tope de la base (%.1f y %.1f mm3)' % (v1, v2))
    # boca abajo: cada pieza, 1,5 mm hacia arriba, tiene que chocar con algo
    sujeta = [('puerta_derecha', ['pasador_derecho']), ('meseta', ['rueda_central']), ('rueda_central', ['bisel']),
              ('pasador_derecho', ['meseta', 'marco']), ('aro_puertas', ['meseta']), ('teton', ['plato']), ('plato', ['rueda_central', 'bisel']), ('tubo', ['plato']),
              ('satelite_1', ['rueda_central', 'bisel']), ('bisel', ['cuerpo']), ('plataforma', ['tubo']), ('marco', ['base', 'pasador_derecho']), ('cuerpo', ['base'])]
    sueltas = []
    for n, por in sujeta:
        v = sum(choca(S[n].translate([0, 0, 1.5]), S[q]) for q in por)
        if v < 0.2: sueltas.append(n)
    linea(not sueltas, 'boca abajo: cada pieza, al subirla 1,5 mm, choca con la que la sujeta. Sin sujetar todavia en el modelo: %s' % (', '.join(sueltas) if sueltas else 'ninguna'))
    v1 = min(choca(S['pasador_derecho'].translate([0, sg * 1.5, 0]), S['rueda_central']) for sg in (1, -1))
    linea(v1 > 0.2, 'los pasadores no se pueden salir: moverlos 1,5 mm a lo largo, hacia delante o hacia atras, choca con la rueda central (%.1f mm3)' % v1)
    def flota(grupo_, contra):                                     # cuanto sube un grupo de piezas, boca abajo, hasta que algo lo para
        for i in range(1, 41):
            if sum(choca(S[a].translate([0, 0, 0.1 * i]), S[b]) for a in grupo_ for b in contra) > 0.05: return 0.1 * (i - 1)
        return 99.0
    fijo_ = ['marco', 'meseta', 'pasador_derecho', 'pasador_izquierdo', 'puerta_derecha', 'puerta_izquierda']
    f1 = flota(['bisel'], ['cuerpo']); f2 = flota(['rueda_central'], ['bisel']); f3 = flota(fijo_, ['rueda_central', 'aro_puertas']); f4 = flota(['tubo', 'plato'], ['bisel', 'rueda_central'])
    linea(max(f1, f1 + f2, f1 + f2 + f3, f1 + f4) <= 1.5, 'boca abajo, lo que se descuelga cada cosa hasta que la para la siguiente: bisel %.1f mm; rueda central %.1f mas; puertas, meseta y marco %.1f mas; tubo y plato %.1f sobre el bisel' % (f1, f2, f3, f4))
    v1 = sum(choca(S['funda'], S[n]) + choca(S['frase'], S[n]) for n in nombres); g1 = min(S['funda'].min_gap(S[n], 3.0) for n in ('bisel', 'cuerpo', 'base', 'puerta_derecha'))
    linea(v1 < 0.02 and g1 > 0.2, 'la funda, puesta con la caja cerrada, no pisa nada (%.2f mm3) y lo mas cerca que queda de la caja son %.2f mm' % (v1, g1))
    # D-34: el soporte, sujeto con la caja cerrada y libre arriba del todo
    sop0 = S['soporte'] + S['reloj_de_pega']; resto0 = [puesta(n, 0) for n in nombres if n not in ('soporte', 'reloj_de_pega')]
    def tope(v):                                                   # cuanto se deja mover el soporte con el reloj, cerrada, hasta chocar con algo
        for i in range(1, 61):
            if sum(choca(sop0.translate([v[0] * 0.1 * i, v[1] * 0.1 * i, v[2] * 0.1 * i]), r_) for r_ in resto0) > 0.05: return 0.1 * (i - 1)
        return 6.0
    mv = {k: tope(v) for k, v in (('arriba', (0, 0, 1)), ('abajo', (0, 0, -1)), ('derecha', (1, 0, 0)), ('izquierda', (-1, 0, 0)), ('delante', (0, -1, 0)), ('detras', (0, 1, 0)))}
    linea(max(mv.values()) <= 1.0, 'cerrada, el soporte con el reloj no se mueve mas de 1 mm en ninguna direccion: ' + '; '.join('%s %.1f' % kv for kv in mv.items()))
    sopG = puesta('soporte', G) + puesta('reloj_de_pega', G); restoG = [puesta(n, G) for n in nombres if n not in ('soporte', 'reloj_de_pega')]
    v1 = max(sum(choca(sopG.translate([0, 0, 0.5 * i]), r_) for r_ in restoG) for i in range(1, 81))
    linea(v1 < 0.05, 'abierta del todo, el soporte con el reloj sale tirando hacia arriba 40 mm sin pisar nada (lo que mas, %.3f mm3)' % v1)
    v1 = choca(S['soporte'].rotate([0, 0, 180]), S['plataforma'])
    linea(v1 > 1.0, 'el soporte girado media vuelta no entra en el cajeado: pisa %.1f mm3' % v1)
    v1 = choca(S['pestillo_derecho'].translate([1.5, 0, 0]), S['base']); v2 = choca(S['pestillo_derecho'].translate([0, 0, 1.5]), S['plataforma']); v3 = choca(S['pestillo_derecho'].translate([0, 1.2, 0]), S['plataforma'])
    linea(min(v1, v2, v3) > 0.5, 'los pestillos van guiados: cerrada, sacarlos 1,5 mm choca con la columna (%.1f mm3); levantarlos, con la cola de milano del disco (%.1f); de lado, con su canal (%.1f)' % (v1, v2, v3))
    def mete(n, sg):                                               # sin soporte: cuanto se deja meter un pestillo hacia el cajeado vacio
        for i in range(1, 41):
            if choca(S[n].translate([-sg * 0.05 * i, 0, 0]), S['plataforma']) > 0.05: return 0.05 * (i - 1)
        return 2.0
    m1, m2 = mete('pestillo_derecho', 1), mete('pestillo_izquierdo', -1)
    v1 = max(choca(puesta(n, t), puesta(m_, t)) for t in (0.0, 200.0, G) for n in ('pestillo_derecho', 'pestillo_izquierdo') for m_ in ('plataforma', 'base', 'tubo'))
    linea(max(m1, m2) <= 0.5 and v1 < 0.05, 'sin el soporte puesto, los pestillos no se meten en el cajeado vacio: hacen tope en el disco a %.2f y %.2f mm; y cerrada, a media altura y arriba no pisan nada (%.3f mm3)' % (m1, m2, v1))
    def tau_de(hq):                                                # giro del tubo con la plataforma a hq mm de su final
        return p['giro_arriba'] - hq * (p['giro_arriba'] - p['giro_sube']) / d['recorrido']
    def sale(hq):                                                  # el soporte con el reloj, tirando hacia arriba 40 mm: lo que mas pisa
        t = tau_de(hq); sp = puesta('soporte', t) + puesta('reloj_de_pega', t); rs = [puesta(n, t) for n in nombres if n not in ('soporte', 'reloj_de_pega')]
        return max(sum(choca(sp.translate([0, 0, 0.5 * i]), r_) for r_ in rs) for i in range(1, 81))
    def cogido(hq):                                                # cuanto se deja levantar
        t = tau_de(hq); sp = puesta('soporte', t) + puesta('reloj_de_pega', t); rs = [puesta(n, t) for n in ('pestillo_derecho', 'pestillo_izquierdo')]
        for i in range(1, 41):
            if sum(choca(sp.translate([0, 0, 0.1 * i]), r_) for r_ in rs) > 0.05: return 0.1 * (i - 1)
        return 4.0
    s1, s2, c1, c2 = sale(5.0), sale(PESTILLO_LIBRE), cogido(PESTILLO_LIBRE + 4.0), cogido(d['recorrido'] / 2)
    linea(max(s1, s2) < 0.05 and max(c1, c2) <= 1.0, 'el soporte queda libre en los ultimos %.0f mm de subida y sujeto por debajo: a 5 y a %.0f mm del final sale sin pisar nada (%.3f y %.3f mm3); a %.0f mm del final y a media altura solo se deja levantar %.1f y %.1f mm' % (PESTILLO_LIBRE, PESTILLO_LIBRE, s1, s2, PESTILLO_LIBRE + 4.0, c1, c2))
    def metido(n, t):                                              # el pestillo, en el tramo libre, sin salir (puede estar de las dos maneras)
        s_, psi_, ang_, h_ = D.movimiento(p, d, t); return S[n].translate([0, 0, h_])
    v1 = max(choca(metido(n, tau_de(hq)), puesta(m_, tau_de(hq))) for hq in (0.0, 5.0, 10.0, PESTILLO_LIBRE) for n in ('pestillo_derecho', 'pestillo_izquierdo') for m_ in ('plataforma', 'base', 'tubo', 'soporte'))
    linea(v1 < 0.05, 'en el tramo libre los pestillos pueden estar metidos o salidos: metidos tampoco pisan nada (%.3f mm3)' % v1)
    planos = {n: S[n].bounding_box()[5] for n in ('puerta_derecha', 'puerta_izquierda', 'meseta', 'rueda_central', 'bisel')}
    zp_arriba = puesta('plataforma', G).bounding_box()[5]
    zp_arriba = puesta('plataforma', G).bounding_box()[5]
    linea(max(abs(v) for v in planos.values()) < 1e-6 and abs(zp_arriba + p['puerta_grueso']) < 1e-6, 'a ras: la cara de arriba de las puertas, la meseta, la placa de la rueda central y el bisel estan en Z = 0. Arriba, el pedestal queda a ras del asiento de las puertas: en Z = %.2f' % zp_arriba)
    return out, ok_total, S, P, p, d

if __name__ == '__main__':
    p, d, d2, P = piezas()
    S = {n: solido(q.ops) for n, q in P.items()}
    for n, q in P.items():
        bb = S[n].bounding_box()
        print('%-18s %-10s ops %3d  vol %9.1f mm3  caja %6.1f x %6.1f x %6.1f  z %7.2f..%7.2f  trozos %d' % (n, q.mueve.split(':')[0][:10], len(q.ops), S[n].volume(), bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2], bb[2], bb[5], len(S[n].decompose())))
    mov = [[round(v, 5) for v in D.movimiento(p, d, float(t_))] for t_ in range(int(p['giro_tubo']) + 1)]
    cte = {'ROT': ROT, 'giro_tubo': p['giro_tubo'], 'relacion': d['relacion'], 'eje_x': d['eje_x'], 'eje_z': d['eje_z'], 'r_ejes': d['r_ejes'], 'z_central': p['z_central'], 'z_satelite': p['z_satelite'],
           'aro_sentido': p['aro_sentido'], 'reloj_margen': p['reloj_margen'], 'bola_y': d['bola_y'], 'recorrido': d['recorrido'], 'pestillo_libre': PESTILLO_LIBRE}
    json.dump({'d2': d2, 'mov': mov, 'cte': cte, 'P': [list(q) for q in D.P_DEF], 'D': {k: v for k, v in d.items() if isinstance(v, (int, float))}, 'piezas': {n: {'color': q.color, 'mueve': q.mueve, 'nota': q.nota, 'ops': q.ops, 'volumen': S[n].volume()} for n, q in P.items()}}, open(os.path.join(AQUI, 'caja-v5-piezas.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    out, ok, *_ = comprueba(float(os.environ.get('PASO', '2')))
    for l in out: print(l)
    # las comprobaciones de la fase 1 (caja_diseno_v5.py) se repiten aqui: con otras medidas del reloj, las dos tienen que dar bien
    f1 = D.comprueba(escribe=False)
    mal1 = [l for l in f1['comprobaciones'] if 'FALLA' in l]
    print('  %s fase 1 (medidas y movimiento), repetida con estas mismas medidas: %d comprobaciones con fallo' % ('bien ' if f1['todo_bien'] else 'FALLA', len(mal1)))
    for l in mal1: print('      ' + l.strip())
    print('TODO BIEN' if ok and f1['todo_bien'] else 'HAY FALLOS')
