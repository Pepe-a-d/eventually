# 1. Cifras del reporte contra el modelo
from comun import *
print('--- medidas generales')
todo = [n for n in CAJA if n not in ('reloj_de_pega', 'soporte')]
B = np.array([bb(S[n]) for n in todo]); print('caja sin funda (sin reloj/soporte): x %.2f y %.2f z %.2f  (min %s max %s)' % (B[:,3].max()-B[:,0].min(), B[:,4].max()-B[:,1].min(), B[:,5].max()-B[:,2].min(), B[:,:3].min(0), B[:,3:].max(0)))
b = bb(S['cuerpo']); print('cuerpo bbox', [round(v,2) for v in b], 'lado x %.2f, fondo y %.2f (con el indice)' % (b[3]-b[0], b[4]-b[1]))
b = bb(S['funda']); print('funda', b[3]-b[0], b[4]-b[1], b[5]-b[2])
print('cuerpo_lado', d['cuerpo_lado'], 'caja_alto', d['caja_alto'], 'bisel_r_ext*2', 2*d['bisel_r_ext'], 'bisel ala d', 2*d['bisel_ala_r'])
for sx in (1,-1):
    a = puerta(sx, 90.0); b = bb(a); print('puerta %+d abierta 90: z max %.2f  x de %.2f a %.2f' % (sx, b[5], b[0], b[3]))
    # por mitades en Y
    for y0,y1 in ((-40,0),(0,40)):
        c = a ^ caja(-100,y0,-50,100,y1,60); print('    mitad y %d..%d: z max %.2f, x min/max %.2f %.2f' % (y0,y1,bb(c)[5], bb(c)[0], bb(c)[3]))
r = puesta('reloj_de_pega', G); print('reloj arriba: z de %.2f a %.2f; bbox %s' % (bb(r)[2], bb(r)[5], [round(v,2) for v in bb(r)]))
s = puesta('soporte', G); print('soporte arriba bbox', [round(v,2) for v in bb(s)])
pf = puesta('plataforma', G); print('plataforma arriba z max %.3f ; abajo z max %.3f; recorrido %.2f' % (bb(pf)[5], bb(S['plataforma'])[5], d['recorrido']))
print('--- bisel')
bi = S['bisel']
for z in (-0.5, -4, -7.5, -8.5, -12):
    cs = bi.slice(z); pol = cs.to_polygons(); rr = np.concatenate([np.hypot(q[:,0], q[:,1]) for q in pol]); print('  bisel z=%.1f r max %.3f r min %.3f  contornos %d' % (z, rr.max(), rr.min(), len(pol)))
# numero de estrias: contar minimos locales del radio del contorno exterior a z=-3
cs = bi.slice(-3.0).to_polygons(); ext = max(cs, key=lambda q: np.hypot(q[:,0],q[:,1]).max()); r = np.hypot(ext[:,0],ext[:,1]); bajo = r < d['bisel_r_ext']-0.3
print('  estrias (tramos hundidos en el contorno exterior):', int(np.sum(bajo & ~np.roll(bajo,1))), ' hondo %.2f' % (d['bisel_r_ext']-r.min()))
ang = np.degrees(np.arctan2(ext[:,1],ext[:,0])); 
print('  ancho de estria 2.0 mm; paso %.2f mm; lomo %.2f mm' % (2*math.pi*d['bisel_r_ext']/120, 2*math.pi*d['bisel_r_ext']/120-2.0))
print('  estrias en altura: de z=%.1f a 0 -> %.1f mm de los %.1f que asoman' % (d['z_cuerpo_arriba']+1.0, -(d['z_cuerpo_arriba']+1.0), p['bisel_visto']))
print('--- engranajes')
print('relacion', d['relacion'], 102/180, 'giro bisel', d['giro_bisel'], 'vueltas', d['giro_bisel']/360)
print('paso rampa %.3f mm/vuelta tubo; por vuelta de bisel %.2f' % (d['rampa_paso'], d['rampa_paso']*d['relacion']))
for rc in (76.0, 77.3, 77.5, 78.6): print('  pendiente a r=%.1f: %.2f grados' % (rc, math.degrees(math.atan(d['rampa_paso']/(2*math.pi*rc)))))
# dientes del satelite: grueso por radios, del solido
sat = S['satelite_1']; c = CP.pol(d['r_ejes'], 270.0)
cs = sat.translate([-c[0], -c[1], 0]).slice(-6.0)
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
pols = cs.to_polygons(); ext = max(pols, key=lambda q: np.hypot(q[:,0],q[:,1]).max()); G2 = Polygon(ext)
rmax = np.hypot(ext[:,0],ext[:,1]).max(); rmin = np.hypot(ext[:,0],ext[:,1]).min(); print('satelite r punta %.3f r fondo %.3f, dientes:' % (rmax, rmin))
for nombre, r in (('punta (r_a)', rmax-1e-4), ('punta -0.05', rmax-0.05), ('primitivo', 9.0), ('media altura', (rmax+rmin)/2), ('base rb', 9*math.cos(math.radians(20)))):
    circ = Point(0,0).buffer(r, 720).exterior
    inter = circ.intersection(G2)
    segs = list(inter.geoms) if hasattr(inter,'geoms') else [inter]
    L = sorted(s_.length for s_ in segs if s_.length>1e-6)
    print('  %-14s r=%.3f  arcos dentro del diente: n=%d  min %.3f  mediana %.3f mm' % (nombre, r, len(L), L[0] if L else 0, L[len(L)//2] if L else 0))
# lo mismo para la rueda central y el bisel
ce = S['rueda_central'].slice(-6.0).to_polygons(); ext = max(ce, key=lambda q: np.hypot(q[:,0],q[:,1]).max()); r = np.hypot(ext[:,0],ext[:,1]); print('rueda central z=-6: r max %.3f (punta %.3f) ; n dientes por cruces del primitivo:' % (r.max(), d['central_punta']), end=' ')
G3 = Polygon(ext); inter = Point(0,0).buffer(d['r_central'], 2000).exterior.intersection(G3); L = sorted(s_.length for s_ in inter.geoms); print(len(L), 'grueso primitivo %.3f' % L[len(L)//2])
inter = Point(0,0).buffer(d['central_punta']-1e-3, 2000).exterior.intersection(G3); L = sorted(s_.length for s_ in inter.geoms if s_.length>1e-6); print('   punta central: n %d, %.3f mm' % (len(L), L[len(L)//2]))
bs = S['bisel'].slice(-6.0).to_polygons(); inn = min(bs, key=lambda q: np.hypot(q[:,0],q[:,1]).max()); r = np.hypot(inn[:,0],inn[:,1]); print('bisel dentado z=-6: r min %.3f (punta %.3f) r max %.3f (fondo %.3f)' % (r.min(), d['bisel_punta'], r.max(), d['bisel_fondo']))
G4 = Polygon(inn); 
for nombre, rr in (('primitivo', d['r_bisel']), ('punta', d['bisel_punta']+1e-3)):
    circ = Point(0,0).buffer(rr, 4000).exterior; fuera = circ.difference(G4); L = sorted(s_.length for s_ in (fuera.geoms if hasattr(fuera,'geoms') else [fuera]) if s_.length>1e-6); print('   bisel %s: dientes %d, grueso %.3f' % (nombre, len(L), L[len(L)//2]))
print('diente_grueso teorico', d['diente_grueso'], ' = pi*m/2 - juego/2 ->', math.pi*1.5/2, '-', p['juego_dientes']/2)
print('--- volumen')
V = {n: S[n].volume() for n in P}
tot_json25 = sum(V[n] for n in CAJA); print('suma de las 25 entradas (con reloj de pega, soporte, sin funda/frase?):', CAJA.__len__(), tot_json25/1000)
print('  todas menos probetas (25):', sum(V[n] for n in P if P[n].mueve!='probeta')/1000, 'n', len([n for n in P if P[n].mueve!='probeta']))
print('  sin reloj de pega (24):', sum(V[n] for n in P if P[n].mueve!='probeta' and n!='reloj_de_pega')/1000)
print('  sin reloj ni soporte:', sum(V[n] for n in P if P[n].mueve!='probeta' and n not in ('reloj_de_pega','soporte'))/1000)
print('  sin reloj ni frase ni funda:', sum(V[n] for n in P if P[n].mueve not in ('probeta','funda') and n not in ('reloj_de_pega',))/1000)
print('  masa PLA 1.24 g/cm3 de 1367:', 1367*1.24, ' de la suma sin reloj:', sum(V[n] for n in P if P[n].mueve!='probeta' and n!='reloj_de_pega')/1000*1.24)
print('--- tabla de piezas: bbox')
for n in P:
    b = bb(S[n]); print('  %-18s %7.2f x %7.2f x %7.2f   vol %10.1f  trozos %d' % (n, b[3]-b[0], b[4]-b[1], b[5]-b[2], V[n], len(S[n].decompose())))
print('pasador largo d2', d2['pasador_largo'], 'canto_junta', d2['canto_junta'])
print('--- recorrido / tramos')
def tau_de(f, lo, hi):
    for _ in range(60):
        m = (lo+hi)/2
        if f(m): hi = m
        else: lo = m
    return hi
t_psi25 = tau_de(lambda t: D.movimiento(p,d,t)[1] >= p['aro_reposo'], 45, 100); t_psi85 = tau_de(lambda t: D.movimiento(p,d,t)[1] >= p['aro_reposo']+p['aro_cambio'], 45, 100)
t_a0 = tau_de(lambda t: D.movimiento(p,d,t)[2] > 0.01, 45, 100); t_a90 = tau_de(lambda t: D.movimiento(p,d,t)[2] > 89.99, 45, 100)
print('aro sale del reposo a tau=%.2f; termina el cambio a tau=%.2f; puerta >0.01 a %.2f; >89.99 a %.2f; el aro termina de girar a tau=%.1f' % (t_psi25, t_psi85, t_a0, t_a90, p['giro_puertas_fin']))
for t in (45, 63, 83, 92, 100, 335, 345): print('  tubo %5.1f -> bisel %6.1f ; mov %s' % (t, t/d['relacion'], [round(v,3) for v in D.movimiento(p,d,t)]))
print('  a tau=92 el aro lleva %.2f de %.2f grados; a tau=100 la plataforma ha subido %.2f mm' % (D.movimiento(p,d,92)[1], d['aro_giro'], D.movimiento(p,d,100)[3]))
# inclinacion de la pista respecto al giro del aro
peor = 0
def en_aro(q):
    x = d['eje_x'] + D.bola_x(p, d, q); return math.hypot(x, d['bola_y']), math.degrees(math.atan2(d['bola_y'], x)) - p['aro_sentido']*q
for i in range(1, 2000):
    psi = d['aro_giro']*i/2000; e = 0.005
    r1,a1 = en_aro(psi-e); r2,a2 = en_aro(psi+e)
    if abs(r2-r1)>1e-12:
        v = abs(math.degrees(math.atan2(r2-r1, math.radians(a2-a1)*(r1+r2)/2))); v = min(v, 180-v); peor = max(peor, v)
print('pista: inclinacion maxima respecto a un circulo: %.2f grados (reporte 28; fase 1 dice 30)' % peor)
print('aro_giro', d['aro_giro'], 'teton', bb(S['teton']), 'manivela_r', p['manivela_r'])
