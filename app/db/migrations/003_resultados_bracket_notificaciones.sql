-- HU-03: resultado manual, bracket con historial y notificaciones.

PRAGMA foreign_keys = OFF;
BEGIN;

-- `persona.tipo` debe admitir al Organizador. SQLite no permite modificar un
-- CHECK con ALTER TABLE, así que se recrea la tabla conservando sus datos.
CREATE TABLE persona_nueva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cuenta_discord TEXT,
    tipo TEXT NOT NULL CHECK (tipo IN ('Jugador', 'Moderador', 'Organizador')),
    nickname TEXT,
    pais TEXT,
    equipo_id INTEGER REFERENCES equipo (id)
);

INSERT INTO persona_nueva (id, nombre, cuenta_discord, tipo, nickname, pais, equipo_id)
SELECT id, nombre, cuenta_discord, tipo, nickname, pais, equipo_id
FROM persona;

DROP TABLE persona;

ALTER TABLE persona_nueva RENAME TO persona;

-- Organizador 1 - 0..* Torneo
ALTER TABLE torneo ADD COLUMN organizador_id INTEGER REFERENCES persona (id);

CREATE TABLE resultado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partida_id INTEGER NOT NULL UNIQUE REFERENCES partida (id) ON DELETE CASCADE,
    moderador_id INTEGER NOT NULL REFERENCES persona (id),
    fecha_hora_registro TEXT NOT NULL,
    origen TEXT NOT NULL DEFAULT 'manual' CHECK (origen IN ('manual', 'automatico'))
);

CREATE TABLE resultado_marcador (
    resultado_id INTEGER NOT NULL REFERENCES resultado (id) ON DELETE CASCADE,
    equipo_id INTEGER NOT NULL REFERENCES equipo (id),
    marcador INTEGER NOT NULL CHECK (marcador >= 0),
    PRIMARY KEY (resultado_id, equipo_id)
);

CREATE TABLE bracket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torneo_id INTEGER NOT NULL UNIQUE REFERENCES torneo (id) ON DELETE CASCADE,
    ultima_actualizacion TEXT
);

CREATE TABLE bracket_actualizacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bracket_id INTEGER NOT NULL REFERENCES bracket (id) ON DELETE CASCADE,
    resultado_id INTEGER NOT NULL UNIQUE REFERENCES resultado (id) ON DELETE CASCADE,
    fecha_hora TEXT NOT NULL
);

CREATE TABLE notificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partida_id INTEGER NOT NULL REFERENCES partida (id) ON DELETE CASCADE,
    resultado_id INTEGER NOT NULL REFERENCES resultado (id) ON DELETE CASCADE,
    destinatario_tipo TEXT NOT NULL CHECK (destinatario_tipo IN ('Organizador', 'Jugador')),
    destinatario_id INTEGER NOT NULL REFERENCES persona (id),
    canal TEXT NOT NULL DEFAULT 'Plataforma' CHECK (canal IN ('Plataforma', 'Discord')),
    mensaje TEXT NOT NULL,
    fecha_hora TEXT NOT NULL,
    leida INTEGER NOT NULL DEFAULT 0 CHECK (leida IN (0, 1))
);

CREATE TABLE integraciones_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sistema TEXT NOT NULL,
    operacion TEXT NOT NULL,
    detalle TEXT,
    fecha_hora TEXT NOT NULL
);

CREATE INDEX idx_resultado_marcador_equipo ON resultado_marcador (equipo_id);
CREATE INDEX idx_bracket_actualizacion_bracket ON bracket_actualizacion (bracket_id);
CREATE INDEX idx_notificacion_destinatario ON notificacion (destinatario_tipo, destinatario_id);
CREATE INDEX idx_notificacion_partida ON notificacion (partida_id);

COMMIT;
PRAGMA foreign_keys = ON;
