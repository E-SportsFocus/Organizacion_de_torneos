# Proposal

## Why

La historia HU-09 ("Creación y gestión de torneos, participantes y premios") atiende la necesidad fundamental del rol de Organizador de disponer de un apartado exclusivo y centralizado para la configuración autónoma del campeonato. Anteriormente, la información del torneo, los participantes y la estructura de premios eran predeterminados o estáticos en la base de datos de desarrollo. Para permitir una gestión realista, integral y desacoplada (cumpliendo el requisito funcional RP-11 y caso de uso CU-09), se requiere una interfaz administrativa exclusiva donde el Organizador pueda registrar los datos generales del torneo, seleccionar e inscribir a los equipos/jugadores participantes y definir la bolsa de premios desglosada por posiciones competitivas.

## What Changes

- Se introduce la capacidad `gestion-torneo` para permitir al Organizador crear, parametrizar y actualizar torneos de deportes electrónicos.
- Se amplía el esquema de base de datos (`app/db/migrations/006_torneo_premios_inscripciones.sql`) añadiendo atributos a `torneo` (`fecha_inicio`, `zona_horaria`, `bolsa_premios`, `descripcion`, `estado`), la tabla `premio` y la tabla `inscripcion`.
- Se implementa el servicio de negocio `app/servicios/torneo_gestion.py` para encapsular la lógica de creación, actualización, inscripción de equipos y definición de premios.
- Se crean las rutas `/organizador/torneo` y `/organizador/torneo/guardar` en `app/rutas/organizador.py`.
- Se implementa la plantilla de gestión `app/templates/gestion_torneo.html` accesible exclusivamente en sesión de Organizador, integrando la opción "Creación de torneo" en el menú lateral.
- Se agregan pruebas automatizadas en `tests/test_hu09.py` cubriendo los 4 escenarios Gherkin.

## Capabilities

### New Capabilities
- `gestion-torneo`: gestión integral y exclusiva del Organizador para la creación y edición de torneos, inscripción oficial de equipos participantes y desglose de la estructura de premios.

### Modified Capabilities
<!-- No se modifican las capacidades previas de anuncio, disponibilidad o resultado -->

## Impact

- `app/db/migrations/006_torneo_premios_inscripciones.sql`: migración de base de datos con tablas `premio` e `inscripcion` y columnas en `torneo`.
- `app/servicios/torneo_gestion.py`: servicio con funciones de creación/actualización de torneo, inscripción de equipos y gestión de premios.
- `app/rutas/organizador.py`: rutas GET y POST para la gestión del torneo.
- `app/templates/gestion_torneo.html`: interfaz administrativa de 3 secciones (Datos generales, Participantes, Premios).
- `app/templates/organizador.html`: tarjeta de acceso al gestor y resumen del torneo activo.
- `app/templates/base.html`: enlace exclusivo de "Creación de torneo" para el rol Organizador y breadcrumb dinámico.
- `tests/test_hu09.py`: suite de pruebas para los 4 escenarios de HU-09.
- `.cin324/historias/HU-09.md`, `Historias_de_usuario.md`, `07-criterios-aceptacion.md`, `08-modelo-dominio.md`, `09-casos-de-uso.md`, `12-trazabilidad.md`.

## Fuera de alcance

- Pasarelas de pago reales o transferencias bancarias automatizadas para la entrega de premios (la bolsa se maneja de forma nominal en CLP dentro del sistema).
- Autenticación federada o registro externo de nuevos usuarios (se mantiene el esquema de sesión por roles de demostración acordado para el prototipo).
