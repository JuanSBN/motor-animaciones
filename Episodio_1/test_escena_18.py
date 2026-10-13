import os
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

texto_18 = "Así que la próxima vez que veas la increíble variedad de tonos de piel en el mundo, recuerda: no hay razas biológicas, solo hay geografía, supervivencia y el diseño más elegante de la evolución."

print("Iniciando llamada para Escena 18 con gemini-3.1-flash-tts-preview...", flush=True)

try:
    resp = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=texto_18,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
                )
            )
        )
    )
    data = resp.candidates[0].content.parts[0].inline_data.data
    print(f"ÉXITO: Se recibieron {len(data)} bytes para Escena 18!", flush=True)
    with open("assets/audio/puck_temp_18.pcm", "wb") as f:
        f.write(data)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}", flush=True)
