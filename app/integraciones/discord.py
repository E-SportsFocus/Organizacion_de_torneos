import json


class Discord:
    """Interfaz del canal de Discord usado para simular los avisos del torneo."""

    def notificar_resultado(self, conexion, resultado_id, mensaje, fecha_hora):
        raise NotImplementedError

    def anunciar_ganador(self, conexion, partida, ganador, marcador_texto, fecha_hora):
        raise NotImplementedError

    def avisar_solicitud_cambio(self, conexion, partida_id, equipo, nuevo_horario, fecha_hora):
        raise NotImplementedError

    def avisar_resolucion_cambio(self, conexion, partida_id, estado, nuevo_horario, motivo, fecha_hora):
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

    def anunciar_ganador(self, conexion, partida, ganador, marcador_texto, fecha_hora):
        mensaje = (
            f"Anuncio del ganador en {partida['torneo']}: "
            f"{ganador['equipo']} ({marcador_texto}) en {partida['fase']}."
        )
        detalle = json.dumps(
            {
                "partida_id": partida["partida_id"],
                "ganador": ganador["equipo"],
                "marcador": marcador_texto,
                "mensaje": mensaje,
            },
            ensure_ascii=False,
        )
        conexion.execute(
            """
            INSERT INTO integraciones_log (sistema, operacion, detalle, fecha_hora)
            VALUES ('Discord', 'anunciar_ganador', ?, ?)
            """,
            (detalle, fecha_hora),
        )
        return True

    def avisar_solicitud_cambio(self, conexion, partida_id, equipo, nuevo_horario, fecha_hora):
        mensaje = f"Aviso en canal de Discord: {equipo} solicitó cambio de horario para la partida #{partida_id} proponiendo {nuevo_horario}."
        detalle = json.dumps(
            {
                "partida_id": partida_id,
                "equipo": equipo,
                "nuevo_horario": nuevo_horario,
                "mensaje": mensaje,
            },
            ensure_ascii=False,
        )
        conexion.execute(
            """
            INSERT INTO integraciones_log (sistema, operacion, detalle, fecha_hora)
            VALUES ('Discord', 'aviso_solicitud_cambio', ?, ?)
            """,
            (detalle, fecha_hora),
        )
        return True

    def avisar_resolucion_cambio(self, conexion, partida_id, estado, nuevo_horario, motivo, fecha_hora):
        if estado == "Aprobada":
            mensaje = f"Aviso en canal de Discord: Partida #{partida_id} reprogramada con éxito. Nuevo horario: {nuevo_horario}."
        else:
            mensaje = f"Aviso en canal de Discord: Solicitud de cambio de horario para la partida #{partida_id} rechazada. Motivo: {motivo}."
        detalle = json.dumps(
            {
                "partida_id": partida_id,
                "estado": estado,
                "nuevo_horario": nuevo_horario,
                "motivo": motivo,
                "mensaje": mensaje,
            },
            ensure_ascii=False,
        )
        conexion.execute(
            """
            INSERT INTO integraciones_log (sistema, operacion, detalle, fecha_hora)
            VALUES ('Discord', 'aviso_resolucion_cambio', ?, ?)
            """,
            (detalle, fecha_hora),
        )
        return True
