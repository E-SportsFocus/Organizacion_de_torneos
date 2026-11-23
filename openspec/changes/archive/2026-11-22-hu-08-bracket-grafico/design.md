# Design

## Context

Actualmente `/bracket` lista las partidas en una tabla y un historial cronológico de actualizaciones de moderación (RP-10, HU-03). La comunidad y los usuarios requieren una representación visual gráfica del progreso de llaves (bracket arbóreo) similar al estándar de plataformas como Liquipedia y VLR.gg, organizada por columnas de fases conectadas visualmente.

## Goals / Non-Goals

**Goals:**
- Implementar en `app/servicios/bracket.py` una función para estructurar las partidas del torneo en rondas ordenadas secuencialmente (`Cuartos de final`, `Semifinal`, `Final`), enriqueciendo cada nodo con equipos, marcadores individuales, ganador detectado, estado y conector.
- Renderizar en `app/templates/bracket.html` el árbol visual con flexbox/grid responsivo, tarjetas de nodo con diseño limpio, casillas de puntaje tipo esport, resalte del ganador y líneas de conexión.
- Garantizar la compatibilidad con el modo claro y modo oscuro usando las variables CSS de `base.html`.
- Mantener la sección de historial de actualizaciones de moderación existente (RP-10) debajo del árbol visual o en pestaña alternable accesible.

**Non-Goals:**
- Múltiples formatos de torneo dinámicos no presentes en el dominio actual (por ejemplo, brackets de eliminación doble con losers bracket infinito o suizos).
- Modificación directa del DOM con librerías pesadas externas (se hace con HTML/CSS nativo limpio y semántico sin dependencias extras).

## Decisions

### 1. Estructuración en Backend (`app/servicios/bracket.py`)
- Se crea la función `obtener_bracket_estructurado(conexion, torneo_id)` que consulta las partidas del torneo junto con sus equipos (desde `disponibilidad`), resultados (`resultado`, `resultado_marcador`) y las agrupa por fase en el orden canónico:
  1. `Cuartos de final`
  2. `Semifinal`
  3. `Final`
- Cada partida estructurada contiene:
  - `id`, `fase`, `fecha_hora`, `estado`
  - `equipos`: lista de objetos con `id`, `nombre`, `marcador` (entero o `-`), `es_ganador` (bool)
  - `tiene_resultado`: bool
  - `ganador_nombre`: string o None

### 2. Estilos visuales del árbol y conectores
- Contenedor `.bracket-arbol` con `display: flex; gap: 2.5rem; overflow-x: auto; padding: 1rem 0;`.
- Columnas de ronda `.bracket-columna-ronda` con encabezado de fase y contenedor de nodos `.bracket-nodos`.
- Nodo de enfrentamiento `.bracket-nodo`: tarjeta con borde sutil, fecha/hora, estado en chip y lista de dos slots `.bracket-slot-equipo`.
- Cada slot tiene nombre de equipo y casilla `.bracket-marcador`. El ganador recibe la clase `.ganador` con fondo sutil y texto resaltado.
- Conectores horizontales y verticales entre rondas mediante pseudo-elementos CSS (`::after`, `::before`) y clases de conector que enlazan visualmente las llaves.

## Risks / Trade-offs

- [Partidas sin equipos definidos o incompletos] $\rightarrow$ Se muestra "Por definir" o TBD si un slot no tiene equipo asignado aún.
- [Compatibilidad con pruebas de HU-03 y HU-07] $\rightarrow$ Se mantiene la tabla de auditoría y las palabras clave de las vistas existentes para que ninguna prueba previa sufra regresión.
