import json

with open("esquema_maestro.json", "r", encoding="utf-8") as f:
    data = json.load(f)

text_triggers = ["label", "text", "word", "percent", "%", "chart", "sign", "title", "dial", "diagram"]
for s in data["escenas"]:
    for p in s.get("planos", []):
        prompt = p["prompt"].lower()
        found = [w for w in text_triggers if w in prompt]
        if found:
            sid = s["id"]
            pid = p["id_plano"]
            print(f"Escena {sid} P{pid} [{found}]: {p['prompt']}")
