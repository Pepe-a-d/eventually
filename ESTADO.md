# Estado del proyecto

Puesto al día el **20 de noviembre de 2026** por la sesión del PC. Cuando cambie algo, se cambia aquí y se pone la fecha. Lo que cada cosa significa y por qué se decidió está en [DECISIONES.md](DECISIONES.md).

Cada dato dice de dónde sale: **decidido** (lo eligió Pepe), **medido** (sobre una pieza), **del modelo**, **calculado**, **estimado** o **supuesto**.

## 1. Activo

| Qué | Dónde | En qué punto está |
| --- | --- | --- |
| **Caja v5: iris y ascensor** | `caja/BRIEF-v5.md` | Diseño decidido por Pepe. Nada modelado ni impreso |
| **Probeta 1: el iris** | `caja/BRIEF-v5.md`, apartado 11 | Encargada a la sesión del PC. Forma acordada con Pepe: una carcasa de 8 láminas y dos juegos de láminas, de 1,2 y de 0,8 mm (D-23). **Sin modelar** |
| Resultados de las probetas | `caja/resultados-probetas.md` | P0 bien. P1 no vale |
| La web | `docs/` | Publicada. Falta probarla en un iPhone |
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

Cada milímetro de hueco cuesta unos 1,7 mm de diámetro de carcasa (calculado en plano, sin CAD).

## 6. Preguntas a Pepe sin contestar

1. ¿Qué día se entrega? El brief dice «más de un mes desde el 20 de noviembre».
2. ¿Está montado el reloj? Si lo está, faltan sus medidas.
3. ¿Valen los textos del tutorial de la caja y los de la puerta al reloj («Esto sigue. Luego.», «Ya lo tengo»)?
4. ¿Puede cada sesión subir su trabajo al terminar sin pedírselo? Hoy la regla es que no (ver `COMO-TRABAJAMOS.md`, apartado 6).

## 7. Lo siguiente

1. Modelar la probeta del iris y dejar los `.3mf` en `caja/probetas-v5/`. Sesión del PC.
2. Que Pepe la imprima y la pruebe con la tabla «vale si».
3. Después, por este orden: probeta del ascensor, probeta del planetario y la caja entera.
4. Rehacer el tutorial de la web cuando la v5 tenga forma.
