# La caja v5 entera: revisión de la sesión del Mac

Sesión del Mac · 22 de noviembre de 2026 · revisa [caja-entera.md](caja-entera.md), el reporte de la sesión del PC.
Programa de comprobación: [`calculos-mac/revisar_caja_v5.py`](calculos-mac/revisar_caja_v5.py). Los demás programas, en [`calculos-mac/revision-caja/`](calculos-mac/revision-caja/).

## En una frase

El modelo está bien construido y el reporte sale de verdad de él, pero **no tiene cero errores: he encontrado 9 en las piezas, 1 en el programa y 6 en el reporte y los ficheros.** Ninguno tumba la idea. Casi todos son de los que una pieza impresa habría sacado a la primera, y arreglarlos ahora cuesta poco. **Mi consejo es no imprimir nada, tampoco la probeta de las puertas, hasta que estén corregidos:** cinco de los nueve están en esa probeta.

**Lo que esta revisión es y no es.** Son pruebas de geometría sobre el dibujo: distancias, piezas que se pisan, capas sin apoyo, caminos de montaje. No hay ninguna fuerza. Aunque después de los arreglos mi programa no dé ningún fallo, eso querrá decir que el dibujo cumple, no que la caja funcione. Eso lo dirán las probetas.

## 1. Cómo se ha hecho

1. **He vuelto a construir las 27 piezas en el Mac** con el programa de la sesión del PC. Me da lo mismo que a ella: mismas comprobaciones, mismos volúmenes. El reporte no inventa nada.
2. **Le he hecho las pruebas que ese programa no hace.** El del PC mira, de 2 en 2 grados, si dos piezas se pisan. No mira si quedan demasiado justas para imprimirse, ni las piezas con sus juegos, ni el montaje paso a paso, ni si cada pieza sale sin soportes, ni si el texto del reporte coincide con el modelo.
3. **Cinco revisiones independientes, en paralelo:** puertas, ascensor y engranajes, impresión, montaje, y reporte contra modelo. Cada una con sus programas.
4. **Cada hallazgo de los apartados 2 y 3 lo he repetido yo** con un programa mío distinto. Lo que no he repetido lo digo.

**Lo que no he podido mirar:** el fichero de Fusion (aquí no hay Fusion). Sí he comparado con el modelo los nueve ficheros de imprimir que salieron de Fusion: siete coinciden pieza a pieza; los otros dos (tubo y plataforma), solo en volumen y medidas, porque sus mallas no están cerradas.

## 2. Errores en las piezas

Ordenados por lo que importan. «Línea» es la línea de `revisar_caja_v5.py` que hoy da FALLA y tiene que dar «bien».

### E1. Hay un agujero en el centro de la junta de las puertas

- **Qué:** con las puertas cerradas queda un agujero de **0,3 × 1,2 mm** en el centro de la raya. Mirando desde arriba se ve lo de dentro, y a contraluz pasa la luz.
- **Por qué:** cada puerta lleva media junta en cuña y media en hueco. La cuña empieza a 0,6 mm del centro y el hueco de la otra acaba en el centro: en ese tramo no tapa ninguna.
- **Qué incumple:** «sin agujero; mirando desde arriba no se ve lo de dentro». El reporte dice «por la raya solo se ve puerta».
- **Por qué no se vio:** la única comprobación de la junta es de la fase 1 y está hecha con la junta antigua, en escalón, que ya no existe (ver P1).
- **Línea:** «cerradas, mirando desde arriba no queda ningún agujero».

### E2. Los tetones de la plataforma no tienen juego en la rampa

- **Qué:** el diseño dice 0,20 mm de holgura entre cada tetón y su ranura. En los tramos planos la hay. **En la rampa quedan 0,02 mm.** Con lo medido en piezas impresas (0,15 ya sujeta), eso es un ajuste a presión durante 243 de los 345 grados de giro.
- **Por qué:** la holgura está puesta en vertical, y la ranura sube inclinada 15°: un tetón redondo en una ranura inclinada pierde sitio. Además la ranura se dibuja barriendo un trapecio de lados rectos, que se mete otro poco.
- **Consecuencia probable:** la plataforma se agarrota al subir. No se pisan en el modelo, así que el programa del PC no podía verlo.
- **Línea:** «en la rampa, entre los tetones de la plataforma y las ranuras del tubo quedan 0,15 mm o más».

### E3. Las puertas abiertas no quedan sujetas donde pide el brief, y se acercan al reloj

- **Qué pide el brief:** abiertas, entre 85° y 95°, y el reloj siempre a 3 mm o más de ellas.
- **Con el aro en su sitio exacto:** cada puerta se deja mover entre 87,25° y 93,0°. Hasta ahí cumple el ángulo. Pero a 87,25° **el reloj queda a 2,3 mm,** no a 3, y la puerta se mete 0,9 mm en el hueco libre de 50 × 59.
- **Con el aro corrido lo que le deja su holgura:** el aro solo va centrado por su borde, con 0,3 mm de juego. En mi prueba, con el aro corrido 0,15 mm la puerta cede hasta **84,75°** y el reloj queda a **1,0 mm**. El revisor de las puertas, corriéndolo 0,29 mm en la peor dirección, llegó a 82,3°, donde **la puerta toca el reloj.**
- **Por qué:** hacia dentro no hay ningún tope fijo. A la puerta abierta solo la sujeta una bola de 5 mm contra la pared de su pista, y esa pista va en un aro que tiene juego.
- **Importa más de lo que parece:** empujar una puerta hacia dentro es justo lo que corre el aro. Y es lo que no te convenció del iris: que parezca frágil.
- **Salvedad:** las medidas del reloj son supuestas.
- **Líneas:** las tres de «abiertas…» y la del reloj de pega.

### E4. Las dos puertas se rozan al abrir, y se pisan si una se adelanta 2°

- **Qué:** al empezar a abrir, la arista de abajo de cada puerta se acerca a la otra: de 0,3 mm pasan a **0,08 mm** a los 5°. El propio programa del PC pedía 0,2 o más, pero lo comprobó con la junta antigua.
- **Y si no van a la vez:** con una puerta 2° por delante de la otra, se pisan. El mecanismo deja bastante más que eso: a medio abrir, cada puerta baila varios grados contra su pista.
- **De pie,** el peso lleva a las dos al mismo lado y probablemente no pase. Inclinando la caja o tocando una puerta, sí.
- **Líneas:** «al abrir a la vez…» y «con una puerta 2 grados por delante…».

### E5. El ala del bisel está dibujada al revés: una repisa entera en el aire

- **Qué:** el reporte dice que todas las piezas salen sin soportes. El ala del bisel, la que lo retiene bajo el labio del cuerpo, tenía que ser una escalera de tres peldaños para imprimirse sin soportes. **Los peldaños tienen las alturas cambiadas** y lo que sale es una repisa plana de 2,4 mm en toda la vuelta: unos 1.150 mm² impresos en el aire.
- **Consecuencia:** saldrá descolgada, y esa cara va a 0,4 mm del cuerpo.
- **Está también en el fichero de imprimir** `caja-probeta-planetario-bisel.3mf`.
- **Línea:** «bisel, boca abajo: el ala se imprime en escalera».

### E6. El aro de las puertas: un extremo de cada pista nace en el aire, y una pared mide 0,3 mm

- **Qué:** el final de cada pista, por el lado de «abierto», sobresale del anillo que la sostiene: 12 mm² por pista impresos en el aire. Es justo la pared que hace de tope de la puerta abierta hacia fuera.
- **Y además:** en el lado de «cerrado», la pared de fuera de la pista mide **0,30 mm**, menos que la boquilla. El parámetro dice 2 mm. Esa no trabaja, pero no saldrá.
- **Está también en el fichero de imprimir** `caja-probeta-puertas-bandeja-B.3mf`.
- **Líneas:** las dos de «aro de las puertas».

### E7. La varilla de la puerta toca el aro antes que la bola

- **Qué:** cerrada, la varilla pasa a 0,107 mm del canto de la pista; la bola tiene 0,15. Al levantar una puerta, lo primero que toca es la varilla, de 3 mm. El programa dice que la varilla no debe tocar «en ningún ángulo».
- **Línea:** «cerradas, entre cada puerta (varilla y bola) y el aro».

### E8. El cuerpo y la funda entran girados

- **Qué dice el reporte:** que el cuerpo «solo entra con el índice al frente» y la funda «solo entra con su frente al frente».
- **El cuerpo:** girado un cuarto o media vuelta asienta igual; lo único que cambia es que un pestillo no hace clic.
- **La funda:** el índice sale 0,6 mm y la funda tiene 0,5 de holgura por lado. Girada y corrida 0,2 mm, baja hasta el fondo sin tocar nada. La frase quedaría girada respecto al frente.
- **Qué incumple:** «ninguna pieza se puede montar en una posición que no sea la suya».
- **Líneas:** «el cuerpo girado…» y «la funda girada…».

### E9. Con el reloj arriba, el pedestal no rellena el hueco: quedan dos zanjas

- **Qué pide el brief:** arriba, el pedestal rellena el hueco con 1 mm o menos de rendija por lado. El reporte dice 0,4.
- **Qué hay:** a los lados, 0,9 mm hasta cada puerta: bien. **Delante y detrás del reloj queda a la vista una zanja de 7,7 mm de ancho y 5 de hondo.** Es el asiento donde apoyaban las puertas cerradas, que es más largo que el hueco por el que sube el pedestal.
- **No sé si te importa:** se ve en la animación que ya viste y diste por buena. Lo cuento porque el reporte no lo dice. **Es tuyo decidir si se arregla.**
- **Línea:** «reloj arriba: alrededor del pedestal…».

## 3. Error en el programa: con otro reloj no se regenera solo

No afecta a la caja con las medidas de hoy. Afecta a lo que más va a pasar: que midas el reloj y no mida lo supuesto.

- El reporte dice que el día que midas el reloj «se cambian ahí y se regenera todo». Lo he probado con un reloj 2 mm más ancho, 2 más de fondo y 4 más alto.
- **La primera parte del programa dice HAY FALLOS** (a la rueda central le queda 1,1 mm bajo los dientes, y la espiral del plato se sale del tubo). **La segunda parte, la que hace las piezas, dice TODO BIEN** con esas mismas medidas: no repite las comprobaciones de la primera.
- Para que vuelva a pasar hay que cambiar a mano los dientes de la rueda central y el radio del tubo, con condiciones que el programa no dice. Con una combinación que la primera parte da por buena (81 dientes), los seis satélites pisan al bisel.
- Varias medidas están escritas a mano y no salen de las del reloj: las columnas, el asiento, los ejes de los satélites.
- Con 1 mm más de ancho y 1 más de fondo a la vez, ya falla. **El margen de hoy es de alrededor de 1 mm.**

Esto último lo encontró el revisor del ascensor; yo he repetido la primera prueba.

## 4. Errores en el reporte y en los ficheros

| # | Qué dice | Qué hay |
| --- | --- | --- |
| P1 | La fase 1 comprueba la junta («no hay ninguna línea recta que la cruce», «no se tocan: 0,30 mm») | Lo comprueba sobre la junta antigua, en escalón. Las piezas llevan otra, en cuña. Sobre la junta real no había ninguna comprobación. `caja-v5.json` es también de esa versión anterior |
| P2 | Orden de montaje: 8, rueda central; 10, plato; 11, satélites | **No se puede.** El plato es un anillo que va debajo de la rueda central y no pasa alrededor de ella; los satélites tampoco entran en sus ejes con ella puesta. Vale este orden: pasadores, cerrar puertas y tetón, plato, satélites, **rueda central**, bisel y cuerpo. Comprobado: así nada pisa nada |
| P3 | «Todas, sin soportes» | Falso para el bisel (E5), el aro (E6) y el tetón con pomo de la probeta, que viene en su fichero con el pomo arriba: 55 mm² en el aire. Dándole la vuelta sale bien |
| P4 | Probeta del planetario: «al girar el bisel pasa todo en su orden» | En ningún fichero está el tetón normal, y el de pomo no cabe bajo el plato. Sin él no se puede hacer esa prueba |
| P5 | «Boca abajo no se cae nada: bien» | La lista de piezas que comprueba no incluye el soporte ni el reloj. Con la caja cerrada caen 5 mm sobre las puertas; abierta, se salen. El brief pide a la vez «soporte suelto» y «boca abajo no se cae nada»: **esa contradicción es mía, y la decides tú** |
| P6 | Varias cifras | Ver la tabla de abajo |

Cifras del reporte que no coinciden con el modelo (calculadas por el revisor del reporte; no las he repetido una a una):

| Reporte | Modelo |
| --- | --- |
| Las puertas abiertas sobresalen 25,5 mm | 27,65 mm la mitad que lleva la cuña; 25,35 la otra |
| Diente más fino: punta de 0,44 mm; 1,12 a media altura | 0,81 y 2,26. El reporte da la mitad del grueso |
| Tetones con 0,2 mm de holgura; cabeceo de 0,14° | 0,02 mm en la rampa (E2) |
| Pedestal arriba, rendija de 0,4 mm por lado | 0,9 a los lados y zanjas de 7,7 delante y detrás (E9) |
| Reloj a 6,00 mm de la rueda central | 18,3. El 6,00 es el tope de búsqueda del programa |
| Imanes a unos 37 mm de la cabeza del reloj | 34. Cumple los 30 del brief |
| Puertas abiertas, entre 86,2° y 94,0° | 87,25° a 93,0° con el aro en su sitio; peor con su holgura (E3) |
| 25 piezas más el reloj de pega | Las 25 cuentan el reloj de pega y la frase. Se imprimen 23 |
| Los ficheros del tubo y la plataforma tienen «aristas con más de dos caras» | El del tubo tiene 44 aristas abiertas: 72 mm de costura sin cerrar por dentro. El volumen cuadra |

## 5. Riesgos: no son errores del dibujo, los dirá la probeta

De más a menos.

1. **El engrane va justo y puede acuñarse.** Entre flancos de dientes quedan de 0,07 a 0,09 mm, menos de lo que «sujeta» en pieza impresa. Y al bisel no lo centra nada firme: empujado de lado 0,3 mm, un satélite se queda sin sitio.
2. **El bisel tiene poca ventana en altura:** si queda 0,3 mm bajo, se sienta sobre los puentes; si queda 0,4 alto, roza el cuerpo. Depende de tres pilas de piezas de unos 100 mm.
3. **El tetón suelto puede inclinarse** 6° con sus holguras, y a 9,5° se acuña entre el marco y el plato.
4. **El cuerpo no tiene rampa de entrada ni forma de quitarlo.** Los pestillos son escalones a 90° y la junta con la base queda enrasada: no hay dónde hacer palanca. Si no sale sin romper, no se puede abrir nada de dentro. Y cogiendo la caja por el cuerpo, todo lo demás cuelga de esos cuatro pestillos.
5. **El plato se pone a ciegas:** solo asienta si el tetón está a ±0,2 mm de su sitio, y al cerrar las puertas a mano el aro se pasa 0,7°.
6. **Techos en puente** de 17 a 24 mm en la meseta, sobre las ventanas del aro, con el aro pasando a 0,6 mm por debajo.
7. **La bola de cada puerta nace casi en el aire** al imprimirse. Son pocos mm², pero es la bola que corre con 0,15 de holgura.
8. **Arriba, el pedestal queda a 0,01 o 0,02 mm** del marco con los juegos de la plataforma, y la plataforma descansa 0,25 mm por debajo del ras, no a ras.
9. **Entre dos ranuras del tubo queda una pared de 1,8 mm,** no los 3,7 que dice la fase 1, que supone los tetones a 120° exactos.
10. **Cerradas y boca abajo, las puertas se descuelgan más de lo dicho:** las dos a la vez, 1,8 a 2,0 mm en la punta; el reporte dice 1,5.

El detalle y las cifras de cada uno, en los `HALLAZGOS.md` de [`calculos-mac/revision-caja/`](calculos-mac/revision-caja/).

## 6. Lo comprobado y bien

- **El programa del PC, ejecutado aquí, da lo mismo que subió.**
- **Ninguna pieza pisa a otra** en todo el recorrido, tampoco afinando mucho más: plataforma en 819 posiciones, puertas de 0,25 en 0,25 grados, engrane de 0,05 en 0,05.
- **Los topes paran el tubo** en 0° y 345° exactos, y actúan antes de que los tetones lleguen al final de su ranura.
- **Los seis satélites engranan y quedan retenidos** boca abajo en cualquier giro, estén o no bajo un puente.
- **La plataforma no se cae ni se sube sola** más de 0,3 mm en ningún giro.
- **Plataforma, tubo, marco, rueda central y plato solo entran en una posición.**
- **Todas las piezas caben** en la impresora, son de un solo trozo y ninguna empieza en el aire.
- **Los diez imanes** van en pareja, caben y están a 34 mm o más de la cabeza del reloj.
- **Siete de los nueve ficheros de imprimir** son, pieza a pieza, las del modelo, y vienen bien orientados salvo el tetón con pomo.
- **Las medidas generales,** el recorrido, los giros y la tabla de piezas del reporte coinciden.

## 7. Mi parte

- **El brief se contradecía:** pedí «soporte suelto» y «boca abajo no se cae nada» (P5).
- **Mi estimación de 150 mm de lado estaba mal:** no conté el sitio de las bisagras ni de lo que mueve las puertas. Salen 178,8.
- **Pedí comprobar «que ninguna pieza pisa a otra»** y no pedí comprobar que quedaran con holgura de imprimir. Por eso E2 pasó todas las pruebas.

## 8. Qué propongo (decide Pepe)

1. **No imprimir todavía,** tampoco la probeta de las puertas: E1, E3, E4, E6 y E7 están en ella, y el tetón con pomo viene del revés.
2. **Que la sesión del PC corrija E1 a E8, el programa (apartado 3) y el reporte (apartado 4).** Cómo arreglar cada cosa lo decide ella, que es quien conoce el modelo. Lo que yo haría, por si ayuda, está en el relevo.
3. **Tú decides dos cosas:** si las zanjas de delante y detrás del reloj (E9) te importan, y si el soporte tiene que quedar sujeto con la caja boca abajo (P5).
4. **Después de cada arreglo, se ejecuta `revisar_caja_v5.py`.** Cuando no dé ningún fallo, se imprime la probeta de las puertas. Ese programa tarda dos minutos y funciona también en el PC. Hoy da 15 líneas en FALLA. Dos de ellas son las de E9 y P5: si decides que no te importan, se quitan del programa y se apunta por qué.
