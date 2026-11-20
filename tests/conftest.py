from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.db.conexion import aplicar_migraciones, conectar
from app.fabrica import crear_app

AHORA = datetime(2026, 11, 17, 12, 0, 0)


class DatosDePrueba:
    def __init__(self, conexion):
        self.conexion = conexion

    def equipo(self, nombre, pais="Colombia"):
        cursor = self.conexion.execute(
            "INSERT INTO equipo (nombre, pais) VALUES (?, ?)", (nombre, pais)
        )
        self.conexion.commit()
        return cursor.lastrowid

    def persona(self, nombre, tipo, equipo_id=None, nickname=None):
        cursor = self.conexion.execute(
            """
            INSERT INTO persona (nombre, cuenta_discord, tipo, nickname, pais, equipo_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nombre, nombre.lower().replace(" ", "_"), tipo, nickname, "Colombia", equipo_id),
        )
        self.conexion.commit()
        return cursor.lastrowid

    def jugador(self, nombre, equipo_id):
        return self.persona(nombre, "Jugador", equipo_id=equipo_id, nickname=nombre.lower())

    def moderador(self, nombre="Moderador de prueba"):
        return self.persona(nombre, "Moderador")

    def organizador(self, nombre="Organizador de prueba"):
        return self.persona(nombre, "Organizador")

    def torneo(self, nombre="Torneo de prueba"):
        cursor = self.conexion.execute(
            "INSERT INTO torneo (nombre, juego, zona_horaria) VALUES (?, ?, ?)",
            (nombre, "Valorant", "America/Bogota"),
        )
        self.conexion.commit()
        return cursor.lastrowid

    def partida(self, torneo_id, moderador_id, fecha_hora, equipos, estado="Programada", fase="Fase de prueba"):
        cursor = self.conexion.execute(
            """
            INSERT INTO partida (torneo_id, moderador_id, fecha_hora, fase, estado)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                torneo_id,
                moderador_id,
                fecha_hora.isoformat(timespec="minutes"),
                fase,
                estado,
            ),
        )
        partida_id = cursor.lastrowid
        for equipo_id in equipos:
            self.conexion.execute(
                "INSERT INTO disponibilidad (equipo_id, partida_id) VALUES (?, ?)",
                (equipo_id, partida_id),
            )
        self.conexion.commit()
        return partida_id

    def disponibilidad(self, partida_id, equipo_id):
        return self.conexion.execute(
            "SELECT * FROM disponibilidad WHERE partida_id = ? AND equipo_id = ?",
            (partida_id, equipo_id),
        ).fetchone()

    def marcar_confirmada(self, partida_id, equipo_id, fecha):
        self.conexion.execute(
            """
            UPDATE disponibilidad
            SET confirmada = 'Confirmada', fecha_confirmacion = ?
            WHERE partida_id = ? AND equipo_id = ?
            """,
            (fecha.isoformat(timespec="seconds"), partida_id, equipo_id),
        )
        self.conexion.commit()


@pytest.fixture
def ahora():
    return AHORA


@pytest.fixture
def base(tmp_path):
    ruta = tmp_path / "prueba.db"
    conexion = conectar(ruta)
    aplicar_migraciones(conexion)
    datos = DatosDePrueba(conexion)
    yield datos, ruta
    conexion.close()


@pytest.fixture
def cliente(base):
    datos, ruta = base
    aplicacion = crear_app(ruta_db=ruta, reloj=lambda: AHORA)
    with TestClient(aplicacion) as cliente_http:
        yield cliente_http, datos
