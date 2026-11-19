from datetime import datetime, timedelta

from app.db.conexion import preparar_base

EQUIPOS = [
    ("Equipo Alfa", "Colombia"),
    ("Equipo Bravo", "México"),
    ("Equipo Charlie", "Argentina"),
    ("Equipo Delta", "Chile"),
]

JUGADORES = {
    "Equipo Alfa": [("Ana Ríos", "ana_rios"), ("Beto Salas", "beto_salas")],
    "Equipo Bravo": [("Carla Méndez", "carla_mendez"), ("Diego Paz", "diego_paz")],
    "Equipo Charlie": [("Elena Gómez", "elena_gomez"), ("Fabián Torres", "fabian_torres")],
    "Equipo Delta": [("Gloria Vega", "gloria_vega"), ("Hugo Lara", "hugo_lara")],
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

    cursor = conexion.execute(
        "INSERT INTO torneo (nombre, juego, zona_horaria) VALUES (?, ?, ?)",
        ("Copa E-Sports Focus", "Valorant", "America/Bogota"),
    )
    torneo_id = cursor.lastrowid

    partidas = [
        (equipos["Equipo Alfa"], equipos["Equipo Bravo"], ahora + timedelta(hours=6), "Cuartos de final", "Programada"),
        (equipos["Equipo Charlie"], equipos["Equipo Delta"], ahora + timedelta(hours=30), "Cuartos de final", "Programada"),
        (equipos["Equipo Alfa"], equipos["Equipo Delta"], ahora - timedelta(hours=1), "Cuartos de final", "Programada"),
        (equipos["Equipo Alfa"], equipos["Equipo Charlie"], ahora - timedelta(hours=2), "Semifinal", "En curso"),
        (equipos["Equipo Bravo"], equipos["Equipo Delta"], ahora - timedelta(days=1), "Final", "Anunciada"),
    ]

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
        for equipo_id in (equipo_a, equipo_b):
            conexion.execute(
                "INSERT INTO disponibilidad (equipo_id, partida_id) VALUES (?, ?)",
                (equipo_id, partida_id),
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
