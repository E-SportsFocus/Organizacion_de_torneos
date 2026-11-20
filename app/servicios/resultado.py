import re

from app.integraciones.discord import DiscordSimulado
from app.servicios import anuncio as servicio_anuncio

ESTADO_PENDIENTE = "Pendiente de resultado"
ESTADO_CONFIRMADO = "Resultado confirmado"
ESTADO_ANUNCIADA = "Anunciada"
ORIGEN_MANUAL = "manual"
TIPO_MODERADOR = "Moderador"
TIPO_JUGADOR = "Jugador"
TIPO_ORGANIZADOR = "Organizador"

MENSAJE_NO_EXISTE = "La partida indicada no existe."
MENSAJE_SOLO_MODERADOR = "Solo un Moderador puede registrar el resultado de una partida."
MENSAJE_NO_ASIGNADO = (
    "Solo el Moderador asignado a la partida puede registrar el resultado."
)
MENSAJE_YA_TIENE_RESULTADO = "La partida ya tiene un resultado registrado."
MENSAJE_NO_PENDIENTE = "La partida no está pendiente de resultado."
MENSAJE_SIN_EQUIPOS = "La partida no tiene dos equipos registrados."
MENSAJE_INCOMPLETO = "Completa el resultado de ambos equipos."
MENSAJE_MARCADOR_INVALIDO = (
    "El marcador debe ser un número entero mayor o igual a 0."
)
MENSAJE_EMPATE = "El resultado no puede ser empate; debe haber un ganador."
MENSAJE_REGISTRADO = "Resultado registrado."

_PATRON_ENTERO = re.compile(r"^[0-9]+$")


class ErrorResultado(Exception):
    """Error de negocio al registrar un resultado; su mensaje se muestra al usuario."""

    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje


def equipos_de_partida(conexion, partida_id):
    filas = conexion.execute(
        """
        SELECT e.id AS equipo_id, e.nombre AS equipo
        FROM disponibilidad d
        JOIN equipo e ON e.id = d.equipo_id
        WHERE d.partida_id = ?
        ORDER BY e.nombre
        """,
        (partida_id,),
    ).fetchall()
    return [dict(fila) for fila in filas]


def _convertir_marcador(valor):
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, int):
        return valor if valor >= 0 else None
    texto = str(valor).strip()
    if not _PATRON_ENTERO.match(texto):
        return None
    return int(texto)


def _resumen_marcador(equipos):
    ordenados = sorted(equipos, key=lambda equipo: equipo["equipo"])
    return " - ".join(
        f"{equipo['equipo']} {equipo['marcador']}" for equipo in ordenados
    )


def _notificar(conexion, partida, resultado_id, equipos, ganador, fecha_hora):
    mensaje = (
        f"{MENSAJE_REGISTRADO} {partida['fase']}: {_resumen_marcador(equipos)}. "
        f"Ganador: {ganador['equipo']}. El bracket fue actualizado."
    )

    destinatarios = []
    if partida["organizador_id"] is not None:
        destinatarios.append((TIPO_ORGANIZADOR, partida["organizador_id"]))

    jugadores = conexion.execute(
        """
        SELECT p.id
        FROM persona p
        JOIN disponibilidad d ON d.equipo_id = p.equipo_id
        WHERE d.partida_id = ? AND p.tipo = ?
        ORDER BY p.id
        """,
        (partida["partida_id"], TIPO_JUGADOR),
    ).fetchall()
    for fila in jugadores:
        destinatarios.append((TIPO_JUGADOR, fila["id"]))

    vistos = set()
    for tipo, destinatario_id in destinatarios:
        clave = (tipo, destinatario_id)
        if clave in vistos:
            continue
        vistos.add(clave)
        conexion.execute(
            """
            INSERT INTO notificacion (
                partida_id, resultado_id, destinatario_tipo, destinatario_id,
                canal, mensaje, fecha_hora
            )
            VALUES (?, ?, ?, ?, 'Plataforma', ?, ?)
            """,
            (
                partida["partida_id"],
                resultado_id,
                tipo,
                destinatario_id,
                mensaje,
                fecha_hora,
            ),
        )
    return mensaje, len(vistos)


def _bracket_del_torneo(conexion, torneo_id, fecha_hora):
    fila = conexion.execute(
        "SELECT id FROM bracket WHERE torneo_id = ?", (torneo_id,)
    ).fetchone()
    if fila is None:
        cursor = conexion.execute(
            "INSERT INTO bracket (torneo_id, ultima_actualizacion) VALUES (?, ?)",
            (torneo_id, fecha_hora),
        )
        return cursor.lastrowid
    conexion.execute(
        "UPDATE bracket SET ultima_actualizacion = ? WHERE id = ?",
        (fecha_hora, fila["id"]),
    )
    return fila["id"]


def registrar_resultado(
    conexion, partida_id, persona_id, marcadores, ahora, discord=None
):
    """Registra el resultado manual y aplica la transición de EST-01.

    Valida todo antes de escribir: si algo falla no se modifica la partida.
    """
    partida = conexion.execute(
        """
        SELECT p.id AS partida_id, p.torneo_id, p.moderador_id, p.fase,
               p.estado, t.organizador_id, t.nombre AS torneo
        FROM partida p
        JOIN torneo t ON t.id = p.torneo_id
        WHERE p.id = ?
        """,
        (partida_id,),
    ).fetchone()
    if partida is None:
        raise ErrorResultado(MENSAJE_NO_EXISTE)

    persona = conexion.execute(
        "SELECT id, tipo FROM persona WHERE id = ?", (persona_id,)
    ).fetchone()
    if persona is None or persona["tipo"] != TIPO_MODERADOR:
        raise ErrorResultado(MENSAJE_SOLO_MODERADOR)
    if partida["moderador_id"] != persona["id"]:
        raise ErrorResultado(MENSAJE_NO_ASIGNADO)

    if conexion.execute(
        "SELECT 1 FROM resultado WHERE partida_id = ?", (partida_id,)
    ).fetchone():
        raise ErrorResultado(MENSAJE_YA_TIENE_RESULTADO)
    if partida["estado"] != ESTADO_PENDIENTE:
        raise ErrorResultado(MENSAJE_NO_PENDIENTE)

    equipos = equipos_de_partida(conexion, partida_id)
    if len(equipos) != 2:
        raise ErrorResultado(MENSAJE_SIN_EQUIPOS)

    normalizados = {}
    for clave, valor in (marcadores or {}).items():
        try:
            normalizados[int(clave)] = valor
        except (TypeError, ValueError):
            raise ErrorResultado(MENSAJE_MARCADOR_INVALIDO) from None

    valores = []
    for equipo in equipos:
        valor = normalizados.get(equipo["equipo_id"])
        if valor is None or not str(valor).strip():
            raise ErrorResultado(MENSAJE_INCOMPLETO)
        marcador = _convertir_marcador(valor)
        if marcador is None:
            raise ErrorResultado(MENSAJE_MARCADOR_INVALIDO)
        equipo["marcador"] = marcador
        valores.append(marcador)

    if valores[0] == valores[1]:
        raise ErrorResultado(MENSAJE_EMPATE)

    ganador = max(equipos, key=lambda equipo: equipo["marcador"])
    fecha_hora = ahora.isoformat(timespec="seconds")

    cursor = conexion.execute(
        """
        INSERT INTO resultado (partida_id, moderador_id, fecha_hora_registro, origen)
        VALUES (?, ?, ?, ?)
        """,
        (partida_id, persona_id, fecha_hora, ORIGEN_MANUAL),
    )
    resultado_id = cursor.lastrowid
    for equipo in equipos:
        conexion.execute(
            """
            INSERT INTO resultado_marcador (resultado_id, equipo_id, marcador)
            VALUES (?, ?, ?)
            """,
            (resultado_id, equipo["equipo_id"], equipo["marcador"]),
        )

    bracket_id = _bracket_del_torneo(conexion, partida["torneo_id"], fecha_hora)
    conexion.execute(
        """
        INSERT INTO bracket_actualizacion (bracket_id, resultado_id, fecha_hora)
        VALUES (?, ?, ?)
        """,
        (bracket_id, resultado_id, fecha_hora),
    )

    mensaje, notificaciones = _notificar(
        conexion, partida, resultado_id, equipos, ganador, fecha_hora
    )

    adaptador = discord or DiscordSimulado()
    adaptador.notificar_resultado(conexion, resultado_id, mensaje, fecha_hora)

    marcador_texto = _resumen_marcador(equipos)
    publicacion = servicio_anuncio.publicar_ganador(
        conexion,
        partida,
        resultado_id,
        ganador,
        marcador_texto,
        fecha_hora,
        discord=adaptador,
    )

    conexion.execute(
        "UPDATE partida SET estado = ? WHERE id = ?",
        (ESTADO_ANUNCIADA, partida_id),
    )
    conexion.commit()

    return {
        "resultado_id": resultado_id,
        "partida_id": partida_id,
        "equipos": equipos,
        "ganador": ganador,
        "marcador_texto": marcador_texto,
        "notificaciones": notificaciones,
        "fecha_hora_registro": fecha_hora,
        "estado": ESTADO_ANUNCIADA,
        "publicacion": publicacion,
    }


def resultados_por_partida(conexion):
    """Devuelve los resultados indexados por partida, con marcador y ganador."""
    resultados = {}
    for fila in conexion.execute(
        """
        SELECT r.id AS resultado_id, r.partida_id, r.moderador_id,
               r.fecha_hora_registro, r.origen, m.nombre AS moderador
        FROM resultado r
        JOIN persona m ON m.id = r.moderador_id
        ORDER BY r.id
        """
    ):
        resultados[fila["partida_id"]] = {
            "resultado_id": fila["resultado_id"],
            "partida_id": fila["partida_id"],
            "moderador_id": fila["moderador_id"],
            "moderador": fila["moderador"],
            "fecha_hora_registro": fila["fecha_hora_registro"],
            "origen": fila["origen"],
            "equipos": [],
        }

    por_resultado = {
        resultado["resultado_id"]: resultado for resultado in resultados.values()
    }
    for fila in conexion.execute(
        """
        SELECT rm.resultado_id, rm.equipo_id, rm.marcador, e.nombre AS equipo
        FROM resultado_marcador rm
        JOIN equipo e ON e.id = rm.equipo_id
        JOIN resultado r ON r.id = rm.resultado_id
        ORDER BY r.partida_id, e.nombre
        """
    ):
        resultado = por_resultado.get(fila["resultado_id"])
        if resultado is not None:
            resultado["equipos"].append(
                {
                    "equipo_id": fila["equipo_id"],
                    "equipo": fila["equipo"],
                    "marcador": fila["marcador"],
                }
            )

    for resultado in resultados.values():
        if resultado["equipos"]:
            resultado["ganador"] = max(
                resultado["equipos"], key=lambda equipo: equipo["marcador"]
            )
            resultado["marcador_texto"] = _resumen_marcador(resultado["equipos"])
        else:
            resultado["ganador"] = None
            resultado["marcador_texto"] = ""
        resultado["marcadores"] = {
            equipo["equipo_id"]: equipo["marcador"]
            for equipo in resultado["equipos"]
        }
    return resultados


def listar_bracket(conexion, torneo_id):
    partidas = conexion.execute(
        """
        SELECT id AS partida_id, fecha_hora, fase, estado
        FROM partida
        WHERE torneo_id = ?
        ORDER BY fecha_hora, id
        """,
        (torneo_id,),
    ).fetchall()
    resultados = resultados_por_partida(conexion)
    bracket = []
    for fila in partidas:
        partida = dict(fila)
        partida["resultado"] = resultados.get(partida["partida_id"])
        partida["equipos"] = equipos_de_partida(conexion, partida["partida_id"])
        bracket.append(partida)
    return bracket


def historial_bracket(conexion, torneo_id):
    filas = conexion.execute(
        """
        SELECT ba.fecha_hora, ba.resultado_id, r.partida_id,
               p.fase, p.fecha_hora AS fecha_partida
        FROM bracket_actualizacion ba
        JOIN bracket b ON b.id = ba.bracket_id
        JOIN resultado r ON r.id = ba.resultado_id
        JOIN partida p ON p.id = r.partida_id
        WHERE b.torneo_id = ?
        ORDER BY ba.fecha_hora DESC, ba.id DESC
        """,
        (torneo_id,),
    ).fetchall()
    resultados = resultados_por_partida(conexion)
    historial = []
    for fila in filas:
        registro = dict(fila)
        resultado = resultados.get(registro["partida_id"])
        registro["marcador_texto"] = resultado["marcador_texto"] if resultado else ""
        registro["ganador"] = resultado["ganador"] if resultado else None
        historial.append(registro)
    return historial
