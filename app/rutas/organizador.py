from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.servicios import anuncio as servicio_anuncio
from app.servicios import resultado as servicio_resultado
from app.servicios import torneo_gestion as servicio_torneo

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


def _contexto_vacio(organizador=None, torneo=None, mensaje=None, error=None):
    org_dict = dict(organizador) if organizador else None
    return {
        "organizador": org_dict,
        "persona": org_dict,
        "torneo": dict(torneo) if torneo else None,
        "partidas": [],
        "anuncios": [],
        "pendientes": [],
        "premios": [],
        "equipos_inscritos": [],
        "mensaje": mensaje,
        "error": error,
    }


def crear_router(templates, abrir_conexion, reloj=None):
    router = APIRouter()

    @router.get("/organizador", response_class=HTMLResponse)
    def vista_organizador(
        request: Request, persona_id: int | None = None, mensaje: str | None = None
    ):
        anuncios = {}
        with abrir_conexion() as conexion:
            organizador = _organizador_seleccionado(conexion, persona_id)
            if organizador is None:
                contexto = _contexto_vacio()
            else:
                torneo = conexion.execute(
                    """
                    SELECT id, nombre, juego, organizador_id, fecha_inicio, descripcion, estado, bolsa_premios
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
                    contexto["premios"] = servicio_torneo.obtener_premios_torneo(
                        conexion, torneo["id"]
                    )
                    contexto["equipos_inscritos"] = servicio_torneo.obtener_equipos_inscritos(
                        conexion, torneo["id"]
                    )

        if mensaje == "guardado_ok":
            contexto["mensaje"] = "¡Configuración del torneo guardada exitosamente!"
        elif mensaje:
            contexto["mensaje"] = mensaje

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

    @router.get("/organizador/torneo/gestion", response_class=HTMLResponse)
    def vista_gestion_torneo(
        request: Request,
        persona_id: int | None = None,
        torneo_id: int | None = None,
        mensaje: str | None = None,
        error: str | None = None,
    ):
        with abrir_conexion() as conexion:
            organizador = _organizador_seleccionado(conexion, persona_id)
            if torneo_id:
                torneo = conexion.execute(
                    "SELECT * FROM torneo WHERE id = ?", (torneo_id,)
                ).fetchone()
            else:
                torneo = conexion.execute(
                    """
                    SELECT * FROM torneo
                    WHERE organizador_id = ?
                    ORDER BY id LIMIT 1
                    """,
                    (organizador["id"],),
                ).fetchone()

            todos_equipos = servicio_torneo.listar_equipos_con_jugadores(conexion)
            premios = (
                servicio_torneo.obtener_premios_torneo(conexion, torneo["id"])
                if torneo
                else []
            )
            inscritos_ids = (
                [
                    e["id"]
                    for e in servicio_torneo.obtener_equipos_inscritos(
                        conexion, torneo["id"]
                    )
                ]
                if torneo
                else []
            )

        premios_map = {p["posicion"]: p for p in premios}
        premios_formulario = []
        for pos in (1, 2, 3):
            pos_txt = (
                "1.º Lugar (Campeón)"
                if pos == 1
                else "2.º Lugar (Subcampeón)"
                if pos == 2
                else "3.º Lugar"
            )
            premio_actual = premios_map.get(
                pos,
                {
                    "posicion": pos,
                    "posicion_texto": pos_txt,
                    "monto_texto": "",
                    "descripcion": "",
                },
            )
            premios_formulario.append(premio_actual)

        contexto = {
            "organizador": dict(organizador) if organizador else None,
            "persona": dict(organizador) if organizador else None,
            "torneo": dict(torneo) if torneo else None,
            "todos_equipos": todos_equipos,
            "inscritos_ids": inscritos_ids,
            "premios_formulario": premios_formulario,
            "mensaje": (
                "¡Torneo, participantes y premios guardados exitosamente!"
                if mensaje == "guardado_ok"
                else mensaje
            ),
            "error": error,
        }
        return templates.TemplateResponse(
            request=request, name="gestion_torneo.html", context=contexto
        )

    @router.post("/organizador/torneo/guardar", response_class=HTMLResponse)
    async def guardar_torneo(request: Request):
        form = await request.form()
        persona_id = int(form.get("persona_id", 0))
        torneo_id_val = form.get("torneo_id")
        torneo_id = (
            int(torneo_id_val)
            if torneo_id_val and str(torneo_id_val).isdigit()
            else None
        )
        nombre = str(form.get("nombre", "")).strip()
        juego = str(form.get("juego", "Valorant")).strip()
        fecha_inicio = str(form.get("fecha_inicio", "")).strip()
        zona_horaria = str(form.get("zona_horaria", "America/Bogota")).strip()
        descripcion = str(form.get("descripcion", "")).strip()
        estado = str(form.get("estado", "En curso")).strip()
        bolsa_premios = str(form.get("bolsa_premios", "")).strip()

        equipos_ids = [
            int(v) for v in form.getlist("equipos_ids") if str(v).isdigit()
        ]

        premios = []
        for pos in (1, 2, 3):
            monto = str(form.get(f"premio_{pos}_monto", "")).strip()
            desc = str(form.get(f"premio_{pos}_desc", "")).strip()
            pos_txt = str(
                form.get(f"premio_{pos}_texto", f"{pos}.º Lugar")
            ).strip()
            if monto or desc:
                premios.append(
                    {
                        "posicion": pos,
                        "posicion_texto": pos_txt,
                        "monto_texto": monto,
                        "descripcion": desc,
                    }
                )

        with abrir_conexion() as conexion:
            organizador = _organizador_seleccionado(conexion, persona_id)
            try:
                t_id = servicio_torneo.crear_o_actualizar_torneo(
                    conexion,
                    organizador_id=organizador["id"],
                    torneo_id=torneo_id,
                    nombre=nombre,
                    juego=juego,
                    fecha_inicio=fecha_inicio,
                    zona_horaria=zona_horaria,
                    descripcion=descripcion,
                    estado=estado,
                    bolsa_premios=bolsa_premios,
                    premios=premios,
                    equipos_ids=equipos_ids,
                    ahora=reloj() if reloj else None,
                )
            except servicio_torneo.ErrorGestionTorneo as e:
                todos_equipos = servicio_torneo.listar_equipos_con_jugadores(
                    conexion
                )
                premios_formulario = []
                for pos in (1, 2, 3):
                    premios_formulario.append(
                        {
                            "posicion": pos,
                            "posicion_texto": str(
                                form.get(f"premio_{pos}_texto", f"{pos}.º Lugar")
                            ),
                            "monto_texto": str(
                                form.get(f"premio_{pos}_monto", "")
                            ),
                            "descripcion": str(
                                form.get(f"premio_{pos}_desc", "")
                            ),
                        }
                    )
                contexto = {
                    "organizador": dict(organizador),
                    "persona": dict(organizador),
                    "torneo": {
                        "id": torneo_id,
                        "nombre": nombre,
                        "juego": juego,
                        "fecha_inicio": fecha_inicio,
                        "zona_horaria": zona_horaria,
                        "descripcion": descripcion,
                        "estado": estado,
                        "bolsa_premios": bolsa_premios,
                    },
                    "todos_equipos": todos_equipos,
                    "inscritos_ids": equipos_ids,
                    "premios_formulario": premios_formulario,
                    "error": e.mensaje,
                }
                return templates.TemplateResponse(
                    request=request,
                    name="gestion_torneo.html",
                    context=contexto,
                    status_code=400,
                )

        return RedirectResponse(
            url=f"/organizador/torneo/gestion?persona_id={persona_id}&torneo_id={t_id}&mensaje=guardado_ok",
            status_code=303,
        )

    return router
