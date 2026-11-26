# Tasks

## 1. Modelo, trazabilidad y criterios

- [x] 1.1 Completar `08-modelo-dominio.md` y `diagramas/modelo-dominio.puml` (atributos de Torneo, asociación `inscribe`, Premio y correspondencia clase → tabla).
- [x] 1.2 Reescribir `12-trazabilidad.md` con enlaces a código y pruebas, sin `Anuncio` como clase.
- [x] 1.3 Actualizar `07-criterios-aceptacion.md` (HU-04, HU-08 y HU-09) y `09-casos-de-uso.md` con la implementación real.
- [x] 1.4 Actualizar `11-diagramas-estado.md`, `diagramas/est-01.puml` y `diagramas/est-03.puml`.

## 2. Código y datos

- [x] 2.1 Incorporar `rondas_bracket` al contexto de `/` y reemplazar la tabla de enfrentamientos por el bracket resumido.
- [x] 2.2 Agregar la columna **Torneo** en `app/templates/jugador.html`.
- [x] 2.3 Validar el catálogo de estados en `app/servicios/torneo_gestion.py` y ajustar el formulario y el seed.
- [x] 2.4 Crear las migraciones `007_resultado_moderador_opcional.sql` y `008_torneo_estado_borrador.sql`.

## 3. Pruebas y documentación

- [x] 3.1 Actualizar `tests/test_hu04.py`, `tests/test_hu07.py` y `tests/test_hu09.py` (6 escenarios de HU-09).
- [x] 3.2 Actualizar `README.md` (7 HU, 49 pruebas, seed y recorrido de HU-09).
- [x] 3.3 Actualizar `.cin324/historias/HU-07.md` y `.cin324/proyecto.md`.
- [x] 3.4 Regenerar los PNG de `modelo-dominio`, `est-01` y `est-03`.
- [x] 3.5 Ejecutar `pytest` y `openspec validate --strict --all`.
- [x] 3.6 Archivar este cambio en `openspec/changes/archive/`.
