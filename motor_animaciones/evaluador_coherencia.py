"""
evaluador_coherencia.py
Módulo de Control de Calidad y Coherencia Visual basado en Embeddings (CLIP).

Ventajas sobre VLMs (Moondream/LLMs):
- Ejecución ultra-rápida (menos de 200ms en CPU local).
- Cero dependencia de red o conexiones SSH lentas.
- Medición matemática objetiva en espacio latente (similitud del coseno 0-100%).
- Rechazo automático de imágenes fuera de modelo (off-model) o con artefactos severos.
"""

import os
import sys
import torch
from pathlib import Path
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
RUTA_CANON_DIA = BASE_DIR / "niko_canon_ep2.png"
RUTA_CANON_PIJAMA = BASE_DIR / "niko_referencia_pijama.png"

MODEL_ID = "openai/clip-vit-base-patch32"

class EvaluadorCoherencia:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EvaluadorCoherencia, cls).__new__(cls)
            cls._instance._inicializar()
        return cls._instance

    def _inicializar(self):
        self.processor = CLIPProcessor.from_pretrained(MODEL_ID)
        self.model = CLIPModel.from_pretrained(MODEL_ID)
        self.model.eval()

        # Precalcular embeddings de referencia canónicos
        self.emb_niko_dia = self.calcular_embedding(str(RUTA_CANON_DIA))
        self.emb_niko_pijama = self.calcular_embedding(str(RUTA_CANON_PIJAMA))

    def calcular_embedding(self, img_path: str):
        img = Image.open(img_path).convert("RGB")
        inputs = self.processor(images=img, return_tensors="pt")
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
            if hasattr(features, "pooler_output"):
                features = features.pooler_output
            elif hasattr(features, "image_embeds"):
                features = features.image_embeds
            features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features

    def evaluar_niko(self, img_path: str, es_pijama: bool = False, umbral: float = 75.0) -> dict:
        """
        Evalúa si la imagen candidata mantiene la identidad y estilo canónico de Niko.
        """
        if not os.path.exists(img_path):
            return {"aprobado": False, "score": 0.0, "mensaje": "Imagen no encontrada"}

        emb_candidata = self.calcular_embedding(img_path)
        emb_referencia = self.emb_niko_pijama if es_pijama else self.emb_niko_dia

        similitud = torch.cosine_similarity(emb_referencia, emb_candidata).item() * 100.0
        aprobado = similitud >= umbral

        return {
            "aprobado": aprobado,
            "score": round(similitud, 2),
            "umbral": umbral,
            "tipo_referencia": "pijama" if es_pijama else "dia/aventura",
            "mensaje": f"{'✅ APROBADO' if aprobado else '❌ RECHAZADO'} ({similitud:.1f}% >= {umbral:.1f}%)"
        }

if __name__ == "__main__":
    evaluador = EvaluadorCoherencia()
    test_img = str(RUTA_CANON_DIA)
    res = evaluador.evaluar_niko(test_img)
    print("Test auto-evaluación:", res)
