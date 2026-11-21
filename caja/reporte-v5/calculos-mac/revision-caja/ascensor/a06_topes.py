# 6. Topes: a que giro para el tubo, con que superficie, y si la oreja toca algo mas en su vuelta
from comun import *
G = p['giro_tubo']
tu = S['tubo']; ba = S['base']
ops = P['tubo'].ops
oreja = CP.solido([dict(ops[4]), dict(ops[5]), dict(ops[6]), dict(ops[7])])
anillo_t = CP.solido([{'t': 'prisma', 'eje': 'z', 'c0': -130, 'c1': 0, 'pol': CP.geo(CP.disco(d['tubo_r_ext'], n=600)), 'op': '+'}])
oreja = oreja - anillo_t                      # solo lo que sobresale del tubo
print('oreja (lo que sobresale):', bb(oreja), 'vol %.1f' % oreja.volume())
bops = P['base'].ops
for i, o in enumerate(bops): print('  base op', i, o['t'], o['op'], o.get('c0'), o.get('c1'))
print('\nGiro exacto al que el tubo empieza a pisar la base (paso 0.01 grados):')
for nombre, centro, sg in (('cerrado', 0.0, -1), ('abierto', G, 1)):
    for i in range(0, 200):
        e = 0.01 * i
        v = vol(tu.rotate([0, 0, ROT * (centro + sg * e)]), ba)
        if v > 1e-4:
            print('  %s: pisa a partir de tau = %.2f (%.2f grados mas alla); a %.2f, %.3f mm3' % (nombre, centro + sg * e, e, centro + sg * e, v)); break
    # superficie: volumen comun con 0.2 grados de mas, dividido por lo que se mete
    e = 0.2
    I = tu.rotate([0, 0, ROT * (centro + sg * e)]) ^ ba
    r_m = 83.5
    print('     con 0.2 grados de mas: %.3f mm3, caja %s -> superficie de contacto aprox. %.1f mm2' % (I.volume(), bb(I), I.volume() / (math.radians(e) * r_m)))
    g = gap(puesta('tubo', centro), ba, 1.0)
    print('     en el tope (tau = %.0f): dist tubo-base %.4f (el tubo apoya en su pista: 0 es apoyo); oreja-base %.4f' % (centro, g, gap(oreja.rotate([0, 0, ROT * centro]), ba, 1.0)))
print('\nAntes del tope, quien para primero? distancia de otras cosas al llegar:')
for tau in (0.0, G):
    for a, b in (('plataforma', 'tubo'), ('teton', 'plato'), ('teton', 'aro_puertas'), ('teton', 'marco')):
        print('   tau %.0f  %s - %s: %.3f' % (tau, a, b, gap(puesta(a, tau), puesta(b, tau), 3.0)))
# pasandose del tope: cuanto mas giraria hasta que choca otra cosa (si el tope no estuviera)
for nombre, centro, sg in (('cerrado', 0.0, -1), ('abierto', G, 1)):
    for a, b in (('plataforma', 'tubo'), ('teton', 'plato')):
        for i in range(1, 400):
            e = 0.02 * i; tau = centro + sg * e
            A = puesta(a, centro); B = S[b].rotate([0, 0, ROT * tau])
            if vol(A, B) > 1e-3:
                print('   %s: sin tope, %s y %s chocarian %.2f grados mas alla' % (nombre, a, b, e)); break
print('\nLa oreja en su vuelta (tau de 0 a 345, paso 0.5): distancia minima a cada pieza fija y a las que no giran con ella')
fijas = ['base', 'cuerpo', 'marco', 'plataforma', 'bisel']
res = {n: (9.0, 0.0) for n in fijas}
# base sin el tope (para ver lo demas de la base): se quita la op del tope
i_tope = [i for i, o in enumerate(bops) if o['t'] == 'prisma' and abs(o['c1'] - (d['z_suelo'] + 16.5)) < 1e-6][0]
base_sin_tope = CP.solido([o for i, o in enumerate(bops) if i != i_tope and not (o['op'] == '-' and abs(o.get('c0', 0) - (d['z_suelo'] + 0.6 + 9.4)) < 1e-6)])
tope = S['base'] - base_sin_tope
print('   tope:', bb(tope))
res['base sin tope'] = (9.0, 0.0); res['tope'] = (9.0, 0.0)
for i in range(691):
    tau = 0.5 * i
    o = oreja.rotate([0, 0, ROT * tau])
    for n in list(res):
        A = base_sin_tope if n == 'base sin tope' else tope if n == 'tope' else puesta(n, tau)
        if n == 'base': continue
        g = o.min_gap(A, 3.0)
        if g < res[n][0]: res[n] = (g, tau)
for n, (g, tau) in res.items():
    if n != 'base': print('   oreja - %-14s dist min %.3f (tau %.1f)' % (n, g, tau))
# con el tubo descentrado lo que le deja el aro de la base (0.35)
print('   pared del cuerpo a %.3f del eje; punta de la oreja a %.3f: quedan %.3f; con el tubo descentrado 0.35, %.3f' % (d['cuerpo_lado'] / 2 - p['cuerpo_pared'], d['tubo_r_ext'] + 5.3, d['cuerpo_lado'] / 2 - p['cuerpo_pared'] - d['tubo_r_ext'] - 5.3, d['cuerpo_lado'] / 2 - p['cuerpo_pared'] - d['tubo_r_ext'] - 5.3 - 0.35))
# ranuras de iman: pared que queda
gi = math.degrees((0.7 + 0.875) / (d['tubo_r_ext'] + 2.8))
print('   iman: ranura de 1.75 x 5.3 a %.2f mm de la cara del tope (pared de PLA entre iman y cara: 0.70 mm en la oreja y 0.70 en el tope)' % 0.7)
