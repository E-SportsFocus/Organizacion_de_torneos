-- Alinear `resultado.moderador_id` con la multiplicidad 0..1 del modelo de dominio:
-- un resultado automático (HU-01) no tiene Moderador y el manual (HU-03) siempre lo informa.
-- SQLite no permite quitar NOT NULL con ALTER TABLE, así que se recrea la tabla.

PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE resultado_nueva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partida_id INTEGER NOT NULL UNIQUE REFERENCES partida (id) ON DELETE CASCADE,
    moderador_id INTEGER REFERENCES persona (id),
    fecha_hora_registro TEXT NOT NULL,
    origen TEXT NOT NULL DEFAULT 'manual' CHECK (origen IN ('manual', 'automatico'))
);

INSERT INTO resultado_nueva (id, partida_id, moderador_id, fecha_hora_registro, origen)
SELECT id, partida_id, moderador_id, fecha_hora_registro, origen
FROM resultado;

DROP TABLE resultado;

ALTER TABLE resultado_nueva RENAME TO resultado;

COMMIT;
PRAGMA foreign_keys = ON;
