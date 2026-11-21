# Estado del proyecto

Puesto al día el **21 de noviembre de 2026, 08:05,** por la sesión del Mac (antes, a la 01:05, por la del PC). Cuando cambie algo, se cambia aquí y se pone la fecha. Lo que cada cosa significa y por qué se decidió está en [DECISIONES.md](DECISIONES.md).

Cada dato dice de dónde sale: **decidido** (lo eligió Pepe), **medido** (sobre una pieza), **del modelo**, **calculado**, **estimado** o **supuesto**.

## 1. Activo

| Qué | Dónde | En qué punto está |
| --- | --- | --- |
| **Caja v5: iris y ascensor** | `caja/BRIEF-v5.md` | Diseño decidido por Pepe. Solo está modelada la probeta del iris. Nada impreso |
| **Probeta 1: el iris** | `caja/reporte-v5/probeta-iris.md`, `caja/probetas-v5/` | **Modelada el 21-nov, sin imprimir.** Una carcasa de 8 láminas y dos juegos, de 1,2 y de 0,8 mm (D-23). Cumple todo el encargo en el modelo menos el diámetro: **133,5 mm, y el objetivo eran 130. Pepe lo acepta: el resto de la caja se adapta a 133,5** (D-27). **Revisada por la sesión del Mac el 21-nov** (`caja/reporte-v5/contra-reporte-iris.md`): las medidas cuadran, pero calcula que no cerrará del todo con láminas de 1,2 ni de 0,8 mm (estimado; lo dirá la pieza). **Pepe añade un tercer juego de láminas de 0,4 mm (D-28): sin modelar, lo hace la sesión del PC.** Falta que Pepe la imprima |
| Resultados de las probetas | `caja/resultados-probetas.md` | P0 bien. P1 no vale |
| La web | `docs/` | Publicada en su dirección de siempre; GitHub Pages sirve `/docs` desde el 21-nov (D-26). Falta probarla en un iPhone |
| Tutorial de la caja en la web | `docs/frames/caja/`, `docs/caja.js`, `docs/caja.css` | Publicado, pero **describe la v4.1**. Hay que rehacerlo con la v5 |
| Tarjeta de autenticidad | `tarjeta/` | Terminada. Sin imprimir, que conste |
| QR | `qr/` | Terminado y comprobado |

## 2. Parado

| Qué | Dónde | Por qué |
| --- | --- | --- |
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

## 4. Lo que se aprovecha de la v4

Los contornos de la frase (`caja/historico/frase-v3.json`), la funda de campana con colchón de aire, la pinza en C y la peana, el rebaje del NFC, las holguras de P0 y la forma de trabajar con un generador en Python.

## 5. Supuestos que siguen sin medir

| Qué | Valor | Nota |
| --- | --- | --- |
| Cabeza del reloj | 40 mm, 43,5 con corona, 11 de grueso | Supuesto. No consta que el reloj esté montado |
| Brazalete cerrado | Óvalo de unos 67 × 53 mm | Supuesto |
| Hueco libre del iris | 75 mm | Estimado a partir de los dos anteriores |
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
3. Que la sesión del PC modele el tercer juego de láminas, de 0,4 mm (D-28). Mientras, Pepe puede imprimir las cinco bandejas que ya hay.
4. Que Pepe la imprima y la pruebe con la tabla «vale si» del reporte y los añadidos del apartado 5 de la revisión. **Sin forzar.** El resultado va a `caja/resultados-probetas.md`.
5. Después, por este orden: probeta del ascensor, probeta del planetario y la caja entera.
6. Rehacer el tutorial de la web cuando la v5 tenga forma.
