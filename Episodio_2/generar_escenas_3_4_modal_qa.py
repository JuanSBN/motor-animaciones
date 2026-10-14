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
os.makedirs(OUT_DIR_EP2, exist_ok=True)
os.makedirs(OUT_DIR_REMOTION, exist_ok=True)

# Configuración de Modal
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-escenas-3-4-flux2", image=image)

@app.function(gpu="A100", timeout=1200)
def generar_imagenes_modal(prompts: list, ref_bytes_list: list, hf_token: str, use_ref_flags: list):
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
        use_ref = use_ref_flags[i] if i < len(use_ref_flags) else False
        ref_bytes = ref_bytes_list[i] if (i < len(ref_bytes_list) and ref_bytes_list[i]) else None
        ref_img = [Image.open(io.BytesIO(ref_bytes)).convert("RGB")] if (use_ref and ref_bytes) else None

        tipo = "con conditioning de Niko" if ref_img else "Text-to-Image PURO"
        print(f"🎬 Generando {i+1}/{len(prompts)} [{tipo}]...")

        kwargs = {
            "prompt": p,
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1344,
            "height": 768
        }
        if ref_img:
            kwargs["image"] = ref_img

        img_out = pipe(**kwargs).images[0]
        byte_arr = io.BytesIO()
        img_out.save(byte_arr, format='PNG')
        resultados.append(byte_arr.getvalue())

    return resultados

def auditar_con_moondream(gate, ruta_local: str, qa_type: str) -> bool:
    print(f"🔍 Auditando {os.path.basename(ruta_local)} con Moondream...")
    if qa_type == "niko":
        p = "Does the cartoon character have teal hair and a bandage on his cheek? Answer PASS or FAIL."
        resp = gate.consultar_moondream(ruta_local, p)
        print(f"   Veredicto: {resp}")
        return "fail" not in resp.lower()
    elif qa_type == "diagram":
        p = "Is there any human body, neck, or strange anatomy in this diagram? Answer PASS if it is an isolated object/diagram without human bodies, or FAIL if human body parts appear."
        resp = gate.consultar_moondream(ruta_local, p)
        print(f"   Veredicto: {resp}")
        return "fail" not in resp.lower()
    return True

def main():
    sys.path.append(r"c:\Users\Lenovo\Documents\Animaciones\motor_animaciones")
    from niko_bible import prompt_niko, prompt_escena, RUTA_CANONICA_NIKO, RUTA_CANONICA_PIJAMA
    from oracle_moondream_gate import OracleMoondreamGate

    with open(RUTA_CANONICA_NIKO, "rb") as f:
        bytes_niko_canon = f.read()
    with open(RUTA_CANONICA_PIJAMA, "rb") as f:
        bytes_niko_pijama = f.read()

    ITEMS = [
        # --- ESCENA 3 ---
        {
            "filename": "ep2_escena_3_p1.png",
            "prompt": prompt_niko(
                "wearing his iconic green vest over yellow-striped t-shirt, excitedly pointing with a wooden pointer stick at a glowing friendly cartoon brain illustration",
                plano="medio",
                ambiente="warm cozy library studio with soft background illumination"
            ),
            "ref": bytes_niko_canon,
            "use_ref": True,
            "qa": "niko"
        },
        {
            "filename": "ep2_escena_3_p2.png",
            "prompt": (
                "2D flat vector cartoon explainer illustration, clean bold outlines, flat shading, vibrant colors, "
                "isolated glowing golden seahorse-shaped organ representing the hippocampus, gently glowing with warm amber synaptic light, "
                "floating peacefully against a deep dark navy blue scientific background, NO human body, NO head, NO neck, NO torso, NO text"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_3_p3.png",
            "prompt": prompt_escena(
                "colorful floating glowing memory orbs flowing smoothly like a stream of light into a central brain control console, each orb showing clean cartoon icons of senses like sight, sound, and touch",
                plano="general"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_3_p4.png",
            "prompt": prompt_escena(
                "cute friendly cartoon memory archivists organizing glowing colorful memory spheres into tall sleek modular filing cabinets, clean futuristic library archive inside the mind",
                plano="medio"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_3_p5.png",
            "prompt": prompt_escena(
                "close-up of a whimsical retro-futuristic cartoon surveillance security camera with a glowing red blinking REC indicator light, vigilantly watching over memory archives",
                plano="detalle"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_3_p6.png",
            "prompt": prompt_niko(
                "giving a cheerful thumbs-up gesture next to a glowing cartoon security monitor, confident and smiling",
                plano="medio",
                ambiente="clean cartoon security room"
            ),
            "ref": bytes_niko_canon,
            "use_ref": True,
            "qa": "niko"
        },

        # --- ESCENA 4 ---
        {
            "filename": "ep2_escena_4_p1.png",
            "prompt": prompt_niko(
                "sitting up in cozy bed wearing comfortable bedtime yellow sleeping shirt, looking up at the ceiling with quiet bedtime contemplation",
                plano="medio",
                ambiente="peaceful dark blue bedroom at night with soft moonlit window",
                pijama=True
            ),
            "ref": bytes_niko_pijama,
            "use_ref": True,
            "qa": "niko"
        },
        {
            "filename": "ep2_escena_4_p2.png",
            "prompt": (
                "2D flat vector cartoon diagram, clean outlines: cross section profile of brain where outer cerebral cortex still glows softly awake in gentle yellow, while inner hippocampus powers down into deep calm navy blue, clear contrast of brain regions, NO human face, NO neck, NO torso, NO text"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_4_p3.png",
            "prompt": prompt_escena(
                "sleek stylized digital countdown clock floating in dark space displaying 10:00 minutes with a soft mechanical toggle switch gently flipping to OFF position",
                plano="detalle"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_4_p4.png",
            "prompt": prompt_escena(
                "extreme close-up of a retro camera lens where the glowing red REC light just clicked OFF, gentle fade out of indicator lights",
                plano="detalle"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_4_p5.png",
            "prompt": prompt_escena(
                "wide peaceful shot of a quiet bedtime bedroom: night lamp casting a warm gentle amber glow on the wooden floor and wall, silent serene atmosphere",
                plano="general"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        },
        {
            "filename": "ep2_escena_4_p6.png",
            "prompt": prompt_niko(
                "resting head peacefully on white soft pillow with eyes half-open drowsily, calm tranquil half-asleep expression",
                plano="primer_plano",
                ambiente="cozy bed sheets with soft ambient room lighting",
                pijama=True
            ),
            "ref": bytes_niko_pijama,
            "use_ref": True,
            "qa": "niko"
        },
        {
            "filename": "ep2_escena_4_p7.png",
            "prompt": prompt_escena(
                "whimsical cartoon mental filing cabinet with a cute friendly wooden sign hanging that reads CLOSED, memory spheres gently dissolving into soft glowing stardust, peaceful end of day",
                plano="medio"
            ),
            "ref": None,
            "use_ref": False,
            "qa": "diagram"
        }
    ]

    prompts = [item["prompt"] for item in ITEMS]
    ref_bytes_list = [item["ref"] for item in ITEMS]
    use_ref_flags = [item["use_ref"] for item in ITEMS]

    print(f"🚀 Generando {len(ITEMS)} imágenes en Modal...")
    with modal.enable_output():
        with app.run():
            imgs_bytes = generar_imagenes_modal.remote(prompts, ref_bytes_list, HF_TOKEN, use_ref_flags)

    gate = OracleMoondreamGate()
    print(f"🛡️ Moondream QA Gate conectado: {gate.disponible}")

    for idx, b in enumerate(imgs_bytes):
        item = ITEMS[idx]
        fname = item["filename"]
        p1 = os.path.join(OUT_DIR_EP2, fname)
        p2 = os.path.join(OUT_DIR_REMOTION, fname)

        with open(p1, "wb") as f:
            f.write(b)
        with open(p2, "wb") as f:
            f.write(b)

        # QA check
        auditar_con_moondream(gate, p1, item["qa"])
        print(f"✅ Guardado y verificado: {fname} ({len(b)} bytes)")

    gate.limpiar_entorno()
    print("\n🎉 ¡Todas las imágenes de Escenas 3 y 4 generadas y guardadas exitosamente!")

if __name__ == "__main__":
    main()
