# Estado del proyecto

Puesto al día el **26 de noviembre de 2026, 19:36,** por la sesión del PC (antes, el 25 a las 13:25, por la misma). Cuando cambie algo, se cambia aquí y se pone la fecha. Lo que cada cosa significa y por qué se decidió está en [DECISIONES.md](DECISIONES.md).

Cada dato dice de dónde sale: **decidido** (lo eligió Pepe), **medido** (sobre una pieza), **del modelo**, **calculado**, **estimado** o **supuesto**.

## 1. Activo

| Qué | Dónde | En qué punto está |
| --- | --- | --- |
| **Caja v5: puertas y ascensor** | `caja/BRIEF-v5.md` | **Cambio del 21-nov (D-29): caja cuadrada; la tapa son dos puertas con bisagra, a izquierda y derecha, que se abren solas mientras el reloj sube. Se mantienen el bisel redondo, los engranajes a la vista, el satélite azul y el ascensor.** El iris se deja. **Brief nuevo, completo, del 21-nov.** **Cambio del 24-nov (D-34), en su apartado 13: con el reloj arriba, el suelo de alrededor queda liso y hundido 5 mm (se acaban las zanjas), y el soporte va sujeto por la forma de las piezas mientras la caja no esté abierta del todo. Modelado el 25-nov** |
| **La caja entera en Fusion** | `caja/reporte-v5/caja-entera.md`, `caja/Eventually-caja-v5.f3d` | **Modelada el 21-nov, revisada por la sesión del Mac el 22 (9 errores en las piezas), corregida por la del PC el 24 (D-33), cambiada el 25 con lo decidido en D-34 y D-35, y revisada entera ese mismo día (D-36). Nada impreso.** Tres programas la comprueban y los tres dan cero fallos: los dos de la sesión del PC, el de la revisión de la sesión del Mac (`caja/reporte-v5/calculos-mac/revisar_caja_v5.py`) y la auditoría nueva (`caja/caja_auditoria_v5.py`: montaje pieza a pieza, impresión capa a capa y holguras). **Lo del 25-nov (del modelo):** arriba, el pedestal queda a ras del asiento de las puertas, 5 mm bajo la tapa; el ascensor sube 81,1 mm y la caja mide 115,7 de alto (178,8 de lado, igual). **El soporte es un cojín ovalado al que el reloj va abrochado** (D-35), sobre un pie de 42 × 50 mm que entra en un cajeado del pedestal; lo cogen dos pestillos que dos columnas de la base mantienen metidos con la plataforma abajo; cerrada, no se mueve más de 0,3 mm; con la caja abierta está libre. Son 25 piezas. La revisión corrigió once cosas (apartado 0.3 del reporte): las más serias, que los pestillos no se podían montar y que los dientes engranaban demasiado justos. **Lo que no cumple o no está demostrado:** las medidas del reloj y del brazalete son supuestas, y el cojín sale de ellas; que el soporte no vuelque en la mesilla está solo calculado (17° a 21° hacia delante); si el soporte se queda atascado a medio entrar (1,6 mm alto o más), la caja cierra con él sin sujetar (reporte, 2.4). **Pepe no ha dicho todavía si le gustan el suelo hundido y el soporte nuevo** (dibujos `caja/reporte-v5/caja-reloj-arriba.png` y `caja-soporte.png`). **Falta la revisión a fondo de la sesión del Mac.** El vídeo `caja/video-v5/` es del modelo del 21-nov |
| Probetas de la caja v5 | `caja/probetas-v5/caja-probeta-*.3mf` | Tres, sacadas del modelo: puertas, ascensor y planetario. **Rehechas el 25-nov con el modelo revisado; la del ascensor lleva ahora el soporte y los pestillos. Las escribe `caja/caja_probetas_v5.py`, sin Fusion, con mallas cerradas. Sin imprimir y sin abrir en Bambu Studio.** Entre las tres son casi toda la caja: qué se imprime lo decide Pepe (reporte, apartado 9; D-15 sigue en pie) |
| **Carpeta de pruebas, con guía** | `caja/pruebas-v5/` | **Nueva, del 26-nov, pedida por Pepe.** Las mismas diez bandejas de `probetas-v5/` (son copias idénticas), numeradas en el orden de imprimir, y una guía con dibujos (`GUIA.md` y `00-GUIA-DE-PRUEBAS.pdf`, 19 páginas): ajustes propuestos, cómo tiene que verse cada bandeja, el montaje paso a paso de las tres pruebas y qué probar en cada una. Cada paso de montaje de la guía está comprobado en el modelo. **Nada impreso todavía; sin abrir en Bambu Studio.** Pepe no ha dicho aún si imprime |
| **Ficheros de imprimir de toda la caja** | `caja/imprimir-v5/` | **Nuevos, del 25-nov (D-36):** doce bandejas con las 25 piezas ya orientadas, y una guía (`LEEME.md`) con colores, ajustes propuestos y avisos. **Sin abrir en Bambu Studio y sin laminar.** Valen para el reloj supuesto: si las medidas de verdad son otras, se regeneran. D-15 sigue en pie: la caja entera no se imprime sin medir el reloj |
| Probeta 1: el iris (cerrada) | `caja/reporte-v5/probeta-iris.md`, `caja/probetas-v5/` | **Modelada el 21-nov, sin imprimir.** Una carcasa de 8 láminas y dos juegos, de 1,2 y de 0,8 mm (D-23). Cumple todo el encargo en el modelo menos el diámetro: **133,5 mm, y el objetivo eran 130. Pepe lo acepta: el resto de la caja se adapta a 133,5** (D-27). **Revisada por la sesión del Mac el 21-nov** (`caja/reporte-v5/contra-reporte-iris.md`): las medidas cuadran, pero calcula que no cerrará del todo con láminas de 1,2 ni de 0,8 mm (estimado; lo dirá la pieza). **Tercer juego de láminas, de 0,4 mm (D-28): modelado el 21-nov a las 08:15.** **IMPRESA Y PROBADA por Pepe el 21-nov: funciona con los tres gruesos** (al revés de lo que se calculó). **Pero Pepe cree que no va a alcanzar la calidad que busca y va a valorar opciones con la sesión del Mac. El iris queda en el aire.** Detalle en `caja/resultados-probetas.md`. **Lo que no le llega (dicho a la sesión del Mac a las 15:10): cómo se ve cerrado y que parece frágil.** El tacto y el acabado no. La sesión del Mac le presentó cuatro alternativas y **Pepe eligió otra, suya: puertas en caja cuadrada (D-29)** |
| Resultados de las probetas | `caja/resultados-probetas.md` | P0 bien. P1 no vale. **Iris: funciona con los tres gruesos, pero a Pepe no le convence la calidad** (21-nov, dicho por Pepe, sin cifras) |
| La web | `docs/` | Publicada en su dirección de siempre; GitHub Pages sirve `/docs` desde el 21-nov (D-26). Falta probarla en un iPhone |
| Tutorial de la caja en la web | `docs/frames/caja/`, `docs/caja.js`, `docs/caja.css` | Publicado, pero **describe la v4.1**. Hay que rehacerlo con la v5 |
| Tarjeta de autenticidad | `tarjeta/` | Terminada. Sin imprimir, que conste |
| QR | `qr/` | Terminado y comprobado |

## 2. Parado

| Qué | Dónde | Por qué |
| --- | --- | --- |
| Brief del iris | `caja/historico/BRIEF-v5-iris.md` | Pepe cambió el iris por puertas (D-29). Se guarda porque el reporte de la probeta del iris responde a su apartado 11 |
| Caja v4 y parche v4.1 | `caja/historico/` | La probeta P1 falló: los imanes no mueven el mecanismo (D-19) |
| Segundo parche de la v4.1 | `caja/historico/contra-reporte-v4.1.md`, apartado 7 | Era para la v4.1. No se hace |
| Vídeo explicativo de la v4.1 | `caja/historico/video-v4.1/` | Enseña una caja que ya no se va a hacer |

## 3. Descartado: no volver a proponerlo

Lista de `caja/BRIEF-v5.md`, apartado 0.

- La aguja como llave, y la aguja en general.
- Cualquier mecanismo que dependa de imanes.
- El trinquete.
- Números o grabados en el iris.
- La tarjeta bajo el reloj: no cabe por el hueco.
- Una corona en el costado y una cara plana en el cilindro como marca del frente.
- Engranajes escondidos del todo, o del todo a la vista.
- Girar la base en vez del bisel.
- El reloj tumbado.
- Engranajes que giran en su sitio: los satélites tienen que orbitar.
- De antes: palabras en la tapa, piezas de acero, pestaña de arrancar.
- De la probeta del iris: la variante de 6 láminas (D-23).
- De la tapa (D-29): el iris de láminas, para la caja.

## 4. Lo que se aprovecha de la v4

Los contornos de la frase (`caja/historico/frase-v3.json`), la funda de campana con colchón de aire, el rebaje del NFC, las holguras de P0 y la forma de trabajar con un generador en Python. La pinza en C y la peana ya no: el soporte es otro (D-35).

## 5. Supuestos que siguen sin medir

| Qué | Valor | Nota |
| --- | --- | --- |
| Cabeza del reloj | 40 mm, 43,5 con corona, 11 de grueso | Supuesto. No consta que el reloj esté montado |
| Brazalete cerrado | Óvalo de unos 67 × 53 mm | Supuesto |
| Hueco libre de las puertas | 50 × 59 mm | Estimado a partir de los dos anteriores, con 3 mm por lado (antes, un círculo de 75 para el iris) |
| Holguras de las piezas que giran en el iris | 0,25 mm por lado | Supuesto. Sin probar a capa de 0,2 mm |
| Las láminas del iris se doblan lo bastante al cerrar | 1,1 mm en la punta la de 1,2; 0,7 la de 0,8 | Calculado. Lo dirá la probeta |

Cada milímetro de hueco cuesta unos 1,7 mm de diámetro de carcasa (calculado en plano con el modelo simple de antes de D-27; sin rehacer con el modelo de ahora).

## 6. Preguntas a Pepe sin contestar

1. ¿Qué día se entrega? El brief dice «más de un mes desde el 20 de noviembre».
2. ¿Está montado el reloj? Si lo está, faltan sus medidas.
3. ¿Valen los textos del tutorial de la caja y los de la puerta al reloj («Esto sigue. Luego.», «Ya lo tengo»)?
4. P0 repetida a 0,2 mm: Pepe mandó una foto el 21-nov y están leídos los valores (5,20 · 0,15 · 0,20, en `caja/resultados-probetas.md`). Pepe confirmó la lectura. Falta saber qué piel tapa el imán a 0,2 mm (la fila de abajo no tiene marca).

## 7. Lo siguiente

1. ~~Modelar la probeta del iris.~~ Hecho el 21-nov: `caja/probetas-v5/` y `caja/reporte-v5/probeta-iris.md`.
2. ~~Que la sesión del Mac revise el reporte.~~ Hecho el 21-nov: `caja/reporte-v5/contra-reporte-iris.md`. El diámetro ya está decidido: 133,5 mm, y el resto de la caja se adapta (D-27). **Ojo al brief:** donde `caja/BRIEF-v5.md` cuente con 130 mm de iris, ahora son 133,5. La sesión del Mac lo rehará cuando la probeta diga qué iris vale, porque puede cambiar otra vez.
3. ~~Que la sesión del PC modele el tercer juego de láminas, de 0,4 mm (D-28).~~ Hecho el 21-nov: `caja/probetas-v5/iris-laminas-0.4mm-x8.3mf`. Las cinco bandejas anteriores no han cambiado.
4. ~~Que Pepe la imprima y la pruebe.~~ Hecho el 21-nov: funciona con los tres gruesos (`caja/resultados-probetas.md`). A Pepe no le convenció cómo se ve cerrado y le pareció frágil. **Decidió cambiar el iris por dos puertas, en caja cuadrada (D-29).**
5. ~~Que la sesión del PC modele la caja entera, la compruebe en el modelo y haga el reporte.~~ Hecho el 21-nov: `caja/reporte-v5/caja-entera.md`.
6. ~~Que la sesión del Mac revise el reporte.~~ Hecho el 22-nov. ~~Que la sesión del PC corrija.~~ Hecho el 24-nov (D-33). ~~Que Pepe decida las zanjas y el soporte boca abajo.~~ Decidido el 24-nov (D-34). ~~Que la sesión del PC modele lo de D-34.~~ Hecho el 25-nov, y además el soporte nuevo (D-35) y una revisión entera (D-36). **Ahora: que Pepe mire los dos dibujos, y que la sesión del Mac haga su revisión a fondo.**
7. Imprimir las probetas, sacadas del modelo: puertas, ascensor y planetario. Los ficheros están hechos. La sesión del PC propone empezar solo por la de puertas; **Pepe no ha dicho todavía cuál.**
8. Medir el reloj y poner sus medidas en el modelo. Sin eso no se imprime la caja completa (D-15).
9. Rehacer el tutorial de la web cuando la v5 tenga forma.
