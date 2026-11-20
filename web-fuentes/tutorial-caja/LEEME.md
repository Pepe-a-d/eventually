# Guion de los fotogramas del tutorial de la caja

Con esto se generaron los 189 fotogramas de `docs/frames/caja/` (20 de noviembre de 2026, sesión del PC). Describen la caja **v4.1, que está parada**: con la v5 hay que rehacerlos.

| Fichero | Qué es |
| --- | --- |
| `web.html`, `web.js` | La escena en three.js: piezas, luces, cámara y línea de tiempo (función `estado`) |
| `renderweb.mjs` | Abre la escena en Chrome sin ventana y guarda un PNG transparente por fotograma. Los tramos están en `TRAMOS` |
| `prueba.mjs` | Abre la web y hace capturas del tutorial en móvil y en escritorio |
| `graba.mjs` | Graba un vídeo de la web recorriendo el tutorial |
| `mallas-v4.1.zip` | Las piezas del modelo v4.1, exportadas de Fusion como mallas, y `datos.json` con sus medidas |
| `package.json` | Lo que hay que instalar con `npm install` |

## Cómo se usa

1. `npm install` en esta carpeta. Hace falta Node 20 o más y Google Chrome.
2. Descomprimir `mallas-v4.1.zip` en una carpeta `mallas/` aquí mismo.
3. `node renderweb.mjs todo` deja los PNG en `webpng/`.
4. Pasarlos a WebP en dos tamaños (1080 × 1934 y 720 × 1290) y copiarlos a `docs/frames/caja/d` y `m`.
5. Si cambia el número de fotogramas, poner al día `timeline` en `docs/frames/caja/manifest.json` y los rangos `data-caja-range` de `docs/index.html`. Van emparejados.

## Ojo

- `renderweb.mjs`, `prueba.mjs` y `graba.mjs` llevan escritas las rutas de la máquina donde se usaron (`/usr/bin/google-chrome`, `/home/claude/work/sitio`). Hay que cambiarlas.
- `web.js` hereda de la escena del vídeo (`caja/historico/video-v4.1/escena.js`) y conserva código que la web no usa: rótulos, despiece y emergencia.
- El paso 4 se hizo con un programa de Python suelto (Pillow, calidad 80 y 64, con transparencia). No está guardado como fichero.
