import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

d = json.load(open(r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\esquema_maestro_ep2_tight.json", encoding="utf-8"))

for idx, esc in enumerate(d["escenas"][:4]):
    print(f"\n==================== ESCENA {idx+1} ({esc['duracion_frames']}f / {esc['duracion_segundos']}s) ====================")
    curr_f = 0
    planos = esc.get("planos", [])
    palabras = esc.get("palabras", [])
    
    for p in planos:
        p_dur = p["duracion_frames"]
        p_start_f = curr_f
        p_end_f = curr_f + p_dur
        p_start_s = p_start_f / 30.0
        p_end_s = p_end_f / 30.0
        
        words_in_p = [w["w"] for w in palabras if (w["s"] >= p_start_s and w["s"] < p_end_s)]
        
        print(f"\n📸 Plano {p['id_plano']} ({p_dur}f | {p_start_s:.2f}s -> {p_end_s:.2f}s): {p.get('imagen')}")
        print(f"   Locución esperada: \"{p.get('locucion_plano')}\"")
        print(f"   Palabras reales sonando: {' '.join(words_in_p)}")
        curr_f = p_end_f
