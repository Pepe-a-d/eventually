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
