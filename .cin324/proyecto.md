# Estado del proyecto — generación de la aplicación

## Proyecto
- Nombre: E-Sports Focus — Organización de torneos
- Repositorio de documentación: esta carpeta
- Última auditoría: 2026-11-10 — resultado: con supuestos (sin bloqueantes)

## Mapa de artefactos (rutas detectadas)
| Artefacto | Ruta(s) | Estado |
|-----------|---------|--------|
| BPMN AS-IS | `Images/diagrama.bpmn`, `Images/diagrama.png`, `Proceso_AS-IS.md` | completo |
| BPMN TO-BE | `Images/diagram.bpmn`, `Images/diagram.png`, `Rediseño_y_TO-BE.md` | completo |
| Historias de usuario | `Historias_de_usuario.md` (HU-01..03), `07-criterios-aceptacion.md` (HU-01..06) | completo |
| Criterios Gherkin | `07-criterios-aceptacion.md` | completo |
| Modelo de dominio | `diagramas/modelo-dominio.puml`, `diagramas/modelo-dominio.png`, `08-modelo-dominio.md` | completo |
| Casos de uso | `09-casos-de-uso.md`, `diagramas/casos-de-uso.puml` | completo |
| Diagramas de estado | `diagramas/est-01.puml` (Partida), `diagramas/est-02.puml` (SolicitudCambioHorario), `11-diagramas-estado.md` | completo |
| Diagramas de secuencia | `diagramas/dss-01.puml`, `dss-02.puml`, `dss-03.puml`, `10-diagramas-secuencia.md` | completo |
| Requisitos y atributos de calidad | `Clasificación_de_requisitos.md`, `Atributos_de_calidad.md`, `12-trazabilidad.md` | completo |

## Supuestos acordados (por elementos faltantes o dudosos)
- 2026-11-10 — **Alcance revisado:** el estudiante vuelve a HU-04 como primera historia por ser más sencilla y no depender de sistemas externos. HU-02 y HU-03 quedan pendientes para ciclos posteriores. HU-04 proviene de `07-criterios-aceptacion.md`, no de `Historias_de_usuario.md` (señalado al estudiante).
- 2026-11-10 — HU-04 modifica la disponibilidad (`Pendiente → Confirmada`) sin diagrama de estado propio; se acepta `confirmada` como atributo de `Disponibilidad` (confirmado por el estudiante).
- 2026-11-10 — La regla de las 8 horas de HU-04 se mantiene tal como está en el Gherkin (confirmado por el estudiante).
- 2026-11-10 — La asociación Partida–Equipo se deja como `0..*` a `2` en el modelo (confirmado por el estudiante).
- 2026-11-10 — `07-criterios-aceptacion.md` es la fuente del Gherkin para HU-01..HU-06; las historias HU-02 y HU-03 se toman de `Historias_de_usuario.md` (decisión del estudiante).
- 2026-11-10 — La tabla de actividades del TO-BE se usa sin IDs `ACT-TOBE-xx`; los enlaces a `as-is.bpmn`/`to-be.bpmn` quedan como están (no bloqueante).
- 2026-11-17 — HU-04 validada: se acepta confirmar mientras la partida esté `Programada` (las 8 horas solo indican «requiere revisión» al Moderador), el Moderador es actor secundario de solo lectura en CU-01 y la «requiere revisión» se calcula al consultar (sin tarea en segundo plano). Ficha en `.cin324/historias/HU-04.md`.

## Stack (se define una sola vez)
- Decisión: 2026-11-17 — **Opción B (Python)**, confirmada por el estudiante
- Lenguaje y framework: Python 3.12 + FastAPI + Uvicorn; plantillas Jinja2
- Base de datos: SQLite con la biblioteca estándar `sqlite3` (`data/app.db`); migraciones SQL numeradas en `app/db/migrations/`, registradas en `schema_migrations`
- Pruebas: pytest + `TestClient` de FastAPI (httpx), una por escenario Gherkin
- Cómo instalar: `python -m venv .venv`; `.venv\Scripts\activate`; `pip install -r requirements.txt`
- Cómo ejecutar: `python -m app.db.seed` (crea la base y datos de ejemplo); `uvicorn app.main:app --reload` en http://localhost:8000
- Cómo probar: `pytest`

## Historias
| Historia | Estado | Cambio de OpenSpec | Fecha | Observaciones |
|----------|--------|--------------------|-------|----------------|
| HU-01 | fuera de alcance | — | — | Ignorada por decisión del estudiante |
| HU-02 | pendiente | — | — | Notificación del resultado |
| HU-03 | pendiente | — | — | Registro manual del resultado |
| HU-04 | lista para especificar | — | 2026-11-17 | Ficha confirmada; confirmación de disponibilidad; sin sistemas externos |
| HU-05 | fuera de alcance por ahora | — | — | No priorizada |
| HU-06 | fuera de alcance por ahora | — | — | No priorizada |

## Validaciones
| Historia | Informe | Estado | Fecha |
|----------|---------|--------|-------|
| — | — | — | — |

## Cambios posteriores
| Cambio | Historia afectada | Motivo | Fecha |
|--------|-------------------|--------|-------|
| — | — | — | — |
