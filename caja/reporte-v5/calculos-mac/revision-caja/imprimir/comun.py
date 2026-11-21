# Revision de imprimibilidad de la caja v5. Utilidades comunes.
#   - construye los solidos del modelo (manifold3d) y los coloca como dice la tabla del apartado 5 del reporte
#   - corta en capas de 0,2 mm y pasa cada capa a shapely
import os, sys, math, functools
import numpy as np
import shapely
from shapely.geometry import Polygon, MultiPolygon, Point, LineString, box
from shapely.ops import unary_union

AQUI = os.path.dirname(os.path.abspath(__file__))
REV = os.path.dirname(AQUI)
sys.path.insert(0, REV)
import caja_piezas_v5 as CP, caja_diseno_v5 as D

CAPA = 0.2
EPS_Z = 1e-3            # se corta un pelo por encima de la mitad de la capa, para no caer justo en una cara horizontal

# como se imprime cada pieza segun la tabla del apartado 5 del reporte (True = boca abajo: media vuelta sobre X)
ORIENT = {
    'base': False, 'tubo': False, 'cuerpo': True, 'funda': True, 'frase': True, 'plataforma': False, 'bisel': True,
    'plato': False, 'marco': False, 'satelite_1': False, 'teton': False, 'pasador_derecho': False, 'soporte': False,
    'rueda_central': True, 'puerta_derecha': True, 'puerta_izquierda': True, 'meseta': False, 'aro_puertas': False,
    'probeta_anillo': True, 'probeta_teton': False,      # estas dos no estan en la tabla: postura sacada de los .3mf (tresmf.py): el anillo boca abajo y el teton CON EL POMO ARRIBA
}

@functools.lru_cache(None)
def modelo():
    p, d, d2, P = CP.piezas()
    S = {n: CP.solido(q.ops) for n, q in P.items()}
    return p, d, d2, P, S

def colocada(nombre, boca_abajo=None, S=None):
    """El solido en su postura de impresion, con z minimo = 0. Devuelve (solido, funcion que pasa de coordenadas de impresion a coordenadas de la pieza)."""
    if S is None: S = modelo()[4]
    s = S[nombre] if isinstance(nombre, str) else nombre
    if boca_abajo is None: boca_abajo = ORIENT[nombre]
    if boca_abajo:
        s = s.rotate([180, 0, 0])            # (x, y, z) -> (x, -y, -z)
    z0 = s.bounding_box()[2]
    s = s.translate([0, 0, -z0])
    if boca_abajo:
        inv = lambda x, y, z: (x, -y, -(z + z0))
    else:
        inv = lambda x, y, z: (x, y, z + z0)
    return s, inv

def a_shapely(cs):
    """CrossSection de manifold -> geometria shapely (regla par-impar)."""
    anillos = [np.asarray(c) for c in cs.to_polygons()]
    pols = []
    for a in anillos:
        if len(a) >= 3:
            q = Polygon(a)
            if not q.is_valid: q = q.buffer(0)
            if q.area > 1e-9: pols.append(q)
    if not pols: return Polygon()
    if len(pols) == 1: return pols[0]
    g = shapely.symmetric_difference_all(pols)
    if not g.is_valid: g = g.buffer(0)
    return g

def capas(s, capa=CAPA):
    """Lista de (z medio, geometria) de abajo arriba."""
    z1 = s.bounding_box()[5]
    n = int(math.ceil((z1 - 1e-6) / capa))
    out = []
    for i in range(n):
        z = (i + 0.5) * capa + EPS_Z
        if z >= z1: z = (i * capa + z1) / 2
        out.append((z, a_shapely(s.slice(z))))
    return out

def trozos(g, amin=1e-6):
    if g.is_empty: return []
    gs = list(g.geoms) if hasattr(g, 'geoms') else [g]
    return [q for q in gs if q.geom_type == 'Polygon' and q.area > amin]

def abrir(g, r):
    """Encoger y ensanchar r (con esquinas vivas): lo que queda es lo que tiene mas de 2r de ancho."""
    return g.buffer(-r, join_style=2, mitre_limit=5).buffer(r, join_style=2, mitre_limit=5)

def muestras(c, paso):
    """Puntos dentro de un poligono: una rejilla y un punto seguro."""
    x0, y0, x1, y1 = c.bounds
    pts = [c.representative_point()]
    nx = max(1, int((x1 - x0) / paso)); ny = max(1, int((y1 - y0) / paso))
    nx, ny = min(nx, 14), min(ny, 14)
    xs = np.linspace(x0, x1, nx + 2)[1:-1]; ys = np.linspace(y0, y1, ny + 2)[1:-1]
    cand = shapely.points(*np.meshgrid(xs, ys)).ravel()
    dentro = shapely.contains(c, cand)
    pts += list(cand[dentro])
    return pts

def alcance(c, apoyo):
    """Lo mas lejos que queda un punto de c del apoyo (la capa de debajo)."""
    if apoyo.is_empty: return float('inf')
    pts = [Point(xy) for xy in c.exterior.coords] + muestras(c, 0.5)
    return float(max(shapely.distance(np.array(pts, dtype=object), apoyo)))

def puente(c, apoyo, lmax=120.0, paso_ang=15):
    """Mira si un trozo sin apoyo es un puente. Devuelve (luz con una sola direccion, luz punto a punto, fraccion de puntos con puente).
    luz con una sola direccion: la menor, entre todas las direcciones, de la cuerda mas larga apoyada en los dos extremos (inf si en ninguna direccion lo estan todos los puntos)."""
    if apoyo.is_empty: return float('inf'), float('inf'), 0.0
    x0, y0, x1, y1 = c.bounds
    cerca = apoyo.intersection(box(x0 - lmax, y0 - lmax, x1 + lmax, y1 + lmax))
    if cerca.is_empty: return float('inf'), float('inf'), 0.0
    pts = muestras(c, max(0.4, max(x1 - x0, y1 - y0) / 8))
    angs = np.radians(np.arange(0, 180, paso_ang))
    cuerdas = np.full((len(pts), len(angs)), np.inf)
    for i, pt in enumerate(pts):
        for j, a in enumerate(angs):
            u = (math.cos(a), math.sin(a)); ds = []
            for sg in (1, -1):
                ray = LineString([(pt.x, pt.y), (pt.x + sg * lmax * u[0], pt.y + sg * lmax * u[1])])
                it = ray.intersection(cerca)
                if it.is_empty: ds = None; break
                ds.append(pt.distance(it))
            if ds: cuerdas[i, j] = ds[0] + ds[1]
    una = float(cuerdas.max(axis=0).min())
    por_punto = cuerdas.min(axis=1)
    frac = float(np.isfinite(por_punto).mean())
    pp = float(por_punto[np.isfinite(por_punto)].max()) if frac > 0 else float('inf')
    return una, pp, frac
