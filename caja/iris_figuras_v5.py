# Figuras del reporte de la probeta del iris. Lee iris-v5.json.   python3 figuras.py <carpeta de salida>
import json, math, sys, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import Polygon, Point
from shapely.affinity import rotate as srot
AQUI = os.path.dirname(os.path.abspath(__file__))
sal = sys.argv[1] if len(sys.argv) > 1 else AQUI
j = json.load(open(os.path.join(AQUI, 'iris-v5.json'), encoding='utf-8')); d = j['d']; P = dict((a[0], a[2]) for a in j['P_DEF']); N = int(P['laminas'])
def G(l): return [Polygon(o, h) for o, h in l]
lam0 = Polygon(j['lamina']); E = tuple(j['eje']); T = tuple(j['teton'])
AZUL = '#1f3fa8'
# --- planta: abierto, a medias, cerrado
fig, axs = plt.subplots(1, 3, figsize=(18, 6.4))
for ax, frac, tit in zip(axs, (0, 0.5, 1), ('Abierto', 'A medio giro', 'Cerrado')):
    g = j['giro_lamina'] * frac
    for w in G(j['pared']):
        x, y = w.exterior.xy; ax.fill(x, y, fc='#d8d8d4', ec='#555', lw=0.6)
        for h in w.interiors:
            x, y = h.xy; ax.fill(x, y, fc='white', ec='#555', lw=0.6)
    for k in range(N):
        for i in G(j['isla']):
            x, y = srot(i, 360 / N * k, origin=(0, 0)).exterior.xy; ax.fill(x, y, fc='#888', ec='none')
    for k in range(N):
        b = srot(srot(lam0, g, origin=E), 360 / N * k, origin=(0, 0))
        x, y = b.exterior.xy; ax.fill(x, y, alpha=0.45 if k else 0.75, fc='#aeb6c2' if k else AZUL, ec='#333', lw=0.6)
        t = srot(srot(Point(T), g, origin=E), 360 / N * k, origin=(0, 0)); ax.plot(t.x, t.y, 'o', c='k', ms=3.5)
        e = srot(Point(E), 360 / N * k, origin=(0, 0)); ax.plot(e.x, e.y, 'o', c='white', mec='k', ms=4)
    t1 = srot(Point(T), g, origin=E)
    ang = math.degrees(math.atan2(t1.y, t1.x)) - math.degrees(math.atan2(T[1], T[0]))
    for a in G(j['aro']):
        a = srot(a, ang, origin=(0, 0)); x, y = a.exterior.xy; ax.plot(x, y, '-', c='#0a7d55', lw=1.1)
        for h in a.interiors:
            x, y = h.xy; ax.plot(x, y, '-', c='#0a7d55', lw=0.9)
    for u in G(j['unas']):
        x, y = u.exterior.xy; ax.fill(x, y, fc='#e69500')
    ax.add_patch(plt.Circle((0, 0), d['RA'], fill=False, ec='#c00', lw=0.9, ls='--'))
    ax.set_aspect('equal'); ax.set_xlim(-80, 80); ax.set_ylim(-72, 72); ax.set_title(tit, fontsize=15); ax.axis('off')
fig.text(0.5, 0.02, 'Visto desde arriba, sin la tapa. Gris: pared y postes. Azul: una lamina. Verde: el aro, con sus ranuras y la orejeta. Naranja: las cuatro uñas de la bayoneta. Rojo a trazos: hueco de 75 mm.', ha='center', fontsize=11)
plt.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.07, wspace=0.02)
plt.savefig(os.path.join(sal, 'iris-planta.png'), dpi=75); plt.close()
# --- corte por un poste
fig, ax = plt.subplots(figsize=(13, 4.6))
Rext, Resc, Rc, RA, Rt = d['R_ext'], d['R_esc'], d['R_c'], d['RA'], d['Rt']
zs, zi, zt, za1, zp0, ztot = d['z_suelo'], d['z_isla'], d['z_techo'], d['z_aro1'], d['z_tapa0'], d['z_total']
def r(x0, x1, z0, z1, c, **kw): ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fc=c, ec='#222', lw=0.7, **kw))
B = '#e9e7e1'
r(RA, Rext, 0, zs, B)                                   # suelo
r(Resc, Rext, zs, ztot, B)                               # pared fina tras el alveolo y banda
r(Rt - P['isla_r'], Resc, zs, zi, B)                     # isla
r(Rt - P['poste_d'] / 2, Rt + P['poste_d'] / 2, zi, zt, B)   # poste
t = P['lamina_grosor']
r(RA + 0.6, Rt - P['poste_d'] / 2 - 0.25, zi, zi + t, '#aeb6c2'); r(Rt + P['poste_d'] / 2 + 0.25, Rt + P['cola_r'], zi, zi + t, '#aeb6c2')
tr = P['teton_radio']; r(tr - 1.5, tr + 1.5, zi + t, zi + t + P['teton_alto'], '#aeb6c2')
r(d['R_aro_in'], tr - 1.75, zt, za1, '#7fbf9f'); r(tr + 1.75, d['R_aro_ext'], zt, za1, '#7fbf9f')
th = P['tapa_holgura']
r(RA, Resc - th - 0.8, zp0, ztot, '#f6f5f0')
for i in range(4): r(Resc - th - 0.8, Resc - th - 0.2 * i, zp0 + 0.2 * i, zp0 + 0.2 * (i + 1), '#f6f5f0')
for i, v in enumerate((0.2, 0.4, 0.6, 0.8)):
    r(Resc - v, Resc, zp0 + 0.2 * (i + 1), zp0 + 0.2 * (i + 2) if i < 3 else ztot, '#e69500')
ax.annotate('plato de abajo', (45, zs / 2), ha='center', va='center', fontsize=9)
ax.annotate('lamina (la cola, en su poste)', (50, zi + t / 2), ha='center', va='center', fontsize=9)
ax.annotate('aro', (55, (zt + za1) / 2), ha='center', va='center', fontsize=9)
ax.annotate('tapa', (50, (zp0 + ztot) / 2), ha='center', va='center', fontsize=9)
ax.annotate('teton', (tr, zi + t + 1.0), xytext=(tr - 2.5, 11.4), fontsize=9, arrowprops=dict(arrowstyle='-', lw=0.6))
ax.annotate('isla y poste', (Rt, 3.0), xytext=(Rt - 8, -2.2), fontsize=9, arrowprops=dict(arrowstyle='-', lw=0.6))
ax.annotate('uña de la bayoneta', (Resc - 0.4, ztot - 0.3), xytext=(Resc - 7, 11.4), fontsize=9, arrowprops=dict(arrowstyle='-', lw=0.6))
ax.annotate('hueco de 75 mm', (RA - 1.2, 5), rotation=90, ha='center', va='center', fontsize=9, color='#c00')
ax.plot([RA, RA], [-1, 11], '--', c='#c00', lw=0.8)
ax.annotate('', (Rext + 1.5, 0), (Rext + 1.5, ztot), arrowprops=dict(arrowstyle='<->', lw=0.7)); ax.annotate('%.1f mm' % ztot, (Rext + 2.0, ztot / 2), fontsize=9, va='center')
ax.set_xlim(RA - 3, Rext + 7); ax.set_ylim(-3, 12.5); ax.set_aspect(1.6); ax.axis('off')
ax.set_title('Corte por un poste, del hueco (izquierda) al canto exterior (derecha). La altura esta exagerada 1,6 veces.', fontsize=11)
plt.tight_layout(); plt.savefig(os.path.join(sal, 'iris-corte.png'), dpi=85); plt.close()
print('figuras en', sal)
