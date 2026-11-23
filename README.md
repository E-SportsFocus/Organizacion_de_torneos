# Proyecto de E-Sports Focus

- [Ingeniería de requisitos - Entrega 1](IngReq-Entrega1.md)
- [Ingeniería de requisitos - Entrega 2](./IngReq-Entrega%202.md)

## Aplicación web (HU-03, HU-04, HU-05, HU-06, HU-07 y HU-08)

Aplicación web sencilla en Python (FastAPI + Jinja2 + SQLite) generada desde la documentación de requisitos. Historias implementadas:

- **HU-04 — Confirmación de disponibilidad** (CU-01).
- **HU-05 — Solicitud de cambio de horario** (CU-02): solicitud de reprogramación con más de 2 horas de anticipación, resolución por el Moderador (aprobar o rechazar con motivo) y aviso simulado en Discord.
- **HU-03 — Registro manual del resultado** (CU-04): resultado, bracket con historial y notificación simulada.
- **HU-06 — Anuncio automático del ganador** (CU-06): publicación en la plataforma, anuncio simulado en Discord y pantalla del Organizador.
- **HU-07 — Inicio público del torneo** (CU-07): anuncios y bracket resumido de solo lectura en la página de inicio (con enlace al detalle de partidas en `/bracket`), con un menú desplegable común para navegar y cambiar de rol de demostración.
- **HU-08 — Visualización gráfica del Bracket del torneo** (CU-08): árbol interactivo de llaves tipo esport (Liquipedia/VLR) organizado por columnas de rondas secuenciales, con marcadores individuales, destaque del equipo ganador, estado claro para partidas pendientes y coexistencia con la tabla de auditoría (RP-10).

### Requisitos

Python 3.11 o superior.

### Instalar

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Crear la base y los datos de ejemplo

Si ya existe una base de una versión anterior, bórrala para cargar los datos nuevos:

```powershell
Remove-Item data\app.db -ErrorAction SilentlyContinue
python -m app.db.seed
```

Carga 1 torneo ("Copa E-Sports Focus"), 8 equipos de 2 jugadores, 2 moderadores (Marta Arbitraje y Óscar Réplica), 1 organizador (Olga Organización) y las 4 llaves iniciales de **Cuartos de final** en simulación real:

1. Alfa vs Bravo (`Programada`, disponibilidad `Pendiente`).
2. Charlie vs Delta (`Programada`, disponibilidad `Pendiente`).
3. Eco vs Foxtrot (`Programada`, disponibilidad `Pendiente`).
4. Golf vs Hotel (`Programada`, disponibilidad `Pendiente`).

**Flujo de simulación real:**

1. Los **Jugadores** confirman la disponibilidad de su equipo (HU-04) o solicitan un cambio de horario (HU-05).
2. Cuando **ambos equipos** de una partida confirman disponibilidad, la partida pasa automáticamente de `Programada` a `Pendiente de resultado`.
3. El **Moderador** registra el marcador oficial (HU-03) → la partida pasa a `Anunciada` y el ganador se anuncia (HU-06).
4. El equipo ganador avanza dinámicamente a la siguiente fase (**Semifinal** o **Final**) con disponibilidad `Pendiente`, debiendo confirmar nuevamente.
5. El ciclo se repite hasta coronar al campeón.

No hay resultados predeterminados ni fases precreadas: las **Semifinales** y la **Final** se construyen dinámicamente a medida que el Moderador registra los resultados.

Es idempotente: si ya hay datos, no los duplica.

### Ejecutar

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

También puedes activar el entorno con `.venv\Scripts\Activate.ps1` y usar `uvicorn app.main:app --reload`. Abre <http://localhost:8000>.

### Probar

```powershell
pytest
```

### Recorrido de HU-04 (disponibilidad)

1. Abre el menú **☰** y elige un jugador en **Entrar como** (por ejemplo, Ana Ríos del Equipo Alfa).
2. Verás las partidas del equipo con su disponibilidad. Pulsa **Confirmar disponibilidad** en una partida `Programada` y `Pendiente`; aparecerá el aviso «Disponibilidad del equipo confirmada.».
3. En una partida ya iniciada o finalizada no aparece el botón; si se envía el formulario, responde «La partida ya inició o finalizó; el plazo para confirmar la disponibilidad venció.».
4. Entra como **Moderador** para ver la disponibilidad de ambos equipos y la marca «Requiere revisión» cuando faltan 8 horas o menos y algún equipo sigue pendiente.

### Recorrido de HU-03 (registro manual del resultado)

1. Abre el menú **☰** y entra como **Marta Arbitraje** (Moderador asignado a las partidas).
2. Para registrar un resultado, primero ambos equipos deben confirmar disponibilidad (HU-04). Cuando lo hagan, la partida pasará de `Programada` a `Pendiente de resultado`.
3. En una partida `Pendiente de resultado`, escribe el marcador de ambos equipos y pulsa **Registrar resultado**.
4. La partida pasa a `Anunciada` y aparece «Resultado registrado. Ganador: … El bracket fue actualizado. El ganador quedó anunciado.».
5. Abre **Bracket** en el menú desplegable: verás el marcador, el ganador y el historial de actualizaciones. El equipo ganador avanza a la siguiente fase con disponibilidad `Pendiente`.
6. Entra como **Óscar Réplica** (Moderador no asignado): la partida pendiente no muestra el formulario, sino la nota de que solo el Moderador asignado puede registrarla.
7. El resultado solo admite marcadores enteros mayores o iguales a 0 y **no admite empate**; un envío incompleto o empatado no modifica la partida.

La notificación al Organizador y a los Jugadores se guarda en la tabla `notificacion`, el anuncio y su estado de envío en la tabla `anuncio`, y las llamadas a Discord se simulan en `integraciones_log`: no hay integración real con Discord ni con la API del videojuego.

### Recorrido de HU-05 (solicitud de cambio de horario)

1. Abre el menú **☰** y entra como **Ana Ríos** (Equipo Alfa) o **Elena Gómez** (Equipo Charlie).
2. En las partidas programadas donde falten más de 2 horas para el inicio, despliega «Solicitar cambio de horario», selecciona un nuevo horario propuesto y pulsa «Enviar solicitud».
3. Si la partida inicia en 2 horas o menos, el sistema rechaza la solicitud e informa que el plazo ya venció.
4. Entra como **Marta Arbitraje** (Moderador asignado): en la sección «Solicitudes de cambio de horario» verás la solicitud del equipo.
5. Puedes pulsar **Aprobar** (la partida se reprograma con el nuevo horario y se avisa a Discord) o desplegar **Rechazar...** e indicar un motivo obligatorio (la partida conserva su horario original).
6. Si una solicitud queda sin decisión y se alcanza el plazo límite de 2 horas antes de la partida, la solicitud vence automáticamente y la partida conserva su horario.

### Recorrido de HU-06 (anuncio del ganador)

1. Abre el menú **☰** y elige **Olga Organización** en **Entrar como** (Organizador).
2. Verás la sección **Anuncios** con los ganadores de partidas que ya tengan resultado registrado y publicado en la plataforma con **Discord enviado**.
3. Las partidas sin resultado aparecen como «Todavía no hay un ganador que anunciar» y «Falta registrar el resultado».
4. Cuando el Moderador registra un resultado, la partida pasa a `Anunciada` y el anuncio aparece en el panel del Organizador y en el bracket.
5. Si Discord no responde, el ganador igual queda publicado y el anuncio figura como **pendiente de envío**; las pruebas simulan ese fallo.

### Recorrido de HU-07 (inicio público y menú desplegable)

1. Abre <http://localhost:8000>: el inicio ya muestra el torneo, sin pasar por ningún botón.
2. Verás el nombre y el juego del torneo, la marca **Vista pública · solo lectura**, los **Anuncios de ganadores**, el **Bracket** resumido y el enlace hacia el detalle de partidas en `/bracket`.
3. Las partidas con resultado muestran el ganador; las partidas pendientes muestran **Sin resultado** y no inventan un ganador.
4. Pulsa el botón **☰** de la derecha: el menú se despliega bajo la barra, alineado a la derecha, con **Navegación** (Inicio y Bracket) y **Entrar como**, que muestra tres botones: **Jugador**, **Moderador** y **Organizador**.
5. Pulsa uno de los tres botones para desplegar la lista de personas de ese rol (solo una lista a la vez). Elige una persona y entrarás a su vista. Cierra el menú con la **X**, con **Esc** o tocando fuera.
6. La página pública no tiene formularios ni botones para registrar resultados o anunciar ganadores: es solo de lectura.
7. El enlace anterior `/torneo` redirige al inicio, así que no se rompe si lo tenías guardado.

### Recorrido de HU-08 (bracket gráfico)

1. Abre el menú **☰** y pulsa **Bracket** (o accede directamente a <http://localhost:8000/bracket>).
2. Verás la tarjeta principal **Árbol visual de llaves** con la estructura de fases en columnas horizontales. Inicialmente solo aparecen los **Cuartos de final** en estado `Programada`.
3. Cada enfrentamiento se presenta en una tarjeta de llave con fecha, estado en chip y dos casillas para los equipos con sus casillas individuales de marcador.
4. A medida que los jugadores confirman disponibilidad y el moderador registra resultados, las **Semifinales** y la **Final** se van construyendo dinámicamente en el árbol.
5. En las partidas con resultado confirmado, el equipo ganador aparece resaltado visualmente en verde suave con su marcador destacado y la indicación de que avanza a la siguiente ronda.
6. En las partidas pendientes o programadas, las casillas muestran su estado de espera sin asignar un ganador prematuro.
7. Debajo del árbol visual, se mantiene accesible la tabla detallada de **Partidas** y el **Historial de actualizaciones** con la auditoría cronológica de moderación (cumpliendo RP-10).

Las 5 pruebas de `tests/test_hu03.py` corresponden a los 5 escenarios Gherkin de `07-criterios-aceptacion.md`, las 4 de `tests/test_hu04.py` a los escenarios de HU-04, las 5 de `tests/test_hu05.py` a los escenarios de HU-05, las 3 de `tests/test_hu06.py` a los escenarios de HU-06, las 4 de `tests/test_hu07.py` a los escenarios de HU-07 y las 5 de `tests/test_hu08.py` a los escenarios y avance dinámico de HU-08. En total son 43 pruebas.
