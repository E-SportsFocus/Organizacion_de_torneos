from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.servicios import anuncio as servicio_anuncio
from app.servicios import bracket as servicio_bracket
from app.servicios import cambio_horario as servicio_cambio
from app.servicios import disponibilidad as servicio_disponibilidad
from app.servicios import resultado as servicio

PREFIJO_MARCADOR = "marcador_"


def _formatear_fecha(valor):
    if not valor:
        return "—"
    return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")


def _persona(conexion, persona_id):
    return conexion.execute(
        "SELECT id, nombre, tipo FROM persona WHERE id = ?", (persona_id,)
    ).fetchone()


def _moderador_seleccionado(conexion, persona_id):
    if persona_id is None:
        fila = conexion.execute(
            """
            SELECT id, nombre, tipo
            FROM persona
            WHERE tipo = ?
            ORDER BY id
            LIMIT 1
            """,
            (servicio.TIPO_MODERADOR,),
        ).fetchone()
        if fila is None:
            raise HTTPException(
                status_code=404, detail="No hay moderadores de ejemplo"
            )
        return fila
    persona = _persona(conexion, persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if persona["tipo"] != servicio.TIPO_MODERADOR:
        raise HTTPException(
            status_code=400, detail="La persona indicada no es un Moderador"
        )
    return persona


def crear_router(templates, abrir_conexion, reloj, discord=None):
    router = APIRouter()

    def _contexto_moderador(
        conexion,
        persona,
        mensaje=None,
        error=None,
        valores=None,
        partida_id=None,
    ):
        partidas = servicio_disponibilidad.listar_partidas_moderador(
            conexion, reloj()
        )
        resultados = servicio.resultados_por_partida(conexion)
        anuncios = servicio_anuncio.anuncios_por_partida(conexion)
        for partida in partidas:
            partida["fecha_texto"] = _formatear_fecha(partida["fecha_hora"])
            partida["resultado"] = resultados.get(partida["partida_id"])
            partida["anuncio"] = anuncios.get(partida["partida_id"])
            if partida["resultado"]:
                partida["resultado"]["fecha_texto"] = _formatear_fecha(
                    partida["resultado"]["fecha_hora_registro"]
                )
            partida["puede_registrar"] = (
                partida["estado"] == servicio.ESTADO_PENDIENTE
                and partida["moderador_id"] == persona["id"]
            )

        if mensaje == "ok":
            resultado = resultados.get(partida_id)
            if resultado and resultado["ganador"]:
                mensaje = (
                    f"{servicio.MENSAJE_REGISTRADO} Ganador: "
                    f"{resultado['ganador']['equipo']}. El bracket fue actualizado."
                )
                anuncio = anuncios.get(partida_id)
                if anuncio and anuncio["discord_estado"] == servicio_anuncio.DISCORD_PENDIENTE:
                    mensaje += " El anuncio en Discord quedó pendiente de envío."
                elif anuncio:
                    mensaje += " El ganador quedó anunciado."
            else:
                mensaje = servicio.MENSAJE_REGISTRADO

        solicitudes = servicio_cambio.listar_solicitudes_moderador(
            conexion, persona["id"], reloj()
        )
        for s in solicitudes:
            s["fecha_solicitud_texto"] = _formatear_fecha(s["fecha_solicitud"])
            s["nuevo_horario_texto"] = _formatear_fecha(s["nuevo_horario"])
            s["partida_fecha_texto"] = _formatear_fecha(s["partida_fecha_hora"])

        return {
            "persona": dict(persona),
            "moderador": persona["nombre"],
            "partidas": partidas,
            "solicitudes": solicitudes,
            "mensaje": mensaje,
            "error": error,
            "valores": valores or {},
        }

    @router.get("/moderador", response_class=HTMLResponse)
    def vista_moderador(
        request: Request,
        persona_id: int | None = None,
        mensaje: str | None = None,
        partida: int | None = None,
    ):
        with abrir_conexion() as conexion:
            persona = _moderador_seleccionado(conexion, persona_id)
            contexto = _contexto_moderador(
                conexion,
                persona,
                mensaje=mensaje,
                partida_id=partida,
            )
        return templates.TemplateResponse(
            request=request, name="moderador.html", context=contexto
        )

    @router.post("/partidas/{partida_id}/resultado", response_class=HTMLResponse)
    async def registrar(request: Request, partida_id: int):
        formulario = await request.form()
        try:
            persona_id = int(formulario.get("persona_id"))
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400, detail="No se identificó al Moderador"
            ) from None

        marcadores = {}
        valores = {}
        for clave, valor in formulario.items():
            if not clave.startswith(PREFIJO_MARCADOR):
                continue
            equipo_id = clave[len(PREFIJO_MARCADOR) :]
            marcadores[equipo_id] = valor
            valores[equipo_id] = str(valor)

        with abrir_conexion() as conexion:
            persona = _persona(conexion, persona_id)
            if persona is None:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
            try:
                servicio.registrar_resultado(
                    conexion,
                    partida_id,
                    persona_id,
                    marcadores,
                    reloj(),
                    discord=discord,
                )
            except servicio.ErrorResultado as error:
                contexto = _contexto_moderador(
                    conexion,
                    persona,
                    error=error.mensaje,
                    valores=valores,
                )
                return templates.TemplateResponse(
                    request=request,
                    name="moderador.html",
                    context=contexto,
                    status_code=400,
                )

        return RedirectResponse(
            url=(
                f"/moderador?persona_id={persona_id}"
                f"&mensaje=ok&partida={partida_id}"
            ),
            status_code=303,
        )

    @router.get("/bracket", response_class=HTMLResponse)
    def vista_bracket(request: Request):
        with abrir_conexion() as conexion:
            torneo = conexion.execute(
                "SELECT id, nombre, juego FROM torneo ORDER BY id LIMIT 1"
            ).fetchone()
            if torneo is None:
                return templates.TemplateResponse(
                    request=request,
                    name="bracket.html",
                    context={"torneo": None, "partidas": [], "historial": [], "rondas_bracket": []},
                )
            bracket = conexion.execute(
                "SELECT ultima_actualizacion FROM bracket WHERE torneo_id = ?",
                (torneo["id"],),
            ).fetchone()
            partidas = servicio.listar_bracket(conexion, torneo["id"])
            historial = servicio.historial_bracket(conexion, torneo["id"])
            rondas_bracket = servicio_bracket.obtener_bracket_estructurado(conexion, torneo["id"])

        for partida in partidas:
            partida["fecha_texto"] = _formatear_fecha(partida["fecha_hora"])
        for registro in historial:
            registro["fecha_texto"] = _formatear_fecha(registro["fecha_hora"])

        if bracket:
            bracket = dict(bracket)
            bracket["ultima_actualizacion_texto"] = _formatear_fecha(
                bracket["ultima_actualizacion"]
            )

        return templates.TemplateResponse(
            request=request,
            name="bracket.html",
            context={
                "torneo": dict(torneo),
                "bracket": bracket,
                "partidas": partidas,
                "historial": historial,
                "rondas_bracket": rondas_bracket,
            },
        )

    return router
