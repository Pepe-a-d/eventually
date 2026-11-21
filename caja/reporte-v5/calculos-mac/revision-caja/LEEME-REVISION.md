# Entorno comun de la revision (sesion del Mac)

- Python con numpy, scipy, shapely, manifold3d y trimesh:  python
- Esta carpeta es una COPIA de trabajo. Contiene caja_diseno_v5.py y caja_piezas_v5.py (identicos a los del repo) y historico/frase-v3.json.
- El repositorio esta en <repositorio> (solo lectura para ti: NO modifiques nada alli, NO hagas git).
  Documentos: caja/BRIEF-v5.md (encargo), caja/reporte-v5/caja-entera.md (reporte del PC), caja/reporte-v5/caja-*-comprobaciones.txt,
  caja/generador_caja_v5.py (Fusion), caja/caja-v5-piezas.json, caja/probetas-v5/caja-probeta-*.3mf.

## Como construir el modelo (tarda unos 5 s)
    import sys; sys.path.insert(0, '<esta carpeta>')
    import caja_piezas_v5 as CP, caja_diseno_v5 as D
    p, d, d2, P = CP.piezas()                      # p: parametros, d: derivadas, P: dict nombre -> Pieza (ops, mueve, color)
    S = {n: CP.solido(q.ops) for n, q in P.items()}  # solidos manifold3d, con la caja CERRADA (tubo a 0 grados)
    M = CP.mover(S[n], n, P[n].mueve, p, d, tau)   # la pieza colocada para un giro de tubo tau (0..345 grados)
    D.movimiento(p, d, tau) -> (recorrido del teton mm, giro del aro grados, angulo de puertas grados, altura plataforma mm)
- manifold3d: (A ^ B).volume() es el volumen comun; A.min_gap(B, radio_busqueda) la distancia minima; A.bounding_box() -> (x0,y0,z0,x1,y1,z1);
  A.slice(z) -> CrossSection (.to_polygons(), .area()); A.translate/rotate/transform; A.to_mesh() (vert_properties, tri_verts).
- Ejes: X derecha, Y hacia atras (el frente es -Y), Z arriba; Z = 0 es la cara de arriba de las puertas cerradas. Al abrir, tubo y bisel giran a favor de las agujas (ROT = -1).
- Piezas: puerta_derecha, puerta_izquierda, aro_puertas, teton, marco, meseta, pasador_derecho, pasador_izquierdo, rueda_central,
  satelite_1..6, plato, tubo, plataforma, soporte, reloj_de_pega, bisel, base, cuerpo, funda, frase, probeta_anillo, probeta_teton.
- Impresion: FDM, PLA, capa de 0,2 mm, boquilla 0,4. Holguras MEDIDAS en piezas impresas: 0,15 mm por lado sujeta, 0,20 pasa sin forzar, 0,25 gira suelto.
