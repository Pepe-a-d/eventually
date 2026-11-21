# Eventually, caja v5. Probeta 1: el iris. Diseno en plano y comprobaciones (BRIEF-v5.md, apartado 11).
#
# Este programa NO necesita Fusion. Hace tres cosas:
#   1. A partir de la lista de parametros P_DEF calcula la forma de cada pieza, capa a capa.
#   2. Comprueba, grado a grado, que el iris abre, cierra, cabe y no choca.
#   3. Escribe iris-v5.json, que es lo que lee generador_iris_v5.py dentro de Fusion.
# Para cambiar una medida: se cambia aqui, en P_DEF, se ejecuta y despues se ejecuta el generador en Fusion.
#
# Necesita Python 3 con numpy, scipy y shapely:   python3 iris_diseno_v5.py
#
# Como es el iris (de abajo arriba):
#   - BASE: plato de abajo con la pared. En la pared hay un alveolo por lamina y, dentro, una isla con un
#     poste. La isla esta donde no pasa nunca ninguna otra lamina.
#   - LAMINAS: cada una tiene un agujero en la cola, que entra en su poste, y un teton hacia arriba.
#     Hay tres juegos: A de 1,2 mm, B de 0,8 y C de 0,4. En B y C la cola se engorda hasta 1,2 para que
#     ajuste igual entre la isla y el aro, y el teton se alarga lo mismo. En C, ademas, el teton nace de un refuerzo.
#     Se apilan en escalera: la raiz de cada una va ARRIBA, sobre las dos anteriores, y la punta ABAJO.
#   - ARO: va encima de las laminas, apoyado en los postes. Tiene una ranura por teton y una orejeta que
#     sale por un hueco de la pared. Los extremos de ese hueco son los topes de abierto y cerrado.
#   - TAPA: plato de arriba. Entra por arriba y se gira (bayoneta) hasta el tope. Sin pegamento ni tornillos.
#
# Ejes: X e Y en el plano del iris, con el centro del hueco en (0, 0); Z hacia arriba, la mesa en Z = 0.
# Angulos en grados, positivos en sentido contrario a las agujas del reloj visto desde arriba.
# La lamina 0 tiene su cola en el eje +X. Giro de lamina 0 = abierto; al cerrar gira en sentido positivo.
import json, math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))

# (nombre, unidad, valor, de donde sale / para que sirve)
P_DEF = [
    ('laminas',          '',    8,     'DECIDIDO (D-23): numero de laminas'),
    ('hueco_d',          'mm',  75.0,  'ESTIMADO en el brief: hueco libre con el iris abierto. Las medidas del reloj son supuestas'),
    ('agujero_d',        'mm',  5.0,   'Objetivo de agujero central con el iris cerrado (el brief pide 8 o menos)'),
    ('lamina_grosor',    'mm',  1.2,   'Grosor de la lamina del juego A (el brief pide 1,2 o mas)'),
    ('lamina_grosor_b',  'mm',  0.8,   'DECIDIDO (D-23): grosor del juego B, para comparar el tacto'),
    ('lamina_grosor_c',  'mm',  0.4,   'DECIDIDO (D-28): grosor del juego C, dos capas. La revision del Mac calcula que es el unico que cierra del todo'),
    ('refuerzo_r',       'mm',  3.0,   'Juego C: radio del refuerzo que rodea al teton, para que no nazca de una hoja de dos capas'),
    ('lamina_retiro',    'mm',  0.6,   'Lo que la lamina abierta queda escondida detras del borde del hueco'),
    ('luna_ancho',       'mm',  25.0,  'Ancho maximo de la lamina. La lamina es una luna: el hueco entre dos circulos'),
    ('luna_radio',       'mm',  34.3,  'Radio del circulo que dibuja el canto exterior de la lamina'),
    ('luna_ang',         'deg', 18.0,  'Hacia donde cae la parte mas ancha de la lamina, respecto a su cola'),
    ('lamina_inicio',    'deg', -6.0,  'Donde se corta la raiz de la lamina, respecto a su cola'),
    ('canto',            'mm',  0.45,  'Rebaje del canto de arriba de la lamina, para que la de encima no se enganche'),
    ('solape',           'mm',  1.2,   'Lo minimo que cada lamina monta sobre la vecina con el iris cerrado'),
    ('eje_radio',        'mm',  61.9,  'A que distancia del centro del iris gira cada lamina (centro de su poste)'),
    ('cola_r',           'mm',  3.3,   'Radio del disco de la cola de la lamina'),
    ('cola_juego',       'mm',  0.35,  'Separacion entre la cola y la pared del alveolo'),
    ('isla_r',           'mm',  2.6,   'Radio de la isla donde apoya la cola. Menor que la cola, para que otras laminas puedan pasar por debajo de su borde'),
    ('poste_d',          'mm',  3.2,   'Diametro del poste sobre el que gira la lamina'),
    ('teton_d',          'mm',  3.0,   'Diametro del teton que arrastra el aro'),
    ('teton_alto',       'mm',  2.0,   'Alto del teton sobre la lamina de 1,2 (la de 0,8 lo lleva 0,4 mas largo)'),
    ('teton_radio',      'mm',  41.8,  'A que distancia del centro del iris esta el teton, con el iris abierto'),
    ('teton_ang',        'deg', 3.0,   'Angulo del teton respecto a la cola, con el iris abierto'),
    ('sobregiro',        'deg', 1.5,   'Grados que la lamina puede pasar de abierto, para absorber las holguras'),
    ('sobrecierre',      'deg', 0.7,   'Grados que la lamina puede pasar de cerrado, por lo mismo: con holgura la lamina va retrasada respecto al aro'),
    ('holg_mueve',       'mm',  0.2,   'SUPUESTO del brief: holgura por lado entre piezas que se mueven'),
    ('holg_eje',         'mm',  0.25,  'SUPUESTO: holgura por lado del poste en su agujero y del teton en su ranura. En P0, 0,10 sujetaba y 0,15 pasaba; aqui tiene que girar suelto'),
    ('holg_altura',      'mm',  0.2,   'Juego en altura de la cola entre la isla y el aro'),
    ('suelo',            'mm',  1.2,   'Grosor del plato de abajo'),
    ('camara',           'mm',  4.8,   'Alto libre para las laminas: cuatro gruesos de lamina'),
    ('aro_grosor',       'mm',  2.0,   'Grosor del aro'),
    ('aro_juego',        'mm',  0.2,   'Juego en altura entre el aro y la tapa'),
    ('aro_dentro',       'mm',  1.0,   'Lo que el borde interior del aro queda por fuera del hueco'),
    ('aro_holgura',      'mm',  0.25,  'Separacion entre el canto del aro y la pared'),
    ('tapa',             'mm',  1.6,   'Grosor de la tapa (plato de arriba)'),
    ('tapa_holgura',     'mm',  0.3,   'Separacion entre el canto de la tapa y la pared'),
    ('pared_juego',      'mm',  0.5,   'Separacion entre el canto de las laminas y la pared'),
    ('escalon',          'mm',  1.2,   'Ancho del escalon de la pared donde apoya la tapa'),
    ('banda',            'mm',  1.2,   'Grosor de la pared por encima del escalon y por detras de cada alveolo'),
    ('una_n',            '',    4,     'Numero de uñas de la bayoneta'),
    ('una_sale',         'mm',  0.8,   'Lo que cada uña vuela sobre la tapa (en rampa de 45 grados, sin soportes)'),
    ('una_ancho',        'deg', 14.0,  'Ancho de cada uña'),
    ('una_tope',         'deg', 2.0,   'Parte de la uña que baja hasta el escalon y hace de tope de giro de la tapa'),
    ('orejeta_largo',    'mm',  9.0,   'Lo que la orejeta del aro sale de la pared'),
    ('orejeta_ancho',    'mm',  8.0,   'Ancho de la orejeta'),
    ('paso_arco',        'deg', 1.5,   'Grados entre puntos de los arcos: finura de las curvas'),
]

def params():
    p = {n: v for n, _, v, _ in P_DEF}
    for par in os.environ.get('IRIS_PRUEBA', '').split(','):          # solo para probar valores sin tocar la lista
        if '=' in par:
            p[par.split('=')[0]] = float(par.split('=')[1])
    return p

def rot(p, ang, c=(0.0, 0.0)):
    a = math.radians(ang)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))

def pol(r, ang):
    return (r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang)))

def derivadas(p):
    d = {}
    d['RA'] = p['hueco_d'] / 2
    d['r1'] = d['RA'] + p['lamina_retiro']                 # canto interior de la lamina abierta
    d['Rt'] = p['eje_radio']
    dist = d['r1'] - p['agujero_d'] / 2                    # lo que tiene que desplazarse el centro del canto
    d['giro_lamina'] = math.degrees(2 * math.asin(dist / (2 * d['Rt'])))
    # radios de la pared
    d['R_esc'] = d['Rt'] + p['cola_r'] + p['cola_juego']   # fondo de los alveolos = borde exterior del escalon
    d['R_c'] = d['R_esc'] - p['escalon']                   # pared de la camara de las laminas
    d['R_ext'] = d['R_esc'] + p['banda']
    d['D_ext'] = 2 * d['R_ext']
    d['R_aro_in'] = d['RA'] + p['aro_dentro']
    d['R_aro_ext'] = d['R_c'] - p['aro_holgura']
    # alturas, desde la mesa
    d['z_suelo'] = p['suelo']
    d['z_techo'] = p['suelo'] + p['camara']                # cara de arriba de los postes = cara de abajo del aro
    d['z_isla'] = d['z_techo'] - p['lamina_grosor'] - p['holg_altura']
    d['z_aro1'] = d['z_techo'] + p['aro_grosor']
    d['z_tapa0'] = d['z_aro1'] + p['aro_juego']
    d['z_total'] = d['z_tapa0'] + p['tapa']
    return d

def eje(d):
    return (d['Rt'], 0.0)

def teton(p):
    return pol(p['teton_radio'], p['teton_ang'])

def angulo_aro(p, d, giro):
    """Cuanto ha girado el aro (grados) cuando la lamina ha girado 'giro'. La ranura del aro es radial y sigue al teton."""
    t0 = teton(p)
    t1 = rot(t0, giro, eje(d))
    return math.degrees(math.atan2(t1[1], t1[0]) - math.atan2(t0[1], t0[0]))

# ---------------------------------------------------------------------------------------------------
# A partir de aqui hace falta numpy, scipy y shapely.
def comprueba(escribe=True):
    import numpy as np
    from shapely.geometry import Polygon, Point, LineString, box
    from shapely.affinity import rotate as srot
    from shapely.ops import unary_union
    from scipy.optimize import linprog

    p = params(); d = derivadas(p)
    N = int(p['laminas']); paso_n = 360.0 / N
    RA, r1, Rt, rho = d['RA'], d['r1'], d['Rt'], p['cola_r']
    R_c, R_esc, R_ext = d['R_c'], d['R_esc'], d['R_ext']
    E = eje(d); cierre = d['giro_lamina']; sobre = p['sobregiro']; cierre_tope = cierre + p['sobrecierre']
    QS = max(8, int(round(90.0 / p['paso_arco'])))
    def disco(r, c=(0.0, 0.0), qs=None):
        return Point(c).buffer(r, qs or (QS if r > 12 else 16))
    def sector(ra, rb, a0, a1):
        n = max(2, int(abs(a1 - a0) / 0.5) + 1)
        angs = [a0 + (a1 - a0) * i / n for i in range(n + 1)]
        return Polygon([pol(rb, a) for a in angs] + [pol(ra, a) for a in reversed(angs)])
    def partes(g):
        return [q for q in (list(g.geoms) if hasattr(g, 'geoms') else [g]) if q.geom_type == 'Polygon' and q.area > 1e-4]
    def limpia(g, r=0.3):
        """Quita laminillas mas finas que 2r."""
        return g.buffer(-r).buffer(r)
    out = []; ok_total = True
    def linea(ok, txt):
        nonlocal ok_total
        ok_total = ok_total and ok
        out.append(('  bien  ' if ok else '  FALLA ') + txt)
    def nota(txt):
        out.append('  nota  ' + txt)

    # ---------------- la lamina (abierta, numero 0, cola en +X)
    ec = p['luna_ancho'] + r1 - p['luna_radio']
    luna = disco(p['luna_radio'], pol(ec, p['luna_ang']), 120).difference(disco(r1, qs=160))
    a0 = p['lamina_inicio']
    cuna = Polygon([(0, 0)] + [pol(300, a) for a in np.arange(a0, a0 + 181, 3)])
    cuerpo = luna.intersection(cuna)
    if cuerpo.geom_type != 'Polygon': cuerpo = max(cuerpo.geoms, key=lambda g: g.area)
    cola = disco(rho, E, 24)
    cerca = cuerpo.intersection(disco(rho + 6, E, 24))
    cuello = unary_union([cola, cerca]).convex_hull.intersection(disco(rho + 6, E, 24))
    lam0 = unary_union([cuerpo, cola, cuello]).buffer(0)
    lam0 = lam0.buffer(-0.5).buffer(0.5).buffer(0.5).buffer(-0.5)        # esquinas redondeadas a 0,5
    lam0 = unary_union([lam0, cola]).simplify(0.004)
    assert lam0.geom_type == 'Polygon', 'la cola no toca la lamina'
    tet0 = teton(p)
    def gira(g, giro, k=0):
        return srot(srot(g, giro, origin=E), paso_n * k, origin=(0, 0))
    def lam(k, giro):
        return gira(lam0, giro, k)
    pasos = [cierre * i / round(cierre) for i in range(int(round(cierre)) + 1)]         # de abierto a cerrado, grado a grado
    pasos_ext = [-sobre - 0.5] + [-sobre] + pasos + [cierre_tope, cierre_tope + 0.5]     # con los sobregiros y un margen
    barr0 = unary_union([gira(lam0, g) for g in np.linspace(pasos_ext[0], pasos_ext[-1], 50)])
    otras = unary_union([srot(barr0, paso_n * k, origin=(0, 0)) for k in range(1, N)])

    # 1. abierto: nada asoma al hueco
    rmin = min(math.hypot(x, y) for x, y in lam0.exterior.coords)
    linea(rmin >= RA + 0.3, 'abierto, las laminas quedan %.2f mm por detras del borde del hueco de %.0f mm' % (rmin - RA, 2 * RA))

    # 2. cerrado: cubre todo menos el agujero central, con solape
    cer = [lam(k, cierre) for k in range(N)]
    libre = disco(RA + 0.2, qs=180).difference(unary_union(cer))
    trozos = [g for g in partes(libre) if g.area > 0.02]
    centro = [g for g in trozos if g.contains(Point(0, 0))]
    agujero = 2 * Point(0, 0).distance(centro[0].exterior) if centro else 0.0
    linea(len(trozos) <= 1 and agujero <= 8.0, 'cerrado, agujero central de %.1f mm y %d rendijas mas' % (agujero, len(trozos) - (1 if centro else 0)))
    enc = unary_union([b.buffer(-p['solape'] / 2) for b in cer])
    zona = disco(RA + 0.2, qs=180).difference(disco(agujero / 2 + p['solape'] + 0.6))
    falta = zona.difference(enc).area
    linea(falta < 0.3, 'cerrado, cada lamina monta al menos %.1f mm sobre la vecina (sin cubrir asi: %.2f mm2)' % (p['solape'], falta))

    cer_t = [lam(k, cierre_tope) for k in range(N)]
    libre_t = [g for g in partes(disco(RA, qs=180).difference(unary_union(cer_t))) if g.contains(Point(0, 0))]
    agujero_tope = 2 * Point(0, 0).distance(libre_t[0].exterior) if libre_t else 0.0

    # 3. pared, alveolos e islas
    rmax = max(math.hypot(x, y) for x, y in barr0.exterior.coords)
    linea(rmax <= Rt + rho + 0.02, 'en todo el giro la lamina no sale mas alla de su cola (llega a %.2f mm del centro; el fondo del alveolo esta a %.2f)' % (rmax, R_esc))
    # Las formas que se repiten de una capa a otra (el canto exterior, el fondo de los alveolos, el hueco de la
    # orejeta) salen siempre del MISMO poligono, punto por punto. Si no, al unir las capas en Fusion quedan
    # caras casi coincidentes y la union falla.
    D_big = disco(R_ext + 0.5)                                               # se recorta a R_ext con un cilindro de verdad
    D_esc = disco(R_esc)
    alv_bruto = unary_union([barr0.buffer(p['pared_juego']), disco(rho + p['cola_juego'], E, 24)])
    vacio = unary_union([disco(R_c)] + [srot(alv_bruto, paso_n * k, origin=(0, 0)) for k in range(N)])
    vacio = vacio.buffer(0.3).buffer(-0.3).simplify(0.002).intersection(D_esc)   # sin paredes mas finas que 0,6
    pared = D_big.difference(vacio)
    alv0 = min(partes(vacio.difference(disco(R_c + 0.02))), key=lambda g: g.distance(Point(E)))
    angs = [math.degrees(math.atan2(y, x)) for x, y in alv0.exterior.coords]
    alv_a0, alv_a1 = min(angs), max(angs)
    libre_ang = paso_n - (alv_a1 - alv_a0)
    linea(libre_ang >= 8, 'cada alveolo ocupa de %.1f a %.1f grados; entre dos alveolos quedan %.1f grados de pared gruesa (%.1f mm)' % (alv_a0, alv_a1, libre_ang, math.radians(libre_ang) * R_c))
    ri = p['isla_r']
    isla0 = unary_union([disco(ri, E, 24), box(Rt, -(ri - 0.4), R_esc + 0.3, ri - 0.4)])
    sin_cola = lam0.difference(disco(rho + 0.01, E, 24))
    barr_sin = unary_union([gira(sin_cola, g) for g in np.linspace(pasos_ext[0], pasos_ext[-1], 50)])
    isla0 = unary_union([disco(ri, E, 24), isla0.difference(barr_sin.buffer(0.3))])
    isla0 = max(partes(limpia(isla0, 0.25)), key=lambda g: g.area).simplify(0.002)
    dist_isla = isla0.distance(otras)
    linea(dist_isla >= 0.3, 'ninguna otra lamina toca la isla en todo el giro (la mas cercana pasa a %.2f mm)' % dist_isla)
    islas = unary_union([srot(isla0, paso_n * k, origin=(0, 0)) for k in range(N)])
    choque_pared = barr0.buffer(0.3).intersection(pared).area
    linea(choque_pared < 0.01, 'las laminas pasan a 0,3 mm o mas de la pared en todo el giro (pisado: %.2f mm2)' % choque_pared)

    # 4. grado a grado: opuestas, teton y apilado
    opuestas = 0.0; teton_min = 1e9
    op = N // 2 if N % 2 == 0 else None
    for g in pasos_ext:
        L = [lam(k, g) for k in range(N)]
        if op: opuestas = max(opuestas, L[0].intersection(L[op]).area)
        tp = Point(rot(tet0, g, E))
        for k in range(1, (N - 1) // 2 + 1): teton_min = min(teton_min, tp.distance(L[k]))
    if op: linea(opuestas < 0.05, 'laminas opuestas: se pisan %.2f mm2 como mucho (tiene que ser cero para poder apilarlas)' % opuestas)
    linea(teton_min >= p['teton_d'] / 2 + 0.8, 'el teton de cada lamina queda siempre a %.1f mm o mas de las laminas que van encima' % teton_min)
    dentro = lam0.buffer(-(p['canto'] + 0.6)).contains(disco(p['teton_d'] / 2, tet0, 12))
    linea(dentro, 'el teton cae dentro de su lamina con 0,6 mm o mas de margen')
    ref_dentro = lam0.buffer(-0.3).contains(disco(p['refuerzo_r'], tet0, 24))
    linea(ref_dentro and teton_min - p['refuerzo_r'] >= 0.8, 'juego C: el refuerzo del teton cabe dentro de la lamina y queda a %.1f mm o mas de las laminas que van encima' % (teton_min - p['refuerzo_r']))

    def apila(t, refuerzo=False):
        """Laminas rigidas e inclinadas dentro de la camara. Devuelve, por giro, cuanto se pisarian
        (lo que tienen que ceder flexando) y el plano de la lamina 0: z = a x + b y + c, desde el suelo de la camara."""
        res_g = []
        H = p['camara']; zp = H - p['lamina_grosor'] - p['holg_altura']
        for g in pasos:
            L = [lam(k, g) for k in range(N)]
            A = []; B = []
            def zc(k, x, y):
                xr, yr = rot((x, y), -paso_n * k)
                return [xr, yr, 1.0]
            def muestra(poly, n=50):
                pts = []
                for q in partes(poly):
                    if q.area < 0.05: continue
                    cs = list(q.exterior.coords)
                    pts += cs[::max(1, len(cs) // n)]
                    pts.append(q.representative_point().coords[0])
                return pts
            for k in range(1, N):
                if op and k == op: continue
                inter = L[0].intersection(L[k])
                if inter.is_empty or inter.area < 0.05: continue
                arriba_k = k <= (N - 1) // 2
                for (x, y) in muestra(inter):
                    zk = zc(k, x, y); z0 = zc(0, x, y)
                    dif = [zk[i] - z0[i] for i in range(3)] if arriba_k else [z0[i] - zk[i] for i in range(3)]
                    A.append([-dif[0], -dif[1], -dif[2], -1.0]); B.append(-t)             # dif >= t - cede
            for (x, y) in list(L[0].exterior.coords)[::2]:
                z0 = zc(0, x, y); r = math.hypot(x, y)
                suelo_z = 0.0 if r >= RA else -p['suelo']
                techo_z = H if r >= d['R_aro_in'] else H + p['aro_grosor'] + p['aro_juego'] + p['tapa']
                A.append([-z0[0], -z0[1], -z0[2], -1.0]); B.append(-(suelo_z + t / 2))
                A.append([z0[0], z0[1], z0[2], -1.0]); B.append(techo_z - t / 2)
            for th in range(0, 360, 30):                           # la cola: entera entre la isla y el aro, aunque cabecee
                xi, yi = E[0] + p['isla_r'] * math.cos(math.radians(th)), E[1] + p['isla_r'] * math.sin(math.radians(th))
                xc, yc = E[0] + rho * math.cos(math.radians(th)), E[1] + rho * math.sin(math.radians(th))
                A.append([-xi, -yi, -1.0, 0.0]); B.append(-(zp + t / 2))                       # por debajo, apoya en la isla
                A.append([xc, yc, 1.0, 0.0]); B.append(H - p['lamina_grosor'] + t / 2)         # por arriba, el aro
            if refuerzo:                                           # el refuerzo del teton tampoco puede tocar el aro
                tp = rot(tet0, g, E)
                for th in range(0, 360, 45):
                    A.append([tp[0] + p['refuerzo_r'] * math.cos(math.radians(th)), tp[1] + p['refuerzo_r'] * math.sin(math.radians(th)), 1.0, 0.0]); B.append(H - p['lamina_grosor'] + t / 2)
            r_ = linprog([0, 0, 0, 1], A_ub=A, b_ub=B, bounds=[(None, None)] * 3 + [(0, 40)], method='highs')
            res_g.append((float(g), float(r_.x[3]) if r_.status == 0 else None, [float(v) for v in r_.x[:3]] if r_.status == 0 else None))
        return res_g
    planos = {}
    largo_lam = max(math.hypot(x - E[0], y - E[1]) for x, y in lam0.exterior.coords)
    juegos = (('A', p['lamina_grosor']), ('B', p['lamina_grosor_b']), ('C', p['lamina_grosor_c']))
    for nombre, t in juegos:
        rg = apila(t, nombre == 'C')
        malos = [round(g, 1) for g, c, _ in rg if c is None]
        cede = max((c for _, c, _ in rg if c is not None), default=float('nan'))
        cede0 = rg[0][1]; medio = rg[len(rg) // 2][1]
        # Ojo: en la primera version aqui se calculaba una fuerza (11 gramos por lamina de 1,2) tratando la lamina como
        # una regla que se dobla por la punta. Estaba mal: lo que hace falta es que la punta se retuerza (revision
        # de la sesion del Mac, reporte-v5/contra-reporte-iris.md). Aqui solo se da la geometria, que es lo seguro.
        linea(not malos and cede <= t, 'apilado, juego %s (%.1f mm): colocadas rigidas, las laminas se pisarian %.2f mm abiertas, %.2f a medio giro y %.2f cerradas. Eso lo tiene que ceder la punta retorciendose. SE CONFIRMA IMPRIMIENDO' % (nombre, t, cede0, medio, cede))
        planos[nombre] = rg
        d['cede_' + nombre] = cede

    # 5. aro: giro, ranuras, orejeta
    a_nominal = angulo_aro(p, d, cierre); a_cierre = angulo_aro(p, d, cierre_tope); a_abre = angulo_aro(p, d, -sobre)
    s = 1.0 if a_cierre > 0 else -1.0                                       # sentido en que gira el aro para cerrar
    a_min, a_max = min(a_cierre, a_abre), max(a_cierre, a_abre)
    radios = [math.hypot(*rot(tet0, g, E)) for g in pasos_ext]
    linea(a_max - a_min <= 60, 'el aro gira %.1f grados de tope a tope (el brief pide 60 o menos): %.1f de abierto a cerrado, mas %.1f de sobregiro al abrir y %.1f al cerrar; el teton va de %.1f a %.1f mm de radio' % (a_max - a_min, abs(a_nominal), abs(a_abre), abs(a_cierre - a_nominal), min(radios), max(radios)))
    peor = 0
    for g in pasos_ext:
        tp = rot(tet0, g, E)
        v = (-(tp[1] - E[1]), tp[0] - E[0]); tg = (-tp[1], tp[0])
        cosang = abs(v[0] * tg[0] + v[1] * tg[1]) / (math.hypot(*v) * math.hypot(*tg))
        peor = max(peor, math.degrees(math.acos(min(1, cosang))))
    linea(peor <= 45, 'la ranura del aro empuja al teton con %.0f grados de sesgo como mucho (por debajo de 45 no se acuña)' % peor)
    r_ran0 = min(radios) - 0.3; r_ran1 = max(radios) + 0.3                   # centros de los extremos de la ranura
    w_ran = p['teton_d'] / 2 + p['holg_eje']
    th0 = math.degrees(math.atan2(tet0[1], tet0[0]))
    ranura0 = LineString([pol(r_ran0, th0), pol(r_ran1, th0)]).buffer(w_ran, 12)
    ranuras = unary_union([srot(ranura0, paso_n * k, origin=(0, 0)) for k in range(N)])
    linea(r_ran0 - w_ran - d['R_aro_in'] >= 0.8 and d['R_aro_ext'] - (r_ran1 + w_ran) >= 3.0, 'la ranura del aro va de %.1f a %.1f mm de radio; el aro, de %.1f a %.1f' % (r_ran0 - w_ran, r_ran1 + w_ran, d['R_aro_in'], d['R_aro_ext']))
    linea(d['R_aro_ext'] >= Rt + 0.8, 'el aro apoya en los %d postes: cubre %.1f mm de los %.1f de cada uno' % (N, min(p['poste_d'], d['R_aro_ext'] - (Rt - p['poste_d'] / 2)), p['poste_d']))
    # orejeta y hueco de la pared: centrados en el tramo de pared gruesa entre el alveolo 0 y el 1
    beta = math.degrees(math.asin(p['orejeta_ancho'] / 2 / R_ext))
    dlt = math.degrees(0.1 / R_ext)
    c_libre = (alv_a1 + paso_n + alv_a0) / 2
    phi0 = c_libre - (a_min + a_max) / 2                                     # angulo de la orejeta con el iris abierto
    hueco_a0 = phi0 + a_min - beta - dlt; hueco_a1 = phi0 + a_max + beta + dlt
    margen = (libre_ang - (hueco_a1 - hueco_a0)) / 2
    hueco = sector(R_c - 0.6, R_ext + 2.0, hueco_a0, hueco_a1)
    orejeta0 = sector(R_c - 2.0, R_ext + p['orejeta_largo'], phi0 - beta, phi0 + beta)
    linea(margen >= 1.0, 'el hueco de la orejeta va de %.1f a %.1f grados; a cada lado quedan %.1f grados de pared gruesa que hacen de tope (%.1f mm)' % (hueco_a0, hueco_a1, margen, math.radians(margen) * R_c))
    aro_lleno = unary_union([disco(d['R_aro_ext']).difference(ranuras), orejeta0])       # el agujero central se hace con un cilindro de verdad
    aro0 = aro_lleno.difference(disco(d['R_aro_in']))

    # 6. bayoneta de la tapa
    n_u = int(p['una_n']); semi = p['una_ancho'] / 2; tope = p['una_tope']
    u_cent = [c_libre + paso_n * (1 + 2 * j) for j in range(n_u)] if N == 2 * n_u else [c_libre + 360.0 / n_u * (j + 0.5) for j in range(n_u)]
    giro_tapa = p['una_ancho'] - tope + 1.0                                  # grados que se gira la tapa para cerrarla
    esc = [0.2, 0.4, 0.6, 0.8]                                              # rampa de 45 grados en capas de 0,2
    z0t = d['z_tapa0']
    capas_una = []                                                          # (z0, z1, vuelo)
    for i, v in enumerate(esc):
        v = min(v, p['una_sale'])
        z_a = z0t + 0.2 * (i + 1); z_b = z0t + 0.2 * (i + 2) if i < len(esc) - 1 else d['z_total']
        capas_una.append((z_a, z_b, v))
    def unas(v):
        return unary_union([sector(R_esc - v, R_esc + 0.3, c - semi, c + semi) for c in u_cent])
    topes = unary_union([sector(R_esc - p['una_sale'], R_esc + 0.3, c + s * (semi - tope), c + s * semi) if s > 0 else sector(R_esc - p['una_sale'], R_esc + 0.3, c - semi, c - semi + tope) for c in u_cent])
    # la tapa, en su posicion cerrada: los rebajes quedan girados respecto a las uñas
    th0 = p['tapa_holgura']
    rebajes_metida = unary_union([sector(R_esc - th0 - 0.8, R_esc + 1.0, c - semi - 1.0, c + semi + 1.0) for c in u_cent])
    rebajes = srot(rebajes_metida, s * giro_tapa, origin=(0, 0))
    capas_tapa = []                                                         # (z0, z1, forma) en posicion cerrada
    th = p['tapa_holgura']
    for i in range(4):
        capas_tapa.append((z0t + 0.2 * i, z0t + 0.2 * (i + 1), disco(R_esc - th - 0.2 * i).difference(rebajes)))
    capas_tapa.append((z0t + 0.8, d['z_total'], disco(R_esc - th - 0.8)))
    tapa_llena = list(capas_tapa)
    capas_tapa = [(a, b, g.difference(disco(RA))) for a, b, g in capas_tapa]

    # ---------------- las piezas, capa a capa (en su sitio, montadas, con el iris abierto)
    z_h = d['z_techo'] - 0.2                                                # el hueco de la orejeta empieza 0,2 por debajo del aro
    muro = unary_union([pared])
    base_capas = [
        (0.0, d['z_suelo'], D_big),
        (d['z_suelo'], d['z_isla'], unary_union([muro, islas])),
        (d['z_isla'], z_h, muro),
        (z_h, d['z_tapa0'], muro.difference(hueco)),
    ]
    banda = D_big.difference(D_esc)
    base_capas.append((d['z_tapa0'], d['z_tapa0'] + 0.2, unary_union([banda, topes]).difference(hueco)))
    for z_a, z_b, v in capas_una:
        base_capas.append((z_a, z_b, unary_union([banda, unas(v), topes]).difference(hueco)))
    postes = [[rot(E, paso_n * k)[0], rot(E, paso_n * k)[1], d['z_isla'], d['z_techo'], p['poste_d'] / 2, 'suma'] for k in range(N)]
    aro_capas = [(d['z_techo'], d['z_aro1'], aro0)]
    aro_lleno_capas = [(d['z_techo'], d['z_aro1'], aro_lleno)]

    def lamina_capas(t, juego):
        c = p['canto']
        if juego == 'A':
            cap = [(0.0, t - 0.4, lam0), (t - 0.4, t - 0.2, lam0.buffer(-0.2)), (t - 0.2, t, lam0.buffer(-c))]
            alto = p['teton_alto']
        elif juego == 'B':
            cap = [(0.0, t - 0.2, lam0), (t - 0.2, t, lam0.buffer(-0.25)), (t, p['lamina_grosor'], disco(rho - 0.2, E, 24))]
            alto = p['teton_alto'] + (p['lamina_grosor'] - t)
        else:                                                               # C: dos capas, cola y refuerzo del teton hasta 1,2
            cap = [(0.0, t - 0.2, lam0), (t - 0.2, t, lam0.buffer(-0.2)),
                   (t, p['lamina_grosor'], unary_union([disco(rho - 0.2, E, 24), disco(p['refuerzo_r'], tet0, 24)]))]
            alto = p['teton_alto'] + (p['lamina_grosor'] - t)
        nace = p['lamina_grosor'] if juego == 'C' else t                     # altura de la que nace el teton
        cil = [[E[0], E[1], -0.1, p['lamina_grosor'] + 0.1, p['poste_d'] / 2 + p['holg_eje'], 'resta'],
               [tet0[0], tet0[1], nace - 0.05, t + alto, p['teton_d'] / 2, 'suma']]
        return cap, cil, alto

    # 7. choques entre piezas, capa contra capa
    def choque(capas_a, capas_b):
        peor = 0.0
        for a0_, a1_, ga in capas_a:
            for b0_, b1_, gb in capas_b:
                if min(a1_, b1_) - max(a0_, b0_) > 1e-6:
                    peor = max(peor, ga.intersection(gb).area)
        return peor
    base_real = [(a, b, g.intersection(disco(R_ext)).difference(disco(RA))) for a, b, g in base_capas]
    ch_aro = max(choque(base_real, [(a, b, srot(g, ang, origin=(0, 0))) for a, b, g in aro_capas]) for ang in np.linspace(a_min, a_max, 25))
    linea(ch_aro < 0.01, 'el aro no toca la base en todo su giro (pisado: %.3f mm2)' % ch_aro)
    ch_tapa = max(choque(base_real, [(a, b, srot(g, -s * ang, origin=(0, 0))) for a, b, g in capas_tapa]) for ang in np.linspace(0, giro_tapa - 0.15, 27))
    linea(ch_tapa < 0.01, 'la tapa entra y gira %.0f grados hasta el tope sin tocar las uñas (pisado: %.3f mm2)' % (giro_tapa, ch_tapa))
    ch_mas = choque(base_real, [(a, b, srot(g, s * 1.0, origin=(0, 0))) for a, b, g in capas_tapa])
    linea(ch_mas > 0.05, 'el tope de la bayoneta para la tapa (si girase 1 grado mas chocaria %.2f mm2)' % ch_mas)
    borde = capas_tapa[0][2]; labio = unas(p['una_sale'])
    pisa = borde.intersection(labio).area
    linea(pisa > 4 * n_u, 'cerrada, cada uña monta %.1f mm sobre el borde de la tapa a lo largo de %.0f mm' % (p['una_sale'] - th, pisa / n_u / (p['una_sale'] - th)))
    apoyo = borde.intersection(disco(R_esc).difference(disco(R_c))).intersection(muro.buffer(0.01))
    frac = apoyo.area / (math.pi * (R_esc ** 2 - R_c ** 2))
    linea(frac >= 0.3, 'la tapa apoya en el escalon de la pared en el %.0f %% de la vuelta' % (100 * frac))
    topes_apoyo = topes.difference(hueco).difference(muro.buffer(0.01)).area
    linea(topes_apoyo < 0.05, 'los topes de las uñas nacen sobre pared maciza (en el aire: %.2f mm2)' % topes_apoyo)
    # laminas contra la base: por debajo de la isla solo cuenta la pared; a la altura de la cola, pared sin alveolos
    ch_lam = barr0.buffer(0.2).intersection(muro).area
    linea(ch_lam < 0.01, 'las laminas no tocan la pared ni otra isla (pisado: %.3f mm2)' % ch_lam)
    # teton: no puede tocar la tapa aunque la lamina suba hasta el aro, y tiene que seguir dentro del aro si baja
    for nombre, t in juegos:
        _, _, alto = lamina_capas(t, nombre)
        punta_alta = d['z_techo'] - (p['lamina_grosor'] - t) + alto            # con la cola pegada al aro
        punta_baja = d['z_isla'] + t + alto                                     # con la cola apoyada en la isla
        cae = math.hypot(tet0[0] - E[0], tet0[1] - E[1]) * p['holg_altura'] / (p['isla_r'] + rho)     # lo que baja el teton si la lamina cabecea todo lo que le deja su juego
        linea(punta_alta <= d['z_tapa0'] - 0.05 and punta_baja - cae - d['z_techo'] >= 0.9, 'teton del juego %s: mide %.1f mm; entra en el aro entre %.1f y %.1f mm de los %.1f del aro, y nunca toca la tapa' % (nombre, alto, punta_baja - cae - d['z_techo'], min(p['aro_grosor'], punta_alta - d['z_techo']), p['aro_grosor']))
    # holgura acumulada en la punta de la lamina
    brazo_t = math.hypot(tet0[0] - E[0], tet0[1] - E[1])
    baile = 2 * p['holg_eje'] * largo_lam / brazo_t
    nota('holguras: el poste y el teton tienen %.2f mm de juego por lado; en la punta de la lamina eso son hasta %.1f mm de retraso. Por eso los topes dejan pasar %.1f grados de lamina al abrir y %.1f al cerrar. Agujero cerrado previsto: entre %.1f mm (sin holgura) y %.1f mm (con toda la holgura)' % (p['holg_eje'], baile, sobre, p['sobrecierre'], agujero_tope, agujero_tope + 2 * baile))
    linea(d['z_total'] <= 10.0, 'grueso total %.2f mm (el brief pide 10 o menos)' % d['z_total'])
    linea(d['D_ext'] <= 130.0, 'diametro exterior %.1f mm (el objetivo del brief es 130 o menos)' % d['D_ext'])

    # ---------------- salida
    def geo(g):
        return [[[[round(x, 4), round(y, 4)] for x, y in list(q.exterior.coords)[:-1]], [[[round(x, 4), round(y, 4)] for x, y in list(h.coords)[:-1]] for h in q.interiors]] for q in partes(g)]
    def capas_json(capas):
        return [[round(a, 4), round(b, 4), geo(g)] for a, b, g in capas]
    piezas = {
        'base': {'capas': capas_json(base_capas), 'cilindros': postes, 'dentro_r': R_ext, 'agujero_r': RA, 'z': 0.0, 'ang': 0.0},
        'aro': {'capas': capas_json([(a - d['z_techo'], b - d['z_techo'], g) for a, b, g in aro_lleno_capas]), 'cilindros': [], 'agujero_r': d['R_aro_in'], 'z': d['z_techo'], 'ang': 0.0},
        'tapa': {'capas': capas_json([(a - z0t, b - z0t, g) for a, b, g in tapa_llena]), 'cilindros': [], 'agujero_r': RA, 'z': z0t, 'ang': 0.0},
    }
    for nombre, t in juegos:
        cap, cil, alto = lamina_capas(t, nombre)
        piezas['lamina_' + nombre] = {'capas': capas_json(cap), 'cilindros': cil, 'z': d['z_isla'], 'ang': 0.0, 'copias': N, 'grosor': t, 'teton_alto': alto}
    def vol(capas, dentro=None, agujero=None):
        v = 0.0
        for a, b, g in capas:
            if dentro: g = g.intersection(disco(dentro, qs=180))
            if agujero: g = g.difference(disco(agujero, qs=180))
            v += g.area * (b - a)
        return v
    piezas['base']['volumen'] = vol(base_capas, R_ext, RA) + N * math.pi * (p['poste_d'] / 2) ** 2 * (d['z_techo'] - d['z_isla'])
    piezas['aro']['volumen'] = vol(aro_capas, None, d['R_aro_in'])
    piezas['tapa']['volumen'] = vol(capas_tapa, None, RA)
    for nombre, t in juegos:
        cap, cil, alto = lamina_capas(t, nombre)
        nace = p['lamina_grosor'] if nombre == 'C' else t
        piezas['lamina_' + nombre]['volumen'] = vol(cap) - math.pi * (p['poste_d'] / 2 + p['holg_eje']) ** 2 * p['lamina_grosor'] + math.pi * (p['teton_d'] / 2) ** 2 * (t + alto - nace)
    caja = lam0.minimum_rotated_rectangle
    cx = list(caja.exterior.coords)
    lados = [(math.hypot(cx[i + 1][0] - cx[i][0], cx[i + 1][1] - cx[i][1]), math.degrees(math.atan2(cx[i + 1][1] - cx[i][1], cx[i + 1][0] - cx[i][0]))) for i in range(2)]
    ang_cama = -max(lados)[1]                                               # el lado largo, a lo largo de X
    tumbada = srot(lam0, ang_cama, origin=(0, 0))
    bx0, by0, bx1, by1 = tumbada.bounds
    cama = [[ang_cama, (i % 2) * (bx1 - bx0 + 3.0) - bx0, (i // 2) * (by1 - by0 + 3.0) - by0] for i in range(N)]
    d['cama_laminas'] = [2 * (bx1 - bx0) + 3.0, math.ceil(N / 2) * (by1 - by0 + 3.0) - 3.0]
    datos = {
        'P_DEF': [[n, u, v, c] for n, u, v, c in P_DEF], 'd': d, 'piezas': piezas,
        'lamina': [[round(x, 4), round(y, 4)] for x, y in list(lam0.exterior.coords)[:-1]], 'eje': list(E), 'teton': list(tet0),
        'isla': geo(isla0), 'alveolo': geo(alv0), 'pared': geo(pared.intersection(disco(R_ext))), 'aro': geo(aro0), 'hueco': geo(hueco),
        'tapa_borde': geo(capas_tapa[0][2]), 'unas': geo(unas(p['una_sale'])), 'topes': geo(topes),
        'giro_lamina': cierre, 'giro_aro': a_cierre, 'giro_aro_abre': a_abre, 'sentido': s, 'giro_tapa': giro_tapa,
        'orejeta_ang': phi0, 'ranura': [r_ran0 - w_ran, r_ran1 + w_ran, 2 * w_ran],
        'agujero_cerrado': agujero, 'agujero_tope': agujero_tope, 'planos': planos, 'baile_punta': baile, 'cama': cama, 'giro_aro_nominal': a_nominal,
        'comprobaciones': out, 'todo_bien': ok_total,
    }
    if escribe:
        json.dump(datos, open(os.path.join(AQUI, 'iris-v5.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return datos

if __name__ == '__main__':
    datos = comprueba()
    d = datos['d']
    print('Iris v5: %d laminas, hueco %.0f mm' % (params()['laminas'], params()['hueco_d']))
    print('  diametro exterior %.1f mm, grueso %.2f mm, la lamina gira %.1f grados y el aro %.1f' % (d['D_ext'], d['z_total'], datos['giro_lamina'], abs(datos['giro_aro'])))
    for l in datos['comprobaciones']: print(l)
    print('TODO BIEN, salvo el diametro' if all(('FALLA' not in l) or ('diametro exterior' in l) for l in datos['comprobaciones']) and not datos['todo_bien'] else ('TODO BIEN' if datos['todo_bien'] else 'HAY FALLOS'))
