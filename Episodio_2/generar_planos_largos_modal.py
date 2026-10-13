import os
import sys
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Cargar variables de entorno locales
def load_dotenv():
    env_file = r"c:\Users\Lenovo\Documents\Animaciones\.env"
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v

load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Niko Bible definitions inlined for Modal container compatibility
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

def prompt_niko(accion: str, plano: str = "medio", ambiente: str = "") -> str:
    partes = [ESTILO, NIKO, PLANOS.get(plano, PLANOS["medio"]), accion]
    if ambiente:
        partes.append(ambiente)
    return ", ".join(partes)

def prompt_escena(descripcion: str, plano: str = "general") -> str:
    return ", ".join([
        ESTILO,
        PLANOS.get(plano, PLANOS["general"]),
        descripcion,
        "all elements integrated into the scene lighting, cast shadows and glow reflected on surroundings",
    ])


OUT_DIR_EP2 = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img"
OUT_DIR_REMOTION = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_1\remotion_app\public\assets\img"
os.makedirs(OUT_DIR_EP2, exist_ok=True)
os.makedirs(OUT_DIR_REMOTION, exist_ok=True)

ITEMS = [
    {
        "filename": "ep2_escena_1_p12_a.png",
        "prompt": (
            "2D flat cartoon illustration style, clean bold outlines, flat shading, vibrant colors, "
            "Niko in blue-and-yellow striped pajamas sitting in bed rubbing his eyes in groggy morning awakening, "
            "warm golden morning sunlight coming through the window, confusion expression, 16:9, NO text, NO letters"
        )
    },
    {
        "filename": "ep2_escena_1_p13_a.png",
        "prompt": prompt_escena(
            "stylized glowing holographic human brain with master biological power switch and synaptic circuits gently powering down",
            plano="medio"
        )
    },
    {
        "filename": "ep2_escena_2_p1_a.png",
        "prompt": prompt_niko(
            "walking happily and casually on a sunny cartoon city sidewalk, whistling with eyes closed, oblivious to a loose stone on the path",
            plano="medio",
            ambiente="sunny city buildings in background"
        )
    },
    {
        "filename": "ep2_escena_2_p3_a.png",
        "prompt": prompt_escena(
            "futuristic cartoon brain memory filing cabinet with glowing holographic caution labels, danger warning triangles and safety shields",
            plano="detalle"
        )
    },
    {
        "filename": "ep2_escena_2_p4_a.png",
        "prompt": prompt_escena(
            "breathtaking wide view of the edge of the conscious neon city overlooking a massive dark purple foggy abyss of dreams",
            plano="general"
        )
    },
    {
        "filename": "ep2_escena_2_p5_a.png",
        "prompt": prompt_niko(
            "standing at the broken edge of a glowing golden synaptic bridge, looking down into mysterious purple fog with caution and wonder",
            plano="medio",
            ambiente="deep violet misty abyss"
        )
    }
]

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-planos-largos-flux2", image=image)

@app.function(gpu="A100", timeout=1200)
def generar_imagenes_modal(prompts: list, hf_token: str):
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

    resultados = []
    for i, p in enumerate(prompts):
        print(f"🎬 Generando imagen {i+1}/{len(prompts)}...")
        kwargs = {
            "prompt": p,
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1344,
            "height": 768
        }
        img_out = pipe(**kwargs).images[0]
        byte_arr = io.BytesIO()
        img_out.save(byte_arr, format='PNG')
        resultados.append(byte_arr.getvalue())

    return resultados

def main():
    prompts = [item["prompt"] for item in ITEMS]
    print(f"🎨 Generando {len(prompts)} imágenes extra en Modal usando prompt_niko()...")
    with modal.enable_output():
        with app.run():
            imgs_bytes = generar_imagenes_modal.remote(prompts, HF_TOKEN)

    for idx, b in enumerate(imgs_bytes):
        filename = ITEMS[idx]["filename"]
        p1 = os.path.join(OUT_DIR_EP2, filename)
        p2 = os.path.join(OUT_DIR_REMOTION, filename)
        with open(p1, "wb") as f:
            f.write(b)
        with open(p2, "wb") as f:
            f.write(b)
        print(f"✅ Guardado: {filename} ({len(b)} bytes)")

if __name__ == "__main__":
    main()
