# 4. Las comprobaciones de comprueba() (fase 2), rehechas con mas cuidado
import sys, time
from comun import *
def P_(*a): print(*a); sys.stdout.flush()
def libre(f, paso, tope, umbral=0.02):
    """Primer desplazamiento (multiplo de 'paso') en el que f(desplazamiento) pisa mas de 'umbral'. Devuelve el ultimo libre."""
    x = paso
    while x <= tope + 1e-9:
        if f(x) > umbral: return x - paso
        x += paso
    return float('inf')
P_('=== 1. barrido de interferencias mas fino')
def barrido(taus, nombres, umbral=0.02):
    peor = {}
    for it, tau in enumerate(taus):
        M = {n: puesta(n, tau) for n in nombres}; B = {n: bb(M[n]) for n in nombres}
        for i, a in enumerate(nombres):
            for b in nombres[i + 1:]:
                if P[a].mueve == P[b].mueve and it > 0: continue
                A_, B_ = B[a], B[b]
                if A_[0] > B_[3] or B_[0] > A_[3] or A_[1] > B_[4] or B_[1] > A_[4] or A_[2] > B_[5] or B_[2] > A_[5]: continue
                v = vol(M[a], M[b])
                if v > peor.get((a, b), (0, 0))[0]: peor[(a, b)] = (v, tau)
    return sorted(((v, t, a, b) for (a, b), (v, t) in peor.items() if v > 1e-4), reverse=True)
t0 = time.time()
r = barrido([float(t) for t in np.arange(0.5, G, 1.0)], CAJA)       # medios grados: posiciones que el autor no miro
P_('  todas las piezas, tau = 0.5, 1.5, ... (345 posiciones intermedias), %.0f s: parejas que pisan > 0.0001 mm3:' % (time.time() - t0), [(round(v, 4), t, a, b) for v, t, a, b in r[:8]] or 'ninguna')
t0 = time.time()
mec = ['puerta_derecha', 'puerta_izquierda', 'aro_puertas', 'teton', 'marco', 'meseta', 'plato', 'rueda_central', 'pasador_derecho', 'pasador_izquierdo', 'plataforma', 'reloj_de_pega', 'soporte', 'tubo']
r = barrido([float(t) for t in np.arange(44, 104.001, 0.1)], mec)
P_('  mecanismo de puertas, tau 44..104 de 0,1 en 0,1 (601 posiciones), %.0f s:' % (time.time() - t0), [(round(v, 4), round(t, 1), a, b) for v, t, a, b in r[:8]] or 'ninguna')

P_('=== 2. las dos puertas entre si, al abrir (angulo de 0 a 90 de 0,25 en 0,25), con y sin desfase por su juego')
for desf in (0.0, 1.0, 2.0, 3.0, -1.0, -2.0, -3.0):
    peor = (0, 0); cerca = (9e9, 0)
    for ang in np.arange(0.0, 90.01, 0.25):
        a = puerta(1, max(0.0, min(94.0, ang + desf))); b = puerta(-1, float(ang))
        v = vol(a, b)
        if v > peor[0]: peor = (v, float(ang))
        if ang <= 30:
            g = a.min_gap(b, 3.0)
            if g < cerca[0]: cerca = (g, float(ang))
    P_('  derecha %+.0f grados respecto a la izquierda: pisan como mucho %.3f mm3 (a %.2f grados); lo mas cerca en los primeros 30 grados: %.3f mm (a %.2f)' % (desf, peor[0], peor[1], cerca[0], cerca[1]))

P_('=== 3. juego de las puertas bloqueadas (paso 0,05 grados; contra aro, meseta, marco y la otra puerta)')
def juego(sx, desde, signo, contra, paso=0.05, tope=12.0, umbral=0.02):
    return libre(lambda dl: sum(vol(puerta(sx, desde + signo * dl), c) for c in contra), paso, tope, umbral)
for psi_tau, nombre in ((0.0, 'tau 0 (aro a 0)'), (45.0, 'tau 45'), (58.0, 'tau 58 (aro %.2f)' % D.movimiento(p, d, 58)[1]), (62.0, 'tau 62 (aro %.2f, fin del reposo)' % D.movimiento(p, d, 62)[1])):
    aro = puesta('aro_puertas', psi_tau)
    for sx in (1, -1):
        P_('  cerrada, %s, puerta %+d: se deja levantar %.2f grados contra el aro solo; %.2f contra aro+meseta+marco+otra puerta cerrada' % (nombre, sx, juego(sx, 0.0, 1, [aro]), juego(sx, 0.0, 1, [aro, S['meseta'], S['marco'], puerta(-sx, 0.0)])))
for tau_, nombre in ((83.0, 'tau 83 (aro %.2f, recien abierta)' % D.movimiento(p, d, 83)[1]), (92.0, 'tau 92'), (100.0, 'tau 100'), (G, 'tau 345')):
    aro = puesta('aro_puertas', tau_); a90 = D.movimiento(p, d, tau_)[2]
    for sx in (1, -1):
        P_('  abierta (%.2f), %s, puerta %+d: hacia dentro %.2f (solo aro) / %.2f (aro+meseta+marco); hacia fuera %.2f (solo aro) / %.2f (aro+meseta+marco+rueda central)' % (a90, nombre, sx, juego(sx, a90, -1, [aro]), juego(sx, a90, -1, [aro, S['meseta'], S['marco']]), juego(sx, a90, 1, [aro]), juego(sx, a90, 1, [aro, S['meseta'], S['marco'], S['rueda_central']])))
P_('  umbral: con 0.001 mm3 en vez de 0.02 -> cerrada %.2f ; abierta dentro %.2f fuera %.2f' % (juego(1, 0.0, 1, [puesta('aro_puertas', 0)], umbral=0.001), juego(1, 90.0, -1, [puesta('aro_puertas', G)], umbral=0.001), juego(1, 90.0, 1, [puesta('aro_puertas', G), S['meseta']], umbral=0.001)))
# cerrada, empujada hacia abajo con un dedo: apoya?
P_('  cerrada, empujada hacia ABAJO: se deja girar %.2f grados antes de pisar meseta/aro (0 = apoya)' % juego(1, 0.0, -1, [S['meseta'], puesta('aro_puertas', 0), S['marco']]))
# a medio abrir (tau 72): cuanto baila
for tau_ in (66.0, 72.0, 78.0):
    aro = puesta('aro_puertas', tau_); a_ = D.movimiento(p, d, tau_)[2]
    P_('  a medio abrir (tau %.0f, puerta a %.1f): baila -%.2f / +%.2f grados contra el aro' % (tau_, a_, juego(1, a_, -1, [aro]), juego(1, a_, 1, [aro])))

P_('=== 4. teton: juego real en cada ranura, en varias posiciones')
for tau_ in (0.0, 30.0, 46.0, 60.0, 72.5, 90.0, 100.0, 200.0, G):
    te = puesta('teton', tau_); pl = puesta('plato', tau_); ar = puesta('aro_puertas', tau_)
    jr = [libre(lambda e: vol(te.translate([0, sg * e, 0]), pl), 0.02, 6.0) for sg in (1, -1)]       # radial, contra la espiral
    jt = [libre(lambda e: vol(te.translate([sg * e, 0, 0]), S['marco']), 0.02, 6.0) for sg in (1, -1)]   # de lado, contra la ranura recta del marco
    ja = [libre(lambda e: vol(ar.rotate([0, 0, sg * e]), te), 0.02, 6.0) for sg in (1, -1)]              # giro del aro con el teton quieto
    jz = libre(lambda e: vol(te.translate([0, 0, e]), pl) + vol(te.translate([0, 0, e]), ar), 0.02, 6.0)
    P_('  tau %5.1f: teton radial +%.2f/-%.2f mm (espiral); de lado +%.2f/-%.2f (marco); aro libre +%.2f/-%.2f grados con el teton quieto; el teton sube %.2f mm' % (tau_, jr[0], jr[1], jt[0], jt[1], ja[0], ja[1], jz))

P_('=== 5. plataforma: juego vertical, giro y cabeceo reales')
for tau_ in (0.0, 46.0, 90.0, 92.0, 93.0, 94.0, 96.0, 120.0, 200.0, 300.0, 334.0, 336.0, 340.0, G):
    pf = puesta('plataforma', tau_); tu = puesta('tubo', tau_)
    ab = libre(lambda e: vol(pf.translate([0, 0, -e]), tu) + vol(pf.translate([0, 0, -e]), S['base']), 0.01, 3.0)
    ab_t = libre(lambda e: vol(pf.translate([0, 0, -e]), tu), 0.01, 3.0)
    ar = libre(lambda e: vol(pf.translate([0, 0, e]), tu) + vol(pf.translate([0, 0, e]), S['marco']), 0.01, 3.0)
    P_('  tau %5.1f (h %.2f): baja %.2f mm (solo contra el tubo: %.2f) y sube %.2f mm antes de pisar' % (tau_, D.movimiento(p, d, tau_)[3], ab, ab_t, ar))
pf = puesta('plataforma', 200.0); tu = puesta('tubo', 200.0)
gi_ = [libre(lambda e: vol(pf.rotate([0, 0, sg * e]), S['base']), 0.01, 3.0) for sg in (1, -1)]
P_('  giro libre contra las columnas (tau 200): +%.2f / -%.2f grados' % tuple(gi_))
rad = [libre(lambda e: vol(pf.translate([e * math.cos(math.radians(a)), e * math.sin(math.radians(a)), 0]), tu) + vol(pf.translate([e * math.cos(math.radians(a)), e * math.sin(math.radians(a)), 0]), S['base']), 0.01, 2.0) for a in (0, 90, 180, 270, 45)]
P_('  desplazamiento lateral libre (tau 200), en 0/90/180/270/45 grados: %s mm' % [round(v, 2) for v in rad])
zc0 = d2['zc0'] + D.movimiento(p, d, 200.0)[3]; z_top = d['z_disco1_abajo'] + d['pedestal_alto'] + D.movimiento(p, d, 200.0)[3] + p['reloj_alto']
peor = (0, 0)
for a in range(0, 360, 30):
    eje = [math.cos(math.radians(a)), math.sin(math.radians(a)), 0.0]
    def inclinada(e):
        # giro de e grados alrededor de un eje horizontal que pasa por el centro del plano de los tetones
        th = math.radians(e); c, s = math.cos(th), math.sin(th); x, y, z = eje
        Rm = np.array([[c + x * x * (1 - c), x * y * (1 - c), y * s], [x * y * (1 - c), c + y * y * (1 - c), -x * s], [-y * s, x * s, c]])
        t = np.array([0, 0, zc0]) - Rm @ np.array([0, 0, zc0])
        return pf.transform(np.column_stack([Rm, t]))
    v = libre(lambda e: vol(inclinada(e), tu) + vol(inclinada(e), S['base']), 0.01, 2.0)
    if v > peor[0]: peor = (v, a)
P_('  cabeceo libre maximo (tau 200, eje horizontal por el plano de los tetones, 12 direcciones): %.2f grados (eje a %d grados) -> %.2f mm en lo alto del reloj (%.1f mm por encima de los tetones)' % (peor[0], peor[1], math.radians(peor[0]) * (z_top - zc0), z_top - zc0))

P_('=== 6. dientes: holgura real de giro')
for tau_ in (0.0, 37.0, 200.0):
    bi = puesta('bisel', tau_); sats = [puesta('satelite_%d' % i, tau_) for i in range(1, 7)]
    jb = [libre(lambda e: sum(vol(bi.rotate([0, 0, sg * e]), s_) for s_ in sats), 0.01, 3.0, 0.005) for sg in (1, -1)]
    js = []
    for i in range(1, 7):
        th = float(P['satelite_%d' % i].mueve.split(':')[1]) + CP.ROT * tau_; c = CP.pol(d['r_ejes'], th); s_ = sats[i - 1]
        js.append([libre(lambda e: vol(s_.translate([-c[0], -c[1], 0]).rotate([0, 0, sg * e]).translate([c[0], c[1], 0]), S['rueda_central']) + vol(s_.translate([-c[0], -c[1], 0]).rotate([0, 0, sg * e]).translate([c[0], c[1], 0]), bi), 0.02, 16.0, 0.005) for sg in (1, -1)])
    P_('  tau %5.1f: el bisel gira en vacio +%.2f/-%.2f grados con los satelites quietos (%.2f mm en el primitivo); cada satelite, con central y bisel quietos: %s grados' % (tau_, jb[0], jb[1], math.radians(jb[0] + jb[1]) * d['r_bisel'], [(round(a, 2), round(b, 2)) for a, b in js]))
for i in range(1, 7):
    th = float(P['satelite_%d' % i].mueve.split(':')[1]); c = CP.pol(d['r_ejes'], th)
    s_ = S['satelite_%d' % i].translate([-c[0], -c[1], 0]).rotate([0, 0, 180.0 / p['z_satelite']]).translate([c[0], c[1], 0])
    print('  satelite_%d girado medio diente: pisa central %.1f y bisel %.1f mm3' % (i, vol(s_, S['rueda_central']), vol(s_, S['bisel'])), end=';')
P_()
P_('  holgura radial del satelite en su eje: agujero %.2f, eje %.2f -> %.2f por lado' % (2.75 + p['holg_gira'], 2.75, p['holg_gira']))

P_('=== 7. topes: cuanto se pasa antes de chocar')
for nombre, base_ang, sg in (('cerrado', 0.0, -1), ('abierto', G, 1)):
    f = libre(lambda e: vol(S['tubo'].rotate([0, 0, CP.ROT * (base_ang + sg * e)]), S['base']), 0.05, 5.0)
    f2 = libre(lambda e: vol(S['tubo'].rotate([0, 0, CP.ROT * (base_ang + sg * e)]), S['base']) + vol(puesta('plataforma', base_ang), S['tubo'].rotate([0, 0, CP.ROT * (base_ang + sg * e)])), 0.05, 5.0)
    P_('  %s: el tubo se pasa %.2f grados antes de pisar la base (y %.2f antes de pisar base o tetones)' % (nombre, f, f2))

P_('=== 8. boca abajo: cada pieza, sola, cuanto sube (hacia la tapa) hasta que algo la para; caja cerrada y abierta')
for tau_, est in ((0.0, 'cerrada'), (G, 'abierta')):
    M = {n: puesta(n, tau_) for n in CAJA}
    res = []
    for n in CAJA:
        if n == 'base': continue
        otros = [M[q] for q in CAJA if q != n]
        def f(e):
            m = M[n].translate([0, 0, e]); B = bb(m); v = 0
            for o in otros:
                b = bb(o)
                if B[0] > b[3] or b[0] > B[3] or B[1] > b[4] or b[1] > B[4] or B[2] > b[5] or b[2] > B[5]: continue
                v += vol(m, o)
            return v
        res.append((n, libre(f, 0.1, 30.0)))
    P_('  %s: ' % est + '; '.join('%s %s' % (n, ('%.1f' % v) if v < 1e9 else 'NADA LA PARA en 30 mm') for n, v in res))

P_('=== 9. pasadores: cuanto corren a lo largo')
for n in ('pasador_derecho', 'pasador_izquierdo'):
    otros = [S[q] for q in CAJA if q != n]
    r = [libre(lambda e: sum(vol(S[n].translate([0, sg * e, 0]), o) for o in otros), 0.05, 20.0) for sg in (1, -1)]
    P_('  %s: +%.2f / -%.2f mm' % (n, r[0], r[1]))

P_('=== 10. funda')
g = {n: S['funda'].min_gap(S[n], 5.0) for n in CAJA if n not in ('reloj_de_pega', 'soporte')}
P_('  distancia de la funda a cada pieza (< 5 mm):', {n: round(v, 2) for n, v in g.items() if v < 5.0})
for a in (90, 180, 270):
    P_('  funda girada %d grados: pisa %.2f mm3 (cuerpo), %.2f (bisel)' % (a, vol(S['funda'].rotate([0, 0, a]), S['cuerpo']), vol(S['funda'].rotate([0, 0, a]), S['bisel'])), end=';')
P_()
P_('  funda con la caja ABIERTA (tau 345): pisa puertas %.1f mm3, reloj %.1f' % (vol(S['funda'], puerta(1, 90)) + vol(S['funda'], puerta(-1, 90)), vol(S['funda'], puesta('reloj_de_pega', G))))

P_('=== 11. piezas de la probeta de puertas (el autor no las mete en ningun barrido)')
an = S['probeta_anillo']; tp = S['probeta_teton']
peor = {}
for tau_ in np.arange(0, 101, 1.0):
    s_, psi, ang, h = D.movimiento(p, d, float(tau_))
    tpm = tp.translate([0, -s_, 0])
    for q in ('marco', 'meseta', 'aro_puertas', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo'):
        m = puesta(q, float(tau_))
        for nom, o in (('anillo', an), ('teton_pomo', tpm)):
            v = vol(o, m)
            if v > peor.get((nom, q), (0, 0))[0]: peor[(nom, q)] = (v, float(tau_))
    v = vol(an, tpm)
    if v > peor.get(('anillo', 'teton_pomo'), (0, 0))[0]: peor[('anillo', 'teton_pomo')] = (v, float(tau_))
P_('  probeta: parejas que se pisan (tau 0..100):', {k: (round(v[0], 3), v[1]) for k, v in peor.items() if v[0] > 1e-4} or 'ninguna')
tp13 = tp.translate([0, -p['teton_recorrido'], 0])
P_('  teton con pomo: distancia a la meseta %.2f (cerrado) / %.2f (abierto); al anillo %.2f / %.2f; al cuello del marco %.2f / %.2f' % (tp.min_gap(S['meseta'], 30), tp13.min_gap(S['meseta'], 30), tp.min_gap(an, 30), tp13.min_gap(an, 30), tp.min_gap(S['marco'], 30), tp13.min_gap(S['marco'], 30)))
for nom, o, aro in (('cerrado', tp, puesta('aro_puertas', 0)), ('abierto', tp13, puesta('aro_puertas', G))):
    sube = libre(lambda e: vol(o.translate([0, 0, e]), S['meseta']) + vol(o.translate([0, 0, e]), an) + vol(o.translate([0, 0, e]), aro) + vol(o.translate([0, 0, e]), S['marco']), 0.1, 30.0)
    P_('  probeta boca abajo, teton con pomo (%s): sube %s' % (nom, ('%.1f mm' % sube) if sube < 1e9 else 'sin que nada lo pare (se cae)'))
P_('  anillo boca abajo: sube %s' % (lambda v: ('%.1f mm' % v) if v < 1e9 else 'sin que nada lo pare (hay que sujetarlo, lo dice el reporte)')(libre(lambda e: sum(vol(an.translate([0, 0, e]), S[q]) for q in ('meseta', 'marco', 'pasador_derecho', 'puerta_derecha')), 0.1, 30.0)))
P_('  con el teton con pomo puesto, el plato pisa %.1f mm3 (no se puede montar el plato con ese teton)' % vol(tp, S['plato']))
