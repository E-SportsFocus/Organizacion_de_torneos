"""Pruebas de aceptación para HU-09: Creación y gestión de torneos, participantes y premios."""

import pytest
from app.servicios import torneo_gestion as servicio


def test_creacion_torneo_con_datos_validos(base, ahora):
    """HU-09 · Escenario: Registro exitoso de un nuevo torneo con sus datos generales"""
    datos, ruta = base
    organizador = datos.organizador("Olga Organización")

    torneo_id = servicio.crear_o_actualizar_torneo(
        datos.conexion,
        organizador_id=organizador,
        nombre="Torneo Relámpago CS2",
        juego="Counter-Strike 2",
        fecha_inicio="2026-11-25T18:00",
        zona_horaria="America/Santiago",
        descripcion="Torneo rápido de fin de semana",
        estado="Inscripciones abiertas",
        bolsa_premios="$1.000 USD",
        ahora=ahora,
    )

    fila = datos.conexion.execute(
        "SELECT * FROM torneo WHERE id = ?", (torneo_id,)
    ).fetchone()

    assert fila is not None
    assert fila["nombre"] == "Torneo Relámpago CS2"
    assert fila["juego"] == "Counter-Strike 2"
    assert fila["zona_horaria"] == "America/Santiago"
    assert fila["estado"] == "Inscripciones abiertas"
    assert fila["bolsa_premios"] == "$1.000 USD"
    assert fila["organizador_id"] == organizador


def test_asignacion_e_inscripcion_de_equipos_participantes(base, ahora):
    """HU-09 · Escenario: Asignación e inscripción de equipos participantes"""
    datos, ruta = base
    organizador = datos.organizador("Olga Organización")
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")

    torneo_id = servicio.crear_o_actualizar_torneo(
        datos.conexion,
        organizador_id=organizador,
        nombre="Copa Apertura",
        juego="Valorant",
        fecha_inicio="2026-11-24T15:00",
        equipos_ids=[alfa, bravo],
        ahora=ahora,
    )

    inscritos = servicio.obtener_equipos_inscritos(datos.conexion, torneo_id)
    assert len(inscritos) == 2
    nombres = {e["nombre"] for e in inscritos}
    assert "Equipo Alfa" in nombres
    assert "Equipo Bravo" in nombres


def test_definicion_y_desglose_de_estructura_de_premios(base, ahora):
    """HU-09 · Escenario: Definición y desglose de la estructura de premios"""
    datos, ruta = base
    organizador = datos.organizador("Olga Organización")

    premios = [
        {
            "posicion": 1,
            "posicion_texto": "1.º Lugar (Campeón)",
            "monto_texto": "$500 USD + Trofeo",
            "descripcion": "Premio al campeón",
        },
        {
            "posicion": 2,
            "posicion_texto": "2.º Lugar",
            "monto_texto": "$250 USD",
            "descripcion": "Premio al subcampeón",
        },
        {
            "posicion": 3,
            "posicion_texto": "3.º Lugar",
            "monto_texto": "$100 USD",
            "descripcion": "Tercer puesto",
        },
    ]

    torneo_id = servicio.crear_o_actualizar_torneo(
        datos.conexion,
        organizador_id=organizador,
        nombre="Copa de Maestros",
        juego="Valorant",
        fecha_inicio="2026-11-26T20:00",
        premios=premios,
        ahora=ahora,
    )

    premios_db = servicio.obtener_premios_torneo(datos.conexion, torneo_id)
    assert len(premios_db) == 3
    assert premios_db[0]["posicion"] == 1
    assert premios_db[0]["monto_texto"] == "$500 USD + Trofeo"
    assert premios_db[1]["posicion"] == 2
    assert premios_db[1]["monto_texto"] == "$250 USD"
    assert premios_db[2]["posicion"] == 3
    assert premios_db[2]["monto_texto"] == "$100 USD"


def test_validacion_campos_obligatorios_torneo(base, ahora):
    """HU-09 · Escenario: Validación de campos obligatorios al registrar el torneo"""
    datos, ruta = base
    organizador = datos.organizador("Olga Organización")

    with pytest.raises(servicio.ErrorGestionTorneo) as exc_vacio:
        servicio.crear_o_actualizar_torneo(
            datos.conexion,
            organizador_id=organizador,
            nombre="",
            juego="Valorant",
            fecha_inicio="2026-11-24T10:00",
        )
    assert "nombre del torneo es obligatorio" in exc_vacio.value.mensaje.lower()

    with pytest.raises(servicio.ErrorGestionTorneo) as exc_corto:
        servicio.crear_o_actualizar_torneo(
            datos.conexion,
            organizador_id=organizador,
            nombre="ab",
            juego="Valorant",
            fecha_inicio="2026-11-24T10:00",
        )
    assert "al menos 3 caracteres" in exc_corto.value.mensaje.lower()


def test_actualizacion_de_torneo_y_premios_existentes(base, ahora):
    """HU-09 · Actualización de un torneo ya existente conservando integridad"""
    datos, ruta = base
    organizador = datos.organizador("Olga Organización")

    torneo_id = servicio.crear_o_actualizar_torneo(
        datos.conexion,
        organizador_id=organizador,
        nombre="Copa Inicial",
        juego="Valorant",
        fecha_inicio="2026-11-24T10:00",
        bolsa_premios="$500 USD",
        premios=[
            {
                "posicion": 1,
                "posicion_texto": "1.º Lugar",
                "monto_texto": "$500 USD",
                "descripcion": "",
            }
        ],
        ahora=ahora,
    )

    # Actualizar a nuevos valores
    servicio.crear_o_actualizar_torneo(
        datos.conexion,
        organizador_id=organizador,
        torneo_id=torneo_id,
        nombre="Copa Inicial Renovada",
        juego="Valorant",
        fecha_inicio="2026-11-24T12:00",
        bolsa_premios="$800 USD",
        premios=[
            {
                "posicion": 1,
                "posicion_texto": "1.º Lugar",
                "monto_texto": "$600 USD",
                "descripcion": "Actualizado",
            },
            {
                "posicion": 2,
                "posicion_texto": "2.º Lugar",
                "monto_texto": "$200 USD",
                "descripcion": "Nuevo premio",
            },
        ],
        ahora=ahora,
    )

    fila = datos.conexion.execute(
        "SELECT * FROM torneo WHERE id = ?", (torneo_id,)
    ).fetchone()
    assert fila["nombre"] == "Copa Inicial Renovada"
    assert fila["bolsa_premios"] == "$800 USD"

    premios_db = servicio.obtener_premios_torneo(datos.conexion, torneo_id)
    assert len(premios_db) == 2
    assert premios_db[0]["monto_texto"] == "$600 USD"
    assert premios_db[1]["monto_texto"] == "$200 USD"
