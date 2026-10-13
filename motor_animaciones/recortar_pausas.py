"""
recortar_pausas.py

Acorta los silencios largos del TTS usando los timestamps palabra a palabra de Whisper
y recalcula todo el esquema para que imagen, subtítulos y audio sigan sincronizados.

Qué hace por cada escena:
  1. Lee el audio TTS y su alineación Whisper (segments[].words[]).
  2. Deja como máximo MAX_PAUSA segundos entre palabras (0.6-0.9 s -> 0.25 s).
  3. Escribe un WAV nuevo <audio>_tight.wav con micro-fades para que no haya clics.
  4. Guarda escena["palabras"] = [{w, s, e}] en la nueva línea de tiempo (para WordCaptions).
  5. Recalcula duracion_frames de la escena y de cada plano a partir de dónde empieza
     realmente su primera palabra.
  6. Avisa de los planos que siguen durando más de MAX_PLANO_SEG.

Uso:
  python recortar_pausas.py \
      --esquema ../Episodio_2/esquema_maestro_ep2.json \
      --public ../Episodio_1/remotion_app/public \
      --alineaciones ../Episodio_2 \
      --patron "whisper_alignment_escena_{id}.json"

El esquema original no se toca: se escribe <esquema>_tight.json.
"""

import argparse
import json
import math
import re
import subprocess
import tempfile
import unicodedata
import wave
from pathlib import Path

import numpy as np

FPS = 30
MAX_PAUSA = 0.25
MARGEN_INICIO = 0.05
COLA_FINAL = 0.35
FADE_MS = 8
MAX_PLANO_SEG = 4.0


def leer_wav(ruta: Path):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(ruta), "-ac", "1", "-c:a", "pcm_s16le", str(tmp_path)],
        check=True,
    )
    with wave.open(str(tmp_path), "rb") as w:
        sr = w.getframerate()
        datos = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    tmp_path.unlink(missing_ok=True)
    return datos, sr


def escribir_wav(ruta: Path, datos: np.ndarray, sr: int):
    pcm = np.clip(datos, -32768, 32767).astype(np.int16)
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def palabras_whisper(alineacion: dict):
    palabras = []
    for seg in alineacion.get("segments", []):
        for p in seg.get("words", []):
            if p.get("start") is None or p.get("end") is None:
                continue
            palabras.append({"w": p["word"].strip(), "s": float(p["start"]), "e": float(p["end"])})
    return palabras


def calcular_tramos(palabras, duracion_audio):
    """Devuelve los tramos [ini, fin] del audio original que se conservan."""
    if not palabras:
        return [(0.0, duracion_audio)]
    tramos = []
    ini = max(0.0, palabras[0]["s"] - MARGEN_INICIO)
    for actual, siguiente in zip(palabras, palabras[1:]):
        hueco = siguiente["s"] - actual["e"]
        if hueco > MAX_PAUSA:
            medio = MAX_PAUSA / 2
            tramos.append((ini, actual["e"] + medio))
            ini = siguiente["s"] - medio
    tramos.append((ini, min(duracion_audio, palabras[-1]["e"] + COLA_FINAL)))
    return tramos


def remapear(t, tramos):
    """Convierte un tiempo del audio original a la nueva línea de tiempo recortada."""
    acumulado = 0.0
    for ini, fin in tramos:
        if t < ini:
            return acumulado
        if t <= fin:
            return acumulado + (t - ini)
        acumulado += fin - ini
    return acumulado


def recortar_audio(datos, sr, tramos):
    fade = int(sr * FADE_MS / 1000)
    piezas = []
    for ini, fin in tramos:
        trozo = datos[int(ini * sr): int(fin * sr)].copy()
        if len(trozo) > 2 * fade:
            rampa = np.linspace(0, 1, fade)
            trozo[:fade] *= rampa
            trozo[-fade:] *= rampa[::-1]
        piezas.append(trozo)
    return np.concatenate(piezas) if piezas else datos


def normalizar(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn" and c.isalnum())


def limites_planos(planos, palabras):
    """
    Asigna a cada plano el índice de su primera palabra Whisper usando proporción de caracteres.
    Es robusto aunque Whisper escriba "11" donde el guion dice "once".
    """
    largos = [len(normalizar(p.get("locucion_plano", ""))) or 1 for p in planos]
    total_guion = sum(largos)
    acumulado_palabras = np.cumsum([len(normalizar(p["w"])) or 1 for p in palabras])
    total_whisper = acumulado_palabras[-1]

    indices = [0]
    acumulado = 0
    for largo in largos[:-1]:
        acumulado += largo
        objetivo = acumulado / total_guion * total_whisper
        idx = int(np.searchsorted(acumulado_palabras, objetivo, side="left")) + 1
        indices.append(min(max(idx, indices[-1] + 1), len(palabras) - 1))
    return indices


def procesar_escena(escena, public_dir: Path, ruta_alineacion: Path, avisos):
    audio_rel = (escena.get("archivos_generados") or {}).get("audio_tts")
    if not audio_rel:
        avisos.append(f"Escena {escena['id']}: sin audio generado todavía, se omite.")
        return
    audio_path = public_dir / audio_rel
    if not ruta_alineacion.exists():
        avisos.append(f"Escena {escena['id']}: sin alineación ({ruta_alineacion.name}), se omite.")
        return

    datos, sr = leer_wav(audio_path)
    duracion_original = len(datos) / sr
    palabras = palabras_whisper(json.loads(ruta_alineacion.read_text(encoding="utf-8")))
    tramos = calcular_tramos(palabras, duracion_original)
    nuevo = recortar_audio(datos, sr, tramos)
    duracion_nueva = len(nuevo) / sr

    salida_rel = re.sub(r"(\.\w+)$", r"_tight.wav", audio_rel)
    escribir_wav(public_dir / salida_rel, nuevo, sr)

    palabras_nuevas = [
        {"w": p["w"], "s": round(remapear(p["s"], tramos), 3), "e": round(remapear(p["e"], tramos), 3)}
        for p in palabras
    ]

    escena["archivos_generados"]["audio_tts"] = salida_rel
    escena["palabras"] = palabras_nuevas
    escena["duracion_segundos"] = round(duracion_nueva, 2)
    escena["duracion_frames"] = int(math.ceil(duracion_nueva * FPS))

    planos = escena.get("planos") or []
    if planos and palabras_nuevas:
        indices = limites_planos(planos, palabras_nuevas)
        inicios = [0] + [int(round(palabras_nuevas[i]["s"] * FPS)) for i in indices[1:]]
        inicios.append(escena["duracion_frames"])
        for i, plano in enumerate(planos):
            plano["duracion_frames"] = max(15, inicios[i + 1] - inicios[i])
            seg = plano["duracion_frames"] / FPS
            if seg > MAX_PLANO_SEG and not plano.get("componente"):
                avisos.append(
                    f"Escena {escena['id']} plano {plano['id_plano']}: {seg:.1f}s con una sola imagen. "
                    f"Scene.tsx lo reencuadra, pero mejor generar una imagen extra ({plano.get('descripcion', '')})."
                )

    ahorro = duracion_original - duracion_nueva
    print(f"Escena {escena['id']}: {duracion_original:.2f}s -> {duracion_nueva:.2f}s (-{ahorro:.2f}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--esquema", required=True, type=Path)
    ap.add_argument("--public", required=True, type=Path, help="Carpeta public/ de remotion_app")
    ap.add_argument("--alineaciones", required=True, type=Path)
    ap.add_argument("--patron", default="whisper_alignment_escena_{id}.json")
    args = ap.parse_args()

    esquema = json.loads(args.esquema.read_text(encoding="utf-8"))
    avisos = []
    for escena in esquema["escenas"]:
        procesar_escena(escena, args.public, args.alineaciones / args.patron.format(id=escena["id"]), avisos)

    total = sum(e.get("duracion_frames", 0) for e in esquema["escenas"])
    esquema["metadata"]["duracion_total_frames"] = total
    esquema["metadata"]["duracion_total_segundos"] = round(total / FPS, 2)

    salida = args.esquema.with_name(args.esquema.stem + "_tight.json")
    salida.write_text(json.dumps(esquema, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nEsquema escrito en {salida} ({total / FPS:.1f}s totales)")
    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print(" -", a)


if __name__ == "__main__":
    main()
