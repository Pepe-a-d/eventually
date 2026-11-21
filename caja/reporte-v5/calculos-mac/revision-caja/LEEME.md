# Programas de la revisión de la caja v5 (sesión del Mac, 22-nov-2026)

Son los programas con los que se buscaron los fallos de [`../../contra-reporte-caja.md`](../../contra-reporte-caja.md), repartidos en cinco frentes:
`puertas/`, `ascensor/` (ascensor y planetario), `imprimir/`, `montaje/` y `papeles/` (reporte contra modelo). Cada carpeta tiene un
`HALLAZGOS.md` con lo que encontró ese frente y qué programa reproduce cada cifra. `mac/` son las comprobaciones con que la sesión del Mac
repitió por su cuenta los hallazgos principales.

**Para repetir la revisión no hacen falta:** basta `../revisar_caja_v5.py`, que reúne las pruebas que deciden.

Se ejecutaron sobre una copia de trabajo, fuera del repositorio. Donde un programa o un texto dice `<carpeta-de-trabajo>`, es esa copia
(una carpeta con `caja_diseno_v5.py`, `caja_piezas_v5.py` e `historico/frase-v3.json`); `<repositorio>` es la raíz de este repositorio.
Para volver a ejecutarlos hay que poner ahí las rutas de la máquina en que se usen. Necesitan numpy, scipy, shapely, manifold3d y trimesh.
