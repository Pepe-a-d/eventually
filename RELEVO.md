# Relevo

Notas de una sesión para la siguiente. **La más nueva, arriba.** Cada sesión deja una entrada al terminar, aunque sea corta.

Plantilla:

```
## AAAA-MM-DD HH:MM · sesión del Mac / del PC
- **Hecho:**
- **Cambió:** ficheros o carpetas.
- **A medias:**
- **Para la otra sesión:**
- **Para Pepe:**
```

---

## 2026-11-21 01:05 · sesión del PC

- **Hecho:** modelada la **probeta del iris** (encargo del apartado 11 de `caja/BRIEF-v5.md`), porque Pepe dijo «Empieza el modelado». Comprobada en plano grado a grado y medida en Fusion. **Sin imprimir.**
  - Cumple todo el encargo en el modelo **menos el diámetro: 133,5 mm, no 130.** Mi cálculo de D-23 (125 a 127) estaba mal. Explicado en D-27 y en el reporte, apartado 2.
  - Lo que más puede fallar: al cerrar, las láminas tienen que doblarse 1,1 mm en la punta (calculado). Por eso van los dos juegos, de 1,2 y de 0,8.
- **Cambió:** todo nuevo, dentro de `caja/`:
  - `reporte-v5/probeta-iris.md`: **el reporte. Empezar por aquí.** Con sus figuras y `comprobaciones-plano.txt`.
  - `probetas-v5/`: siete `.3mf` ya orientados y `comprobaciones-fusion.txt`.
  - `iris_diseno_v5.py` (las medidas, en `P_DEF`, y las comprobaciones; no necesita Fusion, sí numpy, scipy y shapely), `iris-v5.json` (lo que escribe), `generador_iris_v5.py` (se ejecuta en Fusion y lee ese fichero), `iris_figuras_v5.py`.
  - `Eventually-iris-v5.f3d`: el modelo montado. Hay también un `.step` de 18 MB, solo en el PC (`C:\Users\pepea\Documents\FusionClaude\WatchBox\Eventually-iris-v5.step`).
  - `ESTADO.md`, `DECISIONES.md` (D-27, **propuesta**; nota en D-23) e `HISTORIA.md`, al día.
- **A medias:** nada. En el Fusion del PC queda abierto un documento sin guardar, «Sin título», con el iris montado. No está en la nube de Autodesk. Los documentos de la v2, v3 y v4.1 ya no estaban abiertos cuando empecé; sus `.f3d` siguen en `caja/historico/`.
- **Para la sesión del Mac:**
  1. Revisa `caja/reporte-v5/probeta-iris.md` antes de que Pepe imprima, como pedías. Mira sobre todo el apartado 4 (supuestos) y las uñas de la bayoneta: vuelan 0,8 mm en rampa de 45° y pisan solo 0,5 mm de tapa.
  2. **No tengo los tres valores de la P0 a 0,2 mm.** Pepe solo me dijo «El p0 lo repetí y bien». Hay que preguntárselos a él.
  3. El aro gira solo 16° de abierto a cerrado. Para el planetario: el bisel tendrá que girar bastante más que el aro.
  4. `contexto.md`: de acuerdo, no lo toco.
- **Para Pepe:** decir si se imprime así, con 133,5 mm (pregunta 4 del apartado 6 de `ESTADO.md`). Después, imprimir las cinco bandejas y probarla con la tabla «vale si» del reporte.

## 2026-11-21 00:15 · sesión del Mac

- **Hecho:**
  - Leído el repositorio entero. **La unificación no perdió nada** (comprobado): los 7 ficheros de la web y los 621 fotogramas, `caja/BRIEF-v5.md`, `caja/resultados-probetas.md` y `sesiones/SESION-MAC.md` son idénticos a los de los repositorios antiguos. En el Mac no quedaba nada sin subir.
  - Con el permiso de Pepe (D-26), las tres tareas del relevo:
    1. **GitHub Pages sirve `/docs`.** Ojo: cambiar el ajuste no vuelve a publicar; hubo que pedirlo con `gh api -X POST repos/Pepe-a-d/eventually/pages/builds`. A los 40 segundos estaba.
    2. **Archivados** `eventually-caja` y `eventually-proyecto`.
    3. **El Mac trabaja ya en un clon de este repositorio**, en `~/Watchpage`. La carpeta de antes es `~/Watchpage-antiguo`.
  - **Web comprobada en su dirección de siempre** (medido con `curl` y en el navegador): la portada, `caja.js`, `img/enlace.jpg`, `frames/caja/manifest.json` y `sw.js` responden; con `?caja` sale solo el tutorial y con `?reloj`, el reloj. `…/eventually/docs/` da ahora 404, como debe.
  - **`pelicula.py` probado:** encuentra `docs/` y rehace los 240 fotogramas idénticos, byte a byte. Solo cambia el número de versión de `manifest.json`. Dejé la web como estaba.
- **Cambió:**
  - Borrado el `index.html` de la raíz: ya no se sirve.
  - `DECISIONES.md`: rellenados los motivos de D-01, D-14 y D-20 con lo que Pepe dijo en mis conversaciones, y cómo se llegó al iris. Nueva D-26. Quedan tres motivos que Pepe nunca dio.
  - `HISTORIA.md`: el nombre lo propuso la sesión del Mac y Pepe lo aceptó; la pestaña de arrancar fue idea de Pepe; apartado nuevo del 21 de noviembre.
  - `ESTADO.md`, `README.md` y `COMO-TRABAJAMOS.md` (apartado 11): puestos al día con lo anterior.
  - `caja/resultados-probetas.md`: nota sobre la P0 repetida a 0,2 mm.
- **A medias:** nada mío.
- **Para la sesión del PC:**
  1. Si Pepe te dio los tres valores de la P0 a 0,2 mm (alojamiento, holgura, piel), apúntalos en `caja/resultados-probetas.md`. Yo solo sé que «salió bien».
  2. Cuando subas la probeta del iris, deja el reporte en `caja/reporte-v5/`. La reviso antes de que Pepe la imprima, como con las versiones anteriores, salvo que Pepe diga otra cosa.
  3. El apartado 0 de `caja/BRIEF-v5.md` te pedía poner al día `contexto.md`: ya no hace falta, lo sustituyen `ESTADO.md` y `DECISIONES.md`.
- **Para Pepe:** nada que hacer. Siguen abiertas las tres preguntas del apartado 6 de `ESTADO.md`.

## 2026-11-21 00:00 · sesión del PC

- **Hecho:** fusionada la unificación en `main`, porque Pepe dijo «Fusiona». Desde ahora **este repositorio es el único**. Regla nueva de subida en `COMO-TRABAJAMOS.md`, apartado 6 (D-25): cada sesión sube su trabajo y Pepe confirma antes.
- **Cambió:** `LEEME.md` pasa a llamarse `README.md`, para que GitHub lo enseñe al abrir el repositorio. `DECISIONES.md` tiene arriba una lista de «Huecos por rellenar».
- **A medias:**
  - **GitHub Pages sigue sirviendo la raíz.** La sesión del PC no puede cambiar ese ajuste: su acceso a GitHub no llega a la configuración de Pages. Mientras tanto la web funciona por la redirección de la raíz, en `…/eventually/docs/`.
  - Archivar `eventually-caja` y `eventually-proyecto`.
  - La probeta del iris: sin modelar (D-23). Es lo siguiente de la sesión del PC.
- **Para la sesión del Mac**, la primera vez que leas esto:
  1. **Tu carpeta.** Comprueba con `git status` que no queda nada sin subir en `~/Watchpage`, `~/Watchpage/site` y `~/Watchpage/caja`. Si queda algo, no lo subas a los repositorios antiguos: cópialo al sitio que le toque aquí. Después renombra `~/Watchpage` a `~/Watchpage-antiguo` y clona este: `git clone https://github.com/Pepe-a-d/eventually.git ~/Watchpage`. Lo que era `site/` es ahora `docs/`.
  2. **GitHub Pages.** Con el permiso de Pepe, ponlo a servir `/docs`: `gh api -X PUT repos/Pepe-a-d/eventually/pages -f "source[branch]=main" -f "source[path]=/docs"`. Espera un par de minutos y comprueba que <https://pepe-a-d.github.io/eventually/> enseña la web sin pasar por `/docs/` en la dirección, con `?caja` y con `?reloj`. Cuando funcione, borra el `index.html` de la raíz y apúntalo aquí.
  3. **Repositorios antiguos.** Con el permiso de Pepe, archívalos: `gh repo archive Pepe-a-d/eventually-caja --yes` y `gh repo archive Pepe-a-d/eventually-proyecto --yes`. Quedan de solo lectura; no se borran.
  4. **`pelicula.py`.** Le cambié `SITE` para que apunte a `docs/`. No lo he ejecutado: pruébalo.
  5. **Lo que solo sabes tú.** Rellena los «Huecos por rellenar» de `DECISIONES.md` y corrige `HISTORIA.md`. Lo de tus conversaciones con Pepe lo saqué de `sesiones/SESION-MAC.md` y de `caja/BRIEF-v5.md`.
  6. **Tu resumen.** `sesiones/SESION-MAC.md` queda como historia. Lo nuevo va en `ESTADO.md`, `DECISIONES.md` y aquí.
- **Para Pepe:** dile a la sesión del Mac «lee el git de `Pepe-a-d/eventually`». Si prefieres cambiar tú el ajuste de la web: en GitHub, repositorio `eventually` → *Settings* → *Pages* → en *Branch*, elige `main` y la carpeta `/docs` → *Save*.

## 2026-11-20 23:55 · sesión del PC

- **Hecho:** junté los tres repositorios y lo que solo estaba en el PC en esta estructura, en la rama `unificacion` de `eventually`. Escribí `LEEME.md` (ahora `README.md`), `ESTADO.md`, `HISTORIA.md`, `DECISIONES.md`, `COMO-TRABAJAMOS.md` y este fichero. **No está fusionado ni publicado.**
- **Cambió:**
  - La web pasa de la raíz a `docs/`. En la raíz queda un `index.html` que solo redirige a `docs/`, como red de seguridad.
  - `web-fuentes/tools/pelicula.py`: `SITE` apunta a `docs/` (era `site/`). `.claude/launch.json`: sirve `docs`.
  - Nuevo: `web-fuentes/tutorial-caja/` con el guion de los fotogramas del tutorial y las mallas de la v4.1. Es lo que pedía el apartado 0 de `caja/BRIEF-v5.md`.
  - Nuevo: `caja/historico/video-v4.1/` con el vídeo de la v4.1 y sus fuentes.
  - `caja/BRIEF-v5.md` y `caja/resultados-probetas.md` están copiados sin tocar. Sus rutas son las de antes: `contexto.md`, `frase-v3.json` y lo demás de la v4 están ahora en `caja/historico/`.
- **A medias y pendiente:** lo recoge la entrada de arriba, que la sustituye.
- `caja/historico/contexto.md` no está puesto al día. Su papel lo hacen ahora `ESTADO.md` y `DECISIONES.md`.
