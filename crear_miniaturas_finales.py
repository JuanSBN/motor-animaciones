"""
crear_miniaturas_finales.py
Genera las 3 miniaturas terminadas en formato oficial de YouTube (1920x1080)
montando la tipografía de alto impacto (amarillo brillante + trazo negro 3D)
sobre las 3 ilustraciones aprobadas por el usuario.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = r"c:\Users\Lenovo\Documents\Animaciones\miniaturas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Rutas de las imágenes aprobadas por el usuario
IMGS = {
    "miniatura_1_split_cavernicolas": {
        "src": r"C:\Users\Lenovo\.gemini\antigravity\brain\eca3fd45-df48-4b97-9eba-a44d2e61b37b\.user_uploaded\media_1791842442737_66ef2a33.jpg",
        "texto": "¿CÓMO PASÓ?",
        "pos": "top_center",
        "offset_y": 70
    },
    "miniatura_2_cartel_cazadores": {
        "src": r"C:\Users\Lenovo\.gemini\antigravity\brain\eca3fd45-df48-4b97-9eba-a44d2e61b37b\.user_uploaded\media_1791842442749_bf31d9bb.jpg",
        "texto": "¿POR QUÉ?",
        "subtexto": "???",
        "pos": "top_center",
        "offset_y": 60
    },
    "miniatura_3_niko_centro_shrug": {
        "src": r"C:\Users\Lenovo\.gemini\antigravity\brain\eca3fd45-df48-4b97-9eba-a44d2e61b37b\.user_uploaded\media_1791842029375_16f8bb8f.jpg",
        "texto": "¿POR QUÉ CAMBIÓ?",
        "pos": "top_center",
        "offset_y": 65
    }
}

FONT_PATH = r"C:\Windows\Fonts\ariblk.ttf" # Arial Black para máxima legibilidad

def dibujar_texto_youtube(draw, x, y, texto, font, fill_color="#FFE600", stroke_color="#0A0A0A", stroke_width=18):
    # Sombra negra profunda / 3D proyectada
    for ox, oy in [(10, 14), (8, 12), (6, 10)]:
        draw.text((x + ox, y + oy), texto, font=font, fill="#000000", stroke_width=stroke_width, stroke_fill="#000000")
    
    # Trazo negro grueso de contraste
    draw.text((x, y), texto, font=font, fill=fill_color, stroke_width=stroke_width, stroke_fill=stroke_color)

def procesar_miniatura(nombre, config):
    src_path = config["src"]
    if not os.path.exists(src_path):
        print(f"Error: No existe {src_path}")
        return

    # Abrir y redimensionar a 1920x1080 limpio
    img = Image.open(src_path).convert("RGBA")
    img = img.resize((1920, 1080), Image.Resampling.LANCZOS)

    # Capa de dibujo
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Tipografía grande de YouTube (tamaño 140 a 160)
    font_size = 145 if len(config["texto"]) <= 10 else 125
    font = ImageFont.truetype(FONT_PATH, font_size)

    # Calcular dimensiones del texto
    bbox = font.getbbox(config["texto"])
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Posicionamiento centrado arriba
    x = (1920 - text_w) // 2
    y = config.get("offset_y", 60)

    # Ligero viñeteado oscuro en la parte superior para que el texto resalte aún más
    vignette = Image.new("RGBA", (1920, 320), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for row in range(320):
        alpha = int(120 * (1 - (row / 320.0)**1.2))
        v_draw.line([(0, row), (1920, row)], fill=(0, 0, 0, alpha))
    img.alpha_composite(vignette, (0, 0))

    # Dibujar texto principal
    dibujar_texto_youtube(draw, x, y, config["texto"], font, fill_color="#FFE600", stroke_color="#111111", stroke_width=18)

    # Subtexto si existe (ej. "???")
    if "subtexto" in config:
        sub_font = ImageFont.truetype(FONT_PATH, 75)
        sub_bbox = sub_font.getbbox(config["subtexto"])
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = (1920 - sub_w) // 2
        sub_y = y + text_h + 35
        dibujar_texto_youtube(draw, sub_x, sub_y, config["subtexto"], sub_font, fill_color="#F8FAFC", stroke_color="#111111", stroke_width=12)

    # Combinar capas
    final_img = Image.alpha_composite(img, overlay).convert("RGB")

    out_path = os.path.join(OUTPUT_DIR, f"{nombre}.png")
    final_img.save(out_path, "PNG", quality=95)
    print(f"✅ Miniatura generada: {out_path}")
    return out_path

if __name__ == "__main__":
    for nombre, cfg in IMGS.items():
        procesar_miniatura(nombre, cfg)
