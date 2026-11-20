-- HU-06: anuncio del ganador y estado del envío a Discord.

BEGIN;

CREATE TABLE anuncio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partida_id INTEGER NOT NULL UNIQUE REFERENCES partida (id) ON DELETE CASCADE,
    resultado_id INTEGER NOT NULL UNIQUE REFERENCES resultado (id) ON DELETE CASCADE,
    fecha_hora_publicacion TEXT NOT NULL,
    discord_estado TEXT NOT NULL CHECK (discord_estado IN ('Enviado', 'Pendiente')),
    discord_fecha_hora TEXT,
    discord_detalle TEXT
);

CREATE INDEX idx_anuncio_discord_estado ON anuncio (discord_estado);
CREATE INDEX idx_anuncio_fecha_publicacion ON anuncio (fecha_hora_publicacion);

-- Relleno para las partidas que ya estaban anunciadas antes de HU-06.
INSERT INTO anuncio (
    partida_id, resultado_id, fecha_hora_publicacion,
    discord_estado, discord_fecha_hora, discord_detalle
)
SELECT p.id, r.id, r.fecha_hora_registro,
       'Enviado', r.fecha_hora_registro, 'Anuncio previo a HU-06'
FROM partida p
JOIN resultado r ON r.partida_id = p.id
WHERE p.estado = 'Anunciada'
  AND NOT EXISTS (
      SELECT 1 FROM anuncio a WHERE a.partida_id = p.id
  );

COMMIT;
