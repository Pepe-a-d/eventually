# Imprimir la caja v5: todas las piezas, bandeja a bandeja

Escrito el 25 de noviembre de 2026 por la sesión del PC. Los ficheros los escribe `../caja_probetas_v5.py` directamente desde el modelo; no pasan por Fusion.

**Antes de imprimir nada, lee esto:**

- **Las medidas del reloj son supuestas.** La caja entera sale de ellas. Si el reloj de verdad mide otra cosa, estos ficheros no valen: se cambian las medidas arriba de `../caja_diseno_v5.py` y se vuelven a escribir (`python3 caja_diseno_v5.py`, `python3 caja_piezas_v5.py`, `python3 caja_probetas_v5.py`). La decisión D-15 sigue en pie: no se imprime la caja entera sin medir antes el reloj.
- **Ninguna pieza de esta caja se ha impreso todavía.** En el modelo todo encaja y nada se pisa; que funcione lo dirán las piezas. Lo prudente sigue siendo empezar por la probeta de las puertas (`../probetas-v5/`).
- **No he abierto estos ficheros en Bambu Studio.** Sí los he vuelto a abrir con un programa, uno a uno: las 26 mallas son cerradas, sin triángulos de área cero, apoyan en la cama y caben en la bandeja. El laminado no está comprobado.

## Ajustes que propongo (sin probar en esta caja)

| Qué | Valor | Por qué |
| --- | --- | --- |
| Material | PLA | Es lo que se usó en las probetas anteriores |
| Boquilla y capa | 0,4 mm y 0,2 mm | Las holguras del modelo están medidas con probetas a capa de 0,2 |
| Soportes | **Ninguno, en ninguna pieza** | Todas están pensadas para salir sin soportes. Si el laminador los pone solos, quítalos: dentro de las ranuras estorbarían |
| Compensación del «pie de elefante» | Activada | Varias piezas encajan justo por la cara que toca la cama (soporte, puertas, satélites) |
| Paredes | 3 | Estimado |
| Relleno | 15 %. **Macizo (100 %)** en satélites, tetón, pasadores, pestillos, puertas y soporte | Son pequeñas o trabajan; el plástico que gastan es poco |
| Costura | Detrás o alineada, en el cuerpo y la funda | Son las caras que se ven |

## Las bandejas

Todas caben en la X1 Carbon. Dentro de cada fichero las piezas ya están como se imprimen: no hay que girarlas.

| Fichero | Piezas | Color | Cómo va | Ojo con |
| --- | --- | --- | --- | --- |
| `caja-01-base.3mf` | Base con sus tres columnas | Blanco | De pie | La pieza más alta junto con el cuerpo (96 mm). Las columnas son finas y altas: mejor sin corrientes de aire |
| `caja-02-tubo.3mf` | Tubo | Blanco | De pie | Las tres ranuras de dentro son en V a 45°: salen sin soportes |
| `caja-03-cuerpo.3mf` | Cuerpo | Blanco | **Boca abajo** | Lo que toca la cama es el borde de arriba, el que se ve |
| `caja-04-funda-y-frase.3mf` | Funda y frase | **Mármol y azul** | **Boca abajo** | Son dos piezas, una dentro de otra: la frase son las tres primeras capas del techo. Hay que cargarlas como **un solo objeto con dos partes** y dar el azul a la parte `frase`. Si al abrir aparecen como dos objetos sueltos, no las muevas: tienen que quedar exactamente donde están. Los trazos de la frase miden de 0,8 a 1,0 mm |
| `caja-05-plataforma.3mf` | Plataforma con pedestal | Blanco | El disco en la cama | Bajo la pared del pedestal hay dos pasos de 6 mm en puente |
| `caja-06-bisel.3mf` | Bisel | Blanco | **Boca abajo** | La cara que se ve, en la cama |
| `caja-07-plato.3mf` | Plato | Blanco | La espiral en la cama | La espiral y tres cajeados son techos en puente (5 y 16 mm) |
| `caja-08-marco-y-piezas-pequenas.3mf` | Marco, 5 satélites, tetón, 2 pasadores y 2 pestillos | Blanco | — | Los pasadores van tumbados sobre su cara plana |
| `caja-09-rueda-central-y-puertas.3mf` | Rueda central y las dos puertas | Blanco | **Boca abajo** | La cara que se ve, en la cama. Las dos puertas son distintas |
| `caja-10-meseta-y-aro.3mf` | Meseta y aro de las puertas | Blanco | De pie | La meseta tiene techos en puente de 10 a 12 mm; dos de ellos, muy cerca de la cama |
| `caja-11-satelite-azul.3mf` | El satélite azul | **Azul** | Plano | La misma cara abajo que los otros cinco |
| `caja-12-soporte.3mf` | Soporte del reloj | Blanco, el mismo que la plataforma | **Tumbado** sobre su costado derecho | Así el cojín sale sin soportes. **Macizo (100 %):** pesa abajo y vuelca menos (unos 104 g). Su pie tiene que caer solo hasta el fondo del cajeado del pedestal (0,3 mm por lado): si no cae, lija la cara que tocó la cama |

Son 25 piezas, 12 bandejas y tres colores. Si todo fuera macizo serían unos 1.335 cm³ de plástico (1,65 kg); con relleno al 15 % será bastante menos. **No está laminado: ni el peso ni las horas los sé.**

## Imanes

Diez, de 5 × 1,6 mm, todos de adorno: sin ellos la caja funciona igual. Dos en la oreja del tubo y dos en el tope de la base (entran de canto, desde fuera); dos en dos esquinas del cuerpo y dos en la funda; uno en el fondo del cajeado del pedestal y uno bajo el pie del soporte. Siempre imán contra imán. Los de la funda, el cuerpo, el pedestal y el soporte van en cajeras abiertas: a presión o con un punto de pegamento.

## Después

El montaje, paso a paso, está en el apartado 7 de [`../reporte-v5/caja-entera.md`](../reporte-v5/caja-entera.md). Cada paso está comprobado en el modelo (`../reporte-v5/caja-auditoria.txt`, parte A).
