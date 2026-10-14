import json
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SCHEMA_TIGHT = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\esquema_maestro_ep2_tight.json"
SCHEMA_TIGHT_TIGHT = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\esquema_maestro_ep2_tight_tight.json"

with open(SCHEMA_TIGHT, "r", encoding="utf-8") as f:
    schema = json.load(f)

with open(SCHEMA_TIGHT_TIGHT, "r", encoding="utf-8") as f:
    schema_tt = json.load(f)

# Extraer palabras de escenas 3 y 4
palabras_escena_3 = schema_tt["escenas"][2]["palabras"]
palabras_escena_4 = schema_tt["escenas"][3]["palabras"]

# Definir los 6 planos dinámicos para Escena 3 (Total: 656 frames = 21.86s)
planos_escena_3 = [
    {
        "id_plano": 1,
        "locucion_plano": "Para entender este misterio, primero tenemos que mirar cómo funciona tu grabadora interna...",
        "palabras_clave_plano": ["grabadora interna", "misterio"],
        "duracion_frames": 105,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p1.png",
        "descripcion": "Niko señalando un holograma amigable del cerebro con un puntero"
    },
    {
        "id_plano": 2,
        "locucion_plano": "...una estructura cerebral con forma de caballito de mar llamada Hipocampo.",
        "palabras_clave_plano": ["Hipocampo", "caballito de mar"],
        "duracion_frames": 100,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p2.png",
        "descripcion": "Hipocampo dorado estilizado con forma de caballito de mar flotando en el cerebro"
    },
    {
        "id_plano": 3,
        "locucion_plano": "Durante todo el día, el hipocampo recibe todo lo que ves, hueles y sientes...",
        "palabras_clave_plano": ["lo que ves", "hueles y sientes"],
        "duracion_frames": 110,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p3.png",
        "descripcion": "Esferas de memoria luminosas con iconos sensoriales fluyendo hacia la consola cerebral"
    },
    {
        "id_plano": 4,
        "locucion_plano": "...y lo va archivando en la memoria a corto plazo...",
        "palabras_clave_plano": ["memoria a corto plazo"],
        "duracion_frames": 115,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p4.png",
        "descripcion": "Archiveros cartoon organizando las esferas de memoria en archivadores futuristas"
    },
    {
        "id_plano": 5,
        "locucion_plano": "...como una cámara de seguridad...",
        "palabras_clave_plano": ["cámara de seguridad"],
        "duracion_frames": 115,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p5.png",
        "descripcion": "Cámara de seguridad retro-futurista con luz roja parpadeante de REC"
    },
    {
        "id_plano": 6,
        "locucion_plano": "...encendida las veinticuatro horas.",
        "palabras_clave_plano": ["veinticuatro horas"],
        "duracion_frames": 111,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p6.png",
        "descripcion": "Niko sonriente haciendo gesto de pulgar arriba junto al monitor de seguridad"
    }
]

# Definir los 7 planos dinámicos para Escena 4 (Total: 788 frames = 26.26s)
planos_escena_4 = [
    {
        "id_plano": 1,
        "locucion_plano": "Pero cuando te metes a la cama, los científicos descubrieron un fenómeno asombroso...",
        "palabras_clave_plano": ["fenómeno asombroso", "te metes a la cama"],
        "duracion_frames": 110,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p1.png",
        "descripcion": "Niko sentado en la cama en pijama mirando al techo bajo la luz de la luna"
    },
    {
        "id_plano": 2,
        "locucion_plano": "...el hipocampo no se duerme al mismo tiempo que el resto del cuerpo.",
        "palabras_clave_plano": ["no se duerme", "resto del cuerpo"],
        "duracion_frames": 115,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p2.png",
        "descripcion": "Corte transversal del cerebro: corteza iluminada y hipocampo apagándose en gris"
    },
    {
        "id_plano": 3,
        "locucion_plano": "Se apaga de cuatro a diez minutos ANTES de que pierdas el conocimiento.",
        "palabras_clave_plano": ["cuatro a diez minutos", "ANTES"],
        "duracion_frames": 120,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p3.png",
        "descripcion": "Temporizador digital marcando 10:00 con un interruptor mecánico cambiando a OFF"
    },
    {
        "id_plano": 4,
        "locucion_plano": "Imagina que una cámara de seguridad deja de grabar...",
        "palabras_clave_plano": ["deja de grabar"],
        "duracion_frames": 110,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p4.png",
        "descripcion": "Lente de la cámara de seguridad donde la luz REC se apaga y la pantalla se apaga"
    },
    {
        "id_plano": 5,
        "locucion_plano": "...mientras las luces de la habitación todavía siguen encendidas.",
        "palabras_clave_plano": ["luces de la habitación", "encendidas"],
        "duracion_frames": 115,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p5.png",
        "descripcion": "Vista amplia de la habitación pacífica con lámpara de noche encendida"
    },
    {
        "id_plano": 6,
        "locucion_plano": "Durante esos minutos finales, estás despierto...",
        "palabras_clave_plano": ["minutos finales", "estás despierto"],
        "duracion_frames": 110,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p6.png",
        "descripcion": "Primer plano de Niko con la cabeza en la almohada y ojos somnolientos"
    },
    {
        "id_plano": 7,
        "locucion_plano": "...pero nadie está guardando el archivo.",
        "palabras_clave_plano": ["nadie está guardando"],
        "duracion_frames": 108,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p7.png",
        "descripcion": "Archivador de memoria con cartel de CERRADO y esferas disolviéndose en polvo de estrellas"
    }
]

# Actualizar Escena 3
schema["escenas"][2]["duracion_frames"] = 656
schema["escenas"][2]["duracion_segundos"] = 21.86
schema["escenas"][2]["archivos_generados"] = {
    "audio_tts": "assets/audio/voz_puck_ep2_escena_3_tight.wav"
}
schema["escenas"][2]["palabras"] = palabras_escena_3
schema["escenas"][2]["planos"] = planos_escena_3

# Actualizar Escena 4
schema["escenas"][3]["duracion_frames"] = 788
schema["escenas"][3]["duracion_segundos"] = 26.26
schema["escenas"][3]["archivos_generados"] = {
    "audio_tts": "assets/audio/voz_puck_ep2_escena_4_tight.wav"
}
schema["escenas"][3]["palabras"] = palabras_escena_4
schema["escenas"][3]["planos"] = planos_escena_4

# Calcular nueva duración total (Escenas 1, 2, 3 y 4)
total_frames = sum(
    e.get("duracion_frames", 0)
    for e in schema["escenas"]
    if e.get("archivos_generados", {}).get("audio_tts") and e.get("duracion_frames", 0) > 0
)
schema["metadata"]["duracion_total_frames"] = total_frames
schema["metadata"]["duracion_total_segundos"] = round(total_frames / 30.0, 2)

with open(SCHEMA_TIGHT, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2, ensure_ascii=False)

print(f"✅ Esquema maestro actualizado: Escenas 1 a 4 listas con {total_frames} frames ({total_frames/30:.2f}s)!")
