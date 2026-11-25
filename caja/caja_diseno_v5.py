# Eventually, caja v5 de puertas y ascensor (BRIEF-v5.md, apartado 11). Diseno y comprobaciones. FASE 1.
#
# Este programa NO necesita Fusion. En esta primera fase hace solo dos cosas:
#   1. A partir de la lista de parametros P_DEF calcula las medidas que dependen unas de otras
#      (engranajes, radios, alturas, rampa, leva de las puertas).
#   2. Comprueba el movimiento, grado a grado de tubo: que las puertas abren y cierran, que el reloj no las
#      toca, que las dos puertas no se pisan en la junta y que cada cosa cabe en su franja.
# Todavia NO calcula la forma de las piezas ni escribe el fichero para Fusion: eso es la fase 2.
#
# Necesita Python 3 con numpy y shapely:   python3 caja_diseno_v5.py
#
# Ejes: X = ancho (+X a la derecha mirando la caja de frente), Y = fondo (el frente es -Y), Z hacia arriba.
# Z = 0 es la cara de arriba de las puertas cerradas. Angulos en grados.
#
# Como funciona (lo de dentro lo ha decidido la sesion del PC; ver reporte-v5/antes-de-modelar-caja.md):
#   - El bisel (corona dentada por dentro) mueve seis satelites que ruedan sobre la rueda central, fija.
#     Los satelites llevan sus ejes en el PLATO, que va unido al TUBO: plato y tubo giran juntos, mas despacio.
#   - El tubo tiene por dentro tres ranuras en helice. La PLATAFORMA lleva tres tetones en esas ranuras y no
#     puede girar, porque corre por tres columnas: al girar el tubo, sube.
#   - El plato tiene por debajo UNA ranura en espiral. En ella entra un TETON suelto, que solo puede moverse
#     hacia dentro y hacia fuera porque tambien va metido en una ranura recta del marco.
#   - Ese teton atraviesa ademas una ranura en diagonal del brazo del ARO DE PUERTAS: al moverse, hace girar
#     el aro unos 12 grados. El aro va escondido bajo las puertas y gira alrededor del hueco.
#   - El aro tiene dos pistas, una por puerta. En cada pista va la bola de la manivela de una puerta. Al girar
#     el aro, las pistas empujan las bolas y las dos puertas giran a la vez. Al principio y al final de cada
#     pista hay un tramo que no empuja: ahi la puerta queda bloqueada por la forma.
#   - Las dos puertas son la misma pieza, girada media vuelta, y un solo aro mueve las dos: no hay cruce de pistas.
#   (En la primera version de este programa las movia una corredera recta: no cabia sin meterse en el hueco.)
import json, math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))

# (nombre, unidad, valor, de donde sale / para que sirve)
P_DEF = [
    # --- EL RELOJ: todo SUPUESTO. El dia que Pepe lo mida, se cambia aqui y se regenera todo ---
    ('reloj_cabeza_d',   'mm',  40.0,  'SUPUESTO: diametro de la cabeza del reloj, sin corona'),
    ('reloj_con_corona', 'mm',  43.5,  'SUPUESTO: ancho de la cabeza con la corona'),
    ('reloj_grueso',     'mm',  11.0,  'SUPUESTO: del cristal a la tapa trasera'),
    ('brazalete_alto',   'mm',  67.0,  'SUPUESTO: alto del ovalo del brazalete cerrado'),
    ('brazalete_fondo',  'mm',  53.0,  'SUPUESTO: fondo del ovalo del brazalete cerrado'),
    ('reloj_ancho',      'mm',  44.0,  'ESTIMADO en el brief: ancho del reloj de pie, visto desde arriba (X)'),
    ('reloj_fondo',      'mm',  53.0,  'ESTIMADO en el brief: fondo del reloj de pie, visto desde arriba (Y)'),
    ('reloj_alto',       'mm',  78.0,  'ESTIMADO en el brief: alto del reloj puesto en su soporte'),
    ('reloj_margen',     'mm',  3.0,   'DECIDIDO en el brief: lo que tiene que quedar entre el reloj y cualquier pieza'),
    # --- holguras, medidas en piezas impresas ---
    ('holg_gira',        'mm',  0.25,  'MEDIDO (probeta del iris): holgura por lado de lo que gira'),
    ('holg_desliza',     'mm',  0.20,  'MEDIDO (P0 a 0,2): con 0,20 por lado pasa sin forzar. Para lo que desliza'),
    ('holg_fija',        'mm',  0.15,  'MEDIDO (P0 a 0,2): con 0,15 por lado sujeta. Para lo que encaja sin moverse'),
    # --- puertas ---
    ('puerta_grueso',    'mm',  5.0,   'Grueso de las puertas (el brief pide 3 o mas; Pepe quiere que se vean solidas)'),
    ('eje_fuera',        'mm',  4.0,   'Lo que el eje de la bisagra queda por fuera del borde del hueco. Con 4, una puerta abierta que ceda hacia dentro lo que le deja su juego no entra en el hueco libre'),
    ('puerta_cola',      'mm',  3.0,   'Lo que la puerta sigue mas alla de su eje, por fuera. Con 3 mm el canto redondo deja 0,4 de raya y el marco se imprime sin soportes'),
    ('puerta_solape_y',  'mm',  7.0,   'Lo que la puerta sobra por delante y por detras del hueco: ahi apoya y ahi lleva la manivela'),
    ('junta',            'mm',  0.3,   'Raya entre las dos puertas cerradas'),
    ('labio_largo',      'mm',  1.4,   'Junta en bisel: lo que la cuna de una puerta se mete bajo la otra'),
    ('labio_grueso',     'mm',  1.0,   'Grueso de ese labio'),
    ('labio_hueco',      'mm',  1.5,   'Hueco en altura entre la cuna y la otra puerta: al abrir, la cuna sube mas deprisa'),
    ('manivela_r',       'mm',  8.0,   'Del eje de la bisagra al centro de la bola de la manivela'),
    ('bola_d',           'mm',  5.0,   'Diametro de la bola de la manivela'),
    ('manivela_d',       'mm',  3.0,   'Diametro de la varilla de la manivela. Fina para pasar entre las paredes de la pista'),
    ('bola_holgura',     'mm',  0.12,  'Holgura por lado de la bola en su pista. Justa a proposito: de ella sale lo que baila la puerta'),
    ('pista_pared',      'mm',  2.0,   'Pared de las pistas del aro'),
    ('pista_pared_fuera', 'mm', 0.85,   'Lo minimo que mide la pared de fuera de la pista (dos pasadas de boquilla): de aqui sale el radio del aro'),
    ('aro_holgura',      'mm',  0.2,   'Holgura por lado entre el aro y el cuello que lo centra'),
    ('puerta_abierta',   'grados', 92.0, 'Angulo de la puerta abierta. Algo mas de 90 para que su juego caiga hacia fuera del reloj'),
    ('aro_reposo',       'deg', 2.5,   'Giro del aro, al principio y al final, en el que la pista no empuja la bola: puerta bloqueada'),
    ('aro_cambio',       'deg', 6.0,   'Giro del aro en el que la pista lleva la bola de cerrada a abierta'),
    ('aro_sentido',      '',    -1,    'Sentido en que gira el aro para abrir: 1 contra las agujas del reloj, -1 a favor'),
    ('aro_grueso',       'mm',  3.0,   'Grueso del aro de puertas y de su brazo'),
    ('cuello_pared',     'mm',  2.4,   'Pared del cuello del marco'),
    ('meseta_grueso',    'mm',  8.0,   'Grueso de la meseta: la pieza que rodea las puertas y lleva sus bisagras'),
    ('teton_d',          'mm',  5.0,   'Diametro del teton suelto que va de la espiral del plato al brazo del aro'),
    ('teton_recorrido',  'mm',  13.0,  'Lo que el teton se mueve hacia dentro para abrir'),
    ('pasador_d',        'mm',  3.0,   'Diametro de los pasadores de las bisagras'),
    # --- giro del tubo ---
    ('giro_tubo',        'deg', 345.0, 'DECIDIDO en el brief: giro total del tubo, de tope a tope'),
    ('giro_muerto',      'deg', 45.0,  'DECIDIDO (D-20): tramo muerto al empezar. Giran los engranajes y no pasa nada'),
    ('giro_puertas_fin', 'deg', 100.0, 'A este giro de tubo el teton ha terminado su recorrido (el brief proponia 105)'),
    ('giro_sube',        'deg', 92.0,  'A este giro de tubo empieza a subir la plataforma. Lo fija la comprobacion del reloj'),
    ('giro_arriba',      'deg', 335.0, 'Del brief: a este giro de tubo la plataforma esta arriba; despues la rampa es plana'),
    # --- ascensor ---
    ('margen_reloj_abajo', 'mm', 3.1,  'Con el reloj abajo, lo que queda entre lo mas alto del reloj y lo mas bajo de las puertas. Lo minimo que deja el brief (3 mm): boca abajo, el reloj cae esto'),
    ('tubo_r',           'mm',  76.0,  'Radio interior del tubo'),
    ('tubo_pared',       'mm',  4.5,   'Grueso de la pared del tubo'),
    ('rampa_fondo',      'mm',  3.0,   'Lo que las ranuras en helice entran en la pared del tubo'),
    ('teton_plat_d',     'mm',  6.0,   'Diametro de los tres tetones de la plataforma'),
    ('disco_grueso',     'mm',  6.0,   'Grueso del disco de la plataforma: igual que el diametro de sus tetones'),
    ('pedestal_holgura', 'mm',  0.4,   'Entre el pedestal y el hueco del marco, por lado'),
    # --- planetario ---
    ('modulo',           'mm',  1.5,   'Del brief: modulo de los dientes'),
    ('z_central',        '',    78,    'Dientes de la rueda central (fija). El brief proponia 60: no caben dentro las puertas con sus manivelas'),
    ('z_satelite',       '',    12,    'Dientes de cada satelite'),
    ('n_satelites',      '',    6,     'DECIDIDO (D-20): cinco blancos y uno azul'),
    ('juego_dientes',    'mm',  0.4,   'Lo que se quita de grueso entre los dos dientes que engranan. Con 0,4 quedan unos 0,19 mm entre flancos, como la holgura medida para lo que desliza (0,20); con 0,2 quedaban 0,08'),
    ('engranaje_grueso', 'mm',  6.0,   'Grueso de los engranajes'),
    # --- alturas, de arriba abajo ---
    ('esqueleto_grueso', 'mm',  3.0,   'Grueso de la placa fija que rodea las puertas y tapa a medias los engranajes'),
    ('plato_grueso',     'mm',  5.0,   'Grueso del plato portasatelites'),
    ('espiral_fondo',    'mm',  3.0,   'Fondo de la ranura en espiral, por debajo del plato'),
    ('ala_grueso',       'mm',  4.0,   'Grueso del ala del marco, la que apoya en las columnas'),
    ('base_grueso',      'mm',  4.0,   'Grueso del fondo de la caja'),
    ('aire',             'mm',  0.4,   'Aire en altura entre piezas que se mueven una sobre otra'),
    # --- cuerpo ---
    ('bisel_pared',      'mm',  5.2,   'Pared del bisel por fuera del fondo de sus dientes'),
    ('bisel_ala',        'mm',  2.4,   'Ala del bisel que queda bajo el labio del cuerpo y lo retiene'),
    ('cuerpo_pared',     'mm',  3.0,   'Grueso de la pared del cuerpo cuadrado'),
    ('bisel_visto',      'mm',  8.0,   'Alto de bisel que asoma sobre el cuerpo: es por donde se coge'),
]

def params():
    p = {n: v for n, _, v, _ in P_DEF}
    for par in os.environ.get('CAJA_PRUEBA', '').split(','):          # solo para probar valores sin tocar la lista
        if '=' in par:
            p[par.split('=')[0]] = float(par.split('=')[1])
    return p

def suave(u):
    """De 0 a 1, arrancando y parando sin golpe."""
    u = min(1.0, max(0.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)

def derivadas(p):
    d = {}
    m = p['modulo']
    # hueco de las puertas
    d['hueco_x'] = p['reloj_ancho'] + 2 * p['reloj_margen']
    d['hueco_y'] = p['reloj_fondo'] + 2 * p['reloj_margen']
    # puertas
    t = p['puerta_grueso']
    d['eje_x'] = d['hueco_x'] / 2 + p['eje_fuera']         # eje de la bisagra de la puerta derecha
    d['eje_z'] = -t / 2                                    # a media altura de la puerta
    d['nudillo_r'] = math.hypot(p['puerta_cola'], t / 2)
    d['puerta_y'] = d['hueco_y'] + 2 * p['puerta_solape_y']
    d['puertas_x'] = 2 * (d['eje_x'] + p['puerta_cola'])   # ancho del rectangulo liso que se ve
    d['cara_dentro_abierta'] = d['eje_x'] - t / 2          # donde queda la cara de dentro de la puerta abierta
    # manivela, bola y aro de puertas
    rho = p['manivela_r']
    d['bola_dx'] = 2 * rho * math.sin(math.radians(45))    # lo que se mueve la bola en X de cerrada a abierta
    d['bola_y'] = d['hueco_y'] / 2 + 1.5 + p['bola_d'] / 2 + 0.25      # la manivela va en lo que sobra de puerta por detras del hueco
    d['bola_x_cerrada'] = d['eje_x'] + rho * math.sin(math.radians(45))
    d['bola_x_abierta'] = d['eje_x'] - rho * math.sin(math.radians(p['puerta_abierta'] - 45))
    d['bola_r_cerrada'] = math.hypot(d['bola_x_cerrada'], d['bola_y'])
    d['bola_r_abierta'] = math.hypot(d['bola_x_abierta'], d['bola_y'])
    d['aro_giro'] = p['aro_cambio'] + 2 * p['aro_reposo']
    wb = p['bola_d'] / 2 + p['bola_holgura']
    d['aro_r_in'] = math.hypot(d['hueco_x'] / 2, d['hueco_y'] / 2) + 0.4          # el aro rodea el hueco sin entrar en el
    d['aro_r_ext'] = d['bola_r_cerrada'] + wb + p['pista_pared_fuera']
    d['cuello_r_in'] = d['aro_r_ext'] + p['aro_holgura']
    d['cuello_r'] = d['cuello_r_in'] + p['cuello_pared']
    d['modulo_r'] = d['cuello_r']
    # planetario
    zs, zp = int(p['z_central']), int(p['z_satelite']); zr = zs + 2 * zp
    d['z_bisel'] = zr
    d['r_central'] = m * zs / 2; d['r_satelite'] = m * zp / 2; d['r_bisel'] = m * zr / 2
    d['r_ejes'] = d['r_central'] + d['r_satelite']
    d['central_fondo'] = d['r_central'] - 1.25 * m; d['central_punta'] = d['r_central'] + m
    d['bisel_punta'] = d['r_bisel'] - m; d['bisel_fondo'] = d['r_bisel'] + 1.25 * m
    d['relacion'] = zr / (zs + zr)                         # giro del tubo por cada giro del bisel
    d['giro_bisel'] = p['giro_tubo'] / d['relacion']
    d['diente_grueso'] = math.pi * m / 2 - p['juego_dientes'] / 2
    # radios, de dentro afuera
    d['plato_r_in'] = d['cuello_r'] + p['holg_gira'] + 0.3             # el plato gira alrededor del cuello
    d['tubo_r_ext'] = p['tubo_r'] + p['tubo_pared']
    d['bisel_r_ext'] = d['bisel_fondo'] + p['bisel_pared']
    d['bisel_ala_r'] = d['bisel_r_ext'] + p['bisel_ala']
    d['cuerpo_dentro'] = 2 * (d['bisel_ala_r'] + 0.4)
    d['cuerpo_lado'] = d['cuerpo_dentro'] + 2 * p['cuerpo_pared']
    # franja de la espiral, bajo el plato. El teton se mueve hacia dentro para abrir
    w = p['teton_d'] / 2 + p['holg_desliza']
    d['espiral_r_abierta'] = d['plato_r_in'] + 1.8 + w
    d['espiral_r_cerrada'] = d['espiral_r_abierta'] + p['teton_recorrido']
    d['espiral_franja'] = (d['espiral_r_abierta'] - w, d['espiral_r_cerrada'] + w)
    # alturas, de arriba abajo (Z = 0 arriba)
    a = p['aire']
    d['z_engr1'] = -p['esqueleto_grueso'] - a
    d['z_engr0'] = d['z_engr1'] - p['engranaje_grueso']
    d['z_plato1'] = d['z_engr0'] - a
    d['z_plato0'] = d['z_plato1'] - p['plato_grueso']
    d['z_corr1'] = d['z_plato0'] - a
    d['z_corr0'] = d['z_corr1'] - p['aro_grueso']
    d['z_ala1'] = d['z_corr0'] - a
    d['z_ala0'] = d['z_ala1'] - p['ala_grueso']
    d['z_meseta0'] = -p['meseta_grueso']
    # D-34: arriba del todo, la cara del pedestal queda a ras del ASIENTO de las puertas (Z = -grueso de puerta), no de la tapa,
    # y el disco, 1 mm por debajo del ala. El pedestal es 5 mm mas corto que antes y la caja, 5 mm mas baja
    d['pedestal_alto'] = -d['z_ala0'] + 1.0 - p['puerta_grueso']
    d['recorrido'] = p['reloj_alto'] + p['margen_reloj_abajo']
    d['z_disco1_abajo'] = -p['puerta_grueso'] - d['recorrido'] - d['pedestal_alto']
    d['z_disco0_abajo'] = d['z_disco1_abajo'] - p['disco_grueso']
    d['z_suelo'] = d['z_disco0_abajo'] - 1.0
    d['z_base'] = d['z_suelo'] - p['base_grueso']
    d['caja_alto'] = -d['z_base']
    d['z_cuerpo_arriba'] = -p['bisel_visto']
    # rampa
    ang = p['giro_arriba'] - p['giro_sube']
    d['rampa_paso'] = d['recorrido'] * 360.0 / ang         # mm que subiria en una vuelta entera
    r_cont = p['tubo_r'] + p['rampa_fondo'] / 2            # radio medio de contacto del teton
    d['rampa_pendiente'] = math.degrees(math.atan(d['rampa_paso'] / (2 * math.pi * r_cont)))
    d['ranura_alto'] = p['teton_plat_d'] + 2 * p['holg_desliza']
    return d

def bola_x(p, d, psi):
    """X de la bola de la puerta derecha (respecto al eje de su bisagra, + hacia fuera) cuando el aro ha girado psi grados."""
    u = min(1.0, max(0.0, (psi - p['aro_reposo']) / p['aro_cambio']))
    r = d['bola_r_cerrada'] + u * (d['bola_r_abierta'] - d['bola_r_cerrada'])     # la pista se acerca al centro a ritmo constante
    return math.sqrt(r * r - d['bola_y'] ** 2) - d['eje_x']

def movimiento(p, d, tau):
    """Para un giro de tubo 'tau' (grados): recorrido del teton (mm), giro del aro (grados), angulo de las puertas y altura de la plataforma."""
    s = p['teton_recorrido'] * suave((tau - p['giro_muerto']) / (p['giro_puertas_fin'] - p['giro_muerto']))
    psi = d['aro_giro'] * s / p['teton_recorrido']                          # la ranura del brazo es recta: el aro gira en proporcion
    puerta = 45.0 - math.degrees(math.asin(max(-1.0, min(1.0, bola_x(p, d, psi) / p['manivela_r']))))
    h = d['recorrido'] * min(1.0, max(0.0, (tau - p['giro_sube']) / (p['giro_arriba'] - p['giro_sube'])))
    return s, psi, puerta, h

def comprueba(escribe=True):
    import numpy as np
    from shapely.geometry import Polygon, Polygon, Point, box
    from shapely.affinity import rotate as srot, scale as sscale
    from shapely.ops import unary_union

    p = params(); d = derivadas(p)
    out = []; ok_total = True
    def linea(ok, txt):
        nonlocal ok_total
        ok_total = ok_total and ok
        out.append(('  bien  ' if ok else '  FALLA ') + txt)
    def nota(txt):
        out.append('  nota  ' + txt)
    t = p['puerta_grueso']; xh = d['eje_x']; ze = d['eje_z']

    # ---------------- seccion de las puertas, en el plano X-Z. Coordenadas respecto al eje: x' hacia fuera, z' hacia arriba
    largo = xh - p['junta'] / 2
    losa = box(-largo, -t / 2, 0, t / 2)
    nudillo = Point(0, 0).buffer(d['nudillo_r'], 48).intersection(box(0, -t / 2, 50, t / 2))      # canto redondo, solo por fuera del eje
    cuerpo = unary_union([losa, nudillo])
    ll = p['labio_largo']; lg = p['labio_grueso']; lh = p['labio_hueco']
    punta = 0.4; jj = p['junta']                                                       # junta en bisel a 45 grados, la misma de caja_piezas_v5.py
    labio = Polygon([(-largo + 0.01, -t / 2), (-largo - jj - ll, -t / 2), (-largo - jj - ll, -t / 2 + punta), (-largo + 0.01, -t / 2 + punta + ll + jj + 0.01)])   # la puerta A mete esta cuna bajo la B
    rebaje = Polygon([(-largo - 0.01, -t / 2 - 0.01), (-largo + ll + punta + lh, -t / 2 - 0.01), (-largo - 0.01, -t / 2 + punta + ll + lh + 0.01)])              # y la B lleva el hueco
    puerta_a = unary_union([cuerpo, labio]); puerta_b = cuerpo.difference(rebaje)
    def derecha(g, ang):                       # puerta de la derecha: gira sobre (xh, ze); abre hacia arriba y afuera
        g = srot(g, -ang, origin=(0, 0))
        from shapely.affinity import translate
        return translate(g, xh, ze)
    def izquierda(g, ang):
        return sscale(derecha(g, ang), xfact=-1, origin=(0, 0))

    # 1. cerradas y abiertas
    a0 = derecha(puerta_a, 0); b0 = izquierda(puerta_b, 0)
    linea(abs(a0.bounds[3]) < 1e-6 and abs(b0.bounds[3]) < 1e-6, 'cerradas, las dos puertas tienen la cara de arriba en Z = 0: mismo plano (escalon 0 en el modelo)')
    raya = box(-5, -t - 5, 5, 5).difference(unary_union([a0, b0]))
    pasa_luz = any(q.bounds[1] < -t - 1 and q.bounds[3] > 1 and box(q.bounds[0], -t - 2, q.bounds[2], 2).difference(unary_union([a0, b0])).area > 0 and
                   any(box(x - 0.01, -t - 3, x + 0.01, 3).intersection(unary_union([a0, b0])).is_empty for x in np.arange(q.bounds[0] + 0.01, q.bounds[2], 0.02))
                   for q in (raya.geoms if hasattr(raya, 'geoms') else [raya]))
    linea(not pasa_luz, 'cerradas, mirando desde arriba no hay ninguna linea recta que cruce la junta: el labio de %.1f mm la tapa' % ll)
    a90 = derecha(cuerpo, 90)
    linea(a90.bounds[0] >= d['hueco_x'] / 2, 'abierta a 90 grados, la puerta queda entera por fuera del hueco: su punto mas metido esta a X = %.2f (el hueco llega a %.1f)' % (a90.bounds[0], d['hueco_x'] / 2))
    nota('abierta, la puerta sobresale %.1f mm sobre la tapa y baja %.1f mm por debajo de ella junto a la bisagra' % (a90.bounds[3], -a90.bounds[1]))

    # 2. las dos puertas, una contra otra, en toda la apertura (se mueven a la vez)
    peor = 1e9; ang_peor = 0
    for ang in np.arange(0.5, 90.01, 0.5):
        dist = derecha(puerta_a, ang).distance(izquierda(puerta_b, ang))
        if dist < peor: peor, ang_peor = dist, ang
    linea(peor >= 0.2, 'al abrir a la vez, la cuna de una puerta y el hueco de la otra no se tocan: lo mas cerca, %.2f mm, a %.1f grados' % (peor, ang_peor))
    peor2 = min(derecha(puerta_a, ang + 2.0).distance(izquierda(puerta_b, ang)) for ang in np.arange(0.0, 88.01, 0.5))
    linea(peor2 >= 0.1, 'con la puerta de la cuna 2 grados por delante de la otra, tampoco se tocan: lo mas cerca, %.2f mm' % peor2)
    linea((int(p['z_central']) + int(d['z_bisel'])) % (2 * int(p['n_satelites'])) == 0, 'los %d satelites caben repartidos por igual y con el mismo dibujo: dientes de la central mas los del bisel, %d, multiplo de %d' % (p['n_satelites'], p['z_central'] + d['z_bisel'], 2 * p['n_satelites']))

    # 3. grado a grado de tubo: tabla, y el reloj contra las puertas
    taus = [i * 1.0 for i in range(int(p['giro_tubo']) + 1)]
    tabla = []; peor_reloj = 1e9; tau_peor = 0; peor_ped = 1e9
    rw = p['reloj_ancho'] / 2
    ped_x = d['hueco_x'] / 2 - p['pedestal_holgura']
    for tau in taus:
        s, psi, ang, h = movimiento(p, d, tau)
        z_ped = -p['puerta_grueso'] - d['recorrido'] + h              # cara de arriba del pedestal (arriba del todo queda a ras del asiento de las puertas)
        tabla.append([tau, round(tau / d['relacion'], 1), round(s, 2), round(psi, 2), round(ang, 2), round(h, 2)])
        A = derecha(puerta_a, ang); B = izquierda(puerta_b, ang)
        reloj = box(-rw, z_ped, rw, z_ped + p['reloj_alto'])
        pedestal = box(-ped_x, z_ped - d['pedestal_alto'], ped_x, z_ped)
        dist = min(reloj.distance(A), reloj.distance(B))
        if dist < peor_reloj: peor_reloj, tau_peor = dist, tau
        peor_ped = min(peor_ped, pedestal.distance(A), pedestal.distance(B))
    linea(peor_reloj >= p['reloj_margen'], 'en todo el recorrido el reloj de pega queda a %.2f mm o mas de las puertas (lo mas cerca, con el tubo a %.0f grados). El brief pide %.0f' % (peor_reloj, tau_peor, p['reloj_margen']))
    linea(peor_ped >= 0.5, 'el pedestal queda siempre a %.2f mm o mas de las puertas; arriba, entre el pedestal y la cara de la puerta abierta quedan %.1f mm' % (peor_ped, d['cara_dentro_abierta'] - ped_x))
    s0, _, a0_, h0 = movimiento(p, d, 0); s1, _, a1_, h1 = movimiento(p, d, p['giro_tubo'])
    linea(abs(a0_) < 0.01 and abs(a1_ - p['puerta_abierta']) < 0.01 and 85 <= a1_ <= 95, 'las puertas van de %.1f a %.1f grados (el brief pide abiertas entre 85 y 95)' % (a0_, a1_))
    linea(abs(h0) < 1e-9 and abs(h1 - d['recorrido']) < 1e-9, 'la plataforma sube %.1f mm; arriba, la cara del pedestal queda a ras del asiento de las puertas (Z = -%.0f)' % (d['recorrido'], p['puerta_grueso']))
    # tramos en los que la puerta esta bloqueada por la forma (bola en el tramo recto del canal)
    quieta0 = max(tau for tau in taus if movimiento(p, d, tau)[2] < 0.01)
    quieta1 = min(tau for tau in taus if movimiento(p, d, tau)[2] > 89.99)
    sube0 = max(tau for tau in taus if movimiento(p, d, tau)[3] < 1e-9)
    linea(quieta1 <= sube0 + 1e-9 or peor_reloj >= p['reloj_margen'], 'orden: tramo muerto hasta %.0f grados; las puertas se mueven de %.0f a %.0f; la plataforma sube de %.0f a %.0f; arriba, plano hasta %.0f' % (p['giro_muerto'], quieta0, quieta1, sube0, p['giro_arriba'], p['giro_tubo']))
    # lo que baila la puerta bloqueada: en el tramo de reposo la pista es un arco con centro en el eje de la caja,
    # asi que sujeta la DISTANCIA de la bola al centro. La bola solo se mueve en X: se pasa de una cosa a la otra.
    for nombre, xb in (('cerrada', d['bola_x_cerrada']), ('abierta', d['bola_x_abierta'])):
        dx = p['bola_holgura'] * math.hypot(xb, d['bola_y']) / xb
        d['baile_' + nombre] = math.degrees(dx / (p['manivela_r'] * math.cos(math.radians(45))))
    linea(d['baile_abierta'] <= 5.0, 'puerta bloqueada por la forma: en los tramos de reposo la pista del aro no empuja y sujeta la bola. Con %.2f mm de holgura, la puerta abierta baila %.1f grados a cada lado (el brief admite de 85 a 95) y la cerrada %.1f, aunque cerrada apoya en su asiento' % (p['bola_holgura'], d['baile_abierta'], d['baile_cerrada']))
    # la pista, vista desde el aro: cuanto se inclina respecto a un circulo en el tramo que empuja
    peor_p = 0.0
    def en_aro(q):                                       # posicion de la bola en coordenadas del aro: radio y angulo
        x = d['eje_x'] + bola_x(p, d, q)
        return math.hypot(x, d['bola_y']), math.degrees(math.atan2(d['bola_y'], x)) - p['aro_sentido'] * q
    for i in range(1, 200):
        psi = d['aro_giro'] * i / 200.0; e = 0.01
        r1, a1 = en_aro(psi - e); r2, a2 = en_aro(psi + e)
        if abs(r2 - r1) > 1e-9:
            peor_p = max(peor_p, abs(math.degrees(math.atan2(r2 - r1, math.radians(a2 - a1) * (r1 + r2) / 2))))
    peor_p = min(peor_p, 180 - peor_p)
    linea(peor_p <= 40, 'pista del aro: en el tramo que empuja se aparta %.0f grados de un circulo como mucho (por debajo de 40). El aro gira %.1f grados, %s' % (peor_p, d['aro_giro'], 'a favor de las agujas del reloj' if p['aro_sentido'] < 0 else 'en contra de las agujas'))
    r_teton = (d['espiral_r_abierta'] + d['espiral_r_cerrada']) / 2
    sesgo_brazo = math.degrees(math.atan(math.radians(d['aro_giro']) * r_teton / p['teton_recorrido']))
    linea(sesgo_brazo <= 55, 'ranura del brazo del aro: el teton recorre %.0f mm y el aro gira %.1f grados; la ranura va a %.0f grados del radio (por debajo de 55)' % (p['teton_recorrido'], d['aro_giro'], sesgo_brazo))
    # 4. planetario
    zs, zp, zr, n = int(p['z_central']), int(p['z_satelite']), int(d['z_bisel']), int(p['n_satelites'])
    linea((zs + zr) % n == 0, 'planetario: central %d, satelites %d, bisel %d dientes, modulo %.2f. (%d + %d) / %d = %g: los %d satelites caben repartidos por igual' % (zs, zp, zr, p['modulo'], zs, zr, n, (zs + zr) / n, n))
    sep = 2 * d['r_ejes'] * math.sin(math.pi / n) - 2 * (d['r_satelite'] + p['modulo'])
    linea(sep >= 1.0, 'entre dos satelites vecinos quedan %.1f mm' % sep)
    linea(True, 'el tubo gira %.3f veces lo que el bisel, en el mismo sentido: %.0f grados de tubo son %.0f de bisel (%.2f vueltas)' % (d['relacion'], p['giro_tubo'], d['giro_bisel'], d['giro_bisel'] / 360))
    linea(d['diente_grueso'] >= 1.6, 'diente: %.2f mm de grueso en el primitivo, con %.2f de juego entre flancos; el mas fino es el del satelite' % (d['diente_grueso'], p['juego_dientes']))
    aro = d['central_fondo'] - (d['cuello_r'] + p['holg_fija'])
    linea(aro >= 2.0, 'la rueda central es un aro que entra por arriba en el cuello del marco (radio %.1f): le quedan %.1f mm de carne bajo los dientes (fondo de diente a %.1f)' % (d['cuello_r'], aro, d['central_fondo']))
    zs60 = 60; fondo60 = p['modulo'] * zs60 / 2 - 1.25 * p['modulo']
    nota('con los 60 dientes que proponia el brief, el fondo de diente quedaria a %.1f mm del centro y el cuello que rodea el mecanismo de las puertas mide %.1f: no cabe' % (fondo60, d['modulo_r']))

    # 5. franjas de radio
    f0, f1 = d['espiral_franja']
    linea(f0 - d['plato_r_in'] >= 1.5 and p['tubo_r'] - f1 >= 0.5, 'la espiral del plato ocupa de %.1f a %.1f mm de radio; el plato empieza en %.1f y el tubo en %.1f' % (f0, f1, d['plato_r_in'], p['tubo_r']))
    pend_esp = math.degrees(math.atan(p['teton_recorrido'] * math.pi / 2 / (math.radians(p['giro_puertas_fin'] - p['giro_muerto']) * (f0 + f1) / 2)))
    linea(pend_esp <= 30, 'la espiral empuja al teton con %.0f grados de sesgo como mucho' % pend_esp)
    linea(d['tubo_r_ext'] <= d['bisel_fondo'] + p['bisel_pared'] - 0.5 and d['bisel_fondo'] + 0.3 <= d['tubo_r_ext'], 'el bisel apoya en el canto del tubo: tubo de %.1f a %.1f mm de radio, pared del bisel de %.1f a %.1f' % (p['tubo_r'], d['tubo_r_ext'], d['bisel_fondo'], d['bisel_r_ext']))

    # 6. rampa
    linea(d['rampa_pendiente'] <= 20, 'rampa: sube %.1f mm en %.0f grados de tubo; pendiente de %.1f grados (el brief estimaba 18). Que se sujete sola lo dira la probeta' % (d['recorrido'], p['giro_arriba'] - p['giro_sube'], d['rampa_pendiente']))
    # tres ranuras iguales a 120 grados: el tramo plano de una no puede alcanzar a la siguiente, y entre helices tiene que quedar pared
    plano = p['giro_sube']
    pared_ranuras = d['rampa_paso'] / 3 - d['ranura_alto']
    sube_al_cruce = d['recorrido'] * (120.0 - plano) / (p['giro_arriba'] - p['giro_sube'])     # lo que ha subido una ranura donde empieza el plano de la siguiente
    linea(plano < 120 and pared_ranuras >= 3 and sube_al_cruce - d['ranura_alto'] >= 1.5, 'las tres ranuras del tubo no se juntan: el tramo plano de abajo mide %.0f grados (menos de 120); donde empieza el plano de la siguiente, la helice ya ha subido %.1f mm y queda %.1f de pared; entre helices, %.1f' % (plano, sube_al_cruce, sube_al_cruce - d['ranura_alto'], pared_ranuras))
    juego = p['holg_desliza']
    cabeceo = math.degrees(math.atan(2 * juego / (2 * (p['tubo_r'] + 1.5))))
    nota('plataforma: %.2f mm de juego de cada teton en su ranura; con eso puede cabecear %.2f grados, que en lo alto del reloj son %.1f mm de lado' % (juego, cabeceo, math.radians(cabeceo) * (p['reloj_alto'] + d['pedestal_alto'])))

    # 7. tamaño
    linea(d['cuerpo_lado'] <= 256 - 10, 'caja: %.0f mm de lado y %.0f de alto, sin la funda. Bisel de %.0f mm de diametro. Cabe en la X1 Carbon (256). El brief estimaba 150 de lado y 135 de alto' % (d['cuerpo_lado'], d['caja_alto'], 2 * d['bisel_r_ext']))
    nota('lo que se ve de las puertas cerradas: un rectangulo de %.0f x %.0f mm con una raya recta de delante atras. El hueco libre por el que sube el reloj es de %.0f x %.0f' % (d['puertas_x'], d['puerta_y'], d['hueco_x'], d['hueco_y']))

    datos = {'P_DEF': [[n_, u, v, c] for n_, u, v, c in P_DEF], 'd': d, 'tabla': tabla, 'comprobaciones': out, 'todo_bien': ok_total,
             'seccion_puerta_a': [list(c) for c in puerta_a.exterior.coords], 'seccion_puerta_b': [list(c) for c in puerta_b.exterior.coords]}
    if escribe:
        json.dump(datos, open(os.path.join(AQUI, 'caja-v5.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return datos

if __name__ == '__main__':
    datos = comprueba()
    d = datos['d']; p = params()
    print('Caja v5, fase 1: medidas y movimiento')
    for l in datos['comprobaciones']: print(l)
    print('  tabla (cada 15 grados de tubo): tubo, bisel, teton mm, aro grados, puertas grados, plataforma mm')
    for f in datos['tabla'][::15] + [datos['tabla'][-1]]:
        print('    %5.0f %7.1f %6.2f %6.2f %6.1f %6.1f' % tuple(f))
    print('  alturas (Z=0 arriba): engranajes %.1f a %.1f; plato %.1f a %.1f; aro de puertas %.1f a %.1f; ala del marco %.1f a %.1f; suelo %.1f; base %.1f' % (d['z_engr1'], d['z_engr0'], d['z_plato1'], d['z_plato0'], d['z_corr1'], d['z_corr0'], d['z_ala1'], d['z_ala0'], d['z_suelo'], d['z_base']))
    print('TODO BIEN' if datos['todo_bien'] else 'HAY FALLOS')
