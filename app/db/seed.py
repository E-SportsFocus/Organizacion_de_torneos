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
    moderador_marta_id = cursor.lastrowid

    cursor = conexion.execute(
        "INSERT INTO persona (nombre, cuenta_discord, tipo) VALUES (?, ?, 'Moderador')",
        ("Óscar Réplica", "oscar_replica"),
    )
    moderador_oscar_id = cursor.lastrowid

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

    # Simulación real: solo Cuartos de final en estado "Programada" con
    # disponibilidad "Pendiente". Los jugadores deben confirmar su disponibilidad
    # antes de que el moderador pueda registrar resultados.
    # Marta modera las llaves 1 y 2; Óscar modera las llaves 3 y 4.
    partidas = [
        (equipos["Equipo Alfa"], equipos["Equipo Bravo"], ahora + timedelta(hours=6), "Cuartos de final", moderador_marta_id),
        (equipos["Equipo Charlie"], equipos["Equipo Delta"], ahora + timedelta(hours=8), "Cuartos de final", moderador_marta_id),
        (equipos["Equipo Eco"], equipos["Equipo Foxtrot"], ahora + timedelta(hours=10), "Cuartos de final", moderador_oscar_id),
        (equipos["Equipo Golf"], equipos["Equipo Hotel"], ahora + timedelta(hours=12), "Cuartos de final", moderador_oscar_id),
    ]

    for equipo_a, equipo_b, fecha_hora, fase, mod_id in partidas:
        cursor = conexion.execute(
            """
            INSERT INTO partida (torneo_id, moderador_id, fecha_hora, fase, estado)
            VALUES (?, ?, ?, ?, 'Programada')
            """,
            (
                torneo_id,
                mod_id,
                fecha_hora.isoformat(timespec="minutes"),
                fase,
            ),
        )
        partida_id = cursor.lastrowid
        # Disponibilidad queda en "Pendiente" por defecto (sin confirmar)
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
