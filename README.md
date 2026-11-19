# Proyecto de E-Sports Focus

- [Ingeniería de requisitos - Entrega 1](IngReq-Entrega1.md)
- [Ingeniería de requisitos - Entrega 2](./IngReq-Entrega%202.md)

## Aplicación web (HU-04 — Confirmación de disponibilidad)

Aplicación web sencilla en Python (FastAPI + Jinja2 + SQLite) generada desde la documentación de requisitos. Historia implementada: **HU-04 — Confirmación de disponibilidad** (CU-01).

### Requisitos

Python 3.11 o superior.

### Instalar

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Crear la base y los datos de ejemplo

```powershell
python -m app.db.seed
```

Carga 1 torneo, 4 equipos de 2 jugadores, 1 moderador y 4 partidas: una en 6 horas, una en 30 horas, una iniciada hace 1 hora y una finalizada. Es idempotente: si ya hay datos, no los duplica.

### Ejecutar

```powershell
uvicorn app.main:app --reload
```

Abre <http://localhost:8000>.

### Probar

```powershell
pytest
```

### Recorrido de la historia

1. En **Inicio**, entra como un jugador (por ejemplo, Ana Ríos del Equipo Alfa).
2. Verás las partidas del equipo con su disponibilidad. Pulsa **Confirmar disponibilidad** en una partida `Programada` y `Pendiente`; aparecerá el aviso «Disponibilidad del equipo confirmada.».
3. En una partida ya iniciada o finalizada no aparece el botón; si se envía el formulario, responde «La partida ya inició o finalizó; el plazo para confirmar la disponibilidad venció.».
4. Entra como **Moderador** para ver la disponibilidad de ambos equipos y la marca «Requiere revisión» cuando faltan 8 horas o menos y algún equipo sigue pendiente.

Las 4 pruebas de `tests/test_hu04.py` corresponden a los 4 escenarios Gherkin de `07-criterios-aceptacion.md`.
