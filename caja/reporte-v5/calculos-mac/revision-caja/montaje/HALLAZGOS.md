# Revisión de montaje de la caja v5: hallazgos

Revisor independiente, 21-22 de noviembre de 2026. Modelo: `caja_piezas_v5.py` y `caja_diseno_v5.py` de la copia de trabajo (idénticos a los del repositorio). Texto revisado: apartados 7 y 4.1 de `caja/reporte-v5/caja-entera.md`.

Todo lo que sigue es geometría del modelo (volumen común entre piezas, umbral 0,05 mm³). No hay ninguna fuerza calculada. Los programas están en esta carpeta y se ejecutan con `python <programa>`; cada uno deja su salida en el `.txt` del mismo nombre.

## ERRORES

### E1. Paso 10: el plato no se puede poner después de la rueda central (paso 8)

- El plato es un anillo de 54,46 a 80,5 mm de radio que va **debajo** de la rueda central. La rueda central llega a 60 mm (dientes), 61,5 (placa) y 74,3 (dedos).
- Bajando el plato en vertical con la rueda central puesta: pisa a la rueda central **9.313 mm³** a 9,5 mm de su sitio; pisa desde 14,5 hasta 0,5 mm.
- No hay otro camino girando o inclinando: un anillo no pasa alrededor de un disco mayor que su agujero.
- Programa: `t1_pasos.py`.

### E2. Paso 11: los satélites no entran en sus ejes con la rueda central puesta

- La placa de la rueda central (radio 61,5) tapa 4,5 mm de cada satélite (que llega hasta 57 mm de radio).
- En vertical, cada satélite pisa a la rueda central **74,6 mm³**; pisa desde 9,0 hasta 0,5 mm de su sitio.
- Busqué un camino inclinándolo, desplazándolo y girándolo: desde su sitio el satélite solo consigue subir 1,05 mm e inclinarse 6,5°. Para salir del eje tiene que subir 6,2 mm. No hay camino en el modelo.
- Programas: `t1_pasos.py` y `t2_satelite_inclinado.py`.

**El orden que sí vale para E1 y E2 (comprobado, sin cambiar ninguna pieza):** pasos 1 a 7, después 9 (cerrar puertas y tetón), 10 (plato), 11 (satélites), **8 (rueda central)**, 12 y 13. Con ese orden nada pisa nada, salvo los pestillos del cuerpo, que es lo previsto. Programa: `t3_orden_alternativo.py`.

### E3. Boca abajo, el soporte y el reloj no están sujetos y caen sobre las puertas

- Caja cerrada, boca abajo: soporte y reloj caen **5,0 mm** hasta apoyarse en las puertas (5,5 a 5,8 mm si las puertas ya están descolgadas). Geométricamente solo los sujeta un imán.
- Con la caja abierta (tubo a 100°, 200° o 345°) salen de la caja: más de 150 mm sin que nada los pare. Con el tubo a 70° caen 14,25 mm hasta las puertas a medio abrir.
- De lado y cerrada, resbalan sobre el pedestal entre 8,75 y 15,75 mm hasta que el reloj toca el marco. De lado y abierta, hacia delante o hacia atrás no los para nada.
- El reporte dice en 4.1 «Boca abajo no se cae nada: bien», pero su lista de comprobación no incluye el soporte ni el reloj (tampoco la puerta izquierda, el pasador izquierdo ni los satélites 2 a 6; esos sí los he comprobado y están bien).
- Matiz: el brief pide a la vez «soporte suelto» y «boca abajo no se cae nada». Es una contradicción del encargo, y el reporte ya declara el soporte como provisional. La decisión es de Pepe.
- Programas: `t5_gravedad.py`, `t7_puertas_boca_abajo.py`, `t10_varios2.py`, `t12_soporte_de_lado.py`.

## RIESGOS

### El cuerpo y sus cuatro pestillos (`t6_cuerpo.py`, `t4_mal_montado.py`)

- **R1. No hay rampa de entrada.** El canto de abajo del cuerpo (arista viva) cae sobre un escalón horizontal de 0,35 mm y después otro de 0,5. Interferencia total, 0,85 mm por lado, durante 3,7 mm de bajada (de 4,0 a 0,3 mm de su sitio); máximo 66,9 mm³. La pared tiene que abombarse 0,85 mm en el centro de cada uno de los cuatro lados a la vez. Estimación mía, no medida: eso es una deformación de alrededor del 0,1 % en una pared de 3 mm y 172 mm de luz, así que debería ceder; pero sin rampa no cede sola al empujar.
- **R2. No se ve cómo se quita.** Las caras de enganche son planas, a 90°; enganchan 0,85 mm de fondo en 56 mm de largo total (**47,6 mm²**), con 0,3 mm de juego en altura. La junta entre cuerpo y base queda enrasada por fuera, sin ranura: «hacer palanca en un pestillo» no tiene dónde. Si no sale sin romper, no se puede abrir nada de dentro, porque todo lo demás sale después del cuerpo.
- **R3. Aparte de los pestillos, nada sujeta al cuerpo.** Sube 120 mm sin tocar nada más. Con la caja de pie, si se levanta cogiéndola por el cuerpo, todo lo demás cuelga de esos 47,6 mm²: 849 cm³ si fuera macizo (1,05 kg como mucho) más el reloj.
- **R4. El cuerpo entra girado 90°, 180° y 270°.** Asienta del todo dejando solo 9,1 mm³ de interferencia (dos trozos de 3,7 × 0,85 × 1,8 mm en el pestillo ancho), menos que los 66,9 mm³ que hay que vencer para meterlo bien. «El cuerpo solo entra con el índice al frente» no se cumple. Funciona igual; cambia dónde queda el índice, y a 90° y 270° los imanes de la funda no coinciden.

### Otras piezas que entran mal sin que la forma lo impida

- **R5. La funda entra en las cuatro posiciones.** El índice sobresale 0,6 mm y la funda tiene 0,5 mm de holgura por lado: corriéndola 0,10 mm baja los 130 mm sin pisar nada. «La funda solo entra con su frente al frente» no se cumple. Efecto: la frase queda girada. (`t4_mal_montado.py`)
- **R6. El aro entra volcado** (pistas hacia abajo, brazo atrás) y queda 0,25 mm más bajo. Se descubre después: la meseta queda 0,75 mm alta, la puerta de pie se queda 2,5 mm alta y el pasador no entra. «Solo cabe ahí» no es exacto. (`t11_volcadas.py`)
- **R7. Una puerta cara abajo se puede montar** tumbada (corrida 1 mm al centro y deslizada): pisa solo 0,76 mm³ y el pasador entra. Se ve, como dice el reporte: la varilla asoma 5,7 mm y choca con la otra puerta (202 mm³). (`t11_volcadas.py`)
- **R8. Un satélite del revés entra y engrana igual** (0,000 mm³). Solo cambia la cara que se ve; el brief pide la misma cara en los seis. (`t4_mal_montado.py`)

### Montaje

- **R9. Paso 9 y 10: el plato no asienta si el aro está en su tope.** Al cerrar las puertas con el brazo, el aro no para en 0° sino en −0,70° (lo para la meseta). Ahí el tetón queda 0,83 mm fuera de su sitio, y el plato solo asienta con el tetón a ±0,2 mm: se queda 2,6 mm alto, sobre el tetón. Con el plato encima, el brazo queda tapado. Hay que acertar a ciegas. (`t8_aro_topes.py`)
- **R10. Paso 13: el soporte y el reloj no se pueden poner con la caja cerrada** (chocan con las puertas). Hay que abrirla antes; el texto no lo dice. (`t1_pasos.py`)
- **R11. Con el orden corregido, los pasadores quedan sin tapar** desde el paso 7 hasta que se pone la rueda central: sin ella nada los para a lo largo (en la prueba recorren 22 mm, hasta el bisel). (`t7_puertas_boca_abajo.py`)

### Boca abajo y de lado

- **R12. Las puertas cerradas se descuelgan más de lo declarado.** Una sola, con la otra en su sitio: 2,0° (la para la otra puerta). Las dos a la vez, contando la holgura del pasador: 3,25°, de 1,8 a 2,0 mm en la punta (el reporte dice 1,5). Una sola con el aro corrido los 0,3 mm de holgura que tiene en el cuello: hasta 6,25°, de 3,0 a 3,4 mm; es el caso peor. Y si el reloj cae sobre ellas (E3), lo aguantan solo la bola y la pista. (`t7_puertas_boca_abajo.py`, `t9_varios.py`)
- **R13. La funda, boca abajo, no la para nada** en 140 mm: solo sus dos imanes. Cogida por la funda no se cae nada (la caja queda dentro, como en un vaso). Es lo que pide el brief («suelta»). (`t5_gravedad.py`)
- **R14. De lado, la oreja del tubo pasa a 0,075 mm de la pared del cuerpo** en cuatro puntos del giro (0,575 mm con el tubo centrado; el tubo se desplaza 0,5). Puede rozar. El bisel, de lado, se apoya en los dientes de los satélites (0,05 a 0,10 mm) y en el labio del cuerpo (0,40). (`t5_gravedad.py`, `t10_varios2.py`)

## Comprobado y bien

- **Pasos 1 a 7 y 9:** cada pieza baja 120 mm (los pasadores, a lo largo de Y, por delante y por detrás) sin pisar nada. Paso 12: el bisel sube por dentro del cuerpo, y cuerpo y bisel bajan sobre todo lo demás pisando solo los pestillos. También vale poner antes el bisel y bajar después el cuerpo solo. (`t1_pasos.py`, `t9_varios.py`)
- **Puertas de pie:** entran con el aro entre 7,75° y 11,6° (su tope de abierto), y también corridas ±0,25 mm o inclinadas ±2°. Con el aro en otra posición se quedan de 2,0 a 3,5 mm altas. (`t8_aro_topes.py`, `t10_varios2.py`, `t4_mal_montado.py`)
- **Solo entran en una posición:** plataforma (barrido de 1° en 1°), tubo (solo baja entre −0,6° y 0°; a 120° y 240° pisa 5,6 mm³, que por mi cuenta son unos 2 mm de interferencia), marco (girado se queda 3 mm alto; volcado se ve), rueda central (se queda 8 mm alta) y plato (se queda 3 mm alto). El plato tampoco asienta con las puertas abiertas y el tubo en 0° (50,9 mm³). (`t4_mal_montado.py`, `t11_volcadas.py`)
- **Meseta:** entra a 0° y a 180°. No es exactamente simétrica: difiere de su copia girada en 325,9 mm³ (las tres ranuras de las llaves). No importa: entonces la rueda central solo entra a 180°, y girada 180° es idéntica salvo las llaves. El texto «las dos son la misma» sobra en lo literal, no en el efecto.
- **Pasadores y tetón:** simétricos, da igual por qué lado. **Puertas intercambiadas:** son la misma pieza (diferencia 0,0000 mm³).
- **Boca abajo, las otras 22 piezas** (tubo a 0°, 70°, 100°, 200° y 345°): ninguna se desplaza más de 0,9 mm cogiendo la caja por el cuerpo, 1,2 mm por la base y 1,4 mm por la funda. Coincide con el reporte: bisel 0,4 mm, rueda central 0,2 más.
- **Qué sujeta el interior boca abajo:** cogida por el cuerpo, todo acaba en el ala del bisel contra el labio del cuerpo (1.068 mm²), no en los pestillos. Por el camino: plato bajo el bisel (962 mm²), tubo bajo el plato (2.084 mm²), dedos de la rueda central bajo el techo del bisel (117 mm² en planta) y meseta bajo el labio de la rueda central (350 mm²). Los pestillos solo cargan si se coge por la base, o de pie por el cuerpo (R3). (`t9_varios.py`)
- **De lado** (±X y ±Y, tubo a 0° y 345°): ninguna pieza se desplaza más de 1,0 mm (los pasadores, a lo largo); las demás, 0,8 o menos. Nada deja de engranar ni se sale de su guía.
- **Pasadores:** con la rueda central puesta se mueven 0,45 mm a lo largo y paran. **Bisel:** con el cuerpo puesto no sube (106,8 mm³ a 0,5 mm).
- **Desmontaje:** con el orden corregido, al revés, ninguna pieza de la caja queda encerrada. Todo depende de que el cuerpo salga (R2).

## Lo que no pude comprobar

- Nada de fuerzas: si la pared del cuerpo cede, si los pestillos aguantan el peso, si los imanes sujetan el soporte o la funda, si el pasador entra a mano con 0,15 mm de holgura en 90 mm.
- Los desplazamientos por gravedad son solo traslaciones rectas de cada pieza, más el giro de las puertas. No he mirado cabeceos ni giros combinados, ni sacudidas.
- La búsqueda de E2 inclina el satélite solo alrededor del eje tangencial (la más favorable); no es una búsqueda en los seis movimientos.
- Encajar a ciegas los dientes del bisel y de la rueda central en los seis satélites: en el modelo coinciden; en la mano no lo sé.
- El modelo de Fusion y los ficheros 3MF: solo he usado el programa de Python.
- El reloj de pega es un aro cerrado enlazado con el soporte: en el modelo no se puede poner ni quitar (se mueve de 0,4 a 1,8 mm y choca). Solo importa si se imprime; un reloj de verdad abre el brazalete.
