"""
generar_planos_corregidos_y_escena5.py
Aplica los 3 blindajes definitivos:
  1. Regenera ep2_escena_3_p1.png en Plano Medio (cintura arriba, 12 años, 1 sola curita blanca).
  2. Rediseña Escena 5 en 5 planos dinámicos (3.5s - 5.5s), eliminando humanos en diagramas.
  3. Evalúa con CLIP, actualiza esquema maestro, compila en Remotion y masteriza a -14 LUFS.
"""

import os
import sys
import io
import json
import shutil
import subprocess
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
app = modal.App("ep2-blindaje-definitivo", image=image_modal)

@app.function(gpu="A100", timeout=800)
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
    from niko_bible import RUTA_CANONICA_NIKO, RUTA_CANONICA_PIJAMA
    from evaluador_coherencia import EvaluadorCoherencia

    with open(RUTA_CANONICA_NIKO, "rb") as f:
        bytes_canon_dia = f.read()
    with open(RUTA_CANONICA_PIJAMA, "rb") as f:
        bytes_canon_pijama = f.read()

    planos_meta = [
        # --- PLANO REGENERADO: ESCENA 3 PLANO 1 (Niko Biblioteca) ---
        {
            "nombre": "ep2_escena_3_p1.png",
            "prompt": (
                "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant saturated colors, 16:9 composition: "
                "medium shot from the waist up filling the frame: Niko, an athletic 12-year-old pre-teen adventurer boy, strictly identical to reference character: "
                "defined jawline, NOT chubby cheeks, small cute button nose, expressive dark brown eyes, messy spiky dark teal-green hair (#1F6B63) with loose curved curl at the crown, "
                "exactly ONE single small cream-white rectangular adhesive medical bandage on his left cheek, clear smooth skin on right cheek with NO second bandage, "
                "olive green utility cargo vest over yellow-and-orange horizontally striped shirt, "
                "holding a wooden pointer stick with a confident friendly smile, pointing toward two glowing translucent brain diagrams hovering in the air beside him, "
                "warm wooden library bookshelves background, soft warm lighting, no watermark, no text, no captions"
            ),
            "ref_bytes": bytes_canon_dia,
            "usa_ref": True,
            "es_niko": True,
            "es_pijama": False
        },
        # --- ESCENA 5: 5 PLANOS DINÁMICOS SIN HUMANOS EN DIAGRAMAS ---
        {
            "nombre": "ep2_escena_5_p1.png",
            "prompt": (
                "2D flat vector explainer infographic, clean bold lines, flat cel shading, vibrant colors, 16:9 composition: "
                "Futuristic cross-section diagram of the human brain with the thalamus highlighted in the center as an elegant glowing golden control tower station, "
                "bioluminescent circuitry, scientific educational illustration, pure architectural infographic, strictly ZERO humans, no people, no children, no characters, no text, no labels"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False,
            "es_pijama": False
        },
        {
            "nombre": "ep2_escena_5_p2.png",
            "prompt": (
                "2D flat vector explainer infographic, clean bold lines, flat cel shading, vibrant colors, 16:9 composition: "
                "Dynamic visual metaphor of sensory railway tracks entering the brain: glowing neon tracks carrying incoming sound waves, warm light rays, and vibrating tactile pulses at high speed into a central hub, "
                "pure biological technology infographic, strictly ZERO humans, no people, no characters, empty scene, no text"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False,
            "es_pijama": False
        },
        {
            "nombre": "ep2_escena_5_p3.png",
            "prompt": (
                "2D flat vector explainer infographic, clean bold lines, flat cel shading, vibrant colors, 16:9 composition: "
                "Stylized holographic routing console inside the brain sorting incoming sensory data packets, glowing visual streams and auditory signals flowing through gentle biological filters, "
                "pure futuristic interface infographic, strictly ZERO humans, no people, no characters, no text"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False,
            "es_pijama": False
        },
        {
            "nombre": "ep2_escena_5_p4.png",
            "prompt": (
                "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant saturated colors, 16:9 composition: "
                "Massive round stylized vault doors slowly closing shut with heavy soft-gold mechanical locks, gracefully shutting off the sensory railway lines, lights dimming smoothly, "
                "cinematic dramatic perspective, strictly ZERO humans, no people, no characters, empty scene, no text"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False,
            "es_pijama": False
        },
        {
            "nombre": "ep2_escena_5_p5.png",
            "prompt": (
                "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant saturated colors, 16:9 composition: "
                "Cozy close medium shot: Niko, an athletic 12-year-old pre-teen cartoon boy, sleeping peacefully in a comfortable bed, "
                "head resting on a soft blue pillow, eyes closed in serene calm sleep, dark teal-green messy hair with loose curl on crown, "
                "exactly ONE single small cream-white adhesive bandage on his left cheek, clear smooth skin on right cheek with NO second bandage, "
                "yellow sleeping shirt, dark cozy nighttime bedroom ambiance, gentle warm bedside lamp glow fading into night, peaceful dream atmosphere, no text, no watermark"
            ),
            "ref_bytes": bytes_canon_pijama,
            "usa_ref": True,
            "es_niko": True,
            "es_pijama": True
        }
    ]

    prompts = [p["prompt"] for p in planos_meta]
    refs = [p["ref_bytes"] for p in planos_meta]
    flags = [p["usa_ref"] for p in planos_meta]

    print("🚀 Generando en Modal A100 los 6 planos blindados...")
    with app.run():
        res_bytes = modal_gen.remote(prompts, refs, flags, HF_TOKEN)

    evaluador = EvaluadorCoherencia()

    for i, p in enumerate(planos_meta):
        out_p = IMG_DIR / p["nombre"]
        with open(out_p, "wb") as f:
            f.write(res_bytes[i])
        shutil.copy(str(out_p), str(PUBLIC_IMG / p["nombre"]))
        print(f"💾 Guardado: {p['nombre']}")

        if p["es_niko"]:
            ev = evaluador.evaluar_niko(str(out_p), es_pijama=p["es_pijama"])
            print(f"   🛡️ CLIP Score: {ev['score']:.1f}% -> {ev['mensaje']}")

    # ==============================================================
    # ACTUALIZAR ESQUEMA MAESTRO CON LAS NUEVAS DURACIONES DE PLANOS
    # ==============================================================
    print("\n📋 Actualizando esquema maestro...")
    schema_file = EP2_DIR / "esquema_maestro_ep2_tight.json"
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Asegurar Escena 1 Plano 13 con imagen corregida
    for plano in data["escenas"][0]["planos"]:
        if plano.get("id_plano") == 13:
            plano["imagen"] = "assets/img/ep2_escena_1_p12_a.png"

    # 2. Asegurar Escena 3 Plano 1 con imagen corregida
    data["escenas"][2]["planos"][0]["imagen"] = "assets/img/ep2_escena_3_p1.png"

    # 3. Reemplazar Escena 5 con los 5 planos rítmicos dinámicos
    planos_escena_5 = [
        {
            "id_plano": 1,
            "locucion_plano": "El segundo responsable es el Tálamo...",
            "palabras_clave_plano": ["el Tálamo"],
            "duracion_frames": 126,
            "animacion": "zoom_in_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_5_p1.png",
            "descripcion": "Diagrama de infografía del cerebro destacando la torre de control del tálamo"
        },
        {
            "id_plano": 2,
            "locucion_plano": "...la gran estación de trenes sensorial de tu cabeza. Cada sonido de la calle, cada roce de la sábana...",
            "palabras_clave_plano": ["estación de trenes sensorial", "sonido", "roce"],
            "duracion_frames": 150,
            "animacion": "paneo_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_5_p2.png",
            "descripcion": "Vías sensoriales luminosas transportando estímulos acústicos y táctiles hacia la estación"
        },
        {
            "id_plano": 3,
            "locucion_plano": "...y cada sombra pasa por el tálamo antes de llegar a tu mente consciente.",
            "palabras_clave_plano": ["sombra", "mente consciente"],
            "duracion_frames": 159,
            "animacion": "zoom_in_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_5_p3.png",
            "descripcion": "Consola holográfica enrutando y filtrando los datos sensoriales biológicos"
        },
        {
            "id_plano": 4,
            "locucion_plano": "Para que puedas dormirte, el tálamo cierra las puertas y corta todas las vías de entrada exterior.",
            "palabras_clave_plano": ["cierra las puertas", "corta las vías"],
            "duracion_frames": 189,
            "animacion": "zoom_in_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_5_p4.png",
            "descripcion": "Compuertas blindadas de bóveda sellándose y bloqueando los estímulos del exterior"
        },
        {
            "id_plano": 5,
            "locucion_plano": "Tus ojos se cierran, pero en realidad fue tu cerebro el que desconectó los cables.",
            "palabras_clave_plano": ["ojos se cierran", "desconectó los cables"],
            "duracion_frames": 175,
            "animacion": "paneo_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_5_p5.png",
            "descripcion": "Plano medio íntimo de Niko durmiendo plácidamente en su almohada con iluminación nocturna"
        }
    ]

    dur_escena_5 = sum(p["duracion_frames"] for p in planos_escena_5)
    assert dur_escena_5 == 799, f"Suma incorrecta Escena 5: {dur_escena_5}"

    data["escenas"][4]["audio"] = "assets/audio/voz_puck_ep2_escena_5.wav"
    data["escenas"][4]["archivos_generados"] = {
        "audio_tts": "assets/audio/voz_puck_ep2_escena_5.wav"
    }
    data["escenas"][4]["duracion_frames"] = dur_escena_5
    data["escenas"][4]["planos"] = planos_escena_5

    total_frames = sum(e["duracion_frames"] for e in data["escenas"][:5])
    data["metadata"]["duracion_total_frames"] = total_frames
    data["metadata"]["duracion_total_segundos"] = round(total_frames / 30.0, 2)

    with open(schema_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Esquema maestro actualizado: Total {total_frames} frames ({total_frames/30.0:.2f}s)")

    # ==============================================================
    # RENDERIZAR EN REMOTION Y MASTERIZAR A -14 LUFS
    # ==============================================================
    print("\n🎬 Renderizando en Remotion...")
    cmd_render = ["npx", "remotion", "render", "Episodio2", "out/ep2_tight_full.mp4", "--concurrency=4"]
    subprocess.run(cmd_render, cwd=str(REMOTION_DIR), shell=True, check=True)

    print("\n🎛️ Masterizando audio a estándar YouTube (-14 LUFS)...")
    remotion_out = REMOTION_DIR / "out" / "ep2_tight_full.mp4"
    cmd_master = [
        "py", "-3.13", str(MOTOR_DIR / "masterizar.py"),
        str(remotion_out),
        "--copiar-video"
    ]
    subprocess.run(cmd_master, cwd=str(BASE_DIR), check=True)

    mastered_out = REMOTION_DIR / "out" / "ep2_tight_full_youtube.mp4"
    final_dest = EP2_DIR / "ep2_tight_final.mp4"
    shutil.copy(str(mastered_out), str(final_dest))
    print(f"\n🎉 VIDEO FINAL EXPORTADO EXITOSAMENTE A: {final_dest.name}")

if __name__ == "__main__":
    main()
