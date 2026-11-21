# Las dos funciones de t1_pasos.py, para usarlas desde otros programas.
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
