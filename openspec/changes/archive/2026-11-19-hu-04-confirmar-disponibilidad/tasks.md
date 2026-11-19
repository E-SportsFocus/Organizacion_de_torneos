# Tasks — HU-04 Confirmación de disponibilidad

## 1. Estructura del proyecto y dependencias

- [x] 1.1 Crear `requirements.txt` con `fastapi`, `uvicorn[standard]`, `jinja2`, `python-multipart`, `pytest` y `httpx`; verificar que `pip install -r requirements.txt` termina sin errores en un `venv`.
- [x] 1.2 Crear la estructura `app/` (`main.py`, `db/`, `dominio/`, `servicios/`, `rutas/`, `templates/`) y `tests/`; verificar que `uvicorn app.main:app` arranca y `GET /` responde 200 con una página mínima.

## 2. Base de datos y datos de ejemplo

- [x] 2.1 Crear `app/db/migrations/001_personas_equipos_torneos_partidas.sql` con las tablas `persona`, `equipo`, `torneo` y `partida` (FK, `CHECK` de estados de EST-01 y `ON DELETE CASCADE` del torneo); verificar aplicándola sobre una base vacía y consultando `sqlite_master`.
- [x] 2.2 Crear `app/db/migrations/002_disponibilidad.sql` con la tabla `disponibilidad` (`UNIQUE(equipo_id, partida_id)`, `CHECK` de `Pendiente`/`Confirmada` y FK en cascada a `partida`); verificar que la migración aplica después de la 001.
- [x] 2.3 Implementar `app/db/conexion.py` para abrir `data/app.db`, activar `PRAGMA foreign_keys = ON` y aplicar las migraciones en orden registrándolas en `schema_migrations`; verificar que dos arranques seguidos no reaplican migraciones.
- [x] 2.4 Implementar `app/db/seed.py` idempotente (1 torneo, 4 equipos de 2 jugadores, 1 moderador, 4 partidas —en 6 h, en 30 h, iniciada hace 1 h y finalizada— y 2 disponibilidades `Pendiente` por partida); verificar que `python -m app.db.seed` dos veces deja los mismos conteos.
- [x] 2.5 Crear en `tests/conftest.py` una fixture de base SQLite temporal con el esquema y datos controlados (reloj fijo) y verificar con una prueba trivial que la fixture responde una consulta.

## 3. Lógica de disponibilidad

- [x] 3.1 Implementar `listar_partidas_equipo(conexion, equipo_id, ahora)` en `app/servicios/disponibilidad.py` con la disponibilidad del equipo; verificar con una prueba que devuelve solo las partidas de ese equipo.
- [x] 3.2 Implementar `listar_partidas_moderador(conexion, ahora)` con la disponibilidad de ambos equipos y la marca `requiere_revision` según la regla de las 8 horas y el estado `Programada`; verificar con pruebas de partida a 6 h, a 30 h y con la hora de inicio pasada.
- [x] 3.3 Implementar `confirmar_disponibilidad(conexion, disponibilidad_id, persona_id, ahora)` con las validaciones y los mensajes del diseño (jugador del equipo, partida `Programada`, no confirmada antes) y guardar `fecha_confirmacion`; verificar con pruebas cada rechazo y el caso exitoso.

## 4. Pantallas, rutas y pruebas por escenario

- [x] 4.1 Crear `app/templates/base.html` e `index.html` con el selector de rol de demostración (Jugador / Moderador); verificar que la página lista los jugadores de ejemplo y navega a cada rol.
- [x] 4.2 Crear `GET /jugador` y `POST /disponibilidad/{id}/confirmar` con su plantilla: partidas del equipo, estado de disponibilidad y mensajes de éxito o error; verificar a mano la confirmación y un intento sobre una partida iniciada.
- [x] 4.3 Crear `GET /moderador` con la plantilla que muestra ambos equipos, su disponibilidad y «Requiere revisión»; verificar a mano con los datos de ejemplo.
- [x] 4.4 Escribir las 4 pruebas de integración con `TestClient`, nombradas `HU-04 · <escenario>`: confirmación dentro del plazo, equipo sin confirmar pendiente, partida que no inicia con un equipo pendiente y confirmación fuera del plazo; verificar que `pytest` pasa completo.
- [x] 4.5 Actualizar `README.md` con cómo instalar, ejecutar (`python -m app.db.seed`, `uvicorn app.main:app --reload`), la URL, los datos de ejemplo y cómo correr `pytest`; verificar que los comandos escritos funcionan tal cual.

## Workflow follow-up

- Revisar las especificaciones con el estudiante (paso 6 de `cin324-generar-app`).
- Archivar el cambio `hu-04-confirmar-disponibilidad` después de la validación del sistema.
