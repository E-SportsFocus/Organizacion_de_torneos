# Design — HU-04 Confirmación de disponibilidad

## Context

Es la primera historia del proyecto: no existe código de la aplicación, solo la documentación de requisitos. Ver `proposal.md` para el porqué. El stack confirmado es Python 3.12 + FastAPI + Jinja2 + `sqlite3` + pytest, con SQLite en `data/app.db`.

La ficha confirmada (`.cin324/historias/HU-04.md`) fija dos puntos relevantes: no hay diagrama de secuencia para CU-01, así que el flujo se toma de la ficha, y la condición «requiere revisión» se calcula al consultar, sin tarea en segundo plano.

## Goals / Non-Goals

**Goals:**
- Modelar en SQLite solo las tablas que esta historia lee o escribe, con los nombres del modelo de dominio.
- Registrar la disponibilidad por equipo y partida, y consultarla desde el rol Moderador.
- Un test de integración por cada uno de los 4 escenarios Gherkin.

**Non-Goals:**
- Transición `Programada → En curso`, resultados, bracket, notificaciones y cambio de horario (otras historias).
- Scheduler o tareas en segundo plano: «requiere revisión» es un cálculo al consultar.
- Autenticación real: selector de rol de demostración.
- Integraciones externas: esta historia no usa ninguna, así que no se crea carpeta `app/integraciones` todavía.

## Decisions

### Tablas derivadas del modelo de dominio

Se crean solo las clases que la historia usa. La herencia Persona → Jugador/Moderador se resuelve con **una tabla `persona` y columna `tipo`** (regla de traducción del curso), con los atributos propios como columnas anulables.

| Tabla | Columnas | Origen |
|---|---|---|
| `persona` | `id`, `nombre`, `cuenta_discord`, `tipo` (`Jugador`/`Moderador`), `nickname`, `pais`, `equipo_id` | Persona, Jugador, Moderador (herencia → una tabla) |
| `equipo` | `id`, `nombre`, `pais` | Equipo |
| `torneo` | `id`, `nombre`, `juego`, `zona_horaria` | Torneo |
| `partida` | `id`, `torneo_id` (FK, `ON DELETE CASCADE`), `moderador_id` (FK a `persona`), `fecha_hora` (ISO 8601), `fase`, `estado` | Partida (`contiene` composición → cascada; `arbitrada por` 0..* a 1) |
| `disponibilidad` | `id`, `equipo_id` (FK), `partida_id` (FK, `ON DELETE CASCADE`), `confirmada` (`Pendiente`/`Confirmada`), `fecha_confirmacion` (ISO 8601, nula) | Disponibilidad (`Equipo 1 – 0..*`, `0..* – 1 Partida`) |

Restricciones: `UNIQUE(equipo_id, partida_id)` en `disponibilidad` (una por equipo y partida); `CHECK (confirmada IN ('Pendiente','Confirmada'))`; `CHECK (estado IN ('Programada','En curso','Pendiente de resultado','Resultado confirmado','Anunciada'))` en `partida` (estados de EST-01); `PRAGMA foreign_keys = ON` por conexión.

Alternativa descartada: tabla por subclase (`jugador`, `moderador`). Se descarta por ser más tablas y JOINs para una historia que solo lee nombre y pertenencia al equipo.

### Lógica en `app/servicios/disponibilidad.py`

- `confirmar_disponibilidad(conexion, disponibilidad_id, persona_id, ahora)` valida en este orden: la persona existe y es `Jugador`; la partida está en estado `Programada`; la disponibilidad es de su equipo; la disponibilidad no está ya `Confirmada`; entonces guarda `Confirmada` + `fecha_confirmacion = ahora`.
- `listar_partidas_equipo(conexion, equipo_id, ahora)` devuelve partidas con la disponibilidad del equipo y una marca `requiere_revision`.
- `listar_partidas_moderador(conexion, ahora)` devuelve partidas con la disponibilidad de ambos equipos y la marca `requiere_revision`.

No se crea una máquina de estados para `Disponibilidad`: el modelo no la define y la ficha lo confirmó como atributo. La transición `Pendiente → Confirmada` se aplica en la función anterior y es idempotente.

### Regla de las 8 horas (decisión C8 de la validación)

La confirmación se acepta en cualquier momento mientras la partida esté `Programada`; no se rechaza por anticipación. Las 8 horas solo alimentan la marca de revisión:

`requiere_revision = partida.estado == 'Programada' AND algún equipo con disponibilidad 'Pendiente' AND ahora >= partida.fecha_hora - 8 horas`

Así se cumplen los escenarios 2 y 3 (`≤ 8 h` con pendiente, y hora de inicio alcanzada) sin tarea en segundo plano.

### Reloj inyectable

Todas las funciones reciben `ahora` (datetime). La aplicación usa `datetime.now()`; los tests pasan una hora fija para que los escenarios de plazo sean deterministas.

### Rutas y pantallas (CU-01, flujo de la ficha)

| Método y ruta | Pantalla | Acción |
|---|---|---|
| `GET /` | `index.html` | Selector de rol de demostración (Jugador / Moderador) |
| `GET /jugador?persona_id=<id>` | `jugador.html` | Partidas programadas del equipo, disponibilidad y botón «Confirmar» |
| `POST /disponibilidad/{id}/confirmar` | redirige a `/jugador` | Confirma; en error vuelve a la vista con el mensaje |
| `GET /moderador` | `moderador.html` | Partidas con disponibilidad de ambos equipos y la marca «requiere revisión» |

Mensajes de error definidos (para la revisión de especificaciones):
- Partida iniciada o finalizada: «La partida ya inició o finalizó; el plazo para confirmar la disponibilidad venció.»
- Disponibilidad ya confirmada: «La disponibilidad de este equipo ya estaba confirmada.»
- Jugador ajeno al equipo: «No puedes confirmar la disponibilidad de un equipo al que no perteneces.»
- Confirmación exitosa: «Disponibilidad del equipo confirmada.»
- Moderador: «Requiere revisión» junto a la partida.

### Migraciones y datos de ejemplo

- `app/db/migrations/001_personas_equipos_torneos_partidas.sql` y `002_disponibilidad.sql`, aplicadas al arrancar y registradas en `schema_migrations`.
- `python -m app.db.seed` idempotente: 1 torneo, 4 equipos de 2 jugadores, 1 moderador y 5 partidas (en 6 h, en 30 h, una `Programada` con la hora de inicio ya pasada, una `En curso` y una finalizada `Anunciada`). Cada partida nace con dos `disponibilidad` en `Pendiente`.
- Los tests usan una base temporal con el mismo esquema y su propio seed controlado.

## Risks / Trade-offs

- **Fechas del seed relativas a la ejecución** → los datos de ejemplo se generan con desplazamientos desde la hora actual para que los plazos sean visibles, y los tests no dependen del seed sino de datos propios con reloj fijo.
- **«Requiere revisión» es calculado, no persistido** → si otra historia necesita reaccionar a ese estado (por ejemplo, impedir el inicio), tendrá que leer la misma regla; se documenta en el módulo de servicio.
- **Una sola tabla `persona` con `tipo`** → mezcla columnas de roles; se acepta por simplicidad y porque el curso lo propone para la herencia.
- **Confirmación sin guarda de 8 horas** → un jugador puede confirmar con mucha anticipación y luego cambiar de idea; no hay escenario para desconfirmar, se deja fuera de alcance.
