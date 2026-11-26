# Proposal

## Why

La revisión de la rúbrica y de las correcciones del profesor detectó inconsistencias entre los artefactos de requisitos y el código: el modelo de dominio no describía todos los atributos de `Torneo` ni la asociación `Torneo — Equipo`; la trazabilidad citaba `Anuncio` como clase; los criterios Gherkin no cubrían todos los escenarios implementados; el inicio (`/`) seguía mostrando una tabla de enfrentamientos en lugar del bracket resumido; la vista del jugador no indicaba el torneo de cada partida; y el estado del torneo no se validaba contra el catálogo de EST-03. Este cambio alinea esos puntos sin incorporar una historia nueva.

## What Changes

- Se completan `08-modelo-dominio.md` y `diagramas/modelo-dominio.puml`: atributos de `Torneo`, asociación `inscribe`, `Premio` sin «condiciones de entrega» y correspondencia clase → tabla SQLite.
- Se reescribe `12-trazabilidad.md` con enlaces a código y pruebas, sin `Anuncio` como clase del dominio.
- Se actualizan los criterios Gherkin de HU-04, HU-08 y HU-09 y la tabla de casos de uso con la implementación real.
- El inicio (`/`) muestra un bracket resumido por fases; la tabla detallada con marcador e historial queda solo en `/bracket`.
- La vista del jugador muestra la columna **Torneo**.
- `crear_o_actualizar_torneo` valida el estado contra `Borrador`, `Inscripciones abiertas`, `En curso` y `Finalizado`, y rechaza también el valor vacío.
- La migración `007_resultado_moderador_opcional.sql` permite `NULL` en `resultado.moderador_id`, como exige la multiplicidad `0..1` del modelo para resultados automáticos.
- La migración `008_torneo_estado_borrador.sql` normaliza los torneos existentes con estado vacío al valor inicial `Borrador`.
- Se actualizan las pruebas de HU-04, HU-07 y HU-09 y el `README.md`.

## Capabilities

### New Capabilities
<!-- No se agregan capacidades nuevas. -->

### Modified Capabilities
- `torneo-publico`: el inicio muestra el bracket resumido por fases y no la tabla detallada de partidas.
- `disponibilidad`: la vista del jugador indica el torneo de cada partida.
- `gestion-torneo`: el estado del torneo se valida contra el catálogo de EST-03 y se documentan los escenarios de actualización y estado inválido.

## Impact

- `app/templates/torneo.html`, `app/rutas/torneo.py`, `app/templates/jugador.html`.
- `app/servicios/torneo_gestion.py`, `app/rutas/organizador.py`, `app/templates/gestion_torneo.html`, `app/db/seed.py`.
- `app/db/migrations/007_resultado_moderador_opcional.sql`, `app/db/migrations/008_torneo_estado_borrador.sql`.
- `tests/test_hu04.py`, `tests/test_hu07.py`, `tests/test_hu09.py`.
- `07-criterios-aceptacion.md`, `08-modelo-dominio.md`, `09-casos-de-uso.md`, `11-diagramas-estado.md`, `12-trazabilidad.md`, `README.md`.
- `diagramas/modelo-dominio.puml`, `diagramas/est-01.puml`, `diagramas/est-03.puml` y sus PNG.
- `.cin324/historias/HU-07.md`, `.cin324/proyecto.md`.

## Fuera de alcance

- La integración real con la API del videojuego (HU-01) y la autenticación real.
- Cambios en el flujo de negocio de HU-03, HU-04, HU-05, HU-06 y HU-08.
- Transiciones automáticas del estado del torneo: el Organizador selecciona el estado y el sistema valida el catálogo.
