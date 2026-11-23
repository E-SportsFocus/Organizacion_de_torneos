"""Servicio de estructuración y visualización del bracket del torneo (HU-08)."""

from datetime import datetime
from app.servicios import resultado as servicio_resultado

ORDEN_FASES_CANONICO = [
    "Cuartos de final",
    "Semifinal",
    "Final",
]


def _formatear_fecha(valor):
    if not valor:
        return "—"
    try:
        return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(valor)


def estructurar_partida_bracket(partida):
    """Enriquece una partida con slots de equipo, marcadores individuales y estado de victoria."""
    resultado = partida.get("resultado")
    equipos_raw = partida.get("equipos") or []
    
    equipos_estructurados = []
    ganador_id = resultado["ganador"]["equipo_id"] if (resultado and resultado.get("ganador")) else None
    ganador_nombre = resultado["ganador"]["equipo"] if (resultado and resultado.get("ganador")) else None

    for eq in equipos_raw:
        eq_id = eq.get("id") or eq.get("equipo_id")
        nombre = eq.get("nombre") or eq.get("equipo") or "Por definir"
        if resultado and resultado.get("marcadores") and eq_id in resultado["marcadores"]:
            marcador = resultado["marcadores"][eq_id]
            es_ganador = (eq_id == ganador_id)
        else:
            marcador = "—"
            es_ganador = False

        equipos_estructurados.append({
            "id": eq_id,
            "nombre": nombre,
            "marcador": marcador,
            "es_ganador": es_ganador,
        })

    # Asegurar siempre 2 slots de enfrentamiento
    while len(equipos_estructurados) < 2:
        equipos_estructurados.append({
            "id": None,
            "nombre": "Por definir",
            "marcador": "—",
            "es_ganador": False,
        })

    return {
        "id": partida.get("partida_id") or partida.get("id"),
        "fase": partida.get("fase", "Fase regular"),
        "fecha_hora": partida.get("fecha_hora"),
        "fecha_texto": partida.get("fecha_texto") or _formatear_fecha(partida.get("fecha_hora")),
        "estado": partida.get("estado", "Programada"),
        "tiene_resultado": (resultado is not None),
        "ganador_id": ganador_id,
        "ganador_nombre": ganador_nombre,
        "equipos": equipos_estructurados,
        "resultado": resultado,
    }


def obtener_bracket_estructurado(conexion, torneo_id):
    """
    Agrupa las partidas del torneo en rondas ordenadas secuencialmente
    para alimentar la visualización en árbol de llaves (HU-08).
    """
    partidas_crudas = servicio_resultado.listar_bracket(conexion, torneo_id)
    
    # Agrupación por fase
    partidas_por_fase = {}
    for p in partidas_crudas:
        p_estructurada = estructurar_partida_bracket(p)
        fase = p_estructurada["fase"]
        if fase not in partidas_por_fase:
            partidas_por_fase[fase] = []
        partidas_por_fase[fase].append(p_estructurada)

    # Ordenar las fases según la secuencia canónica del torneo
    rondas = []
    # Primero las canónicas presentes
    for fase_nombre in ORDEN_FASES_CANONICO:
        if fase_nombre in partidas_por_fase:
            rondas.append({
                "nombre": fase_nombre,
                "partidas": sorted(partidas_por_fase[fase_nombre], key=lambda x: (x["fecha_hora"] or "", x["id"])),
            })

    # Agregar cualquier fase personalizada adicional no contemplada en el orden canónico
    for fase_nombre, partidas in partidas_por_fase.items():
        if fase_nombre not in ORDEN_FASES_CANONICO:
            rondas.append({
                "nombre": fase_nombre,
                "partidas": sorted(partidas, key=lambda x: (x["fecha_hora"] or "", x["id"])),
            })

    return rondas
