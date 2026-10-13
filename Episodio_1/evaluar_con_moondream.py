import sys
import base64
import json
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(r"c:\Users\Lenovo\Documents\Proyecto\curioreels")
import oracle_remote

def test_moondream_image(image_path: str):
    print(f"🔍 Subiendo imagen a Oracle: {image_path}", flush=True)
    remote_path = "/tmp/eval_image.png"
    upload_res = oracle_remote.scp_to_remote(image_path, remote_path)
    if upload_res.returncode != 0:
        print("❌ Error al subir imagen:", upload_res.stderr)
        return

    print("🤖 Ejecutando Moondream QA en Oracle...", flush=True)
    prompt = "Describe this image in detail. Does it show any text, labels, or character design sheets?"

    remote_code = f"""
import urllib.request, json, base64

with open('{remote_path}', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

data = {{
    'model': 'moondream',
    'messages': [
        {{
            'role': 'user',
            'content': {json.dumps(prompt)},
            'images': [b64]
        }}
    ],
    'stream': False
}}
req = urllib.request.Request(
    'http://localhost:11434/api/chat',
    data=json.dumps(data).encode('utf-8'),
    headers={{'Content-Type': 'application/json'}}
)
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw_text = resp.read().decode('utf-8')
        res = json.loads(raw_text)
        print('CHAT RESPONSE:', res.get('message', {{}}).get('content'))
except Exception as e:
    print('ERROR:', e)
"""
    # Write remote script to /tmp/run_moondream.py
    write_cmd = f"cat << 'EOF' > /tmp/run_moondream.py\n{remote_code}\nEOF\npython3 /tmp/run_moondream.py"
    res = oracle_remote.run_ssh_command(write_cmd)
    print("MOONDREAM VERDICT:\n", res.stdout)
    if res.stderr:
        print("STDERR:\n", res.stderr)

if __name__ == "__main__":
    test_moondream_image("assets/img/ep1_escena_3_p2.png")
