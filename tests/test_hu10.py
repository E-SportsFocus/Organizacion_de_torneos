"""Pruebas de aceptación para HU-10: Control del estado del torneo por el Organizador.

Verifica la visibilidad y restricciones del estado Borrador:
- Torneos en Borrador ocultos a Jugador, Moderador y Visitante.
- Organizador sí puede ver un torneo en Borrador.
- El estado del torneo es visible cuando está publicado.
- No se confirma disponibilidad si el torneo está en Borrador.
- No se registra resultado si el torneo está en Borrador.
- El jugador ve el nombre y estado del torneo en sus partidas.
"""

from datetime import timedelta

from app.servicios import disponibilidad as servicio_disp
from app.servicios import resultado as servicio_res
import pytest


# ── Helpers ──────────────────────────────────────────────────────────────────

def _crear_torneo_borrador(datos, ahora):
    """Crea un torneo en estado Borrador con una partida programada."""
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    jugador_alfa = datos.jugador("Ana Ríos", alfa)
    moderador = datos.moderador("Marta Arbitraje")
    organizador = datos.organizador("Olga Organización")

    torneo = datos.torneo("Copa E-Sports Focus")
    datos.conexion.execute(
        "UPDATE torneo SET estado = ?, organizador_id = ? WHERE id = ?",
        ("Borrador", organizador, torneo),
    )
    datos.conexion.commit()

    partida = datos.partida(
        torneo, moderador, ahora + timedelta(hours=2),
        [alfa, bravo], estado="Programada", fase="Cuartos de final",
    )

    return {
        "torneo": torneo,
        "partida": partida,
        "alfa": alfa,
        "bravo": bravo,
        "jugador_alfa": jugador_alfa,
        "moderador": moderador,
        "organizador": organizador,
    }


# ── Tests de visibilidad (vistas HTTP) ───────────────────────────────────────

def test_torneo_en_borrador_no_se_muestra_a_visitante(cliente, ahora):
    """HU-10 · Un torneo en Borrador no se muestra a un Visitante."""
    http, datos = cliente
    _crear_torneo_borrador(datos, ahora)

    respuesta = http.get("/")
    assert respuesta.status_code == 200
    html = respuesta.text
    assert "El torneo aún no está publicado" in html
    assert "Copa E-Sports Focus" not in html


def test_bracket_en_borrador_no_se_muestra_a_visitante(cliente, ahora):
    """HU-10 · El bracket de un torneo en Borrador no se muestra a un Visitante."""
    http, datos = cliente
    _crear_torneo_borrador(datos, ahora)

    respuesta = http.get("/bracket")
    assert respuesta.status_code == 200
    html = respuesta.text
    assert "El torneo aún no está publicado" in html


def test_torneo_en_borrador_es_visible_para_organizador(cliente, ahora):
    """HU-10 · El Organizador sí puede ver un torneo en Borrador."""
    http, datos = cliente
    esc = _crear_torneo_borrador(datos, ahora)

    respuesta = http.get(f"/?persona_id={esc['organizador']}")
    assert respuesta.status_code == 200
    html = respuesta.text
    assert "El torneo aún no está publicado" not in html


def test_estado_del_torneo_es_visible_cuando_esta_publicado(cliente, ahora):
    """HU-10 · Cuando el torneo NO está en Borrador, el badge del estado se muestra."""
    http, datos = cliente
    organizador = datos.organizador("Olga Organización")
    torneo = datos.torneo("Copa Abierta")
    datos.conexion.execute(
        "UPDATE torneo SET estado = ?, organizador_id = ? WHERE id = ?",
        ("Inscripciones abiertas", organizador, torneo),
    )
    datos.conexion.commit()

    respuesta = http.get("/")
    assert respuesta.status_code == 200
    html = respuesta.text
    assert "Inscripciones abiertas" in html
    assert "Copa Abierta" in html


# ── Tests de lógica de negocio (servicios) ───────────────────────────────────

def test_no_se_confirma_disponibilidad_si_torneo_en_borrador(base, ahora):
    """HU-10 / HU-04 · Rechaza confirmar disponibilidad en torneo Borrador."""
    datos, _ruta = base
    esc = _crear_torneo_borrador(datos, ahora)

    disp = datos.disponibilidad(esc["partida"], esc["alfa"])
    with pytest.raises(servicio_disp.ErrorDisponibilidad) as exc:
        servicio_disp.confirmar_disponibilidad(
            datos.conexion, disp["id"], esc["jugador_alfa"], ahora,
        )
    assert "Borrador" in exc.value.mensaje


def test_no_se_registra_resultado_si_torneo_en_borrador(base, ahora):
    """HU-10 / HU-03 · Rechaza registrar resultado en torneo Borrador."""
    datos, _ruta = base
    esc = _crear_torneo_borrador(datos, ahora)

    # Cambiar partida a "Pendiente de resultado" para intentar registrar
    datos.conexion.execute(
        "UPDATE partida SET estado = ? WHERE id = ?",
        ("Pendiente de resultado", esc["partida"]),
    )
    datos.conexion.commit()

    with pytest.raises(servicio_res.ErrorResultado) as exc:
        servicio_res.registrar_resultado(
            datos.conexion, esc["partida"], esc["moderador"],
            {esc["alfa"]: 2, esc["bravo"]: 1}, ahora,
        )
    assert "Borrador" in exc.value.mensaje


def test_jugador_no_ve_partidas_si_torneo_en_borrador(cliente, ahora):
    """HU-10 · Un jugador no ve partidas si el torneo está en estado Borrador."""
    http, datos = cliente
    esc = _crear_torneo_borrador(datos, ahora)

    respuesta = http.get(f"/jugador?persona_id={esc['jugador_alfa']}")
    assert respuesta.status_code == 200
    html = respuesta.text
    assert "El equipo no tiene partidas programadas." in html
    assert "Cuartos de final" not in html


def test_jugador_ve_torneo_y_estado_en_sus_partidas(cliente, ahora):
    """HU-10 / HU-04 · El jugador ve el nombre y el estado del torneo en su panel."""
    http, datos = cliente
    alfa = datos.equipo("Equipo Alfa")
    jugador = datos.jugador("Ana Ríos", alfa)
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador("Marta Arbitraje")
    organizador = datos.organizador("Olga Organización")
    torneo = datos.torneo("Copa Visible")
    datos.conexion.execute(
        "UPDATE torneo SET estado = ?, organizador_id = ? WHERE id = ?",
        ("Inscripciones abiertas", organizador, torneo),
    )
    datos.conexion.commit()
    datos.partida(
        torneo, moderador, ahora + timedelta(hours=2),
        [alfa, bravo], estado="Programada", fase="Cuartos",
    )

    respuesta = http.get(f"/jugador?persona_id={jugador}")
    assert respuesta.status_code == 200
    html = respuesta.text
    assert "Copa Visible" in html
    assert "Inscripciones abiertas" in html
