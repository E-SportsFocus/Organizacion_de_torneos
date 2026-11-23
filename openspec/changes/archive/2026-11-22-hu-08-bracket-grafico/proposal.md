# Proposal

## Why

La historia HU-08 (Visualización gráfica del Bracket del torneo) atiende la necesidad de los usuarios y participantes de comprender de un vistazo la progresión del torneo y el estado de los enfrentamientos. Anteriormente, la visualización de `/bracket` y del inicio era primordialmente tabular y auditada (`Partidas`, `Historial de actualizaciones`). Para dar una experiencia interactiva competitiva de estándar esport (similar a Liquipedia y VLR.gg), se requiere una vista de árbol de llaves con rondas en columnas horizontales, tarjetas de enfrentamiento conectadas con casillas de puntaje individuales, destaque visual del equipo clasificado o ganador, y estado claro para partidas pendientes sin inventar resultados.

## What Changes

- Se introduce la capacidad `bracket-grafico` para organizar y presentar las partidas del torneo en una estructura de árbol visual jerárquico por fases (por ejemplo: Cuartos de final, Semifinal, Final).
- En el backend (`app/servicios/bracket.py` y `app/rutas/torneo.py`), se estructuran las partidas agrupadas en rondas ordenadas cronológica y lógicamente para alimentar la vista visual del árbol.
- En la plantilla `app/templates/bracket.html`, se implementa un árbol visual (`.bracket-arbol`) con columnas de rondas (`.bracket-columna-ronda`), nodos de partida (`.bracket-nodo`), slots de equipos con marcadores individuales (`.bracket-slot-equipo`, `.bracket-marcador`), etiquetas de estado y líneas conectoras fluidas (CSS/SVG) acordes a la paleta institucional (modo claro y modo oscuro).
- Se preserva la tabla de auditoría e historial de actualizaciones del bracket (cumpliendo RP-10 y compatibilidad con HU-03).
- Se añaden pruebas automatizadas en `tests/test_hu08.py` para verificar los 4 escenarios Gherkin.

## Capabilities

### New Capabilities
- `bracket-grafico`: visualización interactiva y estructurada de las llaves del torneo en árbol de rondas secuenciales con casillas de puntuación, resalte de ganadores y conector visual, manteniendo coexistencia con el historial de auditoría.

### Modified Capabilities
<!-- No se modifican las capacidades funcionales de resultado o disponibilidad -->

## Impact

- `app/servicios/bracket.py`: nuevo servicio de estructuración y agrupación de llaves para el árbol visual.
- `app/rutas/torneo.py`: inyección de la estructura de rondas del bracket al renderizar `/bracket` (y opcionalmente `/`).
- `app/templates/bracket.html`: vista de árbol de llaves con diseño responsivo, tema claro/oscuro y líneas conectoras.
- `tests/test_hu08.py`: suite completa de pruebas para los 4 escenarios de HU-08.
- `.cin324/historias/HU-08.md`, `07-criterios-aceptacion.md`, `09-casos-de-uso.md`, `12-trazabilidad.md`, `Historias_de_usuario.md`.

## Fuera de alcance

- Algoritmos automáticos de generación combinatoria de brackets dinámicos de N equipos (el torneo actual utiliza las fases sembradas del dominio: Cuartos de final, Semifinal y Final).
- Edición directa interactiva tipo drag-and-drop en el bracket (la edición sigue siendo a través del flujo oficial de registro de resultados de Moderador de HU-03).
