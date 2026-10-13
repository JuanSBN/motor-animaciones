import os
import sys
import shutil
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

HF_TOKEN = os.environ.get("HF_TOKEN", "")

ITEMS = [
    {
        "id": "ep1_escena_8_p2",
        "ruta": "assets/img/ep1_escena_8_p2.png",
        "prompt": "Clean scientific educational cartoon showing gentle golden sunbeams activating glowing Vitamin D energy particles inside human bone tissue, strong healthy skeleton structure glowing with vibrant health. 2D flat cartoon illustration style, clean lines, flat shading, pure solid background, NO suitcase, NO luggage, NO text, NO letters.",
        "use_ref": False
    },
    {
        "id": "ep1_escena_5_p1",
        "ruta": "assets/img/ep1_escena_5_p1.png",
        "prompt": "Ancient prehistoric African humans walking proudly across the sun-drenched savannah in broad daylight under a bright equatorial sun, with rich dark protective skin and a glowing golden aura representing biological sun armor. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors, NO tents, NO campfire, NO night, NO text.",
        "use_ref": False
    }
]

def main():
    prompts = [item["prompt"] for item in ITEMS]
    use_ref_flags = [item["use_ref"] for item in ITEMS]
    rutas = [item["ruta"] for item in ITEMS]
    
    remotion_img_dir = os.path.join("remotion_app", "public", "assets", "img")
    os.makedirs(remotion_img_dir, exist_ok=True)
    os.makedirs("assets/img", exist_ok=True)
    
    print(f"🚀 Enviando {len(ITEMS)} imágenes críticas a Modal (FLUX.2 Klein)...")
    from orquestador import app, generar_imagenes_flux_16_9
    
    with modal.enable_output():
        with app.run():
            imagenes_bytes = generar_imagenes_flux_16_9.remote(
                prompts, [], HF_TOKEN, use_ref_flags
            )
            
    print(f"\n💾 Guardando {len(imagenes_bytes)} imágenes corregidas...")
    for item, img_bytes in zip(ITEMS, imagenes_bytes):
        ruta = item["ruta"]
        with open(ruta, "wb") as f:
            f.write(img_bytes)
        dst = os.path.join(remotion_img_dir, os.path.basename(ruta))
        shutil.copy2(ruta, dst)
        print(f"✅ Reemplazado con éxito: {ruta} -> {dst}")
        
    print("\n🎉 ¡Regeneración completada!")

if __name__ == "__main__":
    main()
