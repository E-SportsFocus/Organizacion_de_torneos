# Trazabilidad

## Matriz de trazabilidad

| Requisito (Entrega 1) | Historia | Caso de uso | Secuencia | Estado | Clases del dominio |
|---|---|---|---|---|---|
| RP-01 | [HU-04](./07-criterios-aceptacion.md) | [CU-01](./09-casos-de-uso.md) | --- | [EST-01](./11-diagramas-estado.md) | Disponibilidad, Equipo, Partida |
| RP-02 | [HU-05](./07-criterios-aceptacion.md) | [CU-02](./09-casos-de-uso.md) | [DSS-03](./10-diagramas-secuencia.md) | [EST-02](./11-diagramas-estado.md) | SolicitudCambioHorario, Equipo, Partida |
| RP-03 | [HU-05](./07-criterios-aceptacion.md) | [CU-02](./09-casos-de-uso.md) | [DSS-03](./10-diagramas-secuencia.md) | [EST-02](./11-diagramas-estado.md) | SolicitudCambioHorario, Moderador |
| RP-04 | [HU-01](./07-criterios-aceptacion.md) | [CU-03](./09-casos-de-uso.md) | [DSS-01](./10-diagramas-secuencia.md) | [EST-01](./11-diagramas-estado.md) | Partida, Resultado |
| RP-05 | [HU-03](./07-criterios-aceptacion.md) | [CU-04](./09-casos-de-uso.md) | [DSS-02](./10-diagramas-secuencia.md) | [EST-01](./11-diagramas-estado.md) | Moderador, Resultado, Partida |
| RP-06 | [HU-02](./07-criterios-aceptacion.md) | [CU-05](./09-casos-de-uso.md) | [DSS-01](./10-diagramas-secuencia.md), [DSS-02](./10-diagramas-secuencia.md) | [EST-01](./11-diagramas-estado.md) | Bracket, Resultado, Organizador, Jugador |
| RP-07 | [HU-06](./07-criterios-aceptacion.md) | [CU-06](./09-casos-de-uso.md) | [DSS-01](./10-diagramas-secuencia.md), [DSS-02](./10-diagramas-secuencia.md) | [EST-01](./11-diagramas-estado.md) | Resultado, Organizador, Partida |
| RP-08 | [HU-01](./07-criterios-aceptacion.md) | [CU-03](./09-casos-de-uso.md) | [DSS-01](./10-diagramas-secuencia.md) | [EST-01](./11-diagramas-estado.md) | Resultado, Partida |
| RP-09 | [HU-04](./07-criterios-aceptacion.md) | [CU-01](./09-casos-de-uso.md) | --- | --- | Disponibilidad |
| RP-10 | [HU-02](./07-criterios-aceptacion.md), [HU-03](./07-criterios-aceptacion.md) | [CU-05](./09-casos-de-uso.md), [CU-04](./09-casos-de-uso.md) | [DSS-01](./10-diagramas-secuencia.md), [DSS-02](./10-diagramas-secuencia.md) | [EST-01](./11-diagramas-estado.md) | Bracket, Resultado, Moderador |

Las historias HU-01 a HU-06 aparecen todas en la matriz.

## Observaciones

- **RP-07 (anuncio de ganadores):** el anuncio está en [DSS-01](./10-diagramas-secuencia.md) y [DSS-02](./10-diagramas-secuencia.md) (publicar el ganador y anunciarlo en Discord) y corresponde a la transición "Resultado confirmado → Anunciada" de [EST-01](./11-diagramas-estado.md).
- **RP-09 (disponibilidad del 99 %):** es un requisito no funcional transversal. No se modela en un caso de uso ni en un diagrama. Se verifica con la métrica M-FI01 de los atributos de calidad de la Entrega 1. Se asocia a HU-04 y CU-01 porque la confirmación de disponibilidad depende de que el sistema esté disponible.
- **RP-01 y RP-09 sin secuencia:** la confirmación de disponibilidad es un caso simple de consulta y escritura. Su efecto en el ciclo de vida aparece como condición de inicio en EST-01 ("Ambos equipos confirmaron disponibilidad").
- **RP-08 (detección en 5 segundos):** se representa en el bucle de consulta de [DSS-01](./10-diagramas-secuencia.md) y como plazo de detección en HU-01. La medición con el umbral de 5 segundos corresponde a la prueba de rendimiento, no al diagrama.
- **RP-10 (registro auditable de cada actualización del bracket):** se cubre con el historial de actualizaciones del Bracket (HU-02, escenario "Cada actualización del bracket queda registrada") y con los datos de origen, fecha, hora y Moderador que conserva cada Resultado (HU-01 y HU-03).
- **HU-04 a HU-06 no están en `Historias_de_usuario.md` (Entrega 1):** se definen en [07-criterios-aceptacion.md](./07-criterios-aceptacion.md). Si el equipo decide agregarlas a la Entrega 1 para mantener coherencia, deben copiarse sin cambiar los IDs.
- **Reclamos (hallazgo H-05 de la elicitación):** no tiene historia ni requisito en la Entrega 1, así que no aparece en la matriz. Queda como candidato para una próxima iteración.
- **Terminología:** el "Árbitro" de RP-05 se trata como el **Moderador** de esta entrega, y el Moderador que puede registrar un resultado es el **Moderador asignado** a la partida.
- **RY-03 (validar API pública):** sigue pendiente. El flujo de [DSS-02](./10-diagramas-secuencia.md) es la respuesta del sistema si la API no existe o no está disponible.
