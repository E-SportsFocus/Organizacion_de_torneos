# Proyecto de E-Sports Focus

- [Ingeniería de requisitos - Entrega 1](IngReq-Entrega1.md)
- [Ingeniería de requisitos - Entrega 2](./IngReq-Entrega%202.md)

## Aplicación web (HU-03 y HU-04)

Aplicación web sencilla en Python (FastAPI + Jinja2 + SQLite) generada desde la documentación de requisitos. Historias implementadas:

- **HU-04 — Confirmación de disponibilidad** (CU-01).
- **HU-03 — Registro manual del resultado** (CU-04): resultado, bracket con historial y notificación simulada.

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
5. Bravo vs Delta, hace 1 día, `Anunciada`, con resultado sembrado 2–1 y su actualización de bracket.
6. Bravo vs Charlie, hace 3 horas, `Pendiente de resultado` (la que se registra en HU-03).

Es idempotente: si ya hay datos, no los duplica.

### Ejecutar

```powershell
uvicorn app.main:app --reload
```

Abre <http://localhost:8000>.

### Probar

```powershell
pytest
```

### Recorrido de HU-04 (disponibilidad)

1. En **Inicio**, entra como un jugador (por ejemplo, Ana Ríos del Equipo Alfa).
2. Verás las partidas del equipo con su disponibilidad. Pulsa **Confirmar disponibilidad** en una partida `Programada` y `Pendiente`; aparecerá el aviso «Disponibilidad del equipo confirmada.».
3. En una partida ya iniciada o finalizada no aparece el botón; si se envía el formulario, responde «La partida ya inició o finalizó; el plazo para confirmar la disponibilidad venció.».
4. Entra como **Moderador** para ver la disponibilidad de ambos equipos y la marca «Requiere revisión» cuando faltan 8 horas o menos y algún equipo sigue pendiente.

### Recorrido de HU-03 (registro manual del resultado)

1. En **Inicio**, entra como **Marta Arbitraje** (Moderador asignado a las partidas).
2. En la semifinal **Bravo vs Charlie**, que está `Pendiente de resultado`, escribe el marcador de ambos equipos y pulsa **Registrar resultado**.
3. La partida pasa a `Resultado confirmado` y aparece «Resultado registrado. Ganador: … El bracket fue actualizado.».
4. Abre **Bracket** en la navegación: verás el marcador, el ganador y el historial de actualizaciones, incluida la final sembrada 2–1.
5. Entra como **Óscar Réplica** (Moderador no asignado): la partida pendiente no muestra el formulario, sino la nota de que solo el Moderador asignado puede registrarla.
6. El resultado solo admite marcadores enteros mayores o iguales a 0 y **no admite empate**; un envío incompleto o empatado no modifica la partida.

La notificación al Organizador y a los Jugadores se guarda en la tabla `notificacion` y la llamada a Discord se simula en `integraciones_log`: no hay integración real con Discord ni con la API del videojuego.

Las 5 pruebas de `tests/test_hu03.py` corresponden a los 5 escenarios Gherkin de `07-criterios-aceptacion.md` y las 4 de `tests/test_hu04.py` a los escenarios de HU-04.
