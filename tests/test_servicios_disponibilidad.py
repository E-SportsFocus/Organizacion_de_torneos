from datetime import timedelta

import pytest

from app.servicios import disponibilidad as servicio


def _preparar_partida(datos, ahora, horas, estado="Programada", equipos_nombres=("Equipo Alfa", "Equipo Bravo")):
    equipos = [datos.equipo(nombre) for nombre in equipos_nombres]
    moderador = datos.moderador()
    torneo = datos.torneo()
    partida = datos.partida(
        torneo,
        moderador,
        ahora + timedelta(hours=horas),
        equipos,
        estado=estado,
    )
    return partida, equipos, moderador, torneo


def test_listar_partidas_equipo_solo_devuelve_las_del_equipo(base, ahora):
    datos, _ = base
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    carlos = datos.equipo("Equipo Carlos")
    moderador = datos.moderador()
    torneo = datos.torneo()
    partida_alfa = datos.partida(torneo, moderador, ahora + timedelta(hours=6), [alfa, bravo])
    datos.partida(torneo, moderador, ahora + timedelta(hours=30), [bravo, carlos])

    partidas = servicio.listar_partidas_equipo(datos.conexion, alfa, ahora)

    assert [partida["partida_id"] for partida in partidas] == [partida_alfa]
    assert partidas[0]["equipo"] == "Equipo Alfa"


def test_listar_partidas_moderador_marca_revision_segun_la_regla_de_ocho_horas(base, ahora):
    datos, _ = base
    alfa = datos.equipo("Equipo Alfa")
    bravo = datos.equipo("Equipo Bravo")
    moderador = datos.moderador()
    torneo = datos.torneo()
    proxima = datos.partida(torneo, moderador, ahora + timedelta(hours=6), [alfa, bravo])
    lejana = datos.partida(torneo, moderador, ahora + timedelta(hours=30), [alfa, bravo])
    pasada = datos.partida(torneo, moderador, ahora - timedelta(hours=1), [alfa, bravo])
    en_curso = datos.partida(torneo, moderador, ahora - timedelta(hours=2), [alfa, bravo], estado="En curso")

    partidas = {partida["partida_id"]: partida for partida in servicio.listar_partidas_moderador(datos.conexion, ahora)}

    assert partidas[proxima]["requiere_revision"] is True
    assert partidas[lejana]["requiere_revision"] is False
    assert partidas[pasada]["requiere_revision"] is True
    assert partidas[en_curso]["requiere_revision"] is False
    assert len(partidas[proxima]["equipos"]) == 2


def test_confirmar_disponibilidad_guarda_estado_y_fecha(base, ahora):
    datos, _ = base
    partida, equipos, _, _ = _preparar_partida(datos, ahora, horas=6)
    jugador = datos.jugador("Ana Ríos", equipos[0])
    registro = datos.disponibilidad(partida, equipos[0])

    servicio.confirmar_disponibilidad(datos.conexion, registro["id"], jugador, ahora)

    actualizado = datos.disponibilidad(partida, equipos[0])
    assert actualizado["confirmada"] == "Confirmada"
    assert actualizado["fecha_confirmacion"] == ahora.isoformat(timespec="seconds")
    assert datos.disponibilidad(partida, equipos[1])["confirmada"] == "Pendiente"


def test_confirmar_disponibilidad_rechaza_jugador_de_otro_equipo(base, ahora):
    datos, _ = base
    partida, equipos, _, _ = _preparar_partida(datos, ahora, horas=6)
    ajeno = datos.jugador("Ajeno", equipos[1])
    registro = datos.disponibilidad(partida, equipos[0])

    with pytest.raises(servicio.ErrorDisponibilidad) as error:
        servicio.confirmar_disponibilidad(datos.conexion, registro["id"], ajeno, ahora)

    assert error.value.mensaje == servicio.MENSAJE_EQUIPO_AJENO
    assert datos.disponibilidad(partida, equipos[0])["confirmada"] == "Pendiente"


def test_confirmar_disponibilidad_rechaza_a_quien_no_es_jugador(base, ahora):
    datos, _ = base
    partida, equipos, moderador, _ = _preparar_partida(datos, ahora, horas=6)
    registro = datos.disponibilidad(partida, equipos[0])

    with pytest.raises(servicio.ErrorDisponibilidad) as error:
        servicio.confirmar_disponibilidad(datos.conexion, registro["id"], moderador, ahora)

    assert error.value.mensaje == servicio.MENSAJE_EQUIPO_AJENO


def test_confirmar_disponibilidad_rechaza_partida_no_programada(base, ahora):
    datos, _ = base
    partida, equipos, _, _ = _preparar_partida(datos, ahora, horas=-1, estado="En curso")
    jugador = datos.jugador("Ana Ríos", equipos[0])
    registro = datos.disponibilidad(partida, equipos[0])

    with pytest.raises(servicio.ErrorDisponibilidad) as error:
        servicio.confirmar_disponibilidad(datos.conexion, registro["id"], jugador, ahora)

    assert error.value.mensaje == servicio.MENSAJE_FUERA_DE_PLAZO
    assert datos.disponibilidad(partida, equipos[0])["confirmada"] == "Pendiente"


def test_confirmar_disponibilidad_rechaza_si_ya_estaba_confirmada(base, ahora):
    datos, _ = base
    partida, equipos, _, _ = _preparar_partida(datos, ahora, horas=6)
    jugador = datos.jugador("Ana Ríos", equipos[0])
    datos.marcar_confirmada(partida, equipos[0], ahora)
    registro = datos.disponibilidad(partida, equipos[0])

    with pytest.raises(servicio.ErrorDisponibilidad) as error:
        servicio.confirmar_disponibilidad(datos.conexion, registro["id"], jugador, ahora)

    assert error.value.mensaje == servicio.MENSAJE_YA_CONFIRMADA


def test_confirmar_disponibilidad_rechaza_persona_inexistente(base, ahora):
    datos, _ = base
    partida, equipos, _, _ = _preparar_partida(datos, ahora, horas=6)
    registro = datos.disponibilidad(partida, equipos[0])

    with pytest.raises(servicio.ErrorDisponibilidad) as error:
        servicio.confirmar_disponibilidad(datos.conexion, registro["id"], 9999, ahora)

    assert error.value.mensaje == servicio.MENSAJE_EQUIPO_AJENO
