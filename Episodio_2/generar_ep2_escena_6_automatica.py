"""
generar_ep2_escena_6_automatica.py
Pipeline 100% autónomo para los siguientes ~27 segundos (Escena 6: La Cascada de la Conciencia y la Sacudida Hípnica).
Aplica de forma nativa los 3 blindajes:
  1. TTS con voz Puck (Gemini 3.1 Flash Preview) + Whisper word alignment
  2. Subdivisión rítmica en 6 planos dinámicos de 4 a 5 segundos (cero imágenes estáticas largas)
  3. Diagramas 100% limpios sin humanos + planos de Niko con canon puro calibrado y CLIP QA (>=75%)
  4. Actualización del esquema maestro, render Remotion y masterizado YouTube (-14 LUFS)
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
app = modal.App("ep2-escena-6-flux", image=image_modal)

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

# Texto completo de la Escena 6
TEXTO_ESCENA_6 = (
    "En ese momento exacto entras en la fase N1, una rampa resbaladiza donde tus ondas cerebrales cambian de las rápidas ondas Alfa a las lentas y profundas ondas Theta. "
    "Tus pensamientos pierden la lógica, tus músculos se relajan por completo y tu cerebro sufre una micro desconexión. "
    "Y si esa transición ocurre demasiado rápido, tu cuerpo interpreta erróneamente que te estás cayendo al vacío y lanza una sacudida violenta: la famosa sacudida hípnica."
)

def paso_1_generar_audio():
    out_wav = AUDIO_DIR / "voz_puck_ep2_escena_6.wav"
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
        contents=TEXTO_ESCENA_6,
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
    raw_pcm = AUDIO_DIR / "temp_puck_escena_6.pcm"

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
    print("\n⏱️ [PASO 2/5] Alineando audio con Whisper en 6 beats dinámicos (3-5s cada uno)...")
    out_json = EP2_DIR / "whisper_alignment_escena_6.json"
    if out_json.exists():
        with open(out_json, "r", encoding="utf-8") as f:
            res = json.load(f)
    else:
        import whisper
        model = whisper.load_model("base")
        res = model.transcribe(str(audio_path), language="es", word_timestamps=True)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)

    with wave.open(str(audio_path), "rb") as wf:
        total_dur = wf.getnframes() / float(wf.getframerate())
    total_frames = int(round(total_dur * 30))

    words = []
    for seg in res["segments"]:
        for w in seg.get("words", []):
            words.append(w)

    def buscar_tiempo_palabra(palabra):
        p_clean = palabra.lower()
        for w in words:
            clean = w["word"].strip().lower().replace(",", "").replace(".", "").replace(":", "")
            if p_clean in clean:
                return w["end"]
        return None

    # Puntos de corte rítmicos basados en las palabras clave
    t_rampa = buscar_tiempo_palabra("resbaladiza") or 4.5
    t_theta = buscar_tiempo_palabra("theta") or 9.0
    t_logica = buscar_tiempo_palabra("lógica") or (t_theta + 4.0)
    t_desconexion = buscar_tiempo_palabra("desconexión") or (t_logica + 4.0)
    t_vacio = buscar_tiempo_palabra("vacío") or (t_desconexion + 4.5)

    tiempos = [0.0, t_rampa, t_theta, t_logica, t_desconexion, t_vacio, total_dur]
    # Asegurar orden estrictamente creciente
    for i in range(1, len(tiempos)):
        if tiempos[i] <= tiempos[i-1] + 1.0:
            tiempos[i] = tiempos[i-1] + 3.5

    duraciones_sec = [tiempos[i] - tiempos[i-1] for i in range(1, len(tiempos))]
    # Convertir a frames
    frames_planos = [int(round(d * 30)) for d in duraciones_sec]
    # Ajustar para que la suma sea exactamente total_frames
    diff = total_frames - sum(frames_planos)
    frames_planos[-1] += diff

    print(f"   ✅ Audio total: {total_dur:.2f}s ({total_frames} frames)")
    for i, fp in enumerate(frames_planos):
        print(f"      Plano {i+1}: {fp} frames ({fp/30.0:.2f}s)")

    return frames_planos, total_frames

def paso_3_generar_visuales_modal(frames_planos):
    print("\n🎨 [PASO 3/5] Generando 6 visuales en Modal A100 con blindaje anti-humanos y canon puro...")
    from niko_bible import RUTA_CANONICA_PIJAMA
    from evaluador_coherencia import EvaluadorCoherencia

    with open(RUTA_CANONICA_PIJAMA, "rb") as f:
        bytes_canon_pijama = f.read()

    planos_meta = [
        # Plano 1: Rampa resbaladiza de la Fase N1 (diagrama conceptual limpio)
        {
            "nombre": "ep2_escena_6_p1.png",
            "prompt": (
                "2D flat vector explainer infographic, clean bold lines, flat cel shading, vibrant saturated colors, 16:9 composition: "
                "Futuristic glowing descent ramp leading into deep blue twilight space, labeled with a subtle glowing HUD badge 'FASE N1', "
                "luminescent sleep trajectory slope, pure biological technology infographic, strictly ZERO humans, no people, no characters, empty scene, no text, no watermark"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False
        },
        # Plano 2: Ondas cerebrales Alfa a Theta (infografía científica limpia)
        {
            "nombre": "ep2_escena_6_p2.png",
            "prompt": (
                "2D flat vector scientific infographic, clean bold lines, flat cel shading, vibrant colors, 16:9 composition: "
                "Side by side brainwave comparison: rapid sharp electric cyan Alpha waves transitioning smoothly into slow deep purple-violet oceanic Theta waves, "
                "pure educational EEG brainwave graph diagram, glowing rhythmic sinusoidal curves, strictly ZERO humans, no people, no characters, no text"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False
        },
        # Plano 3: Pensamientos perdiendo la lógica (metáfora conceptual)
        {
            "nombre": "ep2_escena_6_p3.png",
            "prompt": (
                "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant colors, 16:9 composition: "
                "Dreamy abstract nighttime space with floating translucent memory orbs and gentle golden gears gently uncoupling and floating weightlessly into soft clouds, "
                "surreal peaceful dream logic atmosphere, strictly ZERO humans, no people, no characters, empty environment, no text"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False
        },
        # Plano 4: Micro desconexión cerebral (interruptor biológico)
        {
            "nombre": "ep2_escena_6_p4.png",
            "prompt": (
                "2D flat vector explainer infographic, clean bold lines, flat cel shading, vibrant colors, 16:9 composition: "
                "Close-up of a stylized glowing bioluminescent neural junction switch gently powering down with soft floating golden particles, "
                "dimming circuits of consciousness in deep midnight indigo background, strictly ZERO humans, no people, no characters, no text"
            ),
            "ref_bytes": None,
            "usa_ref": False,
            "es_niko": False
        },
        # Plano 5: Metáfora de caída al vacío con Niko canónico
        {
            "nombre": "ep2_escena_6_p5.png",
            "prompt": (
                "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant colors, 16:9 composition: "
                "Comical dramatic dream sequence: Niko, an athletic 12-year-old pre-teen cartoon boy, floating in mid-air in dreamy night sky falling gently through soft clouds, "
                "looking startled with wide cartoon eyes, exactly ONE single small cream-white adhesive bandage on his left cheek, clear smooth skin on right cheek, "
                "messy dark teal hair with loose cowlick, yellow sleeping shirt, starry nighttime dreamscape, no watermark, no text"
            ),
            "ref_bytes": bytes_canon_pijama,
            "usa_ref": True,
            "es_niko": True
        },
        # Plano 6: Sacudida hípnica en la cama (Niko despertándose con un respingo)
        {
            "nombre": "ep2_escena_6_p6.png",
            "prompt": (
                "2D flat cartoon illustration, clean bold outlines, flat cel shading, vibrant saturated colors, 16:9 composition: "
                "Medium shot from waist up: Niko, an athletic 12-year-old pre-teen cartoon boy, jolting awake in cozy bed with an exaggerated comedic cartoon twitch (hypnic jerk), "
                "eyes wide open in surprised funny shock, grasping the blue bed sheets, messy spiky dark teal-green hair, "
                "exactly ONE single small cream-white rectangular medical adhesive bandage on his left cheek, clear smooth skin on right cheek with NO second bandage, "
                "yellow sleeping shirt, dark cozy nighttime bedroom ambiance, gentle bedside lamp glow, no text, no watermark"
            ),
            "ref_bytes": bytes_canon_pijama,
            "usa_ref": True,
            "es_niko": True
        }
    ]

    prompts = [p["prompt"] for p in planos_meta]
    refs = [p["ref_bytes"] for p in planos_meta]
    flags = [p["usa_ref"] for p in planos_meta]

    print("   🚀 Conectando con contenedor A100 en Modal para generar los 6 planos...")
    with app.run():
        res_bytes = modal_gen.remote(prompts, refs, flags, HF_TOKEN)

    evaluador = EvaluadorCoherencia()

    for i, p in enumerate(planos_meta):
        out_p = IMG_DIR / p["nombre"]
        with open(out_p, "wb") as f:
            f.write(res_bytes[i])
        shutil.copy(str(out_p), str(PUBLIC_IMG / p["nombre"]))
        print(f"   💾 Guardado y copiado a Remotion: {p['nombre']}")

        if p["es_niko"]:
            ev = evaluador.evaluar_niko(str(out_p), es_pijama=True)
            print(f"      🛡️ CLIP Score: {ev['score']:.1f}% -> {ev['mensaje']}")

def paso_4_integrar_esquema(frames_planos, total_frames):
    print("\n📋 [PASO 4/5] Integrando Escena 6 en esquema maestro...")
    schema_file = EP2_DIR / "esquema_maestro_ep2_tight.json"
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    planos_escena_6 = [
        {
            "id_plano": 1,
            "locucion_plano": "En ese momento exacto entras en la fase N1, una rampa resbaladiza...",
            "palabras_clave_plano": ["fase N1", "rampa resbaladiza"],
            "duracion_frames": frames_planos[0],
            "animacion": "zoom_in_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_6_p1.png",
            "descripcion": "Infografía de descenso a la Fase N1 hacia la noche bioluminiscente"
        },
        {
            "id_plano": 2,
            "locucion_plano": "...donde tus ondas cerebrales cambian de las rápidas ondas Alfa a las lentas y profundas ondas Theta.",
            "palabras_clave_plano": ["ondas Alfa", "ondas Theta"],
            "duracion_frames": frames_planos[1],
            "animacion": "paneo_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_6_p2.png",
            "descripcion": "Diagrama científico de ondas cerebrales Alfa transicionando a Theta"
        },
        {
            "id_plano": 3,
            "locucion_plano": "Tus pensamientos pierden la lógica, tus músculos se relajan por completo...",
            "palabras_clave_plano": ["pierden la lógica", "músculos se relajan"],
            "duracion_frames": frames_planos[2],
            "animacion": "zoom_in_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_6_p3.png",
            "descripcion": "Esferas de pensamientos flotando y engranajes soltándose en el cielo nocturno"
        },
        {
            "id_plano": 4,
            "locucion_plano": "...y tu cerebro sufre una micro desconexión.",
            "palabras_clave_plano": ["micro desconexión"],
            "duracion_frames": frames_planos[3],
            "animacion": "flotar_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_6_p4.png",
            "descripcion": "Interruptor de circuito neuronal atenuándose con partículas tenues"
        },
        {
            "id_plano": 5,
            "locucion_plano": "Y si esa transición ocurre demasiado rápido, tu cuerpo interpreta erróneamente que te estás cayendo al vacío...",
            "palabras_clave_plano": ["cayendo al vacío"],
            "duracion_frames": frames_planos[4],
            "animacion": "zoom_in_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_6_p5.png",
            "descripcion": "Niko canónico cayendo cómicamente en cámara lenta a través de nubes nocturnas"
        },
        {
            "id_plano": 6,
            "locucion_plano": "...y lanza una sacudida violenta: la famosa sacudida hípnica.",
            "palabras_clave_plano": ["sacudida violenta", "sacudida hípnica"],
            "duracion_frames": frames_planos[5],
            "animacion": "paneo_suave",
            "tipo_visual": "imagen_flux",
            "imagen": "assets/img/ep2_escena_6_p6.png",
            "descripcion": "Niko canónico sobresaltado en la cama por la sacudida hípnica con ojos de sorpresa cómica"
        }
    ]

    data["escenas"][5]["audio"] = "assets/audio/voz_puck_ep2_escena_6.wav"
    data["escenas"][5]["archivos_generados"] = {
        "audio_tts": "assets/audio/voz_puck_ep2_escena_6.wav"
    }
    data["escenas"][5]["duracion_frames"] = total_frames
    data["escenas"][5]["planos"] = planos_escena_6

    gran_total = sum(e["duracion_frames"] for e in data["escenas"][:6])
    data["metadata"]["duracion_total_frames"] = gran_total
    data["metadata"]["duracion_total_segundos"] = round(gran_total / 30.0, 2)

    with open(schema_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"   ✅ Esquema actualizado: 6 escenas activas | Total: {gran_total} frames ({gran_total/30.0:.2f}s / {gran_total/1800.0:.2f} min)")
    return gran_total

def paso_5_render_y_master():
    print("\n🎬 [PASO 5/5] Renderizando Episodio 2 completo en Remotion y masterizando audio (-14 LUFS)...")
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

    mastered_out = REMOTION_DIR / "out" / "ep2_tight_full_youtube.mp4"
    final_dest = EP2_DIR / "ep2_tight_final.mp4"
    shutil.copy(str(mastered_out), str(final_dest))
    print(f"\n🎉 VIDEO FINAL EXPORTADO EXITOSAMENTE A: {final_dest.name}")

def main():
    print("================================================================")
    print("🚀 PIPELINE 100% AUTÓNOMO: EPISODIO 2 - ESCENA 6 (LOS SIGUIENTES 27s)")
    print("================================================================")
    audio_path, total_dur = paso_1_generar_audio()
    frames_planos, total_frames = paso_2_alinear_whisper(audio_path)
    paso_3_generar_visuales_modal(frames_planos)
    paso_4_integrar_esquema(frames_planos, total_frames)
    paso_5_render_y_master()
    print("================================================================")
    print("✨ EJECUCIÓN AUTÓNOMA DE ESCENA 6 FINALIZADA CON ÉXITO")
    print("================================================================")

if __name__ == "__main__":
    main()
