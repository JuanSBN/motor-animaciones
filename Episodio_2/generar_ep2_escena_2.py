import sys
import os
import subprocess
import wave
import json
import whisper

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

OUT_AUDIO_DIR = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\audio"
os.makedirs(OUT_AUDIO_DIR, exist_ok=True)

texto_escena_2 = (
    "Si te tropiezas por la calle, tu mente recuerda el tropiezo. "
    "Si te quemas con una taza caliente, recuerdas el dolor al instante. "
    "Tu memoria es implacable registrando peligros y errores. "
    "Pero ese puente exacto entre estar despierto y estar inconsciente "
    "es el único recuerdo que la evolución te tiene terminantemente prohibido guardar."
)

print("🎙️ [PILAR 1] Generando voz oficial de Niko con gemini-3.1-flash-tts-preview (Puck)...")
resp = client.models.generate_content(
    model="gemini-3.1-flash-tts-preview",
    contents=texto_escena_2,
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
raw_pcm = os.path.join(OUT_AUDIO_DIR, "temp_escena_2_puck.pcm")
clean_wav = os.path.join(OUT_AUDIO_DIR, "voz_puck_ep2_escena_2.wav")

with open(raw_pcm, "wb") as f:
    f.write(raw_bytes)

# Filtro estandarizado 48kHz, estereo, lowpass 9500Hz
cmd = [
    "ffmpeg", "-y",
    "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw_pcm,
    "-ar", "48000", "-ac", "2",
    "-af", "lowpass=f=9500",
    clean_wav
]
subprocess.run(cmd, check=True)
if os.path.exists(raw_pcm):
    os.remove(raw_pcm)

with wave.open(clean_wav, "rb") as wf:
    dur = wf.getnframes() / float(wf.getframerate())
frames_total = int(round(dur * 30))
print(f"✅ Audio Escena 2 generado: {dur:.2f} segundos ({frames_total} frames)")

# 2. PILAR 2: Whisper Alignment
print("\n🎯 [PILAR 2] Ejecutando alineación forzada con Whisper (word_timestamps)...")
model = whisper.load_model("base")
res_whisper = model.transcribe(clean_wav, language="es", word_timestamps=True)

out_json = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\whisper_alignment_escena_2.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(res_whisper, f, indent=2, ensure_ascii=False)

print("\n--- TIMESTAMPS EXACTOS POR WHISPER (ESCENA 2) ---")
for seg in res_whisper["segments"]:
    start = seg["start"]
    end = seg["end"]
    txt = seg["text"].strip()
    print(f"[{start:05.2f}s -> {end:05.2f}s] ({int(round(start*30))}f -> {int(round(end*30))}f): {txt}")

print(f"\n✅ Guardado alineamiento Whisper en {out_json}")
