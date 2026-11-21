# Cómo se dibujan las vistas en perspectiva de la caja v5

1. `python3 ../caja_render_v5.py <carpeta>` escribe en esa carpeta una malla por vista (`*.json`).
2. `node render_caja.mjs <carpeta> <carpeta-de-png> ../caja-v5-vistas.json` las dibuja con three.js en un Chrome sin pantalla (hace falta `puppeteer-core`, `three` y Chrome; las rutas de arriba del fichero son las de la sesión del PC y hay que cambiarlas).
3. `python3 ../caja_figuras_v5.py laminas <carpeta-de-png>` monta las láminas del reporte. `python3 ../caja_figuras_v5.py cortes` hace los cortes, que no necesitan lo anterior.

## La animación (`../video-v5/eventually-caja-v5-como-funciona.mp4`)

1. `python3 ../caja_animacion_v5.py <carpeta>` escribe `mallas.json`: cada pieza una vez, con la caja cerrada, y la tabla de movimiento.
2. `node anim.mjs 0 1` dibuja los 2.160 cuadros (72 s a 30 por segundo, 1280 × 720) en trozos de 90, cada uno directo a un `.mp4`; los que ya existen se saltan. `anim.html` coloca las piezas en cada cuadro y tapa los cortes con el color de cada pieza. Las escenas y los textos están arriba de `anim.mjs`.
3. Los trozos se unen sin recodificar: `node anim.mjs lista` da el orden para `ffmpeg -f concat`.

Sin sonido. Tarda unos 45 minutos en una máquina sin tarjeta gráfica.
