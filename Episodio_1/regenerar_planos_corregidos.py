import os
import sys
import shutil
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

HF_TOKEN = os.environ.get("HF_TOKEN", "")

ITEMS = [
    {
        "id": "ep1_escena_15_p2",
        "ruta": "assets/img/ep1_escena_15_p2.png",
        "prompt": "Delicious rustic Arctic feast of freshly caught salmon fish fillets arranged on a clean wooden platter with wild berries, glowing warm golden nutrient sun particles floating around the food. 2D flat cartoon illustration style, clean lines, flat shading, appetizing, cozy warm lighting, solid soft background, NO text, NO letters, NO words, NO humans.",
        "use_ref": False
    },
    {
        "id": "ep1_escena_17_p2",
        "ruta": "assets/img/ep1_escena_17_p2.png",
        "prompt": "Diverse stylized cartoon human characters standing side by side around a glowing golden DNA double helix network connecting all of them, showing genetic unity and individual diversity. Warm clean aesthetic, educational infographic illustration, 2D flat cartoon style, clean thick outlines, solid pastel background, NO text, NO letters, NO tree, NO words.",
        "use_ref": False
    },
    {
        "id": "ep1_escena_18_p2",
        "ruta": "assets/img/ep1_escena_18_p2.png",
        "prompt": "A sleek modern white commercial passenger airplane soaring through a bright sunny blue sky with fluffy white cartoon clouds and golden sunshine. 2D flat cartoon illustration style, clean crisp lines, flat shading, vibrant colors, NO bottles, NO medicine, NO text, NO letters.",
        "use_ref": False
    },
    {
        "id": "ep1_escena_10_p2",
        "ruta": "assets/img/ep1_escena_10_p2.png",
        "prompt": "Silhouette of an ancient human standing on a mountain peak at golden dawn, happily bathing in warm golden sunbeams, surrounded by glowing sparkles of life energy. 2D flat cartoon illustration style, clean lines, flat shading, majestic morning light, NO bottles, NO containers, NO text, NO words.",
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
    
    print(f"🚀 Enviando {len(ITEMS)} imágenes corregidas a Modal (FLUX.2 Klein)...")
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
        
    print("\n🎉 ¡Regeneración selectiva completada con éxito!")

if __name__ == "__main__":
    main()
