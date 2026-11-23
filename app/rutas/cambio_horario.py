from datetime import datetime, timedelta
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.servicios import cambio_horario as servicio
from app.servicios import disponibilidad as servicio_disp


def _formatear_fecha(valor):
    try:
        return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(valor)


def crear_router(abrir_conexion, reloj, discord=None, templates=None):
    router = APIRouter(prefix="/cambio-horario", tags=["cambio-horario"])

    @router.post("/solicitar")
    def solicitar(
        request: Request,
        persona_id: int = Form(...),
        partida_id: int = Form(...),
        nuevo_horario: str = Form(...),
    ):
        with abrir_conexion() as conexion:
            try:
                servicio.solicitar_cambio_horario(
                    conexion,
                    partida_id=partida_id,
                    jugador_id=persona_id,
                    nuevo_horario=nuevo_horario,
                    ahora=reloj(),
                    discord=discord,
                )
            except servicio.ErrorCambioHorario as error:
                if templates:
                    persona = conexion.execute(
                        """
                        SELECT p.id, p.nombre, p.tipo, e.id AS equipo_id, e.nombre AS equipo
                        FROM persona p
                        LEFT JOIN equipo e ON e.id = p.equipo_id
                        WHERE p.id = ?
                        """,
                        (persona_id,),
                    ).fetchone()
                    if persona:
                        ahora = reloj()
                        partidas = servicio_disp.listar_partidas_equipo(
                            conexion, persona["equipo_id"], ahora
                        )
                        for p in partidas:
                            p["fecha_texto"] = _formatear_fecha(p["fecha_hora"])
                            f_dt = datetime.fromisoformat(p["fecha_hora"])
                            p["puede_solicitar_cambio"] = (
                                p["estado"] == "Programada"
                                and p.get("confirmada") == "Pendiente"
                                and ahora < f_dt - timedelta(hours=2)
                            )
                            p["min_nuevo_horario"] = (ahora + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M")

                        solicitudes = servicio.listar_solicitudes_equipo(
                            conexion, persona["equipo_id"], ahora
                        )
                        for s in solicitudes:
                            s["fecha_solicitud_texto"] = _formatear_fecha(s["fecha_solicitud"])
                            s["nuevo_horario_texto"] = _formatear_fecha(s["nuevo_horario"])
                            s["partida_fecha_texto"] = _formatear_fecha(s["partida_fecha_hora"])

                        contexto = {
                            "persona": dict(persona),
                            "partidas": partidas,
                            "solicitudes": solicitudes,
                            "error": str(error),
                        }
                        return templates.TemplateResponse(
                            request=request,
                            name="jugador.html",
                            context=contexto,
                            status_code=status.HTTP_400_BAD_REQUEST,
                        )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error),
                )
        return RedirectResponse(
            url=f"/jugador?persona_id={persona_id}&mensaje=Solicitud+de+cambio+de+horario+registrada+con+exito.",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    @router.post("/{solicitud_id}/aprobar")
    def aprobar(
        solicitud_id: int,
        persona_id: int = Form(...),
    ):
        with abrir_conexion() as conexion:
            try:
                servicio.aprobar_solicitud(
                    conexion,
                    solicitud_id=solicitud_id,
                    moderador_id=persona_id,
                    ahora=reloj(),
                    discord=discord,
                )
            except servicio.ErrorCambioHorario as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error),
                )
        return RedirectResponse(
            url=f"/moderador?persona_id={persona_id}&mensaje=Solicitud+aprobada+y+partida+reprogramada.",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    @router.post("/{solicitud_id}/rechazar")
    def rechazar(
        solicitud_id: int,
        persona_id: int = Form(...),
        motivo: str = Form(...),
    ):
        with abrir_conexion() as conexion:
            try:
                servicio.rechazar_solicitud(
                    conexion,
                    solicitud_id=solicitud_id,
                    moderador_id=persona_id,
                    motivo=motivo,
                    ahora=reloj(),
                    discord=discord,
                )
            except servicio.ErrorCambioHorario as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error),
                )
        return RedirectResponse(
            url=f"/moderador?persona_id={persona_id}&mensaje=Solicitud+rechazada.",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return router
