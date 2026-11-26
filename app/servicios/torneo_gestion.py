"""Servicio para la creación y gestión integral de torneos, participantes y premios (HU-09)."""

from datetime import datetime


class ErrorGestionTorneo(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(mensaje)


ESTADOS_TORNEO = (
    "Borrador",
    "Inscripciones abiertas",
    "En curso",
    "Finalizado",
)


def listar_equipos_con_jugadores(conexion):
    """Devuelve todos los equipos registrados con sus integrantes."""
    filas = conexion.execute(
        """
        SELECT e.id AS equipo_id, e.nombre AS equipo_nombre, e.pais AS equipo_pais,
               p.id AS jugador_id, p.nombre AS jugador_nombre, p.nickname, p.cuenta_discord
        FROM equipo e
        LEFT JOIN persona p ON p.equipo_id = e.id AND p.tipo = 'Jugador'
        ORDER BY e.nombre, p.nombre
        """
    ).fetchall()

    equipos = {}
    for f in filas:
        eq_id = f["equipo_id"]
        if eq_id not in equipos:
            equipos[eq_id] = {
                "id": eq_id,
                "nombre": f["equipo_nombre"],
                "pais": f["equipo_pais"],
                "jugadores": [],
            }
        if f["jugador_id"]:
            equipos[eq_id]["jugadores"].append(
                {
                    "id": f["jugador_id"],
                    "nombre": f["jugador_nombre"],
                    "nickname": f["nickname"],
                    "cuenta_discord": f["cuenta_discord"],
                }
            )
    return list(equipos.values())


def obtener_premios_torneo(conexion, torneo_id):
    """Devuelve los premios asociados a un torneo ordenados por posición."""
    return [
        dict(fila)
        for fila in conexion.execute(
            """
            SELECT id, torneo_id, posicion, posicion_texto, monto_texto, descripcion
            FROM premio
            WHERE torneo_id = ?
            ORDER BY posicion ASC
            """,
            (torneo_id,),
        ).fetchall()
    ]


def obtener_equipos_inscritos(conexion, torneo_id):
    """Devuelve los equipos formalmente inscritos en el torneo."""
    filas = conexion.execute(
        """
        SELECT e.id, e.nombre, e.pais, te.fecha_inscripcion
        FROM torneo_equipo te
        JOIN equipo e ON e.id = te.equipo_id
        WHERE te.torneo_id = ?
        ORDER BY e.nombre
        """,
        (torneo_id,),
    ).fetchall()

    todos = {eq["id"]: eq for eq in listar_equipos_con_jugadores(conexion)}
    resultado = []
    for f in filas:
        eq = dict(f)
        eq["jugadores"] = todos.get(f["id"], {}).get("jugadores", [])
        resultado.append(eq)
    return resultado


def validar_datos_torneo(nombre, juego, fecha_inicio, zona_horaria, estado=None):
    """Valida los campos obligatorios y el catálogo de estados del torneo."""
    if not nombre or not nombre.strip():
        raise ErrorGestionTorneo("El nombre del torneo es obligatorio.")
    if len(nombre.strip()) < 3:
        raise ErrorGestionTorneo("El nombre del torneo debe tener al menos 3 caracteres.")
    if not juego or not juego.strip():
        raise ErrorGestionTorneo("El videojuego es obligatorio.")
    if not zona_horaria or not zona_horaria.strip():
        raise ErrorGestionTorneo("La zona horaria es obligatoria.")
    if estado is None:
        estado = "Borrador"
    if estado not in ESTADOS_TORNEO:
        raise ErrorGestionTorneo(
            "El estado del torneo no es válido. "
            "Usa Borrador, Inscripciones abiertas, En curso o Finalizado."
        )


def crear_o_actualizar_torneo(
    conexion,
    organizador_id,
    torneo_id=None,
    nombre="",
    juego="Valorant",
    fecha_inicio=None,
    zona_horaria="America/Bogota",
    descripcion="",
    estado="Borrador",
    bolsa_premios="",
    premios=None,
    equipos_ids=None,
    ahora=None,
):
    """Crea o actualiza un torneo con sus premios e inscripciones."""
    ahora = ahora or datetime.now()
    validar_datos_torneo(nombre, juego, fecha_inicio, zona_horaria, estado)

    if torneo_id:
        conexion.execute(
            """
            UPDATE torneo
            SET nombre = ?, juego = ?, fecha_inicio = ?, zona_horaria = ?,
                descripcion = ?, estado = ?, bolsa_premios = ?
            WHERE id = ?
            """,
            (
                nombre.strip(),
                juego.strip(),
                fecha_inicio or ahora.strftime("%Y-%m-%dT%H:%M"),
                zona_horaria.strip(),
                descripcion.strip() if descripcion else "",
                estado or "Borrador",
                bolsa_premios.strip() if bolsa_premios else "",
                torneo_id,
            ),
        )
    else:
        cursor = conexion.execute(
            """
            INSERT INTO torneo (nombre, juego, zona_horaria, organizador_id, fecha_inicio, descripcion, estado, bolsa_premios)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                nombre.strip(),
                juego.strip(),
                zona_horaria.strip(),
                organizador_id,
                fecha_inicio or ahora.strftime("%Y-%m-%dT%H:%M"),
                descripcion.strip() if descripcion else "",
                estado or "Borrador",
                bolsa_premios.strip() if bolsa_premios else "",
            ),
        )
        torneo_id = cursor.lastrowid
        # Bracket inicial asociado
        conexion.execute(
            "INSERT INTO bracket (torneo_id, ultima_actualizacion) VALUES (?, ?)",
            (torneo_id, ahora.isoformat(timespec="seconds")),
        )

    # Actualizar o insertar premios
    if premios is not None:
        conexion.execute("DELETE FROM premio WHERE torneo_id = ?", (torneo_id,))
        for p in premios:
            pos = int(p.get("posicion", 1))
            pos_txt = p.get("posicion_texto", f"{pos}.º Lugar")
            monto = p.get("monto_texto", "").strip()
            desc = p.get("descripcion", "").strip()
            if monto or desc:
                conexion.execute(
                    """
                    INSERT INTO premio (torneo_id, posicion, posicion_texto, monto_texto, descripcion)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (torneo_id, pos, pos_txt, monto, desc),
                )

    # Actualizar o insertar inscripciones de equipos
    if equipos_ids is not None:
        conexion.execute("DELETE FROM torneo_equipo WHERE torneo_id = ?", (torneo_id,))
        for eq_id in equipos_ids:
            conexion.execute(
                """
                INSERT INTO torneo_equipo (torneo_id, equipo_id, fecha_inscripcion)
                VALUES (?, ?, ?)
                """,
                (torneo_id, int(eq_id), ahora.isoformat(timespec="seconds")),
            )

    conexion.commit()
    return torneo_id
