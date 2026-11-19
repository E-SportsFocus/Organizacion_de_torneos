from datetime import timedelta


def _preparar_escenario(datos, ahora, horas, estado="Programada"):
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador()
    jugador = datos.jugador("Ana Ríos", alfa)
    torneo = datos.torneo()
    partida = datos.partida(
        torneo,
        moderador,
        ahora + timedelta(hours=horas),
        [alfa, bravo],
        estado=estado,
    )
    return {
        "alfa": alfa,
        "bravo": bravo,
        "jugador": jugador,
        "partida": partida,
        "disponibilidad": datos.disponibilidad(partida, alfa),
    }


def test_confirmacion_dentro_del_plazo(cliente, ahora):
    """HU-04 · Un equipo confirma su disponibilidad dentro del plazo"""
    http, datos = cliente
    escenario = _preparar_escenario(datos, ahora, horas=6)

    respuesta = http.post(
        f"/disponibilidad/{escenario['disponibilidad']['id']}/confirmar",
        data={"persona_id": escenario["jugador"]},
    )

    assert respuesta.status_code == 200
    assert "Disponibilidad del equipo confirmada." in respuesta.text
    registro = datos.disponibilidad(escenario["partida"], escenario["alfa"])
    assert registro["confirmada"] == "Confirmada"
    assert registro["fecha_confirmacion"] is not None

    consulta = http.get("/moderador")
    assert consulta.status_code == 200
    assert "Equipo Alfa" in consulta.text
    assert consulta.text.count("Confirmada") >= 1


def test_equipo_sin_confirmar_queda_pendiente(cliente, ahora):
    """HU-04 · Un equipo sin confirmar queda con disponibilidad pendiente"""
    http, datos = cliente
    escenario = _preparar_escenario(datos, ahora, horas=6)

    consulta = http.get("/moderador")

    assert consulta.status_code == 200
    assert "Requiere revisión" in consulta.text
    assert "Pendiente" in consulta.text
    registro = datos.disponibilidad(escenario["partida"], escenario["alfa"])
    assert registro["confirmada"] == "Pendiente"


def test_partida_no_inicia_con_un_equipo_pendiente(cliente, ahora):
    """HU-04 · Una partida con un equipo sin confirmar no inicia automáticamente"""
    http, datos = cliente
    escenario = _preparar_escenario(datos, ahora, horas=-1)

    consulta = http.get("/moderador")

    assert consulta.status_code == 200
    assert "Programada" in consulta.text
    assert "Requiere revisión" in consulta.text
    fila = datos.conexion.execute(
        "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()
    assert fila["estado"] == "Programada"


def test_no_se_confirma_fuera_del_plazo(cliente, ahora):
    """HU-04 · No se confirma disponibilidad fuera del plazo"""
    http, datos = cliente
    escenario = _preparar_escenario(datos, ahora, horas=-2, estado="En curso")

    respuesta = http.post(
        f"/disponibilidad/{escenario['disponibilidad']['id']}/confirmar",
        data={"persona_id": escenario["jugador"]},
    )

    assert respuesta.status_code == 400
    assert (
        "La partida ya inició o finalizó; el plazo para confirmar la disponibilidad venció."
        in respuesta.text
    )
    registro = datos.disponibilidad(escenario["partida"], escenario["alfa"])
    assert registro["confirmada"] == "Pendiente"
    assert registro["fecha_confirmacion"] is None
