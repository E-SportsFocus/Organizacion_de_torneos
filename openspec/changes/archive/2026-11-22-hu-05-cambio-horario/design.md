# Design

## Context

El sistema ya cuenta con gestión de disponibilidad de equipos (`disponibilidad`), registro de resultados manuales (`resultado`), anuncios oficiales (`anuncio`) e inicio público (`torneo-publico`). La clase `SolicitudCambioHorario` está prevista en el modelo de dominio (`08-modelo-dominio.md`), sus transiciones en EST-02 (`11-diagramas-estado.md`) y su flujo en DSS-03 (`10-diagramas-secuencia.md`).

## Goals / Non-Goals

**Goals:**
- Implementar la persistencia de solicitudes con tabla `solicitud_cambio_horario` (migración `005_cambio_horario.sql`).
- Implementar servicio `app/servicios/cambio_horario.py` que aplique la regla de 2 horas previas para solicitar y el vencimiento automático al alcanzar dicho umbral sin decisión.
- Adaptar `Discord` simulado para registrar las operaciones `aviso_solicitud_cambio` y `confirmacion_nuevo_horario`.
- Extender las interfaces de `/jugador` (para crear solicitudes y ver su estado) y `/moderador` (para aprobar o rechazar con motivo).

**Non-Goals:**
- Tareas programadas de fondo tipo cron para vencer solicitudes: el vencimiento se calcula de forma reactiva al consultar o evaluar las solicitudes con la función del reloj inyectado.
- Edición de solicitudes ya enviadas o solicitudes cruzadas entre jugadores sin mediación del moderador.

## Decisions

### 1. Modelo de base de datos
- Tabla `solicitud_cambio_horario` con `id`, `partida_id`, `equipo_id`, `solicitante_id`, `nuevo_horario`, `fecha_solicitud`, `estado`, `motivo_rechazo`, `fecha_resolucion`, `moderador_id`.
- *Alternativa considerada:* Agregar columnas a `partida` (descartada porque una partida puede tener múltiples solicitudes a lo largo del tiempo según la relación 1 a 0..* en `08-modelo-dominio.md`).

### 2. Vencimiento reactivo de solicitudes
- Toda consulta de solicitudes ejecuta primero `actualizar_solicitudes_vencidas(conexion, ahora)` para pasar a `Vencida` aquellas solicitudes en `Solicitada` cuya partida inicie en 2 horas o menos.
- *Alternativa considerada:* Celery / BackgroundTasks en bucle (innecesario, agrega complejidad y dependencias externas no permitidas en SQLite/FastAPI del curso).

### 3. Registro de auditoría y Discord
- Se registran las operaciones en `integraciones_log` con `sistema = 'Discord'`, manteniendo consistencia con `HU-03` y `HU-06`.

## Risks / Trade-offs

- [Conflicto de fecha en formato texto] $\rightarrow$ Se utiliza siempre formato ISO-8601 (`YYYY-MM-DDTHH:MM`) consistente con el resto de la aplicación.
- [Moderador no asignado intentando resolver] $\rightarrow$ Se valida en el servicio que la persona sea de tipo `Moderador` y que sea el moderador asignado a la partida correspondiente.
