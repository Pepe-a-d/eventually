# Probeta 1, el iris: revisión de la sesión del Mac

Sesión del Mac · 21 de noviembre de 2026 · revisa [probeta-iris.md](probeta-iris.md) antes de imprimir.
Cálculos propios en [`calculos-mac/apilado_iris.py`](calculos-mac/apilado_iris.py) (solo necesita numpy).

## En una frase

El modelo está bien hecho y las medidas del reporte son ciertas, pero **creo que el iris no va a cerrar del todo con ninguno de los dos juegos de láminas**: se pondrá duro con un agujero de unos 3 a 4 cm (láminas de 1,2) o de 1,5 a 2 cm (láminas de 0,8). El motivo es el grueso de las láminas, y **parte de la culpa es de mi brief**, que pedía a la vez láminas de 1,2 mm o más y un agujero cerrado de 8 mm o menos.

Es una previsión calculada. Según la regla del proyecto, no vale hasta que la pieza lo diga. Por eso propongo imprimir igualmente.

## 1. Lo que he comprobado y cuadra

Medido por mí sobre los `.3mf` exportados, sin usar Fusion:

| Qué | Reporte del PC | Medido en el `.3mf` |
| --- | --- | --- |
| Diámetro exterior de la base | 133,5 mm | 133,49 mm |
| Grueso de la base | 9,8 mm | 9,80 mm |
| Aro | 2,0 mm de grueso | 2,00 mm; 131,8 × 128,2 mm con la orejeta |
| Tapa | 1,6 mm | 1,60 mm; 130,5 mm de diámetro |
| Lámina de 1,2 | tetón de 2,0 mm | 1,20 mm de lámina y 3,20 de alto total |
| Lámina de 0,8 | tetón de 2,4 mm | 0,80 mm de lámina, cola de 1,20 y 3,20 de alto total |
| Volúmenes | 19 490 · 16 313 · 13 942 · 1 586 · 1 079 mm³ | 19 428 · 16 322 · 13 950 · 1 586 · 1 078 mm³ |

- **Se imprime sin soportes.** Lo único que vuela son las cuatro uñas: unos 11 mm² por capa, en escalones de 0,2 mm (45°). La tapa va con la cara ancha hacia la cama, como dice el reporte.
- **Las alturas caen en capas enteras de 0,2 mm** (1,2 · 4,6 · 5,8 · 6,0 · 8,0 · 8,2 · 9,8).
- **El apilado de las láminas lo he rehecho por otro camino** (punto a punto en una rejilla de 0,35 mm, en vez de con polígonos) y me salen las mismas cifras que al PC: 0,26 mm de pisado con el iris abierto y 1,13 cerrado para las de 1,2; 0 y 0,73 para las de 0,8.
- **El borde del hueco no engancha las láminas:** en el cálculo quedan siempre a más de 1,2 mm del plato de abajo.
- **El sesgo de la ranura (41°) no acuña.** Con rozamiento de 0,3 (supuesto) se acuñaría por encima de 73°. El límite de 45° del PC es prudente.

## 2. Lo que no cuadra: cómo se «absorbe» el pisado

El reporte dice que las láminas se pisan 1,1 mm al cerrar y que lo absorben doblándose con **unos 11 gramos por lámina**. La cifra de 1,1 mm es correcta. La de 11 gramos no: sale de tratar la lámina como una regla de 64 mm sujeta por un extremo que se dobla por la punta. No es eso lo que tiene que pasar.

**Lo que pide la geometría (esto no depende de fuerzas ni de materiales):**

- Las ocho láminas montan en rueda: cada una encima de la anterior, y la última debajo de la primera. He comprobado que cada lámina solo toca a sus dos vecinas en todo el giro.
- Para que eso sea posible, cada lámina tiene que **bajar un grueso entero dentro de su propio ancho**. Es una escalera de caracol: ocho peldaños de un grueso por vuelta.
- Cerca de la pared hay mucho ancho para bajar y casi no se nota. Cerca del centro la lámina es muy estrecha y tiene que ir muy inclinada de lado:

| Agujero | Inclinación de lado que necesita la lámina de 1,2 | La de 0,8 | Una de 0,4 |
| --- | --- | --- | --- |
| 40 mm | 4,4° | 2,9° | 1,5° |
| 20 mm | 8,7° | 5,8° | 2,9° |
| 10 mm | 17° | 11,5° | 5,8° |
| 5 mm (el cierre del modelo) | 31° | 22° | 11,5° |

- La lámina plana, con el juego que tiene su cola (0,2 mm entre la isla y el aro), solo puede inclinarse **1,9°**. Con eso las de 1,2 apilan sin deformarse solo con el agujero por encima de 93 mm, es decir, nunca (el hueco abierto mide 75). Las de 0,8, por encima de 62 mm.
- Todo lo que falte hasta la cifra de la tabla lo tiene que poner la lámina **retorciéndose**, y sobre todo en la punta, que mide 2 a 4 mm de ancho. Una punta de PLA de 1,2 mm de grueso no se retuerce 31°.

**Lo que calculo que pasará (estimado, con fuerzas: lo tiene que confirmar la pieza):**

| Juego | Fuerza entre láminas con el agujero a 20 mm | Dónde calculo que se pone duro |
| --- | --- | --- |
| 1,2 mm | unos 250 g | agujero de **30 a 40 mm** |
| 0,8 mm | unos 40 g | agujero de **15 a 20 mm** |
| 0,6 mm (no existe) | unos 11 g | agujero de unos 10 mm |
| 0,4 mm (no existe) | 1 g | cierra hasta los 5 mm |

Supuestos de esa tabla: PLA con módulo de torsión de 1 100 MPa, rozamiento de 0,3, un dedo que empuja la orejeta con 0,5 a 1 kg, y la torsión repartida a lo largo de la lámina. Puede estar equivocada en un factor de 2 o 3 en la fuerza, pero la fuerza crece tan deprisa al cerrar que el diámetro cambia poco.

**Mi parte de culpa.** El apartado 11 de mi brief pedía «láminas de 1,2 mm o más» y «agujero cerrado de 8 mm o menos». Con láminas planas las dos cosas no caben juntas, y no lo comprobé. El 1,2 lo puse por robustez y para que no se transparentara, sin calcular el apilado.

## 3. Otras tres cosas, menores

1. **El aro gira poco y eso quita fuerza.** El aro gira 15° y la lámina 33°: el dedo llega a la lámina con menos de la mitad de fuerza. El brief dejaba hasta 60°. Con una ranura inclinada o curva, en vez de radial, el aro giraría 45 a 60° y empujaría tres o cuatro veces más. Además le viene bien al resto de la caja: el tubo tenía previstos 60° para abrir el iris.
2. **La tapa puede irse aflojando sola.** Las láminas, al forzarse, hacen palanca en su cola y empujan el aro hacia arriba contra la tapa (calculo cerca de 1 kg en total con las de 1,2 cerradas, bastante menos con las de 0,8). Al abrir el iris, el aro gira justo en el sentido que suelta la bayoneta, y la tapa no tiene retén. Mi cuenta dice que aguanta, con poco margen (1,7 veces). Se ve fácil: una raya de lápiz que cruce de la tapa a la pared antes de empezar.
3. **Las uñas (lo que pedía mirar el PC).** Bien para imprimir: 45°, 0,8 mm de vuelo. Pisan 0,5 mm de tapa y la tapa tiene 0,3 mm de juego de lado: si se va toda a un lado, en el contrario pisa 0,2. Con las láminas de 0,8 no me preocupa. Con las de 1,2 forzadas hasta el fondo, sí: no hay que forzar.

## 4. Lo que propongo (decide Pepe)

1. **Imprimir la probeta tal como está.** Sirve igual para lo demás: si los ejes giran sueltos, si la tapa entra, si las uñas salen limpias, el diámetro real. Y dirá si mi previsión es cierta.
2. **Añadir un tercer juego de láminas finas, de 0,4 mm** (y, si no cuesta, otro de 0,6). Solo cambian las láminas: la carcasa es la misma, porque la cola ya se engorda a 1,2 como en el juego de 0,8. Es un cambio de un número en `iris_diseno_v5.py` y una bandeja más. **Pepe dijo que sí al de 0,4 el 21-nov a las 08:05 (D-28).** El de 0,6 no lo ha pedido.
3. **Al probar, no forzar.** Cerrar hasta que se ponga duro y apuntar cuánto mide el agujero en ese punto, con cada juego.
4. Para la versión siguiente del iris, según lo que salga: lámina escalonada (fina en la punta, gruesa en la raíz), más giro de aro y un retén para la tapa.

Sobre las de 0,4: son dos capas de PLA blanco. Dejarán pasar luz, aunque no se verá lo de dentro con nitidez. Si cierran bien, ya se verá si hace falta la lámina escalonada para que la parte que se ve sea más gruesa.

## 5. Añadir a la tabla «vale si»

- Con cada juego: **diámetro del agujero cuando empieza a ponerse duro**, sin forzar.
- Si las puntas se levantan o se hunden al cerrar (mirar de lado).
- Si la raya de lápiz de la tapa se ha movido después de las 20 veces.
- Los tres valores de la P0 a 0,2 mm, que siguen sin apuntar: qué alojamiento de imán, qué ventana sujeta y cuál pasa.
