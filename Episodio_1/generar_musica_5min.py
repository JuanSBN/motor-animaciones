import numpy as np
import wave
import os
import sys
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sample_rate = 44100
duration = 330.0 # 5.5 minutos para cubrir los 5 minutos completos
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Progreso de acordes lofi cálidos: Cmaj7 - Am7 - Dm7 - G7
chords = [
    [261.63, 329.63, 392.00, 493.88], # Cmaj7
    [220.00, 261.63, 329.63, 392.00], # Am7
    [146.83, 174.61, 220.00, 261.63], # Dm7
    [196.00, 246.94, 293.66, 349.23], # G7
]

audio = np.zeros_like(t)
chord_duration = 3.0 # cada acorde dura 3s

num_chords = int(duration / chord_duration)

for i in range(num_chords):
    chord = chords[i % len(chords)]
    start_idx = int(i * chord_duration * sample_rate)
    end_idx = min(len(t), int((i + 1) * chord_duration * sample_rate))
    chunk_len = end_idx - start_idx
    chunk_t = np.linspace(0, chord_duration, chunk_len, endpoint=False)
    
    # Envolvente suave y cálida
    env = np.sin(np.pi * chunk_t / chord_duration) ** 0.6
    
    chord_wave = np.zeros(chunk_len)
    for freq in chord:
        # Tono suave Rhodes con armónicos aterciopelados
        tone = (
            0.65 * np.sin(2 * np.pi * freq * chunk_t) +
            0.22 * np.sin(2 * np.pi * 2 * freq * chunk_t) +
            0.08 * np.sin(2 * np.pi * 3 * freq * chunk_t)
        )
        chord_wave += tone
        
    # Bajo sutil y profundo
    bass_freq = chord[0] / 2
    bass = 0.45 * np.sin(2 * np.pi * bass_freq * chunk_t)
    
    audio[start_idx:end_idx] += (chord_wave * 0.12 + bass * 0.18) * env

# Normalizar volumen suave documental
audio = audio / np.max(np.abs(audio) + 1e-6) * 0.28
audio_int16 = (audio * 32767).astype(np.int16)

out_path = "assets/audio/musica_fondo_lofi.wav"
with wave.open(out_path, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_int16.tobytes())

# Copiar a Remotion
remotion_audio = os.path.join("remotion_app", "public", "assets", "audio", "musica_fondo_lofi.wav")
os.makedirs(os.path.dirname(remotion_audio), exist_ok=True)
shutil.copy2(out_path, remotion_audio)

print(f"🎵 Música documental lofi generada con éxito ({duration}s / {duration/60:.1f} min)")
