# Design — HU-03 · Registro manual del resultado

## Context

La aplicación ya tiene las migraciones `001` (equipos, torneos, personas y partidas) y `002` (disponibilidad). La partida ya admite los estados `Programada`, `En curso`, `Pendiente de resultado`, `Resultado confirmado` y `Anunciada`, pero no existe dónde guardar el resultado, el bracket ni las notificaciones. `persona.tipo` solo permite `Jugador` y `Moderador`, y `torneo` no tiene organizador asociado. La vista del Moderador lista todas las partidas y no distingue quién es el moderador seleccionado. Los dos equipos de una partida se obtienen de sus registros de `disponibilidad`.

La motivación y el alcance están en `proposal.md`; los requisitos, en `specs/resultado/spec.md`.

## Goals / Non-Goals

**Goals:**
- Registrar el resultado manual con la identidad del Moderador, la fecha, la hora y el origen `manual`.
- Validar permisos, estado de la partida, marcadores completos y ausencia de empate.
- Actualizar el bracket y conservar el historial de cada actualización.
- Registrar la notificación al Organizador y a los Jugadores, con Discord simulado.
- Pasar la partida de `Pendiente de resultado` a `Resultado confirmado`.

**Non-Goals:**
- La integración con la API y la transición automática `En curso → Pendiente de resultado` (HU-01).
- La vista/consulta de la notificación y del bracket por el jugador (HU-02) y el anuncio del ganador (HU-06).
- La tabla `partida_equipo`; los equipos se siguen infiriendo de `disponibilidad`.
- Autenticación real, integración real con Discord y requisitos no funcionales.

## Decisions

### 1. Esquema de datos

Se agrega la migración `003_resultados_bracket_notificaciones.sql`:

| Tabla | Columnas principales | Origen en el modelo |
|-------|----------------------|---------------------|
| `resultado` | `id`, `partida_id` único, `moderador_id`, `fecha_hora_registro`, `origen` (`manual`/`automatico`) | Clase Resultado; asociaciones Partida 1–0..1 Resultado y Moderador 0..1–0..* Resultado |
| `resultado_marcador` | `resultado_id`, `equipo_id`, `marcador` (entero ≥ 0); PK compuesta | «marcador por equipo» de Resultado |
| `bracket` | `id`, `torneo_id` único, `ultima_actualizacion` | Clase Bracket; Torneo 1–1 Bracket |
| `bracket_actualizacion` | `id`, `bracket_id`, `resultado_id` único, `fecha_hora` | «historial de actualizaciones» de Bracket |
| `notificacion` | `id`, `partida_id`, `resultado_id`, `destinatario_tipo` (`Organizador`/`Jugador`), `destinatario_id`, `mensaje`, `fecha_hora`, `leida` | RP-06 y DSS-02 |
| `integraciones_log` | `id`, `sistema`, `operacion`, `detalle`, `fecha_hora` | Registro de la simulación de Discord |

Además:
- `persona.tipo` se amplía con `Organizador`. SQLite no permite modificar un `CHECK` con `ALTER TABLE`, así que la migración recrea `persona` (crear `persona_nueva`, copiar, borrar la anterior y renombrar), con `PRAGMA foreign_keys = OFF` durante la operación. La clave foránea de `partida.moderador_id` se conserva.
- `torneo` recibe `organizador_id` (nullable, FK a `persona`), que representa la asociación `Organizador 1 – 0..* Torneo`.

**Alternativas descartadas:** guardar los dos marcadores como columnas de `resultado` (más simple, pero no asocia cada marcador a su equipo y duplica la relación Partida–Equipo) y guardar el bracket completo como una tabla (duplicaría datos que ya están en partidas y resultados). Se prefiere el marcador por equipo y el bracket calculado.

### 2. Transición de estado y transacción

Una sola función de servicio, `registrar_resultado(conexion, partida_id, persona_id, marcadores, ahora)`, concentra la guarda de EST-01:

1. Verifica que la persona sea `Moderador` y que sea el `moderador_id` de la partida.
2. Verifica que la partida esté en `Pendiente de resultado` y que no tenga ya un resultado.
3. Verifica que existan exactamente dos equipos para la partida en `disponibilidad`.
4. Valida los dos marcadores (presentes, enteros ≥ 0, distintos).
5. Inserta `resultado`, `resultado_marcador`, `bracket`, `bracket_actualizacion` y las `notificacion` en una sola transacción.
6. Actualiza `partida.estado` a `Resultado confirmado`.
7. Llama al adaptador de Discord simulado y registra la llamada en `integraciones_log`.

Si cualquier validación falla, no se escribe nada y se lanza `ErrorResultado` con un mensaje para el usuario. El estado inicial no se crea aquí: la partida llega en `Pendiente de resultado` desde el seed o, en el futuro, desde HU-01.

### 3. Identificación de los equipos y de los marcadores

Los dos equipos se leen de `disponibilidad` para la partida. El formulario usa un campo por equipo, `marcador_<equipo_id>`, y el servicio construye un diccionario `{equipo_id: marcador}`. Así no se depende del orden de los equipos ni de una noción de «local/visitante» que el modelo no define.

Se valida que la partida tenga exactamente dos equipos; si no, se rechaza con «La partida no tiene dos equipos registrados.». Es una guarda de implementación, no una regla nueva del dominio.

### 4. Permisos y selector de rol

La aplicación no tiene autenticación real. El índice lista los moderadores y el Organizador; la vista del Moderador recibe `persona_id` por la URL y el formulario lo envía en el `POST`. El servicio valida el rol y la asignación. Un Jugador o un Moderador no asignado recibe un `400` con el mensaje correspondiente y la partida no cambia.

Mensajes propuestos:
- `Solo un Moderador puede registrar el resultado de una partida.`
- `Solo el Moderador asignado a la partida puede registrar el resultado.`
- `La partida no está pendiente de resultado.`
- `La partida ya tiene un resultado registrado.`
- `Completa el resultado de ambos equipos.`
- `El resultado no puede ser empate; debe haber un ganador.`
- `El marcador debe ser un número entero mayor o igual a 0.`
- `Resultado registrado. Ganador: <equipo>.`

### 5. Bracket calculado e historial

El contenido del bracket se calcula desde `partida`, `resultado`, `resultado_marcador` y `disponibilidad`: fases, equipos, marcador, ganador y estado. La tabla `bracket` solo guarda la última actualización y `bracket_actualizacion` guarda el historial con el resultado que la originó. La vista `/bracket` muestra el bracket y, debajo, el historial (fecha, hora, partida y marcador).

El bracket se crea la primera vez que se registra un resultado en el torneo (`INSERT ... ON CONFLICT` o búsqueda previa) y su `ultima_actualizacion` se actualiza en la misma transacción.

### 6. Notificaciones y Discord simulado

Para cada resultado se crean filas en `notificacion`:
- una para el Organizador del torneo (`torneo.organizador_id`), si existe;
- una por cada Jugador de los dos equipos.

El mensaje incluye la partida, los equipos, el marcador, el ganador y una referencia al bracket. El canal de la plataforma es la propia tabla. La publicación en Discord se resuelve con `app/integraciones/discord.py`:
- interfaz `Discord` con `notificar_resultado(...)`;
- `DiscordSimulado`, que registra la llamada en `integraciones_log` y devuelve éxito.

La implementación se selecciona por configuración (por defecto, la simulada). No hay llamada de red.

### 7. Rutas y pantallas

| Ruta | Método | Función |
|------|--------|---------|
| `/` | GET | Selector de rol con jugadores, moderadores y Organizador |
| `/moderador?persona_id=<id>` | GET | Partidas y formulario de resultado para las que están `Pendiente de resultado` |
| `/partidas/{partida_id}/resultado` | POST | Registra el resultado y redirige a `/moderador?persona_id=<id>&mensaje=ok` o vuelve a mostrar el error |
| `/bracket` | GET | Bracket calculado e historial de actualizaciones |

`moderador.html` muestra el marcador y el ganador de las partidas con resultado, y el formulario de dos campos para las pendientes. `bracket.html` es una vista compartida; HU-02 la reutilizará para el jugador y HU-06 añadirá el anuncio.

### 8. Datos de ejemplo y pruebas

- `seed.py` agrega a **Óscar Réplica** (Moderador no asignado a la partida pendiente), a **Olga Organización** (Organizador) y asigna el organizador al torneo. Agrega la sexta partida **Bravo vs Charlie**, `Pendiente de resultado`, asignada a Marta. A la partida `Anunciada` (Bravo vs Delta) le siembra un resultado 2–1 con su bracket y su historial, para que el bracket no esté vacío.
- `sembrar` sigue siendo idempotente y solo actúa si el torneo no existe. Para ver los datos nuevos en `data/app.db`, el `README` indica borrar esa base y volver a ejecutar el seed; las pruebas usan una base temporal.
- `tests/test_hu03.py` tiene una prueba por escenario Gherkin (5), usando la fixture `cliente` y creando los datos con `DatosDePrueba`. Las pruebas de rechazo comprueban además que no se crearon filas en `resultado` ni se actualizó el bracket.

## Risks / Trade-offs

- **Recrear `persona` para ampliar el `CHECK`:** puede afectar la FK de `partida.moderador_id`. → Se hace con `PRAGMA foreign_keys = OFF`, se copian los datos y se prueba sobre una base existente antes de dar la tarea por terminada.
- **Base existente sin los datos nuevos:** `sembrar` no vuelve a ejecutarse si el torneo ya existe. → El `README` indica borrar `data/app.db` y volver a sembrar; las pruebas no dependen de la base de desarrollo.
- **Equipos inferidos de `disponibilidad`:** si una partida no tiene exactamente dos registros, el registro se rechaza. → Se valida y se deja anotada la deuda de `partida_equipo` para un cambio futuro.
- **Notificación al Organizador si `torneo.organizador_id` es nulo:** no habría destinatario. → Se notifica solo si existe; el seed lo asigna y los jugadores siempre reciben la suya.
- **Bracket calculado:** no guarda una «foto» histórica del bracket, solo el resultado que originó cada actualización. → Es suficiente para RP-10 y para el alcance del curso; el historial conserva la trazabilidad.
- **Discord simulado:** no hay entrega real. → Se declara en la guía de pruebas y se registra en `integraciones_log`.

## Migration Plan

1. Aplicar la migración `003` al arrancar (el runner ya aplica las migraciones pendientes).
2. Recrear la base de ejemplo (`data/app.db`) y ejecutar `python -m app.db.seed` para los datos nuevos.
3. Verificar con `pytest` y con el recorrido manual de los 5 escenarios.
4. Rollback: al ser una migración aditiva, se puede restaurar una copia de la base anterior; no se reescriben las migraciones `001` y `002`.
