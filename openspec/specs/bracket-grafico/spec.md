# bracket-grafico Specification

## Purpose
Permite que visitantes y participantes consulten el bracket del torneo en formato de árbol visual de llaves organizado por rondas consecutivas con marcadores individuales, destaque del equipo clasificado o ganador y conectores entre fases, manteniendo la auditoría histórica.

## Requirements

### Requirement: Organización secuencial de rondas en el bracket gráfico
El sistema DEBE (SHALL) organizar y presentar las partidas del torneo en un árbol visual de llaves estructurado en columnas secuenciales correspondientes a cada ronda (por ejemplo: Cuartos de final, Semifinal, Final), donde cada enfrentamiento muestre los equipos participantes, la fecha programada y su estado actual.

#### Scenario: El bracket gráfico muestra las rondas organizadas secuencialmente
- **GIVEN** que el torneo tiene partidas programadas o jugadas en distintas fases
- **WHEN** un visitante consulta la página del bracket
- **THEN** ve el árbol visual de llaves organizado por columnas de rondas
- **AND** cada enfrentamiento muestra los equipos participantes, la fecha y el estado

### Requirement: Destaque visual del ganador y visualización de marcadores
El sistema DEBE (SHALL) mostrar en cada enfrentamiento que posea un resultado confirmado las casillas individuales de puntuación para cada equipo, destacar visualmente al equipo ganador y reflejar el avance hacia la siguiente fase competitiva.

#### Scenario: Los enfrentamientos con resultado destacan al equipo ganador
- **GIVEN** que una partida del bracket tiene un resultado registrado
- **WHEN** se visualiza la llave de esa partida
- **THEN** se muestran los marcadores de cada equipo en casillas individuales
- **AND** el equipo ganador aparece visualmente destacado
- **AND** se visualiza la conexión de avance hacia la siguiente ronda

### Requirement: Estado claro para partidas pendientes
El sistema DEBE (SHALL) representar las partidas que aún no cuentan con resultado confirmado en un estado visible de espera sin asignar ni inventar equipos ganadores prematuramente.

#### Scenario: Las partidas pendientes no muestran ganador anticipado
- **GIVEN** que una partida del bracket aún no tiene resultado confirmado
- **WHEN** se visualiza en el árbol de llaves
- **THEN** la partida muestra su estado de espera
- **AND** no se asigna ni inventa un ganador prematuramente

### Requirement: Coexistencia con la vista de auditoría
El sistema DEBE (SHALL) mantener accesible junto con el árbol gráfico de llaves el historial de auditoría y actualizaciones del bracket registrado por los moderadores para asegurar la trazabilidad requerida por la norma RP-10.

#### Scenario: Se permite alternar entre vista de árbol gráfico y tabla de auditoría
- **GIVEN** que el usuario está consultando el bracket del torneo
- **WHEN** navega por la sección
- **THEN** dispone del árbol visual interactivo de llaves
- **AND** puede consultar el historial detallado de actualizaciones y auditoría
