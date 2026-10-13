"""
niko_bible.py

Fuente única de verdad del personaje para FLUX. Todos los scripts de generación deben
construir el prompt con `prompt_niko()` en lugar de describir a Niko a mano; así no cambian
las tiritas, el color del pelo ni la edad entre planos.

Uso:
  from niko_bible import prompt_niko, prompt_escena, SEMILLA_NIKO, NEGATIVO
  prompt = prompt_niko("sentado en la cama, sobresaltado, la alarma sonando", plano="medio")
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA_CANONICA_NIKO = str(BASE_DIR / "niko_referencia_canonica.jpg")
RUTA_CANONICA_PIJAMA = str(BASE_DIR / "niko_referencia_pijama.png")

ESTILO = (
    "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant saturated colors, "
    "soft vignette, explainer video style, 16:9 composition, no text, no letters, no watermark"
)

NIKO = (
    "Niko, a 12-year-old cartoon boy, strictly identical character: "
    "round head, big expressive brown eyes, messy spiky dark teal-green hair (#2BB5A0), "
    "exactly ONE small light-blue band-aid on his left cheek, "
    "warm light tan skin, green vest over yellow-and-white striped t-shirt, dark blue shorts, white sneakers, "
    "consistent proportions, head-to-body ratio 1:3, clean stylized animation style"
)

NIKO_PIJAMA = (
    "Niko, a 12-year-old cartoon boy in bed pajamas, strictly identical character: "
    "round head, big expressive brown eyes, messy spiky dark teal-green hair (#2BB5A0), "
    "exactly ONE small light-blue band-aid on his left cheek, "
    "warm light tan skin, yellow sleeping shirt, cozy bedtime attire, "
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
    "different hair color, blonde, black hair, two band-aids, no band-aids, orange hoodie, "
    "super-deformed chibi, tiny anime dot eyes, headless body, severed neck, floating heads, "
    "older character, adult, teenager, flat lighting mismatch"
)

SEMILLA_NIKO = 424242


def prompt_niko(accion: str, plano: str = "medio", ambiente: str = "", pijama: bool = False) -> str:
    char = NIKO_PIJAMA if pijama else NIKO
    partes = [ESTILO, char, PLANOS.get(plano, PLANOS["medio"]), accion]
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
