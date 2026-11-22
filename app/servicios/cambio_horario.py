from datetime import datetime, timedelta

from app.integraciones.discord import DiscordSimulado

ESTADO_SOLICITADA = "Solicitada"
ESTADO_APROBADA = "Aprobada"
ESTADO_RECHAZADA = "Rechazada"
ESTADO_VENCIDA = "Vencida"

ANTICIPACION_MINIMA_HORAS = 2

MENSAJE_SOLICITUD_OK = "Solicitud de cambio de horario registrada con éxito."
MENSAJE_PLAZO_VENCIDO = "El plazo para solicitar cambios de horario ya venció (debe solicitarse con más de 2 horas de anticipación)."
MENSAJE_HORARIO_INVALIDO = "El horario propuesto debe ser posterior a la fecha y hora actual."
MENSAJE_SOLICITUD_NO_ENCONTRADA = "Solicitud no encontrada."
MENSAJE_SOLICITUD_YA_RESUELTA = "La solicitud ya no está en estado Solicitada."
MENSAJE_MOTIVO_OBLIGATORIO = "Debe indicar un motivo para rechazar la solicitud."
MENSAJE_SOLO_MODERADOR_ASIGNADO = "Solo el Moderador asignado a la partida puede resolver esta solicitud."
MENSAJE_APROBADA_OK = "Solicitud aprobada: la partida quedó reprogramada con el nuevo horario."
MENSAJE_RECHAZADA_OK = "Solicitud rechazada: la partida conserva su horario original."


class ErrorCambioHorario(ValueError):
    pass


def _a_datetime(valor):
    if isinstance(valor, datetime):
        return valor
    return datetime.fromisoformat(valor)


def actualizar_solicitudes_vencidas(conexion, ahora):
    ahora_dt = _a_datetime(ahora)
    solicitudes = conexion.execute(
        """
        SELECT s.id, p.fecha_hora
        FROM solicitud_cambio_horario s
        JOIN partida p ON p.id = s.partida_id
        WHERE s.estado = ?
        """,
        (ESTADO_SOLICITADA,),
    ).fetchall()

    for fila in solicitudes:
        fecha_partida = _a_datetime(fila["fecha_hora"])
        # Si faltan 2 horas o menos para la partida
        if ahora_dt >= fecha_partida - timedelta(hours=ANTICIPACION_MINIMA_HORAS):
            conexion.execute(
                """
                UPDATE solicitud_cambio_horario
                SET estado = ?, fecha_resolucion = ?
                WHERE id = ?
                """,
                (
                    ESTADO_VENCIDA,
                    ahora_dt.isoformat(timespec="seconds"),
                    fila["id"],
                ),
            )
    conexion.commit()


def solicitar_cambio_horario(
    conexion,
    partida_id: int,
    jugador_id: int,
    nuevo_horario,
    ahora,
    discord=None,
):
    ahora_dt = _a_datetime(ahora)
    nuevo_horario_dt = _a_datetime(nuevo_horario)

    if nuevo_horario_dt <= ahora_dt:
        raise ErrorCambioHorario(MENSAJE_HORARIO_INVALIDO)

    jugador = conexion.execute(
        "SELECT id, nombre, tipo, equipo_id FROM persona WHERE id = ?",
        (jugador_id,),
    ).fetchone()
    if not jugador or jugador["tipo"] != "Jugador" or not jugador["equipo_id"]:
        raise ErrorCambioHorario("El solicitante debe ser un jugador con equipo asignado.")

    partida = conexion.execute(
        """
        SELECT p.id, p.fecha_hora, p.estado, p.moderador_id
        FROM partida p
        WHERE p.id = ?
        """,
        (partida_id,),
    ).fetchone()
    if not partida:
        raise ErrorCambioHorario("Partida no encontrada.")

    # Verificar que el equipo del jugador juegue en esta partida
    en_partida = conexion.execute(
        "SELECT 1 FROM disponibilidad WHERE partida_id = ? AND equipo_id = ?",
        (partida_id, jugador["equipo_id"]),
    ).fetchone()
    if not en_partida:
        raise ErrorCambioHorario("El equipo del jugador no participa en esta partida.")

    if partida["estado"] != "Programada":
        raise ErrorCambioHorario("Solo se pueden solicitar cambios de horario para partidas programadas.")

    fecha_partida = _a_datetime(partida["fecha_hora"])
    # Regla: debe faltar MÁS de 2 horas
    if ahora_dt >= fecha_partida - timedelta(hours=ANTICIPACION_MINIMA_HORAS):
        raise ErrorCambioHorario(MENSAJE_PLAZO_VENCIDO)

    equipo = conexion.execute(
        "SELECT nombre FROM equipo WHERE id = ?", (jugador["equipo_id"],)
    ).fetchone()
    equipo_nombre = equipo["nombre"] if equipo else "Equipo"

    cursor = conexion.execute(
        """
        INSERT INTO solicitud_cambio_horario (
            partida_id, equipo_id, solicitante_id, nuevo_horario,
            fecha_solicitud, estado
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            partida_id,
            jugador["equipo_id"],
            jugador_id,
            nuevo_horario_dt.isoformat(timespec="minutes"),
            ahora_dt.isoformat(timespec="seconds"),
            ESTADO_SOLICITADA,
        ),
    )
    solicitud_id = cursor.lastrowid
    conexion.commit()

    # Publicar aviso en Discord
    adaptador_discord = discord or DiscordSimulado()
    adaptador_discord.avisar_solicitud_cambio(
        conexion,
        partida_id,
        equipo_nombre,
        nuevo_horario_dt.isoformat(timespec="minutes"),
        ahora_dt.isoformat(timespec="seconds"),
    )
    conexion.commit()

    return {
        "id": solicitud_id,
        "partida_id": partida_id,
        "nuevo_horario": nuevo_horario_dt.isoformat(timespec="minutes"),
        "estado": ESTADO_SOLICITADA,
    }


def aprobar_solicitud(
    conexion,
    solicitud_id: int,
    moderador_id: int,
    ahora,
    discord=None,
):
    ahora_dt = _a_datetime(ahora)
    actualizar_solicitudes_vencidas(conexion, ahora_dt)

    solicitud = conexion.execute(
        """
        SELECT s.*, p.moderador_id AS partida_moderador_id, p.fecha_hora AS partida_fecha_hora
        FROM solicitud_cambio_horario s
        JOIN partida p ON p.id = s.partida_id
        WHERE s.id = ?
        """,
        (solicitud_id,),
    ).fetchone()

    if not solicitud:
        raise ErrorCambioHorario(MENSAJE_SOLICITUD_NO_ENCONTRADA)

    if solicitud["estado"] != ESTADO_SOLICITADA:
        raise ErrorCambioHorario(MENSAJE_SOLICITUD_YA_RESUELTA)

    moderador = conexion.execute(
        "SELECT id, nombre, tipo FROM persona WHERE id = ?", (moderador_id,)
    ).fetchone()
    if not moderador or moderador["tipo"] != "Moderador":
        raise ErrorCambioHorario("Solo un Moderador puede aprobar solicitudes.")

    if solicitud["partida_moderador_id"] and solicitud["partida_moderador_id"] != moderador_id:
        raise ErrorCambioHorario(MENSAJE_SOLO_MODERADOR_ASIGNADO)

    # Actualizar partida con nuevo horario
    conexion.execute(
        "UPDATE partida SET fecha_hora = ? WHERE id = ?",
        (solicitud["nuevo_horario"], solicitud["partida_id"]),
    )

    # Actualizar solicitud
    conexion.execute(
        """
        UPDATE solicitud_cambio_horario
        SET estado = ?, fecha_resolucion = ?, moderador_id = ?
        WHERE id = ?
        """,
        (
            ESTADO_APROBADA,
            ahora_dt.isoformat(timespec="seconds"),
            moderador_id,
            solicitud_id,
        ),
    )
    conexion.commit()

    adaptador_discord = discord or DiscordSimulado()
    adaptador_discord.avisar_resolucion_cambio(
        conexion,
        solicitud["partida_id"],
        ESTADO_APROBADA,
        solicitud["nuevo_horario"],
        None,
        ahora_dt.isoformat(timespec="seconds"),
    )
    conexion.commit()

    return {
        "id": solicitud_id,
        "partida_id": solicitud["partida_id"],
        "nuevo_horario": solicitud["nuevo_horario"],
        "estado": ESTADO_APROBADA,
    }


def rechazar_solicitud(
    conexion,
    solicitud_id: int,
    moderador_id: int,
    motivo: str,
    ahora,
    discord=None,
):
    ahora_dt = _a_datetime(ahora)
    actualizar_solicitudes_vencidas(conexion, ahora_dt)

    if not motivo or not motivo.strip():
        raise ErrorCambioHorario(MENSAJE_MOTIVO_OBLIGATORIO)

    solicitud = conexion.execute(
        """
        SELECT s.*, p.moderador_id AS partida_moderador_id
        FROM solicitud_cambio_horario s
        JOIN partida p ON p.id = s.partida_id
        WHERE s.id = ?
        """,
        (solicitud_id,),
    ).fetchone()

    if not solicitud:
        raise ErrorCambioHorario(MENSAJE_SOLICITUD_NO_ENCONTRADA)

    if solicitud["estado"] != ESTADO_SOLICITADA:
        raise ErrorCambioHorario(MENSAJE_SOLICITUD_YA_RESUELTA)

    moderador = conexion.execute(
        "SELECT id, nombre, tipo FROM persona WHERE id = ?", (moderador_id,)
    ).fetchone()
    if not moderador or moderador["tipo"] != "Moderador":
        raise ErrorCambioHorario("Solo un Moderador puede rechazar solicitudes.")

    if solicitud["partida_moderador_id"] and solicitud["partida_moderador_id"] != moderador_id:
        raise ErrorCambioHorario(MENSAJE_SOLO_MODERADOR_ASIGNADO)

    conexion.execute(
        """
        UPDATE solicitud_cambio_horario
        SET estado = ?, motivo_rechazo = ?, fecha_resolucion = ?, moderador_id = ?
        WHERE id = ?
        """,
        (
            ESTADO_RECHAZADA,
            motivo.strip(),
            ahora_dt.isoformat(timespec="seconds"),
            moderador_id,
            solicitud_id,
        ),
    )
    conexion.commit()

    adaptador_discord = discord or DiscordSimulado()
    adaptador_discord.avisar_resolucion_cambio(
        conexion,
        solicitud["partida_id"],
        ESTADO_RECHAZADA,
        solicitud["nuevo_horario"],
        motivo.strip(),
        ahora_dt.isoformat(timespec="seconds"),
    )
    conexion.commit()

    return {
        "id": solicitud_id,
        "partida_id": solicitud["partida_id"],
        "estado": ESTADO_RECHAZADA,
        "motivo_rechazo": motivo.strip(),
    }


def listar_solicitudes_equipo(conexion, equipo_id: int, ahora):
    actualizar_solicitudes_vencidas(conexion, ahora)
    filas = conexion.execute(
        """
        SELECT s.*, p.fase, p.fecha_hora AS partida_fecha_hora,
               per.nombre AS solicitante_nombre, m.nombre AS moderador_nombre
        FROM solicitud_cambio_horario s
        JOIN partida p ON p.id = s.partida_id
        JOIN persona per ON per.id = s.solicitante_id
        LEFT JOIN persona m ON m.id = s.moderador_id
        WHERE s.equipo_id = ?
        ORDER BY s.id DESC
        """,
        (equipo_id,),
    ).fetchall()
    return [dict(f) for f in filas]


def listar_solicitudes_moderador(conexion, moderador_id: int, ahora):
    actualizar_solicitudes_vencidas(conexion, ahora)
    filas = conexion.execute(
        """
        SELECT s.*, p.fase, p.fecha_hora AS partida_fecha_hora,
               eq.nombre AS equipo_nombre, per.nombre AS solicitante_nombre
        FROM solicitud_cambio_horario s
        JOIN partida p ON p.id = s.partida_id
        JOIN equipo eq ON eq.id = s.equipo_id
        JOIN persona per ON per.id = s.solicitante_id
        WHERE p.moderador_id = ? OR s.moderador_id = ?
        ORDER BY s.id DESC
        """,
        (moderador_id, moderador_id),
    ).fetchall()
    return [dict(f) for f in filas]
