# Cómo se dibujan las vistas en perspectiva de la caja v5

1. `python3 ../caja_render_v5.py <carpeta>` escribe en esa carpeta una malla por vista (`*.json`).
2. `node render_caja.mjs <carpeta> <carpeta-de-png> ../caja-v5-vistas.json` las dibuja con three.js en un Chrome sin pantalla (hace falta `puppeteer-core`, `three` y Chrome; las rutas de arriba del fichero son las de la sesión del PC y hay que cambiarlas).
3. `python3 ../caja_figuras_v5.py laminas <carpeta-de-png>` monta las láminas del reporte. `python3 ../caja_figuras_v5.py cortes` hace los cortes, que no necesitan lo anterior.
