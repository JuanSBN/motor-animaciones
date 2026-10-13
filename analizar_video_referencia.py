"""
analizar_video_referencia.py
Extrae fotogramas clave y analiza el ritmo, cortes y estilo visual
del video de referencia 'Curiosamente Graficado'.
"""

import os
import sys
import subprocess
import json

VIDEO_PATH = r"C:\Users\Lenovo\Downloads\¿Por Qué Realmente No Podemos Explorar las Profundidades de la Amazonía - Curiosamente Graficado (720p, h264).mp4"
OUT_DIR = r"c:\Users\Lenovo\Documents\Animaciones\analisis_amazonia"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Extraer fotogramas en momentos narrativos clave
tiempos = [
    ("00:00:08", "01_intro_hook"),
    ("00:00:25", "02_personaje_pregunta"),
    ("00:01:10", "03_mapa_escala"),
    ("00:02:30", "04_peligro_fauna"),
    ("00:04:15", "05_infografia_datos"),
    ("00:06:50", "06_obstaculo_rio"),
    ("00:10:20", "07_tribus_aisladas"),
    ("00:14:00", "08_tecnologia_drones"),
    ("00:17:10", "09_conclusion_cierre")
]

for t, nombre in tiempos:
    out_file = os.path.join(OUT_DIR, f"{nombre}.png")
    cmd = [
        "ffmpeg", "-ss", t, "-i", VIDEO_PATH,
        "-vframes", "1", "-q:v", "2", "-y", out_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Extracted: {nombre}")

# 2. Analizar cortes de escena en los primeros 120 segundos para medir Pacing (segundos por plano)
cmd_scenes = [
    "ffprobe", "-show_entries", "frame=pkt_pts_time",
    "-select_streams", "v",
    "-filter:v", "select='gt(scene,0.25)',showinfo",
    "-read_intervals", "%+120",
    "-of", "csv=p=0",
    VIDEO_PATH
]
res = subprocess.run(cmd_scenes, capture_output=True, text=True)
cuts = [float(x.strip()) for x in res.stdout.strip().split('\n') if x.strip() and x.strip().replace('.','',1).isdigit()]

print(f"\n--- ANÁLISIS DE PACING (Primeros 2 minutos) ---")
print(f"Total de cortes detectados en 120s: {len(cuts)}")
if len(cuts) > 1:
    duraciones = [cuts[i] - cuts[i-1] for i in range(1, len(cuts))]
    avg_dur = sum(duraciones) / len(duraciones)
    print(f"Duración promedio por plano: {avg_dur:.2f} segundos")
    print(f"Plano más corto: {min(duraciones):.2f}s | Plano más largo: {max(duraciones):.2f}s")
