from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.db.conexion import RUTA_DB_POR_DEFECTO, aplicar_migraciones, conectar
from app.rutas.disponibilidad import crear_router

DIRECTORIO_PLANTILLAS = Path(__file__).resolve().parent / "templates"


def crear_app(ruta_db=None, reloj=None):
    ruta = Path(ruta_db) if ruta_db else RUTA_DB_POR_DEFECTO
    conexion_inicial = conectar(ruta)
    aplicar_migraciones(conexion_inicial)
    conexion_inicial.close()

    templates = Jinja2Templates(directory=str(DIRECTORIO_PLANTILLAS))

    @contextmanager
    def abrir_conexion():
        conexion = conectar(ruta)
        try:
            yield conexion
        finally:
            conexion.close()

    aplicacion = FastAPI(title="E-Sports Focus — Organización de torneos")
    aplicacion.include_router(
        crear_router(templates, abrir_conexion, reloj or datetime.now)
    )
    return aplicacion
