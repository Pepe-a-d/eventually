# Abre los nueve .3mf de las probetas (exportados desde Fusion) y los compara con el modelo de manifold.
#   cuerpos, estanqueidad, volumen, caja envolvente, z minimo, orientacion (que cara toca la cama), separacion entre cuerpos
#   y volumen de la diferencia simetrica con la pieza del modelo colocada igual.
# Uso:  python -I tresmf.py     (los .3mf se leen como datos: solo se interpreta el XML)
import sys, os, glob, zipfile, math, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xml.etree.ElementTree as ET
import numpy as np
import trimesh
import manifold3d as mf
from comun import *

CARPETA = '<repositorio>/caja/probetas-v5'
NS = '{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'

def lee_3mf(fn):
    """Lista de (nombre, vertices, triangulos) ya con la transformacion de la bandeja aplicada."""
    z = zipfile.ZipFile(fn)
    raiz = ET.fromstring(z.read('3D/3dmodel.model'))
    unidad = raiz.get('unit', 'millimeter')
    objs = {}
    for o in raiz.iter(NS + 'object'):
        m = o.find(NS + 'mesh')
        if m is None:
            objs[o.get('id')] = ('componentes', o); continue
        V = np.array([[float(v.get('x')), float(v.get('y')), float(v.get('z'))] for v in m.find(NS + 'vertices')])
        T = np.array([[int(t.get('v1')), int(t.get('v2')), int(t.get('v3'))] for t in m.find(NS + 'triangles')])
        objs[o.get('id')] = (o.get('name'), V, T)
    out = []
    for it in raiz.find(NS + 'build'):
        ob = objs[it.get('objectid')]
        assert ob[0] != 'componentes', 'objeto con componentes: no previsto'
        nombre, V, T = ob
        tr = it.get('transform')
        if tr:
            a = np.array([float(x) for x in tr.split()]).reshape(4, 3)
            V = V @ a[:3] + a[3]
        out.append((nombre, V, T))
    return unidad, out

def aristas(m):
    """(aristas con una sola cara, aristas con mas de dos caras) despues de soldar vertices iguales."""
    e = np.sort(m.edges, axis=1)
    _, cuenta = np.unique(e, axis=0, return_counts=True)
    return int((cuenta == 1).sum()), int((cuenta > 2).sum())

def a_manifold(m):
    mesh = mf.Mesh(vert_properties=np.asarray(m.vertices, dtype=np.float32), tri_verts=np.asarray(m.faces, dtype=np.uint32))
    try: mesh.merge()
    except Exception: pass
    s = mf.Manifold(mesh)
    return s if s.status() == mf.Error.NoError and s.num_tri() > 0 else None

def candidatos():
    """Cada pieza del modelo en las dos posturas (de pie y boca abajo), con z minimo 0."""
    p, d, d2, P, S = modelo()
    out = []
    for n, s in S.items():
        if n in ('reloj_de_pega',): continue
        for ba in (False, True):
            c, _ = colocada(s, ba)
            out.append((n, ba, c))
    return out

def centra(s, bb):
    """Mueve s para que el centro en planta y el z minimo de su caja coincidan con los de bb."""
    b = s.bounding_box()
    return s.translate([(bb[0] + bb[3]) / 2 - (b[0] + b[3]) / 2, (bb[1] + bb[4]) / 2 - (b[1] + b[4]) / 2, bb[2] - b[2]])

def cortes_trimesh(m, zs):
    """Area de la seccion de una malla (aunque no sea variedad) a varias alturas."""
    from shapely.ops import unary_union
    out = []
    for z in zs:
        try:
            sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
            if sec is None: out.append(0.0); continue
            pl, _ = sec.to_2D() if hasattr(sec, 'to_2D') else sec.to_planar()
            out.append(float(pl.area))
        except Exception as e:
            out.append(float('nan'))
    return out

if __name__ == '__main__':
    cand = candidatos()
    resumen_json = {}
    for fn in sorted(glob.glob(os.path.join(CARPETA, 'caja-probeta-*.3mf'))):
        unidad, cuerpos = lee_3mf(fn)
        print('=' * 110)
        print('%s   unidad %s   objetos %d' % (os.path.basename(fn), unidad, len(cuerpos)))
        mans = []; todo = []
        for k, (nombre, V, T) in enumerate(cuerpos):
            m = trimesh.Trimesh(V, T, process=True)          # suelda vertices repetidos
            partes = trimesh.graph.connected_components(m.face_adjacency, nodes=np.arange(len(m.faces)), engine='scipy')
            ab, nm = aristas(m)
            bb = np.concatenate([m.bounds[0], m.bounds[1]])
            vol = float(m.volume)
            s = a_manifold(m)
            # a que pieza del modelo se parece: por volumen y caja, y luego por diferencia simetrica
            mejores = []
            for n, ba, c in cand:
                cb = c.bounding_box()
                if abs(c.volume() - vol) > 0.03 * max(vol, 1) + 5: continue
                dims_ok = all(abs((cb[3 + i] - cb[i]) - (bb[3 + i] - bb[i])) < 0.6 for i in range(3))
                ds = None
                if s is not None:
                    cc = centra(c, bb)
                    ds = cc.volume() + s.volume() - 2 * (cc ^ s).volume()
                mejores.append((ds if ds is not None else (0 if dims_ok else 1e9), n, ba, dims_ok, c))
            mejores.sort(key=lambda x: x[0])
            print('  cuerpo %d (%s): %d vertices, %d caras, trozos conexos %d, estanco (trimesh) %s, aristas sueltas %d, aristas con mas de 2 caras %d, variedad para manifold3d: %s' % (
                k + 1, nombre, len(m.vertices), len(m.faces), len(partes), m.is_watertight, ab, nm, 'si' if s is not None else 'NO'))
            print('     caja x %.2f..%.2f  y %.2f..%.2f  z %.2f..%.2f   (%.1f x %.1f x %.1f)   volumen %.1f mm3' % (bb[0], bb[3], bb[1], bb[4], bb[2], bb[5], bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2], vol))
            if not mejores:
                print('     NO SE PARECE A NINGUNA PIEZA DEL MODELO por volumen')
            for ds, n, ba, dims_ok, c in mejores[:4]:
                print('     candidata %-18s %-10s volumen modelo %.1f (%+.2f %%)  caja %s  diferencia simetrica %s' % (
                    n, 'boca abajo' if ba else 'de pie', c.volume(), 100 * (vol - c.volume()) / c.volume(), 'igual' if dims_ok else 'DISTINTA',
                    ('%.1f mm3 (%.2f %% del volumen)' % (ds, 100 * ds / vol)) if s is not None else 'no se puede (no es variedad)'))
            if s is None and mejores:
                # comparacion por cortes: area de la seccion a varias alturas, contra la mejor candidata con caja igual
                zs = list(np.linspace(bb[2] + 0.1, bb[5] - 0.1, 40))
                at = cortes_trimesh(m, zs)
                for ds, n, ba, dims_ok, c in mejores[:4]:
                    if not dims_ok: continue
                    cc = centra(c, bb)
                    am = [cc.slice(z).area() for z in zs]
                    dif = [abs(a - b) for a, b in zip(at, am)]
                    print('     por cortes contra %s %s: diferencia de area media %.2f mm2, maxima %.2f mm2 (a z %.1f; area alli %.0f)' % (n, 'boca abajo' if ba else 'de pie', float(np.nanmean(dif)), float(np.nanmax(dif)), zs[int(np.nanargmax(dif))], am[int(np.nanargmax(dif))]))
            mans.append(s); todo.append((m, bb))
        # la bandeja entera
        allb = np.array([b for _, b in todo])
        x0, y0, z0 = allb[:, 0].min(), allb[:, 1].min(), allb[:, 2].min(); x1, y1, z1 = allb[:, 3].max(), allb[:, 4].max(), allb[:, 5].max()
        print('  BANDEJA: x %.1f..%.1f  y %.1f..%.1f  z %.2f..%.2f  -> ocupa %.1f x %.1f x %.1f mm; %s en 256 x 256 x 256 (margen %.1f y %.1f mm por lado); z minimo de cada cuerpo: %s' % (
            x0, x1, y0, y1, z0, z1, x1 - x0, y1 - y0, z1 - z0, 'CABE' if (x1 - x0 <= 256 and y1 - y0 <= 256 and z1 - z0 <= 256) else 'NO CABE',
            (256 - (x1 - x0)) / 2, (256 - (y1 - y0)) / 2, ' '.join('%.3f' % b[2] for b in allb)))
        for i, j in itertools.combinations(range(len(todo)), 2):
            bi, bj = todo[i][1], todo[j][1]
            sep_caja = max(max(bi[0] - bj[3], bj[0] - bi[3]), max(bi[1] - bj[4], bj[1] - bi[4]), max(bi[2] - bj[5], bj[2] - bi[5]))
            if mans[i] is not None and mans[j] is not None:
                pisa = (mans[i] ^ mans[j]).volume()
                hueco = mans[i].min_gap(mans[j], 12.0)
                if pisa > 1e-3 or hueco < 2.0:
                    print('  CUERPOS %d y %d: se pisan %.2f mm3; separacion minima %.2f mm' % (i + 1, j + 1, pisa, hueco))
            elif sep_caja < 2.0:
                print('  CUERPOS %d y %d: sus cajas quedan a %.2f mm (no se puede medir mejor: alguno no es variedad)' % (i + 1, j + 1, sep_caja))
        seps = []
        for i, j in itertools.combinations(range(len(todo)), 2):
            if mans[i] is not None and mans[j] is not None:
                seps.append(mans[i].min_gap(mans[j], 30.0))
        if seps: print('  separacion minima entre cuerpos de la bandeja: %.2f mm' % min(seps))
