# 3(b): el JSON del repo frente al regenerado con el codigo actual, operacion por operacion y volumen por volumen
import json, sys, re
R='<repositorio>/caja/'
A=json.load(open(R+'caja-v5-piezas.json',encoding='utf-8'))
B=json.load(open('regen/caja-v5-piezas.json',encoding='utf-8'))
print('claves', sorted(A)==sorted(B), sorted(A))
for k in A:
    if k=='piezas': continue
    print(k, 'IGUAL' if A[k]==B[k] else 'DISTINTO')
    if A[k]!=B[k] and isinstance(A[k],dict):
        for kk in set(A[k])|set(B[k]):
            if A[k].get(kk)!=B[k].get(kk): print('   ',kk, str(A[k].get(kk))[:80], str(B[k].get(kk))[:80])
print('piezas repo',len(A['piezas']),'regen',len(B['piezas']), list(A['piezas'])==list(B['piezas']))
def flat(o):
    out=[]
    def rec(x):
        if isinstance(x,(int,float)): out.append(float(x))
        elif isinstance(x,list):
            for y in x: rec(y)
        elif isinstance(x,dict):
            for kk in sorted(x):
                if kk not in('t','op','eje'): rec(x[kk])
    rec(o); return out
for n in A['piezas']:
    a=A['piezas'][n]; b=B['piezas'][n]
    msg=[]
    if len(a['ops'])!=len(b['ops']): msg.append('n ops %d/%d'%(len(a['ops']),len(b['ops'])))
    for i,(oa,ob) in enumerate(zip(a['ops'],b['ops'])):
        if oa==ob: continue
        if (oa['t'],oa['op'],oa.get('eje'))!=(ob['t'],ob['op'],ob.get('eje')): msg.append('op %d tipo distinto'%i); continue
        fa,fb=flat(oa),flat(ob)
        if len(fa)!=len(fb): msg.append('op %d (%s%s): n numeros %d/%d'%(i,oa['t'],oa['op'],len(fa),len(fb)))
        else:
            m=max(abs(x-y) for x,y in zip(fa,fb)); msg.append('op %d (%s%s): dif max %.5f'%(i,oa['t'],oa['op'],m))
    dv=a['volumen']-b['volumen']
    for k in ('color','mueve','nota'):
        if a[k]!=b[k]: msg.append('%s distinto'%k)
    print('%-18s vol repo %10.2f regen %10.2f dif %+.4f  %s'%(n,a['volumen'],b['volumen'],dv,'; '.join(msg) if msg else 'ops identicas'))
# caja-v5.json
A=json.load(open(R+'caja-v5.json',encoding='utf-8')); B=json.load(open('regen/caja-v5.json',encoding='utf-8'))
for k in A:
    if A[k]!=B.get(k):
        print('caja-v5.json clave',k,'DISTINTA')
        if isinstance(A[k],dict):
            for kk in set(A[k])|set(B[k]):
                if A[k].get(kk)!=B[k].get(kk): print('   ',kk,A[k].get(kk),B[k].get(kk))
        elif isinstance(A[k],list):
            for i,(x,y) in enumerate(zip(A[k],B[k])):
                if x!=y: print('   ',i,str(x)[:150],'|',str(y)[:150])
            print('   len',len(A[k]),len(B[k]))
print('claves solo en regen', set(B)-set(A), 'solo en repo', set(A)-set(B))
