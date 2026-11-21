# Eventually, caja v5 (puertas y ascensor): construye en Fusion la caja entera.
#
# No tiene medidas propias. Todas salen de caja_diseno_v5.py (la lista de medidas, con las del reloj arriba) y de
# caja_piezas_v5.py, que escribe caja-v5-piezas.json: cada pieza como una lista de operaciones sencillas
# (prisma, cilindro, cono, esfera, giro y helice) que se suman o se restan. Este programa las repite en Fusion.
#
# Para cambiar una medida:  1) se cambia en caja_diseno_v5.py   2) python3 caja_piezas_v5.py   3) se vuelve a lanzar esto.
#
# Uso, desde la consola de Fusion o por el conector:
#     g = {'__file__': RUTA, '__name__': 'generador_caja'}; exec(compile(open(RUTA, encoding='utf-8').read(), RUTA, 'exec'), g)
#     g['main']()                       # todo de una vez (tarda varios minutos)
# o por partes:  g['empieza']();  g['construye'](['base', 'tubo']);  ...;  g['monta']();  g['comprobar']([0, 45, 76, 345])
import adsk.core as C, adsk.fusion as F, math, json, os, time

CARPETA = os.path.dirname(os.path.abspath(globals().get('__file__', '.')))
K = 0.1          # mm -> cm (unidad interna de Fusion)
J = {}           # lo que trae caja-v5-piezas.json
S = {}           # cada pieza, construida, en su sitio con la caja cerrada
AVISOS = []

def app(): return C.Application.get()
def des(): return F.Design.cast(app().activeProduct)
_TM = []
def T():
    # Se guarda el gestor: despues de una operacion fallida, volver a pedirlo repite el error antiguo.
    if not _TM:
        _TM.append(F.TemporaryBRepManager.get())
    return _TM[0]
def pt(x, y, z): return C.Point3D.create(x * K, y * K, z * K)
def vec(x, y, z): return C.Vector3D.create(x, y, z)
def copia(b): return T().copy(b)
def cut(a, b):
    T().booleanOperation(a, b, F.BooleanTypes.DifferenceBooleanType); return a
def join(a, b):
    T().booleanOperation(a, b, F.BooleanTypes.UnionBooleanType); return a
def transforma(body, m):
    T().transform(body, m); return body
def m_giro(deg, eje=(0, 0, 1), centro=(0, 0, 0)):
    m = C.Matrix3D.create(); m.setToRotation(math.radians(deg), vec(*eje), pt(*centro)); return m
def m_mueve(dx, dy, dz):
    m = C.Matrix3D.create(); m.translation = C.Vector3D.create(dx * K, dy * K, dz * K); return m

# ---------------------------------------------------------------- las seis operaciones
def _aux():
    occ = des().rootComponent.occurrences.addNewComponent(C.Matrix3D.create())
    occ.component.name = '_aux'
    return occ, occ.component

def _caras(comp, polys, punto):
    """Mete en el componente una cara plana por poligono. punto(a, b) da el punto 3D de cada vertice."""
    def wire(ring):
        pts = []
        for a, b in ring:
            q = (round(a, 4), round(b, 4))
            if not pts or q != pts[-1]:
                pts.append(q)
        if pts[0] == pts[-1]:
            pts.pop()
        q3 = [punto(a, b) for a, b in pts]
        return T().createWireFromCurves([C.Line3D.create(q3[i], q3[(i + 1) % len(q3)]) for i in range(len(q3))], False)[0]
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for outer, holes in polys:
        comp.bRepBodies.add(T().createFaceFromPlanarWires([wire(outer)] + [wire(h) for h in holes]), bf)
    bf.finishEdit()
    caras = C.ObjectCollection.create()
    for b in comp.bRepBodies:
        caras.add(b.faces.item(0))
    return caras

def _recoge(feat, occ):
    out = None
    for b in feat.bodies:
        c = copia(b)
        out = c if out is None else join(out, c)
    occ.deleteMe()
    return out

def prisma(polys, c0, c1, eje='z'):
    """Poligonos planos extruidos de c0 a c1. eje 'z': puntos (x, y). eje 'y': puntos (x, z). eje 'x': puntos (y, z)."""
    if eje == 'y':
        c0, c1 = -c1, -c0
    cm = (c0 + c1) / 2.0
    occ, comp = _aux()
    caras = _caras(comp, polys, lambda a, b: pt(a, b, cm))
    inp = comp.features.extrudeFeatures.createInput(caras, F.FeatureOperations.NewBodyFeatureOperation)
    inp.setSymmetricExtent(C.ValueInput.createByReal(abs(c1 - c0) * K), True)
    out = _recoge(comp.features.extrudeFeatures.add(inp), occ)
    if eje != 'z':
        m = C.Matrix3D.create()
        if eje == 'y':        # (a, b, c) -> (a, -c, b)
            m.setWithCoordinateSystem(pt(0, 0, 0), vec(1, 0, 0), vec(0, 0, 1), vec(0, -1, 0))
        else:                 # (a, b, c) -> (c, a, b)
            m.setWithCoordinateSystem(pt(0, 0, 0), vec(0, 1, 0), vec(0, 0, 1), vec(1, 0, 0))
        transforma(out, m)
    return out

def revol(perfil, a0, a1):
    """Perfil (radio, z) girado alrededor del eje Z, del angulo a0 al a1."""
    ang = a1 - a0
    occ, comp = _aux()
    caras = _caras(comp, [(perfil, [])], lambda r, z: pt(r, 0, z))
    inp = comp.features.revolveFeatures.createInput(caras.item(0), comp.zConstructionAxis, F.FeatureOperations.NewBodyFeatureOperation)
    if ang >= 359.999:
        inp.setAngleExtent(False, C.ValueInput.createByReal(2 * math.pi))
    else:
        inp.setAngleExtent(True, C.ValueInput.createByReal(math.radians(ang) / 2.0))      # simetrico (asi no depende del sentido); Fusion pide el angulo de cada lado
    out = _recoge(comp.features.revolveFeatures.add(inp), occ)
    return transforma(out, m_giro(a0 + (0.0 if ang >= 359.999 else ang / 2.0)))

def helice(polys, z0, z1, giro):
    """Poligonos en planta que suben de z0 a z1 girando 'giro' grados alrededor del eje Z (positivo: contra el reloj, visto desde arriba)."""
    def una(signo):
        occ, comp = _aux()
        caras = _caras(comp, polys, lambda a, b: pt(a, b, z0))
        sk = comp.sketches.add(comp.xZConstructionPlane)
        linea = sk.sketchCurves.sketchLines.addByTwoPoints(sk.modelToSketchSpace(pt(0, 0, z0)), sk.modelToSketchSpace(pt(0, 0, z1)))
        path = comp.features.createPath(linea)
        inp = comp.features.sweepFeatures.createInput(caras, path, F.FeatureOperations.NewBodyFeatureOperation)
        inp.twistAngle = C.ValueInput.createByReal(signo * math.radians(giro))
        return _recoge(comp.features.sweepFeatures.add(inp), occ)
    # punto de prueba: el centro del primer poligono, a media altura, girado medio giro. Tiene que caer dentro.
    ring = polys[0][0]
    cx = sum(q[0] for q in ring) / len(ring); cy = sum(q[1] for q in ring) / len(ring)
    a = math.radians(giro / 2.0)
    prueba = pt(cx * math.cos(a) - cy * math.sin(a), cx * math.sin(a) + cy * math.cos(a), (z0 + z1) / 2.0)
    for signo in (1.0, -1.0):
        b = una(signo)
        if b.pointContainment(prueba) == F.PointContainment.PointInsidePointContainment:
            return b
    raise RuntimeError('helice: el barrido no pasa por donde debe')

def op_solido(o):
    t = o['t']
    if t == 'prisma': return prisma(o['pol'], o['c0'], o['c1'], o['eje'])
    if t == 'cil': return T().createCylinderOrCone(pt(*o['a']), o['r'] * K, pt(*o['b']), o['r'] * K)
    if t == 'cono': return T().createCylinderOrCone(pt(*o['a']), o['ra'] * K, pt(*o['b']), o['rb'] * K)
    if t == 'esfera': return T().createSphere(pt(*o['c']), o['r'] * K)
    if t == 'revol': return revol(o['perfil'], o['a0'], o['a1'])
    if t == 'helice': return helice(o['pol'], o['z0'], o['z1'], o['giro'])
    raise ValueError(t)

def pieza(nombre):
    """Construye una pieza y compara su volumen con el que calculo caja_piezas_v5.py (que redondea los cilindros a 48 caras)."""
    pz = J['piezas'][nombre]
    body = None
    for i, o in enumerate(pz['ops']):
        s = op_solido(o)
        try:
            body = s if body is None else (join(body, s) if o['op'] == '+' else cut(body, s))
        except RuntimeError as e:
            # caras o aristas que coinciden: se repite moviendo la herramienta unas milesimas, de varias maneras, hasta que Fusion sabe hacerlo
            hecho = False
            for nombre_m, mm in (('una milesima en diagonal', m_mueve(0.001, 0.001, 0.001)), ('4 milesimas hacia arriba', m_mueve(0, 0, 0.004)), ('4 milesimas hacia abajo', m_mueve(0, 0, -0.004)),
                                 ('6 milesimas de grado', m_giro(0.006)), ('6 milesimas de grado al reves', m_giro(-0.006)), ('una centesima hacia arriba', m_mueve(0, 0, 0.01))):
                try: F.TemporaryBRepManager.get()
                except RuntimeError: pass
                try:
                    s = transforma(op_solido(o), mm)
                    body = join(body, s) if o['op'] == '+' else cut(body, s)
                    AVISOS.append('%s, operacion %d (%s): repetida desplazando la herramienta %s' % (nombre, i, o['t'], nombre_m)); hecho = True; break
                except RuntimeError as e2:
                    e = e2
            if not hecho:
                raise RuntimeError('%s, operacion %d (%s): %s' % (nombre, i, o['t'], str(e).split('\n')[0]))
    v = body.volume * 1000
    dif = abs(v - pz['volumen']) / pz['volumen']
    if dif > 0.012:
        raise RuntimeError('%s: volumen %.1f mm3 en Fusion y %.1f en el programa' % (nombre, v, pz['volumen']))
    return body, v

# ---------------------------------------------------------------- montaje y movimiento
def mov(tau):
    """(lo que ha corrido el teton, giro del aro, angulo de las puertas, altura de la plataforma) para un giro de tubo."""
    tau = min(max(tau, 0.0), J['cte']['giro_tubo'])
    i = int(math.floor(tau)); f = tau - i
    a = J['mov'][i]; b = J['mov'][min(i + 1, len(J['mov']) - 1)]
    return [a[k] + (b[k] - a[k]) * f for k in range(4)]

def puesta(nombre, tau):
    """Copia de una pieza colocada como esta cuando el tubo ha girado 'tau' grados."""
    c = J['cte']; mu = J['piezas'][nombre]['mueve']; b = copia(S[nombre])
    s, psi, ang, h = mov(tau)
    if mu in ('fijo', 'funda', 'probeta') or tau == 0: return b
    if mu == 'tubo': return transforma(b, m_giro(c['ROT'] * tau))
    if mu == 'bisel': return transforma(b, m_giro(c['ROT'] * tau / c['relacion']))
    if mu == 'plataforma': return transforma(b, m_mueve(0, 0, h))
    if mu == 'aro': return transforma(b, m_giro(c['aro_sentido'] * psi))
    if mu == 'teton': return transforma(b, m_mueve(0, -s, 0))
    if mu in ('puerta_derecha', 'puerta_izquierda'):
        sx = 1 if mu == 'puerta_derecha' else -1
        return transforma(b, m_giro(sx * ang, (0, 1, 0), (sx * c['eje_x'], 0, c['eje_z'])))
    if mu.startswith('satelite'):
        th = math.radians(float(mu.split(':')[1])); cx, cy = c['r_ejes'] * math.cos(th), c['r_ejes'] * math.sin(th)
        dth = c['ROT'] * tau
        transforma(b, m_giro(dth * c['z_central'] / c['z_satelite'], (0, 0, 1), (cx, cy, 0)))
        return transforma(b, m_giro(dth))
    raise ValueError(mu)

def put(name, bodies):
    """Pone uno o varios cuerpos en un componente nuevo con ese nombre."""
    if not isinstance(bodies, (list, tuple)):
        bodies = [bodies]
    root = des().rootComponent
    for o in [o for o in root.occurrences if o.component.name == name]:
        o.deleteMe()
    occ = root.occurrences.addNewComponent(C.Matrix3D.create())
    comp = occ.component
    comp.name = name
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for b in bodies:
        comp.bRepBodies.add(b, bf)
    bf.finishEdit()
    for i in range(comp.bRepBodies.count):
        comp.bRepBodies.item(i).name = name if comp.bRepBodies.count == 1 else '%s_%d' % (name, i + 1)
    return occ

def colores():
    d = des()
    lib = app().materialLibraries.itemById('BA5EE55E-9982-449B-9D66-9F036540E140')
    def mk(pid, name, rgb):
        a = d.appearances.itemByName(name)
        if a is None:
            a = d.appearances.addByCopy(lib.appearances.itemById(pid), name)
        for k in range(a.appearanceProperties.count):
            pr = a.appearanceProperties.item(k)
            if pr.objectType == C.ColorProperty.classType():
                C.ColorProperty.cast(pr).value = C.Color.create(rgb[0], rgb[1], rgb[2], 255)
                break
        return a
    ap = {'blanco': mk('Prism-127', 'Eventually - papel', (247, 246, 242)), 'azul': mk('Prism-115', 'Eventually - tinta azul', (31, 63, 168)),
          'gris': mk('Prism-127', 'Eventually - reloj de pega', (150, 156, 165)), 'marmol': mk('Prism-127', 'Eventually - marmol', (222, 219, 212))}
    for o in d.rootComponent.occurrences:
        pz = J['piezas'].get(o.component.name)
        if pz:
            for i in range(o.component.bRepBodies.count):
                o.component.bRepBodies.item(i).appearance = ap[pz['color']]

def parametros():
    """Copia las medidas a los parametros de usuario de Fusion, para poder leerlas alli. Son informativas."""
    ups = des().userParameters; n = 0
    for nombre, unidad, valor, coment in [(q[0], q[1], q[2], q[3] if len(q) > 3 else '') for q in J['P']]:
        u = {'mm': 'mm', 'grados': 'deg'}.get(unidad, '')
        expr = ('%g %s' % (valor, u)).strip()
        try:
            it = ups.itemByName(nombre)
            if it: it.expression = expr
            else: ups.add(nombre, C.ValueInput.createByString(expr), u, coment[:240])
            n += 1
        except RuntimeError:
            pass
    return n

# ---------------------------------------------------------------- pasos
def carga():
    J.clear()
    J.update(json.load(open(os.path.join(CARPETA, 'caja-v5-piezas.json'), encoding='utf-8')))

def empieza(nuevo=True):
    carga()
    if nuevo:
        app().documents.add(C.DocumentTypes.FusionDesignDocumentType)
    des().designIntent = F.DesignIntentTypes.HybridDesignIntentType
    return 'piezas en el fichero: %d' % len(J['piezas'])

def construye(nombres=None, segundos=45):
    """Construye las piezas que falten (o las que se pidan) hasta agotar el tiempo. Devuelve lo hecho y lo que queda."""
    t0 = time.time(); hechas = []
    for n in (nombres or list(J['piezas'])):
        if n in S: continue
        if time.time() - t0 > segundos: break
        t1 = time.time()
        S[n], v = pieza(n)
        hechas.append('%s: %.1f mm3 (programa %.1f), %.0f s' % (n, v, J['piezas'][n]['volumen'], time.time() - t1))
    return hechas, [n for n in J['piezas'] if n not in S]

def monta(tau=0.0, quita=()):
    for n in J['piezas']:
        if n in quita or J['piezas'][n]['mueve'] == 'probeta': continue
        put(n, puesta(n, tau))
    colores()
    app().activeViewport.fit()
    return 'montada con el tubo a %g grados' % tau

def _caja(b):
    bb = b.boundingBox
    return (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z, bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)

def vol_inter(a, b):
    """Volumen (mm3) que comparten dos cuerpos. Si dos caras coinciden y Fusion no sabe, se repite separandolos 2 centesimas."""
    def una(dz):
        c = copia(a)
        if dz: transforma(c, m_mueve(0, 0, dz))
        T().booleanOperation(c, b, F.BooleanTypes.IntersectionBooleanType)
        return c.volume * 1000
    try:
        return una(0.0)
    except RuntimeError as e:
        ultimo = e
    vals = []
    for dz in (0.02, -0.02):
        try: F.TemporaryBRepManager.get()
        except RuntimeError: pass
        try: vals.append(una(dz))
        except RuntimeError as e: ultimo = e
    if not vals:
        raise ultimo
    return min(vals)

def comprobar(taus, segundos=50, desde=0, solo=None):
    """En cada posicion, mira que ninguna pieza pise a otra. Devuelve (lineas, por donde va) para seguir en otra llamada.
    Con solo = {nombres}, mira nada mas las parejas en que entra alguna de esas piezas (para repetir tras cambiar unas pocas)."""
    t0 = time.time(); out = []
    nombres = [n for n in J['piezas'] if J['piezas'][n]['mueve'] not in ('funda', 'probeta')]
    i = desde
    while i < len(taus):
        if time.time() - t0 > segundos: break
        tau = taus[i]
        M = {n: puesta(n, tau) for n in nombres}
        B = {n: _caja(M[n]) for n in nombres}
        peor = (0.0, '', ''); pares = 0
        for ia, a in enumerate(nombres):
            for b in nombres[ia + 1:]:
                if J['piezas'][a]['mueve'] == J['piezas'][b]['mueve'] and i > 0: continue
                if solo and a not in solo and b not in solo: continue
                A_, B_ = B[a], B[b]
                if A_[0] > B_[3] or B_[0] > A_[3] or A_[1] > B_[4] or B_[1] > A_[4] or A_[2] > B_[5] or B_[2] > A_[5]: continue
                v = vol_inter(M[a], M[b]); pares += 1
                if v > peor[0]: peor = (v, a, b)
        s, psi, ang, h = mov(tau)
        out.append('%s  tubo %5.1f  puertas %5.1f  plataforma %5.1f mm  pares mirados %3d  lo que mas se pisa: %.3f mm3%s' % (
            'bien ' if peor[0] <= 0.02 else 'FALLA', tau, ang, h, pares, peor[0], (' (%s y %s)' % (peor[1], peor[2])) if peor[0] > 0.02 else ''))
        i += 1
    return out, i

def exporta_f3d(nombre='Eventually-caja-v5.f3d'):
    fn = os.path.join(CARPETA, nombre)
    em = des().exportManager
    em.execute(em.createFusionArchiveExportOptions(fn))
    return '%s (%d bytes)' % (fn, os.path.getsize(fn))

def exporta_3mf(fichero, cuerpos, sub='probetas-v5'):
    """Escribe un .3mf con uno o varios cuerpos ya orientados como se imprimen."""
    carpeta = os.path.join(CARPETA, sub)
    if not os.path.isdir(carpeta):
        os.makedirs(carpeta)
    occ = put('_exp', cuerpos)
    fn = os.path.join(carpeta, fichero + '.3mf')
    em = des().exportManager
    em.execute(em.createC3MFExportOptions(occ, fn))
    occ.deleteMe()
    return '%s (%d bytes)' % (fn, os.path.getsize(fn))

def a_la_cama(body, boca_abajo=False, dx=0.0, dy=0.0):
    """Copia de una pieza apoyada en Z = 0 como se imprime; boca_abajo la voltea (media vuelta alrededor del eje X)."""
    b = copia(body)
    if boca_abajo:
        transforma(b, m_giro(180.0, (1, 0, 0)))
    bb = b.boundingBox
    return transforma(b, m_mueve(dx - (bb.minPoint.x + bb.maxPoint.x) / 2 / K, dy - (bb.minPoint.y + bb.maxPoint.y) / 2 / K, -bb.minPoint.z / K))

def main():
    out = [empieza()]
    while True:
        hechas, faltan = construye(segundos=3600)
        out += hechas
        if not faltan: break
    out.append(monta())
    return out
