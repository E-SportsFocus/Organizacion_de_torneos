# disponibilidad Specification

## Purpose

Permite que un jugador confirme en la plataforma la disponibilidad de su equipo para una partida programada del torneo, y que el Moderador consulte ese estado para saber si la partida puede jugarse.

## Requirements

### Requirement: Confirmación de disponibilidad dentro del plazo

El sistema DEBE (SHALL) permitir que un jugador de un equipo confirme la disponibilidad de ese equipo para una partida programada, registrándola como "Confirmada" con su fecha de confirmación.

#### Scenario: Un equipo confirma su disponibilidad dentro del plazo

- **GIVEN** que el equipo tiene una partida programada en el torneo
- **AND** que faltan 8 horas o menos para el inicio de la partida
- **WHEN** un jugador del equipo confirma la disponibilidad del equipo
- **THEN** la disponibilidad del equipo queda registrada como "Confirmada"
- **AND** el Moderador puede consultar el estado de la disponibilidad

### Requirement: Disponibilidad pendiente y partida para revisión

El sistema DEBE (SHALL) mantener la disponibilidad de cada equipo como "Pendiente" mientras no se confirme, y DEBE mostrar al Moderador que la partida requiere revisión.

#### Scenario: Un equipo sin confirmar queda con disponibilidad pendiente

- **GIVEN** que el equipo tiene una partida programada en el torneo
- **AND** que el equipo no ha confirmado su disponibilidad
- **WHEN** faltan 8 horas o menos para el inicio de la partida
- **THEN** la disponibilidad del equipo queda registrada como "Pendiente"
- **AND** el Moderador ve que la partida requiere revisión

### Requirement: La partida no inicia con un equipo sin confirmar

El sistema DEBE (SHALL) mantener la partida en estado "Programada" y marcarla para revisión del Moderador cuando llega la hora de inicio y algún equipo sigue con disponibilidad "Pendiente".

#### Scenario: Una partida con un equipo sin confirmar no inicia automáticamente

- **GIVEN** que la partida está programada
- **AND** que la disponibilidad de uno de los equipos está "Pendiente"
- **WHEN** llega la hora de inicio de la partida
- **THEN** la partida permanece en estado "Programada"
- **AND** queda marcada para revisión del Moderador

### Requirement: Confirmación fuera del plazo

El sistema DEBE (SHALL) rechazar la confirmación de disponibilidad cuando la partida ya inició o ya finalizó, sin modificar la disponibilidad registrada.

#### Scenario: No se confirma disponibilidad fuera del plazo

- **GIVEN** que la partida ya inició o ya finalizó
- **WHEN** un jugador intenta confirmar la disponibilidad de su equipo
- **THEN** el sistema no acepta la confirmación
- **AND** la disponibilidad de la partida no cambia
