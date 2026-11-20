# Proposal

## Why

La HU-06 cierra el flujo de negocio del torneo: hoy el resultado se registra y se notifica, pero el ganador no se publica como anuncio y la partida nunca llega al estado "Anunciada". El Organizador tampoco tiene una pantalla propia y depende de revisar el bracket. Esto deja sin cubrir RP-07 y la actividad del TO-BE que automatiza el anuncio de los ganadores.

## What Changes

- Al confirmarse un resultado, el sistema publica al ganador en la plataforma, envía el anuncio al canal de Discord del torneo (simulado) y deja la partida en estado "Anunciada".
- Si Discord no responde, el ganador se publica igual en la plataforma y el anuncio queda "Pendiente de envío"; la partida igualmente pasa a "Anunciada".
- Se agrega la pantalla del Organizador en `/organizador`, con una sección de Anuncios y una tabla de partidas con su resultado y estado de anuncio (opción B confirmada por el estudiante).
- Se agrega una tabla de soporte `anuncio` para registrar la publicación y el estado del envío a Discord. No se crea una clase `Anuncio` en el dominio.
- Se modifica la especificación de `resultado`: el registro manual ya no deja la partida en "Resultado confirmado", sino que la deja en "Anunciada" tras publicar y anunciar al ganador.
- Se actualizan los datos de ejemplo y las pruebas de HU-03 afectadas por el nuevo estado final.

## Capabilities

### New Capabilities
- `anuncio`: publicación automática del ganador en la plataforma, anuncio en Discord, estado "Anunciada" y consulta del Organizador.

### Modified Capabilities
- `resultado`: el registro manual del resultado publica al ganador y deja la partida en "Anunciada" en lugar de "Resultado confirmado".

## Impact

- `app/servicios/resultado.py`: publicar al ganador y anunciarlo después de confirmar el resultado.
- `app/integraciones/discord.py`: nuevo mensaje `anunciar_ganador` en el adaptador simulado.
- `app/rutas/organizador.py` y `app/fabrica.py`: nueva vista `/organizador`; la fábrica acepta un adaptador de Discord para poder probar el fallo.
- `app/templates/organizador.html` y `app/templates/index.html`: pantalla del Organizador y acceso desde el inicio.
- `app/db/migrations/004_anuncios.sql` y `app/db/seed.py`.
- `tests/test_hu06.py` y ajuste de `tests/test_hu03.py`.
- No cambia el modelo de dominio. Los artefactos del curso se mantienen sin cambios.

## Fuera de alcance

- HU-01 (integración con la API del videojuego): el camino automático queda preparado, pero no se implementa.
- HU-02 (vista del jugador), HU-05 (cambio de horario) y HU-07 (página pública del torneo).
- La entrega física del premio, la integración real con Discord y la autenticación real.
- El reintento automático de un anuncio pendiente: solo se muestra su estado.
