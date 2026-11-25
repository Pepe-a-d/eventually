# Eventually, caja v5: dibujos del reporte, sacados del modelo (caja_piezas_v5.py).
#   python3 caja_figuras_v5.py cortes            cortes de verdad (cada pieza cortada por un plano), con nombres
#   python3 caja_figuras_v5.py laminas <png>     monta las laminas a partir de las vistas que dibuja caja_render_v5.py
import json, math, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import caja_piezas_v5 as C

AQUI = os.path.dirname(os.path.abspath(__file__))
SAL = os.path.join(AQUI, 'reporte-v5')
COL = {'base': '#c9ccd1', 'cuerpo': '#e4e1d8', 'tubo': '#b9d4bd', 'plato': '#8fbf98', 'plataforma': '#e7c1bb', 'marco': '#d9cfa8', 'meseta': '#f1e7b6', 'aro_puertas': '#f0b46a',
       'teton': '#c7641a', 'rueda_central': '#b7b3d9', 'bisel': '#9db7dd', 'puerta_derecha': '#ffffff', 'puerta_izquierda': '#ffffff', 'pasador_derecho': '#555b66',
       'pasador_izquierdo': '#555b66', 'soporte': '#9aa0a8', 'pestillo_derecho': '#d2552b', 'pestillo_izquierdo': '#d2552b', 'reloj_de_pega': '#c5cad1', 'funda': '#efece4'}

def corte(S, P, p, d, tau, plano):
    """Poligonos de cada pieza cortada por el plano 'y' (y = 0, se ve de frente) o 'x' (x = 0, se ve de lado)."""
    out = {}
    for n, q in P.items():
        if q.mueve in ('funda', 'probeta'): continue
        m = C.mover(S[n], n, q.mueve, p, d, tau)
        m = m.rotate([90, 0, 0]) if plano == 'y' else m.rotate([0, 0, -90]).rotate([90, 0, 0])
        cs = m.slice(0.0)
        pols = [np.asarray(a) for a in cs.to_polygons()]
        if pols: out[n] = [np.column_stack([a[:, 0], -a[:, 1]]) if plano == 'y' else np.column_stack([a[:, 0], -a[:, 1]]) for a in pols]
    return out

def pinta(ax, cortes, titulo, etiquetas=()):
    for n, pols in cortes.items():
        verts = []; codes = []
        for a in pols:
            verts += list(a) + [a[0]]; codes += [Path.MOVETO] + [Path.LINETO] * (len(a) - 1) + [Path.CLOSEPOLY]
        col = COL.get(n, '#2a4fb5' if n == 'satelite_1' else '#dfe3ea')
        ax.add_patch(PathPatch(Path(verts, codes), facecolor=col, edgecolor='#30343a', linewidth=0.45))
    for txt, (ax_, az_), (tx, tz) in etiquetas:
        ax.annotate(txt, xy=(ax_, az_), xytext=(tx, tz), fontsize=7.6, va='center', ha='right' if tx < ax_ else 'left',
                    arrowprops=dict(arrowstyle='-', color='#444', linewidth=0.55, shrinkA=1, shrinkB=0))
    ax.set_aspect('equal'); ax.set_xlim(-150, 150); ax.set_ylim(-128, 78); ax.axis('off'); ax.set_title(titulo, fontsize=10, loc='left')

def cortes():
    p, d, d2, P = C.piezas(); S = {n: C.solido(q.ops) for n, q in P.items()}
    G = p['giro_tubo']
    Rt0 = d['espiral_r_cerrada']
    fr = [('cuerpo (piel cuadrada)', (-88, -70), (-100, -70)), ('base', (-60, -120.6), (-100, -112)), ('tubo, con la rampa por dentro', (-78.2, -50), (-100, -50)),
          ('plataforma', (-55, -114.6), (-100, -98)), ('pedestal', (-15, -100), (-100, -86)), ('bisel (lo que se gira)', (-81, -6), (-100, -2)),
          ('plato: lleva los satélites', (-68, -12.3), (-100, -14)), ('marco', (-64, -20.6), (-100, -26)), ('aro de las puertas', (-45, -16.7), (-100, -38)),
          ('rueda central (fija) y su dedo', (-66, -1.5), (-100, 12)), ('meseta', (-45, -6.5), (-60, 26)), ('pasador (bisagra)', (-28, -2.5), (-30, 40)),
          ('puerta', (12, -2.5), (30, 40)), ('reloj de pega (supuesto): aquí, su brazalete', (8, -11.6), (100, -40)), ('soporte, con la peana metida en el pedestal', (14, -84), (100, -84)), ('pestillo', (40, -104.5), (100, -98)),
          ('diente del bisel', (76.5, -6.4), (100, 12)), ('rueda central, dientes', (58, -6.4), (100, 26))]
    la = [('satélite azul', (-67.5, -6.4), (-100, 12)), ('tetón de las puertas', (Rt0, -17.5), (100, -30)), ('espiral, bajo el plato', (Rt0, -13), (100, -16)),
          ('brazo del aro', (Rt0 - 4, -16.7), (100, -44)), ('tetón de la plataforma, en la rampa', (77, -114.6), (100, -100)), ('ranura de la rampa', (-78, -60), (-100, -60)),
          ('las dos puertas (se ve la junta de lado)', (0, -2.5), (-20, 40)), ('satélite', (67.5, -6.4), (100, 12)), ('imán del soporte', (12, -89), (100, -72)), ('columna de la base', (-70, -70), (-100, -80)), ('reloj de pega (supuesto)', (-20, -45), (-100, -30))]
    fig, axs = plt.subplots(2, 2, figsize=(15, 11), dpi=150)
    pinta(axs[0][0], corte(S, P, p, d, 0, 'y'), 'Cerrada, cortada por el centro y vista de frente', fr)
    pinta(axs[0][1], corte(S, P, p, d, 0, 'x'), 'Cerrada, cortada por el centro y vista desde la derecha (el frente queda a la izquierda)', la)
    pinta(axs[1][0], corte(S, P, p, d, G, 'y'), 'Abierta: puertas de pie y reloj arriba, de frente')
    pinta(axs[1][1], corte(S, P, p, d, G, 'x'), 'Abierta, desde la derecha')
    fig.tight_layout(); fig.savefig(os.path.join(SAL, 'caja-cortes.png'), facecolor='white'); plt.close(fig)
    # detalle de la bisagra, la junta y el enganche, de frente
    fig, axs = plt.subplots(1, 2, figsize=(15, 5.2), dpi=150)
    for ax, (x0, x1, tit) in zip(axs, ((-12, 12, 'La junta del centro (en bisel) — corte a 20 mm por detrás del centro'), (20, 92, 'Bisagra, meseta, rueda central, satélites y bisel — corte por el centro'))):
        c = corte(S, P, p, d, 0, 'y')
        if x0 < 0:
            c = {}
            for n, q in P.items():
                if not n.startswith('puerta') and n != 'meseta': continue
                cs = S[n].translate([0, -20, 0]).rotate([90, 0, 0]).slice(0.0)
                c[n] = [np.column_stack([np.asarray(a)[:, 0], -np.asarray(a)[:, 1]]) for a in cs.to_polygons()]
        pinta(ax, c, tit)
        ax.set_xlim(x0, x1); ax.set_ylim(-26 if x0 > 0 else -9, 4)
    fig.tight_layout(); fig.savefig(os.path.join(SAL, 'caja-detalles.png'), facecolor='white'); plt.close(fig)

# ---------------------------------------------------------------- laminas con las vistas en perspectiva
def proy(pt, cam, mira, W=1500, H=1100, fov=28.0):
    """Donde cae en la imagen un punto del modelo, con la misma camara que usa render_caja.mjs."""
    cam, mira, pt = np.array(cam, float), np.array(mira, float), np.array(pt, float)
    f = mira - cam; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    v = pt - cam; z = v @ f
    k = (H / 2) / math.tan(math.radians(fov / 2))
    return (W / 2 + k * (v @ r) / z, H / 2 - k * (v @ u) / z)

def laminas(png):
    from PIL import Image, ImageDraw, ImageFont
    def fuente(t):
        for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',):
            if os.path.exists(f): return ImageFont.truetype(f, t)
        return ImageFont.load_default()
    F1, F2 = fuente(30), fuente(24)
    vistas = {v[3]: v for v in json.load(open(os.path.join(AQUI, 'caja-v5-vistas.json')))}
    def abre(n, caja=None):
        im = Image.open(os.path.join(png, n + '.png')).convert('RGB')
        return im.crop(caja) if caja else im
    def hoja(celdas, cols, sal, ancho=760, F2=F2):
        ims = []
        for im, pie in celdas:
            k = ancho / im.size[0]; im = im.resize((ancho, int(im.size[1] * k)))
            lona = Image.new('RGB', (ancho, im.size[1] + 64), 'white'); lona.paste(im, (0, 0))
            ImageDraw.Draw(lona).text((14, im.size[1] + 14), pie, fill='#222', font=F2); ims.append(lona)
        h = max(i.size[1] for i in ims); filas = (len(ims) + cols - 1) // cols
        H = Image.new('RGB', (cols * ancho, filas * h), 'white')
        for j, i in enumerate(ims): H.paste(i, ((j % cols) * ancho, (j // cols) * h))
        H.save(os.path.join(SAL, sal)); return sal
    p = C.D.params(); d = C.D.derivadas(p)
    mv = lambda t: C.D.movimiento(p, d, t)
    rec = (230, 60, 1270, 1000)
    pasos = (0, 45, 72, 100, 220, 345)
    textos = ['1. Cerrada', '2. Tramo muerto: solo giran engranajes', '3. Las puertas se abren', '4. Puertas de pie; empieza a subir', '5. El reloj sube', '6. Arriba, tope']
    hoja([(abre('paso-%d' % (i + 1), rec), '%s (tubo %d°, bisel %d°)' % (textos[i], t, round(t / d['relacion']))) for i, t in enumerate(pasos)], 3, 'caja-apertura.png', F2=fuente(21))
    hoja([(abre('caja-con-funda', (250, 60, 1250, 1000)), 'Con la funda'), (abre('caja-cerrada', (250, 60, 1250, 1000)), 'Sin la funda, cerrada'), (abre('planta', (330, 130, 1170, 970)), 'Planta')], 3, 'caja-vistas.png')
    hoja([(abre('manivela-%d' % (i + 1), (230, 240, 1270, 640)), t) for i, t in enumerate(('Cerradas: la bola, en el tramo quieto de su pista', 'A medio abrir: el aro gira y la pista empuja la bola', 'Abiertas: la bola, en el otro tramo quieto'))], 3, 'caja-puertas-manivela.png')
    hoja([(abre('aro-cerrado', (330, 110, 1090, 820)), 'El aro (tostado) con la caja cerrada, desde arriba'), (abre('aro-abierto', (330, 110, 1090, 820)), 'Con la caja abierta: el aro ha girado %.0f°' % d['aro_giro']),
          (abre('probeta-puertas', (200, 250, 950, 830)), 'La probeta de las puertas')], 3, 'caja-puertas-aro.png')
    # despiece con nombres
    v = vistas['despiece']; im = abre('despiece'); dr = ImageDraw.Draw(im)
    import caja_render_v5 as R
    nombres = [('cuerpo', 'cuerpo', -50), ('bisel', 'bisel', -7), ('rueda_central', 'rueda central (fija)', -4), ('satelite', 'seis satélites (uno azul)', -6), ('puerta_derecha', 'dos puertas (distintas)', -2),
               ('pasador_derecho', 'dos pasadores', -2.5), ('meseta', 'meseta', -4), ('plato', 'plato', -12), ('teton', 'tetón', -16), ('aro_puertas', 'aro de las puertas', -16), ('marco', 'marco', -20),
               ('tubo', 'tubo', -60), ('plataforma', 'plataforma, soporte y reloj de pega', -105), ('base', 'base con tres columnas', -120)]
    rot = []
    for n, txt, z in nombres:
        dz = R.DESPIECE.get(n, 418)
        x, y = proy((85, -40, z + dz), v[1], v[2])
        dr.line([(x, y), (1010, y)], fill='#555', width=2); rot.append((y, txt))
    lona = Image.new('RGB', (1700, 1100), im.getpixel((5, 5))); lona.paste(im, (0, 0)); dr = ImageDraw.Draw(lona)
    for y, txt in rot: dr.text((1020, y - 17), txt, fill='#111', font=F1)
    lona.crop((330, 0, 1700, 1100)).save(os.path.join(SAL, 'caja-despiece.png'))

if __name__ == '__main__':
    if sys.argv[1] == 'cortes': cortes()
    else: laminas(sys.argv[2])
