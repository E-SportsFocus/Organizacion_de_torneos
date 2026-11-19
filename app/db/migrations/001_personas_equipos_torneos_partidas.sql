CREATE TABLE equipo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    pais TEXT NOT NULL
);

CREATE TABLE torneo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    juego TEXT NOT NULL,
    zona_horaria TEXT NOT NULL
);

CREATE TABLE persona (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cuenta_discord TEXT,
    tipo TEXT NOT NULL CHECK (tipo IN ('Jugador', 'Moderador')),
    nickname TEXT,
    pais TEXT,
    equipo_id INTEGER REFERENCES equipo (id)
);

CREATE TABLE partida (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torneo_id INTEGER NOT NULL REFERENCES torneo (id) ON DELETE CASCADE,
    moderador_id INTEGER REFERENCES persona (id),
    fecha_hora TEXT NOT NULL,
    fase TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Programada' CHECK (
        estado IN (
            'Programada',
            'En curso',
            'Pendiente de resultado',
            'Resultado confirmado',
            'Anunciada'
        )
    )
);
