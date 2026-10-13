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

# Copiar las escenas 1-4 que ya quedaron 100% perfectas
for i in range(1, 5):
    src = f"assets/audio/voz_puck_ep1_escena_{i}.wav"
    dst = os.path.join(public_audio, f"voz_puck_ep1_escena_{i}.wav")
    shutil.copy2(src, dst)
print("✅ Acto 1 (Escenas 1 a 4) verificado y sincronizado!")

# Agrupaciones de los Actos 2 a 5
actos = [
    {
        "id_acto": 2,
        "escenas": [5, 6, 7, 8],
    },
    {
        "id_acto": 3,
        "escenas": [9, 10, 11],
    },
    {
        "id_acto": 4,
        "escenas": [12, 13, 14],
    },
    {
        "id_acto": 5,
        "escenas": [15, 16, 17, 18, 19],
    }
]

def obtener_silencios(wav_path):
    cmd = ["ffmpeg", "-i", wav_path, "-af", "silencedetect=noise=-28dB:d=0.35", "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    lines = res.stderr.splitlines()
    silencios = []
    for line in lines:
        if "silence_end" in line:
            # Ejemplo: [Parsed_silencedetect_0 @ ...] silence_end: 11.229875 | silence_duration: 0.836479
            parts = line.split("silence_end:")
            if len(parts) > 1:
                end_str = parts[1].split("|")[0].strip()
                dur_str = line.split("silence_duration:")[1].strip()
                t_end = float(end_str)
                t_dur = float(dur_str)
                t_mid = t_end - (t_dur / 2.0)
                silencios.append((t_mid, t_dur))
    return silencios

for acto in actos:
    id_acto = acto["id_acto"]
    escenas_ids = acto["escenas"]
    print(f"\n🎙️ Procesando Acto {id_acto} (Escenas {escenas_ids})...", flush=True)
    
    textos = []
    for id_e in escenas_ids:
        escena = next(e for e in data["escenas"] if e["id"] == id_e)
        textos.append(escena["locucion"])
        
    # Unir con saltos de párrafo para que el modelo haga pausas naturales de ~1 segundo entre escenas
    texto_continuo = "\n\n".join(textos)
    
    pcm_path = f"assets/audio/temp_acto_{id_acto}.pcm"
    wav_acto = f"assets/audio/acto_{id_acto}_continuo.wav"
    
    resp = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=texto_continuo,
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
    with open(pcm_path, "wb") as f:
        f.write(raw_bytes)
        
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", pcm_path,
        "-ar", "48000", "-ac", "2",
        "-af", "lowpass=f=9500",
        wav_acto
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(pcm_path):
        os.remove(pcm_path)
        
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", wav_acto], capture_output=True, text=True)
    dur_total = float(probe.stdout.strip())
    print(f" -> Audio continuo de Acto {id_acto} generado: {dur_total:.2f}s", flush=True)
    
    # Encontrar pausas de separación
    silencios = obtener_silencios(wav_acto)
    # Filtrar solo silencios significativos (> 0.45s) y ordenar por duración descendente para encontrar las N-1 pausas entre escenas
    num_pausas_necesarias = len(escenas_ids) - 1
    # Excluir silencios muy al inicio (< 2s) o muy al final (> dur_total - 2s)
    silencios_validos = [s for s in silencios if 2.0 < s[0] < (dur_total - 1.5)]
    # Ordenar por duración de silencio
    silencios_validos.sort(key=lambda s: s[1], reverse=True)
    
    # Tomar los N-1 cortes con pausas más largas
    cortes = sorted([s[0] for s in silencios_validos[:num_pausas_necesarias]])
    
    puntos = [0.0] + cortes + [dur_total]
    print(f" -> Puntos de corte para Acto {id_acto}: {puntos}", flush=True)
    
    for idx, id_e in enumerate(escenas_ids):
        t_inicio = puntos[idx]
        t_fin = puntos[idx+1]
        out_escena = f"assets/audio/voz_puck_ep1_escena_{id_e}.wav"
        
        cmd_cut = [
            "ffmpeg", "-y",
            "-i", wav_acto,
            "-ss", str(t_inicio), "-to", str(t_fin),
            "-c", "copy",
            out_escena
        ]
        subprocess.run(cmd_cut, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        dst = os.path.join(public_audio, os.path.basename(out_escena))
        shutil.copy2(out_escena, dst)
        print(f"    ✅ Escena {id_e} lista ({t_fin - t_inicio:.2f}s)!", flush=True)
        
    time.sleep(2)

# Actualizar duraciones de todas las 19 escenas en esquema_maestro.json
print("\n📊 Recalculando frames y duraciones para esquema_maestro.json...", flush=True)
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

print(f"\n🎉 ¡TODAS LAS 19 ESCENAS HAN SIDO UNIFICADAS CON LA MISMA VOZ PUCK! Total: {total_segundos:.2f}s ({total_frames} frames / {total_segundos/60:.2f} min)", flush=True)
