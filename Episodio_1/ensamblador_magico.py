import os
import re
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx

def main():
    print("=================================================")
    print("🤖 ENSAMBLADOR AUTOMÁTICO DE EPISODIOS")
    print("=================================================")
    
    base_dir = r"C:\Users\Lenovo\Documents\Animaciones\Episodio_1"
    videos_dir = os.path.join(base_dir, "Videos_Base")
    audios_dir = os.path.join(base_dir, "Audios")
    output_file = os.path.join(base_dir, "Episodio_1_FINAL.mp4")

    print(f"Buscando videos en: {videos_dir}")
    print(f"Buscando audios en: {audios_dir}")

    # Función para extraer el número de la escena (ej. "1_selva.mp4" -> 1)
    def get_number(filename):
        match = re.search(r'^(\d+)', filename)
        return int(match.group(1)) if match else 9999

    video_files = sorted([f for f in os.listdir(videos_dir) if f.lower().endswith(('.mp4', '.mov', '.avi'))], key=get_number)
    audio_files = sorted([f for f in os.listdir(audios_dir) if f.lower().endswith(('.mp3', '.wav', '.m4a'))], key=get_number)

    if not video_files:
        print("\n❌ ¡Oops! No encontré ningún video en la carpeta Videos_Base.")
        return
    if not audio_files:
        print("\n❌ ¡Oops! No encontré ningún audio en la carpeta Audios.")
        return

    print(f"¡Encontré {len(video_files)} videos y {len(audio_files)} audios listos para ensamblar!\n")

    clips_finales = []

    # Emparejar cada video con su audio
    for i, (v_file, a_file) in enumerate(zip(video_files, audio_files)):
        print(f"🎬 Sincronizando Escena {i+1}: {v_file} + {a_file}")
        
        video_path = os.path.join(videos_dir, v_file)
        audio_path = os.path.join(audios_dir, a_file)
        
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        v_dur = video_clip.duration
        a_dur = audio_clip.duration
        
        print(f"   -> Duración de Video original: {v_dur:.2f}s | Voz/Audio: {a_dur:.2f}s")
        
        if a_dur > v_dur:
            # Si el audio de voz es más largo, multiplicamos el video con un efecto "Bumerán" (Ping-Pong)
            print("   -> ⚠️ El diálogo es más largo. Bumeraneando el video para cubrir el tiempo...")
            reversed_clip = video_clip.fx(vfx.time_mirror)
            
            ping_pong_clips = []
            dur_acumulada = 0
            adelante = True
            
            while dur_acumulada < a_dur:
                clip_a_sumar = video_clip if adelante else reversed_clip
                ping_pong_clips.append(clip_a_sumar)
                dur_acumulada += v_dur
                adelante = not adelante
                
            video_extendido = concatenate_videoclips(ping_pong_clips)
            video_sincronizado = video_extendido.subclip(0, a_dur)
        else:
            # Si el video sobró, lo recortamos limpio donde termina la voz
            print("   -> ✂️ Recortando el exceso de video al final de la voz...")
            video_sincronizado = video_clip.subclip(0, a_dur)
            
        # Ponerle la pista de voz al video
        video_listo = video_sincronizado.set_audio(audio_clip)
        clips_finales.append(video_listo)

    if clips_finales:
        print("\n⏳ Uniendo todas las escenas... (El proceso de Renderizado empezará ahora)")
        pelicula_final = concatenate_videoclips(clips_finales, method="compose")
        
        pelicula_final.write_videofile(
            output_file, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            logger="bar" # Muestra la barra de carga bonita en la consola
        )
        print(f"\n✅ ¡MISIÓN CUMPLIDA! Tu película completa está lista en:\n{output_file}")

if __name__ == "__main__":
    main()
