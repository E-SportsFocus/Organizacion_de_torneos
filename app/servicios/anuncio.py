from app.integraciones.discord import DiscordSimulado

DISCORD_ENVIADO = "Enviado"
DISCORD_PENDIENTE = "Pendiente"


def publicar_ganador(
    conexion,
    partida,
    resultado_id,
    ganador,
    marcador_texto,
    fecha_hora,
    discord=None,
):
    """Publica al ganador y registra el envío del anuncio a Discord.

    La publicación en la plataforma se guarda antes de llamar al sistema
    externo. Si Discord falla, el anuncio queda pendiente y la publicación
    no se pierde.
    """
    cursor = conexion.execute(
        """
        INSERT INTO anuncio (
            partida_id, resultado_id, fecha_hora_publicacion, discord_estado
        )
        VALUES (?, ?, ?, ?)
        """,
        (partida["partida_id"], resultado_id, fecha_hora, DISCORD_PENDIENTE),
    )
    anuncio_id = cursor.lastrowid
    estado = DISCORD_PENDIENTE
    detalle = None
    try:
        (discord or DiscordSimulado()).anunciar_ganador(
            conexion, partida, ganador, marcador_texto, fecha_hora
        )
    except Exception as error:  # el canal externo no debe romper la publicación
        detalle = str(error).strip() or error.__class__.__name__
    else:
        estado = DISCORD_ENVIADO

    conexion.execute(
        """
        UPDATE anuncio
        SET discord_estado = ?, discord_fecha_hora = ?, discord_detalle = ?
        WHERE id = ?
        """,
        (
            estado,
            fecha_hora if estado == DISCORD_ENVIADO else None,
            detalle,
            anuncio_id,
        ),
    )
    return {
        "anuncio_id": anuncio_id,
        "discord_estado": estado,
        "discord_detalle": detalle,
        "fecha_hora_publicacion": fecha_hora,
    }


def anuncios_por_partida(conexion):
    """Devuelve los anuncios indexados por partida."""
    return {
        fila["partida_id"]: dict(fila)
        for fila in conexion.execute(
            """
            SELECT id AS anuncio_id, partida_id, resultado_id,
                   fecha_hora_publicacion, discord_estado,
                   discord_fecha_hora, discord_detalle
            FROM anuncio
            ORDER BY fecha_hora_publicacion DESC, id DESC
            """
        )
    }
