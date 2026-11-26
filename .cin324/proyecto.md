# Estado del proyecto — generación de la aplicación

## Proyecto
- Nombre: E-Sports Focus — Organización de torneos
- Repositorio de documentación: esta carpeta
- Última auditoría: 2026-11-26 — resultado: consistencia de artefactos y código revisada

## Mapa de artefactos (rutas detectadas)
| Artefacto | Ruta(s) | Estado |
|-----------|---------|--------|
| BPMN AS-IS | `Images/diagrama.bpmn`, `Images/diagrama.png`, `Proceso_AS-IS.md` | completo |
| BPMN TO-BE | `Images/diagram.bpmn`, `Images/diagram.png`, `Rediseño_y_TO-BE.md` | completo |
| Historias de usuario | `Historias_de_usuario.md` (HU-01..03), `07-criterios-aceptacion.md` (HU-01..09) | completo |
| Criterios Gherkin | `07-criterios-aceptacion.md` | completo |
| Modelo de dominio | `diagramas/modelo-dominio.puml`, `diagramas/modelo-dominio.png`, `08-modelo-dominio.md` | completo |
| Casos de uso | `09-casos-de-uso.md`, `diagramas/casos-de-uso.puml`, `diagramas/casos-de-uso.png` | completo |
| Diagramas de estado | `diagramas/est-01.puml`, `diagramas/est-01.png` (Partida), `diagramas/est-02.puml`, `diagramas/est-02.png` (SolicitudCambioHorario), `diagramas/est-03.puml`, `diagramas/est-03.png` (Torneo), `11-diagramas-estado.md` | completo |
| Diagramas de secuencia | `diagramas/dss-01.puml`, `diagramas/dss-01.png`, `diagramas/dss-02.puml`, `diagramas/dss-02.png`, `diagramas/dss-03.puml`, `diagramas/dss-03.png`, `diagramas/dss-04.puml`, `diagramas/dss-04.png`, `10-diagramas-secuencia.md` | completo |
| Requisitos y atributos de calidad | `Clasificación_de_requisitos.md`, `Atributos_de_calidad.md`, `12-trazabilidad.md` | completo |

## Supuestos acordados (por elementos faltantes o dudosos)
- 2026-11-10 — **Alcance revisado:** el estudiante vuelve a HU-04 como primera historia por ser más sencilla y no depender de sistemas externos. HU-02 y HU-03 quedan pendientes para ciclos posteriores. HU-04 proviene de `07-criterios-aceptacion.md`, no de `Historias_de_usuario.md` (señalado al estudiante).
- 2026-11-10 — HU-04 modifica la disponibilidad (`Pendiente → Confirmada`) sin diagrama de estado propio; se acepta `confirmada` como atributo de `Disponibilidad` (confirmado por el estudiante).
- 2026-11-10 — La regla de las 8 horas de HU-04 se mantiene tal como está en el Gherkin (confirmado por el estudiante).
- 2026-11-10 — La asociación Partida–Equipo se deja como `0..*` a `2` en el modelo (confirmado por el estudiante).
- 2026-11-10 — `07-criterios-aceptacion.md` es la fuente del Gherkin para HU-01..HU-06; las historias HU-02 y HU-03 se toman de `Historias_de_usuario.md` (decisión del estudiante).
- 2026-11-10 — La tabla de actividades del TO-BE se usa sin IDs `ACT-TOBE-xx`; los enlaces a `as-is.bpmn`/`to-be.bpmn` quedan como están (no bloqueante).
- 2026-11-17 — HU-04 validada: se acepta confirmar mientras la partida esté `Programada` (las 8 horas solo indican «requiere revisión» al Moderador), el Moderador es actor secundario de solo lectura en CU-01 y la «requiere revisión» se calcula al consultar (sin tarea en segundo plano). Ficha en `.cin324/historias/HU-04.md`.
- 2026-11-19 — **Alcance confirmado por el estudiante:** HU-01 queda fuera porque depende de la API del videojuego. HU-04 se valida y se archiva. La siguiente historia es HU-03 (registro manual, sin depender de la API) y después HU-06. Discord se simula; no se excluye por ser sistema externo.
- 2026-11-19 — **Validación de HU-04:** los 4 escenarios Gherkin se cumplen; 12 pruebas automáticas pasan. Observaciones menores sin cambios de requisitos: la fecha de confirmación se muestra en formato ISO y el `README`/`tasks.md` dicen 4 partidas de ejemplo cuando el `seed` crea 5.
- 2026-11-20 — **HU-03 validada:** no se permiten empates; el marcador es el resultado final de la serie. HU-03 incluye el registro, la actualización del bracket con historial y la notificación simulada a Organizador y Jugadores. Se mantiene la inferencia de los equipos desde `disponibilidad` (sin `partida_equipo`). Ficha en `.cin324/historias/HU-03.md`; se ajustaron `07-criterios-aceptacion.md`, `11-diagramas-estado.md` y `08-modelo-dominio.md`.
- 2026-11-20 — **HU-03 implementada y validada por el estudiante:** los 5 escenarios Gherkin se cumplen; 26 pruebas automáticas pasan (14 de HU-03 y las 12 existentes de HU-04). El cambio se archivó y la capacidad `resultado` quedó en `openspec/specs/resultado/spec.md`. La base `data/app.db` se recreó con los datos nuevos.
- 2026-11-20 — **HU-06 validada:** el anuncio del ganador se representa sin una clase `Anuncio`; se usa `Partida.estado = Anunciada` y un registro técnico del envío a Discord. La pantalla del Organizador usa la opción B (sección de Anuncios separada). Ficha en `.cin324/historias/HU-06.md`. HU-07 (página pública del torneo, opción C) queda para el ciclo siguiente.
- 2026-11-20 — **HU-06 implementada:** anuncio automático al confirmar el resultado, tabla `anuncio` (migración `004`), adaptador `DiscordSimulado.anunciar_ganador`, pantalla `/organizador` y acceso desde el inicio. Se agregó la rama «Discord no responde» a DSS-01 y DSS-02. 29 pruebas pasan (17 de servicios, 5 de HU-03, 4 de HU-04 y 3 de HU-06).
- 2026-11-20 — **HU-06 cerrada:** validada por el estudiante; las specs `anuncio` y `resultado` se sincronizaron y el cambio se archivó en `openspec/changes/archive/2026-11-20-hu-06-anuncio-ganador`. 29 pruebas pasan.
- 2026-11-20 — **HU-07 validada:** página pública del torneo (opción C) con anuncios, bracket y partidas de solo lectura; menú desplegable derecho con navegación e inicios de sesión de demostración (Jugador, Moderador y Organizador). Se agrega el actor Visitante y el caso de uso CU-07. Ficha en `.cin324/historias/HU-07.md`; cambio `hu-07-pagina-torneo`.
- 2026-11-20 — **HU-07 implementada:** el inicio (`/`) muestra el torneo con anuncios, bracket y partidas; `/torneo` redirige a `/`; el menú desplegable en `base.html` usa barra blanca, panel de 360 px alineado a la derecha, cierre con X/`Esc`/clic fuera, foco y atributos ARIA, y el procesador de contexto con los roles de demostración. Se retiran del inicio las tarjetas de rol duplicadas. 4 pruebas nuevas de HU-07 y 33 pruebas en total. Pendiente de validación por el estudiante.
- 2026-11-21 — **HU-07 ajustada por feedback:** barra blanca con borde, menú desplegable bajo la barra (sin fondo oscuro, 360 px en escritorio y ancho completo en móvil) y «Entrar como» con tres botones de rol que despliegan la lista de personas (una por vez). 33 pruebas y `openspec validate --strict` válidos.
- 2026-11-21 — **HU-07 validada y archivada:** el estudiante aprobó el inicio público y el menú de tres botones. Spec `torneo-publico` sincronizada en `openspec/specs/torneo-publico/spec.md`; cambio en `openspec/changes/archive/2026-11-21-hu-07-pagina-torneo`.
- 2026-11-22 — **Ajuste de Inicio y Paleta de colores:** se retiró la tarjeta redundante de Partidas del inicio (`/`), dejando solo Anuncios y Bracket resumido con enlace hacia `/bracket` (donde reside la tabla completa con marcadores e historial). Se incorporó la paleta de colores personalizada (`#F4E9CD`, `#9DBEBB`, `#77ACA2`, `#468189`) mediante variables CSS armónicas para mejorar la estética visual y cumplir criterios de contraste/accesibilidad. Se actualizaron los artefactos de requisitos y la especificación.
- 2026-11-22 — **HU-08 implementada y validada:** visualización gráfica de bracket tipo árbol con llaves competitivas, rondas secuenciales y actualización dinámica de ganadores.
- 2026-11-23 — **HU-09 acordada con el docente:** incorporación del módulo exclusivo del Organizador para creación y configuración de torneos, gestión de jugadores/equipos participantes y estructura de premios (RP-11, CU-09). Ficha en `.cin324/historias/HU-09.md`.
- 2026-11-26 — **Ajuste de consistencia de artefactos y código:** se completó el modelo de dominio (atributos de Torneo, asociación `inscribe`, Premio sin «condiciones de entrega» y correspondencia clase → tabla SQLite); se corrigió la trazabilidad (sin `Anuncio` como clase, con enlaces a código y pruebas); se actualizaron los criterios Gherkin (HU-04 con torneo visible, HU-08 con avance dinámico, HU-09 con actualización y estado inválido); se agregó la columna **Torneo** en la vista del jugador; el inicio muestra un bracket resumido por fases y la tabla detallada queda solo en `/bracket`; se validó el catálogo de estados del torneo (rechazando también el valor vacío); los torneos existentes con estado vacío se normalizan a `Borrador` (migración `008`); y `resultado.moderador_id` pasó a admitir `NULL` para alinear la base con el modelo (migración `007`).

## Stack (se define una sola vez)
- Decisión: 2026-11-17 — **Opción B (Python)**, confirmada por el estudiante
- Lenguaje y framework: Python 3.12 + FastAPI + Uvicorn; plantillas Jinja2
- Base de datos: SQLite con la biblioteca estándar `sqlite3` (`data/app.db`); migraciones SQL numeradas en `app/db/migrations/`, registradas en `schema_migrations`
- Pruebas: pytest + `TestClient` de FastAPI (httpx), una por escenario Gherkin
- Cómo instalar: `python -m venv .venv`; `.venv\Scripts\activate`; `pip install -r requirements.txt`
- Cómo ejecutar: `python -m app.db.seed` (crea la base y datos de ejemplo); `.venv\Scripts\python.exe -m uvicorn app.main:app --reload` en http://localhost:8000 (o activar `.venv` y usar `uvicorn app.main:app --reload`)
- Cómo probar: `.venv\Scripts\python.exe -m pytest` (o `pytest` con el entorno activado)
- Entorno local preparado el 2026-11-19: Python 3.12.10, `.venv` con dependencias y OpenSpec CLI 2.1.0.

## Historias
| Historia | Estado | Cambio de OpenSpec | Fecha | Observaciones |
|----------|--------|--------------------|-------|----------------|
| HU-01 | fuera de alcance | — | 2026-11-19 | Depende de la API del videojuego; excluida por decisión del estudiante |
| HU-02 | pendiente | — | — | Notificación del resultado; necesita un resultado de HU-03 |
| HU-03 | implementada, validada y archivada | `openspec/changes/archive/2026-11-20-hu-03-registrar-resultado` | 2026-11-20 | Registro manual del resultado; 5 escenarios y 14 pruebas; spec en `openspec/specs/resultado/spec.md` |
| HU-04 | implementada, validada y archivada | `openspec/changes/archive/2026-11-19-hu-04-confirmar-disponibilidad` | 2026-11-19 | Confirmación de disponibilidad; 4 escenarios y 12 pruebas; validada sin bloqueantes |
| HU-05 | implementada, validada y archivada | `openspec/changes/archive/2026-11-22-hu-05-cambio-horario` | 2026-11-22 | Solicitud y resolución de cambio de horario; 5 escenarios y 5 pruebas; 38 pruebas en total; spec en `openspec/specs/cambio-horario/spec.md` |
| HU-06 | implementada, validada y archivada | `openspec/changes/archive/2026-11-20-hu-06-anuncio-ganador` | 2026-11-20 | Anuncio del ganador; 3 escenarios y 3 pruebas; pantalla del Organizador con opción B; 29 pruebas en total |
| HU-07 | implementada, validada y archivada; reajustada | `openspec/changes/archive/2026-11-21-hu-07-pagina-torneo` | 2026-11-21 | Inicio público del torneo y menú desplegable con tres botones de rol; 4 escenarios y 4 pruebas; spec en `openspec/specs/torneo-publico/spec.md`. Reajuste 2026-11-26: bracket resumido por fases y tabla detallada solo en `/bracket`. |
| HU-08 | implementada, validada y archivada | `openspec/changes/archive/2026-11-22-hu-08-bracket-grafico` | 2026-11-22 | Visualización gráfica del Bracket del torneo (árbol de llaves estilo Liquipedia/VLR con avance dinámico en vivo); 5 escenarios y 5 pruebas; spec en `openspec/specs/bracket-grafico/spec.md` |
| HU-09 | implementada, validada y archivada; ampliada | `openspec/changes/archive/2026-11-23-hu-09-gestion-torneo` | 2026-11-23 | Creación y gestión de torneos, participantes y premios por el Organizador (RP-11, CU-09); 6 escenarios y 6 pruebas; 49 pruebas en total; spec en `openspec/specs/gestion-torneo/spec.md`. Incluye validación del catálogo de estados. |

## Validaciones
| Historia | Informe | Estado | Fecha |
|----------|---------|--------|-------|
| HU-04 | Validación en chat (no se guardó archivo) | Validada sin observaciones bloqueantes | 2026-11-19 |
| HU-03 | Validación en chat (no se guardó archivo) | Validada por el estudiante sin observaciones bloqueantes | 2026-11-20 |
| HU-06 | Validación en chat (no se guardó archivo) | Confirmada por el estudiante; ficha lista para especificar | 2026-11-20 |
| HU-06 | Implementación (validada y archivada) | 29 pruebas pasan; `openspec validate --strict` válido; specs sincronizadas | 2026-11-20 |
| HU-07 | Validación en chat (no se guardó archivo) | Confirmada por el estudiante; ficha lista para especificar | 2026-11-20 |
| HU-07 | Implementación (validada y archivada) | 33 pruebas pasan; `openspec validate --strict` válido; spec `torneo-publico` sincronizada; menú revisado en el navegador | 2026-11-21 |
| HU-05 | Implementación (validada) | 38 pruebas pasan; `openspec validate` válido; capacidad `cambio-horario` especificada y probada | 2026-11-22 |
| HU-08 | Implementación (validada) | 42 pruebas pasan; `openspec validate` válido; capacidad `bracket-grafico` especificada y probada | 2026-11-22 |
| HU-09 | Implementación (validada y archivada) | 48 pruebas pasan; `openspec validate --all` (7 specs válidas); capacidad `gestion-torneo` especificada, probada y archivada | 2026-11-23 |
| Consistencia | Revisión de artefactos vs código | 49 pruebas pasan; `openspec validate --all` válido; modelo, trazabilidad, Gherkin, CU, estados y README alineados | 2026-11-26 |

## Cambios posteriores
| Cambio | Historia afectada | Motivo | Fecha |
|--------|-------------------|--------|-------|
| Ajuste semántico de disponibilidad (colores verde/amarillo/rojo, estado Cancelado por plazo vencido) y retiro de emojis excepto copa | HU-04, HU-07 | Petición del estudiante para clarificar estados de disponibilidad y refinar la estética visual | 2026-11-22 |
| Rediseño heurístico UX/UI (4 fases: Arquitectura Inicio/Bracket, Wayfinding/Migas, Hero y VS-inline, Responsividad y Badges) | HU-07 | Auditoría de usabilidad y jerarquía visual aprobada por el estudiante | 2026-11-22 |
| Simplificación de inicio (sin tabla Partidas redundante) y paleta modo oscuro/claro con alternador | HU-07 | Petición del estudiante para clarificar la vista pública y dotar de identidad visual con tema dual | 2026-11-22 |
| Bracket resumido por fases en `/` y tabla detallada solo en `/bracket` | HU-07 | El inicio conservaba una tabla de enfrentamientos; se reemplazó por el resumen exigido por la spec | 2026-11-26 |
| Corrección de consistencia de modelo, trazabilidad, Gherkin, casos de uso, estados, vista del jugador, README y esquema (cambio OpenSpec `openspec/changes/archive/2026-11-26-ajuste-consistencia-artefactos`) | HU-04, HU-07, HU-08, HU-09 | Revisión de la rúbrica y correcciones del profesor | 2026-11-26 |
