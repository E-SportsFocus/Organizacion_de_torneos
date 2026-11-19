# Proposal — HU-04 Confirmación de disponibilidad

## Why

Hoy los jugadores solo se enteran de su partida por Discord y el Moderador no tiene una confirmación formal de que los equipos puedan jugar. HU-04 reemplaza esa revisión informal por un registro en la plataforma, para que el Moderador sepa con anticipación si la partida puede jugarse.

## What Changes

- Se agrega la pantalla del Jugador para ver las partidas programadas de su equipo y confirmar la disponibilidad del equipo para una partida.
- Se registra la disponibilidad por equipo y partida, con su valor (`Pendiente`/`Confirmada`) y la fecha de confirmación; se crea en `Pendiente` junto con cada partida.
- Se agrega la consulta del Moderador: estado de disponibilidad de cada partida y marca «requiere revisión» cuando la hora de inicio ya pasó y algún equipo sigue `Pendiente`.
- Se rechaza la confirmación si la partida ya inició o ya finalizó, si el jugador no pertenece al equipo o si la disponibilidad ya estaba confirmada.
- Se agregan los datos de ejemplo mínimos de torneo, equipos, jugadores, moderador y partidas que esta historia necesita leer.

## Capabilities

### New Capabilities
- `disponibilidad`: confirmación y consulta de la disponibilidad de un equipo para una partida del torneo.

### Modified Capabilities
- Ninguna: es la primera historia y no existen especificaciones vigentes.

## Impact

- Historia: **HU-04** (`07-criterios-aceptacion.md`, líneas 99-132); ficha confirmada en `.cin324/historias/HU-04.md`.
- Actividad del TO-BE: **Confirman disponibilidad en la plataforma (Jugadores)**; en el AS-IS era «Revisan la información que recibieron» (`Rediseño_y_TO-BE.md:37`).
- Caso de uso: **CU-01 — Confirmar la disponibilidad del equipo para una partida** (actor principal Jugador; Moderador como actor secundario de solo lectura).
- Requisito funcional cubierto: **RP-01**. RP-09 (no funcional) no se implementa.
- Datos: tablas nuevas para `persona`, `jugador`, `moderador`, `equipo`, `torneo`, `partida` y `disponibilidad` (se crean solo las columnas que esta historia usa).
- Pantallas: selector de rol de demostración, vista del Jugador y vista de consulta del Moderador.
- Sistemas externos: ninguno (no se integra API del videojuego ni Discord).
- Fuera de alcance: HU-02, HU-03, HU-05 y HU-06; inicio automático de la partida (`Programada → En curso`); notificaciones; autenticación real; requisitos no funcionales.
