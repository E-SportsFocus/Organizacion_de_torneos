CREATE TABLE disponibilidad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipo_id INTEGER NOT NULL REFERENCES equipo (id),
    partida_id INTEGER NOT NULL REFERENCES partida (id) ON DELETE CASCADE,
    confirmada TEXT NOT NULL DEFAULT 'Pendiente' CHECK (
        confirmada IN ('Pendiente', 'Confirmada')
    ),
    fecha_confirmacion TEXT,
    UNIQUE (equipo_id, partida_id)
);
