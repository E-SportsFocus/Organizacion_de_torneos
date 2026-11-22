# Proposal

## Why

La historia HU-05 (Solicitud de cambio de horario) cubre los requisitos RP-02 y RP-03 del proyecto y el caso de uso CU-02. Actualmente los equipos solo pueden confirmar disponibilidad (HU-04), pero si un equipo tiene un inconveniente y no puede asistir al horario programado, no dispone de un mecanismo en la plataforma para acordar una reprogramación con el Moderador con la debida anticipación (más de 2 horas). La implementación de HU-05 completa el ciclo previo al juego de las partidas.

## What Changes

- Se introduce la capacidad `cambio-horario` para registrar solicitudes de cambio de horario realizadas por jugadores de equipos con más de 2 horas de anticipación a la partida.
- El Moderador asignado a la partida puede aprobar la solicitud (lo que reprograma la fecha/hora de la partida y avisa a los equipos y a Discord) o rechazarla con un motivo obligatorio (conservando el horario original).
- Si una solicitud queda sin decisión al alcanzarse el plazo de 2 horas antes de la partida, la solicitud pasa automáticamente al estado `Vencida` y la partida conserva su horario.
- Se añade la tabla `solicitud_cambio_horario` mediante migración `005_cambio_horario.sql`.
- Se añade el servicio `app/servicios/cambio_horario.py` y las operaciones correspondientes en `app/integraciones/discord.py`.
- Se actualizan las vistas del Jugador (`/jugador`) y Moderador (`/moderador`) con los formularios y listados respectivos.

## Capabilities

### New Capabilities
- `cambio-horario`: gestión completa de solicitudes de cambio de horario, validación del plazo de 2 horas, notificación simulada a Discord, aprobación por el Moderador con reprogramación de la partida, rechazo con motivo y vencimiento automático.

### Modified Capabilities
<!-- No se modifican los requerimientos base de specs existentes -->

## Impact

- `app/db/migrations/005_cambio_horario.sql`: nueva tabla `solicitud_cambio_horario`.
- `app/servicios/cambio_horario.py`: lógica de negocio, validación de plazos y transiciones EST-02.
- `app/integraciones/discord.py`: avisos de solicitud y reprogramación en `integraciones_log`.
- `app/rutas/cambio_horario.py`, `app/rutas/disponibilidad.py`, `app/rutas/resultado.py`.
- `app/templates/jugador.html`, `app/templates/moderador.html`.
- `tests/test_hu05.py`: suite completa de pruebas para los 5 escenarios Gherkin de HU-05.

## Fuera de alcance

- Negociación de horarios entre jugadores de equipos contrarios (el Moderador es quien aprueba o rechaza unilateralmente según el caso de uso CU-02 y DSS-03).
- Notificaciones push o mensajería en tiempo real (se usa simulación en base de datos vía `integraciones_log`).
- Autenticación real: se usa el selector de rol demo.
