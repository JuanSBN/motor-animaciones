"""
generar_ep2_primeros_30s.py
Genera el audio oficial y las 6 imágenes FLUX.2 para los primeros 30 segundos
del Episodio 2 (El Sueño / El Momento de Quedarse Dormido).
"""

import os
import sys
import wave
import json
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
REF_NIKOS = [
    r"c:\Users\Lenovo\Documents\Animaciones\Episodio_1\assets\img\ep1_escena_13_p2.png",
    r"C:\Users\Lenovo\.gemini\antigravity\brain\eca3fd45-df48-4b97-9eba-a44d2e61b37b\.user_uploaded\media_1791841367098_6324779a.jpg"
]

OUT_AUDIO_DIR = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\audio"
OUT_IMG_DIR = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img"
os.makedirs(OUT_AUDIO_DIR, exist_ok=True)
os.makedirs(OUT_IMG_DIR, exist_ok=True)

# 1. Generar Audio Oficial con Gemini TTS Puck
def generar_audio_puck(texto: str, out_path: str):
    from google import genai
    from google.genai import types
    print(f"🎙️ Generando voz oficial de Puck para Escena 1...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    resp = client.models.generate_content(
        model='gemini-2.5-flash-preview-tts',
        contents=texto,
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO'],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Puck')
                )
            )
        )
    )
    with wave.open(out_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(resp.candidates[0].content.parts[0].inline_data.data)
    
    # Calcular duración exacta
    with wave.open(out_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        dur_seg = frames / float(rate)
    print(f"✅ Audio generado: {out_path} ({dur_seg:.2f} segundos, {int(round(dur_seg * 30))} frames Remotion)")
    return dur_seg

# 2. Configurar Modal para FLUX.2
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("diffusers", "transformers", "accelerate", "torch", "sentencepiece", "protobuf", "huggingface_hub", "pillow")
)
app = modal.App("ep2-primeros-30s-flux2", image=image)

@app.function(gpu="A100", timeout=1200)
def generar_imagenes_modal(prompts: list, ref_bytes_list: list, hf_token: str):
    from huggingface_hub import login
    import torch
    from diffusers import Flux2KleinPipeline
    from PIL import Image
    import io

    login(token=hf_token)
    print("🚀 Cargando FLUX.2 Klein 4B en Modal A100...")
    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=torch.bfloat16
    ).to("cuda")

    ref_images = [Image.open(io.BytesIO(b)).convert("RGB") for b in ref_bytes_list] if ref_bytes_list else []

    resultados = []
    for i, p in enumerate(prompts):
        print(f"🎬 Generando Plano {i+1}/{len(prompts)} en 16:9...")
        kwargs = {
            "prompt": p,
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1344,
            "height": 768
        }
        if ref_images:
            kwargs["image"] = ref_images

        img_out = pipe(**kwargs).images[0]
        byte_arr = io.BytesIO()
        img_out.save(byte_arr, format='PNG')
        resultados.append(byte_arr.getvalue())

    return resultados

def main():
    json_path = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\esquema_maestro_ep2.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    escena_1 = data["escenas"][0]
    audio_path = os.path.join(OUT_AUDIO_DIR, "voz_puck_ep2_escena_1.wav")
    
    # 1. Generar audio
    dur_seg = generar_audio_puck(escena_1["locucion"], audio_path)
    total_frames = int(round(dur_seg * 30))
    escena_1["duracion_segundos"] = round(dur_seg, 2)
    escena_1["duracion_frames"] = total_frames
    escena_1["archivos_generados"] = {
        "audio_tts": "assets/audio/voz_puck_ep2_escena_1.wav"
    }

    # Distribuir frames entre los 6 planos proporcionalmente
    pesos = [0.15, 0.18, 0.14, 0.16, 0.20, 0.17] # Proporción según longitud del texto
    for idx, plano in enumerate(escena_1["planos"]):
        plano["duracion_frames"] = int(round(total_frames * pesos[idx]))
    # Ajustar diferencia de redondeo en el último plano
    diff = total_frames - sum(p["duracion_frames"] for p in escena_1["planos"])
    escena_1["planos"][-1]["duracion_frames"] += diff

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ JSON actualizado con duraciones exactas de audio.")

    # 2. Generar imágenes para los 6 planos
    prompts = [p["prompt"] for p in escena_1["planos"]]
    ref_bytes = []
    for r in REF_NIKOS:
        if os.path.exists(r):
            with open(r, "rb") as rf:
                ref_bytes.append(rf.read())

    print(f"\n🎨 Lanzando generación de los 6 planos en Modal ({len(prompts)} imágenes)...")
    with modal.enable_output():
        with app.run():
            imgs_bytes = generar_imagenes_modal.remote(prompts, ref_bytes, HF_TOKEN)

    # 3. Guardar imágenes
    for idx, b in enumerate(imgs_bytes):
        out_file = os.path.join(OUT_IMG_DIR, f"ep2_escena_1_p{idx+1}.png")
        with open(out_file, "wb") as f:
            f.write(b)
        print(f"✅ Guardado: {out_file}")

    print("\n🎉 ¡Primeros 30 segundos generados con éxito!")

if __name__ == "__main__":
    main()
