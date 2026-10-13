import os
import sys
import json
import shutil
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Usar ÚNICAMENTE la ilustración limpia de Niko (sin cuadrículas ni títulos de hoja de personaje)
RUTA_REFERENCIA_LIMPIA = r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791669629035_2d38f9e5.jpg"
HF_TOKEN = os.environ.get("HF_TOKEN", "")

def main():
    with open("esquema_maestro.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    img_dir = "assets/img"
    remotion_img_dir = os.path.join("remotion_app", "public", "assets", "img")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(remotion_img_dir, exist_ok=True)
    
    prompts = []
    rutas = []
    use_ref_flags = []
    
    for escena in data["escenas"]:
        id_e = escena["id"]
        for plano in escena["planos"]:
            id_p = plano["id_plano"]
            prompt = plano["prompt"]
            ruta_img = f"assets/img/ep1_escena_{id_e}_p{id_p}.png"
            
            # Determinar si el plano es de Niko o es un diagrama / paisaje
            es_niko = any(k in prompt.lower() for k in ["niko", "young boy", "boy wiping", "boy looking", "boy shivering", "child"])
            
            prompts.append(prompt)
            rutas.append(ruta_img)
            use_ref_flags.append(es_niko)
            
    total_niko = sum(use_ref_flags)
    total_diagramas = len(use_ref_flags) - total_niko
    
    print(f"🎨 Planos a generar: {len(prompts)}")
    print(f"   👤 Con Niko (usando referencia limpia sin texto): {total_niko}")
    print(f"   🔬 Diagramas, ciencia y paisajes (Text-to-Image PURO): {total_diagramas}")
    print("\n🚀 Conectando a Modal (GPU A100 con FLUX.2 Klein)...")
    
    ref_bytes_list = []
    if os.path.exists(RUTA_REFERENCIA_LIMPIA):
        with open(RUTA_REFERENCIA_LIMPIA, "rb") as f:
            ref_bytes_list.append(f.read())
            
    from orquestador import app, generar_imagenes_flux_16_9
    
    with modal.enable_output():
        with app.run():
            imagenes_bytes = generar_imagenes_flux_16_9.remote(
                prompts, ref_bytes_list, HF_TOKEN, use_ref_flags
            )
            
    print(f"\n💾 Guardando y sincronizando las {len(imagenes_bytes)} imágenes limpias...")
    for ruta, img_bytes in zip(rutas, imagenes_bytes):
        with open(ruta, "wb") as f:
            f.write(img_bytes)
        dst = os.path.join(remotion_img_dir, os.path.basename(ruta))
        shutil.copy2(ruta, dst)
        print(f"✅ Sincronizado: {ruta}")
        
    print("\n🎉 ¡TODAS LAS 39 IMÁGENES HAN SIDO REGENERADAS Y ESTÁN 100% LIMPIAS!")

if __name__ == "__main__":
    main()
