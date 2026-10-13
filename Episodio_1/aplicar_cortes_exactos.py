import os
import sys
import json
import subprocess
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

public_audio = os.path.join("remotion_app", "public", "assets", "audio")

# Cortes verificados con escucha humana exacta
cortes_exactos = [
    # Acto 2
    ("assets/audio/acto_2_continuo.wav", 0.0, 10.3, "assets/audio/voz_puck_ep1_escena_5.wav"),
    ("assets/audio/acto_2_continuo.wav", 10.3, 20.9, "assets/audio/voz_puck_ep1_escena_6.wav"),
    ("assets/audio/acto_2_continuo.wav", 20.9, 32.4, "assets/audio/voz_puck_ep1_escena_7.wav"),
    ("assets/audio/acto_2_continuo.wav", 32.4, 43.76, "assets/audio/voz_puck_ep1_escena_8.wav"),
    # Acto 4
    ("assets/audio/acto_4_continuo.wav", 0.0, 11.2, "assets/audio/voz_puck_ep1_escena_12.wav"),
    ("assets/audio/acto_4_continuo.wav", 11.2, 21.8, "assets/audio/voz_puck_ep1_escena_13.wav"),
    ("assets/audio/acto_4_continuo.wav", 21.8, 32.12, "assets/audio/voz_puck_ep1_escena_14.wav"),
]

for src_wav, t_start, t_end, out_wav in cortes_exactos:
    cmd = [
        "ffmpeg", "-y",
        "-i", src_wav,
        "-ss", str(t_start), "-to", str(t_end),
        "-c", "copy",
        out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    dst = os.path.join(public_audio, os.path.basename(out_wav))
    shutil.copy2(out_wav, dst)
    print(f"✅ Sincronizado {os.path.basename(out_wav)} ({t_end - t_start:.2f}s)")

with open("esquema_maestro.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("\n📊 Recalculando frames exactos para las 19 escenas...")
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
    print(f"Escena {id_e}: {dur:.2f}s ({frames} frames)")

data["metadata"]["duracion_total_segundos"] = round(total_segundos, 2)
data["metadata"]["duracion_total_frames"] = total_frames

with open("esquema_maestro.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n🎉 ¡TODAS LAS 19 ESCENAS TIENEN DURACIONES Y CORTES PERFECTOS! Total: {total_segundos:.2f}s ({total_frames} frames / {total_segundos/60:.2f} min)")
