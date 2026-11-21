# Tasks

## 1. Inicio público del torneo

- [x] 1.1 Crear `app/rutas/torneo.py` con `GET /`: tomar el primer torneo por `id`, reutilizar `listar_bracket` y `anuncios_por_partida`, y formatear las fechas; verificar que responde 200 y que devuelve un estado vacío si no hay torneo.
- [x] 1.2 Mantener `GET /torneo` como redirección 307 a `/` y registrar el router de torneo en `app/fabrica.py`; verificar que `/` está disponible en una app nueva.
- [x] 1.3 Retirar la vista de inicio de `app/rutas/disponibilidad.py` y la plantilla `index.html`, que ya no se usan.
- [x] 1.4 Crear `app/templates/torneo.html` con las secciones **Anuncios de ganadores**, **Bracket** y **Partidas**, sin formularios ni botones de escritura; verificar que una partida pendiente muestra «Sin resultado» y no un ganador.

## 2. Menú lateral compartido

- [x] 2.1 Reemplazar la navegación horizontal de `app/templates/base.html` por una barra con la marca a la izquierda y un botón de menú de 48 × 48 px a la derecha.
- [x] 2.2 Agregar el panel lateral derecho con **Navegación** (Inicio y Bracket) y **Entrar como** (Jugador, Moderador y Organizador), incluidos los estados vacíos si faltan datos de ejemplo.
- [x] 2.3 Agregar los estilos del panel: fondo oscurecido, transición desde la derecha, 320 px en escritorio, ancho completo en móvil, página activa resaltada y `prefers-reduced-motion`.
- [x] 2.4 Agregar el JavaScript de apertura y cierre: X, `Esc`, clic fuera, `aria-expanded`, `aria-hidden`, `inert`, bloqueo del desplazamiento y retorno del foco al botón.
- [x] 2.5 Registrar en `app/fabrica.py` un `context_processor` que inyecte `nav_jugadores`, `nav_moderadores` y `nav_organizador` en todas las plantillas; verificar que el panel funciona en Inicio, Jugador, Moderador, Organizador y Bracket.

## 3. Pruebas

- [x] 3.1 Agregar `tests/test_hu07.py` con el escenario «El visitante consulta el torneo público»: verificar nombre, juego, anuncios, bracket, partidas y ausencia de formularios en `/`, y que `/torneo` redirige a `/`.
- [x] 3.2 Agregar el escenario «Una partida sin resultado no muestra ganador»: verificar el estado pendiente y la ausencia de ganador.
- [x] 3.3 Agregar el escenario «El visitante abre el menú lateral y cambia de rol»: verificar el botón, el panel, la navegación (Inicio y Bracket) y los accesos de los tres roles.
- [x] 3.4 Agregar el escenario «El menú se cierra sin cambiar de página»: verificar la X, el fondo, el manejador de `Esc` y el estado inicial cerrado.
- [x] 3.5 Ejecutar `.venv\Scripts\python.exe -m pytest` y confirmar que las 29 pruebas existentes siguen pasando.

## 4. Documentación y cierre

- [x] 4.1 Actualizar `README.md` con el inicio público, la redirección de `/torneo`, el menú lateral y el recorrido de prueba de HU-07.
- [x] 4.2 Ejecutar `openspec.cmd validate --strict hu-07-pagina-torneo` y confirmar que el cambio es válido.
- [x] 4.3 Revisar manualmente el panel en el navegador: abrir con el botón, cerrar con X, `Esc` y clic fuera; comprobar el foco y el ancho en móvil.

## Workflow follow-up

- Sincronizar la capacidad `torneo-publico` después de la implementación.
- Archivar el cambio `hu-07-pagina-torneo` cuando el estudiante lo apruebe.
- Verificar el cambio archivado en `openspec/changes/archive/`.
