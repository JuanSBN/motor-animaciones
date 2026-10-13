import os
import sys
import json
import base64
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(r"c:\Users\Lenovo\Documents\Proyecto\curioreels")
import oracle_remote

# Directorio temporal 100% aislado en Oracle (NO toca ningún archivo de otros proyectos)
REMOTE_TMP_DIR = "/tmp/animaciones_moondream_qa"

def preparar_entorno():
    res = oracle_remote.run_ssh_command(f"mkdir -p {REMOTE_TMP_DIR}")
    if res.returncode != 0:
        raise RuntimeError(f"Error preparando Oracle: {res.stderr}")
    print(f"🔒 Entorno aislado en Oracle listo: {REMOTE_TMP_DIR}")

def limpiar_entorno():
    oracle_remote.run_ssh_command(f"rm -rf {REMOTE_TMP_DIR}")
    print("🧹 Entorno temporal en Oracle limpiado con éxito.")

def auditar_imagen_moondream(local_path: str, pregunta: str) -> str:
    fname = os.path.basename(local_path)
    remote_path = f"{REMOTE_TMP_DIR}/{fname}"
    
    # Subir imagen
    scp_res = oracle_remote.scp_to_remote(local_path, remote_path)
    if scp_res.returncode != 0:
        return f"Error SCP: {scp_res.stderr}"

    remote_code = f"""
import urllib.request, json, base64

with open('{remote_path}', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

data = {{
    'model': 'moondream',
    'messages': [
        {{
            'role': 'user',
            'content': {json.dumps(pregunta)},
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
        res = json.loads(resp.read().decode('utf-8'))
        print(res.get('message', {{}}).get('content', ''))
except Exception as e:
    print('ERROR:', e)
"""
    write_cmd = f"cat << 'EOF' > {REMOTE_TMP_DIR}/audit_{fname}.py\n{remote_code}\nEOF\npython3 {REMOTE_TMP_DIR}/audit_{fname}.py"
    res = oracle_remote.run_ssh_command(write_cmd)
    return res.stdout.strip()

def main():
    try:
        preparar_entorno()
        
        casos = [
            {
                "nombre": "Imagen 1 (Escena 13 Plano 2)",
                "ruta": "assets/img/ep1_escena_13_p2.png",
                "pregunta": "Look closely at this image: 1. Are there fake AI letters, gibberish scribbles, or misspelled text on the posters/charts on the wall? 2. Is the boy's face or mouth distorted behind the magnifying glass? Describe any flaws."
            },
            {
                "nombre": "Imagen 2 (Escena 14 Plano 1)",
                "ruta": "assets/img/ep1_escena_14_p1.png",
                "pregunta": "Look closely at the golden balance scale: 1. Is there text or letters on the green shield and golden crystal? 2. What exact letters or words are written on them? Are they misspelled AI words?"
            },
            {
                "nombre": "Imagen 3 (Escena 15 Plano 1)",
                "ruta": "assets/img/ep1_escena_15_p1.png",
                "pregunta": "Describe the man holding the fish: What is his skin color, age, facial hair, and ethnicity? Does he look like an indigenous Inuit person with dark bronze skin, or an elderly fair-skinned person with a grey beard?"
            }
        ]

        for c in casos:
            print(f"\n🔍 Auditando con Moondream en Oracle: {c['nombre']}...")
            res = auditar_imagen_moondream(c["ruta"], c["pregunta"])
            print(f"📋 Resultado Moondream:\n{res}\n" + "-"*50)
            
    finally:
        limpiar_entorno()

if __name__ == "__main__":
    main()
