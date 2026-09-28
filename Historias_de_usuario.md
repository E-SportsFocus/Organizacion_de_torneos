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

**Actividad TO-BE asociada:** Sistema detecta el resultado automáticamente vía API del juego / Árbitro registra el resultado manualmente en la plataforma si la API no esta disponible.

**Criterios de aceptación:**
- CA1: Ante la ausencia o fallo de la API, solo un moderador autorizado debe poder registrar un resultado completo para los equipos de la partida.
- CA2: El registro debe conservar el resultado, la identidad del moderador, la fecha, la hora y su origen manual.
- CA3: Al confirmar el resultado, el sistema debe continuar con la actualización del bracket y la notificación a los participantes correspondientes.

## Regresar 
[Ingeniería en Requisitos - Entrega 1](IngReq-Entrega1.md)
