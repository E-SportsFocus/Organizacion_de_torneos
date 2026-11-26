from datetime import datetime, timedelta

HORAS_ANTICIPACION_REVISION = 8
ESTADO_PROGRAMADA = "Programada"
ESTADO_PENDIENTE_RESULTADO = "Pendiente de resultado"
DISPONIBILIDAD_PENDIENTE = "Pendiente"
DISPONIBILIDAD_CONFIRMADA = "Confirmada"

MENSAJE_FUERA_DE_PLAZO = (
    "La partida ya inició o finalizó; el plazo para confirmar la disponibilidad venció."
)
MENSAJE_YA_CONFIRMADA = "La disponibilidad de este equipo ya estaba confirmada."
MENSAJE_EQUIPO_AJENO = (
    "No puedes confirmar la disponibilidad de un equipo al que no perteneces."
)
MENSAJE_NO_EXISTE = "La disponibilidad indicada no existe."


class ErrorDisponibilidad(Exception):
    """Error de negocio al confirmar disponibilidad; su mensaje se muestra al usuario."""

    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje


def _como_fecha(valor):
    return datetime.fromisoformat(valor)


def requiere_revision(estado, fecha_hora, disponibilidades, ahora):
    # HU-04, escenarios 2 y 3: la partida sigue Programada y algún equipo no confirmó
    # cuando faltan 8 horas o menos para el inicio.
    hay_pendiente = any(
        registro["confirmada"] == DISPONIBILIDAD_PENDIENTE
        for registro in disponibilidades
    )
    return (
        estado == ESTADO_PROGRAMADA
        and hay_pendiente
        and ahora >= _como_fecha(fecha_hora) - timedelta(hours=HORAS_ANTICIPACION_REVISION)
    )


def listar_partidas_equipo(conexion, equipo_id, ahora):
    filas = conexion.execute(
        """
        SELECT p.id AS partida_id,
               p.fecha_hora,
               p.fase,
               p.estado,
               t.nombre AS torneo,
               t.estado AS torneo_estado,
               d.id AS disponibilidad_id,
               d.confirmada,
               d.fecha_confirmacion,
               e.id AS equipo_id,
               e.nombre AS equipo
        FROM partida p
        JOIN torneo t ON t.id = p.torneo_id
        JOIN disponibilidad d ON d.partida_id = p.id AND d.equipo_id = ?
        JOIN equipo e ON e.id = d.equipo_id
        ORDER BY p.fecha_hora
        """,
        (equipo_id,),
    ).fetchall()
    partidas = []
    for fila in filas:
        partida = dict(fila)
        partida["requiere_revision"] = requiere_revision(
            partida["estado"],
            partida["fecha_hora"],
            [partida],
            ahora,
        )
        partidas.append(partida)
    return partidas


def listar_partidas_moderador(conexion, ahora):
    filas = conexion.execute(
        """
        SELECT p.id AS partida_id,
               p.fecha_hora,
               p.fase,
               p.estado,
               p.moderador_id,
               m.nombre AS moderador,
               t.nombre AS torneo,
               e.id AS equipo_id,
               e.nombre AS equipo,
               d.id AS disponibilidad_id,
               d.confirmada,
               d.fecha_confirmacion
        FROM partida p
        JOIN torneo t ON t.id = p.torneo_id
        LEFT JOIN persona m ON m.id = p.moderador_id
        JOIN disponibilidad d ON d.partida_id = p.id
        JOIN equipo e ON e.id = d.equipo_id
        ORDER BY p.fecha_hora, e.nombre
        """
    ).fetchall()

    partidas = {}
    for fila in filas:
        partida = partidas.setdefault(
            fila["partida_id"],
            {
                "partida_id": fila["partida_id"],
                "fecha_hora": fila["fecha_hora"],
                "fase": fila["fase"],
                "estado": fila["estado"],
                "moderador_id": fila["moderador_id"],
                "moderador": fila["moderador"],
                "torneo": fila["torneo"],
                "equipos": [],
            },
        )
        partida["equipos"].append(
            {
                "equipo_id": fila["equipo_id"],
                "equipo": fila["equipo"],
                "disponibilidad_id": fila["disponibilidad_id"],
                "confirmada": fila["confirmada"],
                "fecha_confirmacion": fila["fecha_confirmacion"],
            }
        )

    for partida in partidas.values():
        partida["requiere_revision"] = requiere_revision(
            partida["estado"],
            partida["fecha_hora"],
            partida["equipos"],
            ahora,
        )
    return list(partidas.values())


def confirmar_disponibilidad(conexion, disponibilidad_id, persona_id, ahora):
    registro = conexion.execute(
        """
        SELECT d.id, d.confirmada, d.equipo_id, p.estado, t.estado AS torneo_estado
        FROM disponibilidad d
        JOIN partida p ON p.id = d.partida_id
        JOIN torneo t ON t.id = p.torneo_id
        WHERE d.id = ?
        """,
        (disponibilidad_id,),
    ).fetchone()
    if registro is None:
        raise ErrorDisponibilidad(MENSAJE_NO_EXISTE)

    if registro["torneo_estado"] == "Borrador":
        raise ErrorDisponibilidad(
            "No se puede confirmar disponibilidad mientras el torneo esté en estado Borrador."
        )

    persona = conexion.execute(
        "SELECT id, tipo, equipo_id FROM persona WHERE id = ?", (persona_id,)
    ).fetchone()
    if (
        persona is None
        or persona["tipo"] != "Jugador"
        or persona["equipo_id"] != registro["equipo_id"]
    ):
        raise ErrorDisponibilidad(MENSAJE_EQUIPO_AJENO)

    if registro["estado"] != ESTADO_PROGRAMADA:
        raise ErrorDisponibilidad(MENSAJE_FUERA_DE_PLAZO)

    if registro["confirmada"] == DISPONIBILIDAD_CONFIRMADA:
        raise ErrorDisponibilidad(MENSAJE_YA_CONFIRMADA)

    conexion.execute(
        """
        UPDATE disponibilidad
        SET confirmada = ?, fecha_confirmacion = ?
        WHERE id = ?
        """,
        (
            DISPONIBILIDAD_CONFIRMADA,
            ahora.isoformat(timespec="seconds"),
            disponibilidad_id,
        ),
    )

    # Auto-transición: si ambos equipos ya confirmaron, la partida pasa
    # automáticamente a "Pendiente de resultado" para que el Moderador
    # pueda registrar el marcador (simulación real del flujo del torneo).
    partida_id = conexion.execute(
        "SELECT partida_id FROM disponibilidad WHERE id = ?",
        (disponibilidad_id,),
    ).fetchone()["partida_id"]

    pendientes = conexion.execute(
        """
        SELECT COUNT(*) FROM disponibilidad
        WHERE partida_id = ? AND confirmada = ?
        """,
        (partida_id, DISPONIBILIDAD_PENDIENTE),
    ).fetchone()[0]

    if pendientes == 0:
        conexion.execute(
            """
            UPDATE partida SET estado = ?
            WHERE id = ? AND estado = ?
            """,
            (ESTADO_PENDIENTE_RESULTADO, partida_id, ESTADO_PROGRAMADA),
        )

    conexion.commit()
    return disponibilidad_id
