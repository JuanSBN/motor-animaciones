import os
import sys
import io
import shutil
import modal
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

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

OUT_DIR_EP2 = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img"
OUT_DIR_REMOTION = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_1\remotion_app\public\assets\img"

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-regenerar-niko", image=image)

@app.function(gpu="A100", timeout=600)
def generar_imagen_modal(prompt: str, ref_bytes: bytes, hf_token: str):
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

    ref_img = [Image.open(io.BytesIO(ref_bytes)).convert("RGB")]
    print("🎬 Generando Niko con conditioning canónico de ep2_escena_2_p1...")

    img_out = pipe(
        prompt=prompt,
        image=ref_img,
        num_inference_steps=4,
        guidance_scale=3.5,
        width=1344,
        height=768
    ).images[0]

    byte_arr = io.BytesIO()
    img_out.save(byte_arr, format="PNG")
    return byte_arr.getvalue()

def main():
    sys.path.append(r"c:\Users\Lenovo\Documents\Animaciones\motor_animaciones")
    from niko_bible import prompt_niko, RUTA_CANONICA_NIKO

    with open(RUTA_CANONICA_NIKO, "rb") as f:
        bytes_niko = f.read()

    p = prompt_niko(
        "standing smiling warmly, holding a small wooden pointer and pointing up at a friendly glowing cartoon hologram of a brain floating in the air, exact same facial features as reference boy, exactly ONE small blue band-aid on left cheek, clean smooth right cheek with NO band-aids",
        plano="medio",
        ambiente="warm cozy library room background with soft wooden shelves"
    )

    print("🚀 Solicitando generación en Modal...")
    with modal.enable_output():
        with app.run():
            img_bytes = generar_imagen_modal.remote(p, bytes_niko, HF_TOKEN)

    f1 = os.path.join(OUT_DIR_EP2, "ep2_escena_3_p1.png")
    f2 = os.path.join(OUT_DIR_REMOTION, "ep2_escena_3_p1.png")

    with open(f1, "wb") as f:
        f.write(img_bytes)
    with open(f2, "wb") as f:
        f.write(img_bytes)

    print("✅ ep2_escena_3_p1.png regenerada y guardada exitosamente!")

if __name__ == "__main__":
    main()
