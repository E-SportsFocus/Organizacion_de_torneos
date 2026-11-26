# torneo-publico Specification

## MODIFIED Requirements

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
