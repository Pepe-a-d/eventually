# 5. Los nueve .3mf de las probetas: que piezas llevan, orientacion, mallas. Se leen a mano (XML) y se miden con trimesh y manifold3d.
import sys, glob, os, json, zipfile, re
import xml.etree.ElementTree as ET
import numpy as np, trimesh, manifold3d as mf
from comun import S, P, bb
R = '<repositorio>/caja/'
NS = '{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
def lee(fn):
    z = zipfile.ZipFile(fn); root = ET.fromstring(z.read('3D/3dmodel.model'))
    out = []
    for ob in root.iter(NS + 'object'):
        me = ob.find(NS + 'mesh')
        v = np.array([[float(q.get('x')), float(q.get('y')), float(q.get('z'))] for q in me.find(NS + 'vertices')])
        t = np.array([[int(q.get('v1')), int(q.get('v2')), int(q.get('v3'))] for q in me.find(NS + 'triangles')])
        out.append((ob.get('name'), v, t))
    items = [(it.get('objectid'), it.get('transform')) for it in root.iter(NS + 'item')]
    comps = list(root.iter(NS + 'component'))
    return out, items, comps
def a_cama(m, boca_abajo):
    if boca_abajo: m = m.rotate([180, 0, 0])
    b = m.bounding_box(); return m.translate([-(b[0]+b[3])/2, -(b[1]+b[4])/2, -b[2]])
V = {n: S[n].volume() for n in S}
for fn in sorted(glob.glob(R + 'probetas-v5/caja-probeta-*.3mf')):
    objs, items, comps = lee(fn)
    print('==', os.path.basename(fn), ' objetos %d, items %d (con transform: %d), componentes %d' % (len(objs), len(items), sum(1 for i in items if i[1]), len(comps)))
    allv = np.vstack([o[1] for o in objs]); print('   bandeja: x %.1f..%.1f  y %.1f..%.1f  z %.2f..%.2f' % (allv[:,0].min(), allv[:,0].max(), allv[:,1].min(), allv[:,1].max(), allv[:,2].min(), allv[:,2].max()))
    cajas = []
    for name, v, t in objs:
        m = trimesh.Trimesh(v, t, process=True)
        e = np.sort(m.edges, axis=1); _, cnt = np.unique(e, axis=0, return_counts=True)
        vol = abs(m.volume); ext = m.extents
        cand = sorted(V, key=lambda n: abs(V[n] - vol) / V[n])[:1][0]
        cajas.append(m.bounds)
        # comparacion solida con la pieza del programa, de pie y boca abajo
        txt = ''
        try:
            mm = mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, dtype=np.float32), tri_verts=np.asarray(m.faces, dtype=np.uint32)))
            ok_m = mm.status() == mf.Error.NoError and mm.volume() > 0
        except Exception as ex:
            ok_m = False
        if ok_m:
            b = mm.bounding_box(); mm0 = mm.translate([-(b[0]+b[3])/2, -(b[1]+b[4])/2, -b[2]])
            res = {}
            for ba in (False, True):
                ref = a_cama(S[cand], ba); res[ba] = (mm0 - ref).volume() + (ref - mm0).volume()
            mejor = min(res, key=res.get); txt = 'dif. simetrica con %s %s: %.1f mm3 (%.2f %%); al reves seria %.1f' % (cand, 'BOCA ABAJO' if mejor else 'de pie', res[mejor], 100 * res[mejor] / V[cand], res[not mejor])
        else:
            txt = 'malla no valida para manifold3d (no se puede comparar solido a solido)'
        zmin = m.bounds[0][2]; tri = m.triangles; abajo = (np.abs(tri[:, :, 2] - zmin).max(1) < 1e-3); area_cama = m.area_faces[abajo].sum()
        print('   %-7s vol %10.1f  ext %-22s z0 %.3f ~ %-17s (dif vol %+.2f%%) estanca %-5s aristas>2caras %d sueltas %d  area cama %.0f mm2' % (name, vol, np.round(ext, 2), zmin, cand, 100*(vol-V[cand])/V[cand], m.is_watertight, int((cnt > 2).sum()), int((cnt == 1).sum()), area_cama))
        print('           ', txt)
    # separacion entre cuerpos en la bandeja
    for i in range(len(cajas)):
        for j in range(i+1, len(cajas)):
            a, b = cajas[i], cajas[j]
            sep = max(max(a[0][k] - b[1][k], b[0][k] - a[1][k]) for k in range(2))
            if sep < 2.0: print('      OJO: cuerpos %d y %d a %.2f mm (cajas) en la bandeja' % (i+1, j+1, sep))
