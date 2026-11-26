# disponibilidad Specification

## MODIFIED Requirements

### Requirement: Confirmación de disponibilidad dentro del plazo

El sistema DEBE (SHALL) permitir que un jugador de un equipo confirme la disponibilidad de ese equipo para una partida programada, registrándola como "Confirmada" con su fecha de confirmación. La vista del jugador DEBE (SHALL) indicar el torneo al que pertenece cada partida.

#### Scenario: Un equipo confirma su disponibilidad dentro del plazo

- **GIVEN** que el equipo tiene una partida programada en el torneo
- **AND** que faltan 8 horas o menos para el inicio de la partida
- **WHEN** un jugador del equipo confirma la disponibilidad del equipo
- **THEN** la disponibilidad del equipo queda registrada como "Confirmada"
- **AND** el Moderador puede consultar el estado de la disponibilidad
- **AND** la partida indica el torneo al que pertenece
