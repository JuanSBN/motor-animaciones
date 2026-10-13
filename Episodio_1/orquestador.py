import json
import os
import sys
import modal

# Forzar salida UTF-8 en Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# ----- CONFIGURACIÓN DE MODAL PARA FLUX.2 (16:9 NATIVO) -----
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)

app = modal.App("orquestador-flux2-16-9", image=image)

@app.function(gpu="A100", timeout=1200)
def generar_imagenes_flux_16_9(prompts: list, ref_images_bytes: list, hf_token: str, use_ref_flags: list = None):
    from huggingface_hub import login
    import torch
    from diffusers import Flux2KleinPipeline
    from PIL import Image
    import io
    
    login(token=hf_token)
    print("🚀 Cargando Motor FLUX.2 Klein 4B en Modal...")
    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=torch.bfloat16
    ).to("cuda")
    
    ref_images = [Image.open(io.BytesIO(b)).convert("RGB") for b in ref_images_bytes] if ref_images_bytes else []
    
    resultados = []
    for i, escena in enumerate(prompts):
        use_ref = use_ref_flags[i] if (use_ref_flags and i < len(use_ref_flags)) else (len(ref_images) > 0)
        
        tipo_str = "con referencia limpia de Niko" if (use_ref and ref_images) else "Text-to-Image PURO (sin plantilla)"
        print(f"🎬 Renderizando imagen {i+1}/{len(prompts)} [{tipo_str}] en 16:9 (1344x768)...")
        
        kwargs = {
            "prompt": escena,
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1344,
            "height": 768
        }
        if use_ref and ref_images:
            kwargs["image"] = ref_images
            
        image_out = pipe(**kwargs).images[0]
        
        byte_arr = io.BytesIO()
        image_out.save(byte_arr, format='PNG')
        resultados.append(byte_arr.getvalue())
        
    return resultados

# ----- GENERACIÓN DE VOZ CON GEMINI (CHARON) LOCAL -----
def generar_audio_charon(texto: str, ruta_salida: str, gemini_api_key: str):
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash-preview-tts',
        contents=texto,
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO'],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Charon'
                    )
                )
            )
        )
    )
    import wave
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            with wave.open(ruta_salida, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(part.inline_data.data)
            return True
    return False

# ----- ORQUESTADOR PRINCIPAL -----
def procesar_guion_completo(json_path: str, hf_token: str, gemini_api_key: str, ref_paths: list):
    from moviepy.editor import AudioFileClip
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("assets/img", exist_ok=True)
    
    total_segundos = 0
    total_frames = 0
    prompts_to_generate = []
    output_image_paths = []
    
    print(f"📘 Procesando guion: {data['metadata']['titulo']}")
    
    # 1. Generar Voces con Charon y calcular duraciones
    for escena in data["escenas"]:
        id_escena = escena["id"]
        texto = escena["locucion"]
        prompt = escena["prompt_imagen"]
        audio_path = f"assets/audio/voz_charon_escena_{id_escena}.wav"
        img_path = f"assets/img/flux_16_9_escena_{id_escena}.png"
        
        escena["archivos_generados"]["audio_tts"] = audio_path
        escena["archivos_generados"]["imagen_flux"] = img_path
        
        print(f"🎙️ Generando Voz Charon (Gemini) para Escena {id_escena}...")
        generar_audio_charon(texto, audio_path, gemini_api_key)
        
        # Medir duración exacta del audio generado
        clip = AudioFileClip(audio_path)
        duracion = clip.duration
        clip.close()
        
        frames = int(round(duracion * 30))
        escena["duracion_segundos"] = round(duracion, 2)
        escena["duracion_frames"] = frames
        total_segundos += duracion
        total_frames += frames
        
        prompts_to_generate.append(prompt)
        output_image_paths.append(img_path)
        
    data["metadata"]["duracion_total_segundos"] = round(total_segundos, 2)
    data["metadata"]["duracion_total_frames"] = total_frames
    
    # Guardar JSON actualizado con los nuevos audios y duraciones
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ JSON actualizado con duraciones y archivos de Charon.")
    
    # 2. Generar imágenes 16:9 con FLUX en Modal
    print("\n🎨 Generando imágenes panorámicas 16:9 en Modal...")
    ref_bytes_list = []
    for ruta in ref_paths:
        if os.path.exists(ruta):
            with open(ruta, "rb") as f:
                ref_bytes_list.append(f.read())
        else:
            print(f"⚠️ Imagen de referencia no encontrada: {ruta}")
            
    with modal.enable_output():
        with app.run():
            imagenes_bytes = generar_imagenes_flux_16_9.remote(prompts_to_generate, ref_bytes_list, hf_token)
            
    # 3. Guardar imágenes finales
    for path, img_bytes in zip(output_image_paths, imagenes_bytes):
        with open(path, "wb") as f:
            f.write(img_bytes)
        print(f"✅ Guardado: {path}")
        
    # 4. Sincronizar activos con Remotion
    import shutil
    public_dir = os.path.join("remotion_app", "public")
    if os.path.exists(public_dir):
        print("\n🔄 Sincronizando activos con Remotion Studio...")
        os.makedirs(os.path.join(public_dir, "assets", "audio"), exist_ok=True)
        os.makedirs(os.path.join(public_dir, "assets", "img"), exist_ok=True)
        for escena in data["escenas"]:
            a_src = escena["archivos_generados"]["audio_tts"]
            i_src = escena["archivos_generados"]["imagen_flux"]
            if os.path.exists(a_src):
                shutil.copy2(a_src, os.path.join(public_dir, a_src))
            if os.path.exists(i_src):
                shutil.copy2(i_src, os.path.join(public_dir, i_src))
        print("✅ Activos sincronizados con remotion_app/public/assets!")

    print("\n🎉 ¡Proceso completado con éxito!")

if __name__ == "__main__":
    RUTAS_REFERENCIA = [
        r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791665303682_8824c789.jpg",
        r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791669629035_2d38f9e5.jpg"
    ]
    HF_TOKEN = os.environ.get("HF_TOKEN", "")
    GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
    
    procesar_guion_completo("esquema_maestro.json", HF_TOKEN, GEMINI_KEY, RUTAS_REFERENCIA)
