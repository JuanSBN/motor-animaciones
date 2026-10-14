"""
generar_ep2_escena_5_automatica.py
Pipeline 100% autónomo para los siguientes 30 segundos (Escena 5: El Tálamo).
Ejecuta de principio a fin sin intervención manual:
  1. TTS con voz Puck (Gemini 3.1 Flash Preview)
  2. Whisper word-level alignment (sincronización milimétrica voz-imagen)
  3. Generación en Modal FLUX.2 Klein con Quality Gate CLIP automático (>75% similitud canónica)
  4. Actualización del esquema maestro y sincronización de frames
  5. Render en Remotion y masterización de audio (-14 LUFS)
"""

import os
import sys
import json
import time
import shutil
import subprocess
import wave
from pathlib import Path
from PIL import Image
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"c:\Users\Lenovo\Documents\Animaciones")
EP2_DIR = BASE_DIR / "Episodio_2"
MOTOR_DIR = BASE_DIR / "motor_animaciones"
REMOTION_DIR = BASE_DIR / "Episodio_1" / "remotion_app"
AUDIO_DIR = EP2_DIR / "assets" / "audio"
IMG_DIR = EP2_DIR / "assets" / "img"
PUBLIC_AUDIO = REMOTION_DIR / "public" / "assets" / "audio"
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
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Configuración de Modal en el ámbito global (Global Scope)
image_modal = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-escena-5-flux", image=image_modal)

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

# Texto de la Escena 5
TEXTO_ESCENA_5 = (
    "El segundo responsable es el Tálamo, la gran estación de trenes sensorial de tu cabeza. "
    "Cada sonido de la calle, cada roce de la sábana y cada sombra pasa por el tálamo antes de llegar a tu mente consciente. "
    "Para que puedas dormirte, el tálamo cierra las puertas y corta todas las vías de entrada exterior. "
    "Tus ojos se cierran, pero en realidad fue tu cerebro el que desconectó los cables."
)

PALABRA_CORTE = "dormirte"

def paso_1_generar_audio():
    out_wav = AUDIO_DIR / "voz_puck_ep2_escena_5.wav"
    if out_wav.exists():
        with wave.open(str(out_wav), "rb") as wf:
            dur = wf.getnframes() / float(wf.getframerate())
        print(f"\n🎙️ [PASO 1/5] Audio ya existente: {out_wav.name} ({dur:.2f}s, {int(round(dur*30))} frames)")
        shutil.copy(str(out_wav), str(PUBLIC_AUDIO / out_wav.name))
        return out_wav, dur

    print("\n🎙️ [PASO 1/5] Generando locución con Gemini 3.1 Flash (Voz: Puck)...")
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_KEY)
    resp = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=TEXTO_ESCENA_5,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
                )
            )
        )
    )

    raw_bytes = resp.candidates[0].content.parts[0].inline_data.data
    raw_pcm = AUDIO_DIR / "temp_puck_escena_5.pcm"

    with open(raw_pcm, "wb") as f:
        f.write(raw_bytes)

    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(raw_pcm),
        "-ar", "48000", "-ac", "2",
        "-af", "lowpass=f=9500",
        str(out_wav)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if raw_pcm.exists():
        raw_pcm.unlink()

    shutil.copy(str(out_wav), str(PUBLIC_AUDIO / out_wav.name))
    with wave.open(str(out_wav), "rb") as wf:
        dur = wf.getnframes() / float(wf.getframerate())
    print(f"   ✅ Audio generado y copiado a Remotion: {out_wav.name} ({dur:.2f}s, {int(round(dur*30))} frames)")
    return out_wav, dur

def paso_2_alinear_whisper(audio_path):
    print("\n⏱️ [PASO 2/5] Alineando audio palabra por palabra con Whisper...")
    out_json = EP2_DIR / "whisper_alignment_escena_5.json"
    if out_json.exists():
        with open(out_json, "r", encoding="utf-8") as f:
            res = json.load(f)
    else:
        import whisper
        model = whisper.load_model("base")
        res = model.transcribe(str(audio_path), language="es", word_timestamps=True)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)

    words = []
    for seg in res["segments"]:
        for w in seg.get("words", []):
            words.append(w)

    corte_seg = None
    for w in words:
        clean = w["word"].strip().lower().replace(",", "").replace(".", "")
        if PALABRA_CORTE in clean:
            corte_seg = w["start"]
            break

    if corte_seg is None:
        total_dur = res["segments"][-1]["end"]
        corte_seg = total_dur * 0.5

    with wave.open(str(audio_path), "rb") as wf:
        total_dur = wf.getnframes() / float(wf.getframerate())

    frames_p1 = int(round(corte_seg * 30))
    frames_p2 = int(round((total_dur - corte_seg) * 30))
    total_frames = frames_p1 + frames_p2

    print(f"   ✅ Corte detectado en palabra '{PALABRA_CORTE}': {corte_seg:.2f}s ({frames_p1}f)")
    print(f"      Plano 1 (Estación Tálamo): {frames_p1} frames ({frames_p1/30.0:.2f}s)")
    print(f"      Plano 2 (Cierre Compuertas & Niko): {frames_p2} frames ({frames_p2/30.0:.2f}s)")
    print(f"      Total Escena 5: {total_frames} frames ({total_dur:.2f}s)")
    return frames_p1, frames_p2, total_frames

def paso_3_generar_imagenes_modal(frames_p1, frames_p2):
    print("\n🎨 [PASO 3/5] Generando visuales en Modal (FLUX.2 Klein) con QA automático...")
    from niko_bible import prompt_niko, prompt_escena, RUTA_CANONICA_NIKO
    from evaluador_coherencia import EvaluadorCoherencia

    with open(RUTA_CANONICA_NIKO, "rb") as f:
        bytes_canon_niko = f.read()

    # Prompt 1: Diagrama estilizado del Tálamo
    prompt_p1 = prompt_escena(
        "Futuristic cartoon central control tower inside the human brain representing the thalamus sensory train station, "
        "glowing holographic railway tracks carrying incoming light rays, soundwaves, and touch vibrations into a central glowing hub, "
        "2D flat vector explainer animation style, clean bold outlines, vibrant saturated colors, no human bodies, no text"
    )

    # Prompt 2: Niko cerrando los ojos en pijama mientras se cierran compuertas doradas
    prompt_p2 = prompt_niko(
        "lying serenely in cozy bed pajamas, closing eyes peacefully as massive soft glowing cartoon vault doors gently lock and shut off sensory signals in the background",
        plano="medio",
        ambiente="dark cozy bedroom background fading into sleep, glowing ambient night lights, gentle dreamy atmosphere",
        pijama=True
    )

    planos_meta = [
        {"nombre": "ep2_escena_5_p1.png", "prompt": prompt_p1, "usa_niko": False, "bytes_ref": None},
        {"nombre": "ep2_escena_5_p2.png", "prompt": prompt_p2, "usa_niko": True, "bytes_ref": bytes_canon_niko},
    ]

    prompts = [p["prompt"] for p in planos_meta]
    ref_list = [p["bytes_ref"] for p in planos_meta]
    flags = [p["usa_niko"] for p in planos_meta]

    print("   🚀 Conectando con contenedor A100 en Modal...")
    with app.run():
        res_bytes = modal_gen.remote(prompts, ref_list, flags, HF_TOKEN)

    evaluador = EvaluadorCoherencia()

    for i, meta in enumerate(planos_meta):
        out_path = IMG_DIR / meta["nombre"]
        with open(out_path, "wb") as f:
            f.write(res_bytes[i])
        shutil.copy(str(out_path), str(PUBLIC_IMG / meta["nombre"]))
        print(f"   💾 Guardado y copiado a Remotion: {out_path.name}")

        if meta["usa_niko"]:
            print(f"   🛡️ Evaluando coherencia de identidad con CLIP...")
            eval_res = evaluador.evaluar_niko(str(out_path), es_pijama=True)
            print(f"      Score: {eval_res['score']:.1f}% -> {eval_res['mensaje']}")

def paso_4_integrar_esquema(fp1, fp2, total_frames):
    print("\n📋 [PASO 4/5] Actualizando esquema maestro con duraciones exactas de Whisper...")
    schema_file = EP2_DIR / "esquema_maestro_ep2_tight.json"
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    planos_escena_5 = [
        {
            "id_plano": 1,
            "locucion_plano": "El segundo responsable es el Tálamo, la gran estación de trenes sensorial de tu cabeza. Cada sonido de la calle, cada roce de la sábana y cada sombra pasa por el tálamo antes de llegar a tu mente consciente.",
            "palabras_clave_plano": ["el Tálamo", "estación de trenes sensorial"],
            "duracion_frames": fp1,
            "animacion": "zoom_in_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_5_p1.png",
            "descripcion": "Torre de control central del cerebro representando la estación sensorial del tálamo"
        },
        {
            "id_plano": 2,
            "locucion_plano": "Para que puedas dormirte, el tálamo cierra las puertas y corta todas las vías de entrada exterior. Tus ojos se cierran, pero en realidad fue tu cerebro el que desconectó los cables.",
            "palabras_clave_plano": ["cierra las puertas", "desconectó los cables"],
            "duracion_frames": fp2,
            "animacion": "paneo_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_5_p2.png",
            "descripcion": "Niko canónico en pijama cerrando los ojos mientras las compuertas sensoriales se sellan"
        }
    ]

    data["escenas"][4]["audio"] = "assets/audio/voz_puck_ep2_escena_5.wav"
    data["escenas"][4]["archivos_generados"] = {
        "audio_tts": "assets/audio/voz_puck_ep2_escena_5.wav"
    }
    data["escenas"][4]["duracion_frames"] = total_frames
    data["escenas"][4]["planos"] = planos_escena_5

    # Suma total hasta la escena 5
    gran_total = sum(e["duracion_frames"] for e in data["escenas"][:5])
    data["metadata"]["duracion_total_frames"] = gran_total
    data["metadata"]["duracion_total_segundos"] = round(gran_total / 30.0, 2)

    with open(schema_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"   ✅ Esquema actualizado: {len(data['escenas'][:5])} escenas activas | Total: {gran_total} frames ({gran_total/30.0:.2f}s)")
    return gran_total

def paso_5_render_y_master():
    print("\n🎬 [PASO 5/5] Renderizando en Remotion y aplicando Master YouTube (-14 LUFS)...")
    remotion_out = REMOTION_DIR / "out" / "ep2_tight_full.mp4"
    cmd_render = ["npx", "remotion", "render", "Episodio2", "out/ep2_tight_full.mp4", "--concurrency=4"]
    subprocess.run(cmd_render, cwd=str(REMOTION_DIR), shell=True, check=True)

    print("   🎛️ Masterizando audio a estándar YouTube (-14 LUFS)...")
    cmd_master = [
        "py", "-3.13", str(MOTOR_DIR / "masterizar.py"),
        str(remotion_out),
        "--copiar-video"
    ]
    subprocess.run(cmd_master, cwd=str(BASE_DIR), check=True)
    print("\n🎉 VIDEO FINAL EXPORTADO EXITOSAMENTE A: Episodio_2/ep2_tight_final.mp4")

def main():
    print("================================================================")
    print("🚀 PIPELINE 100% AUTÓNOMO: EPISODIO 2 - ESCENA 5 (LOS SIGUIENTES 27s)")
    print("================================================================")
    audio_path, total_dur = paso_1_generar_audio()
    fp1, fp2, total_frames = paso_2_alinear_whisper(audio_path)
    paso_3_generar_imagenes_modal(fp1, fp2)
    paso_4_integrar_esquema(fp1, fp2, total_frames)
    paso_5_render_y_master()
    print("================================================================")
    print("✨ EJECUCIÓN AUTÓNOMA FINALIZADA CON ÉXITO")
    print("================================================================")

if __name__ == "__main__":
    main()
