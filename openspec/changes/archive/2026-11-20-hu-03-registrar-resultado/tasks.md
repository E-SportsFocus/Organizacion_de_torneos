# Tasks — HU-03 · Registro manual del resultado

## 1. Base de datos y datos de ejemplo

- [x] 1.1 Crear `app/db/migrations/003_resultados_bracket_notificaciones.sql` con las tablas `resultado`, `resultado_marcador`, `bracket`, `bracket_actualizacion`, `notificacion` e `integraciones_log`; recrear `persona` para admitir `Organizador` y agregar `torneo.organizador_id`. Verificar aplicándola sobre una copia de `data/app.db` y comprobando las tablas y columnas con `sqlite3`.
- [x] 1.2 Actualizar `app/db/seed.py` con Óscar Réplica (Moderador no asignado), Olga Organización (Organizador), el organizador del torneo, la sexta partida `Pendiente de resultado` y el resultado sembrado de la partida `Anunciada` con su bracket e historial. Verificar en una base temporal que el seed crea 6 partidas, 2 moderadores, 1 organizador y un bracket con historial.
- [x] 1.3 Ejecutar `pytest tests/test_hu04.py` y verificar que las pruebas de disponibilidad siguen pasando con el nuevo seed y la migración.

## 2. Lógica de registro y simulación

- [x] 2.1 Crear `app/servicios/resultado.py` con las validaciones, la transacción, la actualización del bracket, el registro de notificaciones y la transición `Pendiente de resultado → Resultado confirmado`. Verificar con pruebas unitarias del registro correcto y de cada rechazo.
- [x] 2.2 Crear `app/integraciones/discord.py` con la interfaz `Discord` y `DiscordSimulado`, que registra la llamada en `integraciones_log` y devuelve éxito. Verificar que una llamada deja la fila de log y no hace ninguna petición de red.
- [x] 2.3 Definir en el servicio los mensajes de error y de éxito aprobados en la ficha. Verificar que cada variante devuelve el texto esperado.

## 3. Rutas y pantallas

- [x] 3.1 Actualizar `app/templates/index.html` para listar moderadores y al Organizador, y `app/templates/moderador.html` para recibir `persona_id`, mostrar el resultado y el ganador, y mostrar el formulario solo en las partidas `Pendiente de resultado`. Verificar que la página carga con cada rol y muestra el formulario correcto.
- [x] 3.2 Crear `app/rutas/resultado.py` con `POST /partidas/{partida_id}/resultado`, registrarlo en `app/fabrica.py` y manejar el éxito y los errores. Verificar con `TestClient` el registro, el rechazo y la redirección al moderador.
- [x] 3.3 Crear `app/templates/bracket.html` y la ruta `GET /bracket` con el bracket calculado y el historial de actualizaciones. Verificar que muestra el resultado sembrado y el que se registra desde la aplicación.
- [x] 3.4 Agregar los enlaces de navegación al bracket y al moderador en `base.html` o en las pantallas correspondientes. Verificar que se llega a las dos vistas desde el inicio.

## 4. Pruebas de los escenarios Gherkin

- [x] 4.1 Prueba «Un Moderador asignado registra el resultado completo de una partida pendiente»: verifica el resultado, la identidad del Moderador, la fecha, la hora, el origen `manual`, el bracket, la notificación y el estado `Resultado confirmado`.
- [x] 4.2 Prueba «Un jugador no puede registrar un resultado»: verifica el rechazo y que no se crean filas en `resultado` ni en `bracket`.
- [x] 4.3 Prueba «Un Moderador no asignado a la partida no puede registrar el resultado»: verifica el rechazo y que el estado y el resultado no cambian.
- [x] 4.4 Prueba «Un resultado incompleto no se confirma»: verifica el mensaje «Completa el resultado de ambos equipos.» y la ausencia de resultado.
- [x] 4.5 Prueba «Un empate no se acepta como resultado»: verifica el mensaje «El resultado no puede ser empate; debe haber un ganador.» y la ausencia de resultado.
- [x] 4.6 Ejecutar `pytest` completo (HU-03 y HU-04) y verificar que todas las pruebas pasan.

## 5. Cierre

- [x] 5.1 Ejecutar el recorrido manual de los 5 escenarios con la base sembrada y verificar los mensajes, el bracket y el historial.
- [x] 5.2 Actualizar `README.md` con la instalación, la recreación de `data/app.db`, el arranque, las rutas nuevas (`/moderador`, `/bracket`) y `pytest`. Verificar que los comandos funcionan tal como están escritos.

## Workflow follow-up

- Archivar el cambio después de la validación del estudiante.
- Actualizar `.cin324/proyecto.md` con el cambio, la fecha y las observaciones.
- Hacer el commit con el mensaje `HU-03: registro manual del resultado (cambio hu-03-registrar-resultado)`.
