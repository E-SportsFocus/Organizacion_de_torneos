from datetime import datetime, timedelta

from app.db.conexion import preparar_base

EQUIPOS = [
    ("Equipo Alfa", "Colombia"),
    ("Equipo Bravo", "México"),
    ("Equipo Charlie", "Argentina"),
    ("Equipo Delta", "Chile"),
    ("Equipo Eco", "Perú"),
    ("Equipo Foxtrot", "Brasil"),
    ("Equipo Golf", "Uruguay"),
    ("Equipo Hotel", "Ecuador"),
]

JUGADORES = {
    "Equipo Alfa": [("Ana Ríos", "ana_rios"), ("Beto Salas", "beto_salas")],
    "Equipo Bravo": [("Carla Méndez", "carla_mendez"), ("Diego Paz", "diego_paz")],
    "Equipo Charlie": [("Elena Gómez", "elena_gomez"), ("Fabián Torres", "fabian_torres")],
    "Equipo Delta": [("Gloria Vega", "gloria_vega"), ("Hugo Lara", "hugo_lara")],
    "Equipo Eco": [("Ignacio Soto", "ignacio_soto"), ("Julia Mora", "julia_mora")],
    "Equipo Foxtrot": [("Kevin Rivas", "kevin_rivas"), ("Lorena Cruz", "lorena_cruz")],
    "Equipo Golf": [("Mateo Silva", "mateo_silva"), ("Natalia Ortiz", "natalia_ortiz")],
    "Equipo Hotel": [("Oscar Benítez", "oscar_benitez"), ("Paula Vargas", "paula_vargas")],
}


def sembrar(conexion, ahora=None):
    ahora = (ahora or datetime.now()).replace(microsecond=0)
    if conexion.execute("SELECT COUNT(*) FROM torneo").fetchone()[0]:
        return False

    equipos = {}
    for nombre, pais in EQUIPOS:
        cursor = conexion.execute(
            "INSERT INTO equipo (nombre, pais) VALUES (?, ?)", (nombre, pais)
        )
        equipos[nombre] = cursor.lastrowid

    for equipo, jugadores in JUGADORES.items():
        for nombre, nickname in jugadores:
            conexion.execute(
                """
                INSERT INTO persona (nombre, cuenta_discord, tipo, nickname, pais, equipo_id)
                VALUES (?, ?, 'Jugador', ?, ?, ?)
                """,
                (nombre, nickname, nickname, "—", equipos[equipo]),
            )

    cursor = conexion.execute(
        "INSERT INTO persona (nombre, cuenta_discord, tipo) VALUES (?, ?, 'Moderador')",
        ("Marta Arbitraje", "marta_arbitraje"),
    )
    moderador_id = cursor.lastrowid

    conexion.execute(
        "INSERT INTO persona (nombre, cuenta_discord, tipo) VALUES (?, ?, 'Moderador')",
        ("Óscar Réplica", "oscar_replica"),
    )

    cursor = conexion.execute(
        "INSERT INTO persona (nombre, cuenta_discord, tipo) VALUES (?, ?, 'Organizador')",
        ("Olga Organización", "olga_organizacion"),
    )
    organizador_id = cursor.lastrowid

    cursor = conexion.execute(
        "INSERT INTO torneo (nombre, juego, zona_horaria, organizador_id) VALUES (?, ?, ?, ?)",
        ("Copa E-Sports Focus", "Valorant", "America/Bogota", organizador_id),
    )
    torneo_id = cursor.lastrowid

    conexion.execute(
        "INSERT INTO bracket (torneo_id, ultima_actualizacion) VALUES (?, ?)",
        (torneo_id, ahora.isoformat(timespec="seconds")),
    )

    # Inicia la simulación únicamente con las 4 llaves de Cuartos de final
    # listas para ser moderadas. Semifinal y Final se construirán dinámicamente
    # a medida que el moderador registre los resultados.
    partidas = [
        (equipos["Equipo Alfa"], equipos["Equipo Bravo"], ahora + timedelta(hours=2), "Cuartos de final", "Pendiente de resultado"),
        (equipos["Equipo Charlie"], equipos["Equipo Delta"], ahora + timedelta(hours=4), "Cuartos de final", "Pendiente de resultado"),
        (equipos["Equipo Eco"], equipos["Equipo Foxtrot"], ahora + timedelta(hours=6), "Cuartos de final", "Pendiente de resultado"),
        (equipos["Equipo Golf"], equipos["Equipo Hotel"], ahora + timedelta(hours=8), "Cuartos de final", "Pendiente de resultado"),
    ]

    partidas_ids = []
    for equipo_a, equipo_b, fecha_hora, fase, estado in partidas:
        cursor = conexion.execute(
            """
            INSERT INTO partida (torneo_id, moderador_id, fecha_hora, fase, estado)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                torneo_id,
                moderador_id,
                fecha_hora.isoformat(timespec="minutes"),
                fase,
                estado,
            ),
        )
        partida_id = cursor.lastrowid
        partidas_ids.append(partida_id)
        for equipo_id in (equipo_a, equipo_b):
            conexion.execute(
                """
                INSERT INTO disponibilidad (equipo_id, partida_id, confirmada, fecha_confirmacion)
                VALUES (?, ?, 'Confirmada', ?)
                """,
                (equipo_id, partida_id, ahora.isoformat(timespec="seconds")),
            )

    # Sembrar una solicitud de cambio de horario de ejemplo para Charlie vs Delta (HU-05)
    charlie_jugador = conexion.execute(
        "SELECT id FROM persona WHERE equipo_id = ? LIMIT 1",
        (equipos["Equipo Charlie"],),
    ).fetchone()["id"]
    conexion.execute(
        """
        INSERT INTO solicitud_cambio_horario (
            partida_id, equipo_id, solicitante_id, nuevo_horario,
            fecha_solicitud, estado
        )
        VALUES (?, ?, ?, ?, ?, 'Solicitada')
        """,
        (
            partidas_ids[1],
            equipos["Equipo Charlie"],
            charlie_jugador,
            (ahora + timedelta(days=2, hours=4)).isoformat(timespec="minutes"),
            (ahora - timedelta(hours=1)).isoformat(timespec="seconds"),
        ),
    )

    conexion.commit()
    return True


def main():
    conexion = preparar_base()
    creado = sembrar(conexion)
    conexion.close()
    if creado:
        print("Datos de ejemplo cargados en data/app.db")
    else:
        print("Los datos de ejemplo ya estaban cargados")


if __name__ == "__main__":
    main()
