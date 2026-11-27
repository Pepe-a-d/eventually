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

## 2026-11-27 10:34 · sesión del PC

- **Hecho 1:** subida la carpeta de pruebas (`dbc1b04`), con el «sí» de Pepe.
- **Hecho 2: el tutorial de la web, rehecho con la caja v5. Va en la rama `tutorial-caja-v5`, con pull request: queda publicado cuando esté en `main`.** Pepe pidió cambiarlo en la web; la sesión del PC no pudo subir directamente a `main` (su entorno no la dejó publicar sin otra confirmación) y lo dejó en la rama, como se hizo con el primero. Palabras de Pepe: «crea un video para la web, como hicimos con el primero y luego cambia el video de la web por el nuevo que crees, sigue todo lo que te dije para el video de la web». Lo que le había dicho al primero (D-04, D-05 y tu `sesiones/SESION-MAC.md`): película movida por el scroll e integrada en la página, no un reproductor; sin jerga; y que no enseñe el reloj de verdad.
  - **Fotogramas:** 189, los mismos tramos y las mismas paradas que antes (0, 24, 54, 88, 118, 142, 188), así que `timeline` y los `data-caja-range` no cambian. Salen del modelo del 25-nov sin pasar por Fusion. Seis tramos: la funda; el aro gira y no pasa nada; se abren las puertas; sube el reloj; sale el soporte; y cerrar. El reloj sigue siendo un maniquí gris. Hay una flecha azul que dice hacia dónde se gira: es una ayuda del dibujo, no una pieza.
  - **Pesa** 4,3 MB en móvil y 7,0 MB en escritorio (antes 4,3 y 6,8).
- **Para la sesión del Mac: he tocado ficheros tuyos de `docs/`.** Qué y por qué:
  - `docs/index.html`: los siete textos del tutorial (los de antes hablaban de la aguja-llave y del frente que sale); el texto alternativo del póster; y **he quitado de «Por si acaso» las notas «Si pierdes la llave» e «Imanes»,** porque describen la llave de la v4.1, que ya no existe. No he puesto nada en su lugar: la v5 no tiene apertura de emergencia que contar, y sus imanes son de adorno. El más cercano al reloj es el de debajo del pie del soporte: a 43 mm de la cabeza del reloj y a 35 del brazalete (del modelo, con el reloj supuesto). Si eso merece un aviso, no lo sé: nadie lo ha medido con un reloj. Si quieres otra nota ahí, es tuya.
  - `docs/sw.js`: `CORE` pasa de `eventually-core-v2` a `v3`. El póster del tutorial está en la copia sin conexión y se sirve de la copia antes que de la red: sin cambiar el nombre, quien ya hubiera entrado seguiría viendo el póster viejo.
  - `docs/img/enlace.jpg`: la vista previa del enlace enseñaba la caja v4.1 cerrada. Ahora, la v5 con su funda. Tú misma apuntaste que había que rehacerla si la caja cambiaba a la vista.
  - `docs/frames/caja/` entero (fotogramas, `manifest.json`, `poster.webp`).
  - **No he tocado** `caja.js`, `caja.css`, `app.js`, `styles.css` ni los `?v=`: no cambian.
- **Los textos son una propuesta mía; Pepe no los ha dado por buenos.** Los que prometen algo sin probar con la caja en la mano: «sale con su soporte» tirando hacia arriba, «el soporte lo deja de pie» fuera de la caja, y que las puertas «se quedan de pie». He quitado el «sale con un tirón suave» de la funda.
- **Comprobado:** en Chrome sin ventana, a 390 × 844 y a 1440 × 900, con `?caja` y con `?reloj`: sin errores, la película carga (190 imágenes) y la del reloj sigue igual. Con «reducir movimiento» sale el póster nuevo (la caja abierta con el reloj arriba) y los textos en lista, bien. **Sin probar:** en un teléfono de verdad y sin conexión.
- **Cambió también:** `web-fuentes/tutorial-caja/` (guion nuevo: `mallas_v5.py`, `caja5.html`, `caja5.js`, `render5.mjs`, `a_webp.py`, `prueba5.mjs` y `LEEME.md`; el de la v4.1 pasa a `v4.1/`), `README.md`, `ESTADO.md`, `DECISIONES.md` (estado de D-04).
- **Ojo:** el tutorial enseña un modelo sin imprimir y con las medidas del reloj supuestas. Si la caja cambia a la vista, se repite con los cuatro pasos de `web-fuentes/tutorial-caja/LEEME.md` (unos diez minutos de máquina).
- **Quien ya tenga la web guardada** en el teléfono conserva los fotogramas viejos en su copia sin usarlos (unos 11 MB): la limpieza del `sw.js` solo borra por versión de la película del reloj. No estorba, pero ocupa.
- **Publicado a las 10:46.** Pepe contestó «Hazlo tú». La pull request nº 3 no se pudo fusionar por la API (403), así que `main` avanzó hasta el mismo commit (`237edc7`) y GitHub la dio por fusionada. Comprobado en la dirección pública: la página trae los textos nuevos y ya no las dos notas, y `frames/caja/manifest.json` es el nuevo (versión 1795771958).
- **Corregido a las 11:27, porque Pepe la vio publicada y dijo: «La caja sale muy arriba y muy pequeña».** Tenía razón: la caja ocupaba el 70 % del ancho del fotograma y solo el tercio de arriba, y en escritorio el lienzo entero cabía en el alto de la pantalla, así que quedaba pequeña y arriba a la derecha.
  - **Fotogramas rehechos** con la cámara más cerca y la caja más abajo: ahora va del 11 % al 87 % del ancho y del 18 % al 63 % del alto. Más no cabe: un móvil estrecho recorta hasta un 10 % por cada lado y debajo va el texto. Pesan 4,8 MB en móvil y 7,8 en escritorio.
  - **`docs/caja.css` (es tuyo, sesión del Mac):** en escritorio y en móvil tumbado, el lienzo de la caja mide ahora 1,4 veces el alto de la pantalla (o el ancho de la ventana, si es menor) y está colocado para que la caja quede centrada a la derecha del texto. Le he quitado el fundido de los lados, que con fotogramas transparentes no hace falta, y le he puesto uno arriba, por donde sale la funda. En `docs/index.html`, `caja.css?v=4`. En `docs/sw.js`, `CORE` pasa a `v4` (el póster vuelve a cambiar). La película del reloj no se toca.
  - Comprobado en Chrome sin ventana a 390 × 844, 390 × 664, 360 × 800, 844 × 390, 1024 × 768, 1440 × 900 y 1920 × 1080: sin errores. **Sigue sin probar en un teléfono de verdad.**
- **A las 11:40 quedó publicada la corrección del tamaño** (Pepe: «Si»; `8511de6`).
- **Dos cambios más, a las 13:19, pedidos por Pepe al verla publicada:**
  - «Las transiciones soy muy cortas y las esperas muy largas». Cambia solo el ritmo, no los fotogramas: `timeline` de `docs/frames/caja/manifest.json` (y `TIMELINE` en `a_webp.py`). Los gestos ocupaban el 54 % del recorrido y ahora el 79 %; la imagen espera un 3 % entre gesto y gesto. Con eso se mueven los siete `data-caja-range` y las cinco rayas del contador en `docs/index.html`. En `docs/caja.css` (tuyo, sesión del Mac) los textos de los gestos entran y salen en un octavo de su tramo, no en un cuarto, para que sigan enteros hasta que el gesto termina; `caja.css?v=5`.
  - «Cambia los textos de la animacion de la caja, ya que no es tan complicada como la primera pon textos mas simples». Ahora son: «Se abre girando. Sin llave ni botones.» · «Quita la funda. Tira hacia arriba.» · «Gira el aro. Hacia la derecha. Al principio no pasa nada.» · «Sigue girando. Las puertas se abren solas.» · «Hasta el tope. El reloj sube.» · «Cógelo. Sale con su soporte.» · «Lo mismo, al revés. Mete el soporte, gira hacia la izquierda y pon la funda.» Siguen siendo propuesta mía hasta que Pepe diga que valen.
  - `web-fuentes/tutorial-caja/graba5.mjs` (nuevo): graba la web recorriendo el tutorial a velocidad constante, para ver el ritmo.
- **Para Pepe:** mirar la web en el teléfono (`https://pepe-a-d.github.io/eventually/?caja`) y decir si valen los textos y la flecha azul.

---

## 2026-11-26 19:36 · sesión del PC

- **Hecho:** Pepe pidió (sus palabras): «Haz una carpeta para poder hacer las pruebas, que contenga los archivos de lo que tengo que imprimir en el orden en el que lo tengo que imprimir con una guia que explique como imprimirlos y como montarlos». Está en `caja/pruebas-v5/`:
  - Las diez bandejas de las tres probetas, **numeradas en el orden de imprimir** (`01-puertas-bandeja-A.3mf` … `10-planetario-bisel.3mf`). Son copias idénticas, byte a byte, de las de `caja/probetas-v5/`: el modelo no ha cambiado.
  - La guía: `GUIA.md` y, la misma, `00-GUIA-DE-PRUEBAS.pdf` (19 páginas, A4). Ajustes propuestos, un dibujo de cómo tiene que verse cada bandeja, el montaje paso a paso con dibujos y las tablas de «vale si» del apartado 9 del reporte, con una columna para apuntar.
  - El orden deja probar cosas pronto: con 01 y 02, la prueba de las puertas entera; con 03 y 04, los pestillos y el soporte sobre la plataforma; con 05, que el soporte queda sujeto abajo y suelto arriba; con 06, el ascensor; con 07 a 10, los engranajes encima de todo.
- **Comprobado en el modelo para escribir la guía** (no cambia ninguna pieza):
  - El tetón con pomo y el anillo entran desde arriba, con las puertas cerradas o abiertas, y el pomo recorre sus 13 mm sin tocar nada. Los pasadores entran por los dos lados.
  - El conjunto de las puertas, ya montado, baja en bloque sobre las columnas con el ascensor y el reloj debajo sin pisar nada.
  - Sin el cuerpo, el bisel se apoya en el plato (menos de 0,1 mm) y lo centran los satélites.
  - Qué se puede montar mal: las puertas valen para los dos lados; a los satélites les da igual la cara; la plataforma, el tubo, el plato, el marco y el aro solo entran en una posición; el pestillo, con la cara ancha arriba, no entra. **La meseta entra de dos maneras y la rueda central (o el anillo) tiene que seguirla:** con la meseta a media vuelta, el anillo «en su sitio» no asienta y hay que girarlo media vuelta. Lo he apuntado en el paso 5 del apartado 7 del reporte, que decía solo «es simétrica».
- **Cambió:** `caja/pruebas-v5/` (nueva), `caja/caja_guia_pruebas_v5.py` (nuevo: hace los dibujos de la guía y el HTML del que sale el PDF), `caja/caja_probetas_v5.py` (la lista de probetas pasa arriba del fichero y además escribe la copia numerada), `caja/reporte-v5/caja-entera.md` (apartados 7, 9 y 10; en el 9 ponía `juego_dientes` 0,2 y es 0,4), `caja/imprimir-v5/LEEME.md` (un enlace), `ESTADO.md`. Nada en `docs/`.
- **A medias:** nada.
- **Sin saber:** no he abierto los ficheros en Bambu Studio; los pasos de «cómo abrir un fichero» de la guía (el aviso de que no es de Bambu Lab, la pregunta de un objeto con varias partes) están escritos de memoria y sin probar con estos ficheros. Los ajustes son los propuestos en `imprimir-v5/LEEME.md`, con un cambio para simplificar: relleno al 100 % por bandeja entera (01, 04 y 08) en vez de pieza a pieza.
- **Para la otra sesión:** sigue pendiente tu revisión del modelo del 25-nov (D-34, D-35, D-36). Si revisas, mira también la guía: si un paso de montaje no te cuadra, es más barato corregirlo antes de que Pepe imprima. El apartado 13.2 del brief sigue describiendo el soporte de antes (es tuyo, no lo toco).
- **Para Pepe:** decidir si imprime ya (la guía recomienda empezar por 01 y 02 y parar si las puertas no convencen) y, antes de la bandeja 03, las cinco medidas del reloj. Siguen sin contestar: si le gustan el suelo hundido y el soporte nuevo, y si «y ya» quería decir quitar también los pestillos.

---

## 2026-11-25 13:25 · sesión del PC

Tres encargos de Pepe en la misma mañana. Va todo en una entrada.

- **Hecho 1: modelado el apartado 13 del brief (D-34),** porque Pepe dijo «empieza». Tu `revisar_caja_v5.py` da **ningún fallo.**
  - **Suelo:** he acortado el recorrido, como preferías: 81,1 mm, rampa de 13,9°, caja de 115,7 de alto. El pedestal llega a Z = −5,00. A ras del asiento quedan abiertos 283 mm² (tu medida).
  - **Soporte:** pie de 42 × 50 mm en un cajeado del pedestal, hasta dentro del disco (22,3 mm), con llave detrás. Dos pestillos en cola de milano sobre el disco, a derecha e izquierda. Cerrada, el soporte con el reloj se mueve 0,3 mm como mucho.
- **Hecho 2: soporte nuevo (D-35).** Pepe vio el dibujo y dijo: «El soporte del reloj es raro, haz un soporte normal en el que vaya abrochado y ya». Ahora es un cojín ovalado que llena el brazalete, en voladizo desde una placa a la derecha, con la punta libre. **He entendido que cambia lo de arriba y que el pie y los pestillos se quedan; Pepe no lo ha confirmado.** De paso sale un fallo que no vimos ninguno: el soporte de antes, cerrado por los dos lados, no dejaba poner un brazalete con cierre de pliegue.
- **Hecho 3: revisión entera (D-36).** Pepe pidió revisar todo «hasta 0 errores» y dejarlo para imprimir. He escrito `caja/caja_auditoria_v5.py` (monta la caja pieza a pieza por su camino, mira cada pieza capa a capa como se imprime y mide lo cerca que pasa lo que se mueve). **Encontró fallos de verdad, míos:**
  - Los pestillos **no se podían montar**: su canal acababa a 0,75 mm del borde del disco.
  - El pestillo tenía 0,05 mm a cada lado en el rebaje de la columna y sus esquinas quedaban a 0,09 de ella.
  - Los dientes engranaban con 0,08 mm entre flancos (tu riesgo). Ahora, de 0,16 a 0,19: `juego_dientes` de 0,2 a 0,4.
  - En el tubo, techo plano de 2,5 mm al aire al final de cada hélice. Relleno.
  - Pestañas del cuerpo en cuña (eran escalones); pasadores con una cara plana; 1,0 mm de techo sobre los cuernos del aro (eran 0,6); fuera la repisa de 0,9 mm de las columnas.
  - Mi comprobación de la puerta abierta medía un paso tarde: ya da 89,75° a 94,50°, como la tuya.
  - **Lo que sujetaba el soporte era un labio en filo** (0,2 a 0,5 mm de grueso, 0,9 mm de agarre). Ahora la nariz del pestillo es plana por arriba y a 45° por abajo, sobre un hombro macizo del pie: agarra 0,88 mm con el pestillo contra la columna. `caja_piezas_v5.py` traza ya el camino de sacar y de meter el soporte, cada 0,05 mm.
  - Los `.3mf` tenían triángulos de área cero y tres rebabas de una centésima (base, tubo, plataforma). Limpios: los 51 cuerpos de los 22 ficheros se vuelven a abrir y se comprueban al escribirlos.
  - La lista entera, en el apartado 0.3 del reporte. **La auditoría da ahora 0 fallos.** En Fusion, las 29 piezas salen iguales que en el programa y el recorrido entero (174 posiciones) no tiene ningún choque (reporte, 4.2).
- **Lo que he hecho distinto de tu propuesta del 13.2. Míralo con lupa:**
  - **Columnas a 0°, 180° y 262°** (antes 30°, 150° y 262°). Cambian base, plataforma y marco.
  - **Los pestillos solo sujetan con la plataforma abajo** (h ≤ 8,9 mm); de 12 mm para arriba el soporte está libre (`PESTILLO_LIBRE` = 69 en `caja_piezas_v5.py`). **No cumple «mientras la caja no esté abierta del todo».** Motivo: con los pestillos metidos, quien ponía el soporte lo dejaba apoyado encima, 3,1 mm alto y sin sujetar, y cerrada las puertas quedaban a 0,00 mm del reloj. Tu programa no lo nota porque prueba cerrada y abierta del todo. **Si no te vale, dilo, pero entonces hay que resolver esa trampa de otra manera.**
  - **Lo que queda de esa trampa:** si el soporte se queda atascado 1,6 mm alto o más en su cajeado, los pestillos lo levantan y se meten debajo: queda 2,8 mm alto, sin sujetar, y al reloj le quedan 0,3 mm hasta las puertas (hasta 1,4 mm alto, la cuña lo baja a su sitio; del modelo). Por eso el cajeado tiene 0,3 mm por lado y el pie, chaflán: tiene que bajar por su peso. Sin probar.
  - **Tope hacia dentro** en los pestillos, y **pie más ancho** que la peana (vuelco: fila 8 del apartado 1 del reporte).
- **Lo que no prueba ningún programa:** que los chaflanes aparten de verdad los pestillos; que el soporte baje por su peso; que el reloj entre en el cojín (el reloj de pega es rígido). Es roce y es el reloj de verdad: lo dirá la probeta.
- **Cambió:** en `caja/`: `caja_diseno_v5.py` (solo `juego_dientes`), `caja_piezas_v5.py`, `generador_caja_v5.py`, `caja_probetas_v5.py`, `caja_voladizos_v5.py`, `caja_figuras_v5.py`, `caja_render_v5.py`, `caja-v5.json`, `caja-v5-piezas.json`, `caja-v5-vistas.json`, `Eventually-caja-v5.f3d`; **nuevos:** `caja_auditoria_v5.py`, `imprimir-v5/` (doce bandejas y `LEEME.md`), `probetas-v5/caja-probeta-ascensor-soporte-y-pestillos.3mf`, `reporte-v5/caja-auditoria.txt`, `caja-reloj-arriba.png` y `caja-soporte.png`. Rehechos: los otros nueve `.3mf` de probeta, las comprobaciones, `caja-voladizos.txt` y todos los dibujos. `reporte-v5/caja-entera.md` (apartados 0, 0.2, 0.3, 1, 2.4, 3 a 7, 9 y 10). `ESTADO.md`, `DECISIONES.md` (D-34: cómo quedó; D-35 y D-36 nuevas). No he tocado nada tuyo.
- **A medias:** nada de los tres encargos. **El vídeo** `caja/video-v5/` sigue siendo del 21-nov. **`caja/BRIEF-v5.md` no lo he tocado:** su apartado 13.2 ya no describe lo que hay (pestillos libres desde 12 mm; soporte con cojín). Es tuyo: dime si lo cambias tú o lo cambio yo.
- **Para la sesión del Mac:** tu revisión a fondo, ahora sí. Corre también `python3 caja/caja_auditoria_v5.py` y dime si su parte A (montaje) y su parte B (voladizos) te convencen o se dejan algo: clasifico cada trozo al aire como isla, voladizo, puente o techo, y ahí puedo haberme equivocado a mi favor. Además: el puente de 6 mm bajo la pared del pedestal, la pared de 3,4 mm entre el cajeado y el costado del pedestal, y el soporte impreso tumbado (su pie entra con 0,3 mm). Sigue pendiente lo tuyo de los 2,03 mm bajo los dientes de la rueda central.
- **Para Pepe:** mirar `caja/reporte-v5/caja-reloj-arriba.png` y `caja/reporte-v5/caja-soporte.png`. Dar las medidas del reloj y del brazalete cerrado: sin ellas no hay versión final. Siguen sin contestar: qué probeta se imprime primero, la fecha de entrega y los textos del tutorial.

## 2026-11-24 21:55 · sesión del Mac

- **Hecho: decididas las dos cosas que quedaban (D-34),** porque Pepe dijo «lee git, y decide tu las dos preguntas, pero que el reloj este seguro y se vea todo bien y premium». **Las dos son que sí, y las dos te dan trabajo.** Están en el apartado 13 de `caja/BRIEF-v5.md`:
  - **Zanjas (E9):** el pedestal ya no sube hasta la tapa. Se queda a ras del asiento de las puertas (Z = −5). No hay que tocar las puertas ni su mecanismo. Lo he medido en tu modelo bajando la plataforma 5 mm: a ras del asiento quedan abiertos 243 mm² (rendija del pedestal y las dos ventanas de las manivelas) en vez de 1.062.
  - **Soporte (P5):** sujeto por la forma mientras la caja no esté abierta del todo, libre arriba. Propongo peana alta en un cajeado del pedestal y dos o tres pestillos sobre el disco, cada uno en línea con una columna: la cara de dentro de la columna lo mantiene metido y una muesca arriba lo deja salir. **Es una propuesta sin modelar:** si ves otra forma que cumpla la tabla del 13.2, úsala.
- **Tu corrección:** he repetido `revisar_caja_v5.py` en el Mac sobre tu modelo del 24-nov y me da lo mismo que a ti, 2 fallos. **No he repetido la revisión a fondo** (las cinco revisiones aparte, el montaje paso a paso de lo nuevo, tus ficheros de imprimir): la haré cuando estén estos dos cambios, que vuelven a tocar plataforma, pedestal, soporte y columnas. De lo que me pedías mirar:
  - **1,9 mm a los lados del pedestal:** con el pedestal a ras del asiento dejan de ser una rendija honda: su suelo también está en Z = −5.
  - **0,10 mm que entra la puerta empujada:** lo doy por bueno; el reloj queda a 3,15 mm.
  - **2,03 mm bajo los dientes de la rueda central: no lo he mirado todavía.** Va en la revisión a fondo.
- **Cambió:** `caja/BRIEF-v5.md` (apartado 13 nuevo; cambios con fecha en los apartados 2, 3, 4, 6 y 7), `caja/reporte-v5/calculos-mac/revisar_caja_v5.py`, `DECISIONES.md` (D-34), `ESTADO.md`. No he tocado nada tuyo.
- **`revisar_caja_v5.py` ha cambiado,** para pedir lo decidido:
  - La cara del pedestal, arriba, a 0,3 mm o menos del asiento (antes pedía que no hubiera zanja a ras de la tapa).
  - Cerrada, el soporte con el reloj no se mueve más de 1 mm hacia las puertas ni de lado. Lo prueba contra todas las piezas puestas en τ = 0, así que encuentra tus pestillos se llamen como se llamen.
  - Abierta del todo, el soporte sale tirando hacia arriba 40 mm sin pisar nada. **Para que esta pase, dibuja los pestillos, en τ = giro_tubo, donde quedan con la peana saliendo** (o dales su propio movimiento en `mover`).
- **A medias:** la revisión a fondo de tu corrección, dicho arriba.
- **Para la sesión del PC:** modelar el apartado 13. Eliges tú si acortas el pedestal o el recorrido (prefiero el recorrido, y la caja 5 mm más baja). Mete el soporte y los pestillos en la probeta del ascensor y propón su tabla «vale si». Si algo del 13.2 no sale, dilo antes de darle vueltas: hay alternativas descartadas con su motivo, y decidir otra cosa es de Pepe.
- **Para Pepe:** nada que decidir ahora. Cuando la sesión del PC lo tenga modelado, mirar el dibujo del reloj arriba: el suelo hundido lo he decidido sobre el modelo, y si al verlo no te gusta se vuelve atrás sin romper nada.

## 2026-11-24 19:43 · sesión del PC

- **Hecho: corregida la caja con tu revisión,** porque Pepe dijo «corrige todo. Cuando termines revisa tu trabajo» (D-33). **Tenías razón en todo lo que comprobé.** Tu `revisar_caja_v5.py` pasa de 15 fallos a 2: E9 y P5, que son de Pepe y no ha decidido.
  - **E1 y E4:** dos puertas distintas, como proponías: una con la cuña entera y otra con el hueco entero. Cuña de 1,4 mm, hueco de 1,5.
  - **E2:** media altura de la V = (radio + holgura) / cos(pendiente), a cada radio, y los flancos de la hélice con nueve puntos en vez de una recta. Tu prueba da 0,155 mm.
  - **E3:** bisagra 1 mm más afuera (`eje_fuera` 4), puerta abierta a 92° (`puerta_abierta`, nuevo), `bola_holgura` 0,12 y `aro_holgura` 0,2 (nuevo). Tu prueba: 89,75° a 94,5° con el aro en su sitio; 87,0° con el aro corrido, a 3,15 mm del reloj. No hay tope fijo: sigue siendo la bola en su pista.
  - **E5:** el ala es un cono a 45°. La escalera de 0,8 mm, puesta al derecho, seguía dando 296 mm² al aire con tu criterio.
  - **E6:** el anillo llega debajo de todo el cuerno, y `aro_r_ext` sale de `pista_pared_fuera` (0,85). Para que cupiera sin cambiar los dientes, el cuello baja de 3 a 2,4 mm de pared: **bajo los dientes de la rueda central quedan 2,03 mm.** Míralo.
  - **E7:** paredes de la pista 0,5 mm más bajas.
  - **E8:** llave del cuerpo (un taco de la base escondido en el grueso de la pared del frente) y llave de la funda (un taco 1,5 mm más largo en una esquina, con su cajeado en el cuerpo).
  - **Programa:** la fase 2 repite la fase 1; pide que central + bisel sea múltiplo de 12; columnas, asiento y ejes salen de parámetros; la junta de la fase 1 es la de verdad; `caja-v5.json`, regenerado. **No he probado otro reloj:** el margen sigue siendo corto (2,03 mm bajo los dientes).
  - **Reporte:** apartado 0.1 nuevo con todo esto; orden de montaje, cifras y «sin soportes», corregidos.
  - **Tu riesgo 4:** el cuerpo tiene una ranura detrás para sacarlo. Rampa de entrada en los pestillos, no.
  - **Mi revisión propia:** `caja/caja_voladizos_v5.py` (nuevo) mira capa a capa todas las piezas. No hay repisas al aire; sí los puentes que ya decías (meseta, 17 a 24 mm) y uno que no: el final de cada ranura del tubo acaba en un techo plano de 3 mm de fondo.
- **Cambió:** `caja/caja_diseno_v5.py`, `caja_piezas_v5.py`, `caja_figuras_v5.py`, `caja-v5.json`, `caja-v5-piezas.json`, `Eventually-caja-v5.f3d`; nuevos `caja/caja_probetas_v5.py` y `caja/caja_voladizos_v5.py`; los nueve `.3mf` de `caja/probetas-v5/` (ahora salen del programa, con mallas cerradas; el tetón con pomo va con el pomo en la cama y el tetón normal está en el fichero de los satélites); en `caja/reporte-v5/`: `caja-entera.md`, los siete dibujos, las tres comprobaciones y `caja-voladizos.txt`. `DECISIONES.md` (D-33), `ESTADO.md`. **No he tocado nada tuyo.**
- **A medias:** nada del encargo. **En Fusion está rehecho y comprobado entero** (27 piezas a la primera, 174 posiciones sin ninguna pisada; `caja/reporte-v5/caja-fusion-comprobaciones.txt`). El vídeo de `caja/video-v5/` es del modelo del 21-nov: no lo he rehecho.
- **Para la sesión del Mac:** repetir la revisión. Lo que más me preocupa: los 2,03 mm bajo los dientes, que la puerta abierta empujada entra 0,10 mm en el hueco libre (tu prueba lo da por bueno), y que a los lados del pedestal quedan ahora 1,9 mm hasta cada puerta en vez de 0,9.
- **Para Pepe:** decidir las zanjas (E9) y el soporte boca abajo (P5). Está explicado en las filas 6 y 7 del apartado 1 del reporte.

## 2026-11-22 01:00 · sesión del Mac

- **Hecho: la revisión de la caja v5 entera,** porque Pepe dijo «lee git y haz la revisión completa del modelo de la caja, que tenga 0 errores». Está en `caja/reporte-v5/contra-reporte-caja.md`. **No tiene cero: 9 errores en las piezas, 1 en el programa y 6 en el reporte.** Ninguno tumba la idea. Aconsejo a Pepe no imprimir nada hasta corregirlos; él no ha decidido.
  - Instalé en el Mac shapely, manifold3d, trimesh y scipy (Pepe dijo que sí) y **volví a construir tus 27 piezas con tu programa: me da lo mismo que a ti.** Tu reporte sale de verdad de tu modelo.
  - Lo que busqué es lo que tu programa no mira: piezas que no se pisan pero quedan sin holgura, las piezas con sus juegos, el montaje paso a paso, capas sin apoyo, y el texto contra el modelo.
  - **`caja/reporte-v5/calculos-mac/revisar_caja_v5.py` reúne las pruebas que deciden.** Importa tu `caja_piezas_v5.py`, tarda dos minutos y no escribe nada. Hoy da 15 líneas en FALLA. La meta es que no dé ninguna. Funciona en el PC con lo que ya tienes instalado.
- **Cambió:** nuevos `caja/reporte-v5/contra-reporte-caja.md`, `caja/reporte-v5/calculos-mac/revisar_caja_v5.py` y la carpeta `caja/reporte-v5/calculos-mac/revision-caja/` (programas y hallazgos de cada frente). `ESTADO.md`. **No he tocado ningún fichero tuyo.**
- **A medias:** nada. Cuando corrijas, repito la revisión.
- **Para la sesión del PC.** Cómo arreglar cada cosa lo decides tú. Lo que yo haría, por si ahorra tiempo:
  1. **E1, agujero en la junta (0,3 × 1,2 mm en el centro).** Con dos puertas iguales, las dos cuñas no pueden cubrir el centro: si llegan las dos, chocan. Lo sencillo es volver a lo de tu primera nota: **dos puertas distintas,** una con la cuña entera y otra con el hueco entero. Las dos se siguen imprimiendo con la cara vista en la cama.
  2. **E2, tetones sin juego en la rampa (0,02 mm).** La holgura está puesta en vertical y la ranura va a 15°: media altura de la V = (radio + holgura) / cos(pendiente), y mira además el trapecio de lados rectos, que se mete 0,16 mm a media pared. Comprueba con `min_gap` entre plataforma y tubo en la hélice: tu prueba de «bajarla 0,6 mm choca» no lo ve.
  3. **E3, puertas abiertas sin tope hacia dentro.** Dos caminos que se suman: centrar el aro de verdad (hoy solo lo centra su borde, con 0,3 mm), y que el reposo de «abierto» deje la puerta a 92° o 93°, para que todo su juego caiga hacia fuera del reloj. Un tope fijo sería lo mejor, pero ya viste que estorba al montar.
  4. **E4, las puertas se rozan al abrir (0,08 mm a 5°).** Más hueco en la cuña; con dos puertas distintas (punto 1) es más fácil.
  5. **E5, ala del bisel.** Las tres alturas de la escalera están al revés: el peldaño ancho llega hasta arriba y tapa a los otros dos.
  6. **E6, aro.** Que el anillo llegue por dentro hasta donde llega el cuerno, y que `aro_r_ext` cuente `pista_pared` (hoy es bola + 0,3).
  7. **E7:** que la varilla tenga más sitio que la bola contra el canto de la pista.
  8. **E8, cuerpo y funda.** El índice sale 0,6 mm y la funda tiene 0,5 de holgura: hace falta una llave que no se pueda saltar. En el cuerpo, que girado no asiente (hoy solo falla un clic).
  9. **Programa:** que la fase 2 repita las comprobaciones de la fase 1; que el reparto de satélites pida múltiplo de 12 y no de 6; que columnas, asiento y ejes salgan de parámetros; quitar de la fase 1 la junta en escalón, que ya no existe; regenerar `caja-v5.json`.
  10. **Reporte:** el orden de montaje (plato y satélites **antes** que la rueda central), el tetón con pomo boca abajo en su fichero, el tetón normal que falta en la probeta del planetario, y las cifras de la tabla del apartado 4 de mi revisión.
  11. Los riesgos del apartado 5 no te pido arreglarlos ahora, salvo el 4 si lo ves fácil: **el cuerpo no tiene rampa de entrada ni forma de quitarlo.**
- **Para Pepe:** decidir si se corrige antes de imprimir, y dos cosas suyas: las zanjas de delante y detrás del reloj abierto (E9) y si el soporte tiene que quedar sujeto boca abajo (P5).

## 2026-11-21 18:02 · sesión del PC

- **Hecho: la caja v5 entera, modelada y comprobada en el modelo. Nada impreso.** Reporte en `caja/reporte-v5/caja-entera.md`: lo que no cumple va lo primero (apartado 1).
  - 25 piezas más el reloj de pega. Medidas en `caja/caja_diseno_v5.py` (las del reloj, arriba); piezas y comprobaciones en `caja/caja_piezas_v5.py`; Fusion, con `caja/generador_caja_v5.py`.
  - **Las puertas no llevan la corredera que te conté a las 15:40.** Al dibujarla se metía en el hueco libre de 50 × 59. Ahora las mueve un **aro escondido que gira 11°** alrededor del hueco, con una pista por puerta; al aro lo mueve el plato con un tetón suelto que va a la vez en una espiral (plato), una ranura recta (marco) y una diagonal (brazo del aro). Una sola espiral, sin cruce.
  - Las dos puertas vuelven a ser la misma pieza, con la junta del centro en bisel a 45°.
  - **Mide 178,8 × 178,8 × 122,6** (183,8 × 126 con funda). Pepe aceptó 177 (D-31, apuntada por mí); los 178,8 no los ha visto.
  - De 2 en 2 grados de tubo, 174 posiciones: ninguna pieza pisa a otra y el reloj queda a 3,00 mm o más de todo. En Fusion: las 27 piezas tienen el mismo volumen que en el programa y el recorrido completo no da ninguna pisada; tras cambiar cinco piezas al final, en Fusion repetí solo las parejas en que entran (reporte, 4.2).
  - Tres probetas propuestas, con sus `.3mf` y sus tablas «vale si» (reporte, apartado 9).
- **Cambió:** nuevos en `caja/`: `caja_piezas_v5.py`, `caja-v5-piezas.json`, `generador_caja_v5.py`, `caja_render_v5.py`, `caja-v5-vistas.json`, `render-v5/`, `Eventually-caja-v5.f3d`; `caja_diseno_v5.py`, `caja-v5.json` y `caja_figuras_v5.py`, rehechos. En `caja/reporte-v5/`: `caja-entera.md`, siete dibujos `caja-*.png`, `caja-fase2-comprobaciones.txt`, `caja-fusion-comprobaciones.txt`; borrado `caja-esquema-corte.png` (era de la corredera). En `caja/probetas-v5/`: nueve `caja-probeta-*.3mf`. `antes-de-modelar-caja.md` lleva un aviso de que está superada. `DECISIONES.md`: D-31. `ESTADO.md`, al día.
- **Añadido a las 18:57, porque Pepe pidió «una animación explicando cómo funciona la caja por completo»:** `caja/video-v5/eventually-caja-v5-como-funciona.mp4` (72 s, sin sonido, con rótulos). Sale del mismo modelo: funda, apertura vista por fuera, engranajes en corte, el aro y la bola de las puertas, el ascensor en corte y el cierre. Termina diciendo que es el modelo y que nada está impreso. Cómo se rehace, en `caja/render-v5/LEEME.md`. **No es para la web:** el tutorial de la web sigue describiendo la v4.1.
- **A medias:** nada del encargo. No están hechos los `.3mf` de la caja entera (el brief dice que todavía no).
- **Para la sesión del Mac** (revisión crítica, paso 3 del brief):
  1. **Lo más flojo es el juego de las puertas:** 3° cerradas (1,5 mm en la punta, boca abajo) y entre 86° y 94° abiertas. Sale de una bola de 5 mm con 0,15 de holgura y un brazo de 8 mm. Tengo un remedio pensado y sin dibujar (apartado 6, punto 3). Mira si ves otro.
  2. **He cambiado cosas tuyas sin preguntar,** por ser de dentro: diez imanes en vez de nueve (cuatro en el tope), la junta en bisel en vez de media madera, el reparto de giros (puertas de 63° a 83° de tubo, subida desde 92°) y la rueda central de 78 dientes. Si alguna te parece de las que se ven o se tocan, díselo a Pepe.
  3. **Tres cosas que encontré tarde y están arregladas,** por si quieres comprobarlas: los pasadores se podían salir hacia atrás (ahora la rueda central les tapa las puntas); la puerta no se podía montar (ahora entra de pie); y con la caja cerrada la plataforma quedaba 1 mm caída sobre las entradas del tubo (ahora descansa en un asiento de la base).
  4. Entre las tres probetas sale casi toda la caja. D-15 dice que no se imprime la caja sin medir el reloj. Se lo planteo a Pepe; propongo empezar solo por la de puertas.
  5. La frase la he puesto en el techo de la funda, porque ahí se imprime gratis. Es de Pepe decidirlo.
- **A las 19:02 Pepe dijo:** «Sube todo a git, si me vale todo me gusta esa caja, lo siguiente va a ser revisarla desde la sesion del mac y luego imprimir». Apuntado como D-32. Subido todo. **Te toca la revisión.** No ha dicho qué probeta se imprime.
- **Para Pepe:**
  1. ~~Decir si los 178,8 mm le valen.~~ Dicho: le valen (D-32).
  2. Decidir qué probeta se imprime (propuesta: primero la de puertas, dos bandejas).
  3. Siguen sin contestar: fecha de entrega, si el reloj está montado y sus medidas, los textos del tutorial.
  4. En el Fusion del PC hay tres documentos «Sin título» sin guardar: el del iris, uno con una prueba y el de la caja. Los dos primeros se pueden cerrar sin guardar; el de la caja está exportado a `Eventually-caja-v5.f3d`.

## 2026-11-21 15:40 · sesión del PC

- **Hecho:** leído el brief nuevo y **empezada la caja entera**, porque Pepe dijo «lee git y empieza a modelar». **En Fusion no hay todavía ninguna pieza de la caja.** Está hecha la fase 1: medidas y movimiento, calculados grado a grado de tubo.
  - Lo que cambia respecto a tu brief y por qué, en `caja/reporte-v5/antes-de-modelar-caja.md`. Lo gordo: **la caja sale de 177 × 177 × 122 mm, no de 150.** Dentro de la rueda central tienen que caber las puertas con bisagras y manivelas (52 mm de radio): la rueda pasa de 60 a 78 dientes y el bisel a 102.
  - **Las puertas: una sola ranura en espiral y una sola corredera para las dos.** Quita el cruce de pistas que avisabas. La corredera va detrás de las puertas, se mueve 10,9 mm de delante atrás y lleva dos canales en diagonal; en cada uno entra una bola que cuelga de la puerta. Los tramos rectos del canal bloquean la puerta por la forma.
  - Las dos puertas son piezas distintas (una con labio, otra con rebaje), para que la raya sea recta.
  - Probado en Fusion que la hélice se puede modelar exacta (barrido con giro).
- **Cambió:** nuevos en `caja/`: `caja_diseno_v5.py` (parámetros, con el reloj arriba, y 20 comprobaciones), `caja-v5.json`, `caja_figuras_v5.py`; en `caja/reporte-v5/`: `antes-de-modelar-caja.md`, `caja-esquema-corte.png`, `caja-fase1-comprobaciones.txt`. `ESTADO.md`, al día.
- **A medias:** todo lo demás del encargo. Falta la forma de cada pieza, el generador de Fusion, las comprobaciones en el modelo y el reporte. Queda abierto en el Fusion del PC un documento nuevo sin guardar con la prueba de la hélice.
- **Para la sesión del Mac:**
  1. Si ves un fallo en la corredera única, o en el reparto de giros (puertas de 66° a 84° de tubo, subida desde 88°), dilo ahora, antes de que dibuje las piezas.
  2. El apartado 4 de mi nota lista lo que aún no tengo resuelto: cómo se sujeta el marco a las columnas, la placa de arriba, los pasadores y el cuerpo.
  3. Tus enlaces: de acuerdo, `probeta-iris.md` apunta ahora al brief del iris en `historico/`; lo corrijo cuando toque ese fichero.
- **Para Pepe:** nada bloquea. Si los 177 mm de lado le parecen demasiado, decirlo ya: con dientes algo más finos bajaría a unos 169.

## 2026-11-21 15:20 · sesión del Mac

- **Hecho:** **Pepe ha cambiado el orden de trabajo (D-30): primero la caja entera en Fusion, con todos los mecanismos comprobados en el modelo y su reporte; las probetas, después.** Sustituye a D-21. He reescrito el brief entero para la caja de puertas (D-29): **`caja/BRIEF-v5.md` es nuevo de arriba abajo.** El del iris está en `caja/historico/BRIEF-v5-iris.md`.
- **Cambió:** `caja/BRIEF-v5.md` (nuevo), `caja/historico/BRIEF-v5-iris.md` (movido, con aviso arriba), `DECISIONES.md` (D-30; D-21 sustituida), `ESTADO.md`. **Ojo:** la entrada de abajo, de las 15:15, hablaba de un «apartado 12» con el encargo de una probeta suelta de las puertas. Ya no es eso: el encargo es el apartado 11, la caja entera, y el 12 son las probetas de después.
- **A medias:** nada.
- **Para la sesión del PC:**
  1. **Tu encargo es el apartado 11 de `caja/BRIEF-v5.md`: la caja completa,** con un reloj de pega, comprobada de tope a tope, y el reporte en `caja/reporte-v5/caja-entera.md`.
  2. **Lo primero que hay que resolver es cómo se mueven las puertas.** En el apartado 4 va mi propuesta (dos ranuras en espiral bajo la pestaña del tubo, cada una en su franja de radio) y una trampa que he visto: el tubo gira 345° y los seguidores de las dos puertas están a 180°, así que dos pistas iguales al mismo radio se cruzan. No está dibujado: si no cabe o ves algo mejor, cámbialo y dilo.
  3. Mis medidas son cuentas a mano. Si el modelo dice otra cosa, manda el modelo. No hay ninguna fuerza calculada, a propósito.
  4. Lo que se ve y lo que se toca es de Pepe: si tienes que cambiarlo, pregúntale. Lo de dentro lo decides tú.
  5. Tu `probeta-iris.md` enlaza a `../BRIEF-v5.md`, apartado 11; ese apartado está ahora en `historico/BRIEF-v5-iris.md`. No he tocado tu documento.
  6. Cuando esté el reporte, lo reviso antes de que Pepe imprima nada.
- **Para Pepe:** decirle «lee git» a la sesión del PC. Y, cuando pueda, medir el reloj: todo el hueco sale de medidas supuestas.

## 2026-11-21 15:15 · sesión del Mac

- **Hecho:** **Pepe ha decidido (D-29): fuera el iris. Caja cuadrada, y la tapa son dos puertas con bisagra, una a la izquierda y otra a la derecha del reloj, que se abren solas mientras el reloj sube.** Se mantienen el bisel redondo, los engranajes a la vista, el satélite azul y el ascensor. No eligió ninguna de mis cuatro alternativas (entrada de abajo): la idea es suya, «algo como la 4 pero en una caja cuadrada».
- **Cambió:** `DECISIONES.md` (D-29 nueva; estado de D-20, D-22 y D-27), `caja/BRIEF-v5.md` (aviso arriba y **apartado 12 nuevo: el encargo de la probeta de las puertas**), `ESTADO.md`.
- **A medias:** los apartados 2 a 6 del brief siguen hablando de iris y de cilindro. Los rehago cuando la probeta de las puertas diga qué vale. El aviso de arriba del brief dice qué manda.
- **Para la sesión del PC:**
  1. **El encargo es el apartado 12 de `caja/BRIEF-v5.md`.** Solo el módulo de la tapa, con un aro y una orejeta, como hiciste con el iris. Cómo se mueven las puertas por dentro lo eliges tú; si ves mejor que las empuje la plataforma al subir, dilo antes de modelar.
  2. Lo que más importa a Pepe: **cerrada, plana y sin rendija; y que se vea sólida.** Puertas de 3 mm o más.
  3. Que ninguna pieza se pueda montar del revés.
  4. De tu probeta del iris se aprovecha todo lo que apuntaste: ejes a 0,25 mm, bayoneta de uñas a 45°, montaje sin pegamento.
- **Para Pepe:** decirle «lee git» a la sesión del PC.

## 2026-11-21 15:10 · sesión del Mac

- **Hecho:** leído el resultado del iris. Le pregunté a Pepe qué no le llega, como pedías: **cómo se ve cerrado** (láminas en escalera, agujero central, rendijas) **y que parece frágil.** El tacto y el acabado de impresión no. Le he presentado cuatro alternativas para la tapa, con dibujo. **No ha elegido todavía: nada de esto es una decisión.**
  1. **Iris de gajos al ras** (la que le recomiendo). Ocho piezas gruesas, de unos 3 mm, todas en un mismo plano. Cerradas forman un disco sin agujero, con ocho rayas finas en estrella. Para abrir, cada gajo desliza de lado en línea recta (perpendicular a su eje) unos 40,6 mm. El hueco abierto es un octógono en el que cabe el círculo de 75. Carcasa de unos 136 a 139 mm con 8 gajos y de unos 131 a 133 con 10 (**calculado en plano**, `caja/reporte-v5/calculos-mac/gajos_al_ras.py`; sin dibujar en CAD y sin pieza). Riesgo: piezas que deslizan en guías se pueden atravesar, cosa que con ejes no pasa. Sería la segunda ronda de probeta del iris.
  2. **Dos compuertas** (D-22). Dos medios discos gruesos, una sola raya. **Carcasa de unos 160 mm** (calculado en plano): unos 26 mm más que el iris de ahora. En D-20 recomendé esta ruta «por tamaño»; hecha la cuenta en una caja redonda, es la más ancha.
  3. **Tapa entera que sube con el reloj.** Un disco de una pieza sobre dos columnas del pedestal: cerrada tapa el hueco y al subir queda como un techo sobre el reloj. Sin mecanismo de tapa. Se pierde «se abre como una cámara» y las columnas pueden volver a parecer frágiles.
  4. **Pétalos que se levantan.** Ocho triángulos gruesos con bisagra en el borde del hueco. Cerrados, disco plano sin agujero; abiertos, de pie alrededor del reloj. Ocho bisagras impresas y hay que levantarlos con una leva: la de más riesgo.
  - Seguir con el iris de láminas (más láminas, más gruesas) no lo recomiendo: la escalera y el agujero van con ese tipo de iris.
  - **Mi previsión de que las de 1,2 y 0,8 no cerrarían estaba mal.** Nota añadida arriba de `caja/reporte-v5/contra-reporte-iris.md`.
- **Cambió:** `caja/resultados-probetas.md` (nota fechada con la respuesta de Pepe), `caja/reporte-v5/contra-reporte-iris.md` (nota de que la pieza lo desmiente), `caja/reporte-v5/calculos-mac/gajos_al_ras.py` (nuevo), `ESTADO.md`.
- **A medias:** la elección de Pepe. Cuando elija, apunto la decisión en `DECISIONES.md` y escribo el encargo.
- **Para la sesión del PC:** nada que modelar todavía. Si ves un fallo en la cuenta de los gajos, o una forma mejor de moverlos (por ejemplo, hojas al ras que giran sobre un eje, para aprovechar los ejes que ya sabemos que van bien), dilo antes de que Pepe decida.
- **Para Pepe:** elegir entre las cuatro, o pedir otra cosa.

## 2026-11-21 14:55 · sesión del PC

- **Hecho:** **Pepe ha impreso, montado y probado el iris.** Apuntado en `caja/resultados-probetas.md` con sus palabras. Sin cifras ni foto.
  - **Funciona con los tres gruesos: 1,2, 0,8 y 0,4 mm.** Las de 0,8 dejan el agujero algo más pequeño que las de 1,2.
  - Primero dijo que las de 0,4 se paraban a mitad de recorrido. **Era el aro puesto del revés**, lo corrigió él diez minutos después. Yo ya le había dado una explicación (la raíz de la lámina cedía): estaba mal.
  - **Lo importante: «creo que el iris no va a quedar con el estándar de calidad que busco, voy a valorar opciones con la sesión del Mac».** No me ha dicho qué es lo que no le llega.
  - Las cuentas de fuerzas de las dos sesiones (que las de 1,2 y 0,8 no cerrarían) quedan desmentidas por la pieza.
- **Cambió:** `caja/resultados-probetas.md` (apartado nuevo, arriba), `ESTADO.md`. Nuevos: `caja/reporte-v5/iris-montaje.png`, el dibujo de montaje que le pasé a Pepe, y `caja/iris_montaje_v5.py`, que lo hace.
- **A medias:** nada. No toco el iris hasta que Pepe decida.
- **Para la sesión del Mac:**
  1. **Pepe va a hablar contigo del iris.** Pregúntale primero qué es lo que no alcanza: aspecto, tacto, luz que pasa, agujero o tamaño. Sin eso no se sabe si se arregla o se cambia.
  2. Lo que la pieza sí deja probado, valga o no el iris: ejes y tetones a 0,25 mm de holgura giran; una bayoneta de cuatro uñas en rampa de 45° sale sin soportes y cierra; una carcasa de 133,5 mm con 9,8 de grueso monta sin pegamento.
  3. **Defecto conocido:** el aro se puede montar del revés y entonces se bloquea a mitad de recorrido. Si el iris sigue, hay que impedirlo.
  4. Si el iris cae, el plan B apuntado es D-22 (dos compuertas). Las medidas del brief que partían de 130 mm, mejor no rehacerlas todavía.
- **Para Pepe:** hablar con la sesión del Mac. Aquí no tiene nada pendiente.

## 2026-11-21 08:15 · sesión del PC

- **Hecho:** el encargo de D-28, porque Pepe dijo «lee git»: **juego de 8 láminas de 0,4 mm** para la probeta del iris. Misma silueta, cola engordada a 1,2 y tetón alargado (2,8 mm desde la hoja). **La carcasa no se ha tocado:** he comprobado que la base, el aro, la tapa y las láminas de 1,2 y 0,8 salen idénticas del programa, y no he vuelto a exportar sus `.3mf`.
  - **Añadido que no pedías:** el tetón nace de un refuerzo redondo de 6 mm de diámetro y 1,2 de grueso. Un tetón de 3 mm sobre una hoja de dos capas se arrancaría. Ninguna lámina pasa por encima de esa zona (la más cercana, a 21,8 mm) y está comprobado que no toca el aro.
  - **Lo que pedías mirar.** Rebaje del canto: con dos capas queda de una sola capa, 0,2 mm hacia dentro. Apilado con 0,4: rígidas no se pisan hasta los 27° de giro y se pisan 0,33 mm cerradas. Tetón: entra en el aro entre 1,1 y 2,0 mm, igual que los otros dos juegos, y no toca la tapa. En Fusion: 28 comprobaciones, cero fallos.
  - **Tu cuenta de la torsión: no le veo fallo, y la mía estaba mal.** Los 11 gramos salían de doblar la lámina entera como una regla de 64 mm. Lo que cede es la punta. La he repetido por otro camino (los últimos 15 mm de la punta como voladizo de 5 mm de ancho, cediendo 0,55 mm cada una): unos 100 gramos por contacto con 1,2 mm, del orden de tus 250. Y como va con el grueso a la cuarta, con 0,4 son unas 80 veces menos. Corregido en mi reporte, apartado 4, y en el programa.
- **Cambió:** `caja/probetas-v5/iris-laminas-0.4mm-x8.3mf` e `iris-lamina-0.4mm-suelta.3mf` (nuevos), `comprobaciones-fusion.txt`; `caja/iris_diseno_v5.py` (parámetros `lamina_grosor_c` y `refuerzo_r`), `iris-v5.json`, `generador_iris_v5.py`; `caja/reporte-v5/probeta-iris.md` y `comprobaciones-plano.txt`; `caja/Eventually-iris-v5.f3d`; `ESTADO.md` y el estado de D-28. Tu `apilado_iris.py` sigue funcionando con el `iris-v5.json` nuevo.
- **A medias:** nada. El juego de 0,6 mm no lo he hecho: Pepe no lo ha pedido.
- **Para la sesión del Mac:**
  1. De acuerdo con lo de la versión siguiente (ranura inclinada para 45-60° de aro, lámina escalonada, retén de la tapa). No toco nada hasta que haya pieza.
  2. Gracias por la P0 a 0,2: con 0,20 pasa sin forzar, así que dejo los ejes a 0,25.
- **Para Pepe:** imprimir las seis bandejas de `C:\Users\pepea\Documents\FusionClaude\WatchBox\probetas-v5\` y probar sin forzar, con la tabla «vale si» del reporte.

## 2026-11-21 08:05 · sesión del Mac

- **Hecho:** Pepe ha decidido añadir a la probeta del iris un **tercer juego de láminas, de 0,4 mm** («Sí, añádelo»). Apuntado como **D-28**.
  - **P0 a 0,2 mm:** Pepe mandó una foto de la tira marcada. Leo alojamiento de imán de 5,20 mm, sujeta con 0,15 y pasa sin forzar con 0,20: todo 0,05 mm más justo que a 0,08. Pepe confirmó la lectura. Falta la piel: esa fila no tiene marca. Con eso, los 0,25 mm de holgura de los ejes del iris deberían girar sueltos.
- **Cambió:** `caja/resultados-probetas.md` (apartado nuevo de la P0 a 0,2), `DECISIONES.md` (D-28), `ESTADO.md`, una nota en la fila de láminas del apartado 11 de `caja/BRIEF-v5.md` y otra en `caja/reporte-v5/contra-reporte-iris.md`.
- **A medias:** nada por mi parte.
- **Para la sesión del PC:** el encargo, que sale de D-28:
  1. Un juego de 8 láminas de **0,4 mm** (dos capas), con la misma silueta, la cola engordada a 1,2 mm y el tetón alargado para que llegue al aro, como ya haces con el juego de 0,8. **La carcasa no se toca.**
  2. Ficheros: `caja/probetas-v5/iris-laminas-0.4mm-x8.3mf` y una suelta, con los mismos nombres que las otras.
  3. Mira si con solo dos capas el rebaje del canto y la unión del tetón siguen saliendo bien, y pasa tus comprobaciones de apilado y de tetón con ese grueso. Apunta el resultado en tu reporte.
  4. Un juego de 0,6 mm lo mencioné como posible. **Pepe no lo ha pedido:** no lo hagas sin preguntarle.
- **Para Pepe:** puedes ir imprimiendo las cinco bandejas que ya hay; la carcasa es la misma. Las láminas de 0,4 llegarán en una bandeja aparte.

## 2026-11-21 01:30 · sesión del Mac

- **Hecho:** revisada la **probeta del iris** antes de imprimir, porque Pepe dijo «lee git». Medidos los `.3mf` por mi cuenta y repetido el apilado de las láminas por otro camino.
  - **Las medidas del reporte cuadran** (diámetro, gruesos, volúmenes, giro, pisado de las láminas). Se imprime sin soportes.
  - **Lo que no cuadra:** que el pisado se absorba «doblándose con 11 gramos». Ocho láminas en rueda son una escalera de caracol: cada una tiene que bajar un grueso dentro de su ancho, y cerca del centro eso son 31° de inclinación de lado para la de 1,2 y 22° para la de 0,8. Tiene que ponerlo la torsión de una punta de 2 a 4 mm de ancho. **Calculo que se pondrá duro con el agujero a 30-40 mm (láminas de 1,2) y a 15-20 mm (0,8). Estimado: lo dirá la pieza.**
  - **Parte de la culpa es de mi brief:** pedía láminas de 1,2 mm o más y agujero cerrado de 8 mm o menos, y con láminas planas no caben las dos cosas.
- **Cambió:** nuevo `caja/reporte-v5/contra-reporte-iris.md` y `caja/reporte-v5/calculos-mac/apilado_iris.py` (solo numpy). `ESTADO.md`, al día. No he tocado el reporte del PC ni el modelo.
- **A medias:** las medidas de `caja/BRIEF-v5.md` que partían de 130 mm. No las rehago todavía: el iris puede cambiar otra vez según salga la probeta.
- **Para la sesión del PC:**
  1. **Si Pepe dice que sí** (pregunta 4 de `ESTADO.md`): un tercer juego de láminas de 0,4 mm, y si no cuesta otro de 0,6. Misma silueta y misma carcasa; la cola engordada a 1,2 como en el juego de 0,8. Sin su «sí», no.
  2. Para la versión siguiente del iris, a decidir cuando haya pieza: ranura inclinada o curva para que el aro gire 45 a 60° en vez de 15° (ahora el dedo llega a la lámina con menos de la mitad de fuerza), lámina escalonada (fina en la punta, gruesa en la raíz) y un retén en la tapa (al abrir el iris, el aro gira en el sentido que suelta la bayoneta).
  3. Las uñas: bien para imprimir. Con 0,3 mm de juego de lado, si la tapa se va a un lado en el contrario pisan 0,2 mm. Vale para la probeta.
  4. Si ves un fallo en mi cuenta de la torsión, dilo: es una estimación y no la ha confirmado ninguna pieza.
- **Para Pepe:** imprimir las cinco bandejas tal como están y probar **sin forzar**: cerrar hasta que se ponga duro y apuntar cuánto mide el agujero con cada juego. Antes de empezar, una raya de lápiz que cruce de la tapa a la pared, para ver si la tapa se mueve. Y decidir si se añade el juego de 0,4 mm.

## 2026-11-21 01:05 · sesión del PC

- **Hecho:** modelada la **probeta del iris** (encargo del apartado 11 de `caja/BRIEF-v5.md`), porque Pepe dijo «Empieza el modelado». Comprobada en plano grado a grado y medida en Fusion. **Sin imprimir.**
  - Cumple todo el encargo en el modelo **menos el diámetro: 133,5 mm, no 130.** Mi cálculo de D-23 (125 a 127) estaba mal. Explicado en D-27 y en el reporte, apartado 2.
  - Lo que más puede fallar: al cerrar, las láminas tienen que doblarse 1,1 mm en la punta (calculado). Por eso van los dos juegos, de 1,2 y de 0,8.
- **Cambió:** todo nuevo, dentro de `caja/`:
  - `reporte-v5/probeta-iris.md`: **el reporte. Empezar por aquí.** Con sus figuras y `comprobaciones-plano.txt`.
  - `probetas-v5/`: siete `.3mf` ya orientados y `comprobaciones-fusion.txt`.
  - `iris_diseno_v5.py` (las medidas, en `P_DEF`, y las comprobaciones; no necesita Fusion, sí numpy, scipy y shapely), `iris-v5.json` (lo que escribe), `generador_iris_v5.py` (se ejecuta en Fusion y lee ese fichero), `iris_figuras_v5.py`.
  - `Eventually-iris-v5.f3d`: el modelo montado. Hay también un `.step` de 18 MB, solo en el PC (`C:\Users\pepea\Documents\FusionClaude\WatchBox\Eventually-iris-v5.step`).
  - `ESTADO.md`, `DECISIONES.md` (D-27; nota en D-23) e `HISTORIA.md`, al día.
  - **01:15. Pepe decide D-27:** «el 133,5 está bien si luego adaptamos el resto». Y da el «sí» para subir todo esto.
- **A medias:** nada. En el Fusion del PC queda abierto un documento sin guardar, «Sin título», con el iris montado. No está en la nube de Autodesk. Los documentos de la v2, v3 y v4.1 ya no estaban abiertos cuando empecé; sus `.f3d` siguen en `caja/historico/`.
- **Para la sesión del Mac:**
  1. Revisa `caja/reporte-v5/probeta-iris.md` antes de que Pepe imprima, como pedías. Mira sobre todo el apartado 4 (supuestos) y las uñas de la bayoneta: vuelan 0,8 mm en rampa de 45° y pisan solo 0,5 mm de tapa.
  2. **No tengo los tres valores de la P0 a 0,2 mm.** Pepe solo me dijo «El p0 lo repetí y bien». Hay que preguntárselos a él.
  3. El aro gira solo 16° de abierto a cerrado. Para el planetario: el bisel tendrá que girar bastante más que el aro.
  4. `contexto.md`: de acuerdo, no lo toco.
  5. El iris queda en 133,5 mm por decisión de Pepe. Las medidas de `caja/BRIEF-v5.md` que partan de 130 (bisel, tubo, planetario) hay que rehacerlas con 133,5.
- **Para Pepe:** imprimir las cinco bandejas y probarla con la tabla «vale si» del reporte, cuando la sesión del Mac lo haya revisado.

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
