"""Pruebas de aceptación para HU-08: Visualización gráfica del Bracket del torneo."""

from datetime import timedelta
from app.servicios import resultado as servicio_resultado


def _configurar_torneo_con_fases(datos, ahora):
    """Crea un torneo completo con Cuartos de final, Semifinal y Final."""
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    charlie = datos.equipo("Equipo Charlie")
    delta = datos.equipo("Equipo Delta")
    moderador = datos.moderador("Marta Arbitraje")
    organizador = datos.organizador("Olga Organización")
    torneo = datos.torneo("Copa E-Sports Focus")

    datos.conexion.execute(
        "UPDATE torneo SET organizador_id = ? WHERE id = ?", (organizador, torneo)
    )
    datos.conexion.commit()

    # Partida 1: Cuartos de final (Programada, pendiente)
    p_cuartos = datos.partida(
        torneo,
        moderador,
        ahora + timedelta(hours=4),
        [alfa, bravo],
        estado="Programada",
        fase="Cuartos de final",
    )

    # Partida 2: Semifinal (Programada, pendiente)
    p_semi = datos.partida(
        torneo,
        moderador,
        ahora + timedelta(hours=10),
        [charlie, delta],
        estado="Programada",
        fase="Semifinal",
    )

    # Partida 3: Final (Con resultado y anunciada)
    p_final = datos.partida(
        torneo,
        moderador,
        ahora - timedelta(hours=2),
        [alfa, charlie],
        estado="Pendiente de resultado",
        fase="Final",
    )
    servicio_resultado.registrar_resultado(
        datos.conexion,
        p_final,
        moderador,
        {alfa: 2, charlie: 0},
        ahora,
    )

    return {
        "torneo": torneo,
        "alfa": alfa,
        "bravo": bravo,
        "charlie": charlie,
        "delta": delta,
        "p_cuartos": p_cuartos,
        "p_semi": p_semi,
        "p_final": p_final,
    }


def test_bracket_grafico_muestra_rondas_organizadas_secuencialmente(cliente, ahora):
    """
    Escenario: El bracket gráfico muestra las rondas organizadas secuencialmente
    Dado que el torneo tiene partidas programadas o jugadas en distintas fases
    Cuando un visitante consulta la página del bracket
    Entonces ve el árbol visual de llaves organizado por columnas de rondas
    Y cada enfrentamiento muestra los equipos participantes, la fecha y el estado
    """
    http, datos = cliente
    _configurar_torneo_con_fases(datos, ahora)

    respuesta = http.get("/bracket")

    assert respuesta.status_code == 200
    html = respuesta.text

    # Verifica contenedor del árbol visual
    assert "tarjeta-bracket-visual" in html
    assert "Clasificaciones" in html
    assert "bracket-arbol" in html

    # Verifica columnas de rondas secuenciales
    assert "Cuartos de final" in html
    assert "Semifinal" in html
    assert "Final" in html

    # Verifica equipos y estados en las tarjetas
    assert "Equipo Alfa" in html
    assert "Equipo Bravo" in html
    assert "Programada" in html


def test_enfrentamientos_con_resultado_destacan_ganador_y_marcadores(cliente, ahora):
    """
    Escenario: Los enfrentamientos con resultado destacan al equipo ganador
    Dado que una partida del bracket tiene un resultado registrado
    Cuando se visualiza la llave de esa partida
    Entonces se muestran los marcadores de cada equipo en casillas individuales
    Y el equipo ganador aparece visualmente destacado
    Y se visualiza la conexión de avance hacia la siguiente ronda
    """
    http, datos = cliente
    _configurar_torneo_con_fases(datos, ahora)

    respuesta = http.get("/bracket")

    assert respuesta.status_code == 200
    html = respuesta.text

    # Casillas individuales de marcador
    assert "bracket-marcador-caja" in html
    assert "slot-ganador" in html
    assert "marcador-ganador" in html

    # El ganador (Alfa 2) está destacado sobre Charlie (0)
    assert "Avanza:" in html
    assert "Equipo Alfa" in html


def test_partidas_pendientes_no_muestran_ganador_anticipado(cliente, ahora):
    """
    Escenario: Las partidas pendientes no muestran ganador anticipado
    Dado que una partida del bracket aún no tiene resultado confirmado
    Cuando se visualiza en el árbol de llaves
    Entonces la partida muestra su estado de espera
    Y no se asigna ni inventa un ganador prematuramente
    """
    http, datos = cliente
    _configurar_torneo_con_fases(datos, ahora)

    respuesta = http.get("/bracket")

    assert respuesta.status_code == 200
    html = respuesta.text

    # Las partidas pendientes muestran estado de espera
    assert "Esperando resultado oficial" in html
    assert "bracket-nodo-estado" in html


def test_coexistencia_de_arbol_grafico_y_tabla_de_auditoria(cliente, ahora):
    """
    Escenario: Se permite alternar entre vista de árbol gráfico y tabla de auditoría
    Dado que el usuario está consultando el bracket del torneo
    Cuando navega por la sección
    Entonces dispone del árbol visual interactivo de llaves
    Y puede consultar el historial detallado de actualizaciones y auditoría
    """
    http, datos = cliente
    _configurar_torneo_con_fases(datos, ahora)

    respuesta = http.get("/bracket")

    assert respuesta.status_code == 200
    html = respuesta.text

    # Dispone de la vista visual de clasificaciones
    assert "Clasificaciones" in html
    assert "bracket-arbol" in html

    # Conserva la tabla de auditoría e historial (RP-10)
    assert "Partidas" in html
    assert "Historial de actualizaciones" in html
    assert "Auditoría cronológica de cambios y avances en las llaves" in html


def test_avance_dinamico_de_ganador_a_siguiente_fase(cliente, ahora):
    """
    Simulación real completa: Al inicio solo existen Cuartos de final en Programada.
    Los jugadores confirman disponibilidad → la partida pasa a Pendiente de resultado.
    El moderador registra el resultado → el ganador avanza a Semifinal con disponibilidad
    Pendiente, y la Semifinal aparece en el bracket como Programada.
    """
    http, datos = cliente
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador("Marta Arbitraje")
    organizador = datos.organizador("Olga Organización")
    torneo = datos.torneo("Copa Dinámica")
    datos.conexion.execute(
        "UPDATE torneo SET organizador_id = ? WHERE id = ?", (organizador, torneo)
    )
    datos.conexion.commit()

    j_alfa = datos.jugador("Jugador Alfa", alfa)
    j_bravo = datos.jugador("Jugador Bravo", bravo)

    from app.servicios import disponibilidad as servicio_disp

    # Solo se crea Cuartos de final en Programada (el estado inicial limpio)
    p_cuartos = datos.partida(
        torneo,
        moderador,
        ahora + timedelta(hours=4),
        [alfa, bravo],
        estado="Programada",
        fase="Cuartos de final",
    )

    # Inicialmente en el bracket solo aparece Cuartos de final
    resp1 = http.get("/bracket")
    assert resp1.status_code == 200
    assert "Cuartos de final" in resp1.text
    assert "Semifinal" not in resp1.text

    # Verificar que la partida está en Programada
    estado = datos.conexion.execute(
        "SELECT estado FROM partida WHERE id = ?", (p_cuartos,)
    ).fetchone()["estado"]
    assert estado == "Programada"

    # Jugador de Alfa confirma disponibilidad
    disp_alfa = datos.disponibilidad(p_cuartos, alfa)
    servicio_disp.confirmar_disponibilidad(datos.conexion, disp_alfa["id"], j_alfa, ahora)

    # Partida sigue en Programada (falta Bravo)
    estado = datos.conexion.execute(
        "SELECT estado FROM partida WHERE id = ?", (p_cuartos,)
    ).fetchone()["estado"]
    assert estado == "Programada"

    # Jugador de Bravo confirma → partida pasa automáticamente a Pendiente de resultado
    disp_bravo = datos.disponibilidad(p_cuartos, bravo)
    servicio_disp.confirmar_disponibilidad(datos.conexion, disp_bravo["id"], j_bravo, ahora)

    estado = datos.conexion.execute(
        "SELECT estado FROM partida WHERE id = ?", (p_cuartos,)
    ).fetchone()["estado"]
    assert estado == "Pendiente de resultado"

    # El moderador registra la victoria de Alfa
    servicio_resultado.registrar_resultado(
        datos.conexion,
        p_cuartos,
        moderador,
        {alfa: 2, bravo: 0},
        ahora,
    )

    # El bracket se ha construido dinámicamente: Semifinal aparece con Alfa clasificado
    resp2 = http.get("/bracket")
    assert resp2.status_code == 200
    assert "Cuartos de final" in resp2.text
    assert "Semifinal" in resp2.text
    assert "Equipo Alfa" in resp2.text

    # La semifinal está en Programada (Alfa debe confirmar disponibilidad para la semifinal)
    semi = datos.conexion.execute(
        "SELECT id, estado FROM partida WHERE torneo_id = ? AND fase = 'Semifinal'",
        (torneo,),
    ).fetchone()
    assert semi is not None
    assert semi["estado"] == "Programada"
