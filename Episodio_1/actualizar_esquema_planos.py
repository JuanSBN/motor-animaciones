import json

def actualizar_esquema():
    with open("esquema_maestro.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Definir desglose exacto de locución y palabras clave por plano para cada escena
    desglose = {
        1: [
            {
                "id_plano": 1,
                "imagen": "assets/img/flux_16_9_sol_sabana.png",
                "locucion_plano": "Imagina que estamos hace millones de años...",
                "palabras_clave_plano": ["millones de años"],
                "duracion_frames": 108,
                "animacion": "zoom_in_suave"
            },
            {
                "id_plano": 2,
                "imagen": "assets/img/ep1_escena_1_p1.png",
                "locucion_plano": "...bajo un sol abrasador en la sabana africana.",
                "palabras_clave_plano": ["sol abrasador", "sabana africana"],
                "duracion_frames": 108,
                "animacion": "paneo_suave"
            },
            {
                "id_plano": 3,
                "imagen": "assets/img/ep1_escena_1_p2.png",
                "locucion_plano": "Nuestros primeros ancestros enfrentaban un calor implacable.",
                "palabras_clave_plano": ["primeros ancestros", "calor implacable"],
                "duracion_frames": 108,
                "animacion": "zoom_in_suave"
            }
        ],
        2: [
            {
                "id_plano": 1,
                "locucion_plano": "Para sobrevivir y no sobrecalentarse mientras corrían, los homínidos desarrollaron una solución evolutiva única:",
                "palabras_clave_plano": ["sobrecalentarse", "solución evolutiva"],
                "duracion_frames": 144
            },
            {
                "id_plano": 2,
                "locucion_plano": "perdieron casi todo el pelaje y llenaron su piel de glándulas sudoríparas.",
                "palabras_clave_plano": ["perdieron el pelaje", "glándulas sudoríparas"],
                "duracion_frames": 145
            }
        ],
        3: [
            {
                "id_plano": 1,
                "locucion_plano": "Pero sin pelo, la piel quedó totalmente expuesta a un enemigo invisible y destructor:",
                "palabras_clave_plano": ["sin pelo", "enemigo invisible"],
                "duracion_frames": 140
            },
            {
                "id_plano": 2,
                "locucion_plano": "la radiación ultravioleta del sol.",
                "palabras_clave_plano": ["radiación ultravioleta"],
                "duracion_frames": 141
            }
        ],
        4: [
            {
                "id_plano": 1,
                "locucion_plano": "Aquí entró nuestro escudo biológico definitivo: la Melanina.",
                "palabras_clave_plano": ["escudo biológico", "Melanina"],
                "duracion_frames": 116
            },
            {
                "id_plano": 2,
                "locucion_plano": "Una molécula oscura producida por melanocitos...",
                "palabras_clave_plano": ["molécula oscura", "melanocitos"],
                "duracion_frames": 116
            },
            {
                "id_plano": 3,
                "locucion_plano": "...que cubre el ADN como una sombrilla.",
                "palabras_clave_plano": ["cubre el ADN", "sombrilla"],
                "duracion_frames": 99
            }
        ],
        5: [
            {
                "id_plano": 1,
                "locucion_plano": "Durante cientos de miles de años, tener la piel muy oscura fue la armadura perfecta para proteger la vida en el ecuador.",
                "palabras_clave_plano": ["piel muy oscura", "armadura perfecta", "ecuador"],
                "duracion_frames": 165
            },
            {
                "id_plano": 2,
                "locucion_plano": "Pero la historia no terminó ahí...",
                "palabras_clave_plano": ["la historia no terminó ahí"],
                "duracion_frames": 145
            }
        ],
        6: [
            {
                "id_plano": 1,
                "locucion_plano": "Hace unos sesenta mil años, pequeños grupos de exploradores comenzaron el viaje más ambicioso de nuestra especie:",
                "palabras_clave_plano": ["sesenta mil años", "viaje más ambicioso"],
                "duracion_frames": 158
            },
            {
                "id_plano": 2,
                "locucion_plano": "salieron de África rumbo al norte.",
                "palabras_clave_plano": ["rumbo al norte"],
                "duracion_frames": 159
            }
        ],
        7: [
            {
                "id_plano": 1,
                "locucion_plano": "Al llegar a Europa y el norte de Asia, el entorno cambió drásticamente:",
                "palabras_clave_plano": ["Europa", "cambió drásticamente"],
                "duracion_frames": 172
            },
            {
                "id_plano": 2,
                "locucion_plano": "inviernos congelados, días nublados y una radiación solar muchísimo más débil.",
                "palabras_clave_plano": ["inviernos congelados", "radiación más débil"],
                "duracion_frames": 173
            }
        ],
        8: [
            {
                "id_plano": 1,
                "locucion_plano": "Y ahí surgió un nuevo peligro silencioso.",
                "palabras_clave_plano": ["peligro silencioso"],
                "duracion_frames": 150
            },
            {
                "id_plano": 2,
                "locucion_plano": "El cuerpo humano necesita rayos UV para sintetizar un nutriente indispensable para los huesos: la Vitamina D.",
                "palabras_clave_plano": ["rayos UV", "los huesos", "Vitamina D"],
                "duracion_frames": 190
            }
        ],
        9: [
            {
                "id_plano": 1,
                "locucion_plano": "La armadura que antes salvaba vidas en África, en el frío norte se convirtió en una trampa:",
                "palabras_clave_plano": ["armadura", "una trampa"],
                "duracion_frames": 144
            },
            {
                "id_plano": 2,
                "locucion_plano": "bloqueaba la poca luz solar que quedaba.",
                "palabras_clave_plano": ["bloqueaba la poca luz solar"],
                "duracion_frames": 145
            }
        ],
        10: [
            {
                "id_plano": 1,
                "locucion_plano": "La naturaleza tuvo que recalibrar la fórmula.",
                "palabras_clave_plano": ["recalibrar la fórmula"],
                "duracion_frames": 140
            },
            {
                "id_plano": 2,
                "locucion_plano": "Aquellos individuos con mutaciones de menor melanina podían absorber más sol y sobrevivir.",
                "palabras_clave_plano": ["menor melanina", "absorber más sol", "sobrevivir"],
                "duracion_frames": 180
            }
        ],
        11: [
            {
                "id_plano": 1,
                "locucion_plano": "Generación tras generación, la piel en las latitudes altas fue perdiendo pigmento hasta volverse clara...",
                "palabras_clave_plano": ["latitudes altas", "perdiendo pigmento", "piel clara"],
                "duracion_frames": 174
            },
            {
                "id_plano": 2,
                "locucion_plano": "...actuando como una esponja diseñada para atrapar cada rayo de sol.",
                "palabras_clave_plano": ["esponja", "cada rayo de sol"],
                "duracion_frames": 174
            }
        ],
        12: [
            {
                "id_plano": 1,
                "locucion_plano": "El color de piel no fue un capricho ni una jerarquía.",
                "palabras_clave_plano": ["no fue un capricho", "ni una jerarquía"],
                "duracion_frames": 150
            },
            {
                "id_plano": 2,
                "locucion_plano": "Fue un termostato de radiación solar finamente ajustado por la evolución según el lugar del planeta.",
                "palabras_clave_plano": ["termostato de radiación", "ajustado por la evolución"],
                "duracion_frames": 188
            }
        ],
        13: [
            {
                "id_plano": 1,
                "locucion_plano": "Si colocas un mapa de la radiación ultravioleta junto a un mapa de los tonos de piel indígenas tradicionales...",
                "palabras_clave_plano": ["mapa de radiación", "tonos de piel"],
                "duracion_frames": 158
            },
            {
                "id_plano": 2,
                "locucion_plano": "...coinciden como dos piezas de un rompecabezas.",
                "palabras_clave_plano": ["piezas de un rompecabezas"],
                "duracion_frames": 159
            }
        ],
        14: [
            {
                "id_plano": 1,
                "locucion_plano": "Cerca del ecuador: piel rica en melanina para proteger el folato.",
                "palabras_clave_plano": ["ecuador", "melanina", "folato"],
                "duracion_frames": 154
            },
            {
                "id_plano": 2,
                "locucion_plano": "Cerca de los polos: piel clara para absorber vitamina D. Una balanza perfecta.",
                "palabras_clave_plano": ["polos", "piel clara", "vitamina D", "balanza perfecta"],
                "duracion_frames": 154
            }
        ],
        15: [
            {
                "id_plano": 1,
                "locucion_plano": "Incluso hubo excepciones fascinantes, como los pueblos Inuit del Ártico, que mantuvieron la piel más oscura...",
                "palabras_clave_plano": ["excepciones fascinantes", "pueblos Inuit", "Ártico"],
                "duracion_frames": 187
            },
            {
                "id_plano": 2,
                "locucion_plano": "...porque su dieta basada en pescado graso y focas ya les daba toda la vitamina D.",
                "palabras_clave_plano": ["pescado graso", "vitamina D"],
                "duracion_frames": 187
            }
        ],
        16: [
            {
                "id_plano": 1,
                "locucion_plano": "Pero lo más impactante que descubrió la genética moderna es esto:",
                "palabras_clave_plano": ["genética moderna"],
                "duracion_frames": 140
            },
            {
                "id_plano": 2,
                "locucion_plano": "el color de la piel está determinado por apenas un puñado de genes entre más de veinte mil.",
                "palabras_clave_plano": ["un puñado de genes", "veinte mil"],
                "duracion_frames": 183
            }
        ],
        17: [
            {
                "id_plano": 1,
                "locucion_plano": "Científicamente, no existen las razas biológicas.",
                "palabras_clave_plano": ["no existen las razas biológicas"],
                "duracion_frames": 160
            },
            {
                "id_plano": 2,
                "locucion_plano": "Dos personas de piel oscura en África pueden tener más diferencias genéticas entre sí que con una persona de piel clara en Europa.",
                "palabras_clave_plano": ["diferencias genéticas", "África", "Europa"],
                "duracion_frames": 204
            }
        ],
        18: [
            {
                "id_plano": 1,
                "locucion_plano": "Hoy vivimos en casas con techos...",
                "palabras_clave_plano": ["casas con techos"],
                "duracion_frames": 130
            },
            {
                "id_plano": 2,
                "locucion_plano": "volamos en aviones y nos mudamos de continente en horas, confundiendo al viejo termostato de nuestros antepasados.",
                "palabras_clave_plano": ["volamos en aviones", "mudamos de continente", "termostato"],
                "duracion_frames": 167
            }
        ],
        19: [
            {
                "id_plano": 1,
                "locucion_plano": "La próxima vez que mires el tono de tu piel, no veas una etiqueta.",
                "palabras_clave_plano": ["no veas una etiqueta"],
                "duracion_frames": 160
            },
            {
                "id_plano": 2,
                "locucion_plano": "Mira un mapa vivo: el recordatorio de cuántos rayos de sol necesitaron tus ancestros para darte la vida.",
                "palabras_clave_plano": ["mapa vivo", "rayos de sol", "darte la vida"],
                "duracion_frames": 187
            }
        ]
    }

    # Aplicar los desgloses manteniendo la consistencia de duracion_frames total
    for escena in data["escenas"]:
        eid = escena["id"]
        if eid in desglose:
            planos_info = desglose[eid]
            total_frames_scene = escena["duracion_frames"]
            
            # Si se redefinieron planos (como escena 1 con 3 planos)
            if eid == 1:
                escena["planos"] = planos_info
            else:
                for i, p_info in enumerate(planos_info):
                    if i < len(escena["planos"]):
                        escena["planos"][i]["locucion_plano"] = p_info["locucion_plano"]
                        escena["planos"][i]["palabras_clave_plano"] = p_info["palabras_clave_plano"]
                        if "duracion_frames" in p_info:
                            escena["planos"][i]["duracion_frames"] = p_info["duracion_frames"]

            # Asegurar que la suma de planos sea exactamente duracion_frames de la escena
            suma_planos = sum(p["duracion_frames"] for p in escena["planos"])
            diff = total_frames_scene - suma_planos
            if diff != 0:
                escena["planos"][-1]["duracion_frames"] += diff

    with open("esquema_maestro.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ Esquema maestro actualizado con éxito: Subtítulos per-plano sincronizados al 100%!")

if __name__ == "__main__":
    actualizar_esquema()
