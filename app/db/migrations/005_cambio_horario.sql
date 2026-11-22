-- HU-05: Solicitud de cambio de horario

CREATE TABLE solicitud_cambio_horario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partida_id INTEGER NOT NULL REFERENCES partida (id) ON DELETE CASCADE,
    equipo_id INTEGER NOT NULL REFERENCES equipo (id),
    solicitante_id INTEGER NOT NULL REFERENCES persona (id),
    nuevo_horario TEXT NOT NULL,
    fecha_solicitud TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Solicitada' CHECK (
        estado IN ('Solicitada', 'Aprobada', 'Rechazada', 'Vencida')
    ),
    motivo_rechazo TEXT,
    fecha_resolucion TEXT,
    moderador_id INTEGER REFERENCES persona (id)
);

CREATE INDEX idx_solicitud_partida ON solicitud_cambio_horario (partida_id);
CREATE INDEX idx_solicitud_equipo ON solicitud_cambio_horario (equipo_id);
CREATE INDEX idx_solicitud_estado ON solicitud_cambio_horario (estado);
