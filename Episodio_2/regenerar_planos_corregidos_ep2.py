import os
import sys
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
REF_NIKOS = [
    r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_1_p1.png"
]

OUT_IMG_DIR = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img"
os.makedirs(OUT_IMG_DIR, exist_ok=True)

ITEMS = [
    {
        "filename": "ep2_escena_1_p2.png",
        "prompt": "Young boy Niko lying in his cozy bed under the blanket, wearing comfortable yellow-and-orange striped pajama t-shirt (NO vest, NO jacket, NO outdoor shoes), glancing determinedly at an analog alarm clock on his wooden nightstand. Intense comical focused expression, one eyebrow raised, messy teal hair. Cozy bedroom nighttime lighting. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_reloj_sonando.png",
        "prompt": "Comical macro close-up of a classic red metal twin-bell alarm clock vibrating violently on a wooden nightstand, hammer ringing the bells, motion shock lines and ringing sound waves. Clean minimalist clock face with simple round black dots for hours, simple clock hands at 7:00, absolutely NO letters, NO distorted digits, NO numbers. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors."
    },
    {
        "filename": "ep2_escena_1_p4.png",
        "prompt": "Dynamic comical jump-cut: bright golden morning sunlight bursts through the bedroom window. Young boy Niko sits up startled in his bed, wearing yellow striped pajama t-shirt and pajama shorts (bare feet, NO vest, NO sneakers, NO shoes). Crazy messy teal bed-head hair, wide sleepy squinting eyes, startled comical face, blanket tangled around legs. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_1_p5.png",
        "prompt": "Young boy Niko sitting on the edge of his bed in pajamas (yellow-and-orange striped pajama t-shirt, sleep shorts, bare feet, NO vest, NO sneakers). Messy teal hair, scratching the back of his neck with a comical baffled shrug expression. Behind him on the wall, a mysterious glowing dark void portal with question marks. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    }
]

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-regenerar-corregidos", image=image)

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
        print(f"🎬 Generando Imagen Corregida {i+1}/{len(prompts)}...")
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

    print(f"\n🎨 Regenerando {len(prompts)} imágenes corregidas en Modal...")
    with modal.enable_output():
        with app.run():
            imgs_bytes = generar_imagenes_modal.remote(prompts, ref_bytes, HF_TOKEN)

    for idx, b in enumerate(imgs_bytes):
        filename = ITEMS[idx]["filename"]
        out_file = os.path.join(OUT_IMG_DIR, filename)
        with open(out_file, "wb") as f:
            f.write(b)
        print(f"✅ Guardado corregido: {filename}")

if __name__ == "__main__":
    main()
