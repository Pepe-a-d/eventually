# Hasta donde gira el aro 'a tope' con la mano (pasos 6 y 9), y que pasa en esos topes:
#  - en el tope de 'abierto': entra la puerta de pie?
#  - en el tope de 'cerrado': donde queda el teton, y asienta el plato?
from comun import *
from t1_pasos_fn import camino, informe
sen = p['aro_sentido']; PSI = d['aro_giro']
aro = lambda psi: S['aro_puertas'].rotate([0, 0, sen * psi])
xh, ze = d['eje_x'], d['eje_z']
fijo = {'marco': S['marco'], 'meseta': S['meseta']}
def tope(signo, extra):
    psi = PSI if signo > 0 else 0.0
    for i in range(1, 400):
        q = psi + signo * 0.05
        if choque(aro(q), {**fijo, **extra}, 0.05): return psi, choque(aro(q), {**fijo, **extra}, 0.05)
        psi = q
    return psi, []
# paso 6: sin puertas, aro a tope hacia abierto
pa, c = tope(+1, {}); print('paso 6: sin puertas, el aro gira hacia abierto hasta %.2f grados (su giro nominal es %.1f); lo para %s' % (pa, PSI, c))
M = dict(fijo); M['aro_puertas'] = aro(pa)
informe('   puerta derecha de pie con el aro en su tope de abierto (%.2f)' % pa, camino(puerta(1, 90), M, desde=40.0))
informe('   puerta izquierda de pie con el aro en su tope de abierto (%.2f)' % pa, camino(puerta(-1, 90), M, desde=40.0))
# margen: para que giros del aro entra la puerta de pie
vale = [q for q in np.arange(6.0, pa + 0.001, 0.25) if not camino(puerta(1, 90), {**fijo, 'aro_puertas': aro(q)}, desde=14.0)]
print('   la puerta de pie entra con el aro entre %.2f y %.2f grados' % (min(vale), max(vale)))
# con las puertas puestas de pie y los pasadores: tope de abierto
P90 = {'puerta_derecha': puerta(1, 90), 'puerta_izquierda': puerta(-1, 90), 'pasador_derecho': S['pasador_derecho'], 'pasador_izquierdo': S['pasador_izquierdo']}
pa2, c = tope(+1, P90); print('   con las puertas de pie, el aro sigue hasta %.2f grados; lo para %s' % (pa2, c))
# paso 9: puertas cerradas, aro a tope hacia cerrado
P0 = {'puerta_derecha': S['puerta_derecha'], 'puerta_izquierda': S['puerta_izquierda'], 'pasador_derecho': S['pasador_derecho'], 'pasador_izquierdo': S['pasador_izquierdo']}
pc, c = tope(-1, P0); print('paso 9: con las puertas cerradas, el aro gira hacia cerrado hasta %.2f grados (nominal 0); lo para %s' % (pc, c))
s_t = p['teton_recorrido'] * pc / PSI
print('   ahi el teton (que sigue la ranura del brazo) queda %.2f mm mas afuera que su sitio de cerrado' % (-s_t))
# el teton cabe ahi en el brazo y en el marco?
te = S['teton'].translate([0, -s_t, 0])
print('   teton en esa posicion: pisa %s' % (choque(te, {'marco': S['marco'], 'aro_puertas': aro(pc)}, 0.02) or 'nada'))
# el teton puede quedar en cualquier punto entre los dos? holgura del teton en la ranura del marco hacia fuera
e = 0.0
while e < 5 and not choque(S['teton'].translate([0, e + 0.05, 0]), {'marco': S['marco']}, 0.02): e += 0.05
print('   la ranura del marco deja al teton salir %.2f mm mas alla de su sitio de cerrado' % e)
for ds in (0.0, 0.1, 0.2, 0.3, 0.5, -s_t):
    v = vol(S['plato'], S['teton'].translate([0, ds, 0]))
    print('   plato en su sitio con el teton %.2f mm afuera: pisa %.2f mm3 %s' % (ds, v, '-> asienta' if v <= 0.05 else '-> NO asienta (se queda %.1f mm alto, sobre el teton)' % (S['teton'].bounding_box()[5] - S['plato'].bounding_box()[2])))
# el brazo del aro queda tapado por el plato?
b = S['aro_puertas'].bounding_box()
print('   brazo del aro: llega a %.1f mm de radio; el plato cubre de %.1f a %.1f mm: con el plato encima, el brazo %s' % (b[4], d['plato_r_in'], d['tubo_r_ext'], 'queda tapado' if b[4] < d['tubo_r_ext'] else 'asoma'))
# el aro, con el teton y el plato puestos, cuanto puede girar a cada lado (juego)
