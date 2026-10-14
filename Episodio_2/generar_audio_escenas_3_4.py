import sys
import os
import subprocess
import wave
import json
import whisper
from google import genai
from google.genai import types

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
api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

OUT_AUDIO_DIR = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\audio"
os.makedirs(OUT_AUDIO_DIR, exist_ok=True)

ESCENAS = [
    {
        "id": 3,
        "texto": (
            "Para entender este misterio, primero tenemos que mirar cómo funciona tu grabadora interna: "
            "una estructura cerebral con forma de caballito de mar llamada Hipocampo. "
            "Durante todo el día, el hipocampo recibe todo lo que ves, hueles y sientes, "
            "y lo va archivando en la memoria a corto plazo como una cámara de seguridad encendida las veinticuatro horas."
        )
    },
    {
        "id": 4,
        "texto": (
            "Pero cuando te metes a la cama, los científicos descubrieron un fenómeno asombroso: "
            "el hipocampo no se duerme al mismo tiempo que el resto del cuerpo. "
            "Se apaga de cuatro a diez minutos ANTES de que pierdas el conocimiento. "
            "Imagina que una cámara de seguridad deja de grabar mientras las luces de la habitación todavía siguen encendidas. "
            "Durante esos minutos finales, estás despierto, pero nadie está guardando el archivo."
        )
    }
]

print("🧠 Cargando modelo de Whisper para alineación forzada...")
whisper_model = whisper.load_model("base")

for esc in ESCENAS:
    eid = esc["id"]
    texto = esc["texto"]
    print(f"\n🎙️ Generando TTS con Gemini (Puck) para Escena {eid}...")
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
    raw_pcm = os.path.join(OUT_AUDIO_DIR, f"temp_escena_{eid}_puck.pcm")
    clean_wav = os.path.join(OUT_AUDIO_DIR, f"voz_puck_ep2_escena_{eid}.wav")

    with open(raw_pcm, "wb") as f:
        f.write(raw_bytes)

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
    print(f"✅ Audio Escena {eid} generado: {dur:.2f}s ({int(round(dur*30))} frames)")

    print(f"🎯 Alineando timestamps con Whisper para Escena {eid}...")
    res_whisper = whisper_model.transcribe(clean_wav, language="es", word_timestamps=True)
    out_json = os.path.join(r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2", f"whisper_alignment_escena_{eid}.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(res_whisper, f, indent=2, ensure_ascii=False)
    print(f"✅ Guardado alineamiento Whisper: {out_json}")

print("\n🎉 ¡Audios y alineaciones de Escenas 3 y 4 completados!")
