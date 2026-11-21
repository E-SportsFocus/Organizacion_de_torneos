# Proyecto de E-Sports Focus

- [Ingeniería de requisitos - Entrega 1](IngReq-Entrega1.md)
- [Ingeniería de requisitos - Entrega 2](./IngReq-Entrega%202.md)

## Aplicación web (HU-03, HU-04, HU-06 y HU-07)

Aplicación web sencilla en Python (FastAPI + Jinja2 + SQLite) generada desde la documentación de requisitos. Historias implementadas:

- **HU-04 — Confirmación de disponibilidad** (CU-01).
- **HU-03 — Registro manual del resultado** (CU-04): resultado, bracket con historial y notificación simulada.
- **HU-06 — Anuncio automático del ganador** (CU-06): publicación en la plataforma, anuncio simulado en Discord y pantalla del Organizador.
- **HU-07 — Inicio público del torneo** (CU-07): anuncios, bracket y partidas de solo lectura en la página de inicio, con un menú lateral común para navegar y cambiar de rol de demostración.

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

Carga 1 torneo, 4 equipos de 2 jugadores, 2 moderadores (Marta Arbitraje y Óscar Réplica), 1 organizador (Olga Organización) y 6 partidas:

1. Alfa vs Bravo, en 6 horas, `Programada`.
2. Charlie vs Delta, en 30 horas, `Programada`.
3. Alfa vs Delta, hace 1 hora, `Programada`.
4. Alfa vs Charlie, hace 2 horas, `En curso`.
5. Bravo vs Delta, hace 1 día, `Anunciada`, con resultado sembrado 2–1, su actualización de bracket y su anuncio enviado a Discord.
6. Bravo vs Charlie, hace 3 horas, `Pendiente de resultado` (la que se registra en HU-03 y HU-06).

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
2. En la semifinal **Bravo vs Charlie**, que está `Pendiente de resultado`, escribe el marcador de ambos equipos y pulsa **Registrar resultado**.
3. La partida pasa a `Anunciada` y aparece «Resultado registrado. Ganador: … El bracket fue actualizado. El ganador quedó anunciado.».
4. Abre **Bracket** en el menú lateral: verás el marcador, el ganador y el historial de actualizaciones, incluida la final sembrada 2–1.
5. Entra como **Óscar Réplica** (Moderador no asignado): la partida pendiente no muestra el formulario, sino la nota de que solo el Moderador asignado puede registrarla.
6. El resultado solo admite marcadores enteros mayores o iguales a 0 y **no admite empate**; un envío incompleto o empatado no modifica la partida.

La notificación al Organizador y a los Jugadores se guarda en la tabla `notificacion`, el anuncio y su estado de envío en la tabla `anuncio`, y las llamadas a Discord se simulan en `integraciones_log`: no hay integración real con Discord ni con la API del videojuego.

### Recorrido de HU-06 (anuncio del ganador)

1. Abre el menú **☰** y elige **Olga Organización** en **Entrar como** (Organizador).
2. Verás la sección **Anuncios** con la final sembrada: **Equipo Bravo** ganó 2–1, publicada en la plataforma y con **Discord enviado**.
3. Las partidas sin resultado aparecen como «Todavía no hay un ganador que anunciar» y «Falta registrar el resultado».
4. Registra la semifinal **Bravo vs Charlie** como **Marta Arbitraje**: la partida pasa a `Anunciada` y el anuncio aparece en el panel del Organizador y en el bracket.
5. Si Discord no responde, el ganador igual queda publicado y el anuncio figura como **pendiente de envío**; las pruebas simulan ese fallo.

### Recorrido de HU-07 (inicio público y menú lateral)

1. Abre <http://localhost:8000>: el inicio ya muestra el torneo, sin pasar por ningún botón.
2. Verás el nombre y el juego del torneo, la marca **Vista pública · solo lectura**, los **Anuncios de ganadores**, el **Bracket** y la tabla de **Partidas**.
3. La final sembrada aparece como ganadora; la semifinal pendiente muestra **Sin resultado** y no inventa un ganador.
4. Pulsa el botón **☰** de la derecha: el panel se abre desde la derecha con **Navegación** (Inicio y Bracket) y **Entrar como** (los 8 jugadores agrupados por equipo, los 2 moderadores y la organizadora).
5. Elige un jugador, un moderador o la organizadora; entrarás a su vista. Cierra el panel con la **X**, con **Esc** o tocando fuera.
6. La página pública no tiene formularios ni botones para registrar resultados o anunciar ganadores: es solo de lectura.
7. El enlace anterior `/torneo` redirige al inicio, así que no se rompe si lo tenías guardado.

Las 5 pruebas de `tests/test_hu03.py` corresponden a los 5 escenarios Gherkin de `07-criterios-aceptacion.md`, las 4 de `tests/test_hu04.py` a los escenarios de HU-04, las 3 de `tests/test_hu06.py` a los escenarios de HU-06 y las 4 de `tests/test_hu07.py` a los escenarios de HU-07. En total son 33 pruebas.
