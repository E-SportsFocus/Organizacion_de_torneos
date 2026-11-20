from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.servicios import anuncio as servicio_anuncio
from app.servicios import resultado as servicio_resultado

TIPO_ORGANIZADOR = "Organizador"
ESTADO_PENDIENTE = "Pendiente de resultado"


def _formatear_fecha(valor):
    if not valor:
        return "—"
    return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")


def _organizador_seleccionado(conexion, persona_id):
    if persona_id is None:
        return conexion.execute(
            """
            SELECT id, nombre, tipo
            FROM persona
            WHERE tipo = ?
            ORDER BY id
            LIMIT 1
            """,
            (TIPO_ORGANIZADOR,),
        ).fetchone()

    persona = conexion.execute(
        "SELECT id, nombre, tipo FROM persona WHERE id = ?", (persona_id,)
    ).fetchone()
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if persona["tipo"] != TIPO_ORGANIZADOR:
        raise HTTPException(
            status_code=400, detail="La persona indicada no es un Organizador"
        )
    return persona


def _contexto_vacio(organizador=None, torneo=None):
    return {
        "organizador": dict(organizador) if organizador else None,
        "torneo": dict(torneo) if torneo else None,
        "partidas": [],
        "anuncios": [],
        "pendientes": [],
    }


def crear_router(templates, abrir_conexion):
    router = APIRouter()

    @router.get("/organizador", response_class=HTMLResponse)
    def vista_organizador(request: Request, persona_id: int | None = None):
        anuncios = {}
        with abrir_conexion() as conexion:
            organizador = _organizador_seleccionado(conexion, persona_id)
            if organizador is None:
                contexto = _contexto_vacio()
            else:
                torneo = conexion.execute(
                    """
                    SELECT id, nombre, juego, organizador_id
                    FROM torneo
                    WHERE organizador_id = ?
                    ORDER BY id
                    LIMIT 1
                    """,
                    (organizador["id"],),
                ).fetchone()
                if torneo is None:
                    contexto = _contexto_vacio(organizador)
                else:
                    partidas = servicio_resultado.listar_bracket(
                        conexion, torneo["id"]
                    )
                    anuncios = servicio_anuncio.anuncios_por_partida(conexion)
                    contexto = _contexto_vacio(organizador, torneo)
                    contexto["partidas"] = partidas

        for partida in contexto["partidas"]:
            partida["fecha_texto"] = _formatear_fecha(partida["fecha_hora"])
            partida["anuncio"] = anuncios.get(partida["partida_id"])
            if partida["resultado"]:
                partida["resultado"]["fecha_texto"] = _formatear_fecha(
                    partida["resultado"]["fecha_hora_registro"]
                )
            if partida["anuncio"]:
                partida["anuncio"]["fecha_texto"] = _formatear_fecha(
                    partida["anuncio"]["fecha_hora_publicacion"]
                )

        contexto["anuncios"] = [
            partida
            for partida in contexto["partidas"]
            if partida["anuncio"] is not None and partida["resultado"] is not None
        ]
        contexto["anuncios"].sort(
            key=lambda partida: partida["anuncio"]["fecha_hora_publicacion"],
            reverse=True,
        )
        contexto["pendientes"] = [
            partida
            for partida in contexto["partidas"]
            if partida["estado"] == ESTADO_PENDIENTE and not partida["resultado"]
        ]

        return templates.TemplateResponse(
            request=request, name="organizador.html", context=contexto
        )

    return router
