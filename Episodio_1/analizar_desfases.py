import json

with open("esquema_maestro.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for s in data["escenas"]:
    dur = s.get("duracion_segundos", 0)
    planos = s.get("planos", [])
    print(f"=== Escena {s['id']} ({dur:.1f}s, {len(planos)} planos) ===")
    print("Locucion:", s["locucion"])
    for p in planos:
        p_dur = p.get("duracion_frames", 0) / 30.0
        print(f"   Plano {p['id_plano']} ({p_dur:.1f}s): {p.get('imagen')} | {p.get('prompt')[:65]}...")
