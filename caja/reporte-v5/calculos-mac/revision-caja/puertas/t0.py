from comun import *
for k in sorted(d): print(k, d[k])
print(d2.keys())
for k in ('canto_junta','rec_x','r_reb','pasador_largo'): print(k, d2[k])
for tau in (0,45,50,55,60,63,65,70,75,80,83,85,90,92,95,100,105,345):
    print(tau, [round(v,3) for v in D.movimiento(p,d,tau)])
