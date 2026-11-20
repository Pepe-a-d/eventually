# Cómo trabajamos

Reglas comunes de la sesión de Claude del Mac y de la del PC. El objetivo es que cualquiera de las dos pueda seguir el trabajo de la otra sin preguntar. Sustituye a `caja/historico/instrucciones-de-trabajo.md` y al apartado 6 de `sesiones/SESION-MAC.md`.

## 1. Un solo sitio

- Todo vive en este repositorio. **Lo que no está subido aquí, para la otra sesión no existe.**
- No se crean repositorios ni carpetas sueltas fuera de él. Si algo solo puede estar en una máquina (un documento de Fusion sin guardar, por ejemplo), se dice en [RELEVO.md](RELEVO.md).
- Los guiones y programas con los que se genera algo se suben junto a lo que generan.

## 2. Al empezar

1. `git pull`.
2. Leer [ESTADO.md](ESTADO.md) y la última entrada de [RELEVO.md](RELEVO.md).
3. Si Pepe pega texto de otra conversación, tratarlo como información a comprobar contra el repositorio, no como estado confirmado.

## 3. Al terminar

1. **[RELEVO.md](RELEVO.md), siempre:** una entrada con lo hecho, lo que cambió, lo que queda a medias y lo que se le pide a la otra sesión.
2. **[DECISIONES.md](DECISIONES.md),** si se decidió algo, con lo que llevó a decidirlo.
3. **[ESTADO.md](ESTADO.md),** si cambió lo que está activo, parado o descartado.
4. Subirlo, según el apartado 6.

## 4. Quién lleva qué

| Qué | Lo lleva | Dónde |
| --- | --- | --- |
| La web, la tarjeta y el QR | Sesión del Mac | `docs/`, `web-fuentes/`, `tarjeta/`, `qr/` |
| El diseño de la caja con Pepe y la revisión crítica de cada versión | Sesión del Mac | `caja/` |
| El modelo en Fusion, las probetas y sus ficheros para imprimir | Sesión del PC | `caja/` |
| Vídeos y fotogramas hechos a partir del modelo | Sesión del PC | `web-fuentes/tutorial-caja/` |

Cualquiera puede tocar lo de la otra. Cuando lo haga:

- Lo avisa en `RELEVO.md`, con el fichero y el motivo.
- No reescribe un documento firmado por la otra sesión (un brief, un contra-reporte, un reporte). Añade debajo una nota con fecha y firma, o escribe un documento nuevo que lo conteste.
- Lo que es de los dos (`ESTADO.md`, `DECISIONES.md`, `RELEVO.md`, este documento) se edita directamente.

## 5. Dónde va cada cosa nueva

| Qué | Dónde | Nombre |
| --- | --- | --- |
| Brief o encargo de la caja | `caja/` | `BRIEF-v5.md`, `encargo-…md` |
| Generador de Fusion | `caja/` | `generador_<pieza>_v5.py` |
| Piezas para imprimir, ya orientadas | `caja/probetas-v5/`, `caja/imprimir-v5/` | `<pieza>.3mf` |
| Reporte de una probeta o versión | `caja/reporte-v5/` | `<tema>.md` |
| Lo que dice una pieza impresa | `caja/resultados-probetas.md` | Un apartado con fecha |
| Revisión crítica | `caja/` | `contra-reporte-<qué>.md` |
| Cálculos | junto al documento que los usa | El programa, no solo la cifra |

Lo que deje de valer se mueve a `caja/historico/` y se apunta en `ESTADO.md`. No se borra.

## 6. Git

- **`git pull` antes de empezar y antes de subir.**
- Un commit por cosa hecha, con el mensaje en español: qué y por qué.
- Nunca `push --force` ni reescribir el historial.
- **Subir a `main` dentro de `docs/` publica en la web al momento.** Si Pepe no ha pedido publicar, el cambio va en una rama con pull request.
- Ningún fichero de más de 50 MB.
- **Regla vigente: no se hace commit ni push sin que Pepe lo pida.** Un encargo de Pepe que diga «súbelo» o «sube todo» lo cubre. Está preguntado si quiere relajarla (`ESTADO.md`, apartado 6).

## 7. Cifras y afirmaciones

- Cada cifra dice de dónde sale: **decidido**, **medido**, **del modelo**, **calculado**, **estimado** o **supuesto**.
- **Una fuerza calculada no se da por buena sin una pieza impresa.** La llave magnética cayó por eso.
- «Sin choques en el modelo» no es «funciona».
- Al pedir o describir una pieza, decir en qué dirección sujeta y con qué fuerza, no solo la forma.
- Distinguir siempre lo que una sesión ha hecho, lo que Pepe ha confirmado y lo que solo está propuesto.

## 8. Con Pepe

- En español y claro: se considera poco técnico. Rutas completas y pasos exactos.
- Pepe quiere que le digan lo que está mal, no que todo está bien.
- Al cerrar una tarea: qué se hizo, qué significa, qué cambió, qué sigue incierto y qué tiene que hacer él.
- Las decisiones cerradas no se reabren salvo que él lo pida. Lo descartado está en `ESTADO.md`.

## 9. Orden de trabajo de la caja

1. Primero la probeta del mecanismo; después la caja.
2. Antes de modelar un encargo, decir si algo no se puede cumplir o tiene una forma mejor.
3. Todo paramétrico: cada medida vive en la lista de parámetros del generador, con su comentario.
4. Ninguna caja entera sin medir antes el reloj.

## 10. La web

- Si cambia CSS o JS, subir el `?v=` de `docs/index.html`.
- Los puntos del scroll de la película del reloj están en `TIMELINE` de `web-fuentes/tools/pelicula.py` y en los `data-range` de `docs/index.html`. Van emparejados.
- Lo mismo para el tutorial: `timeline` de `docs/frames/caja/manifest.json` y los `data-caja-range`.
- `pelicula.py` rehace `docs/frames/d` y `docs/frames/m`. No toca `docs/frames/caja`.
- Servidor de prueba: `python3 -m http.server 4319 -d docs`.

## 11. Cada máquina

**Mac.** La carpeta es `~/Watchpage`, un clon de este repositorio. `web-fuentes/tools/imprimir.swift` solo funciona en Mac.

**PC.**

- Fusion está en el PC. La sesión del PC lo maneja a distancia.
- La sesión del PC **no puede ejecutar git en el PC**. Trabaja con un clon propio en la nube y copia al PC lo que Pepe necesita abrir o imprimir.
- Carpeta del PC: `C:\Users\pepea\Documents\FusionClaude\WatchBox`. Tiene lo de la caja hasta la v4.1 y no es un clon. Lo que mande es siempre el repositorio.
- Al copiar un fichero al PC puede llegar la versión anterior durante unos segundos: comprobar el tamaño antes de ejecutarlo.
- No se guarda el documento de Fusion en la nube de Autodesk sin que Pepe lo pida.
