# torneo-publico Specification

## MODIFIED Requirements

### Requirement: Inicio público de solo lectura con el estado del torneo

El sistema DEBE (SHALL) mostrar en la página de inicio el nombre y el juego del torneo, los anuncios de ganadores publicados, el bracket resumido y un enlace hacia el detalle completo en `/bracket`, sin ofrecer acciones para registrar resultados, anunciar ganadores ni modificar datos.

#### Scenario: El visitante consulta el torneo público

- **GIVEN** que el torneo tiene partidas y al menos un ganador anunciado
- **WHEN** el visitante abre la página de inicio
- **THEN** ve el nombre y el juego del torneo
- **AND** ve los anuncios de los ganadores publicados
- **AND** ve el bracket resumido y el enlace al detalle en el bracket
- **AND** no ve acciones para registrar resultados ni para anunciar ganadores
