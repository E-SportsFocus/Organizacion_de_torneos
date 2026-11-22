from datetime import datetime, timedelta

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.servicios import cambio_horario as servicio_cambio
from app.servicios import disponibilidad as servicio

MENSAJE_CONFIRMADA_OK = "Disponibilidad del equipo confirmada."


def _formatear_fecha(valor):
    return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")


def crear_router(templates, abrir_conexion, reloj):
    router = APIRouter()

    def _persona(conexion, persona_id):
        return conexion.execute(
            """
            SELECT p.id, p.nombre, p.tipo, e.id AS equipo_id, e.nombre AS equipo
            FROM persona p
            LEFT JOIN equipo e ON e.id = p.equipo_id
            WHERE p.id = ?
            """,
            (persona_id,),
        ).fetchone()

    def _contexto_jugador(conexion, persona, mensaje=None, error=None):
        ahora = reloj()
        partidas = servicio.listar_partidas_equipo(
            conexion, persona["equipo_id"], ahora
        )
        for partida in partidas:
            partida["fecha_texto"] = _formatear_fecha(partida["fecha_hora"])
            f_dt = datetime.fromisoformat(partida["fecha_hora"])
            partida["puede_solicitar_cambio"] = (
                partida["estado"] == "Programada"
                and ahora < f_dt - timedelta(hours=2)
            )

        solicitudes = servicio_cambio.listar_solicitudes_equipo(
            conexion, persona["equipo_id"], ahora
        )
        for s in solicitudes:
            s["fecha_solicitud_texto"] = _formatear_fecha(s["fecha_solicitud"])
            s["nuevo_horario_texto"] = _formatear_fecha(s["nuevo_horario"])
            s["partida_fecha_texto"] = _formatear_fecha(s["partida_fecha_hora"])

        return {
            "persona": dict(persona),
            "partidas": partidas,
            "solicitudes": solicitudes,
            "mensaje": mensaje,
            "error": error,
        }

    @router.get("/jugador", response_class=HTMLResponse)
    def vista_jugador(
        request: Request, persona_id: int | None = None, mensaje: str | None = None
    ):
        if persona_id is None:
            return RedirectResponse(url="/", status_code=303)
        with abrir_conexion() as conexion:
            persona = _persona(conexion, persona_id)
            if persona is None:
                raise HTTPException(status_code=404, detail="Jugador no encontrado")
            msg_texto = MENSAJE_CONFIRMADA_OK if mensaje == "ok" else mensaje
            contexto = _contexto_jugador(
                conexion,
                persona,
                mensaje=msg_texto,
            )
        return templates.TemplateResponse(
            request=request, name="jugador.html", context=contexto
        )

    @router.post("/disponibilidad/{disponibilidad_id}/confirmar", response_class=HTMLResponse)
    def confirmar(
        request: Request, disponibilidad_id: int, persona_id: int = Form(...)
    ):
        with abrir_conexion() as conexion:
            try:
                servicio.confirmar_disponibilidad(
                    conexion, disponibilidad_id, persona_id, reloj()
                )
            except servicio.ErrorDisponibilidad as error:
                persona = _persona(conexion, persona_id)
                if persona is None:
                    raise HTTPException(status_code=404, detail="Jugador no encontrado")
                contexto = _contexto_jugador(conexion, persona, error=error.mensaje)
                return templates.TemplateResponse(
                    request=request,
                    name="jugador.html",
                    context=contexto,
                    status_code=400,
                )
        return RedirectResponse(
            url=f"/jugador?persona_id={persona_id}&mensaje=ok", status_code=303
        )

    return router
