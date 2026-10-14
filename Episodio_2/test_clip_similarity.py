import os
import sys
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

MODEL_ID = "openai/clip-vit-base-patch32"

print(f"🚀 Cargando extractor de embeddings: {MODEL_ID}...")
processor = CLIPProcessor.from_pretrained(MODEL_ID)
model = CLIPModel.from_pretrained(MODEL_ID)
model.eval()

def obtener_embedding(img_path):
    img = Image.open(img_path).convert("RGB")
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        features = model.get_image_features(**inputs)
        # Normalizar vector
        if hasattr(features, "pooler_output"):
            features = features.pooler_output
        elif hasattr(features, "image_embeds"):
            features = features.image_embeds
        features = features / features.norm(p=2, dim=-1, keepdim=True)
    return features

ref_path = r"c:\Users\Lenovo\Documents\Animaciones\motor_animaciones\niko_canon_ep2.png"

test_images = [
    ("Canónico Niko (Calle)", r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_2_p1.png"),
    ("Niko Cama (Pijama)", r"c:\Users\Lenovo\Documents\Animaciones\motor_animaciones\niko_referencia_pijama.png"),
    ("Niko 1:4.5 (Biblioteca)", r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_3_p1.png"),
    ("Hipocampo Dorado (No es Niko)", r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_3_p2.png"),
    ("Cámara de Seguridad (No es Niko)", r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\ep2_escena_3_p5.png"),
]

print(f"\n📌 Imagen de Referencia Canónica: {os.path.basename(ref_path)}")
emb_ref = obtener_embedding(ref_path)

print("\n--- RESULTADOS DE SIMILITUD DE IDENTIDAD VISUAL ---")
for nombre, ruta in test_images:
    if os.path.exists(ruta):
        emb_test = obtener_embedding(ruta)
        sim = torch.cosine_similarity(emb_ref, emb_test).item() * 100.0
        veredicto = "✅ COHERENTE" if sim >= 70.0 else ("⚠️ PARCIAL" if sim >= 55.0 else "❌ RECHAZADO")
        print(f"{nombre:35s}: {sim:5.1f}% [{veredicto}]")
    else:
        print(f"{nombre:35s}: ARCHIVO NO ENCONTRADO")
