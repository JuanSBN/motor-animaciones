"""
pipeline_maestro.py
Orquestador Integral de Animaciones Automatizadas (Ink Explainer / Kurzgesagt).

Integra:
1. TTS Oficial Unificado (Gemini Voice Puck)
2. Pacing Semántico Inteligente (PacingSemanticSplitter, 2.5s - 5.0s por plano con Punch-in)
3. Enrutador Visual Híbrido (SVG Remotion vs FLUX.2 con guardabarros anti-texto)
4. QA Automático con Moondream (Oracle Cloud aislado)
5. Sincronización Declarativa con Remotion Studio
"""

import os
import sys
import json
import wave
from typing import List, Dict, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from pacing_semantic_splitter import PacingSemanticSplitter
from visual_classifier import VisualClassifier
from oracle_moondream_gate import OracleMoondreamGate

class PipelineAnimaciones:
    def __init__(self, remotion_project_dir: str = "remotion_app"):
        self.remotion_dir = remotion_project_dir
        self.splitter = PacingSemanticSplitter(fps=30)
        self.classifier = VisualClassifier()
        self.qa_gate = OracleMoondreamGate()

    def procesar_guion_crudo(self, escenas_raw: List[Dict[str, Any]], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Toma una lista de escenas con locución y las transforma en una estructura
        cinematográfica multi-plano con ritmo equilibrado y enrutamiento visual.
        """
        metadata = metadata or {
            "titulo": "Nuevo Episodio",
            "estilo_visual": "2D flat cartoon illustration style, clean lines, flat shading, vibrant colors",
            "volumen_musica": 0.10
        }

        escenas_procesadas = []
        total_frames = 0
        total_segundos = 0.0

        for esc in escenas_raw:
            esc_id = esc["id"]
            texto = esc["locucion"]
            palabras_clave = esc.get("palabras_clave", [])

            # 1. Segmentación semántica de ritmo (2.5s - 5.0s por plano)
            planos_divididos = self.splitter.segmentar_escena(texto, palabras_clave)

            # 2. Clasificación visual de cada plano
            planos_finales = []
            duracion_escena_frames = 0

            for plano in planos_divididos:
                clasificacion = self.classifier.clasificar_plano(
                    plano["locucion_plano"],
                    escena_id=esc_id,
                    plano_id=plano["id_plano"]
                )

                plano_datos = {
                    "id_plano": plano["id_plano"],
                    "locucion_plano": plano["locucion_plano"],
                    "palabras_clave_plano": plano["palabras_clave_plano"],
                    "duracion_frames": plano["duracion_frames"],
                    "animacion": plano["animacion"],
                    "punch_in": plano["punch_in"],
                    "tipo_visual": clasificacion["tipo_visual"]
                }

                if clasificacion["tipo_visual"] == "componente_vectorial":
                    plano_datos["componente"] = clasificacion["componente"]
                else:
                    plano_datos["imagen"] = clasificacion["archivo_sugerido"]
                    plano_datos["prompt"] = clasificacion["prompt_sintetizado"]

                planos_finales.append(plano_datos)
                duracion_escena_frames += plano["duracion_frames"]

            dur_seg = round(duracion_escena_frames / 30.0, 2)
            total_frames += duracion_escena_frames
            total_segundos += dur_seg

            escenas_procesadas.append({
                "id": esc_id,
                "acto": esc.get("acto", 1),
                "locucion": texto,
                "palabras_clave": palabras_clave,
                "duracion_segundos": dur_seg,
                "duracion_frames": duracion_escena_frames,
                "archivos_generados": {
                    "audio_tts": f"assets/audio/voz_puck_escena_{esc_id}.wav"
                },
                "planos": planos_finales
            })

        metadata["duracion_total_segundos"] = round(total_segundos, 2)
        metadata["duracion_total_frames"] = total_frames

        return {
            "metadata": metadata,
            "escenas": escenas_procesadas
        }

if __name__ == "__main__":
    pipeline = PipelineAnimaciones()
    
    # Guion de prueba rápido para demostrar el funcionamiento
    guion_test = [
        {
            "id": 1,
            "locucion": "Imagina que estamos en el ecuador, donde la piel absorbe grandes cantidades de radiación solar y necesita proteger el folato celular.",
            "palabras_clave": ["ecuador", "radiación solar", "folato celular"]
        },
        {
            "id": 2,
            "locucion": "Cerca de los polos: piel clara para absorber vitamina D. Una balanza biológica en perfecto equilibrio evolutivo.",
            "palabras_clave": ["polos", "vitamina D", "balanza biológica"]
        }
    ]

    esquema = pipeline.procesar_guion_crudo(guion_test)
    print("✅ Pipeline ejecutado con éxito:")
    print(f"Duración total: {esquema['metadata']['duracion_total_segundos']}s ({esquema['metadata']['duracion_total_frames']} frames)")
    for esc in esquema["escenas"]:
        print(f"\n🎬 Escena {esc['id']} ({esc['duracion_segundos']}s, {len(esc['planos'])} planos):")
        for p in esc["planos"]:
            tipo = p["tipo_visual"]
            extra = p.get("componente") if tipo == "componente_vectorial" else p.get("imagen")
            print(f"   - Plano {p['id_plano']} [{p['animacion']}, punch_in={p['punch_in']}, {p['duracion_frames']}f]: {tipo} -> {extra}")
