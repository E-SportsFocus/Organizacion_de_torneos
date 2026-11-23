# Design

## Context

El sistema cuenta con paneles de Jugador, Moderador y una pantalla inicial de Organizador orientada al anuncio de ganadores (HU-06). Faltaba la funcionalidad central de administración de torneos: la creación y configuración inicial del certamen deportivo por parte del Organizador (HU-09). Para ello se habilita un espacio donde el organizador define las reglas, los videojuegos admitidos (ej: Valorant, League of Legends, CS2, Fortnite), las fechas, los participantes en competencia y la escala de recompensas.

## Goals / Non-Goals

**Goals:**
- Proveer un formulario unificado y claro de 3 secciones:
  1. Información General del Torneo (Nombre, Videojuego, Fecha/hora de inicio, Zona horaria, Estado, Bolsa CLP, Descripción/reglamento).
  2. Participantes y Equipos (Selección múltiple de equipos inscritos con sus integrantes desglosados).
  3. Estructura de Premios (Distribución por puestos: 1.º, 2.º y 3.º lugar con montos en CLP y condiciones).
- Asegurar que la pantalla de creación/gestión sea exclusiva para el Organizador (oculta para Jugador, Moderador y Visitante).
- Permitir que el sistema arranque con datos limpios para que el usuario pueda crear y personalizar su propio torneo.
- Reflejar inmediatamente la información configurada en la portada pública y panel de organizador.

**Non-Goals:**
- Validación de identidad bancaria o cobro de inscripción a jugadores.
- Modificación en caliente de partidas ya jugadas al alterar los equipos.

## Decisions

### 1. Modelo de Datos y Migración (`006_torneo_premios_inscripciones.sql`)
- Ampliación de tabla `torneo`:
  - `fecha_inicio TEXT`
  - `zona_horaria TEXT DEFAULT 'America/Santiago'`
  - `bolsa_premios TEXT`
  - `descripcion TEXT`
  - `estado TEXT DEFAULT 'Borrador'`
- Nueva tabla `premio`:
  - `id INTEGER PRIMARY KEY`, `torneo_id INTEGER`, `posicion INTEGER`, `posicion_texto TEXT`, `monto_texto TEXT`, `descripcion TEXT`.
- Nueva tabla `inscripcion`:
  - `id INTEGER PRIMARY KEY`, `torneo_id INTEGER`, `equipo_id INTEGER`, `fecha_inscripcion TEXT`, `estado TEXT`.

### 2. Capa de Servicios (`app/servicios/torneo_gestion.py`)
- `obtener_torneo_completo(conexion, torneo_id)`
- `guardar_o_crear_torneo(conexion, organizador_id, datos)`
- `guardar_equipos_inscritos(conexion, torneo_id, lista_equipo_ids)`
- `guardar_premios_torneo(conexion, torneo_id, lista_premios)`
- Manejo transaccional con `BEGIN IMMEDIATE` y validación de campos obligatorios (`nombre` y `juego`).

### 3. Exclusividad de Navegación (`app/templates/base.html`)
- El enlace hacia `/organizador/torneo` se condiciona con `{% if en_organizador %}` en el menú lateral.
- La ruta de migas de pan (`base.html`) detecta `/organizador/torneo` y genera la jerarquía `Inicio / Panel Organizador / Gestión del Torneo`.

## Risks / Trade-offs

- [Campos vacíos al inicio] $\rightarrow$ El sistema maneja valores por defecto y placeholders claros ("Ej: Copa E-Sports Focus", "$850.000 CLP") para guiar al usuario sin imponer datos hardcodeados.
- [Compatibilidad con vistas públicas] $\rightarrow$ La portada (`torneo.html`) consume de forma transparente la bolsa de premios y la descripción ingresada por el organizador.
