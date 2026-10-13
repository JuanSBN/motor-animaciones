import os
import sys
import shutil
import modal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Referencias del personaje Niko
RUTAS_REFERENCIA = [
    r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791665303682_8824c789.jpg",
    r"C:\Users\Lenovo\.gemini\antigravity\brain\d4d3428f-a579-412f-8a74-7bb3c635c471\.user_uploaded\media_1791669629035_2d38f9e5.jpg"
]
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# 3 Prompts para los nuevos planos alternos
prompts = [
    # 1. Plano del sol abrasador sobre la sabana
    "Cinematic wide dramatic shot of the prehistoric African savannah landscape under a colossal, scorching glowing sun. Heatwaves shimmering in the air, dusty orange and golden sky, acacia trees in the distance. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors.",
    # 2. Niko mirando con curiosidad su brazo / piel con escudo dorado
    "Close up shot of a young boy looking with curiosity at his arm. Messy teal hair, band-aid on his cheek, green vest, yellow striped t-shirt. A warm golden protective glow emanates around his skin. 2D flat cartoon illustration style, clean lines, flat shading.",
    # 3. Rayos UV púrpuras cayendo hacia la superficie microscópica
    "Microscopic view of glowing purple ultraviolet solar rays beaming down from space towards a cellular landscape. Abstract, vibrant, educational scientific illustration. 2D flat cartoon illustration style, clean lines, flat shading."
]

nombres = [
    "assets/img/flux_16_9_sol_sabana.png",
    "assets/img/flux_16_9_niko_piel.png",
    "assets/img/flux_16_9_rayos_uv.png"
]

def main():
    print("🚀 Conectando con Modal para generar 3 planos adicionales...")
    ref_bytes_list = []
    for r in RUTAS_REFERENCIA:
        if os.path.exists(r):
            with open(r, "rb") as f:
                ref_bytes_list.append(f.read())

    from orquestador import app, generar_imagenes_flux_16_9
    with modal.enable_output():
        with app.run():
            imagenes_bytes = generar_imagenes_flux_16_9.remote(prompts, ref_bytes_list, HF_TOKEN)

    os.makedirs("assets/img", exist_ok=True)
    remotion_img_dir = os.path.join("remotion_app", "public", "assets", "img")
    os.makedirs(remotion_img_dir, exist_ok=True)

    for ruta, img_bytes in zip(nombres, imagenes_bytes):
        with open(ruta, "wb") as f:
            f.write(img_bytes)
        print(f"✅ Guardado local: {ruta}")
        
        # Copiar a Remotion
        dst = os.path.join(remotion_img_dir, os.path.basename(ruta))
        shutil.copy2(ruta, dst)
        print(f"✅ Copiado a Remotion: {dst}")

    print("\n🎉 ¡Los 3 planos adicionales están listos!")

if __name__ == "__main__":
    main()
