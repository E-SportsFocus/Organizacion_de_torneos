# Propuesta de solución para la Evaluacion 2

## Lo que se debe de hacer 
Los estados del torneo hoy no tienen lógica asociada: no hay reglas especificadas sobre qué se puede hacer en cada estado. Por ejemplo, en un torneo en estado «borrador» los jugadores no deben poder confirmar disponibilidad ni ingresar resultados.

Debe especificarse e implementarse este control de estados, incluyendo el diagrama de estados, el modelo de dominio y las HU con sus criterios de aceptación.

Debe poder verse: El estado de los torneos.

## Solución

Se nos pidió modificar el comportamiento de los estados de un torneo, ya que el torneo al estar en borrador, los jugadores puedes seguir accediendo a el y modificar su estado, debiendo ser exclusivamente para el organizador. Debido a esto decidimos agregar una nueva historia de usuario haciendo que esto nos haga unos cambio en los siguientes apartados:

- modificar el diagrama de estado
- clasificación de requerimientos
- modelo de dominio
- diagrama de secuencia
- casos de uso
- la trazabilidad

En algunos apartados tendran cambios diminutos pero en otros seran un poco mas extensos debido al cambio que se nos pide.

## HU-10: Estado Torneo - Interacción Organizador/Usuario 
Como organizador de torneos me gustaría tener control total sobre la edición y estados del torneo, estos permisos deben ser exclusivamente del rol “Organizador/a”.

**Criterios de aceptación:**
- CA1: El sistema no deberá mostrar al usuario en ningún caso un torneo que aun no este en curso.
- CA2: El organizador/a debe poder alternar estados entre torneos y tener acceso a modificarlos

## HU-10 - Gherkin

## Casos de uso

## Modelo de dominio

## Clasificación de requisitos 

**Diagrama de estado**

<img width="700" height="900" alt="image" src="Images/diagramaestado.jpeg">

## Diagrama de secuencia 

## Trazabilidad
