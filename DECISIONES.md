# Registro de decisiones

Aquí se apunta **cada decisión con lo que llevó a tomarla**. Sirve para que una sesión entienda el trabajo de la otra sin tener que adivinar, y para no volver a proponer lo que ya se descartó.

## Cómo se apunta una decisión

Las dos sesiones, la del Mac y la del PC, siguen estas reglas.

1. **Se apunta en el momento**, en la misma tanda de trabajo en que se toma. No se deja para después.
2. **Una entrada por decisión**, con el número siguiente (`D-25`, `D-26`…). Los números no se reutilizan.
3. **El «qué llevó a ella» es obligatorio.** Tiene que decir el hecho concreto: una pieza que falló, una frase de Pepe, un cálculo, un contra-reporte. «Era mejor» no vale.
4. **Si no se sabe el motivo, se escribe «No consta»** y se le pregunta a Pepe. No se inventa.
5. **Se dice de dónde sale cada dato:** decidido, medido, del modelo, calculado, estimado o supuesto. Una fuerza calculada no es un hecho hasta que una pieza impresa la confirme.
6. **Se apunta lo que se descartó y por qué**, para que nadie lo vuelva a proponer.
7. **Una decisión no se borra ni se reescribe.** Si cambia, se le pone «Sustituida por D-nn» y se escribe la nueva.
8. **Solo decide Pepe.** Una sesión puede proponer: se apunta como «Propuesta» y pasa a «Activa» cuando Pepe dice que sí.
9. Si la decisión cambia lo que está activo o parado, se pone al día también [ESTADO.md](ESTADO.md).

### Plantilla

```
### D-nn. Título corto
- **Fecha:** día y, si se sabe, hora.
- **Quién decide:** Pepe / propuesta de la sesión del Mac / propuesta de la sesión del PC.
- **Decisión:** qué se hace, en una o dos frases.
- **Qué llevó a ella:** el hecho, con su procedencia y dónde está el detalle.
- **Qué se descartó:** las alternativas y por qué no.
- **Estado:** Activa / Propuesta / Parada / Sustituida por D-nn.
```

## Huecos por rellenar

Motivos que no están escritos en ningún documento. Quien lo sepa, lo escribe en su entrada y lo borra de esta lista. Si no lo sabe ninguna sesión, se le pregunta a Pepe.

Rellenados por la sesión del Mac el 21-nov-2026 a partir de sus conversaciones con Pepe: D-01, D-14 y D-20. Lo que sigue sin saberse, porque Pepe no lo dijo:

- **D-14:** por qué no le gustó «pronto / tarde» en la tapa.
- **D-20:** por qué sin trinquete, por qué el iris liso y por qué el bisel y no la base. Pepe lo eligió sin dar motivo.

## Decisiones hasta el 20 de noviembre de 2026

Reunidas por la sesión del PC a partir de los documentos de las dos sesiones. Donde el motivo no estaba escrito en ningún sitio, pone «No consta».

### El reloj y la web

### D-01. El nombre
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** el reloj se llama Eventually, con la línea «Late Edition · 1 of 1».
- **Qué llevó a ella:** al encargar la web (19-nov, 13:06), Pepe pidió «decidir un nombre o algo para ponerle». La sesión del Mac propuso «Eventually · Late Edition · 1 of 1», con el lema «Llegará. Cuando llegue.», y Pepe lo aceptó sin cambios («Sí, empiezo»). No dijo por qué le gustó. Interpretación de la sesión del Mac: el nombre sale de la frase que el reloj lleva en la esfera, «Who cares, I'm already late», un reloj que llega tarde y no le importa; «1 of 1» porque es una pieza única montada a mano. *(Rellenado por la sesión del Mac, 21-nov-2026.)*
- **Estado:** Activa.

### D-02. Blanco papel y una sola cosa azul
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** todo es blanco y lo único de color es azul (`#1F3FA8`). La frase va con la letra de la esfera, Reenie Beanie.
- **Qué llevó a ella:** es la estética del propio reloj: esfera blanca, números y segundero azules. A Pepe le gusta mucho esa letra (dicho por él, recogido en `sesiones/SESION-MAC.md`).
- **Estado:** Activa. En la v5 lo azul de la caja es un engranaje (D-20).

### D-03. La web: una película que avanza con el scroll
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe, con la sesión del Mac.
- **Decisión:** el reloj se monta pieza a pieza al deslizar. HTML, CSS y JS sin dependencias. Los fotogramas salen de cinco imágenes con `web-fuentes/tools/pelicula.py`.
- **Qué llevó a ella:** se abre desde un QR o una etiqueta NFC, así que se pensó primero para el móvil en vertical. Con las cinco imágenes bastó: no hicieron falta vídeos.
- **Estado:** Activa.

### D-04. El tutorial de la caja va dentro de la web
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** las instrucciones de la caja son una segunda película movida por el scroll, con textos de la propia página.
- **Qué llevó a ella:** Pepe vio el vídeo de la v4.1 y pidió lo mismo para la web, «integrado en la app y no un simple reproductor». Además estaban pendientes la pista de apertura y el aviso del imán.
- **Qué se descartó:** incrustar el vídeo.
- **Estado:** Activa, pero las imágenes y los textos describen la v4.1. Hay que rehacerlos con la v5.

### D-05. La primera visita no enseña el reloj
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** la primera vez que se abre la web en un teléfono solo salen las instrucciones de la caja. El reloj aparece al pulsar «Ya lo tengo» o pasados 15 minutos.
- **Qué llevó a ella:** quien llega con la caja cerrada no debe ver el reloj antes de abrirla. Los 15 minutos son porque el iPhone recarga las pestañas por su cuenta y lo habría destripado a media apertura.
- **Estado:** Activa.

### La caja, de la v0 a la v4.1

### D-10. La aguja azul es la llave
- **Fecha:** 19-nov-2026, brief original.
- **Quién decide:** Pepe, con la sesión del Mac.
- **Decisión:** la caja se abre con una aguja azul que lleva un imán y arrastra un rotor escondido tras el panel.
- **Qué llevó a ella:** la caja debía abrirse en el mismo orden en que el reloj se monta en la web: papel, aguja, reloj. El riesgo de que el imán no arrastrara el rotor quedó apuntado como R1.
- **Estado:** Sustituida por D-19.

### D-11. De la v1 a la v2: la caja se abre por delante
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** caja-expositor que se abre por el frente, llave más fina y la frase con la letra del reloj.
- **Qué llevó a ella:** Pepe vio la v1, que se abría por arriba, y dijo que era muy incómodo acceder al reloj y usarla como expositor.
- **Estado:** Sustituida por D-20. La idea de que la caja sirva de expositor sigue viva.

### D-12. Solo 14 imanes y nada de acero
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** se diseña con los imanes de 5 × 1,6 mm que hay, y sin chapas.
- **Qué llevó a ella:** Pepe contó los imanes: 14, y no tiene chapas. La v2 pedía 24 (contra-reporte de la v2).
- **Estado:** Activa. Quedan 13 (dato de `caja/BRIEF-v5.md`).

### D-13. Impresora, etiqueta y material
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** Bambu Lab X1 Carbon con AMS, etiqueta NFC de 25 mm y filamento mármol blanco para la funda.
- **Qué llevó a ella:** es lo que Pepe tiene.
- **Estado:** Activa.

### D-14. Sin palabras en la tapa y sin pestaña de arrancar
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** la tapa es lisa y la funda no lleva pestaña.
- **Qué llevó a ella:** *(Rellenado por la sesión del Mac, 21-nov-2026.)*
  - *Palabras en la tapa:* la sesión del Mac propuso que la tapa llevara «pronto / tarde». Pepe (19-nov, 19:38): «Me convence todo menos lo de pronto tarde, quiero lo de la aguja pero no así». No dijo por qué.
  - *Pestaña de arrancar:* la idea fue de Pepe (19-nov, 22:39): «una pestaña que tiras de ella y se rompe». La sesión del Mac la desaconsejó en la propia caja: la caja es para quedársela y quedaría un borde roto para siempre; el PLA rasga mal; al ser de un solo uso, la que se regala es justo la que no se ha probado; y ya había cuatro pasos. Propuso un precinto aparte. Pepe (22:42): «Descarto esta opción».
- **Estado:** Activa.

### D-15. Ninguna caja entera sin medir antes el reloj
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe. Figura entre lo decidido en `sesiones/SESION-MAC.md`.
- **Decisión:** no se imprime la caja completa hasta tener las medidas del reloj montado.
- **Qué llevó a ella:** todas las medidas del reloj son supuestas y el hueco depende de ellas.
- **Estado:** Activa.

### D-16. v3: funda de campana y cierre de un empujón
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe pidió atender el contra-reporte entero.
- **Decisión:** funda de campana, pinza en C con peana, cierre de un empujón y 8 imanes.
- **Qué llevó a ella:** el contra-reporte de la v2: 6 fallos graves. El reloj no se podía montar, cerrar era torpe y no había apertura de emergencia.
- **Estado:** Sustituida por D-17.

### D-17. v4: se cierra con la aguja puesta
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** rotor de un solo sentido con tope, peana corredera y pinza a medida. El cierre de un empujón pasa a opcional.
- **Qué llevó a ella:** el contra-reporte de la v3: el cierre de un empujón se acuña (calculado) y la pinza estaba dibujada con una forma que no es la suya.
- **Estado:** Parada (D-19).

### D-18. v4.1: un parche, no una v5
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** corregir la v4 con un parche y, después, imprimir.
- **Qué llevó a ella:** el contra-reporte de la v4 solo veía 2 fallos graves y recomendaba no hacer otra versión entera. Iban ya cinco sin imprimir nada.
- **Estado:** Parada (D-19).

### La v5

### D-19. Se abandona la llave magnética
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** la v4.1 queda parada. Fuera la aguja. **Ningún mecanismo puede depender de imanes.** Se vuelve a diseñar desde cero.
- **Qué llevó a ella:** la probeta P1, impresa y probada por Pepe (medido): «los imanes no son ni de cerca lo suficientemente fuertes como para mover el mecanismo». Los cálculos decían que sí (0,89 N entre aguja y rotor) y estaban equivocados. Detalle en `caja/resultados-probetas.md`.
- **Qué se descartó:** arreglar la v4.1. Había margen para acercar los imanes (la P0 permitía bajar la piel del panel de 1,4 a 0,8 mm), pero Pepe no quiso seguir por ahí.
- **Estado:** Activa.

### D-20. Caja cilíndrica con iris y ascensor
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe, sector por sector, con la sesión del Mac.
- **Decisión:** se gira el bisel de arriba; unos engranajes se mueven a la vista, la tapa se abre como el diafragma de una cámara y el reloj sube de pie. La tabla completa está en `caja/BRIEF-v5.md`, apartado 3.
- **Qué llevó a ella:** tras D-19 hacía falta un mecanismo que funcione solo con piezas impresas. Lo que consta de cada elección:
  - *Engranajes:* para dar aire de relojería.
  - *Planetario con satélites que orbitan:* lo pidió Pepe. La sesión del Mac creyó primero que no se podía y luego encontró la forma (apartado 5 del brief).
  - *Imanes solo de adorno:* por D-19.
  - *Tarjeta en la funda o fuera:* bajo el reloj no cabe por el hueco.
  - *Tamaño normal de estuche:* Pepe dijo que no hace falta que sea pequeña.
  - *Tramo muerto al empezar a girar:* propuesta de la sesión del Mac («la caja llega tarde»). Pepe: «puede ser interesante».
  - *Sin trinquete:* lo dijo Pepe al elegir la ruta, sin motivo. Antes le había gustado. La sesión del Mac había avisado de que un trinquete de verdad solo deja girar en un sentido y la caja tiene que poder cerrarse; si pesó eso, no consta.
  - *Bisel grafilado:* propuesta de la sesión del Mac, porque el canto estriado dice «gírame» sin una palabra. Pepe lo aceptó.
  - *Iris liso:* la sesión del Mac propuso grabar en el iris los doce números amontonados de la esfera. Pepe: «lo del iris no». Sin motivo.
  - *Índice en relieve:* de tres propuestas para marcar el frente (índice, corona en el costado, cara plana), Pepe: «Me gusta el índice». La sesión del Mac lo recomendaba por sencillo.
  - *El bisel y no la base:* la sesión del Mac preguntó cuál; Pepe: «Giras el bisel de arriba». Sin motivo.
  - *Reloj de pie:* a la pregunta «¿tumbado o de pie?», Pepe contestó que no sabía a qué se refería, «pero igual que en la anterior caja».
  - *Lo azul:* de tres propuestas (un satélite, una marca en el bisel, el interior), eligió el satélite.
  - *Engranajes a medias:* palabras de Pepe, «parcialmente a la vista tipo skeleton», frente a una ventana, todo a la vista o escondidos.
  - *Qué imanes:* Pepe pidió «formas de usar los imanes para dar una experiencia más premium pero sin que nada dependa de ellos». De cinco usos propuestos se quedó con tres: el final del recorrido, la funda y el soporte.
  - *(Motivos rellenados por la sesión del Mac, 21-nov-2026.)*
- **De dónde salió la idea** (20-nov, de las 21:00 a las 23:30, conversación con la sesión del Mac; rellenado por ella el 21-nov-2026):
  1. *Primera lluvia de ideas, sin engranajes:* aguja con un eje en un agujero central de la tapa, aguja como pasador, tapa que gira, aguja como herramienta, imanes más grandes y caja sin cerradura. La sesión del Mac apostaba por la aguja con eje. Pepe no eligió ninguna: pidió engranajes «para darle ese feeling de reloj» y dijo que la aguja no había que usarla «sí o sí».
  2. *Segunda, con engranajes:* corona que retira cerrojos, cajón que sale solo, ascensor, dos puertas, hora secreta, iris y caja que hace tictac. Pepe: «me llaman la 2, 3, 6 y el trinquete» (cajón, ascensor e iris) y «me gustan también los engranajes planetarios». Pidió combinar: «que algo se abra y que el reloj se mueva».
  3. *Tres rutas:* A, iris y ascensor; B, compuertas y ascensor; C, cajón que levanta el reloj. La sesión del Mac recomendó la B, por riesgo y por tamaño. Pepe eligió la A: «Desarrolla la ruta A: iris y ascensor. Sin trinquete. El reloj sube entero». Añadió que la caja no tenía que ser pequeña y que había más de un mes.
- **Qué se descartó:** la lista está en [ESTADO.md](ESTADO.md), apartado 3.
- **Estado:** Activa, **menos el iris y la forma cilíndrica, sustituidos por D-29** (21-nov-2026). Lo demás sigue: bisel, planetario, ascensor, reloj de pie, lo azul, los imanes de adorno.

### D-21. Primero tres probetas, después la caja
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe, a propuesta de la sesión del Mac.
- **Decisión:** iris, ascensor y planetario se prueban por separado y en ese orden. La caja entera no se modela hasta que pasen los tres.
- **Qué llevó a ella:** se hicieron cinco versiones en papel antes de imprimir nada, y la primera pieza impresa tumbó la idea central.
- **Estado:** Sustituida por D-30 (21-nov-2026). La probeta del iris se hizo con esta regla.

### D-22. Plan B del iris
- **Fecha:** 20-nov-2026.
- **Quién decide:** propuesta de la sesión del Mac, recogida en el brief.
- **Decisión:** si el iris no sale en dos rondas, se cambia por dos compuertas correderas movidas por un piñón entre dos cremalleras.
- **Qué llevó a ella:** el iris es la pieza con más riesgo: láminas finas que rozan. El plan B aprovecha el mismo ascensor.
- **Estado:** No se usa. El iris de láminas funcionó, a Pepe no le convenció, y en vez de las compuertas eligió puertas con bisagra (D-29). Además, hecha la cuenta en plano, las compuertas pedían una carcasa de unos 160 mm (calculado, `caja/reporte-v5/calculos-mac/gajos_al_ras.py`).

### D-23. La probeta del iris: una carcasa de 8 láminas y dos gruesos
- **Fecha:** 20-nov-2026, 23:44.
- **Quién decide:** Pepe («Sí me vale esa forma»), a propuesta de la sesión del PC.
- **Decisión:** una sola carcasa de 8 láminas, con dos juegos de láminas, de 1,2 y de 0,8 mm. Agujero central de unos 5 mm, sin prometer cero. El hueco es un parámetro del generador.
- **Qué llevó a ella:** un cálculo en plano de la sesión del PC, sin CAD ni pieza impresa:
  - Con 6 láminas la carcasa sale de 134 a 141 mm; con 8, de 125 a 127. El objetivo eran 130.
  - Tres discos de unos 126 mm y las láminas ya ocupan dos bandejas: dos variantes no caben en una.
  - Al cerrar se apilan 4 o 5 láminas en el centro: cerrar del todo es donde más fácil se engancha.
- **Qué se descartó:** la variante de 6 láminas (no cumple el diámetro) y el agujero cero como requisito.
- **Estado:** Activa. Modelada el 21-nov. **Ojo: la cifra de 125 a 127 mm estaba mal; con el iris dibujado entero salen 133,5 (D-27).**

### D-24. Un solo repositorio y este registro
- **Fecha:** 20-nov-2026, 23:44.
- **Quién decide:** Pepe.
- **Decisión:** todo el proyecto pasa a un solo directorio, con la historia, el estado y cada decisión explicada.
- **Qué llevó a ella:** en palabras de Pepe, que las dos sesiones «compartan recursos, información y puedan trabajar sobre el trabajo de la otra fácilmente». Ese mismo día la sesión del PC tardó tres cuartos de hora en ver un repositorio que no conocía, y el guion del tutorial solo existía en el PC.
- **Qué se descartó:** seguir con tres repositorios y una carpeta que los junta, como estaba en el Mac.
- **Estado:** Activa. Pepe dijo «Fusiona» el 20-nov-2026 a las 23:55.

### D-25. Cada sesión sube su trabajo, con la confirmación de Pepe
- **Fecha:** 20-nov-2026, 23:55.
- **Quién decide:** Pepe.
- **Decisión:** cada sesión puede subir su trabajo al terminar. Antes le dice a Pepe qué va a subir y espera su «sí».
- **Qué llevó a ella:** la regla anterior («nada de commit ni push sin que Pepe lo pida») frenaba que las dos sesiones compartieran el trabajo: el guion del tutorial estuvo horas solo en el PC. Pepe quiere que se comparta, pero sin perder el control de lo que se sube. En sus palabras: «que cada sesión pueda subir su trabajo pero que yo simplemente confirme antes de que suba».
- **Qué se descartó:** subir sin preguntar, y seguir esperando a que Pepe lo pida cada vez.
- **Estado:** Activa. Sustituye a la regla del apartado 6 de `sesiones/SESION-MAC.md`.

### D-26. La web se sirve desde `docs/`, los repositorios antiguos se archivan y el Mac pasa al clon único
- **Fecha:** 21-nov-2026, 00:10.
- **Quién decide:** Pepe. La sesión del Mac le preguntó por las tres tareas del relevo y marcó las tres.
- **Decisión:** GitHub Pages sirve la rama `main`, carpeta `/docs`. `eventually-caja` y `eventually-proyecto` quedan archivados (solo lectura). En el Mac, `~/Watchpage` es un clon de este repositorio y la carpeta de antes es `~/Watchpage-antiguo`.
- **Qué llevó a ella:** el relevo de la sesión del PC. Además, con Pages sirviendo la raíz, la web solo funcionaba saltando a `…/eventually/docs/` y la imagen de la vista previa del enlace daba error 404 (medido con `curl` el 21-nov).
- **Qué se descartó:** nada.
- **Estado:** Activa. Comprobado el 21-nov: la web responde en su dirección de siempre, con `?caja` y con `?reloj`.

### D-27. La probeta del iris se imprime con 133,5 mm y el resto de la caja se adapta
- **Fecha:** 21-nov-2026, 01:05.
- **Quién decide:** Pepe, el 21-nov a la 01:15 («el 133,5 está bien si luego adaptamos el resto»), a propuesta de la sesión del PC.
- **Decisión:** la probeta del iris se imprime tal como está modelada, con 133,5 mm de diámetro exterior (el objetivo del brief eran 130). **El resto de la caja se adapta a ese diámetro**, no al revés. Si al medir el reloj o al probar la pieza cambia el hueco, se recalcula.
- **Qué llevó a ella:**
  - **El cálculo de D-23 estaba mal.** Daba 125 a 127 mm con 8 láminas porque no contaba dónde va el eje de cada lámina ni cómo se sujeta la tapa. Lo hizo la sesión del PC y fue esa cifra la que oyó Pepe.
  - Al dibujarlo entero (calculado en plano, grado a grado, `caja/iris_diseno_v5.py`): el eje de una lámina no puede quedar debajo de otra lámina, así que va a 61,9 mm del centro; detrás van la cola (3,3 mm), su holgura (0,35) y una pared (1,2). Suma 66,75 de radio.
  - Del modelo de Fusion: 133,50 mm medidos. Todo lo demás del encargo se cumple en el modelo.
  - Lo que la probeta tiene que contestar, si un iris de PLA abre y cierra suave, no depende de esos 3,5 mm.
- **Cómo es el iris modelado** (para que la otra sesión no tenga que deducirlo): cada lámina gira en un poste de la base, en una isla pegada a la pared por donde no pasa ninguna otra lámina; lleva un tetón hacia arriba que entra en una ranura radial del aro; el aro va encima de las láminas y saca la orejeta por un hueco de la pared, cuyos extremos son los topes; la tapa cierra con una bayoneta de cuatro uñas en rampa de 45°. Detalle en `caja/reporte-v5/probeta-iris.md`.
- **Qué se descartó:**
  - *La cola de la lámina encajada en un alveolo redondo de la pared, sin poste.* El alveolo solo abrazaba 62° de la cola: se salía de lado (calculado).
  - *Ejes colgados de la tapa, pasando por ranuras del aro.* Cabía en unos 129 mm, pero con muchas piezas finas y un montaje a ciegas. No se llegó a modelar.
  - *Láminas en luna con la cola metida entre las demás.* Salía de 128 mm, pero la cola solo apoyaba en el 21 % de su superficie (calculado).
  - *Bajar ahora a 130 con 10 láminas o con el hueco de 72 mm.* Se deja para después de probar esta: 10 láminas contradice D-23 y el hueco depende del reloj, sin medir.
- **Estado:** Cerrada. Se imprimió así el 21-nov y funcionó, pero el iris ya no va en la caja (D-29): los 133,5 mm dejan de mandar.

### D-28. La probeta del iris lleva un tercer juego de láminas, de 0,4 mm
- **Fecha:** 21-nov-2026, 08:05.
- **Quién decide:** Pepe («Sí, añádelo»), a propuesta de la sesión del Mac.
- **Decisión:** a la probeta del iris se le añade un tercer juego de 8 láminas de 0,4 mm de grueso (dos capas). La carcasa no cambia. Los juegos de 1,2 y de 0,8 se imprimen igual, para comparar. Para este juego deja de valer el «1,2 mm o más» del apartado 11 del brief.
- **Qué llevó a ella:** la revisión de la sesión del Mac (`caja/reporte-v5/contra-reporte-iris.md`), antes de imprimir nada:
  - Ocho láminas en rueda, cada una sobre la anterior, obligan a que cada lámina baje un grueso dentro de su ancho. Con el agujero a 5 mm eso son 31° de inclinación de lado con 1,2 mm, 22° con 0,8 y 11,5° con 0,4 (calculado; es geometría).
  - Estimado, con fuerzas y sin pieza que lo confirme: las de 1,2 se pondrán duras con el agujero a 30-40 mm, las de 0,8 a 15-20 mm, y las de 0,4 llegarían a cerrar.
  - Es barato: solo cambian las láminas y es una bandeja más.
  - El brief de la sesión del Mac pedía a la vez láminas de 1,2 mm o más y agujero de 8 mm o menos, sin haber comprobado que cupieran las dos cosas.
- **Qué se descartó:** nada. Un juego de 0,6 mm se mencionó como posible y Pepe no lo ha pedido. Esperar a imprimir antes de añadirlo tampoco: la carcasa ya se puede ir imprimiendo.
- **Pegas que se conocen:** dos capas de PLA blanco dejan pasar luz. Si cierran, se verá si hace falta una lámina escalonada, fina en la punta y gruesa donde se ve.
- **Estado:** Activa. Modelado por la sesión del PC el 21-nov a las 08:15 (`caja/probetas-v5/iris-laminas-0.4mm-x8.3mf`). Sin imprimir. La sesión del PC añadió, sin que se pidiera, un refuerzo de 6 mm alrededor del tetón: un tetón de 3 mm no puede nacer de una hoja de dos capas.

### D-29. La tapa pasa a ser de dos puertas y la caja, cuadrada
- **Fecha:** 21-nov-2026, 15:15.
- **Quién decide:** Pepe. La idea es suya.
- **Decisión:** se deja el iris. La caja pasa a ser **cuadrada** y la tapa son **dos puertas con bisagra, una a la izquierda y otra a la derecha del reloj, que se abren solas mientras el reloj sube** y quedan de pie a sus lados. **Se mantiene el bisel redondo de arriba, con los engranajes a la vista y el satélite azul**, sobre la caja cuadrada. Todo lo demás de D-20 sigue igual.
- **Qué llevó a ella:**
  - La probeta del iris, impresa y probada por Pepe el 21-nov (medido, `caja/resultados-probetas.md`): funciona con los tres gruesos, pero «creo que el iris no va a quedar con el estándar de calidad que busco».
  - A la pregunta de la sesión del Mac sobre qué no le llegaba, con cuatro respuestas posibles, Pepe marcó dos: **cómo se ve cerrado** (láminas en escalera, agujero central, rendijas) y **que parece frágil**. No marcó el tacto ni el acabado de impresión.
  - La sesión del Mac le presentó cuatro alternativas (iris de gajos al ras, dos compuertas, tapa entera que sube con el reloj, ocho pétalos que se levantan) y recomendó los gajos. Pepe contestó: **«Algo como la 4 pero en una caja cuadrada, unas puertas que se abren solas mientras el reloj sube»**.
  - Después, a dos preguntas de la sesión del Mac, eligió «Dos, a los lados» y «Sí, se mantiene» el bisel. Eran las dos respuestas que la sesión del Mac recomendaba: a los lados, porque abiertas no tapan la esfera vista de frente; el bisel, porque así no cambia nada más de lo decidido.
  - Por qué cuadrada y no redonda con un hueco rectangular: **No consta.** Pepe lo dijo así.
- **Qué se descartó:**
  - *El iris de láminas, para la caja.* Por lo dicho arriba. Hacer las láminas más gruesas arregla la fragilidad y empeora la escalera.
  - *Iris de gajos al ras, dos compuertas correderas, tapa entera que sube y ocho pétalos.* Pepe no las eligió; no dio motivo de cada una.
  - *Dos puertas, delante y detrás,* y *cuatro triángulos.* Pepe eligió las dos de los lados. En las otras, la puerta de delante tapa parte del reloj visto de frente (dicho por la sesión del Mac al preguntar).
  - *Quitar el bisel y mover el reloj de otra forma.* Pepe dijo que se mantiene.
- **Qué falta por saber** (nada de esto está dibujado ni impreso):
  - Cómo se mueven las puertas. Propuesta de la sesión del Mac, sin comprobar: las mueve el mismo giro, con una leva, un poco por delante del reloj y sin que el reloj las toque nunca. Lo dirán el modelo y luego la probeta (`caja/BRIEF-v5.md`, apartados 4 y 12).
  - El tamaño. Estimado a mano por la sesión del Mac: el hueco rectangular de 50 × 59 mm cabe en un círculo de 77 mm, casi el mismo de 75 que rodeaban los engranajes, y desaparece el disco de 133,5 del iris. La caja saldría de unos 150 mm de lado. Sin dibujar.
  - Las medidas del reloj siguen siendo supuestas, y el hueco depende de ellas.
- **Estado:** Activa. Sin modelar.

### D-30. Primero la caja entera, modelada y comprobada; después, las probetas
- **Fecha:** 21-nov-2026, 15:20.
- **Quién decide:** Pepe.
- **Decisión:** la sesión del PC modela la caja completa (D-29), comprueba en el modelo que todos los mecanismos funcionan y hace el reporte. Con el diseño final planeado, se imprimen las probetas, sacadas de ese modelo, para ajustar cada mecanismo. Sustituye a D-21, que mandaba probar tres probetas antes de modelar la caja.
- **Qué llevó a ella:** palabras de Pepe a la sesión del Mac: «quiero que la sesión del pc modele completamente esta caja, compruebe todos los mecanismos funcionando y haga el report, una vez tengamos la caja final planeada y diseñada podemos imprimir las probetas para ver como ajustar cada mecanismo». Viene justo después de la probeta del iris, que se hizo suelta, funcionó y aun así no sirvió para la caja (D-29). Si pesó eso, no consta: Pepe no dio más motivo.
- **Qué se descartó:** seguir con D-21 (una probeta suelta por mecanismo antes de modelar nada más). La sesión del Mac había escrito ya el encargo de una probeta suelta de las puertas; queda dentro del brief nuevo como una de las probetas de después.
- **Pegas que se conocen** (dichas por la sesión del Mac a Pepe al apuntarlo):
  - D-21 nació de que la primera pieza impresa tumbó cinco versiones hechas en papel. Con este orden, si una probeta falla, hay que rehacer parte del modelo. Por eso el brief pide que todo vaya por parámetros.
  - «Comprobado en el modelo» es que las piezas se mueven y no se pisan. No es «funciona».
  - Sigue en pie D-15: la caja completa no se imprime sin medir antes el reloj.
- **Estado:** Activa. Encargo en `caja/BRIEF-v5.md`, apartado 11. Sin modelar.

