# Figuras de la caja v5. Lee caja-v5.json (lo escribe caja_diseno_v5.py).   python3 caja_figuras_v5.py <carpeta de salida>
import json, math, os, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPoly
AQUI = os.path.dirname(os.path.abspath(__file__))
sal = sys.argv[1] if len(sys.argv) > 1 else AQUI
j = json.load(open(os.path.join(AQUI, 'caja-v5.json'), encoding='utf-8')); d = j['d']; P = dict((a[0], a[2]) for a in j['P_DEF'])
BL = '#f3f1ea'; GR = '#c9ced6'; AZ = '#1f3fa8'; VE = '#8fc7a8'; NA = '#f0b860'; RO = '#e7b3b3'

def corte(ax, h, ang, titulo):
    """Corte por el plano X-Z (de izquierda a derecha, visto desde el frente). h = altura de la plataforma, ang = angulo de las puertas."""
    def r(x0, x1, z0, z1, c, sim=True, **kw):
        for s in ((1, -1) if sim else (1,)):
            a, b = sorted((s * x0, s * x1))
            ax.add_patch(Rectangle((a, z0), b - a, z1 - z0, fc=c, ec='#333', lw=0.5, **kw))
    t = P['puerta_grueso']; xh = d['eje_x']; lado = d['cuerpo_lado'] / 2
    # cuerpo y base
    r(lado - P['cuerpo_pared'], lado, d['z_base'], d['z_cuerpo_arriba'], BL)
    r(d['bisel_r_ext'] + 0.4, lado, d['z_cuerpo_arriba'] - 3, d['z_cuerpo_arriba'], BL)
    r(0, lado, d['z_base'], d['z_suelo'], BL, sim=True)
    # tubo y plato
    r(P['tubo_r'], d['tubo_r_ext'], d['z_suelo'] + 0.5, d['z_plato0'], VE)
    r(d['plato_r_in'], d['tubo_r_ext'], d['z_plato0'], d['z_plato1'], VE)
    # bisel
    r(d['bisel_fondo'], d['bisel_r_ext'], d['z_engr0'], 0, NA); r(d['bisel_punta'], d['bisel_fondo'], d['z_engr0'], d['z_engr1'], NA)
    r(d['bisel_punta'] - 1.5, d['bisel_fondo'], -P['esqueleto_grueso'], 0, NA)
    r(d['bisel_r_ext'], d['bisel_ala_r'], d['z_cuerpo_arriba'] - 6.5, d['z_cuerpo_arriba'] - 3.4, NA)
    r(d['tubo_r_ext'] + 0.4, d['bisel_r_ext'], d['z_cuerpo_arriba'] - 6.5, d['z_engr0'], NA)
    # satelites y rueda central
    r(d['r_ejes'] - d['r_satelite'] - 1.5, d['r_ejes'] + d['r_satelite'] + 1.5, d['z_engr0'], d['z_engr1'], AZ, alpha=0.8)
    r(d['cuello_r'] + 0.15, d['central_punta'], d['z_engr0'], d['z_engr1'], GR)
    r(d['cuello_r'] + 0.3, d['central_punta'] + 1.5, -P['esqueleto_grueso'], 0, GR)
    # marco: ala, cuello y meseta
    r(d['hueco_x'] / 2, P['tubo_r'] - 0.6, d['z_ala0'], d['z_ala1'], BL)
    r(xh + d['nudillo_r'] + 0.3, d['cuello_r'], d['z_ala1'], 0, BL)
    r(d['hueco_x'] / 2, xh + d['nudillo_r'] + 0.3, d['z_ala1'], -t - 0.8, BL)
    # columnas (dibujadas en este plano aunque estan giradas)
    r(P['tubo_r'] - 8, P['tubo_r'] - 1.2, d['z_suelo'], d['z_ala0'], '#e2ded2')
    # plataforma, pedestal y reloj
    z1 = d['z_disco1_abajo'] + h
    r(0, P['tubo_r'] - 1.0, z1 - P['disco_grueso'], z1, RO); r(P['tubo_r'] - 1.0, P['tubo_r'] + P['rampa_fondo'] - 0.3, z1 - P['disco_grueso'] + 0, z1, RO)
    ped = d['hueco_x'] / 2 - P['pedestal_holgura']
    r(0, ped, z1, z1 + d['pedestal_alto'], RO)
    zr = z1 + d['pedestal_alto']
    r(0, P['reloj_ancho'] / 2, zr, zr + P['reloj_alto'], '#9aa3ad', alpha=0.55)
    ax.text(0, zr + P['reloj_alto'] / 2, 'reloj\nde pega', ha='center', va='center', fontsize=9)
    # puertas
    for s in (1, -1):
        c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        pts = []
        for x, z in ((-(xh - 0.15), -t / 2), (P['puerta_cola'], -t / 2), (P['puerta_cola'], t / 2), (-(xh - 0.15), t / 2)):
            pts.append((s * (xh + x * c + z * sn), d['eje_z'] - x * sn + z * c))
        ax.add_patch(MPoly(pts, closed=True, fc='#ffffff', ec='#000', lw=1.1))
    ax.set_xlim(-lado - 4, lado + 4); ax.set_ylim(d['z_base'] - 4, P['reloj_alto'] + 8); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(titulo, fontsize=12)

fig, axs = plt.subplots(1, 3, figsize=(21, 9.5))
corte(axs[0], 0.0, 0.0, 'Cerrada: reloj abajo, puertas cerradas')
corte(axs[1], d['recorrido'] * 0.45, 90.0, 'A medio subir: puertas ya de pie')
corte(axs[2], d['recorrido'], 90.0, 'Arriba: el pedestal rellena el hueco')
fig.text(0.5, 0.03, 'Corte de izquierda a derecha, visto desde el frente. Blanco: lo fijo (base, cuerpo, columnas, marco) y las puertas. Verde: tubo y plato, que giran juntos. Naranja: bisel. Azul: satelites. Gris: rueda central y esqueleto, fijos. Rosa: plataforma y pedestal.\nESQUEMA de la fase 1, hecho con las medidas del programa: todavia no es el modelo de Fusion.', ha='center', fontsize=11)
plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.1, wspace=0.02)
plt.savefig(os.path.join(sal, 'caja-esquema-corte.png'), dpi=70); plt.close()
print('figuras en', sal)
