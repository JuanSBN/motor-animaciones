import json

path = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\esquema_maestro_ep2.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

planos_escena_2 = [
    {
        "id_plano": 1,
        "locucion_plano": "Si te tropiezas por la calle, tu mente recuerda el tropiezo.",
        "palabras_clave_plano": ["recuerda el tropiezo"],
        "duracion_frames": 120,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_2_p1.png",
        "descripcion": "Niko tropezándose cómicamente con una piedra en la acera"
    },
    {
        "id_plano": 2,
        "locucion_plano": "Si te quemas con una taza caliente, recuerdas el dolor al instante.",
        "palabras_clave_plano": ["taza caliente", "recuerdas el dolor"],
        "duracion_frames": 135,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_2_p2.png",
        "descripcion": "Niko reaccionando cómicamente soplando una taza humeante"
    },
    {
        "id_plano": 3,
        "locucion_plano": "Tu memoria es implacable registrando peligros y errores.",
        "palabras_clave_plano": ["memoria implacable", "peligros y errores"],
        "duracion_frames": 135,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_2_p3.png",
        "descripcion": "Archivo mental con archivadores y esferas de alertas de peligro"
    },
    {
        "id_plano": 4,
        "locucion_plano": "Pero ese puente exacto entre estar despierto y estar inconsciente...",
        "palabras_clave_plano": ["puente exacto", "estar despierto", "inconsciente"],
        "duracion_frames": 160,
        "animacion": "paneo_suave",
        "punch_in": True,
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_2_p4.png",
        "descripcion": "Puente neuronal luminoso cruzando hacia niebla violeta del sueño"
    },
    {
        "id_plano": 5,
        "locucion_plano": "...es el único recuerdo que la evolución te tiene terminantemente prohibido guardar.",
        "palabras_clave_plano": ["único recuerdo", "terminantemente prohibido"],
        "duracion_frames": 174,
        "animacion": "zoom_in_suave",
        "punch_in": True,
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_2_p5.png",
        "descripcion": "Niko al borde del puente mirando al vacío con candado holográfico de prohibición"
    }
]

total_frames_e2 = sum(p["duracion_frames"] for p in planos_escena_2)
data["escenas"][1]["planos"] = planos_escena_2
data["escenas"][1]["duracion_frames"] = total_frames_e2
data["escenas"][1]["duracion_segundos"] = round(total_frames_e2 / 30.0, 2)
data["escenas"][1]["archivos_generados"] = {
    "audio_tts": "assets/audio/voz_puck_ep2_escena_2.wav"
}

total_primer_minuto = data["escenas"][0]["duracion_frames"] + total_frames_e2
print(f"Escena 1: {data['escenas'][0]['duracion_frames']}f ({data['escenas'][0]['duracion_segundos']}s)")
print(f"Escena 2: {total_frames_e2}f ({round(total_frames_e2/30.0, 2)}s)")
print(f"TOTAL PRIMER MINUTO (Acto 1 completo): {total_primer_minuto}f ({round(total_primer_minuto/30.0, 2)}s)")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Actualizado JSON con Escena 2.")
