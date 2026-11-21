# Eventually, la caja: resultados de las probetas

Lo que han dicho las piezas impresas. Cada resultado lleva la fecha y quién lo midió.

## Probeta 1 de la v5: el iris (21 de noviembre de 2026): FUNCIONA con los tres gruesos, pero Pepe no la da por buena

Impresa, montada y probada por Pepe en la Bambu Lab X1 Carbon, a capa de 0,2 mm. Ficheros de `caja/probetas-v5/`. Apuntado por la sesión del PC con las palabras de Pepe. **No hay cifras ni foto.**

**14:42.** «las de 1.2 y 0.8 bien en todo, las 0.8 un poco mejores en el tamaño del agujero central; las de 0.4 en cambio se paran a mitad de recorrido, por lo tanto solo salen un poco pero no llegan al centro»

**14:51, corrección de Pepe.** «Las de 0,4 funcionan, error mío al montar el mecanismo porque puse el aro del revés. De todas formas creo que el iris no va a quedar con el estándar de calidad que busco, voy a valorar opciones con la sesión del Mac»

| Juego | Resultado |
| --- | --- |
| **1,2 mm** | Funciona. «Bien en todo» |
| **0,8 mm** | Funciona. «Bien en todo». El agujero central cerrado queda algo más pequeño que con 1,2 |
| **0,4 mm** | Funciona, con el aro bien puesto |

**Lo que dice la pieza.**

- **El mecanismo funciona:** un iris de PLA de 8 láminas, con 75 mm de hueco y 133,5 mm de carcasa, abre y cierra con los tres gruesos. Los ejes y los tetones a 0,25 mm de holgura giran. Monta sin pegamento ni tornillos.
- **Pero a Pepe no le convence la calidad** para la caja. No ha dicho todavía qué es lo que no le llega: lo va a hablar con la sesión del Mac. **El iris queda en el aire** hasta que decida; el plan B apuntado es D-22, dos compuertas correderas.
- **El aro se puede montar del revés, y entonces las láminas se paran a mitad de recorrido.** Es un defecto del diseño: nada lo impide ni lo avisa. La sesión del PC le dijo a Pepe que del revés no encajaba, y no era verdad. Si el iris sigue, el aro tiene que llevar algo que solo deje montarlo de una manera.

**Las previsiones, contra la pieza.**

- La revisión de la sesión del Mac calculaba que las de 1,2 se pondrían duras con el agujero a 30-40 mm y las de 0,8 a 15-20 mm. La sesión del PC lo dio por bueno y lo repitió por otro camino. **La pieza dice que cierran las dos.** Otra cuenta de fuerzas desmentida.
- Cuando Pepe dijo que las de 0,4 se paraban, la sesión del PC lo explicó con que la raíz de la lámina cedía y el tetón se salía del aro. **También estaba mal:** era el aro del revés.

**Falta saber:**

- Qué es lo que no alcanza el nivel que Pepe busca: el aspecto, el tacto, la luz que pasa, el agujero, el tamaño.
- Cuánto mide el agujero cerrado con cada juego.
- Si «bien en todo» incluye boca abajo y que la tapa no se movió (la raya de lápiz).

**Nota de la sesión del Mac, 21-nov a las 15:10. Qué es lo que no le llega a Pepe.** Se lo pregunté con cuatro respuestas posibles (cómo se ve cerrado, el tacto al moverlo, que parece frágil, el acabado de impresión) y marcó dos: **«Cómo se ve cerrado»** (las láminas montadas en escalera, el agujero del centro, rendijas o luz) y **«Parece frágil»**. No marcó el tacto ni el acabado de impresión. Es decir: el movimiento le vale; lo que no le vale es la tapa cerrada y la sensación de poca solidez.

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
