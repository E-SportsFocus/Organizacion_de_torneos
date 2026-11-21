# resultado Specification

## Purpose

Permite que el Moderador asignado registre manualmente el resultado de una partida cuando la API del videojuego no está disponible, conservando la trazabilidad del registro y actualizando el bracket del torneo.

## Requirements

### Requirement: Registro manual del resultado por el Moderador asignado

El sistema DEBE (SHALL) permitir que el Moderador asignado a una partida en estado "Pendiente de resultado" registre el marcador de ambos equipos. El resultado DEBE (SHALL) guardarse con la identidad del Moderador, la fecha, la hora y el origen "manual"; el sistema DEBE (SHALL) actualizar el bracket, notificar al Organizador y a los Jugadores de ambos equipos, publicar al ganador en la plataforma y dejar la partida en estado "Anunciada" tras anunciarlo en Discord.

#### Scenario: Un Moderador asignado registra el resultado completo de una partida pendiente

- **GIVEN** que la partida está en estado "Pendiente de resultado"
- **AND** que la API del videojuego no está disponible
- **AND** que el usuario es el Moderador asignado a la partida
- **WHEN** registra el resultado de ambos equipos
- **THEN** el resultado queda registrado con la identidad del Moderador, la fecha, la hora y el origen "manual"
- **AND** el bracket se actualiza y se notifica a los participantes
- **AND** el ganador se publica en la plataforma y la partida queda en estado "Anunciada"

### Requirement: Solo el Moderador asignado puede registrar el resultado

El sistema DEBE (SHALL) rechazar el registro del resultado cuando el usuario no es el Moderador asignado a la partida, sin modificar el estado de la partida ni el resultado registrado.

#### Scenario: Un jugador no puede registrar un resultado

- **GIVEN** que el usuario es un Jugador de una de las partidas
- **WHEN** intenta registrar el resultado de la partida
- **THEN** el sistema rechaza la operación
- **AND** el estado y el resultado de la partida no cambian

#### Scenario: Un Moderador no asignado a la partida no puede registrar el resultado

- **GIVEN** que la partida está en estado "Pendiente de resultado"
- **AND** que el usuario es un Moderador que no está asignado a la partida
- **WHEN** intenta registrar el resultado de la partida
- **THEN** el sistema rechaza la operación
- **AND** el estado y el resultado de la partida no cambian

### Requirement: El resultado debe estar completo y tener un ganador

El sistema DEBE (SHALL) exigir el marcador de ambos equipos y DEBE (SHALL) rechazar el registro cuando falte uno de los marcadores o cuando ambos sean iguales (empate), sin confirmar el resultado.

#### Scenario: Un resultado incompleto no se confirma

- **GIVEN** que la partida está en estado "Pendiente de resultado"
- **AND** que el usuario es el Moderador asignado a la partida
- **WHEN** registra el resultado de un solo equipo
- **THEN** el sistema no confirma el resultado
- **AND** solicita completar el resultado de ambos equipos

#### Scenario: Un empate no se acepta como resultado

- **GIVEN** que la partida está en estado "Pendiente de resultado"
- **AND** que el usuario es el Moderador asignado a la partida
- **WHEN** registra el mismo marcador para ambos equipos
- **THEN** el sistema no confirma el resultado
- **AND** solicita un marcador con un ganador
