import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DIRECTORIO_MIGRACIONES = Path(__file__).resolve().parent / "migrations"
RUTA_DB_POR_DEFECTO = Path(__file__).resolve().parents[2] / "data" / "app.db"


def conectar(ruta=None):
    ruta = Path(ruta) if ruta else RUTA_DB_POR_DEFECTO
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def aplicar_migraciones(conexion):
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            nombre TEXT PRIMARY KEY,
            aplicada_en TEXT NOT NULL
        )
        """
    )
    conexion.commit()
    aplicadas = {
        fila["nombre"]
        for fila in conexion.execute("SELECT nombre FROM schema_migrations")
    }
    for archivo in sorted(DIRECTORIO_MIGRACIONES.glob("*.sql")):
        if archivo.name in aplicadas:
            continue
        conexion.executescript(archivo.read_text(encoding="utf-8"))
        conexion.execute(
            "INSERT INTO schema_migrations (nombre, aplicada_en) VALUES (?, ?)",
            (archivo.name, datetime.now(timezone.utc).isoformat(timespec="seconds")),
        )
        conexion.commit()


def preparar_base(ruta=None):
    conexion = conectar(ruta)
    aplicar_migraciones(conexion)
    return conexion
