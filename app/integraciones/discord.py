import json


class Discord:
    """Interfaz del canal de Discord usado para simular el aviso del resultado."""

    def notificar_resultado(self, conexion, resultado_id, mensaje, fecha_hora):
        raise NotImplementedError


class DiscordSimulado(Discord):
    """Simulación local: no hay red; cada llamada queda en `integraciones_log`."""

    def notificar_resultado(self, conexion, resultado_id, mensaje, fecha_hora):
        detalle = json.dumps(
            {"resultado_id": resultado_id, "mensaje": mensaje},
            ensure_ascii=False,
        )
        conexion.execute(
            """
            INSERT INTO integraciones_log (sistema, operacion, detalle, fecha_hora)
            VALUES ('Discord', 'notificar_resultado', ?, ?)
            """,
            (detalle, fecha_hora),
        )
        return True
