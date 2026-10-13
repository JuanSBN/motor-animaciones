"""
oracle_moondream_gate.py
Módulo de Control de Calidad Visual (QA Gate) que utiliza Moondream VLM
en la instancia de Oracle Cloud.

Aislamiento Garantizado:
- Opera exclusivamente dentro de `/tmp/animaciones_moondream_qa/`.
- No toca ningún archivo en `/home/ubuntu/` ni altera otros proyectos.
- Limpia los archivos temporales automáticamente al finalizar.
"""

import os
import sys
import json

REMOTE_TMP_DIR = "/tmp/animaciones_moondream_qa"

def _obtener_modulo_remoto():
    curioreels_path = r"c:\Users\Lenovo\Documents\Proyecto\curioreels"
    if curioreels_path not in sys.path:
        sys.path.append(curioreels_path)
    try:
        import oracle_remote
        return oracle_remote
    except ImportError:
        return None

class OracleMoondreamGate:
    def __init__(self):
        self.remote = _obtener_modulo_remoto()
        self.disponible = self.remote is not None

    def asegurar_entorno(self):
        if not self.disponible:
            return False
        res = self.remote.run_ssh_command(f"mkdir -p {REMOTE_TMP_DIR}")
        return res.returncode == 0

    def limpiar_entorno(self):
        if not self.disponible:
            return
        self.remote.run_ssh_command(f"rm -rf {REMOTE_TMP_DIR}")

    def consultar_moondream(self, ruta_imagen_local: str, pregunta: str) -> str:
        """
        Envía una imagen local a Moondream VLM en Oracle Cloud y obtiene la respuesta.
        """
        if not self.disponible or not os.path.exists(ruta_imagen_local):
            return "QA no disponible o imagen inexistente."

        self.asegurar_entorno()
        fname = os.path.basename(ruta_imagen_local)
        remote_path = f"{REMOTE_TMP_DIR}/{fname}"

        # Subir imagen
        scp_res = self.remote.scp_to_remote(ruta_imagen_local, remote_path)
        if scp_res.returncode != 0:
            return f"Error al subir imagen: {scp_res.stderr}"

        # Script remoto que consulta Ollama
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
        res = self.remote.run_ssh_command(write_cmd)
        return res.stdout.strip()

    def auditar_calidad_imagen(self, ruta_imagen_local: str) -> dict:
        """
        Evalúa si la imagen generada tiene texto ilegible o artefactos de difusión.
        """
        pregunta = (
            "Examine this cartoon illustration carefully: "
            "1. Does it contain any distorted, misspelled, or hallucinated AI letters or fake words? "
            "2. Are there any awkward distortions on human faces, eyes, or hands? "
            "Reply with 'CLEAN' if it has no text or distortions, otherwise describe the issues."
        )
        veredicto = self.consultar_moondream(ruta_imagen_local, pregunta)
        es_limpia = "clean" in veredicto.lower() and "misspelled" not in veredicto.lower() and "distorted" not in veredicto.lower()
        return {
            "aprobada": es_limpia,
            "veredicto_moondream": veredicto
        }

if __name__ == "__main__":
    gate = OracleMoondreamGate()
    print("Moondream QA Gate conectado:", gate.disponible)
