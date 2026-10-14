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
RUTA_CANONICA_NIKO = str(BASE_DIR / "niko_canon_puro.png")
RUTA_CANONICA_PIJAMA = str(BASE_DIR / "niko_referencia_pijama.png")

ESTILO = (
    "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant saturated colors, "
    "soft vignette, explainer video style, 16:9 composition, no text, no letters, no watermark"
)

NIKO = (
    "Niko, a 12-year-old pre-teen cartoon adventurer boy, strictly identical to reference character: "
    "head with defined jawline, NOT chubby cheeks, small cute button nose, simple arched eyebrows, big expressive dark brown eyes, messy spiky dark teal-green hair (#1F6B63 / #2BB5A0) with a loose curved cowlick strand at the crown, "
    "exactly ONE single small cream-white rectangular adhesive bandage (band-aid) on his left cheek, clear smooth skin on right cheek with NO second band-aid, "
    "warm light tan skin, olive green utility cargo vest with pocket flaps over yellow-and-orange horizontally striped shirt, dark blue shorts, white sneakers, "
    "slender limbs, athletic 12-year-old pre-teen proportions, head-to-body ratio 1:4.8, NOT a toddler, NOT a preschool child, NOT chibi, clean 2D flat vector comic animation style"
)

NIKO_PIJAMA = (
    "Niko, a 12-year-old pre-teen cartoon adventurer boy in bed pajamas, strictly identical character: "
    "head with defined jawline, big expressive dark brown eyes, messy spiky dark teal-green hair with loose curved cowlick, "
    "exactly ONE single small cream-white adhesive bandage on his left cheek, "
    "warm light tan skin, yellow sleeping shirt, cozy bedtime attire, "
    "slender limbs, athletic pre-teen proportions, head-to-body ratio 1:4.8, NOT a toddler, NOT a preschool child"
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
