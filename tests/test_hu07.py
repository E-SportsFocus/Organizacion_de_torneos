from datetime import timedelta

from app.servicios import resultado as servicio_resultado


def _torneo_con_resultado(datos, ahora):
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador("Marta Arbitraje")
    organizador = datos.organizador("Olga Organización")
    torneo = datos.torneo("Copa E-Sports Focus")
    datos.conexion.execute(
        "UPDATE torneo SET organizador_id = ? WHERE id = ?", (organizador, torneo)
    )
    datos.conexion.commit()
    partida = datos.partida(
        torneo,
        moderador,
        ahora - timedelta(hours=2),
        [alfa, bravo],
        estado="Pendiente de resultado",
        fase="Final",
    )
    servicio_resultado.registrar_resultado(
        datos.conexion,
        partida,
        moderador,
        {alfa: 2, bravo: 1},
        ahora,
    )
    return {
        "torneo": torneo,
        "partida": partida,
        "alfa": alfa,
        "bravo": bravo,
        "moderador": moderador,
        "organizador": organizador,
    }


def test_pagina_publica_muestra_anuncios_y_bracket(cliente, ahora):
    """HU-07 · El visitante consulta el torneo público (anuncios y bracket)"""
    http, datos = cliente
    _torneo_con_resultado(datos, ahora)

    respuesta = http.get("/")

    assert respuesta.status_code == 200
    html = respuesta.text
    assert "Copa E-Sports Focus" in html
    assert "Valorant" in html
    assert "Vista pública · solo lectura" in html
    assert "Anuncios de ganadores" in html
    assert "Equipo Alfa es el ganador de Final" in html
    assert "Ganador anunciado" in html
    assert "Bracket resumido" in html
    assert "Enfrentamientos Oficiales" not in html
    assert "<th>Equipos</th>" not in html
    assert "<th>Ganador</th>" not in html
    assert "<h3 style=\"margin-top:0\">Partidas</h3>" not in html
    assert "Ver detalle completo de partidas y marcador en Bracket" in html
    assert "Equipo Bravo" in html
    assert "<form" not in html
    assert "Registrar resultado" not in html
    assert "Anunciar ganador" not in html
    assert "Selector de rol de demostración" not in html
    assert "Ver el torneo público" not in html

    # La tabla detallada de partidas se conserva en /bracket
    respuesta_bracket = http.get("/bracket")
    assert respuesta_bracket.status_code == 200
    assert "Partidas" in respuesta_bracket.text
    assert "Historial de actualizaciones" in respuesta_bracket.text

    redireccion = http.get("/torneo", follow_redirects=False)

    assert redireccion.status_code == 307
    assert redireccion.headers["location"] == "/"


def test_partida_sin_resultado_no_muestra_ganador(cliente, ahora):
    """HU-07 · Una partida sin resultado no muestra ganador"""
    http, datos = cliente
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador("Marta Arbitraje")
    torneo = datos.torneo("Copa E-Sports Focus")
    datos.partida(
        torneo,
        moderador,
        ahora,
        [alfa, bravo],
        estado="Pendiente de resultado",
        fase="Semifinal",
    )

    respuesta = http.get("/")

    assert respuesta.status_code == 200
    html = respuesta.text
    assert "Semifinal" in html
    assert "Pendiente de resultado" in html
    assert "Sin resultado" in html
    assert "es el ganador de" not in html
    assert "Ganador anunciado" not in html


def test_menu_desplegable_ofrece_navegacion_y_roles(cliente):
    """HU-07 · El visitante abre el menú lateral y cambia de rol"""
    http, datos = cliente
    alfa = datos.equipo("Equipo Alfa")
    datos.jugador("Ana Ríos", alfa)
    moderador = datos.moderador("Marta Arbitraje")
    organizador = datos.organizador("Olga Organización")

    respuesta = http.get("/")

    assert respuesta.status_code == 200
    html = respuesta.text
    assert 'aria-label="Abrir menú"' in html
    assert 'aria-expanded="false"' in html
    assert 'id="menu-lateral"' in html
    assert 'aria-label="Menú de navegación"' in html
    assert 'href="/"' in html
    assert 'href="/bracket"' in html
    assert 'href="/torneo"' not in html
    assert html.count('<button class="menu-enlace menu-rol-boton"') == 3
    assert 'aria-controls="menu-rol-jugador"' in html
    assert 'aria-controls="menu-rol-moderador"' in html
    assert 'aria-controls="menu-rol-organizador"' in html
    assert 'id="menu-rol-jugador"' in html
    assert 'id="menu-rol-moderador"' in html
    assert 'id="menu-rol-organizador"' in html
    assert "Ana Ríos" in html
    assert "Equipo Alfa" in html
    assert "Marta Arbitraje" in html
    assert "Olga Organización" in html
    assert f'href="/moderador?persona_id={moderador}"' in html
    assert f'href="/organizador?persona_id={organizador}"' in html
    assert 'aria-current="page"' in html


def test_menu_se_cierra_sin_cambiar_de_pagina(cliente):
    """HU-07 · El menú se cierra sin cambiar de página"""
    http, datos = cliente

    respuesta = http.get("/")

    assert respuesta.status_code == 200
    html = respuesta.text
    assert 'data-menu-cerrar' in html
    assert 'aria-label="Cerrar menú"' in html
    assert "Escape" in html
    assert "cerrarMenu" in html
    assert "inert" in html
    assert "panel.contains(evento.target)" in html
    assert "menu-fondo" not in html
