# Historia del proyecto, paso a paso

Qué se hizo, en orden, hasta el 20 de noviembre de 2026. Escrito por la sesión del PC a partir de los repositorios, los reportes y las conversaciones. Las horas son de Italia y salen de los commits. Lo que no consta se dice.

**Quién es quién.** Pepe decide. La **sesión del Mac** hizo la web, la tarjeta y el QR, y revisa cada versión de la caja. La **sesión del PC** modela la caja en Fusion.

## 1. El reloj y la web (19 de noviembre)

1. Pepe elige el nombre: **Eventually — Late Edition · 1 of 1**.
2. La sesión del Mac hace la web: el reloj se monta pieza a pieza al deslizar, sobre papel blanco. Sale de cinco imágenes hechas en Gemini; no hicieron falta vídeos. Queda publicada a las 18:00.
3. Hace también la tarjeta de autenticidad (85 × 55 mm, diseñada en Figma) y el QR.

## 2. La caja en papel: de la v0 a la v4.1 (19 y 20 de noviembre)

Cada vuelta fue igual: el PC modela una versión y el Mac la revisa con un contra-reporte. Fueron seis rondas sin imprimir nada.

| Paso | Qué se hizo | Qué pasó después |
| --- | --- | --- |
| **v0**, 19-nov 19:55 | Brief de la sesión del Mac: funda de papel, caja y una aguja azul que hace de llave con un imán. El mayor riesgo ya estaba apuntado como R1: que el imán no arrastrara el rotor | Se encarga el modelo a la sesión del PC |
| **v1** | Primera caja en Fusion: alta, se abría por arriba | Pepe la ve y dice que es muy incómodo sacar el reloj y usarla de expositor. Pide una llave más fina y la frase con la letra del reloj |
| **v2**, subida a las 21:42 | Caja-expositor que se abre por delante. Pedía 24 imanes | Contra-reporte (22:09): 6 fallos graves y 11 importantes. Pepe tiene 14 imanes y ninguna chapa de acero: no se puede montar |
| **v3**, subida a las 23:11 | Funda de campana, pinza en C y peana, cierre de un empujón, 8 imanes | Contra-reporte (23:54): 4 graves y 10 importantes. El cierre de un empujón se acuña y la pinza estaba dibujada con una forma falsa |
| **v4**, 20-nov 07:04 | Rotor de un solo sentido con tope, se cierra con la aguja puesta, peana corredera, pinza a medida | Contra-reporte (11:21): 2 graves y 8 importantes. Recomienda un parche, no una v5 |
| **v4.1**, 11:50 | Parche: arregla los 2 graves. Primera subida hecha por la sesión del PC | Contra-reporte (12:17): 5 importantes, ninguno grave. Pide imprimir antes de seguir |

Todo está en `caja/historico/`: generadores, modelos, piezas, reportes y contra-reportes.

## 3. Vídeo y tutorial de la v4.1 (20 de noviembre, mediodía)

1. **13:01.** La sesión del PC hace un vídeo de 68 segundos con la caja v4.1 y su mecanismo. Pepe: «es muy bueno».
2. **13:32.** La sesión del Mac crea el repositorio `eventually-proyecto` con las fuentes de la web, la tarjeta y su resumen.
3. Pepe pide el mismo vídeo como tutorial para la web, «integrado en la app y no un simple reproductor».
4. **14:21.** La sesión del PC lo entrega como una segunda película movida por el scroll. A las 14:27 la del Mac lo revisa, lo fusiona y lo publica.
5. **15:01 a 15:52.** La sesión del Mac añade, a petición de Pepe: el enlace «¿Cómo se abre la caja?» en la portada, la primera visita sin enseñar el reloj y una revisión completa de textos.

Fallo de coordinación de ese día: la sesión del PC vigilaba dos repositorios y no sabía que existía el tercero. Tardó 45 minutos en ver lo que había subido la del Mac. Es una de las razones de tener un solo repositorio.

## 4. Las primeras piezas impresas (20 de noviembre, tarde)

1. Pepe imprime la **P0** (tolerancias). Sale bien. La había impreso con capa de 0,08 mm; la repite a 0,2 mm y también sale bien (dicho por Pepe, sin cifras).
2. Imprime **P1 y P2**. **P1 falla:** «los imanes no son ni de cerca lo suficientemente fuertes como para mover el mecanismo».
3. Los cálculos de las dos sesiones lo daban por bueno. Era el riesgo R1 del primer brief.

## 5. La v5 (20 de noviembre, noche)

1. Pepe decide no arreglar la v4.1 y volver a diseñar desde cero, por sectores: mecanismo, forma, estética y experiencia.
2. En una conversación larga con la sesión del Mac elige el diseño de `caja/BRIEF-v5.md` (23:30): caja cilíndrica, bisel que se gira, engranajes a la vista, tapa de iris y un ascensor que sube el reloj.
3. La sesión del PC recibe el encargo de la primera probeta, el iris. Antes de modelar hace un cálculo en plano: con 6 láminas la carcasa no baja de 134 mm. Pepe acepta una carcasa de 8 láminas con dos gruesos de lámina.
4. **23:44.** Pepe pide juntar todos los directorios en uno y dejar escrito qué llevó a cada decisión. De ahí sale esta organización.
5. **23:55.** Pepe la aprueba («Fusiona») y fija la regla de subida: cada sesión sube su trabajo, y él confirma antes.

## 6. Lo que se aprendió

- **Ninguna fuerza calculada se da por buena sin una pieza impresa que lo confirme.** Vale sobre todo para los imanes.
- **Primero la probeta del mecanismo, después la caja.** Se hicieron cinco versiones enteras antes de probar la idea central.
- **Al pedir un cambio en una pieza, decir en qué dirección sujeta y con qué fuerza, no solo la forma.** Tres de los cinco fallos del parche v4.1 salieron de frases copiadas al pie de la letra.
- **«Sin choques» en el modelo no es «funciona».**
- **Una sesión no ve lo que la otra no ha subido,** ni lo que está en un sitio que no conoce.
