from datetime import timedelta

from fastapi.testclient import TestClient

from app.fabrica import crear_app
from app.integraciones.discord import Discord

AHORA_ISO = "2026-11-17T12:00:00"


def _escenario(datos, ahora):
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    asignado = datos.moderador("Marta Arbitraje")
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
        fase="Semifinal",
    )
    return {
        "alfa": alfa,
        "bravo": bravo,
        "asignado": asignado,
        "organizador": organizador,
        "torneo": torneo,
        "partida": partida,
    }


def _registrar(http, escenario):
    return http.post(
        f"/partidas/{escenario['partida']}/resultado",
        data={
            "persona_id": escenario["asignado"],
            f"marcador_{escenario['alfa']}": "2",
            f"marcador_{escenario['bravo']}": "1",
        },
    )


def test_ganador_se_publica_al_confirmarse_el_resultado(cliente, ahora):
    """HU-06 · El ganador se publica al confirmarse el resultado"""
    http, datos = cliente
    escenario = _escenario(datos, ahora)

    respuesta = _registrar(http, escenario)

    assert respuesta.status_code == 200
    assert "El ganador quedó anunciado." in respuesta.text

    anuncio = datos.conexion.execute(
        "SELECT * FROM anuncio WHERE partida_id = ?", (escenario["partida"],)
    ).fetchone()
    assert anuncio is not None
    assert anuncio["resultado_id"] is not None
    assert anuncio["discord_estado"] == "Enviado"
    assert anuncio["fecha_hora_publicacion"] == AHORA_ISO
    assert anuncio["discord_fecha_hora"] == AHORA_ISO

    partida = datos.conexion.execute(
        "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
    ).fetchone()
    assert partida["estado"] == "Anunciada"

    log = datos.conexion.execute(
        "SELECT operacion, detalle FROM integraciones_log WHERE operacion = 'anunciar_ganador'"
    ).fetchall()
    assert len(log) == 1
    assert "Equipo Alfa" in log[0]["detalle"]

    organizador_html = http.get(
        f"/organizador?persona_id={escenario['organizador']}"
    )
    assert organizador_html.status_code == 200
    assert "Anuncios" in organizador_html.text
    assert "Equipo Alfa es el ganador de Semifinal" in organizador_html.text
    assert "Publicado en la plataforma" in organizador_html.text
    assert "Discord enviado" in organizador_html.text


def test_no_se_anuncia_un_ganador_con_resultado_pendiente(cliente, ahora):
    """HU-06 · No se anuncia un ganador con resultado pendiente"""
    http, datos = cliente
    escenario = _escenario(datos, ahora)

    respuesta = http.get(f"/organizador?persona_id={escenario['organizador']}")

    assert respuesta.status_code == 200
    assert "Todavía no hay un ganador que anunciar." in respuesta.text
    assert "Falta registrar el resultado" in respuesta.text
    assert (
        datos.conexion.execute(
            "SELECT COUNT(*) FROM anuncio WHERE partida_id = ?",
            (escenario["partida"],),
        ).fetchone()[0]
        == 0
    )


class DiscordQueFalla(Discord):
    """Simula un canal de Discord que no responde al anuncio."""

    def notificar_resultado(self, conexion, resultado_id, mensaje, fecha_hora):
        return True

    def anunciar_ganador(self, conexion, partida, ganador, marcador_texto, fecha_hora):
        raise RuntimeError("El canal de Discord no responde")


def test_fallo_de_discord_no_impide_publicar_el_ganador(base, ahora):
    """HU-06 · Un fallo en Discord no impide publicar el ganador en la plataforma"""
    datos, ruta = base
    escenario = _escenario(datos, ahora)
    aplicacion = crear_app(
        ruta_db=ruta, reloj=lambda: ahora, discord=DiscordQueFalla()
    )

    with TestClient(aplicacion) as http:
        respuesta = _registrar(http, escenario)

        assert respuesta.status_code == 200
        assert "El anuncio en Discord quedó pendiente de envío." in respuesta.text

        anuncio = datos.conexion.execute(
            "SELECT * FROM anuncio WHERE partida_id = ?", (escenario["partida"],)
        ).fetchone()
        assert anuncio is not None
        assert anuncio["discord_estado"] == "Pendiente"
        assert anuncio["discord_fecha_hora"] is None
        assert "no responde" in anuncio["discord_detalle"]

        partida = datos.conexion.execute(
            "SELECT estado FROM partida WHERE id = ?", (escenario["partida"],)
        ).fetchone()
        assert partida["estado"] == "Anunciada"

        organizador_html = http.get(
            f"/organizador?persona_id={escenario['organizador']}"
        )
        assert "Equipo Alfa es el ganador de Semifinal" in organizador_html.text
        assert "Discord pendiente de envío" in organizador_html.text
