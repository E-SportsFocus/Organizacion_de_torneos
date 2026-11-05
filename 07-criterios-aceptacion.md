# Criterios de aceptación (Gherkin)

Los escenarios se redactan en lenguaje del negocio, usando los términos del [modelo de dominio](./08-modelo-dominio.md). HU-01 a HU-03 provienen de [Historias de usuario (Entrega 1)](./Historias_de_usuario.md). HU-04 a HU-06 son nuevas en esta entrega y cubren los requisitos RP-01, RP-02, RP-03 y RP-07 de la [clasificación de requisitos](./Clasificación_de_requisitos.md).

## HU-01 — Registro automático del resultado

Historia: Como moderador, quiero que la plataforma obtenga y registre el resultado mediante la API del videojuego, para reducir el trabajo manual y disponer de resultados oportunos.

```gherkin
Característica: Registro automático del resultado de una partida

  Escenario: Registro de un resultado válido recibido desde la API
    Dado que la partida está en estado "En curso"
    Y que la API del videojuego informa un resultado válido para la partida
    Cuando el sistema recibe el resultado
    Entonces el resultado queda registrado en la partida y en los equipos que la disputaron
    Y el resultado conserva la fecha, la hora y el origen "automático"

  Escenario: Un resultado ya registrado no se duplica
    Dado que la partida tiene un resultado registrado
    Cuando la API del videojuego vuelve a informar el mismo resultado
    Entonces el sistema no crea un segundo resultado para la partida
    Y el resultado registrado no cambia

  Escenario: Sin resultado válido la partida queda pendiente
    Dado que la partida está en estado "En curso" y ha terminado
    Cuando la API del videojuego no informa un resultado válido dentro del plazo de detección de 5 segundos
    Entonces la partida queda en estado "Pendiente de resultado"
    Y el Moderador asignado es avisado para registrar el resultado manualmente
```

## HU-02 — Notificación del resultado

Historia: Como jugador participante, quiero recibir una notificación del resultado registrado y consultar el bracket actualizado, para conocer la situación de mi equipo en el torneo.

```gherkin
Característica: Actualización del bracket y notificación del resultado

  Escenario: Un resultado válido actualiza el bracket y notifica a los involucrados
    Dado que se ha registrado un resultado válido para una partida
    Cuando el resultado queda registrado, de forma automática o manual
    Entonces el bracket del torneo se actualiza con el resultado
    Y el Organizador y los Jugadores de la partida reciben una notificación con la partida, los equipos y el resultado

  Escenario: La notificación coincide con el resultado registrado
    Dado que se registró un resultado de 2 a 1 para la partida entre "Equipo Alfa" y "Equipo Beta"
    Cuando se envía la notificación y se actualiza el bracket
    Entonces la notificación y el bracket muestran el mismo marcador de 2 a 1
    Y muestran "Equipo Alfa" como ganador

  Escenario: Una partida pendiente no se presenta como resultado final
    Dado que la partida está en estado "Pendiente de resultado"
    Cuando un Jugador consulta el bracket del torneo
    Entonces el bracket no muestra un ganador para la partida
    Y no se ha enviado una notificación de resultado final

  Escenario: Cada actualización del bracket queda registrada
    Dado que el bracket del torneo se actualizó con el resultado de una partida
    Cuando el Organizador consulta el historial de actualizaciones del bracket
    Entonces el historial muestra la fecha, la hora y el resultado que originó la actualización
```

## HU-03 — Registro manual del resultado

Historia: Como moderador, quiero registrar el resultado cuando no pueda obtenerse mediante la API, para permitir que el torneo continúe y conservar la trazabilidad.

```gherkin
Característica: Registro manual del resultado por un Moderador asignado

  Escenario: Un Moderador asignado registra el resultado completo de una partida pendiente
    Dado que la partida está en estado "Pendiente de resultado"
    Y que la API del videojuego no está disponible
    Y que el usuario es el Moderador asignado a la partida
    Cuando registra el resultado de ambos equipos
    Entonces el resultado queda registrado con la identidad del Moderador, la fecha, la hora y el origen "manual"
    Y el bracket se actualiza y se notifica a los participantes

  Escenario: Un jugador no puede registrar un resultado
    Dado que el usuario es un Jugador de una de las partidas
    Cuando intenta registrar el resultado de la partida
    Entonces el sistema rechaza la operación
    Y el estado y el resultado de la partida no cambian

  Escenario: Un Moderador no asignado a la partida no puede registrar el resultado
    Dado que la partida está en estado "Pendiente de resultado"
    Y que el usuario es un Moderador que no está asignado a la partida
    Cuando intenta registrar el resultado de la partida
    Entonces el sistema rechaza la operación
    Y el estado y el resultado de la partida no cambian

  Escenario: Un resultado incompleto no se confirma
    Dado que la partida está en estado "Pendiente de resultado"
    Y que el usuario es el Moderador asignado a la partida
    Cuando registra el resultado de un solo equipo
    Entonces el sistema no confirma el resultado
    Y solicita completar el resultado de ambos equipos
```

## HU-04 — Confirmación de disponibilidad

Historia: Como jugador de un equipo, quiero confirmar la disponibilidad de mi equipo para una partida, para que el Moderador sepa con anticipación que la partida puede jugarse.

```gherkin
Característica: Confirmación de disponibilidad de un equipo para una partida

  Escenario: Un equipo confirma su disponibilidad dentro del plazo
    Dado que el equipo tiene una partida programada en el torneo
    Y que faltan 8 horas o menos para el inicio de la partida
    Cuando un jugador del equipo confirma la disponibilidad del equipo
    Entonces la disponibilidad del equipo queda registrada como "Confirmada"
    Y el Moderador puede consultar el estado de la disponibilidad

  Escenario: Un equipo sin confirmar queda con disponibilidad pendiente
    Dado que el equipo tiene una partida programada en el torneo
    Y que el equipo no ha confirmado su disponibilidad
    Cuando faltan 8 horas o menos para el inicio de la partida
    Entonces la disponibilidad del equipo queda registrada como "Pendiente"
    Y el Moderador ve que la partida requiere revisión

  Escenario: Una partida con un equipo sin confirmar no inicia automáticamente
    Dado que la partida está programada
    Y que la disponibilidad de uno de los equipos está "Pendiente"
    Cuando llega la hora de inicio de la partida
    Entonces la partida permanece en estado "Programada"
    Y queda marcada para revisión del Moderador

  Escenario: No se confirma disponibilidad fuera del plazo
    Dado que la partida ya inició o ya finalizó
    Cuando un jugador intenta confirmar la disponibilidad de su equipo
    Entonces el sistema no acepta la confirmación
    Y la disponibilidad de la partida no cambia
```

## HU-05 — Solicitud de cambio de horario

Historia: Como jugador de un equipo, quiero solicitar un cambio de horario cuando mi equipo no esté disponible, para jugar la partida en un horario acordado con el Moderador.

```gherkin
Característica: Solicitud y resolución de un cambio de horario

  Escenario: Una solicitud dentro del plazo notifica automáticamente al Moderador
    Dado que la partida está programada
    Y que faltan más de 2 horas para el inicio de la partida
    Cuando un jugador de un equipo solicita un cambio de horario con un horario propuesto
    Entonces la solicitud queda registrada como "Solicitada"
    Y el Moderador es notificado automáticamente de la solicitud
    Y se publica un aviso de la solicitud en el canal de Discord del torneo

  Escenario: El Moderador aprueba una solicitud válida
    Dado que existe una solicitud de cambio de horario en estado "Solicitada"
    Cuando el Moderador aprueba la solicitud
    Entonces la partida queda reprogramada con el horario propuesto
    Y ambos equipos reciben la confirmación del nuevo horario
    Y el nuevo horario se publica en el canal de Discord del torneo

  Escenario: El Moderador rechaza una solicitud
    Dado que existe una solicitud de cambio de horario en estado "Solicitada"
    Cuando el Moderador rechaza la solicitud con un motivo
    Entonces la solicitud queda registrada como "Rechazada"
    Y la partida conserva su horario original
    Y el equipo recibe el motivo del rechazo

  Escenario: Una solicitud fuera del plazo no se acepta
    Dado que la partida está programada
    Y que faltan 2 horas o menos para el inicio de la partida
    Cuando un jugador solicita un cambio de horario
    Entonces el sistema no registra la solicitud
    Y informa que el plazo para solicitar cambios ya venció

  Escenario: Una solicitud sin decisión al llegar al plazo límite vence
    Dado que existe una solicitud de cambio de horario en estado "Solicitada"
    Cuando se alcanza el plazo límite de 2 horas antes de la partida sin decisión del Moderador
    Entonces la solicitud queda registrada como "Vencida"
    Y la partida conserva su horario original
    Y el equipo es informado de que la partida conserva su horario original
```

## HU-06 — Anuncio automático de ganadores

Historia: Como organizador, quiero que la plataforma anuncie automáticamente al ganador de cada partida, para anunciar resultados a tiempo sin depender de un aviso manual del Moderador.

```gherkin
Característica: Anuncio automático del ganador de una partida

  Escenario: El ganador se publica al confirmarse el resultado
    Dado que la partida está en estado "Pendiente de resultado" o "En curso"
    Cuando el resultado de la partida queda confirmado, de forma automática o manual
    Entonces el ganador se publica en la plataforma
    Y el ganador se anuncia en el canal de Discord del torneo
    Y la partida queda en estado "Anunciada"

  Escenario: No se anuncia un ganador con resultado pendiente
    Dado que la partida está en estado "Pendiente de resultado"
    Cuando el Organizador consulta la partida
    Entonces no se publica ningún ganador para la partida
    Y la plataforma indica que falta registrar el resultado

  Escenario: Un fallo en Discord no impide publicar el ganador en la plataforma
    Dado que el resultado de la partida queda confirmado
    Y que el canal de Discord del torneo no responde
    Cuando el sistema anuncia al ganador
    Entonces el ganador queda publicado en la plataforma
    Y el anuncio en Discord queda pendiente de envío
```
