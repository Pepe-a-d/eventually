# Guion de los fotogramas del tutorial de la caja

Con esto se generan los 189 fotogramas de `docs/frames/caja/`, su póster, su `manifest.json` y la imagen de la vista previa del enlace (`docs/img/enlace.jpg`).

**Desde el 27 de noviembre de 2026 describen la caja v5** (puertas y ascensor), tal como está el modelo del 25-nov. Lo hizo la sesión del PC. Las piezas salen directamente del modelo (`caja/caja_piezas_v5.py`): no pasan por Fusion y no hay mallas guardadas. **Si el modelo cambia a la vista, se repiten los cuatro pasos de abajo.**

| Fichero | Qué es |
| --- | --- |
| `mallas_v5.py` | Saca del modelo las piezas, cómo se mueve cada una y la tabla del movimiento. Escribe `piezas.json` |
| `caja5.html`, `caja5.js` | La escena en three.js: luz, cámara y guion (función `estado`). El movimiento de las piezas es el mismo que `mover` de `caja_piezas_v5.py` |
| `render5.mjs` | Abre la escena en Chrome sin ventana y guarda un PNG transparente por fotograma. Los tramos están en `TRAMOS` |
| `a_webp.py` | Pasa los PNG a WebP en dos tamaños (1080 × 1934, calidad 80, y 720 × 1290, calidad 64), y escribe el póster y `manifest.json` |
| `prueba5.mjs` | Sirve `docs/` y hace capturas del tutorial en móvil y en escritorio |
| `package.json` | Lo que hay que instalar con `npm install` |
| `v4.1/` | El guion de la caja v4.1, que está parada. Se guarda como historia |

## Cómo se usa

Hace falta Python con `manifold3d`, `numpy`, `shapely` y `Pillow` (lo mismo que el modelo), Node 20 o más y Google Chrome.

1. `npm install` en esta carpeta.
2. `python3 mallas_v5.py /tmp/tut5/datos`
3. `node render5.mjs /tmp/tut5/datos /tmp/tut5/png todo` y `node render5.mjs /tmp/tut5/datos /tmp/tut5/png enlace`
4. `python3 a_webp.py /tmp/tut5/png ../../docs` y `python3 a_webp.py /tmp/tut5/png ../../docs enlace`

Para ver unos pocos instantes antes de hacerlos todos: `node render5.mjs /tmp/tut5/datos /tmp/tut5/fotos fotos 0 3.5 7.7`.

Para probar la web: `node prueba5.mjs ../../docs /tmp/tut5/capturas` (primera visita) y `node prueba5.mjs ../../docs /tmp/tut5/capturas movil 0,0.5,1 reloj`.

## El guion

| Tramo | Segundos | Fotogramas | Qué pasa |
| --- | --- | --- | --- |
| La funda | 0 a 1,5 | 0 a 24 | La funda sube y se va |
| El giro | 1,5 a 3,5 | 24 a 54 | El aro gira 79° y no pasa nada: solo se mueven los engranajes |
| Las puertas | 3,5 a 5,7 | 54 a 88 | Sigue girando y las dos puertas se abren |
| El reloj | 5,7 a 7,7 | 88 a 118 | Sigue hasta el tope (609° de aro en total) y el reloj sube |
| Fuera | 7,7 a 9,3 | 118 a 142 | El soporte sale hacia arriba y queda en la mesa |
| Para cerrar | 9,3 a 13 | 142 a 188 | Todo al revés, y la funda |

Los fotogramas en que acaba cada tramo son las paradas de `timeline` en `docs/frames/caja/manifest.json`, y van emparejadas con los `data-caja-range` de `docs/index.html`. Si cambia el número de fotogramas de un tramo, hay que tocar los tres sitios: `TRAMOS` en `render5.mjs`, `PARADAS` y `TIMELINE` en `a_webp.py`, y los rangos de la página.

## Ojo

- **La caja no está impresa y las medidas del reloj son supuestas.** El tutorial enseña el modelo.
- El reloj es un maniquí gris, a propósito: la primera visita no debe enseñar el reloj (D-05).
- La flecha azul no es una pieza: es una ayuda del dibujo para decir hacia dónde se gira.
- Lo dibujado tiene que quedar entre el 11 % y el 88 % del ancho del fotograma y entre el 8 % y el 63 % del alto: en un móvil estrecho la página recorta los lados (hasta un 10 % por cada uno) y debajo va el texto, con un velo que empieza al 56 % de la pantalla. Lo mide `prueba5.mjs` a ojo y se puede medir con la transparencia de los PNG.
- En escritorio el lienzo de la caja mide 1,4 veces el alto de la pantalla y está colocado para que el 40 % del alto del fotograma caiga en el centro (`docs/caja.css`). Si se mueve la caja dentro del fotograma, hay que tocar ese 0,4.
