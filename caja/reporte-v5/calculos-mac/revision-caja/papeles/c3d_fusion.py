# 3(d): caja-fusion-comprobaciones.txt contra el JSON y contra lo que deberia haberse mirado
import re, json, sys
from comun import *
R = '<repositorio>/caja/'
J = json.load(open(R + 'caja-v5-piezas.json', encoding='utf-8'))
txt = open(R + 'reporte-v5/caja-fusion-comprobaciones.txt', encoding='utf-8').read()
filas = re.findall(r'bien\s+(\w+)\s+Fusion\s+([\d.]+) mm3\s+programa\s+([\d.]+) mm3\s+diferencia ([+-][\d.]+) %', txt)
print('piezas en el fichero de Fusion:', len(filas), ' en el JSON:', len(J['piezas']))
peor = 0
for n, vf, vp, dif in filas:
    vj = J['piezas'][n]['volumen']; ok = abs(float(vp) - vj) < 0.06
    dreal = 100 * (float(vf) - vj) / vj; peor = max(peor, abs(dreal))
    if not ok or abs(dreal - float(dif)) > 0.006: print('  NO CUADRA', n, vf, vp, vj, dif, dreal)
print('  columna "programa" = volumen del JSON en las %d: %s ; mayor diferencia Fusion/JSON %.2f %%' % (len(filas), all(abs(float(vp) - J['piezas'][n]['volumen']) < 0.06 for n, vf, vp, dif in filas), peor))
print('  faltan:', set(J['piezas']) - {f[0] for f in filas})
# secciones 2 y 3
partes = re.split(r'\n(?=\d\. )', txt)
for sec in partes[1:]:
    cab = sec.split('\n')[0][:110]
    lin = re.findall(r'(bien|FALLA)\s+tubo\s+([\d.]+)\s+puertas\s+([\d.]+)\s+plataforma\s+([\d.]+) mm\s+pares mirados\s+(\d+)\s+lo que mas se pisa: ([\d.]+) mm3', sec)
    if not lin: continue
    taus = [float(l[1]) for l in lin]; pares = [int(l[4]) for l in lin]
    esperado = [2.0 * i for i in range(173)] + [345.0]
    print(cab); print('   lineas %d; taus = 0,2,...,344,345: %s; FALLA: %d; pares min %d max %d media %.1f; max pisa %.3f' % (len(lin), taus == esperado, sum(1 for l in lin if l[0] != 'bien'), min(pares), max(pares), sum(pares) / len(pares), max(float(l[5]) for l in lin)))
    # angulo de puertas y altura que figura, contra el movimiento actual
    dm = max(abs(float(l[2]) - round(D.movimiento(p, d, float(l[1]))[2], 1)) for l in lin); dh = max(abs(float(l[3]) - round(D.movimiento(p, d, float(l[1]))[3], 1)) for l in lin)
    print('   puertas/plataforma del fichero contra movimiento() actual: dif max %.2f grados, %.2f mm' % (dm, dh))
    # replica del recuento de parejas con el modelo actual (cajas que se solapan; misma regla que comprobar())
    solo = {'tubo', 'plataforma', 'base', 'cuerpo', 'meseta'} if sec.startswith('3') else None
    nombres = CAJA
    mios = []
    for i, tau in enumerate(esperado):
        M = {n: puesta(n, tau) for n in nombres}; B = {n: bb(M[n]) for n in nombres}; c = 0
        for ia, a in enumerate(nombres):
            for b in nombres[ia + 1:]:
                if P[a].mueve == P[b].mueve and i > 0: continue
                if solo and a not in solo and b not in solo: continue
                A_, B_ = B[a], B[b]
                if A_[0] > B_[3] or B_[0] > A_[3] or A_[1] > B_[4] or B_[1] > A_[4] or A_[2] > B_[5] or B_[2] > A_[5]: continue
                c += 1
        mios.append(c)
    dif = [(esperado[i], pares[i], mios[i]) for i in range(min(len(pares), len(mios))) if pares[i] != mios[i]]
    print('   recuento de parejas rehecho con el modelo actual: coincide en %d de %d posiciones; media mia %.1f; primeras diferencias (tau, fichero, mio): %s' % (len(pares) - len(dif), len(pares), sum(mios) / len(mios), dif[:8]))
print(re.findall(r'RESUMEN.*', txt))
print([l for l in txt.split('\n') if 'mano' in l or '16:40' in l or 'Tardo' in l])
