# Spec Delta

## Purpose

Permite que un Visitante consulte al abrir el inicio, de forma pública y sin iniciar sesión, los anuncios de ganadores, el bracket y las partidas del torneo, y que navegue entre las vistas desde un menú lateral con accesos de demostración para cada rol.

## ADDED Requirements

### Requirement: Inicio público de solo lectura con el estado del torneo

El sistema DEBE (SHALL) mostrar en la página de inicio el nombre y el juego del torneo, los anuncios de ganadores publicados, el bracket y la tabla de partidas, sin ofrecer acciones para registrar resultados, anunciar ganadores ni modificar datos.

#### Scenario: El visitante consulta el torneo público

- **GIVEN** que el torneo tiene partidas y al menos un ganador anunciado
- **WHEN** el visitante abre la página de inicio
- **THEN** ve el nombre y el juego del torneo
- **AND** ve los anuncios de los ganadores publicados
- **AND** ve el bracket y la tabla de partidas
- **AND** no ve acciones para registrar resultados ni para anunciar ganadores

#### Scenario: El enlace anterior al torneo sigue funcionando

- **GIVEN** que un visitante tiene guardado el enlace `/torneo`
- **WHEN** abre ese enlace
- **THEN** el sistema lo redirige a la página de inicio
- **AND** ve el estado público del torneo

### Requirement: Las partidas sin resultado no muestran ganador

El sistema DEBE (SHALL) mostrar las partidas sin resultado como pendientes y DEBE (SHALL) no mostrar un ganador para ellas.

#### Scenario: Una partida sin resultado no muestra ganador

- **GIVEN** que una partida está en estado "Pendiente de resultado"
- **WHEN** el visitante consulta la página de inicio
- **THEN** la partida aparece como pendiente
- **AND** no se muestra un ganador para esa partida

### Requirement: Menú lateral de navegación y acceso a los roles de demostración

El sistema DEBE (SHALL) mostrar en todas las páginas un botón de menú que abre un panel lateral desde la derecha con la navegación (Inicio y Bracket) y los accesos de demostración de Jugador, Moderador y Organizador. El panel DEBE (SHALL) poder cerrarse sin cambiar de página y DEBE (SHALL) indicar visualmente la página activa.

#### Scenario: El visitante abre el menú lateral y cambia de rol

- **GIVEN** que el visitante está en cualquier página de la aplicación
- **WHEN** pulsa el botón de menú
- **THEN** el panel lateral se abre desde la derecha
- **AND** muestra la navegación (Inicio y Bracket) y los accesos de Jugador, Moderador y Organizador
- **WHEN** elige un jugador de la lista
- **THEN** entra a la vista del jugador seleccionado

#### Scenario: El menú se cierra sin cambiar de página

- **GIVEN** que el panel lateral está abierto
- **WHEN** el visitante pulsa la X, presiona Esc o hace clic fuera del panel
- **THEN** el panel se cierra
- **AND** la página sigue siendo la misma
