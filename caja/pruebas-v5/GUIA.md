# Eventually · Guía de pruebas de la caja v5

Escrita el 26 de noviembre de 2026 por la sesión del PC. Es la misma guía que `00-GUIA-DE-PRUEBAS.pdf`, que está en esta carpeta.

Esta carpeta sirve para **probar la caja por partes antes de imprimirla entera**. Son diez bandejas, numeradas en el orden en que conviene imprimirlas, y tres pruebas:

| Prueba | Qué contesta | Bandejas |
| --- | --- | --- |
| **1. Las puertas** | ¿Te gusta cómo se ve cerrada y te parece sólida? | 01 y 02 |
| **2. El ascensor** | ¿Sube y baja el reloj, y el soporte queda sujeto abajo y suelto arriba? | 03, 04, 05 y 06 |
| **3. Los engranajes** | ¿Girando el bisel pasa todo en su orden: nada, puertas, reloj? | 07, 08, 09 y 10 |

Cada prueba se monta con lo impreso hasta ese momento. **Después de cada una puedes parar:** si la prueba 1 no te convence, te ahorras las otras ocho bandejas.

## 0. Antes de empezar: cuatro avisos

1. **Nada de esto se ha impreso todavía.** En el modelo todo encaja y nada se pisa, y cada paso de montaje de esta guía está comprobado en el modelo. Que funcione de verdad lo dirán las piezas: para eso son las pruebas.
2. **Las medidas del reloj son supuestas.** Si el reloj acaba midiendo otra cosa, estas piezas no valdrán para la caja definitiva y habrá que repetirlas. Para decidir si las puertas te gustan (prueba 1) da igual. Para las pruebas 2 y 3, que entre las dos son casi toda la caja, **te ahorras plástico si mides antes el reloj** (las cinco medidas que te pedí). Tú decides el orden; la decisión D-15 (no imprimir la caja entera sin medir el reloj) sigue en pie.
3. **No he abierto estos ficheros en Bambu Studio.** Los he comprobado con un programa (las mallas son cerradas, apoyan en la cama y caben en la bandeja), pero el laminado no está probado. Si Bambu Studio dice algo raro al abrir alguno, para y dímelo.
4. **Los ajustes de impresión son los que propongo, sin probar en esta caja.** Las horas y los gramos de cada bandeja no los sé: te los dirá el laminador.

**Qué necesitas:** la impresora (Bambu Lab X1 Carbon), PLA (un solo color vale para todo; si usas el blanco y luego el reloj mide lo supuesto, las piezas sirven para la caja de verdad), un trozo de cartón de 50 × 59 mm, algo que pese unos 150 g y se pueda colgar (o el reloj), y un lápiz. **No hace falta pegamento, ni tornillos, ni imanes.** Todo el plástico de las diez bandejas, si fuera macizo, sería algo más de 1 kg; con el relleno que propongo será bastante menos.

**En los dibujos, los colores solo sirven para distinguir las piezas.** No son los colores de imprimir.

## 1. Cómo imprimir

### 1.1 Abrir un fichero

1. Abre **Bambu Studio** y arrastra el fichero (por ejemplo `01-puertas-bandeja-A.3mf`) a la ventana.
2. Si avisa de que el fichero no es de Bambu Lab y que solo va a cargar la geometría, acepta: es lo esperado.
3. Si pregunta si quieres cargarlo como un solo objeto con varias partes, di que **no**: así cada pieza queda suelta.
4. Mira que las piezas estén **tumbadas como en el dibujo de la bandeja** (apartado 1.3). Ya vienen orientadas: **no las gires ni las voltees.** Si alguna se sale de la bandeja o se montan unas sobre otras, usa el botón de ordenar la bandeja; eso las mueve pero no las voltea.
5. Pon los ajustes del apartado 1.2, lamina y, antes de imprimir, mira en la vista previa que **no haya puesto soportes**.

### 1.2 Ajustes (los mismos para todas)

| Qué | Valor | Por qué |
| --- | --- | --- |
| Material | PLA | El de las probetas anteriores |
| Boquilla y altura de capa | 0,4 mm y **0,2 mm** | Las holguras del modelo están medidas con probetas a 0,2 |
| Soportes | **Ninguno** | Todas las piezas están pensadas para salir sin soportes. Dentro de las ranuras estorbarían |
| Compensación del «pie de elefante» | Activada | Varias piezas encajan justo por la cara que toca la cama |
| Paredes | 3 | Estimado |
| Relleno | **15 %**, menos en las bandejas **01, 04 y 08**, que van **al 100 %** | Llevan las piezas pequeñas o que trabajan (puertas, pasadores, soporte, pestillos, satélites) |

### 1.3 Las diez bandejas, en orden

| Así tiene que verse | Qué es |
| --- | --- |
| <img src="figuras/bandeja-01.jpg" width="330"> | **`01-puertas-bandeja-A.3mf`** · relleno **100 %** · 22 mm de alto<br>Marco, las dos puertas, los dos pasadores y el tetón con pomo.<br>Las puertas van boca abajo: la cara que toca la cama es la que se verá. Los pasadores van tumbados sobre su cara plana. |
| <img src="figuras/bandeja-02.jpg" width="330"> | **`02-puertas-bandeja-B.3mf`** · relleno 15 % · 11 mm de alto<br>Meseta, aro de las puertas y anillo.<br>La meseta tiene techos «en puente» de 10 a 12 mm: es normal que el laminador los marque. **Con esta ya puedes hacer la prueba 1.** |
| <img src="figuras/bandeja-03.jpg" width="330"> | **`03-ascensor-plataforma.3mf`** · relleno 15 % · 25 mm de alto<br>La plataforma con su pedestal. |
| <img src="figuras/bandeja-04.jpg" width="330"> | **`04-ascensor-soporte-y-pestillos.3mf`** · relleno **100 %** · 42 mm de alto<br>El soporte del reloj, **tumbado sobre un costado** (así el cojín sale sin soportes), y los dos pestillos. |
| <img src="figuras/bandeja-05.jpg" width="330"> | **`05-ascensor-base.3mf`** · relleno 15 % · 96 mm de alto<br>La base con sus tres columnas. Es alta y las columnas son finas: imprímela con la puerta de la impresora cerrada. |
| <img src="figuras/bandeja-06.jpg" width="330"> | **`06-ascensor-tubo.3mf`** · relleno 15 % · 99 mm de alto<br>El tubo. Las tres ranuras de dentro tienen forma de V para salir sin soportes. **Con esta ya puedes hacer la prueba 2.** |
| <img src="figuras/bandeja-07.jpg" width="330"> | **`07-planetario-plato.3mf`** · relleno 15 % · 11 mm de alto<br>El plato. La espiral va contra la cama. |
| <img src="figuras/bandeja-08.jpg" width="330"> | **`08-planetario-satelites-y-teton.3mf`** · relleno **100 %** · 9 mm de alto<br>Los seis satélites y el tetón normal (sin pomo). En la caja de verdad uno de los satélites es azul; para la prueba da igual. |
| <img src="figuras/bandeja-09.jpg" width="330"> | **`09-planetario-rueda-central.3mf`** · relleno 15 % · 9 mm de alto<br>La rueda central, boca abajo. |
| <img src="figuras/bandeja-10.jpg" width="330"> | **`10-planetario-bisel.3mf`** · relleno 15 % · 14 mm de alto<br>El bisel, boca abajo: la cara que toca la cama es la que se verá. **Con esta ya puedes hacer la prueba 3.** |

## 2. Prueba 1: las puertas (bandejas 01 y 02)

Es la que decide si este diseño te convence. Se monta sobre la mesa, sin el resto de la caja.

<img src="figuras/p1-piezas.jpg" width="515">

El **anillo** y el **tetón con pomo** solo existen para esta prueba: el anillo hace de rueda central y el pomo sirve para abrir y cerrar con el dedo.

### 2.1 Montaje

Pon el marco en la mesa con el lado del hueco (donde irá el brazo del aro) **hacia ti**. Todos los dibujos de esta prueba están vistos desde ese lado.

**Paso 1.** El **aro** sobre el marco, con su brazo en el hueco. Solo cabe así.

<img src="figuras/p1-a.jpg" width="568">

**Paso 2.** La **meseta** sobre el cuello del marco. Entra de dos maneras, a media vuelta una de otra: valen las dos.

<img src="figuras/p1-b.jpg" width="433">

**Paso 3.** Mueve el brazo del aro **a tope hacia la izquierda** (es la posición de «abierto»). Mete cada **puerta de pie**, desde arriba, con la varilla de la bola hacia abajo y la cara lisa (la que tocó la cama) mirando hacia fuera, hasta que la bola entre en su pista del aro. Las dos puertas valen para los dos lados.

<img src="figuras/p1-c.jpg" width="516">

**Paso 4.** Los dos **pasadores**, por el lado, con su **cara plana hacia abajo**, hasta el fondo. Cosen las puertas a la meseta y al marco. Entran igual por delante que por detrás.

<img src="figuras/p1-d.jpg" width="515">

**Paso 5.** Cierra las puertas llevando el brazo **a tope hacia la derecha**. Mete el **tetón con pomo** desde arriba, con el pomo arriba, donde se cruzan la ranura del brazo y la ranura del marco.

<img src="figuras/p1-e.jpg" width="582">

**Paso 6.** El **anillo** encima, alrededor de la meseta, con la cara que tocó la cama hacia arriba. Tapa las puntas de los pasadores para que no se salgan. Si no asienta, gíralo media vuelta.

<img src="figuras/p1-f.jpg" width="390">

### 2.2 Cómo se usa

Empuja el pomo **hacia el centro** (unos 13 mm): las puertas se abren y se quedan de pie. Tira de él hacia fuera y se cierran.

| Cerrada: el pomo, fuera (la flecha dice hacia dónde se empuja) | Abierta: el pomo, 13 mm más adentro |
| --- | --- |
| <img src="figuras/p1-cerrada.jpg" width="300"> | <img src="figuras/p1-abierta.jpg" width="300"> |

### 2.3 Qué probar

| Prueba | Vale si | ¿Qué pasó? |
| --- | --- | --- |
| Abrir y cerrar 20 veces con el pomo | No se engancha | |
| Abierta | Pasa el cartón de 50 × 59 mm | |
| Cerrada, pasando el dedo | No se nota escalón entre las puertas ni con la meseta | |
| Cerrada, a contraluz | No se ve lo de dentro por la raya del centro | |
| Abierta, empujando una puerta con un dedo hacia dentro y hacia fuera | Ni se cierra ni cruje | |
| Boca abajo, sujetando el anillo con los dedos y sacudiendo un poco | No se cae nada. **Apunta cuánto se descuelgan las puertas** (el modelo dice hasta 1,3 mm) | |
| Cerrada, intentando levantar una puerta con la uña | Apunta cuánto se deja | |
| La varilla y la bola de cada puerta, al acabar | No están rotas ni marcadas | |
| ¿Has podido montar algo mal sin darte cuenta? | No | |
| **Lo que decide** | **Que a ti te parezca que cerrada se ve bien y que es sólida** | |

**Si no te convence, para aquí y dímelo.** No imprimas el resto.

## 3. Prueba 2: el ascensor (bandejas 03 a 06)

Son piezas de la caja de verdad: la base, la plataforma, el tubo, el soporte del reloj y sus dos pestillos.

<img src="figuras/p2-piezas.jpg" width="406">

### 3.1 Con las bandejas 03 y 04: pestillos y soporte

Ya se puede probar algo sin esperar a la base y al tubo.

**Paso 1.** Con la plataforma en la mesa, mete cada **pestillo** por el extremo de fuera de su canal, con la **punta en cuña por delante** y la cara ancha (la que tocó la cama) hacia abajo, hasta que haga tope. Son iguales. Al revés no entran.

<img src="figuras/p2-a.jpg" width="650">

**Paso 2.** Abrocha el reloj al cojín del soporte: con el cierre abierto, el brazalete entra por la punta libre del cojín; luego se cierra. Si aún no tienes el reloj, cuelga los 150 g del cojín. Deja caer el **soporte** en el cajeado del pedestal. Solo entra de una manera: si no entra, dale media vuelta.

<img src="figuras/p2-b.jpg" width="476">

| Prueba | Vale si | ¿Qué pasó? |
| --- | --- | --- |
| Mover los pestillos con un dedo en sus canales | Corren sin atascarse y no se salen hacia arriba | |
| Dejar caer el soporte en su cajeado, 10 veces | **Baja hasta el fondo él solo, las 10.** Si alguna se queda a medias, no vale: dímelo. Antes prueba a lijar un poco la cara del soporte que tocó la cama | |
| Sacar el soporte tirando hacia arriba con dos dedos, 10 veces | Sale sin tener que ayudar a los pestillos. Apunta si hay que tirar fuerte | |
| El soporte en la mesa, con el reloj o los 150 g, empujándolo con un dedo | No vuelca con un toque. Apunta hacia dónde vuelca antes | |
| Con el reloj de verdad: abrocharlo y sacudir el soporte | No baila ni se sale. **Si baila, mide cuánto le sobra al brazalete** | |

### 3.2 Con la bandeja 05: la base

**Paso 3.** Saca el soporte. Con los dos pestillos puestos, baja la **plataforma** sobre la base, metiendo sus tres muescas en las tres columnas. Las columnas no están repartidas por igual: **solo entra en una posición.** Los pestillos quedan cogidos entre el disco y las columnas.

<img src="figuras/p2-c.jpg" width="500">

Sin el tubo, la plataforma se sube y se baja con la mano. Ya puedes comprobar lo más importante del soporte: súbela un par de centímetros, mete el soporte y bájala del todo. **Abajo, el soporte no tiene que salir aunque tires; subiéndola otra vez un par de centímetros, sale.**

Ojo: con la plataforma abajo del todo el soporte **no se puede meter** (se queda unos 3 mm alto, apoyado en los pestillos). Es lo previsto: se mete siempre con la plataforma subida.

### 3.3 Con la bandeja 06: el tubo

**Paso 4.** Con la plataforma abajo del todo, baja el **tubo** por fuera de las columnas hasta que sus tres entradas pasen por los tres tetones que la plataforma tiene en el borde. **Solo entra en una posición:** si no baja, gíralo hasta que baje.

<img src="figuras/p2-d.jpg" width="470">

**Paso 5.** Gira el tubo con la mano **en el sentido de las agujas del reloj** (mirando desde arriba). Durante algo más de un cuarto de vuelta la plataforma no se mueve (es el tramo en que, en la caja, se abren las puertas); después sube, hasta el tope, que llega antes de completar la vuelta. Arriba del todo, deja caer el soporte en su cajeado. Al girar, aprieta un poco el tubo contra la base: en la caja lo sujeta lo que lleva encima.

<img src="figuras/p2-e.jpg" width="484">

| Abajo: el soporte, sujeto | Arriba: el soporte sale tirando de él |
| --- | --- |
| <img src="figuras/p2-abajo.jpg" width="300"> | <img src="figuras/p2-arriba.jpg" width="300"> |

| Prueba | Vale si | ¿Qué pasó? |
| --- | --- | --- |
| Subir y bajar 20 veces, con el soporte y el reloj (o 150 g) | No se engancha ni da saltos, y no se nota un punto duro cerca de abajo | |
| A media altura, soltar el tubo | La plataforma no baja sola. **Si baja, no es un fallo de impresión:** habrá que decidir entre menos pendiente o un freno | |
| Arriba y abajo | Hay tope, y un tramo en que girar no sube ni baja | |
| Mirando la plataforma al subir | No cabecea a la vista | |
| Abajo del todo, tirar del soporte hacia arriba y sacudir todo boca abajo | No sale y no se nota suelto. Apunta si suena | |
| Arriba del todo, sacar el soporte con dos dedos, 10 veces | Sale sin soltar nada | |
| A media altura, poner el soporte | Entra igual que arriba | |
| Bajar sin el soporte, sacudir y volver a subir | Los pestillos siguen en su sitio y el soporte vuelve a entrar | |
| Las puntas de los pestillos, al acabar | No están mordidas | |

## 4. Prueba 3: los engranajes (bandejas 07 a 10)

Se monta **encima de las otras dos pruebas.** Juntas son la caja entera menos el cuerpo y la funda.

<img src="figuras/p3-piezas.jpg" width="427">

### 4.1 Montaje

Antes de empezar: deja el ascensor **abajo del todo**, con el tubo girado hasta su tope y el soporte dentro. De la prueba 1, **quita el anillo y el tetón con pomo** (ya no hacen falta) y deja las puertas **cerradas**.

**Paso 1.** Baja las puertas, todo en un bloque, sobre las **tres columnas**. Las tres cajas del marco solo coinciden con las columnas en una posición.

<img src="figuras/p3-a.jpg" width="436">

**Paso 2.** El **tetón** normal, desde arriba, donde se cruzan la ranura del brazo del aro y la del marco (el mismo sitio donde iba el del pomo).

<img src="figuras/p3-b.jpg" width="406">

**Paso 3.** El **plato** sobre el tubo, con la espiral hacia abajo. Tiene tres almenas desiguales: solo asienta en una posición. **Es el paso más a ciegas:** la espiral tiene que encontrar el tetón. Si el plato no asienta, mira que las puertas estén cerradas del todo, el tubo en su tope y el tetón en su sitio.

<img src="figuras/p3-c.jpg" width="484">

**Paso 4.** Los **seis satélites**, cada uno en su eje del plato. Da igual qué cara va arriba.

<img src="figuras/p3-d.jpg" width="498">

**Paso 5.** La **rueda central** sobre la meseta, con la cara que tocó la cama hacia arriba. Solo baja en una posición: gírala hasta que asiente. Sus dientes tienen que entrar entre los de los satélites.

<img src="figuras/p3-e.jpg" width="399">

**Paso 6.** El **bisel** encima, con la cara que tocó la cama hacia arriba. Se apoya en el plato. Sin el cuerpo de la caja se puede levantar con la mano: es normal.

<img src="figuras/p3-f.jpg" width="534">

### 4.2 Cómo se usa

Gira el bisel **en el sentido de las agujas del reloj** (mirando desde arriba). Tiene que pasar esto, en este orden:

1. Durante casi un cuarto de vuelta, **nada**: solo giran los engranajes.
2. Hasta la media vuelta, **se abren las puertas**.
3. Desde ahí hasta el tope (algo más de vuelta y media en total), **sube el reloj**.

Girando al revés, lo mismo hacia atrás: baja el reloj, se cierran las puertas.

| Cerrada | Puertas abiertas | Reloj arriba |
| --- | --- | --- |
| <img src="figuras/p3-cerrada.jpg" width="205"> | <img src="figuras/p3-puertas.jpg" width="205"> | <img src="figuras/p3-arriba.jpg" width="205"> |

### 4.3 Qué probar

| Prueba | Vale si | ¿Qué pasó? |
| --- | --- | --- |
| Girar el bisel de tope a tope, cinco veces en cada sentido | Suave, sin puntos duros ni saltos de diente | |
| Mientras giras | Pasa todo en su orden: nada, puertas, reloj | |
| Cambiar de sentido | El bisel no gira «en vacío» más de lo que te parezca aceptable. Apunta cuánto | |
| Mirando los satélites | Giran alrededor del centro, no se montan unos dientes en otros y no se levantan de sus ejes | |
| Los dientes, al acabar | Ninguno roto ni mordido | |
| **Lo que decide** | **Que abrir la caja girando el bisel te guste: el tacto, las vueltas, lo que se ve** | |

## 5. Qué hacer con los resultados

Después de cada prueba, cuéntamelo en el chat **con tus palabras**; una foto ayuda mucho. Yo lo apunto en `caja/resultados-probetas.md` del repositorio, con la fecha, y corrijo lo que haga falta. No hace falta que rellenes las tablas enteras: lo que no funcione y lo que no te guste es lo que más importa.

Y si en algún momento algo no entra, **no lo fuerces:** casi todas las piezas solo entran de una manera, y lo normal es que esté girada. Si girándola tampoco entra, es un fallo del modelo o de la impresión, y eso es justo lo que la prueba tiene que encontrar.

## 6. Lo que esta guía no cubre

- **El cuerpo y la funda** de la caja no están en estas pruebas. Están en `caja/imprimir-v5/`, con su propia guía (`LEEME.md`), para cuando el reloj esté medido.
- **Los imanes** (son de adorno: la caja funciona igual sin ellos).
- La sesión del Mac todavía no ha revisado este modelo.
