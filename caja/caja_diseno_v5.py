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
#   - El plato tiene por debajo UNA ranura en espiral. En ella entra el teton de la CORREDERA, que va detras
#     de las puertas y solo puede moverse de delante atras. La corredera tiene dos canales en diagonal y en
#     cada uno entra la bola de la manivela de una puerta: al moverse la corredera, las dos puertas giran.
#   - Una sola ranura y una sola corredera para las dos puertas: asi no hay cruce de pistas.
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
    ('eje_fuera',        'mm',  3.0,   'Lo que el eje de la bisagra queda por fuera del borde del hueco'),
    ('puerta_cola',      'mm',  1.2,   'Lo que la puerta sigue mas alla de su eje, por fuera'),
    ('puerta_solape_y',  'mm',  7.0,   'Lo que la puerta sobra por delante y por detras del hueco: ahi apoya y ahi lleva la manivela'),
    ('junta',            'mm',  0.3,   'Raya entre las dos puertas cerradas'),
    ('labio_largo',      'mm',  2.0,   'Media madera: lo que el labio de abajo de una puerta se mete bajo la otra'),
    ('labio_grueso',     'mm',  1.0,   'Grueso de ese labio'),
    ('labio_hueco',      'mm',  1.2,   'Hueco en altura entre el labio y la otra puerta: al abrir, el labio sube mas deprisa'),
    ('manivela_r',       'mm',  6.5,   'Del eje de la bisagra al centro de la bola de la manivela'),
    ('bola_d',           'mm',  5.0,   'Diametro de la bola de la manivela'),
    ('canal_ang',        'deg', 62.0,  'Inclinacion de los canales de la corredera respecto a su movimiento'),
    ('canal_reposo',     'mm',  3.0,   'Tramo recto al principio y al final de cada canal: ahi la puerta queda bloqueada por la forma'),
    ('canal_pared',      'mm',  1.6,   'Pared de la corredera por fuera de cada canal'),
    ('cuello_pared',     'mm',  1.5,   'Pared del cuello del marco alrededor del hueco de las manivelas'),
    ('teton_corr_d',     'mm',  5.0,   'Diametro del teton de la corredera que entra en la espiral del plato'),
    # --- giro del tubo ---
    ('giro_tubo',        'deg', 345.0, 'DECIDIDO en el brief: giro total del tubo, de tope a tope'),
    ('giro_muerto',      'deg', 45.0,  'DECIDIDO (D-20): tramo muerto al empezar. Giran los engranajes y no pasa nada'),
    ('giro_puertas_fin', 'deg', 105.0, 'Del brief: a este giro de tubo la corredera ha terminado su recorrido'),
    ('giro_sube',        'deg', 88.0,  'A este giro de tubo empieza a subir la plataforma. Lo fija la comprobacion del reloj'),
    ('giro_arriba',      'deg', 335.0, 'Del brief: a este giro de tubo la plataforma esta arriba; despues la rampa es plana'),
    # --- ascensor ---
    ('margen_reloj_abajo', 'mm', 5.0,  'Con el reloj abajo, lo que queda entre lo mas alto del reloj y lo mas bajo de las puertas'),
    ('tubo_r',           'mm',  76.0,  'Radio interior del tubo'),
    ('tubo_pared',       'mm',  4.5,   'Grueso de la pared del tubo'),
    ('rampa_fondo',      'mm',  3.0,   'Lo que las ranuras en helice entran en la pared del tubo'),
    ('teton_plat_d',     'mm',  6.0,   'Diametro de los tres tetones de la plataforma'),
    ('disco_grueso',     'mm',  5.0,   'Grueso del disco de la plataforma'),
    ('pedestal_holgura', 'mm',  0.4,   'Entre el pedestal y el hueco del marco, por lado'),
    # --- planetario ---
    ('modulo',           'mm',  1.5,   'Del brief: modulo de los dientes'),
    ('z_central',        '',    78,    'Dientes de la rueda central (fija). El brief proponia 60: no caben dentro las puertas con sus manivelas'),
    ('z_satelite',       '',    12,    'Dientes de cada satelite'),
    ('n_satelites',      '',    6,     'DECIDIDO (D-20): cinco blancos y uno azul'),
    ('juego_dientes',    'mm',  0.2,   'Juego entre flancos'),
    ('engranaje_grueso', 'mm',  6.0,   'Grueso de los engranajes'),
    # --- alturas, de arriba abajo ---
    ('esqueleto_grueso', 'mm',  3.0,   'Grueso de la placa fija que rodea las puertas y tapa a medias los engranajes'),
    ('plato_grueso',     'mm',  5.0,   'Grueso del plato portasatelites'),
    ('espiral_fondo',    'mm',  3.0,   'Fondo de la ranura en espiral, por debajo del plato'),
    ('corredera_grueso', 'mm',  3.0,   'Grueso de la corredera bajo el plato'),
    ('ala_grueso',       'mm',  4.0,   'Grueso del ala del marco, la que apoya en las columnas'),
    ('base_grueso',      'mm',  4.0,   'Grueso del fondo de la caja'),
    ('aire',             'mm',  0.4,   'Aire en altura entre piezas que se mueven una sobre otra'),
    # --- cuerpo ---
    ('bisel_pared',      'mm',  3.6,   'Pared del bisel por fuera del fondo de sus dientes'),
    ('bisel_ala',        'mm',  3.0,   'Ala del bisel que queda bajo el labio del cuerpo y lo retiene'),
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
    # manivela y corredera
    rho = p['manivela_r']
    d['bola_dx'] = 2 * rho * math.sin(math.radians(45))    # lo que se mueve la bola en X de cerrada a abierta
    d['corr_diagonal'] = d['bola_dx'] / math.tan(math.radians(p['canal_ang']))
    d['corr_recorrido'] = d['corr_diagonal'] + 2 * p['canal_reposo']
    # lo mas lejos del centro que llega el mecanismo de las puertas: la esquina del canal de la bola, con la puerta cerrada
    d['manivela_x'] = d['eje_x'] + rho * math.sin(math.radians(45)) + p['bola_d'] / 2 + p['holg_desliza'] + p['canal_pared']
    d['modulo_r'] = math.hypot(d['manivela_x'], d['puerta_y'] / 2)
    d['cuello_r'] = d['modulo_r'] + 0.5 + p['cuello_pared']             # cuello redondo del marco: dentro van puertas, manivelas y corredera
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
    # franja de la espiral, bajo el plato
    w = p['teton_corr_d'] / 2 + p['holg_desliza']
    d['espiral_r_abierta'] = d['plato_r_in'] + 1.8 + w                 # la corredera se mueve hacia dentro para abrir
    d['espiral_r_cerrada'] = d['espiral_r_abierta'] + d['corr_recorrido']
    d['espiral_franja'] = (d['espiral_r_abierta'] - w, d['espiral_r_cerrada'] + w)
    # alturas, de arriba abajo (Z = 0 arriba)
    a = p['aire']
    d['z_engr1'] = -p['esqueleto_grueso'] - a
    d['z_engr0'] = d['z_engr1'] - p['engranaje_grueso']
    d['z_plato1'] = d['z_engr0'] - a
    d['z_plato0'] = d['z_plato1'] - p['plato_grueso']
    d['z_corr1'] = d['z_plato0'] - a
    d['z_corr0'] = d['z_corr1'] - p['corredera_grueso']
    d['z_ala1'] = d['z_corr0'] - a
    d['z_ala0'] = d['z_ala1'] - p['ala_grueso']
    d['pedestal_alto'] = -d['z_ala0'] + 1.0                # arriba del todo, el disco queda 1 mm por debajo del ala
    d['recorrido'] = p['reloj_alto'] + p['puerta_grueso'] + p['margen_reloj_abajo']
    d['z_disco1_abajo'] = -d['pedestal_alto'] - d['recorrido']
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

def movimiento(p, d, tau):
    """Para un giro de tubo 'tau' (grados): recorrido de la corredera, angulo de las puertas y altura de la plataforma."""
    S = d['corr_recorrido']; rep = p['canal_reposo']; rho = p['manivela_r']
    s = S * suave((tau - p['giro_muerto']) / (p['giro_puertas_fin'] - p['giro_muerto']))
    u = min(1.0, max(0.0, (s - rep) / d['corr_diagonal']))
    x_bola = rho * math.sin(math.radians(45)) - u * d['bola_dx']          # respecto al eje de la bisagra, + hacia fuera
    puerta = 45.0 - math.degrees(math.asin(max(-1.0, min(1.0, x_bola / rho))))
    h = d['recorrido'] * min(1.0, max(0.0, (tau - p['giro_sube']) / (p['giro_arriba'] - p['giro_sube'])))
    return s, puerta, h

def comprueba(escribe=True):
    import numpy as np
    from shapely.geometry import Polygon, Point, box
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
    nudillo = Point(0, 0).buffer(d['nudillo_r'], 48).intersection(box(-50, -50, 50, t / 2))
    cuerpo = unary_union([losa, nudillo])
    ll = p['labio_largo']; lg = p['labio_grueso']; lh = p['labio_hueco']
    labio = box(-largo - p['junta'] - ll, -t / 2, -largo + 0.01, -t / 2 + lg)          # la puerta A mete este labio bajo la B
    rebaje = box(-largo - 0.01, -t / 2 - 0.01, -largo + ll + 0.6, -t / 2 + lg + lh)    # y la B esta rebajada por debajo
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
    a90 = derecha(puerta_a, 90)
    linea(a90.bounds[0] >= d['hueco_x'] / 2, 'abierta a 90 grados, la puerta queda entera por fuera del hueco: su punto mas metido esta a X = %.2f (el hueco llega a %.1f)' % (a90.bounds[0], d['hueco_x'] / 2))
    nota('abierta, la puerta sobresale %.1f mm sobre la tapa y baja %.1f mm por debajo de ella junto a la bisagra' % (a90.bounds[3], -a90.bounds[1]))

    # 2. las dos puertas, una contra otra, en toda la apertura (se mueven a la vez)
    peor = 1e9; ang_peor = 0
    for ang in np.arange(0.5, 90.01, 0.5):
        dist = derecha(puerta_a, ang).distance(izquierda(puerta_b, ang))
        if dist < peor: peor, ang_peor = dist, ang
    linea(peor >= 0.2, 'al abrir a la vez, el labio de una puerta y el rebaje de la otra no se tocan: lo mas cerca, %.2f mm, a %.1f grados' % (peor, ang_peor))

    # 3. grado a grado de tubo: tabla, y el reloj contra las puertas
    taus = [i * 1.0 for i in range(int(p['giro_tubo']) + 1)]
    tabla = []; peor_reloj = 1e9; tau_peor = 0; peor_ped = 1e9
    rw = p['reloj_ancho'] / 2
    ped_x = d['hueco_x'] / 2 - p['pedestal_holgura']
    for tau in taus:
        s, ang, h = movimiento(p, d, tau)
        z_ped = -d['recorrido'] + h                                   # cara de arriba del pedestal
        tabla.append([tau, round(tau / d['relacion'], 1), round(s, 2), round(ang, 2), round(h, 2)])
        A = derecha(puerta_a, ang); B = izquierda(puerta_b, ang)
        reloj = box(-rw, z_ped, rw, z_ped + p['reloj_alto'])
        pedestal = box(-ped_x, z_ped - d['pedestal_alto'], ped_x, z_ped)
        dist = min(reloj.distance(A), reloj.distance(B))
        if dist < peor_reloj: peor_reloj, tau_peor = dist, tau
        peor_ped = min(peor_ped, pedestal.distance(A), pedestal.distance(B))
    linea(peor_reloj >= p['reloj_margen'], 'en todo el recorrido el reloj de pega queda a %.2f mm o mas de las puertas (lo mas cerca, con el tubo a %.0f grados). El brief pide %.0f' % (peor_reloj, tau_peor, p['reloj_margen']))
    linea(peor_ped >= 0.5, 'el pedestal queda siempre a %.2f mm o mas de las puertas; arriba, entre el pedestal y la cara de la puerta abierta quedan %.1f mm' % (peor_ped, d['cara_dentro_abierta'] - ped_x))
    s0, a0_, h0 = movimiento(p, d, 0); s1, a1_, h1 = movimiento(p, d, p['giro_tubo'])
    linea(abs(a0_) < 0.01 and abs(a1_ - 90) < 0.01, 'las puertas van de %.1f a %.1f grados' % (a0_, a1_))
    linea(abs(h0) < 1e-9 and abs(h1 - d['recorrido']) < 1e-9, 'la plataforma sube %.1f mm; arriba, la cara del pedestal queda en Z = 0, a ras' % d['recorrido'])
    # tramos en los que la puerta esta bloqueada por la forma (bola en el tramo recto del canal)
    quieta0 = max(tau for tau in taus if movimiento(p, d, tau)[1] < 0.01)
    quieta1 = min(tau for tau in taus if movimiento(p, d, tau)[1] > 89.99)
    sube0 = max(tau for tau in taus if movimiento(p, d, tau)[2] < 1e-9)
    linea(quieta1 <= sube0 + 1e-9 or peor_reloj >= p['reloj_margen'], 'orden: tramo muerto hasta %.0f grados; las puertas se mueven de %.0f a %.0f; la plataforma sube de %.0f a %.0f; arriba, plano hasta %.0f' % (p['giro_muerto'], quieta0, quieta1, sube0, p['giro_arriba'], p['giro_tubo']))
    baile = math.degrees(p['holg_desliza'] / (p['manivela_r'] * math.cos(math.radians(45))))
    nota('en los tramos de «cerrada» y «abierta» la bola esta en un tramo del canal paralelo al movimiento de la corredera: empujar la puerta no mueve nada. Con %.2f mm de holgura de la bola, la puerta baila %.1f grados a cada lado (el brief admite de 85 a 95)' % (p['holg_desliza'], baile))

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
    nota('con los 60 dientes que proponia el brief, el fondo de diente quedaria a %.1f mm del centro y el mecanismo de las puertas llega a %.1f: no cabe' % (fondo60, d['modulo_r']))

    # 5. franjas de radio
    f0, f1 = d['espiral_franja']
    linea(f0 - d['plato_r_in'] >= 1.5 and p['tubo_r'] - f1 >= 0.5, 'la espiral del plato ocupa de %.1f a %.1f mm de radio; el plato empieza en %.1f y el tubo en %.1f' % (f0, f1, d['plato_r_in'], p['tubo_r']))
    pend_esp = math.degrees(math.atan(d['corr_recorrido'] * math.pi / 2 / (math.radians(p['giro_puertas_fin'] - p['giro_muerto']) * (f0 + f1) / 2)))
    linea(pend_esp <= 30, 'la espiral empuja al teton de la corredera con %.0f grados de sesgo como mucho' % pend_esp)
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
    print('  tabla (cada 15 grados de tubo): tubo, bisel, corredera mm, puertas grados, plataforma mm')
    for f in datos['tabla'][::15] + [datos['tabla'][-1]]:
        print('    %5.0f %7.1f %6.2f %6.1f %6.1f' % tuple(f))
    print('  alturas (Z=0 arriba): engranajes %.1f a %.1f; plato %.1f a %.1f; corredera %.1f a %.1f; ala del marco %.1f a %.1f; suelo %.1f; base %.1f' % (d['z_engr1'], d['z_engr0'], d['z_plato1'], d['z_plato0'], d['z_corr1'], d['z_corr0'], d['z_ala1'], d['z_ala0'], d['z_suelo'], d['z_base']))
    print('TODO BIEN' if datos['todo_bien'] else 'HAY FALLOS')
