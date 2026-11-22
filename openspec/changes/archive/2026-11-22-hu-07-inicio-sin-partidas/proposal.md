# Proposal: Ajuste de Inicio y Paleta de Colores

## Why

El estudiante solicitó simplificar la vista pública de inicio (`/`) para eliminar la duplicación de la tabla de partidas con marcador (la cual ya existe detallada en `/bracket` desde HU-03), dejando el inicio enfocado exclusivamente en los anuncios de ganadores y el bracket resumido, con un enlace al detalle completo. Además, se solicitó incorporar una paleta de colores personalizada (`#F4E9CD`, `#9DBEBB`, `#77ACA2`, `#468189`) para que la aplicación tenga una identidad visual atractiva, armónica y moderna sin perder contraste ni legibilidad.

## What Changes

- En `app/templates/torneo.html`: se elimina la tarjeta redundante de Partidas (tabla con marcadores por equipo). El bracket resumido ahora incluye un enlace directo hacia `/bracket` para consultar el detalle completo de partidas y su historial.
- En `app/templates/base.html`: se implementa un sistema dual de temas (Modo Oscuro y Modo Claro) con persistencia en `localStorage` y botón conmutador en la barra de navegación:
  - **Modo Oscuro:** `#0F0C18` (fondo principal), `#1A162B` (superficies y barra), `#2E274A` (bordes), `#00F0FF` (acento primario Cyan Eléctrico) y `#F43F5E` (acento secundario Carmesí Rose).
  - **Modo Claro:** `#F8F7FC` (fondo suave), `#FFFFFF` (superficies y barra), `#E4E0F2` (bordes), `#0284C7` (acento primario Sky Blue) y `#E11D48` (acento secundario Rose Carmesí).
- Se actualizan las pruebas automáticas en `tests/test_hu07.py` para verificar que el inicio contiene anuncios, bracket y el enlace a `/bracket`, comprobando que la tabla detallada reside en `/bracket`.
- Se actualizan los artefactos del curso (`.cin324/historias/HU-07.md`, `07-criterios-aceptacion.md`, `09-casos-de-uso.md`, `12-trazabilidad.md`, `README.md`, `.cin324/proyecto.md`) y la especificación en `openspec/specs/torneo-publico/spec.md`.

## Capabilities

### Modified Capabilities
- `torneo-publico`: el requisito de inicio público ahora especifica anuncios y bracket resumido con enlace al detalle en `/bracket`.

## Fuera de alcance
- Modificaciones en la base de datos o migraciones (los datos leídos se mantienen idénticos).
- Cambios en las rutas internas de los roles (`/moderador`, `/organizador`, `/jugador`).
- Autenticación real.
