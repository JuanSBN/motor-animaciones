import os
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

for m in ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"]:
    print(f"\nProbando {m} con voz Puck...", flush=True)
    try:
        resp = client.models.generate_content(
            model=m,
            contents="Prueba rápida de locución.",
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
        mime = resp.candidates[0].content.parts[0].inline_data.mime_type
        print(f"🎉 {m}: DISPONIBLE! ({len(data)} bytes, mime: {mime})", flush=True)
    except Exception as e:
        print(f"❌ {m}: Error: {e}", flush=True)
