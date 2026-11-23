from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.servicios import anuncio as servicio_anuncio
from app.servicios import resultado as servicio_resultado
from app.servicios import torneo_gestion as servicio_torneo


def _formatear_fecha(valor):
    if not valor:
        return "—"
    return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")


def crear_router(templates, abrir_conexion):
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    def inicio(request: Request):
        contexto = {
            "torneo": None,
            "bracket": None,
            "partidas": [],
            "anuncios": [],
        }

        with abrir_conexion() as conexion:
            torneo = conexion.execute(
                """
                SELECT id, nombre, juego, fecha_inicio, descripcion, estado, bolsa_premios
                FROM torneo
                ORDER BY id
                LIMIT 1
                """
            ).fetchone()

            if torneo is not None:
                bracket = conexion.execute(
                    "SELECT ultima_actualizacion FROM bracket WHERE torneo_id = ?",
                    (torneo["id"],),
                ).fetchone()
                partidas = servicio_resultado.listar_bracket(conexion, torneo["id"])
                anuncios = servicio_anuncio.anuncios_por_partida(conexion)
                premios = servicio_torneo.obtener_premios_torneo(conexion, torneo["id"])

                for partida in partidas:
                    partida["anuncio"] = anuncios.get(partida["partida_id"])

                contexto = {
                    "torneo": dict(torneo),
                    "bracket": dict(bracket) if bracket else None,
                    "partidas": partidas,
                    "premios": premios,
                    "anuncios": [
                        partida
                        for partida in partidas
                        if partida["anuncio"] is not None
                        and partida["resultado"] is not None
                    ],
                }
                contexto["anuncios"].sort(
                    key=lambda partida: partida["anuncio"]["fecha_hora_publicacion"],
                    reverse=True,
                )

        for partida in contexto["partidas"]:
            partida["fecha_texto"] = _formatear_fecha(partida["fecha_hora"])
            if partida["resultado"]:
                partida["resultado"]["fecha_texto"] = _formatear_fecha(
                    partida["resultado"]["fecha_hora_registro"]
                )
            if partida["anuncio"]:
                partida["anuncio"]["fecha_texto"] = _formatear_fecha(
                    partida["anuncio"]["fecha_hora_publicacion"]
                )

        if contexto["bracket"]:
            contexto["bracket"]["ultima_actualizacion_texto"] = _formatear_fecha(
                contexto["bracket"]["ultima_actualizacion"]
            )

        return templates.TemplateResponse(
            request=request, name="torneo.html", context=contexto
        )

    @router.get("/torneo", response_class=HTMLResponse)
    def torneo_redirigido():
        """Conserva los enlaces anteriores a la página pública."""
        return RedirectResponse(url="/", status_code=307)

    return router
