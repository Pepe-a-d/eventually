# Los 13 pasos del apartado 7: cada pieza nueva recorre su camino de entrada en pasos de 0,5 mm
# y se calcula el volumen comun con todo lo ya montado. Umbral: 0,05 mm3.
from comun import *
PASO = 0.5
def camino(nuevo, montado, direc=(0, 0, 1), desde=120.0, paso=PASO, umbral=0.05, hasta=0.0):
    """nuevo: solido en su sitio final. Se coloca desplazado 'desde' mm a lo largo de 'direc' y se acerca hasta 'hasta'.
    Devuelve dict nombre -> (vol max, desplazamiento donde ocurre, primer desplazamiento (el mas lejano) donde pisa, ultimo)."""
    res = {}
    n = int(round((desde - hasta) / paso))
    for i in range(n + 1):
        e = desde - i * paso
        s = nuevo.translate([direc[0] * e, direc[1] * e, direc[2] * e])
        for nm, v in choque(s, montado, umbral):
            r = res.get(nm)
            if r is None: res[nm] = [v, e, e, e]
            else:
                if v > r[0]: r[0], r[1] = v, e
                r[3] = e
    return res
def informe(titulo, res):
    if not res: print('  OK    %s: no pisa nada en todo el camino' % titulo)
    else:
        for nm, (v, e, e0, e1) in res.items():
            print('  PISA  %s: con %s, max %.2f mm3 a %.1f mm de su sitio; pisa desde %.1f hasta %.1f mm' % (titulo, nm, v, e, e0, e1))
t0 = time.time()
M = {}                                             # lo ya montado
def pon(n, s=None): M[n] = s if s is not None else puesta(n, 0.0)
pon('base')
print('Paso 1: plataforma, bajando en vertical'); informe('plataforma', camino(puesta('plataforma', 0), M)); pon('plataforma')
print('Paso 2: tubo, bajando en vertical (tubo en 0 grados)'); informe('tubo', camino(puesta('tubo', 0), M)); pon('tubo')
print('Paso 3: marco'); informe('marco', camino(puesta('marco', 0), M)); pon('marco')
print('Paso 4: aro, en cerrado y en abierto')
informe('aro (cerrado)', camino(puesta('aro_puertas', 0), M)); informe('aro (abierto)', camino(puesta('aro_puertas', G), M))
pon('aro_puertas', puesta('aro_puertas', G))
print('Paso 5: meseta (aro en abierto y en cerrado)')
informe('meseta, aro abierto', camino(S['meseta'], M))
M2 = dict(M); M2['aro_puertas'] = puesta('aro_puertas', 0); informe('meseta, aro cerrado', camino(S['meseta'], M2))
pon('meseta')
print('Paso 6: puertas de pie (90 grados), aro en abierto')
informe('puerta derecha (sin la izquierda)', camino(puerta(1, 90), M)); 
informe('puerta izquierda (sin la derecha)', camino(puerta(-1, 90), M))
M['puerta_derecha'] = puerta(1, 90)
informe('puerta izquierda (con la derecha puesta)', camino(puerta(-1, 90), M)); M['puerta_izquierda'] = puerta(-1, 90)
print('Paso 7: pasadores, a lo largo de Y')
for n in ('pasador_derecho', 'pasador_izquierdo'):
    informe(n + ' desde atras (+Y)', camino(S[n], M, (0, 1, 0)))
    informe(n + ' desde delante (-Y)', camino(S[n], M, (0, -1, 0)))
    pon(n)
print('Paso 8: rueda central (puertas de pie)'); informe('rueda central', camino(S['rueda_central'], M)); pon('rueda_central')
print('Paso 9: se cierran las puertas con el aro; se recorre el giro del aro de abierto a cerrado y despues baja el teton')
peor = {}
for tau in np.arange(100.0, 44.9, -1.0):
    A = {n: puesta(n, tau) for n in ('aro_puertas', 'puerta_derecha', 'puerta_izquierda')}
    for a in A:
        for nm, v in choque(A[a], {k: v for k, v in M.items() if k not in A}, 0.02) + choque(A[a], {k: v for k, v in A.items() if k > a}, 0.02):
            if v > peor.get((a, nm), (0, 0))[0]: peor[(a, nm)] = (v, tau)
print('  cierre de puertas (tubo equivalente de 100 a 45): ', peor if peor else 'no pisa nada')
for n in ('aro_puertas', 'puerta_derecha', 'puerta_izquierda'): pon(n)
informe('teton', camino(puesta('teton', 0), M)); pon('teton')
print('Paso 10: plato, bajando en vertical, con la rueda central ya puesta (orden del reporte)')
informe('plato', camino(puesta('plato', 0), M))
print('   Orden alternativo: plato ANTES de la rueda central')
M3 = {k: v for k, v in M.items() if k != 'rueda_central'}
informe('plato sin rueda central', camino(puesta('plato', 0), M3)); M3['plato'] = puesta('plato', 0)
informe('rueda central despues del plato', camino(S['rueda_central'], M3))
pon('plato')
print('Paso 11: satelites')
for k in range(1, 7):
    informe('satelite_%d' % k, camino(S['satelite_%d' % k], M)); pon('satelite_%d' % k)
print('Paso 12a: bisel dentro del cuerpo, entrando por debajo (el bisel sube 120 mm por dentro del cuerpo)')
informe('bisel en cuerpo', camino(S['bisel'], {'cuerpo': S['cuerpo']}, (0, 0, -1)))
print('Paso 12b: cuerpo y bisel juntos, bajando sobre todo lo demas')
rb_ = camino(S['bisel'], M); informe('bisel', rb_)
rc_ = camino(S['cuerpo'], M); informe('cuerpo', rc_)
pon('bisel'); pon('cuerpo')
print('Paso 13: funda (caja cerrada)'); informe('funda', camino(S['funda'], M))
print('Paso 13: soporte y reloj con la caja CERRADA (tal como esta escrito el orden): bajando desde arriba')
informe('soporte', camino(puesta('soporte', 0), M)); informe('reloj', camino(puesta('reloj_de_pega', 0), M))
print('Paso 13: soporte y reloj con la caja ABIERTA (tubo a 345)')
MG = {n: puesta(n, G) for n in DENTRO if n not in ('soporte', 'reloj_de_pega')}
informe('soporte', camino(puesta('soporte', G), MG)); MG['soporte'] = puesta('soporte', G)
informe('reloj (vertical)', camino(puesta('reloj_de_pega', G), MG))
informe('reloj (de lado, +X)', camino(puesta('reloj_de_pega', G), MG, (1, 0, 0)))
informe('reloj (de lado, -X)', camino(puesta('reloj_de_pega', G), MG, (-1, 0, 0)))
informe('reloj (de frente, -Y)', camino(puesta('reloj_de_pega', G), MG, (0, -1, 0)))
print('tiempo %.0f s' % (time.time() - t0))
