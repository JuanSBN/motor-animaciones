"""
regenerar_planos_corregidos_qa.py
Regenera con el nuevo canon puro blindado:
  1. ep2_escena_3_p1.png: Niko de 12 años canónico en la biblioteca con el puntero (ratio 1:4.8, curita blanca, pelo teal)
  2. ep2_escena_1_p12_a.png: Niko en la cama al despertar desconcertado (pelo teal, curita blanca, pijama canónico)
"""

import os
import sys
import io
import shutil
from pathlib import Path
from PIL import Image
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"c:\Users\Lenovo\Documents\Animaciones")
EP2_DIR = BASE_DIR / "Episodio_2"
MOTOR_DIR = BASE_DIR / "motor_animaciones"
REMOTION_DIR = BASE_DIR / "Episodio_1" / "remotion_app"
IMG_DIR = EP2_DIR / "assets" / "img"
PUBLIC_IMG = REMOTION_DIR / "public" / "assets" / "img"

sys.path.append(str(MOTOR_DIR))

# Cargar variables de entorno
def load_env():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v

load_env()
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Modal configuration
image_modal = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-regenerar-corregidos", image=image_modal)

@app.function(gpu="A100", timeout=600)
def modal_gen(prompts, ref_bytes_list, use_ref_flags, hf_token):
    from huggingface_hub import login
    import torch
    from diffusers import Flux2KleinPipeline
    import io
    login(token=hf_token)
    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=torch.bfloat16
    ).to("cuda")

    outputs = []
    for i, p in enumerate(prompts):
        ref_b = ref_bytes_list[i]
        use_r = use_ref_flags[i]
        ref_img = [Image.open(io.BytesIO(ref_b)).convert("RGB")] if (use_r and ref_b) else None
        kw = {
            "prompt": p,
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1344,
            "height": 768
        }
        if ref_img:
            kw["image"] = ref_img
        out = pipe(**kw).images[0]
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        outputs.append(buf.getvalue())
    return outputs

def main():
    from niko_bible import prompt_niko, RUTA_CANONICA_NIKO, RUTA_CANONICA_PIJAMA
    from evaluador_coherencia import EvaluadorCoherencia

    with open(RUTA_CANONICA_NIKO, "rb") as f:
        bytes_canon_dia = f.read()
    with open(RUTA_CANONICA_PIJAMA, "rb") as f:
        bytes_canon_pijama = f.read()

    # Plano 1: Niko biblioteca (12 años pre-teen canónico, curita blanca)
    prompt_biblioteca = prompt_niko(
        "standing in cozy wooden library holding a wooden pointer stick, smiling confidently, pointing up at two glowing translucent brain diagrams hovering in the air",
        plano="medio",
        ambiente="warm academic library bookshelves background, soft ambient lighting, clean 16:9 composition"
    )

    # Plano 2: Niko despertar (pijama, pelo teal, curita blanca, rascándose la cabeza)
    prompt_despertar = prompt_niko(
        "sitting up on cozy bed in soft morning sunlight, rubbing forehead with one hand with a puzzled confused expression, morning window light pouring in, bed headboard",
        plano="medio",
        ambiente="warm morning bedroom, wooden furniture, golden sunlight beams, peaceful morning mood",
        pijama=True
    )

    planos = [
        {"nombre": "ep2_escena_3_p1.png", "prompt": prompt_biblioteca, "bytes": bytes_canon_dia, "pijama": False},
        {"nombre": "ep2_escena_1_p12_a.png", "prompt": prompt_despertar, "bytes": bytes_canon_pijama, "pijama": True},
    ]

    prompts = [p["prompt"] for p in planos]
    ref_list = [p["bytes"] for p in planos]
    flags = [True, True]

    print("🚀 Generando en Modal A100 los dos planos clave corregidos...")
    with app.run():
        res_bytes = modal_gen.remote(prompts, ref_list, flags, HF_TOKEN)

    evaluador = EvaluadorCoherencia()

    for i, p in enumerate(planos):
        out_path = IMG_DIR / p["nombre"]
        with open(out_path, "wb") as f:
            f.write(res_bytes[i])
        shutil.copy(str(out_path), str(PUBLIC_IMG / p["nombre"]))
        print(f"✅ Guardado en assets y Remotion: {p['nombre']}")

        eval_res = evaluador.evaluar_niko(str(out_path), es_pijama=p["pijama"])
        print(f"   CLIP Score: {eval_res['score']:.1f}% -> {eval_res['mensaje']}")

if __name__ == "__main__":
    main()
