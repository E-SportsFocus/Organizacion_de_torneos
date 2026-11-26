# torneo-publico Specification

## Purpose
Permite que un Visitante consulte al abrir el inicio, de forma pública y sin iniciar sesión, los anuncios de ganadores y el bracket resumido (con enlace al detalle de partidas en `/bracket`), y que navegue entre las vistas desde un menú desplegable con accesos de demostración para cada rol.

## Requirements

### Requirement: Inicio público de solo lectura con el estado del torneo

El sistema DEBE (SHALL) mostrar en la página de inicio el nombre y el juego del torneo, los anuncios de ganadores publicados, un bracket resumido por fases (sin la tabla detallada de partidas) y un enlace hacia el detalle completo en `/bracket`, sin ofrecer acciones para registrar resultados, anunciar ganadores ni modificar datos.

#### Scenario: El visitante consulta el torneo público

- **GIVEN** que el torneo tiene partidas y al menos un ganador anunciado
- **WHEN** el visitante abre la página de inicio
- **THEN** ve el nombre y el juego del torneo
- **AND** ve los anuncios de los ganadores publicados
- **AND** ve el bracket resumido por fases y el enlace al detalle en el bracket
- **AND** no ve la tabla detallada de partidas en el inicio
- **AND** no ve acciones para registrar resultados ni para anunciar ganadores

#### Scenario: El detalle de partidas se consulta en el bracket

- **GIVEN** que el torneo tiene partidas con marcador e historial de actualizaciones
- **WHEN** el visitante abre la página de inicio
- **THEN** el inicio muestra solo el resumen de enfrentamientos por fase
- **AND** el enlace a `/bracket` conduce a la tabla detallada con marcador e historial

### Requirement: Las partidas sin resultado no muestran ganador

El sistema DEBE (SHALL) mostrar las partidas sin resultado como pendientes y DEBE (SHALL) no mostrar un ganador para ellas.

#### Scenario: Una partida sin resultado no muestra ganador

- **GIVEN** que una partida está en estado "Pendiente de resultado"
- **WHEN** el visitante consulta la página de inicio
- **THEN** la partida aparece como pendiente
- **AND** no se muestra un ganador para esa partida

### Requirement: Menú de navegación y acceso a los roles de demostración

El sistema DEBE (SHALL) mostrar en todas las páginas un botón de menú que despliegue bajo la barra, alineado a la derecha, la navegación (Inicio y Bracket) y «Entrar como» con tres botones: Jugador, Moderador y Organizador. Al pulsar un botón de rol, el sistema DEBE (SHALL) desplegar la lista de personas de ese rol y cerrar cualquier otra lista. El menú DEBE (SHALL) poder cerrarse sin cambiar de página y DEBE (SHALL) indicar visualmente la página activa.

#### Scenario: El visitante abre el menú y cambia de rol

- **GIVEN** que el visitante está en cualquier página de la aplicación
- **WHEN** pulsa el botón de menú
- **THEN** el menú se despliega bajo la barra, alineado a la derecha
- **AND** muestra la navegación (Inicio y Bracket) y los botones Jugador, Moderador y Organizador
- **WHEN** pulsa el botón Jugador
- **THEN** se despliega la lista de jugadores y se cierra cualquier otra lista
- **WHEN** elige un jugador de la lista
- **THEN** entra a la vista del jugador seleccionado

#### Scenario: El menú se cierra sin cambiar de página

- **GIVEN** que el menú está abierto
- **WHEN** el visitante pulsa la X, presiona Esc o hace clic fuera del menú
- **THEN** el menú se cierra
- **AND** la página sigue siendo la misma
