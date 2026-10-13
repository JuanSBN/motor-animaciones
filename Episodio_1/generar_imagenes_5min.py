import os
import sys
import json
import shutil
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

RUTAS_REFERENCIA = [
    r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791665303682_8824c789.jpg",
    r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791669629035_2d38f9e5.jpg"
]
HF_TOKEN = os.environ.get("HF_TOKEN", "")

def vincular_existentes():
    os.makedirs("assets/img", exist_ok=True)
    mapeo = {
        "assets/img/ep1_escena_1_p1.png": "assets/img/flux_16_9_sol_sabana.png",
        "assets/img/ep1_escena_1_p2.png": "assets/img/flux_16_9_escena_1.png",
        "assets/img/ep1_escena_3_p1.png": "assets/img/flux_16_9_rayos_uv.png",
        "assets/img/ep1_escena_4_p1.png": "assets/img/flux_16_9_niko_piel.png",
        "assets/img/ep1_escena_4_p2.png": "assets/img/flux_16_9_escena_2.png",
        "assets/img/ep1_escena_4_p3.png": "assets/img/flux_16_9_escena_3.png"
    }
    for dest, src in mapeo.items():
        if os.path.exists(src) and not os.path.exists(dest):
            shutil.copy2(src, dest)
            print(f"🔗 Mapeado existente: {src} -> {dest}")

def main():
    vincular_existentes()
    
    with open("esquema_maestro.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    img_dir = "assets/img"
    remotion_img_dir = os.path.join("remotion_app", "public", "assets", "img")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(remotion_img_dir, exist_ok=True)
    
    prompts_pendientes = []
    rutas_pendientes = []
    
    total_planos = 0
    existentes = 0
    
    for escena in data["escenas"]:
        id_e = escena["id"]
        for plano in escena["planos"]:
            total_planos += 1
            id_p = plano["id_plano"]
            prompt = plano["prompt"]
            ruta_img = f"assets/img/ep1_escena_{id_e}_p{id_p}.png"
            
            if os.path.exists(ruta_img):
                existentes += 1
                # Asegurar que esté en remotion
                dst = os.path.join(remotion_img_dir, os.path.basename(ruta_img))
                if not os.path.exists(dst):
                    shutil.copy2(ruta_img, dst)
            else:
                prompts_pendientes.append(prompt)
                rutas_pendientes.append(ruta_img)
                
    print(f"📊 Total de planos requeridos: {total_planos}")
    print(f"✅ Ya existentes en disco: {existentes}")
    print(f"🎨 Faltan por renderizar en Modal: {len(prompts_pendientes)}")
    
    if not prompts_pendientes:
        print("🎉 ¡Todas las imágenes ya están listas!")
        return

    print(f"\n🚀 Conectando con Modal (FLUX.2 Klein en A100) para {len(prompts_pendientes)} imágenes...")
    
    ref_bytes_list = []
    for r in RUTAS_REFERENCIA:
        if os.path.exists(r):
            with open(r, "rb") as f:
                ref_bytes_list.append(f.read())
                
    from orquestador import app, generar_imagenes_flux_16_9
    
    with modal.enable_output():
        with app.run():
            imagenes_bytes = generar_imagenes_flux_16_9.remote(
                prompts_pendientes, ref_bytes_list, HF_TOKEN
            )
            
    print(f"💾 Guardando {len(imagenes_bytes)} imágenes generadas...")
    for ruta, img_bytes in zip(rutas_pendientes, imagenes_bytes):
        with open(ruta, "wb") as f:
            f.write(img_bytes)
        dst = os.path.join(remotion_img_dir, os.path.basename(ruta))
        shutil.copy2(ruta, dst)
        print(f"✅ Listo: {ruta}")
        
    print("\n🎉 ¡Todas las imágenes panorámicas 16:9 han sido generadas y sincronizadas con éxito!")

if __name__ == "__main__":
    main()
