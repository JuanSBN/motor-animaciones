import sys
import os
import subprocess
import wave

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

texto_escena_1 = (
    "Seguro te ha pasado alguna vez. Estás acostado, mirando el techo a oscuras. "
    "Escuchas el reloj o el silencio de la casa y te dices a ti mismo: "
    "Esta noche voy a prestar atención. Voy a descubrir el segundo exacto en que me duermo. "
    "Cierras los ojos, sientes la almohada, respiras hondo... "
    "y de repente suena la alarma. Ya es de día. "
    "Entre las once y media de la noche y las siete de la mañana hay un vacío absoluto. "
    "No viste venir el sueño, no sentiste el cambio y no recuerdas nada. "
    "No es que te hayas distraído: tu cerebro tiene una orden biológica estricta de borrar ese momento cada noche. ¿Por qué?"
)

print("Generando con gemini-3.1-flash-tts-preview (Puck)...")
resp = client.models.generate_content(
    model="gemini-3.1-flash-tts-preview",
    contents=texto_escena_1,
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
raw_pcm = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\audio\temp_31_puck.pcm"
out_wav = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\audio\voz_puck_ep2_escena_1.wav"

with open(raw_pcm, "wb") as f:
    f.write(raw_bytes)

cmd = [
    "ffmpeg", "-y",
    "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw_pcm,
    "-ar", "48000", "-ac", "2",
    "-af", "lowpass=f=9500",
    out_wav
]
subprocess.run(cmd, check=True)
if os.path.exists(raw_pcm):
    os.remove(raw_pcm)

with wave.open(out_wav, "rb") as wf:
    dur = wf.getnframes() / float(wf.getframerate())
print(f"AUDIO GENERADO EXITOSAMENTE: {out_wav}")
print(f"Duracion: {dur:.3f} segundos ({int(round(dur * 30))} frames)")
