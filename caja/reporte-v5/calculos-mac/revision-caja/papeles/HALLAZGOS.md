# Auditoría del reporte de la caja v5 (`caja/reporte-v5/caja-entera.md`) contra el modelo

Hecha el 21-22 de noviembre de 2026 sobre la copia de trabajo. No se ha tocado el repositorio ni se ha usado git.
Todos los programas y sus salidas están en esta carpeta (`papeles/`). Se lanzan con
`python <programa>`; cada uno tiene su salida guardada al lado (`*_salida.txt`).

| Programa | Qué hace |
| --- | --- |
| `a1_cifras.py` | Medidas generales, bisel, dientes, volumen, tabla de piezas, tramos del recorrido |
| `a2_requisitos.py` | Junta, prisma de 50 × 59, distancias del reloj, los 10 imanes, rendijas del pedestal arriba |
| `a4_comprueba.py` + `a8_resto.py` | Las comprobaciones de `comprueba()` rehechas con paso fino; piezas de probeta; holgura real de los tetones |
| `a5_probetas.py` | Los nueve `.3mf`, sólido a sólido contra el modelo |
| `a6_voladizos.py`, `a6b_detalles.py` | Voladizos capa a capa; ala del bisel; diente; rendijas pasantes; JSON viejo; parámetros muertos |
| `a7_montaje.py`, `a9_llaves.py` | Orden de montaje del apartado 7 y posiciones equivocadas |
| `c3b_json.py`, `c3c_generador.py`, `c3d_fusion.py` | Coherencia entre ficheros |
| `regen/`, `regen2/`, `regen3/` | Fases 1 y 2 regeneradas (iguales a las del repo) y con un reloj mayor |

Clasificación: **ERROR** (el reporte afirma algo falso, hay un incumplimiento sin declarar o los ficheros no casan), **IMPRECISIÓN**, **OK**.

---

## A. ERRORES

### E1. El orden de montaje del apartado 7 no se puede seguir
- **Reporte:** «8. Rueda central sobre la meseta … 10. Plato sobre el tubo … 11. Los seis satélites en sus ejes, entre los dedos de la rueda central».
- **Modelo:** con la rueda central puesta, el plato **no entra** (pisa 9.313 mm³): su agujero mide 54,46 mm de radio y la rueda central llega a 60,0 (dientes), 61,5 (placa) y 74,3 (dedos). Los satélites tampoco (74,6 mm³ cada uno): la placa les tapa de 57 a 61,5 mm de radio y el eje les obliga a bajar en vertical.
- **Orden que sí entra en el modelo:** … pasadores → cerrar puertas y tetón → plato → satélites → rueda central → bisel y cuerpo. Comprobado pieza a pieza: 0 mm³.
- El autor solo comprobó el montaje de las puertas (una línea de la fase 2). El brief (11.8) pedía «que cada pieza se pueda meter, en qué orden».
- Programa: `a7_montaje.py`.

### E2. Con el reloj arriba, el pedestal no «rellena el hueco»: queda una zanja de 7,7 mm delante y detrás
- **Reporte:** «Pedestal arriba: a ras (0,00); rendija de 0,4 mm por lado»; «el pedestal rellena el hueco de las puertas y queda a ras». Brief: «rellena el hueco con 1 mm o menos de rendija por lado».
- **Modelo (corte a 0,05 mm bajo la cara de arriba, tubo a 345°):** a ras sí (0,00). Rendija a cada puerta, **0,9 mm**. Delante y detrás, **7,7 mm de ancho y 5 mm de hondo**, a todo lo ancho entre las puertas: es el rebaje donde apoyaban las puertas, que al abrirse queda al aire (el rebaje mide ±36,8 y el pedestal ±29,1). En su suelo se ven las ventanas de las manivelas. Los 0,4 mm solo son verdad por debajo de 5 mm de profundidad.
- Se ve en el paso 6 de `caja-apertura.png`. No está entre los incumplimientos del apartado 1.
- Programa: `a2_requisitos.py`, bloque E.

### E3. Los tetones de la plataforma tienen en la rampa 0,05-0,09 mm de holgura, no 0,2
- **Reporte:** «Cada tetón tiene 0,2 mm de holgura: si uno se levantara 0,28 mm … cabecearía 0,14°, que arriba del reloj son 0,25 mm».
- **Modelo:** en la hélice la plataforma solo se deja subir o bajar **0,05-0,07 mm** antes de pisar el tubo (tubo a 96°…334°); cabeceo libre máximo **0,07°**, que arriba del reloj son **0,13 mm**; de lado, 0,07-0,10 mm. En los tramos planos sí hay juego: 0,29-0,33 mm.
- **Por qué:** la ranura mide 3,20 mm de media altura *en vertical*, pero va inclinada 15,3°: en perpendicular son 3,087 mm para un tetón de 3,00 → 0,087 mm por lado.
- **Importa:** las holguras medidas en piezas impresas dicen que 0,15 «sujeta» y 0,20 «pasa sin forzar». Con 0,09 lo probable es que la plataforma se agarrote en la rampa. La comprobación del autor («bajarla 0,6 mm choca», «1,2 mm choca») era demasiado gruesa para verlo.
- Programas: `a4_comprueba.py` (bloque 5) y `a8_resto.py`.

### E4. La junta del centro tiene un agujero pasante
- **Reporte:** «Mirando desde arriba por la raya (0,3 mm) solo se ve puerta». Brief: «Sin agujero… no se ve lo de dentro».
- **Modelo:** en el centro hay una rendija de **0,3 × 1,2 mm** (x ±0,15; y ±0,6) que atraviesa las dos puertas: la cuña de cada puerta empieza a 0,6 mm del centro y en ese tramo no hay cuña de ninguna. Debajo está el reloj (a 10 mm). Es muy pequeña, pero es justo lo que el brief excluía.
- Además, dos rendijas de 0,1 × 11,8 mm en los extremos de las puertas, sobre las ventanas de las manivelas (debajo, el aro).
- La única comprobación de esto es de la fase 1 y está hecha sobre la junta en media madera, que ya no existe (ver C.a).
- Programas: `a2_requisitos.py` (bloque A), `a6b_detalles.py`.

### E5. Al abrir, las dos cuñas de la junta pasan a 0,08 mm una de otra, y chocan si una puerta se adelanta 2°
- **Fase 1:** «al abrir a la vez, el labio de una puerta y el rebaje de la otra no se tocan: lo más cerca, 0,30 mm» (criterio del autor: 0,2 o más). Está calculado con la media madera.
- **Modelo real (junta en bisel), de 0,25 en 0,25 grados:** abriendo las dos a la vez no se pisan, pero lo más cerca son **0,076 mm** (a 5,25°). Si una va 2° por delante de la otra se pisan 3,0 mm³; con 3°, 27,8 mm³.
- **Y a medio abrir cada puerta baila ±7°** contra su pista (a 15,6°: −7,40/+7,35; a 40,5°: −7,20/+7,70). El reporte solo da el juego de «cerrada» y «abierta».
- Consecuencia: «abrir y cerrar las hace el mecanismo» es verdad solo dentro de esos ±7°; que las dos vayan a la par lo pone la gravedad. Riesgo de enganche en la junta sin declarar.
- El barrido del autor mira las puertas a 0°, 7,1°, 15,6°…: no ve los primeros grados.
- Programa: `a4_comprueba.py`, bloques 2 y 3.

### E6. «El reloj siempre a 3,00 mm o más» y «hueco libre del todo» solo valen con las puertas exactamente a 90°
- **Reporte:** «el reloj de pega queda siempre a 3,00 mm o más de todo»; «50 × 59 mm, libre del todo con las puertas abiertas»; y a la vez declara que la puerta abierta puede quedar a 86,2°.
- **Modelo, nominal:** correcto (3,75 mm a las puertas; el prisma queda a 0,50 mm de cada puerta).
- **Con el juego que el propio reporte declara (86,25°):** el reloj queda a **1,78 mm** de la puerta y la puerta se mete **1,47 mm** en el prisma de 50 × 59 (a 89° ya lo toca; a 88°, reloj a 2,9 mm). Un taco de 50 × 59 no pasa si las puertas caen hacia dentro.
- No se tocan, pero el requisito de 3 mm «en todo el recorrido» no se cumple con el juego, y no se dice.
- Programa: `a2_requisitos.py`, bloques B y C.

### E7. La funda entra en las cuatro posiciones; el cuerpo, casi
- **Reporte:** «Funda: solo entra con su frente al frente (lleva un canal para el índice del cuerpo)»; «el cuerpo solo entra con el índice al frente».
- **Modelo:** el índice sobresale 0,60 mm y la funda tiene 0,50 mm de holgura por lado. Girada 90°, 180° o 270° pisa 1,5 mm³; desplazándola 0,3 mm, **0,000 mm³: entra**.
- El cuerpo girado pisa 9,1 mm³ (el pestillo ancho en una cajera estrecha). Pero el cuerpo entra a presión: en su montaje normal ya pisa 66,9 mm³ al pasar los cuatro pestillos. Girado ofrece menos resistencia que bien puesto; simplemente uno de los cuatro no hace clic.
- Programas: `a9_llaves.py`, `a7_montaje.py`.

### E8. «Ninguna pieza se puede montar del revés»: tres casos sin declarar
- **Soporte del reloj:** el pedestal es liso; solo lo coloca un imán redondo. Girado 90° o 180°, o corrido 5 mm, no pisa nada (0,000 mm³). De su posición dependen los 3 mm del reloj, así que algo depende de un imán (brief, apartado 2: «nada puede depender de ellos»).
- **Satélite azul:** los seis satélites son idénticos (diferencia 0,000-0,014 mm³) y cualquiera entra en cualquier eje. Nada obliga a que el azul salga del frente.
- **Satélites boca abajo:** son simétricos (0,000 mm³): «todos con la misma cara abajo» al imprimir no garantiza qué cara queda vista.
- Sí funcionan (una sola posición en un barrido de 0,5 en 0,5 grados): plataforma, tubo, marco, rueda central, plato, aro, anillo de probeta.
- Programas: `a7_montaje.py`, `a9_llaves.py`.

### E9. «Todas, sin soportes»: el bisel tiene un voladizo de 2,4 mm en todo su contorno
- **Reporte:** «Todas, sin soportes». **Código:** «ala en escalera: se imprime sin soportes».
- **Modelo:** el ala no es una escalera. El escalón más ancho es también el más alto, y la unión es un rectángulo liso de 2,4 × 3,0 mm: radio 83,575 a z = −11,30 y 85,975 desde z = −11,45. Impreso boca abajo es una repisa horizontal de 2,4 mm al aire en los 525 mm de perímetro (1.121 mm²). Es la cara que retiene el bisel, a 0,4 mm del labio del cuerpo.
- Otros voladizos que el reporte no menciona:
  - Tubo: tres techos planos de 2,8 × 20 mm al final de cada hélice, justo donde descansa el tetón arriba.
  - Tetón con pomo de la probeta: orientado con el pomo arriba, vuela 2,5 mm todo alrededor (basta darle la vuelta).
  - Aro: dos lengüetas de 4,1 mm.
  - Base: pestillos, 1,0 mm.
- Programas: `a6_voladizos.py`, `a6b_detalles.py`, `a8_resto.py`.

### E10. A la probeta 3 le falta una pieza: el tetón normal
- **Reporte:** probeta 3, «Con las otras dos probetas debajo: al girar el bisel pasa todo en su orden: nada, puertas, reloj».
- **Ficheros:** ninguno de los nueve `.3mf` lleva el tetón de 5 × 9. La bandeja A lleva solo el tetón con pomo, y ese pisa al plato (247 mm³): con él puesto no se monta el plato. Sin tetón normal las puertas no se mueven con el bisel.
- Lo demás de los `.3mf` es correcto (ver E).
- Programas: `a5_probetas.py`, `a8_resto.py`.

### E11. Cifras del reporte que no coinciden con el modelo

| Cifra del reporte | Valor del modelo | Programa |
| --- | --- | --- |
| «las puertas sobresalen 25,5 mm» (apartados 3 y 6) | **27,65 mm** (la mitad con cuña) y 25,35 (la otra mitad). 25,5 es la X de la cara de dentro | `a1_cifras.py` |
| «Diente más fino: la punta … 0,44 mm. A media altura, 1,12 mm» | **0,81 mm** en la punta, **2,26** en el primitivo, 2,33 a media altura. Las del reporte son medios gruesos | `a1_cifras.py`, `a6b_detalles.py` |
| «0,2 mm quitados a cada diente» | **0,1 mm** por diente (2,256 = 2,356 − 0,1); 0,2 entre los dos de una pareja. Juego real del bisel: 0,16-0,19 mm en el primitivo | `a1_cifras.py`, `a4_comprueba.py` |
| Reloj a «6,00 de la rueda central» | **18,3 mm**. 6,00 es el radio de búsqueda del programa; lo mismo las siete líneas «6.00» de la fase 2 (soporte: de 8,0 a 28 mm) | `a2_requisitos.py` C |
| Imanes más cercanos a la cabeza, «a unos 37 mm» | **33,95 mm** (soporte) y **35,05** (pedestal). Cumple los 30. Los otros ocho, entre 70 y 112 mm | `a2_requisitos.py` D |
| Pista: «como mucho 28° de inclinación» | **30,5°** (la fase 1 del propio autor dice 30) | `a1_cifras.py` |
| «25 piezas (más el reloj de pega)» | Las 25 del modelo **incluyen** el reloj de pega y la frase. Piezas que se imprimen: **23**, que es lo que suma la tabla del apartado 5 | `a1_cifras.py` |
| «rendija de 0,4 mm por lado» | Ver E2 | |
| Juego 0,28 mm / 0,14° / 0,25 mm | Ver E3 | |

### E12. `caja-v5.json` del repositorio es de una versión anterior del programa
- Tiene 61 parámetros; el código, 62 (falta `manivela_d`).
- Guarda la sección de la puerta en media madera y un juego de puertas de 2,75° / 2,15° que contradice el del reporte (3,75-4,0° / 3,0°).
- `caja-v5-piezas.json` sí corresponde al código (ver C.b).
- Programas: `c3b_json.py`, `a6b_detalles.py`.

### E13. Boca abajo: el reloj con su soporte cae 5 mm sobre las puertas
- **Reporte:** «Boca abajo no se cae nada: Bien».
- **Modelo:** cada pieza de la caja, sola, se para en 0,4 mm o menos (correcto). Pero soporte y reloj, que van sueltos, suben juntos **5,0 mm** hasta apoyar en las puertas por dentro, y las empujan en el sentido de abrir. Con la caja abierta, nada los para. La lista del autor no los incluye.
- Es consecuencia de «soporte suelto» (brief), pero había que decirlo.
- Programa: `a8_resto.py`.

---

## B. IMPRECISIONES

1. **Medida de la caja.** «178,8 × 178,8»: de fondo son 179,35 con el índice (0,6 mm).
2. **Tabla 2.3, fila «83° a 92°: el aro termina su giro».** El aro termina a 100° de tubo. A 92° lleva 10,44° de 11, y entre 92° y 100° el reloj ya sube 2,9 mm. Las puertas no se mueven en ese tramo.
   A 83° la puerta «ya de pie» aún puede caer 10,95° hacia dentro; queda bloqueada (3,65°) desde 92°. El reloj no llega a su altura hasta ~106°.
3. **Juego de las puertas.** Los 3,0° / 3,75° / 4,0° son el primer ángulo que «pisa más de 0,02 mm³» con paso de 0,25°. Libre de verdad: 2,85° cerrada (2,15° si la otra puerta está cerrada, porque las cuñas se traban), 3,65° hacia dentro y 3,95° hacia fuera. Primer roce (umbral 0,001 mm³): 2,30° / 2,95° / 3,15°. El rango «86,2 a 94,0» vale.
4. **«Se abren mientras el reloj sube» (D-29).** En el modelo es una cosa detrás de otra: puertas de 62,4° a 82,6°, reloj desde 92°. El brief lo permite; el reporte lo dice con otras palabras.
5. **«Si el reloj es más ancho… la caja crece» y «se regenera todo».** En alto sí. En planta no: con +1 mm de ancho *y* de fondo (o +2 en uno) la fase 1 da FALLA y el lado sigue en 179. Hay que retocar a mano `z_central` y `tubo_r`. Margen actual: ~1 mm (`regen3/`, `a6_reloj_mayor.txt`).
   El hueco sale de `reloj_ancho` y `reloj_fondo`, no de las medidas «supuestas» (`reloj_con_corona`, `brazalete_*`): cambiar solo estas no mueve el hueco.
6. **«Todas las medidas en una lista» (brief 11).** `caja_piezas_v5.py` tiene decenas de medidas fijas fuera de la lista (ángulos de columnas y llaves, cajeras de imán, índice, 120 estrías, funda, pestillos, soporte). `labio_grueso` no cambia ninguna pieza. Los comentarios de `labio_*` y `puerta_cola` describen la media madera.
7. **Fusion, «46 por posición».** 46 es solo la primera; el resto, 35-49 (media 38,5).
8. **Mallas del ascensor.** El reporte dice «aristas compartidas por más de dos caras» en los dos ficheros. En el tubo son 44 aristas **abiertas** (72 mm en total, ninguna de más de dos caras); en la plataforma, 12 abiertas y 4 de más de dos caras. El volumen cuadra (+0,09 % y 0,00 %).
9. **«Seis dedos rectos de 8 mm».** Son sectores de 7°: 7,4 mm en la raíz y ~9 en la punta.
10. **«La meseta es simétrica».** No del todo (325,9 mm³ distintos, por las llaves a 20°, 140° y 255°). Girada 180° entra y obliga a girar también la rueda central, que queda igual: sin consecuencia.
11. **Pendiente «15,0° donde apoyan los tetones».** 14,99° a 77,5 mm de radio; 15,27° en la boca.
12. **Volumen 1.367 cm³.** Coincide (1.366,7) sin contar reloj de pega ni soporte.
13. **`caja-fusion-comprobaciones.txt`.** Tiene una línea «corregida a mano», y el recorrido completo (punto 2) es de un modelo anterior («el de las 16:40»). El reporte lo cuenta.
14. **Generador.** `parametros()` solo traduce «mm» y «grados», y la lista usa «deg»: los siete ángulos irían a Fusion sin unidad. Además `main()` no llama a `parametros()`.
15. **Probeta de puertas boca abajo.** Además del anillo (que el reporte dice que se sujete), el tetón con pomo se cae con las puertas cerradas: nada lo para.

---

## C. Coherencia entre ficheros

**(a) Fase 1 y la junta en media madera.** `caja-fase1-comprobaciones.txt` se regenera idéntico, pero estas líneas hablan de geometría que ya no existe:

| Línea de la fase 1 | Qué pasa | ¿Hay equivalente sobre la geometría real? |
| --- | --- | --- |
| «no hay ninguna línea recta que cruce la junta: el labio de 2.0 mm la tapa» | Media madera | No. Hecho aquí: E4 |
| «al abrir a la vez… 0,30 mm» | Media madera | Solo el barrido de 2° de tubo (puertas a 0°, 7,1°, 15,6°…). Hecho aquí: E5 |
| nota «sobresale 27,7 mm» | Media madera; por casualidad coincide con el real (27,65) | El reporte da otra cifra (E11) |
| «reloj a 3,50 mm de las puertas» | Reloj como caja de 44 mm | Sí: 3,75 en 3D |
| «abierta baila 2,8° y cerrada 2,2°» | Fórmula | Sí: 3D da otros valores (B3) |
| «rueda central… entra en el cuello del marco»; «el bisel apoya en el canto del tubo» | Disposición anterior (ahora meseta y plato) | — |
| «queda 3,7 de pared» entre ranuras | Supone tetones a 120° exactos | Real: 2,57 mm (`a8_resto.py`). Suficiente |
| nota «cabecear 0,15°, 0,3 mm» | Fórmula | Reporte 0,14°/0,25; 3D 0,07°/0,13 (E3) |

**(b) `caja-v5-piezas.json`.** Regenerado en `regen/`: 27 piezas, las mismas operaciones y los mismos volúmenes (diferencia 0,0000 mm³); `d2`, `mov`, `cte`, `P` y `D` iguales. Única diferencia: las 120 estrías del bisel salen en otro orden; la figura es la misma (0,000000 mm²). **OK.** `caja-v5.json`, no (E12).

**(c) `generador_caja_v5.py`, leído entero.** Reproduce las seis operaciones y el orden suma/resta. **OK.**
- Prisma en X, Y y Z: mismas cajas que `solido()` (probado con un prisma de prueba); matrices sin espejo.
- Cilindro, cono, esfera: exactos en Fusion; 48 caras en el programa, de ahí el +0,29 %.
- Revolución: simétrica y luego girada, mismo sector; manifold gira de +X a +Y, como supone.
- Hélice: prueba los dos sentidos y se queda con el que contiene un punto de control, coherente con manifold.
- Ninguna pieza empieza por una resta. Ninguna se trata distinto; «probeta» se excluye de montaje y barrido, y «funda» del barrido, igual que en el programa.
- Tres matices: la comparación de volumen admite 1,2 % y no detecta una operación mal colocada (eso lo cubre el barrido); `vol_inter()`, si Fusion falla, separa las piezas ±0,02 mm y se queda con el menor **sin anotarlo**; y lo de las unidades (B14).

**(d) `caja-fusion-comprobaciones.txt`.**
- Las 27 piezas están y la columna «programa» es el volumen del JSON en las 27. Mayor diferencia, 0,31 % (tetón y pasadores). **OK.**
- Constan las tres cosas que el reporte dice hechas en Fusion: volúmenes, recorrido de 174 posiciones (98-117 parejas, 0 fallos) y repetición parcial (174 posiciones, 35-49 parejas, 0 fallos).
- Rehíce el recuento de parejas con el modelo actual: coincide en 167 de 174 posiciones (en las otras, 1-3 parejas de diferencia por cajas que se tocan justo). El segundo barrido cubre lo que dice. **OK.**
- No consta en Fusion (el reporte lo dice): distancias del reloj, juegos, boca abajo, topes.

---

## D. Las comprobaciones de `comprueba()` (fase 2), línea a línea

| Línea «bien» | ¿Lo demuestra? | Rehecho |
| --- | --- | --- |
| Ninguna pieza pisa a otra | Sí, en posición nominal. No mira las piezas de probeta ni el efecto de los juegos | 345 posiciones intermedias (0,5°, 1,5°…): ninguna. Tubo 44°-104° de 0,1 en 0,1: ninguna. Piezas de probeta: ninguna |
| Reloj y soporte a cada cosa | 5 líneas buenas (3,00 / 3,00 / 3,50 / 3,75 / 3,75). Las 7 que dicen «6.00» son el tope de búsqueda | Reales: rueda central 18,3; soporte de 8,0 a 28; pasadores 4,75 |
| Cerradas y bloqueadas | Sí, solo contra el aro y solo a 0° | 2,85° libre; 2,15° con la otra puerta. A 58° y 62° de tubo (aro ya girando) contra el aro solo: 3,3° y 7,4° |
| Abiertas y bloqueadas | Sí, solo a 345° | Igual a 92°, 100° y 345° (3,65 / 3,95). A 83°, 10,95° hacia dentro |
| Montaje de las puertas | Sí, pero es la única pieza cuyo montaje se comprueba | El resto: E1 |
| Tetón guiado | Prueba floja (1,2 mm, una posición) | Juego real en 9 posiciones: ±0,22 mm radial y de lado; aro ±0,24-0,28°. Bien |
| Plataforma no se hunde | Abajo, sí (0,15). En la rampa «0,6 mm choca» da bien con cualquier holgura menor de 0,6 | Real: 0,07 mm (E3). Arriba: baja 0,29 |
| Plataforma guiada | Prueba floja (1,2 mm; 2°) | ±0,07 mm; giro ±0,28° (el reporte dice 0,29: coincide) |
| Los dientes engranan | Solo satélite 1, a 0°, medio diente | Los seis dan lo mismo (50,1 y 58,9 mm³); juego ±0,56° por satélite |
| Topes | Sí | Paran a 0,00° de pasarse, en los dos extremos |
| Boca abajo, cada pieza | Lista de 13, una por familia y contra quien el autor eligió; faltan soporte y reloj | Todas las piezas contra todas: se paran en 0,4 mm o menos. Soporte + reloj: E13 |
| Pasadores | Solo el derecho, a 1,5 mm | Los dos corren ±0,45 mm. Bien |
| Lo que se descuelga | Sí | Bisel 0,4; rueda central 0,2. Coincide |
| La funda | Distancia a 4 piezas; no prueba la llave | 0,5 mm a base y cuerpo, 1,0 a bisel y puertas. La llave falla (E7) |
| A ras | Solo mira el punto más alto de cada pieza | Cierto. No ve la zanja (E2) |

---

## E. Probetas y sus nueve `.3mf`

Contenido, comparado sólido a sólido con el modelo (`a5_probetas.py`):

| Fichero | Contiene | Orientación | Diferencia con el modelo |
| --- | --- | --- | --- |
| puertas-bandeja-A | marco, 2 puertas, 2 pasadores, tetón con pomo | marco de pie; puertas boca abajo; pasadores tumbados; tetón con el pomo arriba (E9) | 0,00-0,07 %; pasadores −0,86 % (facetas) |
| puertas-bandeja-B | meseta, aro, anillo | meseta y aro de pie; anillo boca abajo | 0,00 % |
| ascensor-base | base | de pie | 0,00 % |
| ascensor-tubo | tubo | de pie | malla abierta: solo volumen (+0,09 %) y caja |
| ascensor-plataforma | plataforma | de pie | malla abierta: solo volumen (0,00 %) y caja |
| planetario-plato | plato | espiral en la cama | 0,02 % |
| planetario-rueda-central | rueda central | boca abajo | 0,01 % |
| planetario-bisel | bisel | boca abajo | 0,04 % |
| planetario-satelites | 6 satélites | planos | 0,00 % |

- Cada fichero lleva lo que dice el reporte y solo eso. **OK.** Bandeja A: 231 × 157 mm; cuerpos separados 13-24 mm en la B.
- **Falta** el tetón normal (E10).
- **Probeta 1:** completa para lo que describe. Dos avisos: el tetón con pomo se cae boca abajo (B15), y pasa a 0,20 mm del marco y a 0,70 de la meseta (no pisa nada en todo su recorrido).
- **Probeta 2:** completa. Aviso: es donde saldrá E3.
- **Probeta 3:** no se puede probar sola, y el reporte lo dice. Le falta el tetón.
- **Tablas «vale si» frente al brief (apartado 12):**
  - Puertas: están las siete líneas del brief y tres añadidas. Faltaría una línea para la junta al abrir (E5).
  - Ascensor: cubre pendiente, juego y si se sujeta sola.
  - Planetario: cubre tacto, juego y dientes.

---

## F. Requisito por requisito del brief

| Requisito | Resultado | Prueba |
| --- | --- | --- |
| **Ap. 2** Caja cuadrada; se gira el bisel; planetario con satélites que orbitan; un satélite azul; reloj de pie, esfera al frente | Cumple | `a1`, movimiento |
| Puertas que se abren solas mientras el reloj sube | A medias (una cosa tras otra; permitido) | B4 |
| Bisel grafilado | Cumple: 120 estrías de 2 × 0,6 mm, en 7 de los 8 mm que asoman | `a1` |
| Índice del frente, en relieve, bajo el bisel | Cumple: 2 × 7,5 × 0,6 mm | código, `a9` |
| Tramo muerto | Cumple: 0°-45° de tubo (79° de bisel); a la vista, nada hasta 62° | `a1` |
| Satélite azul sale del frente y vuelve casi | Cumple en el modelo (270° → 285°). Nada obliga a montarlo ahí | E8 |
| Imanes de adorno; nada depende de ellos | A medias: la posición del soporte | E8 |
| Tapa lisa; sin trinquete; funda con frase y NFC | Cumple (rebaje de 26 mm para la etiqueta) | código |
| **Ap. 6** Cerradas: mismo plano | Cumple (0,00) | `a2` |
| Cerradas: sin agujero | **No cumple, sin declarar** | E4 |
| Grueso 3 mm o más | Cumple (5; canto de 1,4 declarado) | `a2` |
| Abiertas entre 85° y 95°, sujetas | Cumple con juego (86,35°-93,95°) | `a4` |
| Abrir y cerrar por el mecanismo | A medias: ±7° a medio abrir, sin declarar | E5 |
| Reloj a 3 mm de las puertas | Nominal sí; con el juego, 1,78. **Sin declarar** | E6 |
| Hueco libre 50 × 59, nada entra | Nominal sí; con el juego, no. **Sin declarar** | E6 |
| Plataforma recta; decir juego y cabeceo | Dicho, con cifras que no son las del modelo | E3 |
| Pedestal a ras y rendija de 1 mm o menos | A ras sí; rendija **no, sin declarar** | E2 |
| Tramo plano y tope arriba y abajo | Cumple | `a4` 5 y 7 |
| Seis satélites engranan y orbitan | Cumple | `a4` 6 |
| Decir módulo, juego y diente más fino | Dicho, con dos cifras mal | E11 |
| Bisel no se saca; no toca el cuerpo | Cumple (2,0 mm bajo el labio; 0,395 mm) | `a8` |
| Boca abajo no se cae nada | Piezas, sí. Reloj y soporte, no | E13 |
| Ninguna pieza del revés | **No cumple, sin declarar** | E7, E8, E1 |
| Sin imanes funciona igual | Cumple, salvo colocar el soporte | E8 |
| Cabe en la impresora; orientación y soportes | Cabe. «Sin soportes», no | E9 |
| Mismo acabado por familia | Puertas sí (las dos boca abajo en el `.3mf`); meseta, declarado | `a5` |
| **Ap. 7** Ninguno a menos de 30 mm de la cabeza | Cumple los 10, reloj abajo, arriba y en todo el recorrido: mínimo 33,95 | `a2` D |
| Imán contra imán | Cumple (parejas a 1,46, 2,00 y 0,00 mm). Los 10 caben en sus cajeras | `a2` D |
| Nueve imanes | Diez, declarado | |
| **Ap. 11** Pasos de 2° o menos | Cumple (174); «ida y vuelta», declarado como iguales | |
| Tabla por posición | Está (en `caja-v5.json` grado a grado y en el fichero de Fusion) | |
| Orden de montaje | **No cumple** | E1 |
| Lista de medidas | A medias | B6 |
| Entregables | Están todos. El `.f3d` no se ha podido abrir | |

**Lo que el apartado 1 del reporte declara** (tamaño, descuelgue boca abajo, 10 imanes, imanes pegados, soporte simplificado) es cierto. **Lo que no declara:** E1, E2, E3, E4, E5, E6, E7, E8, E9, E13.

---

## G. Silencios: cosas del modelo que quien imprima debería saber

1. Los tetones van a 0,09 mm en la rampa (E3). Es lo primero que fallará en la probeta del ascensor.
2. La junta pasa a 0,08 mm al abrir y las puertas bailan ±7° a medio camino (E5). Se ajusta con `labio_hueco` (1,2).
3. La zanja alrededor del pedestal con el reloj arriba (E2): es lo que Pepe verá de día.
4. El ala del bisel y los techos planos del tubo (E9).
5. Boca abajo, todo el interior cuelga del bisel, y este del labio del cuerpo y de cuatro pestillos de 1 mm.
6. Las cajeras de imán del cuerpo y de la funda abren hacia abajo: sin pegamento o apriete, se caen. El reporte lo roza en la fila 4.
7. La meseta tiene una piel de 0,7 mm sobre las cajas de las orejas del marco, en la cara vista, junto a las puntas de los pasadores. Y sus bolsillos de abajo son puentes de hasta 9,5 mm.
8. Bajo los tramos planos de abajo, el canto del tubo arranca con 0,15 mm de material (menos de una capa).
9. Margen de ~1 mm si el reloj resulta más ancho y más hondo (B5).
10. El tubo tiene 1,6 mm de pared detrás de las ranuras.

---

## H. Comprobado y bien

- Fases 1 y 2 regeneradas: idénticas a las del repositorio. `caja-v5-piezas.json`, idéntico.
- Medidas: 178,75 × 122,6; con funda 183,75 × 126,0; bisel 167,15 (171,95 con el ala), asoma 8, 120 estrías; hueco 50 × 59; puertas de 5, raya 0,300, bisagra 0,25; recorrido 88,0; 73,88 mm por vuelta de bisel; relación 0,5667; 608,8° de bisel (1,69 vueltas); dientes 78 / 12 / 102, módulo 1,5, grueso 6.
- Tabla del recorrido (0-45-63-83-92-335-345 y sus grados de bisel), salvo B2. Aro, 11,0°; tetón, 13 mm.
- Las 17 filas de medidas de la tabla de piezas coinciden con las cajas del modelo (redondeadas). Pasadores, 89,95 mm.
- Distancias del reloj: 3,000 a meseta y marco, 3,500 al aro, 3,750 a las puertas.
- Ninguna interferencia en 174 + 345 + 601 posiciones.
- Topes exactos; satélites idénticos y los seis engranan; bisel retenido.
- Diez imanes, sitios y distancias (salvo la cifra de 37).
- Volumen 1.367 cm³; las 27 piezas de Fusion contra el JSON.
- Generador fiel al programa. Siete de los nueve `.3mf` son sólido a sólido las piezas del modelo, bien orientadas.

## I. No se pudo comprobar

- `Eventually-caja-v5.f3d`: no hay Fusion aquí. Que el modelo de Fusion sea el final solo consta por los volúmenes del fichero de texto.
- Que las piezas no cambiadas fueran iguales en «el modelo de las 16:40» (no hay copia de ese modelo; no se ha usado git).
- Las dos incidencias de Fusion que cuenta el reporte (lámina de 0,04 mm en el bisel; corte del tubo).
- Los `.3mf` del tubo y de la plataforma, sólido a sólido: sus mallas no son cerradas. Solo volumen y caja.
- «Te dije 177», «quedaría a 4 mm de su pareja», «unas 11 bandejas», «tardó 30 minutos»: sin fuente en el modelo.
- Todo lo que depende de imprimir: roce, si la rampa sujeta, si los voladizos salen, si las mallas abiertas las repara el laminador.
