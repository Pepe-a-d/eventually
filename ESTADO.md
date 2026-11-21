# Estado del proyecto

Puesto al día el **21 de noviembre de 2026, 19:02,** por la sesión del PC (antes, a las 15:20, por la del Mac). Cuando cambie algo, se cambia aquí y se pone la fecha. Lo que cada cosa significa y por qué se decidió está en [DECISIONES.md](DECISIONES.md).

Cada dato dice de dónde sale: **decidido** (lo eligió Pepe), **medido** (sobre una pieza), **del modelo**, **calculado**, **estimado** o **supuesto**.

## 1. Activo

| Qué | Dónde | En qué punto está |
| --- | --- | --- |
| **Caja v5: puertas y ascensor** | `caja/BRIEF-v5.md` | **Cambio del 21-nov (D-29): caja cuadrada; la tapa son dos puertas con bisagra, a izquierda y derecha, que se abren solas mientras el reloj sube. Se mantienen el bisel redondo, los engranajes a la vista, el satélite azul y el ascensor.** El iris se deja. **Brief nuevo, completo, del 21-nov.** Nada de lo nuevo está modelado |
| **La caja entera en Fusion** | `caja/reporte-v5/caja-entera.md`, `caja/Eventually-caja-v5.f3d` | **Modelada entera por la sesión del PC el 21-nov: 25 piezas, en el programa y en Fusion. Nada impreso.** En el modelo, de tope a tope y de 2 en 2 grados, ninguna pieza pisa a otra y el reloj de pega queda a 3,00 mm o más de todo (del modelo). Las puertas las mueve un aro escondido que gira 11°. **Mide 178,8 × 178,8 × 122,6 mm** (183,8 × 126 con funda): **a Pepe le vale, tamaño incluido (D-32).** Lo que no cumple el brief, en el apartado 1 del reporte: boca abajo las puertas se descuelgan hasta 1,5 mm; diez imanes en vez de nueve; soporte del reloj provisional. **Falta la revisión de la sesión del Mac;** después, imprimir (D-32). Hay una animación del modelo en `caja/video-v5/` |
| Probetas de la caja v5 | `caja/probetas-v5/caja-probeta-*.3mf` | Tres, sacadas del modelo: puertas, ascensor y planetario. **Sin imprimir.** Entre las tres son casi toda la caja: qué se imprime lo decide Pepe (reporte, apartado 9; D-15 sigue en pie) |
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

Los contornos de la frase (`caja/historico/frase-v3.json`), la funda de campana con colchón de aire, la pinza en C y la peana, el rebaje del NFC, las holguras de P0 y la forma de trabajar con un generador en Python.

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
6. **Que la sesión del Mac revise el reporte.** A Pepe ya le vale la caja, tamaño incluido (D-32, 21-nov).
7. Imprimir las probetas, sacadas del modelo: puertas, ascensor y planetario. Los ficheros están hechos. La sesión del PC propone empezar solo por la de puertas; **Pepe no ha dicho todavía cuál.**
8. Medir el reloj y poner sus medidas en el modelo. Sin eso no se imprime la caja completa (D-15).
9. Rehacer el tutorial de la web cuando la v5 tenga forma.
