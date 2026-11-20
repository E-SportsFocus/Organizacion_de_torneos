# Tasks

## 1. Migración de anuncios

- [x] 1.1 Crear `app/db/migrations/004_anuncios.sql` con la tabla `anuncio`, sus índices (`partida_id`, `resultado_id`, `discord_estado`) y el relleno de anuncios para las partidas ya `Anunciada` con resultado; verificar que la migración se aplica en una base nueva y queda registrada en `schema_migrations`.
- [x] 1.2 Verificar el relleno con una base de prueba: una partida `Anunciada` con resultado obtiene un `anuncio` con `discord_estado = 'Enviado'`, y una partida pendiente no obtiene anuncio.

## 2. Publicación y anuncio automático

- [x] 2.1 Agregar `anunciar_ganador` a la interfaz `Discord` y a `DiscordSimulado`, registrando la operación `anunciar_ganador` en `integraciones_log`; verificar con una prueba que el log contiene esa operación y el mensaje del ganador.
- [x] 2.2 Implementar en `app/servicios/resultado.py` la publicación del ganador: insertar el anuncio, pasar la partida a `Anunciada` y enviar el anuncio a Discord; verificar que tras registrar un resultado existen el `anuncio`, el estado `Anunciada` y la operación de Discord.
- [x] 2.3 Manejar el fallo de Discord: capturar la excepción, guardar `discord_estado = 'Pendiente'` y confirmar la publicación; verificar que el resultado y el anuncio quedan persistidos y la partida sigue en `Anunciada`.
- [x] 2.4 Permitir que `crear_app` reciba un adaptador de Discord y que el router lo use; verificar con una app de prueba que el adaptador inyectado recibe la llamada de anuncio.
- [x] 2.5 Agregar `tests/test_hu06.py` con el escenario «El ganador se publica al confirmarse el resultado»: verificar anuncio, estado `Anunciada`, log de Discord y ganador visible en `/organizador`.
- [x] 2.6 Agregar el escenario «Un fallo en Discord no impide publicar el ganador en la plataforma»: usar el adaptador que falla y verificar publicación en la plataforma y `discord_estado = 'Pendiente'`.

## 3. Pantalla del Organizador

- [x] 3.1 Implementar `app/rutas/organizador.py` con `GET /organizador?persona_id=...`, seleccionando el primer Organizador si no se indica; verificar que responde 200 y muestra el torneo del Organizador.
- [x] 3.2 Crear `app/templates/organizador.html` con la sección **Anuncios** (ganador, marcador, fecha de publicación y estado de Discord) y la tabla de partidas con resultado, ganador y estado del anuncio; verificar el contenido renderizado con una partida anunciada.
- [x] 3.3 Agregar en `index.html` el acceso «Entrar como Organizador»; verificar que el enlace abre `/organizador` con el organizador de ejemplo.
- [x] 3.4 Agregar el escenario «No se anuncia un ganador con resultado pendiente»: verificar que la pantalla no muestra ganador e indica «Falta registrar el resultado».

## 4. Datos de ejemplo, pruebas existentes y documentación

- [x] 4.1 Actualizar `app/db/seed.py`: quitar el `UPDATE` manual a `Anunciada` y dejar que el servicio cree el anuncio de la final; verificar que la final sembrada queda `Anunciada` con un anuncio `Enviado` y que el seed sigue siendo idempotente.
- [x] 4.2 Ajustar `tests/test_hu03.py` para el nuevo estado final `Anunciada` y las dos operaciones de Discord (`notificar_resultado` y `anunciar_ganador`); verificar que las pruebas de HU-03 siguen pasando.
- [x] 4.3 Actualizar `README.md` con la ruta `/organizador`, el anuncio automático y el estado `Anunciada`; verificar que las instrucciones de instalación, ejecución y prueba siguen siendo correctas.
- [x] 4.4 Ejecutar la suite completa con `.venv\Scripts\python.exe -m pytest` y `openspec.cmd validate hu-06-anuncio-ganador`; verificar que todo pasa y que la validación de OpenSpec es correcta.

## Workflow follow-up

- Sincronizar las capacidades `anuncio` y `resultado` después de la implementación.
- Archivar el cambio `hu-06-anuncio-ganador` cuando el estudiante lo apruebe.
- Verificar el cambio archivado en `openspec/changes/archive/`.
