# Eventually, tutorial de la caja en la web: pasa los PNG de render5.mjs a lo que usa la web.
#   python3 a_webp.py <png> <docs>            fotogramas WebP en dos tamanos, el poster y manifest.json, en <docs>/frames/caja/
#   python3 a_webp.py <png> <docs> enlace     solo <docs>/img/enlace.jpg, a partir de <png>/enlace.png
# Los fotogramas tienen el fondo transparente. 'timeline' del manifiesto va emparejado con los data-caja-range de docs/index.html.
import json, os, sys, time
from PIL import Image

PARADAS = [0, 24, 54, 88, 118, 142, 188]              # fotogramas en que acaba cada gesto (TRAMOS de render5.mjs)
# [cuanto se ha deslizado (0 a 1), fotograma]. Cada gesto ocupa un tramo largo de scroll y la imagen espera poco entre uno y otro
# (27-nov: Pepe vio las transiciones muy cortas y las esperas muy largas; antes los gestos ocupaban el 54 % del recorrido y ahora el 79 %).
TIMELINE = [[0, 0], [0.04, 0], [0.16, 24], [0.19, 24], [0.31, 54], [0.34, 54], [0.48, 88], [0.51, 88], [0.65, 118], [0.68, 118], [0.79, 142], [0.82, 142], [0.98, 188], [1.0, 188]]
TAMANOS = [('d', 1080, 1934, 80, 768), ('m', 720, 1290, 64, 0)]
POSTER = 118                                           # el poster: la caja abierta con el reloj arriba

def main(png, docs, que=None):
    if que == 'enlace':
        Image.open(os.path.join(png, 'enlace.png')).convert('RGB').save(os.path.join(docs, 'img', 'enlace.jpg'), quality=86, optimize=True, progressive=True)
        print('enlace.jpg', os.path.getsize(os.path.join(docs, 'img', 'enlace.jpg')))
        return
    fs = sorted(f for f in os.listdir(png) if f.startswith('f_') and f.endswith('.png'))
    assert len(fs) == PARADAS[-1] + 1, len(fs)
    tiers = []
    for nombre, w, h, q, minimo in TAMANOS:
        d = os.path.join(docs, 'frames', 'caja', nombre); os.makedirs(d, exist_ok=True); total = 0
        for f in fs:
            im = Image.open(os.path.join(png, f)).convert('RGBA')
            assert im.size == (1080, 1934), im.size
            if (w, h) != im.size: im = im.resize((w, h), Image.LANCZOS)
            sal = os.path.join(d, f[:-4] + '.webp'); im.save(sal, 'WEBP', quality=q, method=6, alpha_quality=90); total += os.path.getsize(sal)
        tiers.append({'name': nombre, 'path': 'frames/caja/' + nombre, 'pattern': 'f_%04d.webp', 'width': w, 'height': h, 'minViewportWidth': minimo, 'bytes': total})
        print(nombre, len(fs), 'fotogramas', round(total / 1e6, 2), 'MB')
    im = Image.open(os.path.join(png, fs[POSTER])).convert('RGBA').crop((0, 0, 1080, 1350)).resize((720, 900), Image.LANCZOS)
    im.save(os.path.join(docs, 'frames', 'caja', 'poster.webp'), 'WEBP', quality=82, method=6, alpha_quality=90)
    man = {'version': int(time.time()), 'frameCount': len(fs), 'aspect': 1080 / 1934, 'timeline': TIMELINE, 'poster': 'frames/caja/poster.webp', 'tiers': tiers}
    json.dump(man, open(os.path.join(docs, 'frames', 'caja', 'manifest.json'), 'w'), indent=2)
    print('manifest.json, version', man['version'])

if __name__ == '__main__':
    main(*sys.argv[1:])
