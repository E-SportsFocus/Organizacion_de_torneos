# Clasificación de requisitos
 
## Requisitos de producto
| ID | Requisito | Tipo | Actividad TO-BE asociada |
|----|-----------|--------------------------------|----------------------------|
| RP-01 | El sistema debe permitir a los jugadores/confirmar su disponibilidad para una partida a través de la plataforma. | Funcional | Confirman disponibilidad en la plataforma |
| RP-02 | El sistema debe permitir a los jugadores/equipos solicitar solicitar un cambio de horario cuando no tengan disponibilidad. | Funcional | Solicitan cambio de horario en la plataforma |
| RP-03 | El sistema debe notificar automáticamente al Moderador cuando un jugador/equipo solicite un cambio de horario. | Funcional | Solicitar cambio de horario en la plataforma (Jugadores) |
| RP-04 | El sistema debe integrarse con la API del videojuego para detectar automáticamente el resultado de una partida al finalizar. | Funcional | Sistema detecta el resultado automaticamente vía API |
| RP-05 | El sistema debe permitir al Árbitro/Moderador registrar manualmente el resultado de una partida cuando la API del juego no esté disponible. | Funcional | Árbitro registra el resultado manualmente en la plataforma |
| RP-06 | El sistema debe notificar automáticamente al Organizador y a los Jugadores/Equipos apenas se registre el resultado de una partida, actualizando el bracket del torneo. | Funcional | Sistema notifica automaticamente el resultado al Organizador | 
| RP-07 | El sistema debe anunciar automáticamente a los ganadores de cada partida en la plataforma y en el canal de Discord del torneo. | Funcional | Sistema anuncia automaticamente a los ganadores |
| RP-08 | El sistema debe detectar y notificar el resultado de una partida en un plazo máximo de cinco segundos desde el fin de la partida, cuando la API esté disponible. | No funcional (rendimiento) | Sistema detecta el resultado automaticamente vía API |
| RP-09 | El sistema debe estar disponible al menos el 99% del tiempo durante los horarios de partidas programadas, dado que la confirmación de disponibilidad depende de él. | No funcional (disponibilidad) | Confirman disponibilidad en la plataforma | 
| RP-10 | El sistema debe mantener un registro auditable de cada actualizacion del bracket, para poder verificar discrepancias reportadas por jugadores/equipos. | No funcional (trazabilidad) | Sistema notifica automaticamente el resultado al Organizador |
 
## Requisitos de proyecto
| ID | Requisito |
|----|-----------|
| RY-01 | El equipo debe documentar el proceso de negocio (AS-IS y TO-BE), la clasificación de requisitos, las historias de usuario, la e licitación y los atributos de calidad en una organización de Github compartida, siguiendo la estructura de archivos definida por la cátedra. |
| RY-02 | El desarrollo del prototipo de la plataforma debe llevarse con control de versiones (Git) y un tablero de seguimiento (GitHub Projects) visible para todos los integrantes del equipo. | 
| RY-03 | El equipo debe validar, antes de comprometer la funcionalidad de deteccion automatica de resultados, si existe una API publica o documentada para al menos uno de los videojuegos soportados en el torneo. |
 
## Requisito derivado
**Requisito origen:** RP-04 -- El sistema debe integrarse con la API del videojuego para detectar automáticamente el resultado de una partida al finalizar.

**Requisito derivado:** RP-05 -- El sistema debe permitir al Árbitro/Moderador registrar manualmente el resultado de una partida cuando la API del juego no esté disponible.

**Justificación:** No todos los videojuegos exponen una API publica, y ninguna API garantiza 100% de disponibilidad. Si el proceso dependiera únicamente de RP-04, cualquier caída o ausencia de API dejaría partidas sin resultado registrado, bloqueando el anuncio de ganadores y la entrega de premios (el problema original del Organizador). Por eso se deriva un mecanismo manual de respaldo que cubre exactamente el caso de excepción, tal como se definió en la Iniciativa 3 de rediseño. 

## Regresar
[Ingeniería en Requisitos - Entrega 1](IngReq-Entrega1.md)
