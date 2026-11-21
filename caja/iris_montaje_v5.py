import json, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from shapely.affinity import rotate as srot
j = json.load(open('iris-v5.json', encoding='utf-8')); d = j['d']; P = dict((a[0], a[2]) for a in j['P_DEF']); N = 8
def G(l): return [Polygon(o, h) for o, h in l]
lam0 = Polygon(j['lamina']); E = tuple(j['eje']); T = tuple(j['teton']); s = j['sentido']
def base(ax):
    for w in G(j['pared']):
        x, y = w.exterior.xy; ax.fill(x, y, fc='#d8d8d4', ec='#555', lw=0.6)
        for h in w.interiors:
            x, y = h.xy; ax.fill(x, y, fc='white', ec='#555', lw=0.6)
    for u in G(j['unas']):
        x, y = u.exterior.xy; ax.fill(x, y, fc='#e69500', ec='#a66a00', lw=0.5)
    ax.set_aspect('equal'); ax.set_xlim(-84, 84); ax.set_ylim(-80, 80); ax.axis('off')
def arco(ax, r, a0, a1, c, txt=None, rt=None):
    import numpy as np
    an = np.radians(np.linspace(a0, a1, 40)); ax.plot(r * np.cos(an), r * np.sin(an), c=c, lw=2.2)
    a = math.radians(a1); dx, dy = (-math.sin(a), math.cos(a)) if a1 > a0 else (math.sin(a), -math.cos(a))
    ax.annotate('', (r * math.cos(a) + dx * 4, r * math.sin(a) + dy * 4), (r * math.cos(a), r * math.sin(a)), arrowprops=dict(arrowstyle='-|>', color=c, lw=2.2, mutation_scale=22))
fig, axs = plt.subplots(1, 3, figsize=(19.5, 7))
ax = axs[0]; base(ax)
from shapely.ops import unary_union
L = [srot(lam0, 360 / N * k, origin=(0, 0)) for k in range(N)]
for k in range(N):
    vis = L[k].difference(unary_union([L[(k + i) % N] for i in (1, 2, 3)]))          # lo que no tapan las tres siguientes
    for q in (vis.geoms if hasattr(vis, 'geoms') else [vis]):
        x, y = q.exterior.xy; ax.fill(x, y, fc='#5b74c9' if k == 0 else ('#c9ced6' if k % 2 else '#aeb6c2'), ec='#222', lw=0.8, zorder=3)
    e = srot(Point(E), 360 / N * k, origin=(0, 0)); ax.plot(e.x, e.y, 'o', c='white', mec='k', ms=6, zorder=20)
    t = srot(Point(T), 360 / N * k, origin=(0, 0)); ax.plot(t.x, t.y, 'o', c='k', ms=5, zorder=20)
    c = (56 * math.cos(math.radians(45 * k + 10)), 56 * math.sin(math.radians(45 * k + 10)))
    ax.text(c[0], c[1], str(k + 1), fontsize=17, weight='bold', ha='center', va='center', zorder=30, color='white' if k == 0 else 'k')
arco(ax, 73, 5, 60, '#c00')
ax.text(0, 0, 'Se colocan\nen este orden,\nen sentido contrario\na las agujas del reloj', ha='center', va='center', fontsize=11)
ax.set_title('1. Las láminas: agujero en el poste, tetón arriba', fontsize=14)
ax.text(0, -79, 'Punto blanco: poste. Punto negro: tetón.\nLa 7 y la 8 llevan la punta POR DEBAJO de la 1 y la 2.', ha='center', va='top', fontsize=11)
ax = axs[1]; base(ax)
for a in G(j['aro']):
    x, y = a.exterior.xy; ax.fill(x, y, fc='#1f3fa8', alpha=0.75, ec='#0b1f66', lw=0.8)
    for h in a.interiors:
        x, y = h.xy; ax.fill(x, y, fc='white', ec='#0b1f66', lw=0.8)
for k in range(N):
    t = srot(Point(T), 360 / N * k, origin=(0, 0)); ax.plot(t.x, t.y, 'o', c='k', ms=5, zorder=20)
oa = j['orejeta_ang']
ax.annotate('orejeta, en el hueco\nde la pared', (78 * math.cos(math.radians(oa)), 78 * math.sin(math.radians(oa))), xytext=(70, -62), fontsize=11, ha='center', arrowprops=dict(arrowstyle='-', lw=0.8))
arco(ax, 80, oa - 6, oa - 22, '#c00')
ax.set_xlim(-84, 100); ax.text(86, -8, 'cerrar', color='#c00', fontsize=12, ha='center')
ax.text(0, 0, 'Cara de la cama\nhacia abajo', ha='center', va='center', fontsize=11)
ax.set_title('2. El aro: cada ranura en su tetón', fontsize=14)
ax.text(0, -79, 'Con las láminas abiertas, pegadas a la pared.\nPara cerrar el iris, la orejeta va en el sentido de las agujas.', ha='center', va='top', fontsize=11)
ax = axs[2]; base(ax)
g = j['giro_tapa']
for a in G(j['tapa_borde']):
    a = srot(a, -s * g, origin=(0, 0)); x, y = a.exterior.xy; ax.fill(x, y, fc='#f6f5f0', ec='#333', lw=0.9, alpha=0.93)
    for h in a.interiors:
        x, y = h.xy; ax.fill(x, y, fc='white', ec='#333', lw=0.9)
for u in G(j['unas']):
    x, y = u.exterior.xy; ax.fill(x, y, fc='#e69500', ec='#a66a00', lw=0.5, zorder=10)
c0 = max(math.degrees(math.atan2(u.centroid.y, u.centroid.x)) for u in G(j['unas']) if u.centroid.y > 0 and u.centroid.x > 0)
ax.annotate('uña de la pared, dentro\ndel rebaje de la tapa', (65 * math.cos(math.radians(c0)), 65 * math.sin(math.radians(c0))), xytext=(62, -64), fontsize=11, ha='center', arrowprops=dict(arrowstyle='-', lw=0.8), zorder=30)
arco(ax, 52, 150, 110, '#c00')
ax.text(-22, 26, 'girar hasta\nel tope', color='#c00', fontsize=12, ha='center')
ax.text(0, 0, 'Cara de la cama\nhacia abajo', ha='center', va='center', fontsize=11)
ax.set_title('3. La tapa: se deja caer y se gira', fontsize=14)
ax.text(0, -79, 'Los cuatro rebajes de la tapa, sobre las cuatro uñas naranjas.\nSe gira un poco (13°) en el sentido de las agujas del reloj.', ha='center', va='top', fontsize=11)
plt.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.1, wspace=0.03)
plt.savefig('/home/claude/work/iris/capturas/iris-montaje.png', dpi=75)
