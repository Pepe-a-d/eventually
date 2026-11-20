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

- **D-01:** por qué el nombre Eventually y «Late Edition · 1 of 1».
- **D-14:** por qué se descartaron las palabras en la tapa y la pestaña de arrancar.
- **D-20:** por qué el tramo muerto al empezar a girar, por qué sin trinquete, por qué bisel grafilado, iris liso e índice en relieve; y por qué se descartó girar la base, la corona en el costado, la cara plana y el reloj tumbado.
- **D-20:** de dónde salió la idea del iris y el ascensor: qué otras ideas hubo en la lluvia de ideas y por qué perdieron.

## Decisiones hasta el 20 de noviembre de 2026

Reunidas por la sesión del PC a partir de los documentos de las dos sesiones. Donde el motivo no estaba escrito en ningún sitio, pone «No consta».

### El reloj y la web

### D-01. El nombre
- **Fecha:** 19-nov-2026.
- **Quién decide:** Pepe.
- **Decisión:** el reloj se llama Eventually, con la línea «Late Edition · 1 of 1».
- **Qué llevó a ella:** No consta.
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
- **Qué llevó a ella:** No consta. Se propusieron («pronto/tarde», pestaña de rasgar) y Pepe las descartó.
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
  - *Tramo muerto al empezar a girar, sin trinquete, bisel grafilado, iris liso, índice en relieve:* elegidos por Pepe. El motivo de cada uno no consta.
- **Qué se descartó:** la lista está en [ESTADO.md](ESTADO.md), apartado 3.
- **Estado:** Activa. Nada modelado ni impreso.

### D-21. Primero tres probetas, después la caja
- **Fecha:** 20-nov-2026.
- **Quién decide:** Pepe, a propuesta de la sesión del Mac.
- **Decisión:** iris, ascensor y planetario se prueban por separado y en ese orden. La caja entera no se modela hasta que pasen los tres.
- **Qué llevó a ella:** se hicieron cinco versiones en papel antes de imprimir nada, y la primera pieza impresa tumbó la idea central.
- **Estado:** Activa.

### D-22. Plan B del iris
- **Fecha:** 20-nov-2026.
- **Quién decide:** propuesta de la sesión del Mac, recogida en el brief.
- **Decisión:** si el iris no sale en dos rondas, se cambia por dos compuertas correderas movidas por un piñón entre dos cremalleras.
- **Qué llevó a ella:** el iris es la pieza con más riesgo: láminas finas que rozan. El plan B aprovecha el mismo ascensor.
- **Estado:** Propuesta.

### D-23. La probeta del iris: una carcasa de 8 láminas y dos gruesos
- **Fecha:** 20-nov-2026, 23:44.
- **Quién decide:** Pepe («Sí me vale esa forma»), a propuesta de la sesión del PC.
- **Decisión:** una sola carcasa de 8 láminas, con dos juegos de láminas, de 1,2 y de 0,8 mm. Agujero central de unos 5 mm, sin prometer cero. El hueco es un parámetro del generador.
- **Qué llevó a ella:** un cálculo en plano de la sesión del PC, sin CAD ni pieza impresa:
  - Con 6 láminas la carcasa sale de 134 a 141 mm; con 8, de 125 a 127. El objetivo eran 130.
  - Tres discos de unos 126 mm y las láminas ya ocupan dos bandejas: dos variantes no caben en una.
  - Al cerrar se apilan 4 o 5 láminas en el centro: cerrar del todo es donde más fácil se engancha.
- **Qué se descartó:** la variante de 6 láminas (no cumple el diámetro) y el agujero cero como requisito.
- **Estado:** Activa. Sin modelar.

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
