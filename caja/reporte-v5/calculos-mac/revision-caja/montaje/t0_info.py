from comun import *
for n in P:
    b = S[n].bounding_box()
    print('%-18s %-12s vol %10.1f  x %7.2f..%7.2f y %7.2f..%7.2f z %8.2f..%7.2f' % (n, P[n].mueve[:12], S[n].volume(), b[0], b[3], b[1], b[4], b[2], b[5]))
for k in sorted(d): print(k, d[k])
print(d2.keys()); print({k: v for k, v in d2.items() if isinstance(v, float)})
