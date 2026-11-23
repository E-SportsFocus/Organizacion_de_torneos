# gestion-torneo Specification

## Purpose

Permite que el Organizador gestione de forma integral la creación y configuración de torneos desde un apartado exclusivo, administrando la información general del campeonato, la selección e inscripción de equipos/jugadores participantes y la definición de la estructura oficial de premios.

## Requirements

### Requirement: Registro y configuración de datos generales del torneo

El sistema DEBE (SHALL) permitir que el Organizador registre y actualice la información principal del torneo (nombre oficial, videojuego oficial, fecha y hora de inicio, zona horaria, bolsa total de premios en CLP, descripción y reglamento, y estado del torneo), asociando el torneo a la identidad del Organizador.

#### Scenario: Registro exitoso de un nuevo torneo con sus datos generales

- **GIVEN** que el Organizador se encuentra en el panel de gestión de torneos
- **WHEN** ingresa el nombre del torneo, selecciona el videojuego, define la fecha y hora de inicio y la zona horaria
- **AND** presiona "Guardar torneo"
- **THEN** el sistema registra el nuevo torneo vinculado al Organizador
- **AND** el torneo queda disponible para su administración

### Requirement: Validación de campos obligatorios al registrar el torneo

El sistema DEBE (SHALL) validar que los campos obligatorios del torneo (nombre y videojuego) se encuentren presentes y no vacíos. Si falta algún dato mandatorio, el sistema DEBE (SHALL) rechazar el registro e informar al usuario los campos requeridos.

#### Scenario: Validación de campos obligatorios al registrar el torneo

- **GIVEN** que el Organizador intenta registrar un torneo sin completar el nombre o el videojuego
- **WHEN** envía el formulario
- **THEN** el sistema no registra el torneo
- **AND** muestra un mensaje de error indicando los datos obligatorios requeridos

### Requirement: Asignación e inscripción de equipos y jugadores participantes

El sistema DEBE (SHALL) permitir que el Organizador asigne e inscriba formalmente los equipos que participarán en el campeonato, registrando la nómina oficial de participantes y vinculándolos al torneo.

#### Scenario: Asignación e inscripción de equipos participantes

- **GIVEN** que existe un torneo creado por el Organizador
- **WHEN** el Organizador selecciona los equipos y jugadores que disputarán la competición
- **AND** confirma la inscripción
- **THEN** los equipos quedan registrados como participantes oficiales del torneo
- **AND** se visualizan organizados en el listado de participantes

### Requirement: Definición y desglose de la estructura oficial de premios

El sistema DEBE (SHALL) permitir que el Organizador defina la distribución de premios por posición (por ejemplo: 1.º, 2.º y 3.º lugar), registrando el monto o recompensa y su descripción, para su desglose en el panel de gestión y su difusión en la vista pública del torneo.

#### Scenario: Definición y desglose de la estructura de premios

- **GIVEN** que el Organizador está configurando la premiación del torneo
- **WHEN** ingresa la distribución de premios indicando posición y monto o descripción
- **AND** guarda la configuración de premios
- **THEN** los premios quedan asociados formalmente al torneo
- **AND** se muestran claramente desglosados en el panel y en la vista informativa pública
