# Eventually, caja v5: los dibujos de la guia de pruebas (pruebas-v5/GUIA.md).
#   python3 caja_guia_pruebas_v5.py datos <carpeta>          Escribe una malla por dibujo (<carpeta>/<nombre>.json), <carpeta>/vistas.json y <carpeta>/rotulos.json.
#   (se dibujan con render_caja.mjs, igual que las laminas del reporte)
#   python3 caja_guia_pruebas_v5.py figuras <carpeta> <png>  Pone los rotulos y las flechas y deja los dibujos en pruebas-v5/figuras/.
#   python3 caja_guia_pruebas_v5.py guia <fichero.html>      Ajusta el ancho de los dibujos en pruebas-v5/GUIA.md y escribe la guia en HTML; de ahi sale
#                                                            pruebas-v5/00-GUIA-DE-PRUEBAS.pdf, imprimiendola a PDF con un navegador (A4).
# Los colores son solo para distinguir las piezas en el dibujo: no son los colores de imprimir.
import json, os, sys, math
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
SUELO = -122.7                                   # donde pone el suelo (y la sombra) render_caja.mjs
PAL = {'marco': '#c3c9d2', 'aro_puertas': '#e6b866', 'meseta': '#f6f4ee', 'puerta': '#9fc6ee', 'pasador': '#59626e', 'teton': '#e2761f', 'probeta_teton': '#e2761f',
       'probeta_anillo': '#8fd3a0', 'base': '#d2cdc0', 'plataforma': '#f1c1b9', 'pestillo': '#d64545', 'soporte': '#fbfaf6', 'reloj_de_pega': '#7f8791', 'tubo': '#b7dcbc',
       'plato': '#c9bdea', 'satelite': '#f1d04e', 'rueda_central': '#86cfd0', 'bisel': '#ffffff', 'cama': '#4b4f56'}
NOMBRE = {'marco': 'marco', 'aro_puertas': 'aro de las puertas', 'meseta': 'meseta', 'puerta_derecha': 'puerta', 'puerta_izquierda': 'puerta', 'pasador_derecho': 'pasador',
          'pasador_izquierdo': 'pasador', 'probeta_teton': 'tetón con pomo', 'probeta_anillo': 'anillo', 'base': 'base', 'plataforma': 'plataforma', 'pestillo_derecho': 'pestillo',
          'pestillo_izquierdo': 'pestillo', 'soporte': 'soporte', 'tubo': 'tubo', 'plato': 'plato', 'teton': 'tetón', 'rueda_central': 'rueda central', 'bisel': 'bisel',
          'reloj_de_pega': 'reloj'}
def color(n):
    for k in sorted(PAL, key=len, reverse=True):
        if n.startswith(k): return PAL[k]
    return '#dddddd'

def proy(pt, cam, mira, W=1500, H=1100, fov=28.0):
    cam, mira, pt = np.array(cam, float), np.array(mira, float), np.array(pt, float)
    f = mira - cam; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    v = pt - cam; z = v @ f
    k = (H / 2) / math.tan(math.radians(fov / 2))
    return (float(W / 2 + k * (v @ r) / z), float(H / 2 - k * (v @ u) / z))

FRENTE = (200.0, -330.0, 260.0)                  # desde delante, a la derecha y arriba (la de las laminas del reporte)
ALTA = (130.0, -260.0, 400.0)                    # mas desde arriba
CAMA = (60.0, -230.0, 430.0)                     # la bandeja de la impresora
BRAZO = (-130.0, 260.0, 400.0)                   # la prueba de las puertas, vista desde el lado del brazo del aro
BRAZO_BAJA = (-210.0, 330.0, 190.0)

def datos(sal):
    import manifold3d as mf
    import caja_piezas_v5 as C, caja_probetas_v5 as PB
    p, d, d2, P = C.piezas(); S = {n: C.solido(q.ops) for n, q in P.items()}
    G = p['giro_tubo']
    COMO = {'probeta_teton': 'teton', 'probeta_anillo': 'fijo'}
    def en(n, tau, mv=(0, 0, 0)):
        m = C.mover(S[n], n, COMO.get(n, P[n].mueve), p, d, tau)
        return m.translate(list(mv)) if any(mv) else m
    def vts(m):
        me = m.to_mesh(); return np.asarray(me.vert_properties)[:, :3], np.asarray(me.tri_verts)
    vistas, rot = [], {}
    def escena(nombre, piezas, mesa, etiquetas=(), flechas=(), cam=FRENTE, k=4.6, extra=()):
        """piezas: [(pieza, tau, (dx, dy, dz))]. mesa: la z del modelo que hace de mesa. etiquetas: [(texto, pieza o punto, lado)]. flechas: [(punto, punto)]."""
        dz0 = SUELO - mesa
        out, puestas, todo = [], {}, []
        for n, tau, mv in piezas:
            m = en(n, tau, mv).translate([0, 0, dz0]); v, t = vts(m); puestas.setdefault(n, v); todo.append(v)
            out.append({'n': n, 'c': color(n), 'v': np.round(v, 3).ravel().tolist(), 't': t.ravel().tolist()})
        for n, m in extra:
            v, t = vts(m.translate([0, 0, dz0])); puestas[n] = v; todo.append(v)
            out.append({'n': n, 'c': color(n), 'v': np.round(v, 3).ravel().tolist(), 't': t.ravel().tolist()})
        json.dump(out, open(os.path.join(sal, nombre + '.json'), 'w'))
        V = np.vstack(todo)
        lo, hi = V.min(0), V.max(0); c = (lo + hi) / 2; R = np.linalg.norm(hi - lo) / 2
        u = np.array(cam, float); u /= np.linalg.norm(u); pos = c + u * k * R
        e = []
        for txt, que, lado in etiquetas:
            if isinstance(que, str):
                v = puestas[que]; a = v[np.argmax(v @ u)]                       # el punto de la pieza mas cercano a la camara
            elif isinstance(que[0], str):
                v = puestas[que[0]]; a = v[np.argmax(v @ np.array(que[1], float))]   # el punto de la pieza mas alla en una direccion
            else: a = np.array(que, float) + [0, 0, dz0]
            e.append([txt, proy(a, pos, c), lado])
        f = [[proy(np.array(a, float) + [0, 0, dz0], pos, c), proy(np.array(b, float) + [0, 0, dz0], pos, c)] for a, b in flechas]
        px = np.array([proy(q, pos, c) for q in V[:: max(1, len(V) // 6000)]] + [proy(q, pos, c) for q in (lo, hi)] + [q for a_ in f for q in a_] + [proy(q, pos, c) for o in out if o['n'] == 'cama' for q in np.array(o['v']).reshape(-1, 3)])
        vistas.append([nombre, pos.tolist(), c.tolist(), nombre])
        rot[nombre] = {'caja': [float(px[:, 0].min()), float(px[:, 1].min()), float(px[:, 0].max()), float(px[:, 1].max())], 'etiquetas': e, 'flechas': f}
        print(nombre, len(out))
    def cima(n, tau=0.0, mv=(0, 0, 0)):
        b = en(n, tau, mv).bounding_box(); return ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, b[5])
    def baja(n, tau, alto, mv=(0, 0, 0), q=None):
        """Una flecha que baja desde debajo de la pieza levantada hasta su sitio."""
        b = en(n, tau, mv).bounding_box(); x, y = q if q else ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2)
        return ((x, y, b[2] + alto - 2), (x, y, b[2] + 2 + (alto - 4) * 0.45))

    # ------------------------------------------------------------ las bandejas, como se imprimen
    cama = mf.Manifold.cube([256, 256, 1.5]).translate([-128, -128, -1.5])
    for num, f in PB.ORDEN:
        piezas = PB.B[f]; ex = [('cama', cama)]; et = []
        for n, ba, dx, dy in piezas:
            ex.append((n, PB.a_la_cama(S[n], ba, dx, dy)))
        vistos = {}
        for n, ba, dx, dy in piezas:
            t = 'satélite' if n.startswith('satelite') else NOMBRE[n]
            if t in vistos: continue
            vistos[t] = 1
            cuantos = sum(1 for m, *_ in piezas if (('satélite' if m.startswith('satelite') else NOMBRE[m]) == t))
            plural = {'puerta': 'puertas', 'pasador': 'pasadores', 'pestillo': 'pestillos', 'satélite': 'satélites'}
            et.append((('%d %s' % (cuantos, plural[t])) if cuantos > 1 else t, n, None))
        escena('bandeja-' + num[:2], [], -1.5, et, cam=CAMA, k=3.9, extra=ex)

    # ------------------------------------------------------------ prueba 1: puertas (el marco, en la mesa)
    P1 = ['marco', 'aro_puertas', 'meseta', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo']
    m1 = S['marco'].bounding_box()[2]
    for tau in np.arange(0, G + 1, 15.0):          # nada baja de la mesa
        assert min(en(n, min(tau, G)).bounding_box()[2] for n in P1 + ['probeta_teton', 'probeta_anillo']) > m1 - 0.01
    for sg in (1, -1):                              # los pasadores entran por los dos lados
        fijo = [en(n, G) for n in P1[:5]]
        assert max(sum((en(q, G, (0, sg * t_, 0)) ^ f).volume() for f in fijo) for q in P1[5:] for t_ in np.arange(0, 95, 5.0)) < 1e-3, sg
    X = {'marco': 0, 'aro_puertas': 50, 'probeta_teton': 75, 'meseta': 105, 'pasador_derecho': 140, 'pasador_izquierdo': 140, 'puerta_derecha': 170, 'puerta_izquierda': 170, 'probeta_anillo': 220}
    escena('p1-piezas', [(n, 0, (0, 0, z)) for n, z in X.items()], m1,
           [('anillo (solo para la prueba)', 'probeta_anillo', 'd'), ('2 puertas', 'puerta_izquierda', 'd'), ('2 pasadores', 'pasador_izquierdo', 'd'), ('meseta', 'meseta', 'd'),
            ('tetón con pomo (solo para la prueba)', 'probeta_teton', 'd'), ('aro de las puertas', 'aro_puertas', 'd'), ('marco', 'marco', 'd')], cam=BRAZO_BAJA, k=3.9)
    va0, va1 = [np.asarray(en('aro_puertas', t).to_mesh().vert_properties)[:, :3] for t in (0.0, G)]
    b0, b1 = va0[np.argmax(va0[:, 1])], va1[np.argmax(va1[:, 1])]
    print('   brazo del aro: cerrado x = %.1f, abierto x = %.1f (visto desde el lado del brazo, la derecha del dibujo es -x)' % (b0[0], b1[0]))
    BR = ('aro_puertas', (0, 1, 0))
    escena('p1-a', [('marco', 0, (0, 0, 0)), ('aro_puertas', G, (0, 0, 45))], m1,
           [('el brazo del aro', BR, 'd'), ('el hueco del marco donde va el brazo', (0, 73, -1.5), 'd')], [((0, 62, 45 - 20), (0, 62, 2))], cam=BRAZO)
    escena('p1-b', [('marco', 0, (0, 0, 0)), ('aro_puertas', G, (0, 0, 0)), ('meseta', 0, (0, 0, 45))], m1, [('meseta', 'meseta', 'd'), ('brazo del aro', BR, 'd')],
           [((-30, 46, 45 - 10), (-30, 46, 2))], cam=BRAZO)
    escena('p1-c', [(n, G, (0, 0, 0)) for n in P1[:3]] + [(n, G, (0, 0, 50)) for n in P1[3:5]], m1,
           [('las puertas, de pie', 'puerta_izquierda', 'd'), ('el brazo, a tope hacia este lado', BR, 'd')],
           [baja('puerta_derecha', G, 50, q=(36, 30)), baja('puerta_izquierda', G, 50, q=(-36, 30))], cam=BRAZO)
    escena('p1-d', [(n, G, (0, 0, 0)) for n in P1[:5]] + [(n, G, (0, 62, 0)) for n in P1[5:]], m1, [('pasador: la cara plana, abajo', 'pasador_izquierdo', 'd')],
           [((sx * 29.0, 108 + 42, -2.4), (sx * 29.0, 108 + 6, -2.4)) for sx in (1, -1)], cam=BRAZO)
    escena('p1-e', [(n, 0, (0, 0, 0)) for n in P1] + [('probeta_teton', 0, (0, 0, 40))], m1, [('tetón con pomo', 'probeta_teton', 'd'), ('el brazo, ahora a tope hacia el otro lado', BR, 'd')],
           [baja('probeta_teton', 0, 40)], cam=BRAZO)
    escena('p1-f', [(n, 0, (0, 0, 0)) for n in P1 + ['probeta_teton']] + [('probeta_anillo', 0, (0, 0, 45))], m1, [('anillo', 'probeta_anillo', 'd')],
           [((-40, 44, 45 - 10), (-40, 44, 2))], cam=BRAZO)
    tp0, tp1 = cima('probeta_teton', 0), cima('probeta_teton', G)
    escena('p1-cerrada', [(n, 0, (0, 0, 0)) for n in P1 + ['probeta_teton', 'probeta_anillo']], m1, [],
           [((tp0[0] + 16, tp0[1] + 12, tp0[2] + 1), (tp0[0] + 16, tp0[1] - 6, tp0[2] + 1))], cam=BRAZO)
    escena('p1-abierta', [(n, G, (0, 0, 0)) for n in P1 + ['probeta_teton', 'probeta_anillo']], m1, [], cam=BRAZO)

    # ------------------------------------------------------------ prueba 2: ascensor
    mb = S['base'].bounding_box()[2]; mp = S['plataforma'].bounding_box()[2]
    PE = ['pestillo_derecho', 'pestillo_izquierdo']
    escena('p2-piezas', [('base', 0, (0, 0, 0)), ('plataforma', 0, (0, 0, 115)), ('pestillo_derecho', 0, (45, 0, 115)), ('pestillo_izquierdo', 0, (-45, 0, 115)), ('soporte', 0, (0, 0, 165)), ('tubo', 0, (0, 0, 310))], mb,
           [('tubo', 'tubo', 'd'), ('soporte', 'soporte', 'd'), ('2 pestillos', 'pestillo_derecho', 'd'), ('plataforma', 'plataforma', 'd'), ('base con tres columnas', 'base', 'd')], k=3.9)
    escena('p2-a', [('plataforma', 0, (0, 0, 0)), ('pestillo_izquierdo', 0, (0, 0, 0)), ('pestillo_derecho', 0, (34, 0, 0))], mp,
           [('pestillo: la punta en cuña, por delante', 'pestillo_derecho', 'd'), ('el otro, ya puesto', (-40, 0, -105.0), 'i'), ('cajeado', (0, -10, -86.1), 'i')],
           [((104, 0, -104.5), (84, 0, -104.5))], cam=ALTA)
    escena('p2-b', [('plataforma', G, (0, 0, -81.1))] + [(n, G, (0, 0, -81.1)) for n in PE] + [('soporte', 0, (0, 0, 70)), ('reloj_de_pega', 0, (0, 0, 70))], mp,
           [('soporte, con el reloj abrochado', 'soporte', 'd'), ('la llave del pie va detrás', (0, 26.5, -98 + 70), 'd')], [((30, -30, -108.4 + 68), (30, -30, -86.1 + 6))])
    escena('p2-c', [('base', 0, (0, 0, 0)), ('plataforma', 0, (0, 0, 140))] + [(n, 0, (0, 0, 140)) for n in PE], mb,
           [('plataforma con sus dos pestillos', 'plataforma', 'd'), ('tres columnas', (89, 0, -25), 'd')], [((62, -62, -110.7 + 136), (62, -62, -19.9 + 6))])
    escena('p2-d', [('base', 0, (0, 0, 0)), ('plataforma', 0, (0, 0, 0))] + [(n, 0, (0, 0, 0)) for n in PE] + [('tubo', 0, (0, 0, 150))], mb,
           [('tubo', 'tubo', 'd'), ('plataforma, abajo del todo', (0, -70, -86.1), 'i')], [((70, -70, -111.1 + 146), (70, -70, -19.9 + 8))])
    AS = ['base', 'plataforma', 'tubo'] + PE
    escena('p2-e', [(n, G, (0, 0, 0)) for n in AS] + [('soporte', G, (0, 0, 75)), ('reloj_de_pega', G, (0, 0, 75))], mb,
           [('soporte', 'soporte', 'd'), ('plataforma, arriba del todo', (0, -70, -86.1 + 81.1), 'i')], [((30, -30, -108.4 + 81.1 + 73), (30, -30, -86.1 + 81.1 + 6))])
    escena('p2-abajo', [(n, 0, (0, 0, 0)) for n in AS + ['soporte', 'reloj_de_pega']], mb)
    escena('p2-arriba', [(n, G, (0, 0, 0)) for n in AS + ['soporte', 'reloj_de_pega']], mb)

    # ------------------------------------------------------------ prueba 3: planetario (encima de las otras dos)
    A2 = AS + ['soporte', 'reloj_de_pega']
    SAT = ['satelite_%d' % i for i in range(1, 7)]
    escena('p3-piezas', [(n, 0, (0, 0, 0)) for n in A2] + [(n, 0, (0, 0, 55)) for n in P1] + [('teton', 0, (0, 0, 85)), ('plato', 0, (0, 0, 115))] + [(n, 0, (0, 0, 150)) for n in SAT] +
           [('rueda_central', 0, (0, 0, 185)), ('bisel', 0, (0, 0, 225))], mb,
           [('bisel', 'bisel', 'd'), ('rueda central', 'rueda_central', 'd'), ('6 satélites', 'satelite_2', 'd'), ('plato', 'plato', 'd'), ('tetón (el normal)', 'teton', 'd'),
            ('las puertas de la prueba 1', 'marco', 'd'), ('el ascensor de la prueba 2', 'tubo', 'd')], k=3.9)
    escena('p3-a', [(n, 0, (0, 0, 0)) for n in A2] + [(n, 0, (0, 0, 60)) for n in P1], mb, [('las puertas, cerradas', 'marco', 'd'), ('tres columnas', (89, 0, -25), 'd')],
           [((66, -66, -22.6 + 58), (66, -66, -19.9 + 8))])
    B3 = A2 + P1
    escena('p3-b', [(n, 0, (0, 0, 0)) for n in B3] + [('teton', 0, (0, 0, 35))], mb, [('tetón', 'teton', 'd'), ('brazo del aro', (6, 72, -7.7), 'd')], [baja('teton', 0, 35)], cam=ALTA)
    escena('p3-c', [(n, 0, (0, 0, 0)) for n in B3 + ['teton']] + [('plato', 0, (0, 0, 45))], mb, [('plato: la espiral, hacia abajo', 'plato', 'd')], [((62, -62, -14.8 + 43), (62, -62, -12.0 + 6))])
    escena('p3-d', [(n, 0, (0, 0, 0)) for n in B3 + ['teton', 'plato']] + [(n, 0, (0, 0, 30)) for n in SAT], mb, [('6 satélites, cada uno en su eje', 'satelite_2', 'd')],
           [baja(n, 0, 30) for n in ('satelite_1', 'satelite_2', 'satelite_6')], cam=ALTA)
    escena('p3-e', [(n, 0, (0, 0, 0)) for n in B3 + ['teton', 'plato'] + SAT] + [('rueda_central', 0, (0, 0, 40))], mb, [('rueda central', 'rueda_central', 'd')], [baja('rueda_central', 0, 40, q=(50, -40))], cam=ALTA)
    escena('p3-f', [(n, 0, (0, 0, 0)) for n in B3 + ['teton', 'plato', 'rueda_central'] + SAT] + [('bisel', 0, (0, 0, 45))], mb, [('bisel: la cara que tocó la cama, arriba', 'bisel', 'd')], [((62, -62, -14.4 + 43), (62, -62, -3.6 + 6))])
    T3 = B3 + ['teton', 'plato', 'rueda_central', 'bisel'] + SAT
    escena('p3-cerrada', [(n, 0, (0, 0, 0)) for n in T3], mb)
    escena('p3-puertas', [(n, 100, (0, 0, 0)) for n in T3], mb)
    escena('p3-arriba', [(n, G, (0, 0, 0)) for n in T3], mb)
    json.dump(vistas, open(os.path.join(sal, 'vistas.json'), 'w')); json.dump(rot, open(os.path.join(sal, 'rotulos.json'), 'w'))

def figuras(sal, png):
    from PIL import Image, ImageDraw, ImageFont
    F27, F46 = [ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', t) for t in (30, 54)]
    rot = json.load(open(os.path.join(sal, 'rotulos.json'))); dest = os.path.join(AQUI, 'pruebas-v5', 'figuras'); os.makedirs(dest, exist_ok=True)
    for nombre, r in rot.items():
        im = Image.open(os.path.join(png, nombre + '.png')).convert('RGB'); fondo = im.getpixel((4, 4))
        F = F46 if nombre.startswith('bandeja') else F27; alto = 78 if nombre.startswith('bandeja') else 44
        x0, y0, x1, y1 = r['caja']
        ancho_txt = max([F.getlength(t) for t, a, l in r['etiquetas']] + [0])
        izq = [e for e in r['etiquetas'] if e[2] == 'i']; der = [e for e in r['etiquetas'] if e[2] != 'i']
        mi = int(max([F.getlength(t) for t, a, l in izq] + [0])) + (50 if izq else 0); md = int(max([F.getlength(t) for t, a, l in der] + [0])) + (50 if der else 0)
        # lienzo mas ancho que la foto, para que quepan los rotulos a los lados
        cx0, cx1 = int(x0) - 40, int(x1) + 40
        W = (cx1 - cx0) + mi + md; top, bot = max(0, int(y0) - 50), min(im.size[1], int(y1) + 110)
        lona = Image.new('RGB', (W, bot - top), fondo)
        rec = im.crop((max(0, cx0), top, min(im.size[0], cx1), bot)); lona.paste(rec, (mi + max(0, -cx0), 0))
        ox, oy = mi - cx0, -top
        dr = ImageDraw.Draw(lona)
        for a, b in r['flechas']:
            ax, ay, bx, by = a[0] + ox, a[1] + oy, b[0] + ox, b[1] + oy
            dr.line([(ax, ay), (bx, by)], fill='#b3261e', width=7)
            an = math.atan2(by - ay, bx - ax); L = 26
            dr.polygon([(bx + 10 * math.cos(an), by + 10 * math.sin(an)), (bx - L * math.cos(an - 0.5), by - L * math.sin(an - 0.5)), (bx - L * math.cos(an + 0.5), by - L * math.sin(an + 0.5))], fill='#b3261e')
        for lado, lista in (('i', izq), ('d', der)):
            lista = sorted(lista, key=lambda e: e[1][1]); ys = []
            for t, a, l in lista:
                y = a[1] + oy
                if ys and y < ys[-1] + alto: y = ys[-1] + alto
                ys.append(y)
            sobra = (ys[-1] + 22) - lona.size[1] if ys else 0
            if sobra > 0: ys = [y - sobra for y in ys]
            for (t, a, l), y in zip(lista, ys):
                ax, ay = a[0] + ox, a[1] + oy
                tx = (lona.size[0] - md + 16) if lado == 'd' else (mi - 16 - F.getlength(t))
                fx = tx - 8 if lado == 'd' else tx + F.getlength(t) + 8
                dr.line([(ax, ay), (fx, y)], fill='#333333', width=2); dr.ellipse([ax - 5, ay - 5, ax + 5, ay + 5], fill='#111111')
                dr.text((tx, y - F.size * 0.63), t, fill='#111111', font=F)
        lona.save(os.path.join(dest, nombre + '.jpg'), quality=90)
        print(nombre, lona.size)

CSS = """
@page { size: A4; margin: 15mm 14mm 16mm 14mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10.2pt; line-height: 1.42; color: #1b1b1b; }
h1 { font-size: 21pt; margin: 0 0 6pt 0; } h2 { font-size: 15pt; margin: 20pt 0 6pt 0; padding-top: 6pt; border-top: 2px solid #1f3fa8; color: #1f3fa8; break-after: avoid; }
h3 { font-size: 12pt; margin: 14pt 0 4pt 0; break-after: avoid; } p { margin: 5pt 0; } li { margin: 2.5pt 0; }
table { border-collapse: collapse; width: 100%; margin: 7pt 0; font-size: 9.3pt; } th, td { border: 1px solid #c9c9c9; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background: #eef1f8; } tr { break-inside: avoid; } img { display: block; margin: 4pt auto; max-width: 100%; border-radius: 4px; } td img { margin: 0; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; background: #f2f2f2; padding: 0 2pt; }
p:has(> img) { break-inside: avoid; } p:has(+ p > img) { break-after: avoid; } h2.salto { break-before: page; }
.paso { break-inside: avoid; margin: 9pt 0; } .fila { display: flex; gap: 8px; align-items: flex-start; justify-content: center; break-inside: avoid; margin: 6pt 0; } .fila img { margin: 0; min-width: 0; flex: 0 1 auto; height: auto; }
"""
def guia(html):
    """Ajusta el ancho de los dibujos de GUIA.md a su tamano real y escribe la misma guia en HTML (en <html>), para pasarla a PDF."""
    import re, markdown
    from PIL import Image
    d = os.path.join(AQUI, 'pruebas-v5'); md = open(os.path.join(d, 'GUIA.md'), encoding='utf-8').read()
    def ancho(m):
        f = m.group(1); w = Image.open(os.path.join(d, f)).size[0]
        fijo = {'bandeja': 330, 'p1-cerrada': 300, 'p1-abierta': 300, 'p2-abajo': 300, 'p2-arriba': 300, 'p3-cerrada': 205, 'p3-puertas': 205, 'p3-arriba': 205}
        k = [v for n_, v in fijo.items() if n_ in f]
        return '<img src="%s" width="%d">' % (f, k[0] if k else min(650, round(w * 0.36)))
    md = re.sub(r'<img src="([^"]+)" width="\d+">', ancho, md); open(os.path.join(d, 'GUIA.md'), 'w', encoding='utf-8').write(md)
    h = markdown.markdown(md, extensions=['tables'])
    h = re.sub(r'<h2>(\d)\. Prueba', r'<h2 class="salto">\1. Prueba', h)
    h = re.sub(r'(<p><strong>Paso \d+\.</strong>.*?</p>\s*<p><img [^>]*></p>)', r'<div class="paso">\1</div>', h, flags=re.S)        # cada paso, con su dibujo, sin partir
    h = h.replace('<th>¿Qué pasó?</th>', '<th style="width:27%">¿Qué pasó?</th>').replace('<th>Así tiene que verse</th>', '<th style="width:338px">Así tiene que verse</th>')
    h = h.replace('Es la misma guía que <code>00-GUIA-DE-PRUEBAS.pdf</code>, que está en esta carpeta.', '')
    open(html, 'w', encoding='utf-8').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><base href="file://%s/"><title>Eventually · Guía de pruebas de la caja v5</title><style>%s</style></head><body>%s</body></html>' % (d, CSS, h))

if __name__ == '__main__':
    if sys.argv[1] == 'datos': datos(sys.argv[2])
    elif sys.argv[1] == 'guia': guia(sys.argv[2])
    else: figuras(sys.argv[2], sys.argv[3])
