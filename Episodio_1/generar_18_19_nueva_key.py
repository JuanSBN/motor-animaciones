import os
import sys
import json
import time
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

public_audio = os.path.join("remotion_app", "public", "assets", "audio")
os.makedirs(public_audio, exist_ok=True)
os.makedirs("assets/audio", exist_ok=True)

print("🎙️ Generando Escenas 18 y 19 con la nueva API Key (Puck)...", flush=True)

for id_e in [18, 19]:
    escena = next(e for e in data["escenas"] if e["id"] == id_e)
    texto = escena["locucion"]
    clean_path = f"assets/audio/voz_puck_ep1_escena_{id_e}.wav"
    raw_path = f"assets/audio/puck_temp_{id_e}.pcm"
    
    print(f"\n[{id_e}/19] Solicitando audio para Escena {id_e} con gemini-3.1-flash-tts-preview...", flush=True)
    resp = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
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
    with open(raw_path, "wb") as f:
        f.write(raw_bytes)
        
    # Convertir PCM 24kHz crudo a WAV 48kHz broadcast estéreo limpio con filtro
    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw_path,
        "-ar", "48000", "-ac", "2",
        "-af", "lowpass=f=9500",
        clean_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(raw_path):
        os.remove(raw_path)
        
    dst = os.path.join(public_audio, os.path.basename(clean_path))
    shutil.copy2(clean_path, dst)
    print(f"✅ Escena {id_e} generada y sincronizada!", flush=True)
    time.sleep(2)

# Medir todas las duraciones y actualizar esquema_maestro.json
print("\n📊 Recalculando frames y duraciones para las 19 escenas...", flush=True)
total_segundos = 0
total_frames = 0

for escena in data["escenas"]:
    id_e = escena["id"]
    clean_path = f"assets/audio/voz_puck_ep1_escena_{id_e}.wav"
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", clean_path],
        capture_output=True, text=True
    )
    dur = float(probe.stdout.strip())
    frames = int(round(dur * 30))
    
    escena["archivos_generados"] = {"audio_tts": clean_path}
    escena["duracion_segundos"] = round(dur, 2)
    escena["duracion_frames"] = frames
    
    num_planos = len(escena["planos"])
    for plano in escena["planos"]:
        prop = plano.get("duracion_proporcion", 1.0 / num_planos)
        plano["duracion_frames"] = int(round(frames * prop))
        plano["imagen"] = f"assets/img/ep1_escena_{id_e}_p{plano['id_plano']}.png"
        
    total_segundos += dur
    total_frames += frames
    print(f"Escena {id_e}: {dur:.2f}s ({frames} frames)", flush=True)

data["metadata"]["duracion_total_segundos"] = round(total_segundos, 2)
data["metadata"]["duracion_total_frames"] = total_frames

with open("esquema_maestro.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n🎉 ¡TODAS LAS 19 ESCENAS ESTÁN 100% COMPLETAS CON PUCK! Total: {total_segundos:.2f}s ({total_frames} frames / {total_segundos/60:.2f} minutos)", flush=True)
