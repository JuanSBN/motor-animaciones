"""
niko_bible.py

Fuente única de verdad del personaje. Todo prompt de FLUX que incluya a Niko debe salir de
`prompt_niko()`, y toda generación con Niko debe recibir `referencias_niko()` y `semilla_para()`.

Las tres causas de que Niko cambiara entre planos eran:
  1. Sin semilla fija -> cada ejecución partía de ruido distinto.
  2. Referencias = salidas previas distintas en cada script -> la deriva se acumulaba.
  3. Descripción escrita a mano en cada script ("band-aid on right cheek" vs "band-aid on cheek").

Las referencias canónicas viven en `personaje/niko/` y NO se sobrescriben con salidas nuevas.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parent.parent
DIR_PERSONAJE = RAIZ_REPO / "personaje" / "niko"

ESTILO = "2D flat cartoon illustration style, clean bold black outlines, flat shading, vibrant colors"
ANTI_TEXTO = "NO text, NO letters, NO words, NO labels, NO typography, NO watermark"

# Rasgos que nunca cambian, extraídos de las imágenes aprobadas de los episodios 1 y 2.
NIKO_BASE = (
    "the same recurring cartoon character Niko, a young boy around 10 years old, "
    "big messy spiky teal hair, large round white eyes with small black pupils, small round nose, "
    "light peach skin with rosy cheeks, "
    "exactly two small white band-aids, one on each cheek, "
    "same face shape and proportions as the reference images"
)

VESTUARIOS = {
    "casual": "wearing a yellow t-shirt with thin red horizontal stripes under an olive-green utility vest "
              "with front pockets, dark navy pants",
    "pijama": "wearing a yellow-and-orange striped pajama t-shirt and sleep shorts, bare feet, "
              "NO vest, NO jacket, NO shoes",
}

REFERENCIAS = {
    "casual": ["casual_frente.png", "casual_tres_cuartos.png"],
    "pijama": ["pijama_cama.png", "casual_frente.png"],
}

PLANOS = {
    "general": "wide shot, Niko small in frame, full environment visible",
    "medio": "medium shot from the waist up, Niko centered",
    "primer_plano": "close-up of Niko's face, expression clearly readable",
    "detalle": "extreme close-up detail shot",
}

SEMILLA_BASE = 424242

PALABRAS_NIKO = ("niko", "protagonista", "niño", "imagina", "te despiertas", "te duermes", "tu cama")


def aparece_niko(texto: str) -> bool:
    t = texto.lower()
    return any(p in t for p in PALABRAS_NIKO)


def prompt_niko(accion: str, plano: str = "medio", vestuario: str = "casual", ambiente: str = "") -> str:
    partes = [
        PLANOS.get(plano, PLANOS["medio"]),
        NIKO_BASE,
        VESTUARIOS.get(vestuario, VESTUARIOS["casual"]),
        accion,
    ]
    if ambiente:
        partes.append(ambiente)
    partes += [ESTILO, ANTI_TEXTO]
    return ", ".join(partes) + "."


def prompt_escena(descripcion: str, plano: str = "general") -> str:
    """Planos sin Niko: el objeto debe estar integrado en la luz de la escena, no pegado encima."""
    return ", ".join([
        PLANOS.get(plano, PLANOS["general"]),
        descripcion,
        "all elements integrated into the scene lighting with cast shadows and glow reflected on surroundings",
        "no people",
        ESTILO,
        ANTI_TEXTO,
    ]) + "."


def referencias_niko(vestuario: str = "casual") -> list[Path]:
    rutas = [DIR_PERSONAJE / n for n in REFERENCIAS.get(vestuario, REFERENCIAS["casual"])]
    faltan = [str(r) for r in rutas if not r.exists()]
    if faltan:
        raise FileNotFoundError(f"Faltan referencias canónicas de Niko: {faltan}")
    return rutas


def semilla_para(clave: str) -> int:
    """Semilla estable por plano: regenerar el mismo plano da el mismo resultado; planos distintos varían."""
    h = int(hashlib.sha1(clave.encode("utf-8")).hexdigest()[:8], 16)
    return SEMILLA_BASE + (h % 100_000)


PREGUNTA_QA_NIKO = (
    "Look at the cartoon boy in this image. Answer each with YES or NO: "
    "1) Is his hair teal (blue-green)? "
    "2) Are there white band-aids on his cheeks? "
    "3) Does he wear a yellow striped shirt? "
    "4) Is he drawn in 2D flat cartoon style (not 3D, not realistic)? "
    "Reply in the format: HAIR=YES/NO BANDAID=YES/NO SHIRT=YES/NO STYLE=YES/NO"
)
