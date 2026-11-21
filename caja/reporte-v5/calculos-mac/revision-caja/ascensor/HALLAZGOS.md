# Revisión del ascensor y del planetario (caja v5)

Revisor independiente, sesión del Mac. Modelo: `caja_piezas_v5.py` y `caja_diseno_v5.py` (copias idénticas a las del repositorio, comprobado con `cmp`). El repositorio no se ha tocado.

Todos los programas están en esta carpeta (`ascensor/`) y se lanzan con
`python <programa>`. Cada uno deja su salida en el `*_out.txt` del mismo nombre.
«tau» es el giro del tubo en grados (0 = cerrado, 345 = abierto).

Resultado en una línea: **1 error en la caja tal como está dibujada** (los tetones casi no tienen juego en la hélice), **1 error del modelo paramétrico** (no se regenera solo con otro reloj), 9 riesgos y varias comprobaciones del autor que no prueban lo que dicen. No hay ninguna pieza que pise a otra en el ascensor ni en el engrane.

---

## ERRORES

### E1. Los tres tetones de la plataforma casi no tienen juego en la hélice: 0,027 mm, no los 0,20 de diseño

- **Qué:** en los tramos planos de las ranuras el tetón cónico tiene la holgura prevista. En la hélice, no: queda a 0,019 mm de la pared (distancia mínima) y solo puede subir o bajar 0,027 mm a cada lado. El código (`hv0 = rt_ + hd`) y el reporte del PC («cada tetón tiene 0,2 mm de holgura») dan 0,20. Con las holguras medidas en piezas impresas (0,15 por lado ya sujeta), tres tetones a 0,02 mm es un ajuste a presión durante 243 de los 345 grados.
- **Dónde:** tubo, las tres ranuras en hélice (`tu.helice(trapecio, ...)`, líneas 321-324 de `caja_piezas_v5.py`), contra los conos de los tetones de la plataforma. De tau = 92 a tau = 335, los tres tetones a la vez. El punto más cercano está a media pared de la V (radio 76,5 a 77,3).
- **Cifras:**

| | tramos planos (tau 0-91 y 336-345) | hélice (tau 93-334) |
|---|---|---|
| distancia mínima plataforma-tubo (malla) | 0,18 mm | **0,019 mm** |
| lo que sube o baja el tetón hasta tocar (geometría exacta) | 0,249 mm | **0,027 mm** |
| lo mismo, con mallas (umbral 0,001 mm³) | 0,26 | 0,04 |
| un tetón hacia fuera en su radio (exacta) | 0,278 | 0,026 |
| giro libre de la plataforma | 0,28° (lo paran las columnas) | 0,12° (lo para el tubo) |

- **Por qué pasa** (`a04b_causa.py`), dos causas que se suman:
  1. La ranura sube con 15,27° de pendiente y el tetón es redondo: la altura libre de la ranura se mide en vertical, pero el tetón necesita 3/cos(15,27°). Se pierden 0,110 mm. Con una V perfecta quedarían 0,086 mm.
  2. La V de la hélice se hace barriendo un trapecio de lados **rectos en planta**. Entre la boca (r = 76, a 8,84° del centro) y el fondo (r = 78,8, a 1,66°) esa recta se mete 0,165 mm en la ranura a media pared. Quedan 0,027 mm.
- **No es un artefacto de la malla:** está calculado dos veces, con las mallas de manifold3d y con la definición matemática exacta de la ranura (polígono que sube girando), y coinciden (0,019 mm de distancia normal equivalen a 0,027 en vertical). El generador de Fusion hace un barrido con giro de ese mismo polígono, así que la pieza de Fusion tiene que salir igual; eso no lo he podido medir en Fusion.
- **Matiz:** en el modelo no llega a pisar (volumen común 0). Que se atasque o solo vaya duro lo dirá la probeta del ascensor; con las holguras medidas hasta hoy, no debería deslizar.
- **Programas:** `a04_teton_v.py` (exacto y mallas), `a04b_causa.py` (causas), `a01_barrido.py` (barrido fino), `a02_juegos.py` (juego giro a giro).

### E2. Con otras medidas de reloj el modelo no se regenera solo, y la fase 2 sola dice «TODO BIEN» cuando la fase 1 falla

No afecta a la caja con las medidas de hoy. Afecta a la promesa del código («el día que Pepe lo mida, se cambia aquí y se regenera todo»).

- **Reloj 46 × 55 × 82** (`CAJA_PRUEBA=reloj_ancho=46,reloj_fondo=55,reloj_alto=82`):
  - `python caja_diseno_v5.py` → **HAY FALLOS**: a la rueda central le quedan 1,1 mm bajo los dientes (pide 2,0) y la espiral del plato llega a 76,1 mm de radio, fuera del tubo (76,0).
  - `python caja_piezas_v5.py` → **TODO BIEN**. La fase 2 no repite las comprobaciones de la fase 1 y sus choques en 3D no ven ninguno de los dos fallos.
- **Para que pase hay que cambiar a mano `z_central` y `tubo_r`**, con dos condiciones que el código no dice:
  - `z_central=81, tubo_r=78`: la fase 1 dice TODO BIEN y la fase 2 falla: los seis satélites pisan al bisel **63,04 mm³** cada uno. La colocación de los dientes solo vale si (dientes de central + dientes de bisel) es múltiplo de 12; la fase 1 solo comprueba múltiplo de 6.
  - `z_central=84, tubo_r=80`: pasa todo.
  - Reloj pequeño con `z_central=72, tubo_r=72`: la fase 1 pasa y en la fase 2 el tubo pisa a las columnas **10.360,88 mm³**: los radios de las columnas (66,5 a 74,2) están escritos a mano y no siguen al tubo.
- **Lo que sí pasa:** medidas de hoy; `reloj_alto=82`; `reloj_ancho=45`; `reloj_fondo=54`; reloj 42 × 51 × 74 si se cambian también las medidas del reloj de pega.
- **Programa:** las órdenes y sus salidas están en `a11_prueba_out.txt` y `a11b_prueba_out.txt` (lanzadas sobre una copia en `ascensor/prueba/`, para no pisar el `caja-v5-piezas.json` de la carpeta común).

---

## RIESGOS (dependen de tolerancias de impresión)

**R1. Al bisel no lo centra el cuerpo, sino los dedos de la rueda central y los dientes.** Empujándolo de lado (`p10_bisel.py`, `p08_centrado.py`):
- toca primero el cono de su techo contra la punta de un dedo de la rueda central a **0,29-0,33 mm**;
- el agujero del labio del cuerpo, que es lo que debería centrarlo, no llega hasta 0,39-0,40 mm;
- los dientes: con los satélites en su sitio (pueden girar, no desplazarse) pisan a 0,15-0,20 mm; contando el juego de 0,25 de sus ejes y el plato quieto, el satélite del lado empujado se queda sin sitio entre bisel y central a **0,30-0,55 mm** según la fase del diente (0,30-0,325 con tau = 0).
- **Respuesta a la pregunta del acuñado: sí.** En algunas fases, el engrane se queda sin juego (0,30) antes de que el cuerpo pare al bisel (0,40). Si además el cuerpo se va los 0,15 que tiene en la base, son 0,55. La búsqueda con el plato libre es de rejilla gruesa (0,35-0,60): tómese como orden de magnitud.
- Lo que centra cada cosa, por lado: bisel en el cuerpo 0,40; faldón del bisel sobre el plato 0,50; plato en el cuello del marco 0,55; satélite en su eje 0,25; tubo abajo en el aro de la base 0,35; almenas tubo-plato 0,15. La boca de arriba del tubo solo la centran los ejes de los satélites a través de los dientes.

**R2. El bisel tiene una ventana en altura de 0,30 mm hacia abajo y 0,40 hacia arriba.** Si baja 0,30 respecto a la rueda central, su techo se sienta sobre los seis dedos (0,25 no pisa; 0,30 pisa 0,40 mm³; 0,35 pisa 7,5 mm³). Si sube 0,40, su ala roza el labio del cuerpo. Esas alturas dependen de tres pilas impresas de unos 100 mm (tubo + plato; columnas + marco + meseta + rueda central; cuerpo). El reporte del PC avisa del escalón a la vista, no de que el bisel pueda quedar apoyado en los dedos. `p10_bisel.py`.

**R3. Holgura entre flancos de los dientes: 0,065 a 0,094 mm por flanco.** Juego medido en el modelo: un satélite gira 0,17-0,21 mm en su primitivo con lo demás quieto; el bisel, con el tubo quieto, ±0,13 a ±0,15° (0,38-0,44 mm en su canto). No se pisan en ninguna posición. Pero 0,065-0,094 por flanco está por debajo de los 0,15 que «sujetan» en las piezas medidas, y no hay nada medido sobre dientes. Los mínimos (0,065 con el bisel, 0,081 con la central) coinciden con la interferencia teórica de un piñón de 12 dientes sin destalonar: la punta de la central llega a 60,00 (límite 59,62) y la del bisel a 75,00 (límite 75,50). `p07_engrane.py`, `p07b_engrane_lateral.py`.

**R4. Arriba, el pedestal puede llegar a rozar el hueco.** Rendija nominal 0,40 mm por lado con el marco y con la meseta, 0,90 con las puertas abiertas y con el aro. Con los juegos reales arriba (±0,34 mm en X, +0,29/−0,34 en Y, ±0,26 en altura, ±0,28° de giro, cabeceo ±0,22-0,24°), la guía lo para a **0,008-0,022 mm** del marco y de la meseta: no pisa en ninguna de las posturas probadas, pero es contacto en cuanto la impresión se desvíe. Una esquina puede quedar hasta 0,36 mm por encima del ras. Puertas y aro, nunca a menos de 0,49. `a05_arriba.py`, `a05b_dirigido.py`.

**R5. «A ras» es la posición nominal, no la de reposo.** Apoyada en el suelo del tramo plano de arriba, la plataforma queda **0,25 mm por debajo** del ras; entre tau 334 y 336 baja de −0,03 a −0,25. Abajo descansa en el asiento a −0,15 (los tetones flotan 0,10 sobre el suelo de su ranura). En la hélice, a −0,027. `a04_teton_v.py`.

**R6. Pared más fina entre ranuras: 1,81 mm**, no los 3,7 que imprime la fase 1. Está entre el suelo de la hélice 2 y el techo del tramo plano 3, en el ángulo 327° del tubo, z de −111,35 a −109,47 (1,88 en vertical en la boca; crece hacia el fondo). Las otras dos: 2,52 y 3,21. Pared hacia la cara exterior del tubo: 1,60 mm. `a03_paredes.py`.

**R7. Canto de abajo del tubo en filo.** Bajo los tramos planos de abajo quedan 0,15 mm de material en la boca (menos que una capa), a lo largo de 3 × 95° del canto interior. En la práctica es un chaflán; el tubo apoya en la pista con 1.189 mm². `a03_paredes.py`, `p10_bisel.py`.

**R8. Imanes del tope sujetos solo por el ajuste.** En el tope de la base la ranura está abierta por los dos extremos del radio (no hay material ni hacia el tubo ni hacia fuera); en la oreja, abierta hacia fuera. Ajuste: 0,075 mm por lado en grueso y 0,15 en alto. Un imán del tope que se corra 0,6 mm hacia dentro toca el tubo que gira; uno de la oreja que asome más de 0,575 mm toca la pared del cuerpo. `a06b_imanes.py`.

**R9. Boca abajo, todo menos la base cuelga del labio del cuerpo**, y el cuerpo, de sus cuatro pestillos de 1 mm. El marco, la meseta, las puertas y la rueda central cuelgan de los seis dedos apoyados en el cono del bisel. No calculo fuerzas: solo señalo el camino de la carga. `p09_boca_abajo.py`.

---

## COMPROBADO Y BIEN

1. **Barrido fino del ascensor** (819 posiciones: cada 0,5°, y cada 0,1° de 88 a 96 y de 331 a 339): la plataforma no pisa nada (volumen común 0,0000 con tubo, base, marco, aro, meseta, plato, tetón suelto y puertas). Distancias mínimas: base 0,150 (el asiento, intencionado) y 0,332 (columnas, intencionado); marco y meseta 0,400; aro y puertas 0,900. Por debajo de 0,15 sin ser apoyo: solo el tubo en la hélice (E1). `a01_barrido.py`.
2. **La plataforma no se cae ni se levanta más de 0,5 mm en ningún giro** (346 giros). Baja 0,14 hasta el asiento (tau 0-91), 0,04 en la hélice, 0,26 arriba. Sube 0,26 / 0,04 / 0,26. No hay escalón al pasar sobre las entradas ni sobre los planos de otras ranuras, ni en las transiciones plano-hélice. `a02_juegos.py`.
3. **Las ranuras no se juntan** con los ángulos reales (90, 212, 330); entre una hélice y la entrada de otra quedan 5,05 mm o más. `a03_paredes.py`.
4. **Topes:** el tubo para exactamente en 0,00° y en 345,00°, oreja contra tope con unos 44 mm² de contacto. Sin tope, los tetones llegarían al final de su ranura 0,76° más allá y el tetón suelto 3,2° más allá: el tope actúa primero. En su vuelta, la oreja pasa a 0,575 mm de la pared del cuerpo (0,225 con el tubo descentrado 0,35) y a 1,06 del resto de la base. `a06_topes.py`.
5. **Engrane:** 241 posiciones (tubo cada 0,05° a lo largo de 12°, 2,6 pasos de diente) más 48 repartidas hasta 345°: ningún satélite pisa a la central ni al bisel. Holguras de fondo, 0,375 mm en los cuatro casos. `p07_engrane.py`, `p07b_engrane_lateral.py`.
6. **Satélites boca abajo, en cualquier giro:** siempre retenidos, estén o no debajo de un dedo. Por fuera los tapa el techo del bisel (3,0 mm de solape) y por dentro la placa de la rueda central (4,5 mm). Juego en altura, 0,4 mm; se inclinan 1,1° como mucho. `p09_boca_abajo.py`.
7. **Boca abajo, lo demás:** bisel sube 0,40 (labio del cuerpo, 2,0 mm de solape, 1,6 con el bisel descentrado); plato y tubo, 0 más (los para el bisel); rueda central 0,25 más (0,65 en total); plataforma 0,25 en los planos y 0 en la hélice. Nada queda suelto. `p09_boca_abajo.py`.
8. **Apoyo al apretar el bisel:** bisel sobre plato 962 mm² (anillo de r 78,6 a 80,5, entero encima de la pared del tubo); plato sobre tubo 2.025 mm²; tubo sobre la pista 1.189 mm². Sin tramos al aire. Al apretar nada cede; crece el roce bisel-plato y tubo-base. Los satélites no quedan pillados (0,4 de juego). `p10_bisel.py`.
9. **Montaje del tubo:** baja hasta su sitio sin pisar nada; girado 120° o 240° se queda 6,0 mm alto. Hay que bajarlo arrimado al tope de cerrado: entra con el tubo entre tau = 0 y 0,4°; a 2° ya no. `a12_montaje_tubo.py`.
10. **Con las medidas de hoy**, `caja_diseno_v5.py` y `caja_piezas_v5.py` dan TODO BIEN en la copia de trabajo. `a11_prueba_out.txt`.

---

## COMPROBACIONES Y CÓDIGO DEL AUTOR QUE NO PRUEBAN LO QUE DICEN (punto 11)

- **Fase 1, comprobación 6 (ranuras):** supone ranuras a 120° y que el plano empieza justo en la siguiente. Imprime «queda 3,7 de pared»; lo real es 1,88 (ranuras a 118°, el plano empieza 3° antes y es 0,05 más alto).
- **Fase 1, nota del juego de la plataforma («0,20 mm de cada tetón») y la frase del reporte:** es el parámetro, no una medida. Real: 0,25 en los planos y 0,027 en la hélice.
- **«La plataforma no se puede hundir» y «va guiada»:** mueven 0,6 y 1,2 mm y miran si choca. Prueban que hay pared, no cuánto juego hay; por eso no vieron E1.
- **«Los dientes engranan»:** prueba que un satélite mal girado pisa, no que bien girado engrane. (Engrana: punto 5 de arriba.)
- **Condición de reparto de satélites:** comprueba múltiplo de 6; hace falta múltiplo de 12 (E2).
- **La fase 2 no incluye la fase 1** (E2).
- **El reloj está descrito dos veces** (`reloj_ancho/fondo/alto` y `cabeza/corona/brazalete`). Cambiando solo el primer grupo a un reloj mayor, la comprobación de los 3 mm pasa sin probar nada; a uno menor, falla (2,00 mm) porque el reloj de pega no se encoge.
- **Valores a mano que no salen de parámetros:** radios de columnas y espigas (66,5; 74,2; 68,3; 72,4) y el `70.0` de sus ángulos; asiento de la plataforma (30 a 62); eje de los satélites (2,75); saliente de la oreja (`+5.3`: «pasa a 0,6 mm del cuerpo» solo con las medidas de hoy); peana del soporte (±17 × ±20) e imán en (0, 12).
- **La cara de arriba de los satélites y el techo del bisel están en el mismo plano** (z = −3,40): distancia 0,000 en el modelo. No es un fallo (el satélite descansa 0,4 más abajo, en el plato), pero ninguna comprobación por volumen lo vería si pisara una centésima.
- **La pendiente de la rampa (15,0°)** se calcula a r = 77,5; en la boca, donde el tetón queda más justo, es 15,27°.
- **Paso de 2° y umbral de 0,02 mm³:** con paso de 0,5° / 0,1° y umbral 0 no aparece nada nuevo en la plataforma ni en el engrane.

Fuera de mi parte, pero lo he visto al medir la rendija de arriba: delante y detrás del pedestal, con las puertas abiertas, queda al aire el asiento de las puertas, una franja de 7,7 mm de ancho y 5 mm de hondo. El pedestal rellena el hueco de 50 × 59, no el rectángulo de las puertas.

---

## LO QUE NO HE PODIDO COMPROBAR

- **Fuerzas, roce y si la rampa se sujeta sola.** No hay nada impreso que lo confirme y no doy ninguna cifra.
- **La pieza de Fusion.** He leído que `generador_caja_v5.py` barre el mismo polígono con giro; no he abierto Fusion ni medido el `.f3d`.
- **Los ficheros de las probetas (`.3mf`).** No los he abierto: no sé si coinciden con este modelo.
- **Flexión** de los dedos de la rueda central, del tope de la base y de la pared de 1,81 mm.
- **El acuñado del engrane con todo flotando a la vez** (bisel, seis satélites y plato): lo he hecho satélite a satélite y con rejilla gruesa.
- **Tubo y plato contra el resto** (marco, aro, tetón suelto) en barrido fino: solo he barrido la plataforma, la oreja y los engranajes.
- En el repositorio hay un fichero sin seguimiento que no es mío: `caja/reporte-v5/calculos-mac/revisar_caja_v5.py`. No lo he tocado.
