# Historias de usuario
 
## HU-01: Registro automático del resultado
Como moderador, quiero que la plataforma obtenga y registre el resultado mediante la API del videojuego, para reducir el trabajo manual y disponer de resultados oportunos.

**Actividad TO-BE asociada:**  Determinar los resultados vía API.

**Criterios de aceptación:**
- CA1: Cuando la API proporcione un resultado válido, el sistema debe registrarlo en la partida y equipos correspondientes, sin duplicarlo si   vuelve a recibirlo.
- CA2: El registro debe conservar la fecha, hora y origen automático del resultado.
- CA3: Si no se obtiene un resultado válido, la partida debe quedar pendiente y permitir su registro manual por el moderador
 
## HU-02: Notificación del resultado
Como jugador participante, quiero recibir una notificación del resultado registrado y consultar el bracket actualizado, para conocer la situación de mi equipo en el torneo.

**Actividad TO-BE asociada:** Notifica los resultados al organizador y jugadores con el bracket actualizado.

**Criterios de aceptación:**
- CA1: Al registrarse un resultado válido, de forma automática o manual, el sistema debe actualizar el bracket.
- CA2: El sistema debe notificar directamente al organizador y a los jugadores involucrados, identificando la partida, los equipos y el resultado, con acceso al bracket.
- CA3: La información de la notificación y del bracket debe coincidir con el resultado registrado.
  
## HU-03: Registro manual del resultado

Como moderador, quiero registrar el resultado cuando no pueda obtenerse mediante la API, para permitir que el torneo continúe y conservar la trazabilidad.

**Actividad TO-BE asociada:** Registra manualmente los resultados en la plataforma.

**Criterios de aceptación:**
- CA1: Ante la ausencia o fallo de la API, solo un moderador autorizado debe poder registrar un resultado completo para los equipos de la partida.
- CA2: El registro debe conservar el resultado, la identidad del moderador, la fecha, la hora y su origen manual.
- CA3: Al confirmar el resultado, el sistema debe continuar con la actualización del bracket y la notificación a los participantes correspondientes.

## HU-04: Confirmación de disponibilidad

Como jugador de un equipo, quiero confirmar la disponibilidad de mi equipo para una partida, para que el Moderador sepa con anticipación que la partida puede jugarse.

**Actividad TO-BE asociada:** Confirman disponibilidad en la plataforma (Jugadores).

**Criterios de aceptación:**
- CA1: Un jugador de un equipo puede confirmar la disponibilidad de su equipo para una partida programada si faltan 8 horas o menos.
- CA2: El Moderador puede consultar en todo momento el estado de disponibilidad de los equipos; si algún equipo sigue pendiente, la partida queda marcada como «Requiere revisión».
- CA3: Una partida con un equipo sin confirmar no inicia automáticamente al llegar la hora de inicio y permanece en «Programada» para revisión.
- CA4: No se acepta la confirmación de disponibilidad si la partida ya inició o finalizó.

## HU-05: Solicitud de cambio de horario

Como jugador de un equipo, quiero solicitar un cambio de horario cuando mi equipo no esté disponible, para jugar la partida en un horario acordado con el Moderador.

**Actividad TO-BE asociada:** Solicitud y resolución de cambio de horario (Jugador y Moderador).

**Criterios de aceptación:**
- CA1: Un jugador de un equipo puede solicitar un cambio de horario proponiendo fecha y hora cuando faltan más de 2 horas para el inicio de la partida.
- CA2: Al registrarse dentro del plazo, la solicitud queda en estado «Solicitada», se notifica al Moderador asignado y se publica aviso en Discord.
- CA3: El Moderador puede aprobar una solicitud válida, lo que reprograma la fecha/hora de la partida, confirma a ambos equipos y publica en Discord.
- CA4: El Moderador puede rechazar la solicitud indicando un motivo obligatorio; la partida conserva su horario original y el equipo recibe el motivo.
- CA5: Una solicitud solicitada con 2 horas o menos de anticipación no se acepta; si una solicitud no tiene decisión al llegar a 2 horas antes de la partida, pasa automáticamente a «Vencida».

## HU-06: Anuncio automático de ganadores

Como organizador, quiero que la plataforma anuncie automáticamente al ganador de cada partida, para anunciar resultados a tiempo sin depender de un aviso manual del Moderador.

**Actividad TO-BE asociada:** Publica y anuncia los resultados oficiales y bracket actualizado.

**Criterios de aceptación:**
- CA1: Al confirmarse un resultado, el ganador se publica automáticamente en la plataforma, se anuncia en Discord y la partida pasa a «Anunciada».
- CA2: No se anuncia ningún ganador mientras la partida tenga resultado pendiente.
- CA3: Si Discord no responde, el ganador se publica igual en la plataforma y el anuncio queda marcado como «Pendiente de envío».

## HU-07: Inicio público del torneo y menú desplegable

Como visitante del torneo, quiero ver al abrir el inicio los anuncios de ganadores y el bracket resumido (con enlace al detalle completo de partidas), y navegar entre las vistas desde un menú desplegable, para seguir el torneo desde un solo lugar sin depender de las pantallas internas de Organizador o Moderador.

**Actividad TO-BE asociada:** Consulta pública del torneo y navegación centralizada.

**Criterios de aceptación:**
- CA1: El inicio público muestra el torneo, juego, anuncios de ganadores y bracket resumido con enlace al detalle en `/bracket`, en modo solo lectura y sin formularios internos.
- CA2: Una partida sin resultado no inventa ganadores y muestra «Sin resultado».
- CA3: El menú desplegable lateral permite acceder a Inicio, Bracket y alternar entre los roles de Jugador, Moderador y Organizador con simulación demostrativa.
- CA4: El menú puede cerrarse sin cambiar de página con botón cerrar, tecla Esc o clic exterior.

## HU-08: Visualización gráfica del Bracket del torneo

Como visitante o participante del torneo, quiero consultar el bracket en un formato visual de árbol de llaves con rondas secuenciales y líneas conectoras, para comprender de un vistazo la progresión de los equipos, los resultados de cada enfrentamiento y qué equipos avanzan a las siguientes fases.

**Actividad TO-BE asociada:** Seguimiento visual del progreso del torneo y llaves competitivas.

**Criterios de aceptación:**
- CA1: El bracket gráfico muestra las rondas organizadas secuencialmente en columnas y cada enfrentamiento muestra equipos, fecha y estado.
- CA2: Los enfrentamientos con resultado destacan visualmente al equipo ganador y muestran marcadores en casillas individuales con conexión hacia la siguiente ronda.
- CA3: Las partidas pendientes no muestran ganador anticipado y reflejan su estado de espera.
- CA4: Se permite consultar tanto el árbol visual de llaves como la tabla detallada de auditoría e historial de actualizaciones.

## HU-09: Creación y gestión de torneos, participantes y premios

Como organizador, quiero contar con un apartado exclusivo para crear y configurar torneos, gestionando su información principal, los equipos/jugadores participantes y la estructura de premios, para planificar y poner en marcha competiciones de manera autónoma y transparente desde la plataforma.

**Actividad TO-BE asociada:** Planificación, registro de torneo y configuración competitiva.

**Criterios de aceptación:**
- CA1: El organizador puede crear un torneo indicando su nombre, videojuego, fecha/hora de inicio, zona horaria y descripción opcional.
- CA2: El organizador puede gestionar la lista de equipos y jugadores participantes inscritos en el torneo.
- CA3: El organizador puede configurar la bolsa de premios (*prize pool*) desglosada por posiciones (1.º, 2.º, 3.º lugar u otros reconocimientos).
- CA4: El sistema valida que los campos esenciales no estén vacíos y que las fechas y montos sean consistentes antes de confirmar la creación o actualización.
- CA5: La información de fechas, participantes y premios queda disponible de forma clara en el panel del organizador y en la vista pública de consulta.

## HU-10: Control del estado del torneo por el Organizador
Como organizador de torneos me gustaría tener control total sobre la edición y estados del torneo, estos permisos deben ser exclusivamente del rol “Organizador/a”.

**Actividad TO-BE asociada:**Gestión de estados y control de permisos del torneo

**Criterios de aceptación:**
- CA1: El sistema no deberá mostrar al usuario en ningún caso un torneo que aun no este en curso.
- CA2: El organizador/a debe poder alternar estados entre torneos y tener acceso a modificarlos

## Regresar 
[Ingeniería en Requisitos - Entrega 1](IngReq-Entrega1.md)
