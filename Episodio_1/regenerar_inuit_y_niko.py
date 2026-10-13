import os
import sys
import shutil
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
RUTA_REFERENCIA_NIKO = r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791669629035_2d38f9e5.jpg"

ITEMS = [
    {
        "id": "ep1_escena_13_p2",
        "ruta": "assets/img/ep1_escena_13_p2.png",
        "prompt": "Young boy Niko with messy teal hair, band-aid on his cheek, yellow striped t-shirt and green vest, looking with wonder at a single colorful world map pinned to a warm wooden wall. Clean cozy minimalist room. 2D flat cartoon illustration style, clean bold lines, flat shading, vibrant colors, NO extra posters, NO graphs, NO charts, NO text, NO letters, NO scribbles.",
        "use_ref": True
    },
    {
        "id": "ep1_escena_15_p1",
        "ruta": "assets/img/ep1_escena_15_p1.png",
        "prompt": "Authentic indigenous Inuit hunter with rich warm bronze-tan skin tone, dark almond eyes and dark hair, wearing a traditional thick hooded Arctic fur anorak coat. Standing proudly on glistening Arctic sea ice holding a freshly caught shiny arctic fish, with a traditional wooden kayak on ice under majestic glowing green aurora borealis in polar sky. 2D flat cartoon illustration style, clean lines, flat shading, vibrant, respectful, NO Caucasian elderly man, NO pale skin, NO grey beard, NO text, NO letters.",
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
    
    ref_bytes_list = []
    if os.path.exists(RUTA_REFERENCIA_NIKO):
        with open(RUTA_REFERENCIA_NIKO, "rb") as f:
            ref_bytes_list.append(f.read())
            
    print(f"🚀 Generando {len(ITEMS)} imágenes en Modal...")
    from orquestador import app, generar_imagenes_flux_16_9
    
    with modal.enable_output():
        with app.run():
            imagenes_bytes = generar_imagenes_flux_16_9.remote(
                prompts, ref_bytes_list, HF_TOKEN, use_ref_flags
            )
            
    print(f"\n💾 Guardando {len(imagenes_bytes)} imágenes...")
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
