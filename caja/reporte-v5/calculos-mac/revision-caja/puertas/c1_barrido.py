# Comprobacion 1: barrido fino tubo 40..105 en 0,25; volumen comun y distancia minima de todas las parejas
from comun import *
import time, json
N = ['puerta_derecha','puerta_izquierda','aro_puertas','teton','marco','meseta','pasador_derecho','pasador_izquierdo','rueda_central','plato']
taus = [40 + 0.25*i for i in range(int((105-40)/0.25)+1)] + [0.0, 20.0, 150.0, 250.0, 345.0]
fijo = lambda n: P[n].mueve == 'fijo'
res = {}   # (a,b) -> dict(vmax, tau_v, gmin, tau_g, n_pisa)
t0 = time.time()
for it, tau in enumerate(taus):
    M = {n: mv(n, tau) for n in N}; B = {n: bb(M[n]) for n in N}
    for i, a in enumerate(N):
        for b in N[i+1:]:
            if fijo(a) and fijo(b) and it > 0: continue
            r = res.setdefault((a,b), dict(vmax=0.0, tau_v=None, gmin=9.0, tau_g=None, taus_pisa=[]))
            if not solapan(B[a], B[b], 0.5): continue
            v = vol(M[a], M[b])
            if v > r['vmax']: r['vmax'], r['tau_v'] = v, tau
            if v > 1e-6: r['taus_pisa'].append(tau)
            g = M[a].min_gap(M[b], 0.5)
            if g < r['gmin']: r['gmin'], r['tau_g'] = g, tau
print('tiempo %.0f s, %d posiciones' % (time.time()-t0, len(taus)))
for (a,b), r in sorted(res.items(), key=lambda kv: (-kv[1]['vmax'], kv[1]['gmin'])):
    tp = r['taus_pisa']
    print('%-18s %-18s vmax %9.4f mm3 @%s   gmin %.3f @%s   pisa en %d pos %s' % (a, b, r['vmax'], r['tau_v'], r['gmin'], r['tau_g'], len(tp), ('[%s..%s]' % (min(tp), max(tp))) if tp else ''))
json.dump({'%s|%s' % k: v for k, v in res.items()}, open('c1_barrido.json','w'))
