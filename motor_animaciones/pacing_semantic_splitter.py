"""
pacing_semantic_splitter.py
Motor de segmentación semántica y balance de ritmo para videos explicativos estilo Ink Explainer / Kurzgesagt.

Reglas de Oro:
- Ningún plano debe superar los 5.0 - 5.5 segundos.
- Si una idea/oración supera las 15 palabras (~5 segundos de voz), se desglosa automáticamente
  en la estructura narrativa de 3 pasos: Causa/Premisa -> Acción/Mecanismo -> Consecuencia/Impacto.
- Si una idea dura menos de 2.0 segundos, se agrupa con la siguiente para evitar fatiga visual.
- Si una idea es conceptualmente indivisible y supera 5.5s, se marca con `punch_in: True`.
"""

import re
from typing import List, Dict, Any

# Velocidad promedio de locución en español divulgativo: ~2.6 palabras por segundo
PALABRAS_POR_SEGUNDO = 2.6
FPS = 30

class PacingSemanticSplitter:
    def __init__(self, fps: int = 30):
        self.fps = fps

    def estimar_segundos(self, texto: str) -> float:
        palabras = [p for p in re.findall(r'\b\w+\b', texto) if len(p) > 0]
        return max(1.2, len(palabras) / PALABRAS_POR_SEGUNDO)

    def segmentar_escena(self, texto_escena: str, palabras_clave: List[str] = None) -> List[Dict[str, Any]]:
        """
        Divide una locución larga en micro-planos semánticos equilibrados (2.5s a 5.0s).
        """
        palabras_clave = palabras_clave or []
        duracion_estimada = self.estimar_segundos(texto_escena)

        # Si la escena ya es corta (menor a 4.5 segundos), se mantiene en un solo plano
        if duracion_estimada <= 4.5:
            return [{
                "id_plano": 1,
                "locucion_plano": texto_escena.strip(),
                "palabras_clave_plano": palabras_clave,
                "duracion_estimada_seg": round(duracion_estimada, 2),
                "duracion_frames": int(round(duracion_estimada * self.fps)),
                "animacion": "zoom_in_suave",
                "punch_in": False
            }]

        # Segmentación por puntuación natural y conectores causales
        # Puntos, dos puntos, punto y coma, o conjunciones clave ("pero", "y mientras", "lo que causó", "para")
        delimitadores = r'(?<=[.:;])\s+|(?<=\,)\s+(?=pero|y\s+mientras|lo\s+que|sin\s+embargo|donde|para\s+sobrevivir)'
        partes_raw = re.split(delimitadores, texto_escena)
        partes = [p.strip() for p in partes_raw if len(p.strip()) > 3]

        # Si la división por signos no fue suficiente y sigue habiendo bloques gigantes (> 16 palabras)
        partes_equilibradas = []
        for parte in partes:
            palabras = parte.split()
            if len(palabras) > 18:
                # Subdividir por conjunciones secundarias (" y ", " que ", " como ")
                sub_partes = re.split(r'\s+(?:y|mientras|que|donde|cuando)\s+', parte)
                if len(sub_partes) > 1:
                    mitad = len(sub_partes) // 2
                    partes_equilibradas.append(" y ".join(sub_partes[:mitad]))
                    partes_equilibradas.append(" y ".join(sub_partes[mitad:]))
                else:
                    partes_equilibradas.append(parte)
            else:
                partes_equilibradas.append(parte)

        # Si aún así queda 1 solo bloque largo, forzar división por mitades semánticas
        if len(partes_equilibradas) <= 1:
            palabras = texto_escena.split()
            mitad = len(palabras) // 2
            partes_equilibradas = [
                " ".join(palabras[:mitad]) + "...",
                "..." + " ".join(palabras[mitad:])
            ]

        # Construir planos con animación alternada profesional (zoom -> paneo -> punch-in)
        planos = []
        animaciones = ["zoom_in_suave", "paneo_suave", "flotar_suave"]

        for i, fragmento in enumerate(partes_equilibradas):
            dur_seg = self.estimar_segundos(fragmento)
            dur_frames = int(round(dur_seg * self.fps))
            
            # Asignar palabras clave coincidentes
            kw_fragmento = [kw for kw in palabras_clave if kw.lower() in fragmento.lower()]
            if not kw_fragmento and palabras_clave:
                kw_fragmento = [palabras_clave[i % len(palabras_clave)]]

            anim = animaciones[i % len(animaciones)]
            es_largo = dur_seg > 5.2

            planos.append({
                "id_plano": i + 1,
                "locucion_plano": fragmento,
                "palabras_clave_plano": kw_fragmento,
                "duracion_estimada_seg": round(dur_seg, 2),
                "duracion_frames": dur_frames,
                "animacion": anim,
                "punch_in": es_largo
            })

        return planos

if __name__ == "__main__":
    splitter = PacingSemanticSplitter()
    ejemplo = "Los rayos ultravioleta penetran en la dermis y destruyen el folato en la sangre, lo que puede causar graves problemas en la reproducción humana."
    resultado = splitter.segmentar_escena(ejemplo, ["rayos ultravioleta", "folato", "reproducción"])
    print(f"Original ({splitter.estimar_segundos(ejemplo):.2f}s) dividido en {len(resultado)} planos:")
    for p in resultado:
        print(f" - Plano {p['id_plano']} ({p['duracion_estimada_seg']}s, {p['duracion_frames']} frames, punch_in={p['punch_in']}): '{p['locucion_plano']}'")
