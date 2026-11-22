# cambio-horario Specification

## Purpose
Permite que un jugador solicite un cambio de horario para una partida programada con más de 2 horas de anticipación, y que el Moderador asignado apruebe o rechace la solicitud.

## Requirements

### Requirement: Solicitud de cambio dentro del plazo
El sistema DEBE (SHALL) permitir que un jugador de un equipo solicite un cambio de horario para una partida programada cuando faltan más de 2 horas para su inicio, registrando la solicitud como "Solicitada", notificando al Moderador y publicando el aviso en Discord.

#### Scenario: Una solicitud dentro del plazo notifica automáticamente al Moderador
- **GIVEN** que la partida está programada
- **AND** que faltan más de 2 horas para el inicio de la partida
- **WHEN** un jugador de un equipo solicita un cambio de horario con un horario propuesto
- **THEN** la solicitud queda registrada como "Solicitada"
- **AND** el Moderador es notificado automáticamente de la solicitud
- **AND** se publica un aviso de la solicitud en el canal de Discord del torneo

### Requirement: Aprobación de la solicitud por el Moderador
El sistema DEBE (SHALL) permitir que el Moderador apruebe una solicitud en estado "Solicitada", reprogramando la fecha y hora de la partida con el horario propuesto, confirmándolo a ambos equipos y publicándolo en Discord.

#### Scenario: El Moderador aprueba una solicitud válida
- **GIVEN** que existe una solicitud de cambio de horario en estado "Solicitada"
- **WHEN** el Moderador aprueba la solicitud
- **THEN** la partida queda reprogramada con el horario propuesto
- **AND** ambos equipos reciben la confirmación del nuevo horario
- **AND** el nuevo horario se publica en el canal de Discord del torneo

### Requirement: Rechazo de la solicitud por el Moderador
El sistema DEBE (SHALL) permitir que el Moderador rechace una solicitud en estado "Solicitada" indicando un motivo obligatorio, registrando la solicitud como "Rechazada", conservando la partida su horario original y notificando el motivo al equipo.

#### Scenario: El Moderador rechaza una solicitud
- **GIVEN** que existe una solicitud de cambio de horario en estado "Solicitada"
- **WHEN** el Moderador rechaza la solicitud con un motivo
- **THEN** la solicitud queda registrada como "Rechazada"
- **AND** la partida conserva su horario original
- **AND** el equipo recibe el motivo del rechazo

### Requirement: Rechazo de solicitud fuera del plazo
El sistema DEBE (SHALL) rechazar cualquier intento de solicitud de cambio de horario cuando faltan 2 horas o menos para el inicio de la partida, informando que el plazo venció y sin registrar la solicitud.

#### Scenario: Una solicitud fuera del plazo no se acepta
- **GIVEN** que la partida está programada
- **AND** que faltan 2 horas o menos para el inicio de la partida
- **WHEN** un jugador solicita un cambio de horario
- **THEN** el sistema no registra la solicitud
- **AND** informa que el plazo para solicitar cambios ya venció

### Requirement: Vencimiento automático de solicitud sin decisión
El sistema DEBE (SHALL) cambiar al estado "Vencida" cualquier solicitud en estado "Solicitada" cuando se alcanza el plazo límite de 2 horas antes de la partida sin decisión del Moderador, conservando la partida su horario original.

#### Scenario: Una solicitud sin decisión al llegar al plazo límite vence
- **GIVEN** que existe una solicitud de cambio de horario en estado "Solicitada"
- **WHEN** se alcanza el plazo límite de 2 horas antes de la partida sin decisión del Moderador
- **THEN** la solicitud queda registrada como "Vencida"
- **AND** la partida conserva su horario original
- **AND** el equipo es informado de que la partida conserva su horario original
