from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import RedirectResponse

from app.servicios import cambio_horario as servicio


def crear_router(abrir_conexion, reloj, discord=None):
    router = APIRouter(prefix="/cambio-horario", tags=["cambio-horario"])

    @router.post("/solicitar")
    def solicitar(
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
