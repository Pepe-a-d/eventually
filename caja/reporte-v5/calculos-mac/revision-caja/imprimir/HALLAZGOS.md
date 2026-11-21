# Revisión de imprimibilidad de la caja v5: hallazgos

Revisado: las 20 piezas del modelo (manifold3d) en la postura de la tabla del apartado 5 del reporte, cortadas en capas de 0,2 mm, y los nueve `caja-probeta-*.3mf`. No se ha tocado el repositorio.

**Conclusión:** la frase «Todas, sin soportes» no se cumple en tres sitios (bisel, aro de las puertas y el tetón con pomo tal como viene en su .3mf). Todo cabe en la bandeja, ninguna pieza sale en varios trozos y no hay islas que empiecen en el aire.

Cómo se reproduce (desde esta carpeta, con `PY=python`):

- `$PY capas.py [pieza]` : voladizos, puentes, islas, finos, primera capa. Salidas en `sal-<pieza>.txt` y `capas-<pieza>.json`.
- `$PY detalle.py <pieza | fichero.3mf:n> z0 z1` : capa a capa entre dos alturas de impresión.
- `$PY -I tresmf.py` : los nueve .3mf (`sal-3mf.txt`). `$PY -I capas3mf.py` : el análisis por capas sobre los cuerpos de los .3mf (`sal-3mf-capas.txt`).
- `$PY medidas.py` (dientes, letras, paredes finas, pasador: `sal-medidas.txt`), `$PY laminas.py` (pieles de 1 a 4 capas: `sal-laminas.txt`), `$PY tubo_v.py` (ángulo de las V: `sal-tubo_v.txt`), `seccion.py` y `dibuja.py` (dibujos en `dib/`).

Coordenadas «de impresión»: z = 0 en la cama. Coordenadas «de la pieza»: las del modelo.

---

## ERRORES

### E1. Bisel: el ala no es una escalera, es una repisa plana de 2,4 mm en todo el contorno

- **Dónde:** bisel boca abajo, z de impresión 11,4 (pieza z = -11,4), radios 83,575 a 85,975, los 360°.
- **Cifra:** 1.277,8 mm² de capa sin nada debajo (1.162,7 mm² a más de 0,2 mm de la capa anterior); voladizo de 2,40 mm; no es puente (no hay segundo apoyo).
- **Causa:** en `caja_piezas_v5.py`, líneas 369-370, los tres escalones (0,8, 1,6 y 2,4 mm de ancho) tienen las alturas al revés: el de 2,4 llega hasta arriba del todo (z = -11,4) y los otros dos quedan dentro de él. La sección real es un rectángulo de 2,4 × 3,0 mm. Para que fuera escalera imprimiendo boca abajo, el ancho de 2,4 tendría que acabar en -13,0 y el de 0,8 en -11,4.
- **También en el fichero:** `caja-probeta-planetario-bisel.3mf` tiene lo mismo (misma cifra).
- **Consecuencia:** esa cara es la que retiene el bisel bajo el labio del cuerpo (0,4 mm de aire). Saldrá descolgada.
- **Reproduce:** `$PY detalle.py bisel 11.0 12.0`; `$PY -I detalle.py caja-probeta-planetario-bisel.3mf:1 11.0 12.0`; sección: `$PY seccion.py bisel 0.75 dib/bisel-seccion.svg 68 0 88 14.4` (el contorno va de (83,57; 11,40) a (85,97; 11,40) en horizontal).
- Aviso: aun corregida, cada escalón de 0,8 mm es un voladizo plano de 0,8 mm (dos hilos). Eso sale, pero no es 45°.

### E2. Aro de las puertas: el extremo de cada cuerno cuelga por dentro del anillo

- **Dónde:** donde empiezan los cuernos, z de impresión 3,0 (pieza z = -15,2). En la pieza: x 10,1 a 17,9, y 33,2 a 37,7, y su simétrico (x -17,9 a -10,1, y -37,7 a -33,2). Es la pared que rodea el final de la pista por el lado de «abierto».
- **Cifra:** 12,28 mm² por cuerno sin nada debajo; lo más lejos del anillo, 4,32 mm. Es un gancho de pared de 2 mm unido solo por su raíz (unos 2 mm de ancho), que acaba en punta: el recorte del hueco deja una ranura de alrededor de 1,5 mm (medida en el dibujo) entre esa punta y la otra pared. Voladizo, no puente.
- **Causa:** el cuerno (`caja_piezas_v5.py`, línea 153) llega hasta radio 35, y el anillo empieza en 39,07.
- **También en el fichero:** `caja-probeta-puertas-bandeja-B.3mf`, cuerpo 2 (12,28 mm², 4,32 mm).
- **Consecuencia:** las primeras capas del gancho se imprimen en el aire. Es el tope de las puertas abiertas; la bola toca la pared entre z de impresión 7,5 y 11, así que el daño estaría abajo, pero la pared entera nace mal.
- **Reproduce:** `$PY capas.py aro_puertas`; `$PY -I detalle.py caja-probeta-puertas-bandeja-B.3mf:2 2.8 4.0`; dibujo en `dib/aro-3.1-zoom.svg.png`.

### E3. El tetón con pomo viene en su .3mf con el pomo arriba (seta)

- **Dónde:** `caja-probeta-puertas-bandeja-A.3mf`, cuerpo 6. El vástago de 5 mm está en la cama y el pomo de 10 mm empieza a z 6,5.
- **Cifra:** 58,67 mm² de corona sin apoyo, voladizo de 2,52 mm en todo el contorno. Apoyo en la cama: 19 mm² para 12,4 mm de alto.
- **Arreglo:** darle la vuelta (el pomo en la cama): así no tiene ningún voladizo. No está en la tabla del reporte; el fichero dice estar «ya orientado».
- **Reproduce:** `$PY -I detalle.py caja-probeta-puertas-bandeja-A.3mf:6 6.0 7.2`; `$PY capas.py probeta_teton`.

---

## RIESGOS (saldrá, pero al límite)

De más a menos importante.

1. **Puertas, la bola (5 mm).** Su parte de abajo empieza casi en el aire: en z de impresión 5,7 a 6,3 quedan 0,55, 1,41, 0,69 y 0,23 mm² por capa a más de 0,2 mm de la capa anterior; alcance 0,98 mm. El primer disco de la bola solo pisa 0,1 mm de varilla. Son pocos mm², pero es la bola que corre con 0,15 mm de holgura, y ese punto queda mirando hacia fuera con la puerta abierta. Igual en el .3mf (0,37, 1,51, 0,74, 0,26). La varilla va a 45° exactos: bien.
2. **Tubo, techo plano al final de cada hélice.** z de impresión 94,6 (pieza z = -23,4), tres sitios (pieza (25, 72), (-75, -20), (55, -54)): 37,5 mm² cada uno, 2,8 mm de fondo, puente de 19 mm con un borde libre (la cara interior). Queda justo encima del tetón cuando la plataforma está arriba, con 0,2 mm de holgura. Si el puente se descuelga, roza. Igual en el .3mf (37,1 mm², 19 mm).
3. **Tubo, lámina de una sola capa en el arranque de cada hélice.** En la cama, tres trapecios de 37,4 mm² (unos 22 × 2,8 mm) que solo existen en la primera capa: el suelo de la ranura queda a 0,2 mm de la base del tubo. Se imprime (está en la cama), pero es una telilla de 0,2 mm en la cara que resbala sobre la base. Igual en el .3mf (36,9 mm²).
4. **Meseta, techos sobre las ventanas de los cuernos.** z de impresión 1,44 (pieza z = -6,56): dos de 171,5 mm² y dos de 123,7 mm² (590 mm² en total). Puentes de 12,3 mm los pequeños y de 17 a 24 mm los grandes; círculo inscrito de 10 mm. Debajo pasa el cuerno del aro a 0,6 mm. Igual en el .3mf.
5. **Plato, techo de los tres cajeados de las almenas.** z de impresión 3,0: 62,5 mm² cada uno (17 × 3,75 mm), puente de 17 mm con el borde de fuera libre. La almena del tubo queda a 0,2 mm de ese techo: si se descuelga, el plato apoya en las almenas y sube.
6. **Base, pestillos, y cuerpo, sus cajeras.** Pestillos: voladizo plano de 1,0 mm, tres de 12 mm (12,0 mm²) y uno de 20 mm (20,0 mm²), z de impresión 6,2. Cajeras del cuerpo (boca abajo): techo de 1,15 mm de fondo, 12,6 y 20,6 mm de largo, z de impresión 108,7. Las dos caras que se descuelgan son las que se enfrentan, y entre ellas hay 0,3 mm.
7. **Meseta, cara vista.** Sobre cada caja de oreja queda una piel de 0,7 mm (4 capas), 24,1 mm² × 4, en puente de 12,2 mm con un borde libre. Sobre los agujeros de los pasadores, piel de 0,85 mm.
8. **Meseta, canto en filo.** Entre el hueco y la cuna de cada bisagra queda una aleta de 59 mm que se afila hasta cero: 0,83, 0,53, 0,28 y 0,05 mm de ancho en las capas de z 1,9 a 2,5. Las dos últimas no saldrán.
9. **Aro, pared de la pista de 0,30 mm.** En el extremo de «cerrado» la pista queda a 0,30 mm del borde exterior del aro: tramo de 2,5 mm de largo con menos de 0,3 mm de pared y de 4,9 mm con menos de 0,4, en los 8 mm de alto. Ahí la pared no saldrá o saldrá como un pelo. No es la pared que trabaja.
10. **Plataforma, alma de 0,75 mm.** Cada muesca de columna queda cerrada por fuera con una tira de 0,75 mm de ancho, 21,7 mm de largo y 6 mm de alto (tres). Menos de dos hilos.
11. **Paredes de 0,7 mm junto a las ranuras de imán.** Dos en la oreja del tubo y dos en el tope de la base (unos 4,5 × 0,7 mm, 5,3 mm de alto). Son las caras que chocan en el tope. Los techos de las ranuras son puentes de 1,75 mm: bien.
12. **Dientes.** Punta del satélite 0,42 mm (0,72 a medio milímetro de la punta); rueda central 0,56; bisel 0,62. Un solo hilo en la punta.
13. **Frase.** El 66 % del área de las letras tiene menos de 1,0 mm de ancho y el 9,5 % menos de 0,8 (un solo hilo); menos de 0,5, casi nada (0,3 %). Dentro de las letras quedan 6 islas de funda en la primera capa, cuatro de ellas de 1,2 × 3,3 mm (1,97 mm²). En 11 sitios la funda entre letras tiene menos de 0,4 mm.
14. **Pasadores tumbados.** Apoyo en la cama de 1,07 mm de ancho por 90 mm. Las dos primeras capas salen 0,36 y 0,22 mm por lado (61° y 47°): la cara de abajo no queda redonda. Entran en agujeros horizontales de 3,3 y 3,5 mm cuyos techos también se aplanan (puentes de 1,4 a 1,7 mm).
15. **Puertas, piel de 0,75 mm** (4 capas) por encima y por debajo del agujero del pasador, en los 73 mm. No es fallo de impresión; es poco material en la bisagra.
16. **Soporte del reloj (provisional).** Travesaño en puente de 23,2 mm × 6 mm, z de impresión 15,2, entre dos mejillas de 2,9 × 6 mm.
17. **Cuerpo, índice del frente.** Empieza a 1,5 mm de la cama y sale 0,6 mm: 1,2 mm² en voladizo en una cara vista.
18. **Rueda central y anillo de probeta, labio de 0,8 mm** (4 capas) × 1,5 mm de ancho, en la cama. Es lo que sujeta la meseta boca abajo.
19. **Dos .3mf no son estancos.** `ascensor-tubo`: 44 aristas con una sola cara (72 mm de costura abierta, todas en la cara interior, radio 76,0, z de 4,5 a 59,6); ninguna con más de dos caras, que es lo que dice el reporte. `ascensor-plataforma`: 12 aristas sueltas y 4 con cuatro caras, todas en un solo tetón (pieza (66, -39)). Los volúmenes cuadran (+0,09 % y 0,00 %) y manifold3d los acepta tras soldar vértices. Los otros siete, limpios.
20. **Bandejas justas.** `puertas-bandeja-B` ocupa 224,5 × 240,0 mm: 8,0 mm de margen por lado en Y. `puertas-bandeja-A`, 231,2 × 157,0: 12,4 mm en X.

Datos que no son error:

- Ranuras en V del tubo: el techo va a 48° en los tramos planos (máximo 52°) y hasta 51° en la hélice en el modelo; en el .3mf, 51-53° en todo. No son 45°, pero quedan lejos de necesitar soporte.
- Plato, techo de la espiral: puente de 5,4 a 5,9 mm en toda su longitud (2.074 mm²).
- Marco y base: cajas de espigas con puente de 4,4 mm. Soporte: cajera de imán con puente de 5,2 mm.
- Bisel: el final de las estrías son puentes de 2 mm. Dedos de la rueda central y cuña de la junta de las puertas: 45° exactos.
- Varias alturas no caen en múltiplo de 0,2 (por ejemplo el techo de 1,44 de la meseta): el laminador redondea.

---

## Comprobado y bien

- **Tamaño:** la mayor es la funda, 183,75 × 183,75 × 126,0 mm; todas caben en 256 × 256 × 256 con 36 mm o más por lado. Las medidas de la tabla del reporte coinciden con el modelo.
- **Trozos:** cada pieza es un solo cuerpo (la frase, 24 trozos de letra, como debe). Ninguna isla empieza en el aire en ninguna pieza ni en ningún .3mf.
- **Primera capa:** el centro de gravedad cae dentro del apoyo en todas. La meseta apoya en dos trozos de 2.599 y 2.584 mm² que se unen a z 1,44. La funda con la frase llena el cuadrado entero (33.764 mm², sin huecos) y la capa de encima de la frase queda apoyada.
- **Caras vistas en la cama:** bisel, rueda central, puertas, cuerpo (labio) y funda (techo), como dice la tabla. La frase se lee al derecho vista desde fuera.
- **Sin voladizos:** base (salvo pestillos), tubo (entradas, oreja con su cartela, V), cuerpo (labio en la cama, cajeras de imán abiertas hacia arriba), funda (rebaje del NFC, pies y cajeras de imán abiertos hacia arriba), plataforma (tetones en cono de 45°), marco (orejas, ranura del tetón), satélites, tetón, techo cónico y dientes del bisel, asiento y aro de centrado de la base, espigas de las columnas.
- **Los nueve .3mf:** unidades en mm; z mínimo 0,000 en los 21 cuerpos; cada cuerpo es la pieza que toca, con diferencia simétrica de 0,0 a 20 mm³ (200,8 mm³ en el tubo, 0,09 %, repartidos por la hélice). Posturas como en la tabla: base, plataforma, tubo, plato, marco, meseta y aro de pie; bisel, rueda central, puertas y anillo boca abajo; pasadores tumbados. Separación mínima entre cuerpos: 5,00 mm (bandeja A), 12,95 (B), 5,02 (satélites). Ninguno se pisa.

## No comprobado

- No se ha laminado nada en Bambu Studio: los puentes y voladizos salen de geometría, no del laminador. Cuánto se descuelga cada uno solo lo dice una pieza impresa.
- No hay .3mf de cuerpo, funda con frase, soporte ni tetón suelto: de esas piezas solo se ha visto el modelo.
- No se ha abierto el `.f3d`.
- Los .3mf se han leído interpretando el XML y pasando la malla a trimesh (su lector propio pide `lxml`, que no está instalado).
- Sitio para la torre de purga de la funda (dos colores): con la funda centrada quedan 36 mm por lado; no se ha comprobado en el laminador.
- Adherencia, alabeo de las placas grandes (base y funda) y vibración de las columnas (7,7 × 19,6 mm de sección, 96 mm de alto): no se pueden sacar del modelo.
