# Eventually, la caja: resultados de las probetas

Lo que han dicho las piezas impresas. Cada resultado lleva la fecha y quién lo midió.

## Probeta 1 de la v5: el iris (21 de noviembre de 2026): VALE con láminas de 1,2 y de 0,8 mm

Impresa, montada y probada por Pepe en la Bambu Lab X1 Carbon, a capa de 0,2 mm. Ficheros de `caja/probetas-v5/`. Apuntado por la sesión del PC a las 14:45, con las palabras de Pepe. **No hay cifras ni foto:** lo que sigue es lo que él dijo.

> «las de 1.2 y 0.8 bien en todo, las 0.8 un poco mejores en el tamaño del agujero central; las de 0.4 en cambio se paran a mitad de recorrido, por lo tanto solo salen un poco pero no llegan al centro»

| Juego | Resultado | Qué significa |
| --- | --- | --- |
| **1,2 mm** | «Bien en todo» | El iris abre y cierra. Es el grueso que pedía el brief |
| **0,8 mm** | «Bien en todo». El agujero central cerrado queda algo más pequeño que con 1,2 | El mejor de los tres |
| **0,4 mm** | **No vale.** Las láminas se paran a mitad de recorrido: asoman un poco y no llegan al centro | Ver «Por qué fallan las de 0,4» |

**Las previsiones, contra la pieza.**

- La revisión de la sesión del Mac calculaba que las de 1,2 se pondrían duras con el agujero a 30-40 mm y las de 0,8 a 15-20 mm, y que solo las de 0,4 cerrarían. **La pieza dice lo contrario:** las gruesas cierran y las finas no. La sesión del PC había dado esa estimación por buena y la repitió por otro camino con el mismo resultado: también se equivocó.
- Lo que sí se cumple: los ejes y los tetones a 0,25 mm de holgura giran, y la carcasa de 133,5 mm monta sin pegamento ni tornillos.

**Por qué fallan las de 0,4 (hipótesis de la sesión del PC, sin comprobar).** La lámina de 0,4 es una hoja de dos capas con dos zonas gruesas, la cola y el refuerzo del tetón, separadas por unos 15 mm de hoja fina. El aro empuja el tetón 2 mm por encima de la hoja. Calculo que con unos 30 gramos esa hoja cede, el tetón se tumba y se sale por debajo del aro o se acuña. En las de 1,2 y 0,8 la raíz es rígida y no pasa. Si es eso, es un fallo del dibujo de esa lámina, que hice yo, y no del grueso. Se arreglaría engordando toda la raíz, de la cola al tetón. **No está hecho ni hace falta si se elige 1,2 o 0,8.**

**Falta saber** (preguntado a Pepe):

- Cuánto mide el agujero cerrado con 1,2 y con 0,8.
- Si «bien en todo» incluye las cuatro pruebas de la tabla «vale si»: 20 veces sin engancharse, el cilindro de 75 mm, a contraluz y boca abajo.
- Si la tapa se movió (la raya de lápiz) y si hubo que apretar algo al montar.
- En las de 0,4: si al pararse las láminas el aro también se para, o sigue girando sin ellas.

## P0. Tolerancias (20 de noviembre de 2026)

Impresa y probada por Pepe en la Bambu Lab X1 Carbon. Ficheros de `probetas-v4\` (v4.1). Tira colocada con la esquina cortada abajo a la izquierda.

| Qué | Resultado de la probeta | Valor del modelo | ¿Hay que cambiar algo? |
| --- | --- | --- | --- |
| Alojamiento del imán | El tercero: **5,15 mm**. Entra apretando y no se cae | `iman_aloj_d` = 5,15 mm | No |
| Holgura | Con **0,10 mm** por lado la barrita entra y se queda sujeta. Con **0,15 mm** pasa sin forzar. Con 0,20 a 0,35 mm pasa holgada | `holg_tapa` = 0,20 mm · `holg_desliza` = 0,30 mm · `holg_presion` = 0,15 mm | No (ver notas) |
| Piel | Con **0,8 mm**, la más fina, ya no se ve la sombra del imán | `tapa_piel` = 1,4 mm | No (ver notas) |
| Imán embutido con pausa | Se quedó en su sitio al reanudar | — | No |

**Ojo: P0 se imprimió con el perfil «0.08mm Extra Fine» de Bambu Studio** (capa de 0,08 mm), no con la capa de 0,2 mm que piden la guía y el resto de las piezas. Los resultados de arriba valen para 0,08 mm. Con 0,2 mm los encajes pueden salir algo más justos. Para cerrarlo, P0 se repite a 0,2 mm en la misma bandeja que P1 y P2, con los mismos ajustes.

**Nota del 21-nov-2026:** Pepe la repitió a 0,2 mm. Los valores están en el apartado siguiente, leídos de una foto suya.

**Sin probar:** la fuerza del imán embutido frente a uno suelto (la prueba de los clips). Pepe decidió no hacerla. Queda sin saber si el calor de la impresión le quita fuerza.

## P0 repetida a capa de 0,2 mm (foto de Pepe, 21 de noviembre de 2026)

Pepe la repitió con capa de 0,2 mm y el 21-nov mandó una foto de la tira con marcas de bolígrafo. Esquina cortada abajo a la izquierda, como la primera vez. Las marcas las leyó la sesión del Mac en la foto y **Pepe confirmó la lectura el mismo día** («Has acertado con tus suposiciones»).

| Qué | Marca en la foto | Lectura | A 0,08 mm salió |
| --- | --- | --- | --- |
| Alojamiento del imán | Una raya sobre el **cuarto** empezando por la izquierda | **5,20 mm** | 5,15 mm (el tercero) |
| Holgura que sujeta | Un círculo relleno sobre la **segunda** ventana | **0,15 mm** por lado: entra y se queda | 0,10 mm (la primera) |
| Holgura que pasa sin forzar | Una raya sobre la **tercera** ventana | **0,20 mm** por lado | 0,15 mm (la segunda) |
| Piel | Sin marca | Sin dato: preguntado a Pepe, sin contestar | 0,8 mm ya tapaba el imán |

**A 0,2 mm todo sale 0,05 mm más justo que a 0,08**, en los tres casos. Lo que cambia con eso:

- **El iris (v5):** sus ejes y tetones llevan 0,25 mm de holgura por lado. Con 0,20 ya pasa sin forzar, así que deberían girar sueltos. El supuesto del reporte del iris se sostiene.
- **Imanes de adorno de la v5:** el alojamiento tiene que ser de 5,20 mm, no de 5,15, si la pieza se imprime a 0,2.
- **Un encaje que deba sujetar por presión** a 0,2 mm: 0,15 mm por lado, no 0,10.

## P1. La llave magnética (20 de noviembre de 2026): NO VALE

Impresa y probada por Pepe. En sus palabras: «los imanes no son ni de cerca lo suficientemente fuertes como para mover el mecanismo».

- **La aguja no arrastra el rotor.** Era el riesgo R1 del brief original y el que los contra-reportes dejaron «para las probetas».
- **Los cálculos lo daban por bueno** (0,89 N entre aguja y rotor, 6,9 mN·m de arrastre). Estaban equivocados o eran demasiado optimistas. Ningún otro cálculo de fuerza de imanes de este repositorio debe darse por válido sin medirlo.
- **Faltan los detalles:** si la aguja se pega al centro, si el rotor gira bien con el dedo, con qué espiral se probó.
- **Decisión de Pepe:** volver a la fase de diseño de la caja, con lluvia de ideas separada en forma, mecanismo y estética. La v4.1 queda parada.

## Notas sobre P0 (interpretación de la sesión del Mac)

- **El modelo es más holgado de lo que la impresora necesita.** El plan pedía `holg_tapa` = la ventana más justa que pasa (0,15) y `holg_desliza` una más (0,20). El modelo lleva 0,20 y 0,30. No se cambia: el panel entra seguro. Si en P2 el panel baila en la boca, hay margen para bajar a 0,15.
- **`holg_presion` = 0,15 mm no aprieta en esta impresora:** con 0,15 la barrita pasa sin forzar. Un encaje que tenga que sujetar por presión necesita 0,10. Hoy solo afecta al contorno de la tapa trasera, que no se sujeta por presión sino con su pestaña (y cinta en P1, porque el clip no retiene: contra-reporte v4.1, I1).
- **La piel tiene 0,6 mm de margen.** Si en P1 la aguja no arrastra el rotor, se puede bajar `tapa_piel` de 1,4 hasta 0,8 mm sin que se vea el imán. La prueba se hizo con luz normal, no a contraluz, y con un imán: no con el mecanismo entero detrás.
- **Conclusión: P1 y el aro de P2 se imprimen con los ficheros que ya hay.** No hace falta regenerar nada.
