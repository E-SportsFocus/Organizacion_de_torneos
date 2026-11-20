from datetime import timedelta

from app.servicios import resultado as servicio


def _escenario(datos, ahora):
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    asignado = datos.moderador("Marta Arbitraje")
    otro = datos.moderador("Óscar Réplica")
    ana = datos.jugador("Ana Ríos", alfa)
    beto = datos.jugador("Beto Salas", bravo)
    organizador = datos.organizador("Olga Organización")
    torneo = datos.torneo()
    datos.conexion.execute(
        "UPDATE torneo SET organizador_id = ? WHERE id = ?", (organizador, torneo)
    )
    datos.conexion.commit()
    partida = datos.partida(
        torneo,
        asignado,
        ahora - timedelta(hours=2),
        [alfa, bravo],
        estado="Pendiente de resultado",
    )
    return {
        "alfa": alfa,
        "bravo": bravo,
        "asignado": asignado,
        "otro": otro,
        "ana": ana,
        "beto": beto,
        "organizador": organizador,
        "torneo": torneo,
        "partida": partida,
    }


def test_moderador_asignado_registra_el_resultado_completo(cliente, ahora):
    """HU-03 · Un Moderador asignado registra el resultado completo de una partida pendiente"""
    http, datos = cliente
    escenario = _escenario(datos, ahora)

    respuesta = http.post(
        f"/partidas/{escenario['partida']}/resultado",
        data={
            "persona_id": escenario["asignado"],
            f"marcador_{escenario['alfa']}": "2",
            f"marcador_{escenario['bravo']}": "1",
        },
    )

    assert respuesta.status_code == 200
    assert "Resultado registrado" in respuesta.text
    assert "Ganador: Equipo Alfa" in respuesta.text

    resultado = datos.conexion.execute(
        "SELECT * FROM resultado WHERE partida_id = ?", (escenario["partida"],)
    ).fetchone()
    assert resultado is not None
    assert resultado["moderador_id"] == escenario["asignado"]
    assert resultado["origen"] == "manual"
    assert resultado["fecha_hora_registro"] == ahora.isoformat(timespec="seconds")

    marcadores = {
        fila["equipo_id"]: fila["marcador"]
        for fila in datos.conexion.execute(
            "SELECT equipo_id, marcador FROM resultado_marcador WHERE resultado_id = ?",
            (resultado["id"],),
        )
    }
    assert marcadores == {escenario["alfa"]: 2, escenario["bravo"]: 1}

    partida = datos.conexion.execute(
        "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()
    assert partida["estado"] == "Anunciada"

    bracket = datos.conexion.execute(
        "SELECT * FROM bracket WHERE torneo_id = ?", (escenario["torneo"],)
    ).fetchone()
    assert bracket["ultima_actualizacion"] == ahora.isoformat(timespec="seconds")
    historial = datos.conexion.execute(
        "SELECT * FROM bracket_actualizacion WHERE bracket_id = ?", (bracket["id"],)
    ).fetchall()
    assert [fila["resultado_id"] for fila in historial] == [resultado["id"]]

    notificaciones = datos.conexion.execute(
        "SELECT destinatario_tipo, destinatario_id, mensaje FROM notificacion WHERE partida_id = ?",
        (escenario["partida"],),
    ).fetchall()
    destinatarios = {
        (fila["destinatario_tipo"], fila["destinatario_id"])
        for fila in notificaciones
    }
    assert destinatarios == {
        ("Organizador", escenario["organizador"]),
        ("Jugador", escenario["ana"]),
        ("Jugador", escenario["beto"]),
    }
    assert any("Equipo Alfa 2 - Equipo Bravo 1" in fila["mensaje"] for fila in notificaciones)

    log = datos.conexion.execute(
        "SELECT sistema, operacion FROM integraciones_log ORDER BY id"
    ).fetchall()
    assert [fila["operacion"] for fila in log] == [
        "notificar_resultado",
        "anunciar_ganador",
    ]
    assert all(fila["sistema"] == "Discord" for fila in log)

    bracket_html = http.get("/bracket")
    assert bracket_html.status_code == 200
    assert "Historial de actualizaciones" in bracket_html.text
    assert "Equipo Alfa 2 - Equipo Bravo 1" in bracket_html.text


def test_jugador_no_puede_registrar_un_resultado(cliente, ahora):
    """HU-03 · Un jugador no puede registrar un resultado"""
    http, datos = cliente
    escenario = _escenario(datos, ahora)

    respuesta = http.post(
        f"/partidas/{escenario['partida']}/resultado",
        data={
            "persona_id": escenario["ana"],
            f"marcador_{escenario['alfa']}": "2",
            f"marcador_{escenario['bravo']}": "1",
        },
    )

    assert respuesta.status_code == 400
    assert servicio.MENSAJE_SOLO_MODERADOR in respuesta.text
    assert (
        datos.conexion.execute(
            "SELECT COUNT(*) FROM resultado WHERE partida_id = ?",
            (escenario["partida"],),
        ).fetchone()[0]
        == 0
    )
    assert (
        datos.conexion.execute(
            "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
        ).fetchone()["estado"]
        == "Pendiente de resultado"
    )


def test_moderador_no_asignado_no_puede_registrar_el_resultado(cliente, ahora):
    """HU-03 · Un Moderador no asignado a la partida no puede registrar el resultado"""
    http, datos = cliente
    escenario = _escenario(datos, ahora)

    respuesta = http.post(
        f"/partidas/{escenario['partida']}/resultado",
        data={
            "persona_id": escenario["otro"],
            f"marcador_{escenario['alfa']}": "2",
            f"marcador_{escenario['bravo']}": "1",
        },
    )

    assert respuesta.status_code == 400
    assert servicio.MENSAJE_NO_ASIGNADO in respuesta.text
    assert (
        datos.conexion.execute(
            "SELECT COUNT(*) FROM resultado WHERE partida_id = ?",
            (escenario["partida"],),
        ).fetchone()[0]
        == 0
    )
    assert (
        datos.conexion.execute(
            "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
        ).fetchone()["estado"]
        == "Pendiente de resultado"
    )


def test_resultado_incompleto_no_se_confirma(cliente, ahora):
    """HU-03 · Un resultado incompleto no se confirma"""
    http, datos = cliente
    escenario = _escenario(datos, ahora)

    respuesta = http.post(
        f"/partidas/{escenario['partida']}/resultado",
        data={
            "persona_id": escenario["asignado"],
            f"marcador_{escenario['alfa']}": "2",
        },
    )

    assert respuesta.status_code == 400
    assert servicio.MENSAJE_INCOMPLETO in respuesta.text
    assert (
        datos.conexion.execute(
            "SELECT COUNT(*) FROM resultado WHERE partida_id = ?",
            (escenario["partida"],),
        ).fetchone()[0]
        == 0
    )
    assert (
        datos.conexion.execute(
            "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
        ).fetchone()["estado"]
        == "Pendiente de resultado"
    )


def test_empate_no_se_acepta_como_resultado(cliente, ahora):
    """HU-03 · Un empate no se acepta como resultado"""
    http, datos = cliente
    escenario = _escenario(datos, ahora)

    respuesta = http.post(
        f"/partidas/{escenario['partida']}/resultado",
        data={
            "persona_id": escenario["asignado"],
            f"marcador_{escenario['alfa']}": "2",
            f"marcador_{escenario['bravo']}": "2",
        },
    )

    assert respuesta.status_code == 400
    assert servicio.MENSAJE_EMPATE in respuesta.text
    assert (
        datos.conexion.execute(
            "SELECT COUNT(*) FROM resultado WHERE partida_id = ?",
            (escenario["partida"],),
        ).fetchone()[0]
        == 0
    )
    assert (
        datos.conexion.execute(
            "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
        ).fetchone()["estado"]
        == "Pendiente de resultado"
    )
