# Proposal

## Why

Hoy el estado del torneo solo se puede consultar entrando como Jugador, Moderador u Organizador, y la navegación horizontal mezcla los accesos internos con las vistas de consulta. El profesor señaló que la plataforma se ve desordenada. HU-07 convierte el inicio en una página pública de solo lectura con los anuncios de ganadores, el bracket y las partidas, y agrega un menú desplegable común que ordena la navegación y conserva el selector de rol de demostración. Esto completa la parte «plataforma» de RP-07 sin agregar requisitos funcionales nuevos.

## What Changes

- La página de inicio (`/`) pasa a mostrar el nombre y el juego del torneo, los anuncios de ganadores publicados, el bracket y la tabla de partidas.
- La página es de solo lectura: no tiene formularios ni botones para registrar resultados, anunciar ganadores ni modificar el torneo.
- Las partidas sin resultado se muestran como pendientes y no inventan un ganador.
- Se retiran del inicio las tarjetas duplicadas de Jugador, Moderador y Organizador; esos accesos quedan en el menú desplegable.
- Se conserva `/torneo` como redirección al inicio para no romper enlaces anteriores.
- Se reemplaza la navegación horizontal de `base.html` por una barra con la marca a la izquierda y un botón de menú (☰) a la derecha.
- El botón despliega bajo la barra, alineado a la derecha, el menú con «Navegación» (Inicio y Bracket) y «Entrar como» con los botones Jugador, Moderador y Organizador.
- Al pulsar un rol se despliega la lista de personas de ese rol; solo una lista queda abierta a la vez y el flujo de acceso sigue igual.
- El menú se cierra con la X, con `Esc` o con un clic fuera, sin cambiar de página; en móvil ocupa todo el ancho y en escritorio 360 px.
- Los datos de los roles se inyectan en todas las plantillas mediante un procesador de contexto, para no repetir consultas en cada ruta.
- Se agregan pruebas de la página pública y del menú desplegable.

## Capabilities

### New Capabilities
- `torneo-publico`: consulta pública de solo lectura del torneo y menú desplegable de navegación con accesos de demostración a los roles.

### Modified Capabilities
- Ninguna. `anuncio`, `resultado` y `disponibilidad` no cambian su comportamiento; la página pública solo lee datos existentes.

## Impact

- `app/rutas/torneo.py` y `app/fabrica.py`: nueva vista para `/`, redirección de `/torneo` y registro del router.
- `app/templates/torneo.html`: contenido público del inicio.
- `app/rutas/disponibilidad.py`: se retira la vista de inicio anterior.
- `app/templates/base.html`: barra blanca con menú hamburguesa, menú desplegable, estilos y JavaScript.
- `tests/test_hu07.py`: pruebas de los escenarios.
- `README.md`: recorrido de HU-07 y descripción del menú.
- No hay migraciones ni cambios en el modelo de dominio.
- `07-criterios-aceptacion.md`, `09-casos-de-uso.md` y `12-trazabilidad.md` documentan HU-07, el actor Visitante y CU-07.

## Fuera de alcance

- Autenticación real y permisos.
- Reintento del envío a Discord.
- Entrega del premio.
- Registro de resultados y anuncio manual.
- La API del videojuego.
- El historial de actualizaciones del bracket en la página pública.
