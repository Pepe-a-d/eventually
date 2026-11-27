# Eventually — Late Edition · 1 of 1

Un reloj montado a mano por Pepe para su amigo Pablo, con su web, su tarjeta de autenticidad y su caja impresa en 3D. **Todo el proyecto está en este repositorio**, para que la sesión de Claude del Mac y la del PC trabajen sobre lo mismo.

## Si eres una sesión de Claude y te han dicho «lee el git»

Con este repositorio tienes todo. Haz esto, en orden:

1. `git pull`.
2. Lee [ESTADO.md](ESTADO.md), [RELEVO.md](RELEVO.md) y [COMO-TRABAJAMOS.md](COMO-TRABAJAMOS.md).
3. Mira en la última entrada de `RELEVO.md` lo que te han dejado pendiente, y hazlo o di por qué no.
4. Rellena lo que sepas de la lista «Huecos por rellenar» de [DECISIONES.md](DECISIONES.md) y corrige lo que esté mal en [HISTORIA.md](HISTORIA.md): tú sabes cosas de tus conversaciones con Pepe que la otra sesión no ha visto.
5. Antes de subir nada, dile a Pepe qué vas a subir y espera su «sí».

## Empieza aquí

Léelos en este orden antes de tocar nada:

1. **[ESTADO.md](ESTADO.md)**: qué está activo, qué está parado y qué se descartó.
2. **[RELEVO.md](RELEVO.md)**: qué hizo la última sesión y qué dejó pendiente para la siguiente.
3. **[COMO-TRABAJAMOS.md](COMO-TRABAJAMOS.md)**: las reglas comunes del Mac y del PC.

Para entender cómo se llegó hasta aquí:

- **[HISTORIA.md](HISTORIA.md)**: lo que se hizo, paso a paso.
- **[DECISIONES.md](DECISIONES.md)**: cada decisión con lo que llevó a tomarla, y cómo apuntar las nuevas.

## Qué hay en cada carpeta

| Carpeta | Qué es | Estado |
| --- | --- | --- |
| `docs/` | **La web publicada.** GitHub obliga a que se llame `docs`. En el Mac era `site/` | Activa |
| `web-fuentes/` | De dónde sale la web: fotos de las piezas, imágenes de la película, guion, prompts y herramientas | Activa |
| `web-fuentes/tutorial-caja/` | El guion que genera los fotogramas del tutorial de la caja | Rehecho el 27-nov con la caja v5. El de la v4.1, en `v4.1/` |
| `tarjeta/` | La tarjeta de autenticidad, lista para imprimir | Terminada, sin imprimir |
| `qr/` | El QR de la web, en azul y en negro | Terminado |
| `caja/` | **La caja actual, v5:** `BRIEF-v5.md` y `resultados-probetas.md`. Aquí irá lo nuevo | Activa |
| `caja/historico/` | Todo lo de la caja de la v0 a la v4.1, tal como estaba | Parado |
| `sesiones/` | El resumen que llevaba la sesión del Mac y el LEEME del repositorio antiguo | Historia |

## La web

- Dirección: <https://pepe-a-d.github.io/eventually/>. Es la del QR de la tarjeta y la de la etiqueta NFC: **no puede cambiar**.
- Se publica sola: GitHub Pages sirve la rama `main`. Todo lo que llega a `main` dentro de `docs/` queda publicado.
- GitHub Pages está puesto en *Branch: `main`, carpeta `/docs`* desde el 21 de noviembre de 2026. El `index.html` de la raíz, que redirigía a `docs/` mientras tanto, ya no existe.

## De dónde viene cada cosa

Hasta el 20 de noviembre de 2026 el proyecto estaba repartido en tres repositorios y dos carpetas. Los repositorios `eventually-caja` y `eventually-proyecto` ya no se usan: están archivados, de solo lectura, desde el 21 de noviembre.

| Antes | Ahora |
| --- | --- |
| Repositorio `eventually` (carpeta `site/` del Mac) | `docs/` |
| Repositorio `eventually-proyecto` (carpeta `~/Watchpage` del Mac) | `web-fuentes/`, `tarjeta/`, `qr/` y `sesiones/` |
| Repositorio `eventually-caja` (carpeta `caja/` del Mac, `WatchBox` del PC) | `caja/historico/`, salvo `BRIEF-v5.md` y `resultados-probetas.md`, que suben a `caja/` |
| Vídeo de la caja v4.1 (solo en el PC) | `caja/historico/video-v4.1/` |
| Guion del tutorial de la web (solo en el PC) | `web-fuentes/tutorial-caja/` |

Se copió el estado de cada repositorio en estos commits: `eventually` `7b8f16b`, `eventually-caja` `60fa03a`, `eventually-proyecto` `e7346fa`. El historial fichero a fichero de la caja y de las fuentes sigue en los repositorios antiguos.
