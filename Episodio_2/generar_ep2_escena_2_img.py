import os
import sys
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
REF_NIKOS = [
    r"c:\Users\Lenovo\Documents\Animaciones\Episodio_1\assets\img\ep1_escena_13_p2.png",
    r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_1_niko_desconcierto.png"
]

OUT_IMG_DIR = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img"
os.makedirs(OUT_IMG_DIR, exist_ok=True)

ITEMS = [
    {
        "filename": "ep2_escena_2_p1.png",
        "prompt": "Young boy Niko tripping clumsily over a small stone on a sunny cartoon city sidewalk, arms flailing with comical funny surprised face. Wearing his signature messy teal hair, band-aid on cheek, yellow-striped t-shirt, green vest, blue shorts, sneakers. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_2_p2.png",
        "prompt": "Close-up of young boy Niko reacting comically after sipping from a steaming hot ceramic mug, sticking his pink tongue out with funny heat expression, wavy steam clouds rising. Teal hair, band-aid on cheek, yellow striped shirt and green vest. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_2_p3.png",
        "prompt": "Whimsical cartoon memory archive room: cute little mental librarian workers organizing shiny glowing memory spheres into glowing tall blue cabinets. High-tech clean mental vault. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_2_p4.png",
        "prompt": "Breathtaking cinematic bridge made of glowing synaptic neurons and golden dendrites, stretching from a warm conscious city across a vast chasm into deep mysterious violet dream fog. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    },
    {
        "filename": "ep2_escena_2_p5.png",
        "prompt": "Young boy Niko standing at the edge of the glowing neuronal bridge, looking down into the misty deep purple abyss with wide awe-struck eyes and curiosity. Above the void, a stylized glowing red locked padlock symbol floats. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO text, NO letters, NO words."
    }
]

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-escena-2-flux2", image=image)

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
        print(f"🎬 Generando Escena 2 Plano {i+1}/{len(prompts)}...")
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

    print(f"\n🎨 Generando {len(prompts)} imágenes de Escena 2 en Modal...")
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
