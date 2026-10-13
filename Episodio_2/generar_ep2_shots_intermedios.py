"""
generar_ep2_shots_intermedios.py
Genera las 8 tomas intermedias para Escena 1 en Modal FLUX.2 Klein 4B,
llevando la escena de 6 a 14 planos dinámicos (ritmo de 2.5s por corte).
"""

import os
import sys
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
REF_NIKOS = [
    r"c:\Users\Lenovo\Documents\Animaciones\Episodio_1\assets\img\ep1_escena_13_p2.png",
    r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_1_p1.png"
]

OUT_IMG_DIR = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img"
os.makedirs(OUT_IMG_DIR, exist_ok=True)

ITEMS = [
    {
        "filename": "ep2_escena_1_pov_techo.png",
        "prompt": "First person point of view looking up at the bedroom ceiling in the dark night. Soft shadows cast by tree branches outside the window, faint blue moonlight beam, a silent dark ceiling lamp fixture. Cozy nocturnal atmosphere. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_reloj_noche.png",
        "prompt": "Extreme close-up macro shot of a vintage analog alarm clock on a wooden nightstand in a dark nocturnal bedroom. The clock face illuminated by a gentle bedside lamp warm light, showing hands at 11:42 PM. Cozy atmosphere. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_ojos_alerta.png",
        "prompt": "Close-up macro of young boy Niko's expressive dark eyes wide open with intense comedic determination and hyper-focus. Messy teal hair bangs visible, band-aid on cheek. Blue nocturnal lighting. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_cerrando_ojos.png",
        "prompt": "Macro close-up shot of young boy Niko's eyes slowly closing gently, eyelashes fluttering, peaceful expression. Messy teal hair bangs, nocturnal deep blue shadows, cozy bedroom lighting. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_reloj_sonando.png",
        "prompt": "Comical macro close-up of a bright red retro alarm clock vibrating violently, motion blur lines, ringing bell hammer moving fast, sound waves radiating. Bright cheerful morning backdrop. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_cinta_tiempo.png",
        "prompt": "Conceptual visual timeline or filmstrip showing nighttime hours from 11:30 PM to 7:00 AM, with the middle section ripped out and replaced by a mysterious glowing black portal and floating question marks. Clean minimalist infographic concept. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_niko_desconcierto.png",
        "prompt": "Medium shot of young boy Niko shrugging with both hands open in complete comical bewilderment, looking directly at the camera with raised eyebrows and a baffled smile. Wearing yellow striped shirt and green vest, messy teal hair, band-aid on cheek. Bedroom daytime background. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_candado_zoom.png",
        "prompt": "Close-up dramatic focus on a stylized glowing red padlock secured over the memory vaults of a translucent holographic glowing brain, tiny sparks and glowing question mark floating above. Dark high-tech background. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    }
]

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-shots-intermedios-flux2", image=image)

@app.function(gpu="A100", timeout=1200)
def generar_imagenes_modal(prompts: list, ref_bytes_list: list, hf_token: str):
    from huggingface_hub import login
    import torch
    from diffusers import Flux2KleinPipeline
    from PIL import Image
    import io

    login(token=hf_token)
    print("🚀 Cargando FLUX.2 Klein 4B en Modal A100...")
    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=torch.bfloat16
    ).to("cuda")

    ref_images = [Image.open(io.BytesIO(b)).convert("RGB") for b in ref_bytes_list] if ref_bytes_list else []

    resultados = []
    for i, p in enumerate(prompts):
        print(f"🎬 Generando Micro-Plano {i+1}/{len(prompts)} en 16:9...")
        kwargs = {
            "prompt": p,
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1344,
            "height": 768
        }
        if ref_images:
            kwargs["image"] = ref_images

        img_out = pipe(**kwargs).images[0]
        byte_arr = io.BytesIO()
        img_out.save(byte_arr, format='PNG')
        resultados.append(byte_arr.getvalue())

    return resultados

def main():
    prompts = [item["prompt"] for item in ITEMS]
    ref_bytes = []
    for r in REF_NIKOS:
        if os.path.exists(r):
            with open(r, "rb") as rf:
                ref_bytes.append(rf.read())

    print(f"\n🎨 Lanzando generación de {len(prompts)} tomas intermedias en Modal...")
    with modal.enable_output():
        with app.run():
            imgs_bytes = generar_imagenes_modal.remote(prompts, ref_bytes, HF_TOKEN)

    for idx, b in enumerate(imgs_bytes):
        filename = ITEMS[idx]["filename"]
        out_file = os.path.join(OUT_IMG_DIR, filename)
        with open(out_file, "wb") as f:
            f.write(b)
        print(f"✅ Guardado: {filename}")

if __name__ == "__main__":
    main()
