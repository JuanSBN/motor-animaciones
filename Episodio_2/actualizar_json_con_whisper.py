import json

path = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\esquema_maestro_ep2.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

planos_whisper = [
    {
        "id_plano": 1,
        "locucion_plano": "Seguro te ha pasado alguna vez.",
        "palabras_clave_plano": ["Seguro te ha pasado"],
        "duracion_frames": 63,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p1.png",
        "descripcion": "Niko en la cama de noche mirando arriba pensativo"
    },
    {
        "id_plano": 2,
        "locucion_plano": "Estás acostado, mirando el techo a oscuras.",
        "palabras_clave_plano": ["mirando el techo"],
        "duracion_frames": 111,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_pov_techo.png",
        "descripcion": "POV subjetivo mirando el techo a oscuras con sombras de árboles"
    },
    {
        "id_plano": 3,
        "locucion_plano": "Escuchas el reloj o el silencio de la casa...",
        "palabras_clave_plano": ["Escuchas el reloj"],
        "duracion_frames": 96,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_reloj_noche.png",
        "descripcion": "Macro reloj analógico de noche marcando 11:42 PM"
    },
    {
        "id_plano": 4,
        "locucion_plano": "...y te dices a ti mismo: Esta noche voy a prestar atención.",
        "palabras_clave_plano": ["prestar atención"],
        "duracion_frames": 135,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p2.png",
        "descripcion": "Niko en pijama mirando de reojo al reloj con determinación cómica"
    },
    {
        "id_plano": 5,
        "locucion_plano": "Voy a descubrir el segundo exacto en que me duermo.",
        "palabras_clave_plano": ["segundo exacto"],
        "duracion_frames": 111,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_ojos_alerta.png",
        "descripcion": "Macro ojos de Niko hiper-enfocados en misión secreta"
    },
    {
        "id_plano": 6,
        "locucion_plano": "Cierras los ojos...",
        "palabras_clave_plano": ["Cierras los ojos"],
        "duracion_frames": 69,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_cerrando_ojos.png",
        "descripcion": "Macro párpados cerrándose lentamente en calma"
    },
    {
        "id_plano": 7,
        "locucion_plano": "...sientes la almohada, respiras hondo...",
        "palabras_clave_plano": ["sientes la almohada", "respiras hondo"],
        "duracion_frames": 93,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p3.png",
        "descripcion": "Niko dormido plácidamente en la almohada"
    },
    {
        "id_plano": 8,
        "locucion_plano": "...y de repente suena la alarma!",
        "palabras_clave_plano": ["suena la alarma"],
        "duracion_frames": 84,
        "animacion": "sacudida",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_reloj_sonando.png",
        "descripcion": "Macro alarma roja vibrando violentamente con campanas limpias"
    },
    {
        "id_plano": 9,
        "locucion_plano": "Ya es de día.",
        "palabras_clave_plano": ["Ya es de día"],
        "duracion_frames": 36,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p4.png",
        "descripcion": "Niko sentado sobresaltado en pijama con explosión de sol"
    },
    {
        "id_plano": 10,
        "locucion_plano": "Entre las once y media de la noche y las siete de la mañana...",
        "palabras_clave_plano": ["once y media", "siete de la mañana"],
        "duracion_frames": 120,
        "animacion": "vectorial",
        "tipo_visual": "componente_vectorial",
        "componente": "SleepVoidTimeline",
        "descripcion": "Infografía vectorial nítida en Remotion de la línea temporal 11:30 a 07:00"
    },
    {
        "id_plano": 11,
        "locucion_plano": "...hay un vacío absoluto.",
        "palabras_clave_plano": ["vacío absoluto"],
        "duracion_frames": 63,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p5.png",
        "descripcion": "Niko en pijama al borde de la cama rascándose la cabeza perplejo"
    },
    {
        "id_plano": 12,
        "locucion_plano": "No viste venir el sueño, no sentiste el cambio y no recuerdas nada.",
        "palabras_clave_plano": ["no recuerdas nada"],
        "duracion_frames": 174,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_niko_desconcierto.png",
        "descripcion": "Niko con brazos abiertos desconcertado a cámara"
    },
    {
        "id_plano": 13,
        "locucion_plano": "No es que te hayas distraído: tu cerebro tiene una orden biológica estricta de borrar ese momento cada noche.",
        "palabras_clave_plano": ["orden biológica", "borrar ese momento"],
        "duracion_frames": 225,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p6.png",
        "descripcion": "Niko viendo el holograma del cerebro con candado rojo"
    },
    {
        "id_plano": 14,
        "locucion_plano": "¿Por qué?",
        "palabras_clave_plano": ["Por qué"],
        "duracion_frames": 35,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_candado_zoom.png",
        "descripcion": "Zoom dramático al candado del cerebro con signos ?"
    }
]

total = sum(p["duracion_frames"] for p in planos_whisper)
print(f"Total frames escena 1: {total} ({total/30:.2f}s)")
data["escenas"][0]["planos"] = planos_whisper
data["escenas"][0]["duracion_frames"] = total
data["escenas"][0]["duracion_segundos"] = round(total / 30.0, 2)
data["escenas"][0]["archivos_generados"]["audio_tts"] = "assets/audio/voz_puck_ep2_escena_1.wav"

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ JSON maestro actualizado con alineación 100% precisa de Whisper.")
