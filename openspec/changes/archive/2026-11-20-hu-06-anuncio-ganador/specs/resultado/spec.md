# Spec Delta

## MODIFIED Requirements

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
