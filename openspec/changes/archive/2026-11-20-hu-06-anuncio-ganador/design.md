# Design

## Context

Ver `proposal.md` para la motivación. El estado actual relevante:

- HU-03 registra el Resultado, actualiza el Bracket, notifica al Organizador y a los Jugadores y deja la partida en `Resultado confirmado` (`app/servicios/resultado.py`). El adaptador `DiscordSimulado` solo tiene `notificar_resultado` y escribe en `integraciones_log`.
- La tabla `notificacion` está dirigida a personas (`destinatario_tipo`, `destinatario_id`, `canal`) y no tiene estado de envío.
- No existe una pantalla del Organizador; la página de inicio solo muestra un texto informativo.
- El `seed` fuerza la final a `Anunciada` con un `UPDATE` manual después de registrar el resultado.
- El modelo de dominio no tiene una clase `Anuncio` y no se quiere crear (decisión confirmada en `.cin324/historias/HU-06.md`).

Restricciones: Python 3.12 + FastAPI + Jinja2 + `sqlite3`; migraciones SQL numeradas; sistemas externos simulados; selector de rol de demostración; una historia por cambio.

## Goals / Non-Goals

**Goals:**
- Publicar al ganador y anunciarlo en Discord automáticamente al confirmarse un resultado.
- Dejar la partida en `Anunciada` y conservar el estado del envío a Discord.
- Dar al Organizador una pantalla de solo lectura con Anuncios y partidas (opción B).
- Ser idempotente: una partida tiene como máximo un anuncio.

**Non-Goals:**
- Integración real con Discord o con la API del videojuego (HU-01).
- Reintento automático de envíos pendientes.
- Página pública del torneo (HU-07), autenticación real y entrega del premio.

## Decisions

### 1. Tabla de soporte `anuncio`, sin clase del dominio

La publicación se guarda en una tabla técnica:

```sql
CREATE TABLE anuncio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partida_id INTEGER NOT NULL UNIQUE REFERENCES partida (id) ON DELETE CASCADE,
    resultado_id INTEGER NOT NULL UNIQUE REFERENCES resultado (id) ON DELETE CASCADE,
    fecha_hora_publicacion TEXT NOT NULL,
    discord_estado TEXT NOT NULL CHECK (discord_estado IN ('Enviado', 'Pendiente')),
    discord_fecha_hora TEXT,
    discord_detalle TEXT
);
```

No guarda ganador ni marcador: se derivan de `resultado_marcador`. El `UNIQUE` en `partida_id` y `resultado_id` garantiza la idempotencia.

**Alternativa descartada:** reutilizar `notificacion` con `canal = 'Discord'`. Esa tabla representa avisos a personas, exige `destinatario_id` y no tiene estado de envío. Agregarle una columna mezclaría notificaciones personales con un anuncio de canal.

### 2. La transición a `Anunciada` no depende del éxito de Discord

El ganador se publica en la plataforma antes de llamar a Discord. Si el adaptador falla, se registra `discord_estado = 'Pendiente'` y la partida igualmente pasa a `Anunciada`. Esto respeta el escenario 3 del Gherkin y la salvedad de EST-01 (`11-diagramas-estado.md:26`): el estado refleja la publicación en la plataforma, no el envío externo.

**Alternativa descartada:** mantener la partida en `Resultado confirmado` hasta que Discord responda. Dejaría invisible un ganador ya publicado y contradiría el escenario que exige publicarlo aunque Discord falle.

### 3. El anuncio ocurre dentro del registro del resultado

`registrar_resultado` publica, inserta el `anuncio` y llama a Discord en la misma operación, después de actualizar el bracket y notificar. No se agrega un endpoint ni una tarea en segundo plano: el anuncio es automático y el flujo de DSS-02 ya termina con esas acciones.

**Alternativa descartada:** un endpoint `/partidas/{id}/anunciar`. Obligaría a una acción manual del Organizador, que el Gherkin no pide.

### 4. Adaptador de Discord extensible y fallo simulable

Se agrega `anunciar_ganador(conexion, partida, ganador, marcador, fecha_hora)` a la interfaz `Discord`. `DiscordSimulado` escribe en `integraciones_log` con `operacion = 'anunciar_ganador'` y devuelve `True`. La fábrica `crear_app` acepta un parámetro `discord` para inyectar un adaptador que lanza una excepción en las pruebas; el router lo pasa al servicio.

### 5. Manejo del fallo de Discord

El servicio inserta el anuncio con `discord_estado = 'Pendiente'`, intenta el envío dentro de `try/except` y, si funciona, actualiza a `Enviado` con la fecha. Cualquier excepción del adaptador se registra en `discord_detalle` y no se propaga: la publicación en la plataforma ya está hecha y se confirma con `commit`.

### 6. Pantalla del Organizador (opción B)

- Ruta `GET /organizador?persona_id=<id>`; si no se indica, se usa el primer Organizador.
- Muestra el torneo cuyo `organizador_id` coincide; si no hay, estado vacío.
- Sección **Anuncios** con tarjetas de partidas anunciadas (ganador, marcador, fecha de publicación, estado de Discord) y tarjetas de partidas pendientes con «Falta registrar el resultado».
- Tabla de partidas con fase, fecha, equipos, resultado, ganador, estado y estado del anuncio.
- Solo lectura. No hay formulario de anuncio.
- Se agrega el acceso «Entrar como Organizador» en `index.html`.

### 7. Datos de ejemplo y migración

- `004_anuncios.sql` crea la tabla, sus índices y **rellena** un `anuncio` para cada partida ya `Anunciada` con resultado, usando `resultado.fecha_hora_registro` y `discord_estado = 'Enviado'`. Así las bases existentes no pierden el anuncio de la final.
- El `seed` deja de forzar `Anunciada` con un `UPDATE`: el servicio lo hace al registrar el resultado de la final.

### 8. Pruebas

- Tres pruebas nuevas, una por escenario Gherkin, en `tests/test_hu06.py`.
- La prueba del fallo de Discord crea una app con un adaptador que lanza una excepción.
- Se ajustan las pruebas de HU-03 que esperan `Resultado confirmado` y una sola entrada en `integraciones_log`; ahora el estado final es `Anunciada` y hay dos operaciones de Discord (`notificar_resultado` y `anunciar_ganador`).

## Risks / Trade-offs

- **Cambian las expectativas de HU-03** → se actualizan las pruebas afectadas y se documenta en el README.
- **Un anuncio pendiente puede quedar pendiente para siempre** → el estado se muestra en la pantalla del Organizador; el reintento queda fuera de alcance.
- **`resultado.moderador_id` es `NOT NULL`** → un resultado automático no se puede persistir todavía; es deuda de HU-01, no de este cambio.
- **La tabla `anuncio` no guarda el ganador** → si un resultado se corrigiera en el futuro, el anuncio mostraría el ganador vigente. Es coherente con la regla actual de un único resultado por partida.
- **Backfill en la migración** → se ejecuta una sola vez y solo afecta partidas `Anunciada` con resultado; no modifica datos existentes.

## Migration Plan

1. Aplicar `004_anuncios.sql` al arrancar la app (el mecanismo de migraciones ya existe).
2. Backfill de anuncios para partidas `Anunciada` con resultado.
3. Recrear `data/app.db` con el `seed` para la demostración local.
4. Rollback: eliminar la tabla `anuncio`; no hay cambios en tablas existentes.

## Open Questions

Ninguna que afecte las especificaciones, el enfoque o las tareas.
