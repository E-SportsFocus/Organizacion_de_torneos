# Tasks

## 1. Base de datos y migración
- [x] 1.1 Crear migración `app/db/migrations/006_torneo_premios_inscripciones.sql` con columnas de `torneo` y tablas `premio` e `inscripcion`.
- [x] 1.2 Actualizar `app/db/seed.py` para aplicar la migración y soportar torneos configurados limpiamente.

## 2. Lógica de negocio y servicios
- [x] 2.1 Crear servicio `app/servicios/torneo_gestion.py` con operaciones CRUD de torneo, participantes y premios.
- [x] 2.2 Validar campos obligatorios (`nombre` y `juego`) y reglas de negocio.

## 3. Rutas y plantillas
- [x] 3.1 Añadir rutas GET `/organizador/torneo` y POST `/organizador/torneo/guardar` en `app/rutas/organizador.py`.
- [x] 3.2 Crear plantilla `app/templates/gestion_torneo.html` con diseño responsivo, temas claro/oscuro y formulario de 3 secciones.
- [x] 3.3 Integrar enlace exclusivo de "Creación de torneo" en `base.html` y breadcrumb dinámico.

## 4. Pruebas y documentación
- [x] 4.1 Crear suite de pruebas automatizadas `tests/test_hu09.py` cubriendo los 4 escenarios Gherkin.
- [x] 4.2 Actualizar artefactos de requisitos: `Historias_de_usuario.md`, `07-criterios-aceptacion.md`, `08-modelo-dominio.md`, `09-casos-de-uso.md`, `12-trazabilidad.md`, `.cin324/historias/HU-09.md` y `.cin324/proyecto.md`.
- [x] 4.3 Validar con `openspec.cmd validate --all` y archivar el cambio.
