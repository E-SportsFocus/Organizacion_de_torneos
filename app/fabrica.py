from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.db.conexion import RUTA_DB_POR_DEFECTO, aplicar_migraciones, conectar
from app.rutas import cambio_horario, disponibilidad, organizador, resultado, torneo

DIRECTORIO_PLANTILLAS = Path(__file__).resolve().parent / "templates"


def crear_app(ruta_db=None, reloj=None, discord=None):
    ruta = Path(ruta_db) if ruta_db else RUTA_DB_POR_DEFECTO
    conexion_inicial = conectar(ruta)
    aplicar_migraciones(conexion_inicial)
    conexion_inicial.close()

    @contextmanager
    def abrir_conexion():
        conexion = conectar(ruta)
        try:
            yield conexion
        finally:
            conexion.close()

    def contexto_navegacion(request):
        """Datos del menú lateral comunes a todas las plantillas."""
        with abrir_conexion() as conexion:
            jugadores = [
                dict(fila)
                for fila in conexion.execute(
                    """
                    SELECT p.id, p.nombre, e.nombre AS equipo
                    FROM persona p
                    JOIN equipo e ON e.id = p.equipo_id
                    WHERE p.tipo = 'Jugador'
                    ORDER BY e.nombre, p.nombre
                    """
                )
            ]
            moderadores = [
                dict(fila)
                for fila in conexion.execute(
                    """
                    SELECT id, nombre
                    FROM persona
                    WHERE tipo = 'Moderador'
                    ORDER BY nombre
                    """
                )
            ]
            organizador = conexion.execute(
                """
                SELECT id, nombre
                FROM persona
                WHERE tipo = 'Organizador'
                ORDER BY id
                LIMIT 1
                """
            ).fetchone()
        return {
            "nav_jugadores": jugadores,
            "nav_moderadores": moderadores,
            "nav_organizador": dict(organizador) if organizador else None,
        }

    templates = Jinja2Templates(
        directory=str(DIRECTORIO_PLANTILLAS),
        context_processors=[contexto_navegacion],
    )

    aplicacion = FastAPI(title="E-Sports Focus — Organización de torneos")
    aplicacion.include_router(
        disponibilidad.crear_router(templates, abrir_conexion, reloj or datetime.now)
    )
    aplicacion.include_router(
        cambio_horario.crear_router(
            abrir_conexion, reloj or datetime.now, discord=discord, templates=templates
        )
    )
    aplicacion.include_router(
        resultado.crear_router(
            templates, abrir_conexion, reloj or datetime.now, discord=discord
        )
    )
    aplicacion.include_router(
        organizador.crear_router(templates, abrir_conexion, reloj=reloj or datetime.now)
    )
    aplicacion.include_router(
        torneo.crear_router(templates, abrir_conexion)
    )
    return aplicacion
