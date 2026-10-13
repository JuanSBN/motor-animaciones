import os
import sys
import json
import subprocess
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

with open("esquema_maestro.json", "r", encoding="utf-8") as f:
    data = json.load(f)

os.makedirs("assets/audio", exist_ok=True)
public_audio = os.path.join("remotion_app", "public", "assets", "audio")
os.makedirs(public_audio, exist_ok=True)

total_segundos = 0
total_frames = 0

print(f"🎙️ Generando locuciones con Gemini TTS (Puck) para las {len(data['escenas'])} escenas...")

for escena in data["escenas"]:
    id_e = escena["id"]
    texto = escena["locucion"]
    raw_path = f"assets/audio/puck_temp_{id_e}.wav"
    clean_path = f"assets/audio/voz_puck_ep1_escena_{id_e}.wav"
    
    import time
    if os.path.exists(clean_path):
        print(f"[{id_e}/19] Escena {id_e} ya existe en disco, reutilizando...")
    else:
        modelo_a_usar = "gemini-3.8-flash-lite-tts"
        print(f"[{id_e}/19] Generando Escena {id_e} con {modelo_a_usar} (Puck)...")
        
        raw_bytes = None
        for intento in range(6):
            try:
                resp = client.models.generate_content(
                    model=modelo_a_usar,
                    contents=texto,
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
                break
            except Exception as e:
                if "429" in str(e):
                    print(f" -> Pausa de ritmo de API (429). Esperando 25s (intento {intento+1}/6)...")
                    time.sleep(25)
                else:
                    raise e
                    
        with open(raw_path, "wb") as f:
            f.write(raw_bytes)
            
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", raw_path],
            capture_output=True, text=True
        )
        dur = float(probe.stdout.strip())
        fade_out_start = max(0, dur - 0.01)
        
        # Filtro limpio a 9500Hz + microfade 10ms + 48kHz estereo (audio cristalino sin estatica)
        cmd = [
            "ffmpeg", "-y", "-i", raw_path,
            "-ar", "48000",
            "-ac", "2",
            "-af", f"lowpass=f=9500,afade=t=in:ss=0:d=0.01,afade=t=out:st={fade_out_start:.3f}:d=0.01",
            clean_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(raw_path):
            os.remove(raw_path)

    # Medir duracion oficial del clean_path
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", clean_path],
        capture_output=True, text=True
    )
    dur = float(probe.stdout.strip())
    
    # Copiar a Remotion public
    dst = os.path.join(public_audio, os.path.basename(clean_path))
    shutil.copy2(clean_path, dst)
    
    frames = int(round(dur * 30))
    escena["archivos_generados"] = escena.get("archivos_generados", {})
    escena["archivos_generados"]["audio_tts"] = clean_path
    escena["duracion_segundos"] = round(dur, 2)
    escena["duracion_frames"] = frames
    
    num_planos = len(escena["planos"])
    for idx_p, plano in enumerate(escena["planos"]):
        prop = plano.get("duracion_proporcion", 1.0 / num_planos)
        plano_frames = int(round(frames * prop))
        plano["duracion_frames"] = plano_frames
        plano["imagen"] = f"assets/img/ep1_escena_{id_e}_p{plano['id_plano']}.png"
        
    total_segundos += dur
    total_frames += frames
    print(f" -> Escena {id_e} lista: {dur:.2f}s ({frames} frames)")

data["metadata"]["duracion_total_segundos"] = round(total_segundos, 2)
data["metadata"]["duracion_total_frames"] = total_frames

with open("esquema_maestro.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n🎉 ¡Todas las 19 locuciones listas con Puck! Duración total: {total_segundos:.2f}s ({total_frames} frames / {total_segundos/60:.2f} min)")
