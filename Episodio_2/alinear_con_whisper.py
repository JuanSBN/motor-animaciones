import sys
import os
import json
import whisper

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

audio_path = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\audio\voz_puck_ep2_escena_1.wav"

print(f"Cargando modelo Whisper (base) para alinear audio...")
model = whisper.load_model("base")

print(f"Transcribiendo con timestamps de palabras...")
result = model.transcribe(audio_path, language="es", word_timestamps=True)

print("\n--- SEGMENTOS DETECTADOS POR WHISPER ---")
for seg in result["segments"]:
    start = seg["start"]
    end = seg["end"]
    text = seg["text"].strip()
    print(f"[{start:05.2f}s -> {end:05.2f}s] ({int(round(start*30))}f -> {int(round(end*30))}f): {text}")

out_json = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\whisper_alignment_escena_1.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n✅ Alineacion guardada en: {out_json}")
