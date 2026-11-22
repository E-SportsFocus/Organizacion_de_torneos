# Design

## Context

La aplicación ya tiene las vistas internas de Jugador (`/jugador`), Moderador (`/moderador`), Organizador (`/organizador`) y Bracket (`/bracket`). Los datos del torneo se obtienen con `app.servicios.resultado.listar_bracket` y `app.servicios.anuncio.anuncios_por_partida`. La navegación actual es una fila de enlaces en `base.html` y el selector de rol de demostración vive en `index.html`.

HU-07 agrega una vista pública de solo lectura y una navegación común. No cambia el modelo de dominio ni el estado de las partidas.

## Decisions

### 1. Inicio público `/`

- El módulo `app/rutas/torneo.py` atiende `GET /` con el contenido público del torneo y mantiene `GET /torneo` como redirección 307 a `/` para los enlaces anteriores.
- Retira la vista de inicio de `app/rutas/disponibilidad.py` y la plantilla `index.html`, que ya no se usan.
- Toma el primer torneo por `id`, igual que `/bracket`.
- Reutiliza `listar_bracket` para las partidas y `anuncios_por_partida` para los anuncios. No crea consultas nuevas de negocio.
- La tabla `bracket` solo se consulta para mostrar la última actualización.
- Formatea las fechas con el mismo patrón `dd/mm/aaaa HH:MM` que las otras rutas.

### 2. Plantilla `torneo.html`

Tres secciones dentro de tarjetas, en este orden:

1. **Anuncios de ganadores:** una tarjeta por partida anunciada, con fase, ganador, marcador y fecha de publicación.
2. **Bracket:** tabla con fase, fecha, equipos, ganador y estado.
3. **Partidas:** tabla con fase, fecha, equipos, marcador, ganador y estado.

No incluye formularios, botones de escritura ni enlaces a acciones internas. Si no hay torneo, muestra un estado vacío; si no hay anuncios, un mensaje informativo; si una partida no tiene resultado, muestra «Sin resultado».

### 3. Menú desplegable compartido en `base.html`

- La barra superior es blanca, con borde inferior, la marca a la izquierda y un botón de menú (☰) a la derecha, de 48 × 48 px.
- El botón despliega bajo la barra, alineado a la derecha, un menú con dos grupos:
  - **Navegación:** Inicio y Bracket.
  - **Entrar como:** tres botones (Jugador, Moderador y Organizador); al pulsar uno se despliega la lista de personas de ese rol y se cierra la anterior.
- El menú se cierra con la X, con `Esc` o con un clic fuera. Al cerrarse, el foco vuelve al botón de menú.
- No hay fondo oscurecido: el desplegable se superpone al contenido con una sombra suave.
- En escritorio mide 360 px; en pantallas pequeñas ocupa todo el ancho.
- La página activa se marca con `aria-current="page"` y una barra lateral de color.
- Se respeta `prefers-reduced-motion` para desactivar la transición.

### 4. Datos de los roles en todas las plantillas

- En `crear_app` se registra un `context_processor` de Jinja2 que consulta `persona` y devuelve:
  - `nav_jugadores`: id, nombre y equipo.
  - `nav_moderadores`: id y nombre.
  - `nav_organizador`: id y nombre del primer Organizador.
- Así el panel funciona en cualquier página sin repetir la consulta en cada ruta.
- Si no hay datos, el panel muestra el aviso de ejecutar `python -m app.db.seed`.

### 5. Accesibilidad y leyes de UX aplicadas

- **Fitts:** botón de 48 × 48 px pegado al borde derecho; enlaces con padding amplio.
- **Hick:** dos grupos y pocas opciones por grupo.
- **Jakob:** patrón conocido de hamburguesa + menú desplegable.
- **Proximidad:** navegación separada de los accesos de rol.
- **Von Restorff:** la página activa se resalta.
- **Aesthetic-Usability:** el panel usa los mismos colores, radios y tipografía del resto de la aplicación.
- El botón tiene `aria-label`, `aria-expanded` y `aria-controls`; el panel usa `aria-hidden` e `inert` cuando está cerrado.

### 6. JavaScript sin dependencias

Un bloque pequeño al final de `base.html`:

- Abre y cierra el panel.
- Despliega las listas de Jugador, Moderador y Organizador de a una por vez.
- Sincroniza `aria-expanded`, `aria-hidden` e `inert`.
- Cierra con `Esc`, con el fondo y con la X.
- Bloquea el desplazamiento del cuerpo mientras el panel está abierto.
- Devuelve el foco al botón de menú al cerrar.

No se agrega ninguna biblioteca ni archivo estático externo.

## Data flow

```text
GET /
  -> abrir_conexion()
  -> torneo (primero por id)
  -> listar_bracket(torneo)
  -> anuncios_por_partida()
  -> formatear fechas
  -> torneo.html

GET /torneo
  -> redirección 307 a /

Cualquier plantilla
  -> context_processor
  -> persona (Jugador / Moderador / Organizador)
  -> base.html (menú desplegable)
```

## Risks and trade-offs

- El `context_processor` ejecuta entre una y tres consultas pequeñas por render. Para SQLite y los datos de ejemplo es aceptable; si el número de personas crece, se puede cachear o mover a un servicio.
- Las interacciones del panel (abrir, cerrar, foco) no se pueden probar con `TestClient`; las pruebas verifican el marcado y el script, y la guía pide comprobarlas en el navegador.
- La página pública y el bracket interno comparten la misma fuente de datos; si en el futuro el bracket cambia de formato, ambas vistas deben actualizarse juntas.
- No hay migraciones: la historia solo lee tablas existentes.

## Files

- `app/rutas/torneo.py` (nuevo)
- `app/fabrica.py`
- `app/rutas/disponibilidad.py`
- `app/templates/base.html`
- `app/templates/torneo.html` (nuevo)
- `tests/test_hu07.py` (nuevo)
- `README.md`
