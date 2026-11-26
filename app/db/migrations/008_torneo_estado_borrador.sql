-- Normaliza los torneos creados antes de validar el catálogo de estados.
-- El seed anterior guardaba `torneo.estado` vacío; el estado inicial válido es Borrador.

UPDATE torneo
SET estado = 'Borrador'
WHERE estado IS NULL OR TRIM(estado) = '';
