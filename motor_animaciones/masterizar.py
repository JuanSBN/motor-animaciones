"""
masterizar.py

Último paso después de `remotion render`:
  - Normaliza el audio a -14 LUFS (lo que usa YouTube) con loudnorm en dos pasadas.
  - Exporta en 1080p H.264 de alta calidad para subir a YouTube.
  - Opcionalmente genera una versión ligera (--ligera) para compartir o revisar.

Uso:
  python masterizar.py out/episodio_2.mp4
  python masterizar.py out/episodio_2.mp4 --ligera
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

OBJETIVO_LUFS = -14.0
TRUE_PEAK = -1.5
LRA = 11.0


def medir_loudness(entrada: Path) -> dict:
    filtro = f"loudnorm=I={OBJETIVO_LUFS}:TP={TRUE_PEAK}:LRA={LRA}:print_format=json"
    res = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(entrada), "-af", filtro, "-vn", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    bloque = re.findall(r"\{[^{}]+\}", res.stderr)
    if not bloque:
        raise RuntimeError("No se pudo medir el loudness:\n" + res.stderr[-800:])
    return json.loads(bloque[-1])


def masterizar(entrada: Path, salida: Path, ligera: bool):
    m = medir_loudness(entrada)
    print(f"Loudness original: {m['input_i']} LUFS, pico {m['input_tp']} dBTP")

    filtro_audio = (
        f"loudnorm=I={OBJETIVO_LUFS}:TP={TRUE_PEAK}:LRA={LRA}"
        f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
        f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
        f":offset={m['target_offset']}:linear=true,aresample=48000"
    )

    if ligera:
        video = ["-vf", "scale=-2:720", "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-maxrate", "1500k", "-bufsize", "3000k"]
        audio = ["-c:a", "aac", "-b:a", "128k"]
    else:
        video = ["-vf", "scale=1920:1080:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p"]
        audio = ["-c:a", "aac", "-b:a", "320k"]

    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(entrada), *video, "-af", filtro_audio, *audio,
         "-movflags", "+faststart", str(salida)],
        check=True,
    )
    final = medir_loudness(salida)
    print(f"Listo: {salida} -> {final['input_i']} LUFS, pico {final['input_tp']} dBTP")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", type=Path)
    ap.add_argument("--ligera", action="store_true")
    args = ap.parse_args()
    sufijo = "_ligera" if args.ligera else "_youtube"
    masterizar(args.entrada, args.entrada.with_name(args.entrada.stem + sufijo + ".mp4"), args.ligera)


if __name__ == "__main__":
    main()
