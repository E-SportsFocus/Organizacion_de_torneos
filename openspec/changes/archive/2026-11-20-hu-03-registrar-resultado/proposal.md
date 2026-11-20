# Proposal — HU-03 · Registro manual del resultado

## Why

Cuando la API del videojuego no está disponible, la partida queda en `Pendiente de resultado` y el torneo no puede continuar: hoy la aplicación solo permite consultar la disponibilidad y no existe un lugar donde el Moderador registre el marcador. Sin ese registro no se actualiza el bracket ni se conserva la trazabilidad que exige RP-10.

Esta historia implementa **HU-03 — Registro manual del resultado** (`07-criterios-aceptacion.md`, líneas 63-102), la actividad del TO-BE **«Árbitro registra el resultado manualmente en la plataforma si la API no está disponible»** (`Rediseño_y_TO-BE.md:39`) y el caso de uso **CU-04 — Registrar el resultado de una partida cuando la API no está disponible** (`09-casos-de-uso.md:26`).

## What Changes

- Agrega el flujo para que el **Moderador asignado** registre el resultado de una partida en estado `Pendiente de resultado`.
- Valida que el usuario sea el Moderador asignado, que la partida esté pendiente, que ambos marcadores estén presentes, sean enteros mayores o iguales a 0 y **no sean iguales** (no se admite empate), y que la partida no tenga ya un resultado.
- Persiste el **Resultado** con la identidad del Moderador, la fecha, la hora y el origen `manual`, y el marcador de cada equipo.
- Actualiza el **Bracket** del torneo y registra cada actualización en su historial (RP-10).
- Registra la **notificación** del resultado para el Organizador y los Jugadores de ambos equipos, con un **adaptador de Discord simulado**.
- Lleva la partida de `Pendiente de resultado` a `Resultado confirmado`.
- Agrega datos de ejemplo: un segundo Moderador no asignado, un Organizador, una partida `Pendiente de resultado` y un resultado sembrado para la partida `Anunciada`.
- Agrega pruebas automáticas, una por escenario Gherkin (5 escenarios), y actualiza el `README`.

**Fuera de alcance:**
- HU-01 (integración con la API del videojuego) y la transición automática `En curso → Pendiente de resultado`.
- HU-02 (vista y consulta de la notificación y del bracket por el jugador/organizador).
- HU-05 (cambio de horario).
- HU-06 (publicación y anuncio del ganador, transición `Resultado confirmado → Anunciada` y pantalla del Organizador).
- Integración real con Discord o con la API, autenticación real, RP-08 y RP-09.
- La tabla `partida_equipo`: los dos equipos se siguen infiriendo de `disponibilidad`.

## Capabilities

### New Capabilities

- `resultado`: registro manual del resultado de una partida por el Moderador asignado, con su trazabilidad, la actualización del bracket y la notificación simulada a los participantes.

### Modified Capabilities

Ninguna. La especificación vigente `disponibilidad` no cambia.

## Impact

- **Base de datos:** nueva migración `003_resultados_bracket_notificaciones.sql` con `resultado`, `resultado_marcador`, `bracket`, `bracket_actualizacion` y `notificacion`.
- **Modelo:** `persona.tipo` admite `Organizador`; se agrega un Organizador de ejemplo.
- **Lógica:** `app/servicios/resultado.py` (registro, validaciones y transición de estado) y `app/integraciones/discord.py` (adaptador simulado).
- **Rutas y pantallas:** vista del Moderador con el formulario de resultado, detalle de la partida y vista del bracket con su historial.
- **Datos:** `app/db/seed.py` con los nuevos roles y partidas.
- **Pruebas:** `tests/test_hu03.py` con 5 pruebas de integración.
- **Documentación:** `README.md`.
