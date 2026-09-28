# Atributos de calidad de E-Sports Focus

## Alcance y criterio de priorización

Esta propuesta define la calidad esperada del software de apoyo a la organización y desarrollo de partidas de E-Sports Focus. Se basa en el proceso documentado: publicación del cronograma en Discord, revisión de disponibilidad, reprogramación, entrega de reglas, coordinación de la sala, revisión de resultados y anuncio de ganadores.

Se utiliza **ISO/IEC 25010:2023**, cuyo modelo de calidad del producto contiene nueve características de primer nivel. Las denominaciones en español se acompañan de su equivalente en inglés para evitar confusiones. En esta edición se emplean capacidad de interacción y flexibilidad, y se incorpora seguridad operacional.

El orden prioriza que la información competitiva sea correcta, que el servicio continúe durante las partidas y que solo personas autorizadas puedan modificar datos. Las métricas y umbrales siguientes son **metas propuestas para el proyecto**, no exigencias numéricas de ISO ni resultados de pruebas ejecutadas. Deben validarse con el organizador y el moderador. 
## Priorización de los nueve atributos de primer nivel

| Prioridad | Atributo | Justificación para el proyecto |
|---|---|---|
| 1 | Adecuación funcional — Functional suitability | La programación, los cambios autorizados y los resultados deben cumplir las reglas acordadas. Un resultado incorrecto puede producir un ganador equivocado aunque el servicio sea rápido. |
| 2 | Fiabilidad — Reliability | La consulta de horarios y el registro de resultados deben estar disponibles durante la jornada y conservar la información confirmada ante interrupciones. |
| 3 | Seguridad de la información — Security | Debe protegerse la información de los participantes y evitar modificaciones no autorizadas de horarios, reglas o resultados, conservando la trazabilidad de cambios. |
| 4 | Capacidad de interacción — Interaction capability | Jugadores y moderadores deben entender el horario vigente, las reglas y el estado de una partida sin depender de explicaciones continuas. |
| 5 | Eficiencia de desempeño — Performance efficiency | Las consultas y actualizaciones deben responder oportunamente cuando varios equipos se preparan para jugar. La carga prevista aún debe determinarse. |
| 6 | Compatibilidad — Compatibility | El apoyo digital debe convivir con Discord y los videojuegos utilizados. Una integración automática sería una decisión de alcance por validar. |
| 7 | Flexibilidad — Flexibility | El producto debería adaptarse a variaciones de cantidad de equipos, juegos y organización del torneo conforme se confirmen esos escenarios. |
| 8 | Mantenibilidad — Maintainability | El equipo debe poder corregir errores y modificar reglas del sistema sin afectar funciones ya verificadas. |
| 9 | Seguridad operacional — Safety | Se deben considerar daños potenciales a personas, bienes o entorno derivados del uso. Su prioridad relativa es menor porque el alcance documentado no controla equipos físicos ni procesos críticos; debe reevaluarse si cambia ese alcance. |

Seguridad de la información y seguridad operacional son características distintas. Disponibilidad se trata como parte de fiabilidad, y escalabilidad como parte de flexibilidad; no se cuentan como atributos adicionales de primer nivel.

## Métricas de los tres atributos más importantes

### 1 Adecuación funcional

**Objetivo:** ejecutar correctamente las funciones acordadas para coordinar partidas y comunicar resultados.

**Métrica M-AF01 — Porcentaje de casos funcionales aprobados**

- **Fórmula:** `100 × casos aprobados / casos planificados`.
- **Unidad:** porcentaje.
- **Universo:** suite versionada y acordada antes de ejecutar la prueba. Un caso se aprueba únicamente cuando cumple todas sus salidas esperadas. Los casos bloqueados o no ejecutados permanecen en el denominador y no se cuentan como aprobados. Sin casos definidos, la métrica no es evaluable.
- **Meta:** al menos 95 % del total y 100 % de los casos críticos aprobados. Ambas condiciones deben cumplirse; un promedio alto no compensa un fallo crítico.
- **Procedimiento:** preparar datos de equipos y partidas, fijar resultados esperados con el moderador y ejecutar casos normales, alternativos y de error. Comparar interfaz y datos persistidos con el resultado esperado. Registrar ID, entradas, resultado esperado, resultado obtenido y evidencia.
- **Frecuencia:** antes de cada entrega y después de cambios en reglas o manejo de resultados.
- **Responsable propuesto:** integrante encargado de pruebas; organizador y moderador validan las reglas y los resultados esperados.
- **Evidencia a conservar:** matriz de pruebas fechada, versión evaluada, capturas y registro de defectos.

Casos candidatos derivados del AS-IS, sujetos a aprobación del alcance del software:

| Caso | Situación | Resultado esperado propuesto | Criticidad |
|---|---|---|---|
| AF-01 | Consultar una partida programada. | Mostrar los equipos, fecha, hora y zona horaria acordados. | Crítico |
| AF-02 | Reprogramar una partida con autorización. | Persistir el nuevo horario y mostrarlo como vigente al volver a consultar. | Crítico |
| AF-03 | Registrar la falta de disponibilidad de un equipo. | Mantener la partida pendiente de resolución; no sustituir al equipo sin aplicar la regla validada. | Normal |
| AF-04 | Consultar las reglas de la partida. | Mostrar la versión de reglas asignada a esa partida. | Normal |
| AF-05 | Confirmar un resultado con datos conocidos. | Conservar el resultado aprobado y mostrar el ganador correspondiente. | Crítico |
| AF-06 | Intentar publicar un ganador con resultado pendiente o contradictorio. | Impedir la publicación definitiva e indicar qué validación falta. | Crítico |

Esta métrica mide conformidad con los casos acordados; no demuestra por sí sola que se hayan descubierto todas las necesidades del usuario.

### 2 Fiabilidad

**Objetivo:** mantener operativas las funciones esenciales durante el torneo y recuperar los datos confirmados ante fallos.

**Métrica M-FI01 — Disponibilidad durante la jornada**

- **Fórmula:** `100 × (minutos de la ventana − minutos indisponibles) / minutos de la ventana`.
- **Unidad:** porcentaje por jornada.
- **Ventana:** desde 30 minutos antes de la primera partida programada hasta el registro del último resultado. Para aceptación inicial, usar un ensayo continuo de 240 minutos.
- **Definición de indisponibilidad:** falla de una comprobación por minuto que consulta el cronograma y crea, lee y elimina un resultado de prueba en un torneo aislado. La comprobación completa debe finalizar correctamente en 10 segundos. Cada comprobación fallida cuenta como un minuto indisponible; una muestra faltante cuenta como fallo. Así se evita considerar disponible un servicio que solo muestra su página de inicio.
- **Meta:** disponibilidad igual o superior a 99,5 %. En el ensayo de 240 muestras, como máximo una puede fallar.
- **Condiciones propuestas:** ambiente equivalente al previsto para el piloto, con 50 sesiones concurrentes y una operación cada 10 segundos por sesión, distribuidas entre consulta de cronograma y consulta de resultados. Esta carga es un supuesto de prueba por validar, no una estimación comprobada de usuarios.
- **Frecuencia y responsable propuesto:** ensayo previo a la entrega y monitoreo en cada jornada; encargado de pruebas y operación.
- **Evidencia:** bitácora de comprobaciones con fecha, duración, respuesta, carga y periodo medido. No excluir mantenimientos ocurridos dentro de la ventana.

**Métrica M-FI02 — Recuperación e integridad tras una interrupción**

- **Medidas:** segundos desde la interrupción controlada hasta recuperar las funciones esenciales; número de registros confirmados perdidos o duplicados al comparar los datos antes y después.
- **Meta:** recuperación en un máximo de 300 segundos y cero registros confirmados perdidos o duplicados en cada ensayo.
- **Procedimiento:** ejecutar tres ensayos en un entorno de prueba, registrar operaciones confirmadas, interrumpir y reiniciar el servicio, comprobar su recuperación y comparar los identificadores y contenidos de los registros. Usar datos ficticios.
- **Frecuencia y evidencia:** antes del piloto y después de cambios de persistencia o recuperación; conservar tiempos y comparación de registros por ensayo.

Las métricas evalúan el software propuesto. Una caída de Discord o del videojuego debe registrarse como dependencia externa; no se garantiza aquí la disponibilidad de esos proveedores.

### 3 Seguridad de la información

**Objetivo:** restringir consultas y modificaciones según el rol y permitir identificar cambios relevantes.

**Métrica M-SE01 — Bloqueo de operaciones no autorizadas**

- **Fórmula:** `100 × intentos correctamente bloqueados / intentos no autorizados ejecutados`.
- **Unidad y meta:** porcentaje; 100 %, con cero lecturas restringidas o modificaciones indebidas.
- **Muestra mínima:** 30 casos distintos, definidos a partir de una matriz de permisos aprobada. Incluir sesión inexistente o vencida, jugador que intenta modificar resultados, participante que intenta acceder a otro equipo y moderador que intenta actuar fuera del torneo asignado.
- **Procedimiento:** probar tanto la interfaz como el acceso directo al servicio, si existe. Un bloqueo es correcto solo si se rechaza la operación y no se revela información restringida ni cambia el estado almacenado. Complementar con casos autorizados para verificar que el sistema no apruebe la métrica simplemente bloqueando todo.
- **Frecuencia:** antes de cada entrega y después de cambios de autenticación, permisos o manejo de resultados.
- **Responsable propuesto:** encargado de pruebas, con validación de permisos por el organizador.
- **Evidencia:** matriz de roles, casos ejecutados, respuestas y comparación del estado antes y después. Ocultar credenciales y usar usuarios ficticios.

**Métrica M-SE02 — Trazabilidad de cambios sensibles**

- **Fórmula:** `100 × cambios con registro de auditoría completo / cambios sensibles realizados`.
- **Meta:** 100 % en al menos 20 cambios autorizados de horarios, reglas y resultados.
- **Registro completo:** usuario responsable, fecha y hora con zona horaria, entidad afectada, acción y valores anterior y nuevo. Para creaciones, identificar expresamente que no existía valor anterior.
- **Procedimiento:** ejecutar cambios conocidos y contrastarlos con la auditoría; verificar que un jugador no pueda modificar esos registros. Conservar reporte y evidencia de la comprobación.
- **Frecuencia y responsable propuesto:** junto con M-SE01, por el mismo encargado de pruebas.

Estos indicadores verifican controles específicos; no equivalen a demostrar ausencia de todas las vulnerabilidades.

## Validación y trazabilidad pendientes

## Trazabilidad con los requisitos

Las métricas se relacionan con los requisitos no funcionales definidos en la [clasificación de requisitos](./Clasificación_de_requisitos.md):

| Requisito | Atributo | Métrica |
|---|---|---|
| RP-09 (disponibilidad) | Fiabilidad | M-FI01 |
| RP-10 (trazabilidad del bracket) | Seguridad de la información | M-SE02 |
| RP-08 (rendimiento) | Eficiencia de desempeño | Se mide directamente con el umbral definido en RP-08 |

Los umbrales propuestos deben validarse con el organizador y el moderador.

## Fuentes

- [Descripción del proyecto](./IngReq-Entrega1.md), [proceso AS-IS](./Proceso_AS-IS.md) y [diagrama AS-IS](diagramabueno.png), versión `9198ebecd419de876d10f00acf001f5fa2be0bc6`.
- [ISO — ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html).

## Regresar

[Ingeniería de Requisitos — Entrega 1](./IngReq-Entrega1.md)
