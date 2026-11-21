# anuncio Specification

## Purpose
Permite publicar automáticamente al ganador de una partida en la plataforma y anunciarlo en el canal de Discord del torneo, y que el Organizador consulte los anuncios y el estado de cada partida.

## Requirements

### Requirement: Publicación y anuncio automático del ganador

El sistema DEBE (SHALL) publicar al ganador en la plataforma, anunciarlo en el canal de Discord del torneo y dejar la partida en estado "Anunciada" cuando el resultado queda confirmado, sin requerir una acción manual del Organizador.

#### Scenario: El ganador se publica al confirmarse el resultado

- **GIVEN** que la partida está en estado "Pendiente de resultado" o "En curso"
- **WHEN** el resultado de la partida queda confirmado, de forma automática o manual
- **THEN** el ganador se publica en la plataforma
- **AND** el ganador se anuncia en el canal de Discord del torneo
- **AND** la partida queda en estado "Anunciada"

### Requirement: No se anuncia un ganador con resultado pendiente

El sistema DEBE (SHALL) no publicar ni anunciar un ganador para una partida sin resultado confirmado, y DEBE indicar al Organizador que falta registrar el resultado.

#### Scenario: No se anuncia un ganador con resultado pendiente

- **GIVEN** que la partida está en estado "Pendiente de resultado"
- **WHEN** el Organizador consulta la partida
- **THEN** no se publica ningún ganador para la partida
- **AND** la plataforma indica que falta registrar el resultado

### Requirement: Un fallo de Discord no impide publicar el ganador

El sistema DEBE (SHALL) mantener la publicación del ganador en la plataforma y dejar el anuncio en Discord como "Pendiente de envío" cuando el canal de Discord del torneo no responde.

#### Scenario: Un fallo en Discord no impide publicar el ganador en la plataforma

- **GIVEN** que el resultado de la partida queda confirmado
- **AND** que el canal de Discord del torneo no responde
- **WHEN** el sistema anuncia al ganador
- **THEN** el ganador queda publicado en la plataforma
- **AND** el anuncio en Discord queda pendiente de envío
