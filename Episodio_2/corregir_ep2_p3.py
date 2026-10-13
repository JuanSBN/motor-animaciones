import os
import sys
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
REF_NIKO = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_2_p1.png"

OUT_DIR_EP2 = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img"
OUT_DIR_REMOTION = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_1\remotion_app\public\assets\img"

PROMPT = (
    "A single solo young boy Niko standing inside a high-tech brain memory archive room, profile view. "
    "He is looking at a glowing holographic transparent screen displaying a glowing brain graphic and bright amber danger warning icons with exclamation marks. "
    "Niko has messy teal hair, a small band-aid on cheek, yellow-striped t-shirt, open green vest, casual pants, sneakers. "
    "Only one single boy in the entire scene, completely solo, no other people, no duplicates, no clones. "
    "2D flat cartoon illustration style, clean lineart, flat shading, vibrant colorful palette, 16:9, blank interface without any typography, NO text, NO letters, NO words, NO subtitles."
)

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-corregir-p3", image=image)

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

    ref_img = Image.open(io.BytesIO(ref_bytes)).convert("RGB") if ref_bytes else None

    print(f"🎬 Generando imagen corregida para Escena 2 Plano 3...")
    kwargs = {
        "prompt": prompt,
        "num_inference_steps": 4,
        "guidance_scale": 3.5,
        "width": 1344,
        "height": 768
    }
    if ref_img:
        kwargs["image"] = [ref_img]

    img_out = pipe(**kwargs).images[0]
    byte_arr = io.BytesIO()
    img_out.save(byte_arr, format='PNG')
    return byte_arr.getvalue()

def main():
    ref_bytes = None
    if os.path.exists(REF_NIKO):
        with open(REF_NIKO, "rb") as f:
            ref_bytes = f.read()

    print("🎨 Ejecutando generación en Modal...")
    with modal.enable_output():
        with app.run():
            img_bytes = generar_imagen_modal.remote(PROMPT, ref_bytes, HF_TOKEN)

    filename = "ep2_escena_2_p3.png"
    p1 = os.path.join(OUT_DIR_EP2, filename)
    p2 = os.path.join(OUT_DIR_REMOTION, filename)

    with open(p1, "wb") as f:
        f.write(img_bytes)
    with open(p2, "wb") as f:
        f.write(img_bytes)

    print(f"✅ Imagen actualizada en {p1} y {p2} ({len(img_bytes)} bytes)")

if __name__ == "__main__":
    main()
