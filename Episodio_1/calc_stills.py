import json

with open("esquema_maestro.json", "r", encoding="utf-8") as f:
    data = json.load(f)

accum = 0
targets = [(5, 1), (5, 2), (8, 2), (11, 1)]

for s in data["escenas"]:
    for p in s.get("planos", []):
        dur = p.get("duracion_frames", 30)
        mid = accum + dur // 2
        pair = (s["id"], p["id_plano"])
        if pair in targets:
            print(f"Target Escena {s['id']} Plano {p['id_plano']}: mid frame = {mid}")
        accum += dur
