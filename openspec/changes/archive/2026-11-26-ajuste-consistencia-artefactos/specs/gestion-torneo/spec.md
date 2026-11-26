# gestion-torneo Specification

## MODIFIED Requirements

### Requirement: Registro y configuración de datos generales del torneo

El sistema DEBE (SHALL) permitir que el Organizador registre y actualice la información principal del torneo (nombre oficial, videojuego oficial, fecha y hora de inicio, zona horaria, bolsa total de premios en CLP, descripción y reglamento, y estado del torneo), asociando el torneo a la identidad del Organizador. El estado DEBE (SHALL) pertenecer al catálogo `Borrador`, `Inscripciones abiertas`, `En curso` y `Finalizado`; cualquier otro valor DEBE (SHALL) rechazarse.

#### Scenario: Registro exitoso de un nuevo torneo con sus datos generales

- **GIVEN** que el Organizador se encuentra en el panel de gestión de torneos
- **WHEN** ingresa el nombre del torneo, selecciona el videojuego, define la fecha y hora de inicio y la zona horaria
- **AND** presiona "Guardar torneo"
- **THEN** el sistema registra el nuevo torneo vinculado al Organizador
- **AND** el torneo queda disponible para su administración

#### Scenario: Validación del estado del torneo

- **GIVEN** que el Organizador está configurando el estado del torneo
- **WHEN** envía un estado distinto de "Borrador", "Inscripciones abiertas", "En curso" o "Finalizado"
- **THEN** el sistema no registra el torneo
- **AND** muestra un mensaje indicando que el estado no es válido

## ADDED Requirements

### Requirement: Actualización de un torneo existente conservando integridad

El sistema DEBE (SHALL) permitir que el Organizador actualice un torneo existente sin cambiar su identificador y sin duplicar sus premios ni sus inscripciones.

#### Scenario: Actualización de un torneo existente conservando integridad

- **GIVEN** que existe un torneo creado por el Organizador con premios y equipos inscritos
- **WHEN** el Organizador modifica sus datos generales o su estructura de premios
- **AND** guarda los cambios
- **THEN** el torneo conserva su identificador
- **AND** los premios y las inscripciones se actualizan sin duplicar registros
- **AND** la información actualizada se muestra en el panel y en la vista pública
