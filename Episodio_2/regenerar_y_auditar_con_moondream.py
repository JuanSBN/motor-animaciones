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

# Configuración de Modal
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-regenerar-qa-flux2", image=image)

@app.function(gpu="A100", timeout=1200)
def generar_imagenes_modal(prompts: list, ref_bytes: list, hf_token: str, use_ref_flags: list):
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

    ref_imgs = [Image.open(io.BytesIO(b)).convert("RGB") for b in ref_bytes] if ref_bytes else []

    resultados = []
    for i, p in enumerate(prompts):
        use_ref = use_ref_flags[i] if i < len(use_ref_flags) else False
        tipo = "con conditioning de Niko" if (use_ref and ref_imgs) else "Text-to-Image PURO"
        print(f"🎬 Generando {i+1}/{len(prompts)} [{tipo}]...")
        
        kwargs = {
            "prompt": p,
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1344,
            "height": 768
        }
        if use_ref and ref_imgs:
            kwargs["image"] = ref_imgs

        img_out = pipe(**kwargs).images[0]
        byte_arr = io.BytesIO()
        img_out.save(byte_arr, format='PNG')
        resultados.append(byte_arr.getvalue())

    return resultados

def auditar_con_moondream(gate, ruta_local: str, qa_type: str) -> bool:
    print(f"\n🔍 Auditando {os.path.basename(ruta_local)} con Moondream en Oracle VM...")
    if qa_type == "isolated_brain":
        pregunta = (
            "Examine this image carefully: Is there a human neck, torso, or headless human body under the brain? "
            "Answer PASS if it is an isolated floating brain without body/neck parts, or FAIL if a human neck or body is visible."
        )
        resp = gate.consultar_moondream(ruta_local, pregunta)
        print(f"   Veredicto Moondream: {resp}")
        return "fail" not in resp.lower() and ("pass" in resp.lower() or "isolated" in resp.lower() or "no" in resp.lower())
    elif qa_type == "niko_check":
        pregunta = (
            "Analyze the character in this image: Does he have teal-green hair and a small band-aid? "
            "Are there severe face deformities or text hallucinations? "
            "Answer PASS or FAIL with a brief reason."
        )
        resp = gate.consultar_moondream(ruta_local, pregunta)
        print(f"   Veredicto Moondream: {resp}")
        return "fail" not in resp.lower()
    return True

def main():
    sys.path.append(r"c:\Users\Lenovo\Documents\Animaciones\motor_animaciones")
    from niko_bible import prompt_niko, prompt_escena, RUTA_CANONICA_NIKO
    from oracle_moondream_gate import OracleMoondreamGate

    items_to_generate = [
        {
            "filename": "ep2_escena_1_p13_a.png",
            "prompt": (
                "2D flat vector cartoon explainer illustration style, clean bold outlines, flat shading, vibrant colors, "
                "an isolated glowing electric-blue holographic human brain diagram, floating completely alone in deep dark navy space, "
                "stylized synaptic circuit lines powering down, subtle scientific interface grid, "
                "NO human body, NO head, NO neck, NO shoulders, NO torso, NO face, NO letters, NO text, 16:9 composition"
            ),
            "use_ref": False,
            "qa_type": "isolated_brain"
        },
        {
            "filename": "ep2_escena_2_p5_a.png",
            "prompt": prompt_niko(
                "standing with caution and wonder at the broken edge of a glowing golden synaptic bridge, looking down into mysterious purple fog, wearing his iconic green vest over yellow-striped shirt",
                plano="medio",
                ambiente="deep violet misty abyss with faint floating glowing particles"
            ),
            "use_ref": True,
            "qa_type": "niko_check"
        }
    ]

    ref_bytes = []
    if os.path.exists(RUTA_CANONICA_NIKO):
        with open(RUTA_CANONICA_NIKO, "rb") as f:
            ref_bytes.append(f.read())
        print(f"✅ Imagen canónica de Niko cargada desde {RUTA_CANONICA_NIKO}")
    else:
        print("⚠️ No se encontró la imagen canónica de Niko.")

    prompts = [item["prompt"] for item in items_to_generate]
    use_ref_flags = [item["use_ref"] for item in items_to_generate]

    print(f"🚀 Iniciando generación de {len(items_to_generate)} imágenes en Modal...")
    with modal.enable_output():
        with app.run():
            imgs_bytes = generar_imagenes_modal.remote(prompts, ref_bytes, HF_TOKEN, use_ref_flags)

    gate = OracleMoondreamGate()
    print(f"🛡️ Moondream QA Gate conectado: {gate.disponible}")

    for idx, b in enumerate(imgs_bytes):
        item = items_to_generate[idx]
        filename = item["filename"]
        temp_path = os.path.join(OUT_DIR_EP2, f"temp_{filename}")
        final_path_ep2 = os.path.join(OUT_DIR_EP2, filename)
        final_path_remotion = os.path.join(OUT_DIR_REMOTION, filename)

        with open(temp_path, "wb") as f:
            f.write(b)

        # QA con Moondream
        aprobado = auditar_con_moondream(gate, temp_path, item["qa_type"])
        if aprobado:
            print(f"🎉 QA APROBADO para {filename}! Guardando...")
            shutil.copy2(temp_path, final_path_ep2)
            shutil.copy2(temp_path, final_path_remotion)
        else:
            print(f"⚠️ QA FALLÓ para {filename}. Se guarda provisionalmente.")
            shutil.copy2(temp_path, final_path_ep2)
            shutil.copy2(temp_path, final_path_remotion)

        if os.path.exists(temp_path):
            os.remove(temp_path)

    gate.limpiar_entorno()
    print("\n✅ Proceso de generación y auditoría finalizado.")

if __name__ == "__main__":
    main()
