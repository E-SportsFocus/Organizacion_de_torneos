# Design

## Context

La aplicación ya implementa HU-03 a HU-09. La revisión de consistencia encontró que algunos artefactos de requisitos quedaron desactualizados respecto del código y que dos vistas no reflejaban lo que la especificación exige: el inicio conservaba una tabla de enfrentamientos en lugar del bracket resumido y la vista del jugador no mostraba el torneo de cada partida. Además, el modelo de dominio declara `Moderador 0..1` para `Resultado`, pero la base exigía `NOT NULL`.

## Goals / Non-Goals

**Goals:**
- Hacer que el inicio muestre un bracket resumido por fases, sin la tabla detallada.
- Mostrar el torneo en la vista del jugador.
- Validar el estado del torneo contra los cuatro valores de EST-03.
- Alinear el esquema SQLite con la multiplicidad `0..1` de `Resultado — Moderador`.
- Dejar la trazabilidad con enlaces a código y pruebas.

**Non-Goals:**
- Implementar la API del videojuego (HU-01).
- Automatizar las transiciones del estado del torneo.
- Cambiar las reglas de negocio de disponibilidad, resultado, cambio de horario o anuncio.

## Decisions

### 1. Bracket resumido en el inicio

El contexto de `GET /` incorpora `rondas_bracket` mediante `app.servicios.bracket.obtener_bracket_estructurado`. La plantilla `torneo.html` agrupa las partidas por fase y muestra los equipos y el ganador o el estado de espera. La tabla detallada con marcador e historial se conserva en `GET /bracket`.

Se descartó reutilizar la tabla de `bracket.html` porque duplicaría la vista de auditoría que la HU-07 quiere dejar fuera del inicio. También se descartó renderizar el árbol gráfico completo en el inicio para no competir con la vista de HU-08.

### 2. Torneo visible para el jugador

`listar_partidas_equipo` ya devuelve `t.nombre AS torneo`; solo se agregó la columna a `jugador.html`. No se requiere una consulta nueva ni un cambio de esquema.

### 3. Catálogo de estados del torneo

`ESTADOS_TORNEO` centraliza los valores de EST-03. `crear_o_actualizar_torneo` valida el estado contra el catálogo, rechaza el valor vacío y usa `Borrador` como valor inicial. El formulario de gestión preselecciona `Borrador` cuando el torneo aún no tiene estado. Las transiciones siguen siendo manuales: el Organizador elige el estado y el sistema rechaza valores fuera del catálogo. La migración `008_torneo_estado_borrador.sql` normaliza los torneos existentes con estado vacío.

### 4. `resultado.moderador_id` opcional

La migración `007_resultado_moderador_opcional.sql` recrea la tabla `resultado` sin `NOT NULL` en `moderador_id`. Los resultados manuales (HU-03) siempre informan al Moderador; los automáticos (HU-01) no lo requieren. La migración conserva los datos existentes y las referencias de `resultado_marcador`, `bracket_actualizacion`, `anuncio` y `notificacion`.

## Risks / Trade-offs

- [Duplicación de consulta en `/`] → `obtener_bracket_estructurado` vuelve a leer las partidas que ya se leyeron para los anuncios. El costo es bajo para el tamaño del prototipo y evita acoplar la vista pública al servicio de resultados.
- [Estado inicial en Borrador] → El seed crea un torneo en blanco con estado `Borrador`; el Organizador debe completar los datos. Es coherente con EST-03 y con el flujo de HU-09.
- [Migración de tabla en SQLite] → Se desactivan las claves foráneas durante la recreación y se restauran al final; las pruebas usan una base nueva y verifican el flujo completo.
