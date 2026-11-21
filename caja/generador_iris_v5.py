# Eventually, caja v5. Probeta 1: el iris. Generador para Autodesk Fusion (BRIEF-v5.md, apartado 11).
#
# Se ejecuta DENTRO de Fusion (API de Python). Lee iris-v5.json, que tiene que estar en la misma carpeta,
# y construye las piezas del iris capa a capa. NO decide ninguna medida: todas salen de iris_diseno_v5.py.
# Para cambiar una medida: se cambia en la lista P_DEF de iris_diseno_v5.py, se ejecuta ese programa
# (python3 iris_diseno_v5.py) y despues se vuelve a ejecutar este.
#
# Lo que hace:
#   main()      crea un documento nuevo, copia los parametros (solo como informacion), monta el iris abierto
#               y comprueba en el modelo las medidas que pide el brief. Devuelve una lista de lineas.
#   exportar()  escribe los .3mf, ya orientados para imprimir, en la subcarpeta probetas-v5.
# No guarda nada en la nube.
#
# Ejes: X e Y en el plano del iris, centro del hueco en (0, 0); Z hacia arriba, la mesa en Z = 0.
import adsk.core as C, adsk.fusion as F, math, json, os

CARPETA = os.path.dirname(os.path.abspath(globals().get('__file__', '.')))
K = 0.1          # mm -> cm (unidad interna de Fusion)
EPS = 0.01       # solape entre capas para que al unirlas no queden caras coincidentes
J = {}

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
def cyl(a, b, r): return T().createCylinderOrCone(pt(*a), r * K, pt(*b), r * K)
def cut(a, b):
    T().booleanOperation(a, b, F.BooleanTypes.DifferenceBooleanType)
    return a
def join(a, b):
    T().booleanOperation(a, b, F.BooleanTypes.UnionBooleanType)
    return a
def copia(b): return T().copy(b)
def rotz(body, deg, c=(0.0, 0.0)):
    m = C.Matrix3D.create()
    m.setToRotation(math.radians(deg), vec(0, 0, 1), pt(c[0], c[1], 0))
    T().transform(body, m)
    return body
def mover(body, dx, dy, dz):
    m = C.Matrix3D.create()
    m.translation = C.Vector3D.create(dx * K, dy * K, dz * K)
    T().transform(body, m)
    return body
def vol_inter(a, b):
    """Volumen (mm3) que comparten dos cuerpos. Si no se tocan devuelve 0. Cuando dos caras coinciden
    exactamente (una pieza apoyada en otra) Fusion a veces no sabe calcularlo: entonces se repite subiendo y
    bajando el primero 2 centesimas y se toma el menor, que es el del lado en que las caras se separan."""
    def una(dz):
        c = copia(a)
        if dz:
            mover(c, 0, 0, dz)
        T().booleanOperation(c, b, F.BooleanTypes.IntersectionBooleanType)
        return c.volume * 1000
    try:
        return una(0.0)
    except RuntimeError as e:
        ultimo = e
    vals = []
    for dz in (0.02, -0.02):
        try:
            F.TemporaryBRepManager.get()                          # vacia el error pendiente
        except RuntimeError:
            pass
        try:
            vals.append(una(dz))
        except RuntimeError as e:
            ultimo = e
    if not vals:
        raise ultimo
    return min(vals)

def prisma(polys, z0, z1):
    """Extruye poligonos planos de z0 a z1. polys = [(contorno, [agujeros])] con puntos (x, y)."""
    zm = (z0 + z1) / 2.0
    def wire(ring):
        pts = []
        for a, b in ring:
            q = (round(a, 4), round(b, 4))
            if not pts or q != pts[-1]:
                pts.append(q)
        if pts[0] == pts[-1]:
            pts.pop()
        q3 = [pt(a, b, zm) for a, b in pts]
        return T().createWireFromCurves([C.Line3D.create(q3[i], q3[(i + 1) % len(q3)]) for i in range(len(q3))], False)[0]
    root = des().rootComponent
    occ = root.occurrences.addNewComponent(C.Matrix3D.create())
    comp = occ.component
    comp.name = '_aux'
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for outer, holes in polys:
        comp.bRepBodies.add(T().createFaceFromPlanarWires([wire(outer)] + [wire(h) for h in holes]), bf)
    bf.finishEdit()
    caras = C.ObjectCollection.create()
    for b in comp.bRepBodies:
        caras.add(b.faces.item(0))
    inp = comp.features.extrudeFeatures.createInput(caras, F.FeatureOperations.NewBodyFeatureOperation)
    inp.setSymmetricExtent(C.ValueInput.createByReal(abs(z1 - z0) * K), True)
    feat = comp.features.extrudeFeatures.add(inp)
    out = None
    for b in feat.bodies:
        c = copia(b)
        out = c if out is None else join(out, c)
    occ.deleteMe()
    return out

def cuerpo(nombre):
    """Construye una pieza de iris-v5.json en sus propias coordenadas (su cara de abajo en Z = 0).
    Prueba primero con las capas solapadas EPS y, si Fusion no consigue unirlas, con otros solapes."""
    pz = J['piezas'][nombre]
    fallo = None
    for eps in (EPS, 0.0, 0.05):
        try:
            body = None
            for i, (z0, z1, polys) in enumerate(pz['capas']):
                b = prisma(polys, z0 - (eps if i else 0.0), z1)
                body = b if body is None else join(body, b)
            for x, y, z0, z1, r, op in pz['cilindros']:
                if op == 'suma':
                    join(body, cyl((x, y, z0 - (0.0 if nombre.startswith('lamina') else 0.05)), (x, y, z1), r))
                else:
                    cut(body, cyl((x, y, z0), (x, y, z1), r))
            if pz.get('dentro_r'):
                T().booleanOperation(body, cyl((0, 0, -5), (0, 0, 60), pz['dentro_r']), F.BooleanTypes.IntersectionBooleanType)
            if pz.get('agujero_r'):
                cut(body, cyl((0, 0, -5), (0, 0, 60), pz['agujero_r']))
            if abs(body.volume * 1000 - pz['volumen']) / pz['volumen'] < 0.01:
                return body
            fallo = 'volumen %.1f en vez de %.1f' % (body.volume * 1000, pz['volumen'])
        except RuntimeError as e:
            fallo = str(e).split('\n')[0]
    raise RuntimeError('no se pudo construir %s: %s' % (nombre, fallo))

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

def carga():
    J.clear()
    J.update(json.load(open(os.path.join(CARPETA, 'iris-v5.json'), encoding='utf-8')))
    J['P'] = {n: v for n, _, v, _ in J['P_DEF']}
    return J

def parametros():
    """Copia P_DEF a los parametros de usuario de Fusion. Son informativos: la geometria sale de iris-v5.json."""
    ups = des().userParameters
    for name, unit, val, com in J['P_DEF']:
        expr = ('%g %s' % (val, unit)).strip()
        u = ups.itemByName(name)
        if u is None:
            ups.add(name, C.ValueInput.createByString(expr), unit, com)
        else:
            u.expression = expr
            u.comment = com
    return len(J['P_DEF'])

# ---------------------------------------------------------------- posiciones
def angulo_aro(giro):
    """Cuanto gira el aro cuando la lamina gira 'giro' grados (la ranura es radial y sigue al teton)."""
    E = J['eje']; t0 = J['teton']
    a = math.radians(giro)
    x, y = t0[0] - E[0], t0[1] - E[1]
    t1 = (E[0] + x * math.cos(a) - y * math.sin(a), E[1] + x * math.sin(a) + y * math.cos(a))
    return math.degrees(math.atan2(t1[1], t1[0]) - math.atan2(t0[1], t0[0]))

def lamina_plana(base, k, giro, z):
    """Lamina k, girada 'giro' sobre su poste, plana, con su cara de abajo a la altura z."""
    b = copia(base)
    rotz(b, giro, J['eje'])
    rotz(b, 360.0 / J['P']['laminas'] * k)
    return mover(b, 0, 0, z)

def lamina_inclinada(base, k, plano, t):
    """Lamina k abierta, inclinada como dice el calculo de apilado: z = a x + b y + c desde el suelo de la camara."""
    a, b_, c = plano
    E = J['eje']
    b = copia(base)
    mover(b, 0, 0, -t / 2.0)
    n = (-a, -b_, 1.0)
    L = math.sqrt(n[0] ** 2 + n[1] ** 2 + 1.0)
    ang = math.acos(1.0 / L)
    if ang > 1e-9:
        m = C.Matrix3D.create()
        m.setToRotation(ang, vec(-n[1], n[0], 0), pt(E[0], E[1], 0))
        T().transform(b, m)
    mover(b, 0, 0, J['d']['z_suelo'] + a * E[0] + b_ * E[1] + c)
    return rotz(b, 360.0 / J['P']['laminas'] * k)

def piezas_sueltas():
    return {n: cuerpo(n) for n in ('base', 'aro', 'tapa', 'lamina_A', 'lamina_B')}

def montaje(S):
    """Cuerpos en su sitio, con el iris abierto y el juego A de laminas."""
    d = J['d']; N = int(J['P']['laminas'])
    M = {'base': copia(S['base']), 'aro': mover(copia(S['aro']), 0, 0, d['z_techo']), 'tapa': mover(copia(S['tapa']), 0, 0, d['z_tapa0'])}
    plano = J['planos']['A'][0][2]
    for k in range(N):
        M['lamina_%d' % (k + 1)] = lamina_inclinada(S['lamina_A'], k, plano, J['P']['lamina_grosor'])
    return M

def juego_b(S):
    """Las laminas de 0,8 mm en su sitio, abiertas e inclinadas (no se dejan en el documento; solo para comprobar)."""
    plano = J['planos']['B'][0][2]
    return [lamina_inclinada(S['lamina_B'], k, plano, J['P']['lamina_grosor_b']) for k in range(int(J['P']['laminas']))]

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
    papel = mk('Prism-127', 'Eventually - papel', (247, 246, 242))
    gris = mk('Prism-127', 'Eventually - lamina', (206, 211, 218))
    azul = mk('Prism-115', 'Eventually - tinta azul', (31, 63, 168))
    for o in d.rootComponent.occurrences:
        n = o.component.name
        ap = azul if n == 'aro' else (gris if n.startswith('lamina') else papel)
        for i in range(o.component.bRepBodies.count):
            o.component.bRepBodies.item(i).appearance = ap

# ---------------------------------------------------------------- comprobaciones en el modelo
def comprobar(S, M):
    d = J['d']; P = J['P']; N = int(P['laminas']); s = J['sentido']
    out = []
    def linea(ok, txt):
        out.append(('bien  ' if ok else 'FALLA ') + txt)
    # 1. volumenes: que Fusion ha construido lo mismo que calculo iris_diseno_v5.py
    for n in ('base', 'aro', 'tapa', 'lamina_A', 'lamina_B'):
        v = S[n].volume * 1000; e = J['piezas'][n]['volumen']
        linea(abs(v - e) / e < 0.01, '%s: %.0f mm3 en Fusion, %.0f calculados (%.1f g de PLA macizo), %d cuerpo(s)' % (n, v, e, v * 1.24 / 1000, S[n].lumps.count))
    # 2. medidas exteriores
    bb = S['base'].boundingBox
    dx = (bb.maxPoint.x - bb.minPoint.x) / K; dy = (bb.maxPoint.y - bb.minPoint.y) / K; dz = (bb.maxPoint.z - bb.minPoint.z) / K
    bt = M['tapa'].boundingBox
    alto = bt.maxPoint.z / K
    linea(True, 'MEDIDO diametro exterior de la base: %.2f x %.2f mm' % (dx, dy))
    linea(alto <= 10.0 and abs(dz - alto) < 0.01, 'MEDIDO grueso total montado: %.2f mm (la base sola mide %.2f)' % (alto, dz))
    r_orj = max(math.hypot(v.geometry.x, v.geometry.y) for v in M['aro'].vertices) / K
    linea(True, 'MEDIDO la orejeta del aro llega a %.2f mm del centro: sale %.1f mm de la pared. De la punta de la orejeta al lado contrario: %.1f mm' % (r_orj, r_orj - dx / 2, r_orj + dx / 2))
    # 3. piezas fijas: no se pisan. El aro y la tapa se prueban 0,03 mm levantados, para separar las caras de apoyo
    aro_m = mover(copia(M['aro']), 0, 0, 0.03); tapa_m = mover(copia(M['tapa']), 0, 0, 0.06)
    for a, b, ca, cb in (('aro', 'base', aro_m, M['base']), ('tapa', 'base', tapa_m, M['base']), ('tapa', 'aro', tapa_m, aro_m)):
        v = vol_inter(ca, cb)
        linea(v < 0.01, 'montado, %s y %s se pisan %.3f mm3' % (a, b, v))
    # 4. laminas abiertas e inclinadas como dice el calculo de apilado
    def entre_ellas(L):
        peor = 0.0
        for i in range(N):
            for j in range(i + 1, N):
                peor = max(peor, vol_inter(L[i], L[j]))
        return peor
    LA = [M['lamina_%d' % (k + 1)] for k in range(N)]; LB = juego_b(S)
    va = entre_ellas(LA); vb = entre_ellas(LB)
    linea(True, 'abierto, juego A (1,2 mm): colocadas rigidas, dos laminas vecinas se pisan %.2f mm3. Es lo que el calculo dice que absorben doblandose %.2f mm' % (va, J['planos']['A'][0][1]))
    linea(vb < 0.05, 'abierto, juego B (0,8 mm): colocadas rigidas, las %d laminas en escalera no se pisan (%.3f mm3)' % (N, vb))
    for n, L in (('A', LA), ('B', LB)):
        v = max(max(vol_inter(b, M['base']), vol_inter(b, tapa_m), vol_inter(b, aro_m)) for b in L)
        linea(v < 0.05, 'abierto, ninguna lamina del juego %s toca la base, el aro ni la tapa (pisado: %.3f mm3)' % (n, v))
    # 5. hueco abierto: tiene que pasar un cilindro de 75 mm
    planas = [lamina_plana(S['lamina_A'], k, 0.0, d['z_isla']) for k in range(N)]
    c = cyl((0, 0, -5), (0, 0, 30), P['hueco_d'] / 2 - 0.005)
    v = sum(vol_inter(b, c) for b in planas) + vol_inter(M['base'], c) + vol_inter(M['aro'], c) + vol_inter(M['tapa'], c)
    linea(v < 0.01, 'MEDIDO abierto: un cilindro de %.1f mm pasa sin tocar nada (pisado: %.3f mm3)' % (P['hueco_d'], v))
    lo = None
    for diam in [P['hueco_d'] + 0.2 * i for i in range(1, 15)]:
        if sum(vol_inter(b, cyl((0, 0, -5), (0, 0, 30), diam / 2)) for b in planas) > 0.001:
            break
        lo = diam
    linea(lo is not None, 'MEDIDO abierto: las laminas quedan escondidas; el cilindro mas grande que no las toca mide %.1f mm' % (lo or 0))
    # 6. cerrado: agujero central y que no quede ninguna rendija
    for nombre, giro in (('en la posicion nominal', J['giro_lamina']), ('en el tope de cierre', J['giro_lamina'] + P['sobrecierre'])):
        u = None
        for k in range(N):
            b = lamina_plana(S['lamina_A'], k, giro, 0.0)
            u = b if u is None else join(u, b)
        losa = cyl((0, 0, 0.2), (0, 0, 0.6), P['hueco_d'] / 2)
        v0 = losa.volume * 1000
        cut(losa, u)
        area = losa.volume * 1000 / 0.4
        lo = hi = None
        for diam in [x * 0.2 for x in range(1, 60)]:
            v = vol_inter(u, cyl((0, 0, 0.2), (0, 0, 0.6), diam / 2))
            if v < 0.0005: lo = diam
            else:
                hi = diam
                break
        linea(lo is not None and lo <= 8.0 and losa.lumps.count <= 1, 'MEDIDO cerrado %s: por el agujero central cabe un cilindro de %.1f mm y no uno de %.1f; hueco sin tapar %.1f mm2 de %.0f, en %d trozo(s)' % (nombre, lo or 0, hi or 0, area, v0 / 0.4, losa.lumps.count))
    # 7. giro del aro: se gira hasta que la orejeta toca la pared, hacia los dos lados
    def tope(sentido):
        lo, hi = 0.0, 40.0
        for _ in range(14):
            mid = (lo + hi) / 2
            if vol_inter(rotz(copia(aro_m), sentido * mid), M['base']) < 0.001: lo = mid
            else: hi = mid
        return lo
    t_cierra = tope(s); t_abre = tope(-s)
    linea(t_cierra + t_abre <= 60, 'MEDIDO giro del aro de tope a tope: %.1f grados (%.1f hacia cerrar y %.1f hacia abrir desde la posicion de abierto). Calculado: %.1f y %.1f' % (t_cierra + t_abre, t_cierra, t_abre, abs(J['giro_aro']), abs(J['giro_aro_abre'])))
    # 8. el teton sigue dentro de su ranura en todo el recorrido
    peor = 0.0
    g0 = -P['sobregiro']; g1 = J['giro_lamina'] + P['sobrecierre']
    for i in range(13):
        g = g0 + (g1 - g0) * i / 12.0
        aro = rotz(copia(M['aro']), angulo_aro(g))
        peor = max(peor, vol_inter(lamina_plana(S['lamina_A'], 0, g, d['z_isla'] + P['holg_altura'] - 0.03), aro), vol_inter(lamina_plana(S['lamina_B'], 3, g, d['z_isla']), aro))
    linea(peor < 0.001, 'en 13 posiciones de abierto a cerrado, el teton de la lamina va por su ranura sin tocar el aro (pisado: %.4f mm3)' % peor)
    # 9. bayoneta de la tapa
    g = J['giro_tapa']
    metida = rotz(copia(M['tapa']), -s * g)
    metida = mover(metida, 0, 0, 0.06)
    linea(vol_inter(mover(copia(metida), 0, 0, 3.0), M['base']) < 0.001 and vol_inter(metida, M['base']) < 0.001, 'la tapa entra por arriba en la posicion de meter (girada %.0f grados)' % g)
    v_sube = vol_inter(mover(copia(M['tapa']), 0, 0, 0.45), M['base'])
    linea(v_sube > 0.05, 'cerrada, la tapa no puede salir hacia arriba: las uñas la paran (choque al subirla 0,45 mm: %.2f mm3)' % v_sube)
    v_mas = vol_inter(rotz(copia(tapa_m), s * 1.0), M['base'])
    linea(v_mas > 0.05, 'cerrada, la tapa no gira mas alla del tope (choque al girar 1 grado mas: %.2f mm3)' % v_mas)
    # 10. boca abajo: el aro sujeta las laminas y la tapa sujeta el aro
    v1 = vol_inter(lamina_plana(S['lamina_A'], 0, 0.0, d['z_isla'] + P['holg_altura'] + 0.2), M['aro'])
    v2 = vol_inter(mover(copia(M['aro']), 0, 0, P['aro_juego'] + 0.2), M['tapa'])
    linea(v1 > 0.05 and v2 > 0.05, 'boca abajo: la cola de la lamina solo puede bajar %.1f mm hasta el aro, y el aro %.1f mm hasta la tapa' % (P['holg_altura'], P['aro_juego']))
    return out

# ---------------------------------------------------------------- impresion
def imprimibles(S):
    """(nombre de archivo, cuerpo o lista de cuerpos), cada uno apoyado en la cama como se imprime."""
    out = [('iris-base', copia(S['base'])), ('iris-aro', copia(S['aro'])), ('iris-tapa', copia(S['tapa']))]
    for n, t in (('lamina_A', J['P']['lamina_grosor']), ('lamina_B', J['P']['lamina_grosor_b'])):
        bandeja = []
        for ang, dx, dy in J['cama']:
            bandeja.append(mover(rotz(copia(S[n]), ang), dx, dy, 0))
        out.append(('iris-laminas-%.1fmm-x%d' % (t, len(bandeja)), bandeja))
        out.append(('iris-lamina-%.1fmm-suelta' % t, mover(rotz(copia(S[n]), J['cama'][0][0]), J['cama'][0][1], J['cama'][0][2], 0)))
    return out

def exportar(S, sub=None):
    sub = sub or os.path.join(CARPETA, 'probetas-v5')
    d = des()
    em = d.exportManager
    out = []
    if not os.path.isdir(sub):
        os.makedirs(sub)
    for nombre, body in imprimibles(S):
        occ = put('_exp', body)
        fn = os.path.join(sub, nombre + '.3mf')
        em.execute(em.createC3MFExportOptions(occ, fn))
        occ.deleteMe()
        out.append('%s (%d bytes)' % (fn, os.path.getsize(fn)))
    return out

def main(comprobar_=True, nuevo=True):
    carga()
    if nuevo:
        doc = app().documents.add(C.DocumentTypes.FusionDesignDocumentType)
    d = des()
    d.designIntent = F.DesignIntentTypes.HybridDesignIntentType
    out = ['parametros copiados: %d (informativos)' % parametros()]
    S = piezas_sueltas()
    M = montaje(S)
    for n in M:
        put(n, M[n])
    colores()
    if comprobar_:
        out += comprobar(S, M)
    app().activeViewport.fit()
    return out, S
