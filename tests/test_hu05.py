import json
from datetime import timedelta

from app.servicios import cambio_horario as servicio


def _preparar_escenario(datos, ahora, horas_inicio=6):
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador("Marta Arbitraje")
    jugador = datos.jugador("Ana Ríos", alfa)
    torneo = datos.torneo("Copa E-Sports Focus")
    partida = datos.partida(
        torneo,
        moderador,
        ahora + timedelta(hours=horas_inicio),
        [alfa, bravo],
        estado="Programada",
        fase="Semifinal",
    )
    return {
        "alfa": alfa,
        "bravo": bravo,
        "moderador": moderador,
        "jugador": jugador,
        "partida": partida,
    }


def test_solicitud_dentro_del_plazo_notifica_al_moderador_y_discord(cliente, ahora):
    """HU-05 · Una solicitud dentro del plazo notifica automáticamente al Moderador"""
    http, datos = cliente
    escenario = _preparar_escenario(datos, ahora, horas_inicio=6)
    nuevo_horario = ahora + timedelta(days=1, hours=2)

    respuesta = http.post(
        "/cambio-horario/solicitar",
        data={
            "persona_id": escenario["jugador"],
            "partida_id": escenario["partida"],
            "nuevo_horario": nuevo_horario.isoformat(timespec="minutes"),
        },
    )

    assert respuesta.status_code == 200
    assert "Solicitud de cambio de horario registrada con exito." in respuesta.text

    # Verifica persistencia en base de datos
    fila = datos.conexion.execute(
        "SELECT * FROM solicitud_cambio_horario WHERE partida_id = ?",
        (escenario["partida"],),
    ).fetchone()
    assert fila is not None
    assert fila["estado"] == "Solicitada"
    assert fila["nuevo_horario"] == nuevo_horario.isoformat(timespec="minutes")

    # Verifica registro en Discord
    log = datos.conexion.execute(
        "SELECT * FROM integraciones_log WHERE sistema = 'Discord' AND operacion = 'aviso_solicitud_cambio'"
    ).fetchone()
    assert log is not None
    detalle = json.loads(log["detalle"])
    assert detalle["partida_id"] == escenario["partida"]
    assert "Equipo Alfa" in detalle["equipo"]

    # Verifica visibilidad en panel del Moderador
    consulta_mod = http.get(f"/moderador?persona_id={escenario['moderador']}")
    assert consulta_mod.status_code == 200
    assert "Solicitudes de cambio de horario" in consulta_mod.text
    assert "Equipo Alfa" in consulta_mod.text
    assert "Solicitada" in consulta_mod.text


def test_moderador_aprueba_solicitud_valida(cliente, ahora):
    """HU-05 · El Moderador aprueba una solicitud válida"""
    http, datos = cliente
    escenario = _preparar_escenario(datos, ahora, horas_inicio=6)
    nuevo_horario = ahora + timedelta(days=2)

    servicio.solicitar_cambio_horario(
        datos.conexion,
        escenario["partida"],
        escenario["jugador"],
        nuevo_horario,
        ahora,
    )
    solicitud = datos.conexion.execute(
        "SELECT id FROM solicitud_cambio_horario WHERE partida_id = ?",
        (escenario["partida"],),
    ).fetchone()

    respuesta = http.post(
        f"/cambio-horario/{solicitud['id']}/aprobar",
        data={"persona_id": escenario["moderador"]},
    )

    assert respuesta.status_code == 200
    assert "Solicitud aprobada y partida reprogramada." in respuesta.text

    # Verifica actualización de estado de la solicitud
    sol_actualizada = datos.conexion.execute(
        "SELECT * FROM solicitud_cambio_horario WHERE id = ?", (solicitud["id"],)
    ).fetchone()
    assert sol_actualizada["estado"] == "Aprobada"

    # Verifica reprogramación de la partida
    partida = datos.conexion.execute(
        "SELECT fecha_hora FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()
    assert partida["fecha_hora"] == nuevo_horario.isoformat(timespec="minutes")

    # Verifica publicación en Discord
    log = datos.conexion.execute(
        "SELECT * FROM integraciones_log WHERE sistema = 'Discord' AND operacion = 'aviso_resolucion_cambio'"
    ).fetchone()
    assert log is not None
    detalle = json.loads(log["detalle"])
    assert detalle["estado"] == "Aprobada"


def test_moderador_rechaza_solicitud_con_motivo(cliente, ahora):
    """HU-05 · El Moderador rechaza una solicitud"""
    http, datos = cliente
    escenario = _preparar_escenario(datos, ahora, horas_inicio=6)
    horario_original = datos.conexion.execute(
        "SELECT fecha_hora FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()["fecha_hora"]

    servicio.solicitar_cambio_horario(
        datos.conexion,
        escenario["partida"],
        escenario["jugador"],
        ahora + timedelta(days=1),
        ahora,
    )
    solicitud = datos.conexion.execute(
        "SELECT id FROM solicitud_cambio_horario WHERE partida_id = ?",
        (escenario["partida"],),
    ).fetchone()

    motivo = "Conflicto con la transmisión oficial del torneo"
    respuesta = http.post(
        f"/cambio-horario/{solicitud['id']}/rechazar",
        data={"persona_id": escenario["moderador"], "motivo": motivo},
    )

    assert respuesta.status_code == 200
    assert "Solicitud rechazada." in respuesta.text

    # Verifica que la solicitud quedó rechazada y con motivo
    sol_actualizada = datos.conexion.execute(
        "SELECT * FROM solicitud_cambio_horario WHERE id = ?", (solicitud["id"],)
    ).fetchone()
    assert sol_actualizada["estado"] == "Rechazada"
    assert sol_actualizada["motivo_rechazo"] == motivo

    # Verifica que la partida conserva su horario original
    partida = datos.conexion.execute(
        "SELECT fecha_hora FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()
    assert partida["fecha_hora"] == horario_original

    # Verifica que en la vista del jugador aparece el motivo del rechazo
    consulta_jugador = http.get(f"/jugador?persona_id={escenario['jugador']}")
    assert consulta_jugador.status_code == 200
    assert motivo in consulta_jugador.text


def test_solicitud_fuera_del_plazo_no_se_acepta(cliente, ahora):
    """HU-05 · Una solicitud fuera del plazo no se acepta"""
    http, datos = cliente
    # Faltan 1 hora para la partida (plazo de 2 horas vencido)
    escenario = _preparar_escenario(datos, ahora, horas_inicio=1)

    respuesta = http.post(
        "/cambio-horario/solicitar",
        data={
            "persona_id": escenario["jugador"],
            "partida_id": escenario["partida"],
            "nuevo_horario": (ahora + timedelta(days=1)).isoformat(timespec="minutes"),
        },
    )

    assert respuesta.status_code == 400
    assert (
        "El plazo para solicitar cambios de horario ya venció" in respuesta.text
    )

    # Verifica que no se creó ninguna solicitud
    conteo = datos.conexion.execute(
        "SELECT count(*) as total FROM solicitud_cambio_horario WHERE partida_id = ?",
        (escenario["partida"],),
    ).fetchone()["total"]
    assert conteo == 0


def test_solicitud_sin_decision_al_llegar_al_plazo_limite_vence(base, ahora):
    """HU-05 · Una solicitud sin decisión al llegar al plazo límite vence"""
    datos, _ = base
    # Partida a 4 horas de distancia
    escenario = _preparar_escenario(datos, ahora, horas_inicio=4)
    horario_original = datos.conexion.execute(
        "SELECT fecha_hora FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()["fecha_hora"]

    servicio.solicitar_cambio_horario(
        datos.conexion,
        escenario["partida"],
        escenario["jugador"],
        ahora + timedelta(days=2),
        ahora,
    )

    solicitud = datos.conexion.execute(
        "SELECT * FROM solicitud_cambio_horario WHERE partida_id = ?",
        (escenario["partida"],),
    ).fetchone()
    assert solicitud["estado"] == "Solicitada"

    # Avanza el tiempo a 2 horas y 30 minutos después: ahora faltan 1 hora y media para la partida (<= 2 horas)
    tiempo_avanzado = ahora + timedelta(hours=2, minutes=30)
    solicitudes = servicio.listar_solicitudes_equipo(
        datos.conexion, escenario["alfa"], tiempo_avanzado
    )

    assert len(solicitudes) == 1
    assert solicitudes[0]["estado"] == "Vencida"

    # La partida conserva su horario original
    partida = datos.conexion.execute(
        "SELECT fecha_hora FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()
    assert partida["fecha_hora"] == horario_original
