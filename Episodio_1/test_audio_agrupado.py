import os
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

texto_acto1 = (
    "Imagina que estamos hace millones de años, bajo un sol abrasador en la sabana africana. Nuestros primeros ancestros enfrentaban un calor implacable.\n\n"
    "Para sobrevivir y no sobrecalentarse mientras corrían, los humanos perdieron el pelaje corporal y desarrollaron millones de glándulas sudoríparas.\n\n"
    "Pero sin pelo, la piel quedó totalmente expuesta a un enemigo invisible y destructor: la radiación ultravioleta del sol.\n\n"
    "Aquí entró nuestro escudo biológico definitivo: la Melanina. Una molécula oscura producida por melanocitos que cubre el ADN como una sombrilla."
)

print("🎙️ Probando generación agrupada de Acto 1 (4 escenas en 1 sola llamada)...", flush=True)

try:
    resp = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=texto_acto1,
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
    print(f"🎉 ÉXITO TOTAL: Recibidos {len(raw_bytes)} bytes de audio continuo!", flush=True)
    with open("assets/audio/test_acto1_agrupado.pcm", "wb") as f:
        f.write(raw_bytes)
        
    import subprocess
    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "assets/audio/test_acto1_agrupado.pcm",
        "-ar", "48000", "-ac", "2",
        "-af", "lowpass=f=9500",
        "assets/audio/test_acto1_agrupado.wav"
    ]
    subprocess.run(cmd, check=True)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "assets/audio/test_acto1_agrupado.wav"], capture_output=True, text=True)
    dur = float(probe.stdout.strip())
    print(f"Duración total del Acto 1 continuo: {dur:.2f} segundos!")
except Exception as e:
    print("Error:", e, flush=True)
