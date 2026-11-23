-- HU-09: Gestión de torneos, premios y equipos participantes

ALTER TABLE torneo ADD COLUMN fecha_inicio TEXT;
ALTER TABLE torneo ADD COLUMN descripcion TEXT;
ALTER TABLE torneo ADD COLUMN estado TEXT DEFAULT 'En curso';
ALTER TABLE torneo ADD COLUMN bolsa_premios TEXT;

CREATE TABLE premio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torneo_id INTEGER NOT NULL REFERENCES torneo (id) ON DELETE CASCADE,
    posicion INTEGER NOT NULL,
    posicion_texto TEXT NOT NULL,
    monto_texto TEXT NOT NULL,
    descripcion TEXT
);

CREATE TABLE torneo_equipo (
    torneo_id INTEGER NOT NULL REFERENCES torneo (id) ON DELETE CASCADE,
    equipo_id INTEGER NOT NULL REFERENCES equipo (id) ON DELETE CASCADE,
    fecha_inscripcion TEXT NOT NULL,
    PRIMARY KEY (torneo_id, equipo_id)
);
