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

## 2026-11-20 23:55 · sesión del PC

- **Hecho:** junté los tres repositorios y lo que solo estaba en el PC en esta estructura, en la rama `unificacion` de `eventually`. Escribí `LEEME.md`, `ESTADO.md`, `HISTORIA.md`, `DECISIONES.md`, `COMO-TRABAJAMOS.md` y este fichero. **No está fusionado ni publicado.**
- **Cambió:**
  - La web pasa de la raíz a `docs/`. En la raíz queda un `index.html` que solo redirige a `docs/`, como red de seguridad.
  - `web-fuentes/tools/pelicula.py`: `SITE` apunta a `docs/` (era `site/`). `.claude/launch.json`: sirve `docs`.
  - Nuevo: `web-fuentes/tutorial-caja/` con el guion de los fotogramas del tutorial y las mallas de la v4.1. Es lo que pedía el apartado 0 de `caja/BRIEF-v5.md`.
  - Nuevo: `caja/historico/video-v4.1/` con el vídeo de la v4.1 y sus fuentes.
  - `caja/BRIEF-v5.md` y `caja/resultados-probetas.md` están copiados sin tocar. Sus rutas son las de antes: `contexto.md`, `frase-v3.json` y lo demás de la v4 están ahora en `caja/historico/`.
- **A medias:**
  - Fusionar esta rama en `main` y, en el mismo momento, poner GitHub Pages a servir `/docs`. Hasta entonces mandan los tres repositorios antiguos.
  - Archivar `eventually-caja` y `eventually-proyecto` cuando esto esté fusionado.
  - La probeta del iris: sin modelar. Forma acordada con Pepe en D-23.
  - `caja/historico/contexto.md` no está puesto al día. Su papel lo hacen ahora `ESTADO.md` y `DECISIONES.md`.
- **Para la sesión del Mac:**
  1. No subas nada más a `eventually-caja` ni a `eventually-proyecto` desde que esto se fusione. Si subes algo antes, dilo aquí para traerlo.
  2. Revisa `HISTORIA.md` y `DECISIONES.md`: lo que pasó en tus conversaciones con Pepe lo he sacado de tus documentos. Corrige lo que esté mal y rellena los «No consta» que sepas.
  3. Cuando esté fusionado, cambia tu carpeta: comprueba con `git status` que no queda nada sin subir en `~/Watchpage`, `~/Watchpage/site` y `~/Watchpage/caja`; renombra `~/Watchpage` a `~/Watchpage-antiguo`; y clona: `git clone https://github.com/Pepe-a-d/eventually.git ~/Watchpage`.
  4. `pelicula.py` no lo he ejecutado con la ruta nueva. Compruébalo antes de fiarte.
- **Para Pepe:** decidir si se fusiona, y contestar las preguntas de `ESTADO.md`, apartado 6.
