import json
from moviepy.editor import AudioFileClip

def actualizar_duraciones():
    with open('esquema_maestro.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_frames = 0
    total_segundos = 0

    for escena in data['escenas']:
        audio_path = escena['archivos_generados']['audio_tts']
        clip = AudioFileClip(audio_path)
        duracion = clip.duration
        clip.close()
        
        frames = int(round(duracion * 30))
        escena['duracion_segundos'] = round(duracion, 2)
        escena['duracion_frames'] = frames
        
        total_segundos += duracion
        total_frames += frames
        print(f"Escena {escena['id']}: {duracion:.2f}s ({frames} frames a 30fps)")

    data['metadata']['duracion_total_segundos'] = round(total_segundos, 2)
    data['metadata']['duracion_total_frames'] = total_frames

    with open('esquema_maestro.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Total Video: {total_segundos:.2f}s ({total_frames} frames). JSON actualizado exitosamente.")

if __name__ == '__main__':
    actualizar_duraciones()
