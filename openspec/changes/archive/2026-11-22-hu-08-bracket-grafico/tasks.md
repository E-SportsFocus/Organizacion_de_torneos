# Tasks

## 1. Backend y estructuración de datos
- [x] 1.1 Crear servicio `app/servicios/bracket.py` con `obtener_bracket_estructurado` para consultar y organizar partidas en rondas ordenadas con equipos, marcadores individuales y estado de victoria.
- [x] 1.2 Actualizar ruta `app/rutas/resultado.py` para invocar el servicio de bracket estructurado y pasar `rondas_bracket` al contexto de la plantilla `bracket.html`.

## 2. Plantilla y componentes visuales
- [x] 2.1 Diseñar e implementar en `app/templates/bracket.html` el contenedor del árbol visual con columnas por fase (`Cuartos de final`, `Semifinal`, `Final`).
- [x] 2.2 Implementar nodos de enfrentamiento con cabecera de fecha/hora, slots de equipos, casillas de marcador individuales, destaque visual del ganador y estado de espera en partidas pendientes.
- [x] 2.3 Añadir conectores CSS/SVG fluidos que vinculen las rondas sucesivas del torneo.
- [x] 2.4 Asegurar contraste y estilo armónico en modo claro y modo oscuro, manteniendo la sección de historial de actualizaciones auditable (RP-10).

## 3. Pruebas y validación
- [x] 3.1 Crear archivo de pruebas `tests/test_hu08.py` cubriendo los 4 escenarios Gherkin.
- [x] 3.2 Ejecutar suite completa con pytest y verificar que todas las pruebas pasen (38 existentes + 4 nuevas = 42).
- [x] 3.3 Validar con `openspec.cmd validate --all` y archivar el cambio.
