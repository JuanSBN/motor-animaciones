import json
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SCHEMA_FILE = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\esquema_maestro_ep2_tight.json"

with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
    schema = json.load(f)

# ==========================================
# 1. REPARAR Y SINCRONIZAR ESCENA 1 (1199 frames)
# ==========================================
planos_escena_1 = [
    {
        "id_plano": 1,
        "locucion_plano": "Te ha pasado alguna vez...",
        "palabras_clave_plano": ["alguna vez"],
        "duracion_frames": 62,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p1.png",
        "descripcion": "Niko acostado en la cama con ojos abiertos"
    },
    {
        "id_plano": 2,
        "locucion_plano": "...estás acostado mirando el techo a oscuras...",
        "palabras_clave_plano": ["mirando el techo"],
        "duracion_frames": 94,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_pov_techo.png",
        "descripcion": "POV mirando el techo de la habitación a oscuras"
    },
    {
        "id_plano": 3,
        "locucion_plano": "...escuchas el reloj o el silencio de la casa...",
        "palabras_clave_plano": ["escuchas el reloj"],
        "duracion_frames": 86,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_reloj_noche.png",
        "descripcion": "Reloj digital marcando las horas en la mesita de noche"
    },
    {
        "id_plano": 4,
        "locucion_plano": "...y te dices a ti mismo: Esta noche voy a prestar atención.",
        "palabras_clave_plano": ["prestar atención"],
        "duracion_frames": 107,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p2.png",
        "descripcion": "Niko decidido y concentrado"
    },
    {
        "id_plano": 5,
        "locucion_plano": "Voy a descubrir el segundo exacto en que me duermo.",
        "palabras_clave_plano": ["segundo exacto"],
        "duracion_frames": 93,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_ojos_alerta.png",
        "descripcion": "Primer plano de los ojos de Niko muy abiertos en alerta"
    },
    {
        "id_plano": 6,
        "locucion_plano": "Cierras los ojos...",
        "palabras_clave_plano": ["Cierras los ojos"],
        "duracion_frames": 43,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_cerrando_ojos.png",
        "descripcion": "Detalle de párpados cerrándose lentamente"
    },
    {
        "id_plano": 7,
        "locucion_plano": "...sientes la almohada, respiras hondo...",
        "palabras_clave_plano": ["respiras hondo"],
        "duracion_frames": 75,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p3.png",
        "descripcion": "Niko relajándose en la almohada"
    },
    {
        "id_plano": 8,
        "locucion_plano": "...y de repente suena la alarma!",
        "palabras_clave_plano": ["suena la alarma"],
        "duracion_frames": 71,
        "animacion": "sacudida",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_reloj_sonando.png",
        "descripcion": "Alarma sonando con ondas de sonido vibrantes"
    },
    {
        "id_plano": 9,
        "locucion_plano": "Ya es de día.",
        "palabras_clave_plano": ["es de día"],
        "duracion_frames": 52,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p4.png",
        "descripcion": "Luz de la mañana inundando la habitación y Niko despertando"
    },
    {
        "id_plano": 10,
        "locucion_plano": "Entre las once y media de la noche y las siete de la mañana...",
        "palabras_clave_plano": ["once y media", "siete de la mañana"],
        "duracion_frames": 104,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_cinta_tiempo.png",
        "descripcion": "Línea de tiempo gráfica de 11:30 PM a 7:00 AM con un gran vacío negro"
    },
    {
        "id_plano": 11,
        "locucion_plano": "...hay un vacío absoluto.",
        "palabras_clave_plano": ["vacío absoluto"],
        "duracion_frames": 60,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p5.png",
        "descripcion": "Agujero negro simbólico / cinta rota que representa el tiempo perdido"
    },
    {
        "id_plano": 12,
        "locucion_plano": "No viste venir el sueño, no sentiste el cambio...",
        "palabras_clave_plano": ["no viste venir"],
        "duracion_frames": 75,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_niko_desconcierto.png",
        "descripcion": "Niko desconcertado rascándose la cabeza"
    },
    {
        "id_plano": 13,
        "locucion_plano": "...y no recuerdas nada.",
        "palabras_clave_plano": ["no recuerdas nada"],
        "duracion_frames": 57,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p12_a.png",
        "descripcion": "Signos de interrogación flotando sobre Niko pensativo"
    },
    {
        "id_plano": 14,
        "locucion_plano": "No es que te hayas distraído...",
        "palabras_clave_plano": ["No es que te hayas distraído"],
        "duracion_frames": 90,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_p6.png",
        "descripcion": "Silueta cerebral con engranajes biológicos"
    },
    {
        "id_plano": 15,
        "locucion_plano": "...tu cerebro tiene una orden biológica estricta de borrar ese momento cada noche. ¿Por qué?",
        "palabras_clave_plano": ["orden biológica", "borrar ese momento", "Por qué"],
        "duracion_frames": 130,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_1_candado_zoom.png",
        "descripcion": "Candado cibernético cerrándose con un gran signo de interrogación"
    }
]
schema["escenas"][0]["planos"] = planos_escena_1
schema["escenas"][0]["duracion_frames"] = sum(p["duracion_frames"] for p in planos_escena_1)
assert schema["escenas"][0]["duracion_frames"] == 1199, f"Error suma Escena 1: {schema['escenas'][0]['duracion_frames']}"

# ==========================================
# 2. SINCRONIZAR ESCENA 3 CON WHISPER (656 frames)
# ==========================================
planos_escena_3 = [
    {
        "id_plano": 1,
        "locucion_plano": "Para entender este misterio, primero tenemos que mirar cómo funciona tu grabadora interna...",
        "palabras_clave_plano": ["grabadora interna", "misterio"],
        "duracion_frames": 162,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p1.png",
        "descripcion": "Niko canónico señalando un holograma del cerebro en la biblioteca"
    },
    {
        "id_plano": 2,
        "locucion_plano": "...una estructura cerebral con forma de caballito de mar llamada Hipocampo.",
        "palabras_clave_plano": ["Hipocampo", "caballito de mar"],
        "duracion_frames": 142,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p2.png",
        "descripcion": "Hipocampo dorado estilizado con forma de caballito de mar"
    },
    {
        "id_plano": 3,
        "locucion_plano": "Durante todo el día, el hipocampo recibe todo lo que ves, hueles y sientes...",
        "palabras_clave_plano": ["lo que ves", "hueles y sientes"],
        "duracion_frames": 156,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p3.png",
        "descripcion": "Esferas de memoria luminosas con iconos sensoriales fluyendo hacia la consola"
    },
    {
        "id_plano": 4,
        "locucion_plano": "...y lo va archivando en la memoria a corto plazo...",
        "palabras_clave_plano": ["memoria a corto plazo"],
        "duracion_frames": 80,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p4.png",
        "descripcion": "Archiveros organizando las esferas de memoria en archivadores"
    },
    {
        "id_plano": 5,
        "locucion_plano": "...como una cámara de seguridad encendida las veinticuatro horas.",
        "palabras_clave_plano": ["cámara de seguridad", "veinticuatro horas"],
        "duracion_frames": 116,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_3_p5.png",
        "descripcion": "Cámara de seguridad retro-futurista con luz roja de REC"
    }
]
schema["escenas"][2]["planos"] = planos_escena_3
schema["escenas"][2]["duracion_frames"] = sum(p["duracion_frames"] for p in planos_escena_3)
assert schema["escenas"][2]["duracion_frames"] == 656, f"Error suma Escena 3: {schema['escenas'][2]['duracion_frames']}"

# ==========================================
# 3. SINCRONIZAR ESCENA 4 CON WHISPER (788 frames)
# ==========================================
planos_escena_4 = [
    {
        "id_plano": 1,
        "locucion_plano": "Pero cuando te metes a la cama, los científicos descubrieron un fenómeno asombroso...",
        "palabras_clave_plano": ["fenómeno asombroso", "te metes a la cama"],
        "duracion_frames": 155,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p1.png",
        "descripcion": "Niko acostado en la cama en pijama mirando al techo bajo la luna"
    },
    {
        "id_plano": 2,
        "locucion_plano": "...el hipocampo no se duerme al mismo tiempo que el resto del cuerpo.",
        "palabras_clave_plano": ["no se duerme", "resto del cuerpo"],
        "duracion_frames": 125,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p2.png",
        "descripcion": "Corte transversal del cerebro: corteza iluminada y hipocampo apagándose"
    },
    {
        "id_plano": 3,
        "locucion_plano": "Se apaga de cuatro a diez minutos ANTES de que pierdas el conocimiento.",
        "palabras_clave_plano": ["cuatro a diez minutos", "ANTES"],
        "duracion_frames": 150,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p3.png",
        "descripcion": "Temporizador digital marcando 10:00 con interruptor a OFF"
    },
    {
        "id_plano": 4,
        "locucion_plano": "Imagina que una cámara de seguridad deja de grabar...",
        "palabras_clave_plano": ["deja de grabar"],
        "duracion_frames": 95,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p4.png",
        "descripcion": "Lente de la cámara de seguridad donde la luz REC se apaga"
    },
    {
        "id_plano": 5,
        "locucion_plano": "...mientras las luces de la habitación todavía siguen encendidas.",
        "palabras_clave_plano": ["luces de la habitación", "encendidas"],
        "duracion_frames": 100,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p5.png",
        "descripcion": "Vista amplia de la habitación pacífica con lámpara de noche encendida"
    },
    {
        "id_plano": 6,
        "locucion_plano": "Durante esos minutos finales, estás despierto...",
        "palabras_clave_plano": ["minutos finales", "estás despierto"],
        "duracion_frames": 90,
        "animacion": "paneo_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p6.png",
        "descripcion": "Primer plano de Niko con la cabeza en la almohada y ojos somnolientos"
    },
    {
        "id_plano": 7,
        "locucion_plano": "...pero nadie está guardando el archivo.",
        "palabras_clave_plano": ["nadie está guardando"],
        "duracion_frames": 73,
        "animacion": "zoom_in_suave",
        "tipo_visual": "imagen_flux",
        "imagen": "assets/img/ep2_escena_4_p7.png",
        "descripcion": "Archivador con letrero CLOSED y estrellas disolviéndose"
    }
]
schema["escenas"][3]["planos"] = planos_escena_4
schema["escenas"][3]["duracion_frames"] = sum(p["duracion_frames"] for p in planos_escena_4)
assert schema["escenas"][3]["duracion_frames"] == 788, f"Error suma Escena 4: {schema['escenas'][3]['duracion_frames']}"

total_frames = 1199 + 678 + 656 + 788
schema["metadata"]["duracion_total_frames"] = total_frames
schema["metadata"]["duracion_total_segundos"] = round(total_frames / 30.0, 2)

with open(SCHEMA_FILE, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2, ensure_ascii=False)

print(f"✅ Sincronización perfecta completada: Total {total_frames} frames ({total_frames/30.0:.2f}s)!")
