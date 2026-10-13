import json
import os

episodio_completo = {
    "metadata": {
        "titulo": "Episodio 1: La Evolución del Color de Piel",
        "duracion_objetivo": "5:00",
        "musica_fondo": "assets/audio/musica_fondo_lofi.wav",
        "volumen_musica": 0.10,
        "estilo_visual": "2D flat cartoon illustration style, clean lines, flat shading, vibrant colors"
    },
    "escenas": [
        # --- ACTO 1: EL ORIGEN Y EL ESCUDO SOLAR ---
        {
            "id": 1,
            "acto": 1,
            "locucion": "Imagina que estamos hace millones de años, bajo un sol abrasador en la sabana africana. Nuestros primeros ancestros enfrentaban un calor implacable.",
            "palabras_clave": ["millones de años", "sol abrasador", "sabana africana"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Cinematic wide dramatic shot of the prehistoric African savannah landscape under a colossal, scorching glowing sun. Heatwaves shimmering in the air, dusty orange and golden sky, acacia trees in the distance. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Wide dynamic shot of a young boy melting from extreme heat. Messy teal hair, band-aid on his cheek, green vest, yellow striped t-shirt. Prehistoric African savannah background with a giant glowing sun. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                }
            ]
        },
        {
            "id": 2,
            "acto": 1,
            "locucion": "Para sobrevivir y no sobrecalentarse mientras corrían, los humanos perdieron el pelaje corporal y desarrollaron millones de glándulas sudoríparas.",
            "palabras_clave": ["perdieron el pelaje", "glándulas sudoríparas"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Side-by-side cartoon comparison: a hairy chimpanzee-like ancestor on the left, and a sleek upright human runner sweating on the right. Minimalist warm background. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Close-up of young boy Niko wiping sweat from his forehead with relief, drops of water dripping from his chin, breathing out hot air. Messy teal hair, band-aid on cheek, green vest. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },
        {
            "id": 3,
            "acto": 1,
            "locucion": "Pero sin pelo, la piel quedó totalmente expuesta a un enemigo invisible y destructor: la radiación ultravioleta del sol.",
            "palabras_clave": ["piel expuesta", "radiación ultravioleta"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Microscopic view of glowing purple ultraviolet solar rays beaming down from space towards a cellular landscape. Abstract, vibrant, educational scientific illustration. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Abstract educational diagram of glowing golden B9 folate molecules in blood vessels getting zapped and shattered by purple UV radiation beams. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                }
            ]
        },
        {
            "id": 4,
            "acto": 1,
            "locucion": "Aquí entró nuestro escudo biológico definitivo: la Melanina. Una molécula oscura producida por melanocitos que cubre el ADN como una sombrilla.",
            "palabras_clave": ["la Melanina", "melanocitos", "sombrilla"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Close up shot of a young boy looking with curiosity at his arm. Messy teal hair, band-aid on his cheek, green vest, yellow striped t-shirt. A warm golden protective glow emanates around his skin. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.35,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "A glowing molecular structure of Melanin floating in the center. Pure vibrant yellow solid background. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.35,
                    "animacion": "flotar_suave"
                },
                {
                    "id_plano": 3,
                    "prompt": "Abstract microscopic shot of tiny cute skin cells holding up tiny umbrellas to block glowing purple sunlight. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.30,
                    "animacion": "zoom_in_suave"
                }
            ]
        },

        # --- ACTO 2: EL GRAN ÉXODO Y LA TRAMPA DEL NORTE ---
        {
            "id": 5,
            "acto": 2,
            "locucion": "Durante cientos de miles de años, tener la piel muy oscura fue la armadura perfecta para proteger la vida en el ecuador. Pero la historia no terminó ahí.",
            "palabras_clave": ["armadura perfecta", "el ecuador"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "A peaceful prehistoric tribal camp in ancient Africa at twilight, humans gathered around a crackling campfire under an acacia tree, starry sky. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Young boy Niko looking towards the distant northern mountain horizon with an adventurous smile, holding a torch, starry night sky. Messy teal hair, band-aid, green vest. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                }
            ]
        },
        {
            "id": 6,
            "acto": 2,
            "locucion": "Hace unos sesenta mil años, pequeños grupos de exploradores comenzaron el viaje más ambicioso de nuestra especie: salieron de África rumbo al norte.",
            "palabras_clave": ["sesenta mil años", "salieron de África"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Stylized 2D illustrated world map with glowing dotted migration arrows spreading outward from Africa across Europe and Asia, clean minimal paper background. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "A small group of ancient nomadic travelers with leather backpacks and walking sticks marching across a rocky mountain pass, looking at distant snowy peaks. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                }
            ]
        },
        {
            "id": 7,
            "acto": 2,
            "locucion": "Al llegar a Europa y el norte de Asia, el entorno cambió drásticamente: inviernos congelados, días nublados y una radiación solar muchísimo más débil.",
            "palabras_clave": ["inviernos congelados", "radiación solar débil"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Vast icy snowy landscape in prehistoric northern Europe, dark pine trees weighed down by snow, misty overcast gray sky with a faint, weak pale sun. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Young boy Niko shivering in the freezing northern wind, wrapped in a fluffy fur coat, looking up at the cloudy gray sky with breath misting in the cold air. Messy teal hair, band-aid. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },
        {
            "id": 8,
            "acto": 2,
            "locucion": "Y ahí surgió un nuevo peligro silencioso. El cuerpo humano necesita rayos UV para sintetizar un nutriente indispensable para los huesos: la Vitamina D.",
            "palabras_clave": ["peligro silencioso", "Vitamina D", "los huesos"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Cute scientific cartoon illustration of a human skeleton with glowing strong golden bones, a smiling sun icon feeding calcium into the spine. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Microscopic diagram of faint, weak sunbeams trying to pierce through dense dark melanin shields in the skin but bouncing away, leaving a low battery icon. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },

        # --- ACTO 3: LA GRAN PARADOJA EVOLUTIVA ---
        {
            "id": 9,
            "acto": 3,
            "locucion": "La armadura que antes salvaba vidas en África, en el frío norte se convirtió en una trampa: bloqueaba la poca luz solar que quedaba.",
            "palabras_clave": ["se convirtió en una trampa", "bloqueaba la luz"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Metaphorical illustration of a knight suit made of dark melanin standing alone in a snowstorm, unable to absorb any warmth from the pale sky. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Ancient mother holding a toddler in a snowy cave entrance, looking worried at weak legs, soft fireplace glow behind them. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },
        {
            "id": 10,
            "acto": 3,
            "locucion": "La naturaleza tuvo que recalibrar la fórmula. Aquellos individuos que nacían con mutaciones que producían menos melanina podían absorber más sol y sobrevivir.",
            "palabras_clave": ["menos melanina", "absorber más sol", "sobrevivir"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Glowing double helix DNA strand floating in dark space with a sparkling golden gene mutation highlighted with magic sparkles. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "A silhouette of a human standing in morning mountain sunlight, absorbing golden energy rays, charging up a full glowing green battery labeled Vitamin D. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                }
            ]
        },
        {
            "id": 11,
            "acto": 3,
            "locucion": "Generación tras generación, la piel en las latitudes altas fue perdiendo pigmento hasta volverse clara, actuando como una esponja diseñada para atrapar cada rayo de sol.",
            "palabras_clave": ["latitudes altas", "piel clara", "esponja"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Horizontal gradient evolutionary timeline showing a progression of skin tones adapting gradually over thousands of years across generations. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Cute microscopic skin cell with clear permeable walls happily catching and soaking up gentle golden sunbeams like a happy sponge. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },
        {
            "id": 12,
            "acto": 3,
            "locucion": "El color de piel no fue un capricho ni una jerarquía. Fue un termostato de radiación solar finamente ajustado por la evolución según el lugar del planeta.",
            "palabras_clave": ["termostato de radiación", "ajustado por la evolución"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Graphic illustration of a sleek modern thermostat dial labeled 'SOLAR RADIATION', with a needle adjusting between Equator (dark) and Arctic (light). 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Stylized rotating Earth globe showing a glowing thermal heat map overlay with vibrant UV radiation zones in the tropics and cool blues at the poles. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },

        # --- ACTO 4: EL MAPA GLOBAL Y EL MITO GENÉTICO ---
        {
            "id": 13,
            "acto": 4,
            "locucion": "Si colocas un mapa de la radiación ultravioleta junto a un mapa de los tonos de piel indígenas tradicionales, coinciden como dos piezas de un rompecabezas.",
            "palabras_clave": ["mapa de radiación", "piezas de un rompecabezas"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Two overlapping translucent jigsaw puzzle maps of the world, one showing UV radiation and the other showing global skin tones, snapping together perfectly. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Young boy Niko looking through a scientific magnifying glass with awe at world maps, colorful charts and diagrams pinned on a wooden wall. Messy teal hair, green vest. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                }
            ]
        },
        {
            "id": 14,
            "acto": 4,
            "locucion": "Cerca del ecuador: piel rica en melanina para proteger el folato. Cerca de los polos: piel clara para absorber vitamina D. Una balanza perfecta.",
            "palabras_clave": ["cerca del ecuador", "cerca de los polos", "balanza perfecta"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "A golden scientific scale in perfect balance, with a glowing green Folate shield on one side and a glowing golden Vitamin D sun crystal on the other. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Two smiling human friends from different ancestral climates giving each other a high-five under a friendly cartoon sun. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                }
            ]
        },
        {
            "id": 15,
            "acto": 4,
            "locucion": "Incluso hubo excepciones fascinantes, como los pueblos Inuit del Ártico, que mantuvieron la piel más oscura porque su dieta basada en pescado graso y focas ya les daba toda la vitamina D.",
            "palabras_clave": ["pueblos Inuit", "pescado graso", "vitamina D"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "An indigenous Inuit hunter standing proudly on Arctic ice next to a wooden kayak, holding a big freshly caught shiny salmon fish under aurora borealis lights. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Nutritional cartoon graphic diagram showing a delicious grilled fish glowing with Vitamin D particles entering the human body without needing sunlight. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },
        {
            "id": 16,
            "acto": 4,
            "locucion": "Pero lo más impactante que descubrió la genética moderna es esto: el color de la piel está determinado por apenas un puñado de genes entre más de veinte mil.",
            "palabras_clave": ["genética moderna", "un puñado de genes"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Modern laboratory setting with a scientist in white coat looking at a holographic 3D DNA model with just three tiny glowing beads highlighted among thousands. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Pie chart graphic showing 99.9% labeled 'IDENTICAL HUMAN DNA' in vibrant green, with a microscopic 0.1% sliver in yellow for superficial traits. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                }
            ]
        },

        # --- ACTO 5: LA BIBLIOTECA VIVA DE NUESTROS ANCESTROS ---
        {
            "id": 17,
            "acto": 5,
            "locucion": "Científicamente, no existen las razas biológicas. Dos personas de piel oscura en África pueden tener más diferencias genéticas entre sí que con una persona de piel clara en Europa.",
            "palabras_clave": ["no existen las razas", "diferencias genéticas"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Minimalist white background with a bold red hand-drawn 'X' stamping across the word 'BIOLOGICAL RACE', in clean educational ink explainer style. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "An expansive genealogical family tree showing all human branches blooming from a single giant ancient African baobab trunk, diverse leaves. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                }
            ]
        },
        {
            "id": 18,
            "acto": 5,
            "locucion": "Hoy vivimos en casas con techos, volamos en aviones y nos mudamos de continente en horas, confundiendo al viejo termostato de nuestros antepasados.",
            "palabras_clave": ["casas con techos", "mudamos de continente"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Cross-section cartoon of a modern city building with people sitting under indoor fluorescent lights, looking at computer screens inside cozy apartments. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "A modern commercial airplane flying above white clouds, with a bottle of sunscreen on one side and a bottle of Vitamin D supplements on the other. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "paneo_suave"
                }
            ]
        },
        {
            "id": 19,
            "acto": 5,
            "locucion": "La próxima vez que mires el tono de tu piel, no veas una etiqueta. Mira un mapa vivo: el recordatorio de cuántos rayos de sol necesitaron tus ancestros para darte la vida.",
            "palabras_clave": ["mapa vivo", "cuántos rayos de sol", "darte la vida"],
            "planos": [
                {
                    "id_plano": 1,
                    "prompt": "Emotional close up of young boy Niko looking at his open hand bathed in golden sunset light with a gentle, appreciative smile. Messy teal hair, band-aid on cheek, green vest. 2D flat cartoon illustration style, clean lines, flat shading.",
                    "duracion_proporcion": 0.5,
                    "animacion": "flotar_suave"
                },
                {
                    "id_plano": 2,
                    "prompt": "Inspiring wide panoramic scene of diverse children and people of all different skin tones standing together on a hill watching a majestic golden sunrise over planet Earth. 2D flat cartoon illustration style, clean lines, flat shading, vibrant colors.",
                    "duracion_proporcion": 0.5,
                    "animacion": "zoom_in_suave"
                }
            ]
        }
    ]
}

def main():
    ruta = "esquema_maestro.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(episodio_completo, f, indent=2, ensure_ascii=False)
    print(f"✅ Guion de 5 minutos guardado exitosamente en {ruta}")
    print(f"Total escenas: {len(episodio_completo['escenas'])}")
    total_planos = sum(len(e['planos']) for e in episodio_completo['escenas'])
    print(f"Total planos visuales: {total_planos}")

if __name__ == "__main__":
    main()
