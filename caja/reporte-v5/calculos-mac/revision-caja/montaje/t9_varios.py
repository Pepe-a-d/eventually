# Comprobaciones sueltas:
#  a) paso 12 de otra manera: bisel primero sobre el plato y despues el cuerpo solo, desde arriba
#  b) el reloj de pega y el soporte: se pueden separar en alguna direccion recta? (el brazalete es un aro cerrado)
#  c) plato con las puertas abiertas, y satelites: que eje queda al frente
#  d) superficies de apoyo boca abajo: labio de la rueda central sobre la meseta, dedos bajo el techo del bisel, llaves sobre el cuello
#  e) el aro desplazado dentro de su holgura con las DOS puertas puestas: cuanto cabe
from comun import *
from t1_pasos_fn import camino, informe
M = {n: puesta(n, 0) for n in DENTRO if n not in ('cuerpo', 'soporte', 'reloj_de_pega')}
print('a) cuerpo solo, bajando 120 mm con el bisel ya puesto sobre el plato:'); informe('cuerpo', camino(S['cuerpo'], M))
print('   bisel solo, sin cuerpo, subiendo: nada lo sujeta ->', 'libre' if not camino(S['bisel'], {k: v for k, v in M.items() if k != 'bisel'}, desde=30.0) else 'pisa')
print('   bisel con el cuerpo puesto, subiendo 0,5 mm: pisa al cuerpo %.1f mm3' % vol(S['bisel'].translate([0, 0, 0.5]), S['cuerpo']))
print('b) reloj de pega respecto al soporte (los dos en la plataforma), 60 mm en linea recta:')
so, re = puesta('soporte', G), puesta('reloj_de_pega', G)
for nombre, g in (('+Z', (0, 0, 1)), ('-Z', (0, 0, -1)), ('+X', (1, 0, 0)), ('-X', (-1, 0, 0)), ('+Y', (0, 1, 0)), ('-Y', (0, -1, 0))):
    e = 0.0
    while e < 60 and vol(re.translate([g[0] * (e + 0.2), g[1] * (e + 0.2), g[2] * (e + 0.2)]), so) <= 0.05: e += 0.2
    print('   hacia %s: %s' % (nombre, 'libre' if e >= 60 else 'se mueve %.1f mm y pisa al soporte' % e))
print('d) superficies de apoyo con la caja boca abajo (solape en planta, medido subiendo 0,5 mm la pieza que cuelga):')
def apoyo(a, b, dz=0.5, previo=0.0):
    v = vol(S[a].translate([0, 0, previo + dz]), S[b]) - vol(S[a].translate([0, 0, previo]), S[b])
    return v / dz
print('   bisel sobre el labio del cuerpo (tras 0,4 mm): %.0f mm2' % apoyo('bisel', 'cuerpo', 0.5, 0.4))
print('   rueda central (dedos) bajo el techo en cono del bisel (tras 0,3 mm): %.0f mm2 en planta' % apoyo('rueda_central', 'bisel', 0.5, 0.3))
print('   meseta bajo el labio de la rueda central: %.0f mm2' % apoyo('meseta', 'rueda_central', 0.3))
print('   marco bajo las llaves de la rueda central: %.0f mm2' % apoyo('marco', 'rueda_central', 0.3))
print('   marco bajo la meseta (cuello): %.0f mm2' % apoyo('marco', 'meseta', 0.3))
print('   plato bajo el bisel: %.0f mm2' % apoyo('plato', 'bisel', 0.3))
print('   tubo bajo el plato: %.0f mm2' % apoyo('tubo', 'plato', 0.3))
print('   plataforma (tetones) en las ranuras del tubo (tras 0,3 mm): %.1f mm3 al subir 0,5 mm mas' % (vol(S['plataforma'].translate([0, 0, 0.8]), S['tubo'])))
vc = sum(S[n].volume() for n in ('marco', 'meseta', 'puerta_derecha', 'puerta_izquierda', 'pasador_derecho', 'pasador_izquierdo')) / 1000
print('   de la rueda central cuelgan boca abajo: marco, meseta, puertas y pasadores = %.0f cm3 macizos, mas el reloj y su soporte si caen sobre las puertas' % vc)
print('e) aro desplazado en X dentro de su holgura (%.2f mm), con las dos puertas cerradas en su sitio:' % (d['cuello_r_in'] - d['aro_r_ext']))
otros = {n: M[n] for n in ('puerta_derecha', 'puerta_izquierda', 'marco', 'meseta', 'teton', 'plato')}
for dx in (-0.3, -0.25, -0.2, -0.15, -0.1, 0.1, 0.2, 0.3):
    c = choque(M['aro_puertas'].translate([dx, 0, 0]), otros, 0.02)
    print('   aro %.2f mm en X: pisa %s' % (dx, c or 'nada'))
