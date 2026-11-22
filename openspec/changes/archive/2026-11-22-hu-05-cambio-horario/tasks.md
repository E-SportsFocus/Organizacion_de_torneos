# Tasks

## 1. Migración y adaptador de Discord

- [x] 1.1 Crear migración `app/db/migrations/005_cambio_horario.sql` con la tabla `solicitud_cambio_horario` e índices; verificar con `conectar()` y `aplicar_migraciones()` que se aplica correctamente.
- [x] 1.2 Extender `app/integraciones/discord.py` con `avisar_solicitud_cambio` y `avisar_resolucion_cambio` en `Discord` y `DiscordSimulado`; verificar inserción en `integraciones_log`.

## 2. Servicios de negocio

- [x] 2.1 Implementar `app/servicios/cambio_horario.py` con `solicitar_cambio_horario`, validando pertenencia del jugador al equipo, estado `Programada`, regla de más de 2 horas y fecha futura.
- [x] 2.2 Implementar `aprobar_solicitud` en el servicio: verificar rol de moderador, actualizar solicitud a `Aprobada`, actualizar `fecha_hora` de la partida y registrar en Discord.
- [x] 2.3 Implementar `rechazar_solicitud` en el servicio: verificar motivo obligatorio, actualizar solicitud a `Rechazada`, conservar horario original de la partida y registrar en Discord.
- [x] 2.4 Implementar `actualizar_solicitudes_vencidas` y funciones de consulta `listar_solicitudes_equipo` y `listar_solicitudes_partida`.

## 3. Rutas y vistas

- [x] 3.1 Crear `app/rutas/cambio_horario.py` con endpoints `POST /cambio-horario/solicitar`, `POST /cambio-horario/{id}/aprobar` y `POST /cambio-horario/{id}/rechazar`; registrar router en `app/fabrica.py`.
- [x] 3.2 Actualizar `app/rutas/disponibilidad.py` y `app/templates/jugador.html` para listar solicitudes y formulario de solicitud de cambio de horario cuando faltan más de 2 horas.
- [x] 3.3 Actualizar `app/rutas/resultado.py` y `app/templates/moderador.html` para listar solicitudes pendientes y acciones de aprobación/rechazo con motivo.

## 4. Pruebas automatizadas y documentación

- [x] 4.1 Crear `tests/test_hu05.py` con pruebas para los 5 escenarios Gherkin de HU-05; verificar que todas pasan.
- [x] 4.2 Actualizar `app/db/seed.py` con datos de ejemplo para cambio de horario.
- [x] 4.3 Actualizar `README.md` y `.cin324/proyecto.md`.
- [x] 4.4 Ejecutar suite completa de pruebas (`pytest`) y validar OpenSpec (`openspec.cmd validate --all`).
