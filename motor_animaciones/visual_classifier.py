"""
visual_classifier.py
Enrutador inteligente para el pipeline de animación:
1. Detecta si la escena requiere un componente vectorial SVG interactivo (cero errores de IA).
2. O si requiere una ilustración FLUX.2, inyectando directivas estrictas anti-texto y anti-sesgo cultural.
"""

import re
from typing import Dict, Any

# Catálogo de infografías científicas vectoriales en Remotion
CATALOGO_VECTORIAL = {
    "BalanceScale": {
        "keywords": ["balanza", "equilibrio", "folato", "vitamina d", "proteger el folato", "absorber vitamina"],
        "descripcion": "Balanza dorada oscilante con escudos de Folato B9 y Vitamina D"
    },
    "DnaPieChart": {
        "keywords": ["adn", "genoma", "99.9", "porcentaje", "genes", "veinte mil", "código genético"],
        "descripcion": "Anillo interactivo de 99.9% de ADN idéntico compartido"
    },
    "ThermostatGauge": {
        "keywords": ["termostato", "aguja", "calibrado", "jerarquía", "capricho", "radiación solar"],
        "descripcion": "Termostato solar con aguja animada de Ecuador a Polos"
    },
    "SkinToneTimeline": {
        "keywords": ["gradiente", "latitud", "latitudes", "pigmentación", "tonos de piel", "perdiendo pigmento"],
        "descripcion": "Línea de gradiente geográfico de tonos de piel según latitud"
    },
    "RaceStampCard": {
        "keywords": ["no existen las razas", "razas biológicas", "consenso científico", "categorías biológicas"],
        "descripcion": "Sello dinámico de impacto rojo 'NO EXISTEN' sobre Razas Biológicas"
    }
}

STYLE_SUFFIX = "2D flat cartoon illustration style, clean lines, flat shading, vibrant colors"
NEGATIVE_TEXT_GUARDRAIL = "NO text, NO letters, NO words, NO charts, NO labels, NO typography, clean background"
NIKO_CHARACTER_SHEET = "Young boy Niko, messy teal hair, band-aid on right cheek, olive-green utility vest, yellow striped t-shirt"

class VisualClassifier:
    def clasificar_plano(self, texto_plano: str, escena_id: int = 1, plano_id: int = 1) -> Dict[str, Any]:
        """
        Determina si el plano se renderiza como infografía SVG o como ilustración FLUX.
        """
        texto_lower = texto_plano.lower()

        # 1. Búsqueda de coincidencia en el catálogo vectorial
        for comp_name, config in CATALOGO_VECTORIAL.items():
            for kw in config["keywords"]:
                if kw in texto_lower:
                    return {
                        "tipo_visual": "componente_vectorial",
                        "componente": comp_name,
                        "descripcion": config["descripcion"]
                    }

        # 2. Si no es infografía, es ilustración FLUX.2
        prompt = self.sintetizar_prompt_flux(texto_plano)
        return {
            "tipo_visual": "imagen_flux",
            "prompt_sintetizado": prompt,
            "archivo_sugerido": f"assets/img/ep_escena_{escena_id}_p{plano_id}.png"
        }

    def sintetizar_prompt_flux(self, texto: str) -> str:
        """
        Crea un prompt cinematográfico con guardabarros anti-texto y corrección étnica/cultural.
        """
        texto_lower = texto.lower()
        sujetos = []

        # Guardián de etnias y contextos biológicos específicos
        if "inuit" in texto_lower or "ártico" in texto_lower or "polar" in texto_lower:
            sujetos.append(
                "Authentic indigenous Inuit hunter with warm bronze-tan skin tone, dark eyes, dark hair, "
                "wearing traditional warm fur anorak hood on sea ice with aurora borealis in the background. "
                "Holding a freshly caught fish. NO caucasian elderly man, NO pale skin, NO white beard"
            )
        elif "niko" in texto_lower or "protagonista" in texto_lower or "niño" in texto_lower or "imagina" in texto_lower:
            sujetos.append(f"{NIKO_CHARACTER_SHEET}, showing an expressive curious facial expression")
        elif "sabana" in texto_lower or "sol" in texto_lower or "ancestros" in texto_lower:
            sujetos.append("Cinematic wide shot of the prehistoric African savannah under a giant glowing sun, dusty golden atmospheric haze")
        elif "sudor" in texto_lower or "pelaje" in texto_lower or "correr" in texto_lower:
            sujetos.append("Athletic upright human runner sweating under the sun, drops of sweat glistening on skin, prehistoric landscape")
        elif "casas" in texto_lower or "moderno" in texto_lower or "techos" in texto_lower or "oficina" in texto_lower:
            sujetos.append("Architectural cross-section of a modern building with diverse people working in cozy offices and rooms with laptops and soft lamps")
        else:
            sujetos.append(f"Educational narrative cartoon illustration depicting {texto.strip()}")

        prompt_final = f"{', '.join(sujetos)}. {STYLE_SUFFIX}. {NEGATIVE_TEXT_GUARDRAIL}."
        return prompt_final

if __name__ == "__main__":
    classifier = VisualClassifier()
    test_cases = [
        "Cerca de los polos: piel clara para absorber vitamina D. Una balanza perfecta.",
        "Incluso hubo excepciones fascinantes, como los pueblos Inuit del Ártico, que mantuvieron la piel más oscura.",
        "Científicamente, no existen las razas biológicas.",
        "Imagina que estamos hace millones de años, bajo un sol abrasador en la sabana africana."
    ]

    for t in test_cases:
        res = classifier.clasificar_plano(t)
        print(f"\nFrase: '{t}'")
        print(f"Tipo: {res['tipo_visual']}")
        if res['tipo_visual'] == 'componente_vectorial':
            print(f"Componente SVG: {res['componente']}")
        else:
            print(f"Prompt FLUX: {res['prompt_sintetizado'][:90]}...")
