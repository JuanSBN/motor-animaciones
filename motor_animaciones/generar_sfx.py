import os
import sys
import numpy as np
import wave

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SR = 48000

def guardar_wav(ruta, audio):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    # Normalizar a -3 dB
    audio = audio / (np.max(np.abs(audio)) + 1e-9) * 0.7
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"✅ Generado: {ruta} ({len(pcm)/SR:.2f}s)")

def sintetizar_whoosh():
    # Duración ~0.45s
    dur = 0.45
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    # Ruido blanco base
    np.random.seed(42)
    ruido = np.random.uniform(-1, 1, len(t))
    # Modulación de frecuencia y filtro tipo barrido
    # Envolvente suave estilo campana
    env = np.sin(np.pi * (t / dur)) ** 3
    # Barrido tonal sutil
    freq_sweep = 200 + 900 * np.sin(np.pi * (t / dur))
    tono = np.sin(2 * np.pi * freq_sweep * t)
    audio = (ruido * 0.6 + tono * 0.4) * env
    # Filtro paso bajo suave mediante convolución
    kernel = np.hamming(35)
    kernel /= kernel.sum()
    audio = np.convolve(audio, kernel, mode="same")
    return audio

def sintetizar_pop():
    # Duración ~0.14s
    dur = 0.14
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    # Barrido de tono rápido de ~550Hz a ~70Hz
    freq = 70 + (550 - 70) * np.exp(-t * 45)
    fase = 2 * np.pi * np.cumsum(freq) / SR
    onda = np.sin(fase)
    # Envolvente percusiva rápida
    env = np.exp(-t * 28)
    return onda * env

def sintetizar_ding():
    # Duración ~0.7s
    dur = 0.7
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    # Fundamental 1318 Hz (E6) y segundo armónico 2636 Hz
    f1, f2 = 1318.5, 2637.0
    onda = np.sin(2 * np.pi * f1 * t) * 0.7 + np.sin(2 * np.pi * f2 * t) * 0.3
    # Decaimiento exponencial suave
    env = np.exp(-t * 5.5)
    return onda * env

def main():
    rutas_destino = [
        r"c:\Users\Lenovo\Documents\Animaciones\Episodio_1\remotion_app\public\assets\sfx",
        r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\sfx"
    ]

    whoosh = sintetizar_whoosh()
    pop = sintetizar_pop()
    ding = sintetizar_ding()

    for dest in rutas_destino:
        guardar_wav(os.path.join(dest, "whoosh.wav"), whoosh)
        guardar_wav(os.path.join(dest, "pop.wav"), pop)
        guardar_wav(os.path.join(dest, "ding.wav"), ding)

if __name__ == "__main__":
    main()
