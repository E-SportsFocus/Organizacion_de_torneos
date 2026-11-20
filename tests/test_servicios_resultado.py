from datetime import timedelta

import pytest

from app.servicios import resultado as servicio


def _partida_pendiente(datos, ahora, equipos_nombres=("Equipo Alfa", "Equipo Bravo")):
    equipos = [datos.equipo(nombre) for nombre in equipos_nombres]
    moderador = datos.moderador("Marta Arbitraje")
    torneo = datos.torneo()
    partida = datos.partida(
        torneo,
        moderador,
        ahora - timedelta(hours=2),
        equipos,
        estado="Pendiente de resultado",
    )
    return partida, equipos, moderador, torneo


def test_registrar_resultado_permite_marcador_cero(base, ahora):
    datos, _ = base
    partida, equipos, moderador, _ = _partida_pendiente(datos, ahora)

    resultado = servicio.registrar_resultado(
        datos.conexion,
        partida,
        moderador,
        {equipos[0]: 0, equipos[1]: 1},
        ahora,
    )

    assert resultado["ganador"]["equipo_id"] == equipos[1]
    assert resultado["marcador_texto"] == "Equipo Alfa 0 - Equipo Bravo 1"


@pytest.mark.parametrize("marcador", ["-1", "2.5", "abc", "  "])
def test_registrar_resultado_rechaza_marcadores_invalidos(base, ahora, marcador):
    datos, _ = base
    partida, equipos, moderador, _ = _partida_pendiente(datos, ahora)

    with pytest.raises(servicio.ErrorResultado) as error:
        servicio.registrar_resultado(
            datos.conexion,
            partida,
            moderador,
            {equipos[0]: marcador, equipos[1]: 1},
            ahora,
        )

    assert error.value.mensaje in (
        servicio.MENSAJE_MARCADOR_INVALIDO,
        servicio.MENSAJE_INCOMPLETO,
    )
    assert datos.conexion.execute("SELECT COUNT(*) FROM resultado").fetchone()[0] == 0


def test_registrar_resultado_rechaza_partida_que_no_esta_pendiente(base, ahora):
    datos, _ = base
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador()
    torneo = datos.torneo()
    partida = datos.partida(
        torneo, moderador, ahora - timedelta(hours=2), [alfa, bravo], estado="En curso"
    )

    with pytest.raises(servicio.ErrorResultado) as error:
        servicio.registrar_resultado(
            datos.conexion, partida, moderador, {alfa: 2, bravo: 1}, ahora
        )

    assert error.value.mensaje == servicio.MENSAJE_NO_PENDIENTE


def test_registrar_resultado_rechaza_segundo_resultado(base, ahora):
    datos, _ = base
    partida, equipos, moderador, _ = _partida_pendiente(datos, ahora)

    servicio.registrar_resultado(
        datos.conexion, partida, moderador, {equipos[0]: 2, equipos[1]: 1}, ahora
    )

    with pytest.raises(servicio.ErrorResultado) as error:
        servicio.registrar_resultado(
            datos.conexion, partida, moderador, {equipos[0]: 3, equipos[1]: 1}, ahora
        )

    assert error.value.mensaje == servicio.MENSAJE_YA_TIENE_RESULTADO
    assert datos.conexion.execute("SELECT COUNT(*) FROM resultado").fetchone()[0] == 1


def test_registrar_resultado_rechaza_partida_sin_dos_equipos(base, ahora):
    datos, _ = base
    alfa = datos.equipo("Equipo Alfa")
    moderador = datos.moderador()
    torneo = datos.torneo()
    partida = datos.partida(
        torneo,
        moderador,
        ahora - timedelta(hours=2),
        [alfa],
        estado="Pendiente de resultado",
    )

    with pytest.raises(servicio.ErrorResultado) as error:
        servicio.registrar_resultado(
            datos.conexion, partida, moderador, {alfa: 2}, ahora
        )

    assert error.value.mensaje == servicio.MENSAJE_SIN_EQUIPOS


def test_el_bracket_es_unico_por_torneo_y_conserva_el_historial(base, ahora):
    datos, _ = base
    partida_uno, equipos, moderador, torneo = _partida_pendiente(datos, ahora)
    partida_dos = datos.partida(
        torneo,
        moderador,
        ahora - timedelta(hours=1),
        equipos,
        estado="Pendiente de resultado",
    )

    servicio.registrar_resultado(
        datos.conexion, partida_uno, moderador, {equipos[0]: 2, equipos[1]: 0}, ahora
    )
    servicio.registrar_resultado(
        datos.conexion,
        partida_dos,
        moderador,
        {equipos[0]: 1, equipos[1]: 3},
        ahora + timedelta(hours=1),
    )

    assert (
        datos.conexion.execute(
            "SELECT COUNT(*) FROM bracket WHERE torneo_id = ?", (torneo,)
        ).fetchone()[0]
        == 1
    )
    bracket = datos.conexion.execute(
        "SELECT * FROM bracket WHERE torneo_id = ?", (torneo,)
    ).fetchone()
    assert bracket["ultima_actualizacion"] == (ahora + timedelta(hours=1)).isoformat(
        timespec="seconds"
    )
    historial = datos.conexion.execute(
        "SELECT * FROM bracket_actualizacion WHERE bracket_id = ? ORDER BY id",
        (bracket["id"],),
    ).fetchall()
    assert len(historial) == 2

    resumen = servicio.listar_bracket(datos.conexion, torneo)
    assert len(resumen) == 2
    assert resumen[0]["resultado"]["marcador_texto"] == "Equipo Alfa 2 - Equipo Bravo 0"
    assert resumen[1]["resultado"]["ganador"]["equipo_id"] == equipos[1]
