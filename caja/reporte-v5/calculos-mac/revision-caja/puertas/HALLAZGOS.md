# Revisión del mecanismo de las puertas (caja v5)

Todo sale del modelo de `caja_piezas_v5.py` construido con manifold3d. Los programas están en esta carpeta.
Para repetir cualquiera: `cd` a esta carpeta y `python <programa>`.
`comun.py` construye el modelo y lo usan todos. Las fuerzas son calculadas: no valen hasta que una pieza impresa las confirme.

## ERRORES

**E1. Hay un agujero en el centro de la junta: 0,3 × 1,2 mm (0,36 mm²).**
- Dónde: puertas cerradas, x de −0,15 a +0,15, y de −0,60 a +0,60. El labio de cada puerta empieza en |y| = 0,6 y el rebaje de la otra acaba en y = 0: en ese tramo no hay labio de ninguna.
- Debajo no hay puerta ni meseta: lo primero que toca la vertical es el reloj de pega, en z = −10.
- Inclinando la vista sigue habiendo paso: hasta unos 26° a lo largo de la raya (0,019 mm² a 24°) y hasta unos 10° de lado (0,032 mm²). A 15° de lado ya no.
- Incumple el brief (línea 159: «Sin agujero… mirando desde arriba no se ve lo de dentro») y la prueba «a contraluz» de la probeta. El reporte dice «por la raya solo se ve puerta».
- Reproduce: `c2_vision.py` (proyección) y `t1.py` (columna vertical en (0; 0), (0; 0,3) y (0; −0,5): no atraviesa ninguna puerta; en (0; 0,7) sí).

**E2. Abiertas, las puertas no quedan entre 85° y 95°: quedan entre 82,3° y 95,6°.**
- Con el aro clavado en su sitio exacto: 87,15° a 93,03° (el reporte dice 86,2° a 94,0°).
- Pero el aro solo va centrado por su borde, con 0,30 mm de holgura contra el cuello en todas direcciones (medido en el modelo, con y sin tetón). Desplazado 0,29 mm hacia 60° (o 240° para la izquierda), sin pisar marco, meseta ni tetón, la puerta llega a 82,33°. Hacia fuera, 95,60°, donde la bola toca la ventana de la meseta.
- Empujar una puerta hacia dentro es justo lo que desplaza el aro. No hay ningún tope fijo hacia dentro.
- Reproduce: `c4c_juego_total.py` (búsqueda) y `c4d_verifica.py` (caso directo: volúmenes 0 a 82,5°, 0,0003 mm³ a 82,3°).

**E3. El reloj de pega no queda a 3 mm de las puertas en cuanto se cuenta su juego; con el juego del aro, la puerta lo toca.**
- A 90° exactos: 3,75 mm (lo que dice el reporte).
- Puerta inclinada 2,85° hacia dentro (aro centrado): 2,25 mm, puerta izquierda, tubo a 288°.
- Con los 3,75° que reconoce el propio reporte: 1,78 mm.
- Con 7,5° (alcanzable según E2): se pisan, 0,89 mm³ (tubo 280°); a 82,33°, 2,11 mm³.
- La puerta a 90° está en equilibrio inestable: su centro de gravedad queda 0,03 mm hacia dentro del eje, y 0,66 mm a 87,15°. Cae hacia un extremo u otro del juego.
- Salvedad: las medidas del reloj son supuestas.
- Reproduce: `c7c_pared_y_reloj.py` (tabla final) y `c5_bola.py` (centro de gravedad).

**E4. El montaje descrito no se puede hacer: el plato (paso 10) no entra con la rueda central ya puesta (paso 8).**
- El plato es un anillo de radio interior 54,46 que va por debajo de la rueda central (radio hasta 61,5 y dedos). Bajándolo con la rueda puesta pisa 9.497 mm³ cuando está 9,75 mm por encima de su sitio.
- En el otro orden (tetón, plato y después rueda central) no pisa nada.
- Reproduce: `c8_montaje.py` (últimas tres líneas).

**E5. Las dos comprobaciones de la junta de la fase 1 prueban una junta que ya no existe.**
- `caja_diseno_v5.py` (líneas 232 a 260) comprueba un labio en escalón de 1,0 mm con hueco de 1,2 (media madera), y solo en un corte plano. Las piezas llevan una cuña a 45° (`punta = 0,4`), con el labio solo en media puerta.
- Por eso dan «bien» las líneas «no hay ninguna línea recta que cruce la junta» y «lo más cerca, 0,30 mm», y no vieron E1.
- `labio_grueso` sigue en la lista de parámetros y ya no lo usa ninguna pieza.

## RIESGOS

**R1. Las dos puertas se pisan si una va más de 1,5° a 2,2° por delante de la otra** (con la más baja entre 0° y 10°; 3,15° a 12°; desde 14° ya no). En los términos de la pregunta (a ± δ): desde δ ≈ 0,75° a 1,1°.
- Con una en su asiento, la otra se pisa a partir de 2,16°.
- Si una va más de 10° por delante, al bajar su labio cae encima de la otra y no cierran.
- El mecanismo deja ese margen de sobra: a medio recorrido cada puerta baila ±5,6° a ±7,6° con el aro quieto, y el aro baila ±0,5° de giro (unos ±8° de puerta).
- De pie, el peso las lleva a las dos al mismo lado; boca abajo, inclinada o tocando una puerta, no.
- `c3_desincronizadas.py`, `c3b_umbral.py`, `c4_juego.py`, `c4b_aro.py`.

**R2. La raya de 0,3 mm se cierra a 0,076 mm al pasar por 5°** (la arista de abajo de cada puerta se mete 0,112 mm hacia el centro). En el modelo solo ocurre en y = 0; si las puertas se desplazan a lo largo del pasador, ocurre en una franja.
- Además, la holgura en Y entre el labio y la otra puerta (0,6 mm) es igual a la suma del juego axial de las dos (0,3 + 0,3): con −0,3 y +0,3 quedan a 0,000 mm; con ±0,35 se pisan 0,59 mm³.
- `c1b_cerca.py`, `c3_desincronizadas.py`.

**R3. Cerrada, lo primero que toca al levantar la puerta es la varilla, no la bola.**
- La varilla pasa a 0,107 mm del canto de arriba del cuerno (x 30,9; y 32,8; z −7,1); la bola tiene 0,150.
- La puerta se para a 1,93° (0,94 mm en el canto) por la varilla. Con el aro apoyado en el ala (0,4 más abajo), a 2,24° por la bola.
- Boca abajo (aro +0,4, puerta caída 0,25): a 0,82°, por la varilla, que queda a 0,028 mm.
- El código dice que la varilla no debe tocar «en ningún ángulo».
- `c5_bola.py`, `c5b_boca_abajo.py`.

**R4. Las paredes de la pista no miden los 2 mm de `pista_pared` donde más importa.**
- Cerrado: la pared de fuera mide 0,30 mm (0,30 a 0,75 en todo el reposo), porque `aro_r_ext` = bola + 0,3. Menos que la boquilla.
- Abierto: la pared de dentro (la que para la puerta hacia fuera) mide 0,75 mm en psi 8,5 y 1,85 en psi 11, y no tiene anillo debajo: la pista rompe el borde interior del anillo (llega a radio 37,83; el anillo empieza en 39,07). Vuelan 12,3 mm² por cuerno, hasta 3,24 mm.
- `c7_paredes.py`.

**R5. La ranura del brazo del aro queda abierta por la punta: es una horquilla.**
- La ranura llega a radio 75,64 y el brazo se recorta a 75,20. Boca de 2,99 mm (el tetón, de 5, no sale). Dos dedos sueltos de 2,6 × 3 mm y unos 14 mm.
- La ranura recta del marco también sale por el borde del ala (boca de 3,06 mm).
- `c6_teton.py`.

**R6. El tetón puede inclinarse 6° con las tres ranuras y 8° a 9,5° si el aro cede.**
- La espiral empuja arriba (z −13,5) y el brazo resiste en medio (z −16,7); la ranura del marco no sujeta en esa dirección.
- Su diagonal (10,2 mm) es mayor que el hueco entre el suelo de la ranura y el techo de la espiral (9,6): a 9,45° se acuña entre los dos. Calculado: se queda clavado si el roce pasa de 0,36.
- Metido: 2,5 mm en el marco, 3,0 en el brazo, 2,6 en la espiral (2,8 / 3,0 / 2,3 apoyado; 2,1 / 3,0 / 3,0 boca abajo). No se sale.
- `c6_teton.py`, `c6b_teton_inclinado.py`.

**R7. Cerrada, el juego real no es 3,0°.** Aro centrado: 1,93° a 2,24°. Contando la holgura del aro: hasta 6,06° (2,9 mm en el canto), aunque a 2,16° ya tropieza con la otra puerta. El bloqueo se pierde al final del reposo: 3,25° en psi 2,0 y 6,52° en psi 2,5. `c4c_juego_total.py`, `c4e_reposo.py`.

**R8. A lo largo del pasador, a la puerta la para la bola, no sus cantos.** Toca la pista a 0,16 – 0,22 mm; los cantos tocarían la meseta a 0,30. `c7b_abiertas.py`.

**R9. Empujón a la puerta abierta.**
- Hacia dentro: solo la bola contra la pared de fuera de la pista (2,0 mm, con anillo debajo). Sin tope fijo.
- Hacia fuera: la bola contra la pared de dentro (R4) a 93,03°, y tope fijo de la meseta contra la bola a 95,60°.
- Contacto de punto: huella de unos 0,5 × 0,6 mm con 0,25° de pasada y 0,9 × 1,0 con 1°. A 8 mm del eje.
- Una fuerza en el canto de la puerta llega a la bola multiplicada por 3,48. La varilla (3 mm) tiene 4,46 mm al aire.
- Hacia fuera la bola sube: a 93,03° su ecuador queda 0,29 mm por debajo del canto del cuerno (aro apoyado en el ala).
- `c7b_abiertas.py`.

## COMPROBADO Y BIEN

- **Barrido fino** (tubo 40° a 105° de 0,25 en 0,25, más 0, 20, 150, 250 y 345; todas las parejas): ninguna se pisa, volumen 0. `c1_barrido.py`.
- **Parejas a menos de 0,15 mm:**
  - apoyos: puertas–meseta 0 (asiento, 305,6 mm² por puerta), marco–meseta 0, meseta–rueda central 0;
  - marco–rueda central 0: los pies de las llaves coinciden con el canto del cuello en z = −8. No sé si es apoyo querido;
  - pasadores–marco y pasadores–meseta 0,150: ajuste fijo;
  - no son apoyo: puerta–puerta 0,076 (R2), varilla–aro 0,107 (R3), bola–aro 0,129 en tubo 62,25 (el codo de la pista).
- **Vista de lado** en un corte normal de la junta: la cuña tapa. Lo más cerca, labio y rebaje a 0,477 mm (5,25°). `c3a_seccion.py`.
- **Bloqueo en reposo:** firme con psi ≤ 1,5 y psi ≥ 9,5. El tubo de 0° a 45° está en psi 0, y la plataforma empieza a subir en psi 10,44 (9,89 con el juego del aro). `c4e_reposo.py`.
- **Bola en la pista:** el ecuador queda siempre 1,0 mm o más bajo el canto del cuerno (0,6 con el aro en el ala); entre paredes, 3,5 de sus 5 mm en reposo. Varilla–meseta ≥ 0,227, bola–meseta ≥ 0,226, puerta–aro ≥ 0,752. `c5_bola.py`.
- **Tetón en los extremos:** en la ranura del marco le sobran 1,25 mm (tubo 0°) y 1,20 mm (345°); la espiral sigue 3,2° más allá de cada tope. `c6_teton.py`.
- **Bisagra:** 0,25 mm de juego radial en la puerta. `c7b_abiertas.py`.
- **Montaje, pasos 4 a 7 y 9** (0,25 mm por paso): aro, meseta, puertas de pie (con el aro entre psi 8,5 y 11,6), pasadores y tetón entran sin pisar nada. `c8_montaje.py`.
  - Aro girado (60° a 300°) o boca abajo: no entra.
  - Puerta en el lado contrario: es la misma pieza (diferencia 0). Boca arriba, la manivela asoma 5,7 mm.
  - Pasador: entra igual por delante que por detrás.
  - Meseta a media vuelta: entra, pero no es simétrica (difiere 652 mm³, las ranuras de las llaves). La rueda central va entonces también a media vuelta y no pisa nada. El reporte dice «es simétrica».
  - Puerta con el aro en cerrado o a medias: no asienta (18,8 y 0,55 mm³).
- **Probeta:** el tetón con pomo no pisa nada en su recorrido; a la meseta le quedan 0,70 mm. `c5b_boca_abajo.py`.

## Otras cosas del código (punto 9)

- `juego()` de la fase 2 da 3,00 / 3,75 / 4,00° porque avanza de 0,25 en 0,25 y solo cuenta más de 0,02 mm³. El primer contacto está en 1,93 / 2,85 / 3,03°. Y no cuenta la holgura del aro.
- «El tetón va guiado»: solo prueba que su juego es menor de 1,2 mm.
- El aro y el tetón están dibujados flotando (0,4 y 0,3 mm). De pie bajan, y cambia qué toca primero (R3).
- La cabecera de `caja_diseno_v5.py` dice que el aro gira «unos 12 grados»; son 11.

## NO COMPROBADO

- Roce y fuerzas: enganche del aro, acuñamiento del tetón, resistencia de varilla y paredes.
- La vista inclinada sale de una proyección mía que falló en otra zona (dio por abiertos los cantos de las puertas, donde sí hay meseta). El caso vertical de E1 está confirmado aparte; los ángulos inclinados, no.
- El juego del aro combinando a la vez giro y desplazamiento con el tetón puesto: solo por muestreo (12 direcciones, 3 giros).
- La inclinación del tetón: rejilla de 0,1 mm y 0,5°.
- El brazo del aro contra tubo, columnas, satélites y bisel (no estaban en mi lista).
- El modelo de Fusion y los 3MF. Los pasos 1 a 3 y 11 a 13 del montaje.
