# 1. Barrido fino del ascensor: plataforma contra tubo, base, marco, aro_puertas, meseta
from comun import *
taus = sorted(set([round(0.5 * i, 3) for i in range(691)] + [round(88 + 0.1 * i, 3) for i in range(81)] + [round(331 + 0.1 * i, 3) for i in range(81)]))
otros = ['tubo', 'base', 'marco', 'aro_puertas', 'meseta', 'plato', 'teton', 'puerta_derecha', 'puerta_izquierda']
res = {o: [] for o in otros}
t0 = time.time()
for tau in taus:
    pl = puesta('plataforma', tau)
    for o in otros:
        ot = puesta(o, tau)
        v = vol(pl, ot); g = gap(pl, ot, 1.5)
        res[o].append((tau, v, g))
print('posiciones', len(taus), 'tiempo %.0f s' % (time.time() - t0))
for o in otros:
    a = np.array(res[o])
    iv = a[:, 1].argmax(); ig = a[:, 2].argmin()
    print('%-16s vol max %.4f mm3 (tau %.1f) | dist min %.4f mm (tau %.1f) | nº de giros con vol>0: %d, con vol>0.02: %d' % (o, a[iv, 1], a[iv, 0], a[ig, 2], a[ig, 0], (a[:, 1] > 1e-9).sum(), (a[:, 1] > 0.02).sum()))
np.save('a01_res.npy', {o: np.array(res[o]) for o in otros}, allow_pickle=True)
# perfil de la distancia plataforma-tubo y plataforma-base por tramos
for o in ('tubo', 'base', 'marco', 'aro_puertas', 'meseta'):
    a = np.array(res[o])
    print(o)
    for lo, hi in ((0, 87.9), (88, 96), (96.1, 117), (117.5, 123), (123.5, 237), (237.5, 243), (243.5, 330.5), (331, 339), (339.5, 345)):
        m = (a[:, 0] >= lo) & (a[:, 0] <= hi)
        s = a[m]
        print('   tau %6.1f..%6.1f  vol max %.4f (tau %.1f)  dist min %.4f (tau %.1f)  dist max %.4f' % (lo, hi, s[:, 1].max(), s[s[:, 1].argmax(), 0], s[:, 2].min(), s[s[:, 2].argmin(), 0], s[:, 2].max()))
