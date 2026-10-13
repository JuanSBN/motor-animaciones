"""
niko_bible.py

Fuente única de verdad del personaje para FLUX. Todos los scripts de generación deben
construir el prompt con `prompt_niko()` en lugar de describir a Niko a mano; así no cambian
las tiritas, el color del pelo ni la edad entre planos.

Uso:
  from niko_bible import prompt_niko, prompt_escena, SEMILLA_NIKO, NEGATIVO
  prompt = prompt_niko("sentado en la cama, sobresaltado, la alarma sonando", plano="medio")
"""

ESTILO = (
    "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant saturated colors, "
    "soft vignette, explainer video style, 16:9 composition, no text, no letters, no watermark"
)

NIKO = (
    "Niko, a 12-year-old cartoon boy, same character in every image: "
    "round head, big expressive brown eyes, short spiky teal-green hair (#2BB5A0), "
    "exactly two small light-blue band-aids, one on each cheek, "
    "light tan skin, orange hoodie with white drawstrings, dark blue pants, white sneakers, "
    "consistent proportions, head-to-body ratio 1:3"
)

PLANOS = {
    "general": "wide shot, Niko small in the frame, environment visible",
    "medio": "medium shot from the waist up, Niko centered",
    "primer_plano": "close-up of Niko's face, expression clearly readable",
    "detalle": "extreme close-up detail shot",
}

NEGATIVO = (
    "photorealistic, 3d render, text, letters, captions, watermark, extra fingers, deformed hands, "
    "different hair color, single band-aid, no band-aids, older character, adult, teenager, "
    "floating objects pasted on top, flat lighting mismatch"
)

SEMILLA_NIKO = 424242


def prompt_niko(accion: str, plano: str = "medio", ambiente: str = "") -> str:
    partes = [ESTILO, NIKO, PLANOS.get(plano, PLANOS["medio"]), accion]
    if ambiente:
        partes.append(ambiente)
    return ", ".join(partes)


def prompt_escena(descripcion: str, plano: str = "general") -> str:
    """Para planos sin Niko (cerebro, reloj, servidores...). Integra los objetos en la iluminación."""
    return ", ".join([
        ESTILO,
        PLANOS.get(plano, PLANOS["general"]),
        descripcion,
        "all elements integrated into the scene lighting, cast shadows and glow reflected on surroundings",
    ])
